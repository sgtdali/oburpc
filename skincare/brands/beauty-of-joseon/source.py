"""Beauty of Joseon (beautyofjoseon.com, Shopify, İngilizce global site). Tam içerik listesi sayfa HTML'inde
"Water, ..." ile başlayan virgüllü blok (en uzun olan alınır). Türkçe kullanım talimatı yok."""
import re

import source_common as sc

DOMAIN = "beautyofjoseon.com"


def inci(s, main):
    h = str(s)
    best = ""
    for m in re.finditer(r"(?:Water|Aqua|Oryza Sativa|Propolis|Panax Ginseng)[^<\"]{0,40},[^<\"]{150,4000}", h):
        if len(m.group(0)) > len(best):
            best = m.group(0)
    if best.count(",") >= 4:
        return [x.strip().rstrip(".").upper() for x in sc.split_inci(sc.clean_text(best))], "beauty-of-joseon"


def howto(s):
    return []
