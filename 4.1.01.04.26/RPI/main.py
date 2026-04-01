import re
import sys
import math
import random
import time
import numpy as np

# Tkinter import
try:
    import tkinter as tk
    from tkinter import messagebox, simpledialog, ttk, filedialog, colorchooser, font as tkfont
    TKINTER_AVAILABLE = True
except ImportError:
    TKINTER_AVAILABLE = False
    print("UYARI: tkinter bulunamadı. GUI özellikleri devre dışı.")

# PySide6 import
PYSIDE6_AVAILABLE = False
WEBENGINE_AVAILABLE = False
MULTIMEDIA_AVAILABLE = False
CHARTS_AVAILABLE = False

try:
    from PySide6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QPushButton, QLabel, QLineEdit,
        QTextEdit, QCheckBox, QRadioButton, QComboBox, QListWidget, QTableWidget,
        QTreeWidget, QTabWidget, QSlider, QProgressBar, QSpinBox, QDoubleSpinBox,
        QDateEdit, QTimeEdit, QDateTimeEdit, QCalendarWidget, QDial, QLCDNumber,
        QMessageBox, QFileDialog, QColorDialog, QFontDialog, QInputDialog,
        QVBoxLayout, QHBoxLayout, QGridLayout, QFormLayout, QGroupBox,
        QScrollArea, QSplitter, QStackedWidget, QToolBar, QStatusBar,
        QMenuBar, QMenu, QToolButton, QTableWidgetItem, QTreeWidgetItem,
        QListWidgetItem, QFrame, QSizePolicy
    )
    from PySide6.QtCore import (
        Qt, QTimer, QThread, Signal, Slot, QUrl, QSize, QRect, QPoint,
        QDateTime, QDate, QTime, QPropertyAnimation, QEasingCurve
    )
    from PySide6.QtGui import (
        QIcon, QPixmap, QImage, QFont, QColor, QPalette, QAction,
        QPainter, QPen, QBrush, QMovie
    )
    PYSIDE6_AVAILABLE = True
    try:
        from PySide6.QtWebEngineWidgets import QWebEngineView
        WEBENGINE_AVAILABLE = True
    except ImportError:
        WEBENGINE_AVAILABLE = False
    try:
        from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
        from PySide6.QtMultimediaWidgets import QVideoWidget
        MULTIMEDIA_AVAILABLE = True
    except ImportError:
        MULTIMEDIA_AVAILABLE = False
    try:
        from PySide6.QtCharts import QChart, QChartView, QLineSeries, QPieSeries, QBarSet, QBarSeries
        CHARTS_AVAILABLE = True
    except ImportError:
        CHARTS_AVAILABLE = False
except ImportError:
    PYSIDE6_AVAILABLE = False

# Pygame import - "Hello from pygame community" mesajini bastir
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'


try:
    import pygame
    import pygame.mixer
    import pygame.font
    import pygame.draw
    import pygame.image
    import pygame.transform
    import pygame.event
    import pygame.key
    import pygame.mouse
    import pygame.time
    import pygame.display
    import pygame.sprite
    import pygame.surfarray
    import pygame.mask
    import pygame.camera
    import pygame.locals
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False
    print("UYARI: pygame bulunamadı. Yüklemek için: pip install pygame")

# OpenCV import
try:
    import cv2
    OPENCV_AVAILABLE = True
except ImportError:
    OPENCV_AVAILABLE = False

# lgpio import
try:
    import lgpio
    LGPIO_AVAILABLE = True
except ImportError:
    LGPIO_AVAILABLE = False
    class _GPIOStub:
        OUTPUT = 1
        INPUT = 0
        HIGH = 1
        LOW = 0
        BCM = 11
        BOARD = 10
        PUD_UP = 22
        PUD_DOWN = 21
        PUD_OFF = 20
        RISING = 31
        FALLING = 32
        BOTH = 33
        _pins = {}
        _pwm = {}
        def gpiochip_open(self, chip): return 0
        def gpiochip_close(self, handle): pass
        def gpio_claim_output(self, handle, pin, level=0): self._pins[pin] = {'mod': 'cikis', 'deger': level}
        def gpio_claim_input(self, handle, pin, lflags=0): self._pins[pin] = {'mod': 'giris', 'deger': 0}
        def gpio_write(self, handle, pin, level):
            if pin in self._pins: self._pins[pin]['deger'] = level
        def gpio_read(self, handle, pin):
            if pin in self._pins: return self._pins[pin].get('deger', 0)
            return 0
        def tx_pwm(self, handle, pin, freq, duty, pulse_offset=0, pulse_cycles=0): self._pwm[pin] = {'freq': freq, 'duty': duty}
        def i2c_open(self, gpioDev, i2cAddr, i2cFlags=0): return 0
        def i2c_close(self, handle): pass
        def i2c_write_device(self, handle, data): pass
        def i2c_read_device(self, handle, count): return (count, bytes(count))
        def spi_open(self, spiDev, spiChan, spiBaud, spiFlags=0): return 0
        def spi_close(self, handle): pass
        def spi_xfer(self, handle, data): return (len(data), bytes(len(data)))
        def callback(self, handle, pin, edge, func): return None
        def cancel(self, cb): pass
    lgpio = _GPIOStub()
    print("UYARI: lgpio bulunamadı. GPIO stub modu etkin.")

# requests import
REQUESTS_AVAILABLE = False
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    print("UYARI: requests bulunamadı. Yüklemek için: pip install requests")

import zipfile

import hashlib
import base64
import hmac
import struct


def normalize_satir(satir):
    """
    Türkçe karakterli komutları ASCII karşılıklarına çevirir.
    Hem 'yazdır' hem 'yazdir', hem 'değişken' hem 'degisken' çalışır.
    Sadece komut kelimesini değiştirir, içeriği korur.
    """
    s = satir.strip()
    # (türkçe_komut, ascii_karşılık) - uzundan kısaya sıralı
    eslesme = [
        ('değişken ',   'degisken '),
        ('yazdır ',     'yazdir '),
        ('yazdır',      'yazdir'),
        ('döngü ',      'dongu '),
        ('eğer ',       'eger '),
        ('döndür ',     'dondur '),
        ('değilse:',    'degilse:'),
        ('değilse',     'degilse'),
        ('sözlük ',     'sozluk '),
        ('dön ',        'don '),
        ('her ',        'her '),       # zaten ASCII uyumlu ama explicit
        ('girdi ',      'girdi '),
        ('liste ',      'liste '),
        ('fonksiyon ',  'fonksiyon '), # zaten OK
        # Kısa alternatifler
        ('yaz ',        'yazdir '),
        ('yaz"',        'yazdir "'),   # yaz"merhaba" desteği
        ("yaz'",        "yazdir '"),
    ]
    for turkce, ascii_k in eslesme:
        if s.startswith(turkce):
            kalan = s[len(turkce):]
            return ascii_k + kalan
    return s


def parse_qt_command(satir):
    """
    Komutu token listesine ayirir.
    Kural:
      - "..." -> tek token (string literal)
      - (...) -> tek token (fonksiyon cagrisi veya parantezli ifade)
      - Bosluklarda bol
    Ornek:
      ekran BEYAZ yaziya(yuvarla(fps)) 10 10 yazi
      -> ['ekran', 'BEYAZ', 'yaziya(yuvarla(fps))', '10', '10', 'yazi']
    """
    parcalar = []
    current = ""
    in_string = False
    string_char = None
    paren_depth = 0
    for char in satir:
        if in_string:
            current += char
            if char == string_char:
                in_string = False
        elif char in ('"', "'"):
            in_string = True
            string_char = char
            current += char
        elif char == '(':
            paren_depth += 1
            current += char
        elif char == ')':
            paren_depth -= 1
            current += char
        elif char == ' ' and paren_depth == 0:
            if current.strip():
                parcalar.append(current.strip())
            current = ""
        else:
            current += char
    if current.strip():
        parcalar.append(current.strip())
    return parcalar


# Blok başlatan anahtar kelimeler
BLOK_BASLATAN = ('eger ', 'dongu ', 'her ', 'fonksiyon ', 'eğer ', 'döngü ')
BLOK_KAPATAN = 'son'


