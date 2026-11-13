"""Cosmogenesis Labs (cosmogenesislabs.com, Shopify). Ürün açıklamasında "İçerik Listesi: Aqua, ..." ve
"Nasıl Kullanılır? 🔹 ... 🔹 ..." maddeleri. Kullanımdaki genel uyarılar (haricen kullanılır, çocukların ulaşamayacağı
yer, gözle temas) talimat sayılmaz. Shopify `/products/<handle>.json > body_html` aynı metni verir."""
import re

import source_common as sc

DOMAIN = "cosmogenesislabs.com"
WARN = re.compile(r"(?i)haricen|harici kullanım|ulaşamayacağı|erişemeyeceği|saklayın|muhafaza|temastan kaçın|temas halinde|"
                  r"temas ettirmeyin|yaralı|tahriş olmuş|doktor|güneş ışığına maruz bırakmayın|kimlik")


def _text(s):
    for x in s.select("script, style"):
        x.decompose()
    return re.sub(r"\s+", " ", s.get_text(" ", strip=True))


def inci(s, main):
    t = _text(s)
    m = re.search(r"(?:İçerik Listesi|İçerik Detayları|İçindekiler)\s*:?\s*(.{40,2500}?)(?=\.\s|\s[✨💧🌿🔹✅]|$)", t)
    if m and m.group(1).count(",") >= 4:
        return [x.strip().rstrip(".").upper() for x in sc.split_inci(sc.clean_text(m.group(1)))], "cosmogenesis"


def howto(s):
    t = _text(s)
    m = re.search(r"Nasıl Kullanılır\??\s*(.{15,1500}?)(?=\s(?:Hangi Cilt Tipleri|Kimler İçin|İçerik Listesi|İçerik Detayları|Neden|Öne Çıkan)|$)", t)
    if not m:
        return []
    out = []
    for x in re.split(r"\s*🔹\s*", m.group(1)):
        x = re.sub(r"\s+", " ", x.replace("⚠", "")).strip(" |")
        if not x:
            continue
        # bir madde içinde talimat + uyarı birlikte olabilir: cümleleri ayır, uyarıları at
        sents = [y for y in re.split(r"(?<=[.!])\s+", x) if y and not WARN.search(y)]
        if sents:
            y = " ".join(sents)
            out.append(y if y.endswith((".", "!")) else y + ".")
    return out
