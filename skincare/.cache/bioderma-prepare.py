import json,sys
from pathlib import Path
sys.path.insert(0,'scripts/skincare')
from analyze import Analyzer
from build_data import slug

base=Path('scripts/skincare')
load=lambda p:json.loads(p.read_text(encoding='utf8'))
save=lambda p,d:p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
rows=load(base/'.cache/bioderma-research.json')
catalog=load(base/'catalog.json');texts=load(base/'texts_tr.json')
names=dict(l.split('|') for l in (base/'.cache/bioderma-ingredient-names.tsv').read_text(encoding='utf8').splitlines() if l)
editorial={parts[0]:parts[1:] for l in (base/'.cache/bioderma-editorial.tsv').read_text(encoding='utf8').splitlines() if l for parts in [l.split('|')]}
a=Analyzer();new=[]

functions={
 'HUMECTANT':'Suyu tutarak nem desteği sağlar.',
 'SKIN CONDITIONING - EMOLLIENT':'Cilt yüzeyini yumuşatır ve ürünün yayılmasını kolaylaştırır.',
 'SKIN CONDITIONING':'Cilt yüzeyinin bakımına katkı sağlar.',
 'SKIN CONDITIONING - OCCLUSIVE':'Cilt üzerinde nem kaybını azaltmaya yardımcı bir katman oluşturur.',
 'SKIN CONDITIONING - MISCELLANEOUS':'Kozmetik formüllerde cilt bakım bileşeni olarak kullanılır.',
 'SURFACTANT - EMULSIFYING':'Yağ ve su fazlarının birlikte dağılmasına yardımcı olur.',
 'SURFACTANT - CLEANSING':'Yüzey aktif yapısıyla kir ve yağın temizlenmesine katkı sağlar.',
 'CLEANSING':'Temizleyici formüllerde arındırmaya yardımcı olur.',
 'ANTIOXIDANT':'Oksidasyonu sınırlayarak formülün korunmasına katkı sağlar.',
 'FILM FORMING':'Yüzeyde ince bir film oluşturarak ürünün doku ve tutunmasına katkı sağlar.',
 'VISCOSITY CONTROLLING':'Ürünün kıvamını ve akışkanlığını düzenler.',
 'EMULSION STABILISING':'Emülsiyonun ayrışmasını sınırlayarak homojen kalmasına yardımcı olur.',
 'COLORANT':'Ürüne renk veren bir bileşendir.',
 'OPACIFYING':'Formülün daha opak görünmesine yardımcı olur.',
 'ANTICAKING':'Toz bileşenlerin topaklanmasını azaltır.',
 'ABSORBENT':'Yağ veya nemi tutarak ürünün yüzey hissini düzenler.',
 'GEL FORMING':'Jel yapısının oluşmasına katkı sağlar.',
 'SOLVENT':'Formül bileşenlerinin çözünmesine yardımcı olur.',
 'PRESERVATIVE':'Formülün mikrobiyal bozulmaya karşı korunmasına yardımcı olur.',
 'REDUCING':'İndirgen özellikleriyle formülün kimyasal dengesine katkı sağlar.',
 'BUFFERING':'Formülün pH dengesinin korunmasına katkı sağlar.',
 'CHELATING':'Metal iyonlarını bağlayarak formülün kararlılığına yardımcı olur.',
 'BINDING':'Bileşenlerin bir arada tutulmasına katkı sağlar.',
 'ASTRINGENT':'Cilt yüzeyinde geçici sıkılaşma hissi sağlayabilir.',
 'SKIN PROTECTING':'Cilt yüzeyinin dış etkenlere karşı korunmasına katkı sağlar.',
 'SOOTHING':'Ciltte konfor ve yatışmışlık hissini destekler.',
 'BLEACHING':'Ton eşitsizliği görünümüne yönelik kozmetik formüllerde kullanılır.',
 'UV ABSORBER':'UV ışığını emerek formülün ışığa karşı kararlılığına katkı sağlayabilir; tek başına güneş korumasını göstermez.',
 'ANTIMICROBIAL':'Mikroorganizmaların çoğalmasını sınırlayan formül bileşenlerindendir.',
 'ANTI-SEBORRHEIC':'Yağlı ve pullanma eğilimli cilt veya saçlı deri için kozmetik formüllerde kullanılır.',
 'HAIR CONDITIONING':'Saç yüzeyinin bakımına katkı sağlayan kozmetik bileşenlerindendir.',
 'FRAGRANCE':'Formülün koku yapısına katkı sağlayabilir.',
}
overrides={
 'azelaic-acid':'Dikarboksilik bir asittir; ton eşitsizliği ve pürüz görünümüne yönelik bakım formüllerinde kullanılır. İçerik listesi miktarını göstermediği için ürünün etkisi tek başına bu maddeden çıkarılamaz.',
 'bakuchiol':'Bitki kaynaklı bir bakım bileşenidir; antioksidan ve cildi yumuşatıcı işlevleri bulunur. Retinol ile aynı madde değildir; bitmiş ürünün etkisi formüle ve miktara bağlıdır.',
 'titanium-dioxide':'Beyaz renk ve opaklık sağlayabilen mineral bileşendir; uygun güneş koruyucu formüllerinde UV filtresi olarak da kullanılabilir. Renkli kremde bulunması tek başına ürünün SPF sağladığını göstermez.',
 'undecylenic-glycerides':'Undesilenik asitten türetilen gliserit karışımıdır. Kaynak kaydında işlev bilgisi bulunmadığından bu maddeden tek başına belirli bir cilt etkisi çıkarılmıyor.',
 'polyethylene':'Kozmetik dokuyu, film oluşumunu ve ürünün yüzey hissini düzenleyebilen sentetik bir polimerdir.',
 'ascorbyl-glucoside':'C vitamininin glukoza bağlı bir türevidir. Antioksidan bakım ve daha eşit ton görünümüne yönelik formüllerde kullanılır; saf askorbik asitle aynı bileşen değildir.',
 'ascorbyl-palmitate':'C vitamininin yağda çözünen ester türevidir. Antioksidan işleviyle formülü oksidasyona karşı destekler; saf askorbik asitle aynı bileşen değildir.',
 'sodium-sulfate':'İnorganik bir tuzdur; formülün hacmini ve kıvamını düzenleyebilir. Sodyum lauril sülfat veya sodyum lauret sülfat gibi bir temizleyici yüzey aktif madde değildir.',
 'cysteine-hcl':'Sistein amino asidinin hidroklorür tuzudur. Antioksidan ve indirgen işlevlerle kozmetik formüllerde kullanılabilir.',
}

