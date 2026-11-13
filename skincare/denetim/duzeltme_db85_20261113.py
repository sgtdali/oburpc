"""2026-11-13: ortağın doğrudan DB'ye yazdığı 85 ürün veri hattına alınırken urun_metni.py denetiminde takılan
açıklamalar (iç analiz dili, "parfüm içermiyor" ↔ benzil alkol koku alerjeni, "hiyalüronat" yazımı)."""
TEXT = {
    "mia-klinika-spf-50-bariyer-onarici-gunes-koruyucu-krem":
        "Güneşten korunmaya yönelik bu krem, oktokrilen ve etilheksil metoksisinamat gibi UV filtreleri içerir. "
        "Gliserin ve sodyum hyalüronat nemi desteklerken seramid NP ve skualan cilt bariyerine bakım sağlar. Formülde "
        "eklenmiş parfüm ve kurutucu alkol bulunmuyor. Etilheksil metoksisinamat, mercan resiflerine etkisi "
        "nedeniyle bazı bölgelerde kısıtlanan bir UV filtresi.",
    "mia-klinika-tiger-grass-ton-esitleyici-50-spf-cica-krem-30-ml":
        "Renk pigmentleri içeren bu güneş kreminde çinko oksit, titanyum dioksit ve etilheksil metoksisinamat "
        "filtreleri bulunur. Centella yaprağı özütü ve madekasosid yatıştırıcı bakımı, gliserin ve sodyum hyalüronat "
        "nemi destekler. Formül silikonlu; etilheksil metoksisinamat, mercan resiflerine etkisi nedeniyle bazı "
        "bölgelerde kısıtlanan bir UV filtresi.",
    "nivea-55-plus-yas-canlandirici-yuz-kremi":
        "Olgun ciltlere yönelik, nemlendirici ve yenileyici bir yüz kremi. Gliserin, argan yağı, üzüm çekirdeği yağı "
        "ve soya yağı formülde yumuşatıcı ve nem tutucu olarak yer alıyor; E vitamini ve kalsiyum pantotenat (B5) da "
        "bulunuyor. Dimetikon içeriyor; linalol, limonen, kumarin ve geraniol gibi koku bileşenleri nedeniyle kokuya "
        "hassas ciltler dikkatli olmalı. Oktokrilen ve butil metoksidibenzoilmetan gibi UV filtreleri içeriyor, ancak "
        "ürün bir SPF değeri taşımadığı için güneş koruması yerine kullanılmamalı.",
    "sinoz-biphase-micellar-makyaj-temizleme-suyu":
        "Suya dayanıklı makyajı çözmeye yönelik çift fazlı bir micellar su. Formülde skualan, laktik asit (AHA) ve "
        "tokoferol öne çıkan bileşenler; alkol ve paraben içermiyor, listede eklenmiş parfüm de yok. İzohekzadekan, "
        "izododekan, avokado yağı ve ayçiçeği yağı ile yağ fazı oluşturuluyor; avokado yağı ve izopropil palmitat "
        "akneye eğilimli ciltlerde dikkat gerektirebilir. Benzil alkol içeriyor ve bu madde AB'de alerjen olarak "
        "listelenir; ayrıca benzotriazolil dodesil p-kresol bir UV absorberi olarak yer alıyor.",
}
