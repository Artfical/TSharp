#!/usr/bin/env python3
"""
TPM - T-Sharp Paket Yoneticisi v1.0
Kullanim:
  python tpm.py yukle   <paket>   - Paketi indir ve kur
  python tpm.py kaldir  <paket>   - Paketi kaldir
  python tpm.py listele           - Kurulu paketleri goster
  python tpm.py ara     <sorgu>   - Kayit defterinde ara
  python tpm.py bilgi   <paket>   - Paket bilgisi goster
  python tpm.py guncelle [paket]  - Paket(ler)i guncelle
  python tpm.py baslat  <isim>    - Yeni paket projesi olustur
  python tpm.py yayinla           - Mevcut paketi yayinla (GitHub PR)
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
    "yesil":  "\033[92m",
    "kirmizi": "\033[91m",
    "sari":   "\033[93m",
    "mavi":   "\033[94m",
    "beyaz":  "\033[0m",
    "kalin":  "\033[1m",
}


def renkli(metin, renk):
    if sys.platform == "win32" and not os.environ.get("ANSICON"):
        return metin
    return f"{RENK.get(renk, '')}{metin}{RENK['beyaz']}"


def baslik():
    print(renkli(f"\n  TPM - T-Sharp Paket Yoneticisi v{SURUM} (TSharp {TSHARP_SURUM})", "kalin"))
    print(renkli("  " + "─" * 48, "mavi"))


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


# ==================== KOMUTLAR ====================

def komut_yukle(paket_adi):
    baslik()
    dizinleri_olustur()
    kayit_defteri_guncelle(sessiz=True)
    kayit = kayit_defteri_oku()

    if paket_adi not in kayit:
        print(renkli(f"  Hata: '{paket_adi}' paketi kayit defterinde bulunamadi.", "kirmizi"))
        print(renkli(f"  Arama icin: python tpm.py ara {paket_adi}", "sari"))
        sys.exit(1)

    bilgi = kayit[paket_adi]
    surum = bilgi.get("surum", "?")

    mevcut = kurulu_paket_bilgisi(paket_adi)
    if mevcut and mevcut.get("surum") == surum:
        print(renkli(f"  '{paket_adi}' v{surum} zaten kurulu.", "yesil"))
        return

    print(renkli(f"  Indiriliyor: {paket_adi} v{surum}...", "mavi"))

    indirme_url = bilgi.get("indirme_url", "")
    if not indirme_url:
        print(renkli("  Hata: Indirme adresi bulunamadi.", "kirmizi"))
        sys.exit(1)

    zip_yolu = ONBELLEK_DIZINI / f"{paket_adi}-{surum}.zip"
    try:
        req = urllib.request.Request(
            indirme_url,
            headers={"User-Agent": f"TPM/{SURUM} TSharp/{TSHARP_SURUM}"},
        )
        with urllib.request.urlopen(req, timeout=30) as r:
            zip_yolu.write_bytes(r.read())
    except urllib.error.URLError as e:
        print(renkli(f"  Hata: Indirme basarisiz: {e}", "kirmizi"))
        sys.exit(1)

    # SHA256 dogrulama
    beklenen_sha = bilgi.get("sha256", "")
    if beklenen_sha:
        gercek_sha = hashlib.sha256(zip_yolu.read_bytes()).hexdigest()
        if gercek_sha != beklenen_sha:
            zip_yolu.unlink(missing_ok=True)
            print(renkli("  Hata: SHA256 dogrulama basarisiz. Dosya bozuk olabilir.", "kirmizi"))
            sys.exit(1)

    # Kurulum
    hedef = PAKET_DIZINI / paket_adi
    if hedef.exists():
        shutil.rmtree(hedef)
    hedef.mkdir(parents=True)

    with zipfile.ZipFile(zip_yolu, "r") as zf:
        zf.extractall(hedef)

    print(renkli(f"  '{paket_adi}' v{surum} basariyla kuruldu!", "yesil"))
    aciklama = bilgi.get("aciklama", "")
    if aciklama:
        print(renkli(f"  {aciklama}", "beyaz"))


def komut_kaldir(paket_adi):
    baslik()
    hedef = PAKET_DIZINI / paket_adi
    if not hedef.exists():
        print(renkli(f"  '{paket_adi}' kurulu degil.", "sari"))
        return
    shutil.rmtree(hedef)
    print(renkli(f"  '{paket_adi}' kaldirildi.", "yesil"))


def komut_listele():
    baslik()
    dizinleri_olustur()
    paketler = kurulu_paketler()
    if not paketler:
        print(renkli("  Hic kurulu paket yok.", "sari"))
        print(renkli("  Aramak icin: python tpm.py ara <sorgu>", "mavi"))
        return
    print(renkli(f"  Kurulu paketler ({len(paketler)}):", "kalin"))
    for p in sorted(paketler):
        bilgi = kurulu_paket_bilgisi(p)
        if bilgi:
            surum = bilgi.get("surum", "?")
            aciklama = bilgi.get("aciklama", "")
            print(f"    {renkli(p, 'yesil')} v{surum}  {renkli(aciklama, 'beyaz')}")
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
    ]
    if not sonuclar:
        print(renkli(f"  '{sorgu}' icin sonuc bulunamadi.", "sari"))
        return
    print(renkli(f"  '{sorgu}' icin {len(sonuclar)} sonuc:", "kalin"))
    for isim, bilgi in sorted(sonuclar):
        surum = bilgi.get("surum", "?")
        aciklama = bilgi.get("aciklama", "")
        yazar = bilgi.get("yazar", "")
        kurulu = "  [kurulu]" if (PAKET_DIZINI / isim).exists() else ""
        print(f"    {renkli(isim, 'yesil')} v{surum}{renkli(kurulu, 'mavi')}  {aciklama}  ({yazar})")


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
    print(renkli(f"  Paket: {paket_adi}", "kalin"))
    print(f"  Surum:       {kaynak.get('surum', '?')}")
    print(f"  Aciklama:    {kaynak.get('aciklama', '')}")
    print(f"  Yazar:       {kaynak.get('yazar', '')}")
    print(f"  Bagimlilik:  {', '.join(kaynak.get('bagimliliklar', {}).keys()) or 'yok'}")
    durum = renkli("kurulu", "yesil") if yerel else renkli("kurulu degil", "sari")
    print(f"  Durum:       {durum}")
    if uzak and yerel and uzak.get("surum") != yerel.get("surum"):
        print(renkli(f"  Guncelleme var: v{uzak.get('surum')}", "sari"))


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
            print(renkli(f"  Guncelleniyor: {p} {yerel.get('surum')} -> {uzak.get('surum')}", "mavi"))
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
        "aciklama": f"{paket_adi} icin T-Sharp paketi",
        "yazar": "",
        "tsharp_surum": f">={TSHARP_SURUM}",
        "bagimliliklar": {},
    }
    (hedef / "paket.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    kod = f"""// {paket_adi} - T-Sharp Paketi
