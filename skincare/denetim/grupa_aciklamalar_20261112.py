"""Grup A (Nivea, Rimu Health, Mary&May) ürün açıklamaları (2026-11-12). Gratis içerik listelerinden yazıldı; Nivea epigenetics
göz serumu, Rimu Health krem/serum/tonik listeleri marka sitesiyle karşılaştırıldı. Oranlar ve hedef kitle ürün adına atfedilir.
Uygulama: python -X utf8 urun_metni.py grupa_aciklamalar_20261112 --write
"""
SUN = "Koruma için yeterli miktarda sürülmeli ve iki saatte bir yenilenmeli."
AHA_NOTE = ("AHA ve BHA kuruluk ve hassasiyet yapabilir; ilk zamanlarda gün aşırı denemek ve gündüz güneş koruyucu "
            "kullanmak gerekir.")
BODY_FUNGAL = "Fungal akneye yatkın bölgelerde dikkatli denenmeli."

TEXT = {
"mary-may-deniz-kolajeni-icerikli-yuz-serumu":
    "Nem odaklı, su bazlı bir yüz serumu. Su, gliseret-26 ve 1,2-heksandiolün ardından etilheksilgliserin ve hidrolize "
    "kolajen geliyor; arjinin, kaprilil glikol, adenozin ve karbomer de formülde. Ürün adındaki \"deniz kolajeni\" "
    "ifadesine karşın listede kolajen yalnızca hidrolize kolajen olarak geçiyor, kaynağı belirtilmemiş. Listede parfüm, "
    "alkol, yağ ve silikon yok; kısa ve sade bir içerik listesi.",
"mary-may-bogurtlen-kompleksi-ozu-iceren-cift-fazli-yogun-kivamli-yuz-krem-esansi":
    "Böğürtlen özlü, çift fazlı bir yüz krem esansı; kullanmadan önce çalkalanması gerekiyor. Su ve jojoba yağının ardından "
    "hidrojene poli(C6-14 olefin), pentilen glikol ve mavi nilüfer çiçek suyu geliyor. Böğürtlen, patlıcan, üzüm ve dut "
    "özleri listenin ortasında; centella özü, sodyum hyalüronat, seramid NP, madekasosid ve asiatikozit sonlarda. "
    "Listede parfüm ve alkol yok. Jojoba yağı ikinci sırada ve fungal akneye yatkın ciltlerde dikkatli denenmeli.",

"nivea-canlandirici-yuz-temizleme-jeli-normal-ve-karma-ciltler-icin":
    "Normal ve karma ciltler için tanımlanan, yüz temizleme jeli. Su ve gliserinin ardından koko glukozit ve koko betain "
    "gibi yumuşak temizleyiciler geliyor; aloe vera yaprak suyu tozu ve sodyum hyalüronat da formülde. Denatüre alkol "
    "beşinci sırada, ayrıca listenin sonlarında parfüm var; kuruluğa ya da kokuya hassas olanlar bunu göz önünde "
    "bulundurmalı. Boya olarak iki renk maddesi (CI 42090, CI 16035) kullanılmış.",
"nivea-luminous630-thiamidol-etkili-koyu-halka-karsiti-goz-bakim-kremi":
    "Adına göre koyu halka görünümüne yönelik, Thiamidol içeren bir göz çevresi kremi. Su, gliserin ve metilpropandiolün "
    "ardından dikaprilil karbonat, gliseril stearat ve setearil alkol geliyor; Thiamidol (izobutilamido tiazolil "
    "resorsinol) listenin 13. sırasında, sodyum hyalüronat, kafein ve E vitamini ise onu izliyor. Listede parfüm ve "
    "alkol yok. Hidrojene bitkisel yağ yedinci sırada ve Fulton (1989) çalışmasında komedojenlik puanı 3 almış; bu "
    "yağ, gliseril stearat ve hindistan cevizi gliseritleri nedeniyle fungal akneye yatkın ciltlerde dikkatli denenmeli.",
"nivea-hydro-care-nemlendirici-renksiz-dudak-bakim-kremi":
    "Renksiz, nemlendirici bir dudak bakım kremi. Listenin başında ayçiçeği tohumu mumu, shea yağı ve poligliseril-3 "
    "diizostearat var; ardından avobenzon ve etilheksil triazon gibi iki UV filtresi geliyor, ama ürün adında SPF değeri "
    "belirtilmemiş. E vitamini, askorbil palmitat ve ayçiçeği yağı sonlarda. Listede aroma ile linalool, sitronellol ve "
    "sitral gibi koku alerjenleri var; kokuya hassas olanlar bunu göz önünde bulundurmalı. Poligliseril-3 diizostearat "
    "Fulton (1989) çalışmasında komedojenlik puanı 4 almış; shea yağı ve hidrojene hint yağı da fungal akne açısından not edilmeli.",
"nivea-luminous630-thiamidol-etkili-leke-karsiti-gece-yuz-bakim-kremi":
    "Adına göre leke görünümüne yönelik, Thiamidol içeren bir gece yüz kremi. Su ve gliserinin ardından kaprilik/kaprik "
    "trigliserit, hindistan cevizi gliseritleri, setearil alkol ve setil palmitat geliyor; shea yağı 12., Thiamidol "
    "(izobutilamido tiazolil resorsinol) 13. sırada. Sodyum hyalüronat, pantenol ve pantolakton da formülde. Listenin "
    "sonunda parfüm var; alkol yok. Hindistan cevizi gliseritleri, setil palmitat, gliseril stearat ve shea yağı "
    "nedeniyle fungal akneye yatkın ciltlerde dikkatli denenmeli.",
"nivea-epigenetics-yaslanma-ve-kirisiklik-karsiti-goz-serumu":
    "Adına göre yaşlanma ve kırışıklık görünümüne yönelik bir göz serumu. Su ve gliserinin ardından üçüncü sırada denatüre "
    "alkol var; seteret-20 ve mercanköşk yaprak özü izliyor. Dört farklı hyalüronat türü, palmitoil tripeptit-5 ve "
    "kreatin listenin ortasında. Listede parfüm yok. Alkol ve seteret-20 (Fulton tahriş puanı 3) göz çevresi gibi hassas "
    "bölgede tahriş yapabilir; kuruluğa ya da hassasiyete yatkınlar önce küçük bir alanda denemeli.",
"nivea-glowy-lips-nemlendirici-dudak-parlaticisi-ve-bakim-kremi":
    "Parlaklık veren, nemlendirici bir dudak bakım kremi. Listenin başında oktildodekanol, hint yağı, hindistan cevizi "
    "gliseritleri, kaprilik/kaprik trigliserit ve shea yağı yer alıyor; hidrojene kolza yağı ve poligliseril-3 diizostearat "
    "da var. Sodyum hyalüronat, E vitamini ve askorbil palmitat sonlarda. Koku 'aroma' adıyla katılmış. Poligliseril-3 "
    "diizostearat dokuzuncu sırada ve Fulton (1989) çalışmasında komedojenlik puanı 4 almış; hint yağı, shea yağı ve "
    "hidrojene yağlar nedeniyle fungal akneye yatkın ciltlerde dikkatli denenmeli.",
"nivea-c-vitamini-iceren-ultra-hafif-enerji-nemlendirici-yuz-bakim-kremi":
    "Hafif dokulu, C vitamini türevi içeren bir yüz nemlendiricisi. Su ve gliserinin ardından üçüncü sırada denatüre alkol "
    "var; sonra tapyoka nişastası, setearil izononanoat, izopropil palmitat ve skualan geliyor. Askorbil glukozit "
    "dokuzuncu, sodyum hyalüronat onuncu sırada. Listede limonen ve parfüm de bulunuyor; kokuya ve alkole hassas olanlar "
    "bunu göz önünde bulundurmalı. Altıncı sıradaki izopropil palmitat Fulton (1989) çalışmasında komedojenlik puanı 4 "
    "almış; akneye ve fungal akneye yatkın ciltlerde dikkatli denenmeli.",
"nivea-super10-serum-etkili-aydinlatici-ve-nemlendirici-vucut-losyonu":
    "Serum etkili, aydınlatıcı ve nemlendirici bir vücut losyonu. Su, gliserin ve denatüre alkolün ardından C12-15 alkil "
    "benzoat ve tapyoka nişastası geliyor; avobenzon, oktokrilen ve ensulizol gibi UV filtreleri de listede, ancak adında "
    "SPF değeri yok. Niasinamid, sodyum askorbil fosfat, avokado yağı, retinil palmitat, tokoferil asetat ve pantenol "
    "ortalarda; listenin sonunda parfüm var. Retinil palmitat hafif bir retinoid türevi olsa da hamilelik ve emzirmede "
    "kullanmadan önce doktora danışılmalı. Avokado yağı (Fulton 3) ve retinil palmitat nedeniyle fungal akneye yatkın "
    "bölgelerde dikkatli denenmeli.",
"nivea-yatistirici-ve-nemlendirici-el-bakim-kremi-aloe-vera":
    "Aloe vera içeren, yatıştırıcı ve nemlendirici bir el kremi. Su, gliserin, setearil alkol ve gliseril stearatın "
    "ardından mikrokristalin mum, setearil izononanoat ve C12-15 alkil benzoat geliyor; aloe vera suyu sekizinci sırada. "
    "Jojoba yağı, dimetikon ve sıvı parafin (mineral yağ) de formülde. Metilparaben koruyucu olarak kullanılmış. "
    "Listede parfüm ile linalool, sitronellol, benzil alkol, geraniol, limonen ve alfa-izometil ionon var; kokuya "
    "hassas olanlar bunu göz önünde bulundurmalı. Jojoba yağı, gliseril stearat ve çeşitli yağ asitleri nedeniyle "
    "fungal akneye yatkın ciltlerde dikkatli denenmeli.",
"nivea-yatistirici-yuz-temizleme-kopugu-kuru-ve-hassas-ciltler":
    "Kuru ve hassas ciltler için tanımlanan bir yüz temizleme köpüğü. Su, sorbitol ve gliserinin ardından desil glukozit "
    "ve disodyum kokoil glutamat gibi yumuşak temizleyiciler geliyor; argan yağı ve sodyum hyalüronat da formülde. "
    "Listede alkol yok, ama sonlarda parfüm bulunuyor; kokuya hassas olanlar bunu göz önünde bulundurmalı. Argan yağı "
    "altıncı sırada ve fungal akneye yatkın ciltlerde dikkatli denenmeli.",
"nivea-koruyucu-ve-nemlendirici-el-bakim-kremi-bal-mumu":
    "Bal mumu içeren, koruyucu ve nemlendirici bir el kremi. Su, gliserin ve setil alkolün ardından dördüncü sırada "
    "izopropil palmitat, sonra gliseril stearat, bal mumu ve kaprilik/kaprik trigliserit geliyor. Ayrıca stearik, "
    "palmitik, miristik, araşidik, oleik ve laurik asit gibi yağ asitleri de var. Listenin sonunda parfüm bulunuyor. "
    "İzopropil palmitat Fulton (1989) çalışmasında komedojenlik puanı 4 almış; laurik asit de aynı puanda. Fungal akneye "
    "yatkın ciltlerde dikkatli denenmeli.",
"nivea-cift-fazli-goz-makyaj-temizleyici":
    "Çift fazlı bir göz makyajı temizleyicisi. Su, izododekan ve C15-19 alkandan "
    "sonra dördüncü sırada izopropil palmitat geliyor; etilheksil kokoat, gliserin ve dikaprilil eter onu izliyor. "
    "Biyotin, peygamber çiçeği özü, ayçiçeği yağı ve E vitamini ortalarda. Listede parfüm ve alkol yok. İzopropil palmitat "
    "Fulton (1989) çalışmasında komedojenlik puanı 4 almış; etilheksil kokoat ve ayçiçeği yağıyla birlikte fungal akneye "
    "yatkın ciltlerde dikkatli denenmeli.",
"nivea-zeytinyagi-nemlendirici-el-bakim-kremi":
    "Zeytinyağı içeren, nemlendirici bir el kremi. Su, gliserin, setearil alkol ve gliseril stearatın ardından setearil "
    "izononanoat ve hidrojene hindistan cevizi gliseritleri geliyor; zeytin meyve yağı yedinci sırada. Dimetikon da "
    "formülde. Listede parfüm ile linalool, alfa-izometil ionon, benzil alkol, benzil salisilat ve geraniol var; kokuya "
    "hassas olanlar bunu göz önünde bulundurmalı. Zeytin yağı, gliseril stearat ve çeşitli yağ asitleri nedeniyle fungal "
    "akneye yatkın ciltlerde dikkatli denenmeli.",
"nivea-canlandirici-ve-nemlendirici-tonik-normal-karma-ciltler":
    "Normal ve karma ciltler için tanımlanan, canlandırıcı bir tonik. Su ve ikinci sırada denatüre alkolün ardından aloe "
    "vera yaprak suyu tozu, sodyum hyalüronat ve gliserin geliyor; selüloz gamı, poligliseril-4 kaprat ve kaprilil glikol "
    "sonlarda. Listenin sonunda parfüm var. Alkol ve parfüm nedeniyle kuruluğa ya da kokuya hassas ciltler dikkatli "
    "olmalı.",
"nivea-luminous630-skin-glow-aydinlatici-yuz-temizleme-jeli":
    "Aydınlatıcı etkisi hedeflenen bir yüz temizleme jeli. Su ve ikinci sırada denatüre alkolün ardından sodyum "
    "kokoamfoasetat, gliserin ve koko betain gibi temizleyiciler geliyor; laktik asit altıncı, glikolik asit dokuzuncu "
    "sırada. Aloe vera yaprak suyu tozu, guarana özü, kafein ve gliseril glukozit de formülde. Listede parfüm yok. "
    "AHA içerdiği için kuruluk ve hassasiyet yapabilir; ilk zamanlarda gün aşırı denemek ve gündüz güneş koruyucu "
    "kullanmak gerekir.",
"nivea-spf30-glowy-lips-berry-nemlendirici-dudak-parlaticisi-ve-bakim-kremi":
    "Adında SPF30 belirtilen, berry aromalı, parlaklık veren bir dudak bakım kremi. Listenin başında hint yağı, hindistan "
    "cevizi gliseritleri, kaprilik/kaprik trigliserit, shea yağı ve oktildodekanol var; ardından avobenzon, etilheksil "
    "salisilat, bis-etilheksiloksifenol metoksifenil triazin ve etilheksil triazon gibi kimyasal filtreler geliyor. "
    "Sodyum hyalüronat ve E vitamini sonlarda. Koku 'aroma' adıyla katılmış. Poligliseril-3 diizostearat 13. sırada ve "
    "Fulton (1989) çalışmasında komedojenlik puanı 4 almış; hint yağı ve shea yağı nedeniyle fungal akneye yatkın "
    "ciltlerde dikkatli denenmeli. " + SUN,

"rimu-health-mild-glow-hassas-ciltler-icin-yenileyici-pha-yuz-tonigi":
    "Ürün adına göre hassas ciltler için hazırlanmış, PHA içeren bir yüz toniği. Su ve pentilen glikolün ardından "
    "centella özü, izopentildiol ve pantenol geliyor; PHA grubundan glukonolakton dokuzuncu, seramid NP onuncu sırada, "
    "ardından birkaç hyalüronat türü var. Listenin sonunda parfüm bulunuyor; kokuya hassas olanlar bunu göz önünde "
    "bulundurmalı. Stearik asit nedeniyle fungal akneye yatkın ciltlerde dikkatli denenmeli.",
"rimu-health-brightening-leke-karsiti-bariyer-onarici-aydinlatici-krem":
    "Adına göre leke görünümüne ve bariyere yönelik, aydınlatıcı bir yüz kremi. Su, sodyum poliakrilat, trideset-6 ve "
    "hidrojene polidesenin ardından gliserin ve pantenol geliyor; niasinamid onuncu sırada, onu hyalüronik asit, "
    "allantoin ve kafein izliyor. Avokado, biberiye, adaçayı ve kuşburnu gibi bitki özleri sonlarda. Listenin sonunda "
    "parfüm var; alkol yok. Kokuya hassas olanlar bunu göz önünde bulundurmalı.",
"rimu-health-canlandirici-ve-cilt-tonu-esitleyici-yuz-peeling-serum-aha-10-bha-2":
    "Yüz peeling serumu; ürün adına göre %10 AHA ve %2 BHA içeriyor. Su ve glikolik asitin ardından etoksidiglikol ve "
    "salisilik asit geliyor; laktik, malik ve tartarik asit ile askorbik asit de listede. Hyalüronik asit, aloe vera ve "
    "bisabolol ortalarda. Listede parfüm ve alkol yok. Çok sayıda asit içerdiği için kuruluk ve tahriş yapabilir; haftada "
    "birkaç akşamla başlamak, gündüz güneş koruyucu kullanmak ve retinol gibi başka aktiflerle aynı akşam kullanmamak "
    "gerekir. Polisorbat 20 nedeniyle fungal akneye yatkın ciltlerde dikkatli denenmeli.",
"rimu-health-tum-cilt-tipleri-icin-parfumsuz-yogun-nemlendirici-serum-hyaluronic-acid-2-b5":
    "Ürün adına göre tüm cilt tipleri için, %2 hyalüronik asit ve B5 içeren yoğun nemlendirici bir serum. Su, "
    "hyalüronik asit ve pantenolün ardından propilen glikol, gliserin, sodyum PCA ve hidrolize kolajen geliyor; "
    "allantoin, papatya, yeşil çay ve aynısefa özleri de formülde. Listede parfüm ve alkol yok. Polisorbat 20 nedeniyle "
    "fungal akneye yatkın ciltlerde dikkatli denenmeli. Marka temiz ve kuru cilde, gündüz ya da gece sürülmesini öneriyor.",
"rimu-health-cilt-tonu-esitleyici-ve-yogun-nemlendirici-yuz-kremi-hyaluronic-acid-niacinami":
    "Ürün adına göre cilt tonunu eşitlemeyi hedefleyen, hyalüronik asit ve niasinamid içeren yoğun nemlendirici bir yüz "
    "kremi. Su, sodyum poliakrilat, trideset-6 ve hidrojene polidesenin ardından gliserin ve pantenol geliyor; niasinamid "
    "onuncu, hyalüronik asit on birinci sırada, onları allantoin ve kafein izliyor. Avokado, biberiye, adaçayı ve "
    "kuşburnu gibi bitki özleri sonlarda. Listede parfüm ve alkol yok. Marka temizlenmiş cilde sabah ve akşam "
    "uygulanmasını öneriyor.",
"rimu-health-sebum-control-akne-karsiti-arindirici-yuz-tonigi":
    "Ürün adına göre yağlı ve akneye yatkın ciltlere yönelik, sebum dengeleyici bir yüz toniği. Su, pentilen glikol ve "
    "etoksidiglikolün ardından salisilik asit, glikolik asit ve laktik asit geliyor; niasinamid, çinko PCA, centella özü "
    "ve pantenol onları izliyor. Çay ağacı yağı 20. sırada, listenin sonunda ise parfüm var. Asitler kuruluk ve hassasiyet "
    "yapabilir; ilk zamanlarda gün aşırı denemek ve gündüz güneş koruyucu kullanmak gerekir. Polisorbat 20 nedeniyle "
    "fungal akneye yatkın ciltlerde dikkatli denenmeli.",
"rimu-health-pdrn-sodium-dna-li-yogun-onarici-elastikiyet-kazandirici-yuz-serumu":
    "Ürün adına göre PDRN (sodyum DNA) içeren, onarıcı ve elastikiyet odaklı bir yüz serumu. Su ve difenil dimetikonun "
    "ardından pentilen glikol, propandiol ve 1,2-heksandiol geliyor; niasinamid altıncı, ayçiçeği yağı sekizinci sırada. "
    "Dokuzuncu sıradaki somon yumurtası özütü hayvansal kaynaklı; sodyum DNA onuncu sırada. Hyalüronat türleri, "
    "centella özü, palmitoil tetrapeptit-7 ve sarı kantaron yağı da formülde. Listede parfüm ve alkol yok; difenil "
    "dimetikon bir silikon. Ayçiçeği yağı, kantaron yağı ve pentaeritritil tetraizostearat nedeniyle fungal akneye "
    "yatkın ciltlerde dikkatli denenmeli.",
"rimu-health-gozenek-sikilastirici-siyah-nokta-ve-akne-karsiti-serum":
    "Ürün adına göre gözenek ve siyah nokta görünümüne yönelik, niasinamid içeren bir serum. Su ve niasinamidin ardından "
    "gliserin, çinko PCA, hidroksietilselüloz ve trietanolamin geliyor; sodyum PCA, pantenol, bisabolol ve zeytin "
    "yaprağı özü ortalarda. Hyalüronik asit ve allantoinin yanında laktik asit 18. sırada. Listede parfüm ve alkol "
    "yok. Laktik asit düşük sırada olsa da kuruluk yapabilir; gündüz güneş koruyucu kullanılmalı. Polisorbat 20 "
    "nedeniyle fungal akneye yatkın ciltlerde dikkatli denenmeli.",
"rimu-health-gozenek-sikilastirici-ve-arindirici-tonik-glycolic-acid-6-aha-bha":
    "Ürün adına göre %6 glikolik asit ve AHA-BHA içeren, gözenek odaklı bir yüz toniği. Su ve glikolik asitin ardından "
    "propilen glikol, pantenol, trietanolamin ve gliserin geliyor; bakır glukonat, hyalüronik asit, aloe vera ve "
    "bisabolol ortalarda. Laktik, malik, tartarik ve salisilik asit ile askorbik asit, niasinamid ve kafein de listede. "
    "Sonlarda parfüm var. Asitler kuruluk ve tahriş yapabilir; gece pamukla sürülmesi öneriliyor, gündüz güneş koruyucu "
    "kullanılmalı. Polisorbat 20 nedeniyle fungal akneye yatkın ciltlerde dikkatli denenmeli.",
"rimu-health-goz-alti-aydinlatici-ve-kirisiklik-karsiti-bakim-serumu-caffeine-6-regu-age":
    "Ürün adına göre %6 kafein içeren, göz altı bölgesine yönelik bir bakım serumu. Su, soya proteini, hidrolize pirinç "
    "proteini ve süperoksit dismutazın ardından propilen glikol, gliserin, sodyum PCA, hyalüronik asit ve pantenol "
    "geliyor; kafein onuncu, sodyum askorbil fosfat on birinci sırada. Allantoin, inülin ve avokado meyve özütü de "
    "formülde. Listede parfüm ve alkol yok. Polisorbat 20 nedeniyle fungal akneye yatkın ciltlerde dikkatli denenmeli; "
    "soya alerjisi olanlar soya proteinine dikkat etmeli.",
}
