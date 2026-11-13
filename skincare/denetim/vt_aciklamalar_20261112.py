"""VT Cosmetics ürün açıklamaları ve ad düzeltmeleri (2026-11-12). İçerik listeleri Gratis'ten (markanın Türkiye sitesi
yok; resmî Kore sitesi vt-cosmetics.com listeyi Korece veriyor, karşılaştırılmadı). Reedle Shot 50/100/300/700 kullanım
sıklığı markanın global sayfasından (globalvt-cosmetics.com). Gratis bu serideki esansları "Yüz Kremi" diye adlandırmış;
NAMES adları düzeltir (slug'lar değişmedi). Uygulama: python -X utf8 urun_metni.py vt_aciklamalar_20261112 --write
"""
P = "vt-cosmetics-"
STING = "Silika bazlı bu yapılar nedeniyle uygulamada ciltte hafif batma ya da karıncalanma hissi olabilir; tahriş olmuş ya da yaralı ciltte kullanılmamalı."
REEDLE = ("Reedle Shot serisinde marka, cilde sürülürken batma hissi veren silika bazlı mikro yapılar (\"reedle\") kullanıyor. "
          + STING)
EHP8 = ("Sekizinci sıradaki etilheksil palmitat Fulton (1989) çalışmasında yüksek komedojenlik puanı (4) almış; bu madde, "
        "makademya yağı ve sorbitan oleat nedeniyle akneye ve fungal akneye yatkın ciltlerde dikkatli denenmeli.")
BASE = ("Su, dipropilen glikol, gliserin ve niasinamidin ardından makademya yağı ve etilheksil palmitat geliyor; centella "
        "özütü ve bileşenleri (madekasosid, asiatikozit), propolis ve sodyum hyalüronat da formülde.")
RETINOL = ("Retinoidler ilk haftalarda kuruluk, soyulma ve hassasiyet yapabilir: haftada birkaç akşamla başlamak ve gündüz "
           "güneş koruyucu kullanmak gerekir. Hamilelik ve emzirme döneminde kullanmadan önce doktora danışılmalı.")
HYDROP = ("Nem odaklı bir esans: gliserin, dipropilen glikol ve bütilen glikolün ardından niasinamid, gliseret-26, betain, "
          "pantenol, hidroksietil üre, trehaloz ve allantoin geliyor; ektoin, sodyum hyalüronat ve dekapeptid-40 de formülde.")
LIP = ("Yağ bazlı, parlak bitişli bir dudak bakım ürünü. Hidrojene poliizobuten ve yağ esterlerinin ardından dudakta serinlik "
       "veren mentil laktat ve ısınma hissi veren vanilil butil eter geliyor; dolgun görünüm hissini bu ikili yaratıyor. Jojoba "
       "yağı, E vitamini asetatı, centella bileşenleri, sodyum hyalüronat ve propolis de formülde. Listede parfüm var; "
       "dudakta hassasiyet ya da çatlak varsa batma hissi artabilir.")

