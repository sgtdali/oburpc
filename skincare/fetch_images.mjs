// Ürün görselleri: marka TR sayfasının kendi ürün görseli (fetch_sources.py > brandSite.image: og:image >
// ld+json Product.image > galeri "packshot"; sayfadaki "benzer ürünler" görselleri karışmasın diye
// genel <img> taraması yapılmaz) -> parfüm tarafıyla aynı ayar (1200px içine, WebP q82)
// -> scripts/skincare/out/images/<slug>.webp (git dışı). push_to_db.mjs bunları Supabase Storage'a
// (images/skincare/<marka>/<slug>.webp) yükler ve ürünün image_url'ini yazar.
//
//   node scripts/skincare/fetch_images.mjs            (eksik olanlar)
//   node scripts/skincare/fetch_images.mjs --force    (hepsini yeniden)
//
// Önce fetch_sources.py çalışmış olmalı (marka sayfası .cache/ içinden okunur).
import fs from "fs";
import path from "path";
import sharp from "sharp";
import { fileURLToPath } from "url";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.join(HERE, "out", "images");
const MAX = 1200;
const WEBP_QUALITY = 82;
const force = process.argv.includes("--force");
const onlyArg = process.argv.find((arg) => arg.startsWith("--only="));
const wanted = onlyArg ? new Set(onlyArg.slice(7).split(",").filter(Boolean)) : null;

// fetch_sources.py > get() ile aynı önbellek dosya adı (parametresiz istek: json.dumps({}) = "{}")
const cacheFile = (url) =>
  path.join(HERE, ".cache", (url + "{}").toLowerCase().replace(/[^a-z0-9]+/g, "_").slice(-150) + ".html");

const unescape = (s) => s.replace(/&amp;/g, "&");

function ogImage(html) {
  const m =
    html.match(/<meta[^>]+property="og:image"[^>]+content="([^"]+)"/i) ||
    html.match(/<meta[^>]+content="([^"]+)"[^>]+property="og:image"/i);
  return m ? unescape(m[1]) : null;
}

/** Büyük sürümü önce dene: CeraVe og:image'da "/sm/..._mobil-" verir ("/lg/..._desktop-" var);
 *  Bioderma (Drupal) "/styles/<boyut>/public/" küçültmesi verir (orijinal dosya bu kısım atılınca). */
const candidates = (src) => {
  const base = src.split("?")[0];
  const lg = base.replace("/sm/", "/lg/").replace("_mobil-", "_desktop-").replace(/-sm(?=\.[a-z]+$)/i, "-lg");
  const original = base.replace(/\/styles\/[^/]+\/public\//, "/");
  return [...new Set([lg, original, base, src])];
};

/** Ürünün kendi görseli: raw/<slug>.json > brandSite.image (fetch_sources.py), yoksa önbellekteki og:image */
function sourceImage(p) {
  const raw = path.join(HERE, "raw", `${p.slug}.json`);
  if (fs.existsSync(raw)) {
    const img = JSON.parse(fs.readFileSync(raw, "utf8")).brandSite?.image;
    if (img) return unescape(img);
  }
  const cached = cacheFile(p.brandUrl);
  return fs.existsSync(cached) ? ogImage(fs.readFileSync(cached, "utf8")) : null;
}

let lastRequest = 0;
async function download(url) {
  const wait = 2500 - (Date.now() - lastRequest);
  if (wait > 0) await new Promise((resolve) => setTimeout(resolve, wait));
  lastRequest = Date.now();
  const res = await fetch(url, { headers: { "User-Agent": "Mozilla/5.0" } });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  const type = res.headers.get("content-type") || "";
  if (!type.startsWith("image/")) throw new Error(`görsel değil: ${type}`);
  return Buffer.from(await res.arrayBuffer());
}

const catalog = JSON.parse(fs.readFileSync(path.join(HERE, "catalog.json"), "utf8"));
if (wanted && (!wanted.size || [...wanted].some((s) => !catalog.products.some((p) => p.slug === s)))) {
  throw new Error("--only: tüm slug'lar catalog.json içinde bulunmalı");
}
fs.mkdirSync(OUT, { recursive: true });
const missing = [];

for (const p of catalog.products) {
  if (wanted && !wanted.has(p.slug)) continue;
  const out = path.join(OUT, `${p.slug}.webp`);
  if (fs.existsSync(out) && !force) continue;
  const og = sourceImage(p);
  if (!og) {
    missing.push(`${p.slug} (görsel bulunamadı)`);
    continue;
  }
  let buf = null;
  let used = null;
  for (const u of candidates(new URL(og, p.brandUrl).href)) {
    try {
      buf = await download(u);
      used = u;
      break;
    } catch {}
  }
  if (!buf) {
    missing.push(`${p.slug} (indirilemedi: ${og})`);
    continue;
  }
  const info = await sharp(buf)
    .rotate()
    .resize({ width: MAX, height: MAX, fit: "inside", withoutEnlargement: true })
    .webp({ quality: WEBP_QUALITY })
    .toFile(out);
  console.log(`${p.slug}: ${info.width}x${info.height}, ${(info.size / 1024).toFixed(0)} KB  <- ${used.split("/").pop()}`);
}

if (missing.length) console.log("EKSİK görsel:", missing);
