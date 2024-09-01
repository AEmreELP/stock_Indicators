import numpy as np
import pandas as pd

def calculate_bollinger_bands(close_prices, window=20, num_std=2):
    """
    Bollinger Bantlarını hesaplar.

    Args:
    close_prices (pd.Series or np.array): Kapanış fiyatları.
    window (int): Hareketli ortalama penceresi (varsayılan 20).
    num_std (int): Standart sapmanın çarpanı (varsayılan 2).

    Returns:
    pd.DataFrame: Orta, üst ve alt bantları içeren bir DataFrame.
    """
    # Kapanış fiyatlarını pandas Series'e dönüştürme
    close_prices = pd.Series(close_prices)

    # Rolling mean ve standart sapma hesaplama
    rolling_mean = close_prices.rolling(window).mean()
    rolling_std = close_prices.rolling(window).std()

    # Bollinger Bantları hesaplama
    upper_band = rolling_mean + (rolling_std * num_std)
    lower_band = rolling_mean - (rolling_std * num_std)

    # Sonuçları DataFrame olarak döndürme
    bollinger_bands = pd.DataFrame({
        'Middle Band': rolling_mean,
        'Upper Band': upper_band,
        'Lower Band': lower_band
    })

    return bollinger_bands

# Örnek kullanım
# 1 milyon rastgele kapanış fiyatı
close_prices = np.random.rand(1000000) * 100

# Fonksiyonu çağırma
bollinger_bands = calculate_bollinger_bands(close_prices, window=20, num_std=2)

# İlk birkaç satırı gösterme
print(bollinger_bands.head())
