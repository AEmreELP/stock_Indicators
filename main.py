import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from functions import *
from isyatirimhisse import StockData, Financials

def main():
    # Create sample price data
    #print(generate_sample_stock_data(start_date=datetime(2023, 1, 1), num_days=100, initial_price=100, initial_volume=1000,
    #                           seed=42))

    """data = generate_sample_stock_data(start_date=datetime(2023, 1, 1), num_days=100, initial_price=100, initial_volume=1000,
                               seed=42)
    print(data.iloc[0])

    print(calculate_mfi(data,periods=4))
    print(calculate_ema(data,50))
    print(calculate_rsi(data,10))
    print(calculate_macd(data))
    print(calculate_fisher(data,14))
    print(calculate_stochastic(data,14,3,3))"""
    stock_data = StockData()

    df = stock_data.get_data(
        symbols=['MIATK'],
        start_date='30-06-2024',
        end_date='31-07-2024',
        exchange='0',
        frequency='1d',
        return_type='0',
        save_to_excel=False
    )
    print(df)
    Closing_Tl = df["CLOSING_TL"]
    print(Closing_Tl)
    print("***************")
    print(calculate_mfi(df,14))
    print("***************")
    print(calculate_macd(df))



if __name__ == "__main__":
    main()
