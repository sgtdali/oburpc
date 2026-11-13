"""Thalia Natural Beauty (thalia.com.tr, Shopify). İçerik listesi kapalı akordeonda: "Tam İçerik (INCI) AQUA(WATER), ...".
Kullanım: "Nasıl Kullanılır? 1. ... 2. ... İpucu: ..." — numaralı adımlar alınır, "İpucu" ve sonrası alınmaz.
Site sık 429 veriyor; yavaş çek (2026-11-12'de 2,5 sn arayla çekildi)."""
import re

import source_common as sc

DOMAIN = "thalia.com.tr"
STOP = r"(?:Rutinini Tamamla|Rutindeki Yeri|Uyarılar ve Güvenlik|Öne Çıkan İçerikler|Ürün Künyesi|Nasıl Kullanılır\?)"


def _text(s):
    for x in s.select("script, style"):
        x.decompose()
    return re.sub(r"\s+", " ", s.get_text(" ", strip=True))


def inci(s, main):
    t = _text(s)
    m = re.search(r"Tam İçerik \(INCI\)\s*(.{40,2500}?)(?=\.\s|\s" + STOP + r"|$)", t)
    if m and m.group(1).count(",") >= 4:
        return [x.strip().rstrip(".").upper() for x in sc.split_inci(sc.clean_text(m.group(1)))], "thalia"


def howto(s):
    t = _text(s)
    m = re.search(r"Nasıl Kullanılır\?\s*(.{15,1200}?)(?=\s" + STOP + r"|Tam İçerik|$)", t)
    if not m:
        return []
    body = re.split(r"\s*(?:İpucu|Tamamlayıcı Rutin)\s*:", m.group(1))[0].strip()
    # Sayfa adımları boşluksuz yazıyor: "1. Ellerinizi ... kurulayın.2. Yeterli ..."
    parts = re.split(r"(?:^|(?<=[.!?:])|\s)\s*(\d)\.\s+", " " + body)
    if len(parts) > 2:
        steps = [parts[i + 1] for i in range(1, len(parts) - 1, 2)]
        # son adımın ardından gelen numarasız tanıtım/öneri cümleleri ("Dilerseniz ... kazandırır.") alınmaz
        steps[-1] = re.split(r"(?<=[.!?])(?=[A-ZÇĞİÖŞÜ])", steps[-1])[0]
    else:  # numarasız ("Peeling olarak: ... Maske olarak: ...")
        steps = re.split(r"(?<=[.!?])\s*(?=[A-ZÇĞİÖŞÜ])", body)
    out = []
    for x in steps:
        x = re.sub(r"\s+", " ", x).strip()
        if not x:
            continue
        if not x.endswith((".", "!")):
            x += "."
        out.append(x)
    return out
