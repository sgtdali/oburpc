"""Rimu Health TR (rimuhealthproducts.com). İçerik listesi ürün açıklamasında "Ingredients: Aqua (Water), ..." satırında.
Sayfadaki kullanım metinleri yazım hatalı ("uygulayanız", "Etkilisonuçlar") olduğu için kullanım talimatı alınmıyor.
2026-11-12: 7 Gratis ürünü bu sitedeki sayfayla eşlendi (Sebum Control toniğinde marka listesi Gratis'ten farklı:
at kestanesi ve hidrolize sodyum hyalüronat var, yeşil çay yok; marka listesi esas)."""
import re

import source_common as sc

DOMAIN = "rimuhealthproducts.com"


def inci(s, main):
    t = s.get_text(" | ", strip=True)
    m = re.search(r"(?:Ingredients|INGREDIENTS|İçindekiler|İçerikler|İçerik)\s*:\s*\|?\s*([^|]{40,})", t)
    if m and m.group(1).count(",") >= 4:
        return [x.strip().rstrip(";").upper() for x in sc.split_inci(sc.clean_text(m.group(1)))], "rimu"


def howto(s):
    return []
