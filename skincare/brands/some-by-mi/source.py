"""Some By Mi (en.somebymi.com, Cafe24, İngilizce global site). Ürün bilgi tablosunda <li> içinde
<span class="ttl">… Ingredients</span> ve hemen ardından listeyi taşıyan <span>. Miktar notları ("Extract(1,000 ppm)")
virgül içerebildiği için bölmeden önce atılır. Türkçe kullanım talimatı yok."""
import re

import source_common as sc

DOMAIN = "somebymi.com"


def inci(s, main):
    for ttl in s.select("span.ttl"):
        if ttl.get_text(" ", strip=True).lower().endswith("ingredients"):
            val = ttl.find_next_sibling("span")
            v = val.get_text(" ", strip=True) if val else ""
            v = re.sub(r"\(\s*[\d.,]+\s*(?:ppm|ppb|%)\s*\)", "", v, flags=re.I)
            if v.count(",") >= 4:
                return [x.strip().rstrip(".").upper() for x in sc.split_inci(sc.clean_text(v))], "some-by-mi"
    return None


def howto(s):
    return []
