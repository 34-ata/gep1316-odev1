# -*- coding: utf-8 -*-
"""GEP1316 - Küçük üretim atölyesi için ürün maliyeti ve satış fiyatı hesaplayıcı.

Program bir menü üzerinden çalışır: ürün ekler, eklenen ürünleri listeler
ve raporu CSV dosyasına kaydeder. Sadece Python standart kütüphanesi kullanılır.
"""

import csv
import math


def menu_goster():
    """Menü seçeneklerini ekrana yazar."""
    print()
    print("===== ÜRÜN MALİYET HESAPLAYICI =====")
    print("1 - Ürün ekle")
    print("2 - Ürünleri listele")
    print("3 - Raporu CSV'ye kaydet")
    print("4 - Çıkış")


def metin_al(mesaj):
    """Boş olmayan bir metin girilene kadar sorar ve girilen metni döndürür."""
    while True:
        girdi = input(mesaj)
        girdi = girdi.strip()          # baştaki ve sondaki boşlukları siler
        if girdi == "":
            print("UYARI: Boş bırakılamaz, lütfen tekrar girin.")
        else:
            return girdi


def sayi_al(mesaj, sifir_olabilir):
    """Geçerli ve negatif olmayan bir sayı girilene kadar sorar, sayıyı döndürür.

    sifir_olabilir True ise 0 kabul edilir (kâr oranı için), False ise reddedilir.
    Virgüllü girdi (3,5) noktaya çevrilir. Hatalı girdide program çökmez, tekrar sorar.
    """
    while True:
        girdi = input(mesaj)
        girdi = girdi.strip().replace(",", ".")    # 3,5 yazımını 3.5 yapar
        try:
            sayi = float(girdi)                    # metni sayıya çevirmeyi dener
        except ValueError:                         # çevrilemezse hata yakalanır
            print("UYARI: Lütfen bir sayı girin (örnek: 150 veya 3,5).")
            continue                               # döngü başına dönüp tekrar sorar
        if not math.isfinite(sayi):                # "nan", "inf", "1e400" gibi girdiler
            print("UYARI: Geçerli bir sayı girin.")
            continue
        if sayi < 0:
            print("UYARI: Negatif değer girilemez.")
            continue
        if sayi == 0 and not sifir_olabilir:
            print("UYARI: Bu değer sıfırdan büyük olmalı.")
            continue
        return sayi                                # değer geçerli, döngüden çıkılır


def iscilik_maliyeti_hesapla(sure, saatlik_ucret):
    """İşçilik maliyetini hesaplar: süre (saat) x saatlik ücret (TL)."""
    return sure * saatlik_ucret


def toplam_maliyet_hesapla(hammadde, iscilik):
    """Toplam maliyeti hesaplar: hammadde maliyeti + işçilik maliyeti."""
    return hammadde + iscilik


def satis_fiyati_hesapla(toplam_maliyet, kar_orani):
    """Satış fiyatını hesaplar: maliyetin üzerine kâr oranı (%) eklenir."""
    return toplam_maliyet * (1 + kar_orani / 100)


def gercek_marj_hesapla(kar, satis_fiyati):
    """Gerçek kâr marjını (%) hesaplar: kârın satış fiyatına oranı."""
    if satis_fiyati == 0:              # sıfıra bölme hatasını önler
        return 0.0
    return kar / satis_fiyati * 100


def kar_orani_degerlendir(kar_orani):
    """Girilen kâr oranını yorumlayan kısa bir değerlendirme metni döndürür."""
    if kar_orani < 10:
        return "Düşük – maliyet artışında zarar riski"
    elif kar_orani <= 40:
        return "Normal"
    else:
        return "Yüksek – rekabet açısından kontrol edin"


def sayi_bicimle(sayi):
    """Sayıyı Türkçe Excel biçiminde metne çevirir: iki ondalık, ayırıcı virgül."""
    return f"{sayi:.2f}".replace(".", ",")         # 437.50 -> "437,50"


def urun_bilgisi_al():
    """Ürün bilgilerini kullanıcıdan alır, hesaplamaları yapar ve ürün sözlüğünü döndürür."""
    print()
    print("--- Yeni Ürün ---")
    ad = metin_al("Ürün adı: ")
    hammadde = sayi_al("Hammadde maliyeti (TL): ", False)
    sure = sayi_al("İşçilik süresi (saat): ", False)
    ucret = sayi_al("Saatlik işçilik ücreti (TL): ", False)
    kar_orani = sayi_al("Maliyet üzerine kâr oranı (%): ", True)

    # Hesaplamalar ayrı fonksiyonlarda yapılır, sonuçlar burada toplanır
    iscilik = iscilik_maliyeti_hesapla(sure, ucret)
    toplam_maliyet = toplam_maliyet_hesapla(hammadde, iscilik)
    satis_fiyati = satis_fiyati_hesapla(toplam_maliyet, kar_orani)
    kar = satis_fiyati - toplam_maliyet
    gercek_marj = gercek_marj_hesapla(kar, satis_fiyati)

    # Bir ürünün bütün bilgileri tek bir sözlükte tutulur
    urun = {
        "ad": ad,
        "hammadde": hammadde,
        "sure": sure,
        "ucret": ucret,
        "kar_orani": kar_orani,
        "iscilik": iscilik,
        "toplam_maliyet": toplam_maliyet,
        "satis_fiyati": satis_fiyati,
        "kar": kar,
        "gercek_marj": gercek_marj,
    }
    return urun


