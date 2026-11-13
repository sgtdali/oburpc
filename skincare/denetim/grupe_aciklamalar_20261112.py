"""Grup E ürün açıklamaları (2026-11-12): yoskine, centesol, isntree, mia-klinika, mamonde, the-ceel, janssen-cosmetics,
cosmogenesis-labs, the-purest-solutions, clara-hygienics, the-bath-factory. İçerik listeleri Gratis'ten; marka sitesiyle
karşılaştırma yapılamadı (ayrıntı rapor_e.md). NAMES: markanın yazımı Yoskine (yoskine.com), Gratis "Yoksine" demiş.
Uygulama: python -X utf8 urun_metni.py grupe_aciklamalar_20261112 --write
"""
SUN = "Koruma için yeterli miktarda sürülmeli ve iki saatte bir yenilenmeli."
NOFA = "Listede parfüm ve alkol yok."
ISOE = ("Parfüm listenin sonunda ve Iso E Super de var; kokuya hassas olanlar bunu göz önünde bulundurmalı.")
YOS_PEP = ("heksapeptit-9, tripeptit-1, hidrolize sodyum hyalüronat, aminobütirik asit ve hidrolize Candida saitoana özü "
           "formülde")

NAMES = {
    "yoskine-yoksine-zen-lift-zengin-icerikli-sikilastirici-yuz-kremi":
        "Yoskine Zen Lift Zengin İçerikli Sıkılaştırıcı Yüz Kremi",
}

