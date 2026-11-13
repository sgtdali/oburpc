"""CosIng (AB Komisyonu kozmetik madde veritabanı) tam dökümü.

    python -X utf8 scripts/skincare/cosing_fetch.py

Çıktı: scripts/skincare/cosing/{ingredients,substances,functions}.json
Ayrıntılar ve API notları: docs/skincare-veri-kaynaklari.md (bölüm 3)

API sınırları: sayfa başına en fazla 200 kayıt, 10.000. sonuçtan ötesine sayfa yok.
Bu yüzden kayıtlar substanceId öneklerine bölünür (her dilim < 10.000), her dilim sayfalanır.
substanceId metin olarak saklandığından sayısal aralık sorgusu YANLIŞ sonuç verir; önek kullanılır.
"""
import json, os, sys, time
import requests

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "cosing")
API = "https://webgate.ec.europa.eu/es/search-api/rest/search"
KEY = "285a77fd-1257-4271-8507-f0c6b2961203"  # cosing/assets/env-json-config.json > euSearchApiKey
PAGE = 200
MAX_WINDOW = 9800
DELAY = 0.3

session = requests.Session()
session.headers["User-Agent"] = "uygunbakim-skincare-data/1.0"

# Arama motorunun kendi alanları; veri değil
SKIP_PREFIXES = ("es", "esST_", "esDA_", "corporate-search", "language", "currentVersion")


def call(must, page=1, size=PAGE):
    q = {"bool": {"must": must}}
    sort = [{"field": "substanceId", "order": "ASC"}]
    for attempt in range(5):
        try:
            r = session.post(
                f"{API}?apiKey={KEY}&text=*&pageSize={size}&pageNumber={page}",
                files={"query": (None, json.dumps(q), "application/json"),
                       "sort": (None, json.dumps(sort), "application/json")},
                timeout=120,
            )
            r.raise_for_status()
            return r.json()
        except (requests.RequestException, ValueError) as e:
            wait = 5 * (attempt + 1)
            print(f"  hata ({e}), {wait} sn sonra tekrar", flush=True)
            time.sleep(wait)
    sys.exit("API yanıt vermiyor, durduruldu")


def clean(meta):
    """Tek elemanlı listeleri düzleştir, boşları ve arama motoru alanlarını at."""
    out = {}
    for k, v in meta.items():
        if k.startswith(SKIP_PREFIXES):
            continue
        if isinstance(v, list):
            v = [x for x in v if x not in (None, "", "-")]
            if not v:
                continue
            if len(v) == 1 and k not in ("functionName", "annexNo"):
                v = v[0]
        if v in (None, ""):
            continue
        out[k] = v
    return out


def count(must):
    return call(must, 1, 1).get("totalResults") or 0


def prefix_filter(p):
    """substanceId METİN olarak saklanıyor (sözlük sırası: "100000" < "99999").
    p ile başlayan tüm id'ler: p <= id < üst sınır. Üst sınır p'nin "bir sonraki" öneki:
    "12" -> "13", "19" -> "2", "9" -> sınırsız. (":" gibi rakam dışı karakter API'de çalışmıyor.)"""
    head = p.rstrip("9")
    if not head:
        return {"range": {"substanceId": {"gte": p}}}
    upper = head[:-1] + str(int(head[-1]) + 1)
    return {"range": {"substanceId": {"gte": p, "lt": upper}}}


def windows(base, prefix=""):
    """id uzayını öneklere böl: her parça MAX_WINDOW'dan küçük olacak."""
    out = []
    for d in "0123456789":
        p = prefix + d
        n = count(base + [prefix_filter(p)])
        if n == 0:
            continue
        if n <= MAX_WINDOW:
            out.append((prefix_filter(p), p, n))
            continue
        exact = count(base + [{"term": {"substanceId": p}}])  # tam olarak p olan id
        if exact:
            out.append(({"term": {"substanceId": p}}, p + " (tam)", exact))
        out += windows(base, p)
    return out


def fetch_type(item_type):
    base = [{"term": {"itemType": item_type}}]
    total = count(base)
    wins = windows(base)
    print(f"{item_type}: toplam {total}, {len(wins)} dilim, dilim toplamı {sum(w[2] for w in wins)}", flush=True)
    rows, raw = {}, 0
    for flt, label, n in wins:
        must = base + [flt]
        for page in range(1, (n + PAGE - 1) // PAGE + 1):
            for x in call(must, page).get("results", []):
                m = clean(x["metadata"])
                rows[str(m.get("substanceId"))] = m
                raw += 1
            time.sleep(DELAY)
        print(f"  önek {label}: {n} kayıt, şu ana kadar {len(rows)}", flush=True)
    # API bazı kayıtları birebir aynı (aynı reference) birden çok kez döndürüyor; tekilleştirilir.
    print(f"  {item_type}: {raw} kayıt geldi, {raw - len(rows)} tekrar atıldı, {len(rows)} tekil", flush=True)
    if raw != total:
        print(f"  UYARI: {item_type} için {total} beklenip {raw} kayıt geldi (eksik çekim)", flush=True)
    return sorted(rows.values(), key=lambda m: int(m.get("substanceId", 0)))


def fetch_small(item_type):
    d = call([{"term": {"itemType": item_type}}], 1, PAGE)
    return [clean(x["metadata"]) for x in d.get("results", [])]


def main():
    os.makedirs(OUT, exist_ok=True)
    data = {
        "ingredients": fetch_type("ingredient"),
        "substances": fetch_type("substance"),
        "functions": fetch_small("function"),
    }
    for name, rows in data.items():
        path = os.path.join(OUT, f"{name}.json")
        json.dump(rows, open(path, "w", encoding="utf8"), ensure_ascii=False, separators=(",", ":"))
        print(f"{name}: {len(rows)} kayıt -> {path} ({os.path.getsize(path) // 1024} KB)")


if __name__ == "__main__":
    main()
