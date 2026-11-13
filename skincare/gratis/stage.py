"""Gratis taramasından (crawl.py) marka hazırlık klasörleri üret: scripts/skincare/staging/<marka>/.

    python -X utf8 scripts/skincare/gratis/stage.py [--dry-run]

Kullanıcı kararı (2026-11-10): barkodla okutulan Gratis ürününün içeriği yorumlanabilsin diye içerik listesi
Gratis ürün sayfasından alınır (kaynak etiketi "Gratis"), görsel Gratis'in ürün görselidir; ürünler Türkçe
metinleri yazılınca yayımlanır. İçerik listesi olmayan ürünler eklenmez (yorumlanamaz).

- Aynı markada aynı ad (boy hariç) + aynı içerik listesi = tek ürün; her boyun barkodu ayrı kaydedilir.
- Katalogda zaten olan ürün (marka sitesindeki barkodu Gratis barkoduyla aynı, gratis/_out/brand_gtins.csv)
  yeni ürün olarak eklenmez, yalnızca barkodu kaydedilir. Mevcut markalarda match.py'nin "high"/"review"
  adayları da eklenmez; review.csv'ye yazılır (elle bakılır).
- Kapsam dışı (staging/BRIEF.md): set/kit/çoklu paket, BB/CC krem, güneş sonrası, kategorisi belirsiz ürünler.

Çıktı: staging/<marka>/{products.json, excluded.json, raw/<slug>.json}, gratis/_out/{barcodes.csv, review.csv,
brands.json}. texts.json ve synonyms.json'u metin ajanları yazar (staging/BRIEF.md + staging/GRATIS.md).
"""
import csv, glob, json, os, re, sys, unicodedata
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
SK = os.path.dirname(HERE)
sys.path.insert(0, SK)
sys.path.insert(0, HERE)
import source_common as sc  # noqa: E402

OUT = os.path.join(HERE, "_out")
STAGING = os.path.join(SK, "staging")
dry = "--dry-run" in sys.argv

TR = str.maketrans("çğıöşüÇĞİÖŞÜâîû", "cgiosuCGIOSUaiu")
slugify = lambda s: re.sub(r"[^a-z0-9]+", "-", s.translate(TR).lower()).strip("-")
# Gratis'teki yazımı katalogdaki marka slug'ına bağla (mevcut markalar)
BRAND_SLUGS = {"nivea": "nivea", "loreal-paris": "loreal-paris", "l-oreal-paris": "loreal-paris", "sinoz": "sinoz",
               "the-purest-solutions": "the-purest-solutions", "maruderm": "maruderm", "neutrogena": "neutrogena"}
EXCLUDE = [
    # "+" tek başına değil: "SPF50+", "Niacinamide + Panthenol" ürün adıdır; "50 ml + 20 ml" pakettir
    (r"(?i)\b(set|seti|kit|kiti|ikili|üçlü)\b|\d+\s*'\s*l[ıiuü]\b|\d\s*(ml|g|gr)\s*\+", "set / çoklu paket"),
    (r"(?i)\b(bb|cc)\s*(krem|cream)", "BB/CC krem (makyaj)"),
    (r"(?i)güneş sonrası|after sun", "güneş sonrası"),
    (r"(?i)\b(saç|şampuan|deodorant)\b", "saç / deodorant"),
]


def cache_html(url):
    key = re.sub(r"[^a-z0-9]+", "_", (url + "{}").lower())[-150:]
    path = os.path.join(sc.CACHE, key + ".html")
    return open(path, encoding="utf8").read() if os.path.exists(path) else ""


def image(url):
    for m in re.finditer(r'<script[^>]*application/ld\+json[^>]*>(.*?)</script>', cache_html(url), re.S):
        try:
            d = json.loads(m.group(1))
        except ValueError:
            continue
        if d.get("@type") == "Product":
            img = d.get("image")
            return img[0] if isinstance(img, list) else img
    return None


def inci_list(text):
    # Liste sonuna yapışan beyanları kes: "TOCOPHEROL. • DERMATOLOGICALLY TESTED • VEGAN"
    text = re.split(r"\s•\s|\.\s+(?=[A-ZÇĞİÖŞÜa-zçğıöşü]{3,}\s)", text)[0]
    # Türkçe klavyede yazılmış INCI: "İllicium" -> "ILLICIUM" ("İ".upper() Latin I değildir)
    text = text.replace("İ", "I").replace("ı", "i")
    return [x.upper() for x in sc.split_inci(sc.clean_text(text))]


def base_name(name, brand):
    # "Cı̇lt" gibi birleşik noktalı harfler (Gratis yazımı) ve boy bilgisi ("30 ml", "2 ml x 30") ad/slug'a girmesin
    n = "".join(c for c in unicodedata.normalize("NFC", name) if not unicodedata.combining(c))
    n = re.sub(r"^\s*" + re.escape(brand) + r"\s+", "", n, flags=re.I)
    n = re.sub(r"\s*\b\d+([.,]\d+)?\s*(ml|g|gr|mg|adet|oz)\b\.?(\s*x\s*\d*)?", "", n, flags=re.I)
    n = re.sub(r"\(\s*\)", "", n)
    return re.sub(r"\s+", " ", n).strip(" -–,x")


def gratis_inci(url):
    """Önbellekteki Gratis sayfasından içerik listesi (tools.py check aynı listeyi yeniden üretir)."""
    import crawl
    r = crawl.parse(url, cache_html(url))
    return inci_list(r["inci"]) if r["inci"] else None


