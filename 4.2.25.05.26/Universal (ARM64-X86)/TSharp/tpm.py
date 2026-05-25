#!/usr/bin/env python3
"""
TPM - T-Sharp Paket Yoneticisi v1.0
Paket formati: .tpm (ZIP arsivi, icinde paket.json + *.py dosyalari)

Kullanim:
  python tpm.py yukle   <paket>   - Paketi indir ve kur
  python tpm.py kaldir  <paket>   - Paketi kaldir
  python tpm.py listele           - Kurulu paketleri goster
  python tpm.py ara     <sorgu>   - Kayit defterinde ara
  python tpm.py bilgi   <paket>   - Paket bilgisi goster
  python tpm.py guncelle [paket]  - Paket(ler)i guncelle
  python tpm.py baslat  <isim>    - Yeni paket projesi olustur
  python tpm.py yayinla           - Mevcut paketi .tpm olarak pakelle
"""

import sys
import os
import json
import zipfile
import shutil
import hashlib
import urllib.request
import urllib.error
from pathlib import Path

# ==================== SABITLER ====================

SURUM = "1.0.0"
TSHARP_SURUM = "4.2"

TSHARP_DIZINI = Path.home() / ".tsharp"
PAKET_DIZINI = TSHARP_DIZINI / "paketler"
ONBELLEK_DIZINI = TSHARP_DIZINI / "onbellek"

KAYIT_DEFTERI_URL = (
    "https://raw.githubusercontent.com/Artfical/TSharp/main/registry/paketler.json"
)
KAYIT_DEFTERI_YEREL = TSHARP_DIZINI / "paketler.json"

RENK = {
    "yesil":   "\033[92m",
    "kirmizi": "\033[91m",
    "sari":    "\033[93m",
    "mavi":    "\033[94m",
    "beyaz":   "\033[0m",
    "kalin":   "\033[1m",
}


def renkli(metin, renk):
    if sys.platform == "win32" and not os.environ.get("ANSICON"):
        return metin
    return f"{RENK.get(renk, '')}{metin}{RENK['beyaz']}"


def baslik():
    print(renkli(f"\n  TPM - T-Sharp Paket Yoneticisi v{SURUM}", "kalin"))
    print(renkli("  " + "─" * 46, "mavi"))


def dizinleri_olustur():
    PAKET_DIZINI.mkdir(parents=True, exist_ok=True)
    ONBELLEK_DIZINI.mkdir(parents=True, exist_ok=True)


# ==================== KAYIT DEFTERI ====================

def kayit_defteri_guncelle(sessiz=False):
    if not sessiz:
        print(renkli("  Kayit defteri guncelleniyor...", "sari"))
    try:
        req = urllib.request.Request(
            KAYIT_DEFTERI_URL,
            headers={"User-Agent": f"TPM/{SURUM} TSharp/{TSHARP_SURUM}"},
        )
        with urllib.request.urlopen(req, timeout=10) as r:
            veri = r.read()
        KAYIT_DEFTERI_YEREL.write_bytes(veri)
        if not sessiz:
            print(renkli("  Kayit defteri guncellendi.", "yesil"))
        return True
    except Exception as e:
        if not sessiz:
            print(renkli(f"  Uyari: Kayit defteri guncellenemedi: {e}", "sari"))
        return False


def kayit_defteri_oku():
    if not KAYIT_DEFTERI_YEREL.exists():
        kayit_defteri_guncelle(sessiz=True)
    if not KAYIT_DEFTERI_YEREL.exists():
        return {}
    try:
        return json.loads(KAYIT_DEFTERI_YEREL.read_text(encoding="utf-8"))
    except Exception:
        return {}


# ==================== KURULU PAKET BILGISI ====================

def kurulu_paket_bilgisi(paket_adi):
    manifest = PAKET_DIZINI / paket_adi / "paket.json"
    if not manifest.exists():
        return None
    try:
        return json.loads(manifest.read_text(encoding="utf-8"))
    except Exception:
        return None


def kurulu_paketler():
    if not PAKET_DIZINI.exists():
        return []
    return [
        d.name
        for d in PAKET_DIZINI.iterdir()
        if d.is_dir() and (d / "paket.json").exists()
    ]


