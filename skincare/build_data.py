"""Uygulama verisini üret: catalog.json + raw/*.json (fetch_sources.py) + analyze.py + texts_tr.json
-> scripts/skincare/out/{brands,products,ingredients}.json  (sonra: node scripts/skincare/push_to_db.mjs -> Supabase)

    python -X utf8 scripts/skincare/build_data.py

İçerik listesi yalnızca marka TR sitesinden alınır. Türkçe metni eksik ürün/madde varsa
"EKSİK" diye listeler ve açıklamayı boş bırakır. Ayrıntılar: docs/skincare-veri-kaynaklari.md
"""
import datetime, json, os, re
from analyze import Analyzer

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")  # ara çıktı (git dışı); site veriyi Supabase "skincare" şemasından okur


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


VOCAB = os.path.join(HERE, "..", "..", "lib", "skincare", "vocab.ts")


def vocab_keys(name):
    """vocab.ts'deki bir sözlüğün anahtarları (sayfalar karşılığı olmayan anahtarı sessizce atlar; burada yakalanır)."""
    src = open(VOCAB, encoding="utf8").read()
    block = src.split(f"export const {name}")[1].split("\n};")[0]
    return set(re.findall(r'^\s*"?([a-z0-9_\-]+)"?:\s*[{"]', block, re.M))


def check_vocab(products, ingredients):
    used = {
        "KEY_GROUPS": {g for p in products for g in p["keyIngredientGroups"]},
        "BENEFITS": {b["key"] for p in products for b in p["benefits"]},
        "CONCERNS": {c["key"] for p in products for c in p["concerns"]},
        "CATEGORIES": {p["categorySlug"] for p in products},
        "BRAND_CLAIMS": {c for p in products for c in p["brandClaims"]},
        "INGREDIENT_TAGS": {t for i in ingredients for t in i["tags"]},
        "FUNCTIONS": {f for i in ingredients for f in i["functionKeys"]},
    }
    return {f"vocab.ts > {k}": sorted(v - vocab_keys(k)) for k, v in used.items() if v - vocab_keys(k)}


# Marka sayfasındaki beyanlar (TR metin) -> beyan anahtarı (vocab.ts > BRAND_CLAIMS)
CLAIM_PATTERNS = {
    "non-comedogenic": r"(?:komedojenik|komodojenik|komodejonik) (?:değil|olmayan)|gözenekleri tıkamaz",
    "fragrance-free": r"parfüm içermez|parfüm içermeyen",
    "dermatologist-developed": r"dermatologlarla\*? (birlikte )?geliştiril",
}


IMAGES = os.path.join(HERE, "out", "images")


def image_url(product_slug):
    """fetch_images.mjs'in ürettiği yerel WebP'nin dosya adı; push_to_db.mjs bunu Supabase Storage'a yükleyip
    gerçek adresi yazar. Yoksa None (veritabanındaki mevcut görsel korunur)."""
    return f"{product_slug}.webp" if os.path.exists(os.path.join(IMAGES, product_slug + ".webp")) else None


# Durulanan ürün kategorileri: Fulton komedojenlik puanı bu ürünlerde uyarıya dönüşmez (analyze.py > rinse_off).
# lib/skincare/vocab.ts > RINSE_OFF_CATEGORIES ile aynı olmalı.
RINSE_OFF = {"yuz-temizleyici", "peeling", "maske"}


def checked_at(url):
    """Marka sayfasının fetch_sources.py önbelleğine yazıldığı gün (YYYY-MM-DD); önbellek yoksa None.
    Dosya adı fetch_sources.py > get() ile aynı kuralla üretilir (parametresiz istek: "{}")."""
    key = re.sub(r"[^a-z0-9]+", "_", (url + "{}").lower())[-150:]
    path = os.path.join(HERE, ".cache", key + ".html")
    if not os.path.exists(path):
        return None
    return datetime.date.fromtimestamp(os.path.getmtime(path)).isoformat()


def brand_claims(text):
    t = (text or "").lower()
    return [k for k, rx in CLAIM_PATTERNS.items() if re.search(rx, t)]


