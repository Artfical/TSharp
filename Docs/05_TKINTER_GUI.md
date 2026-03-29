# T-Sharp (T#) — Tkinter GUI (Grafik Arayüz)

![Lisans](https://img.shields.io/badge/Lisans-GNU_AGPL_v3-red.svg)
![Sürüm](https://img.shields.io/badge/Sürüm-v4.1-blue.svg)
![Statü](https://img.shields.io/badge/Proje-Solo_Açık_Kaynak-green.svg)
![Derleyici](https://img.shields.io/badge/Derleyici-TCompile-yellow.svg)

---

## Başlamadan Önce — `kullan gui`

Tkinter modülünü aktive etmek için dosyanın **en başına** yazın:

```tsharp
kullan gui
```

> Tkinter Python ile birlikte gelir, ekstra kurulum gerekmez.
> PySide6 kullanmak istiyorsanız `kullan gui6` yazın — o ayrı bir bölümde anlatılacak.

---

## İçindekiler

1. [Pencere](#1-pencere)
2. [Etiket](#2-etiket)
3. [Buton](#3-buton)
4. [Giriş Kutusu](#4-giriş-kutusu)
5. [Metin Alanı](#5-metin-alanı)
6. [Onay Kutusu](#6-onay-kutusu)
7. [Radyo Buton](#7-radyo-buton)
8. [Combo Kutu](#8-combo-kutu)
9. [Liste Kutusu](#9-liste-kutusu)
10. [Kaydırıcı](#10-kaydırıcı)
11. [İlerleme Çubuğu](#11-i̇lerleme-çubuğu)
12. [Sayaç Kutu](#12-sayaç-kutu)
13. [Widget Değer Okuma ve Ayarlama](#13-widget-değer-okuma-ve-ayarlama)
14. [Widget Görünüm Ayarları](#14-widget-görünüm-ayarları)
15. [Canvas — Çizim Alanı](#15-canvas--çizim-alanı)
16. [Frame ve Ayırıcı](#16-frame-ve-ayırıcı)
17. [Menü](#17-menü)
18. [Notebook — Sekmeli Yapı](#18-notebook--sekmeli-yapı)
19. [Ağaç Görünümü](#19-ağaç-görünümü)
20. [Tablo](#20-tablo)
21. [Kaydırma Alanı](#21-kaydırma-alanı)
22. [Diyalog Kutuları](#22-diyalog-kutuları)
23. [Olay Bağlama](#23-olay-bağlama)
24. [Timer](#24-timer)
25. [Hızlı Başvuru Tablosu](#25-hızlı-başvuru-tablosu)

---

## 1. Pencere

Ana uygulama penceresi. Her GUI programı en az bir pencereyle başlar.

```tsharp
pencere <ad> "<baslik>" <genislik> <yukseklik>
```

Pencereyi açmak ve programı çalışır tutmak için en sona yazılır:

```tsharp
pencere_goster <pencere_adi>
```

Diğer pencere komutları:

```tsharp
pencere_baslik <pencere_adi> "<yeni_baslik>"
pencere_boyut  <pencere_adi> <genislik> <yukseklik>
pencere_renk   <pencere_adi> "<renk>"
pencere_kapat  <pencere_adi>
guncelle       <pencere_adi>    // döngü içinde ekranı tazeler
```

---

## 2. Etiket

Pencereye sabit metin yazmak için kullanılır.

```tsharp
etiket <ad> "<metin>" <pencere_adi>
```

Metni sonradan değiştirmek için `widget_ayarla` kullanılır.

---

## 3. Buton

Tıklanabilir düğme. İsteğe bağlı olarak bir fonksiyon bağlanabilir.

```tsharp
buton <ad> "<metin>" <pencere_adi> [fonksiyon_adi]
```

- `fonksiyon_adi` verilirse butona tıklandığında o fonksiyon çalışır.
- Fonksiyon T# `fonksiyon` komutuyla tanımlanmış olmalıdır.

---

## 4. Giriş Kutusu

Tek satır metin girişi için kullanılır.

```tsharp
giriskutusu <ad> <pencere_adi>
```

Değeri okumak için:

```tsharp
widget_deger <ad> <degisken_adi>
```

---

## 5. Metin Alanı

Çok satırlı metin girişi için kullanılır.

```tsharp
metin_alani <ad> <pencere_adi> [yukseklik] [genislik]
```

- `yukseklik` varsayılanı: `10` satır
- `genislik` varsayılanı: `50` karakter

Değeri okumak için `widget_deger`, yazmak için `widget_ayarla` kullanılır.

---

## 6. Onay Kutusu

İşaretlenebilir kutucuk. `dogru`/`yanlis` değer tutar.

```tsharp
onay_kutusu <ad> "<metin>" <pencere_adi>
```

Oluşturulduğunda iki değişken otomatik yaratılır:

| Değişken | İçerik |
|----------|--------|
| `<ad>` | `BooleanVar` — `dogru` veya `yanlis` |
| `<ad>_widget` | Widget nesnesinin kendisi |

Değeri okumak için:

```tsharp
widget_deger <ad> <degisken_adi>
```

---

## 7. Radyo Buton

Birden fazla seçenekten birini seçmek için kullanılır. Aynı gruptaki tüm radyo butonlar aynı `degisken_adi`'ni paylaşır.

```tsharp
radyo_buton <ad> "<metin>" <pencere_adi> <degisken_adi> [deger]
```

- `degisken_adi` tüm grupta aynı olmalıdır — bu aynı grubu oluşturur.
- `deger` seçildiğinde `degisken_adi`'ne atanacak değerdir. Verilmezse `<ad>` kullanılır.

Seçilen değeri okumak için:

```tsharp
widget_deger <degisken_adi> <sonuc>
```

---

## 8. Combo Kutu

Açılır liste (dropdown). Kullanıcı listeden bir değer seçer.

```tsharp
combo_kutu <ad> <pencere_adi> <liste_degiskeni>
```

Seçilen değeri okumak için `widget_deger` kullanılır.

---

## 9. Liste Kutusu

Kaydırılabilir liste. Tekli veya çoklu seçim desteklenir.

```tsharp
liste_kutusu <ad> <pencere_adi> ["tekli"|"coklu"]
```

- Varsayılan seçim modu: `tekli`
- Liste içeriğini doldurmak için `widget_ayarla <ad> <liste>` kullanılır.

---

## 10. Kaydırıcı

Belirli bir aralıkta değer seçmek için kullanılır (Scale).

```tsharp
kaydirici <ad> <pencere_adi> <min> <max> ["yatay"|"dikey"]
```

- Yön varsayılanı: `yatay`

---

## 11. İlerleme Çubuğu

0–100 arası doluluk gösterir (Progressbar).

```tsharp
ilerleme_cubugu <ad> <pencere_adi> [uzunluk_piksel]
```

- Varsayılan uzunluk: `200` piksel
- Değer atamak için: `widget_ayarla <ad> <sayi>`

---

## 12. Sayaç Kutu

Yukarı/aşağı ok butonuyla sayı girilir (Spinbox).

```tsharp
sayac_kutu <ad> <pencere_adi> [baslangic] [adim]
```

- `baslangic` varsayılanı: `0`
- `adim` varsayılanı: `1`

---

## 13. Widget Değer Okuma ve Ayarlama

### Değer Oku

Widget'ın mevcut değerini bir değişkene atar.

```tsharp
widget_deger <widget_adi> <degisken_adi>
```

Desteklenen widget'lar: `giriskutusu`, `metin_alani`, `kaydirici`, `combo_kutu`, `onay_kutusu`, `radyo_buton` grubu, `liste_kutusu`, `sayac_kutu`

### Değer Ayarla

Widget'ın değerini programdan değiştirir.

```tsharp
widget_ayarla <widget_adi> <deger>
```

| Widget | Davranış |
|--------|----------|
| `etiket` | Metni değiştirir |
| `giriskutusu` | İçeriği temizler, yeni değer yazar |
| `metin_alani` | İçeriği temizler, yeni değer yazar |
| `ilerleme_cubugu` | Doluluk yüzdesini ayarlar |
| `kaydirici` | Konumu ayarlar |
| `combo_kutu` | Seçili değeri ayarlar |
| `onay_kutusu` | `dogru`/`yanlis` atar |
| `liste_kutusu` | Listeyi tamamen değiştirir |
| `sayac_kutu` | Değeri ayarlar |

---

## 14. Widget Görünüm Ayarları

### Renk

```tsharp
widget_renk <ad> "<on_renk>" "<arka_renk>"
```

### Font

```tsharp
widget_font <ad> "<font_ailesi>" <boyut> ["normal"|"bold"|"italic"]
```

### Konum (Piksel)

```tsharp
widget_yerlestir <ad> <x> <y>
```

### Görünürlük ve Durum

```tsharp
widget_gizle       <ad>   // gizler
widget_goster      <ad>   // gösterir
widget_etkinlestir <ad>   // aktif eder
widget_devre_disi  <ad>   // pasif eder (gri)
widget_sil         <ad>   // tamamen yok eder
```

---

## 15. Canvas — Çizim Alanı

Şekil, çizgi ve metin çizmek için kullanılır.

### Oluşturma

```tsharp
canvas <ad> <pencere_adi> [genislik] [yukseklik] [arkaplan_rengi]
```

- Varsayılan boyut: `400x300`
- Varsayılan arka plan: `white`

### Çizim Komutları

```tsharp
canvas_cizgi       <canvas> <x1> <y1> <x2> <y2> [renk] [kalinlik]
canvas_dikdortgen  <canvas> <x1> <y1> <x2> <y2> [kenar_renk] [dolgu_renk]
canvas_oval        <canvas> <x1> <y1> <x2> <y2> [kenar_renk] [dolgu_renk]
canvas_metin       <canvas> <x> <y> "<metin>" [renk]
canvas_resim       <canvas> <x> <y> <resim_degiskeni>
```

> `canvas_oval` ile daire çizmek için x ve y aralıklarını eşit yapın.

Her çizim komutu sonrası `<canvas_adi>_son` değişkenine nesne ID'si atanır. Bu ID ile nesneyi silmek için:

```tsharp
canvas_nesne_sil <canvas> <nesne_id_degiskeni>
```

Tüm çizimi temizlemek için:

```tsharp
canvas_temizle <canvas>
```

---

## 16. Frame ve Ayırıcı

### Frame

Widget'ları gruplamak için kullanılan görünmez kap. Başka widget'lar `pencere_adi` yerine `frame_adi` yazarak frame'e bağlanabilir.

```tsharp
frame <ad> <pencere_adi>
```

### Ayırıcı

Yatay veya dikey görsel çizgi.

```tsharp
ayirici <ad> <pencere_adi> ["yatay"|"dikey"]
```

---

## 17. Menü

Pencereye üst menü çubuğu ekler.

```tsharp
// 1. Menü çubuğunu oluştur ve pencereye bağla
menu_cubugu <cubuk_adi> <pencere_adi>

// 2. Açılır menü başlığı ekle
menu_ekle <menu_adi> <cubuk_adi> "<baslik>"

// 3. Menüye tıklanabilir madde ekle
menu_madde_ekle <menu_adi> "<madde_basligi>" [fonksiyon_adi]

// 4. Maddeler arasına görsel ayırıcı ekle
menu_ayirici_ekle <menu_adi>
```

---

## 18. Notebook — Sekmeli Yapı

Birden fazla sekme içeren yapı.

```tsharp
// 1. Notebook oluştur
notebook <ad> <pencere_adi>

// 2. Sekme ekle — sekme aynı zamanda frame gibi davranır
notebook_sekme <notebook_adi> <sekme_adi> "<sekme_basligi>"
```

Sekmeye widget eklemek için `pencere_adi` yerine `<sekme_adi>` kullanılır:

```tsharp
etiket lbl "İçerik" <sekme_adi>
buton btn "Tıkla" <sekme_adi> fonksiyon_adi
```

---

## 19. Ağaç Görünümü

Hiyerarşik veri göstermek için kullanılır (Treeview).

```tsharp
// Oluştur
agac <ad> <pencere_adi>

// Düğüm ekle — kök için ust_node = ""
agac_ekle <agac_adi> "<ust_node_id>" "<metin>"
```

Her `agac_ekle` sonrası `<agac_adi>_son` değişkenine yeni düğümün ID'si atanır. Bu ID alt düğüm eklemek için `ust_node_id` olarak kullanılabilir.

---

## 20. Tablo

Sütun başlıklı veri tablosu (Treeview — headings modunda).

```tsharp
// 1. Tabloyu oluştur
tablo <ad> <pencere_adi>

// 2. Sütun ekle
tablo_sutun <tablo_adi> "<sutun_adi>" [genislik_piksel]

// 3. Satır ekle (liste olarak)
tablo_satir <tablo_adi> <liste_degiskeni>
```

---

## 21. Kaydırma Alanı

İçeriği çok uzun olan bölümler için kaydırma çubuğu eklenmiş alan.

```tsharp
kaydirma_alani <ad> <pencere_adi>
```

Oluşturulduktan sonra `<ad>` bir frame gibi davranır; widget'lar bu isme bağlanır:

```tsharp
etiket lbl1 "Satır 1" <kaydirma_alani_adi>
etiket lbl2 "Satır 2" <kaydirma_alani_adi>
```

---

## 22. Diyalog Kutuları

Kullanıcıya mesaj göstermek veya giriş almak için hazır pencereler.

```tsharp
// Bilgi mesajı
mesaj_kutusu "<baslik>", "<mesaj>"

// Uyarı mesajı
uyari_kutusu "<baslik>", "<mesaj>"

// Hata mesajı
hata_kutusu "<baslik>", "<mesaj>"

// Evet/Hayır sorusu — sonucu degisken_adi'ne atar (dogru/yanlis)
soru_kutusu <degisken_adi> "<baslik>" "<mesaj>"

// Metin girişi — sonucu degisken_adi'ne atar
giris_kutusu <degisken_adi> "<baslik>" "<mesaj>"

// Renk seçici — sonucu degisken_adi'ne atar
renk_sec <degisken_adi>

// Dosya seçici — sonucu degisken_adi'ne atar
dosya_sec <degisken_adi>

// Klasör seçici — sonucu degisken_adi'ne atar
klasor_sec <degisken_adi>

// Yazı tipi seçici — sonucu degisken_adi'ne atar
yazi_sec <degisken_adi>
```

---

## 23. Olay Bağlama

Bir widget'a klavye veya fare olayı bağlar.

```tsharp
olay_bagla <widget_adi> "<olay>" <fonksiyon_adi>
```

Sık kullanılan olay dizeleri:

| Olay | Anlamı |
|------|--------|
| `"<Button-1>"` | Sol fare tıklaması |
| `"<Button-3>"` | Sağ fare tıklaması |
| `"<Double-Button-1>"` | Çift tıklama |
| `"<Return>"` | Enter tuşu |
| `"<KeyPress>"` | Herhangi bir tuşa basış |
| `"<FocusIn>"` | Widget odak aldığında |
| `"<FocusOut>"` | Widget odak kaybettiğinde |

---

## 24. Timer

Belirli süre sonra bir fonksiyonu çalıştırır (tek seferlik).

```tsharp
timer_olustur <pencere_adi> <milisaniye> <fonksiyon_adi>
```

- `1000` ms = 1 saniye
- Tekrarlayan timer için fonksiyon içinde tekrar `timer_olustur` çağrılır.

---

## 25. Hızlı Başvuru Tablosu

| Komut | Açıklama |
|-------|----------|
| `kullan gui` | Tkinter modülünü aktive eder |
| `pencere <ad> "<baslik>" <g> <y>` | Pencere oluşturur |
| `pencere_goster <ad>` | Pencereyi açar (mainloop) |
| `pencere_baslik <ad> "<baslik>"` | Başlık değiştirir |
| `pencere_boyut <ad> <g> <y>` | Boyut değiştirir |
| `pencere_renk <ad> "<renk>"` | Arka plan rengi |
| `pencere_kapat <ad>` | Pencereyi kapatır |
| `guncelle <ad>` | Ekranı tazeler |
| `etiket <ad> "<metin>" <pencere>` | Metin etiketi |
| `buton <ad> "<metin>" <pencere> [fonk]` | Buton |
| `giriskutusu <ad> <pencere>` | Tek satır giriş |
| `metin_alani <ad> <pencere> [y] [g]` | Çok satır giriş |
| `onay_kutusu <ad> "<metin>" <pencere>` | Checkbox |
| `radyo_buton <ad> "<metin>" <pencere> <grup> [deger]` | Radio button |
| `combo_kutu <ad> <pencere> <liste>` | Dropdown |
| `liste_kutusu <ad> <pencere> [mod]` | Liste kutusu |
| `kaydirici <ad> <pencere> <min> <max> [yon]` | Slider |
| `ilerleme_cubugu <ad> <pencere> [uzunluk]` | Progress bar |
| `sayac_kutu <ad> <pencere> [bas] [adim]` | Spinbox |
| `widget_deger <widget> <degisken>` | Değer okur |
| `widget_ayarla <widget> <deger>` | Değer atar |
| `widget_renk <widget> "<on>" "<arka>"` | Renk ayarlar |
| `widget_font <widget> "<aile>" <boyut> [stil]` | Font ayarlar |
| `widget_yerlestir <widget> <x> <y>` | Piksel konumu |
| `widget_gizle <widget>` | Gizler |
| `widget_goster <widget>` | Gösterir |
| `widget_etkinlestir <widget>` | Aktif eder |
| `widget_devre_disi <widget>` | Pasif eder |
| `widget_sil <widget>` | Yok eder |
| `canvas <ad> <pencere> [g] [y] [renk]` | Çizim alanı |
| `canvas_cizgi <c> <x1> <y1> <x2> <y2> [renk] [kal]` | Çizgi |
| `canvas_dikdortgen <c> <x1> <y1> <x2> <y2> [k] [d]` | Dikdörtgen |
| `canvas_oval <c> <x1> <y1> <x2> <y2> [k] [d]` | Oval/Daire |
| `canvas_metin <c> <x> <y> "<metin>" [renk]` | Metin |
| `canvas_temizle <c>` | Tümünü siler |
| `canvas_nesne_sil <c> <id>` | Tek nesne siler |
| `frame <ad> <pencere>` | Görünmez grup kabı |
| `ayirici <ad> <pencere> [yon]` | Görsel çizgi |
| `menu_cubugu <ad> <pencere>` | Menü çubuğu |
| `menu_ekle <ad> <cubuk> "<baslik>"` | Açılır menü |
| `menu_madde_ekle <menu> "<baslik>" [fonk]` | Menü maddesi |
| `menu_ayirici_ekle <menu>` | Menü ayırıcısı |
| `notebook <ad> <pencere>` | Sekmeli yapı |
| `notebook_sekme <nb> <ad> "<baslik>"` | Sekme ekler |
| `agac <ad> <pencere>` | Ağaç görünümü |
| `agac_ekle <agac> "<ust>" "<metin>"` | Düğüm ekler |
| `tablo <ad> <pencere>` | Tablo oluşturur |
| `tablo_sutun <tablo> "<ad>" [genislik]` | Sütun ekler |
| `tablo_satir <tablo> <liste>` | Satır ekler |
| `kaydirma_alani <ad> <pencere>` | Scroll alanı |
| `mesaj_kutusu "<baslik>", "<mesaj>"` | Bilgi diyaloğu |
| `uyari_kutusu "<baslik>", "<mesaj>"` | Uyarı diyaloğu |
| `hata_kutusu "<baslik>", "<mesaj>"` | Hata diyaloğu |
| `soru_kutusu <d> "<baslik>" "<mesaj>"` | Evet/Hayır |
| `giris_kutusu <d> "<baslik>" "<mesaj>"` | Metin girişi |
| `renk_sec <degisken>` | Renk seçici |
| `dosya_sec <degisken>` | Dosya seçici |
| `klasor_sec <degisken>` | Klasör seçici |
| `yazi_sec <degisken>` | Yazı tipi seçici |
| `olay_bagla <widget> "<olay>" <fonk>` | Olay bağlar |
| `timer_olustur <pencere> <ms> <fonk>` | Zamanlayıcı |

---

> **Sonraki bölüm:** `06_PYSIDE6_GUI.md` — Qt6 tabanlı profesyonel arayüz geliştirme.