TEXT = {
"janssen-cosmetics-goz-cevresi-roll-on-bakim-eliksiri":
    "Göz çevresine uygulanan, roll-on uçlu bir bakım eliksiri. Su, bütilen glikol ve gliserinin ardından pentilen glikol "
    "ve ksantan gam geliyor; kafein yedinci, sodyum hyalüronat sekizinci sırada. İpek ağacı kabuk özütü ile palmitoil "
    "tripeptit-1 ve palmitoil tetrapeptit-7 de formülde. " + NOFA,

"isntree-tw-bifida-icerikli-cilt-bariyeri-destekleyici-yuz-serumu":
    "Bifida ferment lizatı ve niasinamid içeren bir yüz serumu; ürün adına göre cilt bariyerini desteklemeyi hedefliyor. "
    "Su, bütilen glikol, dipropilen glikol ve gliserinin ardından bifida ferment lizatı beşinci, niasinamid altıncı, "
    "pantenol sekizinci, allantoin dokuzuncu sırada. Listenin devamında fermente bitki özleri, beta glukan, bakır "
    "tripeptit-1, palmitoil tripeptit-1, sodyum hyalüronat ve hidrolize kolajen var. Yıldız anason meyve özütü ve cassia "
    "tarçını kabuk özütü gibi koku verici bileşenler de listede; kokuya hassas olanlar dikkatli denemeli.",

"isntree-hyaluronik-asitli-nemlendirici-tonik-plus":
    "Hyalüronik asit türevleriyle nem desteği sunan bir yüz toniği. Su, propandiol, pentilen glikol ve 1,2-heksandiolün "
    "ardından sodyum PCA ve sodyum hyalüronat geliyor; trehaloz, pantenol ve betain de üst sıralarda. Hyalüronik asit 15. "
    "sırada, hidrolize ve çapraz bağlı hyalüronat türevleri de formülde. Centella, scutellaria kök özütü, yeşil çay, aloe "
    "ve papatya gibi bitki özleri ile beta glukan listenin devamında yer alıyor. " + NOFA,

"isntree-hyaluronik-asit-icerikli-tonik":
    "Hyalüronik asit türevlerine dayanan, sade içerikli bir nem toniği. Su, propandiol, pentilen glikol ve "
    "1,2-heksandiolün ardından sodyum hyalüronat beşinci, trehaloz altıncı, pantenol sekizinci sırada. Çapraz bağlı sodyum "
    "hyalüronat, hyalüronik asit ve hidrolize hyalüronat türevleri ile hatmi kök özü, beta glukan ve aloe vera yaprağı özü "
    "de formülde. Gliserin ise listenin ikinci yarısında. " + NOFA,

"isntree-green-tea-fresh-yuz-temizleme-kopugu":
    "Yeşil çay içeren bir yüz temizleme köpüğü. Su ve gliserinin ardından temizleme işini sodyum kokoil alaninat, disodyum "
    "kokoamfodiasetat, sodyum metil kokoil taurat ve lauril hidroksisultain gibi yüzey aktif maddeler yapıyor. Çay yaprağı "
    "tozu 13., çay yaprağı 14., yeşil çay özütü 15. sırada; hyalüronik asit türevleri listenin sonunda. " + NOFA,

"cosmogenesis-labs-ton-esitleyici-50spf-pembe-yuz-gunes-kremi":
    "Pembe tonlu, SPF 50 bir yüz güneş kremi. Filtre tarafında etilheksil metoksisinamat (oktinoksat), Tinosorb S, "
    "etilheksil triazon ve Tinosorb M kullanılıyor; pembe rengi kalamin ve CI 17200 veriyor. Niasinamid 12., pantenol 21. "
    "sırada. Oktinoksat nedeniyle resif dostu güneş kremi arayanlara uygun değil. Gliseril stearat, stearik asit ve setil "
    "palmitat nedeniyle fungal akneye yatkın ciltlerde dikkatli denenmeli. " + NOFA + " " + SUN,

"mamonde-skin-barrier-seramidli-amino-yuz-kopuk-temizleyici":
    "Seramid NP içeren, amino asit bazlı bir yüz köpük temizleyici. Su ve gliserinin ardından potasyum kokoil glisinat ve "
    "sodyum lauroil glutamat temizleme işini üstleniyor; lauril hidroksisultain, sodyum kokoil glisinat ve koko glukozit "
    "de listede. Seramid NP 20., E vitamini 22. sırada. Gliseril stearat, poligliseril-10 laurat ve glikol distearat "
    "nedeniyle fungal akneye yatkın ciltlerde dikkatli denenmeli. " + NOFA,

"mamonde-calming-shot-aydinlatici-ve-nemlendirici-azulen-tonik":
    "Papatya çiçeği özütü ve guaiazulen içeren, nem odaklı bir yüz toniği. Papatya çiçeği özütü listenin birinci sırasında, "
    "suyun bile önünde; ardından su, gliserin, bütilen glikol ve 1,2-heksandiol geliyor. Niasinamid sekizinci, guaiazulen "
    "13., E vitamini 14. sırada. Ürün adı aydınlatıcı etkiyi vurguluyor. " + NOFA,

"the-purest-solutions-goz-alti-aydinlik-gorunum-destekleyici-bakim-serumu":
    "Göz çevresine yönelik, aydınlık görünüm vaat eden bir bakım serumu. Su, fenetil alkol, pentilen glikol ve "
    "hidroksietilselülozun ardından propilen glikol, kafein ve C vitamini türevi etil askorbik asit (6. ve 7. sıra) geliyor; "
    "gliserin, sodyum PCA ve iki deniz yosunu özü de formülde. Listede 14. sırada izopropil alkol ve sonda damask gülü özü "
    "var; hassas göz çevresinde ve kokuya hassas ciltlerde dikkatli denenmeli.",

"centesol-arindirici-canlandirici-yuz-temizleme-jeli":
    "Yüz temizleme jeli. Su ve lauril glukozit, koko glukozit, disodyum laureth sülfosüksinat, sodyum C14-16 olefin sülfonat "
    "ile kokamidopropil betain gibi yüzey aktif maddeler temizliği sağlıyor; gliserin ve pantenol (7. sıra) nem tarafını "
    "destekliyor. Centella yaprak özü, yeşil çay, meyan kökü, elma, şeker kamışı ve E vitamini de formülde. Listede limon "
    "ve tatlı portakal meyve özleri var; kokuya hassas olanlar dikkatli olmalı. Gliseril oleat nedeniyle fungal akneye "
    "yatkın ciltlerde dikkatli denenmeli. Listede alkol yok.",

"centesol-onarici-yogun-nemlendirici-cica-pomad-cilt-bakim-merhemi":
    "Merhem kıvamında, yoğun nemlendirici bir cica bakım ürünü. Su, lanolin, mineral yağ ve petrolatumun ardından pantenol "
    "ve balmumu geliyor; tatlı badem yağı yedinci, skualan 14. sırada. Seramid NP, AP ve EOP, fitosfingozin, fitosteroller, "
    "centella ve bileşenleri (madekasik asit, asiatikozit, asiatik asit) ile E vitamini asetatı da formülde. Lanolin bazı "
    "kişilerde alerjiye yol açabilir. 12. sıradaki gliseril stearat SE Fulton (1989) çalışmasında komedojenlik puanı 3 almış; "
    "bu madde, tatlı badem yağı, gliseril distearat, sodyum stearat ve sodyum palmitat nedeniyle akneye ve fungal akneye "
    "yatkın ciltlerde dikkatli denenmeli. " + NOFA,

"centesol-onarici-yogun-nemlendirici-cica-cilt-bakim-kremi":
    "Yoğun nemlendirici bir cica yüz kremi. Su ve gliserinin ardından heptil undesilenat, petrolatum, setearil olivat, "
    "sorbitan olivat ve shea yağı geliyor; cadı fındığı özütü sekizinci, skualan onuncu sırada. Centella, madekasosid, "
    "kalendula, bisabolol, E vitamini asetatı ve seramid NP de formülde. Listede boswellia uçucu yağı ve benzil alkol var; "
    "kokuya hassas olanlar dikkatli olmalı. Shea, çay tohumu ve ayçiçeği yağı, gliseril stearat, stearik, palmitik ve "
    "miristik asit gibi maddeler nedeniyle akneye ve fungal akneye yatkın ciltlerde dikkatli denenmeli.",

"centesol-onarici-yogun-nemlendirici-gece-bakim-kremi":
    "Gece kullanımına yönelik, yoğun nemlendirici bir yüz kremi. Su, kaprilik/kaprik trigliserit, gliseril stearat ve "
    "pantenolün ardından gliserin, behenil alkol ve setearil alkol geliyor; palmitoil tripeptit-1 ve palmitoil "
    "tetrapeptit-7 sekizinci ve dokuzuncu, niasinamid 12. sırada. Shea ve argan yağı, skualan, centella bileşenleri ile "
    "seramid NP, AP, EOP ve fitosfingozin de formülde. Gliseril stearat, shea ve argan yağı, polisorbat 20 ve 60 ile "
    "sorbitan izostearat nedeniyle fungal akneye yatkın ciltlerde dikkatli denenmeli. " + NOFA,

"centesol-onarici-nemlendirici-canlandirici-yuz-bakim-kremi":
    "Aloe vera suyuyla başlayan, nemlendirici bir yüz kremi. Aloe vera suyunun ardından izodesil izononanoat, kaprilik/kaprik "
    "trigliserit, propandiol ve pantenol (6. sıra) geliyor; niasinamid dokuzuncu sırada. Skualan, shea ve argan yağı, "
    "üre (22.), allantoin, sodyum PCA, trehaloz, seramid NP ve sodyum hyalüronat da formülde. Onuncu sıradaki gliseril "
    "stearat SE Fulton (1989) çalışmasında komedojenlik puanı 3 almış; bu madde, gliseril distearat, shea ve argan yağı, "
    "sodyum stearat ve palmitat nedeniyle akneye ve fungal akneye yatkın ciltlerde dikkatli denenmeli. " + NOFA,

"clara-hygienics-chamomile-gleam-temizleme-yagi":
    "Makyaj ve yüz temizleme ürünü; adında \"temizleme yağı\" geçiyor. Listenin başında PEG-7 gliseril kokoat, su ve "
    "gliserin var; ardından lauril glukozit, sodyum C14-16 olefin sülfonat ve kokamidopropil betain temizleyici olarak "
    "geliyor. Niasinamid yedinci, çinko PCA sekizinci, sodyum hyalüronat ve pantenol dokuzuncu ve onuncu sırada; papatya "
    "çiçeği ve yeşil çay özütleri de formülde. " + NOFA,

"mia-klinika-72-saat-etkili-su-bazli-yogun-nemlendirici-krem":
    "Su bazlı yoğun nemlendirici bir yüz kremi; ürün adında \"72 saat etkili\" ifadesi geçiyor. Su ve gliserinin ardından "
    "kaprilik/kaprik trigliserit, bis-diglisiril poliasiladipat-2, gliseril stearat ve setearil alkol geliyor. Çeşitli "
    "hyalüronik asit türevleri, seramid NP, niasinamid, pantenol, skualan, aloe vera suyu ve bambu özütü de formülde; "
    "dimetikon ve dimetikon çapraz polimeri silikon içeriyor. Gliseril stearat nedeniyle fungal akneye yatkın ciltlerde "
    "dikkatli denenmeli. " + NOFA,

"mia-klinika-nemlendirici-ve-canlandirici-gul-yuz-maskesi":
    "7 ml'lik, nemlendirici bir gül yüz maskesi. Su, gliserin, pantenol ve niasinamidin ardından betain ve yüzyapraklı gül "
    "çiçek yağı geliyor; damask gülü kallus kültürü özütü, hyalüronik asit türevleri, allantoin, bifida ferment lizatı ve "
    "beta glukan da formülde. Listede gül çiçek yağı var; kokuya hassas olanlar dikkatli olmalı. Listede alkol yok.",

"mia-klinika-arindirici-aydinlatici-toz-enzim-peeling":
    "Toz formunda bir enzim peeling. Mısır nişastası, sodyum kokoil izetionat, selüloz asetat ve sodyum lauroil glutamatın "
    "ardından papain enzimi yedinci, azelaik asit sekizinci sırada. Digliserin, madekasosid, sodyum PCA, niasinamid, "
    "allantoin ve sodyum hyalüronat da formülde. Peeling ürünü olduğundan kuruluk ve hassasiyet yapabilir; az kullanımla "
    "başlanmalı ve gündüz güneş koruyucu sürülmeli. Sodyum palmitat nedeniyle fungal akneye yatkın ciltlerde dikkatli "
    "denenmeli. " + NOFA,

"mia-klinika-arindirici-ve-akne-karsiti-azelaik-kil-yuz-maskesi":
    "7 ml'lik kil yüz maskesi; ürün adına göre akneye yatkın ciltlere yönelik. Su, kaolin ve bentonit kilinin ardından "
    "gliserin, kaprilik/kaprik trigliserit ve lauril glukozit geliyor; niasinamid sekizinci, pantenol 13. sırada. Azelaik "
    "asit 16., mandelik asit (AHA) 17. sırada; çinko PCA, laktobiyonik asit, yeşil çay ve centella da formülde. Asitler "
    "kuruluk ve hassasiyet yapabilir; gündüz güneş koruyucu kullanılmalı. " + NOFA,

"the-bath-factory-vucut-losyonu-sweet-vanilla":
    "Vanilya kokulu bir vücut losyonu. Su, mineral yağ ve seteret-20'nin ardından etilheksil palmitat dördüncü, "
    "setearil alkol beşinci, gliserin altıncı sırada; petrolatum, izopropil miristat ve dimetikon da üst sıralarda. Skualan, "
    "sodyum PCA ve sodyum hyalüronat ise daha geride. Listede parfüm ve koku alerjeni olan vanilin var; kokuya hassas olanlar "
    "bunu göz önünde bulundurmalı. Etilheksil palmitat Fulton (1989) çalışmasında komedojenlik puanı 4, sekizinci sıradaki "
    "izopropil miristat 5 almış; bu maddeler, shea yağı ve stearik asit nedeniyle sırt ve göğüs gibi akneye ve fungal "
    "akneye yatkın bölgelerde dikkatli kullanılmalı.",

"the-ceel-salmon-dna-pdrn-onarici-nemlendirici-yuz-kremi":
    "Somon DNA'sı (PDRN) içeren, onarıcı ve nemlendirici bir yüz kremi; bu nitelemeler ürün adına ait. Su, setearil alkol "
    "ve dimetikonun ardından niasinamid dördüncü sırada; etil askorbik asit sekizinci, sodyum DNA onuncu. Shea yağı, "
    "centella, pantenol, sodyum hyalüronat, seramid NP, NS, AP ve EOP ile çok sayıda peptit listenin devamında. Listede "
    "parfüm ve linalool, kumarin, geraniol, vanilin gibi sekiz koku alerjeni var; kokuya hassas olanlar bunu göz önünde "
    "bulundurmalı. Gliseril stearat, shea yağı, stearik asit, poligliseril-10 laurat ve polisorbat 20 nedeniyle fungal "
    "akneye yatkın ciltlerde dikkatli denenmeli.",

"the-ceel-pirinc-sutu-nemlendirici-aydinlatici-ve-leke-karsiti-ton-esitleyici-50-spf-yuz-gu":
    "Pirinç sütü içeren, SPF 50+ ton eşitleyici bir yüz güneş kremi. Filtre tarafında oktinoksat, avobenzon ve "
    "oktokrilen gibi kimyasal filtrelerin yanında mineral filtre titanyum dioksit var. C vitamini (10.), niasinamid (11.), "
    "alfa arbutin (15.) ve pantenol de formülde; dimetikon ve trietoksikaprililsilan silikon içeriyor. Listede parfüm ve "
    "vanilin, linalool, limonen, kumarin gibi çok sayıda koku alerjeni var; kokuya hassas olanlar bunu göz önünde "
    "bulundurmalı. Oktinoksat nedeniyle resif dostu güneş kremi arayanlara uygun değil. Gliseril stearat ve polisorbat 60 "
    "nedeniyle fungal akneye yatkın ciltlerde dikkatli denenmeli. " + SUN,

"yoskine-yoksine-zen-lift-zengin-icerikli-sikilastirici-yuz-kremi":
    "Zen Lift serisinin zengin içerikli yüz kremi; ürün adına göre sıkılaştırıcı. Su, kaprilik/kaprik trigliserit, shea "
    "yağı, gliserin ve setil alkolün ardından izostearil izostearat altıncı sırada. Seramid NG, heksapeptit-9, tripeptit-1, "
    "palmitoil heksapeptid-12, hidrolize sodyum hyalüronat ve aminobütirik asit de formülde; dimetikon ve laktik asit "
    "geride. " + ISOE + " İzostearil izostearat Fulton (1989) çalışmasında komedojenlik puanı 4 almış; bu madde, shea "
    "yağı ve izostearil hidroksistearat nedeniyle akneye ve fungal akneye yatkın ciltlerde dikkatli denenmeli.",

"yoskine-zen-lift-blur-esans":
    "Zen Lift serisinden, pürüzsüz görünüm hedefleyen bir yüz esansı. Su, gliserin ve dimetikonun ardından sodyum akrilat "
    "kopolimeri, kırmızı alg özü, pullulan ve aminobütirik asit geliyor; niasinamid 14. sırada. Tripeptit-1, heksapeptit-9 "
    "ve hidrolize sodyum hyalüronat ile E vitamini de formülde; dimetikon ve polisilikon-11 silikon içeriyor. " + ISOE + " "
    "İzostearil hidroksistearat ve sorbitan seskioleat nedeniyle fungal akneye yatkın ciltlerde dikkatli denenmeli.",

"yoskine-zen-lift-hafif-dokulu-yaslanma-karsiti-yuz-kremi":
    "Zen Lift serisinin hafif dokulu yüz kremi; ürün adına göre yaşlanma karşıtı. Su, gliserin ve gliseril stearatın "
    "ardından izostearil izostearat dördüncü, shea yağı altıncı sırada. Tripeptit-1, heksapeptit-9, hidrolize sodyum "
    "hyalüronat, aminobütirik asit ve mersin yaprak özü de formülde. " + ISOE + " İzostearil izostearat Fulton (1989) "
    "çalışmasında komedojenlik puanı 4 almış; bu madde, gliseril stearat, shea yağı ve izostearil hidroksistearat "
    "nedeniyle akneye ve fungal akneye yatkın ciltlerde dikkatli denenmeli.",

"yoskine-zen-lift-yaslanma-karsiti-yuz-serumu":
    "Zen Lift serisinin yüz serumu; ürün adına göre yaşlanma karşıtı. Su, gliserin ve dimetikonun ardından dikaprilil eter "
    "ve tripelargonin geliyor; glutatyon dokuzuncu, heksapeptit-9 on birinci sırada. C vitamini türevi askorbil "
    "tetraizopalmitat 15., E vitamini 19. sırada; tripeptit-1 ve hidrolize sodyum hyalüronat da formülde. " + ISOE + " "
    "İzostearil hidroksistearat, askorbil tetraizopalmitat, sorbitan izostearat ve polisorbat 60 nedeniyle fungal akneye "
    "yatkın ciltlerde dikkatli denenmeli.",

"yoskine-zen-lift-goz-ve-agiz-cevresi-puruzsuzlestirici-krem":
    "Göz ve ağız çevresine yönelik, pürüzsüzleştirici bir krem. Su, tripelargonin, gliserin ve pentaeritritil "
    "tetraetilheksanoatın ardından gliseril stearat, dimetikon ve kafein geliyor; heksapeptit-9, tripeptit-1 ve hidrolize "
    "sodyum hyalüronat, yeşil çay özütü ve aminobütirik asit de formülde. Soya yağı 19. sırada ve Fulton (1989) "
    "çalışmasında komedojenlik puanı 3 almış; bu yağ, gliseril stearat, askorbil palmitat ve sorbitan izostearat "
    "nedeniyle fungal akneye yatkın ciltlerde dikkatli denenmeli. Listede parfüm ve alkol yok.",
}
