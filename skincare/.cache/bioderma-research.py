import sys,json,re,unicodedata
from pathlib import Path
sys.path.insert(0,'scripts/skincare')
from fetch_sources import brand_page,get
from build_data import slug
from bs4 import BeautifulSoup

base=Path('scripts/skincare'); data=json.loads((base/'.cache/bioderma-inventory-2026-10-05.json').read_text(encoding='utf8'))
catalog=json.loads((base/'catalog.json').read_text(encoding='utf8'))
existing={p['brandUrl']:p for p in catalog['products']}
rows=[]
for url,p in data['/urunlerimiz']['products'].items():
 name=p['name']; reason=None
 if url in data['/gunes-koruyucu']['products'] or re.search(r'SPF',name,re.I):reason='güneş ürünü / SPF'
 elif '/node/' in url or 'shampoo' in name.lower():reason='saç ürünü'
 elif 'refill' in name.lower():reason='aynı ürünün dolum paketi'
 elif '/ar-bb-cream' in url:reason='SPF 30 içeren renkli bakım'
 if reason:
  rows.append({'url':url,**p,'excluded':reason});continue
 name=re.sub(r'^(\w+) \1\b',r'\1',name)
 s=existing[url]['slug'] if url in existing else 'bioderma-'+slug(unicodedata.normalize('NFKD',name.replace('+',' Plus')).encode('ascii','ignore').decode())
 b=brand_page(url)
 html=BeautifulSoup(get(url),'html.parser')
 meta=html.select_one('meta[name="description"]')
 rows.append({'url':url,'name':name,'slug':s,'description':p['description'],'meta':meta.get('content') if meta else '', 'existing':url in existing,'brandSite':b})
 if url not in existing:
  (base/'raw'/f'{s}.json').write_text(json.dumps({'slug':s,'brandSite':b},ensure_ascii=False,indent=1),encoding='utf8')
 print(s,len(b['inci'] or []),'image',bool(b['image']),flush=True)
 (base/'.cache/bioderma-research.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf8')
print('included',sum('excluded' not in r for r in rows),'new',sum('excluded' not in r and not r['existing'] for r in rows),flush=True)
