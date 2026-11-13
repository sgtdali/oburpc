#!/bin/zsh
# Gratis hazırlık klasörlerini kataloğa işle ve veritabanına aktar (denetçi).
#
#   zsh scripts/skincare/gratis/finalize.sh <marka> [<marka> ...]
#
# Her marka için: tools.py check (madde metni dışında HATA varsa marka atlanır) -> synonyms.json'u
# synonyms_gratis.json'a ekle -> merge.py. Sonra tek seferde: build_data.py -> fetch_images.mjs --only ->
# push_to_db.mjs --only -> push_barcodes.mjs. Depo kökünden ya da herhangi bir yerden çalışır.
set -e
cd "$(dirname "$0")/../../.."
SK=scripts/skincare
merged=()
for b in "$@"; do
  errs=$(python3 -X utf8 $SK/staging/tools.py check "$b" 2>/dev/null | grep '^HATA' | grep -v -i 'madde metni\|nameTr\|description\|ingredients' || true)
  if [[ -n "$errs" ]]; then echo "ATLANDI $b:"; echo "$errs" | head -5; continue; fi
  python3 -I - "$b" <<'EOF'
import json, os, sys
b = sys.argv[1]
src = f"scripts/skincare/staging/{b}/synonyms.json"
dst = "scripts/skincare/synonyms_gratis.json"
if os.path.exists(src):
    syn = json.load(open(dst, encoding="utf8")) if os.path.exists(dst) else {}
    syn.update(json.load(open(src, encoding="utf8")))
    json.dump(dict(sorted(syn.items())), open(dst, "w", encoding="utf8"), ensure_ascii=False, indent=1)
EOF
  slugs=$(python3 -X utf8 $SK/staging/merge.py "$b" | sed -n 's/^slug.lar: //p')
  [[ -n "$slugs" ]] && merged+=("$slugs")
  echo "BİRLEŞTİ $b"
done
[[ ${#merged} -eq 0 ]] && { echo "birleşen ürün yok"; exit 0; }
only=$(IFS=,; echo "${merged[*]}")
# Görseller önce: build_data.py yalnızca yerelde WebP'si olan ürüne imageFile yazar
node $SK/fetch_images.mjs --only="$only" | tail -3
python3 -X utf8 $SK/build_data.py | grep -v -i warn | tail -3
node $SK/push_to_db.mjs --only="$only" | tail -3
node $SK/gratis/push_barcodes.mjs | tail -2
