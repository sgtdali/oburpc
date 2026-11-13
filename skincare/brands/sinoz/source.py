"""Sinoz TR. "İçerik Listesi" başlığından sonraki paragraf; harfler ayrı <span>'lere bölünebiliyor
("<span>A</span><span>loe ...") → parçalar ayraçsız birleştirilir. Bulunamazsa genel "İçerik Listesi |" metni."""
import re
import source_common as sc

DOMAIN = "sinoz.com.tr"


def inci(s, main):
    head = next((h for h in s.select("h2, h3") if h.get_text(strip=True) == "İçerik Listesi"), None)
    para = head.find_next_sibling(["p", "div"]) if head else None
    items = re.sub(r"\s+", " ", para.get_text("")).strip() if para else ""
    # Bazı sayfalarda paragraf "Tam İçerik Listesi (INCI): Aqua, ..." diye başlıyor (Avocado Bomb göz kremi).
    items = re.sub(r"(?i)^tam\s+[İIi]̇?çerik\s+listesi\s*(\(inci\))?\s*:\s*", "", items)
    if items.count(",") >= 5:
        return [x.upper() for x in sc.split_inci(sc.clean_text(items))], "sinoz"
