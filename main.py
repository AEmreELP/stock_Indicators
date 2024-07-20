import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from functions import calculate_ema, generate_signals, calculate_mfi

def main():
    # Create sample price data
    np.random.seed(42)  # for reproducibility
    dates = pd.date_range(start='2023-01-01', periods=100, freq='D')
    prices = np.random.randint(100, 150, size=100) + np.sin(np.arange(100)) * 20

    # Create a DataFrame with the sample data
    df = pd.DataFrame({'Date': dates, 'Close': prices})
    df.set_index('Date', inplace=True)

    # Calculate 20-day and 50-day EMAs
    df['EMA_20'] = calculate_ema(df, period=20)
    df['EMA_50'] = calculate_ema(df, period=50)

    # Print the first few rows of the resulting DataFrame
    print("First 10 rows:")
    print(df.head(10))
    print("\nLast 10 rows:")
    print(df.tail(10))

    # Visualize the results
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['Close'], label='Close Price')
    plt.plot(df.index, df['EMA_20'], label='20-day EMA')
    plt.plot(df.index, df['EMA_50'], label='50-day EMA')
    plt.title('Stock Price with 20-day and 50-day EMAs')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True)
    plt.show()

    # Generate and print trading signals
    df = generate_signals(df)
    print("\nTrading Signals:")
    print(df[df['Position'] != 0])




    # Generate random sample data
    np.random.seed(42)
    dates = pd.date_range(start='2023-01-01', periods=100, freq='D')
    high = np.random.randint(100, 150, size=100)
    low = np.random.randint(80, 130, size=100)
    close = np.random.randint(90, 140, size=100)
    volume = np.random.randint(1000000, 5000000, size=100)

    # Create a DataFrame with the sample data
    df = pd.DataFrame({'Date': dates, 'High': high, 'Low': low, 'Close': close, 'Volume': volume})
    df.set_index('Date', inplace=True)

    # Calculate MFI with default period (14)
    df['MFI'] = calculate_mfi(df)

    # Calculate MFI with a custom period (e.g., 21)
    df['MFI_21'] = calculate_mfi(df, periods=21)

    # Print the first few rows of the DataFrame
    print(df[['Close', 'Volume', 'MFI', 'MFI_21']].head())

if __name__ == "__main__":
    main()
