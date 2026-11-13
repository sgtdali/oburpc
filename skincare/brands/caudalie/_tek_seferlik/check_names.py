import json

with open('scripts/skincare/staging/caudalie/products.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

for p in products:
    print(f"{p['slug']} : {p['name']} -> {p['nameTr']}")
