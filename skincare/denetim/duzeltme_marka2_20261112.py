"""2026-11-12 (2. parti): Gratis listesinden marka sitesi listesine geçen ürünlerden açıklaması yeni listeyle
çelişenlerin yeniden yazımı. Marka marka eklenir."""
TEXT = {
    # Thalia: markanın güncel formülünde siklopentasiloksan yok, yerinde izoamil laurat var.
    "thalia-natural-beauty-marjoram-yagi-cay-agaci-matlastirici-yuz-kremi":
        "Mercanköşk ve çay ağacı yağı içeren, matlaştırıcı olarak sunulan bir yüz kremi. Su ve izoamil lauratın "
        "ardından setearil alkol, gliseril stearat ve gliserin geliyor; shea yağı 8., jojoba yağı 11. sırada. "
        "Pantenol, allantoin ve E vitamini asetatı da formülde. Mercanköşk ve çay ağacı yağıyla birlikte parfüm ve "
        "limonen, linalool, sitral gibi çok sayıda koku alerjeni içeriyor; kokuya hassas olanlar bunu göz önünde "
        "bulundurmalı. İzoamil laurat, gliseril stearat, shea ve jojoba yağı nedeniyle fungal akneye yatkın ciltlerde "
        "dikkatli denenmeli.",
    # Cosmogenesis: marka ürünü "Repair Cica SPF 15 Color Correcting Cream" olarak satıyor; eski metin SPF'yi yok sayıyordu.
    "cosmogenesis-labs-tiger-grass-cica-krem":
        "Markanın SPF 15'li, renk düzenleyici (CC) krem olarak sunduğu, %5 centella (tiger grass) içerdiğini belirttiği "
        "bir bakım kremi. Su ve dimetikonun ardından centella özütü üçüncü sırada; listedeki tek UV filtresi beşinci "
        "sıradaki titanyum dioksit. Madekasosid 9., pantenol 13., sodyum hyalüronat 15. sırada, seramid NP ise listenin "
        "sonlarında. Dimetikon ve türevleriyle silikonlu bir formül; listede parfüm ve alkol yok. SPF 15 uzun süre güneşte "
        "kalmak için yeterli değil; böyle günlerde ayrıca güneş kremi kullanılmalı.",
    # The Purest Solutions: marka listesi Gratis'tekinden 7 madde uzun; gül özü artık sonda değil (19.).
    "the-purest-solutions-goz-alti-aydinlik-gorunum-destekleyici-bakim-serumu":
        "Göz çevresine yönelik, aydınlık görünüm vaat eden bir bakım serumu. Su, fenetil alkol, pentilen glikol ve "
        "hidroksietilselülozun ardından propilen glikol, kafein ve C vitamini türevi etil askorbik asit (6. ve 7. sıra) "
        "geliyor; gliserin, sodyum PCA ve iki deniz yosunu özü de formülde. Listenin ikinci yarısında dört farklı "
        "hyalüronat türü var. 14. sırada izopropil alkol, 19. sırada damask gülü özü bulunuyor; hassas göz çevresinde "
        "ve kokuya hassas ciltlerde dikkatli denenmeli.",
    # s'hevec: marka sitesindeki güncel formüller Gratis listelerinden çok farklı; eski metinler yeni listeyle çelişiyordu.
    "she-vec-any-time-of-day-48-saat-etkili-su-bazli-nemlendirici-yuz-kremi":
        "Ürün adına göre 48 saat etkili, su bazlı bir yüz nemlendiricisi. Suyun ardından niasinamid ikinci, gliserin "
        "üçüncü, pantenol dördüncü sırada; betain, kaprilik/kaprik trigliserit ve C13-15 alkan onları izliyor. "
        "Tripeptit-2, seramid NP ve beta glukan listenin ortasında, farklı hyalüronik asit türevleri ise sonunda. "
        "Listede parfüm, alkol ve silikon yok.",
    "she-vec-glow-me-like-you-do-aydinlatici-leke-karsiti-ve-ton-esitleyici-yuz-serumu":
        "Ürün adına göre aydınlatıcı ve ton eşitleyici bir yüz serumu. Suyun hemen ardından C vitamini türevi etil "
        "askorbik asit geliyor; pentilen glikol, propilen glikol, pantenol ve gliserin onu izliyor. Allantoin, sodyum "
        "PCA ve listenin sonunda farklı hyalüronik asit türevleri de formülde. Listede parfüm ve alkol yok. Gündüz "
        "kullanımında güneş koruyucuyla tamamlanmalı.",
    "she-vec-hi-girls-bye-pores-gozenek-sikilastirici-ve-leke-karsiti-yuz-serumu":
        "Ürün adına göre gözenek görünümüne ve lekelere yönelik bir yüz serumu. Suyun ardından niasinamid ikinci "
        "sırada; propandiol, pentilen glikol ve pantenol onu izliyor. Çinko PCA 15. sırada, allantoin, gliserin ve "
        "listenin sonunda farklı hyalüronik asit türevleri de formülde. Listede parfüm ve alkol yok.",
    "she-vec-love-in-blue-this-time-onarici-aydinlatici-yuz-serumu":
        "Ürün adına göre kırışıklık görünümüne yönelik, onarıcı ve aydınlatıcı bir yüz serumu. Suyun ardından "
        "niasinamid ikinci, C vitamini türevi etil askorbik asit üçüncü sırada; pentilen glikol ve pantenol onları "
        "izliyor. Seramid NP dokuzuncu, bakır tripeptit-1 yirminci sırada; magnezyum, çinko ve bakır glukonat ile "
        "farklı hyalüronik asit türevleri de formülde. Listede parfüm ve alkol yok.",
    # The Bath Factory: marka listesinde sıra farklı (etilheksil palmitat 3., gliserin 4., setearil alkol 9.).
    "the-bath-factory-vucut-losyonu-sweet-vanilla":
        "Vanilya kokulu bir vücut losyonu. Su ve mineral yağın ardından etilheksil palmitat üçüncü, gliserin dördüncü, "
        "petrolatum beşinci sırada; poligliseril-3 distearat, seteret-20, izopropil miristat, setearil alkol ve dimetikon "
        "onları izliyor. Shea yağı, skualan, sodyum PCA ve sodyum hyalüronat daha geride. Listede parfüm ve koku "
        "alerjeni olan vanilin var; kokuya hassas olanlar bunu göz önünde bulundurmalı. Üçüncü sıradaki etilheksil "
        "palmitat Fulton (1989) çalışmasında komedojenlik puanı 4, sekizinci sıradaki izopropil miristat 5 almış; bu "
        "maddeler, shea yağı ve stearik asit nedeniyle sırt ve göğüs gibi akneye ve fungal akneye yatkın bölgelerde "
        "dikkatli kullanılmalı.",
    # Beauty of Joseon: markanın güncel listesinde su 1., propolis 5. (Gratis'teki eski etikette propolis 1. idi).
    "beauty-of-joseon-glow-isilti-veren-yuz-bakim-serumu-propolis-niacinamide":
        "Propolis ve niasinamid içeren, ışıltı vaat eden bir yüz serumu. Su, dipropilen glikol, gliserin ve bütilen "
        "glikolün ardından propolis özütü beşinci, niasinamid altıncı sırada. Betain salisilat sekizinci sırada; hafif "
        "bir eksfolyan olduğundan hassas ciltler kullanıma yavaş başlamalı. Çay ağacı ve centella özütü ile tamanu "
        "tohumu yağı listenin sonlarında. Listede parfüm yok; propolis ve bitki özlerine duyarlı olanlar önce küçük bir "
        "bölgede denemeli.",
}
