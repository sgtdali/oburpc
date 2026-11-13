"""Clara Hygienics (clarahygienics.com, Ticimax). Ürün sayfasında "İçerik Listesi: | Aqua, ... ." ve
"Nasıl Kullanılır? | 🔹 ... | 🔹 ... | Kimler İçin Uygundur?". Genel uyarılar (temas, saklama) talimata alınmaz.
Ürün listesi: /sitemap/products/0.xml."""
import re

import source_common as sc

DOMAIN = "clarahygienics.com"
WARN = re.compile(r"(?i)haricen|harici kullanım|ulaşamayacağı|erişemeyeceği|saklayın|muhafaza|temasından kaçın|"
                  r"temas halinde|yaralı|tahriş olmuş|doktor")


def _text(s):
    for x in s.select("script, style"):
        x.decompose()
    return re.sub(r"\s+", " ", s.get_text(" | ", strip=True))


def inci(s, main):
    m = re.search(r"(?:İçerik Listesi|İçindekiler)\s*:?\s*\|\s*([^|]{40,2500})", _text(s))
    if m and m.group(1).count(",") >= 4:
        return [x.strip().rstrip(".").upper() for x in sc.split_inci(sc.clean_text(m.group(1)))], "clara-hygienics"


def howto(s):
    m = re.search(r"Nasıl Kullanılır\??\s*\|\s*(.{10,1500}?)\s*\|\s*(?:Kimler İçin|İçerik Listesi|Neden|Öne Çıkan)", _text(s))
    if not m:
        return []
    out = []
    for x in m.group(1).split("|"):
        x = x.replace("🔹", "").strip()
        if x and not WARN.search(x):
            out.append(x if x.endswith((".", "!")) else x + ".")
    return out
