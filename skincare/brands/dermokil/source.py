"""Dermokil TR (dermokil.com, Shopify). Ürün sayfasında "İçindekiler Aqua, Propylene Glycol, ..." ve
"Nasıl Kullanılır <metin> Aktif İçerik" bölümleri. Site sık 429 veriyor: fetch_sources.py yavaş çalıştırılmalı
(2026-11-12'de eşleştirme tarayıcıdan yapıldı)."""
import re

import source_common as sc

DOMAIN = "dermokil.com"
NEXT = r"(?:Uyarı|Saklama|Paylaş|Yorum|Değerlendir|Sıkça|Benzer|Etiket Bilgisi|Menşei|Nasıl Kullanılır|Aktif İçerik)"


def _text(s):
    for x in s.select("script, style"):
        x.decompose()
    return re.sub(r"\s+", " ", s.get_text(" ", strip=True))


def inci(s, main):
    t = _text(s)
    m = re.search(r"İçindekiler (.{40,1800}?)(?= " + NEXT + r"|$)", t)
    if m and m.group(1).count(",") >= 4:
        return [x.strip().upper() for x in sc.split_inci(sc.clean_text(m.group(1)))], "dermokil"


def howto(s):
    t = _text(s)
    m = re.search(r"Nasıl Kullanılır (.{15,600}?)(?= (?:Aktif İçerik|İçindekiler|Etiket Bilgisi|Uyarı)|$)", t)
    if not m:
        return []
    return [x.strip().rstrip(".") + "." for x in re.split(r"(?<=\.)\s+", m.group(1).strip()) if x.strip(" .")]
