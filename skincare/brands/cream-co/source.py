"""Cream Co (creamco.com.tr, Shopify). Ürün sayfasında "Kullanım <talimat> [Öne Çıkan İçerikler ...] İçindekiler Aqua, ...".
Listenin sonunda nokta yok, ardından rozet metinleri ("DERMATOLOGICALLY TESTED ...") bitişik geliyor; liste büyük harfli
rozet sözcüğünde kesilir. Talimattan tanıtım notları ("Mükemmel bir makyaj bazıdır") alınmaz.
Site Python isteklerine 429 veriyor (2026-11-12 tarayıcıdan okundu)."""
import re

import source_common as sc

DOMAIN = "creamco.com.tr"
PROMO = re.compile(r"(?i)makyaj bazı|cam cilt|uygundur\.?$")


def _text(s):
    for x in s.select("script, style"):
        x.decompose()
    return re.sub(r"\s+", " ", s.get_text(" ", strip=True))


def inci(s, main):
    t = _text(s)
    m = re.search(r"İçindekiler\s+(.{40,3000}?)(?=\s?(?:Dermatologically|DERMATOLOGICALLY|Ophthalmologically)|\.\s|$)", t)
    if m and m.group(1).count(",") >= 4:
        return [x.strip().rstrip(".").upper() for x in sc.split_inci(sc.clean_text(m.group(1)))], "cream-co"


def howto(s):
    t = _text(s)
    m = re.search(r"Kullanım\s+(.{10,800}?)(?=\s(?:Öne Çıkan İçerikler|İçindekiler))", t)
    if not m:
        return []
    out = []
    for x in re.split(r"(?<=[.!])\s*", m.group(1)):
        x = re.sub(r"^Not:\s*", "", x.strip())
        if x and not PROMO.search(x):
            out.append(x if x.endswith((".", "!")) else x + ".")
    return out
