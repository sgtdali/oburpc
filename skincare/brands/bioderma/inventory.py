"""Türkiye ürün dizinini nazikçe sayfala; kaynak kategorilerini ayrı koru."""
import json, re, sys
from pathlib import Path
from urllib.parse import urljoin
from bs4 import BeautifulSoup
SK = Path(__file__).resolve().parents[2]  # scripts/skincare
sys.path.insert(0, str(SK))
from source_common import get  # noqa: E402

ROOT = 'https://www.bioderma.com.tr'
OUT = SK / '.cache' / 'bioderma-inventory-2026-10-05.json'

def listing(path):
    rows, reported = {}, None
    url = ROOT + path
    for page in range(20):
        s = BeautifulSoup(get(url), 'html.parser')
        count = s.select_one('.filter-header__count')
        if count:
            reported = int(re.search(r'\d+', count.get_text()).group())
        headings = s.select('h2.title-1--product')
        if not headings:
            break
        for h in headings:
            box = h.parent
            a = box.select_one('a.gtm-see-product')
            if not a:
                raise ValueError(f'Missing product URL: {h}')
            desc = box.select_one('.routine__description')
            rows[urljoin(ROOT, a['href'])] = {
                'name': h.get_text(' ', strip=True),
                'description': desc.get_text(' ', strip=True) if desc else '',
            }
        print(path, page, len(rows), reported, flush=True)
        next_page = s.select_one('a.load-more[rel="next"]')
        if not next_page or (reported and len(rows) >= reported):
            break
        url = urljoin(url, next_page['href'])
    if len(rows) != reported:
        raise ValueError(f'{path}: {len(rows)} != {reported}')
    return {'reported': reported, 'products': rows}

if __name__ == '__main__':
    data = {p: listing(p) for p in ['/urunlerimiz', '/cilt-bakimi', '/temizleme', '/gunes-koruyucu']}
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf8')
    print(OUT)
