"""L'Oréal Paris TR. İçerik listesi ld+json "Ingredients" alanında; başında parti kodu ve "İÇİNDEKİLER:" olabilir
(source_common.split_inci atar)."""
import html as html_lib
import re

DOMAIN = "lorealparis.com.tr"


def clean_prop(prop):
    """Alanın başında bazen tanıtım metni var ("...İçindekiler AQUA/WATER, ...") ve liste büyük-küçük karışık
    olabiliyor. Listeleri AQUA ile başlıyor; AQUA yoksa alan içerik listesi değildir (bazı ürünlerde alana
    yalnızca "Hyaluronik asit nedir?" yazısı konmuş) → None, sıradaki çıkarıcıya geçilir."""
    prop = html_lib.unescape(prop)
    m = re.search(r"\bAQUA\b", prop, flags=re.I)
    return prop[m.start():].upper() if m else None
