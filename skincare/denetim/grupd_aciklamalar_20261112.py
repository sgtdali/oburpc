"""Grup D ürün açıklamaları (2026-11-12): Cire Aseptine, Skin1004 (9 ürün), Dermal, M-Asam.
İçerik listeleri Gratis kaynaklı; marka sayfası eşleşmeleri rapor_d.md'de.
Uygulama: python -X utf8 urun_metni.py grupd_aciklamalar_20261112 --write
"""
SUN = "Koruma için yeterli miktarda sürülmeli ve iki saatte bir yenilenmeli."
SUN6 = ("Filtrelerin tamamı kimyasal: oktisalat, fenilbenzimidazol sülfonik asit, Uvinul A Plus, Tinosorb S, "
        "etilheksil triazon ve iskotrizinol.")
CIRE_SCENT = ("Listede parfüm ile dimetil fenetil asetat, gül ketonları ve trimetilsiklopentenil metilizopentenol "
              "gibi koku bileşenleri var; kokuya hassas olanlar bunu göz önünde bulundurmalı. ")
FUNGAL_SK = ("{x} nedeniyle fungal akneye yatkın ciltlerde dikkatli denenmeli.")
HYDRO_FUNGAL = ("Shea yağı, polisorbat 60 ve gliseril stearat nedeniyle fungal akneye yatkın ciltlerde dikkatli "
                "denenmeli.")
HYDRO_LIST = ("Su, gliserin, bütilen glikol ve setil etilheksanoatın ardından keçiboynuzu zamkı, İrlanda yosunu özütü "
              "ve karragenan geliyor; allantoin ve adenozin de formülde. ")

