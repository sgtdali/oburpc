"""Mia Klinika (miaklinika.com, ikas/Next.js). İçerik listesi ve kullanım ürün özniteliklerinde:
`#__NEXT_DATA__` > props.pageProps.pageSpecificData.attributes[] > productAttribute.name "İçindekiler" /
"Nasıl Kullanılır?" (İngilizceleri "ingredients" / "How to use"). Ürün listesi: /products.xml."""
import json
import re

from bs4 import BeautifulSoup

import source_common as sc

DOMAIN = "miaklinika.com"
WARN = re.compile(r"(?i)haricen|harici kullanım|ulaşamayacağı|erişemeyeceği|saklayın|muhafaza|temasından kaçın|"
                  r"temas halinde|yaralı|tahriş olmuş|doktor")


def _attrs(s):
    nd = s.select_one("#__NEXT_DATA__")
    if not nd:
        return {}
    try:
        items = json.loads(nd.text)["props"]["pageProps"]["pageSpecificData"].get("attributes") or []
    except (KeyError, TypeError, ValueError):
        return {}
    return {a["productAttribute"]["name"]: BeautifulSoup(a.get("value") or "", "html.parser").get_text(" ", strip=True)
            for a in items if a.get("productAttribute")}


def inci(s, main):
    v = _attrs(s).get("İçindekiler") or _attrs(s).get("ingredients")
    if v and v.count(",") >= 4:
        return [x.strip().rstrip(".").upper() for x in sc.split_inci(sc.clean_text(v))], "mia-klinika"


def howto(s):
    v = _attrs(s).get("Nasıl Kullanılır?") or ""
    return [x.strip() for x in re.split(r"(?<=[.!])\s+", v) if x.strip() and not WARN.search(x)]
