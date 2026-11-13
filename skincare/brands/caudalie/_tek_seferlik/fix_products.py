import json

with open('scripts/skincare/staging/caudalie/products.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

for p in products:
    # Fix slug
    if p['slug'] == 'caudalie-vinoterapist-overnight-detox-oil':
        p['slug'] = 'caudalie-vinotherapist-overnight-detox-oil'

    # Fix nameTr prefixes and TM/R based on reviewer feedback
    orig = p['nameTr'].replace('™', '').replace('®', '')
    
    # Apply series prefix if not present
    if 'Vinoclean' in p['name'] and 'Vinoclean' not in orig:
        orig = 'Vinoclean ' + orig
    elif 'Vinoperfect' in p['name'] and 'Vinoperfect' not in orig:
        orig = 'Vinoperfect ' + orig
    elif 'Vinotherapist' in p['name'] and 'Vinotherapist' not in orig and 'Vinothérapist' not in orig:
        orig = 'Vinothérapist ' + orig
    elif 'Vinothérapist' in orig:
        pass
    elif 'Vinohydra' in p['name'] and 'Vinohydra' not in orig:
        orig = 'Vinohydra ' + orig
    elif 'Resveratrol Lift' in p['name'] and 'Resveratrol-Lift' not in orig and 'Resveratrol Lift' not in orig:
        orig = 'Resveratrol-Lift ' + orig
    elif 'Premier Cru' in p['name'] and 'Premier Cru' not in orig:
        orig = 'Premier Cru ' + orig
    elif 'Vinopure' in p['name'] and 'Vinopure' not in orig:
        orig = 'Vinopure ' + orig
        
    # Extra fix for Vinotherapist to match feedback 
    orig = orig.replace('Vinotherapist', 'Vinothérapist')

    p['nameTr'] = orig.strip()

with open('scripts/skincare/staging/caudalie/products.json', 'w', encoding='utf-8') as f:
    json.dump(products, f, ensure_ascii=False, indent=2)

print("Updated products.json")
