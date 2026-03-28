# T-Sharp (T#) — Şifreleme ve Hash

![Lisans](https://img.shields.io/badge/Lisans-GNU_AGPL_v3-red.svg)
![Sürüm](https://img.shields.io/badge/Sürüm-v4.1-blue.svg)
![Statü](https://img.shields.io/badge/Proje-Solo_Açık_Kaynak-green.svg)
![Derleyici](https://img.shields.io/badge/Derleyici-TCompile-yellow.svg)

---

## Başlamadan Önce — Modül Aktivasyonu

T#'da şifreleme ve hash işlemleri **ayrı modüller** olarak tasarlanmıştır. Kullanmadan önce dosyanın en başında aktive edilmeleri gerekir.

```tsharp
kullan sifrele    // Base64, XOR, dosya şifreleme için
kullan hash       // SHA256, SHA512, MD5, SHA1, HMAC için
```

İkisini aynı anda da kullanabilirsiniz:

```tsharp
kullan sifrele
kullan hash
```

---

## İçindekiler

**Şifreleme Modülü (`kullan sifrele`)**
1. [Base64 Şifreleme — `b64_sifrele`](#1-base64-şifreleme--b64_sifrele)
2. [Base64 Çözme — `b64_coz`](#2-base64-çözme--b64_coz)
3. [XOR Şifreleme — `xor_sifrele`](#3-xor-şifreleme--xor_sifrele)
4. [XOR Çözme — `xor_coz`](#4-xor-çözme--xor_coz)
5. [Dosya Şifreleme — `dosya_sifrele`](#5-dosya-şifreleme--dosya_sifrele)
6. [Dosya Çözme — `dosya_coz`](#6-dosya-çözme--dosya_coz)
7. [Şifreli Dosyaya Yazma — `sifreli_yaz`](#7-şifreli-dosyaya-yazma--sifreli_yaz)
8. [Şifreli Dosya Okuma — `sifreli_oku`](#8-şifreli-dosya-okuma--sifreli_oku)

**Hash Modülü (`kullan hash`)**

9. [SHA256 — `sha256`](#9-sha256--sha256)
10. [SHA512 — `sha512`](#10-sha512--sha512)
11. [MD5 — `md5`](#11-md5--md5)
12. [SHA1 — `sha1`](#12-sha1--sha1)
13. [Dosya SHA256 — `dosya_sha256`](#13-dosya-sha256--dosya_sha256)
14. [HMAC — `hmac_hesapla`](#14-hmac--hmac_hesapla)
15. [Hash Doğrulama — `hash_dogrula`](#15-hash-doğrulama--hash_dogrula)
16. [Tam Örnek Programlar](#16-tam-örnek-programlar)

---

## ŞİFRELEME MODÜLÜ

---

## 1. Base64 Şifreleme — `b64_sifrele`

Metni Base64 formatına kodlar. Veriyi gizlemez, sadece taşınabilir bir formata çevirir. Genellikle veri iletimi için kullanılır.

### Söz dizimi

```tsharp
b64_sifrele <degisken> <metin>
```

### Örnek

```tsharp
kullan sifrele

b64_sifrele kodlanmis "Merhaba T-Sharp!"
yazdır kodlanmis
// TWhocmhhYmEgVC1TaGFycCE=  (Değişebilir)
```

---

## 2. Base64 Çözme — `b64_coz`

Base64 kodlu metni orijinal haline döndürür.

### Söz dizimi

```tsharp
b64_coz <degisken> <b64_metin>
```

### Örnek

```tsharp
kullan sifrele

b64_sifrele kodlanmis "Gizli mesaj"
yazdır "Şifreli:" kodlanmis

b64_coz acik kodlanmis
yazdır "Açık   :" acik
// Açık   : Gizli mesaj
```

---

## 3. XOR Şifreleme — `xor_sifrele`

Metni bir anahtar ile XOR işlemine tabi tutar, ardından Base64 ile kodlar. Aynı anahtar olmadan çözülemez. Hafif ve hızlı bir şifreleme yöntemidir.

### Söz dizimi

```tsharp
xor_sifrele <degisken> <metin> <anahtar>
```

### Örnek

```tsharp
kullan sifrele

degisken mesaj   = "Bu cok gizli bir mesajdir"
degisken anahtar = "benim_super_anahtarim"

xor_sifrele sifreli mesaj anahtar
yazdır "Şifreli:" sifreli
```

> **Önemli:** Anahtar ne kadar uzun ve karmaşık olursa şifreleme o kadar güçlü olur.
> Anahtar boş bırakılamaz — hata verir.

---

## 4. XOR Çözme — `xor_coz`

`xor_sifrele` ile şifrelenmiş metni, **aynı anahtarla** çözer.

### Söz dizimi

```tsharp
xor_coz <degisken> <sifreli_metin> <anahtar>
```

### Örnek

```tsharp
kullan sifrele

degisken mesaj   = "Raspberry Pi ile T-Sharp!"
degisken anahtar = "gizli_anahtar_42"

// Şifrele
xor_sifrele sifreli mesaj anahtar
yazdır "Şifreli :" sifreli

// Çöz
xor_coz cozulmus sifreli anahtar
yazdır "Çözülmüş:" cozulmus
```

**Çıktı:**
```
Şifreli : Hg8cFRUKEhMdGQYGCxYLBxkFGg==  (Değişebilir)
Çözülmüş: Raspberry Pi ile T-Sharp!
```

---

## 5. Dosya Şifreleme — `dosya_sifrele`

Bir dosyayı XOR + Base64 ile şifreleyerek yeni bir `.enc` dosyasına kaydeder.

### Söz dizimi

```tsharp
dosya_sifrele "<kaynak_dosya>" "<hedef_dosya>" "<anahtar>"
```

### Örnek

```tsharp
kullan sifrele

// Önce örnek bir dosya oluştur
dosya_yaz "belge.txt" "Bu dosyanin icindekiler gizlidir."

// Şifrele
dosya_sifrele "belge.txt" "belge.enc" "super_gizli_sifre"
yazdır "Dosya şifrelendi!"
```

---

## 6. Dosya Çözme — `dosya_coz`

`dosya_sifrele` ile şifrelenmiş bir dosyayı, **aynı anahtarla** çözer.

### Söz dizimi

```tsharp
dosya_coz "<sifreli_dosya>" "<hedef_dosya>" "<anahtar>"
```

### Örnek

```tsharp
kullan sifrele

// Şifreli dosyayı çöz
dosya_coz "belge.enc" "belge_acik.txt" "super_gizli_sifre"

// Çözülmüş dosyayı oku ve yazdır
degisken icerik = dosya_oku("belge_acik.txt")
yazdır icerik
```

---

## 7. Şifreli Dosyaya Yazma — `sifreli_yaz`

Bir metni şifreleyerek doğrudan dosyaya yazar. Ara adım (önce yaz, sonra şifrele) gerektirmez.

### Söz dizimi

```tsharp
sifreli_yaz "<dosya_yolu>" "<icerik>" "<anahtar>"
```

### Örnek

```tsharp
kullan sifrele

sifreli_yaz "gizli_notlar.enc" "Banka hesabı şifresi: 1234" "ana_sifre"
yazdır "Gizli not şifreli olarak kaydedildi."
```

---

## 8. Şifreli Dosya Okuma — `sifreli_oku`

`sifreli_yaz` ile yazılmış bir dosyayı okuyup çözer ve değişkene atar.

### Söz dizimi

```tsharp
sifreli_oku <degisken> "<dosya_yolu>" "<anahtar>"
```

### Örnek

```tsharp
kullan sifrele

// Yaz
sifreli_yaz "not.enc" "Bu cok ozel bir not." "sifrem123"

// Oku
sifreli_oku icerik "not.enc" "sifrem123"
yazdır icerik
// Bu cok ozel bir not.
```

---

## HASH MODÜLÜ

Hash fonksiyonları **tek yönlüdür** — bir metinden hash üretilir ama hash'ten metin geri alınamaz. Şifre doğrulama, dosya bütünlük kontrolü ve veri imzalama için kullanılır.

---

## 9. SHA256 — `sha256`

En yaygın kullanılan güvenli hash algoritması. Şifre saklama ve doğrulama için önerilir.

### Söz dizimi

```tsharp
sha256 <degisken> <metin>
```

### Örnek

```tsharp
kullan hash

sha256 sifre_hash "kullanici_sifresi_123"
yazdır sifre_hash
// e3b0c44298fc1c149afb... (64 karakter hex)
```

---

## 10. SHA512 — `sha512`

SHA256'dan daha uzun (128 karakter) ve daha güçlü hash üretir.

### Söz dizimi

```tsharp
sha512 <degisken> <metin>
```

### Örnek

```tsharp
kullan hash

sha512 guclu_hash "onemli_veri"
yazdır guclu_hash
```

---

## 11. MD5 — `md5`

Hızlı ama **güvenlik açısından zayıf** bir hash algoritması. Dosya bütünlük kontrolü gibi güvenlik gerektirmeyen durumlarda kullanılabilir. Şifre saklamak için **kullanmayın**.

### Söz dizimi

```tsharp
md5 <degisken> <metin>
```

### Örnek

```tsharp
kullan hash

md5 kontrol_hash "dosya_icerigi_buraya"
yazdır kontrol_hash
```

---

## 12. SHA1 — `sha1`

MD5'ten biraz daha güvenli ama SHA256 kadar güçlü değil. Eski sistemlerle uyumluluk için kullanılır.

### Söz dizimi

```tsharp
sha1 <degisken> <metin>
```

### Örnek

```tsharp
kullan hash

sha1 eski_hash "eski_sistem_verisi"
yazdır eski_hash
```

---

## 13. Dosya SHA256 — `dosya_sha256`

Bir dosyanın SHA256 hash'ini hesaplar. Dosyanın bozulup bozulmadığını veya değiştirilip değiştirilmediğini kontrol etmek için kullanılır. Büyük dosyaları 64KB'lık parçalar halinde işler.

### Söz dizimi

```tsharp
dosya_sha256 <degisken> "<dosya_yolu>"
```

### Örnek

```tsharp
kullan hash

dosya_sha256 dosya_hash "program.exe"
yazdır "Dosya hash:" dosya_hash
```

```tsharp
kullan hash

// Dosya bütünlük doğrulaması
degisken beklenen = "a3f5d2e1c9b8..." // daha önce kaydedilmiş hash

dosya_sha256 mevcut_hash "indirilen_dosya.zip"

eger mevcut_hash esittir beklenen:
    yazdır "Dosya bütünlüğü doğrulandı. Güvenli!"
degilse:
    yazdır "UYARI: Dosya değiştirilmiş olabilir!"
son
```

---

## 14. HMAC — `hmac_hesapla`

Bir mesajın hem **bütünlüğünü** hem de **kaynağını** doğrulamak için kullanılır. Sadece hash değil, aynı zamanda gizli anahtar gerektirdiği için daha güvenlidir.

### Söz dizimi

```tsharp
hmac_hesapla <degisken> "<anahtar>" "<metin>"
```

### Örnek

```tsharp
kullan hash

hmac_hesapla imza "gizli_api_anahtari" "gonderilecek_mesaj"
yazdır "HMAC İmzası:" imza
```

```tsharp
kullan hash

// API isteğini imzalama
degisken api_key = "abc123secret"
degisken mesaj   = "kullanici_id=42&islem=odeme&tutar=100"

hmac_hesapla istek_imzasi api_key mesaj
yazdır "İstek imzası:" istek_imzasi
```

---

## 15. Hash Doğrulama — `hash_dogrula`

Bir metnin hash'ini hesaplayıp beklenen değerle karşılaştırır. **Sabit zamanlı karşılaştırma** (timing attack koruması) kullanır — güvenli şifre doğrulaması için idealdir.

### Söz dizimi

```tsharp
hash_dogrula <degisken> <metin> <beklenen_hash> ["algoritma"]
```

Algoritma parametresi: `sha256` (varsayılan), `sha512`, `md5`, `sha1`

### Örnek

```tsharp
kullan hash

// Şifreyi hashle ve kaydet
sha256 kayitli_hash "kullanici_sifresi"

// Sonra doğrula
hash_dogrula sonuc "kullanici_sifresi" kayitli_hash "sha256"

eger sonuc:
    yazdır "Şifre doğru! Giriş başarılı."
degilse:
    yazdır "Hata: Yanlış şifre."
son
```

```tsharp
kullan hash

// SHA512 ile doğrulama
sha512 guclu_hash "super_gizli_sifre"

hash_dogrula kontrol "super_gizli_sifre" guclu_hash "sha512"
yazdır kontrol    // dogru

hash_dogrula kontrol "yanlis_sifre" guclu_hash "sha512"
yazdır kontrol    // yanlis
```

---

## 16. Tam Örnek Programlar

### Örnek 1 — Şifreli Not Defteri

```tsharp
kullan sifrele

degisken dosya = "notlar.enc"

girdi ana_sifre "Ana şifrenizi girin: "

dongu dogru:
    yazdır "=== GİZLİ NOT DEFTERİ ==="
    yazdır "1) Not ekle"
    yazdır "2) Notları görüntüle"
    yazdır "3) Çıkış"
    girdi secim "Seçim: "

    eger secim esittir "1":
        girdi yeni_not "Notunuz: "

        // Mevcut notları oku (varsa)
        eger dosya_var_mi(dosya):
            sifreli_oku eski_notlar dosya ana_sifre
            degisken tum_notlar = eski_notlar + "\n" + yeni_not
        degilse:
            degisken tum_notlar = yeni_not
        son

        sifreli_yaz dosya tum_notlar ana_sifre
        yazdır "Not kaydedildi!"
    son

    eger secim esittir "2":
        eger dosya_var_mi(dosya):
            sifreli_oku notlar dosya ana_sifre
            eger notlar degildir hic:
                yazdır "--- Notlarınız ---"
                yazdır notlar
            degilse:
                yazdır "Şifre yanlış veya dosya bozuk."
            son
        degilse:
            yazdır "Henüz not yok."
        son
    son

    eger secim esittir "3":
        yazdır "Güle güle!"
        dur
    son
son
```

### Örnek 2 — Kullanıcı Kayıt ve Giriş Sistemi

```tsharp
kullan hash

degisken kullanici_dosyasi = "kullanicilar.txt"

fonksiyon kayit_ol(kullanici_adi, sifre):
    // Şifreyi hashle - asla düz metin saklanmaz!
    sha256 sifre_hash sifre
    degisken kayit = kullanici_adi + ":" + sifre_hash
    dosya_ekle kullanici_dosyasi kayit + "\n"
    yazdır "Kayıt başarılı:" kullanici_adi
son

fonksiyon giris_yap(kullanici_adi, sifre):
    eger degil dosya_var_mi(kullanici_dosyasi):
        yazdır "Kullanıcı bulunamadı."
        dondur yanlis
    son

    degisken icerik = dosya_oku(kullanici_dosyasi)
    liste satirlar = bol(icerik, "\n")
    sha256 girilen_hash sifre

    her satir icinde satirlar:
        eger uzunluk(satir) buyuktur 0:
            liste parcalar = bol(satir, ":")
            eger parcalar[0] esittir kullanici_adi:
                hash_dogrula eslesme sifre parcalar[1] "sha256"
                eger eslesme:
                    yazdır "Giriş başarılı! Hoş geldin," kullanici_adi
                    dondur dogru
                degilse:
                    yazdır "Hata: Yanlış şifre."
                    dondur yanlis
                son
            son
        son
    son

    yazdır "Kullanıcı bulunamadı:" kullanici_adi
    dondur yanlis
son

// Kullanım
kayit_ol("talha", "guvenli_sifre_123")
kayit_ol("ayse", "baska_sifre_456")

giris_yap("talha", "guvenli_sifre_123")   // Başarılı
giris_yap("talha", "yanlis_sifre")         // Hata
giris_yap("olmayan", "herhangi")            // Bulunamadı
```

### Örnek 3 — Dosya Bütünlük Denetleyicisi

```tsharp
kullan hash

// Kritik dosyaların hash değerlerini kaydet
liste kritik_dosyalar ["ana.tsharp", "ayarlar.txt", "veri.csv"]
degisken hash_dosyasi = "dosya_hashleri.txt"

fonksiyon hashleri_kaydet():
    dosya_yaz hash_dosyasi ""
    her dosya icinde kritik_dosyalar:
        eger dosya_var_mi(dosya):
            dosya_sha256 h dosya
            dosya_ekle hash_dosyasi dosya + ":" + h + "\n"
            yazdır "Hash kaydedildi:" dosya
        degilse:
            yazdır "Dosya bulunamadi:" dosya
        son
    son
    yazdır "Tüm hashler kaydedildi."
son

fonksiyon hashleri_dogrula():
    eger degil dosya_var_mi(hash_dosyasi):
        yazdır "Hash dosyası bulunamadı. Önce kaydet."
        dondur
    son

    degisken kayitlar = dosya_oku(hash_dosyasi)
    liste satirlar = bol(kayitlar, "\n")
    degisken temiz = 0
    degisken degismis = 0

    her satir icinde satirlar:
        eger uzunluk(satir) buyuktur 0:
            liste parcalar = bol(satir, ":")
            degisken dosya_adi  = parcalar[0]
            degisken kayitli_h  = parcalar[1]

            eger dosya_var_mi(dosya_adi):
                dosya_sha256 mevcut_h dosya_adi
                eger mevcut_h esittir kayitli_h:
                    yazdır "Temiz:" dosya_adi
                    temiz += 1
                degilse:
                    yazdır "DEGİSTİRİLMİS:" dosya_adi
                    degismis += 1
                son
            degilse:
                yazdır "SİLİNMİS:" dosya_adi
                degismis += 1
            son
        son
    son

    yazdır "--- Sonuç ---"
    yazdır "Temiz    :" temiz
    yazdır "Degismis :" degismis
son

// Kullanım
hashleri_kaydet()
yazdır
hashleri_dogrula()
```

### Örnek 4 — XOR ile Mesajlaşma Simülasyonu

```tsharp
kullan sifrele

degisken paylasilan_anahtar = "T_Sharp_Gizli_Anahtar_2025"

// Gönderici tarafı
degisken mesaj = "Bulusma yeri: Kizilayda saat 15:00"
yazdır "Orijinal mesaj:" mesaj

xor_sifrele sifreli_mesaj mesaj paylasilan_anahtar
yazdır "Şifreli (iletilen):" sifreli_mesaj
yazdır

// Alıcı tarafı (aynı anahtarla çözer)
xor_coz alinan_mesaj sifreli_mesaj paylasilan_anahtar
yazdır "Çözülen mesaj:" alinan_mesaj

// Doğrulama
eger alinan_mesaj esittir mesaj:
    yazdır "Mesaj bütünlüğü doğrulandı."
son
```

---

## Algoritma Karşılaştırma Tablosu

| Algoritma | Komut | Çıktı Uzunluğu | Güvenlik | Kullanım Amacı |
|-----------|-------|----------------|----------|----------------|
| Base64 | `b64_sifrele` | ~%33 büyür | Yok (kodlama) | Veri taşıma |
| XOR | `xor_sifrele` | Base64 kadar | Orta | Hafif şifreleme |
| MD5 | `md5` | 32 karakter | Düşük ⚠️ | Sadece kontrol |
| SHA1 | `sha1` | 40 karakter | Düşük ⚠️ | Eski sistemler |
| SHA256 | `sha256` | 64 karakter | Yüksek ✓ | Şifre saklama |
| SHA512 | `sha512` | 128 karakter | Çok Yüksek ✓ | Kritik veriler |
| HMAC | `hmac_hesapla` | 64 karakter | Çok Yüksek ✓ | API imzalama |

## Hızlı Başvuru Tablosu

| Komut | Modül | Açıklama |
|-------|-------|----------|
| `kullan sifrele` | — | Şifreleme modülünü aktive eder |
| `kullan hash` | — | Hash modülünü aktive eder |
| `b64_sifrele <d> <metin>` | sifrele | Base64 kodlar |
| `b64_coz <d> <metin>` | sifrele | Base64 çözer |
| `xor_sifrele <d> <metin> <anahtar>` | sifrele | XOR+B64 şifreler |
| `xor_coz <d> <sifreli> <anahtar>` | sifrele | XOR+B64 çözer |
| `dosya_sifrele "<kaynak>" "<hedef>" "<anahtar>"` | sifrele | Dosya şifreler |
| `dosya_coz "<kaynak>" "<hedef>" "<anahtar>"` | sifrele | Dosya çözer |
| `sifreli_yaz "<dosya>" "<metin>" "<anahtar>"` | sifrele | Şifreli yazar |
| `sifreli_oku <d> "<dosya>" "<anahtar>"` | sifrele | Şifreli okur |
| `sha256 <d> <metin>` | hash | SHA-256 hash üretir |
| `sha512 <d> <metin>` | hash | SHA-512 hash üretir |
| `md5 <d> <metin>` | hash | MD5 hash üretir |
| `sha1 <d> <metin>` | hash | SHA-1 hash üretir |
| `dosya_sha256 <d> "<dosya>"` | hash | Dosya SHA-256 hash |
| `hmac_hesapla <d> "<anahtar>" "<metin>"` | hash | HMAC-SHA256 üretir |
| `hash_dogrula <d> <metin> <hash> ["algo"]` | hash | Hash doğrular |

---

> **Sonraki bölüm:** `05_GUI_TKINTER.md` — Tkinter ile masaüstü pencere, buton, etiket ve form bileşenleri.