def urun_ekle(urunler):
    """Yeni ürünü listeye ekler ve özet bilgi ile değerlendirmeyi ekrana yazar."""
    urun = urun_bilgisi_al()
    urunler.append(urun)                           # sözlük listenin sonuna eklenir

    print()
    print("Ürün eklendi:", urun["ad"])
    print(f"  İşçilik maliyeti : {urun['iscilik']:.2f} TL")
    print(f"  Toplam maliyet   : {urun['toplam_maliyet']:.2f} TL")
    print(f"  Satış fiyatı     : {urun['satis_fiyati']:.2f} TL")
    print(f"  Kâr              : {urun['kar']:.2f} TL")
    print(f"  Gerçek kâr marjı : {urun['gercek_marj']:.2f} %")
    print("  Değerlendirme    :", kar_orani_degerlendir(urun["kar_orani"]))


def urunleri_listele(urunler):
    """Kayıtlı ürünleri tablo biçiminde ekrana yazar; liste boşsa uyarı verir."""
    if len(urunler) == 0:
        print("Kayıtlı ürün yok. Önce 1 numaralı seçenekle ürün ekleyin.")
        return

    print()
    print("No  Ürün                 Maliyet(TL)  Fiyat(TL)   Kâr(TL)  Kâr Oranı(%)  Gerçek Marj(%)")
    print("-" * 92)
    sira = 1                                       # satır numarası sayacı
    for urun in urunler:
        print(f"{sira:<3} {urun['ad']:<20} {urun['toplam_maliyet']:>11.2f} "
              f"{urun['satis_fiyati']:>10.2f} {urun['kar']:>9.2f} "
              f"{urun['kar_orani']:>13.2f} {urun['gercek_marj']:>15.2f}")
        sira = sira + 1
    print("-" * 92)
    print("Toplam ürün sayısı:", len(urunler))


def csv_kaydet(urunler, dosya_adi):
    """Ürün raporunu CSV dosyasına yazar; başarılıysa True, hata olursa False döndürür."""
    if not dosya_adi.lower().endswith(".csv"):     # uzantı yazılmamışsa eklenir
        dosya_adi = dosya_adi + ".csv"

    try:
        # utf-8-sig: Excel Türkçe karakterleri doğru okur, delimiter=";" sütunları ayırır
        with open(dosya_adi, "w", newline="", encoding="utf-8-sig") as dosya:
            yazici = csv.writer(dosya, delimiter=";")
            yazici.writerow(["Ürün Adı", "Hammadde (TL)", "İşçilik Süresi (saat)",
                             "Saatlik Ücret (TL)", "Kâr Oranı (%)", "İşçilik Maliyeti (TL)",
                             "Toplam Maliyet (TL)", "Satış Fiyatı (TL)", "Kâr (TL)",
                             "Gerçek Marj (%)"])
            for urun in urunler:
                yazici.writerow([urun["ad"],
                                 sayi_bicimle(urun["hammadde"]),
                                 sayi_bicimle(urun["sure"]),
                                 sayi_bicimle(urun["ucret"]),
                                 sayi_bicimle(urun["kar_orani"]),
                                 sayi_bicimle(urun["iscilik"]),
                                 sayi_bicimle(urun["toplam_maliyet"]),
                                 sayi_bicimle(urun["satis_fiyati"]),
                                 sayi_bicimle(urun["kar"]),
                                 sayi_bicimle(urun["gercek_marj"])])
    except OSError:                                # dosya açılamaz/yazılamazsa
        return False
    print("Rapor kaydedildi:", dosya_adi)
    return True


def main():
    """Ürün listesini oluşturur ve menü döngüsünü çalıştırır."""
    urunler = []                                   # tüm ürünler bu listede tutulur

    while True:
        menu_goster()
        secim = input("Seçiminiz (1-4): ").strip()

        if secim == "1":
            urun_ekle(urunler)
        elif secim == "2":
            urunleri_listele(urunler)
        elif secim == "3":
            if len(urunler) == 0:
                print("Kaydedilecek veri yok. Önce ürün ekleyin.")
            else:
                dosya_adi = input("Dosya adı (boş bırakırsanız rapor.csv): ").strip()
                if dosya_adi == "":
                    dosya_adi = "rapor.csv"
                basarili = csv_kaydet(urunler, dosya_adi)
                if not basarili:
                    print("UYARI: Dosya yazılamadı. Dosya adını veya klasör iznini kontrol edin.")
        elif secim == "4":
            print("Programdan çıkılıyor. İyi çalışmalar!")
            break                                  # while döngüsü sona erer
        else:
            print("UYARI: Geçersiz seçim, 1 ile 4 arasında bir sayı girin.")


# Dosya doğrudan çalıştırıldığında programı başlat
main()
