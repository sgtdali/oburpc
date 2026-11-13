"""İçerik listesinden ürün analizi: özellikler, öne çıkan içerikler, faydalar/endişeler, madde etiketleri.

Girdi: etiketteki INCI listesi + kb/ingredients_kb.json (build_kb.py).
Tüm değerlendirmeler BİZİM kurallarımızdır (docs/skincare-veri-kaynaklari.md, bölüm 4).
İleride içerik analiz aracı (kullanıcının yapıştırdığı liste) aynı kuralları kullanacak.

Bilinen sınır: etikette oran yazmaz. Listenin sonundaki %0,1'lik bir madde de "1 içerik" olarak sayılır.
"""
import json, os, re

# Fulton puanları (saf madde, tavşan kulağı) bitmiş ürünü öngörmez; oran belirleyici (Draelos & DiNardo 2006).
# Bu yüzden puana dayalı ürün düzeyindeki uyarılar yalnızca listenin ilk EARLY_POSITION maddesi için verilir.
# app/skincare/_components/IngredientList.tsx aynı sabiti kullanır (lib/skincare/vocab.ts > EARLY_POSITION).
EARLY_POSITION = 7

HERE = os.path.dirname(os.path.abspath(__file__))
KB_PATH = os.path.join(HERE, "kb", "ingredients_kb.json")

