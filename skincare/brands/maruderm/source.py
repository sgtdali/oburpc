"""Maruderm TR (Gratis barkod pilotu, 2026-11). İçerik listesi "İÇİNDEKİLER (INCI):" yazan kalın paragraftan sonraki
<p>'de ("Aqua (Water), Panthenol, ..."; büyük-küçük karışık → büyük harfe çevrilir). ld+json'da "ingredients" alanı
boş; gtin13 ise dolu (barkod eşlemesinde Gratis'teki barkodla karşılaştırılır).

Not: Gratis ürün açıklamasındaki liste aynı maddeleri farklı sırayla veriyor; sıra için marka sitesi esastır."""
import json

import source_common as sc

DOMAIN = "maruderm.com"


def inci(s, main):
    head = next((p for p in s.select("p") if p.get_text(strip=True).upper().startswith("İÇİNDEKİLER")), None)
    para = head.find_next_sibling("p") if head else None
    items = para.get_text(" ", strip=True) if para else ""
    if items.count(",") >= 5:
        return [x.upper() for x in sc.split_inci(sc.clean_text(items))], "maruderm"


def howto(s):
    """"Nasıl Kullanılır?" <h2>'sinden sonraki <h3> başlık + <p> açıklama çiftleri, bir sonraki <h2>'ye kadar
    ("Cildi Temizleyin: Cildinizi nazik bir temizleyici ile ...")."""
    h2 = next((h for h in s.select("h2") if "NASIL KULLANILIR" in h.get_text(strip=True).upper()), None)
    steps, title = [], None
    for el in (h2.find_all_next(["h2", "h3", "p"]) if h2 else []):
        if el.name == "h2":
            break
        t = el.get_text(" ", strip=True)
        if not t:
            continue
        if el.name == "h3":
            title = t
        else:
            steps.append(f"{title}: {t}" if title else t)
            title = None
    if not steps:
        # Eski sayfalar (ör. bariyer kremi): yalnızca ld+json FAQPage'deki "... nasıl kullanılır?" cevabı
        for tag in s.select('script[type="application/ld+json"]'):
            try:
                d = json.loads(tag.string or "")
            except ValueError:
                continue
            for q in (d.get("mainEntity") or []) if isinstance(d, dict) and d.get("@type") == "FAQPage" else []:
                if "nasıl kullanılır" in (q.get("name") or "").lower():
                    return [sc.clean_text((q.get("acceptedAnswer") or {}).get("text") or "").strip()]
    return steps
