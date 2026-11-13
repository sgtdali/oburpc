import re
import json

with open('summary_caudalie.txt', 'r', encoding='utf-16') as f:
    summary_text = f.read()

products_data = {}
blocks = re.split(r'\n## ', '\n' + summary_text)[1:]

for block in blocks:
    lines = block.strip().split('\n')
    header = lines[0].split(' | ')
    slug = header[0]
    name_tr = header[1]
    
    inci = ""
    icerir = {}
    icermez = []
    aktif = []
    
    for line in lines[1:]:
        if line.startswith('INCI: '):
            inci = line.replace('INCI: ', '')
        elif line.startswith('İÇERİR: '):
            try:
                icerir_str = line.replace('İÇERİR: ', '')
                # Eval is safe here since we generated this file
                icerir = dict(eval(icerir_str))
            except:
                pass
    
    warnings = []
    if 'alcohol' in icerir:
        warnings.append("Formülünde alkol bulunur.")
    if 'fragrance' in icerir:
        warnings.append("İçeriğinde parfüm ve koku veren bileşenler yer almaktadır.")
    if 'allergen' in icerir:
        allergens = ", ".join(icerir['allergen'])
        warnings.append(f"Avrupa Birliği kozmetik regülasyonuna göre etikette belirtilmesi gereken {allergens} gibi koku alerjenleri barındırır.")
    
    # Check if a comedogenic ingredient is in the first 7
    inci_list = [x.strip() for x in inci.split(',')]
    fungal_acne_triggers = icerir.get('fungal', [])
    first_7 = [x.lower().replace(' ', '-') for x in inci_list[:7]]
    early_triggers = [t for t in fungal_acne_triggers if t in first_7]
    if early_triggers:
        warnings.append(f"Listenin başlarında komedojenik/mantar aknesi tetikleyici olabilecek bileşenler ({', '.join(early_triggers)}) bulunmaktadır.")
        
    products_data[slug] = {
        'warnings': " ".join(warnings)
    }

with open('generate_texts_draft.py', 'w', encoding='utf-8') as f:
    f.write("draft_texts = {\n")
    for slug, data in products_data.items():
        f.write(f'    "{slug}": "Fonksiyonel açıklama. {data["warnings"]}",\n')
    f.write("}\n")
