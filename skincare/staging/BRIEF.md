# Ürün ekleme talimatı (paralel ajanlar)

Sen bir markanın **kalan cilt bakım ürünlerini** Uygun Bakım Cilt kataloğuna eklemek için hazırlık yapıyorsun.
Bir denetçi (Claude) işini kontrol edip birleştirecek ve veritabanına aktaracak. Aynı anda başka ajanlar başka
markalarda çalışıyor. Önce `docs/skincare-veri-kaynaklari.md` dosyasının 1, 2, 4 ve 5. bölümlerini oku.

## Çalışma alanı (KESİN KURAL)

- Yalnızca `scripts/skincare/staging/<marka>/` altına yaz. Başka hiçbir dosyayı **değiştirme**: `catalog.json`,
  `texts_tr.json`, `analyze.py`, `fetch_sources.py`, `raw/`, `out/`, `lib/`, `app/`, `docs/`.
- `build_data.py`, `push_to_db.mjs`, `fetch_images.mjs`, `git` **çalıştırma**. Veritabanına dokunma.
- Kaynak çekme, analiz ve denetim için yalnızca `scripts/skincare/staging/tools.py` kullan (kullanımı dosyanın başında).
  Komutları depo kökünden çalıştır: `python -X utf8 scripts/skincare/staging/tools.py ...`
- Çıkarıcı (fetch_sources.py) bir sayfada çalışmıyorsa kodu kendin düzeltme; sorunu ve önerini SORU olarak yaz.

## Kaynak kuralları

1. Tek kaynak markanın **Türkiye sitesi**. Skinsort, Amazon, INCIDecoder, pazar yerleri, başka siteler **kullanılmaz**.
2. İçerik listesini **asla elle yazma**; yalnızca `tools.py fetch` çıktısı geçerlidir. Çıkmıyorsa ürünü ele ve raporla.
3. Siteye nazik ol: istekler arası bekleme araçta var; aynı siteye paralel istek atma.

## Kapsam

- Markanın Türkiye sitesindeki, katalogda **henüz olmayan** tüm cilt bakım ürünleri (yüz, göz, dudak, el, vücut,
  hassas bölge, temizleme, makyaj temizleme). Katalogdaki mevcut ürünler `tools.py check` ile yakalanır.
- **Eklenmez:** BB krem, makyaj amaçlı CC krem, kompakt pudra ve fondöten (güneş serisindeki renkli güneş kremleri eklenir), güneş sonrası ve SPF'siz bronzlaştırıcılar, saç ve saçlı deri
  ürünleri (şampuan, losyon), deodorant/terleme karşıtı, renkli makyaj, yedek dolum (refill), set/kit/rutin/ikili
  paketler, aynı formülün farklı boyutu (tek ürün say). Elenen her şeyi `excluded.json`'a gerekçesiyle yaz.
- Aynı adın farklı formülleri (ör. normal ve "rich" sürüm) ayrı üründür.

## Ürün kaydı (`products.json`)

- `slug` = `<marka>-<ambalaj adı>` (küçük harf, tire). `name` = ambalajdaki ad (çoğunlukla İngilizce/Fransızca
  ürün adı, ör. "Effaclar Duo+M"). `nameTr` = düzgün yazılmış Türkçe ad (BÜYÜK HARF değil, marka adı tekrarlanmaz).
- `category`: `tools.py check`'in listelediği izinli kategorilerden biri; hiçbiri uymuyorsa SORU sor.
- `brandUrl`: ürünün Türkiye sitesindeki sayfası.

## Tutarlılık kontrolü (her ürün için)

- Sayfanın tanıttığı **ana aktif** (ör. "Thiamidol", "%10 niasinamid", "kömür", "retinol") içerik listesinde yoksa,
  sayfaya yanlış ürünün listesi konmuş olabilir: ürünü **ekleme**, `excluded.json` + report.md'ye yaz.
- Liste alanında tanıtım metni varsa (araç "ŞÜPHELİ / çok uzun öğe" der) ürünü ekleme, raporla.
- Listedeki bariz yazım hatalarını (eksik/yer değiştirmiş harf, birleşik kelime) `synonyms.json`'a ekle:
  `{"SİTEDEKİ AD": "COSING ADI"}`. Doğru adın CosIng karşılığından emin değilsen SORU sor. Uydurma eşleştirme yapma.
- `check` sonunda **tanınmayan madde kalmamalı**.

## Türkçe metinler (`texts.json`)

- `products`: her ürün için **3–5 cümle**, özgün Türkçe. `summary` çıktısındaki içerik listesine ve analize dayan:
  kime yönelik, öne çıkan aktifler ve ne işe yaradıkları, formül dokusu, neleri içerdiği / içermediği (analizle aynı),
  dikkat edilecek nokta (alkol, parfüm/uçucu yağ, asit + güneş, Fulton puanı yüksek madde ilk sıralarda vb.).
- **Marka beyanı aktarma:** "marka komedojenik olmadığını / parfüm içermediğini / dermatologlarla geliştirildiğini
  belirtiyor" gibi cümleler YASAK. Yalnızca listeden doğrulanabileni yaz (ör. "Listede eklenmiş parfüm yok; ancak uçucu
  yağlar koku veriyor"). Aktif oranı ve kullanım bilgisi (ör. "%10 niasinamid", "akşam kullanım") yazılabilir.
- Tıbbi iddia, teşhis, tedavi, "hamilelikte güvenli" gibi ifadeler yok. Marka metnini kopyalama/çevirme.
- `ingredients`: `summary`'nin "METNİ YOK" dediği her madde için `{"nameTr", "description"}`. nameTr Türkçe yaygın ad
  (yoksa INCI'nin okunuşu; ör. "Ceteareth-12"), description 1–2 cümle: ne işe yarar, varsa dikkat noktası (AB koku
  alerjeni, uçucu yağ, yüksek komedojenlik puanı). Var olan metinleri tekrar yazma. Emin olmadığın bilgiyi yazma.

## Görsel

- `fetch` çıktısındaki görsel adresine bak: ürün ambalajı mı, kampanya/yaşam tarzı fotoğrafı mı? Kampanya ise aynı
  marka sitesinde (kategori sayfası, galeri, ld+json image listesi) **ambalaj fotoğrafı** ara; bulursan ürüne
  `"imageUrl"` ekle. Bulamazsan report.md'ye yaz. Görseli indirme/dönüştürme denetçinin işi.

## Bitirme

1. `python -X utf8 scripts/skincare/staging/tools.py check <marka>` → **0 HATA** olmalı.
2. `report.md`: kaç sayfa tarandı, eklenen ürünler (slug | ad | kategori | madde sayısı), elenenler ve gerekçeleri,
   yazım hatası eşleştirmeleri ve gerekçeleri, görsel notları, şüpheli durumlar.
3. Son mesajın tek satırla bitsin: `DURUM: BİTTİ` ya da karar gerekiyorsa `DURUM: SORU` ve altında numaralı sorular.
   Soru sorduğunda bekle; denetçi aynı oturumda cevap verecek. Kendi başına riskli karar verme.
