# T-Sharp (T#) — Pygame (Oyun Motoru)

![Lisans](https://img.shields.io/badge/Lisans-GNU_AGPL_v3-red.svg)
![Sürüm](https://img.shields.io/badge/Sürüm-v4.1-blue.svg)
![Statü](https://img.shields.io/badge/Proje-Solo_Açık_Kaynak-green.svg)
![Derleyici](https://img.shields.io/badge/Derleyici-TCompile-yellow.svg)

---

## Başlamadan Önce — `kullan oyun`

Pygame modülünü aktive etmek için dosyanın **en başına** yazın:

```tsharp
kullan oyun
```

> **Gereksinim:** `pip install pygame`

---

## İçindekiler

1. [Başlatma ve Kapatma](#1-başlatma-ve-kapatma)
2. [Ekran Yönetimi](#2-ekran-yönetimi)
3. [Olay Sistemi](#3-olay-sistemi)
4. [Çizim Komutları](#4-çizim-komutları)
5. [Resim ve Yüzey İşlemleri](#5-resim-ve-yüzey-işlemleri)
6. [Metin Yazma](#6-metin-yazma)
7. [Ses Efektleri](#7-ses-efektleri)
8. [Müzik](#8-müzik)
9. [Klavye Kontrolü](#9-klavye-kontrolü)
10. [Fare Kontrolü](#10-fare-kontrolü)
11. [Saat ve FPS](#11-saat-ve-fps)
12. [Renk İşlemleri](#12-renk-işlemleri)
13. [Çarpışma Tespiti](#13-çarpışma-tespiti)
14. [Sprite Sistemi](#14-sprite-sistemi)
15. [Piksel İşlemleri](#15-piksel-işlemleri)
16. [Hazır Sabitler](#16-hazır-sabitler)
17. [Hızlı Başvuru Tablosu](#17-hızlı-başvuru-tablosu)

---

## 1. Başlatma ve Kapatma

```tsharp
oyun_baslat    // pygame ve ses sistemini başlatır, sabitleri yükler
oyun_kapat     // pygame ve ses sistemini kapatır
```

`oyun_baslat` çağrıldığında aşağıdaki sabitler otomatik olarak değişken olarak tanımlanır:
- Olay tipleri: `CIKIS`, `KLAVYE_ASAGI`, `KLAVYE_YUKARI`, `FARE_ASAGI`, `FARE_YUKARI`, `FARE_HAREKET`
- Tuş kodları: `K_ESC`, `K_BOSLUK`, `K_ENTER`, `K_SOL`, `K_SAG`, `K_YUKARI`, `K_ASAGI`, `K_A`–`K_Z`, `K_0`–`K_9`, `K_F1`–`K_F5`, `K_CTRL`, `K_SHIFT`, `K_ALT`, `K_TAB`, `K_GERI`, `K_SIL`
- Renk sabitleri: `SIYAH`, `BEYAZ`, `KIRMIZI`, `YESIL`, `MAVI`, `SARI`, `TURUNCU`, `MOR`, `PEMBE`, `GRI`, `ACIK_GRI`, `KOYU_GRI`, `CAMGOBEGI`, `LACIVERT`, `KAHVERENGI`

---

## 2. Ekran Yönetimi

### Ekran Oluştur

```tsharp
oyun_ekran <ad> <genislik> <yukseklik> [bayraklar]
```

Bayrak seçenekleri (opsiyonel):
- `tam_ekran` — tam ekran mod
- `yeniden_boyutlandir` — pencere boyutu değiştirilebilir
- `cercevesiz` — çerçevesiz pencere

### Pencere Başlığı ve Simgesi

```tsharp
oyun_baslik "<baslik>"
oyun_simge <resim_adi>    // önce resim_yukle ile yüklenmiş olmalı
```

### Ekranı Doldur ve Güncelle

```tsharp
ekran_doldur <ekran_adi> <renk>          // tüm ekranı tek renkle doldur
ekran_guncelle                            // tüm ekranı yenile (flip)
ekran_guncelle_bolge <x> <y> <g> <y2>   // sadece belirli bölgeyi yenile
```

### Ekran Bilgisi ve Tam Ekran

```tsharp
ekran_bilgi <degisken_adi>   // <d>_genislik ve <d>_yukseklik değişkenlerini doldurur
tam_ekran dogru              // tam ekrana geç
tam_ekran yanlis             // pencere moduna dön
pencere_konumu <x> <y>       // pencereyi belirtilen konuma taşı
```

---

## 3. Olay Sistemi

Oyun döngüsünün her iterasyonunda olaylar okunup işlenmelidir.

### Tüm Olayları Oku

```tsharp
olaylari_isle
```

Bu komut olay listesini `_son_olaylar` değişkenine atar.

### Belirli Olay Tipini Filtrele

```tsharp
olay_kontrol <degisken_adi> <olay_tipi>
```

`olay_tipi` olarak `CIKIS`, `KLAVYE_ASAGI`, `FARE_ASAGI` gibi sabitler kullanılır.

### Tipik Oyun Döngüsü Yapısı

```tsharp
dongu oyun_devam:
    olaylari_isle
    olay_kontrol cikis_olaylari CIKIS
    eger uzunluk(cikis_olaylari) buyuktur 0:
        degisken oyun_devam = yanlis
    son

    // güncelleme mantığı buraya

    ekran_doldur ekran SIYAH
    // çizim komutları buraya
    ekran_guncelle
    saat_tikla saat 60
son
```

---

## 4. Çizim Komutları

Tüm çizim komutları bir **ekran adı** ve **renk** alır. Renk olarak hazır sabitler (`KIRMIZI`, `MAVI` vb.) veya `renk_olustur` ile tanımlanmış değişkenler kullanılabilir.

### Çizgi

```tsharp
ciz_cizgi <ekran> <renk> <x1> <y1> <x2> <y2> [kalinlik]
```

### Dikdörtgen (Kenar)

```tsharp
ciz_dikdortgen <ekran> <renk> <x> <y> <genislik> <yukseklik> [kalinlik]
```

### Dikdörtgen (Dolu)

```tsharp
ciz_dolu_dikdortgen <ekran> <renk> <x> <y> <genislik> <yukseklik>
```

### Çember (Kenar)

```tsharp
ciz_cember <ekran> <renk> <merkez_x> <merkez_y> <yaricap> [kalinlik]
```

### Çember (Dolu)

```tsharp
ciz_dolu_cember <ekran> <renk> <merkez_x> <merkez_y> <yaricap>
```

### Elips

```tsharp
ciz_elips <ekran> <renk> <x> <y> <genislik> <yukseklik> [kalinlik]
```

### Çokgen

```tsharp
ciz_cokgen <ekran> <renk> <noktalar_listesi> [kalinlik]
// noktalar_listesi: [[x1,y1],[x2,y2],...] formatında liste
// kalinlik=0 → dolu çokgen
```

### Nokta

```tsharp
ciz_nokta <ekran> <renk> <x> <y>
```

### Yay

```tsharp
ciz_yay <ekran> <renk> <x> <y> <genislik> <yukseklik> <baslangic_aci> <bitis_aci> [kalinlik]
// açılar derece cinsindendir
```

---

## 5. Resim ve Yüzey İşlemleri

### Resim Yükleme ve Çizme

```tsharp
resim_yukle <ad> "<dosya_yolu>"    // PNG, JPG, BMP desteklenir
resim_ciz <ekran> <resim_adi> <x> <y>
resim_kaydet <yuzey_adi> "<dosya_yolu>"
```

### Resim Dönüşümleri

```tsharp
resim_olcekle <kaynak> <hedef> <genislik> <yukseklik>
resim_dondur  <kaynak> <hedef> <aci>            // derece cinsinden, saat yönü tersine
resim_cevir   <kaynak> <hedef> <yatay> <dikey>  // dogru/yanlis
```

### Yüzey İşlemleri

```tsharp
yuzey_olustur <ad> <genislik> <yukseklik> [alfa]   // alfa yazılırsa şeffaflık destekli
yuzeyi_yukle  <ad> "<dosya_yolu>"                   // dosyadan yüzey yükler
yuzey_doldur  <ad> <renk>                           // yüzeyi renkle doldurur
yuzey_kopyala <hedef> <kaynak> [x] [y]              // kaynağı hedefe yapıştırır (blit)
yuzey_effekti <ad> <efekt>                          // efekt: "donustur_alfa" veya "donustur"
```

---

## 6. Metin Yazma

### Yazı Tipi Yükle

```tsharp
yazi_tipi_yukle <ad> "<font_adi_veya_dosya>" <boyut>
```

- `.ttf` veya `.otf` uzantısıyla dosya yolu verilirse dosyadan yükler.
- Uzantı yoksa sistem fontu olarak arar.
- Font bulunamazsa varsayılan Pygame fontu kullanılır.

### Metin Yaz

```tsharp
metin_yaz <ekran> "<metin>" <renk> <x> <y> [font_adi]
```

- Metin **x koordinatına göre ortalanarak** çizilir.
- `font_adi` verilmezse varsayılan 24pt font kullanılır.
- Çizimden sonra `_metin_boyut` değişkenine metnin `(genislik, yukseklik)` değeri atanır.

---

## 7. Ses Efektleri

Kısa ses efektleri için kullanılır (WAV, OGG).

```tsharp
ses_yukle <ad> "<dosya_yolu>"
ses_oynat <ad> [tekrar_sayisi]    // tekrar=0 bir kez, -1 sonsuz döngü
ses_durdur <ad>
ses_devam <ad>
ses_ses_duzeyi <ad> <duzey>       // 0.0 (sessiz) – 1.0 (tam ses)
```

`ses_oynat` sonrası `<ad>_kanal` değişkenine kanal nesnesi atanır.

---

## 8. Müzik

Uzun arkaplan müziği için kullanılır (MP3, OGG, WAV).

```tsharp
muzik_yukle "<dosya_yolu>"
muzik_oynat                       // yüklü müziği oynat
muzik_durdur                      // duraklat (devam ettirilebilir)
muzik_devam                       // duraklatılmış müziği devam ettir
muzik_dur                         // tamamen durdur
muzik_ses_duzeyi <duzey>          // 0.0 – 1.0
muzik_tekrar <sayi>               // -1 = sonsuz, 0 = bir kez
```

---

## 9. Klavye Kontrolü

### Anlık Tuş Durumu

```tsharp
tuslar_oku <degisken_adi>
```

Tüm tuşların basılı olup olmadığını içeren bir dizi atar. Tuş kontrolü için:

```tsharp
tus_basili_mi <sonuc_degiskeni> <tus_sabiti>
```

```tsharp
tus_basili_mi sola_gidiyor K_SOL
eger sola_gidiyor:
    x -= 5
son
```

### Olay Tabanlı Tuş Kontrolü

Tek seferlik tuş basışları için `olaylari_isle` + `olay_kontrol` kullanılır:

```tsharp
olaylari_isle
olay_kontrol tus_olaylari KLAVYE_ASAGI
her olay icinde tus_olaylari:
    // olay değişkeni tuş kodunu içerir
    eger olay esittir K_ESC:
        dur
    son
son
```

---

## 10. Fare Kontrolü

### Fare Konumu

```tsharp
fare_konum <degisken_adi>
```

Oluşturulan değişkenler:

| Değişken | İçerik |
|----------|--------|
| `<ad>` | `[x, y]` listesi |
| `<ad>_x` | X koordinatı |
| `<ad>_y` | Y koordinatı |

### Fare Düğme Durumu

```tsharp
fare_dugme <degisken_adi>
```

| Değişken | İçerik |
|----------|--------|
| `<ad>` | `[sol, orta, sag]` listesi |
| `<ad>_sol` | Sol tuş basılı mı? (`dogru`/`yanlis`) |
| `<ad>_orta` | Orta tuş basılı mı? |
| `<ad>_sag` | Sağ tuş basılı mı? |

### Fare İmleç Görünürlüğü

```tsharp
fare_goster dogru    // imleci göster
fare_gizle          // imleci gizle
```

---

## 11. Saat ve FPS

```tsharp
saat_olustur <ad>              // yeni saat nesnesi oluşturur
saat_tikla <ad> <hedef_fps>    // oyun döngüsünü hedef FPS'e kilitler
fps_al <degisken> [saat_adi]   // mevcut FPS'i okur
```

- `saat_tikla` her döngü sonuna yazılır.
- `saat_adi` verilmezse `oyun_baslat` ile oluşturulan varsayılan saat kullanılır.

---

## 12. Renk İşlemleri

### Özel Renk Oluştur

```tsharp
renk_olustur <ad> <r> <g> <b> [a]
// r, g, b: 0–255 arası tam sayı
// a (alfa): 0–255, verilmezse 255 (tam opak)
```

### Renk Karıştır

```tsharp
renk_karistir <sonuc> <renk1> <renk2> [oran]
// oran: 0.0–1.0, renk1'den renk2'ye geçiş oranı
// varsayılan: 0.5 (eşit karışım)
```

---

## 13. Çarpışma Tespiti

### Dikdörtgen Çarpışma

```tsharp
carpisma_dikdortgen <sonuc> <x1> <y1> <g1> <h1> <x2> <y2> <g2> <h2>
```

İki dikdörtgenin kesişip kesişmediğini kontrol eder. Sonuç `dogru`/`yanlis` olarak `<sonuc>` değişkenine atanır.

### Sprite Çarpışma

```tsharp
carpisma_kontrol <sonuc> <sprite1_adi> <sprite2_adi>
```

İki sprite nesnesinin `rect` alanlarını karşılaştırır.

---

## 14. Sprite Sistemi

Sprite grubu, birden fazla oyun nesnesini toplu olarak yönetmek için kullanılır.

```tsharp
sprite_grubu_olustur <ad>          // yeni boş sprite grubu
sprite_ekle <grup_adi> <sprite>    // gruba sprite ekler
sprite_ciz <grup_adi> <ekran>      // gruptaki tüm sprite'ları çizer
sprite_guncelle <grup_adi>         // gruptaki tüm sprite'ların update() metodunu çağırır
```

---

## 15. Piksel İşlemleri

Yüzeydeki tek tek pikselleri okuyup yazmak için kullanılır.

```tsharp
piksel_al <degisken> <yuzey_adi> <x> <y>    // pikselin RGBA rengini okur
piksel_yaz <yuzey_adi> <x> <y> <renk>       // piksele renk yazar
maske_olustur <ad> <yuzey_adi>              // piksel maskesi oluşturur
```

---

## 16. Hazır Sabitler

`oyun_baslat` çağrıldığında aşağıdaki değişkenler otomatik tanımlanır:

### Olay Tipleri

| Sabit | Anlamı |
|-------|--------|
| `CIKIS` | Pencere kapatma butonu |
| `KLAVYE_ASAGI` | Tuşa basıldı |
| `KLAVYE_YUKARI` | Tuş bırakıldı |
| `FARE_ASAGI` | Fare tuşuna basıldı |
| `FARE_YUKARI` | Fare tuşu bırakıldı |
| `FARE_HAREKET` | Fare hareket etti |

### Tuş Sabitleri

| Sabit | Tuş |
|-------|-----|
| `K_ESC` | Escape |
| `K_BOSLUK` | Boşluk |
| `K_ENTER` | Enter |
| `K_SOL` | Sol ok |
| `K_SAG` | Sağ ok |
| `K_YUKARI` | Yukarı ok |
| `K_ASAGI` | Aşağı ok |
| `K_A` – `K_Z` | Harf tuşları |
| `K_0` – `K_9` | Rakam tuşları |
| `K_F1` – `K_F5` | Fonksiyon tuşları |
| `K_CTRL` | Sol Ctrl |
| `K_SHIFT` | Sol Shift |
| `K_ALT` | Sol Alt |
| `K_TAB` | Tab |
| `K_GERI` | Backspace |
| `K_SIL` | Delete |

### Renk Sabitleri

| Sabit | RGB |
|-------|-----|
| `SIYAH` | (0, 0, 0) |
| `BEYAZ` | (255, 255, 255) |
| `KIRMIZI` | (255, 0, 0) |
| `YESIL` | (0, 255, 0) |
| `MAVI` | (0, 0, 255) |
| `SARI` | (255, 255, 0) |
| `TURUNCU` | (255, 165, 0) |
| `MOR` | (128, 0, 128) |
| `PEMBE` | (255, 192, 203) |
| `GRI` | (128, 128, 128) |
| `ACIK_GRI` | (211, 211, 211) |
| `KOYU_GRI` | (64, 64, 64) |
| `CAMGOBEGI` | (0, 255, 255) |
| `LACIVERT` | (0, 0, 128) |
| `KAHVERENGI` | (139, 69, 19) |

---

## 17. Hızlı Başvuru Tablosu

| Komut | Açıklama |
|-------|----------|
| `kullan oyun` | Pygame modülünü aktive eder |
| `oyun_baslat` | Pygame + ses başlatır, sabitleri yükler |
| `oyun_kapat` | Pygame + ses kapatır |
| `oyun_ekran <ad> <g> <y> [bayrak]` | Oyun ekranı oluşturur |
| `oyun_baslik "<baslik>"` | Pencere başlığını ayarlar |
| `oyun_simge <resim>` | Pencere simgesini ayarlar |
| `ekran_doldur <ekran> <renk>` | Ekranı renkle doldurur |
| `ekran_guncelle` | Ekranı yeniler (flip) |
| `ekran_guncelle_bolge <x> <y> <g> <y2>` | Bölgeyi yeniler |
| `ekran_bilgi <d>` | Ekran boyutunu okur |
| `tam_ekran <dogru/yanlis>` | Tam ekran modu |
| `pencere_konumu <x> <y>` | Pencereyi taşır |
| `olaylari_isle` | Olay listesini okur |
| `olay_kontrol <d> <tip>` | Olayları tipine göre filtreler |
| `ciz_cizgi <e> <r> <x1> <y1> <x2> <y2> [k]` | Çizgi çizer |
| `ciz_dikdortgen <e> <r> <x> <y> <g> <h> [k]` | Dikdörtgen kenar |
| `ciz_dolu_dikdortgen <e> <r> <x> <y> <g> <h>` | Dikdörtgen dolu |
| `ciz_cember <e> <r> <x> <y> <yc> [k]` | Çember kenar |
| `ciz_dolu_cember <e> <r> <x> <y> <yc>` | Çember dolu |
| `ciz_elips <e> <r> <x> <y> <g> <h> [k]` | Elips |
| `ciz_cokgen <e> <r> <noktalar> [k]` | Çokgen |
| `ciz_nokta <e> <r> <x> <y>` | Nokta |
| `ciz_yay <e> <r> <x> <y> <g> <h> <bas> <bit> [k]` | Yay |
| `resim_yukle <ad> "<yol>"` | Resim yükler |
| `resim_ciz <ekran> <resim> <x> <y>` | Resim çizer |
| `resim_olcekle <k> <h> <g> <y>` | Ölçekler |
| `resim_dondur <k> <h> <aci>` | Döndürür |
| `resim_cevir <k> <h> <yatay> <dikey>` | Çevirir |
| `resim_kaydet <yuzey> "<yol>"` | Kaydeder |
| `yuzey_olustur <ad> <g> <y> [alfa]` | Yüzey oluşturur |
| `yuzeyi_yukle <ad> "<yol>"` | Dosyadan yüzey yükler |
| `yuzey_doldur <ad> <renk>` | Yüzeyi doldurur |
| `yuzey_kopyala <hedef> <kaynak> [x] [y]` | Blit işlemi |
| `yuzey_effekti <ad> <efekt>` | Dönüşüm efekti |
| `yazi_tipi_yukle <ad> "<font>" <boyut>` | Yazı tipi yükler |
| `metin_yaz <e> "<metin>" <r> <x> <y> [font]` | Metin yazar (x'e ortalı) |
| `ses_yukle <ad> "<yol>"` | Ses efekti yükler |
| `ses_oynat <ad> [tekrar]` | Ses oynatır |
| `ses_durdur <ad>` | Ses efektini durdurur |
| `ses_devam <ad>` | Devam ettirir |
| `ses_ses_duzeyi <ad> <0.0-1.0>` | Ses seviyesi |
| `muzik_yukle "<yol>"` | Müzik yükler |
| `muzik_oynat` | Müzik oynatır |
| `muzik_durdur` | Müziği duraklatır |
| `muzik_devam` | Müziği devam ettirir |
| `muzik_dur` | Müziği tamamen durdurur |
| `muzik_ses_duzeyi <0.0-1.0>` | Müzik sesi |
| `muzik_tekrar <sayi>` | Tekrar sayısı (-1=sonsuz) |
| `tuslar_oku <d>` | Tüm tuş durumlarını okur |
| `tus_basili_mi <d> <tus>` | Tek tuş kontrolü |
| `fare_konum <d>` | Fare konumunu okur |
| `fare_dugme <d>` | Fare tuş durumlarını okur |
| `fare_goster dogru` | İmleci gösterir |
| `fare_gizle` | İmleci gizler |
| `saat_olustur <ad>` | Saat nesnesi oluşturur |
| `saat_tikla <ad> <fps>` | FPS kilitler |
| `fps_al <d> [saat]` | Anlık FPS okur |
| `renk_olustur <ad> <r> <g> <b> [a]` | Renk oluşturur |
| `renk_karistir <s> <r1> <r2> [oran]` | Renk karıştırır |
| `carpisma_dikdortgen <s> <x1>...<h2>` | Dikdörtgen çarpışma |
| `carpisma_kontrol <s> <sp1> <sp2>` | Sprite çarpışma |
| `sprite_grubu_olustur <ad>` | Sprite grubu oluşturur |
| `sprite_ekle <grup> <sprite>` | Gruba sprite ekler |
| `sprite_ciz <grup> <ekran>` | Grubu çizer |
| `sprite_guncelle <grup>` | Grubu günceller |
| `piksel_al <d> <yuzey> <x> <y>` | Piksel rengi okur |
| `piksel_yaz <yuzey> <x> <y> <renk>` | Piksel yazar |
| `maske_olustur <ad> <yuzey>` | Piksel maskesi oluşturur |

---

> **Sonraki bölüm:** `08_RaspberryPI_GPIO.md` — Raspberry PI serisi cihazlar üzerinde bulunan GPIO pinlerinin kontolü.
