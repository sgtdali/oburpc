"""Ürün açıklamalarını denetle ve texts_tr.json > products'a yaz.
Kullanım: python -X utf8 urun_metni.py <modül> [--write]   (modül: TEXT = {slug: açıklama})
Denetim: "X yok" denen her özellik (parfüm, alkol, yağ, silikon, sülfat, paraben) out/products.json > attributes'ta
ok=True olmalı; "parfüm var" denirse fragrance ok=False olmalı. İç analiz dili ("analiz", "etiket", "işaretl", "risk
notu") ve 155 karakterden kısa ilk cümle sınırı kontrol edilir. Sonra build_data.py + push_to_db.mjs --only.
"""
import importlib, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SK = os.path.dirname(HERE)
sys.path.insert(0, HERE)
TEXT = importlib.import_module(sys.argv[1]).TEXT
WRITE = "--write" in sys.argv
P = {p["slug"]: p for p in json.load(open(os.path.join(SK, "out", "products.json"), encoding="utf8"))}
WORDS = {"parfüm": "fragrance", "alkol": "alcohol", "yağ": "oil", "silikon": "silicone", "sülfat": "sulfate",
         "paraben": "paraben"}
JARGON = re.compile(r"(?i)\banaliz|etiket|işaretl|risk notu|\bdb\b")

bad = 0
for slug, text in TEXT.items():
    if slug not in P:
        print("ÜRÜN YOK:", slug); bad += 1; continue
    ok = {a["key"]: a["ok"] for a in P[slug]["attributes"]}
    probs = []
    for sent in re.split(r"(?<=[.;:])\s+", text):
        low = sent.lower()
        if re.search(r"\b(yok|içermiyor|içermez)\b", low) and "eklenmiş" not in low:
            for w, key in WORDS.items():
                if re.search(rf"\b{w}(?!\w*ı?n?da)", low) and re.search(rf"\b{w}\w*[, ]+(?:[\w, ]+ )?(ve |ya da )?[\w ,]*\b(yok|içermiyor)", low):
                    if not ok.get(key, True):
                        probs.append(f"'{w} yok' ama {key} içeriyor")
        if re.search(r"\bparfüm var\b", low) and ok.get("fragrance", True):
            probs.append("'parfüm var' ama fragrance yok")
    if JARGON.search(text):
        probs.append("iç dil: " + JARGON.search(text).group(0))
    first = re.split(r"(?<=\.)\s", text)[0]
    print(f"{'SORUN ' if probs else ''}{slug} | {len(text)} krk | ilk cümle {len(first)}" + (" | " + "; ".join(probs) if probs else ""))
    bad += bool(probs)

path = os.path.join(SK, "texts_tr.json")
raw = open(path, encoding="utf8", newline="").read()
nl = "\r\n" if "\r\n" in raw else "\n"
data = json.loads(raw)
fmt = next((i for i in (1, 2, 4) if json.dumps(data, ensure_ascii=False, indent=i).replace("\n", nl).strip() == raw.strip()), None)
changed = sum(1 for s, t in TEXT.items() if data["products"].get(s) != t)
print(f"\nsorunlu: {bad} | texts_tr.json'da değişecek: {changed}/{len(TEXT)} | biçim indent {fmt}")
if WRITE:
    if bad or fmt is None:
        sys.exit("yazılmadı: sorun var ya da biçim yeniden üretilemedi")
    data["products"].update(TEXT)
    open(path, "w", encoding="utf8", newline="").write(
        json.dumps(data, ensure_ascii=False, indent=fmt).replace("\n", nl) + (nl if raw.endswith(nl) else ""))
    print("yazıldı")
