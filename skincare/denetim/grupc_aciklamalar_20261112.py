"""Grup C (Olalab, Dermokil, Foreo, 5C Cure) ürün açıklamaları (2026-11-12). Gratis ürün sayfasındaki içerik listesinden
yazıldı; oranlar ve hedef kitle ürün adına atfedilir, "parfüm/alkol/silikon yok" ifadeleri içerik listesinden doğrulanır.
İç analiz dili, tıbbi iddia, marka beyanı aktarımı yok. Doğrulama: python -X utf8 urun_metni.py grupc_aciklamalar_20261112
"""
SUN = "Koruma için yeterli miktarda sürülmeli ve iki saatte bir yenilenmeli."
SPRAY = SUN
RETINOID = ("Retinoid kuruluk, soyulma ve hassasiyet yapabilir: haftada birkaç akşamla başlayıp gündüz güneş koruyucu "
            "kullanmak gerekir. Hamilelik ve emzirmede kullanmadan önce doktora danışılmalı.")
ACID_SUN = "Kuruluk ve hassasiyet yapabilir; kullandığınız günlerde gündüz güneş koruyucu sürmek iyi olur."
PARFUM_VAR = "Listede parfüm var; kokuya hassas olanlar bunu göz önünde bulundurmalı."

TEXT = {
"5c-cure-avocado-kore-yuz-maskesi":
    "Avokado meyve özü ve sodyum hyalüronat içeren, 25 ml'lik bir yüz maskesi. Su, propilen glikol ve gliserinden sonra "
    "dördüncü sırada polisorbat 80 geliyor; avokado meyve özü yedinci, sodyum hyalüronat on birinci sırada. Ak söğüt kabuğu, "
    "Laminaria digitata, Plantago asiatica, karaağaç kabuğu ve kaki yaprağı özleri de formülde. " + PARFUM_VAR +
    " Polisorbat 80 nedeniyle fungal akneye yatkın ciltlerde dikkatli denenmeli. Listede alkol, silikon ve yağ yok.",

"dermokil-50-spf-yuksek-koruyucu-cocuk-gunes-spreyi":
    "Ürün adına göre çocuklar için, adında 50+++ SPF yazan 200 ml'lik bir güneş spreyi; mineral ve kimyasal filtreleri birlikte kullanıyor. "
    "Listenin başında mineral filtre çinko oksit var; dördüncü sırada kimyasal filtre etilheksil salisilat geliyor. Bunların "
    "ardından gliserin, beşinci sırada mineral yağ (sıvı parafin), setearil alkol ve stearik asit sıralanıyor. "
    "Zeytin meyve yağı, aloe vera suyu, laktik asit ve E vitamini asetatı sonlarda yer alıyor. Formülde silikonlar "
    "(polimetilsilseskioksan, dimetikon) var. Stearik asit (9. sırada, Fulton puanı 2-3) ve zeytin meyve yağı nedeniyle "
    "fungal akneye yatkın ciltlerde dikkatli denenmeli. " + SPRAY,

"dermokil-matcha-ozlu-kil-yuz-maskesi":
    "Adında matcha geçen, kil bazlı 50 ml'lik bir yüz maskesi; salisilik asit (BHA) içeriyor. Su ve kilden sonra yeşil çay "
    "özü, dördüncü sırada ceviz çekirdeği yağı geliyor; salisilik asit altıncı, allantoin yedinci sırada. Listede parfüm, "
    "alkol ve silikon yok. Ceviz çekirdeği yağı nedeniyle fungal akneye yatkın ciltlerde dikkatli denenmeli. Salisilik asit "
    "kuruluk ve hassasiyet yapabilir; maske sonrası gündüz güneş koruyucu kullanmak iyi olur.",

"dermokil-pirinc-ozlu-beyazlatici-kil-yuz-maskesi":
    "Pirinç kepeği özü içeren, kil bazlı 50 ml'lik bir yüz maskesi. Su ve kilden sonra gliseril stearat, gliserin ve mısır "
    "nişastası geliyor; pirinç kepeği özü sekizinci, sodyum hyalüronat on birinci sırada. Kayısı çekirdeği tozu hafif "
    "aşındırıcı etki verebilir; shea yağı, E vitamini asetatı ve allantoin de formülde. Listede parfüm, alkol ve silikon "
    "yok. Gliseril stearat (3. sırada), stearik asit (9. sırada, Fulton puanı 2-3) ve shea yağı nedeniyle fungal akneye "
    "yatkın ciltlerde dikkatli denenmeli.",

"dermokil-99-purity-pdrn-sodium-dna-kolajen-gingseng-skin-barrier-kagit-jel-maske":
    "Adında %99 saflıkta PDRN (sodyum DNA) geçen, 25 gr'lık bir kağıt jel maske. Sodyum DNA listenin yirminci sırasında; "
    "daha üstte su, gliserin, propandiol, pentilen glikol ve bütilen glikol, sekizinci sırada palmitoil tripeptit-5 var. "
    "Sodyum hyalüronat, hidrolize sodyum hyalüronat, pantenol, adenozin, allantoin, ginseng kökü özü ve çeşitli peptitler de "
    "formülde. Adında kolajen geçse de içerik listesinde kolajen yok. " + PARFUM_VAR + " Alkol, yağ ve silikon yok.",

"dermokil-99-purity-pdrn-sodium-dna-madecassoside-skin-barrier-kagit-jel-maske":
    "Adında %99 saflıkta PDRN (sodyum DNA) ve madekasosid geçen, 25 gr'lık bir kağıt jel maske. Su, gliserin, propandiol, "
    "pentilen glikol ve bütilen glikolden sonra altıncı sırada madekasosid, yedincisinde Centella asiatica yaprak özü, "
    "sekizincisinde asiatikozit geliyor. Sodyum hyalüronat, palmitoil peptitler, pantenol, adenozin, allantoin ve sodyum DNA "
    "da formülde. " + PARFUM_VAR + " Alkol, yağ ve silikon yok.",

"dermokil-99-purity-pdrn-sodium-dna-cica-centella-skin-barrier-kagit-jel-maske":
    "Adında %99 saflıkta PDRN (sodyum DNA) ve centella geçen, 25 gr'lık bir kağıt jel maske. Su, gliserin ve propandiolün "
    "ardından dördüncü sırada Centella asiatica özü, beşincisinde centella özsuyu geliyor. Sodyum hyalüronat, palmitoil "
    "peptitler, pantenol, adenozin, allantoin ve sodyum DNA da formülde. " + PARFUM_VAR + " Alkol, yağ ve silikon yok.",

"dermokil-99-purity-pdrn-sodium-dna-rose-ceramide-skin-barrier-kagit-jel-maske":
    "Adında %99 saflıkta PDRN (sodyum DNA), gül ve seramid geçen, 25 gr'lık bir kağıt jel maske. Su, gliserin, propandiol, "
    "pentilen glikol ve bütilen glikolden sonra altıncı sırada damask gülü çiçek özü geliyor; sodyum hyalüronat, "
    "palmitoil peptitler, pantenol, adenozin ve allantoin de formülde. Seramid NP otuzuncu sırada, yani listenin sonlarında. "
    + PARFUM_VAR + " Sonlarda yer alan poligliseril-10 stearat ve stearik asit nedeniyle fungal akneye yatkın ciltlerde "
    "dikkatli denenmeli. Alkol ve silikon yok.",

"dermokil-100-dogal-gul-suyu-canlandirici-yenileyici-3d-kapsul-krem":
    "Gül suyu içeren, 50 ml'lik bir nemlendirici kapsül krem. Su, propilen glikol, bütilen glikol ve gliserinden sonra "
    "hidrojene lesitin, C12-16 alkolleri ve palmitik asit geliyor; gül suyu onuncu sırada. Niasinamid, palmitoil "
    "tripeptit-5, E vitamini asetatı, hyalüronik asit, pantenol ve centella özü listenin sonlarına doğru. Formülde silikonlar "
    "(dimetikon, dimetikon/vinil dimetikon çapraz polimeri) var; etanol ve parfüm yok. Palmitik asit (7. sırada, Fulton "
    "puanı 2) ve polisorbat 20 nedeniyle fungal akneye yatkın ciltlerde dikkatli denenmeli.",

"dermokil-kuru-ciltler-icin-yogurt-kagit-maske":
    "Ürün adına göre kuru ciltler için hazırlanmış, 20 gr'lık yoğurt özlü kağıt maske. Su, gliserin, propandiol ve "
    "kaprilik/kaprik trigliseritten sonra sekizinci sırada bisabolol, dokuzuncuda yoğurt özü geliyor; cadı fındığı yaprak "
    "özü, sakkarit izomerat, sodyum hyalüronat ve allantoin de formülde. " + PARFUM_VAR + " Alkol ve silikon yok.",

"dermokil-mat-gorunumlu-ciltler-icin-bal-maskesi":
    "Ürün adına göre mat görünüm isteyen ciltler için hazırlanmış, 20 gr'lık bal özlü bir maske. Su, gliserin, propandiol "
    "ve kaprilik/kaprik trigliseritten sonra beşinci sırada bal özü geliyor; bisabolol, cadı fındığı yaprak özü, sakkarit "
    "izomerat, sodyum hyalüronat ve allantoin de formülde. " + PARFUM_VAR + " Alkol ve silikon yok.",

"dermokil-kojik-asit-leke-karsiti-kil-yuz-maskesi":
    "Kojik asit ve 3-O-etil askorbik asit (C vitamini türevi) içeren, kil bazlı 50 ml'lik bir yüz maskesi. Su ve kilden "
    "sonra gliseril stearat, gliserin, mısır nişastası ve setearil alkol geliyor; shea yağı onuncu, kojik asit on birinci, "
    "etil askorbik asit on üçüncü sırada. Titanyum dioksit, E vitamini asetatı ve allantoin de formülde; renk için CI 16255 "
    "ve tartrazin (CI 19140) kullanılmış. Listede parfüm, alkol ve silikon yok. Gliseril stearat, stearik asit (8. sırada, "
    "Fulton puanı 2-3) ve shea yağı nedeniyle fungal akneye yatkın ciltlerde dikkatli denenmeli.",

"dermokil-detoks-kil-stick-yuz-maskesi":
    "Kil bazlı, 30 gr'lık stick formunda bir yüz maskesi; niasinamid, salisilik asit (BHA) ve 3-O-etil askorbik asit "
    "(C vitamini türevi) içeriyor. Su, kil, gliserin ve bütilen glikolden sonra beşinci sırada sodyum stearat var; "
    "niasinamid sekizinci, salisilik asit dokuzuncu, etil askorbik asit onuncu sırada. Aloe vera özü ve titanyum dioksit de "
    "formülde; renk için tartrazin (CI 19140) kullanılmış. Listede parfüm, alkol, yağ ve silikon yok. Sodyum stearat "
    "nedeniyle fungal akneye yatkın ciltlerde dikkatli denenmeli. Salisilik asit kuruluk yapabilir; gündüz güneş koruyucu "
    "sürmek iyi olur.",

"foreo-luna-micro-foam-temizleyici":
    "100 ml'lik köpük formunda bir yüz temizleyici. Su ve gliserinden sonra temizleme gücünü sodyum kokoil glisinat, "
    "kokamidopropil betain, PEG-150 distearat ve disodyum kokoamfodiasetat gibi yumuşak yüzey aktif maddelerden alıyor. "
    "E vitamini asetatı, centella, semizotu, balık otu ve chia tohumu özleri de formülde. Listede sülfat, parfüm ve alkol "
    "yok. Yedinci sıradaki glikol distearat nedeniyle fungal akneye yatkın ciltlerde dikkatli denenmeli.",

"olalab-akne-siyah-nokta-ve-leke-karsiti-aydinlatici-sikilastirici-5-glikolik-asit-tonik":
    "Ürün adına göre %5 glikolik asit (AHA) içeren, 200 ml'lik bir tonik. Glikolik asit su ve gliserinden hemen sonra "
    "üçüncü sırada; ardından niasinamid, gül suyu, sodyum PCA, propilen glikol ve pantenol geliyor. Allantoin, aloe vera "
    "suyu, biyotin ve ginseng, atkuyruğu, papatya, adaçayı, ısırgan, yeşil çay gibi çok sayıda bitki özü de formülde. "
    "Listede parfüm, alkol, yağ ve silikon yok. AHA kuruluk ve hassasiyet yapabilir; ilk haftalarda gün aşırı kullanmak "
    "ve gündüz güneş koruyucu sürmek iyi olur.",

"olalab-leke-karsiti-aydinlatici-alpha-arbutin-cilt-serumu":
    "Alfa arbutin ve niasinamid içeren, 30 ml'lik su bazlı bir serum. Su ve propilen glikolden sonra üçüncü sırada alfa "
    "arbutin geliyor; ardından Lactobacillus/pirinç fermentasyon süzüntüsü, aloe vera suyu ve niasinamid sıralanıyor. "
    "Sodyum PCA ve gliserin de formülde. Listede eklenmiş parfüm yok, ancak sonlarda AB'de koku alerjeni sayılan benzil "
    "alkol bulunuyor; kokuya hassas olanlar bunu göz önünde bulundurmalı. Yağ ve silikon yok.",

"olalab-yaslanma-karsiti-onarici-cilt-yenileyici-retinol-peptit-cilt-serumu":
    "Retinil palmitat (A vitamini türevi) ve palmitoil peptitler içeren, 30 ml'lik bir serum. Su, gliserin, üzüm çekirdeği "
    "özü ve ksantan gamdan sonra palmitoil tripeptit-1 ile palmitoil tetrapeptit-7 geliyor; retinil palmitat on ikinci "
    "sırada. Listede parfüm var; ayrıca sonlarda benzil "
    "salisilat, sitronellol, öjenol, kumarin ve linalool gibi koku alerjenleri bulunuyor, kokuya hassas olanlar dikkatli "
    "olmalı. Retinil palmitat nedeniyle fungal akneye yatkın ciltlerde dikkatli denenmeli. " + RETINOID,

"olalab-aydinlatici-ton-esitleyici-spf-50-yuksek-uv-koruma-pembe-yuz-gunes-kremi":
    "Pembe tonlu, 50 ml'lik SPF 50+ yüz güneş kremi; hem kimyasal hem mineral filtre kullanıyor. Kimyasal filtreler oktokrilen, "
    "etilheksil metoksisinamat, etilheksil salisilat ve avobenzon; mineral filtreler çinko oksit ile titanyum dioksit. "
    "Niasinamid, meyan kökü özü, pantenol, E vitamini asetatı ve laktik asit de formülde; ton için demir oksitler ve kalamin "
    "var. Silikonlar (dimetikon, trietoksikaprililsilan) ve parfüm listede. Gliseril stearat (6. sırada), stearik asit "
    "(14. sırada, Fulton puanı 2-3) ve setil palmitat nedeniyle fungal akneye yatkın ciltlerde dikkatli denenmeli. " + SUN,

"olalab-torbalanma-koyu-halka-karsiti-aydinlatici-vitamin-c-peptit-goz-kremi":
    "15 ml'lik bir göz kremi; C vitamini türevi, niasinamid, pantenol ve peptitler içeriyor. 3-O-etil askorbik asit on altıncı, "
    "niasinamid on dokuzuncu sırada. Listenin üst sıralarında emolyentler var: gliseril stearat SE dördüncü, "
    "etilheksil palmitat altıncı sırada ve Fulton çalışmasında sırasıyla 3 ve 4 komedojenlik puanı almış. İzododekan ve "
    "dimetikon (silikon) da listede. Parfüm ile sonlarda sitronellol ve hidroksisitronellal koku alerjenleri bulunuyor. "
    "Bu maddeler ve yalancı iğde meyve yağı nedeniyle yağlı ve fungal akneye yatkın ciltlerde dikkatli denenmeli.",

"olalab-yaslanma-karsiti-yenileyici-nemlendirici-retinol-gece-yuz-kremi":
    "Retinil palmitat (A vitamini türevi), niasinamid ve hyalüronik asit içeren, 50 ml'lik bir gece kremi. Üst sıralarda "
    "yağımsı maddeler var: etilheksil palmitat ikinci sırada ve Fulton çalışmasında komedojenlik puanı 4 almış; ardından "
    "gliseril stearat, kayısı çekirdeği yağı ve gliserin, sekizinci sırada shea yağı, on ikincide jojoba yağı geliyor. "
    "Listede parfüm ve etanol var. Bu yağlar, polisorbat 20 ve retinil "
    "palmitat nedeniyle yağlı ve fungal akneye yatkın ciltlerde dikkatli denenmeli. " + RETINOID,

"olalab-arindirici-bariyer-onarici-probiyotik-icerikli-makyaj-yuz-temizleme-jeli":
    "Makyaj temizlemek için hazırlanmış, 200 ml'lik bir yüz temizleme jeli. Su ve lauril glukozit, kokamidopropil betain, "
    "sodyum kokoamfoasetat gibi yüzey aktif maddelerden sonra gliserin ve propilen glikol geliyor; parfüm yedinci sırada. "
    "Papatya özü, Bifida fermentasyon lizatı, pantenol ve niasinamid de formülde. Listede benzil alkol ve on yedinci "
    "sırada izopropil alkol var. Koruyucu olarak metilkloroizotiazolinon ve metilizotiazolinon kullanılmış; bunlara duyarlı "
    "ciltlerde, parfüm ve alkol nedeniyle de hassas ciltlerde dikkatli denenmeli.",

"olalab-c-vitaminli-aydinlatici-leke-karsiti-gunluk-su-bazli-nemlendirici-krem":
    "3-O-etil askorbik asit (C vitamini türevi), niasinamid, pantenol ve çok sayıda hyalüronik asit formu içeren, 50 ml'lik "
    "günlük nemlendirici krem. Sudan hemen sonra ikinci sırada izopropil miristat geliyor ve Fulton çalışmasında "
    "komedojenlik puanı 5 almış; ardından propilen glikol, sodyum akrilat kopolimeri ve dibütil adipat sıralanıyor. Etil "
    "askorbik asit altıncı, pantenol sekizinci, niasinamid on üçüncü sırada. Hidrolize kolajen de formülde. Listede parfüm, "
    "alkol ve silikon yok. İzopropil miristat nedeniyle yağlı, akneye ve fungal akneye yatkın ciltlerde dikkatli "
    "denenmeli.",

"olalab-akne-ve-siyah-nokta-karsiti-gozenek-sikilastirici-niacinamide-cilt-serumu":
    "Niasinamid ve salisilik asit (BHA) içeren, 30 ml'lik bir serum. Su ve gliserinden sonra üçüncü sırada niasinamid, "
    "dördüncüde centella özü geliyor; çay ağacı yağı sekizinci, salisilik asit dokuzuncu sırada. Kahve çekirdeği, at "
    "kestanesi, acı portakal, havuç, ardıç, biberiye ve sarmaşık özleri de formülde. Listede eklenmiş parfüm yok, ancak "
    "çay ağacı yağı ile sonlarda linalool ve limonen gibi koku bileşenleri bulunuyor; uçucu yağlar hassas ciltlerde tahriş "
    "yapabilir. Salisilik asit kuruluk yapabilir; gündüz güneş koruyucu sürmek iyi olur.",

"olalab-c-vitaminli-leke-karsiti-spf-50-yuksek-uv-korumali-yuz-gunes-kremi":
    "C vitamini türevi içeren, 50 ml'lik SPF 50+ yüz güneş kremi; hem kimyasal hem mineral filtre kullanıyor. Kimyasal "
    "filtreler oktokrilen, etilheksil metoksisinamat, etilheksil salisilat ve avobenzon; mineral filtreler çinko oksit ile "
    "titanyum dioksit. Üre, niasinamid, meyan kökü, pantenol, 3-O-etil askorbik asit, allantoin ve laktik asit de formülde. "
    "Silikon (dimetikon), pirinç kepeği yağı ve parfüm listede. Gliseril stearat, stearik asit (15. sırada, Fulton puanı "
    "2-3) ve pirinç kepeği yağı nedeniyle fungal akneye yatkın ciltlerde dikkatli denenmeli. " + SUN,

"olalab-aydinlatici-bariyer-onarici-nemlendirici-ceramide-vitamin-c-cica-serum":
    "Seramid, 3-O-etil askorbik asit (C vitamini türevi) ve centella içeren, 30 ml'lik bir serum. Su, gliserin ve propilen "
    "glikolden sonra dördüncü sırada skualan, beşincide etilheksil palmitat geliyor; etilheksil palmitat Fulton "
    "çalışmasında komedojenlik puanı 4 almış. Niasinamid yedinci, pantenol onuncu, etil askorbik asit on birinci sırada; "
    "seramid NP, AP ve EOP, kolesterol ve fitosfingozin listenin ikinci yarısında. Listede parfüm, alkol ve silikon yok. "
    "Etilheksil palmitat, polisorbat 20 ve gliseril stearat nedeniyle fungal akneye yatkın ciltlerde dikkatli denenmeli.",

"olalab-ince-cizgi-kirisiklik-karsiti-sikilastirici-mikro-alg-peptit-goz-kremi":
    "15 ml'lik bir göz kremi; mikro alg (Dunaliella salina) özü ve peptit içeriyor. Niasinamid, pantenol, sodyum hyalüronat, "
    "E vitamini asetatı ve palmitoil tripeptit-5 de formülde. Su, setearil alkol, gliseril stearat ve shea "
    "yağından sonra niasinamid yedinci, pantenol sekizinci sırada; dokuzuncu ve onuncu sırada silikonlar (siklopentasiloksan, "
    "dimetikon) geliyor. Listede parfüm ve etanol yok. Gliseril stearat, shea yağı ve setil palmitat nedeniyle yağlı ve "
    "fungal akneye yatkın ciltlerde dikkatli denenmeli.",

"olalab-arindirici-makyaj-temizleyici-cift-asamali-yuz-temizleme-yagi":
    "Makyaj temizlemek için hazırlanmış, 200 ml'lik çift aşamalı bir temizleme yağı. Temizleme gücünü ilk sıradaki PEG-7 "
    "gliseril kokoat ile lauril glukozit, disodyum kokoamfodiasetat ve koko glukozit gibi yüzey aktif maddelerden alıyor; "
    "gliseril oleat altıncı sırada. Aloe vera suyu, niasinamid, allantoin, çinko PCA ve laktik asit de formülde. Avokado, "
    "hindistan cevizi ve üzüm çekirdeği yağları on ikinci ile on dördüncü sıralar arasında; hindistan cevizi yağı Fulton "
    "çalışmasında komedojenlik puanı 4 almış. Bu yağlar ve gliseril oleat nedeniyle yağlı ve fungal akneye yatkın ciltlerde "
    "dikkatli denenmeli. Listede parfüm, alkol ve silikon yok.",
}
