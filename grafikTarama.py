!pip install tvDatafeed
!pip install git+https://github.com/rongardF/tvdatafeed tradingview-screener matplotlib openpyxl
!pip install ta
import pandas as pd
import numpy as np
from tvDatafeed import TvDatafeed, Interval
from tradingview_screener import get_all_symbols
import ta
import matplotlib.pyplot as plt
import os

warnings.filterwarnings("ignore")

# TradingView'e giriş yapmadan bağlanın
tv = TvDatafeed()

# Türkiye piyasasındaki tüm sembolleri almak için
try:
    # Tüm sembolleri TradingView'den çekme
    Hisseler = get_all_symbols(market='turkey')
    Hisseler = [symbol.replace('BIST:', '') for symbol in Hisseler]
    Hisseler = sorted(Hisseler)
    print(f"{len(Hisseler)} adet hisse senedi bulundu.")
except Exception as e:
    print(f"Hata alındı: {e}")

# Elmas formasyonu kontrol fonksiyonu
def elmas_formasyonu(df):
    high = df['high']
    low = df['low']

    genişleme = (high.diff().mean() > 0) and (low.diff().mean() < 0)
    daralma = (high.diff().mean() < 0) and (low.diff().mean() > 0)

    return genişleme and daralma

# OBO formasyonu kontrol fonksiyonu
def obo_formasyonu(df):
    high = df['high']
    if len(high) < 5:
        return False
    sol_omuz = high.iloc[-5]
    baş = high.iloc[-3]
    sağ_omuz = high.iloc[-1]

    return baş > sol_omuz and baş > sağ_omuz and abs(sol_omuz - sağ_omuz) / baş < 0.05

# TOBO formasyonu kontrol fonksiyonu
def tobo_formasyonu(df):
    low = df['low']
    if len(low) < 5:
        return False
    sol_omuz = low.iloc[-5]
    baş = low.iloc[-3]
    sağ_omuz = low.iloc[-1]

    return baş < sol_omuz and baş < sağ_omuz and abs(sol_omuz - sağ_omuz) / baş < 0.05

# Flama formasyonu kontrol fonksiyonu
def flama_formasyonu(df):
    high = df['high']
    low = df['low']

    daralan_kanal = (high.diff().mean() < 0) and (low.diff().mean() > 0)
    son_kırılma = high.iloc[-1] > high.mean() or low.iloc[-1] < low.mean()

    return daralan_kanal and son_kırılma

# Üçgen (Triangles) kontrol fonksiyonu
def ucgen_formasyonu(df):
    high = df['high']
    low = df['low']

    # Fiyat sıkışması: high ve low arasında daralma
    daralan_kanal = (high.diff().mean() < 0) and (low.diff().mean() < 0)

    # Kırılma
    son_kırılma = high.iloc[-1] > high.mean() or low.iloc[-1] < low.mean()

    return daralan_kanal and son_kırılma

# Kupa ve Sap (Cup and Handle) kontrol fonksiyonu
def kupa_sap_formasyonu(df):
    low = df['low']
    if len(low) < 10:
        return False
    dip = low.min()
    son_dip = low.iloc[-1]

    return son_dip > dip  # Son dip önceki dipten yüksek mi?

# Yükselen Kanal (Rising Channel) kontrol fonksiyonu
def yukselen_kanal_formasyonu(df):
    high = df['high']
    low = df['low']

    return high.diff().mean() > 0 and low.diff().mean() > 0

# Düşen Kanal (Falling Channel) kontrol fonksiyonu
def dusen_kanal_formasyonu(df):
    high = df['high']
    low = df['low']

    return high.diff().mean() < 0 and low.diff().mean() < 0

# Dikdörtgen (Rectangle) kontrol fonksiyonu
def dikdortgen_formasyonu(df):
    high = df['high']
    low = df['low']

    return high.max() - low.min() < (high.mean() * 0.05)  # Fiyat aralığı daralmış mı?

# Formasyon tarama fonksiyonu
def tarama_algoritmalari(df, formasyon):
    if formasyon == 'elmas':
        return elmas_formasyonu(df)
    elif formasyon == 'flama':
        return flama_formasyonu(df)
    elif formasyon == 'obo':
        return obo_formasyonu(df)
    elif formasyon == 'tobo':
        return tobo_formasyonu(df)
    elif formasyon == 'ucgen':
        return ucgen_formasyonu(df)
    elif formasyon == 'kupa_sap':
        return kupa_sap_formasyonu(df)
    elif formasyon == 'yukselen_kanal':
        return yukselen_kanal_formasyonu(df)
    elif formasyon == 'dusen_kanal':
        return dusen_kanal_formasyonu(df)
    elif formasyon == 'dikdortgen':
        return dikdortgen_formasyonu(df)
    return False

# Kullanıcının formasyon seçimi
def formasyon_secimi():
    formasyonlar = {
        '1': 'elmas',
        '2': 'flama',
        '3': 'obo',
        '4': 'tobo',
        '5': 'ucgen',
        '6': 'kupa_sap',
        '7': 'yukselen_kanal',
        '8': 'dusen_kanal',
        '9': 'dikdortgen'
    }

    print("Lütfen taramak istediğiniz formasyonu seçin:")
    for key, formasyon in formasyonlar.items():
        print(f"{key}: {formasyon.capitalize()} Formasyonu")

    secim = input("Seçiminizi yapın (1-9): ")
    return formasyonlar.get(secim, 'elmas')

# Kullanıcının interval seçimi
def interval_secimi():
    interval_map = {
        '1': Interval.in_15_minute,
        '2': Interval.in_30_minute,
        '3': Interval.in_45_minute,
        '4': Interval.in_1_hour,
        '5': Interval.in_2_hour,
        '6': Interval.in_4_hour,
        '7': Interval.in_daily,
        '8': Interval.in_weekly
    }

    print("\nLütfen zaman dilimini (interval) seçin:")
    print("1: 15 Dakika")
    print("2: 30 Dakika")
    print("3: 45 Dakika")
    print("4: 1 Saat")
    print("5: 2 Saat")
    print("6: 4 Saat")
    print("7: Günlük")
    print("8: Haftalık")

    secim = input("Seçiminizi yapın (1-8): ")
    return interval_map.get(secim, Interval.in_daily)  # Varsayılan olarak günlük

# Main function
def main():
    # Kullanıcının formasyon seçimi
    formasyon = formasyon_secimi()

    # Kullanıcının interval seçimi
    interval = interval_secimi()

    # Tüm BIST hisse senetleri üzerinde formasyon taraması
    tarama_yap(Hisseler, formasyon, interval)


# Programı başlat
main()