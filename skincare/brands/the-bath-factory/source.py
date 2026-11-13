"""The Bath Factory (thebathfactory.com). Ürün sayfasında içerik listesi başlıksız, "Aqua, Paraffinum Liquidum, ... ." diye
ayrı bir bölüm; kullanım talimatı yok. Ürün listesi: /sitemap.xml (-p ile biten adresler)."""
import re

import source_common as sc

DOMAIN = "thebathfactory.com"


def inci(s, main):
    for x in s.select("script, style"):
        x.decompose()
    t = re.sub(r"\s+", " ", s.get_text(" | ", strip=True))
    m = re.search(r"\|\s*((?:Aqua|AQUA|Water)\b[^|]{40,2500}?)\.?\s*\|", t)
    if m and m.group(1).count(",") >= 4:
        return [x.strip().rstrip(".").upper() for x in sc.split_inci(sc.clean_text(m.group(1)))], "the-bath-factory"


def howto(s):
    return []
