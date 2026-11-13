"""Nivea TR. İçerik bölümünde "Dahil:" etiketli paragraf, "Aqua, Glycerin, ..." (büyük-küçük karışık)."""
import re
import source_common as sc

DOMAIN = "nivea.com.tr"


def inci(s, main):
    for para in s.select("p.nx-ingredients__section"):
        label = para.select_one("strong")
        if label and label.get_text(strip=True).rstrip(":").lower() == "dahil":
            label.decompose()
            # Kelimeler <span>'lere bölünebiliyor ("Hydro<span>genated</span>") → ayraçsız birleştir
            items = re.sub(r"\s+", " ", para.get_text("")).strip()
            return [x.upper() for x in sc.split_inci(sc.clean_text(items))], "nivea"
    # 2026-11 yeni tasarım: [data-test=product-ingredients-accordion-item] içinde "Dahil" başlıklı div + span
    for box in s.select("[data-test=product-ingredients-accordion-item]"):
        for label in box.find_all("div", string=re.compile(r"^\s*Dahil:?\s*$", re.I)):
            span = label.find_next_sibling("span")
            if span:
                items = re.sub(r"\s+", " ", span.get_text("")).strip()
                return [x.upper() for x in sc.split_inci(sc.clean_text(items))], "nivea"
