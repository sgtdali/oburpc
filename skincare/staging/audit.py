"""Denetçi kontrolü (ajan çıktısı): python -X utf8 scripts/skincare/staging/audit.py <marka> [--refetch]

- raw listeleri kaynaktan yeniden çekilen listeyle karşılaştırır (elle müdahale tespiti; --refetch ile)
- güneş sonrası, BB krem, saç, refill, set gibi kapsam dışı ürün kaçağı; SPF'siz görünen üründe UV filtresi
- synonyms.json önerileri: hedef ad madde veritabanında var mı
- metinlerde marka beyanı aktarımı, tıbbi ifade, BÜYÜK HARF / marka adı tekrarı
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SK = os.path.dirname(HERE)
sys.path.insert(0, SK)
os.chdir(SK)
import analyze as an  # noqa: E402

brand = sys.argv[1]
refetch = "--refetch" in sys.argv
d = os.path.join(HERE, brand)
load = lambda p, x=None: json.load(open(p, encoding="utf8")) if os.path.exists(p) else x
prods = load(os.path.join(d, "products.json"), [])
tx = load(os.path.join(d, "texts.json"), {"products": {}, "ingredients": {}})
syn = load(os.path.join(d, "synonyms.json"), {})
kb = an.Analyzer()
issues = []

print(f"== {brand}: {len(prods)} ürün, {len(tx['ingredients'])} madde metni, {len(syn)} eşanlam")
for k, v in syn.items():
    if kb.resolve(v) is None:
        issues.append(f"eşanlam hedefi veritabanında yok: {k} -> {v}")
an.SYNONYMS.update(syn)

if refetch:
    import fetch_sources as fs
SCOPE_RX = re.compile(r"(?i)güneş sonrası|after.?sun|bronzlaştırıcı|\bbb ?(krem|cream)\b|şampuan|shampoo|saç\b|refill|yedek|\bset\b|\bkit\b|rutin|ikili|deodorant|terleme")
MED_RX = re.compile(r"(?i)tedavi|egzama|sedef|psoriazis|rozasea tedav|tıbbi cihaz|hamile|emzir|bebek|\d+ ?ay(dan|lık)|iyileştir|reçete")
CLAIM_RX = re.compile(r"(?i)marka(nın|ya göre)?\b[^.]{0,80}(diyor|belirtiyor|beyan|iddia)")
for p in prods:
    s = p["slug"]
    raw = load(os.path.join(d, "raw", s + ".json"))
    inci = raw["brandSite"]["inci"]
    r = kb.analyze(inci)
    uv = [i["raw"] for i in r["ingredients"] if i["kb"] and "uv-filter" in i["kb"]["classes"]
          and not re.search(r"TITANIUM|ZINC OXIDE|CI 77891", i["raw"])]
    # 2026-11-02: güneş koruyucular kapsamda; UV filtresi yalnızca SPF'siz görünen üründe şüphelidir
    if uv and p["category"] != "gunes-koruyucu" and not re.search(r"(?i)spf\s*\d", p["name"]):
        issues.append(f"{s}: UV filtresi var ama SPF'li ürün olarak eklenmemiş: {uv[:3]}")
    if SCOPE_RX.search(p["name"] + " " + p["nameTr"] + " " + p["brandUrl"]):
        issues.append(f"{s}: ad/URL kapsam dışı kelime içeriyor: {p['nameTr']} | {p['brandUrl']}")
    if p["nameTr"].isupper() or p["nameTr"].lower().startswith(brand.split("-")[0]):
        issues.append(f"{s}: nameTr biçimi: {p['nameTr']}")
    desc = tx["products"].get(s, "")
    if CLAIM_RX.search(desc):
        issues.append(f"{s}: açıklamada marka beyanı: {CLAIM_RX.search(desc).group(0)}")
    if MED_RX.search(desc) or MED_RX.search(p["nameTr"]):
        issues.append(f"{s}: tıbbi/yaş ifadesi: {(MED_RX.search(desc) or MED_RX.search(p['nameTr'])).group(0)}")
    if refetch:
        fresh = fs.brand_page(p["brandUrl"])["inci"]
        if fresh != inci:
            issues.append(f"{s}: RAW KAYNAKTAN FARKLI (elle müdahale?) +{[x for x in fresh if x not in inci][:2]} -{[x for x in inci if x not in fresh][:2]}")
for k, v in tx["ingredients"].items():
    if MED_RX.search(v.get("description", "")):
        issues.append(f"madde {k}: tıbbi ifade: {MED_RX.search(v['description']).group(0)}")
print(f"{len(issues)} bulgu")
for i in issues:
    print(" -", i)
