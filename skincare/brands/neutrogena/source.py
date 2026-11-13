"""Neutrogena TR + AB resmî kaynak birleştirmesi.
Türkiye sitesinde (neutrogena.com.tr) Türkçe ürün adı, görsel, kullanım ve beyanlar yer alır;
içerik listesi (INCI) ve EAN-13 barkod ise markanın resmî AB sitesinden (neutrogena.de, inciFallbackUrl) çekilir."""
import json
import re
from bs4 import BeautifulSoup
import source_common as sc

DOMAIN = "neutrogena.com.tr"


def howto(s):
    steps = []
    for h in s.select("h2, h3"):
        title = h.get_text(" ", strip=True).lower()
        if "nasıl kullanılır" in title or title == "kullanımı":
            parent = h.find_parent("div")
            if parent:
                for p in parent.select("p, li"):
                    txt = p.get_text(" ", strip=True)
                    if txt and len(txt) > 15 and txt not in steps:
                        steps.append(txt)
    return steps


def complete(result, s, inci_fallback_url, image_source_url):
    if not result["inci"] and inci_fallback_url:
        if not inci_fallback_url.startswith("https://www.neutrogena.de/"):
            raise ValueError("Neutrogena INCI yedek kaynağı resmî neutrogena.de adresi olmalı")
        de_html = sc.get(inci_fallback_url)
        de_soup = BeautifulSoup(de_html, "html.parser")
        for p in de_soup.select(".rich-text p, p"):
            txt = sc.clean_text(p.get_text(" ", strip=True))
            if re.match(r"^Aqua\b", txt, re.I) and txt.count(",") >= 5:
                result["inci"] = [x.upper() for x in sc.split_inci(txt)]
                result["inciSource"] = "neutrogena-ab"
                result["inciUrl"] = inci_fallback_url
                break
        # AB resmî ürün sayfasındaki JSON-LD Product > gtin13 barkodunu al
        barcodes = list(result.get("barcodes") or [])
        for t in de_soup.select('script[type="application/ld+json"]'):
            try:
                d = json.loads(t.text, strict=False)
            except ValueError:
                continue
            if isinstance(d, dict) and d.get("@type") == "Product":
                for k in ("gtin13", "gtin"):
                    raw = re.sub(r"\D", "", str(d.get(k) or ""))
                    if len(raw) == 14 and raw.startswith("0"):
                        raw = raw[1:]
                    if len(raw) in (8, 12, 13) and raw not in barcodes:
                        barcodes.append(raw)
        if barcodes:
            result["barcodes"] = barcodes
