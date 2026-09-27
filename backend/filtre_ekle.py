# -*- coding: utf-8 -*-
# =====================================================================
#  KATEGORİ FİLTRE (CategoryAttribute) KURULUM SCRIPTI  --  v3
#  Kullanım:  python manage.py shell < kategori_filtreleri_v3.py
# =====================================================================
from products.models import Category, CategoryAttribute
import re

print("=" * 62)
print(" KATEGORİ FİLTRE KURULUMU v3 - Bağlam Duyarlı Seçenekler")
print("=" * 62)

# =====================================================================
# 1) YARDIMCI FONKSİYONLAR
# =====================================================================

def norm(s):
    """Türkçe uyumlu normalizasyon.
    'İ' -> 'i', 'I' -> 'ı', kombine nokta (U+0307) temizliği."""
    if not s:
        return ""
    s = s.replace("\u0307", "")          # 'i̇' -> 'i'
    s = s.replace("İ", "i").replace("I", "ı")
    s = s.lower().strip()
    s = re.sub(r"\s+", " ", s)
    return s


OZEL_ISIMLER = {
    "spf": "SPF",
    "nfc": "NFC",
    "gps": "GPS",
    "usb": "USB",
    "ram (sistem belleği)": "RAM (Sistem Belleği)",
    "ram (sistem belleği) tipi": "RAM (Sistem Belleği) Tipi",
    "ram kapasitesi": "RAM Kapasitesi",
    "ssd kapasitesi": "SSD Kapasitesi",
    "pil gücü (mah)": "Pil Gücü (mAh)",
    "temel işlemci hızı (ghz)": "Temel İşlemci Hızı (GHz)",
    "ekran boyut (inç)": "Ekran Boyut (inç)",
    "güç (watt)": "Güç (Watt)",
    "bb & cc krem": "BB & CC Krem",
    "iç astar & iç taban materyali": "İç Astar & İç Taban Materyali",
    "bakım talimatları (gıda temas)": "Bakım Talimatları (Gıda Temas)",
    "far (ampul) tipleri": "Far (Ampul) Tipleri",
    "boy / ölçü": "Boy / Ölçü",
    "tutuculuk / sertlik": "Tutuculuk / Sertlik",
    "setli/tekil": "Setli/Tekil",
    "kemer/kuşak durumu": "Kemer/Kuşak Durumu",
    "suya/tere dayanıklılık": "Suya/Tere Dayanıklılık",
    "boyut/ebat": "Boyut/Ebat",
}


def _buyuk(c):
    if c == "i":
        return "İ"
    if c == "ı":
        return "I"
    return c.upper()


def baslik(s):
    """Türkçe uyumlu başlık formatı: 'paket i̇çeriği' -> 'Paket İçeriği'."""
    n = norm(s)
    if n in OZEL_ISIMLER:
        return OZEL_ISIMLER[n]
    out = []
    yeni = True
    for ch in n:
        if yeni and ch.isalpha():
            out.append(_buyuk(ch))
            yeni = False
        else:
            out.append(ch)
        if ch in " /&-(":
            yeni = True
    return "".join(out)


# 'secenekler' alanı CharField ise taşmasın diye otomatik kırpma
try:
    _MAX_LEN = CategoryAttribute._meta.get_field("secenekler").max_length
except Exception:
    _MAX_LEN = None


def kirp(sec):
    if not sec or not _MAX_LEN or len(sec) <= _MAX_LEN:
        return sec
    parcalar = [p.strip() for p in sec.split(",")]
    sonuc, toplam = [], 0
    for p in parcalar:
        ek = len(p) + (2 if sonuc else 0)
        if toplam + ek > _MAX_LEN:
            break
        sonuc.append(p)
        toplam += ek
    return ", ".join(sonuc)


# =====================================================================
# 2) TEKRAR KULLANILAN SEÇENEK BLOKLARI
# =====================================================================

RENK = ("Siyah, Beyaz, Gri, Antrasit, Ekru, Bej, Krem, Kahverengi, Taba, Vizon, "
        "Bordo, Kırmızı, Pembe, Pudra, Fuşya, Mor, Lila, Lacivert, Mavi, "
        "Bebe Mavisi, Turkuaz, Petrol, Yeşil, Haki, Mint, Sarı, Hardal, Turuncu, "
        "Somon, Altın, Gümüş, Rose Gold, Çok Renkli, Şeffaf")

METAL_RENK = ("Siyah, Beyaz, Gümüş, Altın, Rose Gold, Bronz, Bakır, Krom, "
              "Antrasit, Gri, Mavi, Yeşil, Bordo, Lacivert, Şampanya, Çok Renkli")

GIYIM_BEDEN = ("Tek Beden, XXS, XS, S, M, L, XL, XXL, 3XL, 4XL, 5XL, 6XL, "
               "32, 34, 36, 38, 40, 42, 44, 46, 48, 50, 52, 54, 56, 58, 60")

AYAKKABI_BEDEN = ("19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, "
                  "35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48")

COCUK_BEDEN = ("Yenidoğan, 0-3 Ay, 3-6 Ay, 6-9 Ay, 9-12 Ay, 12-18 Ay, 18-24 Ay, "
               "2-3 Yaş, 3-4 Yaş, 4-5 Yaş, 5-6 Yaş, 6-7 Yaş, 7-8 Yaş, 9-10 Yaş, "
               "11-12 Yaş, 13-14 Yaş, 56 cm, 62 cm, 68 cm, 74 cm, 80 cm, 86 cm, "
               "92 cm, 98 cm, 104 cm, 110 cm, 116 cm, 122 cm, 128 cm, 134 cm, "
               "140 cm, 146 cm, 152 cm")

BUYUK_BEDEN = ("XL, XXL, 3XL, 4XL, 5XL, 6XL, 7XL, 8XL, "
               "48, 50, 52, 54, 56, 58, 60, 62, 64, 66")

GIYIM_MATERYAL = ("Pamuk, Polyester, Viskon, Keten, Yün, Kaşmir, Akrilik, Elastan, "
                  "Modal, Tencel, Bambu, Naylon, Denim (Kot), İpek, Saten, Şifon, "
                  "Triko, Polar, Kadife, Dantel, Tül, Deri, Suni Deri, Süet, "
                  "Karışım (Mix)")

AYAKKABI_MATERYAL = ("Hakiki Deri, Suni Deri, Süet, Nubuk, Rugan, Tekstil, File, "
                     "Kanvas, Keten, Kauçuk, EVA, Sentetik, Keçe, Saten, Kürk")

CANTA_MATERYAL = ("Hakiki Deri, Suni Deri, Süet, Nubuk, Rugan, Kanvas, Keten, "
                  "Kumaş, Polyester, Naylon, Hasır, Jüt, Simli, Vegan Deri, "
                  "Polikarbon (Valiz), ABS (Valiz)")

EV_MATERYAL = ("Ahşap, Masif Ahşap, MDF, Sunta, Metal, Çelik, Paslanmaz Çelik, "
               "Alüminyum, Cam, Plastik, Polyester, Mermer, Seramik, Porselen, "
               "Rattan, Bambu, Hasır, Kumaş, Deri, Suni Deri, Beton")

MUTFAK_MATERYAL = ("Paslanmaz Çelik, Granit, Döküm, Teflon, Seramik, Porselen, "
                   "Cam, Borosilikat Cam, Emaye, Alüminyum, Bakır, Çelik, Bambu, "
                   "Ahşap, Plastik, Silikon, Melamin")

TAKI_MATERYAL = ("925 Ayar Gümüş, 8 Ayar Altın, 14 Ayar Altın, 18 Ayar Altın, "
                 "22 Ayar Altın, Çelik, Titanyum, Pirinç, Bakır, Alaşım, "
                 "Altın Kaplama, Gümüş Kaplama, Deri, Ahşap, Doğal Taş, İnci")

BOYUT_KUCUK_BUYUK = "Mini, Küçük, Orta, Büyük, Extra Büyük (XL)"

SAYI_1_10 = "1, 2, 3, 4, 5, 6, 7, 8, 9, 10 ve üzeri"


# =====================================================================
# 3) EVET / HAYIR (BOOLEAN) FİLTRELER
# =====================================================================
BOOLEAN_FILTRELER = {
    "nfc", "hızlı şarj", "dokunmatik ekran", "parmak izi okuyucu", "gps",
    "yedek batarya", "beni takip et modu", "sivil havacılık izni", "çift hat",
    "yapay zeka", "sesli görüşme", "kalemle not alma", "çift yönlü kullanım",
    "tek elle kapama", "ayak örtüsü", "yağmurluk", "yavrulu yatak",
    "sallanma fonksiyonu", "dim özelliği", "usb", "kısırlaştırılmış",
    "enerji tasarrufu", "refill", "yaşlanma karşıtı", "suya/tere dayanıklılık",
    "tamir edilebilirlik",
}


# =====================================================================
# 4) GENEL SEÇENEKLER  (bağlamdan bağımsız, her yerde aynı anlama gelenler)
# =====================================================================
GENEL_SECENEKLER = {

    # ---------- TEMEL ----------
    "cinsiyet": "Kadın, Erkek, Unisex, Kız Çocuk, Erkek Çocuk, Bebek",
    "çocuk cinsiyeti": "Kız, Erkek, Unisex",
    "renk": RENK,
    "beden": GIYIM_BEDEN,
    "materyal": GIYIM_MATERYAL,
    "yaş": ("0-3 Ay, 3-6 Ay, 6-9 Ay, 9-12 Ay, 12-18 Ay, 18-24 Ay, 2-3 Yaş, "
            "3-4 Yaş, 4-5 Yaş, 5-6 Yaş, 6-8 Yaş, 8-10 Yaş, 10-12 Yaş, "
            "12-14 Yaş, 14+ Yaş, Yetişkin"),
    "sezon": "İlkbahar/Yaz, Sonbahar/Kış, Dört Mevsim",
    "boyut": BOYUT_KUCUK_BUYUK,
    "boyut/ebat": "Tek Ebat, XS, S, M, L, XL, XXL, Küçük, Orta, Büyük",

    # ---------- GİYİM DETAY ----------
    "kalıp": ("Dar (Slim Fit), Normal (Regular Fit), Bol (Oversize), "
              "Rahat (Relaxed Fit), Vücuda Oturan (Bodycon), Süper Dar (Skinny), "
              "Salaş, Crop"),
    "boy": ("Crop (Kısa), Standart, Uzun, Mini, Midi, Maxi, Diz Üstü, Diz Altı, "
            "Bilek Boy, Tunik Boy"),
    "yaka tipi": ("Bisiklet Yaka, V Yaka, Polo Yaka, Hakim Yaka, Balıkçı Yaka, "
                  "Kare Yaka, Kayık Yaka, Halter Yaka, Gömlek Yaka, Dik Yaka, "
                  "Şal Yaka, Bebe Yaka, Kalp Yaka, Degaje Yaka, Kruvaze, "
                  "Kapüşonlu, Fermuarlı Yaka, Straplez, Yakasız"),
    "kol tipi": ("Kısa Kol, Uzun Kol, Kolsuz, Askılı, Truvakar Kol, Balon Kol, "
                 "Karpuz Kol, Yarasa Kol, Reglan Kol, Volanlı Kol, Straplez, "
                 "Düşük Omuz"),
    "kol boyu": ("Kolsuz, Askılı, Kısa Kol, Yarım Kol, Truvakar (3/4 Kol), "
                 "Uzun Kol"),
    "bel": ("Yüksek Bel, Normal Bel, Düşük Bel, Beli Lastikli, "
            "Ayarlanabilir Bel, Belden Bağlamalı"),
    "paça tipi": ("Dar Paça, Boru Paça, İspanyol Paça, Bol Paça, Lastikli Paça, "
                  "Duble Paça, Jogger Paça, Havuç Paça, Palazzo, Yırtmaçlı Paça"),
    "paça boyu": "Şort, Capri, Bilek Boy, Normal, Uzun, Kısa",
    "siluet": ("Düz Kesim, Dar, Normal, Bol, A Kesim, Kalem, Kloş, Pileli, "
               "Balon, Volanlı, Asimetrik, Yırtmaçlı, Peplum"),
    "alt siluet": ("Slip, Bikini, String, Tanga, Hipster, Boxer, Şort, "
                   "Yüksek Bel, Brazilian"),
    "üst siluet": ("Balenli, Balensiz, Dolgulu, Dolgusuz, Push Up, Bralet, "
                   "Büstiyer, Sporcu Sütyeni, Kaplı, Dantelli"),
    "kap": "A, B, C, D, DD, E, F, G, Kapsız",
    "kumaş tipi": ("Pamuklu, Keten, Polyester, Viskon, Denim (Kot), Şifon, "
                   "Triko, Polar, Kadife, Saten, İpek, Yün, Kaşmir, Süprem, "
                   "Ribana, İnterlok, İki İplik, Üç İplik, Gabardin, Krep, Tül, "
                   "Dantel, Paraşüt, File, Softshell, Simli"),
    "kumaş özellik": ("Esnek, Nefes Alabilir, Antibakteriyel, Su İtici, "
                      "Ütü Gerektirmez, Çekmez, Terletmez, Yumuşak Dokulu"),
    "kumaş teknolojisi": ("Gore-Tex, Dry-Fit (Nem Emici), Nefes Alabilir, "
                          "Su İtici, Su Geçirmez, Rüzgar Geçirmez, Termal, "
                          "Antibakteriyel, UV Korumalı, Hızlı Kuruma, Softshell"),
    "dokuma tipi": ("Örme, Dokuma, Triko, Denim, Dantel, Jakarlı, Keçe, "
                    "Non-woven, El Örgüsü"),
    "desen": ("Düz Renk, Çizgili, Ekose, Kareli, Çiçekli, Baskılı, Puantiyeli, "
              "Geometrik, Leopar, Zebra, Yılan Derisi, Kamuflaj, Etnik, Batik, "
              "Yazı/Slogan, Soyut, Hayvan Figürlü, Nakışlı, Simli"),
    "kapama şekli": ("Fermuarlı, Düğmeli, Çıtçıtlı, Cırt Cırtlı, Bağcıklı, "
                     "Mıknatıslı, Tokalı, Lastikli, Kuşaklı, Kapamasız"),
    "cep": "Cepli, Cepsiz, Fermuarlı Cepli, Gizli Cepli, Kargo Cepli",
    "astar durumu": "Astarlı, Astarsız, Çıkarılabilir Astarlı, İçi Kürklü",
    "kemer/kuşak durumu": "Kemerli, Kemersiz, Çıkarılabilir Kemerli, Kuşaklı",
    "kutu durumu": "Kutulu, Kutusuz, Özel Hediye Kutulu",
    "dolgu materyali": ("Kaz Tüyü, Ördek Tüyü, Suni Elyaf, Silikon Elyaf, "
                        "Polyester Dolgu, Sünger, Şişme (Puf), Yün, Dolgusuz"),
    "kalınlık": "İnce, Orta Kalınlık, Kalın, Ekstra Kalın",
    "parça sayısı": "1 Parça, 2 Parça, 3 Parça, 4 Parça, 5 Parça, 6 ve üzeri",
    "paket içeriği": ("1'li, 2'li, 3'lü, 4'lü, 5'li, 6'lı, 8'li, 10'lu, 12'li, "
                      "24'lü"),
    "adet": "1, 2, 3, 4, 5, 6, 8, 10, 12, 24, 50, 100",
    "set içerik adeti": "1, 2, 3, 4, 5, 6, 7 ve üzeri",
    "kapasite": ("5 L altı, 5-10 L, 10-20 L, 20-30 L, 30-40 L, 40-60 L, "
                 "60 L ve üzeri"),
    "yükseklik": ("20 cm altı, 20-40 cm, 40-60 cm, 60-80 cm, 80-100 cm, "
                  "100-140 cm, 140-180 cm, 180 cm ve üzeri"),
    "genişlik": ("20 cm altı, 20-40 cm, 40-60 cm, 60-80 cm, 80-100 cm, "
                 "100-140 cm, 140-180 cm, 180 cm ve üzeri"),
    "derinlik": ("20 cm altı, 20-30 cm, 30-40 cm, 40-50 cm, 50-60 cm, "
                 "60 cm ve üzeri"),
    "ölçü": ("10 cm altı, 10-30 cm, 30-50 cm, 50-80 cm, 80-120 cm, "
             "120-180 cm, 180 cm ve üzeri"),
    "fonksiyon": ("Sabit, Katlanır, Açılır, Ayarlanabilir, Çok Fonksiyonlu, "
                  "Otomatik, Manuel"),
    "ek özellik": ("Cepli, Kapüşonlu, Fermuarlı, Astarlı, Yırtmaçlı, Fırfırlı, "
                   "Nakışlı, Simli, Esnek, Su İtici, Nefes Alabilir, "
                   "Antibakteriyel, Ütü Gerektirmez, Termal, Reflektörlü, "
                   "Çıkarılabilir Kapüşon"),
    "özellik": ("Su Geçirmez, Nefes Alabilir, Antibakteriyel, Katlanabilir, "
                "Ayarlanabilir, Taşınabilir, Işıklı, Sesli, Kaymaz, "
                "Isıya Dayanıklı, Yıkanabilir, Şarjlı, Hediye Kutulu"),
    "sürdürülebilirlik detayı": ("Organik Pamuk, Geri Dönüştürülmüş Pamuk, "
                                 "Geri Dönüştürülmüş Polyester, "
                                 "Geri Dönüştürülmüş Malzeme, Vegan Ürün, "
                                 "Sertifikalı (GOTS/OEKO-TEX), "
                                 "Su Tasarruflu Üretim, Doğal Malzeme, "
                                 "Belirtilmemiş"),
    "persona": "Klasik, Spor, Şık, Günlük, Trend, Basic",

    # ---------- AYAKKABI ----------
    "topuk boyu": ("Düz (0-1 cm), Kısa (1-4 cm), Orta (5-9 cm), "
                   "Yüksek (10 cm ve üzeri)"),
    "topuk tipi": ("Topuksuz, İnce Topuk (Stiletto), Kalın Topuk, Dolgu Topuk, "
                   "Kama Topuk, Platform, Kütük Topuk, Gizli Topuk"),
    "burun tipi": ("Sivri Burun, Yuvarlak Burun, Küt Burun, Kare Burun, "
                   "Badem Burun, Açık Burun, Çelik Burun"),
    "bağlama şekli": ("Bağcıklı, Bağcıksız, Cırt Cırtlı, Fermuarlı, Tokalı, "
                      "Lastikli, Çıtçıtlı, Slip-On (Geçmeli)"),
    "taban tipi": ("Düz Taban, Kauçuk Taban, EVA Taban, Phylon Taban, "
                   "Hava Yastıklı Taban, Amortisörlü, Ortopedik Taban, "
                   "Kaymaz Taban, Platform Taban, Dişli Taban"),
    "taban teknolojisi": ("Vibram, Gore-Tex Taban, Hava Yastığı, Amortisörlü, "
                          "Kaymaz (Anti-Slip), Şok Emici, Ortopedik"),
    "alt taban materyali": ("Kauçuk, EVA, PU (Poliüretan), TPR, Termo Kauçuk, "
                            "Fiber, Deri, Phylon"),
    "iç astar & iç taban materyali": ("Deri, Suni Deri, Tekstil, Kürk, Keçe, "
                                      "Memory Foam, Ortopedik Astar, Jel, "
                                      "Antibakteriyel Astar"),
    "dış materyal": AYAKKABI_MATERYAL,
    "kullanım alanı": ("Günlük, Spor, Klasik, Outdoor, Koşu, Yürüyüş, Ev, "
                       "Plaj, İş, Özel Gün/Abiye, Kış, Trekking"),
    "spor branşı": ("Futbol, Basketbol, Voleybol, Koşu, Fitness, Tenis, Yüzme, "
                    "Bisiklet, Kayak, Dağcılık, Yoga, Boks, Hentbol"),

    # ---------- SAAT ----------
    "kordon materyali": ("Çelik, Paslanmaz Çelik, Hakiki Deri, Suni Deri, "
                         "Silikon, Kauçuk, Kumaş, Naylon, Hasır (Milano), "
                         "Seramik, Titanyum, Plastik"),
    "kasa materyali": ("Paslanmaz Çelik, Çelik, Alüminyum, Titanyum, Seramik, "
                       "Plastik, Pirinç, Altın Kaplama, Karbon Fiber"),
    "mekanizma": ("Quartz (Pilli), Otomatik, Mekanik (Kurmalı), Dijital, "
                  "Akıllı (Smart), Kronograf, Solar, Kinetik"),
    "cam tipi": ("Mineral Cam, Safir Cam, Akrilik (Plastik) Cam, Hardlex, "
                 "Temperli Cam, Polarize, UV400, Anti-Reflekte, "
                 "Mavi Işık Filtreli, Fotokromik"),
    "cam şekli": ("Yuvarlak, Kare, Dikdörtgen, Oval, Tonneau, Düz, Kavisli"),
    "cam renk": ("Siyah, Gri, Kahverengi, Yeşil, Mavi, Sarı, Pembe, Aynalı, "
                 "Degrade, Şeffaf, Fotokromik, Turuncu"),
    "cam materyali": ("Organik (CR-39), Mineral (Cam), Polikarbon, Nylon, "
                      "Trivex"),
    "kasa çapı": ("28 mm ve altı, 28-32 mm, 32-36 mm, 36-40 mm, 40-44 mm, "
                  "44 mm ve üzeri"),
    "kasa renk": METAL_RENK,
    "kordon renk": RENK,
    "kadran renk": METAL_RENK,
    "kordon boyutu": "S/M, M/L, 18 mm, 20 mm, 22 mm, Ayarlanabilir",
    "ekartman": "12 mm, 14 mm, 16 mm, 18 mm, 20 mm, 22 mm, 24 mm, 26 mm",
    "su geçirmezlik": ("Suya Dayanıklı Değil, Suya Dayanıklı, 3 ATM (30 m), "
                       "5 ATM (50 m), 10 ATM (100 m), 20 ATM (200 m), "
                       "IP67, IP68"),
    "garanti süresi": ("Garanti Yok, 6 Ay, 1 Yıl, 2 Yıl, 3 Yıl, 4 Yıl, 5 Yıl, "
                       "10 Yıl, Ömür Boyu"),
    "garanti tipi": ("İthalatçı Garantili, Resmi Distribütör Garantili, "
                     "Üretici Garantili, Yurt Dışı Garantili, Garantisiz"),
    "batarya türü": ("Lityum (Li-ion), Alkalin, Çinko, Şarj Edilebilir, "
                     "Güneş Enerjili, Pilsiz"),
    "batarya boyutu": ("CR2016, CR2025, CR2032, SR621SW, SR626SW, LR44, AA, "
                       "AAA, 18650"),

    # ---------- GÖZLÜK ----------
    "çerçeve formu": ("Yuvarlak, Kare, Dikdörtgen, Oval, Kelebek, Kedi Gözü, "
                      "Aviator (Damla), Pilot, Altıgen, Maske, Yarım Ay"),
    "çerçeve materyali": ("Metal, Asetat, Plastik, Titanyum, Paslanmaz Çelik, "
                          "TR90, Ahşap, Alüminyum"),
    "çerçeve tipi": ("Tam Çerçeve, Yarım Çerçeve, Çerçevesiz, Ahşap Çerçeve, "
                     "Metal Çerçeve, Plastik Çerçeve"),
    "çerçeve renk": METAL_RENK,

    # ---------- TAKI ----------
    "ayar": ("8 Ayar, 14 Ayar, 18 Ayar, 22 Ayar, 24 Ayar, 925 Ayar Gümüş, "
             "950 Ayar, Çelik, Kaplama"),
    "taş cinsi": ("Taşsız, Pırlanta, Zirkon, Swarovski, İnci, Yakut, Zümrüt, "
                  "Safir, Ametist, Akik, Oniks, Opal, Turkuaz, Kristal, "
                  "Doğal Taş"),

    # ---------- ÇANTA / CÜZDAN ----------
    "çanta tipi": ("Sırt Çantası, El Çantası, Omuz Çantası, Çapraz Çanta, "
                   "Postacı Çantası, Evrak Çantası, Laptop Çantası, "
                   "Bel Çantası, Tote Çanta, Portföy, Valiz"),
    "deri kalitesi": ("Hakiki Deri, Suni Deri (PU), Vegan Deri, Nubuk, Süet, "
                      "Rugan, Floter Deri"),
    "ekran boyut aralığı": ("11 inç ve altı, 12 inç, 13 inç, 14 inç, 15 inç, "
                            "16 inç, 17 inç ve üzeri"),
    "dosya tipi": "A4, A5, Körüklü, Zarf Tipi, Evrak Bölmeli, Çok Bölmeli",

    # ---------- KOZMETİK ----------
    "cilt tipi": ("Tüm Cilt Tipleri, Kuru, Yağlı, Karma, Normal, Hassas, "
                  "Akneye Eğilimli, Olgun Cilt"),
    "saç tipi": ("Tüm Saç Tipleri, Düz, Dalgalı, Kıvırcık, Afro, İnce Telli, "
                 "Kalın Telli, Boyalı, Yağlı, Kuru, Yıpranmış, Kepekli, Normal"),
    "koku türü": ("Çiçeksi, Odunsu, Oryantal, Ferah (Fresh), Narenciye, "
                  "Meyvemsi, Baharatlı, Aromatik, Pudramsı, Vanilyalı, "
                  "Deniz (Aquatic), Fougere, Misk, Tatlı (Gourmand)"),
    "kalıcılık": ("2-4 Saat, 4-8 Saat, 8-12 Saat, 12-24 Saat, "
                  "24 Saat ve üzeri, Uzun Süre Kalıcı"),
    "spf": "SPF Yok, SPF 15, SPF 20, SPF 30, SPF 50, SPF 50+",
    "kapatıcılık": "Hafif, Orta, Yüksek, Tam Kapatıcılık",
    "görünüm": "Mat, Parlak, Saten, Işıltılı, Doğal, Nemli (Dewy)",
    "etki": ("Nemlendirici, Onarıcı, Güçlendirici, Hacim Verici, "
             "Renk Koruyucu, Kepek Karşıtı, Dökülme Karşıtı, Şekillendirici, "
             "Parlaklık Verici, Düzleştirici, Besleyici, Hacim Azaltıcı"),
    "fırça kılı sertliği": "Ekstra Yumuşak, Yumuşak, Orta, Sert",
    "fırça tipi": ("Fondöten Fırçası, Pudra Fırçası, Allık Fırçası, "
                   "Far Fırçası, Kapatıcı Fırçası, Ruj Fırçası, Kaş Fırçası, "
                   "Süngerli Aplikatör, Fırça Seti"),
    "kıl tipi": "Doğal Kıl, Sentetik Kıl, Karışık",
    "tutuculuk / sertlik": "Hafif, Orta, Güçlü, Ekstra Güçlü",
    "koruma süresi": "24 Saat, 48 Saat, 72 Saat, 96 Saat ve üzeri",
    "bıçak sayısı": "1, 2, 3, 4, 5, 6",
    "mama numarası": ("1 Numara (0-6 Ay), 2 Numara (6-12 Ay), "
                      "3 Numara (12+ Ay), 4 Numara, 5 Numara"),

    # ---------- ELEKTRONİK ----------
    "ram (sistem belleği)": ("2 GB, 4 GB, 6 GB, 8 GB, 12 GB, 16 GB, 24 GB, "
                             "32 GB, 64 GB, 128 GB"),
    "ram kapasitesi": ("2 GB, 3 GB, 4 GB, 6 GB, 8 GB, 12 GB, 16 GB, 24 GB, "
                       "32 GB"),
    "ram (sistem belleği) tipi": "DDR3, DDR4, DDR5, LPDDR4X, LPDDR5, LPDDR5X",
    "ssd kapasitesi": ("SSD Yok, 128 GB, 256 GB, 512 GB, 1 TB, 2 TB, 4 TB"),
    "hard disk kapasitesi": "HDD Yok, 500 GB, 1 TB, 2 TB, 4 TB, 8 TB",
    "sabit disk": "500 GB, 825 GB, 1 TB, 2 TB, 4 TB",
    "dahili hafıza": ("16 GB, 32 GB, 64 GB, 128 GB, 256 GB, 512 GB, 1 TB"),
    "işletim sistemi": ("Windows 11, Windows 10, macOS, Linux, FreeDOS, "
                        "Android, iOS, iPadOS, Chrome OS, İşletim Sistemsiz"),
    "işlemci tipi": ("Intel Celeron, Intel Pentium, Intel Core i3, "
                     "Intel Core i5, Intel Core i7, Intel Core i9, "
                     "Intel Core Ultra, AMD Ryzen 3, AMD Ryzen 5, "
                     "AMD Ryzen 7, AMD Ryzen 9, Apple M1, Apple M2, Apple M3, "
                     "Snapdragon, MediaTek, Exynos"),
    "işlemci nesli": ("7. Nesil, 8. Nesil, 9. Nesil, 10. Nesil, 11. Nesil, "
                      "12. Nesil, 13. Nesil, 14. Nesil"),
    "işlemci çekirdek sayısı": "2, 4, 6, 8, 10, 12, 14, 16, 20, 24 ve üzeri",
    "temel işlemci hızı (ghz)": ("2.0 GHz altı, 2.0-2.5 GHz, 2.5-3.0 GHz, "
                                 "3.0-3.5 GHz, 3.5 GHz üzeri"),
    "ekran kartı": ("Dahili (Paylaşımlı), Intel UHD, Intel Iris Xe, "
                    "NVIDIA GTX 1650, NVIDIA RTX 3050, RTX 3060, RTX 4050, "
                    "RTX 4060, RTX 4070, RTX 4080, RTX 4090, AMD Radeon"),
    "ekran kartı hafızası": ("Paylaşımlı, 2 GB, 4 GB, 6 GB, 8 GB, 12 GB, "
                             "16 GB, 24 GB"),
    "ekran kartı bellek tipi": "GDDR5, GDDR6, GDDR6X, HBM2, Paylaşımlı",
    "ekran kartı gücü": "60 W, 75 W, 90 W, 105 W, 115 W, 130 W, 150 W, 175 W",
    "ekran boyutu": ("6 inç ve altı, 6-7 inç, 7-9 inç, 10-11 inç, 12-13 inç, "
                     "14 inç, 15.6 inç, 16 inç, 17 inç ve üzeri"),
    "ekran yenileme hızı": ("60 Hz, 75 Hz, 90 Hz, 120 Hz, 144 Hz, 165 Hz, "
                            "240 Hz, 360 Hz"),
    "çözünürlük": ("HD (1366x768), Full HD (1920x1080), 2K (2560x1440), "
                   "4K (3840x2160), 8K, Retina"),
    "panel tipi": "IPS, TN, VA, OLED, AMOLED, Mini LED, Retina, LCD",
    "optik sürücü tipi": "Optik Sürücü Yok, DVD-RW, Blu-Ray",
    "pil gücü (mah)": ("3000 mAh altı, 3000-4000 mAh, 4000-5000 mAh, "
                       "5000-6000 mAh, 6000 mAh üzeri"),
    "mobil bağlantı hızı": "3G, 4G, 4.5G, 5G",
    "kamera çözünürlüğü": ("8 MP, 12 MP, 16 MP, 32 MP, 48 MP, 50 MP, 64 MP, "
                           "108 MP, 200 MP"),
    "ön kamera sayısı": "1, 2, 3",
    "kozmetik durum": ("Sıfır, Yenilenmiş - Mükemmel, Yenilenmiş - Çok İyi, "
                       "Yenilenmiş - İyi, İkinci El"),
    "bağlantı tipi": ("Type-C, Micro USB, Lightning, USB-A, HDMI, "
                      "3.5 mm Jack, Bluetooth, Wi-Fi, Kablosuz"),
    "bağlantılar": "Wi-Fi, Wi-Fi + Bluetooth, Wi-Fi + 4G, USB-C, Micro USB",
    "uyumlu marka": ("Apple, Samsung, Xiaomi, Huawei, Oppo, Vivo, Realme, "
                     "Honor, General Mobile, Reeder, Tüm Markalar"),
    "cihaz ağırlığı": ("1 kg altı, 1-1.5 kg, 1.5-2 kg, 2-2.5 kg, 2.5 kg üzeri"),
    "şarjlı kullanım süresi": ("4 saate kadar, 4-6 saat, 6-8 saat, 8-10 saat, "
                               "10 saat ve üzeri"),
    "kol sayısı": "Kolsuz, 1 Kol, 2 Kol, 3 Kol",
    "uçuş süresi": ("10 dk altı, 10-20 dk, 20-30 dk, 30-40 dk, 40 dk üzeri"),
    "uçuş mesafesi": ("100 m altı, 100-500 m, 500 m - 1 km, 1-5 km, "
                      "5 km ve üzeri"),
    "kamera özelliği": ("Kamerasız, HD, Full HD, 2.7K, 4K, 6K, "
                        "Gimbal Stabilizatörlü, Gece Görüşlü"),

    # ---------- OYUNCU KOLTUĞU / MOBİLYA MEKANİK ----------
    "sırt mekanizması": ("Sabit, 90-135° Yatar, 90-180° Yatar, "
                         "Salıncak Mekanizmalı, Ayarlanabilir"),
    "kol desteği": ("Kolçaksız, Sabit Kolçak, 2D Ayarlanabilir, "
                    "3D Ayarlanabilir, 4D Ayarlanabilir"),
    "oturak derinliği": "45 cm altı, 45-50 cm, 50-55 cm, 55 cm üzeri",
    "ayak malzemesi": "Ahşap, Metal, Krom, Alüminyum, Plastik, Paslanmaz Çelik",
    "gövde materyali": ("Suntalam, MDF, Masif Ahşap, Sunta, Kontrplak, Metal, "
                        "Plastik, Cam"),
    "raf sayısı": "1, 2, 3, 4, 5, 6, 7 ve üzeri",
    "kapak sayısı": "Kapaksız, 1, 2, 3, 4, 5, 6 ve üzeri",
    "bölme sayısı": "1, 2, 3, 4, 5, 6, 8, 10 ve üzeri",
    "sandalye sayısı": "2, 4, 6, 8, 10, 12",
    "sandalye ve bank sayısı": ("2 Sandalye, 4 Sandalye, 6 Sandalye, "
                                "8 Sandalye, 4 Sandalye + Bank, "
                                "6 Sandalye + Bank"),
    "sandalye kumaşı": ("Keten, Kadife, Chenille, Babyface, Suni Deri, "
                        "Hakiki Deri, Nubuk, Silinebilir Kumaş"),
    "kumaş": ("Keten, Kadife, Chenille, Babyface, Suni Deri, Hakiki Deri, "
              "Nubuk, Jakarlı, Silinebilir Kumaş"),
    "masa fonksiyonu": ("Sabit, Açılır, Katlanır, Yükseklik Ayarlı, "
                        "Uzatılabilir"),
    "masa ölçüsü": ("70x110 cm, 80x80 cm, 80x120 cm, 80x140 cm, 90x160 cm, "
                    "100x180 cm, 120x200 cm"),

    # ---------- AYDINLATMA ----------
    "duy tipi": "E27, E14, GU10, G9, GU5.3, B22, T8, Entegre LED",
    "renk sıcaklığı": ("Gün Işığı (3000K), Ilık Beyaz (4000K), "
                       "Beyaz Işık (6500K), Ayarlanabilir, RGB"),
    "ampul teknolojisi": ("LED, Flöresan, Halojen, Akkor, "
                          "Enerji Tasarruflu, Akıllı Ampul"),
    "ampül başlık sayısı": "1, 2, 3, 4, 5, 6, 8, 12 ve üzeri",
    "güç (watt)": ("500 W altı, 500-1000 W, 1000-1500 W, 1500-2000 W, "
                   "2000 W ve üzeri"),
    "çalışma tipi": ("Elektrikli (Fişli), Pilli, Şarjlı, Solar (Güneş Enerjili), "
                     "USB'li, Kablosuz"),

    # ---------- EV TEKSTİLİ / DEKORASYON ----------
    "çarşaf türü": ("Düz Çarşaf, Lastikli Çarşaf, Nevresim Takımı, Pike, "
                    "Yatak Örtüsü, Alez"),
    "şekil": ("Yuvarlak, Kare, Dikdörtgen, Oval, Kalp, Altıgen, Yıldız, "
              "Düzensiz (Organik)"),
    "çiçek türü": ("Gül, Orkide, Lale, Papatya, Şakayık, Lavanta, Sukulent, "
                   "Yapay Çiçek, Kuru Çiçek, Karışık"),
    "koku aroması": ("Lavanta, Vanilya, Gül, Yasemin, Okyanus, Tarçın, Limon, "
                     "Misk, Kahve, Odunsu, Çamaşır, Kokusuz"),
    "üretim şekli": "El Yapımı, Makine Üretimi, Baskılı, Dokuma, 3D Baskı",
    "iç materyal": ("Granit, Teflon, Seramik, Paslanmaz Çelik, Döküm, Emaye, "
                    "Titanyum, Mermer Kaplama"),
    "bakım talimatları (gıda temas)": ("Bulaşık Makinesinde Yıkanabilir, "
                                       "Elde Yıkanmalı, Fırına Girebilir, "
                                       "Mikrodalgaya Uygun, Dondurucuya Uygun, "
                                       "İndüksiyona Uygun"),
    "kişi sayısı": ("1 Kişilik, 2 Kişilik, 4 Kişilik, 6 Kişilik, 8 Kişilik, "
                    "12 Kişilik, 24 Kişilik"),

    # ---------- KİTAP / KIRTASİYE ----------
    "roman türü": ("Polisiye, Bilim Kurgu, Fantastik, Aşk/Romantik, Tarihi, "
                   "Macera, Gerilim, Klasik, Dram, Korku, Distopya, Öykü, "
                   "Şiir, Deneme, Biyografi"),
    "basım dili": ("Türkçe, İngilizce, Almanca, Fransızca, Arapça, İspanyolca, "
                   "Rusça, Osmanlıca, İtalyanca"),
    "sınıf": ("Okul Öncesi, 1. Sınıf, 2. Sınıf, 3. Sınıf, 4. Sınıf, 5. Sınıf, "
              "6. Sınıf, 7. Sınıf, 8. Sınıf, 9. Sınıf, 10. Sınıf, 11. Sınıf, "
              "12. Sınıf, Mezun, Üniversite"),
    "sınav tipi": ("LGS, TYT, AYT, YKS, YDT, KPSS, ALES, DGS, YDS, Bursluluk, "
                   "Açık Öğretim"),
    "kitap içeriği": ("Konu Anlatımlı, Soru Bankası, Deneme Sınavı, "
                      "Yaprak Test, Föy, Özet, Video Çözümlü, Etkinlik"),
    "cilt bilgisi": ("Ciltli, Ciltsiz, Karton Kapak, Sert Kapak, Spiralli, "
                     "Deri Cilt"),
    "setli/tekil": "Setli, Tekil",
    "sayfa sayısı": ("100 sayfa altı, 100-200 sayfa, 200-300 sayfa, "
                     "300-500 sayfa, 500 sayfa üzeri"),
    "basım yılı": ("2019 ve öncesi, 2020, 2021, 2022, 2023, 2024, 2025, 2026"),
    "ders": ("Matematik, Geometri, Türkçe, Edebiyat, Fen Bilimleri, Fizik, "
             "Kimya, Biyoloji, Tarih, Coğrafya, İngilizce, Felsefe, "
             "Din Kültürü, Sosyal Bilgiler, Hayat Bilgisi"),
    "kağıt boyutu": "A3, A4, A5, A6, B5, 13x21 cm, 17x24 cm, 19x27 cm",
    "sayfa tipi": "Çizgili, Kareli, Düz (Çizgisiz), Noktalı, Milimetrik",
    "defter tipi": ("Spiralli Defter, Dikişli Defter, Bloknot, Ajanda, "
                    "Sert Kapak Defter, PP Kapak Defter"),
    "kapak türü": ("Sert Kapak, Karton Kapak, Plastik Kapak, PP Kapak, "
                   "Deri Kapak"),
    "tel tipi": "Spiralli, Telli, Tel Dikiş, Telsiz",
    "kağıt tipi": ("1. Hamur, 2. Hamur, Kuşe, Kraft, Sarı Samanı, "
                   "Resim Kağıdı, Fotokopi Kağıdı, Asitsiz"),
    "kalem ucu boyutu": "0.3 mm, 0.5 mm, 0.7 mm, 0.9 mm, 1.0 mm, 1.2 mm",

    # ---------- OTOMOBİL ----------
    "jant çapı": ("12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22"),
    "jant": ("12 Jant, 16 Jant, 20 Jant, 24 Jant, 26 Jant, 27.5 Jant, "
             "28 Jant, 29 Jant"),
    "kesit oranı": "30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80",
    "taban genişliği": ("155, 165, 175, 185, 195, 205, 215, 225, 235, 245, "
                        "255, 265, 275, 285"),
    "mevsim": "Yaz Lastiği, Kış Lastiği, 4 Mevsim Lastiği",
    "yakıt tipi": "Benzin, Dizel, LPG, Hibrit, Elektrikli",
    "araç tipi": ("Otomobil, SUV, Hafif Ticari, Kamyonet, Minibüs, Motosiklet, "
                  "Traktör, Karavan"),
    "hız endeksi": ("Q (160 km/s), R (170 km/s), S (180 km/s), T (190 km/s), "
                    "H (210 km/s), V (240 km/s), W (270 km/s), Y (300 km/s)"),
    "yük endeksi": ("75, 80, 85, 88, 91, 94, 95, 98, 100, 102, 105, 108"),
    "islak zeminde frenleme": "A, B, C, D, E",
    "yakıt verimliliği": "A, B, C, D, E",
    "gürültü seviyesi": "65 dB, 67 dB, 69 dB, 70 dB, 71 dB, 72 dB, 73 dB",
    "paspas türleri": ("Kauçuk Paspas, Havuzlu Paspas, 3D Paspas, Halı Paspas, "
                       "Deri Paspas, Bagaj Paspası"),
    "far (ampul) tipleri": ("H1, H3, H4, H7, H11, H15, HB3, HB4, D1S, D2S, "
                            "D3S, D4S, LED, Xenon"),
    "ekran boyut (inç)": "7 inç, 9 inç, 10 inç, 10.1 inç, 12 inç, 13 inç",
    "araç motor hacmi": ("1.0, 1.2, 1.3, 1.4, 1.5, 1.6, 1.8, 2.0, 2.5, "
                         "3.0 ve üzeri"),
    "motor teknolojisi": ("Benzinli, Dizel, Hibrit, Plug-in Hibrit, "
                          "Elektrikli, LPG'li"),
    "yedek parça tipi": "Orijinal, Muadil, Yan Sanayi, Yenilenmiş",
    "teyp özellikleri": ("Bluetooth, USB, Android Auto, Apple CarPlay, "
                         "Dokunmatik Ekran, Navigasyon, Geri Görüş Kamerası, "
                         "Radyo"),
    "telefon tutucu özellikleri": ("Mıknatıslı, Vakumlu, Havalandırma Girişli, "
                                   "Kablosuz Şarjlı, Torpido Üstü, Cam Üstü"),
    "yıl": ("2010 ve öncesi, 2011-2015, 2016-2020, 2021-2023, 2024, 2025, "
            "2026"),

    # ---------- YAPI MARKET ----------
    "boya ağırlığı": ("1 kg, 2.5 kg, 3.5 kg, 7.5 kg, 10 kg, 15 kg, 17.5 kg, "
                      "20 kg"),
    "parlaklık": "Mat, Yarı Mat, İpek Mat, Saten, Parlak",
    "silinebilirlik": "Silinebilir, Ovma Dayanımlı, Silinemez",
    "yapıştırıcı tipi": ("Yapıştırıcı, Silikon, Mastik, Sıcak Silikon, Epoksi, "
                         "Çift Taraflı Bant, Japon Yapıştırıcı"),
    "delikler arası mesafe": ("96 mm, 128 mm, 160 mm, 192 mm, 224 mm, 320 mm"),
    "priz sayısı": "1, 2, 3, 4, 5, 6, 8 ve üzeri",
    "eldiven boyutu": "S, M, L, XL, XXL, 7, 8, 9, 10, 11",

    # ---------- BEBEK / ÇOCUK ----------
    "bez bedeni": ("1 Numara (Yenidoğan), 2 Numara (Mini), 3 Numara (Midi), "
                   "4 Numara (Maxi), 5 Numara (Junior), 6 Numara, 7 Numara"),
    "paket içi bez adedi": ("1-20 Adet, 21-40 Adet, 41-60 Adet, 61-90 Adet, "
                            "90 Adet ve üzeri"),
    "emzik uç materyali": "Silikon, Lateks, Kauçuk",
    "dil": "Türkçe, İngilizce, Almanca, Arapça, Çok Dilli, Dilsiz",
    "iç yatak ölçüsü": ("50x90 cm, 60x120 cm, 70x110 cm, 70x130 cm, "
                        "70x140 cm, 80x180 cm"),
    "kullanım tipi": ("Beşik, Park Yatak, Portatif Beşik, Karyola, Oyun Parkı, "
                      "Anne Yanı Beşik"),

    # ---------- SÜPERMARKET / PETSHOP ----------
    "öğütülme türü": ("Çekirdek, Öğütülmüş, Filtre Kahve, French Press, "
                      "Türk Kahvesi, Espresso, Moka Pot"),
    "aroma": ("Tavuk, Somon, Ton Balığı, Biftek, Kuzu, Hindi, Karışık Et, "
              "Sebzeli, Çilek, Vanilya, Çikolata, Muz, Karışık Meyve, "
              "Fındık, Aromasız"),
    "servis": ("10-20 Servis, 20-30 Servis, 30-50 Servis, 50-70 Servis, "
               "70 Servis ve üzeri"),
    "sertlik": "Yumuşak, Orta, Sert",

    # ---------- HOBİ / PARTİ / MÜZİK ----------
    "parti konsepti": ("Doğum Günü, Bebek Partisi (Baby Shower), "
                       "Cinsiyet Partisi, Yılbaşı, Mezuniyet, "
                       "Bekarlığa Veda, Cadılar Bayramı, Sevgililer Günü, "
                       "Sünnet, Nişan/Düğün, Kına"),
    "balon çeşidi": ("Latex Balon, Folyo Balon, Konfetili Balon, Rakam Balon, "
                     "Harf Balon, Balon Zinciri, Uçan Balon"),
    "müzik türleri": ("Pop, Rock, Jazz, Klasik Müzik, Rap, Elektronik, "
                      "Türk Halk Müziği, Türk Sanat Müziği, Arabesk, Blues"),
    "format": "Plak (LP), CD, Kaset, Dijital, DVD",
    "metraj": "1 m, 5 m, 10 m, 25 m, 50 m, 100 m ve üzeri",
    "tekerlek sayısı": "2 Tekerlekli, 3 Tekerlekli, 4 Tekerlekli",

    # ---------- HİZMET ----------
    "ek hizmetler": ("Ek Hizmet Yok, Montaj/Kurulum Hizmeti, Hediye Paketi, "
                     "Garanti Uzatma, Eski Ürün Alımı, Ekspres Teslimat"),
}


# =====================================================================
# 5) BAĞLAMA GÖRE DEĞİŞEN SEÇENEKLER
#    (Aynı filtre adı farklı kategoride farklı anlama geliyor:
#     Ayakkabıda "Beden" = 38, Giyimde "Beden" = M, Bebekte = 6-9 Ay)
# =====================================================================
BAGLAM_SECENEKLERI = {

    # ------------------------------ GİYİM (varsayılan)
    "giyim": {
        "tip": ("Günlük, Klasik, Spor, Abiye/Özel Gün, Ofis, Plaj, "
                "Ev Giyimi, Tesettür"),
        "ek özellik": ("Cepli, Kapüşonlu, Fermuarlı, Astarlı, Yırtmaçlı, "
                       "Fırfırlı, Nakışlı, Simli, Esnek, Büzgülü, Pileli, "
                       "Düğmeli, Dantel Detaylı, Taş İşlemeli, Kuşaklı"),
        "özellik": ("Esnek, Nefes Alabilir, Ütü Gerektirmez, Antibakteriyel, "
                    "Su İtici, Termal, Çekmez, Solmaz"),
    },

    # ------------------------------ OTOMOBİL & MOTOSİKLET
    "otomobil": {
        "materyal": ("Kauçuk, Plastik, Metal, Çelik, Alüminyum, Deri, "
                     "Suni Deri, Kumaş, Halı, Silikon, Cam, Karbon Fiber"),
        "beden": "S, M, L, XL, XXL, Tek Ebat, Ön Takım, Arka Takım, Takım",
        "hacim": ("1 L, 2 L, 3 L, 4 L, 5 L, 250 ml, 500 ml, 750 ml, "
                  "1000 ml"),
        "türü": ("İç Temizlik, Dış Temizlik, Cila, Yağ, Antifriz, "
                 "Cam Suyu, Koku, Aksesuar, Yedek Parça"),
        "özellik": ("Su Geçirmez, Kaymaz, Isıya Dayanıklı, UV Korumalı, "
                    "Kolay Montaj, Universal (Tüm Araçlara Uygun), "
                    "Araca Özel, Yıkanabilir"),
        "renk": RENK,
        "boyut/ebat": "Küçük, Orta, Büyük, Universal, Araca Özel",
        "tip": ("Orijinal, Muadil, Yan Sanayi, Universal, Araca Özel"),
    },

    # ------------------------------ AYAKKABI
    "ayakkabi": {
        "beden": AYAKKABI_BEDEN,
        "materyal": AYAKKABI_MATERYAL,
        "kalıp": ("Küçük Kalıp, Normal Kalıp, Büyük Kalıp, Dar Kalıp, "
                  "Geniş Kalıp"),
        "boy": "Bilek Boy, Yarım Boy, Uzun Boy, Diz Altı, Diz Üstü",
        "ek özellik": ("Ortopedik, Su Geçirmez, Kaymaz Taban, Hava Yastıklı, "
                       "İçi Kürklü, Işıklı, Gizli Topuklu (Yükseltici), "
                       "Nefes Alabilir, Hafif, Bilek Destekli"),
        "özellik": ("Ortopedik, Su Geçirmez, Kaymaz Taban, Hava Yastıklı, "
                    "İçi Kürklü, Nefes Alabilir, Hafif, Bilek Destekli"),
        "desen": ("Düz Renk, Baskılı, Çizgili, Leopar, Yılan Derisi, Simli, "
                  "Kareli, Çiçekli, Logolu"),
    },

    # ------------------------------ ÇANTA / VALİZ / CÜZDAN
    "canta": {
        "beden": "Mini, Küçük, Orta, Büyük, Extra Büyük",
        "materyal": CANTA_MATERYAL,
        "boyut": BOYUT_KUCUK_BUYUK,
        "boyut/ebat": "Mini, Küçük, Orta, Büyük, Kabin Boy, Orta Boy, Büyük Boy",
        "kapasite": ("5 L altı, 5-10 L, 10-20 L, 20-30 L, 30-40 L, "
                     "40-60 L, 60 L ve üzeri"),
        "tip": ("Cüzdan, Kartlık, Portföy, Para Klipsi, "
                "Bozuk Para Cüzdanı, Pasaportluk"),
        "ek özellik": ("Fermuarlı, Su Geçirmez, Laptop Bölmeli, "
                       "Çıkarılabilir Askılı, USB Çıkışlı, Tekerlekli, "
                       "RFID Korumalı, Ayarlanabilir Askı"),
        "yaş": "Çocuk, Genç, Yetişkin",
        "özellik": ("Fermuarlı, Su Geçirmez, Laptop Bölmeli, Tekerlekli, "
                    "USB Çıkışlı, RFID Korumalı, Çok Bölmeli, "
                    "Çıkarılabilir Askılı, Katlanabilir"),
        "kumaş tipi": ("Kanvas, Keten, Polyester, Naylon, Denim, Hasır, Jüt, "
                       "Simli Kumaş"),
    },

    # ------------------------------ SAAT
    "saat": {
        "materyal": ("Çelik, Paslanmaz Çelik, Deri, Suni Deri, Silikon, "
                     "Kauçuk, Titanyum, Seramik, Alüminyum, Plastik"),
        "özellik": ("Kronometre, Takvim, Alarm, Işıklı, Su Geçirmez, "
                    "Nabız Ölçer, Adımsayar, Dokunmatik, Çift Zaman, "
                    "Bluetooth Bağlantılı, Uyku Takibi"),
        "beden": "Küçük Kasa, Orta Kasa, Büyük Kasa, Ayarlanabilir",
        "boyut": "Küçük, Orta, Büyük",
        "tip": "Analog, Dijital, Analog + Dijital, Akıllı Saat",
    },

    # ------------------------------ GÖZLÜK
    "gozluk": {
        "materyal": ("Metal, Asetat, Plastik, Titanyum, Paslanmaz Çelik, "
                     "TR90, Ahşap"),
        "özellik": ("Polarize, UV Korumalı, Anti-Reflekte, Aynalı, Degrade, "
                    "Fotokromik, Mavi Işık Filtreli, Esnek Çerçeve"),
        "desen": "Düz Renk, Degrade, Leopar, Şeffaf, Mermer Desen, Aynalı",
    },

    # ------------------------------ TAKI
    "taki": {
        "materyal": TAKI_MATERYAL,
        "beden": ("Tek Beden, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, "
                  "20 (Yüzük Ölçüsü), Ayarlanabilir"),
        "boyut/ebat": ("Tek Ebat, Ayarlanabilir, 40 cm, 45 cm, 50 cm, 55 cm, "
                       "60 cm, 70 cm"),
        "model": ("Kolye, Bileklik, Yüzük, Küpe, Halhal, Broş, Piercing, "
                  "Set, Saç Aksesuarı"),
        "özellik": ("Kararmaz, Suya Dayanıklı, Alerji Yapmaz, El Yapımı, "
                    "İsme Özel, Hediye Kutulu, Taşlı"),
        "renk": METAL_RENK,
    },

    # ------------------------------ KOZMETİK / KİŞİSEL BAKIM
    "kozmetik": {
        "renk": ("Renksiz/Şeffaf, Nude, Açık Ten, Orta Ten, Koyu Ten, "
                 "Kırmızı, Bordo, Pembe, Fuşya, Mor, Kahverengi, Turuncu, "
                 "Siyah, Beyaz, Mavi, Yeşil, Altın, Gümüş, Rose Gold"),
        "form": ("Krem, Jel, Sıvı, Serum, Yağ, Köpük, Sprey, Stick, Pudra, "
                 "Balm, Losyon, Toz, Tablet, Maske, Sabun, Mousse, "
                 "Islak Mendil, Roll-On"),
        "hacim": ("10 ml altı, 10-30 ml, 30-50 ml, 50-100 ml, 100-200 ml, "
                  "200-400 ml, 400-750 ml, 750 ml ve üzeri"),
        "tip": ("EDP (Eau de Parfum), EDT (Eau de Toilette), Parfüm, Kolonya, "
                "Body Mist, Şampuan, Saç Kremi, Maske, Serum, Tonik, "
                "Temizleyici, Krem, Güneş Koruyucu"),
        "boy": "Kısa, Orta, Uzun, Ekstra Uzun",
        "içerik": ("Hyaluronik Asit, C Vitamini, Niasinamid, Retinol, "
                   "Salisilik Asit, Glikolik Asit, AHA/BHA, Kolajen, Peptit, "
                   "Aloe Vera, Argan Yağı, Çay Ağacı Yağı, Shea Yağı, "
                   "E Vitamini, Çinko, Keratin, Biotin"),
        "kullanma amacı": ("Nemlendirme, Temizleme, Onarım, Leke Karşıtı, "
                           "Kırışıklık Karşıtı, Sıkılaştırma, Güneş Koruma, "
                           "Akne Karşıtı, Gözenek Sıkılaştırma, Aydınlatma, "
                           "Peeling, Makyaj Temizleme, Besleme"),
        "kullanım amacı": ("Diş Temizliği, Diş Beyazlatma, Diş Eti Bakımı, "
                           "Ağız Kokusu, Hassasiyet Giderici, Diş Taşı Karşıtı"),
        "özellik": ("Vegan, Parabensiz, Sülfatsız, Alkolsüz, Doğal İçerikli, "
                    "Hipoalerjenik, Dermatolojik Test Edilmiş, "
                    "Hayvanlar Üzerinde Test Edilmemiş, Organik"),
        "ek özellik": ("Vegan, Parabensiz, Sülfatsız, Alkolsüz, "
                       "Doğal İçerikli, Hipoalerjenik, Kokusuz, "
                       "Dermatolojik Test Edilmiş"),
        "ürün tipi": ("Ağda, Jilet, Tıraş Makinesi, Epilatör, "
                      "Tüy Dökücü Krem, Lazer Epilasyon Cihazı, Cımbız"),
        "tipi": ("Tek Kullanımlık, Yedek Başlıklı, Jilet, Tıraş Makinesi, "
                 "Elektrikli"),
        "materyal": ("Plastik, Cam, Metal, Silikon, Ahşap, Bambu, "
                     "Doğal Kıl, Sentetik Kıl"),
        "ağırlık": ("50 gr altı, 50-100 gr, 100-250 gr, 250-500 gr, "
                    "500 gr ve üzeri"),
    },

    # ------------------------------ ELEKTRONİK
    "elektronik": {
        "renk": METAL_RENK,
        "materyal": ("Alüminyum, Plastik, Cam, Metal, Karbon Fiber, "
                     "Paslanmaz Çelik, Silikon, Deri"),
        "kullanım amacı": ("Oyun (Gaming), Ofis/İş, Tasarım/Grafik, Eğitim, "
                           "Günlük Kullanım, Video Düzenleme, Yazılım "
                           "Geliştirme"),
        "kapasite": ("8 GB, 16 GB, 32 GB, 64 GB, 128 GB, 256 GB, 512 GB, "
                     "1 TB, 2 TB"),
        "model": ("Standart (Disk Sürücülü), Digital Edition, Slim, Pro, "
                  "Bundle (Oyunlu)"),
        "boyut": "Kompakt, Standart, Büyük, Taşınabilir",
        "özellik": ("Bluetooth, Wi-Fi, NFC, Kablosuz Şarj, Suya Dayanıklı, "
                    "Hızlı Şarj, Yüz Tanıma, Parmak İzi, Dokunmatik Ekran, "
                    "GPS, Nabız Ölçer, Uyku Takibi, Adımsayar"),
        "taşıma kapasitesi": ("100 kg'a kadar, 100-120 kg, 120-150 kg, "
                              "150 kg ve üzeri"),
        "tip": ("Kablolu, Kablosuz, Bluetooth, Type-C, Şarj Aleti, "
                "Kılıf, Ekran Koruyucu, Powerbank"),
    },

    # ------------------------------ BEBEK / ÇOCUK / OYUNCAK
    "bebek": {
        "beden": COCUK_BEDEN,
        "boyut/ebat": COCUK_BEDEN,
        "materyal": ("Pamuk, Organik Pamuk, Penye, Müslin, Polyester, Peluş, "
                     "Silikon, Plastik, Ahşap, Kadife, Polar"),
        "kalıp": "Dar, Normal, Bol, Rahat Kesim",
        "boy": "Kısa, Normal, Uzun, Body, Tulum",
        "hacim": ("60 ml, 90 ml, 125 ml, 150 ml, 240 ml, 260 ml, 330 ml"),
        "tip": ("Cırtlı Bez, Külot Bez, Yıkanabilir Bez, Islak Mendil, "
                "Alt Açma Minderi, Bebek Bezi"),
        "özellik": ("Sesli, Işıklı, Müzikli, Uzaktan Kumandalı, Pilli, "
                    "Eğitici, Ahşap, Puzzle, Su Geçirmez, Emzik Tutuculu, "
                    "Katlanabilir, Taşıma Kolaylığı"),
        "taşıma kapasitesi": ("9 kg'a kadar, 15 kg'a kadar, 22 kg'a kadar, "
                              "22 kg ve üzeri"),
        "fonksiyon": ("Sabit, Sallanır, Katlanabilir, Çekmeceli, "
                      "Yükseklik Ayarlı, Çok Fonksiyonlu, Beşik + Yatak"),
        "boyut": "Mini, Küçük, Orta, Büyük",
        "renk": RENK,
    },

    # ------------------------------ SOFRA & MUTFAK
    "mutfak": {
        "materyal": MUTFAK_MATERYAL,
        "dış materyal": ("Paslanmaz Çelik, Alüminyum, Döküm, Emaye, Granit, "
                         "Çelik, Bakır"),
        "iç materyal": ("Granit, Teflon, Seramik, Paslanmaz Çelik, Döküm, "
                        "Emaye, Titanyum, Mermer Kaplama"),
        "hacim": ("0.5 L, 1 L, 1.5 L, 2 L, 3 L, 4 L, 5 L, 7 L, 10 L ve üzeri"),
        "kapasite": ("0.5 L, 1 L, 1.5 L, 2 L, 3 L, 5 L, 7 L, 10 L ve üzeri"),
        "kullanım alanı": ("Ocak, Fırın, İndüksiyon, Mikrodalga, Servis, "
                           "Buzdolabı, Dondurucu, Bulaşık Makinesi"),
        "boyut/ebat": ("16 cm, 18 cm, 20 cm, 22 cm, 24 cm, 26 cm, 28 cm, "
                       "30 cm, 32 cm, Küçük, Orta, Büyük"),
        "boyut": "Küçük, Orta, Büyük, Standart",
        "özellik": ("Yapışmaz, İndüksiyon Tabanlı, Isıya Dayanıklı, "
                    "Bulaşık Makinesinde Yıkanabilir, Fırına Dayanıklı, "
                    "Kapaklı, Cam Kapaklı, Ergonomik Sap, Çizilmez"),
        "ürün tipi": ("Tencere, Tava, Çaydanlık, Düdüklü Tencere, "
                      "Yemek Takımı, Kahvaltı Takımı, Bardak, Kupa, "
                      "Çatal Bıçak Seti, Servis Tabağı, Saklama Kabı, "
                      "Kesme Tahtası, Sürahi, Tepsi"),
        "parça sayısı": "1, 2, 3, 4, 5, 6, 7, 8, 9, 12, 18, 24, 36 ve üzeri",
    },

    # ------------------------------ EV & YAŞAM (genel)
    "ev": {
        "materyal": EV_MATERYAL,
        "boyut/ebat": ("Tek Kişilik, Çift Kişilik, King Size, Bebek, "
                       "60x90 cm, 70x140 cm, 90x190 cm, 100x200 cm, "
                       "140x190 cm, 160x200 cm, 180x200 cm, 200x220 cm"),
        "boyut": "Küçük, Orta, Büyük, Standart, Tek Ebat",
        "dış materyal": ("Pamuk, Polyester, Ranforce, Saten, Bambu, Keten, "
                         "Mikrofiber, Kadife"),
        "tip": ("Yastık, Yorgan, Battaniye, Havlu, Perde, Halı, Kilim, "
                "Masa Örtüsü, Sepet, Kutu"),
        "türü": ("Dekoratif, Fonksiyonel, Saklama, Aydınlatma, Tekstil, "
                 "Aksesuar"),
        "çeşit": ("Vazo, Biblo, Tablo, Çerçeve, Mum, Ayna, Saat, "
                  "Duvar Dekoru, Saksı, Sepet"),
        "özellik": ("Katlanabilir, Su Geçirmez, Antibakteriyel, Leke Tutmaz, "
                    "Yıkanabilir, Kaymaz Tabanlı, Isıya Dayanıklı, "
                    "Kolay Temizlenir"),
        "kullanım alanı": ("Salon, Yatak Odası, Çocuk Odası, Mutfak, Banyo, "
                           "Ofis, Bahçe, Balkon, Antre, Dış Mekan, Teras"),
        "hacim": ("0.5 L, 1 L, 1.5 L, 2 L, 3 L, 4 L, 5 L, 7 L, 10 L ve üzeri"),
        "ölçü": ("40 cm altı, 40-60 cm, 60-80 cm, 80-100 cm, 100-140 cm, "
                 "140-180 cm, 180 cm ve üzeri"),
        "yükseklik": ("40 cm altı, 40-60 cm, 60-80 cm, 80-100 cm, "
                      "100-140 cm, 140-180 cm, 180 cm ve üzeri"),
        "genişlik": ("40 cm altı, 40-60 cm, 60-80 cm, 80-100 cm, "
                     "100-140 cm, 140-180 cm, 180 cm ve üzeri"),
        "derinlik": ("20 cm altı, 20-30 cm, 30-40 cm, 40-50 cm, 50-60 cm, "
                     "60 cm ve üzeri"),
        "form": ("Düz, L Köşe, U Köşe, Köşe Takımı, Modüler, Yuvarlak, Oval"),
        "fonksiyon": ("Sabit, Açılır, Katlanır, Yataklı (Çekyat), "
                      "Sandıklı, Yükseklik Ayarlı, Çok Amaçlı"),
        "model": ("Avize, Aplik, Masa Lambası, Lambader, Spot, Sarkıt, "
                  "Gece Lambası, Şerit LED"),
        "ürün tipi": ("Tencere, Tava, Çaydanlık, Düdüklü Tencere, "
                      "Yemek Takımı, Kahvaltı Takımı, Bardak, Kupa, "
                      "Çatal Bıçak Seti, Servis Tabağı, Saklama Kabı, "
                      "Kesme Tahtası, Sürahi"),
        "parça sayısı": ("1, 2, 3, 4, 5, 6, 7, 8, 12, 18, 24, 36 ve üzeri"),
        "ek özellik": ("Katlanabilir, Yıkanabilir, Su Geçirmez, Leke Tutmaz, "
                       "Antibakteriyel, Kaymaz Tabanlı, Isıya Dayanıklı, "
                       "Kapaklı, Taşıma Kulplu"),
    },

    # ------------------------------ KİTAP & KIRTASİYE
    "kitap": {
        "boyut": ("Cep Boy, Küçük Boy, Orta Boy, Büyük Boy, A4, A5"),
        "materyal": ("Kağıt, Karton, Plastik, Metal, Ahşap, Silikon, Kumaş"),
        "tip": ("Kalem, Defter, Dosya, Klasör, Zımba, Makas, Yapıştırıcı, "
                "Silgi, Kalemtıraş, Cetvel, Pano, Boya"),
        "türü": ("Kurşun Kalem, Tükenmez Kalem, Jel Kalem, Roller Kalem, "
                 "Dolma Kalem, Fosforlu Kalem, Keçeli Kalem, Versatil"),
        "renk": RENK,
        "gramaj": ("60 gr, 70 gr, 80 gr, 90 gr, 120 gr, 160 gr, 200 gr, "
                   "300 gr"),
        "özellik": ("Silinebilir, Su Bazlı, Kokusuz, Ergonomik, "
                    "Yedek Uçlu, Çift Taraflı, Geri Dönüştürülmüş"),
    },

    # ------------------------------ SPOR & OUTDOOR
    "spor": {
        "beden": GIYIM_BEDEN,
        "materyal": ("Polyester, Pamuk, Elastan, Naylon, Likra, Polar, "
                     "Softshell, Nefes Alabilir Kumaş, Neopren, Alüminyum, "
                     "Çelik, Kauçuk, PVC, EVA"),
        "özellik": ("Katlanabilir, Ayarlanabilir, Kaymaz, Su Geçirmez, "
                    "Taşınabilir, Ağırlık Ayarlı, Dijital Göstergeli, "
                    "Antibakteriyel"),
        "ek özellik": ("Nefes Alabilir, Terletmez, Hızlı Kuruyan, "
                       "Su İtici, Reflektörlü, Cepli, Kapüşonlu, "
                       "UV Korumalı, Esnek"),
        "gramaj": ("500 gr altı, 500-1000 gr, 1-2 kg, 2-3 kg, "
                   "3 kg ve üzeri"),
        "form": "Toz, Tablet, Kapsül, Sıvı, Bar, Jel, Granül",
        "model": ("Fitness, Koşu, Yoga, Pilates, Kamp, Trekking, Bisiklet, "
                  "Yüzme, Kayak"),
        "boyut": "S, M, L, XL, Tek Ebat, Küçük, Orta, Büyük",
    },

    # ------------------------------ İÇ GİYİM / ÇORAP / PİJAMA
    "ic_giyim": {
        "beden": ("XS, S, M, L, XL, XXL, 3XL, 4XL, Tek Beden, "
                  "70, 75, 80, 85, 90, 95, 100, 105, 110, "
                  "36-40, 40-44, 44-48"),
        "boy": ("Kısa, Normal, Uzun, Mini, Midi, Maxi, Diz Üstü, Diz Altı, "
                "Patik, Soket, Dizaltı, Dizüstü"),
        "tip": ("Patik Çorap, Babet Çorap, Soket Çorap, Dizaltı Çorap, "
                "Külotlu Çorap, Termal Çorap, Bilek Çorap, Diz Üstü Çorap"),
        "materyal": ("Pamuk, Modal, Bambu, Mikrofiber, Likra, Elastan, "
                     "Dantel, Saten, İpek, Tül, Polyester, Viskon"),
        "ek özellik": ("Dikişsiz, Dolgusuz, Balensiz, Kaymaz, Antibakteriyel, "
                       "Termal, Emici, Toparlayıcı, Push-Up"),
    },

    # ------------------------------ BÜYÜK BEDEN
    "buyuk_beden": {
        "beden": BUYUK_BEDEN,
    },

    # ------------------------------ AKSESUAR (kemer, atkı, bere, eldiven, şapka)
    "aksesuar": {
        "beden": ("Tek Beden, XS, S, M, L, XL, XXL, "
                  "85, 90, 95, 100, 105, 110, 115, 120 (Kemer)"),
        "materyal": ("Hakiki Deri, Suni Deri, Akrilik, Yün, Pamuk, Kaşmir, "
                     "Polyester, Viskon, İpek, Saten, Triko, Metal"),
        "boyut/ebat": ("Tek Ebat, 70x70 cm, 90x90 cm, 100x100 cm, "
                       "70x180 cm, 80x200 cm"),
    },

    # ------------------------------ SÜPERMARKET / PETSHOP
    "supermarket": {
        "beden": ("XS, S, M, L, XL, XXL, Küçük Irk, Orta Irk, Büyük Irk"),
        "materyal": ("Plastik, Cam, Metal, Kağıt, Karton, Silikon, Bambu, "
                     "Mikrofiber, Sünger, Tekstil"),
        "ağırlık": ("100 gr altı, 100-250 gr, 250-500 gr, 500 gr - 1 kg, "
                    "1-3 kg, 3-5 kg, 5-10 kg, 10 kg ve üzeri"),
        "hacim": ("250 ml altı, 250-500 ml, 500 ml - 1 L, 1-2 L, 2-5 L, "
                  "5 L ve üzeri"),
        "çeşit": ("Çamaşır Deterjanı, Bulaşık Deterjanı, Yumuşatıcı, "
                  "Yüzey Temizleyici, Cam Temizleyici, Çamaşır Suyu, "
                  "Oda Kokusu, Böcek İlacı, Bez/Sünger, Çöp Poşeti"),
        "türü": ("Sıvı, Toz, Jel, Kapsül, Sprey, Tablet, Krem"),
        "ürün tipi": ("Kuru Mama, Yaş Mama, Ödül Maması, Kedi Kumu, Tasma, "
                      "Oyuncak, Mama Kabı, Taşıma Çantası, Yatak, "
                      "Bakım Ürünü, Vitamin"),
        "form": "Toz, Tablet, Kapsül, Sıvı, Granül, Jel, Krem",
        "yaş": ("Yavru (0-12 Ay), Yetişkin (1-7 Yaş), Yaşlı (7+ Yaş), "
                "Tüm Yaşlar"),
        "özellik": ("Tahılsız, Glutensiz, Şekersiz, Organik, Vegan, "
                    "Hipoalerjenik, Tuzsuz, Katkısız"),
        "tip": ("Normal, Uzun, Süper, Gece, Günlük Ped, Külot Ped, Organik, "
                "Tampon"),
        "ek özellik": ("Konsantre, Beyazlatıcı, Leke Çıkarıcı, Hijyenik, "
                       "Antibakteriyel, Hassas Ciltler İçin, Parfümsüz, "
                       "Çevre Dostu, Renkliler İçin, Beyazlar İçin"),
    },

    # ------------------------------ YAPI MARKET
    "yapimarket": {
        "beden": "S, M, L, XL, XXL, 7, 8, 9, 10, 11, Tek Beden",
        "materyal": ("Metal, Çelik, Paslanmaz Çelik, Alüminyum, Plastik, "
                     "Ahşap, Cam, Seramik, Pirinç, Krom, Kauçuk, Silikon"),
        "boyut/ebat": ("2.5 L, 7.5 L, 15 L, 20 L, Küçük, Orta, Büyük, "
                       "30x30 cm, 60x60 cm"),
        "ürün tipi": ("Boya, Fırça, Rulo, Bant, Vida, Çivi, Matkap, "
                      "El Aleti, Priz, Anahtar, Menteşe, Kulp, Silikon"),
        "tip": ("İç Cephe, Dış Cephe, Ahşap Boyası, Metal Boyası, "
                "Astar, Vernik, Su Bazlı, Solvent Bazlı"),
        "özellik": ("Su Bazlı, Kokusuz, Silinebilir, Antibakteriyel, "
                    "Isıya Dayanıklı, Paslanmaz, Kaymaz, Yangına Dayanıklı"),
        "kullanım alanı": ("İç Mekan, Dış Mekan, Banyo, Mutfak, Salon, "
                           "Cephe, Tavan, Ahşap Yüzey, Metal Yüzey"),
        "renk": RENK,
        "ölçü": ("10 mm, 20 mm, 30 mm, 40 mm, 50 mm, 60 mm, 80 mm, 100 mm"),
    },

    # ------------------------------ HOBİ
    "hobi": {
        "materyal": ("Akrilik, Yün, Pamuk, İp, Kağıt, Karton, Ahşap, Plastik, "
                     "Cam, Metal, Kumaş, Boncuk, Keçe"),
        "içerik": ("%100 Akrilik, %100 Pamuk, %100 Yün, Karışım, "
                   "Bambu Karışım, Polyester"),
        "gramaj": "50 gr, 100 gr, 150 gr, 200 gr, 250 gr, 500 gr, 1000 gr",
        "boyut/ebat": "Küçük, Orta, Büyük, A3, A4, A5, 20x20 cm, 30x40 cm",
        "özellik": ("Yıkanabilir, Tüy Bırakmaz, Antialerjik, Su Bazlı, "
                    "Kokusuz, Çocuklar İçin Uygun"),
        "beden": "Tek Beden, S, M, L, XL, Çocuk, Yetişkin",
    },
}


# =====================================================================
#  EK SEÇENEKLER (Elektronik, Beyaz Eşya, Mobilya, Petshop, Oyuncu vb.)
# =====================================================================

BOOLEAN_FILTRELER.update({
    # Küçük ev aletleri / beyaz eşya
    "hepa filtre", "otomatik kapanma", "çöp istasyonu", "haritalandırma",
    "uygulama üzerinden kontrol", "şarj standı", "el süpürgesi kullanımı",
    "kireç önleme", "damlama emniyeti", "süt köpürtücü", "otomatik su alımı",
    "sesli ikaz", "taşma emniyeti", "doğrayıcı", "çırpıcı", "hamur kancası",
    "çıkarılabilir plaka", "izgara özelliği", "buharlı", "yarım yük",
    "ücretsiz kurulum/montaj", "rendeleme ve dilimleme diski",
    "yer silme özelliği", "burun ve kulak temizleme başlığı",
    # TV / görüntü / ses
    "dahili uydu alıcı", "wi-fi özelliği", "smart tv", "hdr", "ethernet",
    "akım koruma", "dahili hoparlör", "curved (kavisli)", "type-c",
    "hdmi", "hdcp", "dvi-d", "dvi-i", "mini displayport", "radio",
    "görüntülü konuşma",
    # Bilgisayar / oyuncu
    "touchpad", "numerik tuşlar", "bilek desteği", "rgb aydınlatma",
    "baskılı", "mikrofon", "aktif gürültü önleme (anc)", "overclock",
    "bluetooth",
    # Kişisel bakım aletleri
    "iyon özelliği", "difüzör", "kablosuz özelliği", "dijital ekran",
    "lcd ekran", "vücut kitle indeksi ölçümü", "vücut su oranı ölçümü",
    "bazal metabolizma hızı ölçümü", "cilt tonu sensörü",
    # Klima
    "inverter", "çift ünite",
    # Bebek / spor
    "katlanabilme", "isofix özelliği", "360 derece dönebilme",
    "5 noktalı emniyet kemeri sistemi", "ayarlanabilir baş desteği",
    "ara kat", "alt açma ünitesi", "sineklik", "taşıma çantası",
    "ayna fonksiyonu", "kapüşon",
})


GENEL_SECENEKLER.update({

    # ---------------- ELEKTRONİK GENEL ----------------
    "frekans": "50 Hz, 60 Hz, 50/60 Hz",
    "voltaj": "12 V, 24 V, 110 V, 220 V, 220-240 V",
    "güç": ("500 W altı, 500-1000 W, 1000-1500 W, 1500-2000 W, "
            "2000-2500 W, 2500 W ve üzeri"),
    "enerji sınıfı": "A, A+, A++, A+++, B, C, D, E, F, G",
    "enerji sınıf aralığı": "A, A+, A++, A+++, B, C, D, E, F, G",
    "enerji sınıfı - soğutma": "A, A+, A++, A+++, B, C, D, E",
    "enerji sınıfı - isıtma": "A, A+, A++, A+++, B, C, D, E",
    "kablo uzunluğu": "1 m altı, 1-2 m, 2-3 m, 3-5 m, 5 m ve üzeri",
    "ses seviyesi": "60 dB altı, 60-70 dB, 70-80 dB, 80 dB ve üzeri",
    "bağlantı": ("Kablolu, Kablosuz, Bluetooth, USB, Type-C, Wi-Fi, "
                 "3.5 mm Jack"),
    "bağlantı türü": ("Kablolu, Kablosuz, Bluetooth, USB, Type-C, "
                      "2.4 GHz Alıcı"),
    "giriş/çıkış portları": ("USB-A, USB-C, HDMI, Ethernet, 3.5 mm Jack, "
                             "Kart Okuyucu, DisplayPort, VGA"),
    "usb çıkış sayısı": "1, 2, 3, 4 ve üzeri",
    "kart değeri": ("25 TL, 50 TL, 100 TL, 200 TL, 250 TL, 500 TL, "
                    "1000 TL ve üzeri"),
    "uyumlu cihaz": ("PlayStation 5, PlayStation 4, Xbox Series X/S, "
                     "Xbox One, Nintendo Switch, PC, Mobil Cihaz"),
    "ürün türü": ("Kol (Gamepad), Şarj İstasyonu, Kulaklık, Kablo, Stand, "
                  "Kılıf, Oyun, Hafıza Kartı"),
    "kılıf tipi": ("Silikon Kılıf, Sert (PC) Kılıf, Kitap Kılıf, "
                   "Cüzdan Kılıf, Şeffaf Kılıf, Darbe Emici, Mıknatıslı, "
                   "Kamera Korumalı, Standlı"),
    "sim kart uyumu": "Tek SIM, Çift SIM, eSIM, SIM Kart Yok",
    "ön kamera çözünürlük aralığı": ("5 MP altı, 5-8 MP, 8-12 MP, "
                                     "12-20 MP, 20 MP ve üzeri"),
    "hafıza kartı tipi": ("MicroSD, MicroSDHC, MicroSDXC, SD, SDHC, SDXC, "
                          "CompactFlash, Memory Stick"),
    "bellek kartı tipi": ("MicroSD, MicroSDHC, MicroSDXC, SD, SDHC, SDXC, "
                          "CompactFlash, Hafıza Kartı Yok"),
    "bellek kapasitesi": ("16 GB, 32 GB, 64 GB, 128 GB, 256 GB, 512 GB, "
                          "1 TB"),

    # ---------------- TV / GÖRÜNTÜ / SES ----------------
    "görüntüleme teknolojisi": ("LED, QLED, Neo QLED, OLED, Mini LED, "
                                "Nano Cell, Crystal UHD, LCD"),
    "görüntü kalitesi": "HD, Full HD, 4K UHD, 8K UHD",
    "görüntü teknolojisi": "LED, LCD, DLP, OLED, Lazer",
    "ekran teknolojisi": ("LCD, IPS, OLED, AMOLED, Super Retina XDR, "
                          "Dynamic AMOLED"),
    "çözünürlük (piksel)": ("1366x768, 1920x1080, 2560x1440, 3840x2160, "
                            "7680x4320"),
    "çözünürlük standartı": ("HD, Full HD, 2K (QHD), 4K (UHD), 5K, 8K"),
    "çözünürlük teknolojisi": "SVGA, WXGA, HD, Full HD, 4K, 8K",
    "model yılı": "2020, 2021, 2022, 2023, 2024, 2025, 2026",
    "ekran boyutu (inç)": ("32 inç altı, 32-43 inç, 43-50 inç, 50-55 inç, "
                           "55-65 inç, 65-75 inç, 75 inç ve üzeri"),
    "hareket seçeneği": ("Sabit, Eğilebilir, Hareketli (Kollu), Dönebilir"),
    "kanal yapısı": "2.0, 2.1, 3.1, 5.1, 7.1, 7.1.4",
    "watt aralığı": ("100 W altı, 100-200 W, 200-300 W, 300-500 W, "
                     "500 W ve üzeri"),
    "parlaklık (ansilümen)": ("1000 altı, 1000-2000, 2000-3000, "
                              "3000-4000, 4000 ve üzeri"),
    "ampul ömrü (eco mod)": ("10.000 saat altı, 10.000-20.000 saat, "
                             "20.000-30.000 saat, 30.000 saat ve üzeri"),
    "dinleme süresi": ("5 saate kadar, 5-10 saat, 10-20 saat, 20-40 saat, "
                       "40 saat ve üzeri"),
    "kulaklık modeli": ("Kulak İçi, Kulak Üstü, Kulak Çevreleyen, "
                        "Kemik İletimli, TWS (Tam Kablosuz), Boyunluklu"),
    "kullanım tipi": "Oyun, Müzik, Ofis/Toplantı, Spor, Günlük",
    "batarya tipi": ("Şarj Edilebilir (Dahili), AA Pil, AAA Pil, "
                     "Lityum, Pilsiz"),
    "tepki süresi": "0.5 ms, 1 ms, 2 ms, 4 ms, 5 ms ve üzeri",
    "ekran yenilenme hızı": ("60 Hz, 75 Hz, 100 Hz, 120 Hz, 144 Hz, "
                             "165 Hz, 240 Hz, 360 Hz"),
    "hdmi giriş sayısı": "1, 2, 3, 4 ve üzeri",
    "sync teknolojisi": ("AMD FreeSync, NVIDIA G-Sync, Adaptive Sync, Yok"),

    # ---------------- BİLGİSAYAR / OYUNCU ----------------
    "tuş düzeni": ("Full Size, TKL (Tenkeyless), %75, %60, Ergonomik"),
    "klavye dili": ("Türkçe Q, Türkçe F, İngilizce (US), İngilizce (UK), "
                    "Almanca"),
    "switch türü": ("Mekanik, Membran, Optik, Hall Effect (Manyetik), "
                    "Makaslı"),
    "switch rengi": ("Red (Kırmızı), Blue (Mavi), Brown (Kahverengi), "
                     "Black (Siyah), Silver (Gümüş), Yellow (Sarı)"),
    "mouse hassasiyeti (dpi)": ("800 DPI, 1600 DPI, 3200 DPI, 6400 DPI, "
                                "12000 DPI, 16000 DPI ve üzeri"),
    "oyun türü": ("Aksiyon, Macera, Spor, Yarış, Strateji, Korku, RPG, "
                  "FPS (Nişancı), Simülasyon, Aile & Çocuk, Dövüş"),
    "okuma hızı": ("500 MB/s altı, 500-1000 MB/s, 1000-2000 MB/s, "
                   "2000-5000 MB/s, 5000 MB/s ve üzeri"),
    "yazma hızı": ("500 MB/s altı, 500-1000 MB/s, 1000-2000 MB/s, "
                   "2000-5000 MB/s, 5000 MB/s ve üzeri"),
    "ram hızı": ("2400 MHz, 2666 MHz, 3000 MHz, 3200 MHz, 3600 MHz, "
                 "4800 MHz, 5600 MHz, 6000 MHz ve üzeri"),
    "uyumlu sistemler": ("Masaüstü (Desktop), Dizüstü (Laptop), Sunucu, "
                         "Mini PC"),
    "çip seti": "NVIDIA, AMD, Intel",
    "grafik işlemcisi": ("NVIDIA GeForce RTX, NVIDIA GeForce GTX, "
                         "AMD Radeon RX, Intel Arc, Dahili Grafik"),
    "soğutucu tipleri": ("Hava Soğutmalı, Sıvı Soğutmalı, Pasif, "
                         "Fanlı, AIO"),

    # ---------------- BEYAZ EŞYA ----------------
    "toplam hacim": ("200 L altı, 200-300 L, 300-400 L, 400-500 L, "
                     "500-600 L, 600 L ve üzeri"),
    "dondurucu özelliği": "No-Frost, Statik, Low-Frost",
    "dondurucu yeri": ("Üstten Donduruculu, Alttan Donduruculu, "
                       "Yan Yana (Gardırop), Donduruculu Değil"),
    "buzluk tipi": "No-Frost, Statik, Çekmeceli, Buzluksuz",
    "maksimum sıkma devri": ("800 devir, 1000 devir, 1200 devir, "
                             "1400 devir, 1600 devir"),
    "kurutma özelliği": "Kurutmalı, Kurutmasız",
    "program sayısı": "5-8, 9-12, 13-16, 17 ve üzeri",
    "su tüketimi": "10 L altı, 10-12 L, 12-15 L, 15 L ve üzeri",
    "maksimum kurutma kapasitesi": ("6 kg, 7 kg, 8 kg, 9 kg, 10 kg, "
                                    "11 kg ve üzeri"),
    "kurutma teknolojisi": "Isı Pompalı, Yoğuşmalı, Vantilatörlü",
    "çekmece sayısı": "1, 2, 3, 4, 5, 6 ve üzeri",
    "ocak tipi": ("Gazlı, Elektrikli, Vitroseramik, İndüksiyon, Domino, "
                  "Gazlı + Elektrikli"),
    "ocak yüzeyi": ("Cam, Vitroseramik, Emaye, Paslanmaz Çelik, Döküm"),
    "ocak göz sayısı": "1, 2, 3, 4, 5, 6",
    "gaz tipi": "Doğalgaz, LPG (Tüp), Doğalgaz + LPG",
    "pişirme özelliği": ("Turbo, Alt-Üst, Statik, Buharlı, Air Fry, "
                         "Pizza Programı, Izgara"),
    "pişirme fonksiyon sayısı": "3, 4, 5, 6, 7, 8 ve üzeri",
    "davlumbaz şekli": ("Duvar Tipi, Ada Tipi, Gömme (Sürgülü), "
                        "Eğik (Cam), Set Altı, Ankastre"),
    "davlumbaz tipi": "Bacalı, Bacasız, Bacalı/Bacasız",
    "filtre tipi": ("Alüminyum Filtre, Karbon Filtre, Yağ Filtresi, "
                    "HEPA Filtre"),
    "filtre türü": ("HEPA, Karbon, Ön Filtre, İyonizer, UV, Pollen"),
    "filtre sayısı": "1, 2, 3, 4 ve üzeri",
    "maksimum emiş gücü": ("300 m³/h altı, 300-500 m³/h, 500-700 m³/h, "
                           "700-1000 m³/h, 1000 m³/h ve üzeri"),
    "saat tipi": "Analog, Dijital, Dokunmatik, Mekanik, Saatsiz",
    "tema / stil": ("Modern, Klasik, Retro, Endüstriyel, Minimalist, "
                    "Country"),
    "maksimum isıl güç": ("20.000 kcal/h altı, 20.000-24.000 kcal/h, "
                          "24.000-28.000 kcal/h, 28.000 kcal/h ve üzeri"),
    "cihaz tipi": "Yoğuşmalı, Hermetik, Bacalı, Premix",
    "isıtma tekniği": "Yoğuşmalı, Konvansiyonel, Premix",
    "isıtma kapasitesi": ("9.000 BTU, 12.000 BTU, 18.000 BTU, 24.000 BTU"),
    "soğutma kapasitesi": ("9.000 BTU, 12.000 BTU, 18.000 BTU, 24.000 BTU"),
    "baca tipi": "Hermetik, Bacalı, Bacasız",
    "eşanjör sayısı": "1, 2",
    "kontrol tipi": "Mekanik, Dijital, Dokunmatik",
    "isıtma gücü": ("1000 W altı, 1000-2000 W, 2000-3000 W, "
                    "3000 W ve üzeri"),
    "özel filtreler": ("Karbon Filtre, HEPA Filtre, Anti-Bakteriyel Filtre, "
                       "Pollen Filtre, Yok"),
    "sıcak soğuk kullanımı": "Sıcak Buhar, Soğuk Buhar, Sıcak ve Soğuk",

    # ---------------- KÜÇÜK EV ALETLERİ ----------------
    "hazne kapasitesi": ("0.5 L altı, 0.5-1 L, 1-2 L, 2-3 L, "
                         "3 L ve üzeri"),
    "hazne malzemesi": "Plastik, Cam, Paslanmaz Çelik, Tritan",
    "motor teknolojisi": ("Fırçasız (Dijital) Motor, Fırçalı Motor, "
                          "Siklonik, İnverter"),
    "aşılabilir engel seviyesi": ("1 cm altı, 1-1.5 cm, 1.5-2 cm, "
                                  "2 cm ve üzeri"),
    "basınç": "4 bar, 5 bar, 6 bar, 7 bar, 8 bar ve üzeri",
    "şok buhar": ("100 gr/dk altı, 100-150 gr/dk, 150-200 gr/dk, "
                  "200 gr/dk ve üzeri"),
    "sürekli buhar": ("20 gr/dk altı, 20-40 gr/dk, 40-60 gr/dk, "
                      "60 gr/dk ve üzeri"),
    "su kapasitesi": ("250 ml altı, 250-500 ml, 500 ml - 1 L, 1-1.5 L, "
                      "1.5 L ve üzeri"),
    "fincan kapasitesi": ("1 Fincan, 2 Fincan, 3 Fincan, 4 Fincan, "
                          "6 Fincan, 10 Fincan ve üzeri"),
    "cezve malzemesi": ("Paslanmaz Çelik, Alüminyum, Bakır, Seramik, "
                        "Döküm"),
    "demlik malzemesi": "Cam, Porselen, Paslanmaz Çelik, Seramik, Çelik",
    "demlik kapasitesi": ("0.5 L altı, 0.5-1 L, 1-1.5 L, 1.5-2 L, "
                          "2 L ve üzeri"),
    "hız ayarı": ("1 Kademe, 2 Kademe, 3 Kademe, 5 Kademe, 6 Kademe, "
                  "Kademesiz (Turbo)"),
    "isı ayarı": "Sabit, Ayarlanabilir, 2 Kademe, 3 Kademe, 5 Kademe",
    "ekmek dilim kapasitesi": "2 Dilim, 4 Dilim, 6 Dilim, 8 Dilim",
    "plaka kullanımı": ("Sabit Plaka, Çıkarılabilir Plaka, "
                        "Çift Taraflı Plaka"),
    "pişirme kapasitesi": ("2 L altı, 2-4 L, 4-6 L, 6-8 L, "
                           "8 L ve üzeri"),

    # ---------------- KİŞİSEL BAKIM ALETLERİ ----------------
    "tıraş bölgesi": ("Yüz & Sakal, Saç, Vücut, Burun & Kulak, "
                      "Çok Amaçlı"),
    "kullanım": "Kuru, Islak, Kuru & Islak",
    "başlık sayısı": "1, 2, 3, 4, 5, 6 ve üzeri",
    "maksimum sıcaklık": ("150 °C altı, 150-180 °C, 180-200 °C, "
                          "200-230 °C, 230 °C ve üzeri"),
    "plaka materyali": ("Seramik, Turmalin, Titanyum, Keratin Kaplama, "
                        "Argan Yağlı, Metal"),
    "maşa çapı": "13 mm, 16 mm, 19 mm, 25 mm, 32 mm, 38 mm ve üzeri",
    "motor tipi": "AC Motor, DC Motor, Dijital Motor",
    "maksimum ağırlık": "150 kg, 180 kg, 200 kg, 250 kg ve üzeri",
    "atım sayısı": ("100.000 altı, 100.000-300.000, 300.000-500.000, "
                    "500.000-1.000.000, 1.000.000 ve üzeri"),
    "kademe ayarı": "3 Kademe, 5 Kademe, 6 Kademe, 10 Kademe",
    "uygulama alanı": ("Yüz, Bacak, Kol, Koltuk Altı, Bikini Bölgesi, "
                       "Tüm Vücut"),

    # ---------------- FOTO & KAMERA ----------------
    "fotoğraf çözünürlük": ("12 MP altı, 12-20 MP, 20-24 MP, 24-32 MP, "
                            "32 MP ve üzeri"),
    "optik zoom": "3x, 5x, 10x, 20x, 30x, 40x ve üzeri",
    "kayıt tipi": "Hafıza Kartı, Dahili Hafıza, HDD, Bulut",

    # ---------------- EV TEKSTİLİ / MOBİLYA ----------------
    "havlu tipi": ("El Havlusu, Yüz Havlusu, Banyo Havlusu, Plaj Havlusu, "
                   "Peştemal, Mutfak Havlusu, Bornoz"),
    "bornoz uzunluğu": "Kısa, Diz Boyu, Uzun",
    "takma şekli": ("Korniş, Pileli, Kuşgözü, Halkalı, Çubuk Geçmeli, "
                    "Klipsli"),
    "işık geçirgenliği": ("Blackout (Karartma), Yarı Karartma, "
                          "Şeffaf (Tül), Işık Geçirir"),
    "kanat sayısı": "1, 2, 3, 4",
    "pile": "Pilesiz, 1/2 Pile, 1/3 Pile, Büzgülü",
    "aksesuar tipi": "Korniş, Kuşgözü, Halka, Klips, Aksesuarsız",
    "hav yüksekliği": ("5 mm altı, 5-10 mm, 10-15 mm, 15-20 mm, "
                       "20 mm ve üzeri"),
    "saçak tipi": "Saçaklı, Saçaksız",
    "koltuk tipi": ("Üçlü, İkili, Tekli, Köşe Koltuk, Berjer, Çekyat, "
                    "Puf, L Köşe, U Köşe"),
    "takım tipi": ("Masa + Sandalye, Oturma Grubu, Bahçe Seti, "
                   "Şezlong Seti, Bistro Set"),
    "takım içeriği": ("3+3+1+1, 3+3+1, 3+2+1, 2+2+1, Köşe Takımı, "
                      "Berjer Dahil"),
    "tasarım": ("Modern, Klasik, Retro, Country, Endüstriyel, "
                "Minimalist, Chesterfield"),
    "kullanım türü": ("Duvara Monte, Kapı Arkası, Portatif, Gömme, "
                      "Ayaklı, Askılık"),
    "yerden yüksekliği": ("120 cm altı, 120-150 cm, 150-180 cm, "
                          "180 cm ve üzeri"),
    "alt modül genişlik": ("60 cm, 80 cm, 100 cm, 120 cm, 140 cm, "
                           "160 cm ve üzeri"),
    "alt modül yükseklik": "70 cm, 80 cm, 85 cm, 90 cm ve üzeri",
    "üst modül genişlik": ("60 cm, 80 cm, 100 cm, 120 cm, 140 cm, "
                           "160 cm ve üzeri"),
    "üst modül yükseklik": "50 cm, 60 cm, 70 cm, 80 cm ve üzeri",
    "yatak cinsi": ("Yaylı, Visco, Sünger, Ortopedik, Lateks, Hibrit, "
                    "Bebek Yatağı"),
    "set içeriği": ("2 Parça, 3 Parça, 4 Parça, 5 Parça, "
                    "6 Parça ve üzeri"),

    # ---------------- YAPI MARKET ----------------
    "matkap türü": ("Darbeli, Darbesiz, Kırıcı Delici, Vidalama, "
                    "Akülü, Kablolu"),
    "akü volt": "3.6 V, 12 V, 18 V, 20 V, 24 V, 36 V",
    "akü sayısı": "Akü Yok, 1, 2, 3",
    "akü kapasitesi": "1.5 Ah, 2.0 Ah, 3.0 Ah, 4.0 Ah, 5.0 Ah ve üzeri",
    "mandren tipi": "Anahtarlı, Anahtarsız, SDS Plus, SDS Max",

    # ---------------- KİTAP / KIRTASİYE ----------------
    "dil seviyesi": ("A1 (Başlangıç), A2, B1, B2, C1, C2 (İleri), "
                     "Tüm Seviyeler"),
    "klasör formu": ("Telli Dosya, Klasör, Sunum Dosyası, Körüklü Dosya, "
                     "Arşiv Kutusu, Çıtçıtlı Dosya"),

    # ---------------- SÜPERMARKET / PETSHOP ----------------
    "yıkama sayısı": ("10 yıkama altı, 10-20 yıkama, 20-30 yıkama, "
                      "30-50 yıkama, 50 yıkama ve üzeri"),
    "kumaş cinsi/rengi": ("Beyazlar, Renkliler, Siyahlar, "
                          "Hassas Kumaşlar, Yünlü, Bebek, Tüm Kumaşlar"),
    "rulo sayısı": "1, 2, 4, 6, 8, 12, 16, 24, 32 ve üzeri",
    "kat sayısı": "2 Katlı, 3 Katlı, 4 Katlı",
    "ağırlık / hacim": ("5 kg altı, 5-10 kg, 10-15 kg, 15-20 kg, "
                        "20 kg ve üzeri"),
    "kum türü": ("Bentonit, Silica (Kristal), Doğal, İnce Taneli, "
                 "Kalın Taneli, Topaklanan"),
    "koku tipi": ("Kokusuz, Lavanta, Marsilya Sabunu, Bebek Pudrası, "
                  "Limon, Aktif Karbon, Çam"),
    "tane şekli": ("İnce Taneli, Kalın Taneli, Topaklanan, Kristal, "
                   "Granül"),
    "mama cinsi": ("Karışık Yem, Muhabbet Kuşu Yemi, Kanarya Yemi, "
                   "Papağan Yemi, Finch Yemi, Güvercin Yemi"),

    # ---------------- SPOR / BİSİKLET ----------------
    "top bedeni": "1 Numara, 3 Numara, 4 Numara, 5 Numara",
    "hız aralığı": ("0-10 km/s, 0-12 km/s, 0-16 km/s, 0-20 km/s, "
                    "0-22 km/s"),
    "açma / kapama": "Katlanabilir, Sabit, Rulo (Sarmalı)",
    "pompa durumu": "Pompalı, Pompasız",
    "çivi tipi": ("Çim Saha (FG), Halı Saha (TF), Salon (IC), "
                  "Yumuşak Zemin (SG), Çoklu Zemin (MG)"),
    "bilek stili": "Bilek Üstü (High), Orta (Mid), Bilek Altı (Low)",
    "menzil": ("20 km altı, 20-40 km, 40-60 km, 60-80 km, "
               "80 km ve üzeri"),
    "max. hız (km/h)": ("20 km/s altı, 20-25 km/s, 25-30 km/s, "
                        "30 km/s ve üzeri"),
    "kask tipi": ("Full Face (Kapalı), Yarım (Jet), Çene Açılır, "
                  "Cross, Bisiklet Kaskı"),
    "eldiven tipi": ("Yazlık, Kışlık, Su Geçirmez, Korumalı, "
                     "Yarım Parmak, Tam Parmak"),

    # ---------------- MÜZİK / HOBİ ----------------
    "gitar tipi": ("Klasik Gitar, Akustik Gitar, Elektro Gitar, "
                   "Bas Gitar, Elektro Akustik, Ukulele"),
    "piyano tipi": ("Dijital Piyano, Akustik Piyano, Kuyruklu Piyano, "
                    "Taşınabilir Piyano"),
    "ağaç boyu": ("60-90 cm, 90-120 cm, 120-150 cm, 150-180 cm, "
                  "180-220 cm, 220 cm ve üzeri"),

    # ---------------- KOZMETİK EK ----------------
    "ürün güvenliği bilgisi": ("Dermatolojik Test Edilmiş, "
                               "Oftalmolojik Test Edilmiş, Hipoalerjenik, "
                               "Vegan, Parabensiz"),

    # ---------------- BEBEK EK ----------------
    "yükseklik ayarı": ("Yok, 3 Kademe, 5 Kademe, 7 Kademe, "
                        "Kademesiz (Ayarlanabilir)"),
    "araba ağırlığı": ("5 kg altı, 5-8 kg, 8-12 kg, 12 kg ve üzeri"),
    "tekerlek": "Tekerlekli, Tekerleksiz, Kilitlenebilir Tekerlekli",
    "emzik uç materyali": "Silikon, Lateks, Kauçuk",
})


BAGLAM_SECENEKLERI.update({

    # ------------------------------ ÇOCUK ÖLÇÜ (sadece bedeni ezer)
    "cocuk": {
        "beden": COCUK_BEDEN,
        "boyut/ebat": COCUK_BEDEN,
    },

    # ------------------------------ BEBEK ÜRÜNLERİ (bez, mama, araba...)
    "bebek_urun": {
        "tip": ("Cırtlı Bez, Külot Bez, Yıkanabilir Bez, Islak Mendil, "
                "Alt Açma Minderi, Emzik, Biberon, Oyuncak"),
        "materyal": ("Plastik, Silikon, Cam, Ahşap, Peluş, Pamuk, "
                     "Polyester, Paslanmaz Çelik, Tritan"),
        "hacim": "60 ml, 90 ml, 125 ml, 150 ml, 240 ml, 260 ml, 330 ml",
        "kullanım şekli": "Manuel, Elektrikli, Şarjlı, Çift Pompalı",
        "çeşit": ("Silikon Önlük, Kumaş Önlük, Kollu Önlük, Cepli Önlük, "
                  "Tek Kullanımlık"),
        "taşıma kapasitesi": ("9 kg'a kadar, 15 kg'a kadar, "
                              "22 kg'a kadar, 22 kg ve üzeri"),
        "özellik": ("Katlanabilir, Sallanır, Müzikli, Işıklı, "
                    "Yükseklik Ayarlı, Çift Yönlü, Tekerlekli, "
                    "Emniyet Kemerli, Taşıma Kolaylığı, Sineklikli"),
        "model": ("Bebek Arabası, Puset, Travel Sistem, Ana Kucağı, "
                  "Kanguru, Yürüteç, Mama Sandalyesi"),
        "boyut": "Mini, Küçük, Orta, Büyük",
        "renk": RENK,
        "fonksiyon": ("Sabit, Sallanır, Katlanabilir, Çekmeceli, "
                      "Yükseklik Ayarlı, Çok Fonksiyonlu, Beşik + Yatak"),
        "şekil": "Yuvarlak, Kare, Dikdörtgen, Oval, Hayvan Figürlü",
        "dil": "Türkçe, İngilizce, Almanca, Arapça, Çok Dilli",
        "taban": "Kaymaz Taban, Süngerli Taban, Yumuşak Taban",
    },

    # ------------------------------ TELEFON
    "telefon": {
        "tip": ("Kılıf, Ekran Koruyucu, Şarj Aleti, Kablo, Powerbank, "
                "Kulaklık, Telefon Tutucu, Selfie Çubuğu"),
        "materyal": ("Silikon, Plastik, Cam, Deri, Suni Deri, "
                     "Alüminyum, TPU, Polikarbon"),
        "türü": ("Mıknatıslı, Vakumlu, Havalandırma Girişli, "
                 "Torpido Üstü, Cam Üstü, Kablosuz Şarjlı"),
    },

    # ------------------------------ BİLGİSAYAR & TABLET
    "bilgisayar": {
        "kapasite": ("8 GB, 16 GB, 32 GB, 64 GB, 128 GB, 256 GB, "
                     "512 GB, 1 TB, 2 TB, 4 TB"),
        "tip": ("Dizüstü (Laptop), Masaüstü, All-in-One, Mini PC, "
                "Tablet, 2'si 1 Arada"),
        "özellik": ("Dokunmatik Ekran, Parmak İzi Okuyucu, "
                    "Arkadan Aydınlatmalı Klavye, Yüz Tanıma, "
                    "Kablosuz Şarj, Kalem Desteği, Çift Ekran"),
        "materyal": ("Alüminyum, Plastik, Magnezyum Alaşım, "
                     "Karbon Fiber, Cam"),
        "boyut": "Kompakt, Standart, Büyük, Taşınabilir",
    },

    # ------------------------------ OYUNCULARA ÖZEL
    "oyuncu": {
        "model": ("Standart (Disk Sürücülü), Digital Edition, Slim, Pro, "
                  "Bundle (Oyunlu), Lite, OLED"),
        "kapasite": "500 GB, 825 GB, 1 TB, 2 TB, 4 TB",
        "özellik": ("RGB Aydınlatmalı, Kablosuz, Titreşimli, "
                    "Mekanik, Gürültü Önleyici, Programlanabilir Tuş, "
                    "Ayarlanabilir DPI"),
        "renk": METAL_RENK,
        "taşıma kapasitesi": ("100 kg'a kadar, 100-120 kg, 120-150 kg, "
                              "150 kg ve üzeri"),
        "tip": ("Klavye, Mouse, Kulaklık, Mousepad, Koltuk, Konsol, "
                "Oyun, Kol (Gamepad)"),
    },

    # ------------------------------ TV & GÖRÜNTÜ & SES
    "tv": {
        "tip": ("Kablolu, Kablosuz, Bluetooth, Soundbar, Uydu Alıcı, "
                "Priz, Kablo, Aparat"),
        "özellik": ("Bluetooth, Wi-Fi, USB Girişi, HDMI Girişi, "
                    "Sesli Asistan, Uzaktan Kumandalı, Ekran Yansıtma, "
                    "Dolby Atmos, Gürültü Önleyici"),
        "renk": METAL_RENK,
        "kapasite": "8 GB, 16 GB, 32 GB, 64 GB, 128 GB",
        "ürün tipi": ("Çanak Anten, LNB, Uydu Alıcı, Kablo, Aparat, "
                      "Ekran Koruyucu"),
        "materyal": "Plastik, Metal, Alüminyum, Cam, Ahşap",
    },

    # ------------------------------ BEYAZ EŞYA
    "beyazesya": {
        "kapasite": ("6 kg, 7 kg, 8 kg, 9 kg, 10 kg, 11 kg, "
                     "12 kg ve üzeri, 6 Kişilik, 12 Kişilik, 14 Kişilik"),
        "kullanım şekli": ("Solo (Bağımsız), Ankastre, Gömme, Set Üstü, "
                           "Tezgah Altı"),
        "hacim": ("20 L altı, 20-25 L, 25-30 L, 30-40 L, 40 L ve üzeri"),
        "güç": ("800 W altı, 800-1000 W, 1000-1500 W, 1500-2000 W, "
                "2000 W ve üzeri"),
        "tip": ("Solo, Ankastre, Gardırop Tipi, Çift Kapılı, "
                "Alttan Donduruculu, Üstten Donduruculu, Mini, "
                "Sandık Tipi, Çekmeceli"),
        "özellik": ("No-Frost, İnverter Motor, Wi-Fi Bağlantılı, "
                    "Buz Pınarı, Sıfır Derece Bölmesi, A Enerji Sınıfı, "
                    "Hızlı Program, Çocuk Kilidi, Gecikmeli Başlatma"),
        "renk": METAL_RENK,
        "materyal": ("Paslanmaz Çelik, Cam, Plastik, Metal, Emaye"),
        "yükseklik": ("150 cm altı, 150-170 cm, 170-185 cm, 185-200 cm, "
                      "200 cm ve üzeri"),
        "genişlik": ("50 cm altı, 50-60 cm, 60-70 cm, 70-80 cm, "
                     "80-90 cm, 90 cm ve üzeri"),
        "derinlik": ("50 cm altı, 50-60 cm, 60-70 cm, 70 cm ve üzeri"),
        "kullanım alanı": ("Mutfak, Çamaşır Odası, Banyo, Balkon, "
                           "Ticari Kullanım"),
    },

    # ------------------------------ KÜÇÜK EV ALETLERİ
    "kucukev": {
        "materyal": ("Paslanmaz Çelik, Plastik, Cam, Seramik, "
                     "Alüminyum, Silikon, Çelik, Tritan"),
        "taban": ("Seramik, Seramik Kaplama, Paslanmaz Çelik, "
                  "Alüminyum, Titanyum, Eloksal"),
        "tip": ("Buharlı, Kuru, Kazanlı, Dikey, Robot, Şarjlı, Kablolu, "
                "Toz Torbalı, Torbasız, Filtre Kahve, Türk Kahvesi, "
                "Espresso"),
        "hacim": ("0.5 L altı, 0.5-1 L, 1-1.5 L, 1.5-2 L, 2-3 L, "
                  "3 L ve üzeri"),
        "kapasite": ("0.5 L altı, 0.5-1 L, 1-2 L, 2-3 L, 3-5 L, "
                     "5 L ve üzeri"),
        "bıçak sayısı": "2, 4, 6, 8",
        "özellik": ("Otomatik Kapanma, Kablosuz, Katlanabilir, "
                    "Yıkanabilir Filtre, Hız Ayarlı, Sesli Uyarı, "
                    "Aşırı Isınma Koruması, Turbo Motor"),
        "renk": METAL_RENK,
        "model": ("Filtre Kahve Makinesi, Türk Kahve Makinesi, "
                  "Espresso Makinesi, Kapsüllü, French Press"),
        "güç": ("500 W altı, 500-1000 W, 1000-1500 W, 1500-2000 W, "
                "2000-2500 W, 2500 W ve üzeri"),
    },

    # ------------------------------ KİŞİSEL BAKIM ALETLERİ
    "bakim_aleti": {
        "tip": ("Saç Düzleştirici, Saç Maşası, Fön Makinesi, "
                "Çok Fonksiyonlu, Tıraş Makinesi, Epilatör, "
                "IPL Lazer, Sakal Düzeltici"),
        "materyal": "Plastik, Seramik, Metal, Cam, Paslanmaz Çelik",
        "özellik": ("İyonlu, Otomatik Kapanma, Dijital Ekran, "
                    "Kablosuz, Isı Ayarlı, Soğuk Hava Üflemeli, "
                    "Su Geçirmez, Şarjlı"),
        "renk": METAL_RENK,
        "kullanım amacı": ("Düzleştirme, Şekillendirme, Kurutma, "
                           "Tıraş, Epilasyon, Bakım"),
    },

    # ------------------------------ KLIMA & ISITICILAR
    "klima": {
        "tip": ("Duvar Tipi (Split), Salon Tipi, Portatif, Kaset Tipi, "
                "Pencere Tipi, Isı Pompası, Elektrikli, Gazlı, "
                "Infrared, Yağlı Radyatör, Fanlı, Konvektör"),
        "kapasite": ("30 L altı, 30-50 L, 50-65 L, 65-80 L, "
                     "80 L ve üzeri"),
        "özellik": ("İnverter, Wi-Fi Kontrollü, Uzaktan Kumandalı, "
                    "Sessiz Çalışma, Otomatik Kapanma, Termostatlı, "
                    "Devrilme Koruması, Iyonizer"),
        "renk": METAL_RENK,
        "güç": ("1000 W altı, 1000-1500 W, 1500-2000 W, 2000-2500 W, "
                "2500 W ve üzeri"),
        "materyal": "Plastik, Metal, Paslanmaz Çelik, Alüminyum, Cam",
    },

    # ------------------------------ FOTO & KAMERA
    "foto": {
        "tip": ("DSLR, Aynasız (Mirrorless), Kompakt, Şipşak (Instant), "
                "Aksiyon Kamera, Video Kamera, Lens, Tripod"),
        "özellik": ("Wi-Fi, Bluetooth, Su Geçirmez, Görüntü Sabitleme, "
                    "4K Video, Gece Görüşü, Dokunmatik Ekran, "
                    "Katlanabilir Ekran"),
        "renk": METAL_RENK,
        "kapasite": "16 GB, 32 GB, 64 GB, 128 GB, 256 GB, 512 GB, 1 TB",
        "materyal": "Plastik, Metal, Alüminyum, Magnezyum Alaşım",
    },
})


# ---- Son eksikler ----
BAGLAM_SECENEKLERI["ayakkabi"].update({
    "taban": ("Kaymaz Taban, Deri Taban, Kauçuk Taban, Keçe Taban, "
              "EVA Taban, Termo Taban"),
    "çeşit": "Halı Saha, Çim Saha, Salon, Sokak, Antrenman",
})
BAGLAM_SECENEKLERI["aksesuar"].update({
    "tip": ("Saat, Gözlük, Cüzdan, Kemer, Şapka, Takı, Kartlık, Atkı, "
            "Eldiven, Kravat"),
    "model": ("Kolye, Bileklik, Yüzük, Küpe, Saat, Gözlük, Kemer, Şapka, "
              "Broş, Set"),
})
BAGLAM_SECENEKLERI["canta"]["model"] = ("El Çantası, Omuz Çantası, "
                                        "Sırt Çantası, Çapraz Çanta, "
                                        "Cüzdan, Valiz, Portföy")
BAGLAM_SECENEKLERI["bebek"]["model"] = ("Akülü Araba, Akülü Motor, "
                                        "Bisiklet, Scooter, "
                                        "Üç Tekerlekli, İtme Kollu")
BAGLAM_SECENEKLERI["spor"].update({
    "taşıma kapasitesi": ("100 kg'a kadar, 100-120 kg, 120-150 kg, "
                          "150 kg ve üzeri"),
    "tip": ("Şapka (Kep), Vizör, Bere, Bandana, Toz, Kapsül, Tablet, "
            "Termal, Sıvı"),
    "hacim": "400 ml, 500 ml, 600 ml, 700 ml, 1000 ml ve üzeri",
})
BAGLAM_SECENEKLERI["ev"].update({
    "taban": ("Kaymaz Taban, Jüt Taban, Lateks Taban, Keçe Taban, "
              "Tabansız"),
    "ağırlık": ("500 gr altı, 500-1000 gr, 1-2 kg, 2-3 kg, 3-4 kg, "
                "4 kg ve üzeri"),
    "paket adedi": "1, 2, 3, 4, 6 ve üzeri",
})
BAGLAM_SECENEKLERI["kitap"]["form"] = ("Stick, Sıvı, Jel, Sprey, Bant, "
                                       "Toz, Silikon")
BAGLAM_SECENEKLERI["kozmetik"].update({
    "kullanım şekli": ("Sıcak Ağda, Soğuk Ağda, Bant Ağda, Roll-On, "
                       "Sprey, Konserve Ağda"),
    "çeşit": ("Mumlu, Mumsuz, Naneli, Şeritli, Kürdanlı, Vitamin, "
              "Mineral, Bitkisel"),
})
BAGLAM_SECENEKLERI["supermarket"]["içerik"] = ("Tavuk, Somon, Ton Balığı, "
                                               "Biftek, Kuzu, Hindi, "
                                               "Karışık Et, Sebzeli, "
                                               "Tahılsız, Az Tahıllı")


# ============ HAM VERİ (kategori ağacı ve filtreleri) ============
raw_data = """
Kadın - Giyim
cinsiyet
beden
boyut/ebat
renk
materyal
fiyat
kol tipi
desen
sezon
yaka tipi
kol boyu
boy
kalıp
kumaş tipi
bel
paça tipi
ek özellik
siluet
parça sayısı
cep
dokuma tipi
tip
yaş
paket i̇çeriği
kapama şekli
kap
sürdürülebilirlik detayı
kemer/kuşak durumu
astar durumu
kutu durumu
alt siluet
üst siluet
dolgu materyali

Kadın - Giyim - Elbise
cinsiyet
beden
renk
boy
fiyat
kol tipi
materyal
kol boyu
yaka tipi
kalıp
sezon
kumaş tipi
desen
siluet
astar durumu
ek özellik
dokuma tipi
cep
ürün detayı
kapama şekli
kemer/kuşak durumu
kap
paket i̇çeriği
sürdürülebilirlik detayı
kutu durumu

Kadın - Giyim - Tişört
cinsiyet
beden
renk
yaka tipi
materyal
kol boyu
fiyat
kalıp
kol tipi
desen
boy
sezon
siluet
kumaş tipi
paket i̇çeriği
ek özellik
cep
sürdürülebilirlik detayı

Kadın - Giyim - Gömlek
cinsiyet
beden
renk
kol boyu
materyal
fiyat
kol tipi
kalıp
boy
desen
yaka tipi
kumaş tipi
sezon
cep
siluet
kutu durumu
sürdürülebilirlik detayı
ek özellik

Kadın - Giyim - Kot Pantolon
cinsiyet
beden
renk
kalıp
paça tipi
bel
fiyat
materyal
boy
ek özellik
siluet
sezon
desen
kumaş tipi
kapama şekli
sürdürülebilirlik detayı

Kadın - Giyim - Kot Ceket
cinsiyet
beden
renk
fiyat
materyal
kalıp
boy
sezon
yaka tipi
kol boyu
kumaş tipi
kol tipi
kapama şekli
desen
siluet
kemer/kuşak durumu
sürdürülebilirlik detayı
ek özellik

Kadın - Giyim - Pantolon
cinsiyet
beden
renk
materyal
paça tipi
fiyat
kalıp
bel
kumaş tipi
sezon
boy
desen
kapama şekli
siluet
dokuma tipi
kemer/kuşak durumu
sürdürülebilirlik detayı

Kadın - Giyim - Mont
cinsiyet
beden
renk
fiyat
boy
materyal
sezon
dolgu materyali
yaka tipi
kalıp
kol tipi
desen
kumaş tipi
siluet
kemer/kuşak durumu
astar durumu
sürdürülebilirlik detayı
kutu durumu

Kadın - Giyim - Bluz
cinsiyet
beden
renk
kol boyu
materyal
fiyat
kol tipi
yaka tipi
sezon
boy
kalıp
desen
kumaş tipi
siluet
ek özellik
paket i̇çeriği
sürdürülebilirlik detayı

Kadın - Giyim - Ceket
cinsiyet
beden
renk
materyal
fiyat
kalıp
boy
kol boyu
sezon
kumaş tipi
desen
yaka tipi
kapama şekli
kol tipi
siluet
astar durumu
kemer/kuşak durumu
sürdürülebilirlik detayı
ek özellik

Kadın - Giyim - Etek
cinsiyet
beden
boy
renk
materyal
fiyat
kalıp
kumaş tipi
sezon
desen
siluet
bel
astar durumu
kemer/kuşak durumu
ek özellik
kapama şekli
sürdürülebilirlik detayı

Kadın - Giyim - Kazak
cinsiyet
beden
renk
materyal
fiyat
yaka tipi
kol boyu
sezon
kalıp
desen
boy
kumaş tipi
siluet
kol tipi
sürdürülebilirlik detayı
kutu durumu

Kadın - Giyim - Tesettür
cinsiyet
beden
boyut/ebat
materyal
fiyat
renk
sezon
kol boyu
boy
yaka tipi
ek özellik
desen
kalıp
kumaş tipi
paça tipi
cep
kapama şekli
dokuma tipi
bel
astar durumu
kemer/kuşak durumu
kol tipi
sürdürülebilirlik detayı
siluet
kutu durumu

Kadın - Giyim - Büyük Beden
cinsiyet
beden
kol tipi
materyal
renk
boy
kol boyu
yaka tipi
fiyat
sezon
kumaş tipi
kalıp
desen
bel
sürdürülebilirlik detayı
kemer/kuşak durumu
siluet
paça tipi
astar durumu

Kadın - Giyim - Trençkot
cinsiyet
beden
renk
boy
fiyat
materyal
astar durumu
kalıp
sezon
kol boyu
kapama şekli
kumaş tipi
siluet
desen
kemer/kuşak durumu
yaka tipi
kol tipi
sürdürülebilirlik detayı
dokuma tipi
cep

Kadın - Giyim - Yağmurluk & Rüzgarlık
cinsiyet
beden
renk
fiyat
boy
kalıp
yaka tipi
materyal
kol tipi
sezon
kumaş tipi
desen
kemer/kuşak durumu
siluet
cep
sürdürülebilirlik detayı
kapama şekli

Kadın - Giyim - Sweatshirt
cinsiyet
beden
renk
fiyat
yaka tipi
materyal
desen
kalıp
sezon
dokuma tipi
kol boyu
boy
kol tipi
kumaş tipi
sürdürülebilirlik detayı
siluet

Kadın - Giyim - Kaban
cinsiyet
beden
renk
boy
fiyat
materyal
siluet
astar durumu
kumaş tipi
yaka tipi
kalıp
sezon
desen
kol boyu
kemer/kuşak durumu
kol tipi
dolgu materyali
kutu durumu
kapama şekli
ek özellik
sürdürülebilirlik detayı
cep

Kadın - Giyim - Hırka
cinsiyet
beden
renk
fiyat
materyal
boy
kol boyu
sezon
yaka tipi
kapama şekli
kalıp
kumaş tipi
kol tipi
siluet
desen
sürdürülebilirlik detayı
kutu durumu
parça sayısı

Kadın - Giyim - Palto
cinsiyet
beden
renk
fiyat
yaka tipi
siluet
boy
materyal
kalıp
desen
kol tipi
sürdürülebilirlik detayı

Kadın - Ayakkabı
cinsiyet
beden
renk
topuk boyu
materyal
fiyat
topuk tipi
dış materyal
burun tipi
bağlama şekli
sezon
kalıp
desen
ek özellik
kullanım alanı
i̇ç astar & i̇ç taban materyali
taban tipi
alt taban materyali
sürdürülebilirlik detayı

Kadın - Ayakkabı - Topuklu Ayakkabı
cinsiyet
beden
renk
topuk boyu
topuk tipi
fiyat
burun tipi
materyal
bağlama şekli
kalıp
dış materyal
sezon
desen
ek özellik
i̇ç astar & i̇ç taban materyali
alt taban materyali

Kadın - Ayakkabı - Sneaker
cinsiyet
beden
renk
fiyat
topuk boyu
materyal
taban tipi
dış materyal
bağlama şekli
ek özellik
topuk tipi
alt taban materyali
desen
sürdürülebilirlik detayı
i̇ç astar & i̇ç taban materyali

Kadın - Ayakkabı - Günlük Ayakkabı
cinsiyet
beden
renk
materyal
topuk boyu
fiyat
topuk tipi
dış materyal
ek özellik
bağlama şekli
kalıp
burun tipi
i̇ç astar & i̇ç taban materyali
sürdürülebilirlik detayı
desen
alt taban materyali

Kadın - Ayakkabı - Babet
cinsiyet
beden
renk
fiyat
materyal
topuk boyu
burun tipi
dış materyal
topuk tipi
kalıp
bağlama şekli
sürdürülebilirlik detayı
alt taban materyali
i̇ç astar & i̇ç taban materyali
desen
ek özellik

Kadın - Ayakkabı - Sandalet
cinsiyet
beden
renk
topuk boyu
materyal
fiyat
topuk tipi
dış materyal
bağlama şekli
özellik
sürdürülebilirlik detayı

Kadın - Ayakkabı - Bot
cinsiyet
beden
renk
topuk boyu
fiyat
materyal
topuk tipi
dış materyal
bağlama şekli
burun tipi
i̇ç astar & i̇ç taban materyali
ek özellik
kullanım alanı
alt taban materyali
kalıp

Kadın - Ayakkabı - Çizme
cinsiyet
beden
renk
topuk boyu
materyal
fiyat
topuk tipi
dış materyal
bağlama şekli
burun tipi
özellik
i̇ç astar & i̇ç taban materyali
sürdürülebilirlik detayı
alt taban materyali

Kadın - Ayakkabı - Kar Botu
cinsiyet
beden
ek özellik
renk
fiyat
topuk boyu
topuk tipi
desen
bağlama şekli
dış materyal
materyal
alt taban materyali
i̇ç astar & i̇ç taban materyali
sürdürülebilirlik detayı

Kadın - Ayakkabı - Loafer
cinsiyet
beden
renk
materyal
topuk boyu
fiyat
dış materyal
topuk tipi
i̇ç astar & i̇ç taban materyali
burun tipi
sürdürülebilirlik detayı
kutu durumu

Kadın - Çanta
cinsiyet
beden
renk
fiyat
materyal
boyut
kapasite
desen
yaş
ek özellik
kumaş tipi
sürdürülebilirlik detayı

Kadın - Çanta - Omuz Çantası
cinsiyet
beden
renk
materyal
fiyat
kapasite
yaş
kumaş tipi
desen
sürdürülebilirlik detayı

Kadın - Çanta - Sırt Çantası
cinsiyet
renk
fiyat
boyut
materyal
kapasite
desen

Kadın - Çanta - Bel Çantası
cinsiyet
renk
fiyat
materyal
desen
sürdürülebilirlik detayı

Kadın - Çanta - Okul Çantası
cinsiyet
renk
fiyat
tip
desen
çocuk cinsiyeti
kapasite
materyal
sürdürülebilirlik detayı
deri kalitesi

Kadın - Çanta - Laptop Çantası
cinsiyet
çanta tipi
renk
fiyat
ekran boyut aralığı
suya/tere dayanıklılık

Kadın - Çanta - Portföy
cinsiyet
renk
materyal
fiyat
sürdürülebilirlik detayı

Kadın - Çanta - Postacı Çantası
cinsiyet
renk
materyal
fiyat

Kadın - Çanta - El Çantası
cinsiyet
renk
fiyat
materyal
boyut
kapasite
desen
ek özellik

Kadın - Çanta - Kanvas Çanta
cinsiyet
beden
renk
fiyat
kapasite
materyal
kumaş tipi
yaş
desen
sürdürülebilirlik detayı

Kadın - Çanta - Makyaj Çantası
fiyat
renk
materyal

Kadın - Çanta - Abiye Çanta
cinsiyet
renk
fiyat
materyal
desen
sürdürülebilirlik detayı

Kadın - Çanta - Çapraz Çanta
cinsiyet
beden
renk
materyal
fiyat
kapasite
yaş
desen
sürdürülebilirlik detayı
kumaş tipi

Kadın - Çanta - Bez Çanta
cinsiyet
beden
renk
fiyat
yaş
desen
kumaş tipi
sürdürülebilirlik detayı
materyal

Kadın - Çanta - Anne Bebek Çantası
cinsiyet
fiyat
renk
materyal
çocuk cinsiyeti

Kadın - Çanta - Evrak Çantası
cinsiyet
beden
fiyat
renk
çanta tipi
ekran boyut aralığı
dosya tipi
suya/tere dayanıklılık

Kadın - Çanta - Tote Çanta
cinsiyet
beden
renk
materyal
fiyat
kumaş tipi
yaş
desen
sürdürülebilirlik detayı
kapasite

Kadın - Çanta - Beslenme Çantası
cinsiyet
renk
fiyat
kapasite
çocuk cinsiyeti
desen
sürdürülebilirlik detayı

Kadın - Çanta - Kartlık
cinsiyet
renk
fiyat
materyal
boyut
deri kalitesi
yaş
desen
sürdürülebilirlik detayı
tip

Kadın - Çanta - Cüzdan
cinsiyet
renk
fiyat
materyal
boyut
deri kalitesi
tip
desen
yaş
sürdürülebilirlik detayı

Kadın - Çanta - Kadın Spor Çantası
cinsiyet
renk
fiyat
boyut
materyal
kapasite
desen
sürdürülebilirlik detayı

Kadın - Aksesuar & Çanta
cinsiyet
beden
fiyat
materyal
renk
boyut/ebat
boyut
desen
ayar
kasa renk
model
tip
özellik
taş cinsi
yaş
sürdürülebilirlik detayı
kumaş tipi
cam tipi
kapasite
cam renk
çerçeve formu
çerçeve renk
çerçeve materyali
cam materyali
çerçeve tipi
mekanizma
kordon materyali
kasa materyali
kasa çapı
kordon renk
su geçirmezlik
cam şekli
ekartman
kadran renk
garanti süresi
deri kalitesi
kutu durumu
batarya türü
batarya boyutu

Kadın - Aksesuar & Çanta - Çanta
cinsiyet
beden
renk
fiyat
materyal
boyut
kapasite
desen
yaş
ek özellik
kumaş tipi
sürdürülebilirlik detayı

Kadın - Aksesuar & Çanta - Saat
cinsiyet
fiyat
renk
kordon materyali
su geçirmezlik
kadran renk
kasa materyali
kasa renk
özellik
mekanizma
cam tipi
cam şekli
garanti süresi
batarya boyutu
kasa çapı
batarya türü
kordon renk

Kadın - Aksesuar & Çanta - Takı
cinsiyet
beden
materyal
boyut/ebat
renk
fiyat
ayar
model
taş cinsi
özellik

Kadın - Aksesuar & Çanta - Cüzdan
cinsiyet
renk
fiyat
materyal
boyut
deri kalitesi
tip
desen
yaş
sürdürülebilirlik detayı

Kadın - Aksesuar & Çanta - Atkı
cinsiyet
beden
renk
materyal
fiyat
desen
kumaş tipi

Kadın - Aksesuar & Çanta - Bere
cinsiyet
beden
renk
fiyat
desen
kumaş tipi
materyal
kutu durumu

Kadın - Aksesuar & Çanta - Eldiven
cinsiyet
beden
materyal
renk
fiyat
desen
kumaş tipi

Kadın - Aksesuar & Çanta - Kemer
cinsiyet
beden
renk
materyal
fiyat

Kadın - Aksesuar & Çanta - Şal
cinsiyet
renk
materyal
boyut/ebat
fiyat
desen

Kadın - Ev & İç Giyim
cinsiyet
beden
materyal
renk
alt siluet
kalıp
fiyat
kumaş tipi
parça sayısı
desen
bel
kol boyu
kap
siluet
yaka tipi
boy
paket i̇çeriği
kol tipi
sürdürülebilirlik detayı
üst siluet
ek özellik

Kadın - Ev & İç Giyim - Pijama Takımı
cinsiyet
beden
materyal
kol boyu
boy
fiyat
renk
kol tipi
kumaş tipi
yaka tipi
sezon
desen
paça tipi
paket i̇çeriği
kapama şekli
bel
siluet

Kadın - Ev & İç Giyim - Gecelik
cinsiyet
beden
materyal
renk
boy
fiyat
kol tipi
kumaş tipi
kalıp
desen
siluet
paket i̇çeriği
kol boyu
kapama şekli
yaka tipi

Kadın - Ev & İç Giyim - Sütyen
cinsiyet
beden
kalıp
materyal
renk
kap
fiyat
paket i̇çeriği
siluet
kumaş tipi
üst siluet
desen
yaka tipi
kol boyu
parça sayısı

Kadın - Ev & İç Giyim - İç Çamaşırı Takımları
cinsiyet
beden
renk
materyal
kalıp
fiyat
alt siluet
üst siluet
desen
ek özellik
kumaş tipi
kap
bel
paket i̇çeriği
kapama şekli

Kadın - Ev & İç Giyim - Fantezi Giyim
cinsiyet
beden
renk
fiyat
materyal
kol boyu
boy
desen
paket i̇çeriği
kumaş tipi
kalıp
kol tipi
yaka tipi

Kadın - Ev & İç Giyim - Çorap
cinsiyet
beden
tip
renk
materyal
fiyat
siluet
paket i̇çeriği
sezon
boy
desen
ek özellik
kumaş tipi

Kadın - Ev & İç Giyim - Korse
cinsiyet
beden
renk
fiyat
desen
kalıp
kol boyu
boy
bel
materyal
yaka tipi
kumaş tipi
kap

Kadın - Ev & İç Giyim - Külot
cinsiyet
beden
materyal
kalıp
renk
paket i̇çeriği
fiyat
bel
parça sayısı
kumaş tipi
alt siluet
siluet
desen
boy

Kadın - Ev & İç Giyim - Büstiyer
cinsiyet
beden
renk
materyal
fiyat
yaka tipi
kol tipi
siluet
kalıp
kumaş tipi
kap
kol boyu
desen
boy
sürdürülebilirlik detayı
kutu durumu
paket i̇çeriği
ek özellik

Kadın - Ev & İç Giyim - Bralet
cinsiyet
beden
renk
materyal
kalıp
fiyat
kap
yaka tipi
kumaş tipi
desen
üst siluet
kol boyu
paket i̇çeriği
siluet
parça sayısı
alt siluet
bel
ek özellik

Kadın - Ev & İç Giyim - Atlet & Body
cinsiyet
beden
renk
materyal
kol tipi
fiyat
paket i̇çeriği
yaka tipi
kalıp
kol boyu
boy
desen
siluet
kumaş tipi
sürdürülebilirlik detayı

Kadın - Ev & İç Giyim - Kombinezon
cinsiyet
beden
materyal
renk
boy
kol boyu
yaka tipi
desen
fiyat
sürdürülebilirlik detayı
alt siluet
kalıp
kap

Kadın - Ev & İç Giyim - Jartiyer
cinsiyet
beden
renk
fiyat
desen
materyal
sürdürülebilirlik detayı
kalıp
paket i̇çeriği
boy

Kadın - Kozmetik
cinsiyet
fiyat
kullanma amacı
cilt tipi
renk
tip
yaşlanma karşıtı
hacim
refill
form
koku türü
etki
ek özellik
saç tipi
i̇çerik
kalıcılık
spf
özellik
boy
suya/tere dayanıklılık
set i̇çerik adeti
görünüm
ek hizmetler

Kadın - Kozmetik - Parfüm
cinsiyet
fiyat
koku türü
tip
hacim
refill

Kadın - Kozmetik - Göz Makyajı
renk
fiyat
form
suya/tere dayanıklılık
boy

Kadın - Kozmetik - Cilt Bakım
cinsiyet
kullanma amacı
cilt tipi
fiyat
i̇çerik
ek özellik
form
yaşlanma karşıtı
set i̇çerik adeti
hacim
spf
refill
renk
tip
ek hizmetler

Kadın - Kozmetik - Saç Bakımı
cinsiyet
saç tipi
etki
fiyat
özellik
renk
tip
kalıcılık
refill

Kadın - Kozmetik - Makyaj
fiyat
renk
form
boy
suya/tere dayanıklılık

Kadın - Kozmetik - Ağız Bakım
kullanım amacı
fiyat
i̇çerik
fırça kılı sertliği
ek hizmetler

Kadın - Kozmetik - Cinsel Sağlık
fiyat

Kadın - Kozmetik - Vücut Bakım
kullanma amacı
fiyat
ek özellik
hacim
refill
tip
form

Kadın - Kozmetik - Hijyenik Ped
özellik
fiyat

Kadın - Kozmetik - Duş Jeli & Kremleri
cinsiyet
hacim
fiyat
refill

Kadın - Kozmetik - Ruj
fiyat
renk
form
boy

Kadın - Kozmetik - Dudak Nemlendirici
fiyat
form
görünüm
tip
kutu durumu
renk
kullanma amacı
spf
ek özellik

Kadın - Kozmetik - Aydınlatıcı & Highlighter
fiyat
form
renk

Kadın - Kozmetik - Eyeliner
renk
fiyat
suya/tere dayanıklılık
form

Kadın - Kozmetik - Ten Makyajı
fiyat
kapatıcılık
cilt tipi
renk
form
suya/tere dayanıklılık
spf
görünüm

Kadın - Kozmetik - Manikür & Pedikür
fiyat

Kadın - Kozmetik - BB & CC Krem
fiyat
cilt tipi
kapatıcılık
renk
spf
suya/tere dayanıklılık

Kadın - Kozmetik - El Kremi
fiyat
hacim
tip
ek özellik
kutu durumu

Kadın - Kozmetik - Yüz Nemlendirici
cilt tipi
kullanma amacı
yaşlanma karşıtı
hacim
fiyat
i̇çerik
ek özellik
form
spf
refill

Kadın - Spor & Outdoor
cinsiyet
beden
renk
sezon
kol boyu
materyal
fiyat
desen
boy
sürdürülebilirlik detayı
kalıp
kumaş tipi
bel
paça tipi
cep
ek özellik
siluet
yaka tipi
kol tipi
paket i̇çeriği
paça boyu
yaş
kumaş teknolojisi
kutu durumu

Kadın - Spor & Outdoor - Sweatshirt
cinsiyet
beden
renk
yaka tipi
fiyat
kol tipi
desen
kalıp
boy
kol boyu
materyal
sürdürülebilirlik detayı
cep

Kadın - Spor & Outdoor - Tişört
cinsiyet
beden
kol tipi
renk
fiyat
kumaş teknolojisi
materyal
kalıp
boy
kol boyu
yaka tipi
desen
sürdürülebilirlik detayı
ek özellik

Kadın - Spor & Outdoor - Spor Sütyeni
cinsiyet
beden
renk
materyal
kalıp
kap
fiyat
yaka tipi
ek özellik
kol boyu
desen
sürdürülebilirlik detayı
kumaş tipi
kutu durumu
paket i̇çeriği
sezon

Kadın - Spor & Outdoor - Tayt
cinsiyet
beden
renk
boy
materyal
paça tipi
fiyat
bel
ek özellik
yaş
kalıp
sezon
kumaş tipi
desen
sürdürülebilirlik detayı
kutu durumu

Kadın - Spor & Outdoor - Eşofman
cinsiyet
beden
paça tipi
renk
fiyat
sezon
materyal
kalıp
bel
siluet
desen
boy
cep
paça boyu
kumaş tipi
sürdürülebilirlik detayı
ek özellik
paket i̇çeriği
kol boyu
kol tipi
yaka tipi

Kadın - Spor & Outdoor - Koşu Ayakkabısı
cinsiyet
beden
renk
fiyat
taban tipi
topuk boyu
bağlama şekli
materyal
ek özellik
dış materyal
topuk tipi
desen
i̇ç astar & i̇ç taban materyali
alt taban materyali
sürdürülebilirlik detayı

Kadın - Spor & Outdoor - Spor Çantası
cinsiyet
renk
fiyat
boyut
kapasite
materyal
desen
sürdürülebilirlik detayı

Kadın - Spor & Outdoor - Spor Ekipmanları
cinsiyet
beden
fiyat
özellik
renk
ek hizmetler

Kadın - Spor & Outdoor - Outdoor Ayakkabı
cinsiyet
beden
renk
ek özellik
kumaş teknolojisi
materyal
fiyat
kalıp
topuk boyu
topuk tipi
bağlama şekli
sürdürülebilirlik detayı
dış materyal
alt taban materyali
i̇ç astar & i̇ç taban materyali
taban teknolojisi

Kadın - Spor & Outdoor - Kar Botu
cinsiyet
beden
ek özellik
renk
fiyat
topuk boyu
topuk tipi
desen
bağlama şekli
dış materyal
materyal
alt taban materyali
i̇ç astar & i̇ç taban materyali
sürdürülebilirlik detayı

Kadın - Spor & Outdoor - Outdoor Ekipmanları
özellik
fiyat
renk
materyal
ek hizmetler

Kadın - Spor & Outdoor - Sporcu Besinleri
gramaj
form
fiyat
aroma
servis

Kadın - Spor & Outdoor - Sporcu Aksesuarları
cinsiyet
beden
renk
fiyat
model

Kadın - Spor & Outdoor - Outdoor Çanta
cinsiyet
renk
fiyat
boyut
kapasite
materyal
desen

Kadın - Spor & Outdoor - Kayak Malzemeleri
cinsiyet
beden
renk
fiyat
kumaş tipi

Kadın - Spor & Outdoor - Uyku Tulumu
fiyat
model
renk

Kadın - Spor & Outdoor - Mat
fiyat
renk

Kadın - Spor & Outdoor - Dağcılık
renk
fiyat

Kadın - Spor & Outdoor - Kadın Spor Ceket
cinsiyet
beden
fiyat
renk
kalıp
kumaş tipi
boy
kol tipi
desen
siluet
cep
yaka tipi
materyal
sürdürülebilirlik detayı
kapama şekli
ek özellik

Kadın - Spor & Outdoor - Spor Ayakkabı
cinsiyet
beden
renk
fiyat
taban tipi
topuk boyu
bağlama şekli
materyal
ek özellik
dış materyal
topuk tipi
desen
i̇ç astar & i̇ç taban materyali
alt taban materyali
sürdürülebilirlik detayı

Erkek - Giyim
cinsiyet
beden
kalıp
materyal
renk
fiyat
sezon
yaka tipi
kol boyu
kol tipi
kumaş tipi
boy
paça tipi
paket i̇çeriği
desen
kumaş teknolojisi
sürdürülebilirlik detayı
siluet
cep
ek özellik
dokuma tipi
bel
kemer/kuşak durumu
kutu durumu
kapama şekli
parça sayısı
tip
astar durumu
dolgu materyali

Erkek - Giyim - Tişört
cinsiyet
beden
yaka tipi
kalıp
renk
materyal
fiyat
kol tipi
desen
kol boyu
kumaş tipi
paket i̇çeriği
sezon
cep
boy
siluet
ek özellik
kumaş teknolojisi
sürdürülebilirlik detayı

Erkek - Giyim - Şort
cinsiyet
beden
materyal
renk
kalıp
fiyat
kumaş tipi
boy
cep
desen
sezon
kapama şekli
bel
paça tipi
kemer/kuşak durumu
siluet
sürdürülebilirlik detayı

Erkek - Giyim - Gömlek
cinsiyet
beden
renk
materyal
kalıp
kol boyu
desen
yaka tipi
kol tipi
fiyat
sezon
kumaş tipi
cep
ek özellik
boy
siluet
kutu durumu
sürdürülebilirlik detayı

Erkek - Giyim - Eşofman
cinsiyet
beden
paça tipi
kalıp
renk
materyal
fiyat
sezon
cep
kumaş tipi
desen
bel
paket i̇çeriği
paça boyu
boy
siluet
yaka tipi
ek özellik
sürdürülebilirlik detayı
kol boyu
kol tipi

Erkek - Giyim - Pantolon
cinsiyet
beden
kalıp
renk
materyal
kumaş tipi
paça tipi
fiyat
bel
sezon
kemer/kuşak durumu
boy
dokuma tipi
desen
kapama şekli
siluet
sürdürülebilirlik detayı

Erkek - Giyim - Ceket
cinsiyet
beden
renk
materyal
kalıp
fiyat
sezon
kapama şekli
yaka tipi
kumaş tipi
desen
astar durumu
siluet
sürdürülebilirlik detayı
boy
kol boyu
kol tipi
kemer/kuşak durumu
ek özellik

Erkek - Giyim - Kot Pantolon
cinsiyet
beden
kalıp
renk
paça tipi
fiyat
bel
materyal
boy
sezon
siluet
kapama şekli
kumaş tipi
ek özellik
desen
sürdürülebilirlik detayı

Erkek - Giyim - Yelek
cinsiyet
beden
materyal
renk
kalıp
yaka tipi
kol tipi
fiyat
dolgu materyali
sezon
kumaş tipi
kapama şekli
boy
desen
kemer/kuşak durumu
siluet
sürdürülebilirlik detayı

Erkek - Giyim - Kazak
cinsiyet
beden
yaka tipi
materyal
renk
kalıp
fiyat
kol boyu
sezon
desen
kumaş tipi
kol tipi
boy
siluet
sürdürülebilirlik detayı
kutu durumu

Erkek - Giyim - Mont
cinsiyet
beden
renk
fiyat
materyal
sezon
kalıp
yaka tipi
dolgu materyali
boy
siluet
desen
kumaş tipi
astar durumu
kol tipi
kemer/kuşak durumu
sürdürülebilirlik detayı
kutu durumu

Erkek - Giyim - Takım Elbise
cinsiyet
beden
renk
kalıp
materyal
fiyat
sezon
desen
yaka tipi
boy
ek özellik
paça tipi
bel
kol tipi
kumaş tipi
sürdürülebilirlik detayı
kol boyu

Erkek - Giyim - Sweatshirt
cinsiyet
beden
yaka tipi
renk
materyal
kalıp
fiyat
desen
sezon
kol boyu
dokuma tipi
kol tipi
siluet
boy
kumaş tipi
sürdürülebilirlik detayı

Erkek - Giyim - Deri Mont
cinsiyet
beden
renk
materyal
fiyat
kumaş tipi
boy
yaka tipi
kalıp
kol tipi
desen
astar durumu
kemer/kuşak durumu
siluet
sürdürülebilirlik detayı
kutu durumu
dolgu materyali
sezon

Erkek - Giyim - Kaban
cinsiyet
beden
renk
materyal
fiyat
kalıp
yaka tipi
boy
kapama şekli
astar durumu
sezon
siluet
dolgu materyali
kumaş tipi
desen
kol boyu
kemer/kuşak durumu
kol tipi
kutu durumu
ek özellik
sürdürülebilirlik detayı

Erkek - Giyim - Hırka
cinsiyet
beden
renk
materyal
fiyat
yaka tipi
kalıp
kumaş tipi
boy
kapama şekli
kol tipi
kol boyu
desen
siluet
sürdürülebilirlik detayı
kutu durumu
parça sayısı
sezon

Erkek - Giyim - Trençkot
cinsiyet
beden
renk
fiyat
materyal
boy
kalıp
yaka tipi
kemer/kuşak durumu
astar durumu
kapama şekli
sürdürülebilirlik detayı
kumaş tipi
desen
kol boyu
kol tipi
siluet
dokuma tipi
sezon

Erkek - Giyim - Palto
cinsiyet
beden
renk
materyal
kalıp
fiyat
boy
yaka tipi
desen
kol tipi
siluet
sürdürülebilirlik detayı

Erkek - Giyim - Yağmurluk
cinsiyet
beden
renk
fiyat
kalıp
materyal
sezon
kumaş tipi
desen
boy
yaka tipi
kemer/kuşak durumu
kol tipi
siluet
cep
sürdürülebilirlik detayı
kapama şekli

Erkek - Giyim - Blazer
cinsiyet
beden
renk
materyal
kalıp
yaka tipi
sezon
fiyat
astar durumu
desen
kumaş tipi
kol tipi
kol boyu
kemer/kuşak durumu
siluet
boy
kapama şekli

Erkek - Giyim - Polar
cinsiyet
beden
renk
fiyat
yaka tipi
kalıp
kapama şekli
cep
materyal
boy
kol boyu
kol tipi
desen
sürdürülebilirlik detayı
kumaş tipi
siluet
boy / ölçü

Erkek - Ayakkabı
cinsiyet
beden
renk
fiyat
materyal
dış materyal
bağlama şekli
topuk boyu
taban tipi
ek özellik
alt taban materyali
i̇ç astar & i̇ç taban materyali
topuk tipi
kullanım alanı
burun tipi
desen
kalıp
sürdürülebilirlik detayı

Erkek - Ayakkabı - Spor Ayakkabı
cinsiyet
beden
renk
fiyat
materyal
bağlama şekli
taban tipi
dış materyal
ek özellik
topuk boyu
topuk tipi
alt taban materyali
i̇ç astar & i̇ç taban materyali
sürdürülebilirlik detayı
desen

Erkek - Ayakkabı - Günlük Ayakkabı
cinsiyet
beden
renk
materyal
fiyat
dış materyal
bağlama şekli
topuk boyu
ek özellik
topuk tipi
alt taban materyali
sürdürülebilirlik detayı

Erkek - Ayakkabı - Yürüyüş Ayakkabısı
cinsiyet
beden
fiyat
renk
bağlama şekli
materyal
ek özellik
topuk boyu
dış materyal

Erkek - Ayakkabı - Krampon
cinsiyet
beden
fiyat
renk
bağlama şekli
spor branşı
topuk tipi
alt taban materyali
dış materyal
topuk boyu
ek özellik
kumaş tipi
desen
sürdürülebilirlik detayı
i̇ç astar & i̇ç taban materyali

Erkek - Ayakkabı - Sneaker
cinsiyet
beden
renk
fiyat
materyal
dış materyal
taban tipi
bağlama şekli
topuk boyu
ek özellik
i̇ç astar & i̇ç taban materyali
alt taban materyali
desen
topuk tipi
sürdürülebilirlik detayı

Erkek - Ayakkabı - Klasik
cinsiyet
beden
renk
materyal
fiyat
dış materyal
bağlama şekli
alt taban materyali
topuk boyu
topuk tipi
sürdürülebilirlik detayı

Erkek - Ayakkabı - Bot
cinsiyet
beden
renk
dış materyal
fiyat
bağlama şekli
materyal
kalıp
ek özellik
kullanım alanı
topuk boyu
i̇ç astar & i̇ç taban materyali
burun tipi
topuk tipi
alt taban materyali

Erkek - Ayakkabı - Kar Botu
cinsiyet
beden
fiyat
ek özellik
dış materyal
renk
alt taban materyali
topuk tipi
topuk boyu
desen
bağlama şekli
materyal
sürdürülebilirlik detayı
i̇ç astar & i̇ç taban materyali

Erkek - Ayakkabı - Deri ayakkabı
cinsiyet
beden
renk
materyal
fiyat
topuk boyu
topuk tipi
dış materyal
bağlama şekli
sürdürülebilirlik detayı
alt taban materyali
i̇ç astar & i̇ç taban materyali
ek özellik
desen
taban tipi

Erkek - Ayakkabı - Loafer
cinsiyet
beden
renk
materyal
fiyat
dış materyal
topuk tipi
i̇ç astar & i̇ç taban materyali
topuk boyu
burun tipi
sürdürülebilirlik detayı
kutu durumu

Erkek - Ayakkabı - Ev Terliği
cinsiyet
beden
materyal
sezon
renk
fiyat
dış materyal
paket i̇çeriği
topuk tipi
sürdürülebilirlik detayı
topuk boyu

Erkek - Ayakkabı - Koşu Ayakkabısı
cinsiyet
beden
renk
fiyat
dış materyal
topuk boyu
ek özellik
topuk tipi
bağlama şekli
alt taban materyali
i̇ç astar & i̇ç taban materyali
desen
sürdürülebilirlik detayı

Erkek - Ayakkabı - Çizme
cinsiyet
beden
fiyat
materyal
renk
topuk boyu
topuk tipi
burun tipi
bağlama şekli
sürdürülebilirlik detayı
alt taban materyali
i̇ç astar & i̇ç taban materyali
dış materyal

Erkek - Kişisel Bakım
cinsiyet
fiyat
kalıcılık
özellik
renk
refill
hacim
tip
koku türü
saç tipi
etki

Erkek - Kişisel Bakım - Parfüm
cinsiyet
fiyat
koku türü
tip
hacim
refill

Erkek - Kişisel Bakım - Cinsel Sağlık
fiyat

Erkek - Kişisel Bakım - Tıraş Bıçağı
cinsiyet
bıçak sayısı
tipi
fiyat

Erkek - Kişisel Bakım - Deodorant
cinsiyet
form
hacim
fiyat
koruma süresi

Erkek - Çanta
cinsiyet
beden
renk
materyal
fiyat
boyut
kapasite
kumaş tipi
yaş
desen
sürdürülebilirlik detayı

Erkek - Çanta - Sırt Çantası
cinsiyet
boyut
renk
fiyat
kapasite
materyal
desen

Erkek - Çanta - Spor Çanta
cinsiyet
kapasite
fiyat
boyut
renk
materyal
desen
sürdürülebilirlik detayı

Erkek - Çanta - Laptop Çantası
cinsiyet
çanta tipi
fiyat
renk
suya/tere dayanıklılık
ekran boyut aralığı

Erkek - Çanta - Valiz & Bavul
cinsiyet
materyal
kapasite
renk
fiyat
boyut
sürdürülebilirlik detayı

Erkek - Çanta - Postacı Çantası
cinsiyet
materyal
renk
fiyat

Erkek - Çanta - Bel Çantası
cinsiyet
renk
fiyat
materyal
desen
sürdürülebilirlik detayı

Erkek - Çanta - Bez Çanta
cinsiyet
beden
renk
fiyat
yaş
desen
kumaş tipi
sürdürülebilirlik detayı
materyal

Erkek - Çanta - Evrak Çantası
cinsiyet
beden
fiyat
renk
çanta tipi
ekran boyut aralığı
dosya tipi
suya/tere dayanıklılık

Erkek - Çanta - Cüzdan
cinsiyet
fiyat
materyal
boyut
renk
tip
deri kalitesi
yaş
desen
sürdürülebilirlik detayı

Erkek - Büyük Beden
cinsiyet
beden
kalıp
materyal
kol tipi
desen
kumaş tipi
renk
fiyat
boy
kol boyu
yaka tipi
sürdürülebilirlik detayı
sezon
siluet

Erkek - Büyük Beden - Büyük Beden Sweatshirt
cinsiyet
beden
yaka tipi
renk
fiyat
boy
kumaş tipi
kol tipi
kol boyu
kalıp
desen
siluet
materyal
sürdürülebilirlik detayı
sezon
kapama şekli

Erkek - Büyük Beden - Büyük Beden T-shirt
cinsiyet
beden
kalıp
yaka tipi
renk
kol boyu
fiyat
desen
materyal
kol tipi
boy
kumaş tipi
sezon
sürdürülebilirlik detayı

Erkek - Büyük Beden - Büyük Beden Gömlek
cinsiyet
beden
kalıp
kol boyu
renk
materyal
kol tipi
boy
desen
sezon
fiyat
yaka tipi
cep
kumaş tipi
sürdürülebilirlik detayı

Erkek - Büyük Beden - Büyük Beden Pantolon
cinsiyet
beden
kalıp
materyal
renk
fiyat
boy
bel
paça tipi
kumaş tipi
sezon
kemer/kuşak durumu
desen
sürdürülebilirlik detayı

Erkek - Büyük Beden - Büyük Beden Mont
cinsiyet
beden
materyal
renk
sezon
kumaş tipi
fiyat
kalıp
kemer/kuşak durumu
boy
yaka tipi
kol tipi
desen
siluet
astar durumu
sürdürülebilirlik detayı
dolgu materyali

Erkek - Büyük Beden - Büyük Beden Kazak
cinsiyet
beden
renk
fiyat
kumaş tipi
boy
kalıp
kol tipi
yaka tipi
desen
kol boyu
siluet
materyal
sürdürülebilirlik detayı
sezon
persona
kapama şekli

Erkek - Büyük Beden - Büyük Beden Hırka
cinsiyet
beden
materyal
renk
fiyat
yaka tipi
kumaş tipi
kol tipi
boy
kalıp
desen
siluet
sürdürülebilirlik detayı
kemer/kuşak durumu
sezon

Erkek - Büyük Beden - Büyük Beden Kaban
cinsiyet
beden
kalıp
kumaş tipi
renk
fiyat
boy
astar durumu
kemer/kuşak durumu
materyal
sürdürülebilirlik detayı
kol tipi
yaka tipi
desen
dolgu materyali
siluet
kapama şekli
kalınlık
sezon

Erkek - Büyük Beden - Büyük Beden Eşofman Altı
cinsiyet
beden
paça tipi
kalıp
renk
boy
sezon
materyal
fiyat
bel
kumaş tipi
siluet
paça boyu
desen
cep
sürdürülebilirlik detayı

Erkek - Saat & Aksesuar
cinsiyet
beden
boyut/ebat
boyut
materyal
fiyat
renk
kordon materyali
mekanizma
kasa renk
kadran renk
taş cinsi
yaş
desen
özellik
ayar
cam tipi
sürdürülebilirlik detayı
kumaş tipi
kasa materyali
kasa çapı
kordon renk
su geçirmezlik
cam şekli
cam renk
çerçeve renk
çerçeve formu
garanti süresi
çerçeve materyali
cam materyali
çerçeve tipi
ekartman
kapasite
deri kalitesi
tip
batarya türü
kutu durumu
batarya boyutu

Erkek - Saat & Aksesuar - Saat
cinsiyet
fiyat
kordon materyali
renk
mekanizma
su geçirmezlik
kadran renk
kasa materyali
cam tipi
özellik
kasa renk
cam şekli
garanti süresi
batarya türü
batarya boyutu
kasa çapı
kordon renk

Erkek - Saat & Aksesuar - Güneş Gözlüğü
cinsiyet
cam renk
fiyat
çerçeve formu
cam materyali
renk
çerçeve materyali
cam tipi
çerçeve tipi
özellik
desen
çerçeve renk
ekartman

Erkek - Saat & Aksesuar - Cüzdan
cinsiyet
fiyat
materyal
boyut
renk
tip
deri kalitesi
yaş
desen
sürdürülebilirlik detayı

Erkek - Saat & Aksesuar - Kemer
cinsiyet
beden
renk
materyal
fiyat

Erkek - Saat & Aksesuar - Çanta
cinsiyet
beden
renk
materyal
fiyat
boyut
kapasite
kumaş tipi
yaş
desen
sürdürülebilirlik detayı

Erkek - Saat & Aksesuar - Şapka
cinsiyet
beden
renk
fiyat
materyal

Erkek - Saat & Aksesuar - Kartlık
cinsiyet
materyal
fiyat
boyut
renk
deri kalitesi
tip
yaş
desen
sürdürülebilirlik detayı

Erkek - Saat & Aksesuar - Valiz
cinsiyet
materyal
kapasite
renk
fiyat
boyut
sürdürülebilirlik detayı

Erkek - Saat & Aksesuar - Kravat
cinsiyet
renk
desen
fiyat
materyal
kumaş tipi

Erkek - Saat & Aksesuar - Boyunluk
cinsiyet
materyal
renk
fiyat
desen
kumaş tipi

Erkek - Saat & Aksesuar - Atkı
cinsiyet
beden
renk
materyal
fiyat
desen
kumaş tipi

Erkek - Saat & Aksesuar - Bere
cinsiyet
beden
fiyat
renk
materyal
desen
kumaş tipi
kutu durumu

Erkek - Saat & Aksesuar - Eldiven
cinsiyet
beden
materyal
renk
fiyat
desen
kumaş tipi

Erkek - İç Giyim
cinsiyet
beden
materyal
renk
paket i̇çeriği
kalıp
fiyat
yaka tipi
siluet
kumaş tipi
desen
bel
kol boyu
boy
kol tipi
sürdürülebilirlik detayı
ek özellik

Erkek - İç Giyim - Boxer
cinsiyet
beden
materyal
paket i̇çeriği
renk
kalıp
fiyat
desen
kumaş tipi
ek özellik
bel
dokuma tipi

Erkek - İç Giyim - Çorap
cinsiyet
beden
materyal
renk
tip
paket i̇çeriği
sezon
siluet
boy
fiyat
desen
kumaş tipi
ek özellik

Erkek - İç Giyim - Pijama
cinsiyet
beden
materyal
kol boyu
paça tipi
renk
fiyat
yaka tipi
boy
sezon
kol tipi
kumaş tipi
paça boyu
sürdürülebilirlik detayı
paket i̇çeriği
desen
bel
siluet
kapama şekli

Erkek - İç Giyim - Atlet
cinsiyet
beden
renk
materyal
paket i̇çeriği
yaka tipi
kol tipi
kalıp
fiyat
kol boyu
kumaş tipi
desen
boy
sürdürülebilirlik detayı
siluet

Erkek - İç Giyim - İçlik
cinsiyet
beden
materyal
renk
fiyat
bel
boy
kumaş tipi
tip

Erkek - Spor & Outdoor
cinsiyet
beden
kol tipi
sezon
materyal
yaka tipi
paça boyu
fiyat
renk
desen
boy
sürdürülebilirlik detayı
kalıp
cep
bel
kumaş tipi
ek özellik
kol boyu
paça tipi
siluet
paket i̇çeriği
kumaş teknolojisi

Erkek - Spor & Outdoor - Eşofman
cinsiyet
beden
paça tipi
kalıp
renk
materyal
fiyat
sezon
cep
kumaş tipi
desen
bel
paket i̇çeriği
paça boyu
boy
siluet
yaka tipi
ek özellik
sürdürülebilirlik detayı
kol boyu
kol tipi

Erkek - Spor & Outdoor - Spor Ayakkabı
cinsiyet
beden
renk
fiyat
materyal
bağlama şekli
taban tipi
dış materyal
ek özellik
topuk boyu
topuk tipi
alt taban materyali
i̇ç astar & i̇ç taban materyali
sürdürülebilirlik detayı
desen

Erkek - Spor & Outdoor - T-shirt
cinsiyet
beden
materyal
kalıp
yaka tipi
kol tipi
renk
fiyat
kol boyu
boy
kumaş teknolojisi
desen
sürdürülebilirlik detayı
ek özellik

Erkek - Spor & Outdoor - Sweatshirt
cinsiyet
beden
yaka tipi
kalıp
materyal
kol tipi
renk
fiyat
boy
kol boyu
desen
cep
sürdürülebilirlik detayı

Erkek - Spor & Outdoor - Forma
cinsiyet
beden
spor branşı
fiyat
renk
kumaş tipi

Erkek - Spor & Outdoor - Spor Çorap
cinsiyet
beden
renk
tip
materyal
fiyat
desen
sürdürülebilirlik detayı

Erkek - Spor & Outdoor - Spor Giyim
cinsiyet
beden
kalıp
kol boyu
fiyat
materyal
desen
renk
sezon
bel
yaka tipi
boy
sürdürülebilirlik detayı
cep
kol tipi
ek özellik
kumaş tipi
paça tipi
siluet
paket i̇çeriği
paça boyu
kumaş teknolojisi

Erkek - Spor & Outdoor - Outdoor Ayakkabı
cinsiyet
beden
fiyat
renk
kumaş teknolojisi
ek özellik
materyal
bağlama şekli
topuk boyu
dış materyal
taban teknolojisi
topuk tipi
sürdürülebilirlik detayı
i̇ç astar & i̇ç taban materyali
alt taban materyali
kalıp

Erkek - Spor & Outdoor - Outdoor Bot
cinsiyet
beden
renk
dış materyal
fiyat
bağlama şekli
materyal
kalıp
ek özellik
kullanım alanı
topuk boyu
i̇ç astar & i̇ç taban materyali
burun tipi
topuk tipi
alt taban materyali

Erkek - Spor & Outdoor - Spor Ekipmanları
cinsiyet
beden
fiyat
özellik
renk
ek hizmetler

Erkek - Spor & Outdoor - Outdoor Ekipmanları
özellik
fiyat
renk
materyal
ek hizmetler

Erkek - Spor & Outdoor - Sporcu Besinleri
gramaj
form
fiyat
aroma
servis

Erkek - Spor & Outdoor - Sporcu Aksesuarları

Erkek - Spor & Outdoor - Sneaker
cinsiyet
beden
renk
fiyat
materyal
dış materyal
taban tipi
bağlama şekli
topuk boyu
ek özellik
i̇ç astar & i̇ç taban materyali
alt taban materyali
desen
topuk tipi
sürdürülebilirlik detayı

Erkek - Spor & Outdoor - Scooter
cinsiyet
yaş
fiyat
renk
tekerlek sayısı
çocuk cinsiyeti
özellik

Erkek - Spor & Outdoor - Bisiklet
cinsiyet
jant
fiyat
renk

Erkek - Spor & Outdoor - Dalış Malzemeleri
cinsiyet
fiyat
renk
ek hizmetler

Erkek - Spor & Outdoor - Rüzgarlık
cinsiyet
beden
renk
fiyat
kalıp
materyal
sezon
kumaş tipi
desen
boy
yaka tipi
kemer/kuşak durumu
kol tipi
siluet
cep
sürdürülebilirlik detayı
kapama şekli

Erkek - Spor & Outdoor - Aksiyon Kamerası
fiyat
özellik
renk
ek hizmetler

Erkek - Spor & Outdoor - Kamp Malzemeleri
fiyat
renk
ek hizmetler

Erkek - Elektronik
cinsiyet
cep telefonu modeli
fiyat
ekran boyutu
renk
kılıf tipi
materyal
uyumlu marka
özellik
ekran kartı
ram (sistem belleği) tipi
uyumlu model
kullanım amacı
beden
garanti tipi
i̇şletim sistemi
i̇şlemci nesli
ssd kapasitesi
i̇şlemci tipi
ram (sistem belleği)
ekran kartı hafızası
ekran yenileme hızı
çözünürlük
tip
rgb aydınlatma
baskılı
bilek desteği
i̇şlemci modeli
hard disk kapasitesi
garanti süresi
bağlantı tipi
cihaz ağırlığı
dokunmatik ekran
i̇şlemci çekirdek sayısı
parmak i̇zi okuyucu
sesli görüşme
panel tipi
tamir edilebilirlik
frekans
kasa renk
voltaj
şarjlı kullanım süresi
kordon renk
ek hizmetler

Erkek - Elektronik - Tıraş Makinesi
tıraş bölgesi
fiyat
tip
kullanım
burun ve kulak temizleme başlığı
başlık sayısı
şarjlı kullanım süresi
garanti tipi
renk
garanti süresi
otomatik kapanma
voltaj
frekans
ek hizmetler

Erkek - Elektronik - Cep Telefonu
fiyat
cep telefonu modeli
ram kapasitesi
mobil bağlantı hızı
pil gücü (mah)
ekran boyutu
nfc
kamera çözünürlüğü
garanti tipi
renk
özellik
kozmetik durum
çift hat
yapay zeka
ön kamera sayısı
ek hizmetler
dahili hafıza

Erkek - Elektronik - Akıllı Saat
fiyat
özellik
sesli görüşme
renk
kordon materyali
kordon renk
kasa renk
garanti tipi
ek hizmetler
kasa çapı
kordon boyutu

Erkek - Elektronik - Akıllı Bileklik
fiyat
özellik
renk
ek hizmetler

Erkek - Elektronik - Laptop
ekran kartı
i̇şlemci tipi
fiyat
ekran boyutu
ekran kartı hafızası
ram (sistem belleği) tipi
i̇şletim sistemi
i̇şlemci nesli
ekran yenileme hızı
hard disk kapasitesi
ekran kartı gücü
kullanım amacı
i̇şlemci modeli
çözünürlük
dokunmatik ekran
panel tipi
i̇şlemci çekirdek sayısı
şarjlı kullanım süresi
cihaz ağırlığı
parmak i̇zi okuyucu
ram (sistem belleği)
ek hizmetler
ssd kapasitesi

Erkek - Elektronik - Oyun & Konsollar
fiyat
uyumlu cihaz
ürün türü
bağlantı
özellik
renk
garanti tipi
ek hizmetler

Erkek - Elektronik - Elektrikli Bisiklet
fiyat
max. hız (km/h)
menzil
jant
taşıma kapasitesi
katlanabilme
renk
ek hizmetler

Erkek - Elektronik - E-pin ve Cüzdan Kodu
fiyat

Erkek - Elektronik - Playstation 5
fiyat
model
kol sayısı
sabit disk
garanti tipi
ek hizmetler

Erkek - Elektronik - Hediye Kartları
fiyat
kart değeri

Erkek - Elektronik - Bluetooth Kulaklık
fiyat
renk
özellik
garanti tipi
ek hizmetler

Erkek - Elektronik - Gaming PC
ekran kartı
fiyat
i̇şlemci tipi
i̇şlemci modeli
ekran kartı hafızası
ram (sistem belleği) tipi
kapasite
i̇şletim sistemi
ekran kartı bellek tipi
ekran boyutu
ekran yenileme hızı
temel i̇şlemci hızı (ghz)
i̇şlemci çekirdek sayısı
optik sürücü tipi
ram (sistem belleği)
ssd kapasitesi
özellik
ek hizmetler

Erkek - Elektronik - Oyuncu Koltuğu
fiyat
renk
taşıma kapasitesi
ayak malzemesi
sırt mekanizması
kol desteği
oturak derinliği

Erkek - Elektronik - Drone
fiyat
uçuş mesafesi
uçuş süresi
kamera özelliği
gps
yedek batarya
beni takip et modu
sivil havacılık i̇zni
renk
garanti süresi
ek hizmetler

Anne & Çocuk - Bebek
cinsiyet
beden
çocuk cinsiyeti
materyal
fiyat
renk
kol boyu
boy
kol tipi
paça tipi
desen
sürdürülebilirlik detayı
kalıp
yaka tipi
paket i̇çeriği
kumaş tipi

Anne & Çocuk - Bebek - Bebek Takımları
cinsiyet
beden
çocuk cinsiyeti
materyal
renk
fiyat
kol boyu
kol tipi
desen
kumaş tipi
boy
kalıp
yaka tipi
paça tipi
sürdürülebilirlik detayı
paket i̇çeriği

Anne & Çocuk - Bebek - Ayakkabı
cinsiyet
beden
renk
çocuk cinsiyeti
fiyat
topuk boyu
topuk tipi
desen
bağlama şekli
alt taban materyali
materyal
dış materyal
ek özellik
sürdürülebilirlik detayı
i̇ç astar & i̇ç taban materyali
taban tipi

Anne & Çocuk - Bebek - Hastane Çıkışı
cinsiyet
beden
çocuk cinsiyeti
renk
materyal
paket i̇çeriği
fiyat
desen
sürdürülebilirlik detayı

Anne & Çocuk - Bebek - Yenidoğan Kıyafetleri
cinsiyet
beden
çocuk cinsiyeti
materyal
renk
fiyat
kol boyu
kumaş tipi
paket i̇çeriği
paça tipi
desen
sürdürülebilirlik detayı
yaka tipi
kol tipi
boy
kalıp
kemer/kuşak durumu
siluet

Anne & Çocuk - Bebek - Tulum
cinsiyet
beden
çocuk cinsiyeti
materyal
renk
kol boyu
fiyat
sezon
paça tipi
yaka tipi
kol tipi
kapama şekli
kumaş tipi
sürdürülebilirlik detayı
desen
boy
kalıp
kemer/kuşak durumu
cep
siluet
kutu durumu
ek özellik

Anne & Çocuk - Bebek - Body & Zıbın
cinsiyet
beden
çocuk cinsiyeti
kol tipi
materyal
fiyat
renk
kol boyu
paket i̇çeriği
boy
kalıp
yaka tipi
desen
sürdürülebilirlik detayı
dokuma tipi

Anne & Çocuk - Bebek - Tişört & Atlet
cinsiyet
beden
çocuk cinsiyeti
renk
kol boyu
fiyat
kol tipi
yaka tipi
desen
materyal
sezon
paket i̇çeriği
boy
kalıp
kumaş tipi
cep
siluet
sürdürülebilirlik detayı
ek özellik

Anne & Çocuk - Bebek - Elbise
cinsiyet
beden
renk
fiyat
çocuk cinsiyeti
kol boyu
kumaş tipi
kemer/kuşak durumu
materyal
boy
kol tipi
kalıp
desen
yaka tipi
astar durumu
siluet
sürdürülebilirlik detayı
dokuma tipi
cep
sezon
ek özellik
paket i̇çeriği
kapama şekli
kap
kutu durumu

Anne & Çocuk - Bebek - Şort
cinsiyet
beden
renk
çocuk cinsiyeti
boy
kalıp
kumaş tipi
fiyat
bel
desen
siluet
kemer/kuşak durumu
materyal
cep
sürdürülebilirlik detayı
paça tipi
kapama şekli
sezon

Anne & Çocuk - Bebek - Bebek Patiği
cinsiyet
beden
çocuk cinsiyeti
renk
materyal
fiyat
topuk tipi
topuk boyu
desen
bağlama şekli
sürdürülebilirlik detayı
ek özellik
dış materyal

Anne & Çocuk - Bebek - Hırka
cinsiyet
beden
çocuk cinsiyeti
renk
fiyat
kumaş tipi
yaka tipi
kol boyu
boy
kalıp
kol tipi
desen
materyal
siluet
sürdürülebilirlik detayı
kutu durumu
kapama şekli
parça sayısı
sezon

Anne & Çocuk - Bebek - Battaniye
materyal
renk
boyut/ebat
fiyat
özellik
desen

Anne & Çocuk - Bebek - Alt Üst Takım
cinsiyet
beden
çocuk cinsiyeti
materyal
renk
fiyat
kol boyu
kol tipi
desen
kumaş tipi
boy
kalıp
yaka tipi
paça tipi
sürdürülebilirlik detayı
paket i̇çeriği

Anne & Çocuk - Bebek - Tişört
cinsiyet
beden
renk
çocuk cinsiyeti
fiyat
boy
kalıp
kol boyu
kumaş tipi
yaka tipi
kol tipi
desen
cep
siluet
materyal
sürdürülebilirlik detayı
sezon
paket i̇çeriği
ek özellik

Anne & Çocuk - Bebek - Etek
cinsiyet
beden
renk
çocuk cinsiyeti
desen
kumaş tipi
sürdürülebilirlik detayı
fiyat
boy
kalıp
materyal
kol boyu
kol tipi
yaka tipi
paça tipi
paket i̇çeriği
siluet
bel
kemer/kuşak durumu
astar durumu

Anne & Çocuk - Bebek - Çorap
cinsiyet
beden
çocuk cinsiyeti
materyal
renk
fiyat
kumaş tipi
desen
tip
siluet
paket i̇çeriği
boy
ek özellik
sezon

Anne & Çocuk - Bebek - Şapka
cinsiyet
beden
çocuk cinsiyeti
fiyat
materyal
kumaş tipi
renk
desen
kutu durumu

Anne & Çocuk - Bebek - Eldiven
cinsiyet
beden
renk
çocuk cinsiyeti
fiyat
desen
kumaş tipi
materyal

Anne & Çocuk - Bebek - Eşofman
cinsiyet
beden
renk
çocuk cinsiyeti
fiyat
boy
kalıp
kol boyu
kol tipi
yaka tipi
desen
materyal
sürdürülebilirlik detayı
kumaş tipi
paça tipi
bel
cep
siluet
ek özellik
paket i̇çeriği
sezon

Anne & Çocuk - Bebek - Bere
cinsiyet
beden
çocuk cinsiyeti
renk
fiyat
desen
materyal
kumaş tipi
kutu durumu

Anne & Çocuk - Kız Çocuk
cinsiyet
beden
çocuk cinsiyeti
fiyat
materyal
sezon
boy
renk
kol boyu
parça sayısı
paket i̇çeriği
kumaş tipi
kol tipi
yaka tipi
dokuma tipi
kalıp
sürdürülebilirlik detayı
desen
siluet
cep
kemer/kuşak durumu
paça tipi
ek özellik
bel
astar durumu
kapama şekli
kutu durumu
tip

Anne & Çocuk - Kız Çocuk - Elbise
cinsiyet
beden
renk
çocuk cinsiyeti
fiyat
kol boyu
materyal
boy
kol tipi
sezon
kumaş tipi
desen
kalıp
yaka tipi
ek özellik
kemer/kuşak durumu
astar durumu
siluet
sürdürülebilirlik detayı
dokuma tipi
cep
paket i̇çeriği
kapama şekli
kap
kutu durumu

Anne & Çocuk - Kız Çocuk - Sweatshirt
cinsiyet
beden
çocuk cinsiyeti
renk
fiyat
yaka tipi
sezon
kol tipi
boy
kalıp
kol boyu
kumaş tipi
desen
materyal
sürdürülebilirlik detayı
dokuma tipi

Anne & Çocuk - Kız Çocuk - Spor Ayakkabı
cinsiyet
beden
çocuk cinsiyeti
renk
fiyat
bağlama şekli
ek özellik
topuk tipi
materyal
desen
dış materyal
i̇ç astar & i̇ç taban materyali
topuk boyu
taban tipi
alt taban materyali
sürdürülebilirlik detayı

Anne & Çocuk - Kız Çocuk - Eşofman
cinsiyet
beden
renk
fiyat
çocuk cinsiyeti
paça tipi
materyal
sezon
siluet
paça boyu
boy
desen
kalıp
kumaş tipi
bel
sürdürülebilirlik detayı
cep
kol boyu
kol tipi
yaka tipi
ek özellik
paket i̇çeriği

Anne & Çocuk - Kız Çocuk - İç Giyim & Pijama
cinsiyet
beden
çocuk cinsiyeti
materyal
kalıp
renk
fiyat
kumaş tipi
desen
paket i̇çeriği
siluet
boy
bel
kol boyu
kol tipi
yaka tipi
sürdürülebilirlik detayı
parça sayısı
alt siluet

Anne & Çocuk - Kız Çocuk - Tişört & Atlet
cinsiyet
beden
çocuk cinsiyeti
renk
kol boyu
fiyat
kol tipi
yaka tipi
desen
materyal
sezon
paket i̇çeriği
boy
kalıp
kumaş tipi
siluet
cep
sürdürülebilirlik detayı
ek özellik

Anne & Çocuk - Kız Çocuk - Tayt
cinsiyet
beden
renk
çocuk cinsiyeti
boy
bel
kumaş tipi
fiyat
desen
kalıp
paça tipi
siluet
materyal
sürdürülebilirlik detayı
paket i̇çeriği
sezon
ek özellik

Anne & Çocuk - Kız Çocuk - Günlük Ayakkabı
cinsiyet
beden
renk
çocuk cinsiyeti
fiyat
materyal
ek özellik
topuk boyu
topuk tipi
bağlama şekli
dış materyal
sürdürülebilirlik detayı
desen
kalıp
burun tipi
i̇ç astar & i̇ç taban materyali
alt taban materyali

Anne & Çocuk - Kız Çocuk - Şort
cinsiyet
beden
çocuk cinsiyeti
renk
boy
kumaş tipi
fiyat
materyal
cep
bel
desen
siluet
kemer/kuşak durumu
kalıp
sürdürülebilirlik detayı
paça tipi
kapama şekli
sezon

Anne & Çocuk - Kız Çocuk - Mont
cinsiyet
beden
çocuk cinsiyeti
renk
sezon
boy
fiyat
kol tipi
yaka tipi
kalıp
kumaş tipi
desen
kemer/kuşak durumu
materyal
astar durumu
siluet
sürdürülebilirlik detayı
kutu durumu
dolgu materyali

Anne & Çocuk - Kız Çocuk - Çocuk Oyun Evi
cinsiyet
çocuk cinsiyeti
fiyat
yaş
dil
parça sayısı
özellik
ek hizmetler

Anne & Çocuk - Kız Çocuk - Oyuncak Bebek
cinsiyet
fiyat
yaş
renk
çocuk cinsiyeti
özellik
dil
ek hizmetler

Anne & Çocuk - Kız Çocuk - Kaban
cinsiyet
beden
çocuk cinsiyeti
renk
fiyat
boy
kalıp
kumaş tipi
yaka tipi
kol boyu
desen
materyal
kemer/kuşak durumu
astar durumu
kol tipi
siluet
kutu durumu
dolgu materyali
kapama şekli
ek özellik
sezon
sürdürülebilirlik detayı

Anne & Çocuk - Kız Çocuk - Abiye & Elbise
cinsiyet
beden
renk
fiyat
boy
kol tipi
çocuk cinsiyeti
kumaş tipi
kol boyu
desen
astar durumu
yaka tipi
kalıp
ürün detayı
ek özellik
kemer/kuşak durumu
siluet
materyal
sürdürülebilirlik detayı
kutu durumu
sezon

Anne & Çocuk - Kız Çocuk - Ceket
cinsiyet
beden
çocuk cinsiyeti
renk
fiyat
kumaş tipi
boy
kalıp
kol boyu
yaka tipi
kol tipi
desen
kemer/kuşak durumu
siluet
materyal
sürdürülebilirlik detayı
kapama şekli
sezon
ek özellik

Anne & Çocuk - Kız Çocuk - Pantolon
cinsiyet
beden
çocuk cinsiyeti
renk
paça tipi
fiyat
kumaş tipi
materyal
sezon
boy
kemer/kuşak durumu
bel
desen
siluet
kalıp
sürdürülebilirlik detayı
dokuma tipi

Anne & Çocuk - Kız Çocuk - Kazak
cinsiyet
beden
çocuk cinsiyeti
renk
materyal
kalıp
fiyat
kumaş tipi
boy
kol boyu
kol tipi
yaka tipi
desen
siluet
kutu durumu
sürdürülebilirlik detayı
sezon

Anne & Çocuk - Kız Çocuk - Bot
cinsiyet
beden
çocuk cinsiyeti
fiyat
ek özellik
renk
materyal
bağlama şekli
topuk tipi
topuk boyu
kullanım alanı
kalıp
dış materyal
i̇ç astar & i̇ç taban materyali
alt taban materyali
burun tipi

Anne & Çocuk - Kız Çocuk - Şapka & Bere & Eldiven
cinsiyet
beden
çocuk cinsiyeti
renk
fiyat
materyal
desen
kumaş tipi
kutu durumu

Anne & Çocuk - Erkek Çocuk
cinsiyet
beden
çocuk cinsiyeti
fiyat
materyal
sezon
boy
renk
kol boyu
parça sayısı
paket i̇çeriği
kumaş tipi
kol tipi
yaka tipi
dokuma tipi
kalıp
sürdürülebilirlik detayı
desen
siluet
cep
paça tipi
kemer/kuşak durumu
bel
ek özellik
kutu durumu
kapama şekli

Anne & Çocuk - Erkek Çocuk - Sweatshirt
cinsiyet
beden
çocuk cinsiyeti
renk
fiyat
yaka tipi
sezon
kol tipi
boy
kalıp
kumaş tipi
kol boyu
desen
materyal
sürdürülebilirlik detayı
dokuma tipi

Anne & Çocuk - Erkek Çocuk - Spor Ayakkabı
cinsiyet
beden
çocuk cinsiyeti
renk
fiyat
bağlama şekli
ek özellik
topuk tipi
materyal
desen
dış materyal
i̇ç astar & i̇ç taban materyali
topuk boyu
taban tipi
alt taban materyali
sürdürülebilirlik detayı

Anne & Çocuk - Erkek Çocuk - Eşofman
cinsiyet
beden
renk
fiyat
çocuk cinsiyeti
paça tipi
materyal
sezon
siluet
paça boyu
boy
desen
kalıp
kumaş tipi
bel
sürdürülebilirlik detayı
cep
kol boyu
kol tipi
ek özellik
yaka tipi
paket i̇çeriği

Anne & Çocuk - Erkek Çocuk - İç Giyim & Pijama
cinsiyet
beden
çocuk cinsiyeti
materyal
kalıp
renk
fiyat
kumaş tipi
desen
paket i̇çeriği
boy
bel
siluet
kol boyu
kol tipi
yaka tipi
sürdürülebilirlik detayı

Anne & Çocuk - Erkek Çocuk - Tişört & Atlet
cinsiyet
beden
çocuk cinsiyeti
renk
kol boyu
fiyat
kol tipi
yaka tipi
desen
materyal
sezon
paket i̇çeriği
boy
kalıp
kumaş tipi
siluet
cep
sürdürülebilirlik detayı
ek özellik

Anne & Çocuk - Erkek Çocuk - Günlük Ayakkabı
cinsiyet
beden
renk
çocuk cinsiyeti
fiyat
materyal
ek özellik
topuk boyu
topuk tipi
bağlama şekli
dış materyal
sürdürülebilirlik detayı
alt taban materyali

Anne & Çocuk - Erkek Çocuk - Okul Çantası
cinsiyet
çocuk cinsiyeti
fiyat
renk
tip
kapasite
desen
materyal
sürdürülebilirlik detayı
deri kalitesi

Anne & Çocuk - Erkek Çocuk - Şort
cinsiyet
beden
çocuk cinsiyeti
renk
boy
kumaş tipi
fiyat
materyal
cep
bel
desen
kemer/kuşak durumu
siluet
kalıp
sürdürülebilirlik detayı
paça tipi
kapama şekli
sezon

Anne & Çocuk - Erkek Çocuk - Gömlek
cinsiyet
beden
çocuk cinsiyeti
renk
kol boyu
fiyat
sezon
kumaş tipi
materyal
boy
kalıp
yaka tipi
kol tipi
desen
cep
siluet
sürdürülebilirlik detayı
kutu durumu
ek özellik

Anne & Çocuk - Erkek Çocuk - Mont
cinsiyet
beden
çocuk cinsiyeti
renk
sezon
boy
fiyat
kol tipi
yaka tipi
kalıp
kumaş tipi
desen
kemer/kuşak durumu
materyal
astar durumu
siluet
sürdürülebilirlik detayı
kutu durumu
dolgu materyali

Anne & Çocuk - Erkek Çocuk - Oyuncak Traktör
cinsiyet
fiyat
çocuk cinsiyeti
yaş
paket i̇çeriği
özellik
ek hizmetler

Anne & Çocuk - Erkek Çocuk - Akülü Araba
cinsiyet
fiyat
yaş
güç
renk
model
özellik
tekerlek sayısı
ek hizmetler

Anne & Çocuk - Erkek Çocuk - Kumandalı Araba
cinsiyet
fiyat
özellik
yaş
renk
ek hizmetler

Anne & Çocuk - Erkek Çocuk - Bisiklet
yaş
fiyat
renk
tekerlek sayısı
özellik
model

Anne & Çocuk - Erkek Çocuk - Boxer
cinsiyet
beden
çocuk cinsiyeti
materyal
renk
paket i̇çeriği
fiyat
desen
kumaş tipi
kalıp
bel
ek özellik
dokuma tipi

Anne & Çocuk - Erkek Çocuk - İçlik
cinsiyet
beden
materyal
renk
çocuk cinsiyeti
fiyat
kumaş tipi
tip
bel
boy

Anne & Çocuk - Erkek Çocuk - Bot
cinsiyet
beden
çocuk cinsiyeti
fiyat
ek özellik
renk
materyal
bağlama şekli
topuk tipi
topuk boyu
kullanım alanı
kalıp
dış materyal
i̇ç astar & i̇ç taban materyali
alt taban materyali
burun tipi

Anne & Çocuk - Erkek Çocuk - Krampon
cinsiyet
beden
fiyat
renk
bağlama şekli
topuk tipi
spor branşı
çocuk cinsiyeti
topuk boyu
ek özellik
desen
dış materyal
alt taban materyali
sürdürülebilirlik detayı
i̇ç astar & i̇ç taban materyali
kumaş tipi

Anne & Çocuk - Erkek Çocuk - Şapka & Bere & Eldiven
cinsiyet
beden
çocuk cinsiyeti
renk
fiyat
materyal
desen
kumaş tipi
kutu durumu

Anne & Çocuk - Erkek Çocuk - Takım Elbise
cinsiyet
beden
renk
çocuk cinsiyeti
fiyat
boy
sezon
kalıp
materyal
ek özellik
desen
kumaş tipi
kol tipi
kol boyu
paça tipi
yaka tipi
sürdürülebilirlik detayı
bel

Anne & Çocuk - Bebek Bakım
fiyat
ek hizmetler

Anne & Çocuk - Bebek Bakım - Bebek Bezi
tip
fiyat
bez bedeni
paket i̇çi bez adedi

Anne & Çocuk - Bebek Bakım - Bebek Şampuanı
boy
fiyat

Anne & Çocuk - Bebek Bakım - Krem & Yağlar
fiyat

Anne & Çocuk - Bebek Bakım - Bebek Çantası
cinsiyet
fiyat
renk
materyal
çocuk cinsiyeti

Anne & Çocuk - Bebek Bakım - Bebek Sabunları
fiyat

Anne & Çocuk - Bebek Bakım - Bebek Deterjanları
fiyat

Anne & Çocuk - Bebek Bakım - Bebek Vücut Kremi
fiyat

Anne & Çocuk - Bebek Bakım - Islak Mendil
paket i̇çeriği
fiyat
ek özellik

Anne & Çocuk - Bebek Bakım - Bebek Yağı
fiyat

Anne & Çocuk - Bebek Bakım - Bebek Buhar Makinesi
renk
fiyat
özellik
sıcak soğuk kullanımı
ek hizmetler

Anne & Çocuk - Oyuncak
cinsiyet
yaş
fiyat
çocuk cinsiyeti
özellik
renk
dil
materyal
parça sayısı
paket i̇çeriği
boyut
batarya türü
boyut/ebat
ek hizmetler

Anne & Çocuk - Oyuncak - Eğitici Oyuncaklar
cinsiyet
yaş
çocuk cinsiyeti
fiyat
dil
paket i̇çeriği
özellik
ek hizmetler

Anne & Çocuk - Oyuncak - Oyuncak Araba
cinsiyet
fiyat
yaş
özellik
çocuk cinsiyeti
paket i̇çeriği
ek hizmetler

Anne & Çocuk - Oyuncak - Oyuncak Bebek
cinsiyet
fiyat
yaş
renk
çocuk cinsiyeti
özellik
dil
ek hizmetler

Anne & Çocuk - Oyuncak - Bebek & Okul Öncesi
cinsiyet
yaş
renk
fiyat
ek hizmetler

Anne & Çocuk - Oyuncak - Kumandalı Oyuncak
cinsiyet
fiyat
yaş
renk
çocuk cinsiyeti
özellik
ek hizmetler

Anne & Çocuk - Oyuncak - Robot Oyuncak
cinsiyet
yaş
fiyat
çocuk cinsiyeti
renk
paket i̇çeriği
özellik
dil
ek hizmetler

Anne & Çocuk - Oyuncak - Çocuk Çizim Tableti
özellik
fiyat
renk
ek hizmetler

Anne & Çocuk - Beslenme Emzirme
fiyat
mama numarası

Anne & Çocuk - Beslenme Emzirme - Biberon & Emzik
materyal
fiyat
yaş
hacim
emzik uç materyali
ek hizmetler

Anne & Çocuk - Beslenme Emzirme - Göğüs Pompası
kullanım şekli
fiyat
özellik
model

Anne & Çocuk - Beslenme Emzirme - Mama Sandalyesi
cinsiyet
fiyat
özellik
taşıma kapasitesi
model
renk
yükseklik ayarı
çocuk cinsiyeti
tekerlek

Anne & Çocuk - Beslenme Emzirme - Mama Önlüğü
materyal
fiyat
çeşit
paket i̇çeriği

Anne & Çocuk - Beslenme Emzirme - Alıştırma Bardağı
hacim
fiyat
renk
materyal

Anne & Çocuk - Beslenme Emzirme - Biberon Temizleyici
fiyat

Anne & Çocuk - Beslenme Emzirme - Biberon Seti
cinsiyet
materyal
renk
fiyat
hacim
yaş
ek hizmetler

Anne & Çocuk - Beslenme Emzirme - Bebek Maması
mama numarası
fiyat

Anne & Çocuk - Beslenme Emzirme - Kavanoz Mama
fiyat

Anne & Çocuk - Beslenme Emzirme - Sterilizatör
özellik
fiyat
ek hizmetler

Anne & Çocuk - Beslenme Emzirme - Bebek Bakım Çantası
cinsiyet
fiyat
renk
materyal
çocuk cinsiyeti

Anne & Çocuk - Beslenme Emzirme - Yemek Setleri
özellik
fiyat

Anne & Çocuk - Beslenme Emzirme - Kaşık Maması
fiyat

Anne & Çocuk - Beslenme Emzirme - Buharlı Pişirici
fiyat
özellik
renk
garanti tipi
voltaj
frekans
ek hizmetler

Anne & Çocuk - Beslenme Emzirme - Termal Çanta
fiyat
renk

Anne & Çocuk - Beslenme Emzirme - Süt Pompası
kullanım şekli
fiyat
özellik
model

Anne & Çocuk - Beslenme Emzirme - Emzirme Önlüğü
fiyat
kumaş tipi
özellik
boyut/ebat

Anne & Çocuk - Beslenme Emzirme - Emzirme Minderi
materyal
fiyat

Anne & Çocuk - Beslenme Emzirme - Göğüs Pedi
fiyat

Anne & Çocuk - Beslenme Emzirme - Göğüs Kremi
fiyat

Anne & Çocuk - Taşıma & Güvenlik
cinsiyet
fiyat
renk
özellik
tip
materyal
ek hizmetler

Anne & Çocuk - Taşıma & Güvenlik - Bebek Arabası & Puset
cinsiyet
fiyat
çift yönlü kullanım
tek elle kapama
renk
taşıma kapasitesi
çocuk cinsiyeti
özellik
ayak örtüsü
yağmurluk
garanti süresi

Anne & Çocuk - Taşıma & Güvenlik - Park Yatak
fiyat
özellik
ara kat
renk
taşıma kapasitesi
alt açma ünitesi
tekerlek
sineklik
taşıma çantası
ek hizmetler

Anne & Çocuk - Taşıma & Güvenlik - Ana Kucağı
cinsiyet
taşıma kapasitesi
fiyat
renk
özellik
çocuk cinsiyeti

Anne & Çocuk - Taşıma & Güvenlik - Portbebe & Kanguru
cinsiyet
taşıma kapasitesi
renk
özellik
çocuk cinsiyeti
fiyat

Anne & Çocuk - Taşıma & Güvenlik - Yürüteç
cinsiyet
fiyat
maksimum taşıma kapasitesi
renk
özellik
çocuk cinsiyeti
model

Anne & Çocuk - Taşıma & Güvenlik - Oto Koltuğu
cinsiyet
taşıma kapasitesi
isofix özelliği
fiyat
360 derece dönebilme
özellik
5 noktalı emniyet kemeri sistemi
çocuk cinsiyeti
ayarlanabilir baş desteği
renk

Anne & Çocuk - Taşıma & Güvenlik - Baston Puset
cinsiyet
taşıma kapasitesi
fiyat
araba ağırlığı
çift yönlü kullanım
çocuk cinsiyeti
renk
garanti süresi
tek elle kapama
ayak örtüsü

Anne & Çocuk - Taşıma & Güvenlik - Kanguru
cinsiyet
taşıma kapasitesi
renk
özellik
çocuk cinsiyeti
fiyat

Anne & Çocuk - Taşıma & Güvenlik - Bebek Salıncakları
ölçü
materyal
renk
fiyat
özellik
derinlik
genişlik
yükseklik
yaş
ek hizmetler

Anne & Çocuk - Bebek Odası
renk
materyal
fiyat
yavrulu yatak
özellik

Anne & Çocuk - Bebek Odası - Bebek Beşiği
fiyat
i̇ç yatak ölçüsü
taşıma kapasitesi
materyal
renk
özellik
fonksiyon
sallanma fonksiyonu
kullanım tipi
derinlik
yükseklik
ek hizmetler
genişlik
paket derinlik
paket yükseklik
paket genişlik

Anne & Çocuk - Bebek Odası - Bebek Yatağı
ölçü
yatak cinsi
fiyat

Anne & Çocuk - Bebek Odası - Bebek Nevresimleri
boyut/ebat
çarşaf türü
materyal
fiyat
özellik
renk
desen

Anne & Çocuk - Bebek Odası - Oyuncak Sepetleri
boyut/ebat
renk
fiyat
materyal
parça sayısı
özellik
hacim

Anne & Çocuk - Bebek Odası - Bebek Cibinlik
boyut/ebat
renk
fiyat
set i̇çeriği
materyal
parça sayısı

Anne & Çocuk - Bebek Odası - Oyuncak Dolabı
genişlik
fiyat
yükseklik
materyal
renk
derinlik
çekmece sayısı
özellik
ek hizmetler

Anne & Çocuk - Bebek Odası - Bebek Odası Mobilyaları
renk
materyal
fiyat
yavrulu yatak
özellik

Anne & Çocuk - Bebek Odası - Bebek Oyun Matları
cinsiyet
boyut/ebat
materyal
özellik
hav yüksekliği
fiyat
yaş
renk
dil
şekil
saçak tipi
taban
üretim şekli
ek hizmetler

Anne & Çocuk - Bebek Odası - Bebek Oyun Parkı
fiyat
özellik
ara kat
renk
taşıma kapasitesi
alt açma ünitesi
tekerlek
sineklik
taşıma çantası
ek hizmetler

Ev & Yaşam - Sofra & Mutfak
ürün tipi
materyal
fiyat
renk
kişi sayısı
parça sayısı
kullanım alanı
hacim
şekil
özellik
i̇ç materyal
boyut/ebat
garanti süresi
dış materyal
bakım talimatları (gıda temas)
kapasite
ek hizmetler

Ev & Yaşam - Sofra & Mutfak - Tencere & Tencere Seti
materyal
boyut/ebat
parça sayısı
fiyat
özellik
hacim
i̇ç materyal
renk
dış materyal

Ev & Yaşam - Sofra & Mutfak - Tava
materyal
boyut/ebat
i̇ç materyal
parça sayısı
özellik
fiyat
ürün tipi
dış materyal

Ev & Yaşam - Sofra & Mutfak - Düdüklü Tencere
fiyat
materyal
özellik
hacim
parça sayısı
garanti süresi

Ev & Yaşam - Sofra & Mutfak - Yemek Takımı
kişi sayısı
renk
parça sayısı
materyal
fiyat
şekil
özellik

Ev & Yaşam - Sofra & Mutfak - Kahvaltı Takımı
kişi sayısı
materyal
fiyat
parça sayısı
renk
şekil
özellik

Ev & Yaşam - Sofra & Mutfak - Tabak
materyal
renk
boyut/ebat
ürün tipi
fiyat
parça sayısı
şekil

Ev & Yaşam - Sofra & Mutfak - Çatal Kaşık Bıçak Seti
kişi sayısı
parça sayısı
materyal
ürün tipi
renk
fiyat
garanti süresi

Ev & Yaşam - Sofra & Mutfak - Saklama Kabı
materyal
hacim
parça sayısı
renk
fiyat

Ev & Yaşam - Sofra & Mutfak - Bardak
ürün tipi
hacim
parça sayısı
renk
fiyat
materyal

Ev & Yaşam - Sofra & Mutfak - Kahve Fincanı
kişi sayısı
renk
fiyat
hacim
materyal
parça sayısı

Ev & Yaşam - Ev Gereçleri
fiyat
renk
materyal
boyut/ebat
parça sayısı
bölme sayısı

Ev & Yaşam - Ev Gereçleri - Hurç
boyut/ebat
renk
materyal
fiyat
parça sayısı

Ev & Yaşam - Ev Gereçleri - Düzenleyiciler
renk
fiyat
materyal
parça sayısı
boyut/ebat

Ev & Yaşam - Ev Gereçleri - Askı
materyal
parça sayısı
fiyat
kullanım türü

Ev & Yaşam - Ev Gereçleri - Çamaşır Sepeti
materyal
renk
boyut/ebat
fiyat
hacim

Ev & Yaşam - Ev Gereçleri - Banyo Düzenleyici
materyal
renk
fiyat

Ev & Yaşam - Ev Gereçleri - Banyo Setleri
materyal
renk
parça sayısı
fiyat

Ev & Yaşam - Ev Gereçleri - Ütü Masası ve Aksesuarları
fiyat
renk

Ev & Yaşam - Ev Gereçleri - Makyaj & Takı Organizeri
fiyat
renk
materyal
parça sayısı
bölme sayısı

Ev & Yaşam - Aydınlatma
kullanım alanı
renk
özellik
materyal
fiyat
model
çalışma tipi
ampül başlık sayısı
boyut/ebat
güç (watt)
yükseklik
duy tipi
renk sıcaklığı
ampul teknolojisi
ek hizmetler
dim özelliği

Ev & Yaşam - Aydınlatma - Avize
kullanım alanı
fiyat
renk
ampül başlık sayısı
boyut/ebat
model
materyal
özellik
duy tipi
yükseklik
ek hizmetler

Ev & Yaşam - Aydınlatma - Lambader
fiyat
materyal
yerden yüksekliği
model
özellik
ampül başlık sayısı
duy tipi
ek hizmetler

Ev & Yaşam - Aydınlatma - Masa ve Gece Lambası
fiyat
renk
çalışma tipi
model
materyal
boyut/ebat
duy tipi
ek hizmetler

Ev & Yaşam - Ev Tekstili
boyut/ebat
materyal
çarşaf türü
renk
fiyat
desen
özellik
dolgu materyali
şekil
kutu durumu
dış materyal
parça sayısı

Ev & Yaşam - Ev Tekstili - Nevresim & Pike Takımı
renk
fiyat
çarşaf türü
materyal
desen
boyut/ebat
kutu durumu
özellik

Ev & Yaşam - Ev Tekstili - Yastık & Yorgan
renk
fiyat
dış materyal
dolgu materyali
boyut/ebat
özellik
ağırlık

Ev & Yaşam - Ev Tekstili - Çarşaf & Alez
boyut/ebat
renk
fiyat
materyal
çarşaf türü
desen
özellik

Ev & Yaşam - Ev Tekstili - Yatak Örtüsü & Battaniye
boyut/ebat
renk
fiyat
materyal
desen
özellik
kutu durumu

Ev & Yaşam - Ev Tekstili - Uyku Seti
boyut/ebat
renk
fiyat
çarşaf türü
materyal
set i̇çeriği
desen
özellik

Ev & Yaşam - Ev Tekstili - Koltuk Örtüsü
renk
boyut/ebat
materyal
fiyat
desen

Ev & Yaşam - Ev Tekstili - Havlu & Bornoz
cinsiyet
beden
renk
fiyat
materyal
desen
parça sayısı
havlu tipi
boyut/ebat
kutu durumu
bornoz uzunluğu
kapüşon
cep

Ev & Yaşam - Ev Tekstili - Banyo Paspası
renk
boyut/ebat
parça sayısı
materyal
özellik
fiyat
hav yüksekliği
desen

Ev & Yaşam - Ev Tekstili - Halı & Kilim
boyut/ebat
renk
fiyat
üretim şekli
şekil
taban
hav yüksekliği
materyal
saçak tipi
özellik
kullanım alanı
desen
paket genişlik
paket yükseklik
paket derinlik

Ev & Yaşam - Ev Tekstili - Perde
boyut/ebat
renk
materyal
takma şekli
işık geçirgenliği
kullanım alanı
desen
fiyat
özellik
parça sayısı
kanat sayısı
pile
aksesuar tipi
paket derinlik
paket genişlik
paket adedi
paket yükseklik

Ev & Yaşam - Ev Tekstili - Seccade
boyut/ebat
materyal
renk
fiyat
taban
saçak tipi

Ev & Yaşam - Ev Dekorasyon
boyut/ebat
renk
fiyat
materyal
parça sayısı
çiçek türü
çerçeve tipi
yükseklik
özellik
şekil
çeşit
üretim şekli
koku aroması
çalışma tipi
adet

Ev & Yaşam - Ev Dekorasyon - Ayna
boyut/ebat
çeşit
şekil
renk
fiyat
materyal
parça sayısı

Ev & Yaşam - Ev Dekorasyon - Tablo
boyut/ebat
renk
çerçeve tipi
fiyat
parça sayısı
materyal

Ev & Yaşam - Ev Dekorasyon - Dekoratif Çiçek & Vazo
renk
fiyat
yükseklik
çiçek türü
materyal
parça sayısı

Ev & Yaşam - Ev Dekorasyon - Kırlent & Kırlent Kılıfı
boyut/ebat
renk
materyal
parça sayısı
fiyat
şekil
çeşit
üretim şekli

Ev & Yaşam - Ev Dekorasyon - Duvar Saati
boyut/ebat
fiyat
materyal
şekil
çalışma tipi

Ev & Yaşam - Mobilya
yükseklik
ölçü
genişlik
materyal
derinlik
fiyat
renk
boyut/ebat
özellik
fonksiyon
masa ölçüsü
model
kapak sayısı
sandalye ve bank sayısı
form
ek hizmetler
parça sayısı
gövde materyali
şekil
ayak malzemesi
masa fonksiyonu
kumaş
sandalye kumaşı
tip
paket derinlik
sandalye sayısı
raf sayısı
paket yükseklik
desen
paket genişlik

Ev & Yaşam - Mobilya - Salon & Oturma Odası
koltuk tipi
genişlik
fiyat
fonksiyon
renk
materyal
parça sayısı
kumaş
boyut/ebat
yükseklik
şekil
derinlik
gövde materyali
özellik
ayak malzemesi
ek hizmetler

Ev & Yaşam - Mobilya - Yatak Odası
yükseklik
ölçü
materyal
genişlik
fiyat
renk
yatak cinsi
özellik
gövde materyali
çekmece sayısı
kapak sayısı
ayna fonksiyonu
derinlik
boyut
fonksiyon
ek hizmetler

Ev & Yaşam - Mobilya - Bahçe Mobilyası
materyal
fiyat
masa ölçüsü
takım tipi
renk
sandalye ve bank sayısı
ek hizmetler

Ev & Yaşam - Mobilya - Çalışma Odası
genişlik
yükseklik
derinlik
renk
materyal
fiyat
özellik
gövde materyali
raf sayısı
tip
ek hizmetler

Ev & Yaşam - Mobilya - Yemek Odası
sandalye ve bank sayısı
masa fonksiyonu
renk
masa ölçüsü
materyal
boyut/ebat
özellik
fiyat
sandalye kumaşı
ek hizmetler

Ev & Yaşam - Mobilya - Oturma Grupları
koltuk tipi
genişlik
fiyat
fonksiyon
renk
materyal
parça sayısı
kumaş
boyut/ebat
yükseklik
şekil
derinlik
gövde materyali
özellik
ayak malzemesi
ek hizmetler

Ev & Yaşam - Mobilya - Genç Odası
fiyat
renk
materyal
yavrulu yatak
özellik

Ev & Yaşam - Mobilya - Koltuk Takımı
takım i̇çeriği
fiyat
renk
fonksiyon
koltuk tipi
kumaş
boyut/ebat
gövde materyali
ayak malzemesi
tasarım
materyal
ek hizmetler

Ev & Yaşam - Mobilya - Mutfak Dolabı
genişlik
yükseklik
derinlik
materyal
fiyat
renk
model
özellik
ek hizmetler

Ev & Yaşam - Mobilya - Şifonyer
genişlik
renk
yükseklik
derinlik
çekmece sayısı
fiyat
materyal
ürün özelliği
ek hizmetler

Ev & Yaşam - Mobilya - Mutfak Tezgahı
alt modül genişlik
materyal
fiyat
alt modül yükseklik
üst modül genişlik
renk
üst modül yükseklik
ek hizmetler

Ev & Yaşam - Mobilya - Dolap
genişlik
derinlik
fiyat
renk
kapak sayısı
gövde materyali
özellik
fonksiyon
ayna fonksiyonu
ek hizmetler
yükseklik

Ev & Yaşam - Mobilya - Gardırop
genişlik
kapak sayısı
derinlik
fiyat
renk
gövde materyali
özellik
fonksiyon
ayna fonksiyonu
ek hizmetler
yükseklik

Ev & Yaşam - Mobilya - Sandalye
renk
materyal
fiyat
sandalye sayısı
model
sandalye kumaşı
ek hizmetler

Ev & Yaşam - Mobilya - Zigon
renk
materyal
parça sayısı
fiyat
şekil
boyut/ebat
ek hizmetler

Ev & Yaşam - Hobi
cinsiyet
beden
fiyat
yaş
renk
i̇çerik
metraj
özellik
balon çeşidi
gramaj
adet
ebatlar
boyut/ebat
materyal
parti konsepti
müzik türleri
format
boyut
enerji tasarrufu
ek hizmetler

Ev & Yaşam - Hobi - Parti Malzemeleri
beden
parti konsepti
renk
yaş
materyal
fiyat
balon çeşidi
özellik
ebatlar
enerji tasarrufu
ek hizmetler

Ev & Yaşam - Hobi - Müzik Alet ve Ekipmanları
fiyat
müzik türleri
format
ek hizmetler

Ev & Yaşam - Hobi - Hediyelik Ürünler
fiyat
boyut
ek hizmetler

Ev & Yaşam - Hobi - Hobi Malzemeleri
renk
i̇çerik
metraj
fiyat
gramaj
adet
boyut/ebat

Ev & Yaşam - Hobi - Uzaktan Kumandalı Araçlar
fiyat
ek hizmetler

Ev & Yaşam - Hobi - Drone
uçuş süresi
fiyat
sivil havacılık i̇zni
uçuş mesafesi
gps
yedek batarya
kamera özelliği
beni takip et modu
renk
garanti süresi
ek hizmetler

Ev & Yaşam - Hobi - Oyun Grupları
cinsiyet
yaş
fiyat
özellik
ek hizmetler

Ev & Yaşam - Hobi - Hediye Sepeti
fiyat

Ev & Yaşam - Hobi - Led Işık
özellik
renk
fiyat
enerji tasarrufu
ebatlar

Ev & Yaşam - Kitap
roman türü
yaş
yazar
fiyat
basım dili
sınıf
basım yılı
kitap i̇çeriği
sayfa sayısı
setli/tekil
sınav tipi
cilt bilgisi
ders
boyut
ek hizmetler

Ev & Yaşam - Kitap - Sınav Hazırlık Kitapları
sınav tipi
ders
kitap i̇çeriği
basım yılı
setli/tekil
fiyat
yazar
basım dili
sayfa sayısı
ek hizmetler

Ev & Yaşam - Kitap - Ders ve Yardımcı Kitaplar
sınıf
ders
basım yılı
kitap i̇çeriği
setli/tekil
fiyat
basım dili
yazar
ek hizmetler

Ev & Yaşam - Kitap - Roman & Edebiyat Kitapları
roman türü
fiyat
setli/tekil
sayfa sayısı
basım dili
yazar
cilt bilgisi
basım yılı
boyut

Ev & Yaşam - Kitap - Kişisel Gelişim & Psikoloji Kitapları
basım dili
setli/tekil
fiyat
yazar

Ev & Yaşam - Kitap - Çocuk Bakım Kitapları
yaş
fiyat
setli/tekil
basım dili
sayfa sayısı
yazar

Ev & Yaşam - Kitap - Yabancı Dil Eğitim Kitapları
basım dili
dil seviyesi
setli/tekil
fiyat

Ev & Yaşam - Kitap - E-Kitaplar
fiyat
ekran boyutu
kapasite
kalemle not alma
su geçirmezlik
bağlantılar
ek hizmetler

Ev & Yaşam - Kitap - Din Kitapları
fiyat
basım dili
boyut
setli/tekil
yazar

Ev & Yaşam - Kitap - Çizgi Roman ve Manga
fiyat
basım dili
setli/tekil
sayfa sayısı

Ev & Yaşam - Kitap - Yabancı Dil Çocuk Kitapları
basım dili
sayfa sayısı
fiyat
setli/tekil
basım yılı
yazar

Ev & Yaşam - Spor & Outdoor
cinsiyet
beden
fiyat
özellik
renk
ek hizmetler

Ev & Yaşam - Spor & Outdoor - Koşu Bandı
taşıma kapasitesi
fiyat
hız aralığı
katlanabilme
özellik
renk
ek hizmetler

Ev & Yaşam - Spor & Outdoor - Dumbell & Ağırlık
fiyat
renk

Ev & Yaşam - Spor & Outdoor - Pilates & Yoga
fiyat
renk
pompa durumu

Ev & Yaşam - Spor & Outdoor - Eliptik Bisiklet
özellik
fiyat
renk

Ev & Yaşam - Spor & Outdoor - Yoga Matı
fiyat
renk
açma / kapama

Ev & Yaşam - Spor & Outdoor - Sporcu Eldiveni
fiyat
renk
özellik

Ev & Yaşam - Spor & Outdoor - Pilates Topu
renk
pompa durumu
fiyat

Ev & Yaşam - Spor & Outdoor - Sporcu Sulukları
kapasite
materyal
fiyat
renk

Ev & Yaşam - Spor & Outdoor - Termoslar
fiyat
materyal
renk

Ev & Yaşam - Kırtasiye
fiyat
kağıt boyutu
renk
sayfa tipi
defter tipi
materyal
paket i̇çeriği
kapak türü
sayfa sayısı
tel tipi
kağıt tipi
kalem ucu boyutu
boyut
tip
gramaj
boyut/ebat
türü
ek hizmetler

Ev & Yaşam - Kırtasiye - Defter
sayfa tipi
kağıt boyutu
sayfa sayısı
fiyat
kapak türü
renk
tel tipi
defter tipi
boyut

Ev & Yaşam - Kırtasiye - Ajanda
fiyat
renk
tel tipi
boyut
kapak türü

Ev & Yaşam - Kırtasiye - Fotokopi Kağıdı
kağıt boyutu
gramaj
kağıt tipi
fiyat

Ev & Yaşam - Kırtasiye - Kalem
fiyat
renk

Ev & Yaşam - Kırtasiye - Boya Seti
fiyat
renk

Ev & Yaşam - Kırtasiye - Dosyalama Arşivleme
renk
fiyat
klasör formu
dosya tipi

Ev & Yaşam - Kırtasiye - Masaüstü Gereçleri
renk
fiyat
materyal
boyut
boyut/ebat
ek hizmetler

Ev & Yaşam - Kırtasiye - Ofis Teknolojisi
fiyat

Ev & Yaşam - Otomobil & Motosiklet
beden
araç marka ve model
jant çapı
fiyat
araç tipi
kesit oranı
paspas türleri
yakıt tipi
mevsim
taban genişliği
islak zeminde frenleme
yakıt verimliliği
hız endeksi
yük endeksi
gürültü seviyesi
renk
özellik
ürün özelliği
materyal
yedek parça tipi
ekran boyut (i̇nç)
teyp özellikleri
motor teknolojisi
tamir edilebilirlik
yıl
araç motor hacmi
far (ampul) tipleri
paket i̇çeriği
telefon tutucu özellikleri
türü
hacim
güç (watt)
ek hizmetler

Ev & Yaşam - Otomobil & Motosiklet - Oto Aksesuar
araç marka ve model
fiyat
renk
türü
özellik
paspas türleri
ürün özelliği
materyal
tamir edilebilirlik
telefon tutucu özellikleri
paket i̇çeriği
ek hizmetler

Ev & Yaşam - Otomobil & Motosiklet - Oto Paspası
araç marka ve model
paspas türleri
renk
ürün özelliği
fiyat

Ev & Yaşam - Otomobil & Motosiklet - Oto Lastik
jant çapı
kesit oranı
taban genişliği
mevsim
araç tipi
yük endeksi
fiyat
gürültü seviyesi
yakıt verimliliği
islak zeminde frenleme
hız endeksi
ek hizmetler
yıl

Ev & Yaşam - Otomobil & Motosiklet - Kask
beden
kask tipi
fiyat
renk

Ev & Yaşam - Otomobil & Motosiklet - Kol Dayama & Kolçak
fiyat
özellik

Ev & Yaşam - Otomobil & Motosiklet - Güneşlik & Perde
fiyat

Ev & Yaşam - Otomobil & Motosiklet - Araç Kokusu
fiyat
renk
paket i̇çeriği

Ev & Yaşam - Otomobil & Motosiklet - Motosiklet Eldiveni
beden
eldiven tipi
fiyat
özellik

Ev & Yaşam - Otomobil & Motosiklet - Motosiklet Botu
beden
renk
fiyat
dış materyal
alt taban materyali
i̇ç astar & i̇ç taban materyali

Ev & Yaşam - Otomobil & Motosiklet - Motosiklet Sepeti
çanta tipi
fiyat

Ev & Yaşam - Yapı Market
beden
boya ağırlığı
boyut/ebat
eldiven boyutu
tip
fiyat
renk
özellik
materyal
desen
kullanım alanı
parça sayısı
paket i̇çeriği
parlaklık
silinebilirlik
ürün tipi
yapıştırıcı tipi
ölçü
delikler arası mesafe
priz sayısı
fonksiyon
yükseklik
usb
garanti süresi
ek hizmetler

Ev & Yaşam - Yapı Market - Banyo Yapı Malzemeleri
boyut/ebat
materyal
renk
ek hizmetler
tip
fonksiyon
fiyat
özellik

Ev & Yaşam - Yapı Market - Elektrikli El Aleti
fiyat
tip
güç (watt)
matkap türü
özellik
garanti süresi
ek hizmetler

Ev & Yaşam - Yapı Market - Hırdavat Ürünleri
beden
boyut/ebat
eldiven boyutu
materyal
fiyat
ürün tipi
özellik
renk
tip
desen
kullanım alanı
parça sayısı
paket i̇çeriği
yapıştırıcı tipi
ölçü
delikler arası mesafe
ek hizmetler

Ev & Yaşam - Yapı Market - Boya
renk
silinebilirlik
özellik
tip
parlaklık
fiyat
boya ağırlığı
ek hizmetler

Ev & Yaşam - Yapı Market - Matkap
matkap türü
fiyat
akü volt
tip
güç (watt)
akü sayısı
özellik
taşıma çantası
mandren tipi
ek hizmetler

Ev & Yaşam - Yapı Market - Ampul
güç (watt)
renk sıcaklığı
duy tipi
ampul teknolojisi
dim özelliği
özellik
enerji sınıfı
fiyat
paket i̇çeriği

Ev & Yaşam - Yapı Market - Vidalama
akü volt
matkap türü
fiyat
akü kapasitesi
akü sayısı
ürün i̇çeriği
özellik
ek hizmetler

Süpermarket - Ev & Temizlik
çeşit
fiyat
ek özellik
hacim
türü
koku aroması
materyal
paket i̇çeriği

Süpermarket - Ev & Temizlik - Çamaşır Yıkama
form
ek özellik
hacim
fiyat
yıkama sayısı
kumaş cinsi/rengi

Süpermarket - Ev & Temizlik - Bulaşık Yıkama
fiyat
ek özellik
hacim
yıkama sayısı
form

Süpermarket - Ev & Temizlik - Paspas & Mop
fiyat
çeşit

Süpermarket - Ev & Temizlik - Çamaşır Deterjanı
ağırlık
form
kumaş cinsi/rengi
hacim
ek özellik
fiyat
yıkama sayısı

Süpermarket - Ev & Temizlik - Bulaşık Deterjanı
fiyat
form
hacim

Süpermarket - Ev & Temizlik - Oda Kokusu
koku aroması
türü
çeşit
fiyat

Süpermarket - Ev & Temizlik - Banyo Temizleyiciler
fiyat
form

Süpermarket - Ev & Temizlik - Yumuşatıcı
hacim
fiyat
çeşit
ek özellik

Süpermarket - Ev & Temizlik - Islak Mendil
paket i̇çeriği
fiyat
ek özellik

Süpermarket - Ev & Temizlik - Tuvalet Kağıdı
rulo sayısı
kat sayısı
fiyat
ek özellik

Süpermarket - Ev & Temizlik - Kağıt Havlu
rulo sayısı
kat sayısı
fiyat
ek özellik

Süpermarket - Ev & Temizlik - Temizlik Bezi
çeşit
paket i̇çeriği
fiyat

Süpermarket - Kişisel Bakım
cinsiyet
fiyat
kullanma amacı
cilt tipi
renk
tip
yaşlanma karşıtı
hacim
refill
form
koku türü
etki
ek özellik
saç tipi
i̇çerik
kalıcılık
spf
özellik
boy
suya/tere dayanıklılık
set i̇çerik adeti
görünüm
ek hizmetler

Süpermarket - Kişisel Bakım - Saç Bakım
cinsiyet
saç tipi
etki
fiyat
özellik
renk
tip
kalıcılık
refill

Süpermarket - Kişisel Bakım - Ağda & Epilasyon
cinsiyet
fiyat
form
cilt tipi
ürün tipi

Süpermarket - Kişisel Bakım - Banyo & Duş
cinsiyet
fiyat
refill

Süpermarket - Kişisel Bakım - Ağız Bakım
kullanım amacı
fiyat
i̇çerik
fırça kılı sertliği
ek hizmetler

Süpermarket - Kişisel Bakım - Cilt Bakım
cinsiyet
kullanma amacı
cilt tipi
fiyat
i̇çerik
ek özellik
form
yaşlanma karşıtı
set i̇çerik adeti
hacim
spf
refill
renk
tip
ek hizmetler

Süpermarket - Kişisel Bakım - Vücut Bakım
kullanma amacı
fiyat
ek özellik
hacim
refill
tip
form

Süpermarket - Kişisel Bakım - Deodorant ve Roll on
cinsiyet
form
fiyat
hacim
koruma süresi

Süpermarket - Kişisel Bakım - Şarjlı Diş Fırçaları
fiyat
fırça kılı sertliği
kullanım amacı
ek hizmetler

Süpermarket - Kişisel Bakım - Kadın Hijyen
fiyat
özellik
hacim
form

Süpermarket - Kişisel Bakım - Kolonya
hacim
form
fiyat

Süpermarket - Kişisel Bakım - Tıraş Ürünleri
cinsiyet
fiyat
bıçak sayısı
tipi
hacim
form

Süpermarket - Kişisel Bakım - Güneş Ürünleri
fiyat
spf
hacim
cilt tipi
tip
form
kullanma amacı
ek özellik
görünüm
yaşlanma karşıtı
suya/tere dayanıklılık
kutu durumu

Süpermarket - Bebek Bakım
fiyat
ek hizmetler

Süpermarket - Bebek Bakım - Süt Arttırıcı İçecekler
fiyat

Süpermarket - Bebek Bakım - Bebek Ek Besin
fiyat

Süpermarket - Bebek Bakım - Bebek Bezi
tip
fiyat
bez bedeni
paket i̇çi bez adedi

Süpermarket - Bebek Bakım - Islak Mendil & Havlu
paket i̇çeriği
fiyat
ek özellik

Süpermarket - Bebek Bakım - Bebek Kozmetik
fiyat
tip
bez bedeni

Süpermarket - Bebek Bakım - Bebek Burun Aspiratörü
fiyat

Süpermarket - Bebek Bakım - Bebek Diş Fırçası
fiyat

Süpermarket - Bebek Bakım - Bebek Mamaları
mama numarası
fiyat

Süpermarket - Bebek Bakım - Bebek Diş Macunu
fiyat

Süpermarket - Bebek Bakım - Bebek Temizleme Pamuğu
fiyat

Süpermarket - Bebek Bakım - Bebek Güneş Kremi
fiyat
spf
tip
refill

Süpermarket - Bebek Bakım - Bebek Pudrası
fiyat
hacim
ek özellik

Süpermarket - Bebek Bakım - Bebek Tırnak Makası
fiyat

Süpermarket - Bebek Bakım - Bebek Yağı
fiyat

Süpermarket - Bebek Bakım - Bebek Bakım Seti
fiyat

Süpermarket - Bebek Bakım - Bebek Şampuanı
boy
fiyat

Süpermarket - Bebek Bakım - Bebek Kolonyası
fiyat

Süpermarket - Bebek Bakım - Bebek Bakım Örtüsü
fiyat
renk

Süpermarket - Gıda ve İçecek
fiyat
öğütülme türü
ağırlık

Süpermarket - Gıda ve İçecek - Çay
fiyat

Süpermarket - Gıda ve İçecek - Özel Gıda
fiyat

Süpermarket - Gıda ve İçecek - Atıştırmalık
fiyat

Süpermarket - Gıda ve İçecek - Kahvaltılık
fiyat

Süpermarket - Gıda ve İçecek - Kuru Gıda
fiyat

Süpermarket - Gıda ve İçecek - Kahve
ağırlık
öğütülme türü
fiyat

Süpermarket - Gıda ve İçecek - Makarna
fiyat

Süpermarket - Gıda ve İçecek - Salça
fiyat

Süpermarket - Gıda ve İçecek - Sıvı Yağ
fiyat

Süpermarket - Gıda ve İçecek - Un
ağırlık
fiyat

Süpermarket - Gıda ve İçecek - Tuz & Baharat
fiyat

Süpermarket - Gıda ve İçecek - Çorba
fiyat

Süpermarket - Gıda ve İçecek - Gevrek
fiyat

Süpermarket - Gıda ve İçecek - Yulaf
fiyat

Süpermarket - Gıda ve İçecek - Konserve
fiyat

Süpermarket - Gıda ve İçecek - Şeker
fiyat

Süpermarket - Gıda ve İçecek - Süt
fiyat

Süpermarket - Gıda ve İçecek - Pasta Süslemeleri
fiyat

Süpermarket - Gıda ve İçecek - Bitki Çayları
fiyat

Süpermarket - Gıda ve İçecek - Gazsız İçecekler
fiyat

Süpermarket - Atıştırmalık
fiyat

Süpermarket - Atıştırmalık - Kuru Meyve
fiyat

Süpermarket - Atıştırmalık - Kuruyemiş
fiyat

Süpermarket - Atıştırmalık - Cips
fiyat

Süpermarket - Atıştırmalık - Çikolata
fiyat

Süpermarket - Atıştırmalık - Gofret
fiyat

Süpermarket - Atıştırmalık - Bisküvi
fiyat

Süpermarket - Atıştırmalık - Kraker
fiyat

Süpermarket - Atıştırmalık - Şekerleme
fiyat

Süpermarket - Atıştırmalık - Sakız
fiyat

Süpermarket - Atıştırmalık - Protein Bar
fiyat

Süpermarket - Atıştırmalık - Sağlıklı Atıştırmalıklar
fiyat

Süpermarket - Atıştırmalık - Unlu Mamüller
fiyat

Süpermarket - Atıştırmalık - Kek
fiyat

Süpermarket - Petshop
beden
ürün tipi
fiyat
kısırlaştırılmış
yaş
ağırlık
özellik
renk
aroma
form
ek hizmetler

Süpermarket - Petshop - Kedi Maması
ağırlık
kısırlaştırılmış
yaş
aroma
fiyat
özellik

Süpermarket - Petshop - Kedi Kumu
ağırlık / hacim
kum türü
koku tipi
tane şekli
fiyat
tip

Süpermarket - Petshop - Köpek Maması
ağırlık
yaş
boyut
aroma
fiyat
özellik

Süpermarket - Petshop - Kedi Vitamini
form
kısırlaştırılmış
fiyat

Süpermarket - Petshop - Köpek Tasması
beden
ürün tipi
fiyat
renk

Süpermarket - Petshop - Kuş Ürünleri
mama cinsi
şekil
fiyat

Süpermarket - Petshop - Akvaryum Ürünleri
fiyat

Süpermarket - Petshop - Kedi Box & Taşıma Çantaları
ürün tipi
fiyat
renk

Süpermarket - Petshop - Kedi ve Köpek Oyuncakları
renk
fiyat
ürün tipi

Süpermarket - Petshop - Kedi Yaş Mamaları
aroma
fiyat
i̇çerik

Süpermarket - Petshop - Kedi Ödül Mamaları
form
fiyat
aroma

Süpermarket - Petshop - Köpek Ödül Mamaları
form
fiyat
aroma

Süpermarket - Petshop - Kısır Kedi Mamaları
ağırlık
aroma
kısırlaştırılmış
özellik
yaş
fiyat

Süpermarket - Petshop - Kedi Şampuanı
fiyat

Süpermarket - Petshop - Su ve Mama Kapları
materyal
hacim
özellik
fiyat
renk

Süpermarket - Petshop - Kuş Yemleri
mama cinsi
fiyat
şekil

Süpermarket - Petshop - Kedi ve Köpek Yatakları
beden
fiyat
renk
boy
tip

Süpermarket - Petshop - Akvaryum Balık Yemi
fiyat

Süpermarket - Petshop - Kedi Tuvaleti
fiyat
tip
renk
ek hizmetler

Süpermarket - Petshop - Kedi Fırça ve Tarağı
fiyat

Süpermarket - Petshop - Kedi Tırmalaması
fiyat
ürün tipi
renk

Kozmetik - Makyaj
fiyat
renk
form
boy
suya/tere dayanıklılık

Kozmetik - Makyaj - Göz Makyajı
renk
fiyat
form
suya/tere dayanıklılık
boy

Kozmetik - Makyaj - Ten Makyajı
fiyat
kapatıcılık
cilt tipi
renk
form
suya/tere dayanıklılık
spf
görünüm

Kozmetik - Makyaj - Dudak Makyajı
fiyat
renk
form
boy

Kozmetik - Makyaj - Makyaj Seti
fiyat

Kozmetik - Makyaj - Oje & Aseton
renk
fiyat

Kozmetik - Makyaj - Fondöten
fiyat
kapatıcılık
cilt tipi
görünüm
suya/tere dayanıklılık
spf
form

Kozmetik - Makyaj - Ruj
fiyat
renk
form
boy

Kozmetik - Makyaj - Dudak Kalemi
fiyat
renk

Kozmetik - Makyaj - Maskara
fiyat
renk
etki
suya/tere dayanıklılık
fırça tipi

Kozmetik - Makyaj - Eyeliner
renk
fiyat
suya/tere dayanıklılık
form

Kozmetik - Makyaj - Göz Kalemi
renk
fiyat
suya/tere dayanıklılık
tip

Kozmetik - Makyaj - Kapatıcılar
fiyat
kapatıcılık
renk
suya/tere dayanıklılık

Kozmetik - Makyaj - Allık
fiyat
renk
form
ürün güvenliği bilgisi

Kozmetik - Makyaj - Highlighter
fiyat
form
renk

Kozmetik - Makyaj - BB & CC Krem
fiyat
cilt tipi
kapatıcılık
renk
spf
suya/tere dayanıklılık

Kozmetik - Makyaj - Kontür ve Paletler
fiyat
form
renk

Kozmetik - Makyaj - Pudra
fiyat
form
kapatıcılık
renk

Kozmetik - Makyaj - Takma Tırnak
renk
fiyat

Kozmetik - Makyaj - Far Paleti
fiyat
renk
boy
form
ürün güvenliği bilgisi
ek hizmetler

Kozmetik - Cilt Bakımı
cinsiyet
kullanma amacı
cilt tipi
fiyat
i̇çerik
ek özellik
form
yaşlanma karşıtı
set i̇çerik adeti
hacim
spf
refill
renk
tip
ek hizmetler

Kozmetik - Cilt Bakımı - Yüz Kremi
cilt tipi
kullanma amacı
yaşlanma karşıtı
hacim
fiyat
i̇çerik
ek özellik
form
spf
refill

Kozmetik - Cilt Bakımı - Yüz Temizleme
cilt tipi
kullanma amacı
fiyat
form
ek özellik
i̇çerik
hacim
refill

Kozmetik - Cilt Bakımı - Yüz Maskesi
kullanma amacı
fiyat
cilt tipi
tip
form
ek özellik
i̇çerik
yaşlanma karşıtı
set i̇çerik adeti

Kozmetik - Cilt Bakımı - Göz Bakımı
kullanma amacı
fiyat
cilt tipi
yaşlanma karşıtı
i̇çerik
ek özellik
hacim
form

Kozmetik - Cilt Bakımı - Güneş Koruyucu
spf
cilt tipi
hacim
tip
fiyat
kullanma amacı
suya/tere dayanıklılık
yaşlanma karşıtı
ek özellik
görünüm
kutu durumu
form

Kozmetik - Cilt Bakımı - Cilt Serumu
i̇çerik
kullanma amacı
cilt tipi
yaşlanma karşıtı
fiyat
hacim
refill
ek özellik

Kozmetik - Cilt Bakımı - El & Ayak Bakımı
fiyat
hacim
ek hizmetler

Kozmetik - Cilt Bakımı - Tonikler
i̇çerik
cilt tipi
kullanma amacı
fiyat
hacim
ek özellik
refill

Kozmetik - Cilt Bakımı - Nemlendiriciler
cilt tipi
kullanma amacı
yaşlanma karşıtı
hacim
fiyat
i̇çerik
ek özellik
form
spf
refill

Kozmetik - Cilt Bakımı - Yüz Maskeleri
kullanma amacı
fiyat
cilt tipi
tip
form
ek özellik
i̇çerik
yaşlanma karşıtı
set i̇çerik adeti

Kozmetik - Cilt Bakımı - Peeling
kullanma amacı
cilt tipi
form
fiyat
i̇çerik
ek özellik

Kozmetik - Cilt Bakımı - El Kremleri
fiyat
hacim
tip
ek özellik
kutu durumu

Kozmetik - Cilt Bakımı - Vücut Losyonları
fiyat
ek özellik
kullanma amacı
tip
hacim
form
refill

Kozmetik - Cilt Bakımı - Selülit Kremleri
fiyat
hacim
tip
form
ek özellik

Kozmetik - Cilt Bakımı - Makyaj Temizleyici
form
fiyat
hacim
cilt tipi
tip
ek özellik
özellik

Kozmetik - Cilt Bakımı - Güneş Kremleri
cilt tipi
spf
fiyat
hacim
ek özellik
görünüm
tip
kullanma amacı
yaşlanma karşıtı
kutu durumu

Kozmetik - Cilt Bakımı - At Kılı Fırçaları
fiyat

Kozmetik - Cilt Bakımı - Cilt Sıkılaştırıcılar
fiyat
kullanma amacı
hacim
refill
form
tip
ek özellik

Kozmetik - Cilt Bakımı - Vücut Spreyleri
fiyat
koku türü
hacim

Kozmetik - Parfüm & Deodorant
cinsiyet
koku türü
fiyat
tip
hacim
refill
form

Kozmetik - Parfüm & Deodorant - Parfüm
cinsiyet
fiyat
koku türü
tip
hacim
refill

Kozmetik - Parfüm & Deodorant - Parfüm Setleri
cinsiyet
fiyat
hacim
tip

Kozmetik - Parfüm & Deodorant - Deodorant
cinsiyet
form
fiyat
hacim
koruma süresi

Kozmetik - Parfüm & Deodorant - Vücut Spreyi
fiyat
koku türü
hacim

Kozmetik - Saç Bakımı
cinsiyet
saç tipi
etki
fiyat
özellik
renk
tip
kalıcılık
refill

Kozmetik - Saç Bakımı - Şampuan
cinsiyet
etki
saç tipi
fiyat
refill

Kozmetik - Saç Bakımı - Saç Şekillendirici
etki
fiyat
tutuculuk / sertlik

Kozmetik - Saç Bakımı - Saç Serumu & Maskesi
etki
saç tipi
fiyat

Kozmetik - Saç Bakımı - Saç Boyası
cinsiyet
renk
kalıcılık
fiyat
özellik

Kozmetik - Saç Bakımı - Mor Şampuan
cinsiyet
fiyat
etki
saç tipi
refill

Kozmetik - Saç Bakımı - Kuru Şampuan
saç tipi
etki
fiyat

Kozmetik - Saç Bakımı - Saç Köpüğü
fiyat
etki

Kozmetik - Saç Bakımı - Saç Kremi
etki
fiyat
saç tipi

Kozmetik - Saç Bakımı - Fön Suyu
fiyat
etki
tutuculuk / sertlik
saç tipi

Kozmetik - Saç Bakımı - Saç Bakım Spreyi
fiyat
etki
tutuculuk / sertlik

Kozmetik - Saç Bakımı - Renk Açıcı
fiyat

Kozmetik - Saç Bakımı - Geçici Saç Boyaları
cinsiyet
renk
kalıcılık
fiyat
özellik

Kozmetik - Saç Bakımı - Saç Makası
fiyat

Kozmetik - Saç Bakımı - Tarak
tip
fiyat
renk

Kozmetik - Saç Bakımı - Saç Bantları
fiyat
renk

Kozmetik - Saç Bakımı - Toka
cinsiyet
renk
fiyat
materyal
desen

Kozmetik - Saç Bakımı - Saç Vitamini
fiyat

Kozmetik - Saç Bakımı - Saç Toniği
fiyat

Kozmetik - Saç Bakımı - Wax
fiyat
tutuculuk / sertlik

Kozmetik - Kişisel Bakım
fiyat

Kozmetik - Kişisel Bakım - Duş Jelleri
cinsiyet
hacim
fiyat
refill

Kozmetik - Kişisel Bakım - Şampuan
cinsiyet
etki
saç tipi
fiyat
refill

Kozmetik - Kişisel Bakım - Pamuk
fiyat

Kozmetik - Kişisel Bakım - Vücut Spreyleri
fiyat
koku türü
hacim

Kozmetik - Kişisel Bakım - Parfüm
cinsiyet
fiyat
koku türü
tip
hacim
refill

Kozmetik - Kişisel Bakım - Deodorant
cinsiyet
form
fiyat
hacim
koruma süresi

Kozmetik - Kişisel Bakım - Ağız Bakım Suyu
kullanım amacı
hacim
i̇çerik
form
fiyat

Kozmetik - Kişisel Bakım - Diş Fırçası
fiyat
fırça kılı sertliği
kullanım amacı
ek hizmetler

Kozmetik - Kişisel Bakım - Diş Macunu
kullanım amacı
fiyat
i̇çerik

Kozmetik - Kişisel Bakım - Diş İpi
fiyat
çeşit

Kozmetik - Kişisel Bakım - Şarjlı Diş Fırçaları
fiyat
fırça kılı sertliği
kullanım amacı
ek hizmetler

Kozmetik - Kişisel Bakım - Törpüler
fiyat

Kozmetik - Kişisel Bakım - Kaş Makası
fiyat

Kozmetik - Kişisel Bakım - Günlük Ped
fiyat

Kozmetik - Kişisel Bakım - Mesane Pedi
fiyat
beden

Kozmetik - Kişisel Bakım - Kese
fiyat

Kozmetik - Kişisel Bakım - Banyo Lifi
fiyat

Kozmetik - Kişisel Bakım - Diş Beyazlatıcı
fiyat
form
i̇çerik

Kozmetik - Kişisel Bakım - Gıda Takviyeleri
çeşit
fiyat
form
aroma

Kozmetik - Saç Şekillendirici
etki
fiyat
tutuculuk / sertlik

Kozmetik - Saç Şekillendirici - Saç Köpüğü
fiyat
etki

Kozmetik - Saç Şekillendirici - Saç Spreyi
fiyat
etki
tutuculuk / sertlik

Kozmetik - Saç Şekillendirici - Jöle
tutuculuk / sertlik
fiyat
etki

Kozmetik - Saç Şekillendirici - Wax
fiyat
tutuculuk / sertlik

Kozmetik - Makyaj Aksesuarları
fiyat
renk
materyal
fırça tipi
tip
kıl tipi

Kozmetik - Makyaj Aksesuarları - Makyaj Fırçaları
fırça tipi
fiyat
kıl tipi
tip

Kozmetik - Makyaj Aksesuarları - Makyaj Süngerleri
fiyat

Kozmetik - Makyaj Aksesuarları - Makyaj Çantaları
fiyat
renk
materyal

Kozmetik - Makyaj Aksesuarları - Cımbız
fiyat

Kozmetik - Makyaj Aksesuarları - Kirpik Kıvırıcı
fiyat
renk

Kozmetik - Epilasyon & Tıraş
cinsiyet
fiyat
form
cilt tipi
ürün tipi

Kozmetik - Epilasyon & Tıraş - Ağda
ürün tipi
fiyat
form
cilt tipi
uygulama alanı
kullanım şekli

Kozmetik - Epilasyon & Tıraş - Tıraş Bıçağı
cinsiyet
bıçak sayısı
tipi
fiyat

Kozmetik - Epilasyon & Tıraş - Epilatör
fiyat
tip
kullanım
garanti tipi
ek hizmetler

Kozmetik - Epilasyon & Tıraş - Tıraş Köpüğü
cinsiyet
hacim
fiyat
form

Kozmetik - Epilasyon & Tıraş - Ağda Bantları
ürün tipi
fiyat
form
cilt tipi
uygulama alanı
kullanım şekli

Kozmetik - Genel Bakım
cinsiyet
fiyat
kullanma amacı
cilt tipi
renk
tip
yaşlanma karşıtı
hacim
refill
form
koku türü
etki
ek özellik
saç tipi
i̇çerik
kalıcılık
spf
özellik
boy
suya/tere dayanıklılık
set i̇çerik adeti
görünüm
ek hizmetler

Kozmetik - Genel Bakım - Cinsel Sağlık
fiyat

Kozmetik - Genel Bakım - Hijyenik Ped
özellik
fiyat

Kozmetik - Genel Bakım - Vücut Bakımı
kullanma amacı
fiyat
ek özellik
hacim
refill
tip
form

Kozmetik - Genel Bakım - El ve Ayak Bakımı
fiyat
hacim
ek hizmetler

Kozmetik - Genel Bakım - Duş Jeli ve Kremi
cinsiyet
hacim
fiyat
refill

Kozmetik - Genel Bakım - Bakım Yağları
hacim
fiyat

Kozmetik - Genel Bakım - Ayak Törpüleri
fiyat

Kozmetik - Genel Bakım - Katı Sabun
fiyat

Kozmetik - Genel Bakım - Sıvı Sabun
fiyat
refill

Kozmetik - Genel Bakım - Pamuk
fiyat

Kozmetik - Genel Bakım - El Dezenfektanı
fiyat
hacim

Ayakkabı & Çanta - Kadın Ayakkabı
cinsiyet
beden
renk
topuk boyu
materyal
fiyat
topuk tipi
dış materyal
burun tipi
bağlama şekli
sezon
kalıp
desen
ek özellik
kullanım alanı
i̇ç astar & i̇ç taban materyali
taban tipi
alt taban materyali
sürdürülebilirlik detayı

Ayakkabı & Çanta - Kadın Ayakkabı - Spor Ayakkabı
cinsiyet
beden
renk
fiyat
taban tipi
topuk boyu
bağlama şekli
materyal
ek özellik
dış materyal
topuk tipi
desen
i̇ç astar & i̇ç taban materyali
alt taban materyali
sürdürülebilirlik detayı

Ayakkabı & Çanta - Kadın Ayakkabı - Topuklu Ayakkabı
cinsiyet
beden
renk
topuk boyu
topuk tipi
fiyat
burun tipi
materyal
bağlama şekli
kalıp
dış materyal
sezon
desen
ek özellik
i̇ç astar & i̇ç taban materyali
alt taban materyali

Ayakkabı & Çanta - Kadın Ayakkabı - Günlük Ayakkabı
cinsiyet
beden
renk
materyal
topuk boyu
fiyat
topuk tipi
dış materyal
ek özellik
bağlama şekli
kalıp
burun tipi
i̇ç astar & i̇ç taban materyali
sürdürülebilirlik detayı
desen
alt taban materyali

Ayakkabı & Çanta - Kadın Ayakkabı - Bot & Bootie
cinsiyet
beden
renk
topuk boyu
fiyat
materyal
topuk tipi
dış materyal
bağlama şekli
burun tipi
i̇ç astar & i̇ç taban materyali
ek özellik
kullanım alanı
alt taban materyali
kalıp

Ayakkabı & Çanta - Kadın Ayakkabı - Sandalet
cinsiyet
beden
renk
topuk boyu
materyal
fiyat
topuk tipi
dış materyal
bağlama şekli
özellik
sürdürülebilirlik detayı

Ayakkabı & Çanta - Kadın Ayakkabı - Terlik
cinsiyet
beden
renk
topuk tipi
materyal
fiyat
topuk boyu
ek özellik
dış materyal
sezon
i̇ç astar & i̇ç taban materyali
kalıp
desen
sürdürülebilirlik detayı

Ayakkabı & Çanta - Kadın Ayakkabı - Sneaker
cinsiyet
beden
renk
fiyat
topuk boyu
materyal
taban tipi
dış materyal
bağlama şekli
ek özellik
topuk tipi
alt taban materyali
desen
sürdürülebilirlik detayı
i̇ç astar & i̇ç taban materyali

Ayakkabı & Çanta - Kadın Ayakkabı - Babet
cinsiyet
beden
renk
fiyat
materyal
topuk boyu
burun tipi
dış materyal
topuk tipi
kalıp
bağlama şekli
sürdürülebilirlik detayı
alt taban materyali
i̇ç astar & i̇ç taban materyali
desen
ek özellik

Ayakkabı & Çanta - Kadın Ayakkabı - Loafer
cinsiyet
beden
renk
materyal
topuk boyu
fiyat
dış materyal
topuk tipi
i̇ç astar & i̇ç taban materyali
burun tipi
sürdürülebilirlik detayı
kutu durumu

Ayakkabı & Çanta - Kadın Ayakkabı - Anne Ayakkabısı
cinsiyet
beden
renk
fiyat
topuk tipi
materyal
topuk boyu
kalıp
burun tipi
dış materyal
ek özellik
bağlama şekli
sürdürülebilirlik detayı
alt taban materyali
desen
i̇ç astar & i̇ç taban materyali

Ayakkabı & Çanta - Kadın Ayakkabı - Taşlı Sandalet
cinsiyet
beden
renk
fiyat
topuk boyu
topuk tipi
materyal
dış materyal
bağlama şekli
sürdürülebilirlik detayı

Ayakkabı & Çanta - Kadın Ayakkabı - Hastane Terlikleri
cinsiyet
beden
renk
fiyat
topuk boyu
topuk tipi
desen
sürdürülebilirlik detayı
materyal
i̇ç astar & i̇ç taban materyali
dış materyal
ek özellik
sezon

Ayakkabı & Çanta - Kadın Ayakkabı - Topuklu Terlik
cinsiyet
beden
renk
topuk boyu
fiyat
materyal
topuk tipi
ek özellik
sezon
dış materyal
desen
i̇ç astar & i̇ç taban materyali
sürdürülebilirlik detayı
kalıp

Ayakkabı & Çanta - Kadın Ayakkabı - Topuklu Bot
cinsiyet
beden
renk
materyal
topuk boyu
fiyat
bağlama şekli
topuk tipi
ek özellik
dış materyal
burun tipi
kalıp
i̇ç astar & i̇ç taban materyali
alt taban materyali
kullanım alanı

Ayakkabı & Çanta - Kadın Ayakkabı - Çizme
cinsiyet
beden
renk
topuk boyu
materyal
fiyat
topuk tipi
dış materyal
bağlama şekli
burun tipi
özellik
i̇ç astar & i̇ç taban materyali
sürdürülebilirlik detayı
alt taban materyali

Ayakkabı & Çanta - Kadın Ayakkabı - Kovboy Çizmesi
cinsiyet
beden
fiyat
renk
materyal
topuk boyu
özellik
topuk tipi
burun tipi
dış materyal
bağlama şekli
i̇ç astar & i̇ç taban materyali
alt taban materyali
sürdürülebilirlik detayı

Ayakkabı & Çanta - Kadın Ayakkabı - Dolgu Topuk Ayakkabı
cinsiyet
beden
renk
topuk boyu
fiyat
topuk tipi
materyal
dış materyal
bağlama şekli
sürdürülebilirlik detayı
ek özellik

Ayakkabı & Çanta - Kadın Ayakkabı - Kar Botu
cinsiyet
beden
ek özellik
renk
fiyat
topuk boyu
topuk tipi
desen
bağlama şekli
dış materyal
materyal
alt taban materyali
i̇ç astar & i̇ç taban materyali
sürdürülebilirlik detayı

Ayakkabı & Çanta - Kadın Ayakkabı - Yağmur Botu
cinsiyet
beden
çocuk cinsiyeti
renk
materyal
fiyat
topuk boyu
topuk tipi
bağlama şekli
alt taban materyali
burun tipi
i̇ç astar & i̇ç taban materyali
dış materyal
sürdürülebilirlik detayı
ek özellik
kullanım alanı
kalıp

Ayakkabı & Çanta - Kadın Ayakkabı - Panduf
cinsiyet
beden
renk
fiyat
topuk tipi
topuk boyu
desen
bağlama şekli
materyal
sürdürülebilirlik detayı
taban
alt taban materyali
i̇ç astar & i̇ç taban materyali
ek özellik
dış materyal

Ayakkabı & Çanta - Erkek Ayakkabı
cinsiyet
beden
renk
fiyat
materyal
dış materyal
bağlama şekli
topuk boyu
taban tipi
ek özellik
alt taban materyali
i̇ç astar & i̇ç taban materyali
topuk tipi
kullanım alanı
burun tipi
desen
kalıp
sürdürülebilirlik detayı

Ayakkabı & Çanta - Erkek Ayakkabı - Spor Ayakkabı
cinsiyet
beden
renk
fiyat
materyal
bağlama şekli
taban tipi
dış materyal
ek özellik
topuk boyu
topuk tipi
alt taban materyali
i̇ç astar & i̇ç taban materyali
sürdürülebilirlik detayı
desen

Ayakkabı & Çanta - Erkek Ayakkabı - Günlük Ayakkabı
cinsiyet
beden
renk
materyal
fiyat
dış materyal
bağlama şekli
topuk boyu
ek özellik
topuk tipi
alt taban materyali
sürdürülebilirlik detayı

Ayakkabı & Çanta - Erkek Ayakkabı - Klasik Ayakkabı
cinsiyet
beden
renk
materyal
fiyat
dış materyal
bağlama şekli
alt taban materyali
topuk boyu
topuk tipi
sürdürülebilirlik detayı

Ayakkabı & Çanta - Erkek Ayakkabı - Bot
cinsiyet
beden
renk
dış materyal
fiyat
bağlama şekli
materyal
kalıp
ek özellik
kullanım alanı
topuk boyu
i̇ç astar & i̇ç taban materyali
burun tipi
topuk tipi
alt taban materyali

Ayakkabı & Çanta - Erkek Ayakkabı - Sneaker
cinsiyet
beden
renk
fiyat
materyal
dış materyal
taban tipi
bağlama şekli
topuk boyu
ek özellik
i̇ç astar & i̇ç taban materyali
alt taban materyali
desen
topuk tipi
sürdürülebilirlik detayı

Ayakkabı & Çanta - Erkek Ayakkabı - Koşu Ayakkabısı
cinsiyet
beden
renk
fiyat
dış materyal
topuk boyu
ek özellik
topuk tipi
bağlama şekli
alt taban materyali
i̇ç astar & i̇ç taban materyali
desen
sürdürülebilirlik detayı

Ayakkabı & Çanta - Erkek Ayakkabı - Krampon
cinsiyet
beden
fiyat
renk
bağlama şekli
spor branşı
topuk tipi
alt taban materyali
dış materyal
topuk boyu
ek özellik
kumaş tipi
desen
sürdürülebilirlik detayı
i̇ç astar & i̇ç taban materyali

Ayakkabı & Çanta - Erkek Ayakkabı - Loafer
cinsiyet
beden
renk
materyal
fiyat
dış materyal
topuk tipi
i̇ç astar & i̇ç taban materyali
topuk boyu
burun tipi
sürdürülebilirlik detayı
kutu durumu

Ayakkabı & Çanta - Erkek Ayakkabı - Halı Saha Ayakkabısı
cinsiyet
beden
fiyat
çivi tipi
bilek stili
renk
bağlama şekli
materyal
çeşit
topuk boyu
dış materyal

Ayakkabı & Çanta - Erkek Ayakkabı - Sandalet
cinsiyet
beden
renk
materyal
fiyat
dış materyal
bağlama şekli
topuk boyu
özellik
topuk tipi
sürdürülebilirlik detayı

Ayakkabı & Çanta - Erkek Ayakkabı - Çizme
cinsiyet
beden
fiyat
materyal
renk
topuk boyu
topuk tipi
burun tipi
bağlama şekli
sürdürülebilirlik detayı
alt taban materyali
i̇ç astar & i̇ç taban materyali
dış materyal

Ayakkabı & Çanta - Erkek Ayakkabı - Postal
cinsiyet
beden
materyal
renk
kalıp
fiyat
topuk tipi
bağlama şekli
topuk boyu
dış materyal
i̇ç astar & i̇ç taban materyali
kullanım alanı
alt taban materyali
ek özellik
burun tipi

Ayakkabı & Çanta - Erkek Ayakkabı - Basketbol Ayakkabısı
cinsiyet
beden
fiyat
renk
bilek stili
bağlama şekli
topuk boyu
dış materyal
topuk tipi
sürdürülebilirlik detayı
alt taban materyali
ek özellik

Ayakkabı & Çanta - Erkek Ayakkabı - Terlik
cinsiyet
beden
fiyat
renk
materyal
ek özellik
dış materyal
sezon
topuk boyu
i̇ç astar & i̇ç taban materyali
desen
topuk tipi
sürdürülebilirlik detayı
kalıp

Ayakkabı & Çanta - Erkek Ayakkabı - Ev Terliği
cinsiyet
beden
materyal
sezon
renk
fiyat
dış materyal
paket i̇çeriği
topuk tipi
sürdürülebilirlik detayı
topuk boyu

Ayakkabı & Çanta - Erkek Ayakkabı - Panduf
cinsiyet
beden
renk
fiyat
topuk boyu
topuk tipi
desen
bağlama şekli
materyal
sürdürülebilirlik detayı
taban
i̇ç astar & i̇ç taban materyali
alt taban materyali
ek özellik
dış materyal

Ayakkabı & Çanta - Erkek Ayakkabı - Deniz Ayakkabısı
cinsiyet
beden
fiyat
renk
materyal
ek özellik
alt taban materyali
desen
i̇ç astar & i̇ç taban materyali
sürdürülebilirlik detayı
dış materyal

Ayakkabı & Çanta - Erkek Ayakkabı - Süet Ayakkabı
cinsiyet
beden
renk
fiyat
topuk boyu
materyal
topuk tipi
bağlama şekli
dış materyal
burun tipi
ek özellik
desen
i̇ç astar & i̇ç taban materyali
alt taban materyali
kalıp
kullanım alanı
sürdürülebilirlik detayı

Ayakkabı & Çanta - Erkek Ayakkabı - Yürüyüş Ayakkabısı
cinsiyet
beden
fiyat
renk
bağlama şekli
materyal
ek özellik
topuk boyu
dış materyal

Ayakkabı & Çanta - Çocuk Ayakkabı
cinsiyet
beden
çocuk cinsiyeti
renk
fiyat
bağlama şekli
materyal
ek özellik
topuk boyu
dış materyal
desen
taban tipi
i̇ç astar & i̇ç taban materyali
topuk tipi
sürdürülebilirlik detayı
alt taban materyali
kalıp
burun tipi

Ayakkabı & Çanta - Çocuk Ayakkabı - Spor Ayakkabı
cinsiyet
beden
çocuk cinsiyeti
renk
fiyat
bağlama şekli
ek özellik
topuk tipi
materyal
desen
dış materyal
i̇ç astar & i̇ç taban materyali
topuk boyu
taban tipi
alt taban materyali
sürdürülebilirlik detayı

Ayakkabı & Çanta - Çocuk Ayakkabı - Günlük Ayakkabı
cinsiyet
beden
renk
çocuk cinsiyeti
fiyat
materyal
ek özellik
topuk boyu
topuk tipi
bağlama şekli
dış materyal
sürdürülebilirlik detayı
desen
alt taban materyali
kalıp
burun tipi
i̇ç astar & i̇ç taban materyali

Ayakkabı & Çanta - Çocuk Ayakkabı - Babet
cinsiyet
beden
renk
topuk boyu
fiyat
çocuk cinsiyeti
topuk tipi
bağlama şekli
desen
dış materyal
kalıp
burun tipi
i̇ç astar & i̇ç taban materyali
materyal
sürdürülebilirlik detayı
alt taban materyali
ek özellik

Ayakkabı & Çanta - Çocuk Ayakkabı - Bot
cinsiyet
beden
çocuk cinsiyeti
fiyat
ek özellik
renk
materyal
bağlama şekli
topuk tipi
topuk boyu
kullanım alanı
kalıp
dış materyal
i̇ç astar & i̇ç taban materyali
alt taban materyali
burun tipi

Ayakkabı & Çanta - Çocuk Ayakkabı - Sneaker
cinsiyet
beden
çocuk cinsiyeti
renk
bağlama şekli
ek özellik
fiyat
materyal
topuk boyu
desen
topuk tipi
taban tipi
dış materyal
i̇ç astar & i̇ç taban materyali
alt taban materyali
sürdürülebilirlik detayı

Ayakkabı & Çanta - Çocuk Ayakkabı - Sandalet
cinsiyet
beden
çocuk cinsiyeti
renk
fiyat
materyal
dış materyal
bağlama şekli
topuk boyu
özellik
topuk tipi
sürdürülebilirlik detayı

Ayakkabı & Çanta - Çocuk Ayakkabı - Terlik
cinsiyet
beden
çocuk cinsiyeti
renk
fiyat
materyal
ek özellik
sezon
desen
topuk tipi
topuk boyu
sürdürülebilirlik detayı
i̇ç astar & i̇ç taban materyali
dış materyal

Ayakkabı & Çanta - Çocuk Ayakkabı - Panduf
cinsiyet
beden
çocuk cinsiyeti
renk
bağlama şekli
fiyat
topuk tipi
topuk boyu
desen
materyal
sürdürülebilirlik detayı
i̇ç astar & i̇ç taban materyali
alt taban materyali
taban
ek özellik
dış materyal

Ayakkabı & Çanta - Çocuk Ayakkabı - Çizme
cinsiyet
beden
çocuk cinsiyeti
renk
fiyat
i̇ç astar & i̇ç taban materyali
topuk tipi
topuk boyu
burun tipi
bağlama şekli
materyal
sürdürülebilirlik detayı
alt taban materyali
dış materyal

Ayakkabı & Çanta - Çocuk Ayakkabı - Basketbol Ayakkabısı
cinsiyet
beden
çocuk cinsiyeti
renk
bilek stili
bağlama şekli
fiyat
dış materyal
topuk boyu
topuk tipi
sürdürülebilirlik detayı
alt taban materyali
ek özellik

Ayakkabı & Çanta - Çocuk Ayakkabı - Krampon
cinsiyet
beden
fiyat
renk
bağlama şekli
topuk tipi
spor branşı
çocuk cinsiyeti
topuk boyu
ek özellik
desen
dış materyal
alt taban materyali
sürdürülebilirlik detayı
i̇ç astar & i̇ç taban materyali
kumaş tipi

Ayakkabı & Çanta - Çocuk Çanta
cinsiyet
beden
renk
çocuk cinsiyeti
fiyat
tip
desen
materyal
sürdürülebilirlik detayı
kapasite
deri kalitesi

Ayakkabı & Çanta - Çocuk Çanta - Sırt Çantası
cinsiyet
çocuk cinsiyeti
renk
boyut
fiyat
kapasite
materyal
desen

Ayakkabı & Çanta - Çocuk Çanta - Okul Çantası
cinsiyet
çocuk cinsiyeti
fiyat
renk
tip
kapasite
desen
materyal
sürdürülebilirlik detayı
deri kalitesi

Ayakkabı & Çanta - Çocuk Çanta - Çekçekli Çanta
cinsiyet
renk
çocuk cinsiyeti
fiyat
tip
desen
sürdürülebilirlik detayı
materyal
deri kalitesi
kapasite

Ayakkabı & Çanta - Çocuk Çanta - Beslenme Çantası
cinsiyet
çocuk cinsiyeti
fiyat
renk
desen
sürdürülebilirlik detayı
kapasite

Ayakkabı & Çanta - Çocuk Çanta - Lisanslı Çantalar
cinsiyet
renk
fiyat
tip
desen
çocuk cinsiyeti
kapasite
materyal
sürdürülebilirlik detayı
deri kalitesi

Ayakkabı & Çanta - Çocuk Çanta - Bel Çantası
cinsiyet
fiyat
çocuk cinsiyeti
renk
desen
sürdürülebilirlik detayı
materyal

Ayakkabı & Çanta - Çocuk Çanta - Postacı Çanta
cinsiyet
çocuk cinsiyeti
fiyat
renk
materyal

Ayakkabı & Çanta - Erkek Aksesuar
cinsiyet
beden
boyut/ebat
boyut
materyal
fiyat
renk
kordon materyali
mekanizma
kasa renk
kadran renk
taş cinsi
yaş
desen
özellik
ayar
cam tipi
sürdürülebilirlik detayı
kumaş tipi
kasa materyali
kasa çapı
kordon renk
su geçirmezlik
cam şekli
cam renk
çerçeve renk
çerçeve formu
garanti süresi
çerçeve materyali
cam materyali
çerçeve tipi
ekartman
kapasite
deri kalitesi
tip
batarya türü
kutu durumu
batarya boyutu

Ayakkabı & Çanta - Erkek Aksesuar - Saat
cinsiyet
fiyat
kordon materyali
renk
mekanizma
su geçirmezlik
kadran renk
kasa materyali
cam tipi
özellik
kasa renk
cam şekli
garanti süresi
batarya türü
batarya boyutu
kasa çapı
kordon renk

Ayakkabı & Çanta - Erkek Aksesuar - Güneş Gözlüğü
cinsiyet
cam renk
fiyat
çerçeve formu
cam materyali
renk
çerçeve materyali
cam tipi
çerçeve tipi
özellik
desen
çerçeve renk
ekartman

Ayakkabı & Çanta - Erkek Aksesuar - Cüzdan
cinsiyet
fiyat
materyal
boyut
renk
tip
deri kalitesi
yaş
desen
sürdürülebilirlik detayı

Ayakkabı & Çanta - Erkek Aksesuar - Kemer
cinsiyet
beden
renk
materyal
fiyat

Ayakkabı & Çanta - Erkek Aksesuar - Şapka
cinsiyet
beden
renk
fiyat
materyal

Ayakkabı & Çanta - Erkek Aksesuar - Bileklik
cinsiyet
beden
boyut/ebat
fiyat
materyal
renk
taş cinsi
ayar
özellik

Ayakkabı & Çanta - Erkek Aksesuar - Kravat
cinsiyet
renk
desen
fiyat
materyal
kumaş tipi

Ayakkabı & Çanta - Erkek Aksesuar - Kolye
fiyat
materyal
özellik

Ayakkabı & Çanta - Erkek Aksesuar - Rozet
fiyat
materyal
özellik

Ayakkabı & Çanta - Erkek Aksesuar - Papyon
cinsiyet
beden
renk
fiyat
desen
materyal

Ayakkabı & Çanta - Kadın Aksesuar
cinsiyet
beden
fiyat
materyal
renk
boyut/ebat
boyut
desen
ayar
kasa renk
model
tip
özellik
taş cinsi
yaş
sürdürülebilirlik detayı
kumaş tipi
cam tipi
kapasite
cam renk
çerçeve formu
çerçeve renk
çerçeve materyali
cam materyali
çerçeve tipi
mekanizma
kasa materyali
kordon materyali
kasa çapı
kordon renk
su geçirmezlik
cam şekli
ekartman
kadran renk
garanti süresi
deri kalitesi
kutu durumu
batarya türü
batarya boyutu

Ayakkabı & Çanta - Kadın Aksesuar - Saat
cinsiyet
fiyat
renk
kordon materyali
su geçirmezlik
kadran renk
kasa materyali
kasa renk
özellik
mekanizma
cam tipi
cam şekli
garanti süresi
batarya boyutu
kasa çapı
batarya türü
kordon renk

Ayakkabı & Çanta - Kadın Aksesuar - Takı
cinsiyet
beden
materyal
boyut/ebat
renk
fiyat
ayar
model
taş cinsi
özellik

Ayakkabı & Çanta - Kadın Aksesuar - Şapka
cinsiyet
beden
renk
fiyat
materyal

Ayakkabı & Çanta - Kadın Aksesuar - Güneş Gözlüğü
cinsiyet
renk
fiyat
çerçeve formu
cam renk
cam materyali
çerçeve materyali
çerçeve tipi
cam tipi
özellik
desen
çerçeve renk
ekartman

Ayakkabı & Çanta - Kadın Aksesuar - Saç Aksesuarları
cinsiyet
beden
renk
materyal
desen
fiyat

Ayakkabı & Çanta - Kadın Aksesuar - Kemer
cinsiyet
beden
renk
materyal
fiyat

Ayakkabı & Çanta - Kadın Aksesuar - Gümüş Kolye
cinsiyet
beden
fiyat
materyal
renk
ayar
özellik
taş cinsi

Ayakkabı & Çanta - Kadın Aksesuar - Hasır Bilezik
cinsiyet
beden
ayar
fiyat
özellik
renk
materyal

Ayakkabı & Çanta - Kadın Çanta
cinsiyet
beden
renk
fiyat
materyal
boyut
kapasite
desen
yaş
ek özellik
kumaş tipi
sürdürülebilirlik detayı

Ayakkabı & Çanta - Kadın Çanta - Omuz Çantası
cinsiyet
beden
renk
materyal
fiyat
kapasite
yaş
kumaş tipi
desen
sürdürülebilirlik detayı

Ayakkabı & Çanta - Kadın Çanta - Sırt Çantası
cinsiyet
renk
fiyat
boyut
materyal
kapasite
desen

Ayakkabı & Çanta - Kadın Çanta - Cüzdan
cinsiyet
renk
fiyat
materyal
boyut
deri kalitesi
tip
desen
yaş
sürdürülebilirlik detayı

Ayakkabı & Çanta - Kadın Çanta - Spor Çantası
cinsiyet
renk
fiyat
boyut
materyal
kapasite
desen
sürdürülebilirlik detayı

Ayakkabı & Çanta - Kadın Çanta - Bel Çantası
cinsiyet
renk
fiyat
materyal
desen
sürdürülebilirlik detayı

Ayakkabı & Çanta - Kadın Çanta - El Çantası
cinsiyet
renk
fiyat
boyut
materyal
desen
ek özellik
kapasite

Ayakkabı & Çanta - Kadın Çanta - Portföy
cinsiyet
renk
materyal
fiyat
sürdürülebilirlik detayı

Ayakkabı & Çanta - Kadın Çanta - Bez Çanta
cinsiyet
beden
renk
fiyat
yaş
desen
kumaş tipi
sürdürülebilirlik detayı
materyal

Ayakkabı & Çanta - Kadın Çanta - Kartlık
cinsiyet
renk
fiyat
materyal
boyut
desen

Ayakkabı & Çanta - Kadın Çanta - Abiye Çanta
cinsiyet
renk
fiyat
materyal
desen
sürdürülebilirlik detayı

Ayakkabı & Çanta - Kadın Çanta - Postacı Çantası
cinsiyet
renk
materyal
fiyat

Ayakkabı & Çanta - Kadın Çanta - Plaj Çantası
cinsiyet
kapasite
renk
materyal
fiyat
deri kalitesi

Ayakkabı & Çanta - Kadın Çanta - Laptop Çantası
cinsiyet
çanta tipi
renk
fiyat
ekran boyut aralığı
suya/tere dayanıklılık

Ayakkabı & Çanta - Kadın Çanta - Kapitone Çanta
cinsiyet
beden
renk
boyut
fiyat
materyal
kapasite
desen
yaş
kumaş tipi
ek özellik
tip
sürdürülebilirlik detayı
deri kalitesi

Ayakkabı & Çanta - Kadın Çanta - Evrak Çantası
cinsiyet
beden
fiyat
renk
çanta tipi
ekran boyut aralığı
dosya tipi
suya/tere dayanıklılık

Ayakkabı & Çanta - Kadın Çanta - Kutu Çanta
cinsiyet
beden
renk
materyal
boyut
fiyat
yaş
desen
sürdürülebilirlik detayı
kumaş tipi
kapasite

Ayakkabı & Çanta - Kadın Çanta - Makyaj Çantası
fiyat
renk
materyal

Ayakkabı & Çanta - Kadın Çanta - Peluş Çanta
cinsiyet
beden
renk
boyut
fiyat
materyal
kapasite
desen
yaş
kumaş tipi
ek özellik
tip
sürdürülebilirlik detayı
deri kalitesi

Ayakkabı & Çanta - Kadın Çanta - Hasır Çanta
cinsiyet
beden
renk
fiyat
materyal
kapasite
desen
yaş
kumaş tipi
sürdürülebilirlik detayı

Ayakkabı & Çanta - Kadın Çanta - Valiz & Bavul
cinsiyet
materyal
renk
kapasite
fiyat
boyut
sürdürülebilirlik detayı

Ayakkabı & Çanta - Erkek Çanta
cinsiyet
beden
renk
materyal
fiyat
boyut
kapasite
kumaş tipi
yaş
desen
sürdürülebilirlik detayı

Ayakkabı & Çanta - Erkek Çanta - Sırt Çantası
cinsiyet
boyut
renk
fiyat
kapasite
materyal
desen

Ayakkabı & Çanta - Erkek Çanta - Postacı Çantası
cinsiyet
materyal
renk
fiyat

Ayakkabı & Çanta - Erkek Çanta - Cüzdan & Kartlık
cinsiyet
materyal
fiyat
boyut
renk
deri kalitesi
tip
yaş
desen
sürdürülebilirlik detayı

Ayakkabı & Çanta - Erkek Çanta - Spor Çantası
cinsiyet
kapasite
fiyat
boyut
renk
materyal
desen
sürdürülebilirlik detayı

Ayakkabı & Çanta - Erkek Çanta - Laptop Çantası
cinsiyet
çanta tipi
fiyat
renk
suya/tere dayanıklılık
ekran boyut aralığı

Ayakkabı & Çanta - Erkek Çanta - Bel Çantası
cinsiyet
renk
fiyat
materyal
desen
sürdürülebilirlik detayı

Ayakkabı & Çanta - Erkek Çanta - Omuz Çantası
cinsiyet
beden
materyal
fiyat
renk
kapasite
yaş
desen
sürdürülebilirlik detayı
kumaş tipi

Ayakkabı & Çanta - Erkek Çanta - Portföy Çanta
cinsiyet
materyal
fiyat
renk
sürdürülebilirlik detayı

Ayakkabı & Çanta - Erkek Çanta - Tıraş Çantası
cinsiyet
materyal
renk
fiyat
desen
boyut
ek özellik
kapasite

Ayakkabı & Çanta - Erkek Çanta - Olta Çantası
fiyat
renk

Ayakkabı & Çanta - Erkek Çanta - Okul Çantası
cinsiyet
fiyat
renk
kapasite
tip
materyal
deri kalitesi
desen
sürdürülebilirlik detayı

Ayakkabı & Çanta - Erkek Çanta - Valiz
cinsiyet
materyal
kapasite
renk
fiyat
boyut
sürdürülebilirlik detayı

Ayakkabı & Çanta - Erkek Çanta - Outdoor Çanta
cinsiyet
beden
renk
fiyat
materyal
ek özellik
kullanım alanı
topuk boyu
kalıp
burun tipi
bağlama şekli
i̇ç astar & i̇ç taban materyali
dış materyal
alt taban materyali

Ayakkabı & Çanta - Erkek Çanta - El Çantası
cinsiyet
materyal
boyut
fiyat
renk
kapasite
desen
ek özellik

Elektronik - Küçük Ev Aletleri
fiyat
güç (watt)
özellik
renk
materyal
garanti tipi
garanti süresi
tamir edilebilirlik
frekans
voltaj
otomatik kapanma
ek hizmetler

Elektronik - Küçük Ev Aletleri - Süpürge
güç (watt)
fiyat
özellik
ses seviyesi
hepa filtre
hazne kapasitesi
renk
motor teknolojisi
garanti tipi
garanti süresi
frekans
ek hizmetler

Elektronik - Küçük Ev Aletleri - Robot Süpürge
yer silme özelliği
fiyat
çöp i̇stasyonu
aşılabilir engel seviyesi
güç (watt)
özellik
haritalandırma
uygulama üzerinden kontrol
şarjlı kullanım süresi
garanti tipi
ses seviyesi
hazne kapasitesi
ek hizmetler

Elektronik - Küçük Ev Aletleri - Dikey Süpürge
özellik
güç (watt)
fiyat
şarj standı
hepa filtre
el süpürgesi kullanımı
ses seviyesi
kablo uzunluğu
hazne kapasitesi
motor teknolojisi
garanti süresi
ek hizmetler
garanti tipi
renk
frekans

Elektronik - Küçük Ev Aletleri - Ütü
fiyat
güç (watt)
tip
otomatik kapanma
taban
kireç önleme
damlama emniyeti
basınç
renk
şok buhar
özellik
sürekli buhar
garanti tipi
su kapasitesi
garanti süresi
frekans
ek hizmetler

Elektronik - Küçük Ev Aletleri - Kahve Makinesi
fiyat
fincan kapasitesi
model
renk
materyal
süt köpürtücü
özellik
cezve malzemesi
otomatik su alımı
su kapasitesi
otomatik kapanma
sesli i̇kaz
taşma emniyeti
damlama emniyeti
ek hizmetler
garanti süresi
garanti tipi
voltaj
frekans

Elektronik - Küçük Ev Aletleri - Çay Makinesi
materyal
fiyat
su kapasitesi
renk
demlik malzemesi
otomatik kapanma
demlik kapasitesi
özellik
garanti süresi
ek hizmetler
frekans
garanti tipi

Elektronik - Küçük Ev Aletleri - Blender Seti
güç
fiyat
materyal
hacim
rendeleme ve dilimleme diski
renk
doğrayıcı
özellik
çırpıcı
hız ayarı
garanti süresi
garanti tipi
frekans
ek hizmetler
voltaj

Elektronik - Küçük Ev Aletleri - Tost Makinesi
fiyat
materyal
ekmek dilim kapasitesi
renk
çıkarılabilir plaka
güç (watt)
izgara özelliği
plaka kullanımı
özellik
isı ayarı
voltaj
garanti süresi
frekans
garanti tipi
ek hizmetler

Elektronik - Küçük Ev Aletleri - Doğrayıcı & Rondo
güç (watt)
fiyat
hazne kapasitesi
materyal
bıçak sayısı
hazne malzemesi
özellik
ek hizmetler
renk
voltaj
frekans
garanti tipi

Elektronik - Küçük Ev Aletleri - Su Isıtıcı & Kettle
materyal
fiyat
hacim
renk
güç (watt)
otomatik kapanma
özellik
garanti süresi
frekans
garanti tipi
ek hizmetler

Elektronik - Küçük Ev Aletleri - Mikser & Mikser Seti
güç (watt)
fiyat
hamur kancası
materyal
hacim
renk
garanti süresi
hız ayarı
garanti tipi
özellik
ek hizmetler

Elektronik - Küçük Ev Aletleri - Airfryer & Fritöz
pişirme kapasitesi
fiyat
özellik
materyal
garanti tipi
renk
garanti süresi
voltaj
ek hizmetler

Elektronik - Giyilebilir Teknoloji
özellik
sesli görüşme
renk
kordon materyali
kordon renk
fiyat
kasa renk
garanti tipi
kasa çapı
kordon boyutu
ek hizmetler

Elektronik - Giyilebilir Teknoloji - Akıllı Saat
fiyat
özellik
sesli görüşme
renk
kordon materyali
kordon renk
kasa renk
garanti tipi
ek hizmetler
kasa çapı
kordon boyutu

Elektronik - Giyilebilir Teknoloji - Akıllı Bileklik
fiyat
özellik
renk
ek hizmetler

Elektronik - Giyilebilir Teknoloji - VR Gözlük
fiyat
özellik
renk
garanti tipi
ek hizmetler

Elektronik - Telefon
fiyat
cep telefonu modeli
pil gücü (mah)
renk
hızlı şarj
garanti tipi
materyal
bağlantı tipi
tip
ek hizmetler
uyumlu marka

Elektronik - Telefon - Cep Telefonu
fiyat
cep telefonu modeli
ram kapasitesi
mobil bağlantı hızı
pil gücü (mah)
ekran boyutu
nfc
kamera çözünürlüğü
garanti tipi
renk
özellik
kozmetik durum
çift hat
yapay zeka
ön kamera sayısı
ek hizmetler
dahili hafıza

Elektronik - Telefon - Android Cep Telefonları
ram kapasitesi
fiyat
mobil bağlantı hızı
nfc
ekran boyutu
pil gücü (mah)
kamera çözünürlüğü
garanti tipi
yapay zeka
çift hat
cep telefonu modeli
renk
özellik
ön kamera sayısı
ek hizmetler
dahili hafıza

Elektronik - Telefon - iPhone Cep Telefonu
cep telefonu modeli
fiyat
garanti tipi
ram kapasitesi
renk
ekran boyutu
ön kamera çözünürlük aralığı
ön kamera sayısı
dahili hafıza
görüntülü konuşma
görüntü teknolojisi
ekran teknolojisi
dokunmatik ekran
radio
özellik
ek hizmetler

Elektronik - Telefon - Telefon Kılıfları
cep telefonu modeli
uyumlu marka
renk
materyal
fiyat

Elektronik - Telefon - Şarj Cihazları
hızlı şarj
bağlantı tipi
fiyat
renk
ek hizmetler

Elektronik - Telefon - Powerbank
pil gücü (mah)
hızlı şarj
fiyat
usb çıkış sayısı
renk
ek hizmetler

Elektronik - Telefon - Araç İçi Telefon Tutucu
türü
telefon tutucu özellikleri
fiyat
renk
materyal

Elektronik - Telefon - iPhone Kılıflar
cep telefonu modeli
renk
fiyat
materyal

Elektronik - Telefon - Kulaklıklar
fiyat
renk
özellik
ek hizmetler
garanti tipi

Elektronik - Foto & Kamera
fiyat
renk
tip
ek hizmetler

Elektronik - Foto & Kamera - Aksiyon Kamera
fiyat
özellik
renk
ek hizmetler

Elektronik - Foto & Kamera - Fotoğraf Makinesi
fiyat
renk
fotoğraf çözünürlük
optik zoom
özellik
ek hizmetler
bellek kartı tipi

Elektronik - Foto & Kamera - Video Kamera
fiyat
özellik
kayıt tipi
bellek kartı tipi
optik zoom
renk
garanti tipi
ek hizmetler

Elektronik - Foto & Kamera - Şipşak Fotoğraf Makinesi
fiyat
renk
özellik
fotoğraf çözünürlük
bellek kartı tipi
optik zoom
ek hizmetler

Elektronik - Foto & Kamera - Dijital Fotoğraf Makinesi
fiyat
renk
fotoğraf çözünürlük
optik zoom
özellik
ek hizmetler
bellek kartı tipi

Elektronik - Foto & Kamera - Kamera Lensleri
fiyat
renk
tip
ek hizmetler

Elektronik - Foto & Kamera - Hafıza Kartı
hafıza kartı tipi
fiyat
kapasite

Elektronik - TV & Görüntü & Ses
fiyat
renk
hareket seçeneği
ek hizmetler

Elektronik - TV & Görüntü & Ses - Televizyon
fiyat
görüntüleme teknolojisi
ekran yenileme hızı
smart tv
görüntü kalitesi
model yılı
i̇şletim sistemi
dahili uydu alıcı
wi-fi özelliği
çözünürlük (piksel)
hdr
özellik
renk
ek hizmetler
ekran boyutu

Elektronik - TV & Görüntü & Ses - Smart TV
renk
fiyat
smart tv
görüntüleme teknolojisi
görüntü kalitesi
wi-fi özelliği
dahili uydu alıcı
ekran boyutu
i̇şletim sistemi
çözünürlük (piksel)
model yılı
hdr
ekran yenileme hızı
özellik
ek hizmetler

Elektronik - TV & Görüntü & Ses - QLED TV
fiyat
görüntüleme teknolojisi
ekran yenileme hızı
smart tv
görüntü kalitesi
model yılı
i̇şletim sistemi
dahili uydu alıcı
wi-fi özelliği
çözünürlük (piksel)
hdr
renk
ek hizmetler
ekran boyutu

Elektronik - TV & Görüntü & Ses - OLED TV
fiyat
görüntüleme teknolojisi
ekran yenileme hızı
smart tv
görüntü kalitesi
model yılı
i̇şletim sistemi
dahili uydu alıcı
wi-fi özelliği
çözünürlük (piksel)
hdr
özellik
renk
ek hizmetler
ekran boyutu

Elektronik - TV & Görüntü & Ses - TV Kumandaları
fiyat
renk

Elektronik - TV & Görüntü & Ses - Soundbar
kanal yapısı
fiyat
özellik
watt aralığı
ek hizmetler

Elektronik - TV & Görüntü & Ses - Projeksiyon Cihazı
parlaklık (ansilümen)
çözünürlük
fiyat
çözünürlük teknolojisi
ampul ömrü (eco mod)
görüntü teknolojisi
ek hizmetler
renk

Elektronik - TV & Görüntü & Ses - Media Player
çözünürlük teknolojisi
ethernet
usb
fiyat
renk
ek hizmetler

Elektronik - TV & Görüntü & Ses - Hoparlör
fiyat
özellik
dinleme süresi
renk
ek hizmetler

Elektronik - TV & Görüntü & Ses - Kulaklık
fiyat
renk
özellik
ek hizmetler
garanti tipi

Elektronik - TV & Görüntü & Ses - Uydu Alıcısı
görüntü kalitesi
fiyat
ethernet
usb
ek hizmetler
renk

Elektronik - TV & Görüntü & Ses - Çanak Anten
ürün tipi
fiyat
renk
garanti süresi
ek hizmetler
garanti tipi

Elektronik - TV & Görüntü & Ses - HDMI Kablo
fiyat
renk

Elektronik - TV & Görüntü & Ses - Akım Korumalı Prizler
priz sayısı
kablo uzunluğu
akım koruma
fiyat
tip
renk
usb
özellik
ek hizmetler

Elektronik - TV & Görüntü & Ses - Kablo & Adaptör
fiyat
renk

Elektronik - TV & Görüntü & Ses - LNB
fiyat
renk
garanti tipi
ürün tipi
garanti süresi
ek hizmetler

Elektronik - TV & Görüntü & Ses - TV Ekran Koruyucu
fiyat

Elektronik - TV & Görüntü & Ses - TV Askı Aparatı
ekran boyutu (i̇nç)
hareket seçeneği
fiyat
renk

Elektronik - TV & Görüntü & Ses - Kablolu Hoparlör
fiyat
özellik
dinleme süresi
renk
ek hizmetler

Elektronik - Dijital Kod & Ürünler
fiyat

Elektronik - Dijital Kod & Ürünler - Dijital Hediye Kartları
fiyat
kart değeri

Elektronik - Dijital Kod & Ürünler - E-pin & Cüzdan Kodları
fiyat

Elektronik - Dijital Kod & Ürünler - Ön Ödemeli Kartlar
fiyat

Elektronik - Beyaz Eşya
fiyat
renk
özellik
ek hizmetler

Elektronik - Beyaz Eşya - Buzdolabı
toplam hacim
yükseklik
genişlik
fiyat
enerji sınıfı
renk
derinlik
dondurucu özelliği
dondurucu yeri
tip
kullanım şekli
buzluk tipi
ücretsiz kurulum/montaj
özellik
ek hizmetler

Elektronik - Beyaz Eşya - Çamaşır Makinesi
kapasite
fiyat
enerji sınıfı
kurutma özelliği
renk
maksimum sıkma devri
derinlik
ücretsiz kurulum/montaj
özellik
ek hizmetler

Elektronik - Beyaz Eşya - Bulaşık Makinesi
fiyat
enerji sınıfı
renk
program sayısı
kapasite
kullanım şekli
genişlik
derinlik
ücretsiz kurulum/montaj
özellik
yarım yük
su tüketimi
ek hizmetler

Elektronik - Beyaz Eşya - Kurutma Makinesi
maksimum kurutma kapasitesi
enerji sınıfı
kurutma teknolojisi
fiyat
renk
derinlik
özellik
ücretsiz kurulum/montaj
ek hizmetler

Elektronik - Beyaz Eşya - Derin Dondurucu
çekmece sayısı
toplam hacim
dondurucu özelliği
tip
enerji sınıfı
genişlik
fiyat
derinlik
yükseklik
renk
özellik
ücretsiz kurulum/montaj
garanti tipi
ek hizmetler

Elektronik - Beyaz Eşya - Ankastre Setler
renk
ocak tipi
ocak yüzeyi
fiyat
pişirme özelliği
davlumbaz şekli
pişirme fonksiyon sayısı
özellik
saat tipi
enerji sınıfı
ücretsiz kurulum/montaj
tema / stil
ek hizmetler

Elektronik - Beyaz Eşya - Kombi
maksimum isıl güç
cihaz tipi
fiyat
isıtma tekniği
isıtma kapasitesi
ücretsiz kurulum/montaj
baca tipi
eşanjör sayısı
ek hizmetler
özellik
renk

Elektronik - Beyaz Eşya - Mikrodalga Fırın
fiyat
hacim
renk
kullanım şekli
izgara özelliği
kontrol tipi
güç
özellik
ek hizmetler

Elektronik - Beyaz Eşya - Aspiratör
kullanım alanı
maksimum emiş gücü
fiyat
genişlik
renk
filtre sayısı
özellik
ek hizmetler

Elektronik - Beyaz Eşya - Mini & Midi Fırın
hacim
pişirme özelliği
fiyat
renk
özellik
pişirme fonksiyon sayısı
buharlı
ek hizmetler

Elektronik - Beyaz Eşya - Ankastre Davlumbaz
genişlik
maksimum emiş gücü
renk
davlumbaz tipi
fiyat
davlumbaz şekli
enerji sınıfı
ücretsiz kurulum/montaj
özellik
ek hizmetler
filtre tipi

Elektronik - Beyaz Eşya - Ankastre Ocak
ocak tipi
gaz tipi
renk
ocak yüzeyi
kullanım şekli
ocak göz sayısı
genişlik
özellik
fiyat
ücretsiz kurulum/montaj
ek hizmetler

Elektronik - Bilgisayar & Tablet
renk
fiyat
i̇şletim sistemi
ram (sistem belleği)
i̇şlemci tipi
ssd kapasitesi
i̇şlemci nesli
ekran kartı
ekran boyutu
ekran kartı hafızası
i̇şlemci modeli
ekran yenileme hızı
ram (sistem belleği) tipi
çözünürlük
kullanım amacı
i̇şlemci çekirdek sayısı
hard disk kapasitesi
dokunmatik ekran
cihaz ağırlığı
panel tipi
parmak i̇zi okuyucu
şarjlı kullanım süresi
ekran kartı gücü
ek hizmetler

Elektronik - Bilgisayar & Tablet - Bilgisayarlar
fiyat
ekran kartı
i̇şlemci tipi
ekran kartı hafızası
ekran boyutu
ram (sistem belleği) tipi
i̇şlemci nesli
i̇şletim sistemi
i̇şlemci modeli
ekran yenileme hızı
hard disk kapasitesi
kullanım amacı
ekran kartı gücü
çözünürlük
i̇şlemci çekirdek sayısı
renk
panel tipi
şarjlı kullanım süresi
cihaz ağırlığı
parmak i̇zi okuyucu
dokunmatik ekran
ek hizmetler
ram (sistem belleği)
ssd kapasitesi

Elektronik - Bilgisayar & Tablet - Tablet
fiyat
ekran boyutu
ram (sistem belleği)
bellek kapasitesi
renk
i̇şletim sistemi
özellik
hızlı şarj
çözünürlük
ek hizmetler
kapasite
sim kart uyumu

Elektronik - Bilgisayar & Tablet - Bilgisayar Bileşenleri
fiyat
kapasite
soğutucu tipleri
garanti tipi
ek hizmetler

Elektronik - Bilgisayar & Tablet - Monitör
çözünürlük
fiyat
panel tipi
çözünürlük standartı
curved (kavisli)
ekran boyutu
görüntüleme teknolojisi
dahili hoparlör
hdmi
özellik
type-c
sync teknolojisi
ek hizmetler
hdmi giriş sayısı
mini displayport
dvi-d
garanti tipi
tepki süresi
ekran yenilenme hızı
dvi-i
hdcp
garanti süresi

Elektronik - Bilgisayar & Tablet - Yazıcı & Tarayıcı
fiyat
renk
ek hizmetler

Elektronik - Bilgisayar & Tablet - Ağ & Modem
fiyat
ek hizmetler

Elektronik - Bilgisayar & Tablet - Klavye
fiyat
bağlantılar
renk
tuş düzeni
numerik tuşlar
klavye dili
touchpad
ek hizmetler

Elektronik - Bilgisayar & Tablet - Mouse
bağlantılar
fiyat
ek hizmetler

Elektronik - Bilgisayar & Tablet - Grafik Tablet
fiyat
özellik
ek hizmetler

Elektronik - Bilgisayar & Tablet - SSD
bağlantı tipi
fiyat
okuma hızı
yazma hızı
ek hizmetler
ssd kapasitesi

Elektronik - Bilgisayar & Tablet - RAM
ekran kartı bellek tipi
ram hızı
uyumlu sistemler
fiyat
özellik
kapasite
ek hizmetler

Elektronik - Bilgisayar & Tablet - Ekran Kartı
ekran kartı hafızası
fiyat
çip seti
ekran kartı bellek tipi
ek hizmetler
grafik i̇şlemcisi
overclock
seri

Elektronik - Bilgisayar & Tablet - Çocuk Çizim Tableti
özellik
fiyat
renk
ek hizmetler

Elektronik - Kişisel Bakım Aletleri
tıraş bölgesi
fiyat
tip
kullanım
maksimum sıcaklık
voltaj
renk
frekans
garanti süresi
başlık sayısı
burun ve kulak temizleme başlığı
otomatik kapanma
garanti tipi
dijital ekran
plaka materyali
kablosuz özelliği
şarjlı kullanım süresi
isı ayarı
ek hizmetler

Elektronik - Kişisel Bakım Aletleri - Saç Düzleştirici
fiyat
maksimum sıcaklık
tip
i̇yon özelliği
renk
isı ayarı
plaka materyali
kablosuz özelliği
otomatik kapanma
dijital ekran
garanti tipi
ek hizmetler

Elektronik - Kişisel Bakım Aletleri - Saç Maşası
maşa çapı
fiyat
tip
maksimum sıcaklık
isı ayarı
plaka materyali
kablosuz özelliği
renk
dijital ekran
voltaj
frekans
otomatik kapanma
garanti tipi
ek hizmetler

Elektronik - Kişisel Bakım Aletleri - Saç Kurutma Makinesi
fiyat
güç
i̇yon özelliği
tip
difüzör
hız ayarı
renk
motor tipi
isı ayarı
özellik
garanti süresi
garanti tipi
otomatik kapanma
frekans
ek hizmetler

Elektronik - Kişisel Bakım Aletleri - Tıraş Makinesi
tıraş bölgesi
fiyat
tip
kullanım
burun ve kulak temizleme başlığı
başlık sayısı
şarjlı kullanım süresi
garanti tipi
renk
garanti süresi
otomatik kapanma
voltaj
frekans
ek hizmetler

Elektronik - Kişisel Bakım Aletleri - Tartı
fiyat
maksimum ağırlık
vücut kitle i̇ndeksi ölçümü
vücut su oranı ölçümü
bazal metabolizma hızı ölçümü
bluetooth
materyal
uygulama üzerinden kontrol
lcd ekran
özellik
garanti tipi
ek hizmetler

Elektronik - Kişisel Bakım Aletleri - Epilasyon Aletleri
fiyat
tip
kullanım
garanti tipi
ek hizmetler

Elektronik - Kişisel Bakım Aletleri - IPL Lazer Epilasyon
fiyat
atım sayısı
uygulama alanı
cilt tonu sensörü
tip
otomatik kapanma
garanti tipi
kademe ayarı
frekans
renk
voltaj
uygulama üzerinden kontrol
ek hizmetler

Elektronik - Oyunculara Özel
fiyat

Elektronik - Oyunculara Özel - Playstation
fiyat
sabit disk
kol sayısı
model
garanti tipi
ek hizmetler

Elektronik - Oyunculara Özel - Xbox
fiyat
model
sabit disk
garanti tipi
renk
özellik
ek hizmetler

Elektronik - Oyunculara Özel - Nintendo
fiyat
model
garanti tipi
bluetooth
oyun türü
ek hizmetler

Elektronik - Oyunculara Özel - Playstation Oyunları
oyun türü
fiyat
bluetooth

Elektronik - Oyunculara Özel - Konsol Aksesuarları
uyumlu cihaz
bağlantı
ürün türü
fiyat
garanti tipi
özellik
renk
ek hizmetler

Elektronik - Oyunculara Özel - Oyuncu Bilgisayarı
ekran kartı
fiyat
i̇şlemci tipi
ekran kartı hafızası
i̇şlemci modeli
ram (sistem belleği) tipi
ekran yenileme hızı
ekran kartı gücü
i̇şlemci nesli
i̇şletim sistemi
ekran boyutu
ekran kartı bellek tipi
ek hizmetler
çözünürlük
i̇şlemci çekirdek sayısı
ram (sistem belleği)
ssd kapasitesi
optik sürücü tipi

Elektronik - Oyunculara Özel - Oyuncu Donanımları
fiyat
bağlantı türü
numerik tuşlar
tuş düzeni
renk
switch türü
rgb aydınlatma
klavye dili
switch rengi
bilek desteği
mikrofon
aktif gürültü önleme (anc)
kullanım tipi
ürün i̇çeriği
mouse hassasiyeti (dpi)
ek hizmetler

Elektronik - Oyunculara Özel - Oyuncu Monitörleri
çözünürlük
panel tipi
fiyat
curved (kavisli)
çözünürlük standartı
görüntüleme teknolojisi
dahili hoparlör
özellik
sync teknolojisi
hdmi
ek hizmetler
hdmi giriş sayısı
ekran boyutu
type-c
ekran yenilenme hızı
tepki süresi
cihaz ağırlığı
enerji sınıf aralığı

Elektronik - Oyunculara Özel - Oyuncu Koltuğu
fiyat
renk
taşıma kapasitesi
ayak malzemesi
sırt mekanizması
kol desteği
oturak derinliği

Elektronik - Oyunculara Özel - Oyuncu Kulaklığı
bağlantı türü
fiyat
kulaklık modeli
mikrofon
renk
kullanım tipi
aktif gürültü önleme (anc)
rgb aydınlatma
ek hizmetler

Elektronik - Oyunculara Özel - Oyuncu Mouse
bağlantı türü
fiyat
kablo uzunluğu
batarya tipi
rgb aydınlatma
mouse hassasiyeti (dpi)
ek hizmetler

Elektronik - Oyunculara Özel - Oyuncu Klavyesi
switch türü
fiyat
bağlantı türü
renk
numerik tuşlar
klavye dili
rgb aydınlatma
tuş düzeni
bilek desteği
ek hizmetler
switch rengi

Elektronik - Oyunculara Özel - Bilgisayar Oyunları
oyun türü
fiyat
garanti tipi
bluetooth
ek hizmetler

Elektronik - Elektronik Aksesuarlar
cinsiyet
cep telefonu modeli
fiyat
ekran boyutu
renk
kılıf tipi
materyal
uyumlu marka
özellik
ekran kartı
ram (sistem belleği) tipi
uyumlu model
kullanım amacı
beden
garanti tipi
i̇şletim sistemi
i̇şlemci nesli
ssd kapasitesi
i̇şlemci tipi
ram (sistem belleği)
ekran kartı hafızası
ekran yenileme hızı
çözünürlük
tip
rgb aydınlatma
baskılı
bilek desteği
hard disk kapasitesi
garanti süresi
bağlantı tipi
i̇şlemci modeli
cihaz ağırlığı
dokunmatik ekran
i̇şlemci çekirdek sayısı
sesli görüşme
parmak i̇zi okuyucu
panel tipi
tamir edilebilirlik
frekans
kasa renk
kordon renk
voltaj
şarjlı kullanım süresi
kasa çapı
kordon materyali
ek hizmetler

Elektronik - Elektronik Aksesuarlar - Bilgisayar Aksesuar
fiyat
bağlantılar
rgb aydınlatma
renk
baskılı
bilek desteği
dinleme süresi
ek hizmetler

Elektronik - Elektronik Aksesuarlar - Telefon Aksesuarları
cep telefonu modeli
fiyat
uyumlu marka
bağlantı tipi
hızlı şarj
renk
materyal
pil gücü (mah)
ek hizmetler

Elektronik - Elektronik Aksesuarlar - TV Aksesuarları
renk
fiyat
hareket seçeneği

Elektronik - Elektronik Aksesuarlar - Veri Depolama
hafıza kartı tipi
okuma hızı
giriş/çıkış portları
fiyat
renk
kapasite
ek hizmetler

Elektronik - Klima & Istıcılar
tip
fiyat
özellik
renk
ek hizmetler

Elektronik - Klima & Istıcılar - Klima
soğutma kapasitesi
tip
isıtma kapasitesi
fiyat
i̇nverter
wi-fi özelliği
enerji sınıfı - soğutma
ücretsiz kurulum/montaj
renk
enerji sınıfı - isıtma
çift ünite
ek hizmetler
özel filtreler

Elektronik - Klima & Istıcılar - Kombi
maksimum isıl güç
cihaz tipi
fiyat
isıtma tekniği
isıtma kapasitesi
ücretsiz kurulum/montaj
baca tipi
eşanjör sayısı
ek hizmetler
özellik
renk

Elektronik - Klima & Istıcılar - Isıtıcılar
güç
fiyat
tip
renk
voltaj
frekans
garanti tipi
özellik
ek hizmetler

Elektronik - Klima & Istıcılar - Vantilatör
tip
fiyat
özellik
renk
ek hizmetler

Elektronik - Klima & Istıcılar - Şofben
yakıt tipi
fiyat
özellik
ücretsiz kurulum/montaj
renk
ek hizmetler

Elektronik - Klima & Istıcılar - Termosifon
kapasite
fiyat
ücretsiz kurulum/montaj
isıtma gücü
özellik
renk
ek hizmetler

Elektronik - Klima & Istıcılar - Hava Temizleyici
fiyat
filtre türü
özellik
renk
ek hizmetler

Elektronik - Klima & Istıcılar - Hava Nemlendirici
özellik
fiyat
sıcak soğuk kullanımı
renk
ek hizmetler

Saat & Aksesuar - Parti Malzemeleri
beden
parti konsepti
renk
yaş
materyal
fiyat
balon çeşidi
özellik
ebatlar
enerji tasarrufu
ek hizmetler

Saat & Aksesuar - Parti Malzemeleri - Led Işık
özellik
renk
fiyat
enerji tasarrufu
ebatlar

Saat & Aksesuar - Parti Malzemeleri - Düğün & Kına
renk
fiyat
materyal
boyut/ebat

Saat & Aksesuar - Parti Malzemeleri - Yılbaşı Süsü
renk
fiyat

Saat & Aksesuar - Parti Malzemeleri - Yılbaşı Ağacı
fiyat
renk
ağaç boyu

Saat & Aksesuar - Parti Malzemeleri - Balon
renk
balon çeşidi
fiyat
özellik

Saat & Aksesuar - Hobi Malzemeleri
renk
i̇çerik
metraj
fiyat
gramaj
adet
boyut/ebat

Saat & Aksesuar - Hobi Malzemeleri - Örgü İpi
renk
i̇çerik
fiyat
gramaj
metraj
adet

Saat & Aksesuar - Hobi Malzemeleri - Boncuk
fiyat

Saat & Aksesuar - Hobi Malzemeleri - Kumaş
renk
boyut/ebat
fiyat

Saat & Aksesuar - Hobi Malzemeleri - Nakış Kiti
fiyat

Saat & Aksesuar - Hobi Malzemeleri - Örgü Kiti
fiyat

Saat & Aksesuar - Drone
uçuş süresi
fiyat
sivil havacılık i̇zni
uçuş mesafesi
gps
yedek batarya
kamera özelliği
beni takip et modu
renk
garanti süresi
ek hizmetler

Saat & Aksesuar - Uzaktan Kumandalı Araçlar
fiyat
ek hizmetler

Saat & Aksesuar - Çakmak Ürünleri
fiyat

Saat & Aksesuar - Çakmak Ürünleri - Benzinli Çakmak
fiyat
renk

Saat & Aksesuar - Çakmak Ürünleri - Klasik Çakmak
renk
fiyat

Saat & Aksesuar - Müzik Aletleri
fiyat
müzik türleri
format
ek hizmetler

Saat & Aksesuar - Müzik Aletleri - Pikap & Gramofon
fiyat
renk
özellik
ek hizmetler

Saat & Aksesuar - Müzik Aletleri - Gitar
fiyat
gitar tipi
renk
ek hizmetler

Saat & Aksesuar - Müzik Aletleri - Plak
sanatçı
müzik türleri
fiyat
format

Saat & Aksesuar - Müzik Aletleri - Piyano
fiyat
piyano tipi
renk
ek hizmetler

Saat & Aksesuar - Müzik Aletleri - Org
fiyat
özellik
ek hizmetler

Saat & Aksesuar - Hediyelik Ürünler
fiyat
boyut
ek hizmetler

Saat & Aksesuar - Hediyelik Ürünler - Konsept Hediyelik
fiyat

Saat & Aksesuar - Hediyelik Ürünler - Figür
fiyat
boyut

Saat & Aksesuar - Hediyelik Ürünler - Hediye Kutusu
renk
fiyat

Saat & Aksesuar - Hediyelik Ürünler - Kar Küresi
fiyat

Saat & Aksesuar - Hediyelik Ürünler - Paketleme Malzemesi
fiyat

Saat & Aksesuar - E-Kitap Okuyucu
ekran boyutu
fiyat
kapasite
kalemle not alma
bağlantılar
su geçirmezlik
ek hizmetler

Saat & Aksesuar - Din ve Mitoloji
fiyat
basım dili
boyut
setli/tekil
yazar

Saat & Aksesuar - Kişisel Gelişim
basım dili
setli/tekil
fiyat
yazar

Saat & Aksesuar - Kişisel Gelişim - Bireysel Gelişim
yazar
fiyat
setli/tekil
basım dili

Saat & Aksesuar - Hobi, Sanat, Akademik
sayfa sayısı
fiyat
basım dili
setli/tekil
boyut
basım yılı
yazar

Saat & Aksesuar - Oyun Grupları
cinsiyet
yaş
fiyat
özellik
ek hizmetler

Saat & Aksesuar - Oyun Grupları - Puzzle
fiyat
özellik
ek hizmetler

Saat & Aksesuar - Oyun Grupları - Oyun Kartları
fiyat

Saat & Aksesuar - Oyun Grupları - Okey Takımı
fiyat

Saat & Aksesuar - Oyun Grupları - Satranç
fiyat
özellik

Saat & Aksesuar - Oyun Grupları - Maket
fiyat
ek hizmetler

Saat & Aksesuar - Kırtasiye
fiyat
kağıt boyutu
renk
sayfa tipi
defter tipi
materyal
paket i̇çeriği
kapak türü
sayfa sayısı
tel tipi
kağıt tipi
kalem ucu boyutu
boyut
tip
gramaj
boyut/ebat
türü
ek hizmetler

Saat & Aksesuar - Kırtasiye - Defter
sayfa tipi
kağıt boyutu
sayfa sayısı
fiyat
kapak türü
renk
tel tipi
defter tipi
boyut

Saat & Aksesuar - Kırtasiye - Ajanda
fiyat
renk
tel tipi
boyut
kapak türü

Saat & Aksesuar - Kırtasiye - Etiket
fiyat

Saat & Aksesuar - Kırtasiye - Suluk & Matara
kapasite
materyal
fiyat
renk

Saat & Aksesuar - Kırtasiye - Yazı Tahtası
ölçü
fiyat
renk

Saat & Aksesuar - Kırtasiye - Pano
ölçü
fiyat

Saat & Aksesuar - Kırtasiye - Silgi
fiyat

Saat & Aksesuar - Kırtasiye - Makas
renk
fiyat
boyut

Saat & Aksesuar - Kırtasiye - Yapıştırıcı
yapıştırıcı tipi
fiyat
form

Saat & Aksesuar - Yabancı Dil Kitaplar
basım dili
roman türü
yazar
fiyat
setli/tekil
boyut

Saat & Aksesuar - Yabancı Dil Kitaplar - Yabancı Dil Eğitimi
basım dili
dil seviyesi
setli/tekil
fiyat

Saat & Aksesuar - Yabancı Dil Kitaplar - Yabancı Dil Roman
basım dili
roman türü
fiyat
setli/tekil
boyut
yazar

Saat & Aksesuar - Yabancı Dil Kitaplar - Yabancı Dil Çocuk Kitapları
basım dili
sayfa sayısı
fiyat
setli/tekil
basım yılı
yazar

Saat & Aksesuar - Çizgi Roman, Dergi ve Gazete
fiyat
basım dili
setli/tekil
sayfa sayısı

Saat & Aksesuar - Ofis
fiyat
tip
ek hizmetler

Saat & Aksesuar - Ofis - Fotokopi Kağıdı
kağıt boyutu
gramaj
kağıt tipi
fiyat

Saat & Aksesuar - Ofis - Pil & Şarj Cihazı
tip
fiyat

Saat & Aksesuar - Ofis - Yazarkasa ve Terazi
fiyat
ek hizmetler

Saat & Aksesuar - Ofis - Hesap Makinesi
tip
fiyat
ek hizmetler

Saat & Aksesuar - Ofis - Dosya & Klasör
renk
fiyat
klasör formu
dosya tipi

Saat & Aksesuar - Ofis - Zımba & Delgeç
renk
boyut
fiyat

Saat & Aksesuar - Ofis - Para Sayma Makinesi
fiyat
özellik

Saat & Aksesuar - Ofis - Ciltleme Makinesi
fiyat
ek hizmetler

Saat & Aksesuar - Ofis - Ofis Sarf Tüketim
fiyat

Saat & Aksesuar - Kalem
fiyat
renk

Saat & Aksesuar - Kalem - Keçeli Kalem
fiyat
renk

Saat & Aksesuar - Kalem - Fosforlu Kalem
fiyat
renk

Saat & Aksesuar - Kalem - Uçlu Kalem
fiyat
renk

Saat & Aksesuar - Kalem - Tükenmez Kalem
renk
fiyat

Saat & Aksesuar - Kalem - Kurşun Kalem
renk
fiyat

Saat & Aksesuar - Kalem - Kalem Kutusu
renk
fiyat
materyal
paket i̇çeriği

Saat & Aksesuar - Kalem - Kalem Ucu
fiyat

Saat & Aksesuar - Kalem - Tahta Kalemi
fiyat
renk

Saat & Aksesuar - Kalem - Teknik Çizim Kalemi
fiyat

Saat & Aksesuar - Eğitim
sınıf
sınav tipi
basım yılı
kitap i̇çeriği
fiyat
ders
setli/tekil
basım dili
yazar
sayfa sayısı
ek hizmetler

Saat & Aksesuar - Eğitim - Sınav Hazırlık
sınav tipi
ders
kitap i̇çeriği
basım yılı
setli/tekil
fiyat
yazar
basım dili
sayfa sayısı
ek hizmetler

Saat & Aksesuar - Eğitim - TYT & AYT
sınav tipi
ders
kitap i̇çeriği
basım yılı
setli/tekil
fiyat
yazar
basım dili
sayfa sayısı
ek hizmetler

Saat & Aksesuar - Eğitim - KPSS
sınav tipi
ders
kitap i̇çeriği
basım yılı
setli/tekil
fiyat
yazar
basım dili
sayfa sayısı
ek hizmetler

Saat & Aksesuar - Eğitim - LGS
sınav tipi
ders
kitap i̇çeriği
basım yılı
setli/tekil
fiyat
yazar
basım dili
sayfa sayısı
ek hizmetler

Saat & Aksesuar - Eğitim - Ders ve Yardımcı Kitaplar
sınıf
ders
basım yılı
kitap i̇çeriği
setli/tekil
fiyat
basım dili
yazar
ek hizmetler

Saat & Aksesuar - Eğitim - Tarih
fiyat
setli/tekil
basım dili
basım yılı
yazar
boyut
sayfa sayısı
ders
kitap i̇çeriği
ek hizmetler

Saat & Aksesuar - Eğitim - Güncel - Genel Konular
fiyat
basım dili
basım yılı
setli/tekil
boyut
sayfa sayısı
yazar

Saat & Aksesuar - Eğitim - Sözlük & İmla Kılavuzu
basım dili
fiyat
setli/tekil
yazar

Saat & Aksesuar - Eğitim - Tıp Kitabı
basım yılı
fiyat
basım dili
setli/tekil
boyut
yazar

Saat & Aksesuar - Eğitim - Bilim & Teknik & Mühendislik
fiyat
basım dili
basım yılı
setli/tekil
boyut
sayfa sayısı
yazar

Saat & Aksesuar - Eğitim - Hukuk Kitabı
fiyat
basım dili
setli/tekil
boyut
sayfa sayısı
yazar

Saat & Aksesuar - Boya & Sanatsal Malzemeler
renk
fiyat
kağıt boyutu
kağıt tipi
kalem ucu boyutu

Saat & Aksesuar - Boya & Sanatsal Malzemeler - Akrilik Boya
renk
fiyat

Saat & Aksesuar - Boya & Sanatsal Malzemeler - Tuval & Şövale
fiyat

Saat & Aksesuar - Boya & Sanatsal Malzemeler - Sanatsal Kağıt
kağıt boyutu
renk
fiyat
kağıt tipi
kalem ucu boyutu

Saat & Aksesuar - Boya & Sanatsal Malzemeler - Kuru Boya Kalemi
fiyat
renk

Saat & Aksesuar - Boya & Sanatsal Malzemeler - Fırça
fiyat

Saat & Aksesuar - Boya & Sanatsal Malzemeler - Kumaş Boyası
renk
fiyat

Saat & Aksesuar - Boya & Sanatsal Malzemeler - Pastel Boya
fiyat
renk

Saat & Aksesuar - Boya & Sanatsal Malzemeler - Sulu Boya
fiyat
renk

Saat & Aksesuar - Boya & Sanatsal Malzemeler - Ahşap Boyası
renk
fiyat

Saat & Aksesuar - Çocuk ve Ebeveyn Kitapları
fiyat
basım dili
setli/tekil
basım yılı
sayfa sayısı
yazar

Saat & Aksesuar - Çocuk ve Ebeveyn Kitapları - Aktivite & Eğitici Kitaplar
yaş
setli/tekil
fiyat
basım dili
sayfa sayısı

Saat & Aksesuar - Çocuk ve Ebeveyn Kitapları - Çocuk Masal ve Öykü Kitabı
yaş
yazar
sayfa sayısı
fiyat
basım dili
setli/tekil

Saat & Aksesuar - Çocuk ve Ebeveyn Kitapları - Çocuk Bakımı & Ebeveynlik
fiyat
basım dili
setli/tekil
basım yılı
sayfa sayısı
yazar

Saat & Aksesuar - Çocuk ve Ebeveyn Kitapları - Boyama Kitapları
fiyat
setli/tekil

Saat & Aksesuar - Çocuk ve Ebeveyn Kitapları - Sesli Çocuk Kitapları
yaş
fiyat
setli/tekil
yazar
boyut
sayfa sayısı

Saat & Aksesuar - İş, Ekonomi & Pazarlama
fiyat
basım dili
basım yılı
boyut
setli/tekil
sayfa sayısı
yazar

Spor & Outdoor - Spor Üst Giyim
cinsiyet
beden
materyal
renk
cep
paça tipi
fiyat
kalıp
sezon
boy
ek özellik
siluet
çocuk cinsiyeti
desen
sürdürülebilirlik detayı
bel
kumaş tipi
kol boyu
yaka tipi
kol tipi
paket i̇çeriği
paça boyu
yaş
kumaş teknolojisi
kumaş özellik
kutu durumu

Spor & Outdoor - Spor Üst Giyim - Spor Tişört
cinsiyet
beden
kalıp
renk
materyal
yaka tipi
kol tipi
fiyat
kol boyu
boy
desen
sürdürülebilirlik detayı
kumaş teknolojisi
ek özellik

Spor & Outdoor - Spor Üst Giyim - Ceket & Yelek
cinsiyet
beden
fiyat
renk
boy
kalıp
kol tipi
desen
sürdürülebilirlik detayı
yaka tipi
materyal
ek özellik

Spor & Outdoor - Spor Üst Giyim - Yağmurluk
cinsiyet
beden
fiyat
renk
boy
materyal
yaka tipi
sezon
kumaş tipi
kalıp
desen
kemer/kuşak durumu
kol tipi
siluet
cep
sürdürülebilirlik detayı
kapama şekli

Spor & Outdoor - Spor Üst Giyim - Spor Sütyeni
cinsiyet
beden
renk
materyal
kalıp
kap
fiyat
yaka tipi
ek özellik
kol boyu
desen
sürdürülebilirlik detayı
kumaş tipi
kutu durumu
paket i̇çeriği
sezon

Spor & Outdoor - Spor Üst Giyim - Sweatshirt
cinsiyet
beden
materyal
boy
renk
yaka tipi
fiyat
kalıp
kol boyu
kol tipi
desen
cep
sürdürülebilirlik detayı

Spor & Outdoor - Spor Üst Giyim - Atlet
cinsiyet
beden
renk
materyal
fiyat
kol tipi
desen
kol boyu
kalıp
yaka tipi
boy
sürdürülebilirlik detayı
paket i̇çeriği

Spor & Outdoor - Spor Üst Giyim - Forma
cinsiyet
beden
spor branşı
fiyat
renk
kumaş tipi

Spor & Outdoor - Spor Üst Giyim - Spor Mont
cinsiyet
beden
fiyat
desen
renk
kalıp
boy
yaka tipi
cep
materyal
sürdürülebilirlik detayı
kol tipi
ek özellik

Spor & Outdoor - Spor Üst Giyim - Spor Şapka
cinsiyet
beden
renk
fiyat
tip
materyal

Spor & Outdoor - Spor Alt Giyim
cinsiyet
beden
materyal
renk
cep
paça tipi
fiyat
kalıp
sezon
boy
ek özellik
siluet
çocuk cinsiyeti
desen
sürdürülebilirlik detayı
bel
kumaş tipi
kol boyu
yaka tipi
kol tipi
paket i̇çeriği
paça boyu
yaş
kumaş teknolojisi
kumaş özellik
kutu durumu

Spor & Outdoor - Spor Alt Giyim - Eşofman Takımı
cinsiyet
beden
fiyat
renk
paça tipi
materyal
kol boyu
kalıp
sezon
yaka tipi
cep
siluet
kol tipi
boy
kumaş tipi
ek özellik
bel
desen
sürdürülebilirlik detayı
paket i̇çeriği

Spor & Outdoor - Spor Alt Giyim - Tayt
cinsiyet
beden
boy
renk
ek özellik
paça tipi
bel
fiyat
sürdürülebilirlik detayı
sezon
materyal
kalıp
kumaş tipi
yaş
desen
kutu durumu

Spor & Outdoor - Spor Alt Giyim - Şort
cinsiyet
beden
renk
boy
materyal
fiyat
cep
kumaş teknolojisi
desen
kalıp
bel
sürdürülebilirlik detayı
ek özellik

Spor & Outdoor - Spor Alt Giyim - Termal Giyim
cinsiyet
beden
materyal
renk
boy
fiyat
kumaş tipi
tip
bel

Spor & Outdoor - Spor Alt Giyim - Çorap
cinsiyet
beden
renk
materyal
tip
paket i̇çeriği
fiyat
desen
sezon
boy
siluet
kumaş tipi
ek özellik

Spor & Outdoor - Spor Alt Giyim - Spor Pantolon
cinsiyet
beden
renk
fiyat
kumaş tipi
bel
boy
desen
cep
siluet
paça tipi
sürdürülebilirlik detayı
materyal
kalıp
kumaş teknolojisi
ek özellik

Spor & Outdoor - Spor Alt Giyim - Terlik
cinsiyet
beden
renk
fiyat
topuk boyu
topuk tipi
sürdürülebilirlik detayı
alt taban materyali
materyal
dış materyal
ek özellik

Spor & Outdoor - Spor Alt Giyim - Eşofman
cinsiyet
beden
renk
paça tipi
fiyat
kalıp
materyal
sezon
desen
çocuk cinsiyeti
bel
paça boyu
cep
boy
siluet
kumaş tipi
yaka tipi
kumaş özellik
sürdürülebilirlik detayı
ek özellik
paket i̇çeriği
kol boyu
kol tipi

Spor & Outdoor - Top
fiyat
özellik
sertlik

Spor & Outdoor - Top - Basketbol Topu
fiyat
renk

Spor & Outdoor - Top - Futbol Topu
fiyat
özellik
pompa durumu
top bedeni

Spor & Outdoor - Spor Ayakkabı
cinsiyet
beden
renk
fiyat
taban tipi
bağlama şekli
materyal
topuk boyu
ek özellik
alt taban materyali
desen
dış materyal
i̇ç astar & i̇ç taban materyali
topuk tipi
sürdürülebilirlik detayı

Spor & Outdoor - Spor Ayakkabı - Sneaker
cinsiyet
beden
renk
fiyat
materyal
topuk boyu
dış materyal
taban tipi
desen
topuk tipi
bağlama şekli
ek özellik
i̇ç astar & i̇ç taban materyali
alt taban materyali
sürdürülebilirlik detayı

Spor & Outdoor - Spor Ayakkabı - Koşu Ayakkabısı
cinsiyet
beden
renk
fiyat
dış materyal
bağlama şekli
topuk boyu
alt taban materyali
ek özellik
i̇ç astar & i̇ç taban materyali
desen
topuk tipi
sürdürülebilirlik detayı

Spor & Outdoor - Spor Ayakkabı - Halı Saha Ayakkabısı
cinsiyet
beden
fiyat
çivi tipi
bilek stili
renk
bağlama şekli
materyal
çeşit
topuk boyu
dış materyal

Spor & Outdoor - Spor Ayakkabı - Basketbol Ayakkabısı
cinsiyet
beden
fiyat
renk
bilek stili
bağlama şekli
topuk boyu
dış materyal
topuk tipi
sürdürülebilirlik detayı
alt taban materyali
ek özellik

Spor & Outdoor - Spor Ayakkabı - Yürüyüş Ayakkabısı
cinsiyet
beden
renk
fiyat
bağlama şekli
ek özellik
materyal
topuk boyu
dış materyal

Spor & Outdoor - Spor Ayakkabı - Outdoor Ayakkabı
cinsiyet
beden
kumaş teknolojisi
renk
fiyat
materyal
taban teknolojisi
bağlama şekli
dış materyal
ek özellik
topuk boyu
topuk tipi
sürdürülebilirlik detayı
alt taban materyali
i̇ç astar & i̇ç taban materyali
kalıp

Spor & Outdoor - Spor Ayakkabı - Tenis Ayakkabısı
cinsiyet
beden
fiyat
renk

Spor & Outdoor - Spor Ayakkabı - Voleybol Ayakkabısı
cinsiyet
beden
fiyat
renk
dış materyal

Spor & Outdoor - Spor Ayakkabı - Fitness Ayakkabısı
cinsiyet
beden
fiyat
renk

Spor & Outdoor - Spor Ayakkabı - Deniz Ayakkabısı
cinsiyet
beden
renk
fiyat
çocuk cinsiyeti
alt taban materyali
materyal
dış materyal
desen
sürdürülebilirlik detayı
i̇ç astar & i̇ç taban materyali
ek özellik

Spor & Outdoor - Spor Ayakkabı - Outdoor Bot
cinsiyet
beden
renk
materyal
topuk boyu
fiyat
bağlama şekli
topuk tipi
ek özellik
dış materyal
burun tipi
kalıp
i̇ç astar & i̇ç taban materyali
alt taban materyali
kullanım alanı

Spor & Outdoor - Spor Ayakkabı - Terlik
cinsiyet
beden
renk
topuk boyu
fiyat
materyal
topuk tipi
ek özellik
sezon
dış materyal
desen
i̇ç astar & i̇ç taban materyali
sürdürülebilirlik detayı
kalıp

Spor & Outdoor - Spor Ayakkabı - Sandalet
cinsiyet
beden
renk
topuk boyu
fiyat
materyal
topuk tipi
bağlama şekli
dış materyal
özellik
sürdürülebilirlik detayı

Spor & Outdoor - Spor Ayakkabı - Çizme
cinsiyet
beden
bağlama şekli
topuk boyu
renk
fiyat
materyal
dış materyal
topuk tipi
i̇ç astar & i̇ç taban materyali
alt taban materyali
burun tipi
kullanım alanı
kalıp
ek özellik
sürdürülebilirlik detayı

Spor & Outdoor - Spor Ayakkabı - Bot
cinsiyet
beden
renk
materyal
topuk boyu
fiyat
bağlama şekli
topuk tipi
ek özellik
dış materyal
burun tipi
kalıp
i̇ç astar & i̇ç taban materyali
alt taban materyali
kullanım alanı

Spor & Outdoor - Spor Ayakkabı - Kar Botu
cinsiyet
beden
renk
ek özellik
fiyat
dış materyal
bağlama şekli
materyal
topuk tipi
sürdürülebilirlik detayı
i̇ç astar & i̇ç taban materyali
alt taban materyali
topuk boyu
desen

Spor & Outdoor - Spor Ayakkabı - Kayak Ayakkabısı
beden
renk
fiyat

Spor & Outdoor - Spor Ayakkabı - Snowboard Botu
beden
fiyat
renk

Spor & Outdoor - Spor Ayakkabı - Havuz Terliği
cinsiyet
beden
renk
topuk boyu
fiyat
ek özellik
materyal
dış materyal
topuk tipi
sezon
desen
i̇ç astar & i̇ç taban materyali
sürdürülebilirlik detayı

Spor & Outdoor - Evde Spor Aletleri
cinsiyet
beden
fiyat
özellik
renk
ek hizmetler

Spor & Outdoor - Evde Spor Aletleri - Elastik Bant
fiyat
renk

Spor & Outdoor - Evde Spor Aletleri - El Yayı
fiyat
renk

Spor & Outdoor - Evde Spor Aletleri - Mat
fiyat
renk

Spor & Outdoor - Evde Spor Aletleri - Çalışma İstasyonları
fiyat
renk
garanti süresi

Spor & Outdoor - Evde Spor Aletleri - Atlama İpi
fiyat
özellik
renk

Spor & Outdoor - Evde Spor Aletleri - Boks Eldiveni
beden
fiyat
renk
özellik

Spor & Outdoor - Evde Spor Aletleri - Dambıl Seti
fiyat
renk

Spor & Outdoor - Evde Spor Aletleri - Eliptik Bisiklet
özellik
fiyat
renk

Spor & Outdoor - Evde Spor Aletleri - Barfiks Barı
fiyat
renk
ek hizmetler

Spor & Outdoor - Evde Spor Aletleri - Eldiven
fiyat
renk
özellik

Spor & Outdoor - Evde Spor Aletleri - Kettlebell
fiyat
renk
ek hizmetler

Spor & Outdoor - Evde Spor Aletleri - Kondisyon Bisikleti
fiyat
özellik
renk

Spor & Outdoor - Evde Spor Aletleri - Yürüme Bandı
taşıma kapasitesi
fiyat
hız aralığı
katlanabilme
özellik
renk
ek hizmetler

Spor & Outdoor - Evde Spor Aletleri - Pilates Topu
renk
pompa durumu
fiyat

Spor & Outdoor - Evde Spor Aletleri - Kürek Çekme Aleti
fiyat
özellik
renk
garanti süresi

Spor & Outdoor - Evde Spor Aletleri - Boks Bandajı
renk
fiyat

Spor & Outdoor - Evde Spor Aletleri - Crossfit
renk
fiyat

Spor & Outdoor - Spor Malzemeleri
cinsiyet
beden
fiyat
özellik
renk
ek hizmetler

Spor & Outdoor - Spor Malzemeleri - Deniz & Plaj
cinsiyet
yaş
fiyat
renk
çocuk cinsiyeti
pompa durumu

Spor & Outdoor - Spor Malzemeleri - Kaykay
fiyat
renk
özellik

Spor & Outdoor - Spor Malzemeleri - Paten
beden
fiyat
renk
özellik

Spor & Outdoor - Spor Malzemeleri - Kamp Malzemeleri
fiyat
renk
ek hizmetler

Spor & Outdoor - Spor Malzemeleri - Dağcılık & Tırmanış
fiyat
özellik
renk

Spor & Outdoor - Spor Malzemeleri - Aksiyon Kamera
fiyat
özellik
renk
ek hizmetler

Spor & Outdoor - Spor Malzemeleri - Çadır Uyku Tulumu
fiyat
model
renk

Spor & Outdoor - Spor Malzemeleri - Su Sporu Malzemeleri
cinsiyet
beden
fiyat
renk
ek hizmetler

Spor & Outdoor - Spor Malzemeleri - Dalış Malzemeleri
cinsiyet
fiyat
renk
ek hizmetler

Spor & Outdoor - Spor Malzemeleri - Balıkçılık Malzemeleri
fiyat
renk

Spor & Outdoor - Spor Malzemeleri - Tenis Malzemeleri
beden
renk
fiyat

Spor & Outdoor - Spor Malzemeleri - Kayak ve Snowboard
cinsiyet
beden
renk
fiyat
kumaş tipi

Spor & Outdoor - Spor Malzemeleri - Okçuluk
beden
fiyat
renk
özellik

Spor & Outdoor - Spor Malzemeleri - Çadır
kapasite
fiyat
mevsim
renk

Spor & Outdoor - Spor Malzemeleri - Havlu
boyut/ebat
renk
materyal
fiyat
havlu tipi
desen
parça sayısı
kutu durumu

Spor & Outdoor - Spor Malzemeleri - Suluk
fiyat
renk

Spor & Outdoor - Spor Malzemeleri - Matlar
fiyat
renk

Spor & Outdoor - Spor Malzemeleri - Bisiklet
cinsiyet
jant
fiyat
renk

Spor & Outdoor - Spor Malzemeleri - Termos
fiyat
materyal
renk

Spor & Outdoor - Spor Malzemeleri - Pilates Topları
renk
pompa durumu
fiyat

Spor & Outdoor - Bisiklet
cinsiyet
jant
fiyat
renk

Spor & Outdoor - Bisiklet - Çocuk Bisikletleri
yaş
fiyat
renk
tekerlek sayısı
özellik
model

Spor & Outdoor - Bisiklet - Elektrikli Bisikletler
fiyat
max. hız (km/h)
menzil
jant
taşıma kapasitesi
katlanabilme
renk
ek hizmetler

Spor & Outdoor - Bisiklet - Bisikletçi Ekipmanları
fiyat
özellik
renk

Spor & Outdoor - Bisiklet - Bisiklet Gözlükleri
renk
fiyat
özellik

Spor & Outdoor - Bisiklet - Bisiklet Kaskları
beden
fiyat
renk

Spor & Outdoor - Fitness Kondisyon
fiyat
renk
ek hizmetler

Spor & Outdoor - Fitness Kondisyon - Pilates Malzemeleri
fiyat
renk
pompa durumu

Spor & Outdoor - Fitness Kondisyon - Fitness Aletleri
renk
fiyat
özellik
ek hizmetler

Spor & Outdoor - Fitness Kondisyon - Kondisyon Bisikleti
fiyat
özellik
renk

Spor & Outdoor - Fitness Kondisyon - Koşu Bandı
taşıma kapasitesi
fiyat
hız aralığı
katlanabilme
özellik
renk
ek hizmetler

Spor & Outdoor - Fitness Kondisyon - Yoga Malzemeleri
renk
fiyat
açma / kapama

Spor & Outdoor - Fitness Kondisyon - Dambıl Seti
fiyat
renk

Spor & Outdoor - Fitness Kondisyon - Ağırlık Plakaları
fiyat
renk

Spor & Outdoor - Fitness Kondisyon - Barfiks
fiyat
renk
ek hizmetler

Spor & Outdoor - Sporcu Besinleri
gramaj
form
fiyat
aroma
servis

Spor & Outdoor - Sporcu Besinleri - Protein Tozu
gramaj
fiyat
aroma
servis

Spor & Outdoor - Sporcu Besinleri - Amino Asit
fiyat
form
aroma
paket i̇çeriği

Spor & Outdoor - Sporcu Besinleri - Karbonhidrat
fiyat
aroma

Spor & Outdoor - Sporcu Besinleri - L-Karnitin (CLA)
form
fiyat
aroma

Spor & Outdoor - Sporcu Besinleri - Güç ve Performans
form
fiyat
aroma

Spor & Outdoor - Sporcu Besinleri - Gıda Takviyesi & Vitaminler
çeşit
fiyat
form
aroma

Spor & Outdoor - Sporcu Besinleri - Kreatin
fiyat
aroma
form
tip

Spor & Outdoor - Sporcu Besinleri - Protein Bar
fiyat

Spor & Outdoor - Sporcu Besinleri - Shaker
materyal
hacim
fiyat
renk
"""


# Çocuk giyiminde "Tip" bez değil kıyafet tipi olmalı
BAGLAM_SECENEKLERI["bebek"]["tip"] = ("Günlük, Bayramlık, Okul, Spor, "
                                      "Ev Giyimi, Mevsimlik, Takım")

# =====================================================================
# 6) BAĞLAM TESPİTİ
#    Önce kategorinin kendi adına, bulunamazsa üst kategorilere bakılır.
#    SIRA ÖNEMLİ: yukarıdaki kural önce kazanır.
#    Başında "=" olan anahtarlar TAM KELİME olarak aranır.
# =====================================================================
BAGLAM_KURALLARI = [
    ("elektronik", ["vr gözlük"]),
    ("ayakkabi",  ["ayakkabı", "ayakkabi", "sneaker", "bot", "çizme",
                   "babet", "sandalet", "loafer", "krampon", "terlik",
                   "patik", "panduf", "postal", "bootie"]),
    ("canta",     ["çanta", "valiz", "bavul", "cüzdan", "kartlık",
                   "portföy"]),
    ("taki",      ["=takı", "kolye", "yüzük", "küpe", "bileklik",
                   "bilezik", "halhal", "piercing"]),
    ("bakim_aleti", ["saç düzleştirici", "saç maşası", "saç kurutma",
                     "tıraş makinesi", "epilasyon aletleri", "ipl",
                     "=tartı", "kişisel bakım aletleri", "fön makinesi"]),
    ("kucukev",   ["küçük ev aletleri", "süpürge", "=ütü", "kahve makinesi",
                   "çay makinesi", "blender", "tost makinesi", "doğrayıcı",
                   "rondo", "su ısıtıcı", "kettle", "mikser", "airfryer",
                   "fritöz"]),
    ("beyazesya", ["beyaz eşya", "buzdolabı", "çamaşır makinesi",
                   "bulaşık makinesi", "kurutma makinesi",
                   "derin dondurucu", "ankastre", "mikrodalga",
                   "aspiratör", "fırın", "=ocak", "davlumbaz"]),
    ("klima",     ["klima", "kombi", "ısıtıcılar", "vantilatör", "şofben",
                   "termosifon", "hava temizleyici", "hava nemlendirici",
                   "ıstıcılar"]),
    ("oyuncu",    ["oyuncu", "oyunculara özel", "playstation", "xbox",
                   "nintendo", "konsol", "gaming", "oyunları"]),
    ("tv",        ["=tv", "televizyon", "soundbar", "projeksiyon",
                   "hoparlör", "kulaklık", "uydu", "anten", "=lnb",
                   "media player", "hdmi", "priz", "adaptör",
                   "görüntü & ses"]),
    ("telefon",   ["telefon", "powerbank", "şarj cihaz", "kılıfları",
                   "kılıflar", "iphone", "android cep"]),
    ("foto",      ["=foto", "foto & kamera", "fotoğraf", "kamera", "lens",
                   "hafıza kartı", "şipşak"]),
    ("bilgisayar", ["bilgisayar", "tablet", "monitör", "klavye", "mouse",
                    "=ssd", "=ram", "ekran kartı", "yazıcı", "tarayıcı",
                    "modem", "laptop", "dizüstü", "bileşen",
                    "veri depolama"]),
    ("elektronik", ["elektronik", "giyilebilir", "akıllı", "drone",
                    "scooter", "dijital kod", "e-pin", "hediye kart",
                    "bluetooth"]),
    ("supermarket", ["süpermarket", "petshop", "kedi", "köpek", "kuş ",
                     "kuş ürünleri", "kuş yemleri", "akvaryum", "gıda",
                     "i̇çecek", "içecek", "atıştırmalık", "temizlik",
                     "deterjan", "yumuşatıcı", "tuvalet kağıdı",
                     "kağıt havlu", "çamaşır yıkama", "bulaşık yıkama",
                     "oda kokusu", "paspas & mop", "temizlik bezi",
                     "banyo temizleyiciler"]),
    ("bebek_urun", ["bebek bezi", "=bez", "biberon", "emzik", "mama",
                    "puset", "beşik", "park yatak", "ana kucağı",
                    "kanguru", "yürüteç", "oto koltuğu", "bebek arabası",
                    "portbebe", "salıncak", "cibinlik", "oyun parkı",
                    "sterilizatör", "göğüs pompası", "süt pompası",
                    "emzirme", "taşıma & güvenlik", "bebek odası",
                    "bebek bakım", "oyuncak", "alıştırma bardağı",
                    "buharlı pişirici", "bebek buhar", "oyun matları",
                    "bebek yatağı", "bebek nevresim", "bebek çantası",
                    "islak mendil"]),
    ("ic_giyim",  ["iç giyim", "iç çamaşırı", "sütyen", "külot", "çorap",
                   "pijama", "gecelik", "korse", "büstiyer", "bralet",
                   "kombinezon", "jartiyer", "atlet", "boxer", "içlik",
                   "fantezi giyim", "body", "zıbın"]),
    ("buyuk_beden", ["büyük beden"]),
    ("kitap",     ["kitap", "kırtasiye", "eğitim", "dergi", "gazete",
                   "roman", "=ofis", "=kalem", "sanatsal", "akademik",
                   "din ve mitoloji", "kişisel gelişim", "pazarlama",
                   "defter", "ajanda", "fotokopi", "dosya", "klasör",
                   "sınav", "ders", "sözlük", "tıp kitabı", "hukuk",
                   "mühendislik", "tarih", "manga", "boyama",
                   "yabancı dil"]),
    ("bebek",     ["bebek", "çocuk", "=anne", "yenidoğan",
                   "hastane çıkışı"]),
    ("kozmetik",  ["kozmetik", "kişisel bakım", "makyaj", "parfüm",
                   "cilt bakım", "cilt bakımı", "saç bakım", "saç bakımı",
                   "epilasyon", "deodorant", "=ruj", "eyeliner", "dudak",
                   "krem", "bakım", "tıraş", "hijyenik ped",
                   "cinsel sağlık", "duş jeli", "duş jelleri", "manikür",
                   "aydınlatıcı", "highlighter", "genel bakım", "şampuan",
                   "saç şekillendirici", "nemlendirici", "fondöten",
                   "maskara", "pudra", "allık", "oje", "peeling",
                   "tonik", "serum", "ağda", "sabun", "pamuk", "diş ",
                   "kolonya", "törpü", "cımbız", "kirpik", "tarak",
                   "toka", "saç boyası", "saç bant", "wax", "jöle",
                   "vücut", "güneş", "far paleti", "kontür",
                   "takma tırnak", "kaş makası", "kese", "banyo lifi",
                   "gıda takviye"]),
    ("otomobil",  ["otomobil", "motosiklet", "lastik", "=araç", "=oto",
                   "kask", "kolçak", "güneşlik"]),
    ("yapimarket", ["yapı market", "boya", "matkap", "vidalama",
                    "hırdavat", "ampul", "el aleti"]),
    ("hobi",      ["hobi", "parti", "müzik", "hediyelik", "çakmak",
                   "uzaktan kumandalı", "örgü", "boncuk", "nakış",
                   "balon", "yılbaşı", "düğün & kına", "led ışık",
                   "gitar", "piyano", "plak", "=org", "pikap",
                   "hediye sepeti", "puzzle", "satranç", "okey", "maket",
                   "oyun kartları"]),
    ("mutfak",    ["sofra", "mutfak", "tencere", "tava", "yemek takımı",
                   "kahvaltı takımı", "bardak", "tabak", "çatal",
                   "saklama kabı", "fincan", "düdüklü"]),
    ("ev",        ["ev & yaşam", "mobilya", "aydınlatma", "ev tekstili",
                   "dekorasyon", "ev gereçleri", "avize", "lambader",
                   "lamba", "nevresim", "yastık", "yorgan", "çarşaf",
                   "alez", "battaniye", "uyku seti", "koltuk", "halı",
                   "kilim", "perde", "seccade", "ayna", "tablo", "vazo",
                   "kırlent", "duvar saati", "dolap", "gardırop",
                   "şifonyer", "zigon", "sandalye", "yatak odası",
                   "salon", "çalışma odası", "yemek odası", "genç odası",
                   "bahçe mobilya", "oturma", "hurç", "düzenleyici",
                   "askı", "sepet", "banyo", "havlu", "bornoz",
                   "ütü masası", "organizer", "tezgah"]),
    ("spor",      ["spor", "outdoor", "fitness", "kamp", "dağcılık",
                   "kayak", "snowboard", "bisiklet", "uyku tulumu",
                   "=top", "forma", "tayt", "eşofman", "sporcu", "=mat",
                   "matlar", "dalış", "kaykay", "paten", "tenis",
                   "okçuluk", "çadır", "suluk", "termos", "dambıl",
                   "kettlebell", "barfiks", "pilates", "yoga", "boks",
                   "crossfit", "koşu bandı", "yürüme bandı", "kondisyon",
                   "eliptik", "atlama i̇pi", "elastik bant", "el yayı",
                   "ağırlık plaka", "kürek çekme", "deniz & plaj",
                   "balıkçılık", "protein", "amino", "kreatin",
                   "karbonhidrat", "shaker", "l-karnitin"]),
    ("aksesuar",  ["aksesuar", "kemer", "atkı", "bere", "eldiven",
                   "şapka", "=şal", "kravat", "boyunluk", "papyon",
                   "rozet", "saç aksesuar"]),
    ("saat",      ["saat"]),
    ("gozluk",    ["gözlük"]),
    ("giyim",     ["giyim", "elbise", "tişört", "t-shirt", "gömlek",
                   "pantolon", "ceket", "mont", "kaban", "palto", "etek",
                   "kazak", "hırka", "bluz", "sweatshirt", "trençkot",
                   "yağmurluk", "rüzgarlık", "şort", "yelek",
                   "takım elbise", "tesettür", "blazer", "polar",
                   "tulum"]),
]

# Alt bağlam -> üst bağlam (seçenek bulunamazsa üstte aranır)
BAGLAM_UST = {
    "beyazesya": "elektronik",
    "kucukev": "elektronik",
    "tv": "elektronik",
    "bilgisayar": "elektronik",
    "oyuncu": "bilgisayar",
    "bakim_aleti": "elektronik",
    "klima": "elektronik",
    "telefon": "elektronik",
    "foto": "elektronik",
    "mutfak": "ev",
    "taki": "aksesuar",
    "gozluk": "aksesuar",
    "saat": "aksesuar",
    "bebek_urun": "bebek",
}


def _eslesiyor(kelime, metin):
    if kelime.startswith("="):
        return re.search(r"(?<!\w)%s(?!\w)" % re.escape(kelime[1:]),
                         metin) is not None
    return kelime in metin


def baglam_bul(path):
    yol = [norm(p) for p in path]
    yaprak = yol[-1]
    # 1) Önce kategorinin kendi adı
    for ad, kelimeler in BAGLAM_KURALLARI:
        for k in kelimeler:
            if _eslesiyor(k, yaprak):
                return ad
    # 2) Sonra üst kategoriler (yapraktan köke doğru)
    for parca in reversed(yol[:-1]):
        for ad, kelimeler in BAGLAM_KURALLARI:
            for k in kelimeler:
                if _eslesiyor(k, parca):
                    return ad
    return "giyim"


def baglam_zinciri(path):
    """Örn: Oyuncu Klavyesi -> ['oyuncu', 'bilgisayar', 'elektronik']
    Çocuk kategorilerinde giyim bedeni '6-9 Ay' olsun diye başa
    'cocuk' eklenir."""
    b = baglam_bul(path)
    zincir = []
    while b and b not in zincir:
        zincir.append(b)
        b = BAGLAM_UST.get(b)

    yol_tam = " > ".join(norm(p) for p in path)
    cocuk_mu = ("çocuk" in yol_tam or "bebek" in yol_tam or
                "yenidoğan" in yol_tam)
    if cocuk_mu and zincir[0] in ("giyim", "ic_giyim", "aksesuar",
                                  "buyuk_beden", "spor"):
        zincir.insert(0, "cocuk")
    return zincir


# =====================================================================
# 7) FİLTRE TİPİ + SEÇENEK ÇÖZÜMLEYİCİ
# =====================================================================
ALIASLAR = {
    "boy / ölçü": "boy",
    "ürün özelliği": "özellik",
    "tipi": "tip",
    "ebatlar": "boyut/ebat",
    "maksimum taşıma kapasitesi": "taşıma kapasitesi",
    "ekran boyut (i̇nç)": "ekran boyutu (inç)",
    "ekran boyut (inç)": "ekran boyutu (inç)",
    "grafik i̇şlemcisi": "grafik işlemcisi",
    "ağırlık / hacim": "ağırlık / hacim",
}


def get_filtre_ozellikleri(isim, zincir):
    a = ALIASLAR.get(norm(isim), norm(isim))

    # 1) Evet / Hayır filtreleri
    if a in BOOLEAN_FILTRELER:
        return "boolean", None

    # 2) Bağlam zinciri (özelden genele)
    for b in zincir:
        ozel = BAGLAM_SECENEKLERI.get(b, {})
        if a in ozel:
            return "secim", kirp(ozel[a])

    # 3) Genel seçenekler
    if a in GENEL_SECENEKLER:
        return "secim", kirp(GENEL_SECENEKLER[a])

    # 4) Kestirilemeyenler serbest metin
    return "metin", None


# =====================================================================
# 8) RAW DATA -> KATEGORİ / FİLTRE SÖZLÜĞÜ
# =====================================================================
kategoriler_ve_filtreler = {}
current_category_path = None

for satir in raw_data.strip().split("\n"):
    satir = satir.strip()
    if not satir:
        continue

    # "1. Kadın" gibi ana başlık satırlarını atla
    if re.match(r"^\d+\.\s", satir):
        continue

    # ÖNEMLİ: " - " (boşluklu tire) ile bölünüyor.
    # split("-") kullanılsaydı "T-shirt" ve "E-Kitap Okuyucu" bozulurdu.
    if " - " in satir:
        current_category_path = tuple(x.strip() for x in satir.split(" - "))
        kategoriler_ve_filtreler.setdefault(current_category_path, [])
        continue

    # Fiyat sistemde zaten var, filtre olarak eklenmiyor
    if norm(satir) == "fiyat":
        continue

    if current_category_path:
        mevcut = kategoriler_ve_filtreler[current_category_path]
        if norm(satir) not in [norm(x) for x in mevcut]:
            mevcut.append(satir)


# =====================================================================
# 9) VERİTABANI İŞLEMLERİ
# =====================================================================
def find_category(path):
    """Türkçe karakter sorunlarına dayanıklı kategori bulucu."""
    cat = None
    for name in path:
        c = Category.objects.filter(name__iexact=name, parent=cat).first()
        if not c:
            hedef = norm(name)
            for aday in Category.objects.filter(parent=cat):
                if norm(aday.name) == hedef:
                    c = aday
                    break
        if not c:
            return None
        cat = c
    return cat


def get_inherited_attributes(cat):
    """Üst kategorilerde tanımlı filtreleri (miras) getirir."""
    attrs = set()
    current = cat.parent
    while current:
        for attr in CategoryAttribute.objects.filter(category=current):
            attrs.add(norm(attr.isim))
        current = current.parent
    return attrs


print("\n1. Adım: TÜM eski filtreler siliniyor...")
silinen = CategoryAttribute.objects.count()
CategoryAttribute.objects.all().delete()
print("   -> %s adet eski filtre temizlendi." % silinen)

print("\n2. Adım: Yeni filtreler bağlama göre analiz edilip ekleniyor...")
print("   (Listedeki kategori sayısı: %s)" % len(kategoriler_ve_filtreler))

eklenen = 0
esgecilen = 0
bulunamayan = []
metin_kalanlar = {}
tip_sayaci = {"secim": 0, "boolean": 0, "metin": 0}

# Üst kategoriler önce işlensin ki miras (inheritance) doğru çalışsın
sirali = sorted(kategoriler_ve_filtreler.items(), key=lambda x: len(x[0]))

for path, filters in sirali:
    cat = find_category(path)
    if not cat:
        bulunamayan.append(" > ".join(path))
        continue

    zincir = baglam_zinciri(path)
    inherited = get_inherited_attributes(cat)

    for f in filters:
        if norm(f) in inherited:
            esgecilen += 1
            continue

        tip, secenek = get_filtre_ozellikleri(f, zincir)
        CategoryAttribute.objects.update_or_create(
            category=cat,
            isim=baslik(f),
            defaults={
                "filtre_tipi": tip,
                "secenekler": secenek,
            },
        )
        eklenen += 1
        tip_sayaci[tip] = tip_sayaci.get(tip, 0) + 1
        if tip == "metin":
            metin_kalanlar.setdefault(norm(f), 0)
            metin_kalanlar[norm(f)] += 1


# =====================================================================
# 10) RAPOR
# =====================================================================
print("\n" + "=" * 62)
print(" İŞLEM TAMAMLANDI")
print("=" * 62)
print(" Eklenen filtre           : %s" % eklenen)
print(" Mirastan engellenen      : %s" % esgecilen)
print("-" * 62)
print(" Seçimli (dropdown)       : %s" % tip_sayaci.get("secim", 0))
print(" Evet/Hayır (boolean)     : %s" % tip_sayaci.get("boolean", 0))
print(" Serbest metin            : %s" % tip_sayaci.get("metin", 0))
print("=" * 62)

if bulunamayan:
    print("\n! Veritabanında BULUNAMAYAN kategoriler (%s adet):"
          % len(bulunamayan))
    for b in bulunamayan[:60]:
        print("   - %s" % b)
    if len(bulunamayan) > 60:
        print("   ... ve %s tane daha" % (len(bulunamayan) - 60))
    print("  (Önce bu kategorileri oluşturup scripti tekrar çalıştır.)")

if metin_kalanlar:
    print("\n! Serbest METİN kalan filtreler (marka/model/ölçü gibi")
    print("  sonsuz değerli alanlar burada normaldir):")
    for ad, adet in sorted(metin_kalanlar.items(), key=lambda x: -x[1]):
        print("   - %-40s (%s kategoride)" % (ad, adet))

print("\nBitti.\n")
exit()