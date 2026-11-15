# GEP1316 – Test Senaryoları

Test edilen program: `maliyet_hesaplayici.py`
Çalıştırma: `python3 maliyet_hesaplayici.py`
Test tarihi: 15.11.2026 · Testler tek bir oturumda, elle çalıştırılmıştır.
Kanıt: `ekran_goruntuleri/03_test_1.png`, `04_test_2.png`, `05_test_3.png`, `06_csv_excel.png`

| No | Senaryo | Girdi | Beklenen sonuç | Gerçek sonuç | Durum |
|----|---------|-------|----------------|--------------|-------|
| 1 | Normal ürün ekleme | `Ahşap tabure`, `150`, `2,5`, `80`, `25` | İşçilik 200,00 · Maliyet 350,00 · Fiyat 437,50 · Kâr 87,50 · Marj %20,00 · "Normal" | Tüm değerler beklenenle aynı | GEÇTİ |
| 2 | Virgüllü ondalık girdi | `Vida seti`, `150,75`, `1,5`, `80,50`, `12,5` | Girdiler kabul edilir · İşçilik 120,75 · Maliyet 271,50 · Fiyat 305,44 · Kâr 33,94 · Marj %11,11 · "Normal" | Girdilerin tamamı kabul edildi, değerler beklenenle aynı | GEÇTİ |
| 3 | Sayı yerine harf (hatalı) | Hammadde: `abc` | "Lütfen bir sayı girin" uyarısı, çökme yok, soru tekrar sorulur | Uyarı verildi, soru tekrar soruldu | GEÇTİ |
| 4 | Negatif sayı (hatalı) | Hammadde: `-5` | "Negatif değer girilemez" uyarısı, soru tekrar sorulur | Uyarı verildi, soru tekrar soruldu | GEÇTİ |
| 5 | Hammaddeye 0 (uç) | Hammadde: `0` | "Bu değer sıfırdan büyük olmalı" uyarısı | Uyarı verildi, soru tekrar soruldu | GEÇTİ |
| 6 | Kâr oranına 0 (sınır değer) | `Maliyetine satış`, `150`, `2,5`, `80`, `0` | 0 kabul edilir · Fiyat 350,00 · Kâr 0,00 · Marj %0,00 · "Düşük – maliyet artışında zarar riski" | Uyarı olmadan kabul edildi, değerler ve değerlendirme beklenenle aynı | GEÇTİ |
| 7 | Sonlu olmayan sayı (uç) | Hammadde: `nan`, `inf`, `1e400` | Üçü de "Geçerli bir sayı girin" uyarısıyla reddedilir | Üçü de reddedildi | GEÇTİ |
| 8 | Boş ürün adı (hatalı) | Ürün adı: (boş Enter) | "Boş bırakılamaz" uyarısı, ad tekrar sorulur | Uyarı verildi, ad tekrar soruldu | GEÇTİ |
| 9 | Menüde geçersiz seçim (hatalı) | Menü: `7`, `abc`, sonra `4` | İkisinde de "Geçersiz seçim" uyarısı, menü yeniden gösterilir · `4` ile düzgün çıkış | İki uyarı da verildi, `4` ile program düzgün kapandı | GEÇTİ |
| 10 | Ürün yokken listeleme/kaydetme (uç) | Program açılınca `2`, sonra `3` | "Kayıtlı ürün yok" · "Kaydedilecek veri yok", dosya adı sorulmaz | İki mesaj da verildi, dosya adı sorulmadı | GEÇTİ |

**Ek kontrol – CSV çıktısı:** 3 ürünle kaydedilen `rapor.csv` Excel'de açıldı. Her bilgi ayrı sütunda, Türkçe karakterler doğru, sayılar sayı olarak tanındı (`06_csv_excel.png`).

**Sonuç:** 10 testin 10'u geçti (7'si hatalı/uç girdi).

## En zor hata

**Belirti:** Hammadde maliyetine `nan` girildiğinde program çökmedi ama maliyet, satış fiyatı, kâr ve marj "nan" çıktı ve bu değerler CSV'ye de yazıldı (`01_nan_hatasi.png`).

**Neden zordu:** Program çökmediği ve hata mesajı vermediği için fark edilmesi zordu. YZ de hatalı girdileri test ettiğini söylemişti, ama yalnızca `abc`, `-5` ve `0` girdilerini denemişti.

**Kök neden:** Python'un `float()` fonksiyonu `"nan"` ve `"inf"` metinlerini hata vermeden sayıya çeviriyor, `1e400` gibi çok büyük bir sayı da `inf`'e dönüşüyor. Ayrıca `nan < 0` karşılaştırması her zaman False döndüğü için `nan` değeri negatiflik kontrolünden de geçiyordu.

**Çözüm:** `sayi_al()` fonksiyonuna, sayıya çevirmenin hemen ardından ve negatiflik kontrolünden önce `math.isfinite()` kontrolü eklendi. Test 7 bu düzeltmenin kalıcı olduğunu doğruluyor (`02_nan_duzeltildi.png`).