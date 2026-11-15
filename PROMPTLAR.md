# YZ ile Çalışma Günlüğü

Araç: Claude (Anthropic), VS Code eklentisi üzerinden
Tarih: 15.11.2026

---

## Prompt 1 – Tasarım (sözde kod, akış şeması, fonksiyonlar)

**Prompt:**
> GEP1316 dersi için bir komut satırı Python uygulaması yazacağım: küçük bir
üretim atölyesi için ürün maliyeti ve satış fiyatı hesaplayıcı.

Kurallar:
- Sadece Python standart kütüphanesi kullan.
- Kod başlangıç seviyesinde ve okunabilir olsun; sözlü sınavda her satırı
  açıklayacağım, o yüzden gereksiz ileri teknik (class, lambda, list
  comprehension zinciri) kullanma.
- Yorumlar Türkçe olsun.

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