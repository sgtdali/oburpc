// Barkod eşlemelerini skincare.product_barcodes'a yaz (uygun-bakim-app barkod tarayıcısı bu tabloyu okur).
//
//   node scripts/skincare/gratis/push_barcodes.mjs [--dry-run]
//
// Kaynaklar (gratis/_out/):
//   brand_gtins.csv  marka sitelerinin ld+json barkodları (brand_gtin.py); iki ürüne düşen barkod atlanır
//   barcodes.csv     Gratis barkodları (stage.py): mevcut ürünler + Gratis'ten eklenen ürünler
// Ürün veritabanında yoksa (henüz aktarılmamış) satır atlanır; tekrar çalıştırmak güvenlidir (var olan barkoda dokunmaz).
// Veritabanı yükünü düşük tutmak için 100'lük parçalarla yazar.
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import dotenv from "dotenv";
import { createClient } from "@supabase/supabase-js";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.join(HERE, "_out");
dotenv.config({ path: path.join(HERE, "..", "..", "..", ".env.local"), quiet: true });
const dryRun = process.argv.includes("--dry-run");

const csv = (name) => {
  const file = path.join(OUT, name);
  if (!fs.existsSync(file)) return [];
  // Python csv çıktısı: virgül içeren alan (ör. varyant adı) çift tırnaklı, tırnak "" ile kaçışlı
  const split = (l) => [...l.matchAll(/(?:^|,)("(?:[^"]|"")*"|[^,]*)/g)].map((m) => m[1].replace(/^"|"$/g, "").replace(/""/g, '"'));
  const [head, ...lines] = fs.readFileSync(file, "utf8").trim().split(/\r?\n/);
  const keys = split(head);
  return lines.map(split).filter((v) => v.length === keys.length)
    .map((v) => Object.fromEntries(keys.map((k, i) => [k, v[i]])));
};

const rows = new Map();
const brand = csv("brand_gtins.csv");
const seen = new Map();
for (const r of brand) seen.set(r.gtin14, (seen.get(r.gtin14) ?? 0) + 1);
for (const r of brand) if (seen.get(r.gtin14) === 1) rows.set(r.gtin14, { slug: r.slug, size: null, url: r.brand_url });
for (const r of csv("barcodes.csv")) if (!rows.has(r.gtin14)) rows.set(r.gtin14, { slug: r.slug, size: r.size || null, url: r.url });

const db = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL, process.env.SUPABASE_SERVICE_ROLE_KEY, {
  db: { schema: "skincare" }, auth: { persistSession: false },
});
const slugs = [...new Set([...rows.values()].map((r) => r.slug))];
const ids = new Map();
for (let i = 0; i < slugs.length; i += 200) {
  const { data, error } = await db.from("products").select("id, slug").in("slug", slugs.slice(i, i + 200));
  if (error) throw error;
  for (const p of data) ids.set(p.slug, p.id);
}
const payload = [...rows].filter(([, r]) => ids.has(r.slug)).map(([gtin, r]) => ({
  gtin, product_id: ids.get(r.slug), size_label: r.size, source_url: r.url,
}));
console.log(`${rows.size} barkod, ${payload.length} tanesinin ürünü veritabanında${dryRun ? " [deneme, yazılmadı]" : ""}`);
if (!dryRun) {
  for (let i = 0; i < payload.length; i += 100) {
    const { error } = await db.from("product_barcodes").upsert(payload.slice(i, i + 100), { onConflict: "gtin", ignoreDuplicates: true });
    if (error) throw error;
  }
  const { count } = await db.from("product_barcodes").select("gtin", { count: "exact", head: true });
  console.log(`yazıldı; tabloda toplam ${count} barkod`);
}
