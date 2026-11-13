"""Centesol (Görkito'nun markası; gorkito.com, ikas). İçerik listesi ve kullanım ikas ürün verisinde:
source_common.ikas_inci / ikas_howto. Ürün listesi: /products.xml (Centesol dışındaki Görkito ürünleri de var)."""
import source_common as sc

DOMAIN = "gorkito.com"


def inci(s, main):
    r = sc.ikas_inci(s)
    if r:
        return r, "centesol"


def howto(s):
    return sc.ikas_howto(s)
