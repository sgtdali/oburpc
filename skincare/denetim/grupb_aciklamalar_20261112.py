"""Benri, Lip Smacker ve Vaseline ürün açıklamaları (2026-11-12). İçerik listeleri Gratis'ten; markaların Türkiye
sitesi doğrulanamadı (rapor_b.md). Uygulama: python -X utf8 urun_metni.py grupb_aciklamalar_20261112 --write
"""
LS_BASE = ("Hint yağı, kaprilik/kaprik trigliserit ve balmumunun ardından kandelilla mumu ve polibüten geliyor; "
           "etilheksil palmitat, ayçiçeği yağı ve parafin ise formülün devamında. Tatlandırıcı olarak sukraloz var.")
LS_FUNGAL = ("Hint yağı, etilheksil palmitat, ayçiçeği yağı, hidrojene soya yağı ve stearik asit nedeniyle fungal akneye "
             "yatkın ciltlerde dikkatli denenmeli.")
LS_EHP6 = "Altıncı sıradaki etilheksil palmitat Fulton (1989) çalışmasında komedojenlik puanı 4 almış."
LS_EHP7 = "Yedinci sıradaki etilheksil palmitat Fulton (1989) çalışmasında komedojenlik puanı 4 almış."
VL_FUNGAL_LIP = ("Hint yağı, setil palmitat, miristil miristat, poligliseril-3 distearat ve shea yağı nedeniyle fungal "
                 "akneye yatkın ciltlerde dikkatli denenmeli.")
VL_LIP_BASE = ("Oktildodekanol, mikrokristal mum, hint yağı ve kaprilik/kaprik trigliseritin ardından petrolatum "
               "(vazelin) geliyor; miristil miristat, shea yağı, karnauba mumu ve balmumu da formülde.")
VL_MM = "Yedinci sıradaki miristil miristat Fulton (1989) çalışmasında komedojenlik puanı 5 almış."
VL_BODY_FUNGAL = ("Stearik asit, izopropil palmitat, glikol stearat ve gliseril stearat nedeniyle fungal akneye yatkın "
                   "bölgelerde dikkatli kullanılmalı.")
VL_IPP = "Dördüncü sıradaki izopropil palmitat Fulton (1989) çalışmasında komedojenlik puanı 4 almış."
PARABEN = "Listede metilparaben ve propilparaben var."
GLUTA_FRAG = "Listede parfüm ve koku alerjenleri var; kokuya hassas olanlar bunu göz önünde bulundurmalı."

