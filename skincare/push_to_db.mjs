// build_data.py'nin ürettiği scripts/skincare/out/*.json -> Supabase "skincare" şeması.
//
//   node scripts/skincare/push_to_db.mjs            (yaz)
//   node scripts/skincare/push_to_db.mjs --dry-run  (yalnızca denetle ve ne yazılacağını say)
//   node scripts/skincare/push_to_db.mjs --only=slug1,slug2  (seçili ürünleri ekle, mevcut marka/maddeleri koru)
//
// .env.local > SUPABASE_SERVICE_ROLE_KEY ile Supabase API'si üzerinden yazar (doğrudan DATABASE_URL bu ağda
// IPv6 olduğu için çözülemiyor). Slug'a göre upsert eder; tekrar çalıştırmak güvenlidir.
// API'de çok adımlı işlem geri alınamadığı için önce TÜM veri denetlenir (eksik marka/madde varsa hiçbir şey yazılmaz).
// JSON'da olmayan ürünler silinmez, "published = false" yapılır (yanlışlıkla silme olmasın).
// Görseller: out/images/<slug>.webp -> Storage "images" kovası, skincare/<marka>/<slug>.webp (parfüm: images/<marka>/<id>.webp);
// adres sonuna içerik özeti eklenir (?v=...) ki aynı yola yeni görsel yüklenince eski önbellek gösterilmesin.
// Yerelde görseli olmayan ürünün veritabanındaki image_url'i korunur.
// Şema: supabase/skincare-sema.sql — ayrıntı: docs/skincare-veri-kaynaklari.md
import crypto from "crypto";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import dotenv from "dotenv";
import { createClient } from "@supabase/supabase-js";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.join(HERE, "..", "..");
const DATA = path.join(HERE, "out");
dotenv.config({ path: path.join(ROOT, ".env.local"), quiet: true });

const dryRun = process.argv.includes("--dry-run");
const read = (name) => JSON.parse(fs.readFileSync(path.join(DATA, `${name}.json`), "utf8"));
const allBrands = read("brands");
const allProducts = read("products");
const allIngredients = read("ingredients");
// Seçili ürünleri eklerken diğer ürünler ve içerik ilişkileri yeniden yazılmaz; yayından kaldırma yapılmaz.
const onlyArg = process.argv.find((arg) => arg.startsWith("--only="));
const wanted = onlyArg ? new Set(onlyArg.slice(7).split(",").filter(Boolean)) : null;
if (wanted && (!wanted.size || [...wanted].some((slug) => !allProducts.some((p) => p.slug === slug)))) {
  throw new Error("--only: tüm slug'lar üretilen products.json içinde bulunmalı");
}
const products = wanted ? allProducts.filter((p) => wanted.has(p.slug)) : allProducts;
const usedBrands = new Set(products.map((p) => p.brandSlug));
const usedIngredients = new Set(products.flatMap((p) => p.ingredientSlugs));
const brands = wanted ? allBrands.filter((b) => usedBrands.has(b.slug)) : allBrands;
const ingredients = wanted ? allIngredients.filter((i) => usedIngredients.has(i.slug)) : allIngredients;

const { NEXT_PUBLIC_SUPABASE_URL: url, SUPABASE_SERVICE_ROLE_KEY: key } = process.env;
if (!url || !key) {
  console.error(".env.local içinde NEXT_PUBLIC_SUPABASE_URL ve SUPABASE_SERVICE_ROLE_KEY olmalı");
  process.exit(1);
}
const db = createClient(url, key, { db: { schema: "skincare" }, auth: { persistSession: false } });

// Arama metni: lib/skincare/catalog.ts > foldSearch ile aynı kural (küçük harf TR, aksansız, ı -> i)
const foldSearch = (t) => t.toLocaleLowerCase("tr").normalize("NFD").replace(/[\u0300-\u036f]/g, "").replace(/ı/g, "i");
const brandName = new Map(brands.map((b) => [b.slug, b.name]));

async function q(promise, what) {
  const { data, error } = await promise;
  if (error) throw new Error(`${what}: ${error.message}`);
  return data;
}

// 1) Denetim: yazmadan önce
const brandSlugs = new Set(brands.map((b) => b.slug));
const ingSlugs = new Set(ingredients.map((i) => i.slug));
const problems = [];
for (const p of products) {
  if (!brandSlugs.has(p.brandSlug)) problems.push(`${p.slug}: marka yok (${p.brandSlug})`);
  const missing = p.ingredientSlugs.filter((s) => !ingSlugs.has(s));
  if (missing.length) problems.push(`${p.slug}: madde yok (${missing.join(", ")})`);
  if (new Set(p.ingredientSlugs).size !== p.ingredientSlugs.length) problems.push(`${p.slug}: aynı madde iki kez`);
}
if (problems.length) {
  console.error("Denetim başarısız, hiçbir şey yazılmadı:\n  " + problems.join("\n  "));
  process.exit(1);
}

// PostgREST tek yanıtta en fazla 1000 satır döndürür (.limit() bunu aşamaz); büyük tablolar sayfalanarak okunur
async function all(table, cols) {
  const rows = [];
  for (let from = 0; ; from += 1000) {
    const page = await q(db.from(table).select(cols).order("id").range(from, from + 999), `${table} okunamadı`);
    rows.push(...page);
    if (page.length < 1000) return rows;
  }
}

