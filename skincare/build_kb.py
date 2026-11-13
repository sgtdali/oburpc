"""Kendi madde veritabanımız: CosIng + Fulton 1989 + ad/işlev kuralları.

    python -X utf8 scripts/skincare/build_kb.py

Girdi:  scripts/skincare/cosing/*.json (cosing_fetch.py), scripts/skincare/kb/fulton_1989.csv
Çıktı:  scripts/skincare/kb/ingredients_kb.json  (her INCI için sınıflar, puanlar, kısıtlamalar)

Kurallar bilerek basit ve okunur tutuldu; her sınıfın gerekçesi docs/skincare-veri-kaynaklari.md'de.
Bir maddeyi yanlış sınıflandıran kural görürsen önce OVERRIDES'a ekle, kalıcı çözüm için kuralı düzelt.
"""
import csv, json, os, re
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
COSING = os.path.join(HERE, "cosing")
KB = os.path.join(HERE, "kb")

# ---------- yardımcılar ----------

def norm(name):
    """INCI karşılaştırma anahtarı: büyük harf, tek boşluk."""
    return re.sub(r"\s+", " ", (name or "").strip().upper())


def as_list(v):
    return v if isinstance(v, list) else ([v] if v not in (None, "") else [])


# ---------- sınıf kuralları ----------

DRYING_ALCOHOLS = {"ALCOHOL", "ALCOHOL DENAT.", "ETHANOL", "ISOPROPYL ALCOHOL", "METHANOL", "PROPANOL"}
FATTY_ALCOHOL_RE = re.compile(
    r"^(CETYL|STEARYL|CETEARYL|BEHENYL|MYRISTYL|LAURYL|ARACHIDYL|OLEYL|ISOSTEARYL|ISOCETYL|"
    r"OCTYLDODECANOL|DECYL|CAPRYLYL|C\d+-\d+) ALCOHOLS?$|^OCTYLDODECANOL$")
FRAGRANCE_NAMES = {"PARFUM", "FRAGRANCE", "AROMA", "PARFUM/FRAGRANCE"}
SULFATE_RE = re.compile(r"(LAURYL|LAURETH|COCETH|MYRETH|PARETH|TRIDECETH|DECETH|COCO|COCOYL|CETEARYL|CETYL|MYRISTYL|"
                        r"C\d+-\d+ ALKYL|ALKYL)[\w\- ]*? SULFATE$")
# "-CONE" silikon ekini yakalar; aynı ekle biten silikon olmayan adlar hariç (2026-11-12: ALPHA-DAMASCONE koku
# maddesi ve HESPERIDIN METHYL CHALCONE silikon sayılıyordu).
SILICONE_RE = re.compile(r"((?<!DAMAS)(?<!CHAL)CONE|CONOL|SILOXANE|SILANE|SILSESQUIOXANE|SILICONE)S?\b")
PLANT_PART_OIL_RE = re.compile(r"^[A-Z]+ [A-Z]+( [A-Z]+)? (SEED|KERNEL|NUT|FRUIT|GERM|BRAN|PULP)?\s?OIL$")
MINERAL_OILS = {"PARAFFINUM LIQUIDUM", "MINERAL OIL", "PETROLATUM", "PARAFFIN", "CERA MICROCRISTALLINA",
                "MICROCRYSTALLINE WAX", "ISOHEXADECANE", "ISODODECANE"}
# Malassezia'yı beslemeyen yağlar (8-10 karbonlu, hidrokarbonlar)
FUNGAL_SAFE = {"CAPRYLIC/CAPRIC TRIGLYCERIDE", "SQUALANE", "SQUALENE", "PARAFFINUM LIQUIDUM", "MINERAL OIL",
               "PETROLATUM", "CAPRYLIC ACID", "CAPRIC ACID", "TRICAPRYLIN", "HYDROGENATED POLYISOBUTENE",
               "ISOHEXADECANE", "ISODODECANE", "COCO-CAPRYLATE/CAPRATE", "COCO-CAPRYLATE"}
# 11-24 karbonlu yağ asitleri ve onlardan türeyen ester/ad kökleri (Malassezia için besin)
FATTY_ACIDS = ["LAURIC", "MYRISTIC", "PALMITIC", "STEARIC", "ISOSTEARIC", "OLEIC", "LINOLEIC", "LINOLENIC",
               "ARACHIDIC", "BEHENIC", "ERUCIC", "RICINOLEIC", "PALMITOLEIC", "HYDROXYSTEARIC", "UNDECYLENIC"]
