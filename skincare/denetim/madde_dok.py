"""Veritabanındaki tüm maddeleri (metin, işlev, puan, etiket, kullanım sayısı) ing_all.json'a döker; metin_tara.py ve
metin_duzelt.py bunu okur. Kullanım: python -X utf8 madde_dok.py
"""
import json, os, sys, urllib.request, collections, re
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..")); HERE=os.path.dirname(os.path.abspath(__file__))
env=dict(l.strip().split("=",1) for l in open(os.path.join(ROOT,".env.local"),encoding="utf8") if "=" in l and not l.startswith("#"))
url=env["NEXT_PUBLIC_SUPABASE_URL"].strip('"'); key=env["SUPABASE_SERVICE_ROLE_KEY"].strip('"')
def get(path):
    out=[]
    for off in range(0,200000,1000):
        r=urllib.request.Request(f"{url}/rest/v1/{path}&limit=1000&offset={off}",headers={"apikey":key,"Authorization":"Bearer "+key,"Accept-Profile":"skincare"})
        page=json.load(urllib.request.urlopen(r)); out+=page
        if len(page)<1000: return out
ing=get("ingredients?select=id,slug,inci,name_tr,function_keys,comedogenic,irritancy,fungal_acne,tags,description,guide,created_at&order=id")
use=collections.Counter(r["ingredient_id"] for r in get("product_ingredients?select=ingredient_id&order=product_id"))
for i in ing: i["uses"]=use[i["id"]]
json.dump(ing,open(os.path.join(HERE,"ing_all.json"),"w",encoding="utf8"),ensure_ascii=False)
new=[i for i in ing if i["created_at"]>="2026-11-10"]; old=[i for i in ing if i["created_at"]<"2026-11-10"]
print(len(ing),len(new),"guide dolu (yeni/eski):",sum(1 for i in new if i["guide"]),sum(1 for i in old if i["guide"]))
print("işlev anahtarları (yeni):",collections.Counter(f for i in new for f in i["function_keys"]).most_common())
t=json.load(open(os.path.join(ROOT,"scripts/skincare/texts_tr.json"),encoding="utf8"))["ingredients"]
print("yeni maddelerden texts_tr.json'da olmayan:",sum(1 for i in new if i["slug"] not in t), "metni DB'den farklı:",sum(1 for i in new if i["slug"] in t and (t[i["slug"]].get("description")!=i["description"] or t[i["slug"]].get("nameTr")!=i["name_tr"])))
print("açıklama uzunluğu ort (yeni/eski):",sum(len(i["description"]) for i in new)//len(new),sum(len(i["description"]) for i in old)//len(old))
words=collections.Counter(w for i in new for w in set(re.findall(r"[a-zçğıöşü]{5,}",i["description"].lower())))
print(words.most_common(150))
