"""Denetçi: onaylanmış hazırlık klasörünü kataloğa işle.

    python -X utf8 scripts/skincare/staging/merge.py <marka> [--skip slug1,slug2] [--dry-run]

- products.json -> catalog.json (yalnızca katalogda olmayan slug'lar; sıra korunur)
- raw/<slug>.json -> scripts/skincare/raw/
- texts.json -> texts_tr.json (yalnızca eksik ürün/madde anahtarları; var olan metne dokunmaz)
- synonyms.json -> yalnızca listelenir; analyze.py'ye denetçi elle ekler (gerekçesiyle)
Dosyalar mevcut biçimde (2 boşluk girinti, CRLF) yazılır.
"""
import json, os, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SK = os.path.dirname(HERE)
brand = sys.argv[1]
dry = "--dry-run" in sys.argv
skip = set()
if "--skip" in sys.argv:
    skip = set(sys.argv[sys.argv.index("--skip") + 1].split(","))
d = os.path.join(HERE, brand)
load = lambda p: json.load(open(p, encoding="utf8"))


def save(path, data):
    if dry:
        return
    crlf = b"\r\n" in open(path, "rb").read(4096)  # dosyanın mevcut satır sonu korunur
    with open(path, "w", encoding="utf8", newline="\r\n" if crlf else "\n") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


prods = [p for p in load(os.path.join(d, "products.json")) if p["slug"] not in skip]
tx = load(os.path.join(d, "texts.json"))
cat_path, tx_path = os.path.join(SK, "catalog.json"), os.path.join(SK, "texts_tr.json")

cat = load(cat_path)
have = {p["slug"] for p in cat["products"]}
assert brand in {b["slug"] for b in cat["brands"]}, f"marka katalogda yok: {brand}"
add = [{k: p[k] for k in ("slug", "brand", "name", "nameTr", "category", "brandUrl", "imageUrl") if p.get(k)}
       for p in prods if p["slug"] not in have]
cat["products"] += add
save(cat_path, cat)

for p in add:
    src = os.path.join(d, "raw", p["slug"] + ".json")
    if not dry:
        shutil.copyfile(src, os.path.join(SK, "raw", p["slug"] + ".json"))

t = load(tx_path)
slugs = {p["slug"] for p in add}
add_pt = {k: v for k, v in tx["products"].items() if k in slugs and k not in t["products"]}
add_it = {k: v for k, v in tx["ingredients"].items() if k not in t["ingredients"]}
t["products"].update(add_pt)
t["ingredients"].update(add_it)
save(tx_path, t)

syn = load(os.path.join(d, "synonyms.json")) if os.path.exists(os.path.join(d, "synonyms.json")) else {}
print(f"{'[deneme] ' if dry else ''}{brand}: +{len(add)} ürün, +{len(add_pt)} ürün metni, +{len(add_it)} madde metni; "
      f"atlanan: {sorted(skip)}; eşanlam (analyze.py'ye elle): {syn}")
print("slug'lar:", ",".join(p["slug"] for p in add))
