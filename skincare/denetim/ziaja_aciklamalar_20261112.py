"""Ziaja ürün açıklamaları (2026-11-12). İçerik listeleri markanın uluslararası sitesinden (en.ziaja.com; ziaja.com.tr
oraya yönleniyor), Gratis listeleriyle aynı. Ad içindeki "(Hassas Ciltler)" gibi hedef kitle ifadeleri ürün adına atfedilir.
Uygulama: python -X utf8 urun_metni.py ziaja_aciklamalar_20261112 --write
"""
P = "ziaja-"
SUN = "Koruma için yeterli miktarda sürülmeli ve iki saatte bir yenilenmeli."
BODY_FUNGAL = ("Shea yağı, gliseril stearat ve polisorbat 80 nedeniyle sırt ve göğüs gibi fungal akneye yatkın bölgelerde "
               "dikkatli kullanılmalı.")
CLAY_FUNGAL = ("Kanola yağı ve hidrojene hindistan cevizi gliseritleri nedeniyle akneye ve fungal akneye yatkın ciltlerde "
               "dikkatli denenmeli.")
CLAY_BASE = ("Su, kanola yağı ve setearil etilheksanoatın ardından {kil} geliyor; oktildodekanol ve emülgatörler "
             "kremsi dokuyu oluşturuyor.")
FERMENT = "çinko, bakır, magnezyum, demir ve silisyum içeren maya fermentleri"

