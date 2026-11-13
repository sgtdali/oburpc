import json
import urllib.request
import re

with open('scripts/skincare/staging/caudalie/products.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

existing_urls = [p['brandUrl'] for p in products]

url = 'https://tr.caudalie.com/sitemap.xml'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
html = urllib.request.urlopen(req).read().decode('utf-8')
urls = re.findall(r'<loc>(.*?)</loc>', html)
sitemap_products = [u for u in urls if '/p/' in u or u.endswith('.html')]

missing = [u for u in sitemap_products if u not in existing_urls]

# Try to categorize missing
excluded = []
to_fetch = []

for u in missing:
    reason = None
    u_lower = u.lower()
    
    if 'set' in u_lower or 'kofre' in u_lower or 'ikili' in u_lower or 'uclusu' in u_lower or 'rutin' in u_lower or 'p1' in u_lower:
        reason = 'set/kit'
    elif 'gunes' in u_lower or 'spf' in u_lower or 'suncare' in u_lower or 'bronze' in u_lower or 'tan' in u_lower:
        reason = 'gunes/bronzlastirici'
    elif 'parfum' in u_lower or 'fragrance' in u_lower or 'koku' in u_lower:
        reason = 'parfum'
    elif 'sac' in u_lower or 'shampoo' in u_lower or 'hair' in u_lower:
        reason = 'sac'
    elif 'yedek' in u_lower or 'refill' in u_lower or 'eco' in u_lower:
        reason = 'yedek dolum'
    elif 'deodorant' in u_lower:
        reason = 'deodorant'
    elif 'vir' in u_lower:
         reason = 'farkli boy/varyant'
    
    if reason:
        excluded.append({
            "url": u,
            "name": u.split('/')[-1].replace('.html', '').replace('-', ' ').title(),
            "reason": reason
        })
    else:
        to_fetch.append(u)

with open('scripts/skincare/staging/caudalie/excluded.json', 'w', encoding='utf-8') as f:
    json.dump(excluded, f, ensure_ascii=False, indent=2)

print(f"Total existing: {len(existing_urls)}")
print(f"Total excluded: {len(excluded)}")
print(f"To fetch (possible valid skincare): {len(to_fetch)}")

for t in to_fetch[:20]:
    print(t)
