# YZ ile Çalışma Günlüğü

Araç: Claude (Anthropic), VS Code eklentisi üzerinden
Tarih: 15.11.2026

---

## Prompt 1 – Tasarım (sözde kod, akış şeması, fonksiyonlar)

**Prompt:**
> GEP1316 dersi için bir komut satırı Python uygulaması yazacağım: küçük bir
> üretim atölyesi için ürün maliyeti ve satış fiyatı hesaplayıcı.
>
> Kurallar:
> - Sadece Python standart kütüphanesi kullan.
> - Kod başlangıç seviyesinde ve okunabilir olsun; sözlü sınavda her satırı
>   açıklayacağım, o yüzden gereksiz ileri teknik (class, lambda, list
>   comprehension zinciri) kullanma.
> - Yorumlar Türkçe olsun.

Şimdilik kod yazma. Önce şunları ver:
1. Programın sözde kodu (pseudocode)
2. Bir akış şeması (Mermaid formatında)
3. Fonksiyon listesi: her fonksiyonun adı, ne aldığı, ne döndürdüğü
4. Verinin nasıl tutulacağı (liste/sözlük yapısı)

Girdiler: ürün adı, hammadde maliyeti (TL), işçilik süresi (saat),
saatlik işçilik ücreti (TL), kâr marjı (%).
Menü: ürün ekle, ürünleri listele, raporu CSV'ye kaydet, çıkış.
Hatalı girdide program çökmemeli, uyarı verip tekrar sormalı.

**YZ'nin yanıtı (özet):**
Sözde kod, Mermaid akış şeması, 11 fonksiyonluk bir liste ve sözlüklerden
oluşan bir liste yapısı önerdi. Hatalı girdiye karşı try/except içeren bir
döngü kurdu; virgüllü sayı girişini ve utf-8-sig kodlamasını kendisi önerdi.

**Kararım:** Kısmen kabul

**Gerekçe:**
- Kabul ettiklerim: Fonksiyonlara bölme ve sözlük yapısı okunabilir, her
  formül tek bir yerde duruyor.
- YZ hatası: "Kâr marjı" adı altında aslında maliyet üzerine kâr oranı
  (markup) formülü kullanılmış. %25 girildiğinde gerçek marj
  87,5 / 437,5 = %20 çıkıyor; kullanıcı yanlış bilgilendirilmiş olur.
  Girdinin adını "maliyet üzerine kâr oranı" yaptırdım ve gerçek marjı
  ayrı bir sütun olarak ekletim.
- Eksik: Kâr oranını değerlendiren bir karar yapısı yoktu
  (düşük/normal/yüksek uyarısı); ekletim.
- Eksik: Virgülle ayrılmış CSV, Türkçe ayarlı Excel'de tek sütuna
  yığılıyor; ";" ayırıcı ve virgüllü ondalık istedim.


  ---

## Prompt 2 – Düzeltmelerle kodu yazdırma

**Prompt:**
> Tasarım genel olarak uygun, şu düzeltmelerle kodu yaz:

1. Kavram hatası: "kâr marjı" dediğin şey aslında maliyet üzerine kâr oranı
   (markup). %25 girince gerçek marj %20 çıkıyor (87.5 / 437.5). Formülü koru
   ama girdinin adını "Maliyet üzerine kâr oranı (%)" yap, sözlük anahtarı
   "kar_orani" olsun. Listede ve CSV'de ayrıca gerçek kâr marjını
   (kar / satis_fiyati * 100) "gercek_marj" olarak göster.
2. Kâr oranı için bir değerlendirme fonksiyonu ekle (if/elif/else):
   %10 altı "Düşük – maliyet artışında zarar riski", %10–40 "Normal",
   %40 üstü "Yüksek – rekabet açısından kontrol edin". Ürün eklenince
   bu mesaj ekrana yazılsın.
3. CSV: encoding="utf-8-sig", delimiter=";" kullan ve sayıları Türkçe
   Excel'in okuyacağı biçimde yaz (2 ondalık, ondalık ayırıcı virgül,
   örn. 437,50). Kullanıcı dosya adını ".csv" olmadan yazarsa uzantıyı ekle.
4. Virgüllü girdi (3,5) kabul edilsin.

Tek dosya: maliyet_hesaplayici.py. Her fonksiyonun başına ne yaptığını
anlatan kısa bir Türkçe docstring koy. Tasarımda olmayan ekstra özellik ekleme.

Ayrıca az önceki sözde kodu ve Mermaid akış şemasını, bu düzeltmeleri
yansıtacak şekilde TASARIM.md dosyasına kaydet.

**YZ'nin yanıtı (özet):**
maliyet_hesaplayici.py'yi (14 fonksiyon, yalnızca csv modülü) ve
TASARIM.md'yi oluşturdu. İstediğim 4 düzeltmenin hepsini uyguladı:
kar_orani adı, gerçek marj sütunu, kâr oranı değerlendirmesi, Türkçe
Excel uyumlu CSV.

**Kararım:** Kabul

**Gerekçe:**
- Programı kendim çalıştırdım; menü, ürün ekleme ve listeleme çalışıyor.
- YZ, değerlendirme metnini CSV'ye sütun olarak eklemedi. Gerekçesi:
  CSV yalnızca ürün verisini tutmalı, değerlendirme türetilmiş bir yorum.
  Bu gerekçeyi uygun buldum ve kabul ettim.
- Kendi testlerimde bu sürümde bir hata buldum (bkz. Prompt 3).


---

## Prompt 3 – Kendi testimde bulduğum hatanın düzeltilmesi