// Buraya fonksiyonlarinizi yazin

fonksiyon merhaba isim
  yazdir "Merhaba " + isim + "! Bu {paket_adi} paketidir."
son
"""
    (hedef / f"{paket_adi}.tsharp").write_text(kod, encoding="utf-8")

    print(renkli(f"  '{paket_adi}' paketi olusturuldu!", "yesil"))
    print(f"  Klasor:   {hedef.resolve()}")
    print(f"  Manifest: {hedef / 'paket.json'}")
    print(f"  Kod:      {hedef / (paket_adi + '.tsharp')}")
    print(renkli("\n  Yayinlamak icin kayit defterini GitHub PR ile guncelleyin.", "mavi"))


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

    zip_adi = f"{isim}-{surum}.zip"
    with zipfile.ZipFile(zip_adi, "w", zipfile.ZIP_DEFLATED) as zf:
        for dosya in Path(".").iterdir():
            if dosya.suffix in (".tsharp", ".json", ".md", ".txt"):
                zf.write(dosya, dosya.name)

    sha256 = hashlib.sha256(Path(zip_adi).read_bytes()).hexdigest()

    print(renkli(f"  '{isim}' v{surum} paketlendi: {zip_adi}", "yesil"))
    print(f"  SHA256: {sha256}")
    print(renkli("\n  Yayinlamak icin adimlar:", "kalin"))
    print(f"  1. {zip_adi} dosyasini GitHub'a yukleyin:")
    print(f"     registry/paketler/{zip_adi}")
    print(f"  2. registry/paketler.json dosyasina ekleyin:")
    giris = {
        isim: {
            "surum": surum,
            "aciklama": manifest.get("aciklama", ""),
            "yazar": manifest.get("yazar", ""),
            "indirme_url": f"https://raw.githubusercontent.com/Artfical/TSharp/main/registry/paketler/{zip_adi}",
            "sha256": sha256,
            "bagimliliklar": manifest.get("bagimliliklar", {}),
        }
    }
    print(json.dumps(giris, ensure_ascii=False, indent=2))
    print(renkli("  3. GitHub'a Pull Request gonderin.", "mavi"))


# ==================== YARDIM ====================

def yardim():
    baslik()
    print("""
  Kullanim: python tpm.py <komut> [arguman]

  Komutlar:
    yukle   <paket>    Paketi indir ve kur
    kaldir  <paket>    Kurulu paketi kaldir
    listele            Kurulu paketleri goster
    ara     <sorgu>    Kayit defterinde ara
    bilgi   <paket>    Paket detaylarini goster
    guncelle [paket]   Paket(ler)i guncelle
    baslat  <isim>     Yeni paket projesi olustur
    yayinla            Mevcut paketi ZIP'e paketler ve
                       kayit defteri girisini hazirlar

  Ornekler:
    python tpm.py yukle matematik
    python tpm.py ara oyun
    python tpm.py listele
    python tpm.py baslat benim-paketim
