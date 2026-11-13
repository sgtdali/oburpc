"""fetch_sources.py ve marka modüllerinin (brands/<marka>/source.py) ortak yardımcıları: önbellekli istek,
INCI metni temizleme/bölme, sayfa metni ve görsel."""
import json, os, re, time
import requests
from bs4 import BeautifulSoup

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, ".cache")
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
DELAY = 2.5

session = requests.Session()
session.headers.update({"User-Agent": UA, "Accept-Language": "tr-TR,tr;q=0.9"})


def get(url, params=None):
    key = re.sub(r"[^a-z0-9]+", "_", (url + json.dumps(params or {}, sort_keys=True)).lower())[-150:]
    path = os.path.join(CACHE, key + ".html")
    if os.path.exists(path):
        return open(path, encoding="utf8").read()
    for wait in (10, 30, 60, None):  # 503 (geçici yoğunluk) / 429 (istek sınırı): bekleyip yeniden dene
        r = session.get(url, params=params, timeout=30)
        if r.status_code not in (429, 503) or wait is None:
            break
        time.sleep(wait)
    r.raise_for_status()
    if not r.encoding or r.encoding.lower() == "iso-8859-1":
        r.encoding = "utf-8"
    os.makedirs(CACHE, exist_ok=True)
    open(path, "w", encoding="utf8").write(r.text)
    time.sleep(DELAY)
    return r.text


def clean_text(t):
    """Satıcı/sayfa yazım farklarını düzelt: 'AQUA / WATER' -> 'AQUA/WATER', 'PEG- 40' -> 'PEG-40'."""
    t = re.sub(r"[​‌‍﻿]", "", t).replace("\xa0", " ")
    t = re.sub(r"\s*/\s*", "/", t)
    t = re.sub(r"(\w)-\s+(\d)", r"\1-\2", t)
    return t


def find_inci(text):
    """Sayfa metnindeki INCI bloğunu bul: virgülle ayrılmış, büyük harfli, en uzun dizi."""
    text = clean_text(text)
    best = ""
    for m in re.finditer(r"(?:[A-Z0-9][A-Z0-9 /\-\.'()&+]*?,\s?){6,}[A-Z0-9][A-Z0-9 /\-\.'()&+]*", text):
        if len(m.group(0)) > len(best):
            best = m.group(0)
    if not best:
        return None
    # Son maddeye yapışan cümle başını kes: "ETHYLHEXYLGLYCERIN. (Code" / "ETHYLHEXYLGLYCERIN K"
    head, _, last = best.rpartition(",")
    last = re.split(r"\.\s|\s\(", last.strip() + " ")[0].strip()
    return (head + ", " + last).strip().rstrip(".")


def split_inci(s):
    # Ürüne ait ld+json alanı başlık, • ayıracı, parti kodu ve etiket uyarısı içerebilir.
    # L'Oréal Paris: "909261 66 - İÇİNDEKİLER: AQUA / WATER, ... (F.I.L. B2745/1)."
    s = re.sub(r"^.*?(?:INGREDIENTS|İÇİNDEKİLER)\s*:\s*", "", s, flags=re.I | re.S)
    s = re.split(r"\((?:code|fil\b|f\.?i\.?l\b)|Lütfen markamızın", s, maxsplit=1, flags=re.I)[0]
    # Caudalie: "... LIMONENE. (182/036) * Organik Tarımla elde edilen içerikler..." ve "ALCOHOL DENAT.*"
    s = re.split(r"\.?\s*\(\d+/\d+\)", s, maxsplit=1)[0].replace("*", "")
    s = s.replace("•", ",")
    s = re.sub(r"\s*\[[A-Z]{1,3}\s*\d+\]?\s*$", "", s)  # kapanış köşeli parantezi eksik parti kodları da var
    s = re.sub(r"(\d),(\d)", r"\1§\2", s)  # "1,2-HEXANEDIOL" bölünmesin
    return [p.strip().rstrip(".").strip().replace("§", ",")
            for p in re.split(r",(?![^()]*\))", s) if p.strip().rstrip(".").strip()]


def main_text(s):
    """Menü/alt bilgi atılmış sayfa metni, h1'den başlar (menüdeki "Dermatologlarla geliştirildi" gibi
    bağlantılar beyan sanılmasın). Parçalar " | " ile ayrılır."""
    s = BeautifulSoup(str(s), "html.parser")
    for t in s.select("header, nav, footer, script, style, noscript, [role=navigation]"):
        t.decompose()
    text = s.get_text(" | ", strip=True)
    h1 = s.select_one("h1")
    i = text.find(h1.get_text(" | ", strip=True)) if h1 else -1
    return text[max(i, 0):]