const existing = await all("products", "slug, image_url, published");
const toHide = wanted ? [] : existing.filter((r) => r.published && !products.some((p) => p.slug === r.slug)).map((r) => r.slug);
const oldImage = new Map(existing.map((r) => [r.slug, r.image_url]));
const existingSlugs = new Set(existing.map((r) => r.slug));
const [knownBrands, knownIngredients] = wanted ? await Promise.all([
  all("brands", "slug"),
  all("ingredients", "slug"),
]) : [[], []];
const brandsToWrite = wanted ? brands.filter((b) => !knownBrands.some((r) => r.slug === b.slug)) : brands;
const ingredientsToWrite = wanted ? ingredients.filter((i) => !knownIngredients.some((r) => r.slug === i.slug)) : ingredients;
const IMAGES = path.join(DATA, "images");
const images = products.filter((p) => p.imageFile && fs.existsSync(path.join(IMAGES, p.imageFile)));

if (dryRun) {
  const links = products.reduce((n, p) => n + p.ingredientSlugs.length, 0);
  console.log(`[deneme] denetim tamam, yazılmadı. Yazılacak: ${brandsToWrite.length} marka, ${ingredientsToWrite.length} madde, ` +
    `${products.length} ürün, ${links} ürün-madde bağı, ${images.length} görsel; yayından kalkacak: ${toHide.length}` +
    (wanted ? `; mevcut marka/maddeler korunacak, yeni: ${brandsToWrite.length} marka, ${ingredientsToWrite.length} madde` : ""));
  process.exit(0);
}

// 2) Yazma
// Görseller önce: yükleme başarısız olursa veritabanına hiç dokunulmaz
const imageUrl = new Map();
for (const p of images) {
  const file = fs.readFileSync(path.join(IMAGES, p.imageFile));
  const key = `skincare/${p.brandSlug}/${p.slug}.webp`;
  const { error } = await db.storage.from("images").upload(key, file, {
    contentType: "image/webp", upsert: true, cacheControl: "31536000",
  });
  if (error) throw new Error(`görsel yüklenemedi (${key}): ${error.message}`);
  const v = crypto.createHash("sha1").update(file).digest("hex").slice(0, 10);
  imageUrl.set(p.slug, `${db.storage.from("images").getPublicUrl(key).data.publicUrl}?v=${v}`);
}

if (brandsToWrite.length) await q(db.from("brands").upsert(
  brandsToWrite.map((b) => ({ slug: b.slug, name: b.name, country: b.country, site: b.site })),
  { onConflict: "slug" },
), "markalar");

if (ingredientsToWrite.length) await q(db.from("ingredients").upsert(
  ingredientsToWrite.map((i) => ({
    slug: i.slug, inci: i.inci, name_tr: i.nameTr, function_keys: i.functionKeys, comedogenic: i.comedogenic,
    irritancy: i.irritancy, fungal_acne: i.fungalAcne, tags: i.tags, restrictions: i.restrictions ?? [],
    description: i.description ?? "",
  })),
  { onConflict: "slug" },
), "maddeler");

const brandId = new Map((await all("brands", "id, slug")).map((r) => [r.slug, r.id]));
const ingId = new Map((await all("ingredients", "id, slug")).map((r) => [r.slug, r.id]));

const saved = await q(db.from("products").upsert(
  products.map((p) => ({
    slug: p.slug, brand_id: brandId.get(p.brandSlug), name: p.name, name_tr: p.nameTr, category_slug: p.categorySlug,
    attributes: p.attributes, key_ingredient_groups: p.keyIngredientGroups, benefits: p.benefits, concerns: p.concerns,
    description: p.description ?? "", brand_claims: p.brandClaims, how_to: p.howTo,
    image_url: imageUrl.get(p.slug) ?? oldImage.get(p.slug) ?? null,
    formula_region: p.formulaRegion, sources: p.sources, barcodes: p.barcodes ?? [],
    // Seçili yeni ürünler içerik ilişkileri tamamlandıktan sonra birlikte yayımlanır.
    published: wanted && !existingSlugs.has(p.slug) ? false : true,
    search_text: foldSearch([brandName.get(p.brandSlug), p.name, p.nameTr, ...(p.barcodes ?? [])].filter(Boolean).join(" ")),
  })),
  { onConflict: "slug" },
).select("id, slug"), "ürünler");
const productId = new Map(saved.map((r) => [r.slug, r.id]));

// İçerik listeleri her seferinde baştan yazılır (sıra değişmiş olabilir)
const ids = [...productId.values()];
await q(db.from("product_ingredients").delete().in("product_id", ids), "eski içerik listeleri");
const links = products.flatMap((p) =>
  p.ingredientSlugs.map((s, idx) => ({ product_id: productId.get(p.slug), ingredient_id: ingId.get(s), position: idx + 1 })),
);
await q(db.from("product_ingredients").insert(links), "içerik listeleri");
if (wanted) await q(db.from("products").update({ published: true }).in("id", ids), "seçili ürünleri yayımlama");

if (toHide.length) await q(db.from("products").update({ published: false }).in("slug", toHide), "yayından kaldırma");

console.log(`Supabase skincare: ${brandsToWrite.length} marka, ${ingredientsToWrite.length} madde, ${products.length} ürün, ` +
  `${links.length} ürün-madde bağı, ${imageUrl.size} görsel yazıldı` + (toHide.length ? `; yayından kaldırılan: ${toHide.join(", ")}` : ""));
