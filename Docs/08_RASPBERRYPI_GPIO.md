# T-Sharp (T#) — Raspberry Pi GPIO

![Lisans](https://img.shields.io/badge/Lisans-GNU_AGPL_v3-red.svg)
![Sürüm](https://img.shields.io/badge/Sürüm-v4.1-blue.svg)
![Statü](https://img.shields.io/badge/Proje-Solo_Açık_Kaynak-green.svg)
![Derleyici](https://img.shields.io/badge/Derleyici-TCompile-yellow.svg)

---

## Platform Uyarısı

GPIO komutları **yalnızca Raspberry Pi** üzerinde çalışır. Yorumlayıcı her GPIO komutu öncesinde `/proc/cpuinfo` dosyasını kontrol ederek platformu doğrular. Raspberry Pi olmayan bir cihazda çalıştırılırsa hata verir ve durur.

Desteklenen mimariler: `armv6l`, `armv7l`, `armv8l`, `aarch64`

> **Gereksinim:** `pip install lgpio`

---

## İçindekiler

1. [GPIO Başlatma ve Kapatma](#1-gpio-başlatma-ve-kapatma)
2. [Pin Modu Ayarlama](#2-pin-modu-ayarlama)
3. [Dijital Yazma ve Okuma](#3-dijital-yazma-ve-okuma)
4. [Pull-Up / Pull-Down Dirençleri](#4-pull-up--pull-down-dirençleri)
5. [Kesme (Interrupt)](#5-kesme-interrupt)
6. [PWM — Darbe Genişlik Modülasyonu](#6-pwm--darbe-genişlik-modülasyonu)
7. [I2C Protokolü](#7-i2c-protokolü)
8. [SPI Protokolü](#8-spi-protokolü)
9. [BCM Pin Numaraları (Raspberry Pi)](#9-bcm-pin-numaraları-raspberry-pi)
10. [Hızlı Başvuru Tablosu](#10-hızlı-başvuru-tablosu)

---

## 1. GPIO Başlatma ve Kapatma

GPIO kullanmadan önce sistemi başlatmak gerekir. Başlatma işlemi otomatik olarak da tetiklenebilir — `gpio_mod`, `gpio_yaz` gibi komutlar `gpio_handle` yoksa `gpio_baslat`'ı otomatik çağırır. Ancak en başta açıkça çağırmak önerilir.

```tsharp
gpio_baslat    // lgpio chip 0'ı açar
gpio_kapat     // chip'i kapatır, tüm pinleri serbest bırakır
```

> Program sonunda her zaman `gpio_kapat` çağrılmalıdır. Çağrılmazsa pin kilitleri açık kalabilir.

---

## 2. Pin Modu Ayarlama

Her pin kullanılmadan önce **giriş** veya **çıkış** olarak tanımlanmalıdır. Pin numaraları **BCM** numaralandırma sistemini kullanır.

```tsharp
gpio_mod <pin_no> <mod>
// mod: "cikis" veya "giris"
```

- `cikis` — pine değer yazmak için (LED, röle, buzzer vb.)
- `giris` — pinden değer okumak için (buton, sensör vb.)

> Pin modu `gpio_yaz` ile yazılmadan önce ayarlanmamışsa, yorumlayıcı uyarı vererek pini otomatik `cikis` moduna alır.

---

## 3. Dijital Yazma ve Okuma

### Pине Değer Yaz

```tsharp
gpio_yaz <pin_no> <deger>
// deger: dogru/1 → HIGH (3.3V), yanlis/0 → LOW (0V)
```

### Pinden Değer Oku

```tsharp
gpio_oku <pin_no> <degisken_adi>
// degisken_adi'ne 0 (LOW) veya 1 (HIGH) atanır
```

---

## 4. Pull-Up / Pull-Down Dirençleri

Giriş pinlerini sabit bir mantık seviyesine bağlamak için dahili dirençler aktive edilir. Özellikle butona basılmadığında pinin "havada" (floating) kalmaması için kullanılır.

### Pull-Up (Yüksek Çekme)

Basılmadığında pin HIGH (1) okunur, butona basılınca LOW (0) olur.

```tsharp
gpio_yukari_cek <pin_no>
```

### Pull-Down (Düşük Çekme)

Basılmadığında pin LOW (0) okunur, butona basılınca HIGH (1) olur.

```tsharp
gpio_asagi_cek <pin_no>
```

---

## 5. Kesme (Interrupt)

Bir pinin durumu değiştiğinde otomatik olarak bir fonksiyon çağırır. Sürekli yoklama (polling) yerine olay tabanlı programlama sağlar.

```tsharp
gpio_kesme <pin_no> <kenar> <fonksiyon_adi>
```

| `kenar` | Anlamı |
|---------|--------|
| `yukari` | LOW → HIGH geçişinde tetiklenir (RISING EDGE) |
| `asagi` | HIGH → LOW geçişinde tetiklenir (FALLING EDGE) |
| `her` | Her iki yönde de tetiklenir (BOTH EDGES) |

Kesmeyi kaldırmak için:

```tsharp
gpio_kesme_kaldir <pin_no>
```

> Fonksiyon daha önce `fonksiyon` komutuyla tanımlanmış olmalıdır.

---

## 6. PWM — Darbe Genişlik Modülasyonu

PWM, bir pini hızlıca açıp kapatarak ortalama voltaj kontrolü sağlar. LED parlaklığı, motor hızı, servo kontrolü gibi uygulamalarda kullanılır.

### PWM Başlat

```tsharp
pwm_baslat <pin_no> <frekans_hz> [duty_cycle]
```

- `frekans_hz` — saniyedeki döngü sayısı (pozitif tam sayı olmalı)
- `duty_cycle` — açık kalma oranı, `0`–`100` arası (varsayılan: `50`)
  - `0` → sürekli kapalı
  - `50` → yarı güç
  - `100` → sürekli açık

### Duty Cycle Güncelle

```tsharp
pwm_ayarla <pin_no> <yeni_duty>
// Önce pwm_baslat çağrılmış olmalıdır
```

### Frekans Güncelle

```tsharp
pwm_frekans <pin_no> <yeni_frekans_hz>
```

### PWM Durdur

```tsharp
pwm_durdur <pin_no>
```

---

## 7. I2C Protokolü

I2C, az sayıda kablo ile birden fazla cihazı bağlamayı sağlayan seri haberleşme protokolüdür. Her cihazın benzersiz bir adresi vardır.

### Bağlantı Aç

```tsharp
i2c_baslat <adres>
// adres: ondalık (39) veya hex (0x27) formatında
```

- I2C varsayılan olarak **bus 1** (`/dev/i2c-1`) üzerinden çalışır.
- Aynı anda tek I2C bağlantısı aktif olabilir.

### Bağlantıyı Kapat

```tsharp
i2c_kapat
```

### Veri Gönder

```tsharp
i2c_yaz <veri>
// veri: tam sayı, liste veya metin olabilir
```

### Veri Oku

```tsharp
i2c_oku <byte_sayisi> <degisken_adi>
// byte_sayisi: 1–4096 arası
// degisken_adi'ne byte listesi atanır
```

### Kayıt Adresi ile Yaz

```tsharp
i2c_kayit_yaz <kayit_adresi> <deger>
// tek bir kayıt adresine tek bir byte yazar
```

### Kayıt Adresi ile Oku

```tsharp
i2c_kayit_oku <kayit_adresi> <byte_sayisi> <degisken_adi>
// kayıt adresini yazıp ardından belirtilen kadar byte okur
```

---

## 8. SPI Protokolü

SPI, yüksek hızlı seri haberleşme protokolüdür. Ekranlar, ADC/DAC çipleri, SD kart modülleri gibi cihazlarla kullanılır.

### Bağlantı Aç

```tsharp
spi_baslat <kanal> [hiz_hz]
// kanal: SPI kanal numarası (genellikle 0 veya 1)
// hiz_hz: varsayılan 1000000 (1 MHz)
```

### Bağlantıyı Kapat

```tsharp
spi_kapat
```

### Veri Transfer Et

```tsharp
spi_transfer <giden_veri> <degisken_adi>
// giden_veri: byte listesi
// degisken_adi'ne gelen byte listesi atanır
// SPI çift yönlüdür: veri gönderilirken aynı anda veri alınır
```

---

## 9. BCM Pin Numaraları (Raspberry Pi)

T# GPIO komutları **BCM (Broadcom)** numaralandırma sistemini kullanır — fiziksel pin numaralarını değil.

```
3V3  ─── [ 1] [ 2] ─── 5V
GPIO2 ── [ 3] [ 4] ─── 5V
GPIO3 ── [ 5] [ 6] ─── GND
GPIO4 ── [ 7] [ 8] ─── GPIO14
GND  ─── [ 9] [10] ─── GPIO15
GPIO17 ─ [11] [12] ─── GPIO18
GPIO27 ─ [13] [14] ─── GND
GPIO22 ─ [15] [16] ─── GPIO23
3V3  ─── [17] [18] ─── GPIO24
GPIO10 ─ [19] [20] ─── GND
GPIO9 ── [21] [22] ─── GPIO25
GPIO11 ─ [23] [24] ─── GPIO8
GND  ─── [25] [26] ─── GPIO7
GPIO0 ── [27] [28] ─── GPIO1
GPIO5 ── [29] [30] ─── GND
GPIO6 ── [31] [32] ─── GPIO12
GPIO13 ─ [33] [34] ─── GND
GPIO19 ─ [35] [36] ─── GPIO16
GPIO26 ─ [37] [38] ─── GPIO20
GND  ─── [39] [40] ─── GPIO21
```

Köşeli parantez içindeki sayılar **fiziksel pin** numaralarıdır. T#'da `gpio_mod 17 cikis` yazıldığında BCM 17, yani fiziksel pin 11 kullanılır.

### Özel Fonksiyon Pinleri

| BCM Pin | Fiziksel | Fonksiyon |
|---------|----------|-----------|
| GPIO2 | 3 | I2C SDA |
| GPIO3 | 5 | I2C SCL |
| GPIO10 | 19 | SPI MOSI |
| GPIO9 | 21 | SPI MISO |
| GPIO11 | 23 | SPI SCLK |
| GPIO8 | 24 | SPI CE0 |
| GPIO7 | 26 | SPI CE1 |
| GPIO12 | 32 | PWM0 |
| GPIO13 | 33 | PWM1 |
| GPIO18 | 12 | PWM0 (alternatif) |
| GPIO19 | 35 | PWM1 (alternatif) |

---

## 10. Hızlı Başvuru Tablosu

| Komut | Açıklama |
|-------|----------|
| `gpio_baslat` | lgpio chip 0'ı açar |
| `gpio_kapat` | Chip'i kapatır |
| `gpio_mod <pin> "cikis"\|"giris"` | Pin modunu ayarlar |
| `gpio_yaz <pin> <deger>` | Pine dijital değer yazar |
| `gpio_oku <pin> <degisken>` | Pinden dijital değer okur |
| `gpio_yukari_cek <pin>` | Pull-up direnci aktive eder |
| `gpio_asagi_cek <pin>` | Pull-down direnci aktive eder |
| `gpio_kesme <pin> <kenar> <fonk>` | Kesme tanımlar |
| `gpio_kesme_kaldir <pin>` | Kesmeyi kaldırır |
| `pwm_baslat <pin> <frekans> [duty]` | PWM başlatır |
| `pwm_ayarla <pin> <duty>` | Duty cycle günceller |
| `pwm_frekans <pin> <frekans>` | Frekans günceller |
| `pwm_durdur <pin>` | PWM durdurur |
| `i2c_baslat <adres>` | I2C bağlantısı açar |
| `i2c_kapat` | I2C bağlantısını kapatır |
| `i2c_yaz <veri>` | I2C ile veri gönderir |
| `i2c_oku <byte_sayisi> <degisken>` | I2C'den veri okur |
| `i2c_kayit_yaz <kayit> <deger>` | Kayıt adresine yazar |
| `i2c_kayit_oku <kayit> <boy> <degisken>` | Kayıt adresinden okur |
| `spi_baslat <kanal> [hiz]` | SPI bağlantısı açar |
| `spi_kapat` | SPI bağlantısını kapatır |
| `spi_transfer <giden> <degisken>` | Çift yönlü veri transferi |
 ---
 
### İşte bu kadar artık sen TSharp biliyorsun
