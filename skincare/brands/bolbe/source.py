"""Bolbe (bolbeskincare.com, Ticimax). Ürün sayfasında "Kullanımı | • ... | Uyarılar | • ..." ve
"İçindekiler: | Aqua, ...". Ürün listesi: /sitemap/products/0.xml. Uyarılar bölümü talimata alınmaz.
Listede art arda tekrarlanan madde (ör. Sodium Ascorbyl Phosphate iki kez) tek yazılır."""
import re

import source_common as sc

DOMAIN = "bolbeskincare.com"


def _text(s):
    for x in s.select("script, style"):
        x.decompose()
    return re.sub(r"\s+", " ", s.get_text(" | ", strip=True))


def inci(s, main):
    t = _text(s)
    m = re.search(r"İçindekiler\s*:?\s*\|\s*([^|]{40,2500})", t)
    if m and m.group(1).count(",") >= 4:
        out = []
        for x in sc.split_inci(sc.clean_text(m.group(1))):
            x = x.strip().rstrip(".").upper()
            if x and (not out or out[-1] != x):
                out.append(x)
        return out, "bolbe"


def howto(s):
    t = _text(s)
    m = re.search(r"Kullanımı\s*\|\s*(.{10,1200}?)\s*\|\s*(?:Uyarılar|İçindekiler)", t)
    if not m:
        return []
    out = []
    for x in m.group(1).split("|"):
        x = x.strip(" •").strip()
        if x:
            out.append(x if x.endswith((".", "!")) else x + ".")
    return out