# Etikette farklı yazılan yaygın adlar -> CosIng INCI
SYNONYMS = {
    "WATER": "AQUA", "EAU": "AQUA", "AQUA/WATER": "AQUA", "WATER/AQUA": "AQUA", "AQUA/WATER/EAU": "AQUA",
    "FRAGRANCE": "PARFUM", "PARFUM/FRAGRANCE": "PARFUM", "FRAGRANCE/PARFUM": "PARFUM",
    "MINERAL OIL": "PARAFFINUM LIQUIDUM", "VITAMIN E": "TOCOPHEROL", "BEESWAX": "CERA ALBA",
    # nokta norm()'da silinir; CosIng adı noktalı
    "ALCOHOL DENAT": "ALCOHOL DENAT.",
    # marka sitelerindeki yazım hataları (La Roche-Posay TR, 2026-10)
    "POLOXAMER338": "POLOXAMER 338", "XANTHAGUM": "XANTHAN GUM",
    "TRISODIUM ETHYLENEDIAMINEDISUCCINATE": "TRISODIUM ETHYLENEDIAMINE DISUCCINATE",
    # Avène termal suyu CosIng'de ayrı kayıt değil; kaynak suyu olduğu için su sayılır
    "AVENE THERMAL SPRING WATER": "AQUA", "AVENE AQUA": "AQUA",
    "ETHYL ASCORBIC ACID": "3-O-ETHYL ASCORBIC ACID",
    # CeraVe TR yapılandırılmış içerik alanındaki boşluk/yazım hataları (2026-10-05).
    "CELLULOSEGUM": "CELLULOSE GUM",
    "HYDROGENATEDSTYRENE/BUTADIENECOPOLYMER": "HYDROGENATED STYRENE/BUTADIENE COPOLYMER",
    "CERAMIDENP": "CERAMIDE NP",
    "SODIUM LAUROYLLACTYLATE": "SODIUM LAUROYL LACTYLATE",
    "PENTAERYTHRITYL TETRA-DI-T-BUTYLHYDROXYHYDROCINNAMATE": "PENTAERYTHRITYL TETRA-DI-T-BUTYL HYDROXYHYDROCINNAMATE",
    "SODIUMCHLORIDE": "SODIUM CHLORIDE",
    "SODIUMMETHYL COCOYL TAURATE": "SODIUM METHYL COCOYL TAURATE",
    "TRISODIUMETHYLENEDIAMINE DISUCCINATE": "TRISODIUM ETHYLENEDIAMINE DISUCCINATE",
    "POTASSIUM CETYLPHOSPHATE": "POTASSIUM CETYL PHOSPHATE",
    "CAPRYLYLGLYCOL": "CAPRYLYL GLYCOL",
    "BUTYROSPERMUM PARKIIBUTTER": "BUTYROSPERMUM PARKII BUTTER",
    "BENZOICACID": "BENZOIC ACID",
    # Eksik baş harfler aynı sıralı resmî UK formülüyle doğrulandı; TR ham veri korunur.
    "ENTYLENE GLYCOL": "PENTYLENE GLYCOL",
    "ENZOIC ACID": "BENZOIC ACID",
    "IS-ETHYLHEXYLOXYPHENOL METHOXYPHENYL TRIAZINE": "BIS-ETHYLHEXYLOXYPHENOL METHOXYPHENYL TRIAZINE",
    # Bioderma TR: boşluk, tire ve INCI nano etiket varyantları; ham etiket korunur.
    "1,2 HEXANEDIOL": "1,2-HEXANEDIOL", "1,2- HEXANEDIOL": "1,2-HEXANEDIOL",
    "TRIDECYLTRIMELLITATE": "TRIDECYL TRIMELLITATE",
    "CAPRYLIC/CAPRICTRIGLYCERIDE": "CAPRYLIC/CAPRIC TRIGLYCERIDE",
    "LAMINARIAOCHROLEUCA EXTRACT": "LAMINARIA OCHROLEUCA EXTRACT",
    "PROPYLENEGLYCOL": "PROPYLENE GLYCOL",
    "ZINC OXIDE [NANO]": "ZINC OXIDE",
    # Sensibio Eye Contour Gel: aynı sıralı Ask.NAOS TR listesiyle doğrulandı.
    "POLYEHTYLENE": "POLYETHYLENE",
    # L'Oréal Paris, Nivea ve Sinoz TR sitelerindeki yazım hataları (2026-10-05); ham etiket korunur.
    "ALCOHOL DET": "ALCOHOL DENAT.", "SODIUM HYALUROTE": "SODIUM HYALURONATE", "LILOOL": "LINALOOL",
    "ISONONYL ISONONOATE": "ISONONYL ISONONANOATE", "SALYCILIC ACID": "SALICYLIC ACID",
    "TIETHANOLAMINE": "TRIETHANOLAMINE",
    "ARGININE HCI": "ARGININE HCL", "BETAIN": "BETAINE", "HYDROGENETED LECITIN": "HYDROGENATED LECITHIN",
    "SACCHARUM OFFCINARUM EXTRACT": "SACCHARUM OFFICINARUM EXTRACT",
    "SODIUM C14-16 OLEIN SULFONATE": "SODIUM C14-16 OLEFIN SULFONATE",
    # La Roche-Posay TR genişletmesi (2026-10-05). "/" parçasından yanlış eşleşmesin diye (GLYCINE SOJA = soya),
    # eski INCI adı (…TAURAMIDE), yaygın ad (DANDELION) ve bozuk boşluklar.
    "GLYCINE SOJA/SOYBEAN STEROLS": "GLYCINE SOJA STEROLS",
    "AMMONIUM POLYACRYLDIMETHYLTAURAMIDE": "AMMONIUM POLYACRYLOYLDIMETHYL TAURATE",
    "DANDELION RHIZOME/ROOT EXTRACT": "TARAXACUM OFFICINALE RHIZOME/ROOT EXTRACT",
    "SODIUM SA CHARIN": "SODIUM SACCHARIN", "DISODIUMEDTA": "DISODIUM EDTA",
    "ALUMINUMSTARCHOCTENYLSUCCINATE": "ALUMINUM STARCH OCTENYLSUCCINATE",
    # Caudalie TR genişletmesi (2026-10-05): baştaki fazla harf, kırık tire, "GLYCERIL" ve eksik tire.
    "IVITIS VINIFERA (GRAPE) SEED OIL": "VITIS VINIFERA SEED OIL",
    "SODIUM CARBOXYMETHYL BETA- GLUCAN": "SODIUM CARBOXYMETHYL BETA-GLUCAN",
    "POLYGLYCERIL-4 OLEATE": "POLYGLYCERYL-4 OLEATE",
    "COCOCAPRYLATE/CAPRATE": "COCO-CAPRYLATE/CAPRATE", "COCO CAPRYLATE/CAPRATE": "COCO-CAPRYLATE/CAPRATE",
    # Güneş koruyucuları (2026-11-02): Avène noktalı ayracı "4-OXOTHIAZOLIDINE"i "4. OXOTHIAZOLIDINE" diye böldü
    # (CosIng adı OXOTHIAZOLIDINE); Caudalie'nin üç dilli mum adı; LRP'de düşmüş "E"; LRP'nin AB'de iki adla
    # yazılan kopolimeri (CosIng'de birleşik kayıt yok, AMMONIUM POLYACRYLOYLDIMETHYL TAURATE adıyla kayıtlı).
    "4 OXOTHIAZOLIDINE": "OXOTHIAZOLIDINE",
    "CANDELLILA CERA/EUPHORBIA CERIFERA (CANDELILLA) WAX/CIRE DE CANDELILLA": "EUPHORBIA CERIFERA CERA",
    "CYCLOH XASILOXANE": "CYCLOHEXASILOXANE",
    "BRASSICA CAMPESTRIS/ALEURITES FORDII OIL COPOLYMER": "BRASSICA CAMPESTRIS/ALEURITES FORDI OIL COPOLYMER",
    "AMMONIUM POLYACRYLDIMETHYLTAURAMIDE/AMMONIUM POLYACRYLOYLDIMETHYL TAURATE": "AMMONIUM POLYACRYLOYLDIMETHYL TAURATE",
    # Ortağın 2026-11-10/11'de doğrudan DB'ye yazdığı 85 ürün veri hattına alınırken (2026-11-13): marka TR
    # sitelerindeki yazım hataları; DB'deki listede ortak bunları elle düzeltmişti.
    "CAPRVLYL GLYCOL": "CAPRYLYL GLYCOL",                                              # L'Oréal
    "PENTAERYTHRITYL TETRA-DI-T-BUTYLI HYDROXYHYDROCINNAMATE":
        "PENTAERYTHRITYL TETRA-DI-T-BUTYL HYDROXYHYDROCINNAMATE",                      # L'Oréal
    "PENTAERYTHRITYL TETRA-DI-T-BUTYL HYDROXYHYDROCINMATE":
        "PENTAERYTHRITYL TETRA-DI-T-BUTYL HYDROXYHYDROCINNAMATE",                      # L'Oréal
    "POTASSIUM CETYLY PHOSPHATE": "POTASSIUM CETYL PHOSPHATE",                         # L'Oréal
    "PEG-60 HYDROGETED CASTOR OIL": "PEG-60 HYDROGENATED CASTOR OIL",                  # L'Oréal
    "ALUMINUM STARCH OCTENYLSUCCITE": "ALUMINUM STARCH OCTENYLSUCCINATE",               # L'Oréal
    "TRITICUM VULGARE GERM OIT": "TRITICUM VULGARE GERM OIL",                          # Mia Klinika
    "DEBHYDROACETIC ACID": "DEHYDROACETIC ACID",                                       # Mia Klinika
    "ROSMARINUS OICINALIS LEAF EXTRACT": "ROSMARINUS OFFICINALIS LEAF EXTRACT",         # Sinoz
}
# "/" ya da parantez parçasından YANLIŞ maddeye bağlananlar (2026-11-11 denetimi): çapraz polimer dimetikon
# sayılıyordu; CI numarasıyla yazılan titanyum dioksit boyadır, UV filtresi kaydına bağlanıyordu.
SYNONYMS.update({
    "DIMETHICONE/VINYLDIMETHICONE CROSSPOLYMER": "DIMETHICONE/VINYL DIMETHICONE CROSSPOLYMER",
    "CI 77 891 (TITANIUM DIOXIDE)": "CI 77891",
})
# Kaynak sayfada virgülü düşmüş, ama ilk parçası tek başına çözüldüğü için repair()'in yakalayamadığı girdiler:
# ikinci madde sessizce kayboluyordu. Ham liste korunur; ayrım burada yapılır.
SPLITS = {
    "SQUALANE/ASCORBYL GLUCOSIDE": ["SQUALANE", "ASCORBYL GLUCOSIDE"],                 # Nivea (Gratis)
    "FRAGRANCE (PARFUM)PHENOXYETHANOL": ["PARFUM", "PHENOXYETHANOL"],                  # Avène
    "IRON OXIDES (CI 77492) (CI 77491) (CI 77499)": ["CI 77492", "CI 77491", "CI 77499"],  # Avène
    "IRON OXIDES (CI 77492). (CI 77491)": ["CI 77492", "CI 77491"],                    # Avène
}
# Gratis ürün sayfalarındaki yazım hataları (staging/<marka>/synonyms.json'dan merge sırasında toplanır; 2026-11)
_GRATIS_SYN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "synonyms_gratis.json")
if os.path.exists(_GRATIS_SYN):
    SYNONYMS.update(json.load(open(_GRATIS_SYN, encoding="utf8")))