TEXT = {
P + "sari-erik-aromali-vucut-kremi":
    "Sarı erik kokulu bir vücut kremi. Su, C12-15 alkil benzoat ve gliserinin ardından emülgatörler ve dimetikon "
    "geliyor; shea yağı ve pantenol listenin ortasında. Listede parfümün yanında AB'de koku alerjeni olarak bildirilen "
    "vanilin, linalool ve sinnamal da var; kokuya hassas olanlar bunu göz önünde bulundurmalı. " + BODY_FUNGAL,
P + "karpuz-aromali-vucut-kremi":
    "Karpuz kokulu bir vücut kremi. Su, C12-15 alkil benzoat ve gliserinin ardından emülgatörler, dimetikon, shea yağı, "
    "propilen glikol ve salatalık özütü geliyor. Listede parfüm var; kokuya hassas olanlar bunu göz önünde "
    "bulundurmalı. " + BODY_FUNGAL,
P + "satin-glow-isilti-veren-el-bakim-iksiri":
    "Işıltı veren pigmentler içeren bir el kremi. Oktildodekanol, setil alkol ve emülgatörlerin ardından gliserin, "
    "yüzyapraklı gül özü ve balmumu geliyor; ışıltıyı sentetik florflogopit, titanyum dioksit ve kalay oksitten oluşan "
    "sedefli pigmentler veriyor. Listede parfüm ile limon ve acı portakal kabuğu yağları ve çok sayıda koku alerjeni var; "
    "kokuya hassas olanlar bunu göz önünde bulundurmalı.",
P + "satin-glow-isilti-veren-vucut-kopugu":
    "Işıltı veren pigmentler içeren, köpük kıvamında bir vücut nemlendiricisi. Su, izopropil palmitat, etilheksil stearat "
    "ve gliserinin ardından emülgatörler ve dimetikon geliyor; E vitamini asetatı, gül özü ve sodyum hyalüronat da "
    "formülde, ışıltıyı sentetik florflogopit, titanyum dioksit ve kalay oksit veriyor. Listede parfüm ve çok sayıda koku "
    "alerjeni var. İkinci sıradaki izopropil palmitat Fulton (1989) çalışmasında komedojenlik puanı 4 almış; sırt ve "
    "göğüs gibi akneye yatkın bölgelerde dikkatli kullanılmalı.",
P + "satin-glow-nemlendirici-spf30-gunduz-kremi":
    "Işıltı veren, SPF 30 bir gündüz kremi. Filtre tarafında etilheksil salisilat, etilheksil triazon, Uvinul A Plus ve "
    "Tinosorb S kullanılıyor. Shea ve kakao yağı, E vitamini asetatı, pantenol, gül ve centella özleri ile sodyum "
    "hyalüronat da formülde; ışıltıyı mika ve titanyum dioksit veriyor. Listede parfüm ve çok sayıda koku alerjeni var. "
    "Kakao yağı Fulton (1989) çalışmasında komedojenlik puanı 4 almış; akneye ve fungal akneye yatkın ciltlerde dikkatli "
    "denenmeli. " + SUN,
P + "satin-glow-nemlendirici-ve-isilti-veren-tonik-sprey":
    "Yüze sıkılarak kullanılan, nem odaklı bir tonik sprey. Su, propilen glikol ve gliserinin ardından yüzyapraklı gül ve "
    "centella özleri ile hafif bir polihidroksi asit olan laktobiyonik asit geliyor. Adındaki ışıltı vurgusuna karşın "
    "listede pigment yok. Listede parfüm ve vanilin, linalool, limon kabuğu yağı gibi koku alerjenleri var; kokuya hassas "
    "olanlar bunu göz önünde bulundurmalı.",
P + "ucuuba-yagi-nemlendirici-el-kremi-5-ure":
    "Marka üre oranını %5 olarak veriyor; üre listenin ikinci sırasında. Etilheksil stearat ve emülgatörlerin yanında "
    "ucuuba (Virola surinamensis) tohum yağı, E vitamini ve balmumu var; az miktarda dimetikon da formülde. Listede "
    "parfüm ve kumarin, öjenol gibi koku alerjenleri bulunuyor; kokuya hassas olanlar bunu göz önünde bulundurmalı.",
P + "tucuma-yagi-puruzsuzlestirici-el-kremi-3-ure":
    "Marka üre oranını %3 olarak veriyor. Etilheksil stearat ve emülgatörlerin ardından üre ve gliserin geliyor; koenzim "
    "Q10, tukuma (Astrocaryum vulgare) çekirdek yağı, E vitamini ve balmumu da formülde, az miktarda dimetikon var. "
    "Listede parfüm ve linalool, geraniol, heksil sinnamal gibi koku alerjenleri bulunuyor.",
P + "c-vitamini-b3-niacinamide-yuz-tonigi":
    "C vitamini türevi sodyum askorbil fosfat ve niasinamid içeren bir yüz toniği. Propilen glikol ve yumuşak bir "
    "temizleyici olan sodyum kokoamfoasetatın ardından hidrolize pirinç proteini, niasinamid, kalsiyum pantotenat (B5), "
    "sodyum askorbil fosfat, E vitamini asetatı ve B6 vitamini geliyor. Japon kamelyası tohum yağı listenin ortasında. "
    "Listede parfüm ve linalool, geraniol gibi koku alerjenleri var.",
P + "c-vitamini-b3-niacinamide-yuz-temizleme-jeli":
    "C vitamini türevi ve niasinamid içeren bir yüz temizleme jeli. Temizleme gücünü kokamidopropil betain, sodyum "
    "lauroil sarkozinat ve koko glukozit gibi yumuşak yüzey aktif maddelerden alıyor; listede sülfat yok. Gliserin, "
    "hidrolize pirinç proteini, niasinamid, B5 ve B6 vitaminleri, sodyum askorbil fosfat ve E vitamini asetatı da "
    "formülde. Listede parfüm ve linalool, geraniol gibi koku alerjenleri var. Durulanan bir üründe vitaminler ciltte kısa "
    "süre kalır.",
P + "c-vitaminli-antioksidan-50-spf-yuz-gunes-kremi":
    "E vitamini ve C vitamini türevi askorbil palmitat içeren, SPF 50+ bir yüz güneş kremi. Filtre tarafında Uvinul A "
    "Plus, etilheksil salisilat, etilheksil triazon, Tinosorb S ve Tinosorb M kullanılıyor; mineral filtre yok. Askorbil "
    "palmitat listenin 21. sırasında; pantenol, lesitin ve gliserin de formülde. Listede parfüm ile acı portakal kabuğu ve "
    "sardunya yağı gibi koku alerjenleri var; kokuya hassas ciltler bunu göz önünde bulundurmalı. " + SUN,
P + "sari-kil-iceren-anti-stres-yuz-maskesi-tum-ciltler":
    "Kil içeren, krem kıvamında bir yüz maskesi. " + CLAY_BASE.format(kil="kil olarak illit") + " Pantenol, gliserin, "
    "lesitin, E vitamini asetatı ve askorbil palmitat da formülde. Listede parfüm ve az miktarda dimetikon var. "
    + CLAY_FUNGAL,
P + "kahverengi-kil-iceren-yenileyici-yuz-maskesi-tum-cilt-tipleri":
    "Kil içeren, krem kıvamında bir yüz maskesi. " + CLAY_BASE.format(kil="kil olarak illit") + " Tatlı badem özü, "
    "pantenol ve E vitamini asetatı da formülde. Listede parfüm ve az miktarda dimetikon var. " + CLAY_FUNGAL,
P + "yesil-kil-iceren-nemlendirici-yuz-maskesi-kuru-normal-ciltler":
    "Kil içeren, krem kıvamında bir yüz maskesi; ürün adına göre kuru ve normal ciltler için. "
    + CLAY_BASE.format(kil="kil olarak illit") + " Gliserin, tara zamkı ve pantenol de formülde; rengi CI 42090 veriyor. "
    "Listede parfüm ve az miktarda dimetikon var. " + CLAY_FUNGAL,
P + "pembe-kil-iceren-yatistirici-yuz-maskesi-hassas-ciltler":
    "Kil içeren, krem kıvamında bir yüz maskesi; ürün adına göre hassas ciltler için. "
    + CLAY_BASE.format(kil="kil olarak kaolin") + " Pantenol ve allantoin de formülde. Listede parfüm ve heksil "
    "sinnamal, linalool gibi koku alerjenleri var; hassas ciltler bunu göz önünde bulundurmalı. " + CLAY_FUNGAL,
P + "ferahlatici-dengeleyici-yatistirici-yuz-maskesi-hassas-ciltler":
    "Ürün adına göre hassas ciltler için hazırlanmış, besleyici bir yüz maskesi. Kanola yağı, gliserin, heksil laurat ve "
    "palmiye yağının ardından deniz suyu, shea yağı ve zeytin yağı geliyor; inülin, fruktoz, " + FERMENT + " ve "
    "sodyum hyalüronat da formülde. Listede parfüm var; hassas ciltler bunu göz önünde bulundurmalı. Yoğun bitkisel yağ "
    "içeriği nedeniyle akneye ve fungal akneye yatkın ciltlere uygun değil.",
P + "ferahlatici-dengeleyici-yagsiz-yuz-maskesi-yagli-ciltler":
    "Ürün adına göre yağlı ciltler için hazırlanmış, yağ içermeyen bir yüz maskesi. Su ve gliserinin ardından çinko "
    "içeren maya fermenti ve deniz suyu geliyor; inülin, fruktoz, bakır, magnezyum, demir ve silisyum içeren maya "
    "fermentleri ve sodyum hyalüronat da formülde. Listede parfüm var; yağ ve silikon yok.",
P + "ferahlatici-dengeleyici-nemlendirici-yuz-maskesi-kuru-ciltler":
    "Ürün adına göre kuru ciltler için hazırlanmış, zengin dokulu bir yüz maskesi. Oktildodekanol, kaprilik/kaprik "
    "trigliserit ve palmiye yağının ardından gliserin, deniz suyu, shea ve kanola yağları geliyor; pantenol, inülin, "
    "fruktoz ve " + FERMENT + " de formülde. Listede parfüm ve az miktarda dimetikon var. Koruyucu olarak metil ve etil "
    "parabenin yanında formaldehit salan bir koruyucu olan diazolidinil üre kullanılıyor; formaldehite hassasiyeti "
    "olanlar için not edilmeli. Yoğun yağ içeriği nedeniyle akneye ve fungal akneye yatkın ciltlere uygun değil.",
P + "karahindiba-bali-iceren-yatistirici-yuz-maskesi-normal-ciltler":
    "Ürün adına göre normal ciltler için, bal içeren bir yüz maskesi. Su, sükroz, ksilitol ve gliserin listenin başında; "
    "setearil alkol, shea yağı, balmumu, lanolin, bal özü ve karahindiba kökü özütü de formülde. Listede parfüm ve renk "
    "maddeleri var. Lanolin, yün yağına hassasiyeti olanlar için not edilmeli.",
P + "manuka-bali-iceren-akne-karsiti-yuz-maskesi-yagli-karma-ciltler":
    "Ürün adına göre yağlı ve karma ciltler için, bal içeren bir yüz maskesi. Gliserin listenin başında; ardından su, "
    "sükroz, ksilitol, çinko içeren maya fermenti, bal özü, niasinamid, B5 ve B6 vitaminleri, sodyum askorbil fosfat ve "
    "manuka yaprak özütü geliyor. Listede parfüm ve renk maddeleri var; yağ ve silikon yok.",
}
