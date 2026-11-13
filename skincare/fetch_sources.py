"""Katalogdaki ürünler için birincil kaynaklardan olguları çek.

    python -X utf8 scripts/skincare/fetch_sources.py [ürün-slug ...]   # argümansız: tüm katalog

Kaynak: yalnızca marka TR sitesi (catalog.json > brandUrl): INCI listesi, Türkçe ürün adı, marka beyanları,
kullanım, görsel adresi (docs/skincare-veri-kaynaklari.md, bölüm 2). Amazon'a bakılmaz: satın alma linki parfüm
tarafındaki gibi programatik arama linkidir (lib/utils.ts > getAmazonSearchLink).
Çıktı: scripts/skincare/raw/<slug>.json.

Genel çıkarıcılar burada; markaya özgü olanlar brands/<marka>/source.py kancalarında (alan adına göre seçilir).
"""
import html as html_lib, json, os, re, sys
from bs4 import BeautifulSoup

# Eski içe aktarmalar (staging/tools.py, bioderma betikleri) için yardımcılar buradan da erişilebilir.
from source_common import (HERE, session, get, clean_text, find_inci, split_inci, main_text, page_image,  # noqa: F401
                           brand_for_url, brand_module)

RAW = os.path.join(HERE, "raw")
INCI_PROPS = ("ingredients", "ingredient", "i̇çerik listesi", "içerik listesi")  # "İ".lower() birleşik nokta üretir


def _norm_ean(val):
    if not val:
        return []
    out = []
    for raw in re.split(r"[,;\s]+", str(val).strip()):
        digits = re.sub(r"\D", "", raw)
        if len(digits) == 14 and digits.startswith("0"):
            digits = digits[1:]
        if len(digits) in (8, 12, 13) and digits not in out:
            out.append(digits)
    return out


def extract_barcodes(url, html, s, image_url=None):
    """Marka ürün sayfasından ürünün kendisine ait EAN-13 / EAN-8 barkodlarını çıkar."""
    eans = []
    def add(vals):
        for v in vals:
            for e in _norm_ean(v):
                if e not in eans:
                    eans.append(e)

    for t in s.select('script[type="application/ld+json"]'):
        try:
            d = json.loads(t.text, strict=False)
        except ValueError:
            continue
        nodes = d if isinstance(d, list) else [d]
        for node in nodes:
            if not isinstance(node, dict) or node.get("@type") not in ("Product", "ProductGroup"):
                continue
            for k in ("gtin13", "gtin", "gtin14", "ean"):
                if node.get(k):
                    add([node[k]])
            sku = str(node.get("sku") or "")
            if re.fullmatch(r"0?\d{12,13}", sku):
                add([sku])
            for sub_key in ("offers", "hasVariant"):
                sub = node.get(sub_key)
                if isinstance(sub, dict):
                    sub = [sub]
                if isinstance(sub, list):
                    for item in sub:
                        if isinstance(item, dict):
                            for k in ("gtin13", "gtin", "gtin14", "ean", "sku"):
                                v = str(item.get(k) or "")
                                if re.fullmatch(r"0?\d{12,13}", v):
                                    add([v])

    if "bioderma.com.tr" in url:
        el = s.select_one("[data-eans]")
        if el:
            add([el.get("data-eans")])
        if not eans:
            add(re.findall(r'"item_id"\s*:\s*"(\d{13})"', html))

    if "eau-thermale-avene.com.tr" in url or "ducray.com" in url:
        m = re.search(r"-(328277\d{7})-", url)
        if m:
            add([m.group(1)])

    if "nivea.com.tr" in url:
        m = re.search(r"-(\d{8}|\d{13})0082\.html", url)
        if m:
            add([m.group(1)])

    if "thepurestsolutions.com" in url:
        add(re.findall(r'"barcode"\s*:\s*"(\d{8,14})"', html))

    if not eans and any(d in url for d in ("cerave.com.tr", "laroche-posay.com.tr", "lorealparis.com.tr")):
        el = s.select_one(".product-details [data-eans], [data-tag-product-id], [data-eans]")
        if el:
            add([el.get("data-eans") or el.get("data-tag-product-id")])
        for img_src in filter(None, [image_url, (s.select_one('meta[property="og:image"]') or {}).get("content")]):
            add(re.findall(r"(?<!\d)(333787\d{7}|343342\d{7}|360052\d{7}|360600\d{7})(?!\d)", str(img_src)))

    return eans


