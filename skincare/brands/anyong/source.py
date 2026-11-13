"""Anyong (anyong.com.tr, ikas/Next.js). Ürün açıklaması sunucu HTML'inde görünmez; `#__NEXT_DATA__` >
props.pageProps.pageSpecificData.description (HTML). İçinde "Nasıl Kullanılır?" ve "İçindekiler" bölümleri.
Ürün listesi: /products.xml. Kullanımdaki genel uyarılar (harici kullanım, çocuklar, gözle temas) talimat sayılmaz."""
import json
import re

from bs4 import BeautifulSoup

import source_common as sc

DOMAIN = "anyong.com.tr"
WARN = re.compile(r"(?i)haricen|harici kullanım|ulaşamayacağı|erişemeyeceği|saklayın|muhafaza|temasından kaçın|temastan kaçın|"
                  r"temas halinde|yaralı|hasarlı|tahriş olmuş|doktor|yaşından küçük|yaş ve altı|yanıcı|ısı kaynak|"
                  r"sağlık riski|sağlık riskleri")
HEAD = r"(?:Neden Anyong\?|İçindekiler|Öne Çıkan İçerikler|Kimler İçin|Nasıl Kullanılır\?|Sıkça Sorulan)"


def description_text(s):
    nd = s.select_one("#__NEXT_DATA__")
    if not nd:
        return ""
    try:
        html = json.loads(nd.text)["props"]["pageProps"]["pageSpecificData"]["description"] or ""
    except (KeyError, TypeError, ValueError):
        return ""
    return re.sub(r"\s+", " ", BeautifulSoup(html, "html.parser").get_text(" | ", strip=True))


def inci(s, main):
    t = description_text(s)
    m = re.search(r"İçindekiler\s*:?\s*\|?\s*([^|]{40,2500})", t)
    if m and m.group(1).count(",") >= 4:
        return [x.strip().rstrip(".").upper() for x in sc.split_inci(sc.clean_text(m.group(1)))], "anyong"


def howto(s):
    t = description_text(s)
    m = re.search(r"Nasıl Kullanılır\?\s*\|\s*(.{15,1500}?)(?=\s\|\s" + HEAD + r"|$)", t)
    if not m:
        return []
    out = []
    for part in m.group(1).split("|"):
        for y in re.split(r"(?<=[.!])\s+", part.strip()):
            y = y.strip()
            if y and not WARN.search(y):
                out.append(y if y.endswith((".", "!")) else y + ".")
    return out
