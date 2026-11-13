"""Maruderm ürün açıklamaları (2026-11-12). Marka sitesindeki içerik listesinden (35 ürün) ya da Gratis'ten (2 ürün)
yazıldı; oranlar markaya atfedilir, "parfüm/alkol yok" ifadeleri analiz sonucuna göre içerik listesinden doğrulanır.
İç analiz dili, tıbbi iddia, marka beyanı aktarımı yok. Uygulama: python -X utf8 urun_metni.py maruderm_aciklamalar_20261112 --write
"""
SUN = "Koruma için yeterli miktarda sürülmeli ve iki saatte bir yenilenmeli."
SPRAY = "Koruma için yeterli miktarda sürülmeli; iki saatte bir ve yüzme ya da terleme sonrası yenilenmeli."
FUNGAL_SA = "Stearik asit nedeniyle fungal akneye yatkın ciltlerde dikkatli denenmeli."
RETINOL = ("Retinol ilk haftalarda kuruluk, soyulma ve hassasiyet yapabilir: haftada birkaç akşamla başlamak ve gündüz "
           "güneş koruyucu kullanmak gerekir. Hamilelik ve emzirme döneminde kullanmadan önce doktora danışılmalı.")
MILD = ("temizleme gücünü kokamidopropil betain, lauril glukozit ve sodyum lauril glukoz karboksilat gibi yumuşak yüzey "
        "aktif maddelerden alıyor; listede sülfat yok.")

