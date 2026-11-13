from generate_texts_draft import draft_texts

batch_2_updates = {
    "caudalie-vinoperfect-illuminating-micropeel-cleansing-foam": "AHA (Mandelik asit) ve organik üzüm suyu ile zenginleştirilmiş formülüyle cildi ölü hücrelerden arındırmayı amaçlayan köpük formlu temizleyicidir. Günlük kullanımla cildin daha aydınlık ve pürüzsüz bir görünüm kazanmasına yardımcı olur.",
    "caudalie-vinoperfect-complexion-correcting-radiance-serum": "Asma çubuğundan elde edilen patentli Viniferine bileşeni içeren leke karşıtı bakım serumudur. Güneş, yaşlanma ve akne izleri gibi farklı kaynaklı leke görünümlerini hafifletmeye ve cilt tonunu eşitlemeye destek olur.",
    "caudalie-vinotherapist-overnight-detox-oil": "Üzüm çekirdeği, badem, lavanta ve biberiye gibi bitkisel ve uçucu yağlardan oluşan %100 doğal türevli içeriklerle formüle edilmiştir. Gece boyunca cildi beslemeyi, serbest radikallerin etkilerine karşı korumayı ve yorgun görünümü hafifletmeyi hedefler.",
    "caudalie-vinoclean-instant-detox-mask": "İçeriğindeki pembe kil ve kahve çekirdeği özü ile formüle edilen, ciltteki kir ve fazla sebumu arındırmayı hedefleyen bakım maskesidir. Beş dakikalık kullanımda gözenek görünümünü sıkılaştırmaya ve cilt dokusunu pürüzsüzleştirmeye yardımcı olur.",
    "caudalie-vinohydra-sos-intense-moisturizing-cream": "Hiyalüronik asit ve hodan (borage) yağı içeren, özellikle kuru ciltlerin nem ihtiyacını karşılamayı amaçlayan yoğun bakım kremidir. Cildin bariyerini destekleyerek nemin korunmasına ve kuruluktan kaynaklanan gerginlik hissinin azalmasına yardımcı olur.",
    "caudalie-vinohydra-moisturizing-mask": "Organik üzüm suyu ve asiatica (Centella asiatica) özü içeren, cilde yoğun nem desteği sunmayı hedefleyen maskedir. Cildi yatıştırarak nem bariyerini güçlendirmeye ve esneklik kazandırmaya destek sağlar.",
    "caudalie-vinohydra-moisturizing-sorbet": "Papatya özü ve shea yağı barındıran, su bazlı ve hafif dokulu nemlendirici kremdir. Hassasiyete eğilimli ciltleri yatıştırmayı ve anında nemlendirmeyi hedefler. Ciltte yağlı his bırakmadan hızla emilir.",
    "caudalie-vinohydra-grape-water-gel-moisturizer": "Organik üzüm suyu ve aloe vera özü içeren jel formlu günlük nemlendirici kremdir. Hafif yapısıyla cildi ağırlık yapmadan nemlendirmeye ve canlandırmaya yardımcı olur. Yağlı bir his bırakmaz.",
    "caudalie-ange-des-vignes-shower-gel": "Sabun içermeyen nazik formülüyle cildi kurutmadan temizlemeyi hedefleyen vücut yıkama jelidir. Neroli (acı portakal çiçeği) ve ahududu notalarından oluşan meyvemsi kokusuyla banyo rutinine eşlik eder.",
    "caudalie-moisturizing-oil-elixir": "Argan yağı ve incir çekirdeği yağı gibi bitkisel yağlar içeren, hem vücut hem de yüz ve saç için kullanılabilen kuru yağdır. Besleyici formülüyle cildi ve saçları yumuşatmayı, kuruluktan korumayı hedefler.",
    "caudalie-resveratrol-lift-lightweight-firming-cashmere-cream": "Resveratrol, hiyalüronik asit ve vegan kolajen güçlendirici içeren hafif dokulu gündüz kremidir. Ciltteki kırışıklık görünümünü hafifletmeyi ve sıkılık kaybını dengelemeye destek olur. Yağlı cilt yapısına uygun olarak tasarlanmıştır.",
    "caudalie-premier-cru-the-eye-cream": "Patentli TET8 teknolojisi ve asma çubuğu özü (Viniferine) ile geliştirilmiş, göz çevresindeki koyu halka ve kırışıklık görünümünü hafifletmeyi hedefleyen bakım kremidir. Özel masaj ucu ile uygulanarak yorgunluk belirtilerini azaltmaya destek olur.",
    "caudalie-premier-cru-the-serum": "Hyalüronik asit ve niasinamid ile zenginleştirilmiş, yaşlanma belirtilerine karşı kapsamlı bakım sunmayı amaçlayan konsantre serumdur. Cildi sıkılaştırmaya, nemlendirmeye ve daha aydınlık bir görünüme kavuşmasına yardımcı olur.",
    "caudalie-premier-cru-the-cream": "Hyalüronik asit, Viniferine ve TET8 teknolojisi içeren çok yönlü bir yaşlanma karşıtı gündüz kremidir. Düzenli kullanımla cildi beslemeyi, kırışıklık ve leke görünümünü dengelemeyi destekler.",
    "caudalie-premier-cru-the-rich-cream": "Shea yağı ve bitkisel seramidlerle formüle edilmiş, özellikle kuru cilt tipleri için geliştirilmiş yoğun yaşlanma karşıtı kremdir. Kapsamlı yaşlanma belirtileriyle mücadele ederken cildin nem bariyerini onarmaya yardımcı olur."
}

import json

with open('scripts/skincare/staging/caudalie/texts.json', 'r', encoding='utf-8') as f:
    texts_data = json.load(f)

for slug, desc in batch_2_updates.items():
    # draft_texts used the old slug for detox oil
    draft_slug = slug
    if slug == "caudalie-vinotherapist-overnight-detox-oil":
        draft_slug = "caudalie-vinoterapist-overnight-detox-oil"
        
    warnings = draft_texts.get(draft_slug, "").replace('Fonksiyonel açıklama.', '').strip()
    full_desc = desc + (" " + warnings if warnings else "")
    texts_data['products'][slug] = full_desc.strip()

with open('scripts/skincare/staging/caudalie/texts.json', 'w', encoding='utf-8') as f:
    json.dump(texts_data, f, ensure_ascii=False, indent=2)

print("Batch 2 texts updated.")
