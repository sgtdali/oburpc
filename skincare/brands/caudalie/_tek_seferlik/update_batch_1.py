import json

products_update = {
    "caudalie-vinoclean-gentle-buffing-cream": "İçeriğindeki jojoba tanecikleri ile cildi nazikçe ölü hücrelerden arındırmayı hedefleyen kremsi bir peelingdir. Formülündeki üzüm çekirdeği yağı ve bal özü, cildi kurutmadan temizlemeye ve yumuşatmaya destek olur. Düzenli kullanımda daha pürüzsüz, arınmış ve aydınlık bir cilt görünümü sağlamaya yardımcıdır.",
    "caudalie-vinoclean-instant-foaming-cleanser": "Papatya ve adaçayı özleri ile formüle edilmiş, cildi nazikçe temizlemeyi ve kirden arındırmayı amaçlayan köpük formlu bir yüz yıkama ürünüdür. Formülündeki üzüm suyu desteği ile cildin nem dengesini korumaya ve cilde tazelik kazandırmaya yardımcı olur. Sabun içermeyen yapısıyla günlük cilt temizliği rutininde yumuşak bir his bırakır.",
    "caudalie-beauty-elixir": "Tarihi bir güzellik iksirinden ilham alan bu sprey tonik, içeriğindeki gül, nane ve biberiye uçucu yağları ile cildi canlandırmayı ve gözenek görünümünü sıkılaştırmayı hedefler. Yüzeydeki nemi desteklerken cilde anında ferahlık ve sağlıklı bir ışıltı kazandırmaya yardımcı olur. Makyaj öncesi cildi hazırlamak veya gün içinde tazelemek için pratik bir kullanım sunar.",
    "caudalie-grape-water": "Yalnızca organik üzüm suyu ile formüle edilmiş, hassasiyete eğilimli ciltleri yatıştırmayı hedefleyen ferahlatıcı bir yüz spreyidir. Cildi nemlendirmeye ve polifenol desteğiyle çevresel etkenlere karşı korumaya yardımcı olur. Günün her anında cildi tazelemek, kuruluk veya gerginlik hissini azaltmaya destek olmak için pratik bir şekilde kullanılabilir.",
    "caudalie-vinoperfect-glycolic-peel-mask": "Glikolik asit ve meyve asitleri (AHA) kompleksi içeren bu maske, cilt yüzeyindeki ölü hücreleri arındırarak daha eşit ve aydınlık bir cilt tonu sağlamayı hefler. Formülündeki asma çubuğu özü (Viniferine) ve skualen desteği ile cildi nemlendirirken, leke görünümünü hafifletmeye yardımcı olur. Sadece on dakikada daha pürüzsüz ve canlı bir cilt dokusu elde etmeyi destekler.",
    "caudalie-vinoperfect-brightening-eye-cream": "Asma çubuğundan elde edilen patentli Viniferine ve kafein ile zenginleştirilmiş, göz altı morluklarının görünümünü hafifletmeyi hedefleyen bakım kremidir. Formülündeki niasinamid desteğiyle göz çevresine aydınlık ve canlı bir görünüm kazandırmaya yardımcı olur. Özel seramik aplikatörü sayesinde uygulandığında serinletici bir masaj etkisi yaratarak yorgun görünümü azaltmaya destek olur.",
    "caudalie-vinotherapist-lip-conditioner": "Üzüm çekirdeği yağı, macadamia yağı ve shea yağı ile formüle edilen bu bakım kremi, dudakları kuruluktan korumaya ve onarımına yardımcı olur. Hafif vanilya notalarıyla dudaklarda yumuşak, nemli ve yapışkan olmayan bir his bırakır. Antioksidan polifenol özellikleriyle dudakları çevresel faktörlere karşı korumayı destekler.",
    "caudalie-vinotherapist-replenishing-vegan-body-butter": "Çöl hurması yağı, üzüm çekirdeği yağı ve shea yağı içeren, özellikle çok kuru ve atopiye eğilimli ciltlerde yoğun nemlendirme ve rahatlama sağlamayı hedefleyen vücut balmıdır. Yoğun yapısına rağmen kolay emilen dokusuyla ciltte kaşıntı ve gerginlik hissini yatıştırmaya yardımcı olur. Cildi besleyerek uzun süreli bir yumuşaklık ve esneklik hissi bırakır.",
    "caudalie-vinotherapist-hyaluronic-nourishing-body-lotion": "Hyalüronik asit, shea yağı ve üzüm çekirdeği polifenolleri içeren bu losyon, cildin günlük nem ihtiyacını karşılamayı ve gün boyu süren bir konfor sağlamayı hedefler. Hafif dokusuyla cilt tarafından hızla emilir ve yağlı bir his bırakmadan esneklik kazandırmaya destek olur. Cildi yumuşatarak pürüzsüz ve aydınlık bir görünüm elde etmeye yardımcıdır.",
    "caudalie-the-des-vignes-hyaluronic-nourishing-body-lotion": "Hyalüronik asit ve bitkisel yağlar ile zenginleştirilmiş formülüyle cildi yoğun şekilde nemlendirmeyi ve beslemeyi amaçlayan vücut losyonudur. İkonik Thé des Vignes (beyaz misk, turunç ve zencefil) kokusuna sahiptir. Cilde gün boyu nem desteği sunarken aynı zamanda nazik ve hoş bir kokuyla sarmalamaya yardımcı olur.",
    "caudalie-fleur-de-vigne-shower-gel": "Aloe vera özü ve bitkisel kökenli nazik temizleyiciler içeren, karpuz, pembe biber ve beyaz gül notaları barındıran ferahlatıcı duş jelidir. Sabun içermeyen yapısıyla cildin doğal nem dengesini koruyarak temizlemeye yardımcı olur. Günlük vücut temizliğini cildi kurutmadan, tazeleyici bir koku eşliğinde yapmanızı destekler.",
    "caudalie-the-des-vignes-shower-gel": "Sabun içermeyen yüksek toleranslı formülüyle cildi kurutmadan nazikçe temizlemeyi hedefleyen vücut yıkama jelidir. Beyaz misk, turunç ve zencefil notalarına sahip ikonik parfümüyle duş anını keyifli ve rahatlatıcı bir deneyime dönüştürür. Tüm cilt tiplerinin günlük kullanımına uygun olarak geliştirilmiştir.",
    "caudalie-rose-de-vigne-shower-gel": "Gül, ışkın otu (rhubarb) ve beyaz misk notaları içeren, cildi kurutmadan arındırmaya destek olan nazik bir duş jelidir. Aloe vera ekstresiyle zenginleştirilmiş sabunsuz formülü, cildin doğal yapısına saygı duyarak temizlik sağlar. Günlük duş rutininizde cildi taze ve romantik bir kokuyla sarmalamaya yardımcı olur.",
    "caudalie-eau-des-vignes-shower-gel": "Bergamot, iris ve beyaz misk notaları barındıran, sabun içermeyen ve cildi nazikçe arındırmayı amaçlayan günlük duş jelidir. Yüksek toleranslı formülü sayesinde en hassas ciltler dahil tüm cilt tipleri için yatıştırıcı bir temizlik sunar. Cildin nem bariyerini koruyarak duş sonrası kuruluk hissini önlemeye destek olur.",
    "caudalie-vinoperfect-concentrated-brightening-glycolic-essence": "Glikolik asit, şakayık kökü özü ve üzüm suyu içeren formülüyle cildi ölü hücrelerden arındırıp aydınlık bir görünüme kavuşmasına destek olan esans formunda bir bakım suyudur. Cildi nemlendirerek leke karşıtı bakım serumunun etkisine hazırlama aşamasında kullanılır. Düzenli kullanımda cilt dokusunu pürüzsüzleştirmeye ve ton eşitsizliklerini hafifletmeye yardımcı olur."
}

