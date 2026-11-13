#!/usr/bin/env python3
"""Gratis barkodları için temkinli katalog adayları üretir."""
import argparse
import csv
from collections import Counter, defaultdict
from difflib import SequenceMatcher
import json
from pathlib import Path
import re
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent / '_out'
FIELDS = ['confidence', 'gtin14', 'gratis_brand', 'gratis_name', 'size', 'gratis_url',
          'our_slug', 'our_name', 'our_nameTr', 'score', 'reason']


def norm(text):
    """Türkçe harfleri ve yazım farklarını karşılaştırılabilir hale getirir."""
    text = str(text or '').replace('İ', 'i').replace('ı', 'i').lower()
    text = unicodedata.normalize('NFKD', text)
    text = ''.join(c for c in text if not unicodedata.combining(c))
    return re.sub(r'[^a-z0-9]+', ' ', text).strip()


def brand_key(text):
    return norm(text).replace(' ', '')


def valid_gtin(value):
    value = str(value or '').strip()
    if not re.fullmatch(r'\d{8}|\d{12,14}', value, flags=re.ASCII):
        return None
    value = value.zfill(14)
    total = sum(int(c) * (3 if i % 2 == 0 else 1)
                for i, c in enumerate(reversed(value[:-1])))
    return value if (10 - total % 10) % 10 == int(value[-1]) else None


FILLER = set('ve ile icin karsiti cilt yuz bakim urunu urun etkili ozel gunluk '
             'nemlendirici nemlendiren onarici onaran yatistirici guclendirici '
             'arindirici temizleyici kremi jeli serumu losyonu spreyi cream gel '
             'care moisturizing moisturising hydrating repair soothing skin face '
             'the plus ml gr gram g adet'.split())
SERIES = set('cicaplast effaclar sensibio hydrance cleanance vinoperfect anthelios '
             'photoderm lipikar toleriane hyalu pigmentclar redermic sebium atoderm '
             'hydrabio abcderm cicabio pigmentbio uvmune uvair'.split())
GROUPS = {
    'renkli': {'renkli', 'tinted', 'bb', 'cc'},
    'gece': {'gece', 'night', 'nuit'},
    'goz': {'goz', 'eye', 'eyes', 'yeux'},
    'dudak': {'dudak', 'lip', 'lips', 'levres'},
    'el': {'el', 'hand', 'hands', 'mains'},
    'jel': {'jel', 'jeli', 'gel'},
    'krem': {'krem', 'kremi', 'cream', 'creme', 'baume', 'balm'},
    'kopuk': {'kopuk', 'kopugu', 'foam', 'foaming', 'mousse'},
    'sprey': {'sprey', 'spreyi', 'spray', 'mist'},
    'losyon': {'losyon', 'losyonu', 'lotion'},
    'serum': {'serum', 'serumu'},
    'stick': {'stick'},
}
FORMS = {'jel', 'krem', 'kopuk', 'sprey', 'losyon', 'serum', 'stick'}


def words(text, brand=''):
    text = re.sub(r'(?i)\b\d+(?:[.,]\d+)?\s*(?:ml|g|gr|kg|l)\b', ' ', str(text or ''))
    value = norm(text)
    if brand:
        value = re.sub(r'\b' + re.escape(norm(brand)) + r'\b', ' ', value)
    return set(value.split())


def features(text):
    tokens = set(norm(text).split())
    flags = {key for key, aliases in GROUPS.items() if tokens & aliases}
    spf = set(re.findall(r'\bspf\s*(\d{1,3})', norm(text)))
    return flags, spf, tokens & SERIES


def inci_overlap(inci, slugs):
    if not inci or not slugs:
        return None
    # Madde sırası tek başına belirleyici değildir; ilk on maddenin kümesi kullanılır.
    parts = [re.sub(r'[^a-z0-9]+', '-', x.lower()).strip('-')
             for x in re.split(r'[,;\n]+', inci) if x.strip()][:10]
    if not parts:
        return None
    return len(set(parts) & set(slugs[:10])) / len(set(parts))


