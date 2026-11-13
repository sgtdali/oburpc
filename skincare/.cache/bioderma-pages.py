import json,time,re
from pathlib import Path
import requests
from bs4 import BeautifulSoup
base=Path('scripts/skincare');products=json.loads((base/'.cache/bioderma-expected-products.json').read_text(encoding='utf8'))
all_slugs={p['slug'] for p in json.loads((base/'catalog.json').read_text(encoding='utf8'))['products'] if p['brand']=='bioderma'}
session=requests.Session();results=[]
def norm(s):return re.sub(r'\s+',' ',s).strip()
def page(path):
 r=session.get('https://uygunbakim.com'+path,timeout=45)
 if r.status_code>=500:
  time.sleep(3);r=session.get('https://uygunbakim.com'+path,timeout=45)
 return r,BeautifulSoup(r.content,'html.parser')
for n,p in enumerate(products,1):
 path='/skincare/product/'+p['slug'];r,s=page(path);errors=[]
 if r.status_code!=200:errors.append('HTTP '+str(r.status_code))
 h1=s.select_one('h1')
 if not h1 or h1.get_text(' ',strip=True)!=p['name']:errors.append('wrong H1')
 text=norm(s.get_text(' ',strip=True))
 if norm(p['description']) not in text:errors.append('description missing')
 if p['nameTr'] not in text:errors.append('Turkish name missing')
 hrefs=[a['href'].rsplit('/',1)[-1] for a in s.select('a[href^="/skincare/ingredients/"]')]
 ordered=list(dict.fromkeys(hrefs))
 if ordered!=p['ingredientSlugs']:errors.append('ingredients missing or wrong order')
 for instruction in p['howTo']:
  if norm(instruction) not in text:errors.append('usage missing');break
 if not any(p['slug'] in str(i) for i in s.select('img')):errors.append('product image missing')
 results.append({'slug':p['slug'],'status':r.status_code,'errors':errors})
 if n%10==0 or errors:print(n,p['slug'],errors or 'PASS',flush=True)
 time.sleep(.2)
indexes=[];catalog_slugs=set()
for path in ['/skincare/brands/bioderma','/skincare/catalog?marka=bioderma','/skincare/catalog?marka=bioderma&sayfa=2']:
 r,s=page(path);links={a['href'].rsplit('/',1)[-1] for a in s.select('a[href^="/skincare/product/"]')}
 assert r.status_code==200,(path,r.status_code)
 if '/brands/' in path:assert links==all_slugs,(path,len(links),len(all_slugs))
 else:catalog_slugs|=links
 indexes.append({'path':path,'status':r.status_code,'productLinks':len(links)})
assert catalog_slugs==all_slugs,(len(catalog_slugs),len(all_slugs))
report={'checkedProducts':len(results),'passedProducts':sum(not r['errors'] for r in results),'products':results,'indexes':indexes,'catalogTotal':len(catalog_slugs)}
(base/'.cache/bioderma-live-pages-verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print('RESULT',report['passedProducts'],'/',len(results),'catalog',len(catalog_slugs),flush=True)
assert report['passedProducts']==61,[r for r in results if r['errors']]
