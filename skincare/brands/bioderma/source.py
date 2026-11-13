"""Bioderma TR. İçerik listesi ürün sayfasındaki <li>'ler; yoksa resmî Ask NAOS TR sayfası, o da yoksa
catalog.json > inciFallbackUrl (NAOS Stars TR). Kullanım "Adım N" (genel) ya da öneri sekmesi."""
import re
import requests
from bs4 import BeautifulSoup
import source_common as sc

DOMAIN = "bioderma.com.tr"


def inci(s, main):
    box = s.select_one('[class*="productingredientslist"]')
    if box and box.select("li"):
        items = ", ".join(li.get_text(" ", strip=True) for li in box.select("li"))
        return sc.split_inci(sc.clean_text(items)), "liste"


def howto(s):
    advice = s.select_one('#advice-wrapper #tab1')
    if not advice:
        return []
    parts = []
    for element in advice.select('.no-treatment p, .no-treatment li, .small p, .small li'):
        if element.name == 'li' and element.select_one('p'):
            continue
        value = element.get_text(" ", strip=True)
        if value and value not in parts:
            parts.append(value)
    return parts


def complete(result, s, inci_fallback_url, image_source_url):
    # Ürün sayfasının bağladığı resmî şeffaflık platformu. İşleve göre gruplu metin yerine tek sıralı içerik
    # düğmesi listesi kullanılır.
    if not result["inci"] or not result["image"]:
        link = s.select_one('a.ask-naos-btn[href^="https://ask-naos.com.tr/product/"]')
        if link:
            ask_url = link["href"]
            try:
                ask = BeautifulSoup(sc.get(ask_url), "html.parser")
            except requests.HTTPError as exc:
                if exc.response.status_code != 404:
                    raise
                ask = BeautifulSoup("", "html.parser")  # eski bağlantı: sonraki resmî kaynağı dene
            if not result["inci"]:
                buttons = ask.select('.ingredients-container .ing-list-wrap button.js-ing-trigger[data-ing-name]')
                if buttons:
                    result["inci"] = [sc.clean_text(b["data-ing-name"]).upper() for b in buttons]
                    result["inciSource"] = "ask-naos-tr"
                    result["inciUrl"] = ask_url
            if not result["image"]:
                image = ask.select_one('img.product-image[data-src]')
                if image:
                    result["image"] = image["data-src"].strip()
                    result["imageUrl"] = ask_url
    if not result["inci"] and inci_fallback_url:
        if not inci_fallback_url.startswith("https://www.naosstars.com/"):
            raise ValueError("INCI yedek kaynağı NAOS Stars Türkiye olmalı")
        shop = BeautifulSoup(sc.get(inci_fallback_url), "html.parser")
        for ul in shop.select('.urunTabAlt ul'):
            items = [li.get_text(" ", strip=True) for li in ul.select('li')]
            if items and re.match(r"^(AQUA/WATER/EAU|SODIUM PALMATE)\b", items[0]):
                result["inci"] = sc.split_inci(sc.clean_text(", ".join(items)))
                result["inciSource"] = "naos-stars-tr"
                result["inciUrl"] = inci_fallback_url
                break
    if image_source_url:
        if not image_source_url.startswith("https://www.naosstars.com/"):
            raise ValueError("Görsel doğrulama kaynağı NAOS Stars Türkiye olmalı")
        shop = BeautifulSoup(sc.get(image_source_url), "html.parser")
        image = shop.select_one('meta[property="og:image"]')
        if not image or not image.get("content"):
            raise ValueError("Doğrulanmış ürün görseli bulunamadı")
        result["image"] = image["content"]
        result["imageUrl"] = image_source_url
