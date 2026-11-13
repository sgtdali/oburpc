"""Paralel ürün ekleme için hazırlık aracı (agy ajanları kullanır; birleştirme/aktarma denetçide).

Her ajan YALNIZCA scripts/skincare/staging/<marka>/ altına yazar. catalog.json, texts_tr.json, analyze.py,
fetch_sources.py, raw/, out/ ve veritabanı denetçiye aittir.

    python -X utf8 scripts/skincare/staging/tools.py fetch <marka> <slug> <url>   # sayfayı çek -> staging/<marka>/raw/<slug>.json + özet
    python -X utf8 scripts/skincare/staging/tools.py summary <marka> [slug]       # analiz özeti (metin yazmak için)
    python -X utf8 scripts/skincare/staging/tools.py ingredients <marka>          # metni yazılacak maddeler + CosIng işlevleri
    python -X utf8 scripts/skincare/staging/tools.py check <marka>                # teslim denetimi (HATA kalmamalı)

Hazırlık klasörü dosyaları (staging/<marka>/):
  products.json   [{"slug","brand","name","nameTr","category","brandUrl"[, "imageUrl"]}]  -> catalog.json'a eklenecek
  excluded.json   [{"url","name","reason"}]                                                -> kapsam dışı / elenen
  texts.json      {"products": {slug: açıklama}, "ingredients": {madde-slug: {"nameTr","description"}}}
  synonyms.json   {"SİTEDEKİ HATALI AD": "COSING ADI"}   (yalnızca bariz yazım hataları; report.md'de gerekçe)
  raw/<slug>.json fetch komutunun çıktısı (elle yazılmaz)
  report.md       özet, elenenler, veri sorunları, SORU'lar
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SK = os.path.dirname(HERE)
sys.path.insert(0, SK)
os.chdir(SK)  # analyze.py kb yolunu göreli açabilir

import fetch_sources as fs  # noqa: E402
import analyze as an  # noqa: E402

slugify = lambda s: re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def prose(item):
    """Liste öğesine düz yazı (tanıtım metni) karışmış mı? Uzun ama BÜYÜK HARFLİ parantezli INCI adları
    ("CARTHAMUS TINCTORIUS (SAFFLOWER) SEED OIL (CARTHAMUS TINCTORIUS SEED OIL)") meşrudur."""
    return len(item) > 70 and (bool(re.search(r"[a-zçğıöşü]{3,}", item)) or bool(re.search(r"[.:!?]\s", item)))
load = lambda p, d=None: json.load(open(p, encoding="utf8")) if os.path.exists(p) else d


def bdir(brand):
    d = os.path.join(HERE, brand)
    os.makedirs(os.path.join(d, "raw"), exist_ok=True)
    return d


def catalog():
    return load(os.path.join(SK, "catalog.json"))


def texts():
    return load(os.path.join(SK, "texts_tr.json"))


def categories():
    src = open(os.path.join(SK, "..", "..", "lib", "skincare", "vocab.ts"), encoding="utf8").read()
    block = src.split("export const CATEGORIES")[1].split("\n};")[0]
    return set(re.findall(r'^\s*"?([a-z0-9\-]+)"?:\s*\{', block, re.M))


def analyzer(brand):
    an.SYNONYMS.update(load(os.path.join(bdir(brand), "synonyms.json"), {}))
    return an.Analyzer()


def fetch(brand, slug, url):
    b = fs.brand_page(url)
    json.dump({"slug": slug, "brandSite": b}, open(os.path.join(bdir(brand), "raw", slug + ".json"), "w", encoding="utf8"),
              ensure_ascii=False, indent=1)
    print(f"{slug}: {len(b['inci'] or [])} madde ({b['inciSource']}), görsel {'var' if b['image'] else 'YOK'} | {b['nameTr']}")
    print("  görsel:", b["image"])
    if not b["inci"]:
        print("  EKSİK: içerik listesi çıkarılamadı (elle yazma; report.md'ye yaz / SORU sor)")
    else:
        print("  INCI:", ", ".join(b["inci"]))
        long = [x for x in b["inci"] if prose(x)]
        if long:
            print("  ŞÜPHELİ (öğede düz yazı var; liste dışı metin karışmış olabilir):", long)


def summary(brand, only=None):
    a = analyzer(brand)
    t = texts()
    for p in load(os.path.join(bdir(brand), "products.json"), []):
        if only and p["slug"] != only:
            continue
        raw = load(os.path.join(bdir(brand), "raw", p["slug"] + ".json"))
        if not raw or not raw["brandSite"]["inci"]:
            print(f"## {p['slug']}: raw yok / INCI yok"); continue
        b = raw["brandSite"]
        r = a.analyze(b["inci"], rinse_off=p["category"] in {"yuz-temizleyici", "peeling", "maske"})
        print(f"## {p['slug']} | {p.get('nameTr')} | {p['category']}")
        print("INCI:", ", ".join(b["inci"]))
        print("İÇERİR:", [(x["key"], x.get("ingredients")) for x in r["attributes"] if not x["ok"]])
        print("İÇERMEZ:", [x["key"] for x in r["attributes"] if x["ok"]])
        print("AKTİF:", r["keyIngredientGroups"], "| FAYDA:", [x["key"] for x in r["benefits"]],
              "| ENDİŞE:", [x["key"] for x in r["concerns"]])
        print("TANINMAYAN:", r["unknown"])
        new = [slugify(i["kb"]["inci"]) for i in r["ingredients"] if i["kb"] and slugify(i["kb"]["inci"]) not in t["ingredients"]]
        print("METNİ YOK (yeni madde):", sorted(set(new)))
        print("SAYFA METNİ (beyan/tanıtım, yalnızca tutarlılık kontrolü için; kopyalanmaz):", (b.get("claims") or "")[:600])
        print()


def ingredients(brand):
    """Metni yazılacak (katalogda metni olmayan) maddeler: CosIng işlevleri, sınıflar, Fulton puanları ve hangi ürünlerde
    geçtiği. Madde metnini bu bilgilere dayanarak yaz; burada olmayan bir özelliği (köken, etki) uydurma."""
    a = analyzer(brand)
    t = texts()
    tx = load(os.path.join(bdir(brand), "texts.json"), {"products": {}, "ingredients": {}})
    need = {}
    for p in load(os.path.join(bdir(brand), "products.json"), []):
        raw = load(os.path.join(bdir(brand), "raw", p["slug"] + ".json"))
        if not raw or not raw["brandSite"]["inci"]:
            continue
        for i in a.analyze(raw["brandSite"]["inci"])["ingredients"]:
            if i["kb"]:
                s = slugify(i["kb"]["inci"])
                if s not in t["ingredients"]:
                    need.setdefault(s, {"kb": i["kb"], "tags": i["tags"], "products": []})["products"].append(p["slug"])
    for s, v in sorted(need.items()):
        k = v["kb"]
        mine = tx["ingredients"].get(s)
        print(f"{s} | INCI: {k['inci']} | işlev: {', '.join(k['functions']) or '-'} | sınıf: {', '.join(k['classes']) or '-'}"
              f" | komedojenlik {k['comedogenic']} tahriş {k['irritancy']} | ürün: {len(v['products'])}"
              f" | mevcut metin: {'VAR' if mine else 'YOK'}")


def check(brand):
    d = bdir(brand)
    errs, warns = [], []
    prods = load(os.path.join(d, "products.json"), [])
    tx = load(os.path.join(d, "texts.json"), {"products": {}, "ingredients": {}})
    cat, t, cats = catalog(), texts(), categories()
    existing = {p["slug"] for p in cat["products"]}
    existing_urls = {p["brandUrl"].rstrip("/") for p in cat["products"]}
    a = analyzer(brand)
    seen = set()
    need_ing = set()
    for p in prods:
        s = p.get("slug", "")
        for k in ("slug", "brand", "name", "nameTr", "category", "brandUrl"):
            if not p.get(k):
                errs.append(f"{s}: '{k}' boş")
        if p.get("brand") != brand:
            errs.append(f"{s}: brand '{p.get('brand')}' != '{brand}'")
        if not s.startswith(brand + "-") or s != slugify(s):
            errs.append(f"{s}: slug '<marka>-<ambalaj adı>' biçiminde, küçük harf ve tire olmalı")
        if s in existing:
            errs.append(f"{s}: zaten katalogda")
        if p.get("brandUrl", "").rstrip("/") in existing_urls:
            errs.append(f"{s}: bu URL zaten katalogda")
        if s in seen:
            errs.append(f"{s}: tekrar eden slug")
        seen.add(s)
        if p.get("category") not in cats:
            errs.append(f"{s}: kategori '{p.get('category')}' geçersiz; izinli: {sorted(cats)}")
        raw = load(os.path.join(d, "raw", s + ".json"))
        if not raw or not raw["brandSite"].get("inci"):
            errs.append(f"{s}: raw/INCI yok (fetch çalıştır)"); continue
        r = a.analyze(raw["brandSite"]["inci"])
        if r["unknown"]:
            errs.append(f"{s}: tanınmayan madde {r['unknown']}")
        if any(prose(x) for x in raw["brandSite"]["inci"]):
            errs.append(f"{s}: INCI öğesinde düz yazı var (liste dışı metin?)")
        if raw["brandSite"].get("url") and raw["brandSite"]["url"].rstrip("/") != p.get("brandUrl", "").rstrip("/"):
            errs.append(f"{s}: raw dosyası başka bir sayfadan ({raw['brandSite']['url']})")
        if not tx["products"].get(s):
            errs.append(f"{s}: ürün açıklaması yok (texts.json > products)")
        else:
            desc = tx["products"][s]
            if re.search(r"(?i)marka(nın|ya göre)?\b[^.]{0,60}(diyor|belirtiyor|beyan)", desc) and re.search(
                    r"(?i)komedojen|parfüm|alkol|paraben|koruyucu|dermatolog", desc):
                errs.append(f"{s}: açıklamada etiket konusunda marka beyanı aktarılıyor (kural 9)")
            if len(desc) < 200:
                warns.append(f"{s}: açıklama kısa ({len(desc)} karakter)")
        if not raw["brandSite"].get("image") and not p.get("imageUrl"):
            warns.append(f"{s}: görsel adresi yok")
        for i in r["ingredients"]:
            if i["kb"]:
                need_ing.add(slugify(i["kb"]["inci"]))
    for s in sorted(need_ing):
        if s not in t["ingredients"]:
            v = tx["ingredients"].get(s)
            if not v or not v.get("nameTr") or not v.get("description"):
                errs.append(f"madde metni yok: {s}")
    for s in tx["products"]:
        if s not in seen:
            warns.append(f"texts.json'da products.json'da olmayan ürün: {s}")
    # Ham liste kaynaktakiyle aynı olmalı (elle düzeltme yasak; önbellekten okunur, siteye yeni istek atmaz)
    for p in prods:
        raw = load(os.path.join(d, "raw", p["slug"] + ".json"))
        if raw and raw["brandSite"].get("inci"):
            try:
                if raw["brandSite"].get("inciSource") == "gratis":  # Gratis ürünü (scripts/skincare/gratis/stage.py)
                    sys.path.insert(0, os.path.join(SK, "gratis"))
                    import stage
                    fresh = stage.gratis_inci(p["brandUrl"])
                else:
                    fresh = fs.brand_page(p["brandUrl"])["inci"]
            except Exception as e:  # noqa: BLE001
                warns.append(f"{p['slug']}: kaynak yeniden okunamadı ({e})"); continue
            if fresh != raw["brandSite"]["inci"]:
                errs.append(f"{p['slug']}: raw içerik listesi kaynaktan farklı — elle düzeltme yasak, `fetch` ile yeniden çek")
    # Şablon metin yasak: her açıklama o ürüne/maddeye özgü yazılmalı
    sents = {}
    for s, v in tx["products"].items():
        for sent in re.split(r"(?<=[.!?])\s+", v):
            key = re.sub(r"\s+", " ", re.sub(r"^[^,]{0,80},", "", sent)).strip().lower()
            if len(key) > 35:
                sents.setdefault(key, set()).add(s)
    for key, slugs in sents.items():
        if len(slugs) >= 3:
            errs.append(f"şablon cümle {len(slugs)} üründe tekrar ediyor: \"{key[:80]}…\" ({sorted(slugs)[:3]}…)")
    idesc = {}
    for s, v in tx["ingredients"].items():
        idesc.setdefault(v.get("description", "").strip().lower(), []).append(s)
        if v.get("nameTr", "").upper() == s.replace("-", " ").upper() and " " in v.get("nameTr", ""):
            warns.append(f"madde {s}: nameTr INCI'nin aynısı ({v['nameTr']}); Türkçe yaygın adı varsa onu yaz")
    for desc, slugs in idesc.items():
        if len(slugs) >= 2:
            errs.append(f"aynı madde açıklaması {len(slugs)} maddede: \"{desc[:70]}…\" ({slugs[:3]}…)")
    # Betik izleri: metinde teknik madde kodu (slug) ya da kırık kelime parçası
    known_slugs = set(t["ingredients"]) | set(tx["ingredients"])
    for s, v in list(tx["products"].items()) + [(k, x.get("description", "")) for k, x in tx["ingredients"].items()]:
        bad = [w for w in re.findall(r"\b[a-z0-9]+(?:-[a-z0-9]+)+\b", v) if w in known_slugs]
        if bad:
            errs.append(f"{s}: metinde teknik madde kodu var {bad[:3]} — Türkçe adını yaz")
        # "(lixir)", "(r-gel)": ürün kodundan kopmuş parça; "(silikon)" gibi Türkçe açıklama parantezi sayılmaz
        frag = [f for f in re.findall(r"\(([a-zçğıöşü-]{1,7})\)", v) if "-" in f or f in s]
        if frag:
            errs.append(f"{s}: metinde anlamsız parça var {frag[:3]}")
    # Kalıp tespiti: ad/INCI kelimeleri atılınca birbirine çok benzeyen metinler
    import difflib

    def skeleton(text, names):
        for n in names:
            for w in re.findall(r"\w{3,}", n or ""):
                text = re.sub(re.escape(w), "", text, flags=re.I)
        return re.sub(r"\s+", " ", text).strip().lower()

    ing_sk = {k: skeleton(x.get("description", ""), [x.get("nameTr"), k.replace("-", " ")]) for k, x in tx["ingredients"].items()}
    keys = list(ing_sk)
    for i, a_ in enumerate(keys):
        sim = [b_ for b_ in keys[i + 1:] if difflib.SequenceMatcher(None, ing_sk[a_], ing_sk[b_]).ratio() > 0.8]
        if len(sim) >= 2:
            errs.append(f"madde {a_}: açıklaması {len(sim)} maddeyle neredeyse aynı kalıp ({sim[:3]}) — maddeye özgü yaz")
    pnames = {p["slug"]: [p.get("nameTr"), p.get("name")] for p in prods}
    pr_sk = {k: skeleton(v, pnames.get(k, [])) for k, v in tx["products"].items()}
    keys = list(pr_sk)
    for i, a_ in enumerate(keys):
        for b_ in keys[i + 1:]:
            if difflib.SequenceMatcher(None, pr_sk[a_], pr_sk[b_]).ratio() > 0.75:
                errs.append(f"{a_} ve {b_}: açıklamalar neredeyse aynı kalıp — ürüne özgü yaz")
    print(f"{brand}: {len(prods)} ürün, {len(errs)} HATA, {len(warns)} uyarı")
    for e in errs:
        print("HATA:", e)
    for w in warns:
        print("uyarı:", w)
    return not errs


if __name__ == "__main__":
    cmd, *args = sys.argv[1:]
    if cmd == "fetch":
        fetch(*args)
    elif cmd == "summary":
        summary(*args)
    elif cmd == "ingredients":
        ingredients(*args)
    elif cmd == "check":
        sys.exit(0 if check(*args) else 1)
    else:
        print(__doc__)
