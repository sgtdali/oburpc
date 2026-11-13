"""Düzeltme modülündeki madde adı/açıklama düzeltmelerini texts_tr.json'a ve Supabase skincare.ingredients'a yazar.
Önce madde_dok.py çalıştır. Düzeltme modülü: FIX = {INCI: (yeni ad | None, yeni açıklama | None)}.
Kullanım: python -X utf8 metin_duzelt.py duzeltmeler_20261111 [--write]   (--write yoksa deneme)
"""
import json, os, sys, urllib.request, urllib.parse
import importlib
FIX = importlib.import_module(sys.argv[1]).FIX

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
WRITE = "--write" in sys.argv
HERE = os.path.dirname(os.path.abspath(__file__))
ing = {i["inci"]: i for i in json.load(open(os.path.join(HERE, "ing_all.json"), encoding="utf8"))}

# 1) texts_tr.json
path = os.path.join(ROOT, "scripts", "skincare", "texts_tr.json")
raw = open(path, encoding="utf8", newline="").read()
nl = "\r\n" if "\r\n" in raw else "\n"
data = json.loads(raw)
fmt = None
for indent in (1, 2, 4):
    out = json.dumps(data, ensure_ascii=False, indent=indent)
    if out.replace("\n", nl).strip() == raw.strip():
        fmt = indent
        break
print("texts_tr.json biçimi: indent", fmt, "| satır sonu", repr(nl), "| sonda boş satır:", raw.endswith(nl))
if fmt is None:
    sys.exit("texts_tr.json biçimi yeniden üretilemedi; dokunulmadı")
t = data["ingredients"]
added = changed = 0
rows = []
for inci, (name, desc) in FIX.items():
    i = ing[inci]
    new_name = name or i["name_tr"]
    new_desc = desc or i["description"]
    rows.append((i["slug"], new_name, new_desc))
    if i["slug"] in t:
        if t[i["slug"]].get("nameTr") != new_name or t[i["slug"]].get("description") != new_desc:
            changed += 1
        t[i["slug"]]["nameTr"] = new_name
        t[i["slug"]]["description"] = new_desc
    else:
        added += 1
        t[i["slug"]] = {"nameTr": new_name, "description": new_desc}
print(f"texts_tr.json: {changed} değişecek, {added} eklenecek")
if WRITE:
    out = json.dumps(data, ensure_ascii=False, indent=fmt).replace("\n", nl) + (nl if raw.endswith(nl) else "")
    open(path, "w", encoding="utf8", newline="").write(out)

# 2) Supabase
env = dict(l.strip().split("=", 1) for l in open(os.path.join(ROOT, ".env.local"), encoding="utf8") if "=" in l and not l.startswith("#"))
url = env["NEXT_PUBLIC_SUPABASE_URL"].strip('"')
key = env["SUPABASE_SERVICE_ROLE_KEY"].strip('"')
ok = 0
for slug, name, desc in rows:
    if not WRITE:
        continue
    body = json.dumps({"name_tr": name, "description": desc}).encode()
    r = urllib.request.Request(
        f"{url}/rest/v1/ingredients?slug=eq.{urllib.parse.quote(slug)}", data=body, method="PATCH",
        headers={"apikey": key, "Authorization": "Bearer " + key, "Content-Profile": "skincare", "Accept-Profile": "skincare",
                 "Content-Type": "application/json", "Prefer": "return=representation"})
    res = json.load(urllib.request.urlopen(r))
    if len(res) == 1 and res[0]["name_tr"] == name and res[0]["description"] == desc:
        ok += 1
    else:
        print("  SORUN:", slug, len(res))
print(f"veritabanı: {ok}/{len(rows)} satır güncellendi" if WRITE else f"[deneme] veritabanında {len(rows)} satır güncellenecek")