def gtin14(g):
    return g.zfill(14) if g and g.isdigit() else None


def main():
    rows = [json.loads(l) for f in sorted(glob.glob(os.path.join(OUT, "products-*.jsonl"))) for l in open(f, encoding="utf8")]
    brand_gtin = {r["gtin14"]: r["slug"] for r in csv.DictReader(open(os.path.join(OUT, "brand_gtins.csv"), encoding="utf8"))}
    dup = {g for g in brand_gtin if list(brand_gtin.values()).count(brand_gtin[g]) > 1}
    matches = {r["gtin14"]: r for r in csv.DictReader(open(os.path.join(OUT, "matches.csv"), encoding="utf8"))}
    cat = json.load(open(os.path.join(SK, "catalog.json"), encoding="utf8"))
    existing_brands = {b["slug"] for b in cat["brands"]}

    barcodes, review, groups = [], [], defaultdict(list)
    excluded = defaultdict(list)
    brands = {}
    for r in rows:
        g = gtin14(r["gtin"])
        bslug = BRAND_SLUGS.get(slugify(r["brand"] or ""), slugify(r["brand"] or ""))
        if g in brand_gtin and g not in dup:  # katalogda zaten var: yalnızca barkod
            barcodes.append({"gtin14": g, "slug": brand_gtin[g], "size": r["size"], "url": r["url"], "basis": "marka sitesi barkodu"})
            continue
        if not r["inci"]:
            continue
        name = base_name(r["name"], r["brand"])
        why = next((w for rx, w in EXCLUDE if re.search(rx, r["name"])), None) or (None if r["category"] else "kategori belirsiz")
        if why:
            excluded[bslug].append({"url": r["url"], "name": r["name"], "reason": why})
            continue
        m = matches.get(g)
        if bslug in existing_brands and m and m["confidence"] in ("high", "review"):
            review.append({**{k: m[k] for k in ("confidence", "gtin14", "gratis_name", "our_slug", "score", "reason")}, "url": r["url"]})
            continue
        inci = inci_list(r["inci"])
        brands[bslug] = r["brand"]
        groups[(bslug, slugify(name), tuple(inci))].append((r, g, name, inci))

    per_brand = defaultdict(list)
    used = set()
    for (bslug, nkey, _), items in groups.items():
        r, g, name, inci = max(items, key=lambda x: bool(image(x[0]["url"])))
        slug = f"{bslug}-{nkey}"[:90].rstrip("-")
        n = 2
        while slug in used:  # aynı ad, farklı formül (içerik listesi farklı)
            slug, n = f"{bslug}-{nkey}-{n}"[:90], n + 1
        used.add(slug)
        per_brand[bslug].append({"product": {"slug": slug, "brand": bslug, "name": name, "nameTr": name,
                                             "category": r["category"], "brandUrl": r["url"]},
                                 "raw": {"slug": slug, "brandSite": {"url": r["url"], "nameTr": name, "inci": inci,
                                                                     "inciSource": "gratis", "claims": None, "howTo": [],
                                                                     "image": image(r["url"]), "title": r["name"]}}})
        for it in items:
            if it[1]:
                barcodes.append({"gtin14": it[1], "slug": slug, "size": it[0]["size"], "url": it[0]["url"], "basis": "gratis"})

    if not dry:
        for bslug, items in per_brand.items():
            d = os.path.join(STAGING, bslug)
            os.makedirs(os.path.join(d, "raw"), exist_ok=True)
            json.dump([x["product"] for x in items], open(os.path.join(d, "products.json"), "w", encoding="utf8"), ensure_ascii=False, indent=2)
            json.dump(excluded.get(bslug, []), open(os.path.join(d, "excluded.json"), "w", encoding="utf8"), ensure_ascii=False, indent=2)
            for x in items:
                json.dump(x["raw"], open(os.path.join(d, "raw", x["product"]["slug"] + ".json"), "w", encoding="utf8"), ensure_ascii=False, indent=1)
        with open(os.path.join(OUT, "barcodes.csv"), "w", encoding="utf8", newline="") as f:
            w = csv.DictWriter(f, ["gtin14", "slug", "size", "url", "basis"]); w.writeheader(); w.writerows(barcodes)
        with open(os.path.join(OUT, "review.csv"), "w", encoding="utf8", newline="") as f:
            w = csv.DictWriter(f, ["confidence", "gtin14", "gratis_name", "our_slug", "score", "reason", "url"]); w.writeheader(); w.writerows(review)
        json.dump({k: v for k, v in brands.items() if k not in existing_brands}, open(os.path.join(OUT, "brands.json"), "w", encoding="utf8"), ensure_ascii=False, indent=2)

    total = sum(len(v) for v in per_brand.values())
    print(f"{'[deneme] ' if dry else ''}{total} yeni ürün, {len(per_brand)} marka ({len(set(per_brand) - existing_brands)} yeni); "
          f"{len(barcodes)} barkod ({sum(b['basis'] != 'gratis' for b in barcodes)} mevcut ürüne); "
          f"{sum(len(v) for v in excluded.values())} elendi; {len(review)} elle bakılacak; "
          f"görselsiz: {sum(1 for v in per_brand.values() for x in v if not x['raw']['brandSite']['image'])}")
    for b, v in sorted(per_brand.items(), key=lambda x: -len(x[1]))[:15]:
        print(f"  {b}: {len(v)}")


if __name__ == "__main__":
    main()
