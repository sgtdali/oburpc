"""Calliel (calliel.com.tr, Shopify). İçerik listesi ürün metafield'ında, sayfada "İçindekiler İÇİNDEKİLER/INGREDIENTS
Aqua, ..." (başlık sırası ve iki nokta değişken). Sayfadaki kullanım metinlerinde kelimeler bitişik yazılmış
("Yeterlimiktarda"), kullanım talimatı alınmıyor. Site Python isteklerine 429 veriyor (2026-11-12 tarayıcıdan okundu)."""
import re

import source_common as sc

DOMAIN = "calliel.com.tr"


def inci(s, main):
    for x in s.select("script, style"):
        x.decompose()
    t = re.sub(r"\s+", " ", s.get_text(" ", strip=True))
    m = re.search(r"(?:INGREDIENTS\s*/\s*İÇİNDEKİLER|İÇİNDEKİLER\s*/\s*INGREDIENTS)\s*:?\s*(.{40,2200}?)"
                  r"(?=\.\s|\s(?:Kargom ne zaman|Nasıl kullanılır|NASIL KULLANILIR|Kullanım)|$)", t)
    if m and m.group(1).count(",") >= 4:
        return [x.strip().rstrip(".").upper() for x in sc.split_inci(sc.clean_text(m.group(1)))], "calliel"


def howto(s):
    return []