# ==================== .TPM DOSYASINI AC ====================

def tpm_dosyasini_kur(tpm_yolu, paket_adi):
    """
    .tpm dosyasini (ZIP arsivi) acar ve ~/.tsharp/paketler/<paket_adi>/ altina kurar.
    Beklenen icerik:
      paket.json          - metadata
      <paket_adi>.py      - ana Python modulu (TSHARP_FONKSIYONLAR icermelidir)
      diger .py dosyalari - varsa yardimci moduller
    """
    hedef = PAKET_DIZINI / paket_adi
    if hedef.exists():
        shutil.rmtree(hedef)
    hedef.mkdir(parents=True)

    with zipfile.ZipFile(tpm_yolu, "r") as zf:
        icerik = zf.namelist()
        # Guvenlik: path traversal engeli
        for dosya in icerik:
            if dosya.startswith("/") or ".." in dosya:
                raise ValueError(f"Guvenli olmayan dosya yolu: {dosya}")
        zf.extractall(hedef)

    # paket.json var mi kontrol et
    if not (hedef / "paket.json").exists():
        shutil.rmtree(hedef)
        raise ValueError(".tpm icinde paket.json bulunamadi.")

    # Ana Python modulu var mi kontrol et
    ana_py = hedef / f"{paket_adi}.py"
    if not ana_py.exists():
        # Belki farkli isimli tek bir .py var?
        py_dosyalari = list(hedef.glob("*.py"))
        if not py_dosyalari:
            shutil.rmtree(hedef)
            raise ValueError(f".tpm icinde {paket_adi}.py bulunamadi.")


# ==================== KOMUTLAR ====================

def komut_yukle(paket_adi):
    baslik()
    dizinleri_olustur()
    kayit_defteri_guncelle(sessiz=True)
    kayit = kayit_defteri_oku()

    if paket_adi not in kayit:
        print(renkli(f"  Hata: '{paket_adi}' kayit defterinde bulunamadi.", "kirmizi"))
        print(renkli(f"  Arama icin: python tpm.py ara {paket_adi}", "sari"))
        sys.exit(1)

    bilgi = kayit[paket_adi]
    surum = bilgi.get("surum", "?")

    mevcut = kurulu_paket_bilgisi(paket_adi)
    if mevcut and mevcut.get("surum") == surum:
        print(renkli(f"  '{paket_adi}' v{surum} zaten kurulu.", "yesil"))
        return

    indirme_url = bilgi.get("indirme_url", "")
    if not indirme_url:
        print(renkli("  Hata: Kayit defterinde indirme adresi yok.", "kirmizi"))
        sys.exit(1)

    dosya_adi = indirme_url.split("/")[-1]
    print(renkli(f"  Indiriliyor: {dosya_adi}  [{paket_adi} v{surum}]", "mavi"))

    tpm_yolu = ONBELLEK_DIZINI / dosya_adi
    try:
        req = urllib.request.Request(
            indirme_url,
            headers={"User-Agent": f"TPM/{SURUM} TSharp/{TSHARP_SURUM}"},
        )
        with urllib.request.urlopen(req, timeout=30) as r:
            tpm_yolu.write_bytes(r.read())
    except urllib.error.URLError as e:
        print(renkli(f"  Hata: Indirme basarisiz: {e}", "kirmizi"))
        sys.exit(1)

    # SHA256 dogrulama
    beklenen_sha = bilgi.get("sha256", "")
    if beklenen_sha:
        gercek_sha = hashlib.sha256(tpm_yolu.read_bytes()).hexdigest()
        if gercek_sha != beklenen_sha:
            tpm_yolu.unlink(missing_ok=True)
            print(renkli("  Hata: SHA256 eslesmedi. Dosya bozuk olabilir.", "kirmizi"))
            sys.exit(1)

    try:
        tpm_dosyasini_kur(tpm_yolu, paket_adi)
    except (ValueError, zipfile.BadZipFile) as e:
        print(renkli(f"  Hata: Paket acilirken sorun: {e}", "kirmizi"))
        sys.exit(1)

    print(renkli(f"  '{paket_adi}' v{surum} basariyla kuruldu!", "yesil"))
    aciklama = bilgi.get("aciklama", "")
    if aciklama:
        print(f"  {aciklama}")
    github = bilgi.get("github", "")
    if github:
        print(renkli(f"  GitHub: {github}", "mavi"))


