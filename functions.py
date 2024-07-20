import numpy as np
import pandas as pd

def calculate_mfi(data, periods=14):
    high = data['High']
    low = data['Low']
    close = data['Close']
    volume = data['Volume']

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