FATTY_ACID_RE = re.compile(r"^(" + "|".join(FATTY_ACIDS) + r") ACID$")
FATTY_ESTER_RE = re.compile(r"(LAURATE|MYRISTATE|PALMITATE|STEARATE|OLEATE|LINOLEATE|LINOLENATE|ARACHIDATE|"
                            r"BEHENATE|ERUCATE|RICINOLEATE|COCOATE|ISOSTEARATE|HYDROXYSTEARATE|PALMATE|OLIVATE|"
                            r"SHEABUTTERATE|TALLOWATE|STEAROYL STEARATE)S?\b")
# Uçucu (esansiyel) yağ: aromatik bitki kısmından elde edilen yağ ya da bilinen aromatik cins.
# Tohum/çekirdek yağları (ör. ZEA MAYS OIL) CosIng'de "PERFUMING" işlevli olsa bile bitkisel yağdır.
AROMATIC_PART_OIL_RE = re.compile(r" (LEAF|HERB|FLOWER|FLOWER/LEAF/STEM|LEAF/STEM|PEEL|BARK|WOOD|ROOT|RHIZOME|"
                                  r"TWIG|NEEDLE|RESIN|STEM|BUD|BERRY|CONE|SEED/NEEDLE|LEAF/TWIG)S?( [A-Z]+)? OIL$")
AROMATIC_GENERA = {
    "CITRUS", "MENTHA", "LAVANDULA", "ROSMARINUS", "EUCALYPTUS", "MELALEUCA", "CYMBOPOGON", "PELARGONIUM",
    "SALVIA", "THYMUS", "ORIGANUM", "CINNAMOMUM", "EUGENIA", "SYZYGIUM", "SANTALUM", "CEDRUS", "JUNIPERUS",
    "PINUS", "JASMINUM", "CANANGA", "POGOSTEMON", "VETIVERIA", "CHRYSOPOGON", "OCIMUM", "ANETHUM",
    "FOENICULUM", "CORIANDRUM", "ZINGIBER", "LITSEA", "BOSWELLIA", "COMMIPHORA", "CUPRESSUS", "ABIES", "PICEA",
    "ARTEMISIA", "CHAMOMILLA", "MATRICARIA", "ANTHEMIS", "ILLICIUM", "PIMPINELLA", "CARUM", "LAURUS", "MYRTUS",
    "TAGETES", "CISTUS", "MELISSA", "NEPETA", "PIPER", "ELETTARIA", "MYRISTICA", "CUMINUM", "LIPPIA", "AQUILARIA",
}
REEF_UNSAFE = {"BENZOPHENONE-3", "ETHYLHEXYL METHOXYCINNAMATE"}  # Hawaii yasası (oxybenzone, octinoxate)

# Aktif madde grupları (ürün sayfasındaki "öne çıkan içerikler")
ACTIVE_RULES = [
    ("ceramide", re.compile(r"^CERAMIDE |^CERAMIDE$|^CERAMIDE-")),
    ("hyaluronic-acid", re.compile(r"HYALURON")),
    ("niacinamide", re.compile(r"^NIACINAMIDE$")),
    ("retinoid", re.compile(r"^RETINOL$|^RETINAL$|^RETINYL |^HYDROXYPINACOLONE RETINOATE$|^RETINOIC")),
    ("aha", re.compile(r"^(GLYCOLIC|LACTIC|MANDELIC|MALIC|TARTARIC) ACID$")),
    ("bha", re.compile(r"^SALICYLIC ACID$|^BETAINE SALICYLATE$|^CAPRYLOYL SALICYLIC ACID$")),
    ("pha", re.compile(r"^GLUCONOLACTONE$|^LACTOBIONIC ACID$")),
    ("vitamin-c", re.compile(r"^ASCORBIC ACID$|ASCORBYL|ASCORBATE$|^3-O-ETHYL ASCORBIC ACID$")),
    ("vitamin-e", re.compile(r"^TOCOPHEROL$|^TOCOPHERYL ")),
    ("peptide", re.compile(r"PEPTIDE")),
    ("panthenol", re.compile(r"^PANTHENOL$|^DEXPANTHENOL$")),
    ("centella", re.compile(r"^CENTELLA ASIATICA|^MADECASSOSIDE$|^ASIATICOSIDE$|^ASIATIC ACID$|^MADECASSIC ACID$")),
    ("azelaic-acid", re.compile(r"^AZELAIC ACID$|^POTASSIUM AZELOYL DIGLYCINATE$")),
    ("bakuchiol", re.compile(r"^BAKUCHIOL$")),
    ("allantoin", re.compile(r"^ALLANTOIN$")),
    ("squalane", re.compile(r"^SQUALANE$")),
    ("urea", re.compile(r"^UREA$")),
    ("brightener", re.compile(r"^(ALPHA-)?ARBUTIN$|^TRANEXAMIC ACID$|^KOJIC ACID$|^GLYCYRRHIZA GLABRA ROOT EXTRACT$")),
]