""")


# ==================== GIRIS NOKTASI ====================

def main():
    if len(sys.argv) < 2:
        yardim()
        sys.exit(0)

    komut = sys.argv[1].lower()

    # Turkce karakter normallestiricisi
    donusum = {
        "yükle": "yukle", "yukle": "yukle",
        "kaldır": "kaldir", "kaldir": "kaldir",
        "güncelle": "guncelle", "guncelle": "guncelle",
        "başlat": "baslat", "baslat": "baslat",
        "yayınla": "yayinla", "yayinla": "yayinla",
        "listele": "listele", "ara": "ara",
        "bilgi": "bilgi", "yardim": "yardim",
        "yardım": "yardim", "help": "yardim",
    }
    komut = donusum.get(komut, komut)

    if komut == "yukle":
        if len(sys.argv) < 3:
            print(renkli("  Kullanim: python tpm.py yukle <paket_adi>", "kirmizi"))
            sys.exit(1)
        komut_yukle(sys.argv[2])
    elif komut == "kaldir":
        if len(sys.argv) < 3:
            print(renkli("  Kullanim: python tpm.py kaldir <paket_adi>", "kirmizi"))
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
            print(renkli("  Kullanim: python tpm.py bilgi <paket_adi>", "kirmizi"))
            sys.exit(1)
        komut_bilgi(sys.argv[2])
    elif komut == "guncelle":
        paket = sys.argv[2] if len(sys.argv) >= 3 else None
        komut_guncelle(paket)
    elif komut == "baslat":
        if len(sys.argv) < 3:
            print(renkli("  Kullanim: python tpm.py baslat <paket_adi>", "kirmizi"))
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