def main():
    catalog = json.load(open(os.path.join(HERE, "catalog.json"), encoding="utf8"))
    texts = json.load(open(os.path.join(HERE, "texts_tr.json"), encoding="utf8"))
    analyzer = Analyzer()
    ingredients, products = {}, []
    missing = {"ürün metni": [], "madde metni": [], "tanınmayan madde": [], "kaynak": []}

    for p in catalog["products"]:
        path = os.path.join(HERE, "raw", p["slug"] + ".json")
        if not os.path.exists(path):
            missing["kaynak"].append(p["slug"])
            continue
        raw = json.load(open(path, encoding="utf8"))
        site = raw["brandSite"]
        inci = site["inci"]
        if not inci:
            missing["kaynak"].append(f'{p["slug"]} (marka sayfasında içerik listesi bulunamadı)')
            continue
        region = p.get("formulaRegion", "Türkiye")  # kaynak bölgesi açıkça korunur
        sunscreen = p["category"] == "gunes-koruyucu" or bool(re.search(r"(?i)\bspf\s*\d", p["name"]))
        result = analyzer.analyze(inci, rinse_off=p["category"] in RINSE_OFF, sunscreen=sunscreen)
        missing["tanınmayan madde"] += [f'{p["slug"]}: {u}' for u in result["unknown"]]

        slugs = []
        for item in result["ingredients"]:
            kb = item["kb"]
            inci_name = kb["inci"] if kb else item["raw"].upper()
            s = slug(inci_name)
            if s in slugs:  # aynı maddeye düşen iki etiket adı (Avène: termal su + su): ilk sıradaki kalır
                continue
            slugs.append(s)
            if s in ingredients:
                continue
            t = texts["ingredients"].get(s)
            if not t or not t.get("nameTr"):  # içerik listesinde kalın satır Türkçe addır
                missing["madde metni"].append(f"{s} ({inci_name})")
            ingredients[s] = {
                "slug": s, "inci": inci_name,
                "nameTr": t["nameTr"] if t else None,
                "functionKeys": [slug(f) for f in (kb["functions"] if kb else [])],
                "comedogenic": kb["comedogenic"] if kb else None,
                "irritancy": kb["irritancy"] if kb else None,
                "fungalAcne": kb["fungalAcne"] if kb else None,
                "tags": item["tags"],
                "restrictions": [{"annex": r["annex"], "maxConcentration": r["maxConcentration"],
                                  "conditional": r.get("conditional", False)} for r in (kb["restrictions"] if kb else [])],
                "description": t["description"] if t else "",
            }

        if p["slug"] not in texts["products"]:
            missing["ürün metni"].append(p["slug"])
        # Gratis'ten eklenen ürünlerde içerik listesi Gratis ürün sayfasından (scripts/skincare/gratis/stage.py)
        # Global (İngilizce) marka sitesinden alınan formülde etiket bunu söyler (Some By Mi; 2026-11-13).
        label = ("Gratis (Türkiye)" if site.get("inciSource") == "gratis"
                 else "Marka sitesi (Global)" if region == "Global" else "Marka sitesi (Türkiye)")
        sources = [{"label": label, "url": site["url"]}]
        checked = checked_at(site["url"])
        if checked:  # içerik listesinin marka sitesinden en son çekildiği gün (ürün sayfasında gösterilir)
            sources[0]["checkedAt"] = checked
        for field in ("inciUrl", "imageUrl"):
            if site.get(field) and not any(s["url"] == site[field] for s in sources):
                label = "NAOS Stars (Türkiye)" if "naosstars.com/" in site[field] else ("Marka resmî sitesi (AB)" if "neutrogena.de/" in site[field] else "Ask.NAOS (Türkiye)")
                sources.append({"label": label, "url": site[field]})
        sources.extend(p.get("verificationSources", []))
        products.append({
            "slug": p["slug"], "brandSlug": p["brand"], "name": p["name"],
            # catalog.json'daki elle yazılmış ad önceliklidir (marka sitelerinde büyük harf / İngilizce olabiliyor)
            "nameTr": p.get("nameTr") or site.get("nameTr"),
            "categorySlug": p["category"],
            "ingredientSlugs": slugs,
            "attributes": result["attributes"],
            "keyIngredientGroups": result["keyIngredientGroups"],
            "benefits": result["benefits"],
            "concerns": result["concerns"],
            "description": texts["products"].get(p["slug"], ""),
            "brandClaims": brand_claims(site.get("claims")),
            "howTo": site.get("howTo") or [],
            "imageFile": image_url(p["slug"]),
            "formulaRegion": region,
            "sources": sources,
            "barcodes": list(dict.fromkeys((p.get("barcodes") or []) + (site.get("barcodes") or []))),
        })

    brands = [{"slug": b["slug"], "name": b["name"], "country": b.get("country"), "site": b.get("site")}
              for b in catalog["brands"]]
    os.makedirs(OUT, exist_ok=True)
    for name, data in [("brands", brands), ("products", products), ("ingredients", list(ingredients.values()))]:
        json.dump(data, open(os.path.join(OUT, name + ".json"), "w", encoding="utf8"), ensure_ascii=False, indent=2)
    print(f"{len(brands)} marka, {len(products)} ürün, {len(ingredients)} madde -> scripts/skincare/out/ (Supabase'e yazmak için: node scripts/skincare/push_to_db.mjs)")
    missing.update(check_vocab(products, list(ingredients.values())))
    for k, v in missing.items():
        if v:
            print(f"EKSİK {k}: {v}")


if __name__ == "__main__":
    main()
