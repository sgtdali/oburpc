"""Madde açıklamalarını CosIng işlevi / Fulton puanı / kendi etiketlerimizle anahtar kelime üzerinden karşılaştırır.
Önce madde_dok.py çalıştır. Kaba bir taramadır (yanlış alarm verir: "bakteri fermentasyonu", "frenk" içindeki "renk");
işaretlenenler flags.json'a yazılır, elle okunur. Kullanım: python -X utf8 metin_tara.py
"""
import json, re, collections
import os
HERE=os.path.dirname(os.path.abspath(__file__))
ing=json.load(open(os.path.join(HERE,"ing_all.json"),encoding="utf8"))
new=[i for i in ing if i["created_at"]>="2026-11-10"]
print("tags:",collections.Counter(t for i in new for t in (i["tags"] or [])).most_common())
print("fungal:",collections.Counter(str(i["fungal_acne"]) for i in new))
F=lambda i:set(i["function_keys"] or []); T=lambda i:set(i["tags"] or [])
def rmin(r):
    m=re.findall(r"\d",re.sub(r"\(.*?\)","",str(r or ""))); return int(m[0]) if m else None
# (ad, metin kalıbı, desteklenme koşulu)
R=[
 ("nem tutucu", r"nem tutucu|nem tutar|nemlendir|su tutma|suyu? (çek|tut)|hidrasyon|nem (çek|bağla|kayb)", lambda i:F(i)&{"humectant","moisturising","skin-conditioning-humectant","skin-conditioning-occlusive","skin-conditioning-emollient","skin-protecting"}),
 ("yumuşatıcı", r"yumuşat|emolyent|emoliyan", lambda i:F(i)&{"skin-conditioning-emollient","skin-conditioning","smoothing","skin-conditioning-occlusive","hair-conditioning"}),
 ("antioksidan", r"antioksidan", lambda i:"antioxidant" in F(i) or "antioxidant" in T(i)),
 ("koruyucu (raf)", r"koruyucu madde|koruyucudur|bozulma(sını|ya)|mikrop.*(üreme|önle)|raf ömr", lambda i:F(i)&{"preservative","antimicrobial","antioxidant","chelating"}),
 ("antimikrobiyal", r"antimikrobiyal|antibakteriyel|bakteri", lambda i:F(i)&{"antimicrobial","preservative","deodorant"}),
 ("kıvam", r"kıvam|koyulaştır|viskozite|jel(leştir| oluştur)", lambda i:F(i)&{"viscosity-controlling","gel-forming","binding","bulking","emulsion-stabilising","film-forming","opacifying","absorbent"}),
 ("emülgatör", r"emülgatör|emülsiyon|yağ(ın)? ve su|su(yun)? ve yağ|karışmasını", lambda i:F(i)&{"surfactant-emulsifying","emulsion-stabilising","surfactant-cleansing","surfactant-hydrotrope","surfactant-dispersing","solvent"}),
 ("temizleyici", r"temizle|yüzey aktif|köpü", lambda i:F(i)&{"surfactant-cleansing","cleansing","foaming","surfactant-foam-boosting","surfactant-emulsifying","antifoaming","abrasive","absorbent","surfactant-hydrotrope"}),
 ("koku", r"koku|parfüm|esans|aroma", lambda i:F(i)&{"fragrance","perfuming","flavouring","deodorant","tonic","refreshing"} or T(i)&{"fragrance-ingredient","eu-allergen","fragrance"}),
 ("renk", r"renk|boya|pigment", lambda i:F(i)&{"colorant","hair-dyeing","opacifying","bleaching"}),
 ("UV", r"\buv\b|güneş (filtre|koru)|ultraviyole|ışınları", lambda i:F(i)&{"uv-filter","uv-absorber","light-stabilizer"}),
 ("çözücü", r"çözücü", lambda i:F(i)&{"solvent","surfactant-hydrotrope","keratolytic","denaturant"}),
 ("pH", r"\bph\b|asitli(k|ğ)", lambda i:F(i)&{"buffering"}),
 ("şelat", r"şelat|metal iyon", lambda i:"chelating" in F(i)),
 ("film", r"film", lambda i:F(i)&{"film-forming","hair-fixing"}),
 ("aşındırıcı/peeling", r"aşındır|peeling|ölü deri|eksfol|soyucu|pul pul", lambda i:F(i)&{"abrasive","exfoliating","keratolytic"}),
 ("astrenjan", r"astrenjan|büzücü|sıkılaştır", lambda i:F(i)&{"astringent","tonic"}),
 ("yatıştırıcı", r"yatıştır|sakinleştir|rahatlat", lambda i:F(i)&{"soothing","skin-protecting"}),
 ("sebum", r"sebum|yağ(lanma| dengesi| üretim)|matlaştır", lambda i:F(i)&{"anti-sebum","anti-seborrheic","absorbent","astringent"}),
 ("cilt koruyucu", r"cildi koru|cilt koruyucu|bariyer", lambda i:F(i)&{"skin-protecting","skin-conditioning-occlusive","skin-conditioning-emollient","skin-conditioning"}),
 ("antistatik/saç", r"antistatik|saç", lambda i:F(i)&{"antistatic","hair-conditioning","hair-fixing","hair-dyeing","hair-waving-or-straightening","detangling"}),
 ("ağartıcı", r"ağart|beyazlat", lambda i:"bleaching" in F(i)),
 ("mantar aknesi", r"mantar akne|malassezia|fungal", lambda i:bool(i["fungal_acne"]) or "fungal-acne-trigger" in T(i)),
 ("komedojen", r"komedojen|gözenek(leri)? tıka|akneye yatkın|akne tetik", lambda i:(rmin(i["comedogenic"]) or 0)>=2 or bool(i["fungal_acne"])),
 ("tahriş", r"tahriş", lambda i:(rmin(i["irritancy"]) or 0)>=2 or T(i)&{"eu-allergen","fragrance-ingredient","fragrance","alcohol","drying-alcohol","aha","bha","retinoid","sulfate","essential-oil"} or F(i)&{"fragrance","perfuming","keratolytic","exfoliating","denaturant","surfactant-cleansing"}),
 ("alerjen", r"alerj", lambda i:T(i)&{"eu-allergen","fragrance-ingredient","fragrance"} or F(i)&{"fragrance","perfuming"}),
 ("İDDİA", r"yaşlanma|kırışık|kolajen üret|elastin|leke|aydınlat|ton eşit|onar|iyileş|sivilce|egzama|tedavi|iltihap|enflam|yara|hücre yenile|sıkılık|dolgun|parlak|canlandır", lambda i:False),
]
flags=collections.defaultdict(list)
for i in new:
    d=i["description"].lower().replace("İ","i")
    for name,rx,ok in R:
        m=re.search(rx,d)
        if m and not ok(i): flags[name].append(i)
tot=set()
for k,v in flags.items():
    print(f"\n== {k}: {len(v)}"); tot|={i['slug'] for i in v}
print("\nişaretlenen farklı madde:",len(tot),"/",len(new))
json.dump({k:[{"inci":i["inci"],"ad":i["name_tr"],"metin":i["description"],"islev":i["function_keys"],"kom":i["comedogenic"],"tah":i["irritancy"],"fungal":i["fungal_acne"],"tags":i["tags"],"uses":i["uses"]} for i in v] for k,v in flags.items()},open(os.path.join(HERE,"flags.json"),"w",encoding="utf8"),ensure_ascii=False,indent=1)
