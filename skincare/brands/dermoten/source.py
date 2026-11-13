"""Dermoten (dermoten.com, Ticimax). Ürün sekmesinde bölümler "|" ile ayrılıyor; sıra sayfadan sayfaya değişiyor
("Nasıl Kullanılır? | İçindekiler | <tanıtım> | ... | Aqua, ... | <kullanım> | Uyarılar: | ..." ya da kullanım
"Uyarılar:" ile aynı bölümde). Liste: en az 5 virgüllü, Türkçe harf içermeyen ilk bölüm. Kullanım: "uygulan/kullanılır"
fiilli, tanıtım iddiası (klinik, kanıtlan, test edilmiş) içermeyen bölüm; "Uyarılar:" sonrası alınmaz.
Ürün listesi: /sitemap/products/0.xml."""
import re

import source_common as sc

DOMAIN = "dermoten.com"
TR = re.compile(r"[çğıöşüÇĞİÖŞÜ]")
VERB = re.compile(r"(?i)uygula|kullanılır|kullanın|sürün|masaj|durula")
PROMO = re.compile(r"(?i)klinik|kanıtlan|test edilmiş|sertifika|GMP|ISO|etkili olduğu|%\d+ azal")
WARN = re.compile(r"(?i)temasından kaçın|temas halinde|ulaşamayacağı|saklayın|muhafaza|haricen|tahriş")


def _segments(s):
    for x in s.select("script, style"):
        x.decompose()
    t = re.sub(r"\s+", " ", s.get_text(" | ", strip=True))
    a = t.find("Nasıl Kullanılır?")
    if a < 0:  # bazı sayfalarda sekme başlığı yok: ürün alanı "Ürün Açıklaması"/ürün adından başlar
        a = max(t.find("Ürün Açıklaması"), 0)
    b = t.find("Etiketler", a)
    if b < 0:
        b = t.find("Ücretsiz Kargo", a)
    return [x.strip() for x in t[a:b if b > a else a + 8000].split("|") if x.strip()]


START = re.compile(r"\b(?:Aqua|AQUA|Water|WATER|Caprylic|CAPRYLIC|Helianthus|HELIANTHUS|Cera |CERA |Cocos|COCOS|Prunus|"
                   r"PRUNUS|Olea|OLEA|Glycerin|GLYCERIN|Butyrospermum|BUTYROSPERMUM|Ethylhexyl|ETHYLHEXYL|Isododecane|"
                   r"Simmondsia|SIMMONDSIA|Paraffinum|PARAFFINUM|Rosa |ROSA )")


def inci(s, main):
    for seg in _segments(s):
        m = START.search(seg)
        if not m:
            continue
        body = re.split(r"\.\s|\.$", seg[m.start():])[0]
        if body.count(",") >= 4 and not TR.search(body):
            return [x.strip().rstrip(".").upper() for x in sc.split_inci(sc.clean_text(body))], "dermoten"


def howto(s):
    for seg in _segments(s):
        seg = re.split(r"Uyarılar\s*:", seg)[0].strip()
        if seg.endswith("?") or len(seg) < 25:
            continue
        if len(seg) < 600 and VERB.search(seg) and not PROMO.search(seg) and seg.count(",") < 5:
            out = [x.strip() for x in re.split(r"(?<=[.!])\s+", seg) if x.strip() and not WARN.search(x)]
            if out:
                return out
    return []
