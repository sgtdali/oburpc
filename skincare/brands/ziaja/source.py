"""Ziaja (Polonya). ziaja.com.tr markanın uluslararası İngilizce sitesine (en.ziaja.com) yönleniyor; Türkiye'de satılan
ürünler orada aynı INCI ile listeleniyor (2026-11-12: 20 Gratis ürününün 20'si birebir aynı madde kümesi).
İçerik listesi sayfa metninde "INCI" başlığından sonraki blokta ("Aqua (Water), Ethylhexyl Salicylate, ...").
"How to use" İngilizce olduğu için kullanım talimatı alınmıyor (Türkçe kaynak yok)."""
import re

import source_common as sc

DOMAIN = "ziaja.com"


def inci(s, main):
    t = s.get_text(" | ", strip=True)
    m = re.search(r"\| INCI \| ([^|]{40,})", t)
    if m and m.group(1).count(",") >= 5:
        return [x.strip().upper() for x in sc.split_inci(sc.clean_text(m.group(1)))], "ziaja"


def howto(s):
    return []