def brand_page(url, inci_fallback_url=None, image_source_url=None):
    """Marka TR sayfası. İçerik listesi sırayla: ld+json Product > ingredients alanı (marka `clean_prop` ile
    süzebilir) > marka `inci` kancası > "İçindekiler"/"İçerik Listesi" başlığından sonraki paragraf > sayfa
    metnindeki virgüllü büyük harf blok."""
    brand = brand_for_url(url)
    hook = lambda name: getattr(brand, name, None)
    html = get(url)
    s = BeautifulSoup(html, "html.parser")
    text = s.get_text(" ", strip=True)
    product, howto = {}, []
    for t in s.select('script[type="application/ld+json"]'):
        try:
            d = json.loads(t.text, strict=False)
        except ValueError:
            continue
        if not isinstance(d, dict):  # bazı sitelerde ld+json bir liste (Garnier)
            continue
        if d.get("@type") == "Product":
            product = d
        if d.get("@type") == "HowTo":
            # Adımlar nesne ({"text": ...}) ya da düz metin (L'Oréal Paris) olabilir. Tek adımlı sayfalarda "step"
            # liste değil tek nesne (L'Oréal Paris, Garnier); listeye sarılmazsa alan adları ("@type", "position",
            # "text") adım diye yazılıyordu (2026-11-13'te fark edildi).
            steps = d.get("step", [])
            if isinstance(steps, (dict, str)):
                steps = [steps]
            howto = [BeautifulSoup(BeautifulSoup(x if isinstance(x, str) else x.get("text", ""), "html.parser")
                                   .get_text(), "html.parser").get_text(" ", strip=True)
                     for x in steps]
            howto = [x for x in howto if x]  # boş "text" (Garnier) adım sayılmaz
    main = main_text(s)

    inci_list, inci_src = None, None
    props = product.get("additionalProperty") or []
    prop = next((p.get("value") for p in props
                 if isinstance(p, dict) and (p.get("name") or "").lower() in INCI_PROPS), None)
    if prop and hook("clean_prop"):
        prop = hook("clean_prop")(prop)
    if prop:
        inci_list, inci_src = split_inci(clean_text(html_lib.unescape(prop))), "ld+json"
    if not inci_list and hook("inci"):
        inci_list, inci_src = hook("inci")(s, main) or (None, None)
    if not inci_list:
        # The Purest Solutions (Shopify) ve Sinoz: "İçindekiler" / "İçerik Listesi" başlığından sonraki paragraf,
        # "Aqua, Niacinamide, ..." (büyük-küçük karışık)
        m = re.search(r"(?:İçindekiler|İçerik Listesi) \| ([^|]{40,})", main)
        if m and m.group(1).count(",") >= 5:
            inci_list, inci_src = [x.upper() for x in split_inci(clean_text(m.group(1)))], "icindekiler"
    inci = find_inci(text)
    if not inci_list and inci:
        inci_list, inci_src = split_inci(inci), "metin"

    # Marka beyanları: INCI bloğundan sonraki kısa paragraf (CeraVe) + ürün alanının INCI'ye kadarki metni
    # (La Roche-Posay: "Alkol içermez. Komedojenik değildir"; Bioderma). Serinin diğer ürünleri INCI'den sonra gelir.
    claims = []
    if inci and text.find(inci) >= 0:
        after = text[text.find(inci) + len(inci):]
        after = re.sub(r"^\.?\s*\(Code[^)]*\)\s*", "", after)
        claims.append(after[:700])
    if inci_src != "metin" and inci_list:
        end = main.upper().find(inci_list[0].upper()[:12])
        claims.append(main[:end if end > 0 else 4000])
    # Ürün alanı belliyse (CeraVe, Caudalie: .product-details) menü ve benzer ürünler beyanlara karışmasın.
    details = s.select_one(".product-details")
    if details:
        claims = [main_text(details)]

    # Kullanım: ld+json HowTo > "Adım N | ..." (Bioderma) > "KULLANIM: | ..." (La Roche-Posay) > marka kancası
    if not howto:
        howto = [m.strip() for m in re.findall(r"Adım \d+ \| ([^|]+)", main)]
    if not howto:
        m = re.search(r"KULLANIM:? \| ([^|]+)", main)
        howto = [m.group(1).strip()] if m else []
    if not howto and hook("howto"):
        howto = hook("howto")(s)

    h1 = s.select_one("h1")
    result = {
        "url": url,
        "nameTr": html_lib.unescape(product.get("name") or "") or (h1.get_text(" ", strip=True) if h1 else None),
        "inci": inci_list,
        "inciSource": inci_src,
        "claims": " | ".join(claims) or None,
        "howTo": howto,
        "image": page_image(s, product),
        "title": s.title.get_text(strip=True) if s.title else None,
    }
    # Markanın resmî ek kaynakları (Bioderma: Ask NAOS, NAOS Stars) ve catalog.json yedek adresleri
    if hook("complete"):
        hook("complete")(result, s, inci_fallback_url, image_source_url)
    elif inci_fallback_url or image_source_url:
        raise ValueError(f"inciFallbackUrl/imageSourceUrl bu marka için tanımlı değil: {url}")
    if not result.get("barcodes"):
        result["barcodes"] = extract_barcodes(url, html, s, result.get("image"))
    return result


def main():
    catalog = json.load(open(os.path.join(HERE, "catalog.json"), encoding="utf8"))
    wanted = set(sys.argv[1:])
    os.makedirs(RAW, exist_ok=True)
    for p in catalog["products"]:
        if wanted and p["slug"] not in wanted:
            continue
        b = brand_page(p["brandUrl"], p.get("inciFallbackUrl"), p.get("imageSourceUrl"))
        if p.get("imageUrl"):
            # og:image kampanya görseliyse (ör. Caudalie Resveratrol-Lift) markanın kendi sitesindeki ambalaj
            # fotoğrafı catalog.json > imageUrl ile elle verilir; adres gözle kontrol edilmiş olmalı.
            b["image"], b["imageNote"] = p["imageUrl"], "catalog.json > imageUrl"
            if not b.get("barcodes"):
                b["barcodes"] = _norm_ean(" ".join(re.findall(r"(?<!\d)(333787\d{7}|343342\d{7}|360052\d{7}|360600\d{7})(?!\d)", p["imageUrl"])))
        json.dump({"slug": p["slug"], "brandSite": b}, open(os.path.join(RAW, p["slug"] + ".json"), "w", encoding="utf8"),
                  ensure_ascii=False, indent=1)
        print(f'{p["slug"]}: {len(b["inci"] or [])} madde ({b["inciSource"]}), {len(b["howTo"])} kullanım adımı, '
              f'görsel {"var" if b["image"] else "YOK"} | {b["nameTr"]}')
        if not b["inci"]:
            print("   EKSİK: içerik listesi bulunamadı; docs/skincare-veri-kaynaklari.md > fetch_sources.py tablosuna bak")


if __name__ == "__main__":
    main()
