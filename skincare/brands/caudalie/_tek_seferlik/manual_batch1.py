import json

products_update = {
    "caudalie-vinoclean-gentle-buffing-cream": "Ciltteki ölü hücreleri uzaklaştırmak için tasarlanmış fiziksel peeling kremi. Üzüm çekirdeği yağı ve bal özleri cildin temizlenirken kurumamasını destekler. Formülündeki hexyldecyl stearate ve hidrojene jojoba yağı, sivilceye veya mantar aknesine eğilimli kişilerde komedojenik potansiyel taşıyabilir. Limonen, linalool, heksil sinnamal gibi koku alerjenleri ile parfüm içerir.",
    "caudalie-vinoclean-instant-foaming-cleanser": "Papatya ve adaçayı özleri içeren bu köpük formlu temizleyici, cildi günlük kirlerden arındırmayı hedefler. Üzüm suyu desteği ile cildin pH dengesini korumaya ve yatıştırmaya yardımcı olur. Sabun içermeyen yapısına rağmen, koku verici parfüm maddesi ve AB uyarı listesindeki linalool alerjenini barındırır.",
    "caudalie-beauty-elixir": "Gül, biberiye ve nane uçucu yağları ile zenginleştirilmiş sprey toniktir. Gözenek görünümünü sıkılaştırmaya ve cilde ferahlık vermeye yardımcı olur. İçerik listesinin ikinci sırasında alkol bulunmaktadır, bu nedenle çok kuru ciltler dikkatli kullanmalıdır. Sitral, farnesol, geraniol ve limonen gibi koku alerjenleri barındırır.",
    "caudalie-grape-water": "Sadece organik üzüm suyu bileşeninden oluşan, hassasiyet yaşayan ciltleri yatıştırmayı ve ferahlatmayı amaçlayan yüz spreyidir. Antioksidan polifenoller ile cildin çevresel faktörlere karşı desteklenmesine yardımcı olur. Parfüm, alkol veya bilinen herhangi bir alerjen madde içermez.",
    "caudalie-vinoperfect-glycolic-peel-mask": "Glikolik asit ve meyve asitleri (AHA) içeren, cilt tonu eşitsizliklerini on dakikalık kullanımla dengelemeyi hedefleyen maskedir. Asma çubuğu özü (Viniferine) ile formüle edilmiştir. İlk sıralardaki sorbitan stearat ve gliseril stearat SE bileşenleri mantar aknesine yatkın ciltler için gözenek tıkayıcı olabilir. Benzil alkol ve parfüm içerir.",
    "caudalie-vinoperfect-brightening-eye-cream": "Göz altı morluklarının görünümünü hafifletmek için tasarlanmış, asma çubuğu özü ve niasinamid barındıran bakım kremidir. Formülünde yer alan kafein sayesinde yorgunluk belirtilerine karşı destek sağlar. Kokusuzdur, parfüm ya da esansiyel yağ alerjenleri içermez.",
    "caudalie-vinotherapist-lip-conditioner": "Üzüm çekirdeği, macadamia ve shea yağı içeren dudak nemlendiricisidir. Soğuk hava gibi çevresel faktörlere karşı dudakları korumayı ve onarmayı destekler. C10-18 trigliseritleri gibi komedojenik olabilecek maddeler içerir; koku profili ise limonen, linalool ve geraniol alerjenleri ile oluşturulmuştur.",
    "caudalie-vinotherapist-replenishing-vegan-body-butter": "Çok kuru ve atopiye eğilimli ciltlerde yoğun nem sağlamak üzere çöl hurması yağı, shea ve üzüm çekirdeği yağı ile formüle edilmiş vücut balmıdır. Formülün üst kısımlarındaki c10-18 trigliseritleri ve hexyldecyl stearat, sivilce oluşumuna yatkın bölgelerde dikkat gerektirir. Parfüm içerir.",
    "caudalie-vinotherapist-hyaluronic-nourishing-body-lotion": "Hyalüronik asit ve shea yağı ile formüle edilen, günlük kullanıma yönelik nemlendirici vücut losyonudur. Yağlı his bırakmadan cilde esneklik kazandırmayı amaçlar. Glyceryl stearate içerdiği için gözenek tıkayıcı potansiyeli bulunabilir. Limonen, linalool, sitral gibi parfüm alerjenleri barındırır.",
    "caudalie-the-des-vignes-hyaluronic-nourishing-body-lotion": "Beyaz misk, turunç ve zencefil notaları taşıyan hyalüronik asitli nemlendirici vücut kremidir. Cildin su tutma kapasitesini artırmayı hedefler. Fungal akneye yatkın ciltler için sorun olabilen glyceryl stearate maddesi içerir. Limonen ve linalool alerjenlerinin yanı sıra parfüm barındırır.",
    "caudalie-fleur-de-vigne-shower-gel": "Aloe vera özü ve bitkisel temizleyici maddeler içeren, sabunsuz formüllü duş jelidir. Karpuz, pembe biber ve beyaz gül koku notalarına sahiptir. İçeriğindeki sucrose cocoate bileşeni bazı ciltlerde komedojenik etki gösterebilir. Linalool ve sitronellol gibi AB uyarı listesindeki koku alerjenleri içerir.",
    "caudalie-the-des-vignes-shower-gel": "Beyaz misk, turunç ve zencefil kokularıyla zenginleştirilmiş temizleyici duş jelidir. Cildin bariyerine zarar vermeden kirleri uzaklaştırmayı amaçlar. Üst sıralardaki sucrose cocoate sivilceye eğilimli vücut bölgelerinde dikkatli kullanılmalıdır. Parfüm, limonen ve linalool alerjenleri bulunur.",
    "caudalie-rose-de-vigne-shower-gel": "Gül ve ışkın otu aromasıyla geliştirilmiş, aloe vera destekli vücut temizleyicisidir. Sabun içermeyen yapısıyla cildi kurutmadan arındırmaya yardımcı olur. Sucrose cocoate formülün ilk 7 maddesi arasında yer alır ve komedojenik olabilir. Hidroksisitronellal, sitronellol ve parfüm içerir.",
    "caudalie-eau-des-vignes-shower-gel": "Bergamot, iris ve beyaz misk notaları barındıran günlük banyo ürünüdür. Yüksek toleranslı sabunsuz yapısıyla tüm ciltleri yatıştırarak yıkamayı hedefler. Mantar aknesini tetikleme potansiyeli olan sucrose cocoate barındırır. Kumarin, geraniol, limonen alerjenleri mevcuttur.",
    "caudalie-vinoperfect-concentrated-brightening-glycolic-essence": "Leke karşıtı bakım öncesi cildi hazırlamak için formüle edilmiş, glikolik asit ve organik üzüm suyu barındıran sıvı toniktir. Cildi ölü hücrelerden nazikçe arındırmaya destek olur. Koku profili linalool, limonen ve parfüm gibi alerjen içeriklerden oluşur."
}

