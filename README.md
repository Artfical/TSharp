# T-Sharp (T#) Programlama Dili ve Derleyici Ekosistemi

![Dil](https://img.shields.io/badge/Dil-Türkçe-red)
![Motor](https://img.shields.io/badge/Motor-Python_3.12-blue)
![Derleyici](https://img.shields.io/badge/Derleyici-PyInstaller-yellow)
![Lisans](https://img.shields.io/badge/Lisans-MIT-green)

<p align="center">
  <img src="https://github-readme-stats.vercel.app/api/pin/?username=kullanici_adin&repo=t-sharp&theme=radical&show_owner=true" alt="T-Sharp Proje Kartı" />
</p>

T-Sharp (T#), bireysel (solo) bir açık kaynak girişimi olarak, bilişsel yükü minimize eden ve algoritma mantığını tamamen ana dilde kurgulayan bir yazılım geliştirme ekosistemidir. Bu proje, sadece bir script dili değil; bir derleyici, bir görsel arayüz motoru ve bir IoT kontrol merkezi olarak yapılandırılmıştır.

---

## 1. Stratejik Misyon ve Açık Kaynak Felsefesi

T-Sharp, yazılım dünyasındaki "İngilizce biliyorsan yazılımcı olabilirsin" tabusunu yıkmak için başlatılmıştır. Tek bir geliştirici tarafından inşa edilen bu mimari, topluluk desteğiyle büyüyecek bir açık kaynak kütüphanesi olmayı hedefler.

### Bireysel Geliştirme ve Modülerlik
Proje, tek bir kişi tarafından yönetilmesine rağmen profesyonel ekiplerin standartlarında bir modülerlik sunar. Her bir bileşen (GUI, Ağ, Donanım) birbirinden bağımsız çalışabilir ancak aynı çekirdek yorumlayıcı tarafından yönetilir. Bu, projenin sürdürülebilirliğini ve genişletilebilirliğini artırır.

### Eğitimde Fırsat Eşitliği
T-Sharp'ın misyonu, en ücra köşedeki bir çocuğun bile elindeki bilgisayarla, yabancı dil engeline takılmadan "Eğer sensörden gelen veri 30'dan büyükse LED'i yak" mantığını kurabilmesini sağlamaktır.

---

## 2. Teknik Mimari ve Çekirdek Yapı

T-Sharp, arka planda hibrit bir çalışma prensibi benimseyen, oldukça karmaşık bir yorumlayıcı ve dönüştürücü (transpiler) katmanına sahiptir.

### Komut Analiz ve Normalizasyon Sistemi
Sistemin çekirdeği olan TSharp sınıfı, her satırı titizlikle analiz eden bir sözcük tarayıcıya sahiptir. Normalizasyon modülü sayesinde, Türkçe karakter hassasiyeti (ı, i, ğ, ü, ş, ö) bir engel olmaktan çıkarılır. Düzenli ifadeler (Regular Expressions) ile desteklenen bu yapı, karmaşık matematiksel formülleri ve mantıksal ifadeleri gerçek zamanlı olarak çözümleyerek işlem sırasına koyar.

### Dinamik Bellek Yönetimi
T-Sharp, kullanıcıyı tür tanımlama zorunluluğundan kurtarır. Dinamik bir bellek sözlüğü kullanarak değişkenleri, listeleri ve fonksiyonları çalışma zamanında (runtime) otomatik olarak haritalandırır.

---

## 3. Derleyici ve Dağıtım Teknolojisi

T-Sharp, yazdığınız Türkçe kodları bağımsız birer yazılım haline getirebilen güçlü bir derleme motoruna sahiptir.

### Derleme Süreci (Compilation Pipeline)
Kullanıcı kodunu tamamladığında, derleme motoru şu aşamaları izler:
1. Kaynak Kod Analizi: .tsharp dosyası taranarak soyut bir sözdizimi ağacı oluşturulur.
2. Python Transpilation: Oluşturulan mantıksal yapı, optimize edilmiş Python koduna dönüştürülür.
3. Paketleme: Bu ara kod, PyInstaller motoru ile entegre edilerek, tüm bağımlılıkları ve yorumlayıcı çekirdeği ile birlikte tek bir .exe (Windows) veya ELF (Linux) dosyasına dönüştürülür.

---

## 4. Entegre Kütüphaneler ve Görsel Sistemler

T-Sharp, modern yazılım dünyasının tüm gereksinimlerini karşılayan gelişmiş alt modüllerle donatılmıştır.

### Görsel Arayüz (GUI) ve Form Yönetimi
* Standart GUI (Tkinter): Hızlı araçlar ve basit pencereler için.
* Profesyonel GUI (PySide6 / Qt): Modern ve çok fonksiyonlu masaüstü uygulamaları için kullanılır. Sekmeli yapılar ve karmaşık yerleşim planları tamamen Türkçe komutlarla yönetilir.

### Ağ Üzerinden Görsel Çekme ve İşleme
Ağ modülü, internet üzerindeki kaynaklara erişimi bir üst seviyeye taşır. Link üzerinden anlık olarak görsel verisi çekilebilir:
* Dinamik Veri Çekme: Requests altyapısı kullanılarak, herhangi bir URL bağlantısındaki görsel verisi ikili (binary) formatta indirilir.
* Görüntüleme: İndirilen veri, doğrudan arayüz üzerindeki etiketlere veya resim kutularına aktarılır. Bu işlem, bellek üzerinde (RAM) gerçekleştiği için performans kaybı yaşanmaz.

### Oyun Motoru ve Multimedya
T-Sharp, oyun geliştirme mantığını kavramak için Pygame tabanlı bir oyun modülü içerir. Ekran tazeleme hızları, tuş kombinasyonları ve görsel nesnelerin koordinat sistemleri, soyutlanmış bir mantıkla kullanıcıya sunulur.

### Siber Güvenlik ve Kriptografi
Hashlib ve HMAC kütüphaneleri üzerinden SHA256 gibi algoritmalarla veri bütünlüğü kontrolü yapılabilir. Sabit zamanlı karşılaştırma teknikleri gibi profesyonel güvenlik detayları, kullanıcıya basit bir "doğrula" mantığıyla sunulur.

---

## 5. Hata Yönetimi ve Rehberlik

T-Sharp, hata yapmayı bir başarısızlık değil, bir öğrenme fırsatı olarak görür. Standart programlama dillerinin verdiği karmaşık ve korkutucu hata mesajları yerine, kullanıcıya yol gösteren bir mekanizma kullanır.

* Sözdizimi Kontrolü: Eğer bir döngü veya koşul bloğu ("son" komutu ile) kapatılmadıysa, derleyici kullanıcıyı hangi satırda neyi unuttuğu konusunda uyarır.
* Mantıksal Rehberlik: Tanımlanmamış bir değişken kullanıldığında sistem hatayı yakalar ve çözüm önerileri sunarak uygulamanın çökmesini engeller.

---

## 6. Proje Yapısı ve Kullanılan Teknolojiler

T-Sharp ekosistemi, gücünü şu köklü teknolojilerin birleşiminden alır:
* Ana Dil ve Yorumlayıcı: Python 3.x
* Arayüz Motorları: PySide6 (Qt6), Tkinter
* Grafik ve Oyun: Pygame
* Derleme ve Paketleme: PyInstaller
* Veri Analizi: NumPy
* İletişim ve Ağ: Requests
* Güvenlik: Hashlib, HMAC

---

## 7. Örnek Uygulama Senaryosu: İnternetten Resim Gösterici

Aşağıdaki mantıksal akış, T-Sharp'ın bir link üzerinden nasıl görsel çektiğini özetler:

1. Kullanıcıdan bir URL adresi alınır.
2. `ag_getir` komutu ile linke bağlanılır ve görsel verisi çekilir.
3. Çekilen veri `gorsel_donustur` komutu ile arayüzün anlayacağı formata çevrilir.
4. Tasarlanan penceredeki `resim_alani` kutusuna bu veri basılır.

---

## 8. Katkıda Bulunma ve Geliştirici İstatistikleri

Solo bir proje olan T-Sharp, her türlü yapıcı eleştiriye ve katkıya açıktır. Aşağıda projenin canlı istatistikleri ve kullanılan teknoloji ağırlığı yer almaktadır:

<p align="left">
  <img src="https://github-readme-stats.vercel.app/api/top-langs/?username=kullanici_adin&layout=compact&theme=radical" alt="Dil İstatistikleri" />
</p>

---

## Sonuç

T-Sharp (T#), kodlamayı bir "teknik iş" olmaktan çıkarıp bir "düşünce biçimi" haline getirir. Türkçe komut seti, derlenebilir yapısı, internetten canlı veri çekme yeteneği ve zengin kütüphane desteğiyle, geleceğin mühendislerini yetiştirmek için eksiksiz bir platform sunar. Bu dille yazılan her satır, özgürce tasarlanmış bir geleceğin temel taşıdır.
