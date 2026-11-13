from generate_texts_draft import draft_texts
import json

batch_3_updates = {
    "caudalie-vinoperfect-dark-spot-correcting-hand-cream": "Avokado yağı, shea yağı ve asma çubuğu özü (Viniferine) ile formüle edilen el bakım kremidir. Elleri nemlendirirken yaşlanma veya güneşe bağlı oluşan koyu leke görünümünü hafifletmeyi hedefler.",
    "caudalie-vinoperfect-instant-brightening-moisturizer": "Niasinamid ve Viniferine bileşenleriyle geliştirilen günlük nemlendiricidir. Cildin doğal ışıltısını artırmayı, cilt tonunu eşitlemeyi ve leke görünümünü dengelemeyi amaçlar.",
    "caudalie-vinoperfect-dark-spot-correcting-glycolic-night-cream": "Glikolik asit, asma çubuğu özü ve papaya enzimi içeren gece bakım kremidir. Gece boyunca cildi nazikçe ölü hücrelerden arındırarak daha pürüzsüz ve aydınlık bir görünüme kavuşmasına yardımcı olur.",
    "caudalie-vinopure-moisturizing-mattifying-fluid": "Organik gül suyu ve polifenoller içeren, yağlı ve karma ciltler için geliştirilen nemlendiricidir. Formülündeki silika tozu sayesinde gün içinde ciltteki sebum fazlasını emerek parlama görünümünü kontrol altına almayı hedefler.",
    "caudalie-vinopure-salicylic-spot-solution": "Doğal salisilik asit, niasinamid ve çay ağacı uçucu yağı içeren bölgesel bakım kremidir. Akneli veya akneye eğilimli bölgelere lokal olarak uygulanır, kurutmaya ve görünümünü hafifletmeye yardımcı olur.",
    "caudalie-vinopure-purifying-gel-cleanser": "Doğal salisilik asit içeren, cildi derinlemesine temizlemeyi amaçlayan yıkama jelidir. Gözenekleri arındırmaya, fazla sebumu dengelemeye ve cilt dokusunu pürüzsüzleştirmeye destek sağlar.",
    "caudalie-vinotherapist-tinted-lip-balm": "Üzüm çekirdeği yağı, macadamia yağı ve shea yağı ile formüle edilen renkli dudak nemlendiricisidir. Dudakları çevresel etkenlere karşı koruyup beslerken, hafif ve doğal bir renk tonu kazandırmaya yardımcı olur.",
    "caudalie-resveratrol-lift-firming-cashmere-body-cream": "Resveratrol, hyalüronik asit ve vegan kolajen alternatifi içeren sıkılaştırıcı vücut kremidir. Kaşmir dokusuyla cildi yoğun şekilde beslerken elastikiyet kaybını dengelemeyi ve cildi sıkılaştırmayı hedefler.",
    "caudalie-vinoclean-moisturizing-toner": "Organik gül suyu ve Vinolevure (üzüm mayası özü) içeren, alkolsüz formüle sahip nemlendirici toniktir. Cildi nazikçe arındırmayı, makyaj kalıntılarını uzaklaştırmayı ve cilt bariyerini yatıştırarak nemlendirmeyi amaçlar.",
    "caudalie-vinoclean-micellar-cleansing-water": "Papatya özü ve organik üzüm suyu ile zenginleştirilmiş misel sudur. Yüz ve göz makyajını cildi ovalamaya gerek kalmadan, nazikçe temizlemeyi ve cildi yatıştırmayı hedefler.",
    "caudalie-vinoclean-cleansing-almond-milk": "Tatlı badem yağı ve peygamber çiçeği (cornflower) özü içeren makyaj temizleme sütüdür. Hassas ciltleri kurutmadan yüz ve göz makyajını arındırmaya, cildi besleyip yumuşatmaya yardımcı olur.",
    "caudalie-vinoclean-makeup-removing-cleansing-oil": "Tatlı badem, hint ve üzüm çekirdeği yağları karışımından oluşan temizleme yağıdır. Suya dayanıklı makyajı bile cilt bariyerini bozmadan çözerek temizlemeyi ve cildi beslemeyi hedefler.",
    "caudalie-resveratrol-lift-instant-firming-serum": "Hyalüronik asit, resveratrol ve vegan kolajen içeriğiyle formüle edilen konsantre bakım serumudur. Ciltteki ince çizgi ve kırışıklık görünümünü hafifletmeyi, yüz ovalini toparlamaya ve sıkılaştırmaya yardımcı olur.",
    "caudalie-resveratrol-lift-firming-cashmere-cream": "Kaşmir hissi veren yumuşak dokusuyla geliştirilen, resveratrol ve vegan kolajen içerikli yaşlanma karşıtı gündüz kremidir. Cildi beslerken elastikiyetini artırmayı ve daha sıkı bir görünüm sağlamayı amaçlar.",
    "caudalie-resveratrol-lift-firming-eye-gel-cream": "Kinoa özü, biopolimerler ve sıkılaştırıcı aktifler (resveratrol, vegan kolajen) içeren jel formlu göz bakım kremidir. Göz çevresindeki yorgunluk belirtilerini, şişkinliği ve ince çizgileri hafifletmeyi hedefler."
}

with open('scripts/skincare/staging/caudalie/texts.json', 'r', encoding='utf-8') as f:
    texts_data = json.load(f)

for slug, desc in batch_3_updates.items():
    warnings = draft_texts.get(slug, "").replace('Fonksiyonel açıklama.', '').strip()
    full_desc = desc + (" " + warnings if warnings else "")
    texts_data['products'][slug] = full_desc.strip()

with open('scripts/skincare/staging/caudalie/texts.json', 'w', encoding='utf-8') as f:
    json.dump(texts_data, f, ensure_ascii=False, indent=2)

print("Batch 3 texts updated.")