TEXT = {
"maruderm-barrier-repair-ceramide-cream":
    "Cilt bariyerini desteklemeye odaklanan, 200 ml'lik bir nemlendirici bakım kremi; marka pantenol oranını %6 olarak "
    "veriyor. Pantenol listenin ikinci sırasında; ardından gliserin, niasinamid, shea yağı ve seramid NP geliyor. Skualan, "
    "sodyum hyalüronat, sodyum PCA ve allantoin de formülde. Listede parfüm ve alkol yok; sonlara doğru az miktarda silikon "
    "(dimetikonol, siklopentasiloksan) bulunuyor. Üst sıralardaki shea yağı nedeniyle yağlı ve fungal akneye yatkın "
    "ciltlerde dikkatli denenmeli.",
"maruderm-gozenek-sikilastirici-bha-ve-peptit-cilt-bakim-serumu":
    "Gözenek ve siyah nokta görünümünü hedefleyen, su bazlı bir BHA serumu; marka salisilik asit oranını %2 olarak "
    "veriyor. Listenin başında niasinamid ve salisilik asit var; onları bezelye peptidi ve pantenol izliyor. Listede "
    "parfüm, alkol, yağ ve silikon yok. Salisilik asit kuruluk ve hassasiyet yapabilir; ilk haftalarda gün aşırı kullanmak "
    "ve gündüz güneş koruyucu sürmek iyi olur. Başka asit ya da retinol içeren ürünlerle aynı akşam kullanmak tahriş "
    "riskini artırır.",
"maruderm-c-vitamini-ve-peptid-aydinlatici-cilt-bakim-serumu":
    "Marka %10 sodyum askorbil fosfat içerdiğini belirttiği, su bazlı bir C vitamini serumu. Sodyum askorbil fosfat, "
    "saf askorbik aside göre daha kararlı ve genellikle daha nazik bir C vitamini türevi; listenin ikinci sırasında. "
    "Ardından niasinamid, bezelye peptidi ve pantenol geliyor. Listede parfüm, alkol, yağ ve silikon yok. Gündüz güneş "
    "koruyucuyla birlikte kullanılmalı.",
"maruderm-hyaluronik-asit-nemlendirici-yuz-ve-vucut-cilt-bakim-kremi":
    "Yüzde ve vücutta kullanılabilen, 200 ml'lik bir nemlendirici krem. Listenin başında gliserin ve niasinamid var; "
    "onları Solidago virgaurea özütü, shea yağı, sodyum hyalüronat, pantenol ve allantoin izliyor. Üre ve E vitamini "
    "asetatı da formülde; sonlarda düşük miktarda dimetikon ve laktik asit bulunuyor. Listede parfüm yok. Shea yağı, setil "
    "stearat ve stearik asit nedeniyle fungal akneye yatkın ciltlerde dikkatli denenmeli.",
"maruderm-gozenek-sikilastirici-siyah-nokta-ve-akne-karsiti-bha-tonik":
    "Gözenek ve siyah nokta görünümü için hazırlanmış bir BHA toniği; marka salisilik asit oranını %2 olarak veriyor. "
    "Gliserin ve izopentildiolün ardından niasinamid ve salisilik asit geliyor; pantenol, papatya ve aloe vera özleri de "
    "formülde. Düşük miktarda yumuşak temizleyiciler (lauril glukozit, kokamidopropil betain) ile hidrolize buğday ve soya "
    "proteinleri var. Listede parfüm ve alkol yok. Salisilik asit kuruluk yapabilir; ilk haftalarda gün aşırı kullanmak ve "
    "gündüz güneş koruyucu sürmek iyi olur.",
"maruderm-niacinamide-10-hyaluronik-asit-panthenol-cilt-bakim-serumu":
    "Marka %10 niasinamid içerdiğini belirttiği, sebum ve gözenek görünümüne yönelik su bazlı bir serum. Niasinamid "
    "listenin ikinci sırasında; ardından gliserin, pantenol ve allantoin geliyor. Hyalüronik asit dört farklı formda "
    "(sodyum hyalüronat, hidrolize, saf ve çapraz bağlı) bulunuyor; hidrolize glikozaminoglikan da nem tarafını "
    "destekliyor. Listede parfüm, alkol, yağ ve silikon yok. Yüksek oranda niasinamid bazı ciltlerde ilk kullanımlarda "
    "kızarıklık yapabilir.",
"maruderm-azelaik-asit-10-aydinlatici-leke-karsiti-cilt-bakim-serumu":
    "Leke ve kızarıklık görünümüne yönelik bir azelaik asit serumu; marka oranı %10 olarak veriyor. Azelaik asit "
    "listenin üçüncü sırasında, poligliserin-6'dan hemen sonra; ardından niasinamid, pantenol, sodyum hyalüronat ve "
    "allantoin geliyor. Listede parfüm, alkol, yağ ve silikon yok. Azelaik asit ilk kullanımlarda hafif batma ya da "
    "kaşıntı hissi verebilir. Gündüz güneş koruyucuyla birlikte kullanılmalı.",
"maruderm-yag-bazli-temizleyici-yuz-ve-vucut-icin-temizleme-yagi":
    "Marka bu ürünü çift aşamalı temizliğin ilk adımı için yağ bazlı bir temizleyici olarak tanıtıyor; yüzde ve vücutta "
    "kullanılabiliyor. Listede bitkisel yağ yok: temizleme gücünü ilk sıradaki PEG-7 gliseril kokoat (hindistan cevizi "
    "yağından türetilen yağımsı bir ester) ile lauril glukozit, sodyum C14-16 olefin sülfonat ve kokamidopropil betain "
    "gibi yüzey aktif maddelerden alıyor. Niasinamid, çinko PCA ve pantenolün yanında dulavratotu, su teresi, ardıç, "
    "lavanta, civanperçemi ve arnika özütleri var. Listede eklenmiş parfüm yok, ancak AB'de koku alerjeni olarak "
    "bildirilen benzil alkol bulunuyor.",
"maruderm-salisilik-asit-cay-agaci-yagi-kil-maskesi":
    "Kaolin kili bazlı, gözenek ve siyah nokta görünümüne yönelik bir yüz maskesi. Kaolinin ardından setearil alkol ve "
    "gliseril stearat geliyor; çay ağacı yağı altıncı, salisilik asit sekizinci sırada. Gliserin, salatalık özütü ve "
    "pantenol de formülde. Eklenmiş parfüm yok, ancak çay ağacı yağı uçucu bir yağ olduğu için hassas ciltlerde tahriş "
    "edebilir. Gliseril stearat ve gliseret-2 kokoat nedeniyle fungal akneye yatkın ciltlerde dikkatli kullanılmalı.",
"maruderm-50-spf-pembe-ton-esitleyici-yuz-gunes-kremi":
    "Cilde pembe bir ton veren (tone-up) SPF 50+ / PA++++ yüz güneş kremi. Filtre tarafı karma: çinko oksidin yanında "
    "Tinosorb S, Tinosorb M ve etilheksil triazon kullanılıyor. Listede pembe renkli bir mineral pigment olan kalamin "
    "bulunuyor; centella özü, sodyum hyalüronat, allantoin ve pantenol de formülde. Listede parfüm ve alkol yok. "
    + FUNGAL_SA + " " + SUN,
"maruderm-50-spf-nemlendirici-yuz-gunes-kremi":
    "Karma filtreli bir SPF 50+ / PA++++ yüz güneş kremi: mineral filtre çinko oksidin yanında Tinosorb S, Tinosorb M "
    "ve etilheksil triazon kullanılıyor. Marka ektoin ve hyalüronik asidi öne çıkarıyor; listede ektoin, seramid NP, "
    "birkaç farklı hyalüronik asit türü, pantenol ve allantoin var. Listede parfüm ve alkol yok. " + FUNGAL_SA + " "
    "Koruma için yeterli miktarda sürülmeli; iki saatte bir ve terleme ya da yüzmeden sonra yenilenmeli.",
"maruderm-10-urea-ure-yogun-nemlendirici-vucut-kremi":
    "Çok kuru ve pürüzlü ciltler için yoğun bir vücut kremi; marka üre oranını %10 olarak veriyor. Üre listenin ikinci "
    "sırasında; ardından gliserin, shea yağı ve pantenol geliyor, salatalık ve aynısefa özütleri ile allantoin de "
    "formülde. Açık çatlak ya da tahriş olmuş ciltte batma hissi verebilir. Listede parfüm var; kokuya hassas olanlar "
    "bunu göz önünde bulundurmalı. Shea ve ayçiçeği yağı nedeniyle sırt ve göğüs gibi fungal akneye yatkın bölgelerde "
    "dikkatli kullanılmalı.",
"maruderm-c-vitamini-yuz-yikama-jeli":
    "İki C vitamini türevi (etil askorbik asit ve sodyum askorbil fosfat) içeren bir yüz yıkama jeli. Jel " + MILD + " "
    "Pantenol, niasinamid ve aloe vera da formülde. Listede parfüm ve alkol yok. Durulanan bir üründe C vitamini "
    "türevleri ciltte kısa süre kalır; aydınlatma için asıl iş serum ve güneş koruyucuya düşer.",
"maruderm-retinol-0-3-cilt-yenileyici-bakim-serumu":
    "Marka retinol oranını %0,3 olarak veriyor; retinol listenin dokuzuncu sırasında. Yanında sık sık retinol "
    "alternatifi olarak anılan bakuchiol, koenzim Q10 ve yeşil çay özütü bulunuyor; sodyum hyalüronat, gliserin ve "
    "pantenol nem desteği veriyor. " + RETINOL + " Onuncu sıradaki etilheksil palmitat Fulton (1989) çalışmasında "
    "yüksek komedojenlik puanı (4) almış; bu madde ve stearik asit, fungal akneye yatkın ciltlerde sorun çıkarabilir.",
"maruderm-spf-50-cocuklar-icin-hassas-koruma-sprey-gunes-kremi":
    "Marka çocuklar için tasarladığı, mineral ve geniş spektrumlu olarak tanıttığı SPF 50+ / PA++++ bir güneş spreyi. "
    "Listenin başında çinko oksit var, ancak formül yalnızca mineral değil: etilheksil triazon, Tinosorb S ve Uvinul A "
    "Plus gibi organik filtreler de kullanılıyor. E vitamini asetatı ve pantenol de formülde. Listede parfüm ve alkol "
    "yok. Stearik asit nedeniyle fungal akneye yatkın ciltlerde dikkatli kullanılmalı. " + SPRAY,
"maruderm-pirinc-ozlu-aydinlatici-yuz-temizleme-jeli":
    "Pirinç tohum suyu ve pirinç özütü içeren, yumuşak bir yüz temizleme jeli. Pirinç tohum suyu listenin ikinci "
    "sırasında; jel " + MILD + " Gliserin, yeşil çay özütü, pantenol ve aloe vera suyu da formülde. Listede parfüm ve "
    "alkol yok.",
"maruderm-pirinc-ozlu-aydinlatici-tonik":
    "Pirinç tohum suyu bazlı, nem odaklı bir yüz toniği. Pirinç tohum suyunun ardından propilen glikol, gliserin ve "
    "pirinç özütü geliyor; sodyum hyalüronat, centella özü ve pantenol de formülde. Listede parfüm ve alkol yok. Peeling "
    "amaçlı asit içermiyor; temizlik sonrası nem adımı olarak düşünülebilir.",
"maruderm-bakuchiol-yuz-bakim-kremi":
    "Retinol yerine bakuchiol kullanan bir yüz kremi; marka onu retinol alternatifi olarak tanıtıyor. Bakuchiol listenin "
    "dördüncü sırasında; gliserin, pantenol, sodyum hyalüronat, skualan ve centella özütü ile birlikte. Allantoin ve "
    "sodyum PCA da formülde. Listede parfüm, alkol, yağ ve silikon yok. Bakuchiol retinole göre daha az tahriş edici "
    "kabul edilse de üzerine yapılan çalışmalar retinole göre çok daha az.",
"maruderm-yenileyici-toz-peeling-adet":
    "Birkaç damla suyla köpürtülerek kullanılan, toz formda bir yüz peelingi; marka %1 laktik asit, %0,8 azelaik asit ve "
    "%0,5 malik asit içerdiğini belirtiyor. Toz, mısır nişastası ve yumuşak bir temizleyici olan sodyum kokoil izetionat "
    "bazlı; pancar kökü ve yaban mersini özütleri, papain enzimi ve allantoin de formülde. Asit oranları düşük ve ürün "
    "durulandığı için hafif bir peeling; yine de hassas ciltlerde haftada birkaç kullanımla başlamak iyi olur. Sodyum "
    "palmitat nedeniyle fungal akneye yatkın ciltlerde dikkatli denenmeli.",
"maruderm-leke-karsiti-ve-beyazlatici-cilt-bakim-serumu":
    "Leke ve ton eşitsizliği görünümüne yönelik bir serum; marka %2 alfa arbutin içerdiğini belirtiyor. Listenin "
    "başında niasinamid var; onu propilen glikol, meyan kökü özütü, alfa arbutin, pantenol ve bezelye peptidi izliyor. "
    "Listede parfüm, alkol, yağ ve silikon yok. Gündüz güneş koruyucuyla birlikte kullanılmalı.",
"maruderm-kolajen-ve-hyaluronik-asit-cilt-bakim-serumu":
    "Marka %5 kolajen ve %2 hyalüronik asit içerdiğini belirttiği bir serum. Hidrolize kolajen listenin ikinci "
    "sırasında; ardından niasinamid, bezelye peptidi, pantenol ve sodyum hyalüronat geliyor. Hidrolize kolajen cilt "
    "yüzeyinde nem tutucu ve film oluşturucu olarak çalışır; cildin kendi kolajeninin yerine geçmez. Listede parfüm, "
    "alkol, yağ ve silikon yok.",
"maruderm-hassas-ve-atopik-ciltler-icin-yuz-yikama-jeli":
    "Marka hassas ve atopik ciltler için önerdiği, yumuşak bir yüz temizleme jeli. Gliserinin ardından kokamidopropil "
    "betain, lauril glukozit ve sodyum lauril glukoz karboksilat gibi yumuşak yüzey aktif maddeler geliyor; listede "
    "sülfat yok. Pantenol, papatya ve aloe vera özleri ile hidrolize buğday, soya ve mısır proteinleri de formülde. "
    "Listede parfüm ve alkol yok. Buğday ve soya proteinleri, bu maddelere alerjisi olanlar için not edilmeli.",
"maruderm-kafein-5-peptit-hyaluronik-asit-goz-cevresi-serumu":
    "Marka %5 kafein içerdiğini belirttiği, şişlik ve morluk görünümüne yönelik bir göz çevresi serumu. Kafein listenin "
    "ikinci sırasında; ardından gliserin, pantenol ve sodyum hyalüronat geliyor. Üç peptid (asetil tetrapeptid-5, "
    "palmitoil pentapeptit-4, asetil heksapeptid-8), allantoin ve farklı formlarda hyalüronik asit de formülde. Listede "
    "parfüm, alkol, yağ ve silikon yok.",
"maruderm-retinol-0-5-cilt-yenileyici-bakim-serumu":
    "Marka %0,5 retinol içerdiğini belirttiği, su içermeyen yağ bazlı bir serum; ilk sıralarda C12-15 alkil benzoat ve "
    "skualan var. Jojoba, kayısı çekirdeği, tatlı badem, avokado, nar çekirdeği, kuşburnu tohumu ve ayçiçeği "
    "yağlarından sonra retinol ve retinil palmitat geliyor; seramid NP, E vitamini asetatı ve az miktarda silikon da "
    "formülde. " + RETINOL + " Yoğun yağ içeriği ve Fulton (1989) çalışmasında komedojenlik puanı 3 olan avokado yağı "
    "nedeniyle akneye ve fungal akneye yatkın ciltler için uygun değil.",
"maruderm-niacinamide-10-leke-karsiti-ve-gozenek-sikilastirici-krem":
    "Marka %10 niasinamid içerdiğini belirttiği, leke ve gözenek görünümüne yönelik 200 ml'lik bir bakım kremi. "
    "Niasinamid listenin ikinci sırasında; ardından gliserin, shea yağı, skualan, pantenol ve allantoin geliyor. Sodyum "
    "hyalüronat ve sodyum PCA da formülde. Listede parfüm, alkol ve silikon yok. Shea yağı nedeniyle yağlı ve fungal "
    "akneye yatkın ciltlerde dikkatli denenmeli.",
"maruderm-glycolic-acid-7-aydinlatici-ve-leke-karsiti-tonik":
    "Marka %7 glikolik asit içerdiğini belirttiği bir AHA toniği. Glikolik asit listenin ikinci sırasında; meyan kökü "
    "özütü, pantenol ve farklı formlarda hyalüronik asit de formülde. Arnika, dulavratotu, su teresi, ardıç, lavanta ve "
    "civanperçemi özütleri de var. Listede eklenmiş parfüm yok, ancak AB'de koku alerjeni olarak bildirilen benzil alkol "
    "bulunuyor. %7 glikolik asit hassas ciltlerde batma ve kızarıklık yapabilir: gün aşırı akşam kullanımıyla başlamak, "
    "retinol ve diğer asitlerle aynı akşam kullanmamak ve gündüz güneş koruyucu sürmek gerekir.",
"maruderm-karma-ve-yagli-ciltlere-ozel-salisilik-asit-yuz-yikama-jeli":
    "Karma ve yağlı ciltler için salisilik asitli bir yüz temizleme jeli. Jel " + MILD + " Salisilik asit yedinci "
    "sırada; pantenol, papatya ve aloe vera özleri ile hidrolize buğday, soya ve mısır proteinleri de formülde. Listede "
    "parfüm ve alkol yok. Durulanan bir üründe salisilik asit ciltte kısa süre kalır; yine de kuruluk olursa kullanım "
    "sıklığı azaltılabilir.",
"maruderm-50-spf-100-mineral-filtre-yuz-gunes-kremi":
    "Filtre olarak yalnızca çinko oksit kullanan, SPF 50+ / PA++++ bir yüz güneş kremi. Çinko oksit listenin ikinci "
    "sırasında; gliserin, C12-15 alkil benzoat ve kaprilik/kaprik trigliseritin ardından pantenol, sodyum hyalüronat ve "
    "allantoin geliyor. Listede parfüm ve alkol yok. Mineral filtreler ciltte hafif beyazlık bırakabilir. " + FUNGAL_SA
    + " " + SUN,
"maruderm-50-spf-leke-karsiti-yuz-gunes-kremi":
    "Leke görünümüne yönelik içerikler barındıran, SPF 50+ / PA++++ bir yüz güneş kremi. Filtre tarafı karma: Tinosorb "
    "S, çinko oksit, etilheksil triazon ve Tinosorb M. Marka alfa arbutini öne çıkarıyor; listede alfa arbutin, "
    "niasinamid, meyan kökü özütü ve diasetil boldin var, pirinç kepeği suyu da ikinci sırada. Listede parfüm ve alkol "
    "yok. " + FUNGAL_SA + " " + SUN,
"maruderm-c-vitamini-spf-50-gunes-kremi":
    "C vitamini türevi sodyum askorbil fosfat içeren, SPF 50+ / PA++++ bir yüz güneş kremi. Filtre tarafı karma: "
    "Tinosorb S, etilheksil triazon, çinko oksit ve Tinosorb M. Sodyum askorbil fosfatın yanında yeşil çay özütü, "
    "seramid NP, farklı formlarda hyalüronik asit, allantoin ve pantenol var. Listede parfüm ve alkol yok. " + FUNGAL_SA
    + " " + SUN,
"maruderm-hyaluronik-asit-nemlendirici-vucut-kremi":
    "Hyalüronik asit ve seramid içeren bir vücut nemlendiricisi. Gliserin ve pantenolün ardından shea yağı, skualan ve "
    "jojoba yağı geliyor; sodyum hyalüronat, seramid NP, sodyum PCA ve allantoin de formülde. Listede parfüm var; kokuya "
    "hassas olanlar bunu göz önünde bulundurmalı. Shea ve jojoba yağı nedeniyle sırt ve göğüs gibi fungal akneye yatkın "
    "bölgelerde dikkatli kullanılmalı.",
"maruderm-arindirici-toz-peeling-adet":
    "Birkaç damla suyla köpürtülerek kullanılan, toz formda bir yüz peelingi; marka %0,5 salisilik asit, %2 çay ağacı "
    "yağı ve %0,5 allantoin içerdiğini belirtiyor. Mısır nişastası ve sodyum kokoil izetionat bazlı; papain enzimi de "
    "formülde. Çay ağacı yağı listenin üçüncü sırasında; uçucu bir yağ olduğu için hassas ciltlerde tahriş edebilir. "
    "Sodyum palmitat nedeniyle fungal akneye yatkın ciltlerde dikkatli denenmeli.",
"maruderm-avokado-kirisiklik-karsiti-goz-cevresi-kremi":
    "Marka kırışıklık görünümüne yönelik olarak tanıttığı bir göz çevresi kremi. Gliserinin ardından alfa arbutin, "
    "pantenol, kafein ve sodyum hyalüronat geliyor; avokado yağı yedinci sırada. Üç peptid (asetil heksapeptid-8, "
    "palmitoil tripeptit-1, palmitoil tetrapeptit-7) ve sodyum PCA da formülde. Listede parfüm, alkol ve silikon yok. "
    "Avokado yağı Fulton (1989) çalışmasında komedojenlik puanı 3 almış; avokado yağı ve polisorbat 20 nedeniyle akneye "
    "ve fungal akneye yatkın ciltlerde dikkatli denenmeli.",
"maruderm-cica-cilt-tonu-esitleyici-15spf-krem":
    "Hafif renkli, SPF 15 bir yüz kremi; marka onu renk eşitleyici bir krem olarak tanıtıyor. Koruma titanyum "
    "dioksitten geliyor; rengi demir oksitler ve kızarıklığı kapatmak için renk düzeltmede kullanılan krom oksit yeşili "
    "veriyor. Dimetikonun ardından centella özü, gliserin ve niasinamid geliyor; madekasosid, pantenol, sodyum "
    "hyalüronat ve beta glukan da formülde. Listede parfüm ve alkol yok. SPF 15 gün boyu güneş koruması için yeterli "
    "değil; güneşe çıkılacaksa altına ayrı bir güneş kremi sürülmeli.",
"maruderm-pirinc-ozlu-aydinlatici-nemlendirici-krem":
    "Pirinç tohum suyu bazlı bir nemlendirici yüz kremi. Pirinç tohum suyunun ardından gliserin, propilen glikol ve "
    "pirinç özütü geliyor; sodyum hyalüronat, pantenol, seramid NP ve allantoin de formülde. Listede parfüm, alkol, yağ "
    "ve silikon yok.",
"maruderm-glikolik-asit-5-kil-yuz-maskesi":
    "Marka %5 glikolik asit içerdiğini belirttiği, kaolin kili bazlı bir yüz maskesi. Kaolinin hemen ardından glikolik "
    "asit geliyor; setearil alkol, setil alkol ve stearik asit kıvamı oluşturuyor, pantenol ve meyan kökü özütü de "
    "formülde. Listede parfüm yok. Glikolik asit hassas ciltlerde batma ve kızarıklık yapabilir; maske sonrası gündüz "
    "güneş koruyucu kullanılmalı. " + FUNGAL_SA,
"maruderm-tranexamic-asit-yuz-bakim-serumu":
    "Leke ve ton eşitsizliği görünümünü hedefleyen, su bazlı hafif bir serum. Listenin başında traneksamik asit ve alfa "
    "arbutin yer alıyor; onları C vitamini türevi etil askorbik asit, yaban mersini ve meyan kökü özütleri izliyor. "
    "Pantenol, allantoin ve bir amino asit karışımı nem tarafını destekliyor. Listede parfüm, alkol, yağ ve silikon yok. "
    "Marka gündüz kullanımında güneş koruyucuyla tamamlanmasını öneriyor.",
"maruderm-50-spf-leke-karsiti-vucut-gunes-spreyi":
    "Vücut için SPF 50+ bir güneş spreyi; leke görünümüne yönelik niasinamid ve alfa arbutin içeriyor. Filtre tarafı "
    "karma: etilheksil triazon, çinko oksit, Uvinul A Plus, Tinosorb S ve Tinosorb M. Arnika çiçeği özütü de formülde. "
    "Listede parfüm ve alkol yok. Stearik asit nedeniyle fungal akneye yatkın ciltlerde dikkatli kullanılmalı. " + SPRAY,
}