**Prompt:**
> Test ederken bir hata buldum: sayi_al() fonksiyonu "nan", "inf" ve "1e400"
gibi girdileri kabul ediyor, çünkü float() bunları hata vermeden çeviriyor.
Hammaddeye nan girince maliyet, fiyat ve kâr "nan" çıkıyor ve CSV'ye de
öyle yazılıyor. Hatalı girdiyi test ettiğini söylemiştin ama bu durumu
denememişsin.

Düzeltmeler:
1. sayi_al() içinde math.isfinite() ile sonlu olmayan sayıları reddet,
   "UYARI: Geçerli bir sayı girin." mesajı versin ve tekrar sorsun.
2. csv_kaydet() içinde open/close yerine "with open(...) as dosya:" kullan.

Başka bir şeyi değiştirme. Yaptığın değişikliği satır numarasıyla göster.

**YZ'nin yanıtı (özet):**
Hatayı kabul etti. sayi_al() içine math.isfinite() kontrolü ekledi ve
bu kontrolü negatiflik testinden önceye koydu, çünkü nan < 0 her zaman
False döndüğü için nan eski sırada bütün kontrollerden geçiyordu.
csv_kaydet() fonksiyonunu with open yapısına çevirdi.

**Kararım:** Kabul (düzeltmeyi kendim test ettikten sonra)

**Gerekçe:**
- YZ hatası: Claude hatalı girdileri test ettiğini söylemişti, ama yalnızca
  abc, -5 ve 0 girdilerini denemişti. Ben hammaddeye "nan" girdiğimde
  program çökmedi, ama maliyet, fiyat ve kâr "nan" çıktı
  (ekran_goruntuleri/01_nan_hatasi.png). Sebebi, float() fonksiyonunun
  "nan" ve "inf" metinlerini geçerli sayı olarak kabul etmesi.
- Düzeltmeden sonra nan, inf ve 1e400 girdilerinin üçü de uyarı verip
  tekrar soruyor, geçerli girdide sonuçlar doğru
  (ekran_goruntuleri/02_nan_duzeltildi.png).
- Çıkardığım ders: YZ'nin "test ettim" demesi yeterli değil, uç
  durumları kendim denemem gerekiyor.


  ---

## Prompt 4 – Tasarım belgesini koda uyumlu hale getirme

**Prompt:**
> Evet, TASARIM.md'deki sayi_al sözde koduna ve gerekiyorsa akış şemasına
> sonlu sayı (nan/inf) kontrolünü ekle. Kodda başka bir şeyi değiştirme.

**YZ'nin yanıtı (özet):**
Sözde koda sonlu sayı kontrolünü ekledi ve bu kontrolün neden negatiflik
testinden önce gelmesi gerektiğini yorum olarak yazdı. Akış şemasında yeni
bir dal açmadı; yalnızca "Girdi geçerli mi?" kutusunun tanımını genişletti.
Fonksiyon tablosunu da güncelledi.

**Kararım:** Kabul

**Gerekçe:**
- Tasarım belgesi koddan geri kalırsa rapordaki akış şeması gerçek programı
  yansıtmaz; ikisinin tutarlı olması gerekiyordu.
- Akış şemasına yeni dal eklememesini doğru buldum: hatalı girdi döngüsü
  zaten mevcuttu, yeni bir dal şemayı gereksiz yere karmaşıklaştırırdı.
- git diff ile yalnızca TASARIM.md'nin değiştiğini, koda dokunulmadığını
  kontrol ettim.


  ---

## Prompt 5 – Test senaryolarının hazırlanması

**Prompt:**
> TESTLER.md dosyası oluştur. İçinde şu sütunlardan oluşan bir test tablosu olsun:
No | Senaryo | Girdi | Beklenen sonuç | Gerçek sonuç | Durum

10 senaryo yaz, en az 5'i hatalı veya uç girdi olsun. Şunları mutlaka kapsa:
- Normal ürün (150 / 2,5 / 80 / 25) ve beklenen hesap sonuçları
- Virgüllü ondalık girdi
- Harf girdisi (abc)
- Negatif sayı
- Hammaddeye 0
- Kâr oranına 0 (kabul edilmeli, değerlendirme "Düşük")
- nan / inf
- Boş ürün adı
- Menüde geçersiz seçim (örn. 7)
- Ürün yokken listeleme ve CSV kaydetme

"Gerçek sonuç" ve "Durum" sütunlarını BOŞ bırak; testleri ben çalıştırıp
dolduracağım. Testleri kendin çalıştırma. Tablonun altına "En zor hata"
başlığıyla boş bir bölüm ekle.

**YZ'nin yanıtı (özet):**
TESTLER.md dosyasında 10 senaryo hazırladı: 1 normal, 1 sınır değer
(kâr oranı 0), 1 biçim (virgüllü ondalık), 7 hatalı/uç girdi. "Gerçek
sonuç" sütununu istediğim gibi boş bıraktı. Ekranda yuvarlama nedeniyle
1 kuruşluk fark olabileceğini ve ekranda ondalık ayırıcının nokta, CSV'de
virgül olduğunu belirtti.

**Kararım:** Kabul

**Gerekçe:**
- Senaryoları ve beklenen sonuçları YZ'ye yazdırdım ama testleri kendisine
  çalıştırtmadım. Prompt 3'teki deneyimden sonra doğrulamayı kendim
  yapmaya karar verdim.
- Beklenen hesap sonuçlarını elle kontrol ettim
  (271,50 × 1,125 = 305,4375 → ekranda 305,44).