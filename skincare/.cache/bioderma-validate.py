import json,sys,re
from pathlib import Path
sys.path.insert(0,'scripts/skincare')
from analyze import Analyzer
from fetch_sources import get,split_inci,clean_text
from bs4 import BeautifulSoup
base=Path('scripts/skincare');new=json.loads((base/'.cache/bioderma-new-slugs.json').read_text());want=set(new)
products=json.loads((base/'out/products.json').read_text(encoding='utf8'));ingredients=json.loads((base/'out/ingredients.json').read_text(encoding='utf8'))
ps=[p for p in products if p['slug'] in want];used={s for p in ps for s in p['ingredientSlugs']};ings=[i for i in ingredients if i['slug'] in used]
assert len(ps)==61 and len(want)==61
assert all(p['description'] and p['nameTr'] and p['imageFile'] and p['howTo'] and p['ingredientSlugs'] for p in ps)
assert all(i['nameTr'] and i['description'] for i in ings)
assert all(p['brandSlug']=='bioderma' and p['formulaRegion']=='Türkiye' for p in ps)
assert all(not re.search(r'SPF|shampoo|refill',p['name'],re.I) for p in ps)
for p in ps:assert (base/'out/images'/p['imageFile']).stat().st_size>1000
a=Analyzer();ask=json.loads((base/'raw/bioderma-sebium-mat-control.json').read_text(encoding='utf8'))['brandSite']['inci']
s=BeautifulSoup(get('https://www.naosstars.com/bioderma-sebium-mat-control-matlastirici-krem-30ml'),'html.parser')
ul=next(u for u in s.select('.urunTabAlt ul') if u.select_one('li') and u.select_one('li').get_text().startswith('AQUA'))
shop=split_inci(clean_text(', '.join(li.get_text(' ',strip=True) for li in ul.select('li'))))
assert [a.resolve(n)['inci'] for n in ask]==[a.resolve(n)['inci'] for n in shop]
for file,rows in [('products',ps),('ingredients',ings)]: (base/'.cache'/f'bioderma-expected-{file}.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf8')
print('PASS: 61 complete products,',len(ings),'used ingredients,',sum(len(p['ingredientSlugs']) for p in ps),'ordered links. Mat Control 27/27 matches.')
