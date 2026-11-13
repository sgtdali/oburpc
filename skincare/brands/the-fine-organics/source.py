"""The Fine Organics (thefineorganics.com, ikas). İçerik listesi ve kullanım ikas ürün verisinde:
source_common.ikas_inci / ikas_howto. Ürün listesi: /products.xml."""
import source_common as sc

DOMAIN = "thefineorganics.com"


def inci(s, main):
    r = sc.ikas_inci(s)
    if r:
        return r, "the-fine-organics"


def howto(s):
    return sc.ikas_howto(s)
