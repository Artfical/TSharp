# T-Sharp (T#) — PySide6 GUI (Qt6 Arayüz)

![Lisans](https://img.shields.io/badge/Lisans-GNU_AGPL_v3-red.svg)
![Sürüm](https://img.shields.io/badge/Sürüm-v4.1-blue.svg)
![Statü](https://img.shields.io/badge/Proje-Solo_Açık_Kaynak-green.svg)
![Derleyici](https://img.shields.io/badge/Derleyici-TCompile-yellow.svg)

---

## Başlamadan Önce — `kullan gui6`

PySide6 modülünü aktive etmek için dosyanın **en başına** yazın:

```tsharp
kullan gui6
```

> **Gereksinim:** `pip install PySide6`

Tkinter'dan farkı: PySide6 modern, şık ve platformlar arası profesyonel arayüzler için kullanılır. Layout sistemi zorunludur — widget'lar pencereye doğrudan değil, layout aracılığıyla eklenir.

---

## Tkinter'dan Temel Farklar

| Tkinter | PySide6 |
|---------|---------|
| `kullan gui` | `kullan gui6` |
| `pencere_goster` | `qt_pencere_goster` + `qt_calistir` |
| Widget pencereye direkt eklenir | Widget layouta eklenir |
| `etiket`, `buton` | `qt_etiket`, `qt_buton` |
| Tüm komutlar `qt_` önekiyle başlar |  |

---

## İçindekiler

1. [Pencere ve Uygulama Döngüsü](#1-pencere-ve-uygulama-döngüsü)
2. [Layout Sistemi](#2-layout-sistemi)
3. [Temel Widgetlar](#3-temel-widgetlar)
4. [Giriş Widgetları](#4-giriş-widgetları)
5. [Seçim Widgetları](#5-seçim-widgetları)
6. [Sayısal ve Tarih Widgetları](#6-sayısal-ve-tarih-widgetları)
7. [Liste, Tablo ve Ağaç](#7-liste-tablo-ve-ağaç)
8. [Sekmeli Yapı](#8-sekmeli-yapı)
9. [Menü, Toolbar ve Statusbar](#9-menü-toolbar-ve-statusbar)
10. [Grafik — Chart](#10-grafik--chart)
11. [Web Tarayıcı Widget'ı](#11-web-tarayıcı-widgetı)
12. [Video Oynatıcı](#12-video-oynatıcı)
13. [Timer](#13-timer)
14. [Diyalog Kutuları](#14-diyalog-kutuları)
15. [Hızlı Başvuru Tablosu](#15-hızlı-başvuru-tablosu)

---

## 1. Pencere ve Uygulama Döngüsü

### Pencere Oluştur

```tsharp
qt_pencere <ad> "<baslik>" <genislik> <yukseklik>
```

- Varsayılan boyut: `800x600`
- Oluşturulduğunda `<ad>_merkez` adında merkez widget değişkeni de otomatik yaratılır. Layout'lar bu merkez widget'a bağlanır.

### Pencereyi Göster ve Çalıştır

PySide6'da pencere açmak **iki adımlıdır**:

```tsharp
qt_pencere_goster <pencere_adi>   // pencereyi görünür yapar
qt_calistir                        // uygulama döngüsünü başlatır (en sona yazılır)
```

> `qt_calistir` her zaman dosyanın **en son satırı** olmalıdır.

---

## 2. Layout Sistemi

PySide6'da widget'lar doğrudan pencereye değil, **layout**'a eklenir. Layout da bir parent widget'a bağlanır.

```tsharp
qt_layout <ad> <tip> <parent_adi>
```

| `tip` | Açıklama |
|-------|----------|
| `dikey` | Widget'ları üst üste dizer (VBoxLayout) |
| `yatay` | Widget'ları yan yana dizer (HBoxLayout) |
| `grid` | Izgara düzeni (GridLayout) |
| `form` | Etiket-giriş çiftleri için (FormLayout) |

Layout bir parent'a bağlandıktan sonra, o parent adıyla eklenen tüm widget'lar otomatik olarak layout'a yerleşir:

```tsharp
qt_pencere ana "Uygulama" 600 400
qt_layout yerlesim dikey ana_merkez   // pencere merkez widget'ına bağla

qt_etiket lbl "Başlık" ana_merkez     // layout'a otomatik eklenir
qt_buton  btn "Tıkla"  ana_merkez fonk
```

---

## 3. Temel Widgetlar

### Etiket

```tsharp
qt_etiket <ad> "<metin>" <parent_adi>
```

### Buton

```tsharp
qt_buton <ad> "<metin>" <parent_adi> [fonksiyon_adi]
```

- `fonksiyon_adi` verilirse butona tıklandığında o fonksiyon çalışır.

### İlerleme Çubuğu

```tsharp
qt_ilerleme_cubugu <ad> <parent_adi>
```

---

## 4. Giriş Widgetları

### Tek Satır Giriş

```tsharp
qt_giriskutusu <ad> <parent_adi>
```

### Çok Satır Metin Alanı

```tsharp
qt_metin_alani <ad> <parent_adi>
```

---

## 5. Seçim Widgetları

### Onay Kutusu

```tsharp
qt_onay_kutusu <ad> "<metin>" <parent_adi>
```

### Radyo Buton

```tsharp
qt_radyo_buton <ad> "<metin>" <parent_adi>
```

- PySide6'da radyo butonlar aynı layout içinde olduğunda otomatik grup oluşturur.

### Combo Kutu (Dropdown)

```tsharp
qt_combo_kutu <ad> <parent_adi>
```

- İçeriği doldurmak için Python tarafında `.addItems()` ile ya da widget üzerinden yönetilir.

### Kaydırıcı

```tsharp
qt_kaydirici <ad> <parent_adi> ["yatay"|"dikey"] [min] [max]
```

- Yön varsayılanı: `yatay`
- Değer aralığı varsayılanı: `0–100`

---

## 6. Sayısal ve Tarih Widgetları

### Sayaç Kutu (SpinBox)

```tsharp
qt_spin_kutu <ad> <parent_adi> [min] [max]
```

- Varsayılan aralık: `0–100`

### Tarih Seçici

```tsharp
qt_tarih_secici <ad> <parent_adi>
```

- Takvim açılır popup ile gelir (`setCalendarPopup` aktif).

### Saat Seçici

```tsharp
qt_saat_secici <ad> <parent_adi>
```

### Takvim Widget'ı

```tsharp
qt_takvim <ad> <parent_adi>
```

- Tam boyutlu aylık takvim görünümü sunar.

---

## 7. Liste, Tablo ve Ağaç

### Liste Widget'ı

```tsharp
qt_liste_widget <ad> <parent_adi>
```

### Tablo Widget'ı

```tsharp
qt_tablo_widget <ad> <parent_adi> [satir_sayisi] [sutun_sayisi]
```

- Varsayılan: `5` satır, `3` sütun

### Ağaç Widget'ı

```tsharp
qt_agac_widget <ad> <parent_adi>
```

---

## 8. Sekmeli Yapı

```tsharp
qt_sekme_widget <ad> <parent_adi>
```

- QTabWidget oluşturur. Sekmeler Qt tarafında yönetilir.

---

## 9. Menü, Toolbar ve Statusbar

### Menü

Doğrudan pencereye bağlanır — layout gerekmez.

```tsharp
qt_menu <ad> "<baslik>" <pencere_adi>
```

- `qt_menu` hem menü çubuğunu oluşturur hem de ona bir menü başlığı ekler.
- Aynı pencereye birden fazla `qt_menu` çağrısıyla farklı başlıklar eklenebilir.

### Toolbar

```tsharp
qt_toolbar <ad> "<baslik>" <pencere_adi>
```

### Statusbar

```tsharp
qt_statusbar <ad> <pencere_adi>
```

- Pencerenin alt kısmına durum çubuğu ekler.

---

## 10. Grafik — Chart

> **Gereksinim:** `pip install PySide6` (Charts modülü dahildir ancak bazı dağıtımlarda ayrı gelebilir.)

```tsharp
qt_grafik <ad> <parent_adi> ["cizgi"|"pasta"|"cubuk"]
```

Oluşturulduğunda üç değişken otomatik yaratılır:

| Değişken | İçerik |
|----------|--------|
| `<ad>` | QChartView — görünüm nesnesi |
| `<ad>_chart` | QChart — grafik nesnesi |
| `<ad>_series` | Seri nesnesi (QLineSeries / QPieSeries / QBarSeries) |

---

## 11. Web Tarayıcı Widget'ı

> **Gereksinim:** `pip install PySide6-WebEngine`

```tsharp
qt_web_tarayici <ad> <parent_adi> "<url>"
```

- `url` verilmezse varsayılan olarak `https://www.google.com` açılır.
- Tam işlevsel Chromium tabanlı bir tarayıcı widget'ı ekler.

---

## 12. Video Oynatıcı

> **Gereksinim:** PySide6 Multimedia modülü

```tsharp
qt_video_oynatici <ad> <parent_adi>
```

Oluşturulduğunda üç değişken otomatik yaratılır:

| Değişken | İçerik |
|----------|--------|
| `<ad>` | QVideoWidget — görüntü alanı |
| `<ad>_player` | QMediaPlayer — oynatıcı kontrolü |
| `<ad>_audio` | QAudioOutput — ses çıkışı |

---

## 13. Timer

Belirli aralıklarla tekrar eden işlemler için kullanılır. Tkinter'ın `timer_olustur`'undan farklı olarak **sürekli tekrar eder**.

```tsharp
qt_timer <ad> <milisaniye> [fonksiyon_adi]
```

- Timer oluşturulduğunda otomatik başlamaz — `<ad>` değişkeni üzerinden Qt API ile başlatılabilir.
- `1000` ms = 1 saniye

---

## 14. Diyalog Kutuları

### Mesaj Kutusu

```tsharp
qt_mesaj_kutusu "<baslik>" "<mesaj>" ["bilgi"|"uyari"|"hata"|"soru"]
```

- Tip verilmezse varsayılan: `bilgi`

### Dosya Diyaloğu

```tsharp
qt_dosya_dialog <degisken_adi> ["ac"|"kaydet"|"klasor"]
```

- `ac` — dosya açma diyaloğu
- `kaydet` — dosya kaydetme diyaloğu
- `klasor` — klasör seçme diyaloğu
- Seçilen yol `degisken_adi`'ne atanır.

### Renk Diyaloğu

```tsharp
qt_renk_dialog <degisken_adi>
```

- Seçilen renk QColor nesnesi olarak `degisken_adi`'ne atanır.

---

## 15. Hızlı Başvuru Tablosu

| Komut | Açıklama |
|-------|----------|
| `kullan gui6` | PySide6 modülünü aktive eder |
| `qt_pencere <ad> "<baslik>" <g> <y>` | Ana pencere oluşturur |
| `qt_pencere_goster <ad>` | Pencereyi görünür yapar |
| `qt_calistir` | Uygulama döngüsünü başlatır (en sona) |
| `qt_layout <ad> <tip> <parent>` | Layout oluşturur ve parent'a bağlar |
| `qt_etiket <ad> "<metin>" <parent>` | Metin etiketi |
| `qt_buton <ad> "<metin>" <parent> [fonk]` | Buton |
| `qt_giriskutusu <ad> <parent>` | Tek satır giriş |
| `qt_metin_alani <ad> <parent>` | Çok satır metin alanı |
| `qt_onay_kutusu <ad> "<metin>" <parent>` | Checkbox |
| `qt_radyo_buton <ad> "<metin>" <parent>` | Radio button |
| `qt_combo_kutu <ad> <parent>` | Dropdown |
| `qt_kaydirici <ad> <parent> [yon] [min] [max]` | Slider |
| `qt_ilerleme_cubugu <ad> <parent>` | Progress bar |
| `qt_spin_kutu <ad> <parent> [min] [max]` | SpinBox |
| `qt_tarih_secici <ad> <parent>` | Tarih seçici (takvim popup'lı) |
| `qt_saat_secici <ad> <parent>` | Saat seçici |
| `qt_takvim <ad> <parent>` | Tam takvim widget'ı |
| `qt_liste_widget <ad> <parent>` | Liste widget'ı |
| `qt_tablo_widget <ad> <parent> [satir] [sutun]` | Tablo widget'ı |
| `qt_agac_widget <ad> <parent>` | Ağaç widget'ı |
| `qt_sekme_widget <ad> <parent>` | Sekmeli yapı |
| `qt_menu <ad> "<baslik>" <pencere>` | Menü ekler |
| `qt_toolbar <ad> "<baslik>" <pencere>` | Toolbar ekler |
| `qt_statusbar <ad> <pencere>` | Statusbar ekler |
| `qt_grafik <ad> <parent> [tip]` | Grafik (cizgi/pasta/cubuk) |
| `qt_web_tarayici <ad> <parent> "<url>"` | Web tarayıcı widget'ı |
| `qt_video_oynatici <ad> <parent>` | Video oynatıcı |
| `qt_timer <ad> <ms> [fonk]` | Zamanlayıcı |
| `qt_mesaj_kutusu "<baslik>" "<mesaj>" [tip]` | Mesaj diyaloğu |
| `qt_dosya_dialog <d> [mod]` | Dosya/klasör seçici |
| `qt_renk_dialog <d>` | Renk seçici |

### Otomatik Oluşan Değişkenler

| Widget | Otomatik Değişken | İçerik |
|--------|-------------------|--------|
| `qt_pencere` | `<ad>_merkez` | Merkez QWidget (layout bağlamak için) |
| `qt_grafik` | `<ad>_chart`, `<ad>_series` | Grafik ve seri nesneleri |
| `qt_video_oynatici` | `<ad>_player`, `<ad>_audio` | Oynatıcı ve ses çıkışı |

---

> **Sonraki bölüm:** `07_PYGAME.md` — Oyun motoru, ekran yönetimi, ses, sprite ve klavye/fare kontrolleri.
