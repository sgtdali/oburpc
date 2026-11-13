"""s'hevec (shevec.com, Shopify). Ürün açıklaması soru-cevap düzeninde: "Nasıl kullanılır? | <cevap> | <sonraki soru?>"
ve "İçerik listesi (INCI) | Aqua, ... . | Vegan ...". Shopify `/products/<handle>.json > body_html` aynı metni verir."""
import re

import source_common as sc

DOMAIN = "shevec.com"
WARN = re.compile(r"(?i)haricen|harici kullanım|ulaşamayacağı|saklayın|temasından kaçın|temas halinde|tahriş olmuş|doktor")


def _parts(s):
    for x in s.select("script, style"):
        x.decompose()
    return [x.strip() for x in re.sub(r"\s+", " ", s.get_text(" | ", strip=True)).split(" | ") if x.strip()]


def inci(s, main):
    p = _parts(s)
    for i, x in enumerate(p):
        if re.match(r"(?i)içerik listesi", x) and i + 1 < len(p) and p[i + 1].count(",") >= 4:
            return [y.strip().rstrip(".").upper() for y in sc.split_inci(sc.clean_text(p[i + 1]))], "she-vec"


def howto(s):
    p = _parts(s)
    for i, x in enumerate(p):
        if x == "Nasıl kullanılır?":
            out = []
            for y in p[i + 1:]:
                if y.endswith("?"):
                    break
                out += [z.strip() for z in re.split(r"(?<=[.!])\s+", y) if z.strip() and not WARN.search(z)]
            return out
    return []