class TSharp:
    """
    TSharp Turkce Programlama Dili Yorumlayicisi v4.1
    - Interaktif modda blok komut destegi (eger/dongu/fonksiyon)
    - Duzeltilmis yazdir, degisken komutlari
    - Gelismis hata yonetimi
    """
    def _temiz_metin_yap(self, deger):
        """
        Liste, tuple veya sözlük gibi verileri ekrana basarken
        köşeli parantez, tırnak ve virgüllerden arındırır.
        """
        if isinstance(deger, (list, tuple)):
            # Liste ise içindeki elemanları aralarında boşluk bırakarak birleştir
            return ' '.join(self._temiz_metin_yap(e) for e in deger)
        elif isinstance(deger, dict):
            # Sözlük ise anahtar:değer şeklinde boşlukla birleştir
            return ' '.join(f"{self._temiz_metin_yap(k)}:{self._temiz_metin_yap(v)}" for k, v in deger.items())
        elif isinstance(deger, str):
            return deger
        elif deger is None:
            return "hic"
        elif isinstance(deger, bool):
            return "dogru" if deger else "yanlis"
        else:
            return str(deger)
        
    def __init__(self):
        self.degiskenler = {}
        self.fonksiyonlar = {}

        # Tkinter GUI
        self.gui_pencereler = {}
        self.gui_widgetlar = {}
        self.widget_sayac = 0
        self.tk_menuler = {}
        self.tk_canvas_nesneleri = {}

        # GPIO
        self.gpio_handle = None
        self.gpio_pins = {}
        self.i2c_handle = None
        self.spi_handle = None
        self.pwm_pins = {}
        self.gpio_callbackler = {}

        # GUI modu
        self.gui_modu = "gui"

        # PySide6 Qt GUI
        self.qapp = None
        self.qt_pencereler = {}
        self.qt_widgetlar = {}
        self.qt_layoutlar = {}
        self.qt_menuler = {}
        self.qt_timerlar = {}
        self.qt_widget_to_layout = {}

        # Pygame
        self.pg_ekran = None
        self.pg_saat = None
        self.pg_yuzeyleri = {}
        self.pg_resimler = {}
        self.pg_sesler = {}
        self.pg_muzikler = {}
        self.pg_fontlar = {}
        self.pg_sprite_gruplari = {}
        self.pg_renk_tampon = {}

        # Network
        self.ag_modu = False
        self.requests_session = None

        # Şifreleme / Hash
        self.sifrele_modu = False
        self.hash_modu = False

        # Dosya çalıştırma modu (hata olunca sys.exit için)
        self._dosya_modu = False

    # ==================== INTERAKTIF MOD ====================

    def interaktif_mod(self):
        print("TSharp 4.1.01.04.26 (varsayılan, Apr 01 2026)")
        print('Çıkış için "çık" yazın.')
        print()

        while True:
            try:
                satir = input(">>> ").rstrip()
            except (KeyboardInterrupt, EOFError):
                print("\nTSharp kapatılıyor...")
                time.sleep(0.5)
                break

            if not satir.strip() or satir.strip().startswith('//'):
                continue

            if satir.strip() in ('çık', 'cik', 'çik', 'exit', 'quit'):
                print("TSharp kapatılıyor...")
                time.sleep(0.5)
                break

            # Blok komut mu? (eger/dongu/her/fonksiyon)
            satir = normalize_satir(satir)
            temiz = satir.strip()
            
            # BLOK_BASLATAN listesinde olan bir komutla mı başlıyor?
            blok_mu = any(temiz.startswith(b) for b in BLOK_BASLATAN)

            if blok_mu:
                # Çok satırlı blok topla
                satirlar = [satir]
                derinlik = 1
                while derinlik > 0:
                    try:
                        ic_satir = input("... ").rstrip()
                    except (KeyboardInterrupt, EOFError):
                        print()
                        break
                    satirlar.append(ic_satir)
                    ic_temiz = ic_satir.strip()
                    if any(ic_temiz.startswith(b) for b in BLOK_BASLATAN):
                        derinlik += 1
                    elif ic_temiz == BLOK_KAPATAN:
                        derinlik -= 1
                try:
                    self.satirlari_calistir(satirlar)
                except ReturnException:
                    pass
                except Exception as e:
                    print(f"Hata: {e}")
            else:
                # Tek satırlık komutlar
                try:
                    self.satirlari_calistir([satir])
                except ReturnException:
                    pass
                except Exception as e:
                    print(f"Hata: {e}")
    def calistir(self, dosya_yolu):
        try:
            if not os.path.exists(dosya_yolu):
                print(f"Hata: Dosya bulunamadi: '{dosya_yolu}'")
                sys.exit(1)
            dosya_boyutu = os.path.getsize(dosya_yolu)
            MAX_BOYUT = 50 * 1024 * 1024  # 50 MB
            if dosya_boyutu > MAX_BOYUT:
                print(f"Hata: Dosya cok buyuk ({dosya_boyutu // (1024*1024)} MB). Maksimum 50 MB.")
                sys.exit(1)
            with open(dosya_yolu, 'r', encoding='utf-8') as f:
                satirlar = f.readlines()
            self._dosya_modu = True
            self.satirlari_calistir(satirlar)
        except SystemExit:
            raise
        except FileNotFoundError:
            print(f"Hata: Dosya bulunamadi: '{dosya_yolu}'")
            sys.exit(1)
        except PermissionError:
            print(f"Hata: Dosya okuma izni yok: '{dosya_yolu}'")
            sys.exit(1)
        except UnicodeDecodeError:
            print(f"Hata: Dosya kodlamasi hatasi ('{dosya_yolu}'). Lutfen UTF-8 kullanin.")
            sys.exit(1)
        except Exception as e:
            print(f"Hata: Dosya okuma hatasi ('{dosya_yolu}'): {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)
        finally:
            self._dosya_modu = False

    def satirlari_calistir(self, satirlar):
        i = 0
        while i < len(satirlar):
            # Satırı string olarak al, strip yap
            ham = satirlar[i]
            satir = normalize_satir(ham if isinstance(ham, str) else str(ham))

            if not satir or satir.startswith('//'):
                i += 1
                continue

            if satir == 'kullan gui6':
                self.gui_modu = "pyside6"
                self.pyside6_kontrol()
                if self.qapp is None:
                    self.qapp = QApplication.instance() or QApplication(sys.argv)
                i += 1
                continue
            if satir == 'kullan gui':
                self.gui_modu = "tkinter"
                i += 1
                continue
            if satir == 'kullan ag':
                self.ag_kontrol()
                self.ag_modu = True
                self.requests_session = requests.Session()
                self.requests_session.headers.update({'User-Agent': 'TSharp/4.1'})
                i += 1
                continue
            if satir == 'kullan oyun':
                self.pygame_kontrol()
                i += 1
                continue
            if satir == 'kullan sifrele':
                self.sifrele_modu = True
                i += 1
                continue
            if satir == 'kullan hash':
                self.hash_modu = True
                i += 1
                continue

            if satir.startswith('fonksiyon '):
                i = self.fonksiyon_tanimla(satirlar, i)
            elif satir.startswith('eger '):
                i = self.eger_blogu(satirlar, i)
            elif satir.startswith('dongu '):
                i = self.dongu_blogu(satirlar, i)
            elif satir.startswith('her '):
                i = self.her_dongusu(satirlar, i)
            else:
                try:
                    self.komutu_calistir(satir)
                except (BreakException, ContinueException, ReturnException):
                    raise
                except Exception as e:
                    print(f"Hata [{satir[:40]}]: {e}")
                    if self._dosya_modu:
                        sys.exit(1)
                i += 1

    def komutu_calistir(self, satir):
        # Temel komutlar
        if satir.startswith('degisken '):
            self.degisken_tanimla(satir)
        elif satir == 'yazdir':
            # Tek başına yazdir -> boş satır
            print()
        elif satir.startswith('yazdir '):
            self.yazdir(satir)
        elif satir.startswith('girdi '):
            self.girdi_al(satir)
        elif satir.startswith('liste '):
            self.liste_tanimla(satir)
        elif satir.startswith('sozluk '):
            self.sozluk_tanimla(satir)
        elif satir.startswith('dondur '):
            deger_str = satir[len('dondur '):].strip()
            deger = self.ifade_hesapla(deger_str) if deger_str else None
            raise ReturnException(deger)
        elif satir == 'dondur':
            raise ReturnException(None)
        elif satir.startswith('don '):
            deger = self.ifade_hesapla(satir[len('don '):])
            raise ReturnException(deger)
        elif satir.startswith('bekle '):
            sure = float(self.ifade_hesapla(satir[len('bekle '):].strip()))
            time.sleep(sure)
        elif satir == 'dur':
            raise BreakException()
        elif satir == 'devam':
            raise ContinueException()

        # ---- TKINTER GUI ----
        elif satir.startswith('pencere ') and self.gui_modu == "tkinter":
            self.pencere_olustur(satir)
        elif satir.startswith('buton ') and self.gui_modu == "tkinter":
            self.buton_olustur(satir)
        elif satir.startswith('etiket ') and self.gui_modu == "tkinter":
            self.etiket_olustur(satir)
        elif satir.startswith('giriskutusu ') and self.gui_modu == "tkinter":
            self.giriskutusu_olustur(satir)
        elif satir.startswith('metin_alani ') and self.gui_modu == "tkinter":
            self.metin_alani_olustur(satir)
        elif satir.startswith('onay_kutusu ') and self.gui_modu == "tkinter":
            self.onay_kutusu_olustur(satir)
        elif satir.startswith('liste_kutusu ') and self.gui_modu == "tkinter":
            self.liste_kutusu_olustur(satir)
        elif satir.startswith('radyo_buton ') and self.gui_modu == "tkinter":
            self.radyo_buton_olustur(satir)
        elif satir.startswith('kaydirici ') and self.gui_modu == "tkinter":
            self.kaydirici_olustur(satir)
        elif satir.startswith('combo_kutu ') and self.gui_modu == "tkinter":
            self.combo_kutu_olustur(satir)
        elif satir.startswith('ilerleme_cubugu ') and self.gui_modu == "tkinter":
            self.ilerleme_cubugu_olustur(satir)
        elif satir.startswith('canvas ') and self.gui_modu == "tkinter":
            self.canvas_olustur(satir)
        elif satir.startswith('frame ') and self.gui_modu == "tkinter":
            self.frame_olustur(satir)
        elif satir.startswith('ayirici ') and self.gui_modu == "tkinter":
            self.ayirici_olustur(satir)
        elif satir.startswith('menu_cubugu ') and self.gui_modu == "tkinter":
            self.menu_cubugu_olustur(satir)
        elif satir.startswith('menu_ekle ') and self.gui_modu == "tkinter":
            self.menu_ekle(satir)
        elif satir.startswith('menu_madde_ekle ') and self.gui_modu == "tkinter":
            self.menu_madde_ekle(satir)
        elif satir.startswith('menu_ayirici_ekle ') and self.gui_modu == "tkinter":
            self.menu_ayirici_ekle(satir)
        elif satir.startswith('notebook ') and self.gui_modu == "tkinter":
            self.notebook_olustur(satir)
        elif satir.startswith('notebook_sekme ') and self.gui_modu == "tkinter":
            self.notebook_sekme_ekle(satir)
        elif satir.startswith('agac ') and self.gui_modu == "tkinter":
            self.agac_olustur(satir)
        elif satir.startswith('agac_ekle ') and self.gui_modu == "tkinter":
            self.agac_ekle(satir)
        elif satir.startswith('tablo ') and self.gui_modu == "tkinter":
            self.tablo_olustur(satir)
        elif satir.startswith('tablo_sutun ') and self.gui_modu == "tkinter":
            self.tablo_sutun_ekle(satir)
        elif satir.startswith('tablo_satir ') and self.gui_modu == "tkinter":
            self.tablo_satir_ekle(satir)
        elif satir.startswith('kaydirma_alani ') and self.gui_modu == "tkinter":
            self.kaydirma_alani_olustur(satir)
        elif satir.startswith('degistirici ') and self.gui_modu == "tkinter":
            self.degistirici_olustur(satir)
        elif satir.startswith('sayac_kutu ') and self.gui_modu == "tkinter":
            self.sayac_kutu_olustur(satir)
        elif satir.startswith('renk_sec ') and self.gui_modu == "tkinter":
            self.renk_sec(satir)
        elif satir.startswith('dosya_sec ') and self.gui_modu == "tkinter":
            self.dosya_sec(satir)
        elif satir.startswith('klasor_sec ') and self.gui_modu == "tkinter":
            self.klasor_sec(satir)
        elif satir.startswith('yazi_sec ') and self.gui_modu == "tkinter":
            self.yazi_tipi_sec(satir)
        elif satir.startswith('widget_deger ') and self.gui_modu == "tkinter":
            self.widget_deger_al(satir)
        elif satir.startswith('widget_ayarla ') and self.gui_modu == "tkinter":
            self.widget_deger_ayarla(satir)
        elif satir.startswith('pencere_goster ') and self.gui_modu == "tkinter":
            self.pencere_goster(satir)
        elif satir.startswith('mesaj_kutusu ') and self.gui_modu == "tkinter":
            self.mesaj_kutusu(satir)
        elif satir.startswith('soru_kutusu ') and self.gui_modu == "tkinter":
            self.soru_kutusu(satir)
        elif satir.startswith('uyari_kutusu ') and self.gui_modu == "tkinter":
            self.uyari_kutusu(satir)
        elif satir.startswith('hata_kutusu ') and self.gui_modu == "tkinter":
            self.hata_kutusu(satir)
        elif satir.startswith('giris_kutusu ') and self.gui_modu == "tkinter":
            self.giris_kutusu(satir)
        elif satir.startswith('pencere_baslik ') and self.gui_modu == "tkinter":
            self.pencere_baslik_ayarla(satir)
        elif satir.startswith('pencere_boyut ') and self.gui_modu == "tkinter":
            self.pencere_boyut_ayarla(satir)
        elif satir.startswith('pencere_renk ') and self.gui_modu == "tkinter":
            self.pencere_renk_ayarla(satir)
        elif satir.startswith('pencere_kapat ') and self.gui_modu == "tkinter":
            self.pencere_kapat(satir)
        elif satir.startswith('widget_renk ') and self.gui_modu == "tkinter":
            self.widget_renk_ayarla(satir)
        elif satir.startswith('widget_font ') and self.gui_modu == "tkinter":
            self.widget_font_ayarla(satir)
        elif satir.startswith('widget_yerlestir ') and self.gui_modu == "tkinter":
            self.widget_yerlestir(satir)
        elif satir.startswith('widget_gizle ') and self.gui_modu == "tkinter":
            self.widget_gizle(satir)
        elif satir.startswith('widget_goster ') and self.gui_modu == "tkinter":
            self.widget_goster(satir)
        elif satir.startswith('widget_etkinlestir ') and self.gui_modu == "tkinter":
            self.widget_etkinlestir(satir)
        elif satir.startswith('widget_devre_disi ') and self.gui_modu == "tkinter":
            self.widget_devre_disi(satir)
        elif satir.startswith('widget_sil ') and self.gui_modu == "tkinter":
            self.widget_sil(satir)
        elif satir.startswith('canvas_cizgi ') and self.gui_modu == "tkinter":
            self.canvas_cizgi(satir)
        elif satir.startswith('canvas_dikdortgen ') and self.gui_modu == "tkinter":
            self.canvas_dikdortgen(satir)
        elif satir.startswith('canvas_oval ') and self.gui_modu == "tkinter":
            self.canvas_oval(satir)
        elif satir.startswith('canvas_metin ') and self.gui_modu == "tkinter":
            self.canvas_metin(satir)
        elif satir.startswith('canvas_resim ') and self.gui_modu == "tkinter":
            self.canvas_resim(satir)
        elif satir.startswith('canvas_temizle ') and self.gui_modu == "tkinter":
            self.canvas_temizle(satir)
        elif satir.startswith('canvas_nesne_sil ') and self.gui_modu == "tkinter":
            self.canvas_nesne_sil(satir)
        elif satir.startswith('olay_bagla ') and self.gui_modu == "tkinter":
            self.olay_bagla(satir)
        elif satir.startswith('timer_olustur ') and self.gui_modu == "tkinter":
            self.tk_timer_olustur(satir)
        elif satir.startswith('guncelle ') and self.gui_modu == "tkinter":
            self.pencere_guncelle(satir)

        # ---- PYSIDE6 GUI ----
        elif satir.startswith('qt_pencere '):
            self.qt_pencere_olustur(satir)
        elif satir.startswith('qt_buton '):
            self.qt_buton_olustur(satir)
        elif satir.startswith('qt_etiket '):
            self.qt_etiket_olustur(satir)
        elif satir.startswith('qt_giriskutusu '):
            self.qt_giriskutusu_olustur(satir)
        elif satir.startswith('qt_metin_alani '):
            self.qt_metin_alani_olustur(satir)
        elif satir.startswith('qt_onay_kutusu '):
            self.qt_onay_kutusu_olustur(satir)
        elif satir.startswith('qt_radyo_buton '):
            self.qt_radyo_buton_olustur(satir)
        elif satir.startswith('qt_combo_kutu '):
            self.qt_combo_kutu_olustur(satir)
        elif satir.startswith('qt_liste_widget '):
            self.qt_liste_widget_olustur(satir)
        elif satir.startswith('qt_tablo_widget '):
            self.qt_tablo_widget_olustur(satir)
        elif satir.startswith('qt_agac_widget '):
            self.qt_agac_widget_olustur(satir)
        elif satir.startswith('qt_sekme_widget '):
            self.qt_sekme_widget_olustur(satir)
        elif satir.startswith('qt_kaydirici '):
            self.qt_kaydirici_olustur(satir)
        elif satir.startswith('qt_ilerleme_cubugu '):
            self.qt_ilerleme_cubugu_olustur(satir)
        elif satir.startswith('qt_spin_kutu '):
            self.qt_spin_kutu_olustur(satir)
        elif satir.startswith('qt_tarih_secici '):
            self.qt_tarih_secici_olustur(satir)
        elif satir.startswith('qt_saat_secici '):
            self.qt_saat_secici_olustur(satir)
        elif satir.startswith('qt_takvim '):
            self.qt_takvim_olustur(satir)
        elif satir.startswith('qt_web_tarayici '):
            self.qt_web_tarayici_olustur(satir)
        elif satir.startswith('qt_video_oynatici '):
            self.qt_video_oynatici_olustur(satir)
        elif satir.startswith('qt_grafik '):
            self.qt_grafik_olustur(satir)
        elif satir.startswith('qt_layout '):
            self.qt_layout_olustur(satir)
        elif satir.startswith('qt_menu '):
            self.qt_menu_olustur(satir)
        elif satir.startswith('qt_toolbar '):
            self.qt_toolbar_olustur(satir)
        elif satir.startswith('qt_statusbar '):
            self.qt_statusbar_olustur(satir)
        elif satir.startswith('qt_timer '):
            self.qt_timer_olustur(satir)
        elif satir.startswith('qt_mesaj_kutusu '):
            self.qt_mesaj_kutusu(satir)
        elif satir.startswith('qt_dosya_dialog '):
            self.qt_dosya_dialog(satir)
        elif satir.startswith('qt_renk_dialog '):
            self.qt_renk_dialog(satir)
        elif satir.startswith('qt_pencere_goster '):
            self.qt_pencere_goster(satir)
        elif satir == 'qt_calistir':
            self.qt_calistir()

        # ---- PYGAME ----
        elif satir == 'oyun_baslat':
            self.oyun_baslat()
        elif satir == 'oyun_kapat':
            self.oyun_kapat()
        elif satir.startswith('oyun_ekran '):
            self.oyun_ekran_olustur(satir)
        elif satir.startswith('oyun_baslik '):
            self.oyun_baslik_ayarla(satir)
        elif satir.startswith('oyun_simge '):
            self.oyun_simge_ayarla(satir)
        elif satir.startswith('ekran_doldur '):
            self.ekran_doldur(satir)
        elif satir == 'ekran_guncelle':
            self.ekran_guncelle()
        elif satir.startswith('ekran_guncelle_bolge '):
            self.ekran_guncelle_bolge(satir)
        elif satir == 'olaylari_isle':
            self.olaylari_isle_komutu()
        elif satir.startswith('olay_kontrol '):
            self.olay_kontrol(satir)
        elif satir.startswith('ciz_cizgi '):
            self.ciz_cizgi(satir)
        elif satir.startswith('ciz_dikdortgen '):
            self.ciz_dikdortgen(satir)
        elif satir.startswith('ciz_dolu_dikdortgen '):
            self.ciz_dolu_dikdortgen(satir)
        elif satir.startswith('ciz_cember '):
            self.ciz_cember(satir)
        elif satir.startswith('ciz_dolu_cember '):
            self.ciz_dolu_cember(satir)
        elif satir.startswith('ciz_elips '):
            self.ciz_elips(satir)
        elif satir.startswith('ciz_cokgen '):
            self.ciz_cokgen(satir)
        elif satir.startswith('ciz_nokta '):
            self.ciz_nokta(satir)
        elif satir.startswith('ciz_yay '):
            self.ciz_yay(satir)
        elif satir.startswith('resim_yukle '):
            self.resim_yukle(satir)
        elif satir.startswith('resim_ciz '):
            self.resim_ciz(satir)
        elif satir.startswith('resim_olcekle '):
            self.resim_olcekle(satir)
        elif satir.startswith('resim_dondur '):
            self.resim_dondur(satir)
        elif satir.startswith('resim_cevir '):
            self.resim_cevir(satir)
        elif satir.startswith('resim_kaydet '):
            self.resim_kaydet(satir)
        elif satir.startswith('yuzeyi_yukle '):
            self.yuzeyi_yukle(satir)
        elif satir.startswith('yuzey_olustur '):
            self.yuzey_olustur(satir)
        elif satir.startswith('yuzey_doldur '):
            self.yuzey_doldur(satir)
        elif satir.startswith('yuzey_kopyala '):
            self.yuzey_kopyala(satir)
        elif satir.startswith('yuzey_effekti '):
            self.yuzey_effekti(satir)
        elif satir.startswith('ses_yukle '):
            self.ses_yukle(satir)
        elif satir.startswith('ses_oynat '):
            self.ses_oynat(satir)
        elif satir.startswith('ses_durdur '):
            self.ses_durdur(satir)
        elif satir.startswith('ses_devam '):
            self.ses_devam(satir)
        elif satir.startswith('ses_ses_duzeyi '):
            self.ses_ses_duzeyi(satir)
        elif satir.startswith('muzik_yukle '):
            self.muzik_yukle(satir)
        elif satir == 'muzik_oynat':
            self.muzik_oynat()
        elif satir == 'muzik_durdur':
            self.muzik_durdur()
        elif satir == 'muzik_devam':
            self.muzik_devam_et()
        elif satir == 'muzik_dur':
            self.muzik_dur()
        elif satir.startswith('muzik_ses_duzeyi '):
            self.muzik_ses_duzeyi(satir)
        elif satir.startswith('muzik_tekrar '):
            self.muzik_tekrar(satir)
        elif satir.startswith('yazi_tipi_yukle '):
            self.yazi_tipi_yukle(satir)
        elif satir.startswith('metin_yaz '):
            self.metin_yaz(satir)
        elif satir.startswith('tuslar_oku '):
            self.tuslar_oku(satir)
        elif satir.startswith('tus_basili_mi '):
            self.tus_basili_mi(satir)
        elif satir.startswith('fare_konum '):
            self.fare_konum_al(satir)
        elif satir.startswith('fare_dugme '):
            self.fare_dugme_al(satir)
        elif satir.startswith('fare_goster '):
            self.fare_goster(satir)
        elif satir == 'fare_gizle':
            self.fare_gizle()
        elif satir.startswith('saat_olustur '):
            self.saat_olustur(satir)
        elif satir.startswith('saat_tikla '):
            self.saat_tikla(satir)
        elif satir.startswith('fps_al '):
            self.fps_al(satir)
        elif satir.startswith('renk_olustur '):
            self.renk_olustur(satir)
        elif satir.startswith('renk_karistir '):
            self.renk_karistir(satir)
        elif satir.startswith('carpisma_kontrol '):
            self.carpisma_kontrol(satir)
        elif satir.startswith('carpisma_dikdortgen '):
            self.carpisma_dikdortgen(satir)
        elif satir.startswith('sprite_grubu_olustur '):
            self.sprite_grubu_olustur(satir)
        elif satir.startswith('sprite_ekle '):
            self.sprite_ekle(satir)
        elif satir.startswith('sprite_ciz '):
            self.sprite_ciz(satir)
        elif satir.startswith('sprite_guncelle '):
            self.sprite_guncelle(satir)
        elif satir.startswith('piksel_al '):
            self.piksel_al(satir)
        elif satir.startswith('piksel_yaz '):
            self.piksel_yaz(satir)
        elif satir.startswith('maske_olustur '):
            self.maske_olustur(satir)
        elif satir.startswith('oyun_bekle '):
            self.oyun_bekle(satir)
        elif satir.startswith('ekran_bilgi '):
            self.ekran_bilgi_al(satir)
        elif satir.startswith('pencere_konumu '):
            self.pencere_konumu_ayarla(satir)
        elif satir.startswith('tam_ekran '):
            self.tam_ekran_ayarla(satir)

        # ---- NETWORK ----
        elif satir.startswith('http_get '):
            self.http_get(satir)
        elif satir.startswith('http_post '):
            self.http_post(satir)
        elif satir.startswith('http_put '):
            self.http_put(satir)
        elif satir.startswith('http_delete '):
            self.http_delete(satir)
        elif satir.startswith('http_head '):
            self.http_head(satir)
        elif satir.startswith('http_patch '):
            self.http_patch(satir)
        elif satir.startswith('dosya_indir '):
            self.dosya_indir(satir)
        elif satir.startswith('json_al '):
            self.json_al(satir)
        elif satir.startswith('json_gonder '):
            self.json_gonder(satir)
        elif satir.startswith('ping '):
            self.ping(satir)
        elif satir.startswith('baslik_ekle '):
            self.baslik_ekle(satir)
        elif satir.startswith('cerez_ekle '):
            self.cerez_ekle(satir)
        elif satir.startswith('timeout_ayarla '):
            self.timeout_ayarla(satir)
        elif satir.startswith('proxy_ayarla '):
            self.proxy_ayarla(satir)
        elif satir.startswith('ssl_dogrula '):
            self.ssl_dogrula(satir)
        elif satir.startswith('yonlendir_izin '):
            self.yonlendir_izin(satir)
        elif satir.startswith('stream_indir '):
            self.stream_indir(satir)
        elif satir.startswith('coklu_dosya_gonder '):
            self.coklu_dosya_gonder(satir)
        elif satir.startswith('durum_kodu '):
            self.durum_kodu(satir)

        # ---- GPIO ----
        elif satir == 'gpio_baslat':
            self.gpio_baslat()
        elif satir == 'gpio_kapat':
            self.gpio_kapat()
        elif satir.startswith('gpio_mod '):
            self.gpio_mod(satir)
        elif satir.startswith('gpio_yaz '):
            self.gpio_yaz(satir)
        elif satir.startswith('gpio_oku '):
            self.gpio_oku(satir)
        elif satir.startswith('gpio_yukari_cek '):
            self.gpio_yukari_cek(satir)
        elif satir.startswith('gpio_asagi_cek '):
            self.gpio_asagi_cek(satir)
        elif satir.startswith('gpio_kesme '):
            self.gpio_kesme_ekle(satir)
        elif satir.startswith('gpio_kesme_kaldir '):
            self.gpio_kesme_kaldir(satir)
        elif satir.startswith('pwm_baslat '):
            self.pwm_baslat(satir)
        elif satir.startswith('pwm_durdur '):
            self.pwm_durdur(satir)
        elif satir.startswith('pwm_ayarla '):
            self.pwm_ayarla(satir)
        elif satir.startswith('pwm_frekans '):
            self.pwm_frekans_ayarla(satir)
        elif satir.startswith('i2c_baslat '):
            self.i2c_baslat(satir)
        elif satir == 'i2c_kapat':
            self.i2c_kapat()
        elif satir.startswith('i2c_yaz '):
            self.i2c_yaz(satir)
        elif satir.startswith('i2c_oku '):
            self.i2c_oku(satir)
        elif satir.startswith('i2c_kayit_yaz '):
            self.i2c_kayit_yaz(satir)
        elif satir.startswith('i2c_kayit_oku '):
            self.i2c_kayit_oku(satir)
        elif satir.startswith('spi_baslat '):
            self.spi_baslat(satir)
        elif satir == 'spi_kapat':
            self.spi_kapat()
        elif satir.startswith('spi_transfer '):
            self.spi_transfer(satir)

        # ---- ZIP ----
        elif satir.startswith('zip_olustur '):
            self.zip_olustur(satir)
        elif satir.startswith('zip_ac '):
            self.zip_ac(satir)
        elif satir.startswith('zip_ekle '):
            self.zip_ekle(satir)
        elif satir.startswith('zip_cikar '):
            self.zip_cikar(satir)
        elif satir.startswith('zip_listele '):
            self.zip_listele(satir)
        elif satir.startswith('zip_sil '):
            self.zip_sil(satir)

        # ---- SIFRELE / BASE64 ----
        elif satir.startswith('b64_sifrele ') and self.sifrele_modu:
            self.b64_sifrele(satir)
        elif satir.startswith('b64_coz ') and self.sifrele_modu:
            self.b64_coz(satir)
        elif satir.startswith('xor_sifrele ') and self.sifrele_modu:
            self.xor_sifrele(satir)
        elif satir.startswith('xor_coz ') and self.sifrele_modu:
            self.xor_coz(satir)
        elif satir.startswith('dosya_sifrele ') and self.sifrele_modu:
            self.dosya_sifrele(satir)
        elif satir.startswith('dosya_coz ') and self.sifrele_modu:
            self.dosya_coz(satir)
        elif satir.startswith('sifreli_yaz ') and self.sifrele_modu:
            self.sifreli_dosya_yaz(satir)
        elif satir.startswith('sifreli_oku ') and self.sifrele_modu:
            self.sifreli_dosya_oku(satir)

        # ---- HASH ----
        elif satir.startswith('sha256 ') and self.hash_modu:
            self.sha256_hesapla(satir)
        elif satir.startswith('sha512 ') and self.hash_modu:
            self.sha512_hesapla(satir)
        elif satir.startswith('md5 ') and self.hash_modu:
            self.md5_hesapla(satir)
        elif satir.startswith('sha1 ') and self.hash_modu:
            self.sha1_hesapla(satir)
        elif satir.startswith('dosya_sha256 ') and self.hash_modu:
            self.dosya_sha256(satir)
        elif satir.startswith('hmac_hesapla ') and self.hash_modu:
            self.hmac_hesapla(satir)
        elif satir.startswith('hash_dogrula ') and self.hash_modu:
            self.hash_dogrula(satir)

        # ---- Atama ve fonksiyon çağrısı ----
        elif '=' in satir and not satir.startswith('=='):
            self.degisken_guncelle(satir)
        elif '(' in satir and ')' in satir:
            self.ifade_hesapla(satir)
        else:
            # Bilinmeyen komut - hata ver
            raise ValueError(f"Bilinmeyen komut: '{satir[:60]}'")

    # ==================== DEGISKEN ISLEMLERI ====================

    def degisken_tanimla(self, satir):
        # "degisken ad = deger" veya "degisken ad deger"
        govde = satir[len('degisken '):].strip()
        if '=' in govde:
            ad, deger_str = govde.split('=', 1)
            ad = ad.strip()
            deger_str = deger_str.strip()
        else:
            parcalar = govde.split(None, 1)
            ad = parcalar[0].strip()
            deger_str = parcalar[1].strip() if len(parcalar) > 1 else ''
        # String doğrulama: string değer " ile sarılmalı
        if deger_str:
            self._string_kural_kontrol(deger_str, satir)
        deger = self.ifade_hesapla(deger_str) if deger_str else None
        self.degiskenler[ad] = deger

    def _string_kural_kontrol(self, deger_str, satir_ornek=''):
            s = deger_str.strip()
        
            if s in self.degiskenler:
                return True # Sorun yok

            if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
                return True # Sorun yok
            
            try:
                float(s)
                return True
            except ValueError:
                pass
            
            if s in ('dogru', 'yanlis', 'hic', 'True', 'False', 'None'):
                return True
            
            if (s.startswith('[') and s.endswith(']')) or (s.startswith('{') and s.endswith('}')):
                return True
            
            if any(op in s for op in ['+', '-', '*', '/', '(', ')', '>', '<', '=', '!', '%', 'and', 'or', 'not', 'in']):
                return True

            # Liste/sözlük indeks erişimi: dizi[ifade] → geçerli
            if '[' in s and ']' in s:
              return True

        # HATA DURUMU
            satir_gosterim = satir_ornek
            if satir_gosterim.startswith("yazdir"):
                satir_gosterim = satir_gosterim.replace("yazdir", "yazdır", 1)

            konum = f" [{satir_gosterim[:40]}]" if satir_gosterim else ""
            print(f"Uyarı: Kodunuzda hata tespit edildi{konum}! "
                  f"String değerler \" içine alınmalıdır. Örnek: \"{s}\"")
            return False # Hata olduğunu bildir
    def degisken_guncelle(self, satir):
        if '=' not in satir:
            return
        # Bileşik atama operatörleri: +=, -=, *=, /=
        for op in ('+=', '-=', '*=', '/=', '//=', '%=', '**='):
            if op in satir:
                sol, sag = satir.split(op, 1)
                sol = sol.strip()
                sag = sag.strip()
                mevcut = self.degiskenler.get(sol, 0)
                yeni = self.ifade_hesapla(sag)
                if op == '+=':   self.degiskenler[sol] = mevcut + yeni
                elif op == '-=': self.degiskenler[sol] = mevcut - yeni
                elif op == '*=': self.degiskenler[sol] = mevcut * yeni
                elif op == '/=':
                    if yeni == 0:
                        print(f"Hata: Sifira bolme ('{sol} /= 0')")
                        return
                    self.degiskenler[sol] = mevcut / yeni
                elif op == '//=':
                    if yeni == 0:
                        print(f"Hata: Sifira bolme ('{sol} //= 0')")
                        return
                    self.degiskenler[sol] = mevcut // yeni
                elif op == '%=':
                    if yeni == 0:
                        print(f"Hata: Sifira mod alma ('{sol} %= 0')")
                        return
                    self.degiskenler[sol] = mevcut % yeni
                elif op == '**=':
                    try:
                        self.degiskenler[sol] = mevcut ** yeni
                    except (OverflowError, ValueError) as e:
                        print(f"Hata: Us alma hatasi ('{sol} **= {yeni}'): {e}")
                return

        sol, sag = satir.split('=', 1)
        sol = sol.strip()
        sag = sag.strip()
        if '[' in sol and ']' in sol:
            degisken_adi = sol[:sol.index('[')].strip()
            indeks_ifade = sol[sol.index('[')+1:sol.index(']')].strip()
            indeks = self.ifade_hesapla(indeks_ifade)
            deger = self.ifade_hesapla(sag)
            if degisken_adi in self.degiskenler:
                try:
                    self.degiskenler[degisken_adi][indeks] = deger
                except (IndexError, KeyError, TypeError) as e:
                    print(f"Hata: Indeks atama hatasi '{degisken_adi}[{indeks}]': {e}")
            else:
                print(f"Hata: Degisken bulunamadi: '{degisken_adi}'")
        else:
            deger = self.ifade_hesapla(sag)
            self.degiskenler[sol] = deger

    def yazdir(self, satir):
        govde = satir[len('yazdir '):].strip()
        if not govde:
            print()
            return
            
        tokenlar = self._yazdir_tokenize(govde)
        parcalar = []
        for tok in tokenlar:
            tok = tok.strip().rstrip(',')
            if not tok:
                continue
            
            # Eğer token bir değişken adıysa (sayı görünse bile) doğrudan değişkene bak
            # Örnek: degisken 1 = "talha" -> yazdir 1 -> talha
            if tok in self.degiskenler:
                parcalar.append(self._temiz_metin_yap(self.degiskenler[tok]))
                continue

            # BURASI KRİTİK: Eğer kural kontrolü False dönerse (hata varsa)
            # fonksiyonu hemen bitir (return), böylece print() çalışmaz.
            if not self._string_kural_kontrol(tok, satir):
                return 
            
            deger = self.ifade_hesapla(tok)
            parcalar.append(self._temiz_metin_yap(deger))
            
        # Eğer yukarıdaki döngü hiç kesilmeden bittiyse çıktı verilir
        print(' '.join(parcalar))
    def _yazdir_tokenize(self, metin):
        """
        yazdir icin govdeyi parcalara ayirir.
        
        Kural:
          - "..." -> tek string token (icindeki her sey korunur)
          - String olmayan kisimlar -> iki "..." arasinda kalan kisim tek ifade sayilir
        
        Ornekler:
          "Merhaba"           -> ['"Merhaba"']
          x                   -> ['x']
          x + y               -> ['x + y']          (tek ifade olarak eval edilir)
          "Isim:" isim        -> ['"Isim:"', 'isim']
          "A:" x + y "B:" z   -> ['"A:"', 'x + y', '"B:"', 'z']
        """
        parcalar = []
        i = 0
        n = len(metin)
        while i < n:
            # Boslukları atla
            while i < n and metin[i] == ' ':
                i += 1
            if i >= n:
                break
            # String literal mi?
            if metin[i] in ('"', "'"):
                str_ch = metin[i]
                j = i + 1
                while j < n and metin[j] != str_ch:
                    j += 1
                j += 1  # kapatan tirnak dahil
                parcalar.append(metin[i:j])
                i = j
            else:
                # String olmayan bolum: sonraki " veya string basina kadar al
                j = i
                while j < n and metin[j] not in ('"', "'"):
                    j += 1
                bolum = metin[i:j].strip()
                if bolum:
                    parcalar.append(bolum)
                i = j
        return parcalar if parcalar else [metin]

    def girdi_al(self, satir):
        govde = satir[len('girdi '):].strip()
        parcalar = govde.split(None, 1)
        degisken_adi = parcalar[0]
        mesaj = self.ifade_hesapla(parcalar[1]) if len(parcalar) > 1 else ""
        deger = input(str(mesaj))
        self.degiskenler[degisken_adi] = deger

    def liste_tanimla(self, satir):
        govde = satir[len('liste '):].strip()
        parcalar = govde.split(None, 1)
        ad = parcalar[0]
        deger = self.ifade_hesapla(parcalar[1]) if len(parcalar) > 1 else []
        self.degiskenler[ad] = deger

    def sozluk_tanimla(self, satir):
        govde = satir[len('sozluk '):].strip()
        parcalar = govde.split(None, 1)
        ad = parcalar[0]
        deger = self.ifade_hesapla(parcalar[1]) if len(parcalar) > 1 else {}
        self.degiskenler[ad] = deger

    # ==================== TKINTER GUI ====================

    def gui_kontrol(self):
        if not TKINTER_AVAILABLE:
            raise ImportError("Tkinter kurulu degil.")

    def pencere_olustur(self, satir):
        self.gui_kontrol()
        govde = satir[len('pencere '):].strip()
        parcalar = parse_qt_command(govde)
        pencere_adi = parcalar[0]
        baslik = self.ifade_hesapla(parcalar[1]) if len(parcalar) > 1 else "TSharp Pencere"
        genislik = int(parcalar[2]) if len(parcalar) > 2 else 400
        yukseklik = int(parcalar[3]) if len(parcalar) > 3 else 300
        pencere = tk.Tk()
        pencere.title(str(baslik))
        pencere.geometry(f"{genislik}x{yukseklik}")
        self.gui_pencereler[pencere_adi] = pencere
        self.degiskenler[pencere_adi] = pencere

    def buton_olustur(self, satir):
        self.gui_kontrol()
        govde = satir[len('buton '):].strip()
        eslesme = re.match(r'^(\w+)\s+(".*?"|\'.*?\')\s+(\w+)(?:\s+(\w+))?$', govde)
        if not eslesme:
            raise ValueError(f"Hatali buton tanimi: {govde}")
        buton_adi = eslesme.group(1)
        metin = self.ifade_hesapla(eslesme.group(2))
        pencere_adi = eslesme.group(3)
        fonksiyon_adi = eslesme.group(4)
        if pencere_adi not in self.gui_pencereler:
            raise ValueError(f"Pencere bulunamadi: {pencere_adi}")
        pencere = self.gui_pencereler[pencere_adi]
        komut = None
        if fonksiyon_adi and fonksiyon_adi in self.degiskenler:
            komut = self.degiskenler[fonksiyon_adi]
        buton = tk.Button(pencere, text=str(metin), command=komut)
        buton.pack(pady=5)
        self.degiskenler[buton_adi] = buton

    def etiket_olustur(self, satir):
        self.gui_kontrol()
        govde = satir[len('etiket '):].strip()
        eslesme = re.match(r'^(\w+)\s+(".*?"|\'.*?\')\s+(\w+)$', govde)
        if not eslesme:
            raise ValueError(f"Hatali etiket tanimi: {govde}")
        etiket_adi = eslesme.group(1)
        metin = self.ifade_hesapla(eslesme.group(2))
        pencere_adi = eslesme.group(3)
        if pencere_adi not in self.gui_pencereler:
            raise ValueError(f"Pencere bulunamadi: {pencere_adi}")
        pencere = self.gui_pencereler[pencere_adi]
        etiket = tk.Label(pencere, text=str(metin))
        etiket.pack(pady=5)
        self.degiskenler[etiket_adi] = etiket

    def giriskutusu_olustur(self, satir):
        self.gui_kontrol()
        govde = satir[len('giriskutusu '):].strip()
        parcalar = govde.split()
        giris_adi = parcalar[0]
        pencere_adi = parcalar[1]
        if pencere_adi not in self.gui_pencereler:
            raise ValueError(f"Pencere bulunamadi: {pencere_adi}")
        pencere = self.gui_pencereler[pencere_adi]
        giris = tk.Entry(pencere)
        giris.pack(pady=5)
        self.degiskenler[giris_adi] = giris

    def metin_alani_olustur(self, satir):
        self.gui_kontrol()
        govde = satir[len('metin_alani '):].strip()
        parcalar = govde.split()
        alan_adi = parcalar[0]
        pencere_adi = parcalar[1]
        yukseklik = int(parcalar[2]) if len(parcalar) > 2 else 10
        genislik = int(parcalar[3]) if len(parcalar) > 3 else 50
        if pencere_adi not in self.gui_pencereler:
            raise ValueError(f"Pencere bulunamadi: {pencere_adi}")
        pencere = self.gui_pencereler[pencere_adi]
        metin_alani = tk.Text(pencere, height=yukseklik, width=genislik)
        metin_alani.pack(pady=5)
        self.degiskenler[alan_adi] = metin_alani

    def onay_kutusu_olustur(self, satir):
        self.gui_kontrol()
        govde = satir[len('onay_kutusu '):].strip()
        eslesme = re.match(r'^(\w+)\s+(".*?"|\'.*?\')\s+(\w+)$', govde)
        if not eslesme:
            raise ValueError(f"Hatali onay kutusu tanimi: {govde}")
        onay_adi = eslesme.group(1)
        metin = self.ifade_hesapla(eslesme.group(2))
        pencere_adi = eslesme.group(3)
        if pencere_adi not in self.gui_pencereler:
            raise ValueError(f"Pencere bulunamadi: {pencere_adi}")
        pencere = self.gui_pencereler[pencere_adi]
        var = tk.BooleanVar()
        onay = tk.Checkbutton(pencere, text=str(metin), variable=var)
        onay.pack(pady=5)
        self.degiskenler[onay_adi] = var
        self.degiskenler[f"{onay_adi}_widget"] = onay

    def liste_kutusu_olustur(self, satir):
        self.gui_kontrol()
        govde = satir[len('liste_kutusu '):].strip()
        parcalar = govde.split()
        liste_adi = parcalar[0]
        pencere_adi = parcalar[1]
        secim_modu = parcalar[2] if len(parcalar) > 2 else "tekli"
        if pencere_adi not in self.gui_pencereler:
            raise ValueError(f"Pencere bulunamadi: {pencere_adi}")
        pencere = self.gui_pencereler[pencere_adi]
        mod = tk.SINGLE if secim_modu == "tekli" else tk.MULTIPLE
        liste = tk.Listbox(pencere, selectmode=mod)
        liste.pack(pady=5)
        self.degiskenler[liste_adi] = liste

    def radyo_buton_olustur(self, satir):
        self.gui_kontrol()
        govde = satir[len('radyo_buton '):].strip()
        parcalar = parse_qt_command(govde)
        radyo_adi = parcalar[0]
        metin = self.ifade_hesapla(parcalar[1])
        pencere_adi = parcalar[2]
        degisken_adi = parcalar[3]
        deger = self.ifade_hesapla(parcalar[4]) if len(parcalar) > 4 else radyo_adi
        if pencere_adi not in self.gui_pencereler:
            raise ValueError(f"Pencere bulunamadi: {pencere_adi}")
        pencere = self.gui_pencereler[pencere_adi]
        if degisken_adi not in self.degiskenler:
            var = tk.StringVar()
            self.degiskenler[degisken_adi] = var
        else:
            var = self.degiskenler[degisken_adi]
        radyo = tk.Radiobutton(pencere, text=str(metin), variable=var, value=str(deger))
        radyo.pack(pady=2)
        self.degiskenler[radyo_adi] = radyo

    def kaydirici_olustur(self, satir):
        self.gui_kontrol()
        govde = satir[len('kaydirici '):].strip()
        parcalar = govde.split()
        kaydirici_adi = parcalar[0]
        pencere_adi = parcalar[1]
        min_deger = int(parcalar[2]) if len(parcalar) > 2 else 0
        max_deger = int(parcalar[3]) if len(parcalar) > 3 else 100
        yon = parcalar[4] if len(parcalar) > 4 else "yatay"
        if pencere_adi not in self.gui_pencereler:
            raise ValueError(f"Pencere bulunamadi: {pencere_adi}")
        pencere = self.gui_pencereler[pencere_adi]
        orient = tk.HORIZONTAL if yon == "yatay" else tk.VERTICAL
        kaydirici = tk.Scale(pencere, from_=min_deger, to=max_deger, orient=orient)
        kaydirici.pack(pady=5)
        self.degiskenler[kaydirici_adi] = kaydirici

    def combo_kutu_olustur(self, satir):
        self.gui_kontrol()
        govde = satir[len('combo_kutu '):].strip()
        parcalar = parse_qt_command(govde)
        combo_adi = parcalar[0]
        pencere_adi = parcalar[1]
        degerler = self.ifade_hesapla(parcalar[2]) if len(parcalar) > 2 else []
        if pencere_adi not in self.gui_pencereler:
            raise ValueError(f"Pencere bulunamadi: {pencere_adi}")
        pencere = self.gui_pencereler[pencere_adi]
        combo = ttk.Combobox(pencere, values=degerler)
        combo.pack(pady=5)
        self.degiskenler[combo_adi] = combo

    def ilerleme_cubugu_olustur(self, satir):
        self.gui_kontrol()
        govde = satir[len('ilerleme_cubugu '):].strip()
        parcalar = govde.split()
        cubuk_adi = parcalar[0]
        pencere_adi = parcalar[1]
        uzunluk = int(parcalar[2]) if len(parcalar) > 2 else 200
        if pencere_adi not in self.gui_pencereler:
            raise ValueError(f"Pencere bulunamadi: {pencere_adi}")
        pencere = self.gui_pencereler[pencere_adi]
        cubuk = ttk.Progressbar(pencere, length=uzunluk, mode='determinate')
        cubuk.pack(pady=5)
        self.degiskenler[cubuk_adi] = cubuk

    def canvas_olustur(self, satir):
        self.gui_kontrol()
        govde = satir[len('canvas '):].strip()
        parcalar = govde.split()
        canvas_adi = parcalar[0]
        pencere_adi = parcalar[1]
        genislik = int(parcalar[2]) if len(parcalar) > 2 else 400
        yukseklik = int(parcalar[3]) if len(parcalar) > 3 else 300
        arkaplan = parcalar[4] if len(parcalar) > 4 else 'white'
        if pencere_adi not in self.gui_pencereler:
            raise ValueError(f"Pencere bulunamadi: {pencere_adi}")
        pencere = self.gui_pencereler[pencere_adi]
        canvas = tk.Canvas(pencere, width=genislik, height=yukseklik, bg=arkaplan)
        canvas.pack(pady=5)
        self.degiskenler[canvas_adi] = canvas

    def frame_olustur(self, satir):
        self.gui_kontrol()
        govde = satir[len('frame '):].strip()
        parcalar = govde.split()
        frame_adi = parcalar[0]
        pencere_adi = parcalar[1]
        if pencere_adi not in self.gui_pencereler:
            raise ValueError(f"Pencere bulunamadi: {pencere_adi}")
        pencere = self.gui_pencereler[pencere_adi]
        frame = tk.Frame(pencere)
        frame.pack(pady=5, fill=tk.BOTH, expand=True)
        self.gui_pencereler[frame_adi] = frame
        self.degiskenler[frame_adi] = frame

    def ayirici_olustur(self, satir):
        self.gui_kontrol()
        govde = satir[len('ayirici '):].strip()
        parcalar = govde.split()
        ayirici_adi = parcalar[0]
        pencere_adi = parcalar[1]
        yon = parcalar[2] if len(parcalar) > 2 else "yatay"
        if pencere_adi not in self.gui_pencereler:
            raise ValueError(f"Pencere bulunamadi: {pencere_adi}")
        pencere = self.gui_pencereler[pencere_adi]
        orient = tk.HORIZONTAL if yon == "yatay" else tk.VERTICAL
        ayirici = ttk.Separator(pencere, orient=orient)
        ayirici.pack(fill=tk.X if yon == "yatay" else tk.Y, pady=5)
        self.degiskenler[ayirici_adi] = ayirici

    def menu_cubugu_olustur(self, satir):
        self.gui_kontrol()
        govde = satir[len('menu_cubugu '):].strip()
        parcalar = govde.split()
        cubuk_adi = parcalar[0]
        pencere_adi = parcalar[1]
        if pencere_adi not in self.gui_pencereler:
            raise ValueError(f"Pencere bulunamadi: {pencere_adi}")
        pencere = self.gui_pencereler[pencere_adi]
        menubar = tk.Menu(pencere)
        pencere.config(menu=menubar)
        self.tk_menuler[cubuk_adi] = menubar
        self.degiskenler[cubuk_adi] = menubar

    def menu_ekle(self, satir):
        self.gui_kontrol()
        govde = satir[len('menu_ekle '):].strip()
        parcalar = parse_qt_command(govde)
        menu_adi = parcalar[0]
        cubuk_adi = parcalar[1]
        baslik = self.ifade_hesapla(parcalar[2]) if len(parcalar) > 2 else menu_adi
        if cubuk_adi not in self.tk_menuler:
            raise ValueError(f"Menu cubugu bulunamadi: {cubuk_adi}")
        cubuk = self.tk_menuler[cubuk_adi]
        menu = tk.Menu(cubuk, tearoff=0)
        cubuk.add_cascade(label=str(baslik), menu=menu)
        self.tk_menuler[menu_adi] = menu
        self.degiskenler[menu_adi] = menu

    def menu_madde_ekle(self, satir):
        self.gui_kontrol()
        govde = satir[len('menu_madde_ekle '):].strip()
        parcalar = parse_qt_command(govde)
        menu_adi = parcalar[0]
        baslik = self.ifade_hesapla(parcalar[1])
        fonksiyon_adi = parcalar[2] if len(parcalar) > 2 else None
        if menu_adi not in self.tk_menuler:
            raise ValueError(f"Menu bulunamadi: {menu_adi}")
        menu = self.tk_menuler[menu_adi]
        komut = None
        if fonksiyon_adi and fonksiyon_adi in self.degiskenler:
            komut = self.degiskenler[fonksiyon_adi]
        menu.add_command(label=str(baslik), command=komut)

    def menu_ayirici_ekle(self, satir):
        self.gui_kontrol()
        menu_adi = satir[len('menu_ayirici_ekle '):].strip()
        if menu_adi not in self.tk_menuler:
            raise ValueError(f"Menu bulunamadi: {menu_adi}")
        self.tk_menuler[menu_adi].add_separator()

    def notebook_olustur(self, satir):
        self.gui_kontrol()
        govde = satir[len('notebook '):].strip()
        parcalar = govde.split()
        nb_adi = parcalar[0]
        pencere_adi = parcalar[1]
        if pencere_adi not in self.gui_pencereler:
            raise ValueError(f"Pencere bulunamadi: {pencere_adi}")
        pencere = self.gui_pencereler[pencere_adi]
        nb = ttk.Notebook(pencere)
        nb.pack(fill=tk.BOTH, expand=True)
        self.degiskenler[nb_adi] = nb

    def notebook_sekme_ekle(self, satir):
        self.gui_kontrol()
        govde = satir[len('notebook_sekme '):].strip()
        parcalar = parse_qt_command(govde)
        nb_adi = parcalar[0]
        sekme_adi = parcalar[1]
        baslik = self.ifade_hesapla(parcalar[2]) if len(parcalar) > 2 else sekme_adi
        if nb_adi not in self.degiskenler:
            raise ValueError(f"Notebook bulunamadi: {nb_adi}")
        nb = self.degiskenler[nb_adi]
        frame = tk.Frame(nb)
        nb.add(frame, text=str(baslik))
        self.gui_pencereler[sekme_adi] = frame
        self.degiskenler[sekme_adi] = frame

    def agac_olustur(self, satir):
        self.gui_kontrol()
        govde = satir[len('agac '):].strip()
        parcalar = govde.split()
        agac_adi = parcalar[0]
        pencere_adi = parcalar[1]
        if pencere_adi not in self.gui_pencereler:
            raise ValueError(f"Pencere bulunamadi: {pencere_adi}")
        pencere = self.gui_pencereler[pencere_adi]
        agac = ttk.Treeview(pencere)
        agac.pack(fill=tk.BOTH, expand=True, pady=5)
        self.degiskenler[agac_adi] = agac

    def agac_ekle(self, satir):
        self.gui_kontrol()
        govde = satir[len('agac_ekle '):].strip()
        parcalar = parse_qt_command(govde)
        agac_adi = parcalar[0]
        ust_adi = self.ifade_hesapla(parcalar[1])
        metin = self.ifade_hesapla(parcalar[2]) if len(parcalar) > 2 else ""
        if agac_adi not in self.degiskenler:
            raise ValueError(f"Agac bulunamadi: {agac_adi}")
        agac = self.degiskenler[agac_adi]
        node_id = agac.insert(str(ust_adi), 'end', text=str(metin))
        self.degiskenler[f"{agac_adi}_son"] = node_id

    def tablo_olustur(self, satir):
        self.gui_kontrol()
        govde = satir[len('tablo '):].strip()
        parcalar = govde.split()
        tablo_adi = parcalar[0]
        pencere_adi = parcalar[1]
        if pencere_adi not in self.gui_pencereler:
            raise ValueError(f"Pencere bulunamadi: {pencere_adi}")
        pencere = self.gui_pencereler[pencere_adi]
        tablo = ttk.Treeview(pencere, show='headings')
        tablo.pack(fill=tk.BOTH, expand=True, pady=5)
        self.degiskenler[tablo_adi] = tablo

    def tablo_sutun_ekle(self, satir):
        self.gui_kontrol()
        govde = satir[len('tablo_sutun '):].strip()
        parcalar = parse_qt_command(govde)
        tablo_adi = parcalar[0]
        sutun_adi = self.ifade_hesapla(parcalar[1])
        genislik = int(parcalar[2]) if len(parcalar) > 2 else 100
        if tablo_adi not in self.degiskenler:
            raise ValueError(f"Tablo bulunamadi: {tablo_adi}")
        tablo = self.degiskenler[tablo_adi]
        mevcut = list(tablo['columns'])
        mevcut.append(str(sutun_adi))
        tablo['columns'] = mevcut
        tablo.column(str(sutun_adi), width=genislik)
        tablo.heading(str(sutun_adi), text=str(sutun_adi))

    def tablo_satir_ekle(self, satir):
        self.gui_kontrol()
        govde = satir[len('tablo_satir '):].strip()
        parcalar = parse_qt_command(govde)
        tablo_adi = parcalar[0]
        degerler = self.ifade_hesapla(parcalar[1]) if len(parcalar) > 1 else []
        if tablo_adi not in self.degiskenler:
            raise ValueError(f"Tablo bulunamadi: {tablo_adi}")
        tablo = self.degiskenler[tablo_adi]
        tablo.insert('', 'end', values=degerler)

    def kaydirma_alani_olustur(self, satir):
        self.gui_kontrol()
        govde = satir[len('kaydirma_alani '):].strip()
        parcalar = govde.split()
        alan_adi = parcalar[0]
        pencere_adi = parcalar[1]
        if pencere_adi not in self.gui_pencereler:
            raise ValueError(f"Pencere bulunamadi: {pencere_adi}")
        pencere = self.gui_pencereler[pencere_adi]
        cerceve = tk.Frame(pencere)
        cerceve.pack(fill=tk.BOTH, expand=True)
        canvas = tk.Canvas(cerceve)
        scrollbar = ttk.Scrollbar(cerceve, orient='vertical', command=canvas.yview)
        ic_frame = tk.Frame(canvas)
        ic_frame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.create_window((0, 0), window=ic_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.gui_pencereler[alan_adi] = ic_frame
        self.degiskenler[alan_adi] = ic_frame

    def degistirici_olustur(self, satir):
        self.gui_kontrol()
        govde = satir[len('degistirici '):].strip()
        parcalar = govde.split()
        deg_adi = parcalar[0]
        pencere_adi = parcalar[1]
        if pencere_adi not in self.gui_pencereler:
            raise ValueError(f"Pencere bulunamadi: {pencere_adi}")
        pencere = self.gui_pencereler[pencere_adi]
        pw = ttk.PanedWindow(pencere, orient=tk.HORIZONTAL)
        pw.pack(fill=tk.BOTH, expand=True)
        self.degiskenler[deg_adi] = pw

    def sayac_kutu_olustur(self, satir):
        self.gui_kontrol()
        govde = satir[len('sayac_kutu '):].strip()
        parcalar = govde.split()
        sayac_adi = parcalar[0]
        pencere_adi = parcalar[1]
        baslangic = float(parcalar[2]) if len(parcalar) > 2 else 0
        adim = float(parcalar[3]) if len(parcalar) > 3 else 1
        if pencere_adi not in self.gui_pencereler:
            raise ValueError(f"Pencere bulunamadi: {pencere_adi}")
        pencere = self.gui_pencereler[pencere_adi]
        sb = ttk.Spinbox(pencere, from_=baslangic, increment=adim, to=9999)
        sb.pack(pady=5)
        self.degiskenler[sayac_adi] = sb

    def renk_sec(self, satir):
        self.gui_kontrol()
        degisken_adi = satir[len('renk_sec '):].strip()
        renk = colorchooser.askcolor(title="Renk Sec")
        self.degiskenler[degisken_adi] = renk

    def dosya_sec(self, satir):
        self.gui_kontrol()
        govde = satir[len('dosya_sec '):].strip()
        parcalar = govde.split()
        degisken_adi = parcalar[0]
        dosya = filedialog.askopenfilename()
        self.degiskenler[degisken_adi] = dosya

    def klasor_sec(self, satir):
        self.gui_kontrol()
        degisken_adi = satir[len('klasor_sec '):].strip()
        klasor = filedialog.askdirectory()
        self.degiskenler[degisken_adi] = klasor

    def yazi_tipi_sec(self, satir):
        self.gui_kontrol()
        degisken_adi = satir[len('yazi_sec '):].strip()
        try:
            yazi = tkfont.askfont()
            self.degiskenler[degisken_adi] = yazi
        except Exception:
            self.degiskenler[degisken_adi] = None

    def pencere_goster(self, satir):
        self.gui_kontrol()
        pencere_adi = satir[len('pencere_goster '):].strip()
        if pencere_adi not in self.gui_pencereler:
            raise ValueError(f"Pencere bulunamadi: {pencere_adi}")
        self.gui_pencereler[pencere_adi].mainloop()

    def mesaj_kutusu(self, satir):
        self.gui_kontrol()
        govde = satir[len('mesaj_kutusu '):].strip()
        elemanlar = self.listeyi_ayir(govde)
        baslik = self.ifade_hesapla(elemanlar[0])
        mesaj = self.ifade_hesapla(elemanlar[1])
        messagebox.showinfo(str(baslik), str(mesaj))

    def soru_kutusu(self, satir):
        self.gui_kontrol()
        govde = satir[len('soru_kutusu '):].strip()
        parcalar = parse_qt_command(govde)
        degisken_adi = parcalar[0]
        baslik = self.ifade_hesapla(parcalar[1])
        mesaj = self.ifade_hesapla(parcalar[2])
        sonuc = messagebox.askyesno(str(baslik), str(mesaj))
        self.degiskenler[degisken_adi] = sonuc

    def uyari_kutusu(self, satir):
        self.gui_kontrol()
        govde = satir[len('uyari_kutusu '):].strip()
        elemanlar = self.listeyi_ayir(govde)
        baslik = self.ifade_hesapla(elemanlar[0])
        mesaj = self.ifade_hesapla(elemanlar[1])
        messagebox.showwarning(str(baslik), str(mesaj))

    def hata_kutusu(self, satir):
        self.gui_kontrol()
        govde = satir[len('hata_kutusu '):].strip()
        elemanlar = self.listeyi_ayir(govde)
        baslik = self.ifade_hesapla(elemanlar[0])
        mesaj = self.ifade_hesapla(elemanlar[1])
        messagebox.showerror(str(baslik), str(mesaj))

    def giris_kutusu(self, satir):
        self.gui_kontrol()
        govde = satir[len('giris_kutusu '):].strip()
        parcalar = parse_qt_command(govde)
        degisken_adi = parcalar[0]
        baslik = self.ifade_hesapla(parcalar[1])
        mesaj = self.ifade_hesapla(parcalar[2]) if len(parcalar) > 2 else ""
        sonuc = simpledialog.askstring(str(baslik), str(mesaj))
        self.degiskenler[degisken_adi] = sonuc

    def pencere_baslik_ayarla(self, satir):
        self.gui_kontrol()
        govde = satir[len('pencere_baslik '):].strip()
        parcalar = parse_qt_command(govde)
        pencere_adi = parcalar[0]
        baslik = self.ifade_hesapla(parcalar[1])
        if pencere_adi not in self.gui_pencereler:
            raise ValueError(f"Pencere bulunamadi: {pencere_adi}")
        self.gui_pencereler[pencere_adi].title(str(baslik))

    def pencere_boyut_ayarla(self, satir):
        self.gui_kontrol()
        govde = satir[len('pencere_boyut '):].strip()
        parcalar = govde.split()
        pencere_adi = parcalar[0]
        genislik = int(parcalar[1])
        yukseklik = int(parcalar[2])
        if pencere_adi not in self.gui_pencereler:
            raise ValueError(f"Pencere bulunamadi: {pencere_adi}")
        self.gui_pencereler[pencere_adi].geometry(f"{genislik}x{yukseklik}")

    def pencere_renk_ayarla(self, satir):
        self.gui_kontrol()
        govde = satir[len('pencere_renk '):].strip()
        parcalar = parse_qt_command(govde)
        pencere_adi = parcalar[0]
        renk = self.ifade_hesapla(parcalar[1])
        if pencere_adi not in self.gui_pencereler:
            raise ValueError(f"Pencere bulunamadi: {pencere_adi}")
        self.gui_pencereler[pencere_adi].configure(bg=str(renk))

    def pencere_kapat(self, satir):
        self.gui_kontrol()
        pencere_adi = satir[len('pencere_kapat '):].strip()
        if pencere_adi in self.gui_pencereler:
            self.gui_pencereler[pencere_adi].destroy()

    def pencere_guncelle(self, satir):
        self.gui_kontrol()
        pencere_adi = satir[len('guncelle '):].strip()
        if pencere_adi in self.gui_pencereler:
            self.gui_pencereler[pencere_adi].update()

    def widget_renk_ayarla(self, satir):
        self.gui_kontrol()
        govde = satir[len('widget_renk '):].strip()
        parcalar = parse_qt_command(govde)
        widget_adi = parcalar[0]
        on_renk = self.ifade_hesapla(parcalar[1]) if len(parcalar) > 1 else None
        arka_renk = self.ifade_hesapla(parcalar[2]) if len(parcalar) > 2 else None
        if widget_adi not in self.degiskenler:
            return
        widget = self.degiskenler[widget_adi]
        try:
            kwargs = {}
            if on_renk: kwargs['fg'] = str(on_renk)
            if arka_renk: kwargs['bg'] = str(arka_renk)
            widget.configure(**kwargs)
        except Exception:
            pass

    def widget_font_ayarla(self, satir):
        self.gui_kontrol()
        govde = satir[len('widget_font '):].strip()
        parcalar = parse_qt_command(govde)
        widget_adi = parcalar[0]
        aile = self.ifade_hesapla(parcalar[1]) if len(parcalar) > 1 else "Arial"
        boyut = int(parcalar[2]) if len(parcalar) > 2 else 12
        stil = self.ifade_hesapla(parcalar[3]) if len(parcalar) > 3 else "normal"
        if widget_adi not in self.degiskenler:
            return
        widget = self.degiskenler[widget_adi]
        try:
            widget.configure(font=(str(aile), boyut, str(stil)))
        except Exception:
            pass

    def widget_yerlestir(self, satir):
        self.gui_kontrol()
        govde = satir[len('widget_yerlestir '):].strip()
        parcalar = govde.split()
        widget_adi = parcalar[0]
        x = int(parcalar[1]) if len(parcalar) > 1 else 0
        y = int(parcalar[2]) if len(parcalar) > 2 else 0
        if widget_adi not in self.degiskenler:
            return
        try:
            self.degiskenler[widget_adi].place(x=x, y=y)
        except Exception:
            pass

    def widget_gizle(self, satir):
        self.gui_kontrol()
        widget_adi = satir[len('widget_gizle '):].strip()
        if widget_adi in self.degiskenler:
            try:
                self.degiskenler[widget_adi].pack_forget()
            except Exception:
                pass

    def widget_goster(self, satir):
        self.gui_kontrol()
        widget_adi = satir[len('widget_goster '):].strip()
        if widget_adi in self.degiskenler:
            try:
                self.degiskenler[widget_adi].pack()
            except Exception:
                pass

    def widget_etkinlestir(self, satir):
        self.gui_kontrol()
        widget_adi = satir[len('widget_etkinlestir '):].strip()
        if widget_adi in self.degiskenler:
            try:
                self.degiskenler[widget_adi].configure(state='normal')
            except Exception:
                pass

    def widget_devre_disi(self, satir):
        self.gui_kontrol()
        widget_adi = satir[len('widget_devre_disi '):].strip()
        if widget_adi in self.degiskenler:
            try:
                self.degiskenler[widget_adi].configure(state='disabled')
            except Exception:
                pass

    def widget_sil(self, satir):
        self.gui_kontrol()
        widget_adi = satir[len('widget_sil '):].strip()
        if widget_adi in self.degiskenler:
            try:
                self.degiskenler[widget_adi].destroy()
                del self.degiskenler[widget_adi]
            except Exception:
                pass

    def widget_deger_al(self, satir):
        self.gui_kontrol()
        govde = satir[len('widget_deger '):].strip()
        parcalar = govde.split()
        widget_adi = parcalar[0]
        degisken_adi = parcalar[1]
        if widget_adi not in self.degiskenler:
            raise ValueError(f"Widget bulunamadi: {widget_adi}")
        widget = self.degiskenler[widget_adi]
        try:
            if isinstance(widget, tk.Entry):
                deger = widget.get()
            elif isinstance(widget, tk.Text):
                deger = widget.get("1.0", tk.END)
            elif isinstance(widget, (tk.Scale, ttk.Combobox)):
                deger = widget.get()
            elif isinstance(widget, (tk.BooleanVar, tk.StringVar)):
                deger = widget.get()
            elif isinstance(widget, tk.Listbox):
                deger = widget.get(0, tk.END)
            elif isinstance(widget, ttk.Spinbox):
                deger = widget.get()
            elif isinstance(widget, ttk.Treeview):
                sel = widget.selection()
                deger = [widget.item(s, 'text') for s in sel]
            else:
                deger = None
            self.degiskenler[degisken_adi] = deger
        except Exception as e:
            print(f"Widget deger alma hatasi: {e}")

    def widget_deger_ayarla(self, satir):
        self.gui_kontrol()
        govde = satir[len('widget_ayarla '):].strip()
        parcalar = parse_qt_command(govde)
        widget_adi = parcalar[0]
        deger = self.ifade_hesapla(parcalar[1])
        if widget_adi not in self.degiskenler:
            raise ValueError(f"Widget bulunamadi: {widget_adi}")
        widget = self.degiskenler[widget_adi]
        try:
            if isinstance(widget, tk.Entry):
                widget.delete(0, tk.END)
                widget.insert(0, str(deger))
            elif isinstance(widget, tk.Text):
                widget.delete("1.0", tk.END)
                widget.insert("1.0", str(deger))
            elif isinstance(widget, (tk.Scale, ttk.Progressbar)):
                widget.set(deger)
            elif isinstance(widget, ttk.Combobox):
                widget.set(deger)
            elif isinstance(widget, (tk.BooleanVar, tk.StringVar)):
                widget.set(deger)
            elif isinstance(widget, tk.Label):
                widget.config(text=str(deger))
            elif isinstance(widget, ttk.Spinbox):
                widget.set(deger)
            elif isinstance(widget, tk.Listbox):
                widget.delete(0, tk.END)
                if isinstance(deger, (list, tuple)):
                    for item in deger:
                        widget.insert(tk.END, item)
        except Exception as e:
            print(f"Widget deger ayarlama hatasi: {e}")

    def canvas_cizgi(self, satir):
        self.gui_kontrol()
        govde = satir[len('canvas_cizgi '):].strip()
        parcalar = parse_qt_command(govde)
        canvas_adi = parcalar[0]
        x1 = int(self.ifade_hesapla(parcalar[1]))
        y1 = int(self.ifade_hesapla(parcalar[2]))
        x2 = int(self.ifade_hesapla(parcalar[3]))
        y2 = int(self.ifade_hesapla(parcalar[4]))
        renk = self.ifade_hesapla(parcalar[5]) if len(parcalar) > 5 else 'black'
        kalinlik = int(parcalar[6]) if len(parcalar) > 6 else 1
        if canvas_adi not in self.degiskenler:
            return
        canvas = self.degiskenler[canvas_adi]
        nesne_id = canvas.create_line(x1, y1, x2, y2, fill=str(renk), width=kalinlik)
        self.degiskenler[f"{canvas_adi}_son"] = nesne_id

    def canvas_dikdortgen(self, satir):
        self.gui_kontrol()
        govde = satir[len('canvas_dikdortgen '):].strip()
        parcalar = parse_qt_command(govde)
        canvas_adi = parcalar[0]
        x1 = int(self.ifade_hesapla(parcalar[1]))
        y1 = int(self.ifade_hesapla(parcalar[2]))
        x2 = int(self.ifade_hesapla(parcalar[3]))
        y2 = int(self.ifade_hesapla(parcalar[4]))
        renk = self.ifade_hesapla(parcalar[5]) if len(parcalar) > 5 else 'black'
        dolgu = self.ifade_hesapla(parcalar[6]) if len(parcalar) > 6 else ''
        if canvas_adi not in self.degiskenler:
            return
        canvas = self.degiskenler[canvas_adi]
        nesne_id = canvas.create_rectangle(x1, y1, x2, y2, outline=str(renk), fill=str(dolgu))
        self.degiskenler[f"{canvas_adi}_son"] = nesne_id

    def canvas_oval(self, satir):
        self.gui_kontrol()
        govde = satir[len('canvas_oval '):].strip()
        parcalar = parse_qt_command(govde)
        canvas_adi = parcalar[0]
        x1 = int(self.ifade_hesapla(parcalar[1]))
        y1 = int(self.ifade_hesapla(parcalar[2]))
        x2 = int(self.ifade_hesapla(parcalar[3]))
        y2 = int(self.ifade_hesapla(parcalar[4]))
        renk = self.ifade_hesapla(parcalar[5]) if len(parcalar) > 5 else 'black'
        dolgu = self.ifade_hesapla(parcalar[6]) if len(parcalar) > 6 else ''
        if canvas_adi not in self.degiskenler:
            return
        canvas = self.degiskenler[canvas_adi]
        nesne_id = canvas.create_oval(x1, y1, x2, y2, outline=str(renk), fill=str(dolgu))
        self.degiskenler[f"{canvas_adi}_son"] = nesne_id

    def canvas_metin(self, satir):
        self.gui_kontrol()
        govde = satir[len('canvas_metin '):].strip()
        parcalar = parse_qt_command(govde)
        canvas_adi = parcalar[0]
        x = int(self.ifade_hesapla(parcalar[1]))
        y = int(self.ifade_hesapla(parcalar[2]))
        metin = self.ifade_hesapla(parcalar[3])
        renk = self.ifade_hesapla(parcalar[4]) if len(parcalar) > 4 else 'black'
        if canvas_adi not in self.degiskenler:
            return
        canvas = self.degiskenler[canvas_adi]
        nesne_id = canvas.create_text(x, y, text=str(metin), fill=str(renk))
        self.degiskenler[f"{canvas_adi}_son"] = nesne_id

    def canvas_resim(self, satir):
        self.gui_kontrol()
        govde = satir[len('canvas_resim '):].strip()
        parcalar = parse_qt_command(govde)
        canvas_adi = parcalar[0]
        x = int(self.ifade_hesapla(parcalar[1]))
        y = int(self.ifade_hesapla(parcalar[2]))
        resim_adi = parcalar[3]
        if canvas_adi not in self.degiskenler:
            return
        canvas = self.degiskenler[canvas_adi]
        resim = self.degiskenler.get(resim_adi)
        if resim:
            nesne_id = canvas.create_image(x, y, image=resim)
            self.degiskenler[f"{canvas_adi}_son"] = nesne_id

    def canvas_temizle(self, satir):
        self.gui_kontrol()
        canvas_adi = satir[len('canvas_temizle '):].strip()
        if canvas_adi in self.degiskenler:
            self.degiskenler[canvas_adi].delete('all')

    def canvas_nesne_sil(self, satir):
        self.gui_kontrol()
        govde = satir[len('canvas_nesne_sil '):].strip()
        parcalar = govde.split()
        canvas_adi = parcalar[0]
        nesne_adi = parcalar[1]
        if canvas_adi in self.degiskenler and nesne_adi in self.degiskenler:
            self.degiskenler[canvas_adi].delete(self.degiskenler[nesne_adi])

    def olay_bagla(self, satir):
        self.gui_kontrol()
        govde = satir[len('olay_bagla '):].strip()
        parcalar = parse_qt_command(govde)
        widget_adi = parcalar[0]
        olay = self.ifade_hesapla(parcalar[1])
        fonksiyon_adi = parcalar[2]
        if widget_adi not in self.degiskenler:
            return
        widget = self.degiskenler[widget_adi]
        fonksiyon = self.degiskenler.get(fonksiyon_adi)
        if fonksiyon and callable(fonksiyon):
            widget.bind(str(olay), fonksiyon)

    def tk_timer_olustur(self, satir):
        self.gui_kontrol()
        govde = satir[len('timer_olustur '):].strip()
        parcalar = govde.split()
        pencere_adi = parcalar[0]
        sure = int(parcalar[1])
        fonksiyon_adi = parcalar[2] if len(parcalar) > 2 else None
        if pencere_adi not in self.gui_pencereler:
            return
        pencere = self.gui_pencereler[pencere_adi]
        fonksiyon = self.degiskenler.get(fonksiyon_adi) if fonksiyon_adi else None
        if fonksiyon and callable(fonksiyon):
            pencere.after(sure, fonksiyon)

    # ==================== PYSIDE6 GUI ====================

    def pyside6_kontrol(self):
        if not PYSIDE6_AVAILABLE:
            raise ImportError("PySide6 kurulu degil.")

    def _widget_ekle(self, widget, parent_adi):
        if parent_adi in self.qt_widget_to_layout:
            layout_name = self.qt_widget_to_layout[parent_adi]
            layout = self.qt_layoutlar.get(layout_name)
            if layout:
                layout.addWidget(widget)
                return True
        if parent_adi in self.qt_layoutlar:
            self.qt_layoutlar[parent_adi].addWidget(widget)
            return True
        return False

    def qt_pencere_olustur(self, satir):
        self.pyside6_kontrol()
        govde = satir[len('qt_pencere '):].strip()
        parcalar = parse_qt_command(govde)
        pencere_adi = parcalar[0]
        baslik = self.ifade_hesapla(parcalar[1]) if len(parcalar) > 1 else "TSharp Qt Pencere"
        genislik = int(parcalar[2]) if len(parcalar) > 2 else 800
        yukseklik = int(parcalar[3]) if len(parcalar) > 3 else 600
        pencere = QMainWindow()
        pencere.setWindowTitle(str(baslik))
        pencere.resize(genislik, yukseklik)
        merkez_widget = QWidget()
        pencere.setCentralWidget(merkez_widget)
        self.qt_pencereler[pencere_adi] = pencere
        self.degiskenler[pencere_adi] = pencere
        self.degiskenler[f"{pencere_adi}_merkez"] = merkez_widget

    def qt_layout_olustur(self, satir):
        self.pyside6_kontrol()
        govde = satir[len('qt_layout '):].strip()
        parcalar = parse_qt_command(govde)
        layout_adi = parcalar[0]
        tip = parcalar[1] if len(parcalar) > 1 else "dikey"
        parent_adi = parcalar[2] if len(parcalar) > 2 else None
        if tip == "dikey":
            layout = QVBoxLayout()
        elif tip == "yatay":
            layout = QHBoxLayout()
        elif tip == "grid":
            layout = QGridLayout()
        elif tip == "form":
            layout = QFormLayout()
        else:
            layout = QVBoxLayout()
        self.qt_layoutlar[layout_adi] = layout
        self.degiskenler[layout_adi] = layout
        if parent_adi:
            parent = self.degiskenler.get(parent_adi)
            if parent:
                parent.setLayout(layout)
                self.qt_widget_to_layout[parent_adi] = layout_adi

    def qt_etiket_olustur(self, satir):
        self.pyside6_kontrol()
        govde = satir[len('qt_etiket '):].strip()
        parcalar = parse_qt_command(govde)
        etiket_adi = parcalar[0]
        metin = self.ifade_hesapla(parcalar[1])
        parent_adi = parcalar[2]
        parent = self.degiskenler.get(parent_adi)
        if parent is None:
            raise ValueError(f"Parent bulunamadi: {parent_adi}")
        etiket = QLabel(str(metin), parent)
        self._widget_ekle(etiket, parent_adi)
        self.degiskenler[etiket_adi] = etiket

    def qt_giriskutusu_olustur(self, satir):
        self.pyside6_kontrol()
        govde = satir[len('qt_giriskutusu '):].strip()
        parcalar = parse_qt_command(govde)
        giris_adi = parcalar[0]
        parent_adi = parcalar[1]
        parent = self.degiskenler.get(parent_adi)
        if parent is None:
            raise ValueError(f"Parent bulunamadi: {parent_adi}")
        giris = QLineEdit(parent)
        self._widget_ekle(giris, parent_adi)
        self.degiskenler[giris_adi] = giris

    def qt_buton_olustur(self, satir):
        self.pyside6_kontrol()
        govde = satir[len('qt_buton '):].strip()
        parcalar = parse_qt_command(govde)
        buton_adi = parcalar[0]
        metin = self.ifade_hesapla(parcalar[1])
        parent_adi = parcalar[2]
        fonksiyon_adi = parcalar[3] if len(parcalar) > 3 else None
        parent = self.degiskenler.get(parent_adi)
        if parent is None:
            raise ValueError(f"Parent bulunamadi: {parent_adi}")
        buton = QPushButton(str(metin), parent)
        self._widget_ekle(buton, parent_adi)
        if fonksiyon_adi and fonksiyon_adi in self.degiskenler:
            fonksiyon = self.degiskenler[fonksiyon_adi]
            if callable(fonksiyon):
                buton.clicked.connect(fonksiyon)
        self.degiskenler[buton_adi] = buton

    def qt_onay_kutusu_olustur(self, satir):
        self.pyside6_kontrol()
        govde = satir[len('qt_onay_kutusu '):].strip()
        parcalar = parse_qt_command(govde)
        onay_adi = parcalar[0]
        metin = self.ifade_hesapla(parcalar[1])
        parent_adi = parcalar[2]
        parent = self.degiskenler.get(parent_adi)
        if parent is None:
            raise ValueError(f"Parent bulunamadi: {parent_adi}")
        onay = QCheckBox(str(metin), parent)
        self._widget_ekle(onay, parent_adi)
        self.degiskenler[onay_adi] = onay

    def qt_radyo_buton_olustur(self, satir):
        self.pyside6_kontrol()
        govde = satir[len('qt_radyo_buton '):].strip()
        parcalar = parse_qt_command(govde)
        radyo_adi = parcalar[0]
        metin = self.ifade_hesapla(parcalar[1])
        parent_adi = parcalar[2]
        parent = self.degiskenler.get(parent_adi)
        if parent is None:
            raise ValueError(f"Parent bulunamadi: {parent_adi}")
        radyo = QRadioButton(str(metin), parent)
        self._widget_ekle(radyo, parent_adi)
        self.degiskenler[radyo_adi] = radyo

    def qt_combo_kutu_olustur(self, satir):
        self.pyside6_kontrol()
        govde = satir[len('qt_combo_kutu '):].strip()
        parcalar = parse_qt_command(govde)
        combo_adi = parcalar[0]
        parent_adi = parcalar[1]
        parent = self.degiskenler.get(parent_adi)
        if parent is None:
            raise ValueError(f"Parent bulunamadi: {parent_adi}")
        combo = QComboBox(parent)
        self._widget_ekle(combo, parent_adi)
        self.degiskenler[combo_adi] = combo

    def qt_liste_widget_olustur(self, satir):
        self.pyside6_kontrol()
        govde = satir[len('qt_liste_widget '):].strip()
        parcalar = parse_qt_command(govde)
        liste_adi = parcalar[0]
        parent_adi = parcalar[1]
        parent = self.degiskenler.get(parent_adi)
        if parent is None:
            raise ValueError(f"Parent bulunamadi: {parent_adi}")
        liste = QListWidget(parent)
        self._widget_ekle(liste, parent_adi)
        self.degiskenler[liste_adi] = liste

    def qt_tablo_widget_olustur(self, satir):
        self.pyside6_kontrol()
        govde = satir[len('qt_tablo_widget '):].strip()
        parcalar = parse_qt_command(govde)
        tablo_adi = parcalar[0]
        parent_adi = parcalar[1]
        satirlar_s = int(parcalar[2]) if len(parcalar) > 2 else 5
        sutunlar = int(parcalar[3]) if len(parcalar) > 3 else 3
        parent = self.degiskenler.get(parent_adi)
        if parent is None:
            raise ValueError(f"Parent bulunamadi: {parent_adi}")
        tablo = QTableWidget(satirlar_s, sutunlar, parent)
        self._widget_ekle(tablo, parent_adi)
        self.degiskenler[tablo_adi] = tablo

    def qt_agac_widget_olustur(self, satir):
        self.pyside6_kontrol()
        govde = satir[len('qt_agac_widget '):].strip()
        parcalar = parse_qt_command(govde)
        agac_adi = parcalar[0]
        parent_adi = parcalar[1]
        parent = self.degiskenler.get(parent_adi)
        if parent is None:
            raise ValueError(f"Parent bulunamadi: {parent_adi}")
        agac = QTreeWidget(parent)
        self._widget_ekle(agac, parent_adi)
        self.degiskenler[agac_adi] = agac

    def qt_sekme_widget_olustur(self, satir):
        self.pyside6_kontrol()
        govde = satir[len('qt_sekme_widget '):].strip()
        parcalar = parse_qt_command(govde)
        sekme_adi = parcalar[0]
        parent_adi = parcalar[1]
        parent = self.degiskenler.get(parent_adi)
        if parent is None:
            raise ValueError(f"Parent bulunamadi: {parent_adi}")
        sekme = QTabWidget(parent)
        self._widget_ekle(sekme, parent_adi)
        self.degiskenler[sekme_adi] = sekme

    def qt_kaydirici_olustur(self, satir):
        self.pyside6_kontrol()
        govde = satir[len('qt_kaydirici '):].strip()
        parcalar = parse_qt_command(govde)
        kaydirici_adi = parcalar[0]
        parent_adi = parcalar[1]
        yon = parcalar[2] if len(parcalar) > 2 else "yatay"
        min_deger = int(parcalar[3]) if len(parcalar) > 3 else 0
        max_deger = int(parcalar[4]) if len(parcalar) > 4 else 100
        parent = self.degiskenler.get(parent_adi)
        if parent is None:
            raise ValueError(f"Parent bulunamadi: {parent_adi}")
        orientation = Qt.Horizontal if yon == "yatay" else Qt.Vertical
        kaydirici = QSlider(orientation, parent)
        kaydirici.setMinimum(min_deger)
        kaydirici.setMaximum(max_deger)
        self._widget_ekle(kaydirici, parent_adi)
        self.degiskenler[kaydirici_adi] = kaydirici

    def qt_ilerleme_cubugu_olustur(self, satir):
        self.pyside6_kontrol()
        govde = satir[len('qt_ilerleme_cubugu '):].strip()
        parcalar = parse_qt_command(govde)
        ilerleme_adi = parcalar[0]
        parent_adi = parcalar[1]
        parent = self.degiskenler.get(parent_adi)
        if parent is None:
            raise ValueError(f"Parent bulunamadi: {parent_adi}")
        ilerleme = QProgressBar(parent)
        self._widget_ekle(ilerleme, parent_adi)
        self.degiskenler[ilerleme_adi] = ilerleme

    def qt_spin_kutu_olustur(self, satir):
        self.pyside6_kontrol()
        govde = satir[len('qt_spin_kutu '):].strip()
        parcalar = parse_qt_command(govde)
        spin_adi = parcalar[0]
        parent_adi = parcalar[1]
        min_deger = int(parcalar[2]) if len(parcalar) > 2 else 0
        max_deger = int(parcalar[3]) if len(parcalar) > 3 else 100
        parent = self.degiskenler.get(parent_adi)
        if parent is None:
            raise ValueError(f"Parent bulunamadi: {parent_adi}")
        spin = QSpinBox(parent)
        spin.setMinimum(min_deger)
        spin.setMaximum(max_deger)
        self._widget_ekle(spin, parent_adi)
        self.degiskenler[spin_adi] = spin

    def qt_tarih_secici_olustur(self, satir):
        self.pyside6_kontrol()
        govde = satir[len('qt_tarih_secici '):].strip()
        parcalar = parse_qt_command(govde)
        tarih_adi = parcalar[0]
        parent_adi = parcalar[1]
        parent = self.degiskenler.get(parent_adi)
        if parent is None:
            raise ValueError(f"Parent bulunamadi: {parent_adi}")
        tarih = QDateEdit(parent)
        tarih.setCalendarPopup(True)
        self._widget_ekle(tarih, parent_adi)
        self.degiskenler[tarih_adi] = tarih

    def qt_saat_secici_olustur(self, satir):
        self.pyside6_kontrol()
        govde = satir[len('qt_saat_secici '):].strip()
        parcalar = parse_qt_command(govde)
        saat_adi = parcalar[0]
        parent_adi = parcalar[1]
        parent = self.degiskenler.get(parent_adi)
        if parent is None:
            raise ValueError(f"Parent bulunamadi: {parent_adi}")
        saat = QTimeEdit(parent)
        self._widget_ekle(saat, parent_adi)
        self.degiskenler[saat_adi] = saat

    def qt_takvim_olustur(self, satir):
        self.pyside6_kontrol()
        govde = satir[len('qt_takvim '):].strip()
        parcalar = parse_qt_command(govde)
        takvim_adi = parcalar[0]
        parent_adi = parcalar[1]
        parent = self.degiskenler.get(parent_adi)
        if parent is None:
            raise ValueError(f"Parent bulunamadi: {parent_adi}")
        takvim = QCalendarWidget(parent)
        self._widget_ekle(takvim, parent_adi)
        self.degiskenler[takvim_adi] = takvim

    def qt_web_tarayici_olustur(self, satir):
        if not WEBENGINE_AVAILABLE:
            raise ImportError("QWebEngineView kullanamıyor.")
        self.pyside6_kontrol()
        govde = satir[len('qt_web_tarayici '):].strip()
        parcalar = parse_qt_command(govde)
        web_adi = parcalar[0]
        parent_adi = parcalar[1]
        url = self.ifade_hesapla(parcalar[2]) if len(parcalar) > 2 else "https://www.google.com"
        parent = self.degiskenler.get(parent_adi)
        if parent is None:
            raise ValueError(f"Parent bulunamadi: {parent_adi}")
        web = QWebEngineView(parent)
        web.setUrl(QUrl(str(url)))
        self._widget_ekle(web, parent_adi)
        self.degiskenler[web_adi] = web

    def qt_video_oynatici_olustur(self, satir):
        if not MULTIMEDIA_AVAILABLE:
            raise ImportError("Multimedia kullanamıyor.")
        self.pyside6_kontrol()
        govde = satir[len('qt_video_oynatici '):].strip()
        parcalar = parse_qt_command(govde)
        video_adi = parcalar[0]
        parent_adi = parcalar[1]
        parent = self.degiskenler.get(parent_adi)
        if parent is None:
            raise ValueError(f"Parent bulunamadi: {parent_adi}")
        video = QVideoWidget(parent)
        player = QMediaPlayer()
        audio = QAudioOutput()
        player.setVideoOutput(video)
        player.setAudioOutput(audio)
        self._widget_ekle(video, parent_adi)
        self.degiskenler[video_adi] = video
        self.degiskenler[f"{video_adi}_player"] = player
        self.degiskenler[f"{video_adi}_audio"] = audio

    def qt_grafik_olustur(self, satir):
        if not CHARTS_AVAILABLE:
            raise ImportError("Charts kullanamıyor.")
        self.pyside6_kontrol()
        govde = satir[len('qt_grafik '):].strip()
        parcalar = parse_qt_command(govde)
        grafik_adi = parcalar[0]
        parent_adi = parcalar[1]
        tip = self.ifade_hesapla(parcalar[2]) if len(parcalar) > 2 else "cizgi"
        parent = self.degiskenler.get(parent_adi)
        if parent is None:
            raise ValueError(f"Parent bulunamadi: {parent_adi}")
        chart = QChart()
        if tip == "cizgi":
            series = QLineSeries()
        elif tip == "pasta":
            series = QPieSeries()
        elif tip == "cubuk":
            series = QBarSeries()
        else:
            series = QLineSeries()
        chart.addSeries(series)
        chart_view = QChartView(chart, parent)
        chart_view.setRenderHint(QPainter.Antialiasing)
        self._widget_ekle(chart_view, parent_adi)
        self.degiskenler[grafik_adi] = chart_view
        self.degiskenler[f"{grafik_adi}_chart"] = chart
        self.degiskenler[f"{grafik_adi}_series"] = series

    def qt_metin_alani_olustur(self, satir):
        self.pyside6_kontrol()
        govde = satir[len('qt_metin_alani '):].strip()
        parcalar = parse_qt_command(govde)
        alan_adi = parcalar[0]
        parent_adi = parcalar[1]
        parent = self.degiskenler.get(parent_adi)
        if parent is None:
            raise ValueError(f"Parent bulunamadi: {parent_adi}")
        metin_alani = QTextEdit(parent)
        self._widget_ekle(metin_alani, parent_adi)
        self.degiskenler[alan_adi] = metin_alani

    def qt_menu_olustur(self, satir):
        self.pyside6_kontrol()
        govde = satir[len('qt_menu '):].strip()
        parcalar = parse_qt_command(govde)
        menu_adi = parcalar[0]
        baslik = self.ifade_hesapla(parcalar[1])
        pencere_adi = parcalar[2]
        pencere = self.qt_pencereler.get(pencere_adi)
        if pencere is None:
            raise ValueError(f"Pencere bulunamadi: {pencere_adi}")
        menubar = pencere.menuBar()
        menu = menubar.addMenu(str(baslik))
        self.qt_menuler[menu_adi] = menu
        self.degiskenler[menu_adi] = menu

    def qt_toolbar_olustur(self, satir):
        self.pyside6_kontrol()
        govde = satir[len('qt_toolbar '):].strip()
        parcalar = parse_qt_command(govde)
        toolbar_adi = parcalar[0]
        baslik = self.ifade_hesapla(parcalar[1])
        pencere_adi = parcalar[2]
        pencere = self.qt_pencereler.get(pencere_adi)
        if pencere is None:
            raise ValueError(f"Pencere bulunamadi: {pencere_adi}")
        toolbar = pencere.addToolBar(str(baslik))
        self.degiskenler[toolbar_adi] = toolbar

    def qt_statusbar_olustur(self, satir):
        self.pyside6_kontrol()
        govde = satir[len('qt_statusbar '):].strip()
        parcalar = parse_qt_command(govde)
        statusbar_adi = parcalar[0]
        pencere_adi = parcalar[1]
        pencere = self.qt_pencereler.get(pencere_adi)
        if pencere is None:
            raise ValueError(f"Pencere bulunamadi: {pencere_adi}")
        statusbar = pencere.statusBar()
        self.degiskenler[statusbar_adi] = statusbar

    def qt_timer_olustur(self, satir):
        self.pyside6_kontrol()
        govde = satir[len('qt_timer '):].strip()
        parcalar = parse_qt_command(govde)
        timer_adi = parcalar[0]
        interval = int(parcalar[1])
        fonksiyon_adi = parcalar[2] if len(parcalar) > 2 else None
        timer = QTimer()
        timer.setInterval(interval)
        if fonksiyon_adi and fonksiyon_adi in self.degiskenler:
            fonksiyon = self.degiskenler[fonksiyon_adi]
            if callable(fonksiyon):
                timer.timeout.connect(fonksiyon)
        self.qt_timerlar[timer_adi] = timer
        self.degiskenler[timer_adi] = timer

    def qt_mesaj_kutusu(self, satir):
        self.pyside6_kontrol()
        govde = satir[len('qt_mesaj_kutusu '):].strip()
        parcalar = parse_qt_command(govde)
        baslik = self.ifade_hesapla(parcalar[0])
        mesaj = self.ifade_hesapla(parcalar[1])
        tip = self.ifade_hesapla(parcalar[2]) if len(parcalar) > 2 else "bilgi"
        msg = QMessageBox()
        msg.setWindowTitle(str(baslik))
        msg.setText(str(mesaj))
        if tip == "bilgi":
            msg.setIcon(QMessageBox.Information)
        elif tip == "uyari":
            msg.setIcon(QMessageBox.Warning)
        elif tip == "hata":
            msg.setIcon(QMessageBox.Critical)
        elif tip == "soru":
            msg.setIcon(QMessageBox.Question)
        msg.exec()

    def qt_dosya_dialog(self, satir):
        self.pyside6_kontrol()
        govde = satir[len('qt_dosya_dialog '):].strip()
        parcalar = parse_qt_command(govde)
        degisken_adi = parcalar[0]
        mod = self.ifade_hesapla(parcalar[1]) if len(parcalar) > 1 else "ac"
        if mod == "ac":
            dosya, _ = QFileDialog.getOpenFileName()
        elif mod == "kaydet":
            dosya, _ = QFileDialog.getSaveFileName()
        elif mod == "klasor":
            dosya = QFileDialog.getExistingDirectory()
        else:
            dosya, _ = QFileDialog.getOpenFileName()
        self.degiskenler[degisken_adi] = dosya

    def qt_renk_dialog(self, satir):
        self.pyside6_kontrol()
        degisken_adi = satir[len('qt_renk_dialog '):].strip()
        renk = QColorDialog.getColor()
        if renk.isValid():
            self.degiskenler[degisken_adi] = renk

    def qt_pencere_goster(self, satir):
        self.pyside6_kontrol()
        pencere_adi = satir[len('qt_pencere_goster '):].strip()
        if pencere_adi not in self.qt_pencereler:
            raise ValueError(f"Pencere bulunamadi: {pencere_adi}")
        self.qt_pencereler[pencere_adi].show()

    def qt_calistir(self):
        self.pyside6_kontrol()
        if self.qapp is None:
            raise ValueError("Qt uygulamasi baslatilmamis.")
        sys.exit(self.qapp.exec())

    # ==================== PYGAME ====================

    def pygame_kontrol(self):
        if not PYGAME_AVAILABLE:
            raise ImportError("pygame kurulu degil. 'pip install pygame' ile kurabilirsiniz.")

    def oyun_baslat(self):
        self.pygame_kontrol()
        if pygame.get_init():
            print("Uyari: Pygame zaten baslatilmis.")
        else:
            pygame.init()
        try:
            pygame.mixer.init()
        except Exception as e:
            print(f"Uyari: Ses sistemi baslatılamadi: {e}. Ses ozellikleri devre disi.")
        if self.pg_saat is None:
            self.pg_saat = pygame.time.Clock()
        # Tuş sabitleri
        self.degiskenler['CIKIS'] = pygame.locals.QUIT
        self.degiskenler['KLAVYE_ASAGI'] = pygame.locals.KEYDOWN
        self.degiskenler['KLAVYE_YUKARI'] = pygame.locals.KEYUP
        self.degiskenler['FARE_ASAGI'] = pygame.locals.MOUSEBUTTONDOWN
        self.degiskenler['FARE_YUKARI'] = pygame.locals.MOUSEBUTTONUP
        self.degiskenler['FARE_HAREKET'] = pygame.locals.MOUSEMOTION
        self.degiskenler['K_ESC'] = pygame.locals.K_ESCAPE
        self.degiskenler['K_BOSLUK'] = pygame.locals.K_SPACE
        self.degiskenler['K_ENTER'] = pygame.locals.K_RETURN
        self.degiskenler['K_SOL'] = pygame.locals.K_LEFT
        self.degiskenler['K_SAG'] = pygame.locals.K_RIGHT
        self.degiskenler['K_YUKARI'] = pygame.locals.K_UP
        self.degiskenler['K_ASAGI'] = pygame.locals.K_DOWN
        for harf in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            self.degiskenler[f'K_{harf}'] = getattr(pygame.locals, f'K_{harf.lower()}')
        for rakam in range(10):
            self.degiskenler[f'K_{rakam}'] = getattr(pygame.locals, f'K_{rakam}')
        for fn in range(1, 6):
            self.degiskenler[f'K_F{fn}'] = getattr(pygame.locals, f'K_F{fn}')
        self.degiskenler['K_CTRL'] = pygame.locals.K_LCTRL
        self.degiskenler['K_SHIFT'] = pygame.locals.K_LSHIFT
        self.degiskenler['K_ALT'] = pygame.locals.K_LALT
        self.degiskenler['K_TAB'] = pygame.locals.K_TAB
        self.degiskenler['K_GERI'] = pygame.locals.K_BACKSPACE
        self.degiskenler['K_SIL'] = pygame.locals.K_DELETE
        # Renk sabitleri
        self.degiskenler['SIYAH'] = (0, 0, 0)
        self.degiskenler['BEYAZ'] = (255, 255, 255)
        self.degiskenler['KIRMIZI'] = (255, 0, 0)
        self.degiskenler['YESIL'] = (0, 255, 0)
        self.degiskenler['MAVI'] = (0, 0, 255)
        self.degiskenler['SARI'] = (255, 255, 0)
        self.degiskenler['TURUNCU'] = (255, 165, 0)
        self.degiskenler['MOR'] = (128, 0, 128)
        self.degiskenler['PEMBE'] = (255, 192, 203)
        self.degiskenler['GRI'] = (128, 128, 128)
        self.degiskenler['ACIK_GRI'] = (211, 211, 211)
        self.degiskenler['KOYU_GRI'] = (64, 64, 64)
        self.degiskenler['CAMGOBEGI'] = (0, 255, 255)
        self.degiskenler['LACIVERT'] = (0, 0, 128)
        self.degiskenler['KAHVERENGI'] = (139, 69, 19)

    def oyun_kapat(self):
        self.pygame_kontrol()
        try:
            if pygame.mixer.get_init():
                pygame.mixer.quit()
        except Exception:
            pass
        pygame.quit()
        self.pg_ekran = None
        self.pg_saat = None

    def oyun_ekran_olustur(self, satir):
        self.pygame_kontrol()
        govde = satir[len('oyun_ekran '):].strip()
        parcalar = parse_qt_command(govde)
        if len(parcalar) < 3:
            print("Hata: oyun_ekran <ad> <genislik> <yukseklik> [bayraklar] seklinde kullanin.")
            return
        ekran_adi = parcalar[0]
        try:
            genislik = int(self.ifade_hesapla(parcalar[1]))
            yukseklik = int(self.ifade_hesapla(parcalar[2]))
        except (ValueError, TypeError) as e:
            print(f"Hata: Gecersiz ekran boyutu: {e}")
            return
        if genislik <= 0 or yukseklik <= 0:
            print(f"Hata: Ekran boyutlari pozitif olmali. Alindi: {genislik}x{yukseklik}")
            return
        bayraklar = 0
        if len(parcalar) > 3:
            bayrak_str = self.ifade_hesapla(parcalar[3])
            if 'tam_ekran' in str(bayrak_str):
                bayraklar |= pygame.FULLSCREEN
            if 'yeniden_boyutlandir' in str(bayrak_str):
                bayraklar |= pygame.RESIZABLE
            if 'cercevesiz' in str(bayrak_str):
                bayraklar |= pygame.NOFRAME
        try:
            ekran = pygame.display.set_mode((genislik, yukseklik), bayraklar)
            self.pg_ekran = ekran
            self.pg_yuzeyleri[ekran_adi] = ekran
            self.degiskenler[ekran_adi] = ekran
        except Exception as e:
            print(f"Hata: Ekran olusturulamadi: {e}")

    def oyun_baslik_ayarla(self, satir):
        self.pygame_kontrol()
        baslik = self.ifade_hesapla(satir[len('oyun_baslik '):].strip())
        pygame.display.set_caption(str(baslik))

    def oyun_simge_ayarla(self, satir):
        self.pygame_kontrol()
        resim_adi = satir[len('oyun_simge '):].strip()
        if resim_adi in self.pg_resimler:
            pygame.display.set_icon(self.pg_resimler[resim_adi])

    def ekran_doldur(self, satir):
        self.pygame_kontrol()
        govde = satir[len('ekran_doldur '):].strip()
        parcalar = parse_qt_command(govde)
        ekran_adi = parcalar[0]
        renk = self.ifade_hesapla(parcalar[1])
        if ekran_adi in self.pg_yuzeyleri:
            self.pg_yuzeyleri[ekran_adi].fill(renk)

    def ekran_guncelle(self):
        self.pygame_kontrol()
        pygame.display.flip()

    def ekran_guncelle_bolge(self, satir):
        self.pygame_kontrol()
        govde = satir[len('ekran_guncelle_bolge '):].strip()
        parcalar = govde.split()
        x, y, g, y2 = int(parcalar[0]), int(parcalar[1]), int(parcalar[2]), int(parcalar[3])
        pygame.display.update((x, y, g, y2))

    def olaylari_isle_komutu(self):
        self.pygame_kontrol()
        olaylar = pygame.event.get()
        self.degiskenler['_son_olaylar'] = olaylar
        return olaylar

    def olay_kontrol(self, satir):
        self.pygame_kontrol()
        govde = satir[len('olay_kontrol '):].strip()
        parcalar = parse_qt_command(govde)
        degisken_adi = parcalar[0]
        olay_tipi = self.ifade_hesapla(parcalar[1]) if len(parcalar) > 1 else None
        olaylar = self.degiskenler.get('_son_olaylar', [])
        if olay_tipi is not None:
            self.degiskenler[degisken_adi] = [o for o in olaylar if o.type == olay_tipi]
        else:
            self.degiskenler[degisken_adi] = olaylar

    def _renk_coz(self, renk):
        if isinstance(renk, (tuple, list)):
            return tuple(renk)
        if isinstance(renk, str) and renk in self.degiskenler:
            return tuple(self.degiskenler[renk])
        return renk

    def ciz_cizgi(self, satir):
        self.pygame_kontrol()
        govde = satir[len('ciz_cizgi '):].strip()
        parcalar = parse_qt_command(govde)
        ekran_adi = parcalar[0]
        renk = self._renk_coz(self.ifade_hesapla(parcalar[1]))
        x1, y1 = int(self.ifade_hesapla(parcalar[2])), int(self.ifade_hesapla(parcalar[3]))
        x2, y2 = int(self.ifade_hesapla(parcalar[4])), int(self.ifade_hesapla(parcalar[5]))
        kalinlik = int(parcalar[6]) if len(parcalar) > 6 else 1
        if ekran_adi in self.pg_yuzeyleri:
            pygame.draw.line(self.pg_yuzeyleri[ekran_adi], renk, (x1, y1), (x2, y2), kalinlik)

    def ciz_dikdortgen(self, satir):
        self.pygame_kontrol()
        govde = satir[len('ciz_dikdortgen '):].strip()
        parcalar = parse_qt_command(govde)
        ekran_adi = parcalar[0]
        renk = self._renk_coz(self.ifade_hesapla(parcalar[1]))
        x, y = int(self.ifade_hesapla(parcalar[2])), int(self.ifade_hesapla(parcalar[3]))
        g, h = int(self.ifade_hesapla(parcalar[4])), int(self.ifade_hesapla(parcalar[5]))
        kalinlik = int(parcalar[6]) if len(parcalar) > 6 else 1
        if ekran_adi in self.pg_yuzeyleri:
            pygame.draw.rect(self.pg_yuzeyleri[ekran_adi], renk, (x, y, g, h), kalinlik)

    def ciz_dolu_dikdortgen(self, satir):
        self.pygame_kontrol()
        govde = satir[len('ciz_dolu_dikdortgen '):].strip()
        parcalar = parse_qt_command(govde)
        ekran_adi = parcalar[0]
        renk = self._renk_coz(self.ifade_hesapla(parcalar[1]))
        x, y = int(self.ifade_hesapla(parcalar[2])), int(self.ifade_hesapla(parcalar[3]))
        g, h = int(self.ifade_hesapla(parcalar[4])), int(self.ifade_hesapla(parcalar[5]))
        if ekran_adi in self.pg_yuzeyleri:
            pygame.draw.rect(self.pg_yuzeyleri[ekran_adi], renk, (x, y, g, h), 0)

    def ciz_cember(self, satir):
        self.pygame_kontrol()
        govde = satir[len('ciz_cember '):].strip()
        parcalar = parse_qt_command(govde)
        ekran_adi = parcalar[0]
        renk = self._renk_coz(self.ifade_hesapla(parcalar[1]))
        x, y = int(self.ifade_hesapla(parcalar[2])), int(self.ifade_hesapla(parcalar[3]))
        yaricap = int(self.ifade_hesapla(parcalar[4]))
        kalinlik = int(parcalar[5]) if len(parcalar) > 5 else 1
        if ekran_adi in self.pg_yuzeyleri:
            pygame.draw.circle(self.pg_yuzeyleri[ekran_adi], renk, (x, y), yaricap, kalinlik)

    def ciz_dolu_cember(self, satir):
        self.pygame_kontrol()
        govde = satir[len('ciz_dolu_cember '):].strip()
        parcalar = parse_qt_command(govde)
        ekran_adi = parcalar[0]
        renk = self._renk_coz(self.ifade_hesapla(parcalar[1]))
        x, y = int(self.ifade_hesapla(parcalar[2])), int(self.ifade_hesapla(parcalar[3]))
        yaricap = int(self.ifade_hesapla(parcalar[4]))
        if ekran_adi in self.pg_yuzeyleri:
            pygame.draw.circle(self.pg_yuzeyleri[ekran_adi], renk, (x, y), yaricap, 0)

    def ciz_elips(self, satir):
        self.pygame_kontrol()
        govde = satir[len('ciz_elips '):].strip()
        parcalar = parse_qt_command(govde)
        ekran_adi = parcalar[0]
        renk = self._renk_coz(self.ifade_hesapla(parcalar[1]))
        x, y = int(self.ifade_hesapla(parcalar[2])), int(self.ifade_hesapla(parcalar[3]))
        g = int(self.ifade_hesapla(parcalar[4]))
        # 5. parametre (yükseklik) birden fazla token olabilir: örn. "yboyut_su * 2"
        # parse_qt_command bunu ['yboyut_su', '*', '2'] diye ayırabilir.
        # Son parametre kalınlık (varsa, tek rakamlı sayı). Onu tespit edip ortadakileri birleştir.
        # Kural: parcalar[5:] içinde son eleman sadece sayıysa kalınlık, geri kalanı h ifadesi.
        h_parcalar = parcalar[5:]
        kalinlik = 0
        if h_parcalar:
            # Son eleman saf sayı mı?
            try:
                son = int(h_parcalar[-1])
                if len(h_parcalar) > 1:
                    kalinlik = son
                    h_ifade = ' '.join(h_parcalar[:-1])
                else:
                    # Tek eleman: ya h ya kalinlik belirsiz. h olarak al, kalinlik=0.
                    h_ifade = h_parcalar[0]
                    kalinlik = 0
            except ValueError:
                h_ifade = ' '.join(h_parcalar)
                kalinlik = 0
            h = int(self.ifade_hesapla(h_ifade))
        else:
            h = g
        if ekran_adi in self.pg_yuzeyleri:
            pygame.draw.ellipse(self.pg_yuzeyleri[ekran_adi], renk, (x, y, g, h), kalinlik)

    def ciz_cokgen(self, satir):
        self.pygame_kontrol()
        govde = satir[len('ciz_cokgen '):].strip()
        parcalar = parse_qt_command(govde)
        ekran_adi = parcalar[0]
        renk = self._renk_coz(self.ifade_hesapla(parcalar[1]))
        noktalar = self.ifade_hesapla(parcalar[2])
        kalinlik = int(parcalar[3]) if len(parcalar) > 3 else 0
        if ekran_adi in self.pg_yuzeyleri:
            pygame.draw.polygon(self.pg_yuzeyleri[ekran_adi], renk, noktalar, kalinlik)

    def ciz_nokta(self, satir):
        self.pygame_kontrol()
        govde = satir[len('ciz_nokta '):].strip()
        parcalar = parse_qt_command(govde)
        ekran_adi = parcalar[0]
        renk = self._renk_coz(self.ifade_hesapla(parcalar[1]))
        x, y = int(self.ifade_hesapla(parcalar[2])), int(self.ifade_hesapla(parcalar[3]))
        if ekran_adi in self.pg_yuzeyleri:
            self.pg_yuzeyleri[ekran_adi].set_at((x, y), renk)

    def ciz_yay(self, satir):
        self.pygame_kontrol()
        govde = satir[len('ciz_yay '):].strip()
        parcalar = parse_qt_command(govde)
        ekran_adi = parcalar[0]
        renk = self._renk_coz(self.ifade_hesapla(parcalar[1]))
        x, y = int(self.ifade_hesapla(parcalar[2])), int(self.ifade_hesapla(parcalar[3]))
        g, h = int(self.ifade_hesapla(parcalar[4])), int(self.ifade_hesapla(parcalar[5]))
        baslangic_aci = int(self.ifade_hesapla(parcalar[6]))
        bitis_aci = int(self.ifade_hesapla(parcalar[7]))
        kalinlik = int(parcalar[8]) if len(parcalar) > 8 else 1
        if ekran_adi in self.pg_yuzeyleri:
            pygame.draw.arc(self.pg_yuzeyleri[ekran_adi], renk, (x, y, g, h),
                           math.radians(baslangic_aci), math.radians(bitis_aci), kalinlik)

    def resim_yukle(self, satir):
        self.pygame_kontrol()
        govde = satir[len('resim_yukle '):].strip()
        parcalar = parse_qt_command(govde)
        if len(parcalar) < 2:
            print("Hata: resim_yukle <ad> <dosya_yolu> seklinde kullanin.")
            return
        resim_adi = parcalar[0]
        dosya_yolu = str(self.ifade_hesapla(parcalar[1]))
        if not os.path.exists(dosya_yolu):
            print(f"Hata: Resim dosyasi bulunamadi: '{dosya_yolu}'")
            self.degiskenler[resim_adi] = None
            return
        try:
            resim = pygame.image.load(dosya_yolu).convert_alpha()
            self.pg_resimler[resim_adi] = resim
            self.pg_yuzeyleri[resim_adi] = resim
            self.degiskenler[resim_adi] = resim
        except pygame.error as e:
            print(f"Resim yukleme hatasi ('{dosya_yolu}'): {e}")
            self.degiskenler[resim_adi] = None
        except Exception as e:
            print(f"Beklenmeyen resim hatasi ('{dosya_yolu}'): {e}")
            self.degiskenler[resim_adi] = None

    def resim_ciz(self, satir):
        self.pygame_kontrol()
        govde = satir[len('resim_ciz '):].strip()
        parcalar = parse_qt_command(govde)
        ekran_adi = parcalar[0]
        resim_adi = parcalar[1]
        x, y = int(self.ifade_hesapla(parcalar[2])), int(self.ifade_hesapla(parcalar[3]))
        if ekran_adi in self.pg_yuzeyleri and resim_adi in self.pg_resimler:
            self.pg_yuzeyleri[ekran_adi].blit(self.pg_resimler[resim_adi], (x, y))

    def resim_olcekle(self, satir):
        self.pygame_kontrol()
        govde = satir[len('resim_olcekle '):].strip()
        parcalar = parse_qt_command(govde)
        kaynak_adi = parcalar[0]
        hedef_adi = parcalar[1]
        genislik = int(self.ifade_hesapla(parcalar[2]))
        yukseklik = int(self.ifade_hesapla(parcalar[3]))
        if kaynak_adi in self.pg_resimler:
            olcekli = pygame.transform.scale(self.pg_resimler[kaynak_adi], (genislik, yukseklik))
            self.pg_resimler[hedef_adi] = olcekli
            self.pg_yuzeyleri[hedef_adi] = olcekli
            self.degiskenler[hedef_adi] = olcekli

    def resim_dondur(self, satir):
        self.pygame_kontrol()
        govde = satir[len('resim_dondur '):].strip()
        parcalar = parse_qt_command(govde)
        kaynak_adi = parcalar[0]
        hedef_adi = parcalar[1]
        aci = float(self.ifade_hesapla(parcalar[2]))
        if kaynak_adi in self.pg_resimler:
            donuk = pygame.transform.rotate(self.pg_resimler[kaynak_adi], aci)
            self.pg_resimler[hedef_adi] = donuk
            self.pg_yuzeyleri[hedef_adi] = donuk
            self.degiskenler[hedef_adi] = donuk

    def resim_cevir(self, satir):
        self.pygame_kontrol()
        govde = satir[len('resim_cevir '):].strip()
        parcalar = parse_qt_command(govde)
        kaynak_adi = parcalar[0]
        hedef_adi = parcalar[1]
        yatay = bool(self.ifade_hesapla(parcalar[2])) if len(parcalar) > 2 else True
        dikey = bool(self.ifade_hesapla(parcalar[3])) if len(parcalar) > 3 else False
        if kaynak_adi in self.pg_resimler:
            cevirilmis = pygame.transform.flip(self.pg_resimler[kaynak_adi], yatay, dikey)
            self.pg_resimler[hedef_adi] = cevirilmis
            self.pg_yuzeyleri[hedef_adi] = cevirilmis
            self.degiskenler[hedef_adi] = cevirilmis

    def resim_kaydet(self, satir):
        self.pygame_kontrol()
        govde = satir[len('resim_kaydet '):].strip()
        parcalar = parse_qt_command(govde)
        yuzey_adi = parcalar[0]
        dosya_yolu = self.ifade_hesapla(parcalar[1])
        if yuzey_adi in self.pg_yuzeyleri:
            pygame.image.save(self.pg_yuzeyleri[yuzey_adi], str(dosya_yolu))

    def yuzeyi_yukle(self, satir):
        self.pygame_kontrol()
        govde = satir[len('yuzeyi_yukle '):].strip()
        parcalar = parse_qt_command(govde)
        yuzey_adi = parcalar[0]
        dosya_yolu = self.ifade_hesapla(parcalar[1])
        try:
            yuzey = pygame.image.load(str(dosya_yolu)).convert_alpha()
            self.pg_yuzeyleri[yuzey_adi] = yuzey
            self.pg_resimler[yuzey_adi] = yuzey
            self.degiskenler[yuzey_adi] = yuzey
        except Exception as e:
            print(f"Yuzey yukleme hatasi: {e}")

    def yuzey_olustur(self, satir):
        self.pygame_kontrol()
        govde = satir[len('yuzey_olustur '):].strip()
        parcalar = govde.split()
        yuzey_adi = parcalar[0]
        genislik = int(parcalar[1])
        yukseklik = int(parcalar[2])
        alfa = len(parcalar) > 3 and parcalar[3] == 'alfa'
        if alfa:
            yuzey = pygame.Surface((genislik, yukseklik), pygame.SRCALPHA)
        else:
            yuzey = pygame.Surface((genislik, yukseklik))
        self.pg_yuzeyleri[yuzey_adi] = yuzey
        self.degiskenler[yuzey_adi] = yuzey

    def yuzey_doldur(self, satir):
        self.pygame_kontrol()
        govde = satir[len('yuzey_doldur '):].strip()
        parcalar = parse_qt_command(govde)
        yuzey_adi = parcalar[0]
        renk = self._renk_coz(self.ifade_hesapla(parcalar[1]))
        if yuzey_adi in self.pg_yuzeyleri:
            self.pg_yuzeyleri[yuzey_adi].fill(renk)

    def yuzey_kopyala(self, satir):
        self.pygame_kontrol()
        govde = satir[len('yuzey_kopyala '):].strip()
        parcalar = parse_qt_command(govde)
        hedef_adi = parcalar[0]
        kaynak_adi = parcalar[1]
        x = int(self.ifade_hesapla(parcalar[2])) if len(parcalar) > 2 else 0
        y = int(self.ifade_hesapla(parcalar[3])) if len(parcalar) > 3 else 0
        if hedef_adi in self.pg_yuzeyleri and kaynak_adi in self.pg_yuzeyleri:
            self.pg_yuzeyleri[hedef_adi].blit(self.pg_yuzeyleri[kaynak_adi], (x, y))

    def yuzey_effekti(self, satir):
        self.pygame_kontrol()
        govde = satir[len('yuzey_effekti '):].strip()
        parcalar = parse_qt_command(govde)
        yuzey_adi = parcalar[0]
        efekt = parcalar[1]
        if yuzey_adi not in self.pg_yuzeyleri:
            return
        yuzey = self.pg_yuzeyleri[yuzey_adi]
        if efekt == 'donustur_alfa':
            yuzey = yuzey.convert_alpha()
        elif efekt == 'donustur':
            yuzey = yuzey.convert()
        self.pg_yuzeyleri[yuzey_adi] = yuzey
        self.degiskenler[yuzey_adi] = yuzey

    def ses_yukle(self, satir):
        self.pygame_kontrol()
        govde = satir[len('ses_yukle '):].strip()
        parcalar = parse_qt_command(govde)
        if len(parcalar) < 2:
            print("Hata: ses_yukle <ad> <dosya_yolu> seklinde kullanin.")
            return
        ses_adi = parcalar[0]
        dosya_yolu = str(self.ifade_hesapla(parcalar[1]))
        if not pygame.mixer.get_init():
            print("Uyari: Ses sistemi baslatilmamis. Ses yukleme atlaniyor.")
            self.degiskenler[ses_adi] = None
            return
        if not os.path.exists(dosya_yolu):
            print(f"Hata: Ses dosyasi bulunamadi: '{dosya_yolu}'")
            self.degiskenler[ses_adi] = None
            return
        try:
            ses = pygame.mixer.Sound(dosya_yolu)
            self.pg_sesler[ses_adi] = ses
            self.degiskenler[ses_adi] = ses
        except Exception as e:
            print(f"Ses yukleme hatasi ('{dosya_yolu}'): {e}")
            self.degiskenler[ses_adi] = None

    def ses_oynat(self, satir):
        self.pygame_kontrol()
        govde = satir[len('ses_oynat '):].strip()
        parcalar = govde.split()
        ses_adi = parcalar[0]
        tekrar = int(parcalar[1]) if len(parcalar) > 1 else 0
        if ses_adi in self.pg_sesler:
            kanal = self.pg_sesler[ses_adi].play(loops=tekrar)
            self.degiskenler[f"{ses_adi}_kanal"] = kanal

    def ses_durdur(self, satir):
        self.pygame_kontrol()
        ses_adi = satir[len('ses_durdur '):].strip()
        if ses_adi in self.pg_sesler:
            self.pg_sesler[ses_adi].stop()

    def ses_devam(self, satir):
        self.pygame_kontrol()
        pygame.mixer.unpause()

    def ses_ses_duzeyi(self, satir):
        self.pygame_kontrol()
        govde = satir[len('ses_ses_duzeyi '):].strip()
        parcalar = govde.split()
        if len(parcalar) < 2:
            print("Hata: ses_ses_duzeyi <ses_adi> <duzey 0.0-1.0> seklinde kullanin.")
            return
        ses_adi = parcalar[0]
        try:
            duzey = float(parcalar[1])
        except ValueError:
            print(f"Hata: Gecersiz ses duzeyi: '{parcalar[1]}'")
            return
        duzey = max(0.0, min(1.0, duzey))  # 0.0 - 1.0 araligina kilitle
        if ses_adi in self.pg_sesler and self.pg_sesler[ses_adi] is not None:
            self.pg_sesler[ses_adi].set_volume(duzey)

    def muzik_yukle(self, satir):
        self.pygame_kontrol()
        dosya_yolu = self.ifade_hesapla(satir[len('muzik_yukle '):].strip())
        try:
            pygame.mixer.music.load(str(dosya_yolu))
        except Exception as e:
            print(f"Muzik yukleme hatasi: {e}")

    def muzik_oynat(self):
        self.pygame_kontrol()
        pygame.mixer.music.play()

    def muzik_durdur(self):
        self.pygame_kontrol()
        pygame.mixer.music.pause()

    def muzik_devam_et(self):
        self.pygame_kontrol()
        pygame.mixer.music.unpause()

    def muzik_dur(self):
        self.pygame_kontrol()
        pygame.mixer.music.stop()

    def muzik_ses_duzeyi(self, satir):
        self.pygame_kontrol()
        duzey = float(self.ifade_hesapla(satir[len('muzik_ses_duzeyi '):].strip()))
        pygame.mixer.music.set_volume(duzey)

    def muzik_tekrar(self, satir):
        self.pygame_kontrol()
        tekrar = int(self.ifade_hesapla(satir[len('muzik_tekrar '):].strip()))
        pygame.mixer.music.play(loops=tekrar)

    def yazi_tipi_yukle(self, satir):
        self.pygame_kontrol()
        govde = satir[len('yazi_tipi_yukle '):].strip()
        parcalar = parse_qt_command(govde)
        font_adi = parcalar[0]
        dosya_yolu_veya_ad = self.ifade_hesapla(parcalar[1])
        boyut = int(parcalar[2]) if len(parcalar) > 2 else 24
        try:
            s = str(dosya_yolu_veya_ad)
            if s.endswith('.ttf') or s.endswith('.otf'):
                font = pygame.font.Font(s, boyut)
            else:
                font = pygame.font.SysFont(s, boyut)
            self.pg_fontlar[font_adi] = font
            self.degiskenler[font_adi] = font
        except Exception as e:
            print(f"Yazi tipi yukleme hatasi: {e}")
            font = pygame.font.Font(None, boyut)
            self.pg_fontlar[font_adi] = font
            self.degiskenler[font_adi] = font

    def metin_yaz(self, satir):
        self.pygame_kontrol()
        govde = satir[len('metin_yaz '):].strip()
        parcalar = parse_qt_command(govde)
        ekran_adi = parcalar[0]
        metin = str(self.ifade_hesapla(parcalar[1]))
        renk = self._renk_coz(self.ifade_hesapla(parcalar[2]))
        x, y = int(self.ifade_hesapla(parcalar[3])), int(self.ifade_hesapla(parcalar[4]))
        font_adi = parcalar[5] if len(parcalar) > 5 else None
        if ekran_adi not in self.pg_yuzeyleri:
            return
        font = self.pg_fontlar.get(font_adi) if font_adi else None
        if font is None:
            font = pygame.font.Font(None, 24)
        yuzey_metin = font.render(metin, True, renk)
        # x koordinatı merkez olarak kullan (ortalanmış çizim)
        metin_genislik = yuzey_metin.get_width()
        blit_x = x - metin_genislik // 2
        self.pg_yuzeyleri[ekran_adi].blit(yuzey_metin, (blit_x, y))
        self.degiskenler['_metin_boyut'] = yuzey_metin.get_size()

    def tuslar_oku(self, satir):
        self.pygame_kontrol()
        degisken_adi = satir[len('tuslar_oku '):].strip()
        self.degiskenler[degisken_adi] = pygame.key.get_pressed()

    def tus_basili_mi(self, satir):
        self.pygame_kontrol()
        govde = satir[len('tus_basili_mi '):].strip()
        parcalar = govde.split()
        degisken_adi = parcalar[0]
        tus_kodu = int(self.ifade_hesapla(parcalar[1]))
        tuslar = pygame.key.get_pressed()
        self.degiskenler[degisken_adi] = bool(tuslar[tus_kodu])

    def fare_konum_al(self, satir):
        self.pygame_kontrol()
        degisken_adi = satir[len('fare_konum '):].strip()
        konum = pygame.mouse.get_pos()
        self.degiskenler[degisken_adi] = list(konum)
        self.degiskenler[f"{degisken_adi}_x"] = konum[0]
        self.degiskenler[f"{degisken_adi}_y"] = konum[1]

    def fare_dugme_al(self, satir):
        self.pygame_kontrol()
        degisken_adi = satir[len('fare_dugme '):].strip()
        dugmeler = pygame.mouse.get_pressed()
        self.degiskenler[degisken_adi] = list(dugmeler)
        self.degiskenler[f"{degisken_adi}_sol"] = dugmeler[0]
        self.degiskenler[f"{degisken_adi}_orta"] = dugmeler[1]
        self.degiskenler[f"{degisken_adi}_sag"] = dugmeler[2]

    def fare_goster(self, satir):
        self.pygame_kontrol()
        pygame.mouse.set_visible(True)

    def fare_gizle(self):
        self.pygame_kontrol()
        pygame.mouse.set_visible(False)

    def saat_olustur(self, satir):
        self.pygame_kontrol()
        saat_adi = satir[len('saat_olustur '):].strip()
        self.degiskenler[saat_adi] = pygame.time.Clock()

    def saat_tikla(self, satir):
        self.pygame_kontrol()
        govde = satir[len('saat_tikla '):].strip()
        parcalar = govde.split()
        saat_adi = parcalar[0]
        fps = int(parcalar[1]) if len(parcalar) > 1 else 60
        if saat_adi in self.degiskenler:
            self.degiskenler[saat_adi].tick(fps)

    def fps_al(self, satir):
        self.pygame_kontrol()
        govde = satir[len('fps_al '):].strip()
        parcalar = govde.split()
        degisken_adi = parcalar[0]
        saat_adi = parcalar[1] if len(parcalar) > 1 else None
        if saat_adi and saat_adi in self.degiskenler:
            self.degiskenler[degisken_adi] = self.degiskenler[saat_adi].get_fps()
        elif self.pg_saat:
            self.degiskenler[degisken_adi] = self.pg_saat.get_fps()

    def renk_olustur(self, satir):
        self.pygame_kontrol()
        govde = satir[len('renk_olustur '):].strip()
        parcalar = parse_qt_command(govde)
        renk_adi = parcalar[0]
        r, g, b = int(self.ifade_hesapla(parcalar[1])), int(self.ifade_hesapla(parcalar[2])), int(self.ifade_hesapla(parcalar[3]))
        a = int(self.ifade_hesapla(parcalar[4])) if len(parcalar) > 4 else 255
        self.degiskenler[renk_adi] = (r, g, b, a)

    def renk_karistir(self, satir):
        self.pygame_kontrol()
        govde = satir[len('renk_karistir '):].strip()
        parcalar = parse_qt_command(govde)
        sonuc_adi = parcalar[0]
        renk1 = self._renk_coz(self.ifade_hesapla(parcalar[1]))
        renk2 = self._renk_coz(self.ifade_hesapla(parcalar[2]))
        oran = float(parcalar[3]) if len(parcalar) > 3 else 0.5
        self.degiskenler[sonuc_adi] = tuple(int(renk1[i] * (1 - oran) + renk2[i] * oran) for i in range(3))

    def carpisma_kontrol(self, satir):
        self.pygame_kontrol()
        govde = satir[len('carpisma_kontrol '):].strip()
        parcalar = parse_qt_command(govde)
        sonuc_adi = parcalar[0]
        s1 = self.degiskenler.get(parcalar[1])
        s2 = self.degiskenler.get(parcalar[2])
        if s1 and s2 and hasattr(s1, 'rect') and hasattr(s2, 'rect'):
            self.degiskenler[sonuc_adi] = s1.rect.colliderect(s2.rect)
        else:
            self.degiskenler[sonuc_adi] = False

    def carpisma_dikdortgen(self, satir):
        self.pygame_kontrol()
        govde = satir[len('carpisma_dikdortgen '):].strip()
        parcalar = parse_qt_command(govde)
        sonuc_adi = parcalar[0]
        # Desteklenen kullanim:
        # carpisma_dikdortgen sonuc x1 y1 g1 h1 x2 y2 g2 h2  (9 arg)
        # carpisma_dikdortgen sonuc x 0 y 0 g h x2 y2 g2 h2  (11 arg - degisken + offset)
        degerler = [int(self.ifade_hesapla(p)) for p in parcalar[1:]]
        if len(degerler) >= 10:
            # 10 deger: x1 offset_x1 y1 offset_y1 g1 h1 x2 y2 g2 h2 gibi
            # Kullanici "x 0 y 0 40 40 50 50 200 100" -> x+0, y+0, 40, 40
            x1 = degerler[0] + degerler[1]
            y1 = degerler[2] + degerler[3]
            g1, h1 = degerler[4], degerler[5]
            x2, y2, g2, h2 = degerler[6], degerler[7], degerler[8], degerler[9]
        elif len(degerler) >= 8:
            x1, y1, g1, h1 = degerler[0], degerler[1], degerler[2], degerler[3]
            x2, y2, g2, h2 = degerler[4], degerler[5], degerler[6], degerler[7]
        else:
            self.degiskenler[sonuc_adi] = False
            return
        self.degiskenler[sonuc_adi] = pygame.Rect(x1, y1, g1, h1).colliderect(pygame.Rect(x2, y2, g2, h2))

    def sprite_grubu_olustur(self, satir):
        self.pygame_kontrol()
        grup_adi = satir[len('sprite_grubu_olustur '):].strip()
        grup = pygame.sprite.Group()
        self.pg_sprite_gruplari[grup_adi] = grup
        self.degiskenler[grup_adi] = grup

    def sprite_ekle(self, satir):
        self.pygame_kontrol()
        govde = satir[len('sprite_ekle '):].strip()
        parcalar = govde.split()
        grup_adi = parcalar[0]
        sprite_adi = parcalar[1]
        if grup_adi in self.pg_sprite_gruplari and sprite_adi in self.degiskenler:
            self.pg_sprite_gruplari[grup_adi].add(self.degiskenler[sprite_adi])

    def sprite_ciz(self, satir):
        self.pygame_kontrol()
        govde = satir[len('sprite_ciz '):].strip()
        parcalar = govde.split()
        grup_adi = parcalar[0]
        ekran_adi = parcalar[1]
        if grup_adi in self.pg_sprite_gruplari and ekran_adi in self.pg_yuzeyleri:
            self.pg_sprite_gruplari[grup_adi].draw(self.pg_yuzeyleri[ekran_adi])

    def sprite_guncelle(self, satir):
        self.pygame_kontrol()
        grup_adi = satir[len('sprite_guncelle '):].strip()
        if grup_adi in self.pg_sprite_gruplari:
            self.pg_sprite_gruplari[grup_adi].update()

    def piksel_al(self, satir):
        self.pygame_kontrol()
        govde = satir[len('piksel_al '):].strip()
        parcalar = govde.split()
        degisken_adi = parcalar[0]
        yuzey_adi = parcalar[1]
        x, y = int(self.ifade_hesapla(parcalar[2])), int(self.ifade_hesapla(parcalar[3]))
        if yuzey_adi in self.pg_yuzeyleri:
            self.degiskenler[degisken_adi] = list(self.pg_yuzeyleri[yuzey_adi].get_at((x, y)))

    def piksel_yaz(self, satir):
        self.pygame_kontrol()
        govde = satir[len('piksel_yaz '):].strip()
        parcalar = parse_qt_command(govde)
        yuzey_adi = parcalar[0]
        x, y = int(self.ifade_hesapla(parcalar[1])), int(self.ifade_hesapla(parcalar[2]))
        renk = self._renk_coz(self.ifade_hesapla(parcalar[3]))
        if yuzey_adi in self.pg_yuzeyleri:
            self.pg_yuzeyleri[yuzey_adi].set_at((x, y), renk)

    def maske_olustur(self, satir):
        self.pygame_kontrol()
        govde = satir[len('maske_olustur '):].strip()
        parcalar = govde.split()
        maske_adi = parcalar[0]
        yuzey_adi = parcalar[1]
        if yuzey_adi in self.pg_yuzeyleri:
            self.degiskenler[maske_adi] = pygame.mask.from_surface(self.pg_yuzeyleri[yuzey_adi])

    def oyun_bekle(self, satir):
        self.pygame_kontrol()
        sure = int(self.ifade_hesapla(satir[len('oyun_bekle '):].strip()))
        pygame.time.wait(sure)

    def ekran_bilgi_al(self, satir):
        self.pygame_kontrol()
        degisken_adi = satir[len('ekran_bilgi '):].strip()
        bilgi = pygame.display.Info()
        self.degiskenler[degisken_adi] = bilgi
        self.degiskenler[f"{degisken_adi}_genislik"] = bilgi.current_w
        self.degiskenler[f"{degisken_adi}_yukseklik"] = bilgi.current_h

    def pencere_konumu_ayarla(self, satir):
        self.pygame_kontrol()
        govde = satir[len('pencere_konumu '):].strip()
        parcalar = govde.split()
        x, y = int(parcalar[0]), int(parcalar[1])
        os.environ['SDL_VIDEO_WINDOW_POS'] = f"{x},{y}"

    def tam_ekran_ayarla(self, satir):
        self.pygame_kontrol()
        durum = self.ifade_hesapla(satir[len('tam_ekran '):].strip())
        if self.pg_ekran:
            if durum:
                self.pg_ekran = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            else:
                bilgi = pygame.display.Info()
                self.pg_ekran = pygame.display.set_mode((bilgi.current_w, bilgi.current_h))

    # ==================== NETWORK ====================

    def ag_kontrol(self):
        if not REQUESTS_AVAILABLE:
            raise ImportError("requests kurulu degil. Yuklemek icin: pip install requests")
        if self.ag_modu and self.requests_session is None:
            self.requests_session = requests.Session()
            self.requests_session.headers.update({'User-Agent': 'TSharp/4.1'})

    def http_get(self, satir):
        self.ag_kontrol()
        govde = satir[len('http_get '):].strip()
        parcalar = parse_qt_command(govde)
        if len(parcalar) < 2:
            print("Hata: http_get <degisken> <url> seklinde kullanin.")
            return
        degisken_adi = parcalar[0]
        url = str(self.ifade_hesapla(parcalar[1]))
        timeout = self.degiskenler.get('ag_timeout', 30)
        try:
            response = self.requests_session.get(url, timeout=timeout)
            self.degiskenler[degisken_adi] = response
            self.degiskenler[f"{degisken_adi}_metin"] = response.text
            self.degiskenler[f"{degisken_adi}_kod"] = response.status_code
        except requests.exceptions.ConnectionError:
            print(f"Hata: Baglanti kurulamadi: '{url}'")
            self.degiskenler[degisken_adi] = None
        except requests.exceptions.Timeout:
            print(f"Hata: Baglanti zaman asimi ({timeout}s): '{url}'")
            self.degiskenler[degisken_adi] = None
        except requests.exceptions.MissingSchema:
            print(f"Hata: Gecersiz URL (http:// veya https:// ile baslamali): '{url}'")
            self.degiskenler[degisken_adi] = None
        except Exception as e:
            print(f"GET istegi hatasi: {e}")
            self.degiskenler[degisken_adi] = None

    def http_post(self, satir):
        self.ag_kontrol()
        govde = satir[len('http_post '):].strip()
        parcalar = parse_qt_command(govde)
        if len(parcalar) < 2:
            print("Hata: http_post <degisken> <url> [veri] seklinde kullanin.")
            return
        degisken_adi = parcalar[0]
        url = str(self.ifade_hesapla(parcalar[1]))
        veri = self.ifade_hesapla(parcalar[2]) if len(parcalar) > 2 else {}
        timeout = self.degiskenler.get('ag_timeout', 30)
        try:
            response = self.requests_session.post(url, data=veri, timeout=timeout)
            self.degiskenler[degisken_adi] = response
            self.degiskenler[f"{degisken_adi}_metin"] = response.text
            self.degiskenler[f"{degisken_adi}_kod"] = response.status_code
        except requests.exceptions.ConnectionError:
            print(f"Hata: Baglanti kurulamadi: '{url}'")
            self.degiskenler[degisken_adi] = None
        except requests.exceptions.Timeout:
            print(f"Hata: Baglanti zaman asimi ({timeout}s): '{url}'")
            self.degiskenler[degisken_adi] = None
        except Exception as e:
            print(f"POST istegi hatasi: {e}")
            self.degiskenler[degisken_adi] = None

    def http_put(self, satir):
        self.ag_kontrol()
        govde = satir[len('http_put '):].strip()
        parcalar = parse_qt_command(govde)
        if len(parcalar) < 2:
            print("Hata: http_put <degisken> <url> [veri] seklinde kullanin.")
            return
        degisken_adi = parcalar[0]
        url = str(self.ifade_hesapla(parcalar[1]))
        veri = self.ifade_hesapla(parcalar[2]) if len(parcalar) > 2 else {}
        timeout = self.degiskenler.get('ag_timeout', 30)
        try:
            response = self.requests_session.put(url, data=veri, timeout=timeout)
            self.degiskenler[degisken_adi] = response
            self.degiskenler[f"{degisken_adi}_metin"] = response.text
            self.degiskenler[f"{degisken_adi}_kod"] = response.status_code
        except requests.exceptions.ConnectionError:
            print(f"Hata: Baglanti kurulamadi: '{url}'")
            self.degiskenler[degisken_adi] = None
        except requests.exceptions.Timeout:
            print(f"Hata: Baglanti zaman asimi ({timeout}s): '{url}'")
            self.degiskenler[degisken_adi] = None
        except Exception as e:
            print(f"PUT istegi hatasi: {e}")
            self.degiskenler[degisken_adi] = None

    def http_delete(self, satir):
        self.ag_kontrol()
        govde = satir[len('http_delete '):].strip()
        parcalar = parse_qt_command(govde)
        if len(parcalar) < 2:
            print("Hata: http_delete <degisken> <url> seklinde kullanin.")
            return
        degisken_adi = parcalar[0]
        url = str(self.ifade_hesapla(parcalar[1]))
        timeout = self.degiskenler.get('ag_timeout', 30)
        try:
            response = self.requests_session.delete(url, timeout=timeout)
            self.degiskenler[degisken_adi] = response
            self.degiskenler[f"{degisken_adi}_kod"] = response.status_code
        except requests.exceptions.ConnectionError:
            print(f"Hata: Baglanti kurulamadi: '{url}'")
            self.degiskenler[degisken_adi] = None
        except requests.exceptions.Timeout:
            print(f"Hata: Baglanti zaman asimi ({timeout}s): '{url}'")
            self.degiskenler[degisken_adi] = None
        except Exception as e:
            print(f"DELETE istegi hatasi: {e}")
            self.degiskenler[degisken_adi] = None

    def http_head(self, satir):
        self.ag_kontrol()
        govde = satir[len('http_head '):].strip()
        parcalar = parse_qt_command(govde)
        if len(parcalar) < 2:
            print("Hata: http_head <degisken> <url> seklinde kullanin.")
            return
        degisken_adi = parcalar[0]
        url = str(self.ifade_hesapla(parcalar[1]))
        timeout = self.degiskenler.get('ag_timeout', 30)
        try:
            response = self.requests_session.head(url, timeout=timeout)
            self.degiskenler[degisken_adi] = response
            self.degiskenler[f"{degisken_adi}_kod"] = response.status_code
        except requests.exceptions.ConnectionError:
            print(f"Hata: Baglanti kurulamadi: '{url}'")
            self.degiskenler[degisken_adi] = None
        except requests.exceptions.Timeout:
            print(f"Hata: Baglanti zaman asimi ({timeout}s): '{url}'")
            self.degiskenler[degisken_adi] = None
        except Exception as e:
            print(f"HEAD istegi hatasi: {e}")
            self.degiskenler[degisken_adi] = None

    def http_patch(self, satir):
        self.ag_kontrol()
        govde = satir[len('http_patch '):].strip()
        parcalar = parse_qt_command(govde)
        if len(parcalar) < 2:
            print("Hata: http_patch <degisken> <url> [veri] seklinde kullanin.")
            return
        degisken_adi = parcalar[0]
        url = str(self.ifade_hesapla(parcalar[1]))
        veri = self.ifade_hesapla(parcalar[2]) if len(parcalar) > 2 else {}
        timeout = self.degiskenler.get('ag_timeout', 30)
        try:
            response = self.requests_session.patch(url, data=veri, timeout=timeout)
            self.degiskenler[degisken_adi] = response
            self.degiskenler[f"{degisken_adi}_kod"] = response.status_code
        except requests.exceptions.ConnectionError:
            print(f"Hata: Baglanti kurulamadi: '{url}'")
            self.degiskenler[degisken_adi] = None
        except requests.exceptions.Timeout:
            print(f"Hata: Baglanti zaman asimi ({timeout}s): '{url}'")
            self.degiskenler[degisken_adi] = None
        except Exception as e:
            print(f"PATCH istegi hatasi: {e}")
            self.degiskenler[degisken_adi] = None

    def dosya_indir(self, satir):
        self.ag_kontrol()
        govde = satir[len('dosya_indir '):].strip()
        parcalar = parse_qt_command(govde)
        if len(parcalar) < 2:
            print("Hata: dosya_indir <url> <dosya_adi> seklinde kullanin.")
            return
        url = str(self.ifade_hesapla(parcalar[0]))
        dosya_adi = str(self.ifade_hesapla(parcalar[1]))
        timeout = self.degiskenler.get('ag_timeout', 60)
        MAX_INDIR_BOYUT = 500 * 1024 * 1024  # 500 MB
        try:
            hedef_dizin = os.path.dirname(dosya_adi)
            if hedef_dizin:
                os.makedirs(hedef_dizin, exist_ok=True)
            response = self.requests_session.get(url, stream=True, timeout=timeout)
            response.raise_for_status()
            icerik_boyut = int(response.headers.get('content-length', 0))
            if icerik_boyut > MAX_INDIR_BOYUT:
                print(f"Hata: Dosya cok buyuk ({icerik_boyut // (1024*1024)} MB). Maksimum 500 MB.")
                return
            indirilen = 0
            with open(dosya_adi, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        indirilen += len(chunk)
                        if icerik_boyut > 0:
                            yuzde = (indirilen / icerik_boyut) * 100
                            print(f"Indiriliyor: %{yuzde:.1f} ({indirilen // 1024} KB)", end='\r')
            print(f"\nIndirme tamamlandi: '{dosya_adi}' ({indirilen // 1024} KB)")
        except requests.exceptions.ConnectionError:
            print(f"Hata: Baglanti kurulamadi: '{url}'")
        except requests.exceptions.Timeout:
            print(f"Hata: Baglanti zaman asimi ({timeout}s): '{url}'")
        except requests.exceptions.HTTPError as e:
            print(f"Hata: HTTP hatasi ({e.response.status_code}): '{url}'")
        except PermissionError:
            print(f"Hata: Dosya yazma izni yok: '{dosya_adi}'")
        except Exception as e:
            print(f"Dosya indirme hatasi: {e}")

    def json_al(self, satir):
        self.ag_kontrol()
        govde = satir[len('json_al '):].strip()
        parcalar = parse_qt_command(govde)
        if len(parcalar) < 2:
            print("Hata: json_al <degisken> <url> seklinde kullanin.")
            return
        degisken_adi = parcalar[0]
        url = str(self.ifade_hesapla(parcalar[1]))
        timeout = self.degiskenler.get('ag_timeout', 30)
        try:
            response = self.requests_session.get(url, timeout=timeout)
            response.raise_for_status()
            self.degiskenler[degisken_adi] = response.json()
        except requests.exceptions.JSONDecodeError:
            print(f"Hata: Sunucu gecerli JSON dondurmedi: '{url}'")
            self.degiskenler[degisken_adi] = None
        except requests.exceptions.ConnectionError:
            print(f"Hata: Baglanti kurulamadi: '{url}'")
            self.degiskenler[degisken_adi] = None
        except requests.exceptions.Timeout:
            print(f"Hata: Baglanti zaman asimi ({timeout}s): '{url}'")
            self.degiskenler[degisken_adi] = None
        except Exception as e:
            print(f"JSON alma hatasi: {e}")
            self.degiskenler[degisken_adi] = None

    def json_gonder(self, satir):
        self.ag_kontrol()
        govde = satir[len('json_gonder '):].strip()
        parcalar = parse_qt_command(govde)
        if len(parcalar) < 3:
            print("Hata: json_gonder <degisken> <url> <veri> seklinde kullanin.")
            return
        degisken_adi = parcalar[0]
        url = str(self.ifade_hesapla(parcalar[1]))
        veri = self.ifade_hesapla(parcalar[2])
        timeout = self.degiskenler.get('ag_timeout', 30)
        try:
            response = self.requests_session.post(url, json=veri, timeout=timeout)
            self.degiskenler[degisken_adi] = response
            self.degiskenler[f"{degisken_adi}_kod"] = response.status_code
        except requests.exceptions.ConnectionError:
            print(f"Hata: Baglanti kurulamadi: '{url}'")
            self.degiskenler[degisken_adi] = None
        except requests.exceptions.Timeout:
            print(f"Hata: Baglanti zaman asimi ({timeout}s): '{url}'")
            self.degiskenler[degisken_adi] = None
        except Exception as e:
            print(f"JSON gonderme hatasi: {e}")
            self.degiskenler[degisken_adi] = None

    def ping(self, satir):
        self.ag_kontrol()
        govde = satir[len('ping '):].strip()
        parcalar = parse_qt_command(govde)
        degisken_adi = parcalar[0]
        url = self.ifade_hesapla(parcalar[1])
        try:
            baslangic = time.time()
            response = self.requests_session.get(str(url), timeout=5)
            sure = (time.time() - baslangic) * 1000
            self.degiskenler[degisken_adi] = sure
            self.degiskenler[f"{degisken_adi}_durum"] = response.status_code
        except Exception as e:
            print(f"Ping hatasi: {e}")
            self.degiskenler[degisken_adi] = -1

    def baslik_ekle(self, satir):
        self.ag_kontrol()
        govde = satir[len('baslik_ekle '):].strip()
        parcalar = parse_qt_command(govde)
        anahtar = self.ifade_hesapla(parcalar[0])
        deger = self.ifade_hesapla(parcalar[1])
        self.requests_session.headers[str(anahtar)] = str(deger)

    def cerez_ekle(self, satir):
        self.ag_kontrol()
        govde = satir[len('cerez_ekle '):].strip()
        parcalar = parse_qt_command(govde)
        anahtar = self.ifade_hesapla(parcalar[0])
        deger = self.ifade_hesapla(parcalar[1])
        self.requests_session.cookies.set(str(anahtar), str(deger))

    def timeout_ayarla(self, satir):
        timeout = int(self.ifade_hesapla(satir[len('timeout_ayarla '):].strip()))
        self.degiskenler['ag_timeout'] = timeout

    def proxy_ayarla(self, satir):
        self.ag_kontrol()
        proxy_url = self.ifade_hesapla(satir[len('proxy_ayarla '):].strip())
        self.requests_session.proxies = {'http': str(proxy_url), 'https': str(proxy_url)}

    def ssl_dogrula(self, satir):
        self.degiskenler['ssl_dogrula'] = bool(self.ifade_hesapla(satir[len('ssl_dogrula '):].strip()))

    def yonlendir_izin(self, satir):
        self.degiskenler['yonlendir_izin'] = bool(self.ifade_hesapla(satir[len('yonlendir_izin '):].strip()))

    def stream_indir(self, satir):
        self.ag_kontrol()
        govde = satir[len('stream_indir '):].strip()
        parcalar = parse_qt_command(govde)
        url = self.ifade_hesapla(parcalar[0])
        dosya_adi = self.ifade_hesapla(parcalar[1])
        try:
            with self.requests_session.get(str(url), stream=True) as response:
                response.raise_for_status()
                toplam_boyut = int(response.headers.get('content-length', 0))
                with open(str(dosya_adi), 'wb') as f:
                    indirilen = 0
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                        indirilen += len(chunk)
                        if toplam_boyut > 0:
                            yuzde = (indirilen / toplam_boyut) * 100
                            print(f"Indiriliyor: %{yuzde:.1f}", end='\r')
                print(f"\nIndirme tamamlandi: {dosya_adi}")
        except Exception as e:
            print(f"Stream indirme hatasi: {e}")

    def coklu_dosya_gonder(self, satir):
        self.ag_kontrol()
        govde = satir[len('coklu_dosya_gonder '):].strip()
        parcalar = parse_qt_command(govde)
        if len(parcalar) < 3:
            print("Hata: coklu_dosya_gonder <degisken> <url> <dosya_listesi> seklinde kullanin.")
            return
        degisken_adi = parcalar[0]
        url = str(self.ifade_hesapla(parcalar[1]))
        dosya_listesi = self.ifade_hesapla(parcalar[2])
        if not isinstance(dosya_listesi, (list, tuple)):
            print("Hata: Dosya listesi bir liste olmali.")
            return
        timeout = self.degiskenler.get('ag_timeout', 60)
        acilanlar = []
        try:
            for d in dosya_listesi:
                if not os.path.exists(str(d)):
                    print(f"Uyari: Dosya bulunamadi, atlaniyor: '{d}'")
                    continue
                acilanlar.append(('files', open(str(d), 'rb')))
            if not acilanlar:
                print("Hata: Gonderilecek gecerli dosya yok.")
                return
            response = self.requests_session.post(url, files=acilanlar, timeout=timeout)
            self.degiskenler[degisken_adi] = response
            self.degiskenler[f"{degisken_adi}_kod"] = response.status_code
        except requests.exceptions.ConnectionError:
            print(f"Hata: Baglanti kurulamadi: '{url}'")
            self.degiskenler[degisken_adi] = None
        except requests.exceptions.Timeout:
            print(f"Hata: Baglanti zaman asimi ({timeout}s): '{url}'")
            self.degiskenler[degisken_adi] = None
        except Exception as e:
            print(f"Coklu dosya gonderme hatasi: {e}")
            self.degiskenler[degisken_adi] = None
        finally:
            for _, f in acilanlar:
                try:
                    f.close()
                except Exception:
                    pass

    def durum_kodu(self, satir):
        govde = satir[len('durum_kodu '):].strip()
        parcalar = govde.split()
        response_adi = parcalar[0]
        kod_adi = parcalar[1]
        if response_adi in self.degiskenler:
            response = self.degiskenler[response_adi]
            if hasattr(response, 'status_code'):
                self.degiskenler[kod_adi] = response.status_code

    # ==================== GPIO ====================

    def _gpio_platform_kontrol(self):
        """GPIO komutlarından önce platformun Raspberry Pi olup olmadığını kontrol eder."""
        import platform
        makine = platform.machine().lower()
        # Raspberry Pi'de makine genellikle 'armv7l', 'aarch64', 'armv6l' gibi olur
        # ve /proc/cpuinfo dosyasında 'Raspberry Pi' geçer
        pi_mi = False
        try:
            with open('/proc/cpuinfo', 'r') as f:
                icerik = f.read()
            if 'raspberry pi' in icerik.lower() or 'bcm' in icerik.lower():
                pi_mi = True
        except Exception:
            pass
        if not pi_mi and makine not in ('armv7l', 'aarch64', 'armv6l', 'armv8l'):
            raise RuntimeError(
                "GPIO yalnızca Raspberry Pi üzerinde çalışır. "
                f"Mevcut platform: {platform.system()} {platform.machine()}"
            )

    def gpio_baslat(self):
        self._gpio_platform_kontrol()
        if self.gpio_handle is not None:
            print("Uyarı: GPIO zaten açık. Tekrar başlatılmıyor.")
            return
        try:
            self.gpio_handle = lgpio.gpiochip_open(0)
            print("GPIO başlatıldı (chip 0).")
        except Exception as e:
            print(f"GPIO başlatma hatası: {e}")
            self.gpio_handle = None

    def gpio_kapat(self):
        if self.gpio_handle is not None:
            try:
                lgpio.gpiochip_close(self.gpio_handle)
            except Exception:
                pass
            self.gpio_handle = None

    def gpio_mod(self, satir):
        self._gpio_platform_kontrol()
        govde = satir[len('gpio_mod '):].strip()
        parcalar = govde.split()
        if len(parcalar) < 2:
            print("Hata: gpio_mod <pin> <cikis|giris> seklinde kullanin.")
            return
        try:
            pin = int(parcalar[0])
        except ValueError:
            print(f"Hata: Gecersiz pin numarasi: '{parcalar[0]}'")
            return
        mod = parcalar[1]
        if mod not in ("cikis", "giris"):
            print(f"Hata: Gecersiz GPIO modu: '{mod}'. 'cikis' veya 'giris' kullanin.")
            return
        if self.gpio_handle is None:
            self.gpio_baslat()
        if self.gpio_handle is None:
            print("Hata: GPIO baslatilamadi, mod ayarlanamadi.")
            return
        try:
            if mod == "cikis":
                lgpio.gpio_claim_output(self.gpio_handle, pin)
                self.gpio_pins[pin] = "cikis"
            elif mod == "giris":
                lgpio.gpio_claim_input(self.gpio_handle, pin)
                self.gpio_pins[pin] = "giris"
        except Exception as e:
            print(f"GPIO mod hatasi (pin {pin}): {e}")

    def gpio_yaz(self, satir):
        self._gpio_platform_kontrol()
        govde = satir[len('gpio_yaz '):].strip()
        parcalar = govde.split()
        if len(parcalar) < 2:
            print("Hata: gpio_yaz <pin> <deger> seklinde kullanin.")
            return
        try:
            pin = int(parcalar[0])
        except ValueError:
            print(f"Hata: Gecersiz pin numarasi: '{parcalar[0]}'")
            return
        deger = self.ifade_hesapla(parcalar[1])
        deger = 1 if deger else 0
        if self.gpio_handle is None:
            self.gpio_baslat()
        if self.gpio_handle is None:
            print("Hata: GPIO baslatilamadi.")
            return
        if self.gpio_pins.get(pin) not in ("cikis",):
            print(f"Uyari: Pin {pin} cikis olarak ayarlanmamis. Otomatik cikis moduna aliniyor.")
            try:
                lgpio.gpio_claim_output(self.gpio_handle, pin)
                self.gpio_pins[pin] = "cikis"
            except Exception as e:
                print(f"Hata: Pin {pin} cikis moduna alinamadi: {e}")
                return
        try:
            lgpio.gpio_write(self.gpio_handle, pin, deger)
        except Exception as e:
            print(f"GPIO yazma hatasi (pin {pin}): {e}")

    def gpio_oku(self, satir):
        self._gpio_platform_kontrol()
        govde = satir[len('gpio_oku '):].strip()
        parcalar = govde.split()
        if len(parcalar) < 2:
            print("Hata: gpio_oku <pin> <degisken> seklinde kullanin.")
            return
        try:
            pin = int(parcalar[0])
        except ValueError:
            print(f"Hata: Gecersiz pin numarasi: '{parcalar[0]}'")
            return
        degisken_adi = parcalar[1]
        if self.gpio_handle is None:
            self.gpio_baslat()
        if self.gpio_handle is None:
            print("Hata: GPIO baslatilamadi.")
            self.degiskenler[degisken_adi] = None
            return
        try:
            self.degiskenler[degisken_adi] = lgpio.gpio_read(self.gpio_handle, pin)
        except Exception as e:
            print(f"GPIO okuma hatasi (pin {pin}): {e}")
            self.degiskenler[degisken_adi] = None

    def gpio_yukari_cek(self, satir):
        pin = int(satir[len('gpio_yukari_cek '):].strip())
        if self.gpio_handle is None:
            self.gpio_baslat()
        try:
            lgpio.gpio_claim_input(self.gpio_handle, pin, getattr(lgpio, 'SET_PULL_UP', 0))
            self.gpio_pins[pin] = "giris_yukari"
        except Exception as e:
            print(f"GPIO cekme hatasi: {e}")

    def gpio_asagi_cek(self, satir):
        pin = int(satir[len('gpio_asagi_cek '):].strip())
        if self.gpio_handle is None:
            self.gpio_baslat()
        try:
            lgpio.gpio_claim_input(self.gpio_handle, pin, getattr(lgpio, 'SET_PULL_DOWN', 0))
            self.gpio_pins[pin] = "giris_asagi"
        except Exception as e:
            print(f"GPIO cekme hatasi: {e}")

    def gpio_kesme_ekle(self, satir):
        govde = satir[len('gpio_kesme '):].strip()
        parcalar = govde.split()
        pin = int(parcalar[0])
        kenar = parcalar[1]
        fonksiyon_adi = parcalar[2] if len(parcalar) > 2 else None
        if self.gpio_handle is None:
            self.gpio_baslat()
        try:
            if kenar == "yukari": edge = getattr(lgpio, 'RISING_EDGE', 1)
            elif kenar == "asagi": edge = getattr(lgpio, 'FALLING_EDGE', 2)
            else: edge = getattr(lgpio, 'BOTH_EDGES', 3)
            fonksiyon = self.degiskenler.get(fonksiyon_adi) if fonksiyon_adi else None
            if fonksiyon and callable(fonksiyon):
                cb = lgpio.callback(self.gpio_handle, pin, edge, fonksiyon)
                self.gpio_callbackler[pin] = cb
        except Exception as e:
            print(f"GPIO kesme hatasi: {e}")

    def gpio_kesme_kaldir(self, satir):
        pin = int(satir[len('gpio_kesme_kaldir '):].strip())
        if pin in self.gpio_callbackler:
            try:
                self.gpio_callbackler[pin].cancel()
                del self.gpio_callbackler[pin]
            except Exception as e:
                print(f"GPIO kesme kaldirma hatasi: {e}")

    def pwm_baslat(self, satir):
        govde = satir[len('pwm_baslat '):].strip()
        parcalar = govde.split()
        if len(parcalar) < 2:
            print("Hata: pwm_baslat <pin> <frekans> [duty] seklinde kullanin.")
            return
        try:
            pin, frekans = int(parcalar[0]), int(parcalar[1])
        except ValueError as e:
            print(f"Hata: pwm_baslat icin gecersiz deger: {e}")
            return
        duty = int(parcalar[2]) if len(parcalar) > 2 else 50
        duty = max(0, min(100, duty))  # 0-100 araliginda tut
        if frekans <= 0:
            print(f"Hata: PWM frekans pozitif olmali, alindi: {frekans}")
            return
        if self.gpio_handle is None:
            self.gpio_baslat()
        if self.gpio_handle is None:
            print("Hata: GPIO baslatilamadi, PWM baslatilmiyor.")
            return
        try:
            lgpio.tx_pwm(self.gpio_handle, pin, frekans, duty)
            self.pwm_pins[pin] = {'frekans': frekans, 'duty': duty}
        except Exception as e:
            print(f"PWM baslama hatasi (pin {pin}): {e}")

    def pwm_durdur(self, satir):
        pin = int(satir[len('pwm_durdur '):].strip())
        if self.gpio_handle is None:
            return
        try:
            lgpio.tx_pwm(self.gpio_handle, pin, 0, 0)
            self.pwm_pins.pop(pin, None)
        except Exception as e:
            print(f"PWM durdurma hatasi: {e}")

    def pwm_ayarla(self, satir):
        govde = satir[len('pwm_ayarla '):].strip()
        parcalar = govde.split()
        if len(parcalar) < 2:
            print("Hata: pwm_ayarla <pin> <duty> seklinde kullanin.")
            return
        try:
            pin, duty = int(parcalar[0]), int(parcalar[1])
        except ValueError as e:
            print(f"Hata: pwm_ayarla icin gecersiz deger: {e}")
            return
        duty = max(0, min(100, duty))
        if pin not in self.pwm_pins:
            print(f"Uyari: Pin {pin} icin aktif PWM bulunamadi. Once pwm_baslat kullanin.")
            return
        if self.gpio_handle is None:
            print("Hata: GPIO bagli degil.")
            return
        frekans = self.pwm_pins[pin]['frekans']
        try:
            lgpio.tx_pwm(self.gpio_handle, pin, frekans, duty)
            self.pwm_pins[pin]['duty'] = duty
        except Exception as e:
            print(f"PWM ayarlama hatasi (pin {pin}): {e}")

    def pwm_frekans_ayarla(self, satir):
        govde = satir[len('pwm_frekans '):].strip()
        parcalar = govde.split()
        pin, frekans = int(parcalar[0]), int(parcalar[1])
        if pin in self.pwm_pins:
            duty = self.pwm_pins[pin]['duty']
            try:
                lgpio.tx_pwm(self.gpio_handle, pin, frekans, duty)
                self.pwm_pins[pin]['frekans'] = frekans
            except Exception as e:
                print(f"PWM frekans hatasi: {e}")

    def i2c_baslat(self, satir):
        govde = satir[len('i2c_baslat '):].strip()
        if not govde:
            print("Hata: i2c_baslat <adres> seklinde kullanin.")
            return
        try:
            adres = int(govde, 0)  # hex (0x27) veya decimal destegi
        except ValueError:
            print(f"Hata: Gecersiz I2C adresi: '{govde}'. Ornek: i2c_baslat 0x27")
            return
        if self.i2c_handle is not None:
            print("Uyari: I2C zaten acik. Once i2c_kapat kullanin.")
            return
        try:
            self.i2c_handle = lgpio.i2c_open(1, adres)
        except Exception as e:
            print(f"I2C baslama hatasi (adres {hex(adres)}): {e}")
            self.i2c_handle = None

    def i2c_kapat(self):
        if self.i2c_handle is not None:
            try:
                lgpio.i2c_close(self.i2c_handle)
            except Exception:
                pass
            self.i2c_handle = None

    def i2c_yaz(self, satir):
        govde = satir[len('i2c_yaz '):].strip()
        parcalar = parse_qt_command(govde)
        veri = self.ifade_hesapla(parcalar[1] if len(parcalar) > 1 else parcalar[0])
        if self.i2c_handle is None:
            print("Hata: I2C bagli degil. Once 'i2c_baslat' kullanin.")
            return
        try:
            if isinstance(veri, int):
                veri = bytes([veri])
            elif isinstance(veri, list):
                veri = bytes(veri)
            elif not isinstance(veri, (bytes, bytearray)):
                veri = str(veri).encode('utf-8')
            lgpio.i2c_write_device(self.i2c_handle, veri)
        except Exception as e:
            print(f"I2C yazma hatasi: {e}")

    def i2c_oku(self, satir):
        govde = satir[len('i2c_oku '):].strip()
        parcalar = govde.split()
        uzunluk = int(parcalar[0]) if len(parcalar) > 0 else 1
        degisken_adi = parcalar[1] if len(parcalar) > 1 else "i2c_veri"
        if self.i2c_handle is None:
            print("Hata: I2C bagli degil. Once 'i2c_baslat' kullanin.")
            self.degiskenler[degisken_adi] = None
            return
        if uzunluk <= 0 or uzunluk > 4096:
            print(f"Hata: Gecersiz okuma uzunlugu: {uzunluk}. 1-4096 araliginda olmali.")
            self.degiskenler[degisken_adi] = None
            return
        try:
            veri = lgpio.i2c_read_device(self.i2c_handle, uzunluk)
            self.degiskenler[degisken_adi] = list(veri[1])
        except Exception as e:
            print(f"I2C okuma hatasi: {e}")
            self.degiskenler[degisken_adi] = None

    def i2c_kayit_yaz(self, satir):
        govde = satir[len('i2c_kayit_yaz '):].strip()
        parcalar = parse_qt_command(govde)
        kayit = int(self.ifade_hesapla(parcalar[0]))
        veri = int(self.ifade_hesapla(parcalar[1]))
        if self.i2c_handle is None:
            return
        try:
            lgpio.i2c_write_device(self.i2c_handle, [kayit, veri])
        except Exception as e:
            print(f"I2C kayit yazma hatasi: {e}")

    def i2c_kayit_oku(self, satir):
        govde = satir[len('i2c_kayit_oku '):].strip()
        parcalar = govde.split()
        kayit = int(parcalar[0])
        uzunluk = int(parcalar[1]) if len(parcalar) > 1 else 1
        degisken_adi = parcalar[2] if len(parcalar) > 2 else "i2c_veri"
        if self.i2c_handle is None:
            return
        try:
            lgpio.i2c_write_device(self.i2c_handle, [kayit])
            veri = lgpio.i2c_read_device(self.i2c_handle, uzunluk)
            self.degiskenler[degisken_adi] = list(veri[1])
        except Exception as e:
            print(f"I2C kayit okuma hatasi: {e}")

    def spi_baslat(self, satir):
        govde = satir[len('spi_baslat '):].strip()
        parcalar = govde.split()
        kanal = int(parcalar[0])
        hiz = int(parcalar[1]) if len(parcalar) > 1 else 1000000
        try:
            self.spi_handle = lgpio.spi_open(1, kanal, hiz)
        except Exception as e:
            print(f"SPI baslama hatasi: {e}")

    def spi_kapat(self):
        if self.spi_handle is not None:
            try:
                lgpio.spi_close(self.spi_handle)
            except Exception:
                pass
            self.spi_handle = None

    def spi_transfer(self, satir):
        govde = satir[len('spi_transfer '):].strip()
        parcalar = parse_qt_command(govde)
        giden = self.ifade_hesapla(parcalar[0])
        degisken_adi = parcalar[1]
        if self.spi_handle is None:
            return
        try:
            gelen = lgpio.spi_xfer(self.spi_handle, giden)
            self.degiskenler[degisken_adi] = list(gelen[1])
        except Exception as e:
            print(f"SPI transfer hatasi: {e}")

    # ==================== ZIP ====================

    def zip_olustur(self, satir):
        dosya_adi = self.ifade_hesapla(satir[len('zip_olustur '):].strip())
        try:
            with zipfile.ZipFile(str(dosya_adi), 'w'):
                pass
        except Exception as e:
            print(f"Zip olusturma hatasi: {e}")

    def zip_ac(self, satir):
        govde = satir[len('zip_ac '):].strip()
        parcalar = parse_qt_command(govde)
        dosya_adi = self.ifade_hesapla(parcalar[0])
        degisken_adi = parcalar[1]
        try:
            zf = zipfile.ZipFile(str(dosya_adi), 'a')
            self.degiskenler[degisken_adi] = zf
        except Exception as e:
            print(f"Zip acma hatasi: {e}")

    def zip_ekle(self, satir):
        govde = satir[len('zip_ekle '):].strip()
        parcalar = parse_qt_command(govde)
        zip_adi = self.ifade_hesapla(parcalar[0])
        dosya_yolu = self.ifade_hesapla(parcalar[1])
        arsiv_adi = self.ifade_hesapla(parcalar[2]) if len(parcalar) > 2 else None
        try:
            with zipfile.ZipFile(str(zip_adi), 'a') as zf:
                zf.write(str(dosya_yolu), arsiv_adi or os.path.basename(str(dosya_yolu)))
        except Exception as e:
            print(f"Zip ekleme hatasi: {e}")

    def zip_cikar(self, satir):
        govde = satir[len('zip_cikar '):].strip()
        parcalar = parse_qt_command(govde)
        zip_adi = self.ifade_hesapla(parcalar[0])
        hedef = self.ifade_hesapla(parcalar[1])
        dosya = self.ifade_hesapla(parcalar[2]) if len(parcalar) > 2 else None
        try:
            with zipfile.ZipFile(str(zip_adi), 'r') as zf:
                if dosya:
                    zf.extract(str(dosya), str(hedef))
                else:
                    zf.extractall(str(hedef))
        except Exception as e:
            print(f"Zip cikarma hatasi: {e}")

    def zip_listele(self, satir):
        govde = satir[len('zip_listele '):].strip()
        parcalar = parse_qt_command(govde)
        zip_adi = self.ifade_hesapla(parcalar[0])
        degisken_adi = parcalar[1]
        try:
            with zipfile.ZipFile(str(zip_adi), 'r') as zf:
                dosyalar = zf.namelist()
                self.degiskenler[degisken_adi] = dosyalar
                for dosya in dosyalar:
                    print(f"  - {dosya}")
        except Exception as e:
            print(f"Zip listeleme hatasi: {e}")

    def zip_sil(self, satir):
        dosya_adi = self.ifade_hesapla(satir[len('zip_sil '):].strip())
        try:
            os.remove(str(dosya_adi))
        except Exception as e:
            print(f"Zip silme hatasi: {e}")

    # ==================== IFADE HESAPLAMA ====================

    def ifade_hesapla(self, ifade):
        ifade = str(ifade).strip()
        if not ifade:
            return ""

        # String literalleri - icindeki her sey oldugu gibi doner
        if (ifade.startswith('"') and ifade.endswith('"') and len(ifade) >= 2) or \
           (ifade.startswith("'") and ifade.endswith("'") and len(ifade) >= 2):
            return ifade[1:-1]

        # Boolean ve None
        if ifade == 'dogru': return True
        if ifade == 'yanlis': return False
        if ifade == 'hic': return None

        # Tam sayi
        try:
            return int(ifade)
        except ValueError:
            pass

        # Ondalikli
        try:
            return float(ifade)
        except ValueError:
            pass

        # Liste literali
        if ifade.startswith('[') and ifade.endswith(']'):
            icerik = ifade[1:-1].strip()
            if not icerik:
                return []
            return [self.ifade_hesapla(e.strip()) for e in self.listeyi_ayir(icerik)]

        # Sozluk literali
        if ifade.startswith('{') and ifade.endswith('}'):
            icerik = ifade[1:-1].strip()
            if not icerik:
                return {}
            sozluk = {}
            for eleman in self.listeyi_ayir(icerik):
                if ':' in eleman:
                    k, v = eleman.split(':', 1)
                    sozluk[self.ifade_hesapla(k.strip())] = self.ifade_hesapla(v.strip())
            return sozluk

        # Turkce operatorleri donustur
        ifade = self.turkce_to_python(ifade)

        # Saf fonksiyon cagrisi mi? Ornek: "uzunluk(x)" evet, "uzunluk(x) > 0" hayir
        if '(' in ifade and ')' in ifade:
            ilk_paren = ifade.index('(')
            son_paren = ifade.rindex(')')
            # Saf cagri: parantez kapandiktan sonra baska karakter yok
            if son_paren == len(ifade) - 1:
                on_kisim = ifade[:ilk_paren].strip()
                # Sadece bir kelime ise fonksiyon cagrisi
                if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', on_kisim):
                    return self.fonksiyon_cagir(ifade)

        # Indeks erisimi: dizi[0]
        if '[' in ifade and ']' in ifade:
            ilk_kose = ifade.index('[')
            son_kose = ifade.rindex(']')
            if son_kose == len(ifade) - 1:
                degisken_adi = ifade[:ilk_kose].strip()
                indeks_ifade = ifade[ilk_kose+1:son_kose].strip()
                if degisken_adi in self.degiskenler:
                    indeks = self.ifade_hesapla(indeks_ifade)
                    try:
                        return self.degiskenler[degisken_adi][indeks]
                    except (IndexError, KeyError, TypeError) as e:
                        print(f"Hata: Indeks erisim hatasi '{degisken_adi}[{indeks}]': {e}")
                        return None

        # Degisken
        if ifade in self.degiskenler:
            return self.degiskenler[ifade]

        # Matematiksel / mantiksal / karmasik ifade - eval
        # TSharp builtin fonksiyonlarini eval ortamina ekle
        try:
            yerel = {k: v for k, v in self.degiskenler.items()}
            yerel['math'] = math
            yerel['random'] = random
            yerel['np'] = np
            if OPENCV_AVAILABLE:
                yerel['cv2'] = cv2
            # TSharp builtin'lerini ekle - "uzunluk(x) > 0" gibi ifadeler calissin
            ts = self
            yerel['uzunluk']       = lambda x: len(x)
            yerel['tur']           = lambda x: type(x).__name__
            yerel['yaziya']        = lambda x: str(x)
            yerel['sayiya']        = lambda x: int(x)
            yerel['ondalikliya']   = lambda x: float(x)
            yerel['yuvarla']       = lambda x, n=0: round(x, n)
            yerel['mutlak']        = lambda x: abs(x)
            yerel['karekok']       = lambda x: math.sqrt(x)
            yerel['taban']         = lambda x: math.floor(x)
            yerel['tavan']         = lambda x: math.ceil(x)
            yerel['minimum']       = lambda x: min(x) if isinstance(x, (list,tuple)) else x
            yerel['maksimum']      = lambda x: max(x) if isinstance(x, (list,tuple)) else x
            yerel['toplam']        = lambda x: sum(x) if isinstance(x, (list,tuple)) else x
            yerel['icindemi']      = lambda a, b: a in b
            yerel['rastgele_sayi'] = lambda a, b: random.randint(int(a), int(b))
            yerel['rastgele_sec']  = lambda x: random.choice(x)
            return eval(ifade, {"__builtins__": {}}, yerel)
        except Exception:
            return ifade

    def fonksiyon_cagir(self, ifade):
        fonk_adi = ifade[:ifade.index('(')].strip()
        params_str = ifade[ifade.index('(')+1:ifade.rindex(')')].strip()
        args = [self.ifade_hesapla(p) for p in self.listeyi_ayir(params_str)] if params_str else []

        # Yerleşik fonksiyonlar
        builtins = {
            'uzunluk': lambda: len(args[0]) if args else 0,
            'tur': lambda: type(args[0]).__name__ if args else 'none',
            'yaziya': lambda: str(args[0]) if args else '',
            'sayiya': lambda: int(args[0]) if args else 0,
            'ondalikliya': lambda: float(args[0]) if args else 0.0,
            'ekle': lambda: (args[0].append(args[1]), args[0])[1] if len(args) >= 2 and isinstance(args[0], list) else args[0],
            'cikar': lambda: (args[0].remove(args[1]), args[0])[1] if len(args) >= 2 and isinstance(args[0], list) else args[0],
            'sirala': lambda: sorted(args[0]) if args and isinstance(args[0], (list, tuple)) else (sorted(args) if args else []),
            'tersine_cevir': lambda: list(reversed(args[0])) if args and isinstance(args[0], list) else args[0],
            'birles': lambda: args[0] + args[1] if len(args) >= 2 and isinstance(args[0], list) else [],
            'dilimleme': lambda: args[0][int(args[1]):int(args[2])] if len(args) >= 3 else [],
            'icindemi': lambda: args[0] in args[1] if len(args) >= 2 else False,
            'indeks': lambda: args[1].index(args[0]) if len(args) >= 2 else -1,
            'rastgele_sayi': lambda: random.randint(int(args[0]), int(args[1])) if len(args) >= 2 else random.random(),
            'rastgele_sec': lambda: random.choice(args[0]) if args and isinstance(args[0], list) else None,
            'karistir': lambda: (random.shuffle(lst := args[0][:]), lst)[1] if args else [],
            'mutlak': lambda: abs(args[0]) if args else 0,
            'karekok': lambda: math.sqrt(args[0]) if args else 0,
            'us': lambda: math.pow(args[0], args[1]) if len(args) >= 2 else 0,
            'yuvarla': lambda: round(args[0], args[1] if len(args) >= 2 else 0) if args else 0,
            'taban': lambda: math.floor(args[0]) if args else 0,
            'tavan': lambda: math.ceil(args[0]) if args else 0,
            'minimum': lambda: min(args[0]) if args and isinstance(args[0], (list, tuple)) else (min(args) if args else None),
            'maksimum': lambda: max(args[0]) if args and isinstance(args[0], (list, tuple)) else (max(args) if args else None),
            'toplam': lambda: sum(args[0]) if args and isinstance(args[0], (list, tuple)) else sum(args),
            'ortalama': lambda: (sum(args[0]) / len(args[0])) if args and isinstance(args[0], (list, tuple)) and args[0] else (sum(args) / len(args) if args else 0),
            'sinus': lambda: math.sin(args[0]) if args else 0,
            'kosinus': lambda: math.cos(args[0]) if args else 0,
            'tanjant': lambda: math.tan(args[0]) if args else 0,
            'logaritma': lambda: math.log(args[0], args[1]) if len(args) >= 2 else (math.log(args[0]) if args else 0),
            'pi': lambda: math.pi,
            'radyana': lambda: math.radians(args[0]) if args else 0,
            'dereceye': lambda: math.degrees(args[0]) if args else 0,
            'buyuk_harf': lambda: str(args[0]).upper() if args else '',
            'kucuk_harf': lambda: str(args[0]).lower() if args else '',
            'basa_bas': lambda: str(args[0]).strip() if args else '',
            'bol': lambda: str(args[0]).split(str(args[1])) if len(args) >= 2 else (str(args[0]).split() if args else []),
            'birlestir': lambda: str(args[0]).join([str(x) for x in args[1]]) if len(args) >= 2 else '',
            'degistir': lambda: str(args[0]).replace(str(args[1]), str(args[2])) if len(args) >= 3 else (str(args[0]) if args else ''),
            'baslar_mi': lambda: str(args[0]).startswith(str(args[1])) if len(args) >= 2 else False,
            'biter_mi': lambda: str(args[0]).endswith(str(args[1])) if len(args) >= 2 else False,
            'bul': lambda: str(args[0]).find(str(args[1])) if len(args) >= 2 else -1,
            'dilim': lambda: str(args[0])[int(args[1]):int(args[2])] if len(args) >= 3 else (str(args[0])[int(args[1]):] if len(args) >= 2 else ''),
            'zaman': lambda: time.time(),
            'bekle': lambda: time.sleep(float(args[0])) if args else None,
            'dosya_oku': self._builtin_dosya_oku,
            'dosya_yaz': self._builtin_dosya_yaz,
            'dosya_ekle': self._builtin_dosya_ekle,
            'dosya_var_mi': lambda: os.path.exists(str(args[0])) if args else False,
            'klasor_olustur': lambda: (os.makedirs(str(args[0]), exist_ok=True), True)[1] if args else False,
        }

        if fonk_adi in builtins:
            try:
                fn = builtins[fonk_adi]
                # dosya builtins kendi args referansini kapatiyor, digerlerini cagiralim
                if fonk_adi in ('dosya_oku', 'dosya_yaz', 'dosya_ekle'):
                    return fn(args)
                return fn()
            except Exception as e:
                raise ValueError(f"Fonksiyon hatasi '{fonk_adi}': {e}")

        # Kullanıcı tanımlı fonksiyon
        if fonk_adi in self.degiskenler:
            fonk = self.degiskenler[fonk_adi]
            if callable(fonk):
                return fonk(*args)

        raise ValueError(f"Bilinmeyen fonksiyon: {fonk_adi}")

    def listeyi_ayir(self, icerik):
        elemanlar = []
        eleman = ""
        parantez = 0
        koseli = 0
        tirnak = False
        tirnak_char = None
        for char in icerik:
            if char in ['"', "'"]:
                if not tirnak:
                    tirnak = True
                    tirnak_char = char
                elif char == tirnak_char:
                    tirnak = False
                eleman += char
            elif tirnak:
                eleman += char
            elif char == '(':
                parantez += 1
                eleman += char
            elif char == ')':
                parantez -= 1
                eleman += char
            elif char in '[{':
                koseli += 1
                eleman += char
            elif char in ']}':
                koseli -= 1
                eleman += char
            elif char == ',' and parantez == 0 and koseli == 0:
                elemanlar.append(eleman.strip())
                eleman = ""
            else:
                eleman += char
        if eleman.strip():
            elemanlar.append(eleman.strip())
        return elemanlar

    def turkce_to_python(self, ifade):
        ifade = re.sub(r'\bdogru\b', 'True', ifade)
        ifade = re.sub(r'\byanlis\b', 'False', ifade)
        ifade = re.sub(r'\bhic\b', 'None', ifade)
        ifade = re.sub(r'\besittir\b', '==', ifade)
        ifade = re.sub(r'\bbuyuktur\b', '>', ifade)
        ifade = re.sub(r'\bkucuktur\b', '<', ifade)
        ifade = re.sub(r'\bdegildir\b', '!=', ifade)
        ifade = re.sub(r'\bbuyuk_esit\b', '>=', ifade)
        ifade = re.sub(r'\bkucuk_esit\b', '<=', ifade)
        ifade = re.sub(r'\bve\b', 'and', ifade)
        ifade = re.sub(r'\bveya\b', 'or', ifade)
        ifade = re.sub(r'\bdegil\b', 'not', ifade)
        ifade = re.sub(r'\bicinde\b', 'in', ifade)
        ifade = re.sub(r'\bmod\b', '%', ifade)
        ifade = re.sub(r'\bbolum\b', '//', ifade)
        return ifade

    def kosul_kontrol(self, kosul):
        sonuc = self.ifade_hesapla(kosul)
        if isinstance(sonuc, np.ndarray):
            return False
        return bool(sonuc)

    def eger_blogu(self, satirlar, baslangic):
        satir = satirlar[baslangic].strip() if isinstance(satirlar[baslangic], str) else str(satirlar[baslangic]).strip()
        kosul = re.sub(r'^eger\s+', '', satir).replace(':', '').strip()
        kosul_sonuc = self.kosul_kontrol(kosul)
        i = baslangic + 1
        blok_satirlari = []
        degilse_satirlari = []
        degilse_mod = False
        derinlik = 1
        while i < len(satirlar):
            s = satirlar[i].strip() if isinstance(satirlar[i], str) else str(satirlar[i]).strip()
            # ic ice blok baslayinca derinligi artir
            if any(s.startswith(b) for b in BLOK_BASLATAN):
                derinlik += 1
            elif s == 'son':
                derinlik -= 1
                if derinlik == 0:
                    break
            # degilse sadece derinlik 1'de anlam ifade eder
            if derinlik == 1 and s in ('degilse:', 'degilse'):
                degilse_mod = True
                i += 1
                continue
            if degilse_mod:
                degilse_satirlari.append(satirlar[i])
            else:
                blok_satirlari.append(satirlar[i])
            i += 1
        if kosul_sonuc:
            self.satirlari_calistir(blok_satirlari)
        elif degilse_satirlari:
            self.satirlari_calistir(degilse_satirlari)
        return i + 1

    def dongu_blogu(self, satirlar, baslangic):
        satir = satirlar[baslangic].strip() if isinstance(satirlar[baslangic], str) else str(satirlar[baslangic]).strip()
        kosul = satir[len('dongu '):].replace(':', '').strip()
        i = baslangic + 1
        blok_satirlari = []
        derinlik = 1
        while i < len(satirlar):
            s = satirlar[i].strip() if isinstance(satirlar[i], str) else str(satirlar[i]).strip()
            # ic ice blok baslayinca derinligi artir
            if any(s.startswith(b) for b in BLOK_BASLATAN):
                derinlik += 1
            elif s == 'son':
                derinlik -= 1
                if derinlik == 0:
                    break
            blok_satirlari.append(satirlar[i])
            i += 1
        MAX_DONGU = 10_000_000  # sonsuz dongu koruması
        dongu_sayac = 0
        while self.kosul_kontrol(kosul):
            dongu_sayac += 1
            if dongu_sayac > MAX_DONGU:
                print(f"Hata: Dongu {MAX_DONGU} iterasyonu asti. Sonsuz dongu olabilir, durduruldu.")
                break
            try:
                self.satirlari_calistir(blok_satirlari)
            except BreakException:
                break
            except ContinueException:
                continue
        return i + 1

    def her_dongusu(self, satirlar, baslangic):
        satir = satirlar[baslangic].strip() if isinstance(satirlar[baslangic], str) else str(satirlar[baslangic]).strip()
        icerik = satir[len('her '):].replace(':', '').strip()
        parcalar = icerik.split(' icinde ')
        if len(parcalar) != 2:
            raise ValueError(f"Hatali her dongusu: {satir}")
        degisken_adi = parcalar[0].strip()
        liste = self.ifade_hesapla(parcalar[1].strip())
        i = baslangic + 1
        blok_satirlari = []
        derinlik = 1
        while i < len(satirlar):
            s = satirlar[i].strip() if isinstance(satirlar[i], str) else str(satirlar[i]).strip()
            if any(s.startswith(b) for b in BLOK_BASLATAN):
                derinlik += 1
            elif s == 'son':
                derinlik -= 1
                if derinlik == 0:
                    break
            blok_satirlari.append(satirlar[i])
            i += 1
        for eleman in (liste if isinstance(liste, (list, tuple, range)) else []):
            # Pygame Event nesnesi ise .key özelliğini değişkene ata (klavye olayları için)
            if PYGAME_AVAILABLE and type(eleman).__name__ == 'Event':
                if hasattr(eleman, 'key'):
                    self.degiskenler[degisken_adi] = eleman.key
                else:
                    self.degiskenler[degisken_adi] = eleman
            else:
                self.degiskenler[degisken_adi] = eleman
            try:
                self.satirlari_calistir(blok_satirlari)
            except BreakException:
                break
            except ContinueException:
                continue
        return i + 1

    def fonksiyon_tanimla(self, satirlar, baslangic):
        satir = satirlar[baslangic].strip() if isinstance(satirlar[baslangic], str) else str(satirlar[baslangic]).strip()
        icerik = satir[len('fonksiyon '):].replace(':', '').strip()
        if '(' in icerik and ')' in icerik:
            fonk_adi = icerik[:icerik.index('(')].strip()
            params_str = icerik[icerik.index('(')+1:icerik.index(')')].strip()
            parametreler = [p.strip() for p in params_str.split(',')] if params_str else []
        else:
            raise ValueError(f"Hatali fonksiyon tanimi: {satir}")
        if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', fonk_adi):
            raise ValueError(f"Gecersiz fonksiyon adi: '{fonk_adi}'. Sadece harf, rakam ve alt cizgi kullanin.")
        i = baslangic + 1
        govde_satirlari = []
        derinlik = 1
        while i < len(satirlar):
            s = satirlar[i].strip() if isinstance(satirlar[i], str) else str(satirlar[i]).strip()
            if any(s.startswith(b) for b in BLOK_BASLATAN):
                derinlik += 1
            elif s == 'son':
                derinlik -= 1
                if derinlik == 0:
                    break
            govde_satirlari.append(satirlar[i])
            i += 1
        else:
            print(f"Uyari: '{fonk_adi}' fonksiyonu 'son' ile kapatilmamis.")

        MAX_CAGRIMA_DERINLIGI = 500
        cagri_sayaci = [0]

        def fonksiyon_calistir(*args):
            cagri_sayaci[0] += 1
            if cagri_sayaci[0] > MAX_CAGRIMA_DERINLIGI:
                cagri_sayaci[0] = 0
                raise RecursionError(f"Fonksiyon '{fonk_adi}' maksimum cagrima derinligini ({MAX_CAGRIMA_DERINLIGI}) asti. Sonsuz ozyineleme olabilir.")
            eski_degiskenler = self.degiskenler.copy()
            for j, param in enumerate(parametreler):
                if j < len(args):
                    self.degiskenler[param] = args[j]
                else:
                    self.degiskenler[param] = None
            sonuc = None
            try:
                self.satirlari_calistir(govde_satirlari)
            except ReturnException as e:
                sonuc = e.deger
            except RecursionError:
                raise
            finally:
                self.degiskenler = eski_degiskenler
                cagri_sayaci[0] = max(0, cagri_sayaci[0] - 1)
            return sonuc

        self.fonksiyonlar[fonk_adi] = (parametreler, govde_satirlari)
        self.degiskenler[fonk_adi] = fonksiyon_calistir
        return i + 1


    # ==================== DOSYA YARDIMCI ====================

    def _builtin_dosya_oku(self, args):
        if not args:
            return None
        try:
            with open(str(args[0]), 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            print(f"Hata: Dosya bulunamadi: '{args[0]}'")
            return None
        except PermissionError:
            print(f"Hata: Dosya okuma izni yok: '{args[0]}'")
            return None
        except UnicodeDecodeError:
            # UTF-8 basarisiz olursa latin-1 ile tekrar dene
            try:
                with open(str(args[0]), 'r', encoding='latin-1') as f:
                    return f.read()
            except Exception as e:
                print(f"Hata: Dosya okuma hatasi ('{args[0]}'): {e}")
                return None

    def _builtin_dosya_yaz(self, args):
        if len(args) < 2:
            print("Hata: dosya_yaz icin en az 2 arguman gerekli.")
            return False
        try:
            hedef_dizin = os.path.dirname(str(args[0]))
            if hedef_dizin:
                os.makedirs(hedef_dizin, exist_ok=True)
            with open(str(args[0]), 'w', encoding='utf-8') as f:
                f.write(str(args[1]))
            return True
        except PermissionError:
            print(f"Hata: Dosya yazma izni yok: '{args[0]}'")
            return False
        except Exception as e:
            print(f"Hata: Dosya yazma hatasi ('{args[0]}'): {e}")
            return False

    def _builtin_dosya_ekle(self, args):
        if len(args) < 2:
            print("Hata: dosya_ekle icin en az 2 arguman gerekli.")
            return False
        try:
            with open(str(args[0]), 'a', encoding='utf-8') as f:
                f.write(str(args[1]))
            return True
        except PermissionError:
            print(f"Hata: Dosya ekleme izni yok: '{args[0]}'")
            return False
        except Exception as e:
            print(f"Hata: Dosya ekleme hatasi ('{args[0]}'): {e}")
            return False

    # ==================== SIFRELE / BASE64 ====================

    def _sifrele_kontrol(self):
        if not self.sifrele_modu:
            raise RuntimeError("Sifrele modulu aktif degil. 'kullan sifrele' komutunu ekleyin.")

    def _hash_kontrol(self):
        if not self.hash_modu:
            raise RuntimeError("Hash modulu aktif degil. 'kullan hash' komutunu ekleyin.")

    # --- BASE64 ---

    def b64_sifrele(self, satir):
        """
        b64_sifrele <degisken_adi> <metin_ifadesi>
        Metni Base64 ile şifreler, sonucu değişkene atar.
        Örnek: b64_sifrele sonuc "Merhaba Dunya"
        """
        self._sifrele_kontrol()
        govde = satir[len('b64_sifrele '):].strip()
        parcalar = parse_qt_command(govde)
        degisken_adi = parcalar[0]
        metin = self.ifade_hesapla(parcalar[1])
        if isinstance(metin, bytes):
            ham = metin
        else:
            ham = str(metin).encode('utf-8')
        sonuc = base64.b64encode(ham).decode('utf-8')
        self.degiskenler[degisken_adi] = sonuc

    def b64_coz(self, satir):
        """
        b64_coz <degisken_adi> <b64_metin_ifadesi>
        Base64 şifreli metni çözer.
        Örnek: b64_coz acik sifreli_metin
        """
        self._sifrele_kontrol()
        govde = satir[len('b64_coz '):].strip()
        parcalar = parse_qt_command(govde)
        degisken_adi = parcalar[0]
        sifreli = self.ifade_hesapla(parcalar[1])
        try:
            if isinstance(sifreli, bytes):
                ham = sifreli
            else:
                ham = str(sifreli).encode('utf-8')
            sonuc = base64.b64decode(ham).decode('utf-8')
            self.degiskenler[degisken_adi] = sonuc
        except Exception as e:
            print(f"Base64 cozme hatasi: {e}")
            self.degiskenler[degisken_adi] = None

    # --- XOR Şifreleme ---

    def _xor_isle(self, veri: bytes, anahtar: bytes) -> bytes:
        """Veriyi XOR ile işler - hem şifreleme hem çözme için."""
        anahtar_uzun = len(anahtar)
        return bytes(veri[i] ^ anahtar[i % anahtar_uzun] for i in range(len(veri)))

    def xor_sifrele(self, satir):
        """
        xor_sifrele <degisken_adi> <metin> <anahtar>
        Metni XOR + Base64 ile şifreler (anahtar ile).
        Örnek: xor_sifrele sifreli "gizli mesaj" "benim_anahtarim"
        """
        self._sifrele_kontrol()
        govde = satir[len('xor_sifrele '):].strip()
        parcalar = parse_qt_command(govde)
        degisken_adi = parcalar[0]
        metin = str(self.ifade_hesapla(parcalar[1])).encode('utf-8')
        anahtar = str(self.ifade_hesapla(parcalar[2])).encode('utf-8')
        if not anahtar:
            print("Hata: Anahtar bos olamaz.")
            return
        # XOR uygula
        xor_sonuc = self._xor_isle(metin, anahtar)
        # Base64 ile kodla (taşınabilirlik için)
        b64_sonuc = base64.b64encode(xor_sonuc).decode('utf-8')
        self.degiskenler[degisken_adi] = b64_sonuc

    def xor_coz(self, satir):
        """
        xor_coz <degisken_adi> <sifreli_metin> <anahtar>
        XOR + Base64 şifreli metni çözer.
        Örnek: xor_coz acik sifreli "benim_anahtarim"
        """
        self._sifrele_kontrol()
        govde = satir[len('xor_coz '):].strip()
        parcalar = parse_qt_command(govde)
        degisken_adi = parcalar[0]
        sifreli = str(self.ifade_hesapla(parcalar[1]))
        anahtar = str(self.ifade_hesapla(parcalar[2])).encode('utf-8')
        if not anahtar:
            print("Hata: Anahtar bos olamaz.")
            return
        try:
            # Base64 çöz
            xor_veri = base64.b64decode(sifreli.encode('utf-8'))
            # XOR ile geri al
            acik = self._xor_isle(xor_veri, anahtar).decode('utf-8')
            self.degiskenler[degisken_adi] = acik
        except Exception as e:
            print(f"XOR cozme hatasi: {e}")
            self.degiskenler[degisken_adi] = None

    # --- Dosya Şifreleme ---

    def dosya_sifrele(self, satir):
        """
        dosya_sifrele <kaynak_dosya> <hedef_dosya> <anahtar>
        Dosyayı XOR+Base64 ile şifreler.
        Örnek: dosya_sifrele "belge.txt" "belge.enc" "sifre123"
        """
        self._sifrele_kontrol()
        govde = satir[len('dosya_sifrele '):].strip()
        parcalar = parse_qt_command(govde)
        kaynak = str(self.ifade_hesapla(parcalar[0]))
        hedef  = str(self.ifade_hesapla(parcalar[1]))
        anahtar = str(self.ifade_hesapla(parcalar[2])).encode('utf-8')
        try:
            with open(kaynak, 'rb') as f:
                veri = f.read()
            sifreli = self._xor_isle(veri, anahtar)
            b64 = base64.b64encode(sifreli)
            with open(hedef, 'wb') as f:
                f.write(b64)
            print(f"Dosya sifrelendi: {kaynak} -> {hedef}")
        except Exception as e:
            print(f"Dosya sifreleme hatasi: {e}")

    def dosya_coz(self, satir):
        """
        dosya_coz <kaynak_dosya> <hedef_dosya> <anahtar>
        Şifreli dosyayı çözer.
        Örnek: dosya_coz "belge.enc" "belge_acik.txt" "sifre123"
        """
        self._sifrele_kontrol()
        govde = satir[len('dosya_coz '):].strip()
        parcalar = parse_qt_command(govde)
        kaynak  = str(self.ifade_hesapla(parcalar[0]))
        hedef   = str(self.ifade_hesapla(parcalar[1]))
        anahtar = str(self.ifade_hesapla(parcalar[2])).encode('utf-8')
        try:
            with open(kaynak, 'rb') as f:
                b64 = f.read()
            xor_veri = base64.b64decode(b64)
            acik = self._xor_isle(xor_veri, anahtar)
            with open(hedef, 'wb') as f:
                f.write(acik)
            print(f"Dosya cozuldu: {kaynak} -> {hedef}")
        except Exception as e:
            print(f"Dosya cozme hatasi: {e}")

    def sifreli_dosya_yaz(self, satir):
        """
        sifreli_yaz <dosya_yolu> <icerik> <anahtar>
        Metni şifreleyerek dosyaya yazar.
        Örnek: sifreli_yaz "gizli.enc" "bu gizli bir mesaj" "anahtar"
        """
        self._sifrele_kontrol()
        govde = satir[len('sifreli_yaz '):].strip()
        parcalar = parse_qt_command(govde)
        dosya   = str(self.ifade_hesapla(parcalar[0]))
        icerik  = str(self.ifade_hesapla(parcalar[1])).encode('utf-8')
        anahtar = str(self.ifade_hesapla(parcalar[2])).encode('utf-8')
        try:
            sifreli = self._xor_isle(icerik, anahtar)
            b64 = base64.b64encode(sifreli)
            with open(dosya, 'wb') as f:
                f.write(b64)
            print(f"Sifreli dosya yazildi: {dosya}")
        except Exception as e:
            print(f"Sifreli yazma hatasi: {e}")

    def sifreli_dosya_oku(self, satir):
        """
        sifreli_oku <degisken_adi> <dosya_yolu> <anahtar>
        Şifreli dosyayı okur ve çözer.
        Örnek: sifreli_oku icerik "gizli.enc" "anahtar"
        """
        self._sifrele_kontrol()
        govde = satir[len('sifreli_oku '):].strip()
        parcalar = parse_qt_command(govde)
        degisken_adi = parcalar[0]
        dosya   = str(self.ifade_hesapla(parcalar[1]))
        anahtar = str(self.ifade_hesapla(parcalar[2])).encode('utf-8')
        try:
            with open(dosya, 'rb') as f:
                b64 = f.read()
            xor_veri = base64.b64decode(b64)
            acik = self._xor_isle(xor_veri, anahtar).decode('utf-8')
            self.degiskenler[degisken_adi] = acik
        except Exception as e:
            print(f"Sifreli okuma hatasi: {e}")
            self.degiskenler[degisken_adi] = None

    # ==================== HASH ====================

    def sha256_hesapla(self, satir):
        """
        sha256 <degisken_adi> <metin_ifadesi>
        SHA-256 hash hesaplar.
        Örnek: sha256 hash_sonuc "sifre123"
        """
        self._hash_kontrol()
        govde = satir[len('sha256 '):].strip()
        parcalar = parse_qt_command(govde)
        degisken_adi = parcalar[0]
        metin = str(self.ifade_hesapla(parcalar[1]))
        sonuc = hashlib.sha256(metin.encode('utf-8')).hexdigest()
        self.degiskenler[degisken_adi] = sonuc

    def sha512_hesapla(self, satir):
        """
        sha512 <degisken_adi> <metin_ifadesi>
        SHA-512 hash hesaplar.
        Örnek: sha512 hash_sonuc "sifre123"
        """
        self._hash_kontrol()
        govde = satir[len('sha512 '):].strip()
        parcalar = parse_qt_command(govde)
        degisken_adi = parcalar[0]
        metin = str(self.ifade_hesapla(parcalar[1]))
        sonuc = hashlib.sha512(metin.encode('utf-8')).hexdigest()
        self.degiskenler[degisken_adi] = sonuc

    def md5_hesapla(self, satir):
        """
        md5 <degisken_adi> <metin_ifadesi>
        MD5 hash hesaplar (sadece kontrol amaçlı, güvenli değil).
        Örnek: md5 hash_sonuc "kontrol_metni"
        """
        self._hash_kontrol()
        govde = satir[len('md5 '):].strip()
        parcalar = parse_qt_command(govde)
        degisken_adi = parcalar[0]
        metin = str(self.ifade_hesapla(parcalar[1]))
        sonuc = hashlib.md5(metin.encode('utf-8')).hexdigest()
        self.degiskenler[degisken_adi] = sonuc

    def sha1_hesapla(self, satir):
        """
        sha1 <degisken_adi> <metin_ifadesi>
        SHA-1 hash hesaplar.
        Örnek: sha1 hash_sonuc "metin"
        """
        self._hash_kontrol()
        govde = satir[len('sha1 '):].strip()
        parcalar = parse_qt_command(govde)
        degisken_adi = parcalar[0]
        metin = str(self.ifade_hesapla(parcalar[1]))
        sonuc = hashlib.sha1(metin.encode('utf-8')).hexdigest()
        self.degiskenler[degisken_adi] = sonuc

    def dosya_sha256(self, satir):
        """
        dosya_sha256 <degisken_adi> <dosya_yolu>
        Bir dosyanın SHA-256 hash'ini hesaplar.
        Örnek: dosya_sha256 dosya_hash "program.exe"
        """
        self._hash_kontrol()
        govde = satir[len('dosya_sha256 '):].strip()
        parcalar = parse_qt_command(govde)
        degisken_adi = parcalar[0]
        dosya = str(self.ifade_hesapla(parcalar[1]))
        try:
            h = hashlib.sha256()
            with open(dosya, 'rb') as f:
                while True:
                    blok = f.read(65536)  # 64KB blok
                    if not blok:
                        break
                    h.update(blok)
            self.degiskenler[degisken_adi] = h.hexdigest()
        except Exception as e:
            print(f"Dosya SHA256 hatasi: {e}")
            self.degiskenler[degisken_adi] = None

    def hmac_hesapla(self, satir):
        """
        hmac_hesapla <degisken_adi> <anahtar> <metin>
        HMAC-SHA256 mesaj doğrulama kodu üretir.
        Örnek: hmac_hesapla sonuc "gizli_anahtar" "dogrulanacak_mesaj"
        """
        self._hash_kontrol()
        govde = satir[len('hmac_hesapla '):].strip()
        parcalar = parse_qt_command(govde)
        degisken_adi = parcalar[0]
        anahtar = str(self.ifade_hesapla(parcalar[1])).encode('utf-8')
        metin   = str(self.ifade_hesapla(parcalar[2])).encode('utf-8')
        sonuc = hmac.new(anahtar, metin, hashlib.sha256).hexdigest()
        self.degiskenler[degisken_adi] = sonuc

    def hash_dogrula(self, satir):
        """
        hash_dogrula <degisken_adi> <metin> <beklenen_hash> [algoritma]
        Hash doğrular - dogru/yanlis döner.
        Algoritma: sha256 (varsayılan), sha512, md5, sha1
        Örnek: hash_dogrula sonuc "sifre123" beklenen_hash "sha256"
        """
        self._hash_kontrol()
        govde = satir[len('hash_dogrula '):].strip()
        parcalar = parse_qt_command(govde)
        degisken_adi = parcalar[0]
        metin        = str(self.ifade_hesapla(parcalar[1]))
        beklenen     = str(self.ifade_hesapla(parcalar[2]))
        algoritma    = str(self.ifade_hesapla(parcalar[3])) if len(parcalar) > 3 else 'sha256'
        algo_map = {
            'sha256': hashlib.sha256,
            'sha512': hashlib.sha512,
            'md5':    hashlib.md5,
            'sha1':   hashlib.sha1,
        }
        if algoritma not in algo_map:
            print(f"Bilinmeyen algoritma: {algoritma}. Secenekler: sha256, sha512, md5, sha1")
            self.degiskenler[degisken_adi] = False
            return
        hesaplanan = algo_map[algoritma](metin.encode('utf-8')).hexdigest()
        # Sabit zamanlı karşılaştırma (timing attack'e karşı)
        eslesme = hmac.compare_digest(hesaplanan, beklenen)
        self.degiskenler[degisken_adi] = eslesme


class ReturnException(Exception):
    def __init__(self, deger=None):
        self.deger = deger

class BreakException(Exception):
    pass

class ContinueException(Exception):
    pass

if __name__ == "__main__":
    tsharp = TSharp()
    try:
        if len(sys.argv) > 1:
            tsharp.calistir(sys.argv[1])
        else:
            # İnteraktif mod zaten kendi içinde döngüye sahip
            tsharp.interaktif_mod()
    except (KeyboardInterrupt, EOFError):
        print("\nTSharp kapatılıyor...")
        sys.exit(0)
    except Exception as e:
        # traceback yerine daha temiz bir hata mesajı
        print(f"Sistem Hatası: {e}")
        sys.exit(1)
