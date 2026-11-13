"""Madde eşleştirme denetimi: (1) 10 Kasım 2026'dan beri eklenen maddelerin işlev/Fulton puanı yerel KB ile aynı mı,
(2) Gratis kaynaklı ürünlerde etiket adı hangi yoldan eşleşti (birebir / eşanlam / parantez / boşluk / PARÇA).
"Parça" yolu yanlış maddeye bağlayabilir; çıktıdaki listeyi gözle kontrol et. Kullanım: python -X utf8 eslesme_denetimi.py
"""
import json, os, re, sys, glob, urllib.request, collections
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..")); SK = os.path.join(ROOT, "scripts", "skincare")
sys.path.insert(0, SK); os.chdir(SK)
import analyze as a
A = a.Analyzer()
env = dict(l.strip().split("=", 1) for l in open(os.path.join(ROOT, ".env.local"), encoding="utf8") if "=" in l and not l.startswith("#"))
url = env["NEXT_PUBLIC_SUPABASE_URL"].strip('"'); key = env["SUPABASE_SERVICE_ROLE_KEY"].strip('"')
def get(path):
    out = []
    for off in range(0, 100000, 1000):
        r = urllib.request.Request(f"{url}/rest/v1/{path}&limit=1000&offset={off}", headers={"apikey": key, "Authorization": "Bearer " + key, "Accept-Profile": "skincare"})
        page = json.load(urllib.request.urlopen(r)); out += page
        if len(page) < 1000: return out
db = get("ingredients?select=slug,inci,function_keys,comedogenic,irritancy,fungal_acne,tags,created_at&order=id")
new = [i for i in db if i["created_at"] >= "2026-11-10"]
print("DB madde:", len(db), "yeni:", len(new))
slug = lambda s: re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
# 1) DB vs yerel KB
nokb, dfunc, dcom, dirr = [], [], [], []
for i in new:
    k = A.kb.get(i["inci"])
    if not k: nokb.append(i["inci"]); continue
    kf = [slug(f) for f in k["functions"]]
    if sorted(kf) != sorted(i["function_keys"] or []): dfunc.append((i["inci"], kf, i["function_keys"]))
    if (k["comedogenic"] or None) != (i["comedogenic"] or None): dcom.append((i["inci"], k["comedogenic"], i["comedogenic"]))
    if (k["irritancy"] or None) != (i["irritancy"] or None): dirr.append((i["inci"], k["irritancy"], i["irritancy"]))
print("KB'de olmayan:", len(nokb), nokb[:20])
print("işlev farkı:", len(dfunc)); [print("  ", x) for x in dfunc[:15]]
print("komedojenlik farkı:", len(dcom), dcom[:15])
print("tahriş farkı:", len(dirr), dirr[:15])
print("yeni maddelerde puanı olan: kom", sum(1 for i in new if i["comedogenic"]), "tahriş", sum(1 for i in new if i["irritancy"]))
print("  örnek:", [(i["inci"], i["comedogenic"], i["irritancy"]) for i in new if i["comedogenic"]][:25])
print("KB kaynak alanları:", list(next(iter(A.kb.values())).keys()))
# 2) Eşleşme yolu
routes = collections.Counter(); odd = collections.defaultdict(set); unresolved = collections.Counter()
n_prod = 0
for f in glob.glob(os.path.join(SK, "raw", "*.json")):
    d = json.load(open(f, encoding="utf8")); s = d.get("brandSite") or {}
    if s.get("inciSource") != "gratis": continue
    n_prod += 1
    for raw in A.repair(s["inci"]):
        n = a.norm(raw); k = A.resolve(raw)
        if not k: unresolved[n] += 1; routes["çözülmedi"] += 1; continue
        noparen = re.sub(r"\s*\([^)]*\)", "", n)
        if n in A.kb: r = "birebir"
        elif n in a.SYNONYMS: r = "eşanlam"
        elif noparen in A.kb or a.SYNONYMS.get(noparen) in A.kb: r = "parantez silindi"
        elif re.sub(r"[^A-Z0-9]", "", n) == re.sub(r"[^A-Z0-9]", "", k["inci"]): r = "boşluk farkı"
        else: r = "parça ('/' ya da parantez içi)"
        routes[r] += 1
        if r.startswith("parça") or r == "boşluk farkı": odd[(r, n, k["inci"])].add(d["slug"])
print("\nGratis ürünü:", n_prod, "eşleşme yolları:", dict(routes))
print("çözülmeyen:", unresolved.most_common(20))
json.dump([{"yol": r, "etiket": n, "eslesen": k, "urun": len(v), "ornek": sorted(v)[0]} for (r, n, k), v in sorted(odd.items(), key=lambda x: -len(x[1]))],
          open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "odd_routes.json"), "w", encoding="utf8"), ensure_ascii=False, indent=1)
print("parça/boşluk yoluyla eşleşen farklı etiket:", len(odd))
for (r, n, k), v in sorted(odd.items(), key=lambda x: -len(x[1]))[:60]:
    print(f"  [{len(v)}] {n}  ->  {k}   ({r[:5]})")