# Kurala uymayan bilinen istisnalar: ad -> sınıf ekle (+) / çıkar (-)
OVERRIDES = {
    "BENZYL ALCOHOL": {"-": ["drying-alcohol"]},
}


def classify(name, funcs, allergens):
    n = norm(name)
    f = {x.upper() for x in funcs}
    c = set()
    if n in DRYING_ALCOHOLS or n.startswith("SD ALCOHOL"):
        c.add("drying-alcohol")
    if FATTY_ALCOHOL_RE.search(n):
        c.add("fatty-alcohol")
    if n in FRAGRANCE_NAMES:
        c.add("fragrance")
    if n in allergens:
        c.update({"eu-allergen", "fragrance"})
    if n.endswith("PARABEN"):
        c.add("paraben")
    if SULFATE_RE.search(n) and "CHONDROITIN" not in n:
        c.add("sulfate")
    if SILICONE_RE.search(n):
        c.add("silicone")
    if n in MINERAL_OILS:
        c.add("mineral-oil")
    is_oil_name = n.endswith(" OIL") and not n.startswith(("PEG-", "PPG-", "SULFATED"))
    if is_oil_name and not n.startswith("HYDROGENATED") and not re.search(r" (SEED|KERNEL|NUT|GERM|BRAN|FRUIT) OIL$", n) \
            and (AROMATIC_PART_OIL_RE.search(n) or n.split()[0] in AROMATIC_GENERA or n in allergens):
        c.update({"essential-oil", "fragrance"})
    elif (is_oil_name or n.endswith(" BUTTER")) and n not in MINERAL_OILS:
        c.add("plant-oil")
    if n.startswith("POLYSORBATE"):
        c.add("polysorbate")
    if FATTY_ACID_RE.search(n):
        c.add("fatty-acid")
    if FATTY_ESTER_RE.search(n) and not n.startswith("PEG-"):
        c.add("fatty-ester")
    if {"UV FILTER", "UV ABSORBER"} & f:
        c.add("uv-filter")
    if n in REEF_UNSAFE:
        c.add("reef-unsafe")
    if "PRESERVATIVE" in f:
        c.add("preservative")
    if {"HUMECTANT", "SKIN CONDITIONING - HUMECTANT", "MOISTURISING"} & f:
        c.add("humectant")
    if {"SKIN CONDITIONING - EMOLLIENT", "REFATTING"} & f:
        c.add("emollient")
    if {"OCCLUSIVE", "SKIN CONDITIONING - OCCLUSIVE"} & f:
        c.add("occlusive")
    if "ANTIOXIDANT" in f:
        c.add("antioxidant")
    if {"SOOTHING"} & f:
        c.add("soothing")
    if {"EXFOLIATING", "KERATOLYTIC"} & f:
        c.add("exfoliant")
    for group, rx in ACTIVE_RULES:
        if rx.search(n):
            c.add("active:" + group)
    o = OVERRIDES.get(n, {})
    c.update(o.get("+", []))
    c.difference_update(o.get("-", []))
    return c