TEXT = {
P + "reedle-shot-50-yuz-kremi":
    "Reedle Shot serisinin en hafif versiyonu; marka günlük kullanıma uygun olduğunu belirtiyor. " + REEDLE + " " + BASE
    + " Listede parfüm ve alkol yok. " + EHP8,
P + "reedle-shot-100-yuz-kremi":
    "Reedle Shot serisinin temel versiyonu; marka günlük kullanıma uygun olduğunu belirtiyor. " + REEDLE + " " + BASE
    + " Listede ayrıca bir amino asit karışımı bulunuyor. Listede parfüm ve alkol yok. " + EHP8,
P + "reedle-shot-300-yuz-kremi":
    "Reedle Shot 100'den daha yoğun bir versiyon; marka üç günde bir kullanılmasını öneriyor. " + REEDLE + " " + BASE
    + " Listede parfüm ve alkol yok. " + EHP8,
P + "reedle-shot-700-yuz-kremi":
    "Reedle Shot serisinin en yoğun versiyonu; marka haftada bir, yoğun bakım olarak kullanılmasını öneriyor. Diğer "
    "versiyonlardan daha kremsi bir yapısı var: gliserin, propandiol ve yağ esterlerinin ardından makademya ve shea yağı, "
    "niasinamid ve silika geliyor; seramid NP, hidrolize elastin, centella bileşenleri ve sodyum hyalüronat da formülde. "
    + STING + " Listede parfüm ve alkol yok. Shea ve makademya yağı, stearik asit ve palmitik asit nedeniyle fungal akneye "
    "yatkın ciltlerde dikkatli denenmeli.",
P + "pro-cica-reedle-shot-100-yuz-kremi":
    "Reedle Shot 100'ün centella ağırlıklı \"Pro Cica\" versiyonu. " + REEDLE + " Niasinamidin ardından makademya yağı ve "
    "etilheksil palmitat geliyor; centella özütü ve bileşenleri, jojoba yağı, seramid NP, sodyum hyalüronat, beta glukan ve "
    "allantoin de formülde. Listede parfüm ve alkol yok. " + EHP8,
P + "kolajen-icerikli-reedle-shot-100-yuz-kremi":
    "Reedle Shot 100'ün kolajen içeren versiyonu. " + REEDLE + " " + BASE + " Listede kolajen özütü, kolajen suyu ve süt "
    "proteini de var. Listede parfüm ve alkol yok. " + EHP8,
P + "kolajen-reedle-shot-300-yuz-kremi":
    "Kolajen içeren, Reedle Shot serisinden daha yoğun bir esans. " + REEDLE + " " + BASE + " Kolajen suyu, kolajen "
    "özütü ve süt proteini listenin ikinci yarısında. Listede parfüm ve alkol yok. " + EHP8,
P + "kolajen-reedle-shot-700-yuz-kremi":
    "Kolajen içeren, Reedle Shot serisinin yoğun versiyonlarından biri. " + REEDLE + " " + BASE + " Pantenol, seramid NP, "
    "süt proteini ve kolajen özütü de formülde. Listede parfüm ve alkol yok. " + EHP8,
P + "reti-a-reedle-shot-100-yuz-kremi":
    "Retinoid içeren bir Reedle Shot esansı. " + REEDLE + " Listenin ortasında retinol (18. sıra) ve hidroksipinakolon "
    "retinoat (20. sıra) var; bakuchiol, centella özütü, allantoin ve sodyum hyalüronat da formülde. " + RETINOL
    + " Dokuzuncu sıradaki etilheksil palmitat Fulton (1989) çalışmasında yüksek komedojenlik puanı (4) almış; bu madde, "
    "makademya yağı ve gliseril stearat gibi esterler nedeniyle akneye ve fungal akneye yatkın ciltlerde dikkatli denenmeli.",
P + "salyangoz-icerikli-reedle-shot-100b-yuz-kremi":
    "Salyangoz salgısı süzüntüsü içeren bir Reedle Shot esansı; salyangoz salgısı listenin ikinci sırasında. " + REEDLE
    + " Gliserin, bütilen glikol ve niasinamidin yanında centella bileşenleri, propolis, bir amino asit karışımı ve sodyum "
    "hyalüronat var. Listede parfüm, alkol, yağ ve silikon yok.",
P + "black-truffle-reedle-shot-100-yuz-kremi":
    "Siyah trüf özütü içeren bir Reedle Shot esansı; trüf özütü listenin altıncı sırasında. " + REEDLE + " Niasinamid, "
    "pantenol, seramid NP, kolajen, Pro-Xylane (hidroksipropil tetrahidropirantriol) ve B12 vitamini de formülde; renk için "
    "altın (CI 77480) kullanılmış. Listede parfüm ve alkol yok; az miktarda silikon (dimetikonol) var.",
P + "red-booster-reedle-shot-100-yuz-kremi":
    "Red Booster adını taşıyan bir Reedle Shot esansı. " + REEDLE + " Gliserin, dipropilen glikol ve niasinamidin ardından "
    "eklipta ve kakao özütleri geliyor; pantenol, arbutin, centella bileşenleri, kan ağacı (Croton lechleri) reçinesi, "
    "seramid NP ve sodyum hyalüronat da formülde. Listede parfüm yok. Moringa yağı nedeniyle fungal akneye yatkın ciltlerde "
    "dikkatli denenmeli.",
P + "vita-light-reedle-shot-100-yuz-kremi":
    "C vitamini ve antioksidanlar içeren bir Reedle Shot esansı. " + REEDLE + " Niasinamid listenin dördüncü sırasında; "
    "askorbik asit (C vitamini) 15. sırada. Koenzim Q10, astaksantin, yalancı iğde yağı, glutatyon, ferulik asit ve az "
    "miktarda retinil palmitat da formülde. Listede parfüm ve alkol yok.",
P + "pdrn-reedle-shot-100-yuz-kremi":
    "PDRN adını taşıyan, krem kıvamına yakın bir Reedle Shot esansı. Ürün adındaki PDRN, listede sodyum DNA olarak listenin "
    "sonlarında (52. sıra) yer alıyor. " + REEDLE + " Yağ esterleri ve niasinamidin yanında asetil heksapeptid-8, bakır "
    "tripeptit-1, palmitoil pentapeptit-4, birçok farklı hyalüronik asit türü, yalancı iğde yağı ve shea yağı var. Listede "
    "parfüm ve alkol yok. Poligliseril esterleri ve bitkisel yağlar nedeniyle fungal akneye yatkın ciltlerde dikkatli "
    "denenmeli.",
P + "hydrop-reedle-shot-100hl-yuz-kremi":
    "Reedle Shot serisinin nem odaklı Hydrop versiyonu. " + HYDROP + " Neem, zerdeçal ve kutsal reyhan özütleri listenin "
    "sonlarında. " + STING + " Listede parfüm, alkol ve yağ yok; az miktarda silikon (fenil trimetikon) var.",
P + "hydrop-reedle-shot-300hl-yuz-kremi":
    "Reedle Shot serisinin nem odaklı Hydrop versiyonu (300hL). " + HYDROP + " Neem, zerdeçal ve kutsal reyhan özütleri "
    "listenin sonlarında. " + STING + " Listede parfüm, alkol ve yağ yok; az miktarda silikon (fenil trimetikon) var.",
P + "hydrop-reedle-shot-700hl-yuz-kremi":
    "Reedle Shot serisinin nem odaklı Hydrop versiyonu (700hL). " + HYDROP + " Neem yaprak özütü bu versiyonda listenin "
    "daha üst sıralarında (21. sıra). " + STING + " Listede parfüm, alkol ve yağ yok; az miktarda silikon (fenil "
    "trimetikon) var.",
P + "reedle-shot-baslangic-asamasi-lip-plumper-dudak-parlatici-bakim-kremi":
    LIP + " Diğer Lip Plumper ile içerik listesi neredeyse aynı; marka bunu başlangıç seviyesi olarak sunuyor.",
P + "reedle-shot-lip-plumper-dudak-parlatici-bakim-kremi":
    LIP,
P + "reedle-shot-lifting-yuz-serumu":
    "Peptid ağırlıklı bir yüz serumu. Gliserin, niasinamid ve bütilen glikolün ardından heptil undesilenat, skualan ve "
    "makademya yağı geliyor; kolesterol, kolza sterolleri ve pantenol de formülde. Listenin ikinci yarısında bakır "
    "tripeptit-1, palmitoil tripeptit-1, asetil heksapeptid-8, palmitoil pentapeptit-4 gibi çok sayıda peptid, hidrolize "
    "elastin ve kolajen özütü var. Listede parfüm var; kokuya hassas olanlar bunu göz önünde bulundurmalı.",
P + "reedle-shot-lifting-yuz-kremi":
    "Peptid içeren, besleyici bir yüz kremi. Gliserinin ardından kolza sterolleri, hidrojene lesitin, setil etilheksanoat "
    "ve kolesterol geliyor; hindistan cevizi yağı, skualan, makademya yağı ve niasinamid de üst sıralarda. Listenin "
    "ikinci yarısında çok sayıda peptid, hidrolize elastin ve kolajen özütü var. Listede parfüm var. Sekizinci sıradaki "
    "hindistan cevizi yağı Fulton (1989) çalışmasında yüksek komedojenlik puanı (4) almış; akneye ve fungal akneye yatkın "
    "ciltlerde dikkatli denenmeli.",
P + "reedle-shot-lifting-goz-kremi":
    "Zengin dokulu, peptid içeren bir göz çevresi kremi. Gliserinin ardından hidrojene poliolefin, C13-15 alkan, çayır "
    "köpüğü yağı ve az miktarda silikon geliyor; niasinamid, shea yağı, hindistan cevizi yağı, bakuchiol, seramid NP, "
    "sodyum hyalüronat ve çok sayıda peptid de formülde. Listede parfüm var; göz çevresi hassas bir bölge olduğu için "
    "kokuya hassas olanlar bunu göz önünde bulundurmalı. Hindistan cevizi yağı (Fulton puanı 4) ve çok sayıda bitkisel yağ "
    "ile ester nedeniyle akneye ve fungal akneye yatkın ciltlerde dikkatli denenmeli.",
P + "reedle-shot-vita-light-yuz-kremi":
    "Vitamin karışımı içeren, jel kıvamına yakın bir yüz kremi. Niasinamid listenin ikinci sırasında; ardından gliserin, "
    "propandiol, kaprilik/kaprik trigliserit, skualan, pantenol ve bisabolol geliyor. Listenin ikinci yarısında C vitamini "
    "(askorbik asit, sodyum askorbil fosfat), B grubu vitaminler, ferulik asit, beta karoten, glutatyon ve çok düşük "
    "miktarda retinol var. Listede parfüm ve alkol yok.",
P + "reedle-shot-vita-light-goz-kremi":
    "Vitamin karışımı içeren bir göz çevresi kremi; formülü aynı serinin yüz kremine çok benziyor. Niasinamid listenin "
    "ikinci sırasında; gliserin, skualan, pantenol, bisabolol ve centella özütü de üst sıralarda. Listenin ikinci yarısında "
    "C vitamini, B grubu vitaminler, glutatyon, ferulik asit ve düşük miktarda retinol var. Listede parfüm ve alkol yok.",
P + "tx-toning-esans-1000-shot":
    "Leke ve ton eşitsizliği görünümüne yönelik, traneksamik asit içeren bir esans. Gliserinin ardından traneksamik asit "
    "ve niasinamid geliyor; allantoin, sodyum hyalüronat, dipotasyum glisirizat, seramid NP, kolesterol ve glutatyon da "
    "formülde. Listede parfüm ve alkol yok. Gündüz güneş koruyucuyla birlikte kullanılmalı.",
P + "tx-toning-esans-2000-shot":
    "Leke ve ton eşitsizliği görünümüne yönelik, traneksamik asit içeren bir esans. 1000 Shot versiyonundan farklı olarak "
    "traneksamik asit listenin ilk sırasında, sudan hemen sonra; ardından gliserin ve niasinamid geliyor. Allantoin, "
    "sodyum hyalüronat, seramid NP, kolesterol ve glutatyon da formülde. Listede parfüm ve alkol yok. Gündüz güneş "
    "koruyucuyla birlikte kullanılmalı.",
P + "tx-toning-tonik":
    "Traneksamik asit ve niasinamid içeren, ton eşitsizliği görünümüne yönelik bir tonik. Gliserin ve niasinamidin "
    "ardından traneksamik asit altıncı sırada; eritritol, trehaloz, allantoin, seramid NP, glutatyon ve centella özü de "
    "formülde. Listede papain enzimi var, ancak listenin sonlarında. Listede parfüm ve alkol yok.",
P + "tx-toning-yuz-kremi":
    "Traneksamik asit ve niasinamid içeren bir yüz kremi. Gliserin, bütilen glikol ve yağ esterlerinin ardından "
    "niasinamid dokuzuncu, traneksamik asit 17. sırada; pantenol, sodyum hyalüronat, glutatyon, seramid NP, kolesterol ve "
    "skualan da formülde. Listede parfüm ve alkol yok. Çok sayıda ester ve makademya yağı nedeniyle fungal akneye yatkın "
    "ciltlerde dikkatli denenmeli.",
P + "pdrn-100-yuz-serumu":
    "PDRN adını taşıyan, yağ ağırlıklı bir yüz serumu. Ürün adındaki PDRN, listede sodyum DNA olarak 28. sırada. Su, "
    "izopropil miristat, kaprilik/kaprik trigliserit ve gliserinin ardından niasinamid geliyor; beş farklı seramid, "
    "pantenol, skualan, allantoin ve ginseng özütü de formülde. Listede parfüm ve alkol yok. İkinci sıradaki izopropil "
    "miristat Fulton (1989) çalışmasında en yüksek komedojenlik puanını (5) almış; akneye ve fungal akneye yatkın ciltler "
    "için uygun değil.",
P + "pdrn-100-yuz-kremi":
    "PDRN adını taşıyan, zengin dokulu bir yüz kremi. Ürün adındaki PDRN, listede sodyum DNA olarak listenin sonlarında "
    "(70. sıra). Gliserin, bütilen glikol ve yağ esterlerinin ardından niasinamid geliyor; beş farklı seramid, "
    "fitosfingozin, kolesterol, pantenol ve birçok farklı hyalüronik asit türü de formülde. Listede parfüm ve alkol yok; az "
    "miktarda silikon (vinil dimetikon) var. Yağ asitleri, bitkisel yağlar ve esterler nedeniyle akneye ve fungal akneye "
    "yatkın ciltlerde dikkatli denenmeli.",
P + "pdrn-isilti-verici-yuz-serumu":
    "PDRN adını taşıyan, yağ içeren bir yüz serumu. Ürün adındaki PDRN, listede sodyum DNA olarak 25. sırada. Metil "
    "propandiolün ardından çayır köpüğü yağı ve niasinamid geliyor; skualan, beş farklı seramid, baobab yağı, sodyum "
    "hyalüronat, pantenol, allantoin ve ginseng özütü de formülde. Listede parfüm ve alkol yok. Çayır köpüğü ve baobab "
    "yağları nedeniyle fungal akneye yatkın ciltlerde dikkatli denenmeli.",
}