TEXT = {
"benri-seftali-pie-pops-vucut-losyonu":
    "Şeftali Pie Pops adıyla satılan, 500 ml'lik bir vücut losyonu. Su, setearil alkol ve gliseril stearatın ardından PEG-100 "
    "stearat, mineral yağ, etilheksil palmitat, gliserin ve dimetikon geliyor; aloe vera özü ve E vitamini asetatı listenin "
    "sonlarında. Listede parfüm var; kokuya hassas olanlar bunu göz önünde bulundurmalı. Altıncı sıradaki etilheksil "
    "palmitat Fulton (1989) çalışmasında komedojenlik puanı 4 almış; bu madde ve gliseril stearat nedeniyle sırt ve göğüs "
    "gibi fungal akneye yatkın bölgelerde dikkatli kullanılmalı.",
"benri-argan-yagli-yogun-nemlendirici-el-vucut-kremi":
    "Argan yağı içeren, 500 ml'lik bir el ve vücut kremi. Su, setearil alkol ve gliseril stearatın ardından PEG-100 stearat, "
    "etilheksil palmitat, mineral yağ, gliserin ve dimetikon geliyor; argan çekirdeği yağı listenin ortasından sonra, "
    "E vitamini asetatı onun ardından. Listede parfüm ile heksil sinnamal, linalool ve öjenol gibi koku alerjenleri var. "
    "Beşinci sıradaki etilheksil palmitat Fulton (1989) çalışmasında komedojenlik puanı 4 almış; bu madde, gliseril stearat "
    "ve argan yağı nedeniyle fungal akneye yatkın bölgelerde dikkatli kullanılmalı.",
"lip-smacker-coca-cola-dudak-kremi":
    "Coca Cola aromalı bir dudak bakım ürünü. " + LS_BASE + " Listede aroma, sukraloz ve limonen, sitral, sinnamal, öjenol, "
    "geraniol, benzil benzoat gibi koku alerjenleri var; kokuya hassas olanlar bunu göz önünde bulundurmalı. " + LS_EHP6 + " "
    + LS_FUNGAL,
"lip-smacker-dudak-kremi-elsa":
    "Elsa temalı, aromalı bir dudak bakım ürünü. " + LS_BASE + " Listede parfüm ile linalool, vanilin, benzaldehit, limonen "
    "ve benzil alkol gibi koku alerjenleri var; kokuya hassas olanlar bunu göz önünde bulundurmalı. " + LS_EHP6 + " "
    + LS_FUNGAL,
"lip-smacker-disney-elsa-anna-dudak-kremi":
    "Disney Elsa ve Anna temalı, aromalı bir dudak bakım ürünü. " + LS_BASE + " Listede aroma ve benzil alkol var; renk "
    "veren maddeler arasında tartrazin (CI 19140) de bulunuyor. " + LS_EHP6 + " " + LS_FUNGAL,
"lip-smacker-tropikal-kokteyl-dudak-kremi":
    "Tropikal kokteyl aromalı bir dudak bakım ürünü. " + LS_BASE + " Listede aroma ve limonen, sitronellol, linalool, sitral, "
    "geraniol gibi koku alerjenleri var; kokuya hassas olanlar bunu göz önünde bulundurmalı. " + LS_EHP7 + " " + LS_FUNGAL,
"lip-smacker-fanta-dudak-kremi":
    "Fanta aromalı bir dudak bakım ürünü. " + LS_BASE + " Listede aroma ve limonen, benzil alkol, linalool, sitral gibi koku "
    "alerjenleri var; renk veren maddeler arasında tartrazin (CI 19140) de bulunuyor. " + LS_EHP6 + " " + LS_FUNGAL,
"lip-smacker-rapunzel-magical-glow-dudak-kremi":
    "Rapunzel Magical Glow adıyla satılan, aromalı bir dudak bakım ürünü. " + LS_BASE + " Listede aroma ve benzil benzoat, "
    "benzil alkol, linalool, sitral gibi koku alerjenleri var; kokuya hassas olanlar bunu göz önünde bulundurmalı. "
    + LS_EHP6 + " " + LS_FUNGAL,
"lip-smacker-cilekli-fanta-dudak-kremi":
    "Çilekli Fanta aromalı bir dudak bakım ürünü. Hint yağı, kaprilik/kaprik trigliserit, balmumu ve kandelilla mumunun "
    "ardından aroma, polibüten ve etilheksil palmitat geliyor; ayçiçeği yağı, parafin ve sukraloz formülün devamında. "
    "Listede aromanın yanında limonen, sitral ve metil 2-oktinoat var; kokuya hassas olanlar bunu göz önünde "
    "bulundurmalı. " + LS_EHP7 + " " + LS_FUNGAL,
"lip-smacker-sprite-dudak-kremi":
    "Sprite aromalı bir dudak bakım ürünü. " + LS_BASE + " Listede aroma ve limonen, benzil benzoat, sitral, linalool, "
    "geraniol gibi koku alerjenleri var; kokuya hassas olanlar bunu göz önünde bulundurmalı. " + LS_EHP6 + " " + LS_FUNGAL,
"lip-smacker-cilekli-dudak-kremi":
    "Çilek aromalı bir dudak bakım ürünü. " + LS_BASE + " Listede aroma ve benzil alkol var; renk veren maddeler arasında "
    "tartrazin (CI 19140) de bulunuyor. " + LS_EHP6 + " " + LS_FUNGAL,
"lip-smacker-dudak-kremi-pamuk-prenses":
    "Pamuk Prenses temalı, aromalı bir dudak bakım ürünü. " + LS_BASE + " Listede aroma ve benzil benzoat, benzaldehit, "
    "vanilin, limonen, benzil alkol gibi koku alerjenleri var; renk veren maddeler arasında tartrazin (CI 19140) de "
    "bulunuyor. " + LS_EHP6 + " " + LS_FUNGAL,
"vaseline-lip-therapy-dudak-bakim-kremi-original":
    "Vazelin bazlı bir dudak bakım kremi. " + VL_LIP_BASE + " Gliserin, E vitamini asetatı ve pantenol "
    "da formülde; listede parfüm yok. " + VL_MM + " " + VL_FUNGAL_LIP,
"vaseline-lip-therapy-dudak-bakim-kremi-aloe-vera":
    "Aloe vera özlü, vazelin bazlı bir dudak bakım kremi. " + VL_LIP_BASE + " Avokado yağı, yeşil çay özütü ve aloe vera "
    "özü listenin ikinci yarısında. Listede parfüm ile sitral, sitronellol, limonen, öjenol ve linalool gibi koku "
    "alerjenleri var; kokuya hassas olanlar bunu göz önünde bulundurmalı. " + VL_MM + " " + VL_FUNGAL_LIP,
"vaseline-lip-therapy-dudak-bakim-kremi-cherry-blush":
    "Kiraz tonunda renk veren, vazelin bazlı bir dudak bakım kremi. Oktildodekanol, mikrokristal mum ve hint yağının ardından "
    "kaprilik/kaprik trigliserit, setil palmitat, petrolatum ve miristil miristat geliyor; renk için pigmentler ve mika var. "
    "Listede parfüm, mentol ve benzil alkol, öjenol, vanilin gibi koku alerjenleri bulunuyor; kokuya hassas olanlar bunu göz "
    "önünde bulundurmalı. " + VL_MM + " " + VL_FUNGAL_LIP,
"vaseline-lip-therapy-dudak-bakim-kremi-rosy-lips":
    "Hafif pembe renk veren, vazelin bazlı bir dudak bakım kremi. " + VL_LIP_BASE + " Gül yağı, zeytin ve tatlı badem yağı "
    "listenin ikinci yarısında. Listede parfüm ile sitronellol, limonen, linalool ve benzil "
    "benzoat gibi koku alerjenleri var; kokuya hassas olanlar bunu göz önünde bulundurmalı. " + VL_MM + " " + VL_FUNGAL_LIP,
"vaseline-lip-therapy-dudak-bakim-kremi-cocoa-butter":
    "Kakao yağlı, hafif renkli, vazelin bazlı bir dudak bakım kremi. " + VL_LIP_BASE + " Kakao yağı on birinci sırada; "
    "jojoba, makademya yağı, yeşil çay ve avokado özleri de formülde. Listede parfüm, limonen ve benzil benzoat var; "
    "kokuya hassas olanlar bunu göz önünde bulundurmalı. " + VL_MM + " " + VL_FUNGAL_LIP,
"vaseline-lip-therapy-yumusatici-dudak-kremi-kakao-yagi":
    "Yalnızca birkaç maddeden oluşan, kakao yağlı bir dudak yumuşatıcısı. Liste petrolatum (vazelin) ile başlıyor, ardından "
    "kakao yağı geliyor; sonra benzil alkol, benzil benzoat, benzil sinnamat ve limonen var. Listede parfüm yazmıyor ama "
    "bu koku alerjenleri bulunuyor; kokuya hassas olanlar bunu göz önünde bulundurmalı. İkinci sıradaki kakao yağı Fulton "
    "(1989) çalışmasında komedojenlik puanı 4 almış; fungal akneye yatkın ciltlerde de dikkatli denenmeli.",
"vaseline-lip-therapy-yumusatici-dudak-kremi-rosy-lips":
    "Hafif pembe renk veren, çok kısa içerik listeli bir dudak yumuşatıcısı. Petrolatum (vazelin), tatlı badem yağı ve şam "
    "gülü yağından oluşuyor; ardından parfüm ve linalool geliyor, renk için titanyum dioksit ve bir pigment var. Listede "
    "parfüm ile gül yağı kaynaklı koku alerjenleri bulunuyor; kokuya hassas olanlar bunu göz önünde bulundurmalı. Tatlı badem "
    "yağı nedeniyle fungal akneye yatkın ciltlerde dikkatli denenmeli.",
"vaseline-vucut-losyonu-hassas-bakim-kuru-cok-kuru-ve-hassas-ciltler-icin":
    "Ürün adına göre kuru, çok kuru ve hassas ciltler için bir vücut losyonu. Su, gliserin ve stearik asidin ardından "
    "izopropil palmitat, glikol stearat, PEG-100 stearat, dimetikon, mineral yağ ve gliseril stearat geliyor; petrolatum "
    "(vazelin) onuncu sırada. " + PARABEN + " " + VL_IPP + " " + VL_BODY_FUNGAL,
"vaseline-vucut-losyonu-kakao-isiltisi-parlakligini-kaybetmis-ve-kuru-ciltler-icin":
    "Ürün adına göre parlaklığını kaybetmiş ve kuru ciltler için, kakao yağlı bir vücut losyonu. Su, petrolatum (vazelin) "
    "ve gliserinin ardından stearik asit, izopropil palmitat, glikol stearat ve dimetikon geliyor; kakao ve shea yağı onuncu "
    "ve on birinci sırada. Listede parfüm ve sitronellol, kumarin, geraniol, linalool gibi koku alerjenleri ile metilparaben "
    "ve propilparaben var. Beşinci sıradaki izopropil palmitat ve onuncu sıradaki kakao yağı Fulton (1989) çalışmasında "
    "komedojenlik puanı 4 almış. " + VL_BODY_FUNGAL,
"vaseline-vucut-losyonu-aloe-vera-ferahligi-kuru-ciltler-icin":
    "Ürün adına göre kuru ciltler için, aloe vera ferahlığı vurgulu bir vücut losyonu. Su, stearik asit, gliserin, glikol "
    "stearat ve izopropil palmitatın ardından petrolatum (vazelin), trietanolamin ve gliseril stearat geliyor; aloe vera "
    "yaprak suyu tozu ve laktik asit listenin sonlarında. Listede parfüm, linalool, geraniol, heksil sinnamal gibi koku "
    "alerjenleri ile metilparaben ve propilparaben var. Beşinci sıradaki izopropil palmitat Fulton (1989) çalışmasında "
    "komedojenlik puanı 4 almış. " + VL_BODY_FUNGAL,
"vaseline-vucut-losyonu-temel-onarim-kuru-ciltler-icin":
    "Ürün adına göre kuru ciltler için bir vücut losyonu. Su, petrolatum (vazelin) ve gliserinin ardından stearik asit, "
    "izopropil palmitat, glikol stearat ve dimetikon geliyor; kakao ve shea yağı onuncu ve on birinci sırada. Listede "
    "parfüm ve sitronellol, kumarin, geraniol, linalool gibi koku alerjenleri ile metilparaben ve propilparaben var. "
    "Beşinci sıradaki izopropil palmitat ve onuncu sıradaki kakao yağı Fulton (1989) çalışmasında komedojenlik puanı 4 "
    "almış. " + VL_BODY_FUNGAL,
"vaseline-gluta-hya-serum-etkili-yogun-nemlendirici-gece-losyonu":
    "Gluta-Hya serisinden, gece kullanımı için tasarlanmış bir vücut losyonu. Su, dimetikon, gliserin ve izoheksadekanın "
    "ardından niasinamid geliyor; glutatyon, hidrolize kolajen, sodyum PCA ve sodyum hyalüronat listenin ikinci yarısında, "
    "petrolatum (vazelin) de formülde. Listede metilparaben var. " + GLUTA_FRAG,
"vaseline-gluta-hya-serum-etkili-canlandirici-vucut-losyonu":
    "Gluta-Hya serisinden bir vücut losyonu. Su, dimetikon, izoheksadekan ve gliserinin ardından niasinamid geliyor; "
    "glutatyon, sodyum PCA ve sodyum hyalüronat listenin ikinci yarısında, petrolatum (vazelin) de formülde. Listede "
    "metilparaben var. " + GLUTA_FRAG,
"vaseline-gluta-hya-serum-etkili-vucut-losyonu-sikilastirici":
    "Gluta-Hya serisinden, adına göre sıkılaştırıcı etkili bir vücut losyonu. Su, dimetikon, gliserin ve izoheksadekanın "
    "ardından niasinamid geliyor; hidrolize kolajen, sodyum PCA, glutatyon ve sodyum hyalüronat da formülde, petrolatum "
    "(vazelin) daha sonra. Listede metilparaben var. " + GLUTA_FRAG,
"vaseline-gunluk-gunes-koruyucu-stick-spf-50":
    "SPF 50+ değerli, stick formunda bir güneş koruyucu. Filtrelerin hepsi kimyasal: homosalat, oktokrilen, etilheksil "
    "salisilat, avobenzon, etilheksil metoksisinamat ve bis-etilheksiloksifenol metoksifenil triazin. Dimetikon, silikon "
    "bazlı polimerler ve sentetik mum dokuyu oluşturuyor. Listede parfüm ile benzil alkol, heksil sinnamal ve linalool var; "
    "kokuya hassas olanlar bunu göz önünde bulundurmalı. Dördüncü sıradaki etilheksil palmitat Fulton (1989) çalışmasında "
    "komedojenlik puanı 4 almış; fungal akneye yatkın ciltlerde dikkatli denenmeli. Koruma için yeterli miktarda "
    "sürülmeli ve iki saatte bir yenilenmeli.",
}
