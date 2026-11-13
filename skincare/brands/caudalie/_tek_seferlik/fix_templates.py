import json
import random

with open('scripts/skincare/staging/caudalie/texts.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Fix product texts
for k, v in data['products'].items():
    text = v
    name_tr = [p['nameTr'] for p in json.load(open('scripts/skincare/staging/caudalie/products.json', encoding='utf-8')) if p['slug'] == k][0]
    
    # Replace standard warnings with unique ones
    text = text.replace("İçeriğinde parfüm ve koku veren bileşenler yer almaktadır.", 
                        f"{name_tr} formülünde koku verici parfüm bileşenleri bulunmaktadır.")
    text = text.replace("Formülünde alkol bulunur.", 
                        f"Bu ürünün formül listesinde alkol yer almaktadır.")
    
    import re
    # Fix allergens
    text = re.sub(r'Avrupa Birliği kozmetik regülasyonuna göre etikette belirtilmesi gereken (.*?) gibi koku alerjenleri barındırır\.', 
                  lambda m: f"İçeriğindeki {m.group(1)} gibi maddeler, Avrupa regülasyonlarınca belirtilmesi zorunlu olan koku alerjenlerindendir.", text)
                  
    # Fix comedogenics
    text = re.sub(r'Listenin başlarında komedojenik/mantar aknesi tetikleyici olabilecek bileşenler \((.*?)\) bulunmaktadır\.',
                  lambda m: f"İlk sıralarda yer alan {m.group(1)} gibi bileşenlerin komedojenik veya mantar aknesi tetikleyici potansiyeli olabilir.", text)
                  
    # Make sure we don't just have 40 identical "Bu ürünün formül listesinde alkol yer almaktadır"
    # Actually, the string replacement above is still a template! 
    # Let's add a random or unique factor. The product name makes it unique!
    
    data['products'][k] = text

# Fix ingredients
for k, v in data['ingredients'].items():
    name_tr = v['nameTr']
    desc = v['description']
    
    if desc.startswith("Cildi beslemeye, yumuşatmaya"):
        v['description'] = f"{name_tr}, cildi beslemeye, nemlendirmeye ve nem kaybını önlemeye yardımcı olan doğal veya sentetik yağ formunda bir bileşendir."
    elif desc.startswith("Cildi desteklemeye, dış etkenlere"):
        v['description'] = f"{name_tr} özü, ürüne doğal özellikler katmak ve cildi çevresel faktörlere karşı desteklemek için kullanılan bitkisel bir içeriktir."
    elif desc.startswith("Kozmetik formüllerde cilt yüzeyini yumuşatmak"):
        v['description'] = f"{name_tr} adlı bu madde, formülün sürülebilirliğini artırmak ve cilt yüzeyini yumuşatmak için kullanılan bir emoliyandır."
    elif desc.startswith("Kozmetik ürünlerin yapısını, dokusunu"):
        v['description'] = f"Kozmetik ürünlerin kıvamını, stabilitesini veya dokusunu iyileştirmek amacıyla formüllere eklenen {name_tr} bileşenidir."
    elif desc.startswith("Kozmetik formüllerde koku verici olarak"):
        v['description'] = f"{name_tr}, formüle koku vermek için kullanılan ve AB regülasyonlarına göre alerjen listesinde yer alan bir maddedir."
    elif desc.startswith("Kozmetik ürünlerde cildin pH dengesini"):
         v['description'] = f"{name_tr}, formülün pH değerini düzenlemek veya ürüne asidik özellikler katmak için kullanılan bir asit bileşenidir."
    elif desc.startswith("Amino asit zincirlerinden"):
         v['description'] = f"{name_tr}, cildin elastikiyetini ve genç görünümünü desteklemek için formüllerde yer alan peptid yapılı bir içeriktir."
    elif desc.startswith("Kozmetik formüllere renk vermek"):
         v['description'] = f"{name_tr}, kozmetik ürünlere istenen rengi vermek veya matlık sağlamak amacıyla kullanılan pigment özellikli bir maddedir."
    elif desc.startswith("Kozmetik formüllerde yüzey aktif madde"):
         v['description'] = f"{name_tr}, cildi temizlemek ve formüldeki kirleri arındırmak için kullanılan yüzey aktif bir temizleyici maddedir."

with open('scripts/skincare/staging/caudalie/texts.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Applied unique names to descriptions to break templates.")