NAMES = {
    P + "reedle-shot-50-yuz-kremi": "Reedle Shot 50",
    P + "reedle-shot-100-yuz-kremi": "Reedle Shot 100",
    P + "reedle-shot-300-yuz-kremi": "Reedle Shot 300",
    P + "reedle-shot-700-yuz-kremi": "Reedle Shot 700",
    P + "pro-cica-reedle-shot-100-yuz-kremi": "Pro Cica Reedle Shot 100",
    P + "kolajen-icerikli-reedle-shot-100-yuz-kremi": "Kolajen İçerikli Reedle Shot 100",
    P + "kolajen-reedle-shot-300-yuz-kremi": "Kolajen Reedle Shot 300",
    P + "kolajen-reedle-shot-700-yuz-kremi": "Kolajen Reedle Shot 700",
    P + "reti-a-reedle-shot-100-yuz-kremi": "Reti-A Reedle Shot 100",
    P + "salyangoz-icerikli-reedle-shot-100b-yuz-kremi": "Salyangoz İçerikli Reedle Shot 100B",
    P + "black-truffle-reedle-shot-100-yuz-kremi": "Black Truffle Reedle Shot 100",
    P + "red-booster-reedle-shot-100-yuz-kremi": "Red Booster Reedle Shot 100",
    P + "vita-light-reedle-shot-100-yuz-kremi": "Vita-Light Reedle Shot 100",
    P + "pdrn-reedle-shot-100-yuz-kremi": "PDRN Reedle Shot 100",
    P + "hydrop-reedle-shot-100hl-yuz-kremi": "Hydrop Reedle Shot 100hL",
    P + "hydrop-reedle-shot-300hl-yuz-kremi": "Hydrop Reedle Shot 300hL",
    P + "hydrop-reedle-shot-700hl-yuz-kremi": "Hydrop Reedle Shot 700hL",
    P + "reedle-shot-baslangic-asamasi-lip-plumper-dudak-parlatici-bakim-kremi": "Reedle Shot Lip Plumper Başlangıç",
    P + "reedle-shot-lip-plumper-dudak-parlatici-bakim-kremi": "Reedle Shot Lip Plumper",
}
