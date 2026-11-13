"""Gratis cilt bakımı ürünlerinden barkod adayları (barkodla ürün analizi: uygun-bakim-app tarayıcısı).

    python -X utf8 scripts/skincare/gratis/crawl.py [--limit N]

Ürün adresleri gratis.com/sitemap/Product-tr-TRY.xml'den gelir; kategori adresin ilk parçasıdır (CATEGORIES).
Her ürün sayfası source_common.get ile önbellekli ve istekler arası 2,5 sn beklenerek çekilir (robots.txt ürün
sayfalarına izin veriyor; arama/filtre adresleri yasak ve kullanılmıyor). Tekrar çalıştırmak yalnızca yeni
sayfaları indirir.

Yalnızca olgular saklanır: barkod (sayfadaki "eanUpc"), ad, marka, Gratis kategorisi, boy, içerik listesi (varsa,
açıklamadaki "İçindekiler:" satırı). Gratis'in açıklama metni ve görselleri alınmaz. İçerik listesinin sırası
marka etiketinden farklı olabiliyor (Maruderm pilotu, 2026-11): ürün eklerken liste marka sitesinden alınır,
buradaki liste yalnızca aday ve karşılaştırma içindir.
Çıktı: scripts/skincare/gratis/_out/products.jsonl (git dışı).
"""
import html as html_lib, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import source_common as sc  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_out")
SITEMAP = "https://www.gratis.com/sitemap/Product-tr-TRY.xml"

# Gratis yaprak kategorileri -> sitedeki kategori (vocab.ts > CATEGORIES); None = kategori elle belirlenir
CATEGORIES = {
    "yuz-serumlari-cilt-serumu-yaglari": "serum",
    "gunluk-nemlendirici-kremler-spreyler": "nemlendirici",
    "yuz-bakim-kremleri": "nemlendirici",
    "yuz-nemlendirici-gece-kremleri": "gece-kremi",
    "tonikler": "tonik",
    "gul-suyu": "tonik",
    "yuz-temizleme-jelleri": "yuz-temizleyici",
    "yuz-temizleme-kopukleri": "yuz-temizleyici",
    "yuz-temizleme-sutu": "yuz-temizleyici",
    "yuz-temizleme-sabunu": "yuz-temizleyici",
    "yuz-temizleme-urunleri": "yuz-temizleyici",
    "yuz-temizleme-yaglari-balmlari": "makyaj-temizleyici",
    "yuz-makyaj-temizleme-suyu": "misel-su",
    "goz-makyaji-temizleyiciler": "makyaj-temizleyici",
    "yuz-peeling-urunleri": "peeling",
    "yuz-maskeleri": "maske",
    "yuz-bakim-maskesi-paket": "maske",
    "goz-kremleri": "goz-bakimi",
    "goz-maskesi": "goz-bakimi",
    "yuz-gunes-kremleri": "gunes-koruyucu",
    "gunes-korumali-spf-yuz-kremleri": "gunes-koruyucu",
    "gunes-kremleri": "gunes-koruyucu",
    "gunes-spreyleri": "gunes-koruyucu",
    "bebek-cocuk-gunes-kremleri": "gunes-koruyucu",
    "dudak-kremi": "dudak-bakimi",
    "dudak-bakim-paket-maskeler": "dudak-bakimi",
    "dudak-maskesi": "dudak-bakimi",
    "el-vucut-kremleri": "vucut-bakimi",
    "vucut-losyonlari": "vucut-bakimi",
    "cilt-bakim": None,
    "erkek-cilt-bakim": None,
}


def product_urls():
    xml = sc.session.get(SITEMAP, timeout=60).text
    urls = re.findall(r"<loc>(https://www\.gratis\.com/[^<]+-p-\d+)</loc>", xml)
    return [u for u in urls if u.split("/")[3] in CATEGORIES]


def attr(page, key):
    m = re.search(r'"key":"%s","translation":"[^"]*","value":("(?:[^"\\]|\\.)*"|\[[^\]]*\]|\d+)' % key, page)
    return json.loads(m.group(1)) if m else None


def parse(url, raw):
    page = raw.replace('\\"', '"')
    product, crumbs = {}, []
    for m in re.finditer(r'<script[^>]*application/ld\+json[^>]*>(.*?)</script>', raw, re.S):
        try:
            d = json.loads(m.group(1))
        except ValueError:
            continue
        if d.get("@type") == "Product":
            product = d
        elif d.get("@type") == "BreadcrumbList":
            crumbs = [i["name"] for i in d.get("itemListElement", [])][1:]
    desc = html_lib.unescape(re.sub(r"<[^>]+>", " ", product.get("description") or ""))
    m = re.search(r"İçindekiler\s*:?\s*(.+?)(?:\.\s*$|\.\s+[A-ZÇĞİÖŞÜ][a-zçğıöşü]|$)", desc, re.S)
    inci = re.sub(r"\s+", " ", m.group(1)).strip() if m and m.group(1).count(",") >= 5 else None
    leaf = url.split("/")[3]
    return {
        "gratisId": url.rsplit("-p-", 1)[1],
        "url": url,
        "gtin": attr(page, "eanUpc"),
        "name": product.get("name"),
        "brand": (product.get("brand") or {}).get("name"),
        "gratisCategory": leaf,
        "category": CATEGORIES[leaf],
        "breadcrumb": crumbs,
        "size": attr(page, "hacim") or attr(page, "agirlik"),
        "inci": inci,
    }


def main():
    limit = int(sys.argv[sys.argv.index("--limit") + 1]) if "--limit" in sys.argv else None
    # --shard 1/2: adreslerin yarısı; Gratis'e en fazla iki eşzamanlı akış (≈0,8 istek/sn) açılır
    shard, shards = map(int, sys.argv[sys.argv.index("--shard") + 1].split("/")) if "--shard" in sys.argv else (1, 1)
    urls = product_urls()[shard - 1::shards][:limit]
    os.makedirs(OUT, exist_ok=True)
    rows, failed = [], []
    for n, url in enumerate(urls, 1):
        try:
            rows.append(parse(url, sc.get(url)))
        except Exception as e:  # tek sayfa hatası taramayı durdurmasın; sonraki çalıştırmada yeniden denenir
            failed.append(f"{url}: {e}")
        if n % 100 == 0:
            print(f"{n}/{len(urls)}", flush=True)
    name = "products.jsonl" if shards == 1 else f"products-{shard}of{shards}.jsonl"
    with open(os.path.join(OUT, name), "w", encoding="utf8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"{len(rows)} ürün ({sum(1 for r in rows if r['gtin'])} barkodlu, "
          f"{sum(1 for r in rows if r['inci'])} içerik listeli) -> scripts/skincare/gratis/_out/{name}")
    for f in failed:
        print("HATA", f)


if __name__ == "__main__":
    main()
