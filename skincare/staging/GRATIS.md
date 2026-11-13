# Gratis ürünleri: metin ajanı talimatı

`BRIEF.md`'nin kuralları geçerli; **aşağıdaki farklar önceliklidir**. Önce `BRIEF.md`'yi oku.
Bu bilgisayarda `python` yok: komutlarda `python3` kullan (`python3 -X utf8 scripts/skincare/staging/tools.py ...`).

Bu ürünler Gratis'ten geliyor (kullanıcı kararı, 2026-11-10: barkodla okutulan Gratis ürününün içeriği yorumlanabilsin).
Hazırlık klasörlerini `scripts/skincare/gratis/stage.py` üretti: her `staging/<marka>/` altında `products.json`,
`excluded.json` ve `raw/<slug>.json` hazır. İçerik listesi Gratis ürün sayfasından alındı.

## Senin işin (her marka için)

1. `python -X utf8 scripts/skincare/staging/tools.py summary <marka>` çıktısını oku.
2. `products.json` içinde yalnızca şu alanları düzelt: `name` ve `nameTr` (boy/ml/gram yok, marka adı yok, düzgün
   Türkçe büyük-küçük harf; ürünün ambalajında İngilizce/Korece seri adı varsa `name` o ad olabilir, ör.
   "Centella Ampoule"; yoksa `name` = `nameTr`), `category` (`tools.py check`'in izinli listesinden).
   **`slug`, `brand`, `brandUrl` değişmez.** `raw/` dosyalarına **dokunma** (fetch çalıştırma; Gratis'e istek atma).
3. Kapsam dışı ürünü (BRIEF.md > Kapsam: set/kit, BB/CC krem, fondöten, güneş sonrası, saç, deodorant, makyaj,
   cihaz/aksesuar; ya da sayfanın ana aktifi listede yoksa) `products.json`'dan çıkar, `excluded.json`'a gerekçesiyle ekle.
4. `texts.json` > `products`: her ürün için 3–5 cümle özgün Türkçe açıklama (BRIEF.md > Türkçe metinler kuralları).
   Kaynak yalnızca `summary` çıktısı. Gratis/marka tanıtım metni yok, kopyalama yok, marka beyanı aktarma yok.
5. `texts.json` > `ingredients`: **boş bırak** (`{}`). Madde metinleri merkezi olarak ayrı yazılıyor.
6. `synonyms.json`: `check`'in "tanınmayan madde" dediği her ad için, bariz yazım hatasıysa
   `{"GRATİS'TEKİ AD": "COSING ADI"}`. Hedef ad madde veritabanında olmalı (kontrol:
   `python -X utf8 -c "import sys; sys.path.insert(0,'scripts/skincare'); import os; os.chdir('scripts/skincare'); import analyze as a; print(a.Analyzer().resolve('AD'))"`
   None dönmemeli). Emin değilsen ya da madde gerçekten CosIng'de yoksa ürünü `excluded.json`'a "tanınmayan madde: …"
   gerekçesiyle taşı; uydurma eşleştirme yapma.
7. `python -X utf8 scripts/skincare/staging/tools.py check <marka>`: **"madde metni yok" / ingredients ile ilgili
   satırlar dışında HATA kalmamalı.** Diğer hataları düzelt.
8. `report.md`: eklenen/elenen sayısı, eşanlamlar ve gerekçeleri, şüpheli durumlar.

## Kesin kurallar

- Yalnızca sana verilen markaların `staging/<marka>/` klasörüne yaz. `catalog.json`, `texts_tr.json`, `analyze.py`,
  `raw/` (üst klasör), `out/`, `lib/`, `app/`, `gratis/` ve başka markaların klasörleri yasak.
- `build_data.py`, `push_to_db.mjs`, `merge.py`, `fetch_images.mjs`, `git` çalıştırma. Veritabanına dokunma. Ağ isteği atma.
- Bir marka bitince sıradakine geç; sonunda her marka için tek satır özet ver: `<marka>: +N ürün, -M elendi, K eşanlam, check: 0 hata`.