TEXT = {
# ---------------------------------------------------------------- SKIN1004
"skin1004-madagascar-centella-hyalu-cica-uyku-maskesi":
    "Gece boyunca yüzde bırakılan, nem odaklı bir uyku maskesi. Listenin başında centella yaprak suyu, su, bütilen "
    "glikol ve gliserin var; niasinamid altıncı sırada. Ardından hyalüronik asit ve türevleri, pantenol, adenozin ve "
    "seramid NP geliyor. Listede parfüm ve alkol yok. Setearil olivat ve sorbitan olivat nedeniyle fungal akneye "
    "yatkın ciltlerde dikkatli denenmeli.",
"skin1004-madagascar-centella-gozenek-bakimi-yapan-yuz-serumu":
    "Centella ve peptitler içeren, ürün adına göre gözenek bakımına yönelik bir yüz serumu. Su, bütilen glikol, "
    "propandiol ve aloe verayı centella özütü, gliserin ve karbomer izliyor. Palmitoil tetrapeptit-7, asetil "
    "oktapeptit-3 ve bakır tripeptit-1 gibi çok sayıda peptit ile sodyum hyalüronat, hyalüronik asit ve pantenol de "
    "listede. Parfüm ve alkol yok; listede komedojenlik puanı yüksek bir madde de görünmüyor.",
"skin1004-madagascar-centella-hyalu-cica-nemlendirici-yuz-kremi":
    "Centella ve hyalüronik asit türevleri içeren bir nemlendirici yüz kremi. Su ve gliserinin ardından "
    "pentaeritritil tetraizostearat, niasinamid ve kaprilik/kaprik trigliserit geliyor; setearil alkol, gliseril "
    "stearat ve stearil alkol kremsi dokuyu veriyor. Centella özütü on birinci sırada. Listede parfüm ve alkol yok. "
    "Pentaeritritil tetraizostearat, gliseril stearat ve poligliseril stearatlar nedeniyle fungal akneye yatkın "
    "ciltlerde dikkatli denenmeli.",
"skin1004-centella-tone-bright-leke-karsiti-tonik-bakim-pedi":
    "Niasinamid ve C vitamini türevleri içeren, ürün adına göre leke karşıtı bir tonik bakım pedi (60 adet). Su ve "
    "niasinamidin ardından bütilen glikol, pantenol, centella özütü ve hidroksietil üre geliyor; etil askorbik asit, "
    "askorbik asit, ferulik asit, kojik asit ve glutatyon listenin ikinci yarısında. Parfüm ve alkol yok. Askorbik "
    "asit ve kojik asit tahriş yapabileceğinden hassas ciltlerde önce küçük bir alanda denenmeli; gündüz güneş "
    "koruyucu kullanılmalı.",
"skin1004-hyalu-cica-blue-yuz-serumu":
    "Centella ve niasinamid içeren, nem odaklı bir yüz serumu. Su ve centella yaprak suyunun ardından bütilen glikol, "
    "heksandiol, niasinamid ve gliserin geliyor; hyalüronik asidin üç farklı biçimi, pantenol ve seramid NP de "
    "formülde. Listede parfüm ve alkol yok. Setearil olivat ve sorbitan olivat nedeniyle fungal akneye yatkın "
    "ciltlerde dikkatli denenmeli.",
"skin1004-madagascar-centella-hyalu-cica-yuz-mist":
    "Yüze sıkılarak kullanılan, nem odaklı bir yüz misti. Yeşil çay yaprağı suyu ve sudan sonra heksandiol, "
    "izopentildiol, Cordyceps özütü ve centella özütü geliyor; ksilitol, betain ve hyalüronik asidin üç biçimi "
    "listenin ilk yarısında. Seramid NP son sırada. Listede parfüm ve alkol yok. Poligliseril-10 oleat, miristat, "
    "poligliseril-6 dioleat ve poligliseril-4 laurat nedeniyle fungal akneye yatkın ciltlerde dikkatli denenmeli.",
"skin1004-centella-ve-10-niasinamid-icerikli-leke-karsiti-ampul-yuz-serumu":
    "Ürün adına göre %10 niasinamid içeren, leke karşıtı bir ampul yüz serumu. Su ve bütilen glikolün ardından "
    "niasinamid üçüncü sırada geliyor; askorbil glukozit, propandiol, traneksamik asit ve centella özütü ardından "
    "sıralanıyor. E vitamini asetatı, pantenol ve madekasosid listenin sonunda. Listede parfüm ve alkol yok. "
    "Yüksek oranlı aktifler tahriş yapabileceğinden önce küçük bir alanda denenmeli; gündüz güneş koruyucu "
    "kullanılmalı.",
"skin1004-centella-ve-10-azelaik-asit-icerikli-yatistirici-ampul-yuz-serumu":
    "Ürün adına göre %10 azelaik asit içeren, yatıştırıcı bir ampul yüz serumu. Su ve azelaik asidin ardından "
    "hidroksipropil siklodekstrin, pentilen glikol, propandiol, potasyum azeloil diglisinat ve azelamid MEA geliyor; "
    "pantenol onuncu, allantoin on beşinci, centella özütü on altıncı sırada. Listede parfüm ve alkol yok. Azelaik "
    "asit ilk kullanımda batma ve kızarıklık yapabileceğinden azar azar başlanmalı.",
"skin1004-centella-hyalu-cica-jelly-fit-ampul-tonik-ped":
    "Niasinamid ve centella içeren, nem odaklı bir ampul tonik ped (60 adet). Su, bütilen glikol ve niasinamidin "
    "ardından heksandiol, centella özütü, sodyum hyalüronat, allantoin, glukonolakton ve pantenol geliyor. Skualan, "
    "seramid NP ve kolesterol listenin ikinci yarısında. Listede parfüm ve alkol yok. Poligliseril-10 laurat "
    "nedeniyle fungal akneye yatkın ciltlerde dikkatli denenmeli.",
# ---------------------------------------------------------------- CIRE ASEPTINE
"cire-aseptine-soft-cilek-prebiyotikli-krem":
    "Çilek kokulu, küçük boy (30 ml) bir el ve vücut kremi. Su ve gliserinin ardından izopropil palmitat, gliseril "
    "stearat ve mineral yağ geliyor; yabani çilek meyve özü 16., inülin 18. sırada. Listede parfüm, hekzametilindanopiran "
    "ve Iso E Super gibi koku bileşenleri ile sodyum setearil sülfat var; kokuya hassas olanlar dikkat etmeli. "
    "Üçüncü sıradaki izopropil palmitat Fulton (1989) çalışmasında komedojenlik puanı 4 almış; stearik ve palmitik "
    "asitle birlikte fungal akneye yatkın ciltlerde dikkatli kullanılmalı.",
"cire-aseptine-soft-hindistan-cevizi-prebiyotikli-el-vucut-ve-yuz-kremi":
    "Hindistan cevizi kokulu, küçük boy (30 ml) bir el, vücut ve yüz kremi. Su ve gliserinin ardından izopropil "
    "palmitat, gliseril stearat ve mineral yağ geliyor; inülin 17. sırada. Listede parfüm ile acı portakal kabuğu yağı, "
    "limonen, metil salisilat ve hekzametilindanopiran gibi koku bileşenleri var; kokuya hassas olanlar dikkat etmeli. "
    "Üçüncü sıradaki izopropil palmitat Fulton (1989) çalışmasında komedojenlik puanı 4 almış; yüzde kullanılacaksa ve "
    "fungal akneye yatkın ciltlerde dikkatli denenmeli.",
"cire-aseptine-seffaf-aeresol-sprey-kremi-cocuk-hassas-50-spf":
    "Çocuk ve hassas ciltler için üretildiği belirtilen, 50 SPF şeffaf aerosol güneş koruyucu sprey (200 ml). Listenin "
    "başında denatüre alkol ve izopropil miristat var; bütan, izobütan ve propan itici gaz olarak yer alıyor. Dört "
    "kimyasal filtre kullanılıyor: Uvinul A Plus, avobenzon, oktisalat ve etilheksil triazon. Listede parfüm yok. "
    "Alkol ilk sırada olduğundan kuruluk veya tahriş yapabilir; izopropil miristat Fulton (1989) çalışmasında "
    "komedojenlik puanı 5 almış, fungal akneye yatkın ciltlerde dikkatli denenmeli. " + SUN,
"cire-aseptine-mineral-filtreli-karma-ve-yagli-ciltler-50-spf-yuz-gunes-koruyucu-krem":
    "Mineral filtreli, 50+ SPF yüz güneş koruyucu kremi (50 ml); ürün adına göre karma ve yağlı ciltler için. Su "
    "listenin başında; çinko oksit ikinci, titanyum dioksit yedinci sırada ve filtreler yalnızca bu iki mineralden "
    "oluşuyor. Ardından kaprilik/kaprik trigliserit, bütiloktil salisilat, propilen glikol ve silika geliyor. "
    "Listede parfüm ve alkol yok. Poligliseril izostearat, polirisinoleat, stearik asit ve sorbitan izostearat "
    "nedeniyle fungal akneye yatkın ciltlerde dikkatli denenmeli. " + SUN,
"cire-aseptine-50-spf-cocuk-gunes-koruyucu-krem":
    "Çocuklar için üretildiği belirtilen 50+ SPF güneş koruyucu krem (100 ml). Su ve C12-15 alkil benzoattan sonra "
    "filtreler geliyor. " + SUN6 + " Pantenol ve E vitamini asetatı da formülde; dimetikon ve polimetilsilseskioksan "
    "silikon grubundan. Listede parfüm ve alkol yok. " + SUN,
"cire-aseptine-akne-karsiti-anti-acne-50-spf-yuz-gunes-koruyucu-krem":
    "Ürün adına göre akneye yatkın ciltler için 50+ SPF yüz güneş koruyucu kremi (50 ml). Su ve C12-15 alkil "
    "benzoattan sonra filtreler geliyor. " + SUN6 + " Pantenol, E vitamini asetatı ve PEG-60 badem gliseritleri "
    "formülde; dimetikon silikon grubundan. " + CIRE_SCENT + "PEG-60 badem gliseritleri nedeniyle fungal akneye "
    "yatkın ciltlerde dikkatli denenmeli. " + SUN,
"cire-aseptine-50-spf-seffaf-gunes-koruyucu-sprey":
    "Şeffaf 50+ SPF güneş koruyucu sprey (200 ml). Listenin başında denatüre alkol ve izopropil miristat var; "
    "ardından dört kimyasal filtre geliyor: Uvinul A Plus, avobenzon, oktisalat ve etilheksil triazon. Parfüm yedinci "
    "sırada; geranil asetat, hekzametilindanopiran, mentol ve gül ketonları gibi koku bileşenleri de var, kokuya "
    "hassas olanlar dikkat etmeli. Alkol ilk sırada olduğundan kuruluk yapabilir; izopropil miristat Fulton (1989) "
    "çalışmasında komedojenlik puanı 5 almış, fungal akneye yatkın ciltlerde dikkatli denenmeli. " + SUN,
"cire-aseptine-gunluk-nemlendirme-daily-moisturizing-50-spf-yuz-gunes-koruyucu-krem":
    "Ürün adına göre günlük nemlendirme sunan 50+ SPF yüz güneş koruyucu kremi (50 ml). Su ve C12-15 alkil "
    "benzoattan sonra filtreler geliyor. " + SUN6 + " Gliserin, pantenol, centella yaprak özü, niasinamid, hidrolize "
    "kolajen ve sodyum hyalüronat da listede; dimetikon silikon grubundan. " + CIRE_SCENT + SUN,
"cire-aseptine-yaslanma-karsiti-anti-age-50-spf-yuz-gunes-koruyucu-krem":
    "Ürün adına göre yaşlanma belirtilerine yönelik 50+ SPF yüz güneş koruyucu kremi (50 ml). Su ve C12-15 alkil "
    "benzoattan sonra filtreler geliyor. " + SUN6 + " Kaprilik/kaprik trigliserit, pantenol, E vitamini asetatı ve "
    "Laminaria ochroleuca (deniz yosunu) özütü de formülde; dimetikon silikon grubundan. " + CIRE_SCENT + SUN,
"cire-aseptine-leke-karsiti-anti-blemish-50-spf-yuz-gunes-koruyucu-krem":
    "Ürün adına göre leke karşıtı 50+ SPF yüz güneş koruyucu kremi (50 ml). Su ve C12-15 alkil benzoattan sonra "
    "filtreler geliyor; beşinci sırada niasinamid var. " + SUN6 + " Alfa arbutin on birinci, centella yaprak özü "
    "on yedinci sırada; dimetikon silikon grubundan. " + CIRE_SCENT + SUN,
# ---------------------------------------------------------------- DERMAL
"dermal-madecassoside-blemish-control-pad-kizariklik-karsiti-ton-esitleyici-ped":
    "Ürün adına göre kızarıklığa ve ton eşitsizliğine yönelik, 12 adetlik bir tonik ped. Su, dipropilen glikol ve "
    "gliseret-26'nın ardından niasinamid dördüncü sırada; allantoin onuncu, centella özütü yirmi altıncı, madekasosid, "
    "asiatikozit, madekasik asit ve asiatik asit listenin sonunda. Listede paçuli, lavandin, adaçayı, tatlı portakal "
    "ve okaliptus yağları gibi koku veren uçucu yağlar var; kokuya hassas olanlar dikkat etmeli. Poligliseril-10 "
    "miristat, laurat ve zeytin meyve yağı nedeniyle fungal akneye yatkın ciltlerde dikkatli denenmeli.",
"dermal-korea-seoul-face-collagen-hydrogel-eriyen-yuz-maskesi":
    "Tek kullanımlık, yüzde eriyen hidrojel yüz maskesi (34 g). " + HYDRO_LIST + "Hidrolize kolajen 32. sırada; "
    "palmitoil pentapeptit-4, palmitoil tripeptit-1, palmitoil tetrapeptit-7, bakır tripeptit-1 ve asetil heksapeptid-8 "
    "peptitleri listenin sonunda. Listede parfüm ve limon meyve özütü var; kokuya hassas olanlar dikkat etmeli. "
    + HYDRO_FUNGAL,
"dermal-korea-vitamin-hidrojel-eriyen-yuz-maskesi":
    "Tek kullanımlık, yüzde eriyen hidrojel yüz maskesi (34 g). " + HYDRO_LIST + "Sodyum hyalüronat, aloe ve beş "
    "farklı seramid listenin ikinci yarısında. Listede parfüm var; kokuya hassas olanlar dikkat etmeli. Shea yağı, polisorbat 60, gliseril "
    "stearat, kamelya tohum yağı ve jojoba yağı nedeniyle fungal akneye yatkın ciltlerde dikkatli denenmeli.",
"dermal-pdrn-yuz-temizleme-ped":
    "Ürün adına göre yüz temizleme pedi (12 adet). Su ve niasinamidin ardından dipropilen glikol, bütilen glikol, "
    "heksandiol, gliserin, gliseret-26 ve glikolipitler geliyor; adındaki PDRN listede sodyum DNA olarak dokuzuncu "
    "sırada. Hyalüronik asidin çeşitli türevleri ve allantoin de formülde. Listede parfüm, limon ve tatlı portakal "
    "kabuğu yağları ile linalil asetat, linalool, heksil sinnamal ve limonen gibi koku alerjenleri var; kokuya "
    "hassas olanlar bunu göz önünde bulundurmalı.",
"dermal-retinol-peptide-lifting-pad-elastikiyeti-artirici-tonik-yuz-temizleme-pedi":
    "Retinol ve peptit içeren, ürün adına göre elastikiyet vurgulu bir tonik ped (12 adet). Su, dipropilen glikol, "
    "gliseret-26 ve betainin ardından bakuchiol 22., retinol 27., bakır tripeptit-1 ve palmitoil pentapeptit-4 "
    "listenin son bölümünde. Listede parfüm ve heksil sinnamal var. Retinol kuruluk ve soyulmaya yol açabilir; gündüz "
    "güneş koruyucu kullanılmalı, hamilelik ve emzirmede doktora danışılmalı. Soya yağı, poligliseril-10 miristat "
    "ve laurat nedeniyle fungal akneye yatkın ciltlerde dikkatli denenmeli.",
"dermal-korea-seoul-face-hyaluronic-hydrogel-eriyen-yuz-maskesi":
    "Tek kullanımlık, yüzde eriyen hidrojel yüz maskesi (34 g). " + HYDRO_LIST + "Sodyum hyalüronat 30. sırada; "
    "aloe ve beş farklı seramid de listenin ikinci yarısında. Listede parfüm var; kokuya hassas olanlar dikkat "
    "etmeli. Shea yağı, polisorbat 60, gliseril stearat, kamelya tohum yağı ve jojoba yağı nedeniyle fungal akneye "
    "yatkın ciltlerde dikkatli denenmeli.",
# ---------------------------------------------------------------- M-ASAM
"m-asam-aqua-intense-supreme-hyaluron-yuz-kremi":
    "Hyalüronik asit içeren nemlendirici bir yüz kremi (50 ml). Su, kaprilik/kaprik trigliserit, koko kaprilat/kaprat "
    "ve gliserinin ardından setearil alkol, sodyum stearoil glutamat ve shea yağı geliyor; sodyum hyalüronat sekizinci, "
    "hyalüronik asit dokuzuncu, üre on birinci sırada. Ayçiçeği yağı, E vitamini ve dimetikon da formülde. Listenin "
    "sonlarında etanol de var. Parfüm yok. Shea yağı, ayçiçeği yağı, poligliseril-10 stearat ve pentaeritritil "
    "distearat nedeniyle fungal akneye yatkın ciltlerde dikkatli denenmeli.",
}

NAMES = {}
