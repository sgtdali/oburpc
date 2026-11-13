"""Eau Thermale Avène TR (Pierre Fabre). İçerik listesi "composition_inci" panelinde, noktayla ayrılı:
"GLYCERIN. ZINC OXIDE. ..." Aynı altyapıyı Ducray da kullanır (brands/ducray/source.py)."""
import re
import source_common as sc

DOMAIN = "eau-thermale-avene.com.tr"


def inci(s, main):
    box = s.select_one("#composition_inci-panel p")
    if box:
        items = re.split(r"\.\s+(?=[A-Z0-9])", box.get_text(" ", strip=True).rstrip("."))
        return sc.split_inci(sc.clean_text(", ".join(items))), "avene"
