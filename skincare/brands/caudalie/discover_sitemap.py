"""Caudalie TR site haritasından katalogda/staging'de olmayan ürün sayfalarını bulur, kabaca eler.

    python -X utf8 scripts/skincare/brands/caudalie/discover_sitemap.py   (repo kökünden)

URL'deki kelimelere göre ön eleme yapar (set, güneş, parfüm, saç, yedek dolum…); sonuç yalnızca bir aday
listesidir, her ürün sayfası yine elle/denetçiyle kontrol edilir. Çıktı onaylı excluded.json'un üzerine
yazmasın diye staging/caudalie/_out/sitemap_excluded.json'a gider.
"""
import json
import urllib.request
import re

import os

with open('scripts/skincare/catalog.json', 'r', encoding='utf-8') as f:
    products = [p for p in json.load(f)['products'] if p['brand'] == 'caudalie']
staged = 'scripts/skincare/staging/caudalie/products.json'
if os.path.exists(staged):
    with open(staged, 'r', encoding='utf-8') as f:
        products += json.load(f)
os.makedirs('scripts/skincare/staging/caudalie/_out', exist_ok=True)

existing_urls = [p['brandUrl'] for p in products]
existing_slugs = [p['slug'] for p in products]

url = 'https://tr.caudalie.com/sitemap.xml'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
html = urllib.request.urlopen(req).read().decode('utf-8')
urls = re.findall(r'<loc>(.*?)</loc>', html)
sitemap_products = [u for u in urls if '/p/' in u]

missing = [u for u in sitemap_products if u not in existing_urls]

excluded = []
to_fetch = []

for u in missing:
    reason = None
    u_lower = u.lower()
    name = u.split('/')[-1].replace('.html', '').replace('-', ' ').title()
    
    if 'set' in u_lower or 'kofre' in u_lower or 'coffret' in u_lower or 'ikili' in u_lower or 'uclusu' in u_lower or 'rutin' in u_lower or 'p1' in u_lower or 'duo' in u_lower:
        reason = 'set/kit'
    elif 'gunes' in u_lower or 'soleil' in u_lower or 'spf' in u_lower or 'suncare' in u_lower or 'bronze' in u_lower or 'tan' in u_lower or 'güneş' in u_lower:
        reason = 'güneş/bronzlaştırıcı'
    elif 'parfum' in u_lower or 'fragrance' in u_lower or 'koku' in u_lower or 'eau' in u_lower:
        if 'eau-des-vignes-shower-gel' not in u_lower and 'eau-micellaire' not in u_lower:
            reason = 'parfüm/vücut spreyi'
    elif 'sac' in u_lower or 'shampoo' in u_lower or 'hair' in u_lower:
        reason = 'saç'
    elif 'yedek' in u_lower or 'refill' in u_lower or 'eco' in u_lower or 'recharge' in u_lower:
        reason = 'yedek dolum'
    elif 'deodorant' in u_lower:
        reason = 'deodorant'
    elif 'vir' in u_lower:
         reason = 'farklı boy/varyant'
    elif 'tint' in u_lower or 'fondoten' in u_lower or 'pudra' in u_lower:
         reason = 'renkli makyaj'
    elif 'ml' in u_lower:
         reason = 'farklı boy/varyant'
         
    if reason:
        excluded.append({
            "url": u,
            "name": name,
            "reason": reason
        })
    else:
        to_fetch.append(u)

with open('scripts/skincare/staging/caudalie/_out/sitemap_excluded.json', 'w', encoding='utf-8') as f:
    json.dump(excluded, f, ensure_ascii=False, indent=2)

print(f"Total existing: {len(existing_urls)}")
print(f"Total excluded: {len(excluded)}")
print(f"To fetch (possible valid skincare): {len(to_fetch)}")

for t in to_fetch:
    print(t)