ingredients_update = {
    "hexyl-cinnamal": {
        "nameTr": "Heksil sinnamal",
        "description": "Kozmetik formüllerde ürünlere çiçeksi bir koku kazandırmak amacıyla kullanılır. AB regülasyonlarına göre ürün etiketinde özellikle belirtilmesi zorunlu olan koku alerjenleri listesindedir."
    },
    "hexyldecyl-stearate": {
        "nameTr": "Heksildesil stearat",
        "description": "Cilt bakım ürünlerinde cildi yumuşatmak ve nemin tutulmasına yardımcı olmak için kullanılan, sürülebilirliği artıran bir cilt bakım maddesi (emoliyan) ve yağ asidi esteridir."
    },
    "hydrogenated-jojoba-oil": {
        "nameTr": "Hidrojene jojoba yağı",
        "description": "Jojoba yağının hidrojenle doyurulmasıyla elde edilen katı formlu bir cilt bakım maddesidir. Genellikle peeling ürünlerinde cildi nazikçe arındırmak için fiziksel tanecikler olarak görev yapar."
    },
    "mel": {
        "nameTr": "Bal",
        "description": "Kozmetiklerde cildi yatıştırmak, yumuşatmak ve nemlendirmek için kullanılan doğal bir nem çekici (hümektan) ve cilt bakım bileşenidir."
    },
    "phospholipids": {
        "nameTr": "Fosfolipitler",
        "description": "Hücre zarlarının temel yapı taşı olan ve cildin doğal yapısıyla uyumlu, nemlendirici (emoliyan) özellikleri sayesinde cilt bariyerini güçlendirmeye yardımcı olan lipitlerdir."
    },
    "polyglyceryl-10-stearate": {
        "nameTr": "Poligliseril-10 stearat",
        "description": "Yağ ve su bazlı içeriklerin formül içinde homojen şekilde karışmasını sağlayan temizleyici ve emülgatör (yüzey aktif) maddedir."
    },
    "benzyl-benzoate": {
        "nameTr": "Benzil Benzoat",
        "description": "Formüllerde koku maddelerinin çözülmesini sağlayan ve koku verici özellikleri bulunan antimikrobiyal bir çözücüdür. AB'de etikette belirtilmesi gereken koku alerjenidir."
    },
    "salvia-officinalis-leaf-extract": {
        "nameTr": "Adaçayı Yaprağı Özü",
        "description": "Ciltte yatıştırıcı, ferahlatıcı ve sebum dengeleyici özellikleriyle bilinen, adaçayı yapraklarından elde edilen doğal bir cilt bakım özütüdür."
    },
    "potassium-alum": {
        "nameTr": "Potasyum Şapı",
        "description": "Cilt gözeneklerini sıkılaştırmak ve koku oluşumunu engellemek amacıyla kullanılan antimikrobiyal, büzücü (astrenjan) özellikli bir mineral tuzdur."
    },
    "commiphora-myrrha-resin-extract": {
        "nameTr": "Mür Ağacı Reçinesi Özü",
        "description": "Mür ağacının reçinesinden elde edilen, cildi yatıştırma ve ürüne karakteristik odunsu bir koku sağlama işlevleri bulunan doğal bir bitki özütüdür."
    },
    "styrax-tonkinensis-resin-extract": {
        "nameTr": "Sığla Reçinesi Özü",
        "description": "Aselbent ağacı reçinesinden elde edilen, cildi koruma özelliğine sahip ve formülasyonlara hafif vanilyamsı koku veren bir maddedir."
    },
    "citrus-aurantium-amara-flower-oil": {
        "nameTr": "Acı Portakal Çiçeği Yağı",
        "description": "Neroli olarak da bilinen, ürüne parfüm etkisi katan uçucu yağdır. Cilt onarıcı işlevleri bulunsa da, içerdiği alerjenler nedeniyle hassas ciltleri tahriş edebilir."
    },
    "rosa-damascena-flower-oil": {
        "nameTr": "Şam Gülü Yağı",
        "description": "Gül çiçeklerinden damıtılarak elde edilen, ürüne yoğun gül kokusu veren esansiyel bir yağdır. Cildi nemlendirme işlevi bulunmakla birlikte koku alerjenleri içerir."
    },
    "vitis-vinifera-fruit-extract": {
        "nameTr": "Üzüm Meyvesi Özü",
        "description": "Antioksidan polifenoller açısından zengin olan üzüm özütü, cildi serbest radikallerin çevresel zararlarına karşı desteklemek için formüllere eklenir."
    },
    "farnesol": {
        "nameTr": "Farnesol",
        "description": "Doğada birçok esansiyel yağın içinde bulunan antibakteriyel bir koku maddesidir. AB standartlarına göre etikette ayrıca belirtilmesi zorunlu koku alerjenleri arasında yer alır."
    },
    "nitrogen": {
        "nameTr": "Azot (Nitrojen)",
        "description": "Sprey ve aerosol ürünlerin sıkıldığında dışarı itilmesini sağlayan itici (propellant) bir gazdır. Formülün havayla temas edip bozulmasını engeller."
    },
    "salix-alba-bark-extract": {
        "nameTr": "Ak Söğüt Kabuğu Özü",
        "description": "Doğal salisilik asit türevleri (salisin) içeren, cilt yüzeyini pürüzsüzleştirmeye ve gözenek görünümünü arındırmaya yardımcı büzücü bir cilt bakım ekstraktıdır."
    },
    "polyglyceryl-6-laurate": {
        "nameTr": "Poligliseril-6 laurat",
        "description": "Su ve yağ fazlarının ayrışmasını önlemek için formüllere katılan, temizleme özelliğine de sahip olan bitkisel kökenli bir emülgatördür."
    },
    "paeonia-lactiflora-root-extract": {
        "nameTr": "Şakayık Kökü Özü",
        "description": "Ciltteki ton eşitsizliklerini hedef alarak aydınlık bir görünüm sağlamaya yardımcı olan ve antioksidan (cilt koruyucu) işlevi bulunan bir bitki özütüdür."
    },
    "polyglycerin-6": {
        "nameTr": "Poligliserin-6",
        "description": "Gliserinin polimerik hali olan bu nem çekici (hümektan) madde, su moleküllerini cilde bağlayarak yoğun nemlendirme ve yumuşatma işlevi sunar."
    },
    "acer-saccharum-extract": {
        "nameTr": "Şeker Akçaağacı Özü",
        "description": "İçerdiği doğal malik asit ve tartarik asit bileşenleri sayesinde cildi nazikçe eksfoliye etmeye ve cilt yenilenmesini desteklemeye yardımcı olan bitkisel özüttür."
    },
    "papain": {
        "nameTr": "Papain Enzimi",
        "description": "Papaya meyvesinden elde edilen doğal bir enzimdir. Cildin en üst katmanındaki ölü hücre bağlarını çözerek peeling (arındırma) işlemi yapar."
    },
    "hydroxycitronellal": {
        "nameTr": "Hidroksisitronellal",
        "description": "Kozmetik formüllerde ürünlere tatlı, çiçeksi koku vermek için kullanılan sentetik bir maddedir. AB kuralları gereği etikette yazılması zorunlu koku alerjenleri listesindedir."
    },
    "phenylpropanol": {
        "nameTr": "Fenilpropanol",
        "description": "Çiçeksi koku profiline sahip bir solvent ve koku maskeleyici olmasının yanı sıra, formülün mikrobiyal bozulmasını geciktiren antimikrobiyal bir bileşendir."
    }
}

with open('scripts/skincare/staging/caudalie/texts.json', 'r', encoding='utf-8') as f:
    texts_data = json.load(f)

for slug, desc in products_update.items():
    texts_data['products'][slug] = desc

for slug, data in ingredients_update.items():
    texts_data['ingredients'][slug] = data

with open('scripts/skincare/staging/caudalie/texts.json', 'w', encoding='utf-8') as f:
    json.dump(texts_data, f, ensure_ascii=False, indent=2)

print("Batch 1 (manual descriptions) applied.")