for r in rows:
 if 'excluded' in r or r['existing']:continue
 s=r['slug']
 if 'intensive-bar-kalp' in s:
  old=s;s='bioderma-atoderm-intensive-bar';r['slug']=s
  raw=load(base/'raw'/f'{old}.json');raw['slug']=s;save(base/'raw'/f'{s}.json',raw);(base/'raw'/f'{old}.json').unlink()
 if '/atoderm/nutrition-cream' in r['url']:r['name']='Atoderm Nutritive'
 key=r['url'].split('/urunlerimiz/')[-1];category,name_tr,intro=editorial[key]
 b=r['brandSite'];assert b['inci'] and b['image'],s
 result=a.analyze(b['inci']);assert not result['unknown'],(s,result['unknown'])
 for item in result['ingredients']:
  k=item['kb'];ing=slug(k['inci'])
  if ing not in texts['ingredients']:
   assert ing in names,ing
   sentences=[]
   for f in functions:
    if f in k['functions'] and len(sentences)<2:sentences.append(functions[f])
   desc=overrides.get(ing) or ' '.join(sentences)
   assert desc,ing
   texts['ingredients'][ing]={'nameTr':names[ing],'description':desc}
 p={'slug':s,'brand':'bioderma','name':r['name'],'nameTr':name_tr,'category':category,'brandUrl':r['url']}
 if r.get('inciFallbackUrl'):p['inciFallbackUrl']=r['inciFallbackUrl']
 if s=='bioderma-sensibio-eye-contour-gel':p['verificationSources']=[{'label':'INCI yazım doğrulaması (Ask.NAOS Türkiye)','url':'https://ask-naos.com.tr/product/sensibio-eye-contour-gel-bioderma'}]
 selected=[]
 # Asıl formüldeki bakım bileşenleri, yüzey aktif maddeler ve ilk sıralardaki nem/yumuşatıcılar.
 ordered=result['ingredients']
 priority=['SALICYLIC ACID','GLYCOLIC ACID','NIACINAMIDE','PANTHENOL','ASCORBYL GLUCOSIDE','SODIUM HYALURONATE','HYDROLYZED HYALURONIC ACID','GLYCYRRHETINIC ACID','CERAMIDE NP','SQUALANE','CAFFEINE','BAKUCHIOL']
 if category in ('cilt-temizleyici','yuz-temizleyici','misel-su'):
  candidates=[i for i in ordered if any(f in i['kb']['functions'] for f in ['SURFACTANT - CLEANSING','CLEANSING','SURFACTANT - EMULSIFYING'])][:2]
  selected=[i['kb']['inci'] for i in candidates]
 selected += [n for n in priority if any(i['kb']['inci']==n for i in ordered)]
 selected += [i['kb']['inci'] for i in ordered if i['kb']['inci']!='AQUA' and any(f in i['kb']['functions'] for f in ['HUMECTANT','SKIN CONDITIONING - EMOLLIENT','SKIN CONDITIONING'])]
 selected=list(dict.fromkeys(selected))[:3]
 detail='Türkiye içerik listesinde '+', '.join(texts['ingredients'][slug(n)]['nameTr'].lower() for n in selected)+' bulunuyor.'
 fragrance=any(i['kb']['inci']=='PARFUM' for i in ordered)
 desc=intro+' '+detail+(' Parfüm içeriyor.' if fragrance else ' Listede parfüm (PARFUM) bulunmuyor.')
 if category not in ('cilt-temizleyici','yuz-temizleyici','misel-su') and any(n in selected for n in ['SALICYLIC ACID','GLYCOLIC ACID']):
  desc+=' Asit içeren bakımın kullanım sıklığı cildin toleransına göre değerlendirilmelidir.'
 if s=='bioderma-matricium':desc+=' İçeriklerin miktarı listeden belirlenemiyor; bu bileşim tıbbi işlem veya tedavi yerine geçmez.'
 texts['products'][s]=desc
 assert not any(p0['slug']==s for p0 in catalog['products']),s
 catalog['products'].append(p);new.append(s)
save(base/'catalog.json',catalog);save(base/'texts_tr.json',texts);save(base/'.cache/bioderma-research.json',rows);save(base/'.cache/bioderma-new-slugs.json',new)
print('New products',len(new),'catalog',len(catalog['products']),'texts',len(texts['ingredients']))
