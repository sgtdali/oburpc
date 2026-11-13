import json

with open('scripts/skincare/staging/caudalie/texts.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for k, v in data['ingredients'].items():
    desc = v['description']
    if desc == 'Kozmetik formüllerde kullanılan bir bileşendir.':
        # Assign a better description
        if 'oil' in k or 'butter' in k:
            v['description'] = "Cildi beslemeye, yumuşatmaya ve nemin buharlaşmasını önleyerek cilt bariyerini desteklemeye yardımcı olan bir yağ bileşenidir."
        elif 'extract' in k:
            v['description'] = "Cildi desteklemeye, dış etkenlere karşı korumaya veya formüle doğal özellikler katmaya yardımcı bitkisel kaynaklı bir özüttür."
        elif 'stearate' in k or 'laurate' in k or 'myristate' in k or 'palmitate' in k or 'isostearate' in k:
            v['description'] = "Kozmetik formüllerde cilt yüzeyini yumuşatmak, nemi hapsetmek ve ürünün sürülebilirliğini (emoliyan) artırmak amacıyla kullanılan bir bileşendir."
        elif 'copolymer' in k or 'crosspolymer' in k:
            v['description'] = "Ürünün cilt üzerinde homojen dağılmasını, doku kazanmasını ve kıvam almasını sağlamak için formüllere eklenen polimerik bir içeriktir."
        elif 'acid' in k:
            v['description'] = "Kozmetik ürünlerde cildin pH dengesini ayarlamak, formülü stabilize etmek veya içeriğine göre yenileyici özellikler sunmak amacıyla kullanılan asidik bir maddedir."
        elif 'glucoside' in k or 'betaine' in k:
            v['description'] = "Kozmetik formüllerde yüzey aktif madde (temizleyici) olarak görev yapan, kir ve yağın ciltten uzaklaştırılmasına yardımcı olan bir bileşendir."
        elif 'cera' in k or 'wax' in k:
            v['description'] = "Ürünlere yapı, kıvam ve koruyucu özellikler kazandırmak için formüllere eklenen mumsu bir bileşendir."
        elif 'peptide' in k:
            v['description'] = "Amino asit zincirlerinden oluşan, cildin sıkılığını ve pürüzsüz görünümünü desteklemek amacıyla formüllerde kullanılan bir bileşendir."
        elif 'oxide' in k or 'ci-' in k:
            v['description'] = "Kozmetik formüllere renk vermek veya görünümü matlaştırmak amacıyla kullanılan bir renklendirici/pigment bileşenidir."
        elif 'alcohol' in k and k != 'alcohol':
            v['description'] = "Formüllerde emoliyan (yumuşatıcı) ve kıvam artırıcı olarak görev yapan, cildi kurutmayan yağ alkolü yapısında bir bileşendir."
        else:
            v['description'] = "Kozmetik ürünlerin yapısını, dokusunu veya cilt üzerindeki hissini iyileştirmek amacıyla formüllere dahil edilen bir içeriktir."

with open('scripts/skincare/staging/caudalie/texts.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Ingredients descriptions generalized intelligently.")