def norm(s):
    return re.sub(r"\s+", " ", (s or "").strip().strip(".").upper())


def split_inci(text):
    """'AQUA/WATER, GLYCERIN, ... (Code F.I.L D213768/2)' -> ['AQUA/WATER', 'GLYCERIN', ...]"""
    text = re.sub(r"\(code[^)]*\)|\[[^\]]*\]|may contain.*$|\+/-.*$", "", text, flags=re.I)
    parts = [p.strip().rstrip(".").strip() for p in re.split(r",(?![^()]*\))", text)]
    return [p for p in parts if p and len(p) < 200]


class Analyzer:
    def __init__(self, kb_path=KB_PATH):
        self.kb = {k["inci"]: k for k in json.load(open(kb_path, encoding="utf8"))}

    def resolve(self, raw):
        """Etiketteki adı veritabanındaki INCI'ye bağla; bulunamazsa None."""
        n = norm(raw)
        candidates = [n, SYNONYMS.get(n), re.sub(r"\s*\([^)]*\)", "", n)]  # "(NANO)", "(AND)" gibi ekler
        candidates.append(re.sub(r"\s*\[[^\]]*\]", "", n))                  # AB etiketindeki "[NANO]" eki
        candidates += [norm(p) for p in n.split("/")]                        # "AQUA/WATER" -> AQUA
        candidates += [norm(p) for p in re.findall(r"\(([^)]*)\)", n)]       # "GREEN 5 (CI 61570)" -> CI 61570
        for c in candidates:
            c = SYNONYMS.get(c, c) if c else c
            if c and c in self.kb:
                return self.kb[c]
        # Sitede bozulmuş boşluklar: "G L Y C E R I N", "SODIUM SA CHARIN", "SODIUMBENZOATE" -> boşluksuz birebir eşleşme
        for c in candidates:
            k = self._compact().get(re.sub(r"[^A-Z0-9]", "", c or ""))
            if k:
                return self.kb[k]
        return None

    def _compact(self):
        if not hasattr(self, "_compact_idx"):
            idx = {}
            for k in self.kb:
                idx.setdefault(re.sub(r"[^A-Z0-9]", "", k), k)
            self._compact_idx = idx
        return self._compact_idx

    def exact(self, raw):
        """Etiket adı veritabanında birebir (eşanlam ya da yalnızca boşluk farkıyla) var mı? '/' ve parantez
        parçalarına bölerek eşleştirme sayılmaz; liste onarımında yanlış birleştirme yapılmasın diye."""
        n = norm(raw)
        n = SYNONYMS.get(n, n)
        return n in self.kb or re.sub(r"[^A-Z0-9]", "", n) in self._compact()

    def repair(self, inci_list):
        """Marka sitesindeki virgül hataları; ham liste korunur, onarım burada ve her seferinde aynı yapılır:
        - yanlış yerden bölünmüş madde: "PEG-200", "HYDROGENATED GLYCERYL PALMATE" -> birleşik ad veritabanında
          birebir varsa ve parçalardan biri tek başına birebir değilse birleştirilir
        - virgülü düşmüş iki madde: "SODIUM HYALURONATE RETINOL" -> tanınmıyorsa ve iki birebir ada ayrılıyorsa ayrılır"""
        out, i = [], 0
        while i < len(inci_list):
            cur = inci_list[i]
            if norm(cur) in SPLITS:
                out += SPLITS[norm(cur)]
                i += 1
                continue
            nxt = inci_list[i + 1] if i + 1 < len(inci_list) else None
            # Çıplak "PEG-7" / "PPG-26" pratikte bileşik adın baş kısmıdır ("PEG-7 GLYCERYL COCOATE"); tek başına
            # madde olarak da kayıtlı olduğundan ayrıca ele alınır.
            prefix = re.fullmatch(r"(PEG|PPG)-\d+", norm(cur)) is not None
            if nxt is not None and self.exact(f"{cur} {nxt}") and (prefix or not (self.exact(cur) and self.exact(nxt))):
                out.append(f"{cur} {nxt}")
                i += 2
                continue
            # Tek girdide birden çok pigment: "IRON OXIDES (CI 77492,CI 77491,CI 77499)" -> her CI kodu ayrı madde
            group = re.fullmatch(r"[^(]*\(([^)]*,[^)]*)\)", norm(cur))
            if group and self.resolve(cur) is None:
                codes = [p.strip() for p in group.group(1).split(",")]
                if all(self.exact(p) for p in codes):
                    out += codes
                    i += 1
                    continue
            if self.resolve(cur) is None:
                w = norm(cur).split()
                parts = next(([" ".join(w[:k]), " ".join(w[k:])] for k in range(1, len(w))
                              if self.exact(" ".join(w[:k])) and self.exact(" ".join(w[k:]))), None)
                if parts:
                    out += parts
                    i += 1
                    continue
            out.append(cur)
            i += 1
        return out

    # ---------- madde düzeyi ----------

    @staticmethod
    def _rmin(r):
        """Uyarı eşiği için ALT değer: Fulton'da "0-3" = ham madde kaynağına göre değişir; tek başına
        uyarı sebebi değil. "3(1)" = rafine yağda 1 -> parantez dışı değer alınır."""
        if r is None:
            return None
        m = re.findall(r"\d", re.sub(r"\(.*?\)", "", str(r)))
        return int(m[0]) if m else None

    def tags(self, k):
        """Madde etiketleri (lib/skincare/vocab.ts > INGREDIENT_TAGS anahtarları)."""
        c, n, t = set(k["classes"]), k["inci"], []
        com, irr = self._rmin(k["comedogenic"]), self._rmin(k["irritancy"])
        A = lambda g: f"active:{g}" in c
        # bilgi
        for cls, tag in [("active:ceramide", "ceramide"), ("active:hyaluronic-acid", "hyaluronic-acid"),
                         ("active:niacinamide", "niacinamide"), ("active:retinoid", "retinoid"),
                         ("active:vitamin-e", "vitamin-e"), ("active:aha", "aha"), ("active:bha", "bha"),
                         ("antioxidant", "antioxidant"), ("silicone", "silicon"), ("paraben", "paraben"),
                         ("plant-oil", "oil"), ("mineral-oil", "oil"), ("drying-alcohol", "alcohol"),
                         ("fatty-alcohol", "fatty-alcohol"), ("preservative", "preservative"),
                         ("fragrance", "fragrance-ingredient")]:
            if cls in c and tag not in t:
                t.append(tag)
        # olumlu
        if "humectant" in c or A("hyaluronic-acid") or A("urea"):
            t.append("helps-hydrate-dry-skin")
        if A("ceramide") or A("niacinamide") or A("panthenol") or n in ("CHOLESTEROL", "PHYTOSPHINGOSINE"):
            t.append("good-for-barrier-repair")
        if A("retinoid") or A("peptide") or A("vitamin-c") or A("bakuchiol"):
            t.append("helps-with-anti-aging")
        if A("centella") or A("azelaic-acid") or A("niacinamide") or A("allantoin"):
            t.append("helps-reduce-skin-redness")
        if "soothing" in c or A("allantoin") or A("panthenol") or A("centella"):
            t.append("helps-reduce-irritation")
        if A("vitamin-c") or A("niacinamide") or A("azelaic-acid") or A("brightener"):
            t.append("helps-brighten-skin")
            t.append("good-for-dark-spots")
        if A("bha") or A("azelaic-acid") or A("retinoid") or n in ("SULFUR", "ZINC PCA"):
            t.append("helps-fight-acne")
        if A("bha") or A("niacinamide") or n in ("ZINC PCA", "KAOLIN", "BENTONITE"):
            t.append("good-for-oily-skin")
        if A("bha") or A("niacinamide") or A("retinoid"):
            t.append("good-for-minimizing-pores")
        if A("aha") or A("bha") or A("pha") or A("retinoid") or "exfoliant" in c:
            t.append("good-for-skin-texture")
        if A("centella") or A("panthenol") or A("allantoin") or A("retinoid"):
            t.append("good-for-scar-healing")
        # Fulton puanları: madde düzeyinde sadece bilgi; uyarıya dönüşmesi üründeki konuma bağlı (analyze())
        if com is not None and com >= 3:
            t.append("high-comedogenic-rating")
        if irr is not None and irr >= 3:
            t.append("high-irritancy-rating")
        # olumsuz (konumdan bağımsız: düşük oranda da etkili olabilen maddeler)
        if k["fungalAcne"] == "trigger":
            t.append("not-safe-for-fungal-acne")
        if "eu-allergen" in c:
            t.append("eu-allergen")
        if "eu-allergen" in c or "essential-oil" in c or A("retinoid") or A("aha") or "drying-alcohol" in c:
            t.append("may-cause-irritation")
        if "drying-alcohol" in c or "sulfate" in c:
            t.append("can-worsen-dry-skin")
        if "plant-oil" in c or "mineral-oil" in c:
            t.append("may-worsen-oily-skin")
        if "fragrance" in c or "essential-oil" in c or "drying-alcohol" in c or A("retinoid") or A("aha") \
                or n == "MENTHOL":
            t.append("may-worsen-rosacea")
        if "fragrance" in c or "sulfate" in c or "drying-alcohol" in c:
            t.append("may-worsen-eczema")
        if "reef-unsafe" in c:
            t.append("non-reef-safe")
        return list(dict.fromkeys(t))

    # ---------- ürün düzeyi ----------

    BENEFIT_TAGS = {
        "hydrating": "helps-hydrate-dry-skin", "barrier-repair": "good-for-barrier-repair",
        "anti-aging": "helps-with-anti-aging", "redness-reducing": "helps-reduce-skin-redness",
        "reduces-irritation": "helps-reduce-irritation", "brightening": "helps-brighten-skin",
        "dark-spots": "good-for-dark-spots", "acne-fighting": "helps-fight-acne",
        "good-for-oily-skin": "good-for-oily-skin", "reduces-large-pores": "good-for-minimizing-pores",
        "skin-texture": "good-for-skin-texture", "scar-healing": "good-for-scar-healing",
    }
    CONCERN_TAGS = {
        "may-trigger-acne": "bad-for-acne-prone-skin", "may-worsen-oily-skin": "may-worsen-oily-skin",
        "may-worsen-dryness": "can-worsen-dry-skin", "may-worsen-irritation": "may-cause-irritation",
        "may-worsen-rosacea": "may-worsen-rosacea", "may-worsen-eczema": "may-worsen-eczema",
    }
    KEY_GROUP_ORDER = ["ceramide", "retinoid", "niacinamide", "vitamin-c", "aha", "bha", "pha", "azelaic-acid",
                       "hyaluronic-acid", "peptide", "centella", "panthenol", "bakuchiol", "vitamin-e", "urea",
                       "squalane", "allantoin", "brightener"]

    MINERAL_FILTERS = {"ZINC OXIDE", "TITANIUM DIOXIDE"}

    def analyze(self, inci_list, rinse_off=False, sunscreen=False):
        items, unknown = [], []
        for raw in self.repair(inci_list):
            k = self.resolve(raw)
            if k is None:
                unknown.append(raw)
            items.append({"raw": raw, "kb": k, "tags": self.tags(k) if k else []})
        # Ürün düzeyi etiketler: Fulton'a dayalı uyarılar yalnızca ilk EARLY_POSITION maddede (yüksek oran ihtimali).
        # Fulton testleri cilde bırakılan uygulamayla yapıldı; durulanan üründe (rinse_off: temizleyici, peeling,
        # maske) komedojenlik puanı uyarıya dönüşmez, madde düzeyinde bilgi olarak kalır.
        for pos, i in enumerate(items):
            i["productTags"] = list(i["tags"])
            if i["kb"] and pos < EARLY_POSITION:
                if "high-comedogenic-rating" in i["tags"] and not rinse_off:
                    i["productTags"] += ["bad-for-acne-prone-skin", "may-worsen-oily-skin"]
                if "high-irritancy-rating" in i["tags"]:
                    i["productTags"].append("may-cause-irritation")
            i["productTags"] = list(dict.fromkeys(i["productTags"]))
        known = [i for i in items if i["kb"]]
        classes = [set(i["kb"]["classes"]) for i in known]
        has = lambda cls: any(cls in c for c in classes)
        any_tag = lambda tag: sum(tag in i["productTags"] for i in known)

        # Her özellik: hangi maddeler "içerir" sonucunu doğuruyor. ok=False iken "ingredients" bu maddelerin
        # slug'larını (build_data.py ile aynı kural) etiket sırasıyla taşır; ürün sayfası gerekçe olarak gösterir.
        slug = lambda s: re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
        rules = {
            "alcohol": lambda i: "drying-alcohol" in i["kb"]["classes"],
            "allergen": lambda i: "eu-allergen" in i["kb"]["classes"],
            "fragrance": lambda i: "fragrance" in i["kb"]["classes"],
            "paraben": lambda i: "paraben" in i["kb"]["classes"],
            "sulfate": lambda i: "sulfate" in i["kb"]["classes"],
            "reef": lambda i: "reef-unsafe" in i["kb"]["classes"],
            "oil": lambda i: bool({"plant-oil", "mineral-oil", "essential-oil"} & set(i["kb"]["classes"])),
            "silicone": lambda i: "silicone" in i["kb"]["classes"],
            "fungal": lambda i: i["kb"]["fungalAcne"] == "trigger",
            "acne_trigger": lambda i: "bad-for-acne-prone-skin" in i["productTags"],
            # "cruelty" ve "vegan" içerikten hesaplanamaz -> bilinçli olarak yok
        }
        attributes = []
        for key, hit in rules.items():
            causes = list(dict.fromkeys(slug(i["kb"]["inci"]) for i in known if hit(i)))
            attributes.append({"key": key, "ok": not causes, **({"ingredients": causes} if causes else {})})
        groups = []
        # Güneş koruyucularda filtre türü: çinko oksit / titanyum dioksit mineral, diğer UV filtreleri kimyasal; ikisi
        # birden varsa ürün iki grubu da alır (hibrit). "(CI 77891)" diye yazılan titanyum dioksit renklendiricidir,
        # filtre sayılmaz. Yalnızca SPF'li ürünlerde: başka ürünlerde UV emici, formülü korumak için bulunabilir.
        if sunscreen:
            uv = [i for i in known if "uv-filter" in i["kb"]["classes"] and "CI 77891" not in norm(i["raw"])]
            if any(i["kb"]["inci"] in self.MINERAL_FILTERS for i in uv):
                groups.append("uv-mineral")
            if any(i["kb"]["inci"] not in self.MINERAL_FILTERS for i in uv):
                groups.append("uv-chemical")
        for i in known:  # etiketteki sıraya göre ilk görünen grup önce
            for c in i["kb"]["classes"]:
                if c.startswith("active:") and c[7:] not in groups:
                    groups.append(c[7:])
        if sum("antioxidant" in c for c in classes) >= 2 and "antioxidants" not in groups:
            groups.append("antioxidants")

        def counts(mapping):
            out = [{"key": k, "count": any_tag(t)} for k, t in mapping.items()]
            return sorted([o for o in out if o["count"]], key=lambda o: -o["count"])

        return {
            "ingredients": items,
            "unknown": unknown,
            "attributes": attributes,
            "keyIngredientGroups": groups,
            "benefits": counts(self.BENEFIT_TAGS),
            "concerns": counts(self.CONCERN_TAGS),
        }


if __name__ == "__main__":
    import sys
    a = Analyzer()
    r = a.analyze(split_inci(sys.stdin.read()))
    print("bilinmeyen:", r["unknown"])
    print("özellikler:", [(x["key"], x["ok"]) for x in r["attributes"]])
    print("öne çıkan:", r["keyIngredientGroups"])
    print("faydalar:", [(b["key"], b["count"]) for b in r["benefits"]])
    print("endişeler:", [(c["key"], c["count"]) for c in r["concerns"]])
    for i in r["ingredients"]:
        print(f'  {i["raw"]:35} {",".join(i["tags"])}')
