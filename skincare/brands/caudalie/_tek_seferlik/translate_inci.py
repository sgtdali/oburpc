import json
import re

with open('scripts/skincare/staging/caudalie/texts.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Common Turkish translations
tr_map = {
    'oil': 'Yağı',
    'extract': 'Özü',
    'acid': 'Asidi',
    'water': 'Suyu',
    'seed': 'Çekirdeği',
    'leaf': 'Yaprağı',
    'flower': 'Çiçeği',
    'root': 'Kökü',
    'fruit': 'Meyvesi',
    'peel': 'Kabuğu',
    'bark': 'Kabuğu',
    'butter': 'Yağı',
    'juice': 'Suyu',
    'powder': 'Tozu',
    'wax': 'Mumu',
    'cera': 'Mumu'
}

allergens = ['amyl-cinnamal', 'benzyl-alcohol', 'cinnamyl-alcohol', 'citral', 'eugenol', 'hydroxycitronellal', 'isoeugenol', 'amylcinnamyl-alcohol', 'benzyl-salicylate', 'cinnamal', 'coumarin', 'geraniol', 'hydroxyisohexyl-3-cyclohexene-carboxaldehyde', 'anisyl-alcohol', 'benzyl-cinnamate', 'farnesol', 'butylphenyl-methylpropional', 'linalool', 'benzyl-benzoate', 'citronellol', 'hexyl-cinnamal', 'limonene', 'methyl-2-octynoate', 'alpha-isomethyl-ionone', 'evernia-prunastri-extract', 'evernia-furfuracea-extract']

def translate_inci(slug):
    # Special cases
    if slug == 'mel': return 'Bal'
    if slug == 'phospholipids': return 'Fosfolipitler'
    if slug == 'tin-oxide': return 'Kalay Oksit'
    if slug == 'calcium-citrate': return 'Kalsiyum Sitrat'
    if slug == 'ci-15850': return 'CI 15850'
    if slug == 'c12-16-alcohols': return 'C12-16 Alkolleri'
    if slug == 'nitrogen': return 'Azot (Nitrojen)'
    
    parts = slug.split('-')
    res = []
    for p in parts:
        if p in tr_map:
            res.append(tr_map[p])
        else:
            # phonetic translations
            p = p.replace('polyglyceryl', 'poligliseril')
            p = p.replace('stearate', 'stearat')
            p = p.replace('laurate', 'laurat')
            p = p.replace('myristate', 'miristat')
            p = p.replace('palmitate', 'palmitat')
            p = p.replace('acetate', 'asetat')
            p = p.replace('cinnamal', 'sinnamal')
            p = p.replace('hexyldecyl', 'heksildesil')
            p = p.replace('copolymer', 'kopolimer')
            p = p.replace('sodium', 'sodyum')
            p = p.replace('potassium', 'potasyum')
            p = p.replace('calcium', 'kalsiyum')
            p = p.replace('chloride', 'klorür')
            p = p.replace('oxide', 'oksit')
            p = p.replace('hyaluronate', 'hiyalüronat')
            p = p.replace('glycerin', 'gliserin')
            p = p.replace('alcohol', 'alkol')
            
            res.append(p.capitalize())
            
    return " ".join(res)

for k, v in data['ingredients'].items():
    v['nameTr'] = translate_inci(k)
    
    if k in allergens:
        if 'AB\'de etikette' not in v['description']:
            v['description'] = "Kozmetik formüllerde koku verici olarak kullanılan bir bileşendir. AB kozmetik regülasyonlarına göre etikette belirtilmesi gereken koku alerjenleri listesinde yer alır."

with open('scripts/skincare/staging/caudalie/texts.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Ingredient nameTr translated and allergens updated.")
