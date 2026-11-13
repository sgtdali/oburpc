from generate_drafts import draft_texts

batch_1_updates = {
    "caudalie-vinoclean-gentle-buffing-cream": "Cilt yüzeyindeki ölü hücreleri arındırmayı hedefleyen fiziksel peeling ürünüdür. Formülünde üzüm çekirdeği yağı ve bal özü bulunur. Cildi temizlerken nem dengesini korumaya destek olur.",
    "caudalie-vinoclean-instant-foaming-cleanser": "Papatya ve adaçayı özleri içeren, cildi günlük kirden arındırmayı amaçlayan köpük formlu yüz yıkama ürünüdür. Sabun içermeyen yapısıyla cildin pH dengesini korumaya yardımcı olur. Üzüm suyu ile cildi yatıştırmayı destekler.",
    "caudalie-beauty-elixir": "Gül, nane ve biberiye uçucu yağları içeren sprey formlu toniktir. Cildi ferahlatmaya ve gözenek görünümünü sıkılaştırmaya yardımcı olur. Makyaj öncesinde veya gün içinde cildi tazelemek amacıyla kullanılabilir.",
    "caudalie-grape-water": "Sadece organik üzüm suyu ile formüle edilmiş yüz spreyidir. Hassasiyete eğilimli ciltleri yatıştırmayı ve nemlendirmeyi hedefler. Polifenol içeriğiyle antioksidan destek sağlar.",
    "caudalie-vinoperfect-glycolic-peel-mask": "Glikolik asit ve meyve asitleri (AHA) içeren, on dakikada cildi ölü hücrelerden arındırmayı hedefleyen maskedir. Asma çubuğu özü (Viniferine) ile leke görünümünü hafifletmeye yardımcı olur. Cilt tonu eşitsizliklerini dengelemeye destek sağlar.",
    "caudalie-vinoperfect-brightening-eye-cream": "Asma çubuğu özü (Viniferine), niasinamid ve kafein içeren göz bakım kremidir. Göz altı morluklarının görünümünü hafifletmeyi hedefler. Seramik aplikatörü ile masaj yaparak uygulanır.",
    "caudalie-vinotherapist-lip-conditioner": "Üzüm çekirdeği yağı, macadamia yağı ve shea yağı ile formüle edilen dudak bakım kremi. Dudakları nemlendirmeye ve çevresel faktörlerin kurutucu etkilerine karşı korumaya yardımcı olur.",
    "caudalie-vinotherapist-replenishing-vegan-body-butter": "Çöl hurması yağı, üzüm çekirdeği yağı ve shea yağı içeren vücut balmı. Çok kuru ve atopiye eğilimli ciltlerde nemlendirme ve kaşıntı hissini yatıştırma sağlamayı hedefler. Kuru cilt bariyerini destekler.",
    "caudalie-vinotherapist-hyaluronic-nourishing-body-lotion": "Hyalüronik asit ve shea yağı içeren, günlük kullanıma uygun vücut losyonu. Cildin nem ihtiyacını karşılamayı ve esneklik kazandırmayı hedefler. Yağlı his bırakmadan cilt tarafından emilir.",
    "caudalie-the-des-vignes-hyaluronic-nourishing-body-lotion": "Hyalüronik asit ile zenginleştirilmiş vücut losyonudur. Cildi nemlendirmeyi hedeflerken aynı zamanda beyaz misk, turunç ve zencefil notalarına sahip Thé des Vignes kokusuyla sarmalar.",
    "caudalie-fleur-de-vigne-shower-gel": "Aloe vera özü ve bitkisel temizleyiciler içeren duş jelidir. Sabun içermeyen yapısıyla cildin nem bariyerini koruyarak temizlemeye yardımcı olur. Karpuz, pembe biber ve beyaz gül notaları içerir.",
    "caudalie-the-des-vignes-shower-gel": "Sabun içermeyen formülüyle cildi kurutmadan temizlemeyi hedefleyen duş jelidir. Beyaz misk, turunç ve zencefil notaları içeren parfümü bulunur.",
    "caudalie-rose-de-vigne-shower-gel": "Gül, ışkın otu ve beyaz misk notaları içeren nazik duş jelidir. Aloe vera ekstresiyle zenginleştirilmiş sabunsuz formülü ile günlük vücut temizliği sağlar.",
    "caudalie-eau-des-vignes-shower-gel": "Bergamot, iris ve beyaz misk notaları barındıran günlük duş jelidir. Yüksek toleranslı sabunsuz formülü ile cildi kurutmadan arındırmayı amaçlar.",
    "caudalie-vinoperfect-concentrated-brightening-glycolic-essence": "Glikolik asit, şakayık kökü özü ve üzüm suyu içeren likit toniktir. Cildi ölü hücrelerden arındırıp aydınlık bir görünüme hazırlamayı hedefler. Leke karşıtı bakım ritüelinin ilk adımı olarak kullanılır."
}

import json

with open('scripts/skincare/staging/caudalie/texts.json', 'r', encoding='utf-8') as f:
    texts_data = json.load(f)

for slug, desc in batch_1_updates.items():
    full_desc = desc + " " + draft_texts[slug].replace('Fonksiyonel açıklama. ', '')
    texts_data['products'][slug] = full_desc.strip()

with open('scripts/skincare/staging/caudalie/texts.json', 'w', encoding='utf-8') as f:
    json.dump(texts_data, f, ensure_ascii=False, indent=2)

print("Batch 1 texts updated.")
