
import numpy as np
from datetime import datetime, timedelta


def calculate_mfi(data, periods=14):
    high = data['HIGH_TL']
    low = data['LOW_TL']
    close = data['CLOSING_TL']
    volume = data['VOLUME_TL']

    typical_price = (high + low + close) / 3
    raw_money_flow = typical_price * volume

    positive_flow = np.where(typical_price > typical_price.shift(1), raw_money_flow, 0)
    negative_flow = np.where(typical_price < typical_price.shift(1), raw_money_flow, 0)

    positive_mf = pd.Series(positive_flow).rolling(window=periods).sum()
    negative_mf = pd.Series(negative_flow).rolling(window=periods).sum()

    mfr = positive_mf / negative_mf
    mfi = 100 - (100 / (1 + mfr))

    return pd.Series(mfi, name='MFI')

# Example usage:
# Assuming you have a DataFrame 'df' with columns 'High', 'Low', 'Close', and 'Volume'
# df['MFI'] = calculate_mfi(df)

def calculate_ema(data, period, column='Close'):
    """
    Calculate Exponential Moving Average (EMA) for a given dataset.

    Parameters:
    data (pandas.DataFrame): DataFrame containing the price data
    period (int): The period over which to calculate the EMA
    column (str): The name of the column containing the price data (default is 'Close')

    Returns:
    pandas.Series: EMA values
    """
    data = data.sort_index()
    multiplier = 2 / (period + 1)
    sma = data[column].rolling(window=period).mean().iloc[period - 1]
    ema_values = [sma]
    for price in data[column][period:]:
        ema = (price - ema_values[-1]) * multiplier + ema_values[-1]
        ema_values.append(ema)
    ema_series = pd.Series(ema_values, index=data.index[period - 1:], name=f'EMA_{period}')
    return ema_series


def calculate_rsi(data, periods=14):
    close_delta = data['CLOSING_TL'].diff()

    # Make two series: one for lower closes and one for higher closes
    up = close_delta.clip(lower=0)
    down = -1 * close_delta.clip(upper=0)

    # Calculate the EWMA
    ma_up = up.ewm(com=periods - 1, adjust=True, min_periods=periods).mean()
    ma_down = down.ewm(com=periods - 1, adjust=True, min_periods=periods).mean()

    rsi = ma_up / ma_down
    rsi = 100 - (100 / (1 + rsi))
    return rsi


def calculate_macd(df, fast_period=12, slow_period=26, signal_period=9):
    # Calculate the fast and slow EMAs
    ema_fast = df['CLOSING_TL'].ewm(span=fast_period, adjust=False).mean()
    ema_slow = df['CLOSING_TL'].ewm(span=slow_period, adjust=False).mean()

    # Calculate the MACD line
    macd_line = ema_fast - ema_slow

    # Calculate the signal line
    signal_line = macd_line.ewm(span=signal_period, adjust=False).mean()

    # Calculate the MACD histogram
    macd_histogram = macd_line - signal_line

    # Add the MACD indicators to the DataFrame
    df['MACD'] = macd_line
    df['Signal_Line'] = signal_line
    df['MACD_Histogram'] = macd_histogram

    return df


def calculate_fisher(df, period=14):
    high = df['HIGH_TL'].rolling(window=period).max()
    low = df['LOW_TL'].rolling(window=period).min()

    fisher = 0.5 * np.log((high + low) / (high - low))

    return fisher


import pandas as pd


def calculate_stochastic(df, window=14, smooth_k=3, smooth_d=3):
    """
    Calculate the Stochastic Oscillator for a given DataFrame.

    Parameters:
    df (pandas.DataFrame): DataFrame containing the 'High', 'Low', and 'Close' columns.
    window (int): The number of periods to use for the Stochastic Oscillator (default is 14).
    smooth_k (int): The number of periods to use for smoothing the %K line (default is 3).
    smooth_d (int): The number of periods to use for smoothing the %D line (default is 3).

    Returns:
    pandas.DataFrame: The original DataFrame with the following new columns:
        - '%K': The fast Stochastic Oscillator line.
        - '%D': The slow Stochastic Oscillator line.
    """
    lowest_low = df['LOW_TL'].rolling(window=window).min()
    highest_high = df['HIGH_TL'].rolling(window=window).max()

    df['%K'] = ((df['CLOSING_TL'] - lowest_low) / (highest_high - lowest_low)) * 100
    df['%K'] = df['%K'].rolling(window=smooth_k).mean()
    df['%D'] = df['%K'].rolling(window=smooth_d).mean()

    return df


def generate_signals(df):
    """
    Generate trading signals based on EMA crossovers.

    Parameters:
    df (pandas.DataFrame): DataFrame containing 'EMA_20' and 'EMA_50' columns

    Returns:
    pandas.DataFrame: DataFrame with added 'Signal' and 'Position' columns
    """
    df['Signal'] = np.where(df['EMA_20'] > df['EMA_50'], 1, 0)  # 1 for buy, 0 for sell
    df['Position'] = df['Signal'].diff()
    return df
