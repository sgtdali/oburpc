"""build_data.py çıktısını (out/products.json) veritabanıyla karşılaştırır: içerik listesi ve alan farkları.
push_to_db.mjs --only öncesi/sonrası kullan. Farklı slug'lar changed.json'a yazılır. Kullanım: python -X utf8 db_karsilastir.py
"""
import json, os, sys, urllib.request, collections
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
env=dict(l.strip().split("=",1) for l in open(os.path.join(ROOT,".env.local"),encoding="utf8") if "=" in l and not l.startswith("#"))
url=env["NEXT_PUBLIC_SUPABASE_URL"].strip('"'); key=env["SUPABASE_SERVICE_ROLE_KEY"].strip('"')
def get(path):
    out=[]
    for off in range(0,200000,1000):
        r=urllib.request.Request(f"{url}/rest/v1/{path}&limit=1000&offset={off}",headers={"apikey":key,"Authorization":"Bearer "+key,"Accept-Profile":"skincare"})
        page=json.load(urllib.request.urlopen(r)); out+=page
        if len(page)<1000: return out
prods=get("products?select=id,slug,attributes,benefits,concerns,key_ingredient_groups,description,name,name_tr,category_slug&order=id")
ings={i["id"]:i["slug"] for i in get("ingredients?select=id,slug&order=id")}
pi=get("product_ingredients?select=product_id,ingredient_id,position&order=product_id,position")
lists=collections.defaultdict(list)
for r in pi: lists[r["product_id"]].append(ings[r["ingredient_id"]])
db={p["slug"]:{**p,"ings":lists[p["id"]]} for p in prods}
out=json.load(open(os.path.join(ROOT,"scripts/skincare/out/products.json"),encoding="utf8"))
print("DB ürün:",len(db),"yerel üretim:",len(out),"örnek alanlar:",list(out[0].keys()))
changed=[]; other=collections.Counter()
for p in out:
    d=db.get(p["slug"])
    if not d: other["DB'de yok"]+=1; continue
    li=[x["slug"] if isinstance(x,dict) else x for x in p.get("ingredients",p.get("ingredientSlugs",[]))]
    if li!=d["ings"]:
        changed.append((p["slug"],[x for x in d["ings"] if x not in li],[x for x in li if x not in d["ings"]]))
    for k,dk in [("attributes","attributes"),("benefits","benefits"),("concerns","concerns"),("keyIngredientGroups","key_ingredient_groups"),("description","description"),("name","name"),("nameTr","name_tr"),("category","category_slug")]:
        if k in p and json.dumps(p[k],sort_keys=True,ensure_ascii=False)!=json.dumps(d[dk],sort_keys=True,ensure_ascii=False): other[k]+=1; other.setdefault("_ex_"+k,p["slug"])
print("içerik listesi değişen:",len(changed))
for c in changed: print("  ",c[0][:60],"| çıkan:",c[1],"| giren:",c[2])
print("diğer alan farkları:",dict(other))
print("yalnız DB'de:",len(set(db)-{p["slug"] for p in out}))
json.dump([c[0] for c in changed],open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"changed.json"),"w"))
