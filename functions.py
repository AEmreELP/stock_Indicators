import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def generate_sample_stock_data(start_date=datetime(2023, 1, 1), num_days=100, initial_price=100, initial_volume=1000000,
                               seed=42):
    """
    Generate sample stock data with the following specifications:
    - Columns: Date, High, Low, Close, and Volume
    - Random data generation
    - Daily price constraint: Not lower than 90% or higher than 110% of the previous day's price
    - Random volume generation

    Parameters:
    start_date (datetime): The start date for the sample data (default is 2023-01-01)
    num_days (int): The number of days to generate (default is 100)
    initial_price (int): The initial price for the first day (default is 100)
    initial_volume (int): The initial volume for the first day (default is 1,000,000)
    seed (int): The random seed for reproducibility (default is 42)

    Returns:
    pandas.DataFrame: A DataFrame containing the sample stock data
    """
    # Set random seed for reproducibility
    np.random.seed(seed)

    # Generate dates
    dates = [start_date + timedelta(days=i) for i in range(num_days)]

    # Initialize price and volume
    prev_close = initial_price

    # Generate data
    data = []
    for date in dates:
        # Generate price within ±10% of previous close
        low = prev_close * np.random.uniform(0.9, 1.0)
        high = prev_close * np.random.uniform(1.0, 1.1)
        close = np.random.uniform(low, high)

        # Generate random volume
        volume = int(np.random.uniform(0.5, 1.5) * initial_volume)

        data.append([date, high, low, close, volume])
        prev_close = close

    # Create DataFrame
    df = pd.DataFrame(data, columns=['Date', 'High', 'Low', 'Close', 'Volume'])
    return df

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