ingredients_update = {
    "hexyldecyl-stearate": "Cildi yumuşatmaya ve nem kaybını önlemeye destek olan bitkisel kökenli bir cilt bakım bileşenidir.",
    "hydrogenated-jojoba-oil": "Jojoba yağından elde edilen, fiziksel peeling ürünlerinde cildi çizmeden nazikçe arındırmaya yardımcı olan mikro taneciklerdir.",
    "mel": "Formüllerde bal özü olarak bilinir. Cildi nemlendirmeye, yumuşatmaya ve yatıştırmaya destek olan besleyici bir içeriktir.",
    "hexyl-cinnamal": "Kozmetik ürünlerine çiçeksi bir koku kazandıran, bazı bitkilerin uçucu yağlarında doğal olarak da bulunan bir koku bileşenidir.",
    "phospholipids": "Cilt bariyeri ile uyumlu, cildin nem tutma kapasitesini artırmaya ve aktif içeriklerin emilimine yardımcı olan lipitlerdir.",
    "polyglyceryl-10-stearate": "Yağ ve su bazlı içeriklerin bir arada kalmasını sağlayan bitkisel kaynaklı ve cilt dostu bir emülgatördür.",
    "benzyl-benzoate": "Formüllerde koku dengeleyici ve çözücü olarak görev yapan organik bir bileşiktir.",
    "salvia-officinalis-leaf-extract": "Adaçayı yapraklarından elde edilen, arındırıcı ve yatıştırıcı özellikleriyle cildin dengesini korumaya destek olan bitkisel bir özüttür.",
    "potassium-alum": "Genellikle arındırıcı ve gözenek sıkılaştırıcı etkileri nedeniyle formüllere eklenen doğal bir mineral tuzdur.",
    "commiphora-myrrha-resin-extract": "Mür ağacı reçinesinden elde edilen özüttür. Cildi yatıştırmaya ve ürüne doğal bir koku sağlamaya yardımcı olur.",
    "styrax-tonkinensis-resin-extract": "Aselbent (sığla) ağacı reçinesinden elde edilen bitkisel bir içeriktir. Cildin yatıştırılmasına ve formüle hoş bir koku katılmasına destek olur.",
    "citrus-aurantium-amara-flower-oil": "Acı portakal çiçeklerinden (neroli) elde edilen, ferahlatıcı koku veren ve cildi yatıştırmaya yardımcı uçucu bir yağdır.",
    "rosa-damascena-flower-oil": "Isparta gülü (Şam gülü) çiçeklerinden elde edilen bu değerli uçucu yağ, cildi nemlendirmeye ve yatıştırmaya destek olur.",
    "vitis-vinifera-fruit-extract": "Üzüm meyvesinden elde edilen, serbest radikallere karşı koruyucu antioksidanlar (polifenoller) açısından oldukça zengin bir özüttür.",
    "farnesol": "Birçok uçucu yağda doğal olarak bulunan ve ürünlere çiçeksi bir koku kazandıran bir koku bileşenidir.",
    "nitrogen": "Basınçlı sprey ürünlerde itici gaz olarak kullanılır, formülün bozulmadan pürüzsüzce püskürtülmesini sağlar.",
    "salix-alba-bark-extract": "Ak söğüt kabuğundan elde edilen bitkisel bir özüttür. Doğal BHA özellikleriyle cildi pürüzsüzleştirmeye ve gözenekleri arındırmaya destek olur.",
    "polyglyceryl-6-laurate": "Formüllerde emülgatör olarak kullanılan bitkisel kökenli bir bileşendir. Yağ ve suyun ayrışmasını engeller.",
    "paeonia-lactiflora-root-extract": "Şakayık kökünden elde edilen bitkisel bir ekstrakttır. Cildin aydınlık bir görünüm kazanmasına ve ton eşitsizliklerinin hafiflemesine yardımcı olur.",
    "polyglycerin-6": "Gliserinden türetilen ve cildin nem tutma kapasitesini artırmaya destek olan etkili bir nemlendirici içeriktir.",
    "acer-saccharum-extract": "Şeker akçaağacından elde edilen bitkisel bir özüttür. Doğal bir AHA kaynağı olarak cilt yüzeyini nazikçe yenilemeye destek olur.",
    "papain": "Papaya meyvesinden elde edilen doğal bir enzimdir. Cildi kurutmadan ölü hücrelerden arındırmaya ve daha pürüzsüz bir doku sağlamaya yardımcıdır.",
    "oleic-acid": "Zeytinyağı gibi doğal yağlarda bolca bulunan Omega-9 yağ asididir. Cildi beslemeye, yumuşatmaya ve bariyerini güçlendirmeye destek olur.",
    "terminalia-arjuna-extract": "Arjuna ağacı kabuğundan elde edilen bitkisel bir özüttür. Antioksidan özellikleriyle cildi desteklemeye yardımcı olur.",
    "sodium-dehydroacetate": "Formüllerin mikrobiyal bozulmalara karşı korunmasına yardımcı olan, kozmetikte sıkça kullanılan bir koruyucu maddedir.",
    "copernicia-cerifera-cera": "Karnauba mumu olarak da bilinir. Brezilya'da yetişen bir palmiye türünden elde edilir, ürünlere yapı ve kıvam kazandırmaya destek olur.",
    "hydrogenated-castor-oil": "Hint yağından elde edilen ve hidrojene edilerek katılaştırılan bir içeriktir. Cildi yumuşatmaya ve nemin buharlaşmasını önlemeye yardımcı olur.",
    "leontopodium-alpinum-flower-leaf-extract": "Edelweiss (Alp Yıldızı) çiçeği özüdür. Güçlü antioksidan özellikleriyle cildi çevresel faktörlere karşı korumaya destek olur.",
    "butyrospermum-parkii-butter-extract": "Shea yağından elde edilen zengin bir ekstrakttır. Cildi yoğun şekilde beslemeye ve pürüzsüzlük hissi sağlamaya yardımcı olur.",
    "octyldodecyl-myristate": "Bitkisel yağ asitlerinden türetilen bir emoliyandır. Cildi yağlandırmadan yumuşatmaya ve formülün sürülebilirliğini artırmaya destek olur."
}

import json

file_path = 'scripts/skincare/staging/caudalie/texts.json'

with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

for k, v in products_update.items():
    data['products'][k] = v

for k, v in ingredients_update.items():
    if k in data['ingredients']:
        data['ingredients'][k]['description'] = v

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Batch 1 completed.")