def candidate(row, product):
    gratis = row.get('name') or ''
    ours = (product.get('name') or '') + ' ' + (product.get('nameTr') or '')
    a, asp, aseries = features(gratis)
    b, bsp, bseries = features(ours)
    reasons = []
    if asp and bsp and asp != bsp:
        reasons.append('SPF uyuşmazlığı')
    if aseries and bseries and aseries != bseries:
        reasons.append('seri uyuşmazlığı')
    if (a & FORMS) and (b & FORMS) and not (a & b & FORMS):
        reasons.append('ürün formu uyuşmazlığı')
    for flag in ('renkli', 'gece', 'goz', 'dudak', 'el'):
        if (flag in a) != (flag in b):
            reasons.append(flag + ' özelliği uyuşmazlığı')
    overlap = inci_overlap(row.get('inci'), product.get('ingredientSlugs') or [])
    if overlap is not None and overlap < 0.4:
        reasons.append('düşük INCI örtüşmesi (%d)' % round(overlap * 100))
    wa = words(gratis, row.get('brand')) - FILLER
    wb = words(ours) - FILLER
    common = wa & wb
    # Genel sözcükler tek başına ürün kimliği sağlamaz.
    lexical = len(common) / max(1, len(wb))
    ratio = max(SequenceMatcher(None, norm(gratis), norm(product.get(k))).ratio()
                for k in ('name', 'nameTr'))
    score = 100 * (0.75 * lexical + 0.25 * ratio)
    if overlap is not None:
        score = score * 0.75 + overlap * 25
    detail = 'ad ortak: ' + (', '.join(sorted(common)) or 'yok')
    if overlap is not None:
        detail += '; INCI %d' % round(overlap * 100)
    return round(score, 1), reasons, detail, common, lexical, overlap


def load_catalog():
    products = json.loads((ROOT / 'out/products.json').read_text(encoding='utf-8'))
    brands = json.loads((ROOT / 'out/brands.json').read_text(encoding='utf-8'))
    by_brand = defaultdict(list)
    for p in products:
        by_brand[p['brandSlug']].append(p)
    keys = {}
    for b in brands:
        for name in (b['name'], b['slug']):
            keys[brand_key(name)] = b['slug']
    return by_brand, keys


def match(row, by_brand, keys):
    result = dict.fromkeys(FIELDS, '')
    result.update(confidence='none', gratis_brand=row.get('brand') or '',
                  gratis_name=row.get('name') or '', size=row.get('size') or '',
                  gratis_url=row.get('url') or '')
    gtin = valid_gtin(row.get('gtin'))
    if not gtin:
        result['reason'] = 'invalid_gtin'
        return result
    result['gtin14'] = gtin
    brand = keys.get(brand_key(row.get('brand')))
    if not brand:
        result['reason'] = 'unmatched_brand'
        return result
    candidates = []
    for product in by_brand.get(brand, []):
        assessment = candidate(row, product)
        candidates.append((assessment[0], product['slug'], product, assessment))
    if not candidates:
        result['reason'] = 'Markanın katalog ürünü yok'
        return result
    candidates.sort(key=lambda x: (-x[0], x[1]))
    viable = [x for x in candidates if not x[3][1]]
    best = viable[0] if viable else candidates[0]
    score, _, product, (_, rejected, detail, common, lexical, overlap) = best
    result.update(our_slug=product['slug'], our_name=product.get('name') or '',
                  our_nameTr=product.get('nameTr') or '', score=score)
    if rejected:
        result['reason'] = 'Reddedildi: ' + ', '.join(rejected) + '; ' + detail
        return result
    margin = score - viable[1][0] if len(viable) > 1 else 100
    # Eksik SPF/seri bilgisi ve birbirine yakın adaylar otomatik eşleşmeyi engeller.
    af, ap, ar = features(row.get('name') or '')
    bf, bp, br = features((product.get('name') or '') + ' ' + (product.get('nameTr') or ''))
    uncertain = bool(ap != bp or ar != br or (row.get('inci') and overlap is None))
    if common and score >= 70 and lexical >= 1.0 and margin >= 10 and not uncertain and (overlap is None or overlap >= 0.7):
        result['confidence'] = 'high'
    elif common and score >= 35:
        result['confidence'] = 'review'
    result['reason'] = detail + '; aday farkı %.1f' % margin
    if uncertain:
        result['reason'] += '; eksik SPF, seri veya INCI bilgisi'
    return result


