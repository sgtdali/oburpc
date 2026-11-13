"""Olalab TR (olalab.com.tr, Shopify). Ürün sayfasında "İçindekiler: Aqua, ..." ve "· Kullanımı: <metin> ·"
bölümleri. Kullanım metninin ardından madde işaretsiz tanıtım cümleleri gelir; yalnızca noktayla biten cümleler alınır.
Site sık 429 veriyor: 2026-11-12'de eşleştirme tarayıcıdan yapıldı."""
import re

import source_common as sc

DOMAIN = "olalab.com.tr"


def _text(s):
    for x in s.select("script, style"):
        x.decompose()
    return re.sub(r"\s+", " ", s.get_text(" ", strip=True))


def inci(s, main):
    t = _text(s)
    m = re.search(r"İçindekiler:\s*(.{40,1800}?)(?=\s(?:·|Sülfat içermez|Paraben|Kullanımı)|\.\s|$)", t)
    if m and m.group(1).count(",") >= 4:
        return [x.strip().upper() for x in sc.split_inci(sc.clean_text(m.group(1)))], "olalab"


def howto(s):
    t = _text(s)
    m = re.search(r"Kullanımı:\s*(.{15,600}?)(?=\s·|$)", t)
    if not m:
        return []
    out = []
    for x in re.split(r"(?<=\.)\s+", m.group(1).strip()):
        if not x.endswith("."):
            break
        out.append(x.strip())
    return out
