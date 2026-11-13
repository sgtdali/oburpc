import json

with open('scripts/skincare/staging/caudalie/texts.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

products_to_fix = [k for k in data.get('products', {}).keys()]
ingredients_to_fix = []
for k, v in data.get('ingredients', {}).items():
    desc = v.get('description', '')
    if 'Kozmetik form' in desc:
        ingredients_to_fix.append((k, v['nameTr']))

with open('template_texts.py', 'w', encoding='utf-8') as f:
    f.write('products = {\n')
    for p in products_to_fix:
        f.write(f'    "{p}": "",\n')
    f.write('}\n\n')
    f.write('ingredients = {\n')
    for k, name in ingredients_to_fix:
        f.write(f'    "{k}": "",  # {name}\n')
    f.write('}\n')
