# T-Sharp (T#) Programlama Dili ve TCompile Ekosistemi

![Lisans](https://img.shields.io/badge/Lisans-GNU_AGPL_v3-red.svg)
![Sürüm](https://img.shields.io/badge/Sürüm-v4.1-blue.svg)
![Statü](https://img.shields.io/badge/Proje-Solo_Açık_Kaynak-green.svg)
![Derleyici](https://img.shields.io/badge/Derleyici-PyInstaller_Tabanlı-yellow.svg)

---

## 🚀 Proje Hakkında

T-Sharp (T#) v4.1, çocukların ve yazılıma yeni başlayan bireylerin, algoritmik düşünme becerilerini kendi ana dillerinde en üst seviyede geliştirebilmeleri için tasarlanmış; yüksek seviyeli, nesne yönelimli mantığa sahip ve tam kapsamlı bir derleyici (compiler) ekosistemidir. 

Bu proje, kod yazmayı bir dil ezberleme sürecinden çıkarıp, tamamen bir problem çözme ve mantık kurma disiplinine dönüştürmeyi hedefler. v4.1 sürümü ile gelen gelişmiş kütüphane desteği sayesinde sadece terminal üzerinde değil; görsel arayüzler, oyunlar ve gelişmiş ağ uygulamaları dünyasında da tam yetki sağlar.

---

## 1. Eğitim Felsefesi ve Stratejik Vizyon

Teknolojinin temelini anlamak, komutların arkasındaki mantığı kavramaktan geçer. T-Sharp, bilişsel yükü azaltarak öğrencinin zihnini serbest bırakır.

### Mantıksal Soyutlama ve Dil Uyumu
Geleneksel dillerdeki İngilizce terim karmaşası, başlangıç seviyesindeki bir zihnin "mantık" yerine "söz dizimi" (syntax) hatalarına odaklanmasına neden olur. T-Sharp, bu bariyeri Türkçe komut seti ile yıkar. Bir birey "if" yerine "eğer", "loop" yerine "döngü" yazdığında, kurduğu cümle ile bilgisayara verdiği talimat arasında doğrudan bir bağ kurar. Bu bağ, kalıcı öğrenmenin temelidir.

### Solo Geliştirme ve Açık Kaynak Ruhu
Bu proje, tek bir geliştiricinin vizyonuyla inşa edilmiş olsa da, toplumsal bir teknoloji üretim bilinci oluşturmayı hedefler. Açık kaynak kodlu yapısı, her aşamanın şeffaf bir şekilde incelenmesine ve geliştirilmesine olanak tanır. v4.1 sürümü, solo geliştirici deneyimini profesyonel standartlara taşıyan en kararlı yapıdır.

---

## 2. Teknik Mimari ve Çekirdek Yapı

T-Sharp, arka planda hibrit bir çalışma prensibi benimseyen, oldukça karmaşık bir yorumlayıcı (interpreter) katmanına sahiptir.

### Komut Analiz ve Normalizasyon Sistemi
Sistemin çekirdeği olan TSharp sınıfı, her satırı titizlikle analiz eden bir sözcük tarayıcıya sahiptir. "normalize_satir" modülü sayesinde, Türkçe karakter hassasiyeti (ı, i, ğ, ü, ş, ö) bir engel olmaktan çıkarılır. Düzenli ifadeler (Regular Expressions) ile desteklenen bu yapı, karmaşık matematiksel formülleri ve mantıksal ifadeleri gerçek zamanlı olarak çözümleyerek işlem sırasına koyar.

### Dinamik Bellek Yönetimi
T-Sharp, kullanıcıyı tür tanımlama zorunluluğundan kurtarır. Dinamik bir bellek sözlüğü kullanarak değişkenleri, listeleri ve fonksiyonları çalışma zamanında (runtime) otomatik olarak haritalandırır. Bu, esnek bir geliştirme ortamı sağlarken, arka planda bellek güvenliğini koruyan bir izolasyon katmanı oluşturur.

---

## 3. TCompile: PyInstaller Tabanlı Derleme Teknolojisi

T-Sharp v4.1, yazdığınız Türkçe kodları bağımsız çalışabilir dosyalara dönüştüren profesyonel **TCompile** modülünü içerir. 

### TCompile Mimari Yapısı
TCompile, bir dilden diğerine dönüşüm yapan (transpiler) ve ardından bu kodu ikili formata getiren (compiler) hibrit bir yapıdadır:
1. **Analiz ve Tercüme:** Yazılan T-Sharp kodu (.tsharp), TCompile tarafından taranarak optimize edilmiş Python koduna dönüştürülür.
2. **PyInstaller Entegrasyonu:** TCompile, arka planda **PyInstaller** motorunu kullanarak dönüştürülen bu kodu paketler. PyInstaller'ın sunduğu "one-file" (tek dosya) ve "windowed" (arayüz modu) özelliklerini otomatik olarak yapılandırır.
3. **Bağımsız Dağıtım:** Bu süreç sonunda, projeniz tüm bağımlılıkları (PySide6, Pygame, Requests vb.) içerisinde barındıran tek bir .exe (Windows) veya ELF (Linux) dosyasına dönüşür. 

**TCompile**, kullanıcının sisteminde hiçbir altyapı veya Python kurulumu olmasa bile, Türkçe kodla yazılmış bir yazılımın her bilgisayarda çalışmasını garanti altına alır.

---

## 4. Entegre Kütüphaneler ve Görsel Sistemler

v4.1 sürümü, modern yazılım dünyasının tüm gereksinimlerini karşılayan gelişmiş alt modüllerle donatılmıştır.

### Görsel Arayüz (GUI) ve Form Yönetimi
* **Standart GUI (Tkinter):** Hızlı araçlar, basit butonlar ve veri giriş pencereleri için optimize edilmiştir.
* **Profesyonel GUI (PySide6 / Qt6):** Modern, şık ve çok fonksiyonlu masaüstü uygulamaları tasarlamak için kullanılır. Sekmeli yapılar, veri tabloları ve karmaşık yerleşim planları tamamen Türkçe komutlarla yönetilir.

### Ağ Üzerinden Görsel Çekme ve İşleme
T-Sharp, internet üzerindeki kaynaklara erişimi bir üst seviyeye taşır. Link üzerinden anlık olarak görsel verisi çekilebilir:
* **Dinamik Veri Çekme:** Requests altyapısı kullanılarak, herhangi bir URL bağlantısındaki görsel verisi ikili (binary) formatta indirilir.
* **Bellek İçi Görüntüleme:** İndirilen veri, doğrudan arayüz üzerindeki resim alanlarına veya pixmap kutularına aktarılır. Bu işlem bellek üzerinde gerçekleştiği için performans kaybı yaşanmaz.

### Oyun Motoru ve Multimedya
T-Sharp, oyun geliştirme mantığını kavramak için **Pygame** tabanlı bir oyun modülü içerir. Ekran tazeleme hızları, tuş kombinasyonları ve görsel nesnelerin (Sprite) koordinat sistemleri, soyutlanmış bir mantıkla kullanıcıya sunulur.

### Siber Güvenlik ve Kriptografi
**Hashlib** ve **HMAC** kütüphaneleri üzerinden SHA256 gibi algoritmalarla veri bütünlüğü kontrolü yapılabilir. T-Sharp, güvenli kodlama felsefesini en başından kullanıcıya aşılar. Sabit zamanlı karşılaştırma teknikleri (timing attack protection) sayesinde profesyonel düzeyde doğrulama mantığı sunar.

---

## 5. Hata Yönetimi ve Rehberlik

T-Sharp, hata yapmayı bir başarısızlık değil, bir öğrenme fırsatı olarak görür. Standart programlama dillerinin verdiği karmaşık hata mesajları yerine, kullanıcıya yol gösteren bir mekanizma kullanır.

* **Sözdizimi Rehberliği:** Eğer bir döngü veya koşul bloğu ("son" komutu ile) kapatılmadıysa, derleyici kullanıcıyı hangi satırda neyi unuttuğu konusunda uyarır.
* **Mantıksal Koruma:** Tanımlanmamış bir değişken kullanıldığında sistem hatayı yakalar ve çözüm önerileri sunarak uygulamanın çökmesini engeller.

---

## 6. Proje Yapısı ve Kullanılan Teknolojiler

T-Sharp ekosistemi, gücünü şu köklü teknolojilerin birleşiminden alır:
* **Ana Dil:** Python 3.12+
* **Arayüz Motorları:** PySide6 (Qt6), Tkinter
* **Grafik ve Oyun:** Pygame
* **Derleme Motoru:** TCompile (**PyInstaller** tabanlı)
* **Matematik ve Veri:** NumPy, Math
* **Ağ Protokolleri:** Requests
* **Güvenlik:** Hashlib, HMAC

---

## 7. Örnek Uygulama Senaryosu: İnternetten Resim Gösterici

Aşağıdaki mantıksal akış, T-Sharp'ın bir link üzerinden nasıl görsel çektiğini özetler:

1. Kullanıcıdan bir URL adresi alınır.
2. `ag_getir` komutu ile linke bağlanılır ve görsel verisi çekilir.
3. Çekilen veri `gorsel_donustur` komutu ile arayüzün anlayacağı formata çevrilir.
4. Tasarlanan penceredeki `resim_alani` kutusuna bu veri basılır.

---

## 8. Geliştirici ve Proje İstatistikleri

T-Sharp v4.1, tamamen bireysel bir çabanın ürünüdür. Projenin tüm mimarisi, tasarımı ve kodlaması aşağıda belirtilen geliştirici tarafından %100 oranında tamamlanmıştır.

| Geliştirici | Katkı Oranı | Rol |
| :--- | :---: | :--- |
| [**Talha Berk Arslan**](https://github.com/Codertalha5524) | %100 | Baş Geliştirici / Mimar |

---

## 9. Lisans

Bu proje **GNU Affero General Public License v3.0 (AGPL-3.0)** altında lisanslanmıştır. 

Bu lisans uyarınca, yazılımın değiştirilmiş sürümlerini bir ağ üzerinden sunanlar, bu sürümlerin kaynak kodunu kullanıcıların erişimine açmakla yükümlüdür. Bu, projenin ve topluluğun gelişiminin her zaman özgür kalmasını garanti altına alır.

---
**T-Sharp ile sadece kod yazmıyoruz; mantığını kendi dilinde kuran, özgürce üreten ve paylaşan bir gelecek inşa ediyoruz.**
