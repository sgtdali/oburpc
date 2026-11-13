"""SKIN1004 (skin1004.com, Shopify, İngilizce global site). Tam içerik listesi sayfa JSON'unda
"product_info_tab_3_full_ingredients" > "value". Türkçe kullanım talimatı yok. Site Python isteklerine sık 429 veriyor
(2026-11-12'de tarayıcıdan okundu)."""
import json
import re

import source_common as sc

DOMAIN = "skin1004.com"


def inci(s, main):
    h = str(s)
    i = h.find("product_info_tab_3_full_ingredients")
    if i < 0:
        return None
    m = re.search(r'"value":"((?:[^"\]|\.)*)"', h[i:i + 8000])
    if not m:
        return None
    v = re.sub(r"\(\s*[\d.,]+\s*(?:ppm|ppb|%)\s*\)", "", json.loads('"' + m.group(1) + '"'), flags=re.I)
    if v.count(",") >= 4:
        return [x.strip().rstrip(".").upper() for x in sc.split_inci(sc.clean_text(v))], "skin1004"


def howto(s):
    return []
