# matematik - TSharp 4.2 uyumlu paket v1.0.0
# Gelismis matematik fonksiyonlari
# GitHub: https://github.com/Artfical/TSharp
#
# TSHARP_FONKSIYONLAR: {fonk_adi: callable(args) -> deger}
# args = T# tarafindan gecilen arguman listesi

import math


def _faktoriyel(args):
    n = int(args[0])
    if n < 0:
        raise ValueError("Faktoriyel negatif sayi icin tanimsiz")
    return math.factorial(n)


def _asal_mi(args):
    n = int(args[0])
    if n < 2:
        return 0
    if n == 2:
        return 1
    if n % 2 == 0:
        return 0
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return 0
    return 1


def _ebob(args):
    return math.gcd(int(args[0]), int(args[1]))


def _ekok(args):
    a, b = int(args[0]), int(args[1])
    return abs(a * b) // math.gcd(a, b)


TSHARP_FONKSIYONLAR = {
    # Temel
    "kare":            lambda args: float(args[0]) ** 2,
    "kup":             lambda args: float(args[0]) ** 3,
    "us":              lambda args: float(args[0]) ** float(args[1]),
    "mutlak":          lambda args: abs(float(args[0])),
    "faktoriyel":      _faktoriyel,

    # Sayilar teorisi
    "asal_mi":         _asal_mi,
    "ebob":            _ebob,
    "ekok":            _ekok,

    # Geometri
    "daire_alani":     lambda args: math.pi * float(args[0]) ** 2,
    "daire_cevresi":   lambda args: 2 * math.pi * float(args[0]),
    "ucgen_alani":     lambda args: 0.5 * float(args[0]) * float(args[1]),
    "dikdortgen_alani":lambda args: float(args[0]) * float(args[1]),
    "kare_alani":      lambda args: float(args[0]) ** 2,
    "kare_cevresi":    lambda args: 4 * float(args[0]),

    # Istatistik (liste argumani)
    "ortalama":        lambda args: sum(args[0]) / len(args[0]) if isinstance(args[0], list) and args[0] else 0,
    "medyan":          lambda args: sorted(args[0])[len(args[0]) // 2] if isinstance(args[0], list) and args[0] else 0,
    "varyans":         lambda args: sum((x - sum(args[0])/len(args[0]))**2 for x in args[0]) / len(args[0]) if isinstance(args[0], list) and args[0] else 0,
}