def fungal(n, classes):
    """Malassezia (fungal akne) riski: 11-24 karbonlu yağ asitleri, esterleri, polisorbatlar, çoğu bitkisel yağ."""
    if n in FUNGAL_SAFE:
        return None
    # 8-10 karbonlu (kaprilik/kaprik) türevler Malassezia'yı beslemez: PEG-6 CAPRYLIC/CAPRIC GLYCERIDES vb.
    if re.search(r"CAPRYLIC|CAPRIC|CAPRYLATE|CAPRATE", n) and not ({"fatty-acid"} & classes) \
            and not re.search(r"LAUR|MYRIST|PALMIT|STEAR|OLE|LINOLE|COCO|BEHEN", n):
        return None
    if {"fatty-acid", "fatty-ester", "polysorbate"} & classes:
        return "trigger"
    if "plant-oil" in classes or n.endswith(("GLYCERIDES", "TRIGLYCERIDE")):
        return "trigger"
    return None


# ---------- AB alerjenleri ve kısıtlamalar ----------

PLANT_PARTS = {"FLOWER", "LEAF", "TWIG", "BUD", "STEM", "WOOD", "BARK", "PEEL", "NEEDLE"}
PLANT_KINDS = {"OIL": "OIL", "OILS": "OIL", "EXTRACT": "EXTRACT", "EXTRACTS": "EXTRACT", "ABSOLUTE": "ABSOLUTE"}


def strict_plants(text, names):
    """AB 2023/1545 bitki girdisinin ("Cymbopogon citratus / schoenanthus/ flexuosus oils", "Pinus mugo leaf and
    twig oil and extract") kapsadığı INCI adları: cins + girdideki türlerden biri (+ varyete), ardından yalnızca
    girdide geçen bitki kısımları (girdi kısım belirtmiyorsa yaprak/çiçek/kabuk gibi yaygın kısımlar), sonda girdide
    geçen tür (OIL / EXTRACT / ABSOLUTE). Tohum, meyve, kök, kallus ve su türevleri kapsam dışıdır."""
    out = set()
    for part in text.split(";"):
        words = re.findall(r"[A-Za-z]+", part)
        if len(words) < 2 or not words[0][0].isupper():
            continue
        genus, rest = words[0].upper(), [w.upper() for w in words[1:]]
        kinds = {PLANT_KINDS[w] for w in rest if w in PLANT_KINDS}
        parts = {w for w in rest if w in PLANT_PARTS}
        # tür ve varyete adları: kısım/tür/bağlaç olmayan küçük harfli kelimeler (citratus, amara, dulcis…)
        epithets = {w for w in rest if w not in PLANT_KINDS and w not in PLANT_PARTS
                    and w not in {"AND", "OR", "VAR", "SPP"}}
        if not kinds or not epithets:
            continue
        for n in names:
            w = n.replace("/", " ").split()
            if len(w) < 3 or w[0] != genus or w[1] not in epithets or w[-1] not in kinds:
                continue
            middle = set(w[2:-1]) - epithets - set(kinds)  # "OIL/EXTRACT" gibi birleşikler
            if middle <= (parts or PLANT_PARTS):
                out.add(n)
    return out