def komut_kaldir(paket_adi):
    baslik()
    hedef = PAKET_DIZINI / paket_adi
    if not hedef.exists():
        print(renkli(f"  '{paket_adi}' zaten kurulu degil.", "sari"))
        return
    shutil.rmtree(hedef)
    print(renkli(f"  '{paket_adi}' kaldirildi.", "yesil"))


def komut_listele():
    baslik()
    dizinleri_olustur()
    paketler = kurulu_paketler()
    if not paketler:
        print(renkli("  Hic kurulu paket yok.", "sari"))
        print(renkli("  Kesfetmek icin: python tpm.py ara <sorgu>", "mavi"))
        return
    print(renkli(f"  Kurulu paketler ({len(paketler)}):\n", "kalin"))
    for p in sorted(paketler):
        bilgi = kurulu_paket_bilgisi(p)
        if bilgi:
            surum = bilgi.get("surum", "?")
            aciklama = bilgi.get("aciklama", "")
            yazar = bilgi.get("yazar", "")
            print(f"    {renkli(p, 'yesil')} v{surum}  —  {aciklama}  ({yazar})")
        else:
            print(f"    {renkli(p, 'yesil')}")


def komut_ara(sorgu):
    baslik()
    kayit_defteri_guncelle(sessiz=True)
    kayit = kayit_defteri_oku()
    if not kayit:
        print(renkli("  Kayit defteri bos veya erisilemiyor.", "kirmizi"))
        return
    sorgu_kucuk = sorgu.lower()
    sonuclar = [
        (isim, bilgi)
        for isim, bilgi in kayit.items()
        if sorgu_kucuk in isim.lower()
        or sorgu_kucuk in bilgi.get("aciklama", "").lower()
        or sorgu_kucuk in bilgi.get("yazar", "").lower()
    ]
    if not sonuclar:
        print(renkli(f"  '{sorgu}' icin sonuc bulunamadi.", "sari"))
        return
    print(renkli(f"  '{sorgu}' icin {len(sonuclar)} sonuc:\n", "kalin"))
    for isim, bilgi in sorted(sonuclar):
        surum = bilgi.get("surum", "?")
        aciklama = bilgi.get("aciklama", "")
        yazar = bilgi.get("yazar", "")
        github = bilgi.get("github", "")
        kurulu = renkli("  [kurulu]", "yesil") if (PAKET_DIZINI / isim).exists() else ""
        print(f"    {renkli(isim, 'yesil')} v{surum}{kurulu}")
        print(f"      {aciklama}")
        print(f"      Yazar: {yazar}  |  {github}")


def komut_bilgi(paket_adi):
    baslik()
    kayit_defteri_guncelle(sessiz=True)
    kayit = kayit_defteri_oku()
    yerel = kurulu_paket_bilgisi(paket_adi)
    uzak = kayit.get(paket_adi, {})

    if not yerel and not uzak:
        print(renkli(f"  '{paket_adi}' bulunamadi.", "kirmizi"))
        return

    kaynak = yerel or uzak
    print(renkli(f"  {paket_adi}", "kalin"))
    print(f"  Surum:       {kaynak.get('surum', '?')}")
    print(f"  Aciklama:    {kaynak.get('aciklama', '')}")
    print(f"  Yazar:       {kaynak.get('yazar', '')}")
    print(f"  GitHub:      {kaynak.get('github', 'yok')}")
    print(f"  TSharp:      {kaynak.get('tsharp_surum', '?')}")
    bagimliliklar = kaynak.get("bagimliliklar", {})
    print(f"  Bagimlilik:  {', '.join(bagimliliklar.keys()) or 'yok'}")
    durum = renkli("kurulu", "yesil") if yerel else renkli("kurulu degil", "sari")
    print(f"  Durum:       {durum}")
    if uzak and yerel and uzak.get("surum") != yerel.get("surum"):
        print(renkli(f"\n  ! Guncelleme mevcut: v{uzak.get('surum')}", "sari"))
        print(renkli(f"    python tpm.py guncelle {paket_adi}", "mavi"))


