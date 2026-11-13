"""2026-11-13: L'Oréal Paris ve Garnier kullanım talimatları.

fetch_sources.py tek adımlı ld+json HowTo'yu ("step" liste değil tek nesne) yanlış okuyordu; adım olarak alan adları
("@type", "position", "text") yazılmıştı (DB'de 33 ürün). Kod düzeltildi; sayfadaki metin tek parça geldiği için
burada markanın cümleleriyle adımlara bölündü. Çıkarılanlar: başlıklar ("… Nasıl Kullanılır?"), başka ürün önerileri
("rutininizi … ile tamamlayın"), etki/tanıtım cümleleri. Boş adımlı sayfalar (4 Garnier, PDRN serum) boş kalır.

Uygula: python -X utf8 scripts/skincare/denetim/kullanim_loreal_garnier_20261113.py  (raw/<slug>.json howTo + note)
"""
import json
import os

HOWTO = {
    "garnier-dudak-nemlendirici-bakim-maskesi": [
        "Maskeyi dudak çevresini kaplayacak şekilde yerleştirin.",
        "15 dakika bekleyin; bu sürede rahatça hareket edebilirsiniz.",
        "Maskeyi çıkarın, kalan fazla ürünü dudaklarınıza masaj yaparak yedirin.",
    ],
    "loreal-paris-2-5-hyaluronik-asit-kafein-aydinlatici-goz-serumu": [
        "Sabah ve akşam temiz ve kurulanmış cildinize uygulayın.",
        "Gözünüzün iç köşesinden şakaklarınıza kadar küçük daireler halinde masaj yapın; 4 kez tekrarlayın.",
        "Göz kapaklarının üzerinde nazikçe gezdirin.",
        "Parmaklarınızla fazla ürünü nazikçe dağıtın.",
    ],
    "loreal-paris-bright-reveal-fluid-spf50": [
        "Kullanmadan önce çalkalayın.",
        "Her sabah nemlendirici yerine ya da cilt bakım rutininizden sonra ve makyajınızdan önce UV koruması olarak "
        "uygulayın.",
    ],
    "loreal-paris-bright-reveal-niacinamide-serum": [
        "Sabah ve akşam 3-4 damla serumu temiz yüz ve boyun bölgenize uygulayın.",
        "Ardından nemlendiricinizi sürebilirsiniz.",
        "Dekolte bölgesine ve ellere de uygulanabilir.",
        "Göz çevresinden kaçının; gözle teması halinde hemen su ile durulayın.",
        "Sabahları en az 30 faktör güneş koruyucu kullanın.",
    ],
    "loreal-paris-bright-reveal-peeling-serum": [
        "Şişeyi sağa sola iyice çalkalayın (aşağı yukarı yönde çalkalamayın).",
        "Şişeyi ters çevirin ve ucundan sıkarak elinize dökün.",
        "Kuru ve temiz cildinize, göz, burun delikleri ve dudak çevresi dışında, parmak uçlarınızla eşit şekilde "
        "dağıtarak uygulayın.",
        "15 dakika bekleyin.",
        "Artan serumu bir pamukla silin ve ılık suyla durulayın.",
        "Ardından nemlendiricinizi sürebilirsiniz.",
        "Günlük kullanıma uygun değildir; birer gün arayla haftada 4 gece kullanabilirsiniz.",
        "Ertesi gün en az 30 GKF güneş koruyucu kullanın.",
    ],
    "loreal-paris-degerli-cicekler-temizleme-sutu-normal-ve-karma-ciltler": [
        "Sabah ve akşam bir pamuk yardımıyla yüz ve boyun bölgenize uygulayın.",
    ],
    "loreal-paris-detoks-maskesi": [
        "Haftada 2 kez, temiz cildinizde tüm yüzünüze ince bir katman uygulayın; göz çevresine ve dudaklara sürmeyin.",
        "5-10 dakika kurumasını bekleyin, ardından nemli bir havlu ya da ılık suyla temizleyin.",
        "Gözle temas etmesi halinde hemen bol su ile yıkayın.",
    ],
    "loreal-paris-dolgunlastirici-temizleme-jeli": [
        "Her sabah ve akşam nemli yüzünüze ve boynunuza küçük bir miktar uygulayın.",
        "Dairesel hareketlerle nazikçe masaj yapın.",
        "Su ile durulayın.",
    ],
    "loreal-paris-goz-maskesi": [
        "Paketi açın ve maskeyi temiz ve kuru göz çevresine uygulayın.",
        "Maskeyi nazikçe düzleştirin ve 15 dakika bekletin.",
        "Maskeyi çıkarın; fazla ürünü masaj yaparak cilde yedirin ya da bir pamukla temizleyin.",
    ],
    "loreal-paris-koyu-leke-karsiti-nemlendirici-krem-gkf-50": [
        "Kremi her gün temiz yüz ve boyun bölgesine uygulayın.",
        "Göz çevresinden kaçının.",
        "Yoğun ya da uzun süreli güneşe maruz kalacaksanız ayrıca güneş kremi kullanın.",
    ],
    "loreal-paris-lazer-x3-leke-ve-kirisiklik-karsiti-bakim-gkf-25": [
        "Güneşe çıkmadan önce, temizlenmiş yüzünüze her sabah uygulayın.",
        "Dairesel hareketlerle cilde masaj yapın.",
    ],
    "loreal-paris-lazer-x3-yaslanma-karsiti-goz-bakim-kremi": [
        "Sabah ve akşam kullanın.",
        "Tüpü sıkın ve bir damla alın.",
        "İçeriden dışarıya doğru, soğuk ucu kullanarak masaj yaparak uygulayın.",
    ],
    "loreal-paris-lazer-x3-yogun-yaslanma-karsiti-bakim-serum": [
        "Her sabah gündüz kreminizden, her akşam gece kreminizden önce ya da tek başına kullanın.",
        "Parmak uçlarınıza dökülen birkaç damlayı ufak dokunuşlarla uygulayın.",
    ],
    "loreal-paris-lazer-x3-yogun-yaslanma-karsiti-gunduz-bakim-kremi": [
        "Her sabah temizlenmiş yüz ve boyun bölgenize uygulayın.",
        "Daha iyi nüfuz etmesi için dairesel hareketlerle uygulayın.",
    ],
    "loreal-paris-nem-terapisi-aloe-vera-suyu-kuru-ve-hassas-ciltler": [
        "Her sabah ve akşam temiz ve kuru cildinize uygulayın.",
        "Yüzünüze ve boynunuza dairesel hareketlerle masaj yapın.",
    ],
    "loreal-paris-nem-terapisi-aloe-vera-suyu-normalden-kuruya-ciltler": [
        "Her sabah ve akşam temiz ve kuru cildinize uygulayın.",
        "Yüzünüze ve boynunuza dairesel hareketlerle masaj yapın.",
    ],
    "loreal-paris-nem-terapisi-aloe-vera": [
        "Her sabah ve akşam temiz ve kuru cildinize uygulayın.",
        "Yüzünüze ve boynunuza dairesel hareketlerle masaj yapın.",
    ],
    "loreal-paris-normal-ve-karma-ciltler-icin-temizleyici-tonik": [
        "Sabah ve akşam bir pamuk üzerine damlatın.",
        "Durulamaya ve ovalamaya gerek duymadan yüzünüze ve boynunuza uygulayın.",
        "Cildiniz tamamen temizlenene kadar işlemi tekrarlayın.",
    ],
    "loreal-paris-normal-ve-kuru-ciltler-icin-temizleyici-tonik": [
        "Sabah ve akşam bir pamuk üzerine damlatın.",
        "Durulamaya ve ovalamaya gerek duymadan yüzünüze ve boynunuza uygulayın.",
        "Cildiniz tamamen temizlenene kadar işlemi tekrarlayın.",
    ],
    "loreal-paris-revitalift-clinical-12-saf-c-vitamini-aydinlatici-serum": [
        "Cildinizi her zaman kullandığınız temizleyiciyle temizleyin.",
        "2-3 damla serumu yüz ve boyun bölgenize uygulayın.",
        "Sabahları en az 20 faktör güneş koruyucu kullanın.",
    ],
    "loreal-paris-revitalift-clinical-cleansing-gel": [
        "Her sabah ve akşam az miktarda ürünü ıslak yüzünüze dairesel hareketlerle masaj yaparak uygulayın.",
        "Suyla durulayın.",
    ],
    "loreal-paris-revitalift-clinical-uv-fluid-spf50": [
        "Kullanmadan önce çalkalayın.",
        "Her sabah nemlendirici yerine ya da UV koruması olarak uygulayın.",
        "Göz kapağına ve göz çevresine uygulanabilir.",
    ],
    "loreal-paris-revitalift-glycolic-cleansing-gel": [
        "Her sabah ve akşam nemli yüzünüze küçük bir miktar uygulayın.",
        "Dairesel hareketlerle nazikçe masaj yapın.",
        "Su ile durulayın.",
        "Gözlerle temasından kaçının; temas halinde bol su ile durulayın.",
    ],
    "loreal-paris-spot-fading-serum-icerikli-temizleme-jeli-150-ml": [
        "Sabah ve akşam ıslak cildinize az miktarda ürünü masaj yaparak uygulayın.",
        "Su ile durulayın.",
        "Göz çevresinden kaçının; gözle temas durumunda hemen su ile durulayın.",
    ],
    "loreal-paris-yas-uzmani-40-kirisiklik-karsiti-sikilastirici-goz-kremi": [
        "Her sabah ve akşam göz çevresine uygulayın.",
        "Ürün tamamen emilene kadar parmak uçlarınızla hafifçe masaj yapın.",
    ],
    "loreal-paris-yas-uzmani-40-kirisiklik-karsiti-sikilastirici-krem": [
        "Her gün iyice temizlenmiş yüz ve boyun bölgesine dairesel hareketlerle uygulayın.",
    ],
    "loreal-paris-yas-uzmani-50-kirisiklik-karsiti-yenileyici-krem": [
        "Her gün iyice temizlenmiş yüz ve boyun bölgesine dairesel hareketlerle uygulayın.",
    ],
    "loreal-paris-yas-uzmani-60-kirisiklik-karsiti-besleyici-krem": [
        "Her gün iyice temizlenmiş yüz ve boyun bölgesine dairesel hareketlerle uygulayın.",
    ],
}

NOTE = ("2026-11-13: kullanım talimatı denetim/kullanim_loreal_garnier_20261113.py'den (sayfadaki tek parça metin "
        "adımlara bölündü; başlık, ürün önerisi ve etki cümleleri çıkarıldı).")

if __name__ == "__main__":
    raw = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "raw")
    for slug, steps in HOWTO.items():
        f = os.path.join(raw, slug + ".json")
        d = json.load(open(f, encoding="utf8"))
        b = d["brandSite"]
        b["howTo"] = steps
        if NOTE not in (b.get("note") or ""):
            b["note"] = ((b.get("note") or "") + " " + NOTE).strip()
        json.dump(d, open(f, "w", encoding="utf8"), ensure_ascii=False, indent=1)  # fetch_sources.py biçimi
    print(len(HOWTO), "ürün yazıldı")
