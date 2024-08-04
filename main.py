import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from functions import *
from isyatirimhisse import StockData, Financials
import ta

def main():
    stock_data = StockData()

    df = stock_data.get_data(
        symbols=['CWENE'],
        start_date='31-05-2023',
        end_date='31-07-2024',
        exchange='0',
        frequency='1d',
        return_type='0',
        save_to_excel=False
    )

    """ To get all stock prices in excel we used upper codes."""
    print("MFI")
    print(calculate_mfi(df,14))
    print("EMA")
    print(calculate_ema(df,10))
    print("RSI")
    print(calculate_rsi_with_ta(df,14))
    print("MACD")
    print(calculate_macd(df))
    print("FISHER")
    print(calculate_fisher(df,14))
    print("STOCHASTIC")
    print(calculate_stochastic(df,14,3,3))
    print("PIVOT")
    print(calculate_pivot_point(df))



if __name__ == "__main__":
    main()
