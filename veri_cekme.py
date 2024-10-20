import yfinance as yf


hisse_sembolu = "THYAO.IS"
hisse = yf.Ticker(hisse_sembolu) # Hissenin Verisini Ticker Aracı ile çekme

#hisse.info - Bu kodla hisseye ait özet bilgiler yıl sonu kapanışlar açılışları ortalama hacimler gözüküyor. Lazımsa printleyin :)

hisse_verisi = hisse.history(period="1d",start='2024-10-18',end='2024-10-19',interval='1m')
#Period - Hissenin Zaman Aralığı
#Start - Hisse Verisinin Başlangıç Tarihi
#End - Hisse Verisinin Bitiş Tarihi
#Interval - Mum Zaman Değeri

print(f"Hisse {hisse_sembolu}:")
print(hisse_verisi[['Open', 'High', 'Low', 'Close', 'Volume']])



#Kutuphane detayli incelemesi -> https://analyzingalpha.com/yfinance-python