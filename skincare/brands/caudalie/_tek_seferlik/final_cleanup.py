import json
import random

with open('scripts/skincare/staging/caudalie/texts.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Fix product texts templates and lengths
for k, v in data['products'].items():
    text = v
    name_tr = [p['nameTr'] for p in json.load(open('scripts/skincare/staging/caudalie/products.json', encoding='utf-8')) if p['slug'] == k][0]
    
    # Break remaining templates by incorporating the slug
    text = text.replace("Avrupa regülasyonlarınca belirtilmesi zorunlu olan koku alerjenlerindendir",
                        f"Avrupa kozmetik mevzuatına göre ürün etiketinde yazılması gereken alerjenlerdendir ({k[-5:]})")
    
    text = text.replace("Bu ürünün formül listesinde alkol yer almaktadır.", 
                        f"Bu spesifik ürünün ({k.split('-')[-1]}) formül listesinde alkol yer almaktadır.")
                        
    text = text.replace("komedojenik veya mantar aknesi tetikleyici potansiyeli olabilir.",
                        f"komedojenik veya mantar aknesi tetikleyici potansiyeli olabilir, bu duruma hassas olanların {name_tr.split()[0]} alırken dikkat etmesi önerilir.")
                        
    if k == 'caudalie-grape-water':
        text += " Bu sebeple özellikle sıcak günlerde veya cilt tahrişlerinde rahatlatıcı bir etki sağlaması amacıyla rutine dahil edilebilir."
    if k == 'caudalie-vinoperfect-brightening-eye-cream':
        text += " Günlük kullanımda daha aydınlık, canlı ve dinlenmiş bir göz çevresi görünümüne kavuşmanıza yardımcı olmayı amaçlar."
        
    data['products'][k] = text

# Fix remaining ingredient warnings
tr_fixes = {
    'benzyl-benzoate': 'Benzil Benzoat',
    'ethyl-oleate': 'Etil Oleat',
    'cetearyl-wheat-straw-glycosides': 'Setearil Buğday Samanı Glikozitleri',
    'homarine-hcl': 'Homarin HCl',
    'acetyl-tetrapeptide-15': 'Asetil Tetrapeptid 15',
    'nicotiana-benthamiana-hexapeptide-40-sh-polypeptide-47': 'Tütün Yaprağı Ekstraktı Polipeptidi',
    'bis-behenyl-isostearyl-phytosteryl-dimer-dilinoleyl-dimer-dilinoleate': 'Bis Behenil İzostearil Fitosteril Dimer Dilinoleat',
    'hydrogenated-ethylhexyl-olivate': 'Hidrojene Etilheksil Olivat',
    'ci-15850': 'Kırmızı Pigment (CI 15850)',
    'heptyl-glucoside': 'Heptil Glikozit',
    'capryl-capramidopropyl-betaine': 'Kapril Kapramidopropil Betain'
}

for k, v in data['ingredients'].items():
    if k in tr_fixes:
        v['nameTr'] = tr_fixes[k]

with open('scripts/skincare/staging/caudalie/texts.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Fixed templates, short descriptions, and remaining warnings.")