def load_substances(ingredients_by_name, ingredients_by_id):
    S = json.load(open(os.path.join(COSING, "substances.json"), encoding="utf8"))
    # 2023/1545 ile eklenen girdiler etiketteki adı da verir: "shall be indicated as ‘Citral’ in the list of
    # ingredients". Bu girdilerin inciName'i kimyasal addır (3,7-Dimethyl-2,6-octadienal); etiket adı ayrıca eşlenir.
    label_rx = re.compile(r"(?:indicated|mentioned)(?:\s+as\s+((?:[‘'\"][^’'\"]+[’'\"](?:,?\s*(?:or|and)?\s*)?)+))?"
                          r"\s+in the list of ingredients", re.I)
    allergens, restrictions = set(), {}
    for s in S:
        blob = json.dumps(s, ensure_ascii=False)
        targets = set()
        m = label_rx.search(blob)
        for label in re.findall(r"[‘'\"]([^’'\"]+)[’'\"]", m.group(1) or "") if m else []:
            if norm(label) in ingredients_by_name:
                targets.add(norm(label))
        for x in as_list(s.get("identifiedIngredient")):
            for y in re.split(r"[;,]", str(x)):
                if y.strip() in ingredients_by_id:
                    targets.add(norm(ingredients_by_id[y.strip()]["inciName"]))
        for nm in as_list(s.get("nameOfCommonIngredientsGlossary")) + as_list(s.get("inciName")):
            if norm(nm) in ingredients_by_name:
                targets.add(norm(nm))
        if m and m.group(1):
            # 2023/1545 girdileri bitkiyi kısmıyla tanımlar ("Rosa canina flower oil", "Eucalyptus globulus oil"):
            # cins+tür öneki yetmez (kuşburnu tohum yağı, okaliptüs yaprak özütü alerjen değildir) → strict_plants
            allergens |= targets | strict_plants(" ; ".join(map(str, as_list(s.get("inciName")))), ingredients_by_name)
        elif m:
            allergens |= targets
            # "Lavandula angustifolia oil/extract" gibi bitki tanımları: cins+tür ile başlayan INCI'ler
            for nm in as_list(s.get("inciName")):
                for part in re.split(r";|\band\b|/", str(nm)):
                    words = re.findall(r"[A-Za-z]+", part)
                    if len(words) >= 2 and words[0][0].isupper() and words[1].islower():
                        prefix = f"{words[0]} {words[1]}".upper()
                        allergens |= {k for k in ingredients_by_name
                                      if k.startswith(prefix + " ") and re.search(r"(OIL|EXTRACT|ABSOLUTE)$", k)}
        # Ek II girdilerinin bir kısmı koşullu yasaktır (ör. petrolatum: "rafinasyon geçmişi bilinmiyorsa").
        # Ürün sayfasında "yasaklı" diye gösterilmemeli; conditional=True ile ayrılır.
        sname = " ".join(map(str, as_list(s.get("inciName")))).lower()
        conditional = "II" in as_list(s.get("annexNo")) and bool(re.search(r"\bexcept\b|\bunless\b|\bif\b", sname))
        # Karışım girdisi ("Citric acid (and) Silver citrate", Ek V): sınır karışıma (gümüşe) aittir,
        # içindeki tek tek maddelere değil. Yalnızca karışımın kendi adıyla eşleşir.
        names = as_list(s.get("inciName")) + as_list(s.get("nameOfCommonIngredientsGlossary"))
        if any("(and)" in str(nm).lower() for nm in names):
            targets &= {norm(nm) for nm in names}
        for t in targets:
            restrictions.setdefault(t, []).append({
                "annex": as_list(s.get("annexNo")), "ref": s.get("refNo"),
                "maxConcentration": s.get("maximumConcentration"),
                "conditional": conditional,
            })
    return allergens, restrictions


def load_fulton():
    out = {}
    for r in csv.DictReader(open(os.path.join(KB, "fulton_1989.csv"), encoding="utf8")):
        if r["inci"]:
            out.setdefault(norm(r["inci"]), (r["comedogenic"], r["irritancy"]))
    return out


def main():
    I = json.load(open(os.path.join(COSING, "ingredients.json"), encoding="utf8"))
    by_name = {norm(i["inciName"]): i for i in I}
    by_id = {str(i["substanceId"]): i for i in I}
    allergens, restrictions = load_substances(by_name, by_id)
    fulton = load_fulton()

    kb = []
    for n, i in by_name.items():
        funcs = as_list(i.get("functionName"))
        classes = classify(n, funcs, allergens)
        com = fulton.get(n, (None, None))
        kb.append({
            "inci": n,
            "cosingId": str(i["substanceId"]),
            "functions": funcs,
            "cas": i.get("casNo"),
            "classes": sorted(classes),
            "fungalAcne": fungal(n, classes),
            "comedogenic": com[0], "irritancy": com[1],
            "restrictions": restrictions.get(n, []),
        })
    os.makedirs(KB, exist_ok=True)
    path = os.path.join(KB, "ingredients_kb.json")
    json.dump(kb, open(path, "w", encoding="utf8"), ensure_ascii=False, separators=(",", ":"))

    cnt = Counter(c for k in kb for c in k["classes"])
    print(f"{len(kb)} madde -> {path} ({os.path.getsize(path) // 1024} KB)")
    print(f"AB alerjeni: {len(allergens)}, kısıtlamalı: {len(restrictions)}, Fulton puanlı: "
          f"{sum(1 for k in kb if k['comedogenic'] is not None)}, fungal akne riski: "
          f"{sum(1 for k in kb if k['fungalAcne'])}")
    for c, v in sorted(cnt.items()):
        print(f"  {c:28} {v}")


if __name__ == "__main__":
    main()
