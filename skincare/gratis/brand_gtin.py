"""Marka sitelerinden ürün barkodlarını (GTIN/EAN) topla: catalog.json > brandUrl sayfaları.

    python -X utf8 scripts/skincare/gratis/brand_gtin.py [--limit N]

Önce sayfadaki ld+json Product düğümleri (gtin*, tam sayı sku/mpn); bulunamazsa ham HTML'de regex (yedek).
GS1 kontrol basamağı doğrulanır, 14 haneye tamamlanır. Çıktı: gratis/_out/brand_gtins.csv
"""
import argparse, csv, html, json, os, re, sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
SKIN = os.path.dirname(HERE)  # scripts/skincare
sys.path.insert(0, SKIN)
import source_common as sc  # noqa: E402  (önbellekli get, 2.5 s gecikme)
from bs4 import BeautifulSoup  # noqa: E402

OUT = os.path.join(HERE, "_out", "brand_gtins.csv")
GTIN_KEYS = ("gtin", "gtin8", "gtin12", "gtin13", "gtin14")
RX_NUM = re.compile(r"\d{8}|\d{12}|\d{13}|\d{14}")  # sku/mpn için tam sayı kuralı
RX_HTML = re.compile(r'"(gtin13|ean|barcode)"\s*:\s*"(\d{8,14})"')
RX_NAME = re.compile(r'"name"\s*:\s*"([^"]{1,120})"')
PRODUCT_TYPES = ("Product", "ProductGroup")


def norm(val):
    """GS1 kontrolü: 8/12/13/14 hane ve kontrol basamağı tutarlı mı? Tutarlıysa 14 haneye tamamla, değilse None."""
    d = re.sub(r"\D", "", str(val))
    if len(d) not in (8, 12, 13, 14):
        return None
    # Sağdan itibaren kontrol basamağı hariç ağırlıklar 3,1,3,1...
    s = sum(int(c) * (3 if i % 2 == 0 else 1) for i, c in enumerate(reversed(d[:-1])))
    return d.zfill(14) if (10 - s % 10) % 10 == int(d[-1]) else None


def is_product(node):
    t = node.get("@type")
    return any(x in PRODUCT_TYPES for x in (t if isinstance(t, list) else [t]))


def walk_ld(node, found, name="", in_product=False):
    """ld+json ağacını gez. Product altındaki her düğüm (offers, hasVariant, @graph) barkod taşıyabilir."""
    if isinstance(node, list):
        for x in node:
            walk_ld(x, found, name, in_product)
        return
    if not isinstance(node, dict):
        return
    prod = is_product(node)
    in_product = in_product or prod
    if prod and node.get("name"):  # varyant adı: en yakın Product'ın adı
        name = html.unescape(str(node["name"])).strip()
    if in_product:
        label = f"{name} {html.unescape(node['size'])}".strip() if isinstance(node.get("size"), str) else name
        for k in GTIN_KEYS:
            g = norm(node[k]) if node.get(k) else None
            if g:
                found.append((g, f"ld+json.{k}", label))
        for k in ("sku", "mpn"):  # sku/mpn yalnızca tam sayıysa (8/12/13/14 hane) alınır
            v = str(node.get(k) or "").strip()
            g = norm(v) if RX_NUM.fullmatch(v) else None
            if g:
                found.append((g, f"ld+json.{k}", label))
    for v in node.values():
        if isinstance(v, (dict, list)):
            walk_ld(v, found, name, in_product)


def barcodes(html):
    """(gtin14, kaynak alanı, varyant adı) listesi; tekrarlar atılır, ilk görülen kalır."""
    found = []
    for t in BeautifulSoup(html, "html.parser").select('script[type="application/ld+json"]'):
        try:
            walk_ld(json.loads(t.string or "", strict=False), found)
        except ValueError:  # bozuk JSON bloğu: atla
            continue
    if not found:  # yedek: ham HTML'de regex; varyant adı için yakındaki "name" alınır
        for m in RX_HTML.finditer(html):
            g = norm(m.group(2))
            if g:
                names = RX_NAME.findall(html[max(0, m.start() - 400):m.start()])
                found.append((g, f"html.{m.group(1)}", names[-1] if names else ""))
    seen, out = set(), []
    for g, src, var in found:
        if g not in seen:
            seen.add(g)
            out.append((g, src, var))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0, help="ilk N ürün (doğrulama için)")
    args = ap.parse_args()
    products = json.load(open(os.path.join(SKIN, "catalog.json"), encoding="utf8"))["products"]
    if args.limit:
        products = products[: args.limit]

    rows, errors = [], []
    done, hits, per_rows = Counter(), Counter(), Counter()  # marka -> işlenen / barkodlu ürün / satır
    for i, p in enumerate(products, 1):
        brand, url = p["brand"], p.get("brandUrl", "")
        done[brand] += 1
        try:
            found = barcodes(sc.get(url))  # sıralı, önbellekli, 2.5 s gecikmeli
        except Exception as e:  # tek sayfa hatası tüm koşuyu durdurmasın
            errors.append((p["slug"], f"{type(e).__name__}: {str(e)[:150]}"))
            found = []
        print(f"[{i}/{len(products)}] {p['slug']}: {len(found)} barkod", flush=True)
        if found:
            hits[brand] += 1
        per_rows[brand] += len(found)
        for g, src, var in found:
            rows.append({"slug": p["slug"], "brand": brand, "gtin14": g, "source_field": src,
                         "variant": var, "brand_url": url})

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", newline="", encoding="utf8") as f:
        w = csv.DictWriter(f, fieldnames=["slug", "brand", "gtin14", "source_field", "variant", "brand_url"])
        w.writeheader()
        w.writerows(rows)

    print("\n=== ÖZET ===")
    print(f"İşlenen ürün: {len(products)}")
    print(f"En az 1 geçerli barkodlu ürün: {sum(hits.values())}")
    print(f"Toplam satır: {len(rows)}  -> {OUT}")
    print("\nMarka: işlenen | barkodlu | satır")
    for b in sorted(done):
        print(f"  {b}: {done[b]} | {hits[b]} | {per_rows[b]}")
    none = [b for b in sorted(done) if not hits[b]]
    print("Barkod bulunmayan markalar: " + (", ".join(none) or "yok"))
    print(f"\nSayfa hataları: {len(errors)}")
    for slug, err in errors:
        print(f"  {slug}: {err}")


if __name__ == "__main__":
    main()
