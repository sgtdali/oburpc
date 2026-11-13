# Marka bazlı kod

Her markanın klasöründe o markanın sitesine özgü kod durur. Betikler **repo kökünden** çalıştırılır.

## `source.py`: içerik listesi çıkarıcısı

`fetch_sources.py > brand_page()` ürün adresinin alan adına göre (`DOMAIN`) marka modülünü seçer ve aşağıdaki
isteğe bağlı kancaları sabit sırayla çağırır. Ortak yardımcılar `scripts/skincare/source_common.py`'de
(`import source_common as sc`).

| Kanca | Ne zaman | Döndürür |
|---|---|---|
| `DOMAIN` (zorunlu) | `www.` dahil alt alan adları eşleşir | — |
| `clean_prop(prop)` | ld+json içerik alanı bulunduğunda, bölmeden önce | süzülmüş metin ya da `None` (alan içerik listesi değil) |
| `inci(s, main)` | ld+json'dan liste çıkmadıysa | `(liste, inciSource)` ya da `None` |
| `howto(s)` | HowTo / "Adım N" / "KULLANIM:" bulunmadıysa | adım listesi |
| `complete(result, s, inci_fallback_url, image_source_url)` | en sonda; `result`'ı yerinde tamamlar | — |

Kancadan sonra genel yollar denenir: "İçindekiler / İçerik Listesi |" paragrafı, sayfa metnindeki büyük harf blok.
Aynı altyapıyı paylaşan markalar işlevi yeniden kullanır (Ducray: `inci = sc.brand_module("avene").inci`).

**Yeni marka:** `brands/<marka-slug>/source.py` oluştur (en az `DOMAIN` ve hangi yolu kullandığını anlatan
docstring), `fetch_sources.py <slug>` ile `inciSource`'u kontrol et. Mevcut bir çıkarıcıyı değiştirince tüm
katalogu önbellekten yeniden çıkarıp `raw/` ile karşılaştır (hiçbir ürün değişmemeli).

## Keşif ve envanter betikleri

| Marka | Betik | Ne yapar |
|---|---|---|
| Bioderma | `bioderma/inventory.py` | Bioderma TR ürün dizinini sayfalar → `.cache/bioderma-inventory-*.json` |
| Caudalie | `caudalie/discover_sitemap.py` | `tr.caudalie.com/sitemap.xml`'den katalogda olmayan ürün sayfalarını bulur, URL'ye göre kaba ön eleme yapar → `staging/caudalie/_out/sitemap_excluded.json` |
| Ducray | `ducray/discover.py <url> …` | Ducray TR sayfalarındaki `/tr-tr/p/…` ürün ve `/tr-tr/f/…` seri bağlantılarını listeler |

Keşif çıktısı yalnızca aday listesidir; kapsam kararı (set, makyaj, güneş, saç vb.) ve ürün sayfası kontrolü yine
`staging/` iş akışıyla yapılır (bkz. `docs/skincare-veri-kaynaklari.md` §5 "Toplu marka genişletmesi").

## `caudalie/_tek_seferlik/`

Caudalie ajanının 2026-10-05'te yazdığı tek seferlik betikler (ürün adı düzeltme, metin partileri, taslak üretimi).
Arşiv amaçlı tutulur; **yeniden kullanılmamalı**: metin üreten betikler denetimde şablon metin ürettiği için
reddedildi (ürün ve madde metinleri elle, `tools.py summary/ingredients` çıktısına dayanarak yazılır). Yollar repo
köküne göredir ve `staging/caudalie/` dosyalarının o günkü hâlini varsayar.