def read_rows():
    rows = {}
    for path in sorted(OUT.glob('products*.jsonl')):
        with path.open(encoding='utf-8-sig') as f:
            for line_no, line in enumerate(f, 1):
                if not line.strip():
                    continue
                try:
                    row = json.loads(line)
                except json.JSONDecodeError as exc:
                    raise ValueError(f'{path}:{line_no}: geçersiz JSON') from exc
                raw = str(row.get('gtin') or '').strip()
                key = valid_gtin(raw) or ('invalid', raw) if raw else ('missing', str(path), line_no)
                if key in rows:
                    old = rows[key]
                    # Çelişkili kimlikler hiçbir zaman otomatik eşleştirilmez.
                    if norm(old.get('brand')) != norm(row.get('brand')) or norm(old.get('name')) != norm(row.get('name')):
                        old['_conflict'] = True
                    if not old.get('inci') and row.get('inci'):
                        old['inci'] = row['inci']
                else:
                    rows[key] = row
    return list(rows.values())


def sample(by_brand, keys):
    """Dosya yazmadan örnekleri ve temel güvenlik kurallarını sınar."""
    examples = [
        ('La Roche Posay', 'La Roche Posay Cicaplast Baume B5+ Onarıcı Bakım Kremi 40 ml', 'la-roche-posay-cicaplast-baume-b5-plus'),
        ('La Roche Posay', 'La Roche Posay Hyalu B5 Serum 30 ml', 'la-roche-posay-hyalu-b5-serum'),
    ]
    for brand, name, expected in examples:
        row = {'brand': brand, 'name': name, 'gtin': '8682397030826'}
        result = match(row, by_brand, keys)
        print(f"{name} -> {result['our_slug']} ({result['confidence']}, {result['score']})")
        assert result['our_slug'] == expected, result
    assert valid_gtin('8682397030826') == '08682397030826'
    assert valid_gtin('8682397030827') is None
    print('Örnek ve GTIN kontrolleri başarılı.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sample', action='store_true', help='Dosya yazmadan örnekleri sınar')
    args = parser.parse_args()
    by_brand, keys = load_catalog()
    if args.sample:
        sample(by_brand, keys)
        return
    rows = read_rows()
    if not rows:
        print('products*.jsonl içinde ürün bulunamadı; çıktı oluşturulmadı.')
        return
    results = []
    missing = defaultdict(lambda: [0, 0])
    for row in rows:
        result = match(row, by_brand, keys)
        if row.get('_conflict'):
            result['confidence'] = 'none'
            result['reason'] += '; aynı GTIN için çelişkili ürün bilgisi'
        if not keys.get(brand_key(row.get('brand'))):
            counts = missing[result['gratis_brand']]
            counts[0] += 1
            counts[1] += bool(row.get('inci'))
        results.append(result)
    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / 'matches.csv').open('w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(results)
    with (OUT / 'unmatched_brands.csv').open('w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['gratis_brand', 'product_count', 'inci_count'])
        for brand, counts in sorted(missing.items(), key=lambda x: (-x[1][0], x[0])):
            writer.writerow([brand, *counts])
    counts = Counter(r['confidence'] for r in results)
    print('Toplam: %d; high: %d; review: %d; none: %d' %
          (len(results), counts['high'], counts['review'], counts['none']))
    brands = defaultdict(Counter)
    for result in results:
        brands[result['gratis_brand']][result['confidence']] += 1
    for brand, count in sorted(brands.items()):
        print('%s: high %d, review %d, none %d' %
              (brand, count['high'], count['review'], count['none']))


if __name__ == '__main__':
    main()