def page_image(s, product):
    """Ürün görseli: og:image > ld+json Product.image > ürün galerisi (Bioderma: "packshot")."""
    og = s.select_one('meta[property="og:image"]')
    if og and og.get("content"):
        return og["content"]
    img = product.get("image")
    if isinstance(img, list):
        img = img[0] if img else None
    if isinstance(img, dict):
        img = img.get("url")
    if img:
        return img
    tag = s.select_one('img[src*="packshot"]')
    return tag["src"] if tag else None


# --- Marka modülleri: brands/<marka>/source.py --------------------------------------------------------------
# Her modülde DOMAIN (ör. "lorealparis.com.tr") ve isteğe bağlı kancalar bulunur; fetch_sources.py > brand_page()
# bunları sabit sırayla çağırır (kanca sözleşmesi: brands/README.md).
BRANDS = os.path.join(HERE, "brands")
_modules = {}


def brand_module(slug):
    if slug not in _modules:
        import importlib.util
        path = os.path.join(BRANDS, slug, "source.py")
        spec = importlib.util.spec_from_file_location("brand_source_" + slug.replace("-", "_"), path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        _modules[slug] = mod
    return _modules[slug]


def brand_for_url(url):
    """Adresin alan adına göre marka modülü; tanımlı marka yoksa None (yalnızca genel çıkarıcılar)."""
    from urllib.parse import urlparse
    host = urlparse(url).netloc.lower()
    for slug in sorted(os.listdir(BRANDS)):
        if os.path.exists(os.path.join(BRANDS, slug, "source.py")):
            dom = brand_module(slug).DOMAIN
            if host == dom or host.endswith("." + dom):
                return brand_module(slug)
    return None


# --- ikas (Next.js) mağazaları: ürün verisi #__NEXT_DATA__ > props.pageProps.pageSpecificData içinde ---------------
IKAS_WARN = re.compile(r"(?i)haricen|harici kullanım|ulaşamayacağı|erişemeyeceği|saklayın|muhafaza|temasından kaçın|"
                       r"temastan kaçın|temas halinde|yaralı|hasarlı|tahriş olmuş|doktor|yaşından küçük|yanıcı")


def ikas_product(s):
    """(açıklama metni ' | ' ayraçlı, {öznitelik adı: metin}) döndürür; ikas sayfası değilse ('', {})."""
    nd = s.select_one("#__NEXT_DATA__")
    if not nd:
        return "", {}
    try:
        ps = json.loads(nd.text)["props"]["pageProps"]["pageSpecificData"]
    except (KeyError, TypeError, ValueError):
        return "", {}
    desc = re.sub(r"\s+", " ", BeautifulSoup(ps.get("description") or "", "html.parser").get_text(" | ", strip=True))
    attrs = {a["productAttribute"]["name"]: BeautifulSoup(a.get("value") or "", "html.parser").get_text(" ", strip=True)
             for a in ps.get("attributes") or [] if a.get("productAttribute")}
    return desc, attrs


def ikas_inci(s):
    """İçerik listesi: önce "İçindekiler/İçerik/ingredients" özniteliği, sonra açıklamadaki başlıktan sonraki bölüm."""
    desc, attrs = ikas_product(s)
    for k, v in attrs.items():
        if re.search(r"(?i)içindekiler|içerik|ingredient|inci", k) and v.count(",") >= 4:
            return [x.strip().rstrip(".").upper() for x in split_inci(clean_text(v))]
    m = re.search(r"(?:İçindekiler|İÇİNDEKİLER|İçerik Listesi|İçerikler|INCI|Ingredients)\s*:?\s*\|?\s*([^|]{40,2500})", desc)
    if m and m.group(1).count(",") >= 4:
        return [x.strip().rstrip(".").upper() for x in split_inci(clean_text(m.group(1)))]
    return None


def ikas_howto(s):
    """Kullanım: "Nasıl Kullanılır?/Kullanım" özniteliği ya da açıklamadaki bölüm; genel uyarılar atılır."""
    desc, attrs = ikas_product(s)
    v = next((v for k, v in attrs.items() if re.search(r"(?i)nasıl kullanılır|kullanım", k) and v), "")
    if not v:
        m = re.search(r"(?:Nasıl Kullanılır\??|Kullanım(?: Önerisi| Şekli)?)\s*:?\s*\|\s*(.{15,1200}?)"
                      r"(?=\s\|\s(?:İçindekiler|İçerik|Uyarı|Neden|Öne Çıkan|Kimler|Sıkça)|$)", desc)
        v = m.group(1).replace("|", " ") if m else ""
    return [x.strip() for x in re.split(r"(?<=[.!])\s+", v) if x.strip() and not IKAS_WARN.search(x)]
