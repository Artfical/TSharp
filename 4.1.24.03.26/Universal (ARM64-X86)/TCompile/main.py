import os
import sys
import subprocess
import argparse
import shutil

def derle():
    parser = argparse.ArgumentParser(description="TSharp Paketleme Aracı")
    parser.add_argument("dosya", help="Derlenecek .tsh dosyası")
    parser.add_argument("--GUI", action="store_true", help="Konsol penceresini gizler")
    parser.add_argument("--tekdosya", action="store_true", help="Tek bir exe oluşturur")
    parser.add_argument("--ekle", action="append", help="Pakete eklenecek dosyalar (Örn: resim.png)")
    
    args = parser.parse_args()

    if not os.path.exists(args.dosya):
        print(f"Hata: {args.dosya} bulunamadı.")
        return

    ana_dosya = os.path.abspath(args.dosya)
    motor_dosya = os.path.abspath("1.py")
    
    if not os.path.exists(motor_dosya):
        print("Hata: 1.py motor dosyası bulunamadı.")
        return

    # Geçici giriş scripti oluştur (Görünmez Bootstrapper)
    giris_scripti = "_tsharp_entry_.py"
    with open(giris_scripti, "w", encoding="utf-8") as f:
        f.write(f"""
import sys
import os
from motor import TSharp

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

if __name__ == "__main__":
    t = TSharp()
    t.calistir(resource_path("{os.path.basename(ana_dosya)}"))
""")

    # PyInstaller komutunu hazırla
    komut = [
        "pyinstaller",
        "--clean",
        "--noconfirm",
        f"--name={os.path.splitext(os.path.basename(ana_dosya))[0]}",
        f"--add-data={ana_dosya}{os.pathsep}." 
    ]

    # Motoru modül olarak ekle
    shutil.copy(motor_dosya, "motor.py")
    komut.append(f"--add-data=motor.py{os.pathsep}.")

    if args.tekdosya:
        komut.append("--onefile")
    
    if args.GUI:
        komut.append("--windowed")
    else:
        komut.append("--nowindowed")

    # Ek dosyaları dahil et
    if args.ekle:
        for dosya in args.ekle:
            if os.path.exists(dosya):
                komut.append(f"--add-data={os.path.abspath(dosya)}{os.pathsep}.")
            else:
                print(f"Uyarı: Ek dosya bulunamadı: {dosya}")

    komut.append(giris_scripti)

    # Sessizce çalıştır
    print("İşlem başlatıldı...")
    try:
        subprocess.run(komut, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        cikti_yolu = os.path.abspath("dist")
        print(f"Tamamlandı. Çıktı klasörü: {cikti_yolu}")
    except Exception as e:
        print(f"Hata oluştu: {e}")
    finally:
        # Temizlik
        for temp in [giris_scripti, "motor.py", "motor.py.spec", f"{os.path.splitext(os.path.basename(ana_dosya))[0]}.spec"]:
            if os.path.exists(temp):
                try: os.remove(temp)
                except: pass

if __name__ == "__main__":
    derle()