def komut_guncelle(paket_adi=None):
    baslik()
    kayit_defteri_guncelle(sessiz=True)
    kayit = kayit_defteri_oku()
    hedefler = [paket_adi] if paket_adi else kurulu_paketler()
    guncellenen = 0
    for p in hedefler:
        yerel = kurulu_paket_bilgisi(p)
        uzak = kayit.get(p, {})
        if yerel and uzak and yerel.get("surum") != uzak.get("surum"):
            print(renkli(f"  {p}: v{yerel.get('surum')} -> v{uzak.get('surum')}", "mavi"))
            komut_yukle(p)
            guncellenen += 1
    if guncellenen == 0:
        print(renkli("  Tum paketler guncel.", "yesil"))


def komut_baslat(paket_adi):
    baslik()
    hedef = Path(paket_adi)
    if hedef.exists():
        print(renkli(f"  Hata: '{paket_adi}' klasoru zaten var.", "kirmizi"))
        sys.exit(1)
    hedef.mkdir()

    manifest = {
        "isim": paket_adi,
        "surum": "1.0.0",
        "aciklama": f"{paket_adi} paketi",
        "yazar": "",
        "github": "",
        "tsharp_surum": f">={TSHARP_SURUM}",
        "bagimliliklar": {},
    }
    (hedef / "paket.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    # Ana Python modulu - sablonu
    py_kodu = f'''# {paket_adi} - TSharp {TSHARP_SURUM} uyumlu paket
# Bu dosya TSharp interpreter tarafindan yuklenecek
# TSHARP_FONKSIYONLAR: {{fonk_adi: callable(args) -> deger}}

# args = T# tarafindan gecilen arguman listesi
# Ornek: faktoriyel(5) cagrilirsa args = [5]

TSHARP_FONKSIYONLAR = {{
    "merhaba": lambda args: f"Merhaba {{args[0]}}!" if args else "Merhaba!",
    # Buraya kendi fonksiyonlarinizi ekleyin
}}
'''
    (hedef / f"{paket_adi}.py").write_text(py_kodu, encoding="utf-8")

    print(renkli(f"  '{paket_adi}' paketi olusturuldu!", "yesil"))
    print(f"  Klasor:   {hedef.resolve()}")
    print(f"  Manifest: {hedef / 'paket.json'}")
    print(f"  Kod:      {hedef / (paket_adi + '.py')}")
    print()
    print(renkli("  T# kullanimi: kullan " + paket_adi, "mavi"))
    print(renkli("  Yayinlamak icin: python tpm.py yayinla", "sari"))


def komut_yayinla():
    baslik()
    manifest_yolu = Path("paket.json")
    if not manifest_yolu.exists():
        print(renkli("  Hata: Bu dizinde paket.json bulunamadi.", "kirmizi"))
        print(renkli("  Once: python tpm.py baslat <paket_adi>", "sari"))
        sys.exit(1)

    manifest = json.loads(manifest_yolu.read_text(encoding="utf-8"))
    isim = manifest.get("isim", "?")
    surum = manifest.get("surum", "?")

    # Python dosyalari var mi?
    py_dosyalari = list(Path(".").glob("*.py"))
    if not py_dosyalari:
        print(renkli("  Hata: Hic .py dosyasi bulunamadi.", "kirmizi"))
        sys.exit(1)

    tpm_adi = f"{isim}-{surum}.tpm"
    with zipfile.ZipFile(tpm_adi, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.write(manifest_yolu, "paket.json")
        for dosya in py_dosyalari:
            zf.write(dosya, dosya.name)
        # Varsa README ve LICENSE ekle
        for ekstra in ["README.md", "LICENSE", "LISANS"]:
            if Path(ekstra).exists():
                zf.write(ekstra)

    sha256 = hashlib.sha256(Path(tpm_adi).read_bytes()).hexdigest()

    print(renkli(f"  '{isim}' v{surum} paketlendi: {tpm_adi}", "yesil"))
    print(f"  SHA256: {sha256}")
    print()
    print(renkli("  Yayinlamak icin adimlar:", "kalin"))
    print(f"  1. {tpm_adi} dosyasini su yola yukleyin:")
    print(f"     registry/paketler/{tpm_adi}")
    print(f"  2. registry/paketler.json'a su girisi ekleyin:")
    giris = {
        isim: {
            "surum": surum,
            "aciklama": manifest.get("aciklama", ""),
            "yazar": manifest.get("yazar", ""),
            "github": manifest.get("github", ""),
            "tsharp_surum": manifest.get("tsharp_surum", f">={TSHARP_SURUM}"),
            "indirme_url": f"https://raw.githubusercontent.com/Artfical/TSharp/main/registry/paketler/{tpm_adi}",
            "sha256": sha256,
            "bagimliliklar": manifest.get("bagimliliklar", {}),
        }
    }
    print(json.dumps(giris, ensure_ascii=False, indent=2))
    print(renkli("  3. GitHub'a Pull Request gonder.", "mavi"))


# ==================== YARDIM ====================

def yardim():
    baslik()
    print(f"""
  Paket formati: .tpm  (ZIP arsivi: paket.json + *.py)
  Python modulu: TSHARP_FONKSIYONLAR = {{"fonk": callable(args)}}

  Komutlar:
    yukle   <paket>    .tpm indir, ac, kur
    kaldir  <paket>    Kurulu paketi kaldir
    listele            Kurulu paketleri goster
    ara     <sorgu>    Kayit defterinde ara
    bilgi   <paket>    Paket detaylarini goster
    guncelle [paket]   Paket(ler)i guncelle
    baslat  <isim>     Yeni paket projesi olustur
    yayinla            .tpm olustur + kayit girisi hazirla

  Ornekler:
    python tpm.py yukle matematik
    python tpm.py ara   fizik
    python tpm.py bilgi matematik
    python tpm.py baslat benim-paketim
""")


# ==================== GIRIS NOKTASI ====================

def main():
    if len(sys.argv) < 2:
        yardim()
        sys.exit(0)

    komut = sys.argv[1].lower()

    donusum = {
        "yükle": "yukle",   "yukle": "yukle",
        "kaldır": "kaldir", "kaldir": "kaldir",
        "güncelle": "guncelle", "guncelle": "guncelle",
        "başlat": "baslat", "baslat": "baslat",
        "yayınla": "yayinla", "yayinla": "yayinla",
        "listele": "listele", "ara": "ara",
        "bilgi": "bilgi",
        "yardim": "yardim", "yardım": "yardim", "help": "yardim",
    }
    komut = donusum.get(komut, komut)

    if komut == "yukle":
        if len(sys.argv) < 3:
            print(renkli("  Kullanim: python tpm.py yukle <paket>", "kirmizi"))
            sys.exit(1)
        komut_yukle(sys.argv[2])
    elif komut == "kaldir":
        if len(sys.argv) < 3:
            print(renkli("  Kullanim: python tpm.py kaldir <paket>", "kirmizi"))
            sys.exit(1)
        komut_kaldir(sys.argv[2])
    elif komut == "listele":
        komut_listele()
    elif komut == "ara":
        if len(sys.argv) < 3:
            print(renkli("  Kullanim: python tpm.py ara <sorgu>", "kirmizi"))
            sys.exit(1)
        komut_ara(sys.argv[2])
    elif komut == "bilgi":
        if len(sys.argv) < 3:
            print(renkli("  Kullanim: python tpm.py bilgi <paket>", "kirmizi"))
            sys.exit(1)
        komut_bilgi(sys.argv[2])
    elif komut == "guncelle":
        paket = sys.argv[2] if len(sys.argv) >= 3 else None
        komut_guncelle(paket)
    elif komut == "baslat":
        if len(sys.argv) < 3:
            print(renkli("  Kullanim: python tpm.py baslat <paket>", "kirmizi"))
            sys.exit(1)
        komut_baslat(sys.argv[2])
    elif komut == "yayinla":
        komut_yayinla()
    else:
        print(renkli(f"  Bilinmeyen komut: '{komut}'", "kirmizi"))
        yardim()
        sys.exit(1)


if __name__ == "__main__":
    main()
