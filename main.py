import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from functions import *
from isyatirimhisse import StockData, Financials
import ta

def main():
    stock_data = StockData()

    df = stock_data.get_data(
        symbols=['MIATK'],
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



    print("********************************")
    last_mfi=calculate_mfi(df,14).iloc[-1]
    last_rsi=calculate_rsi_with_ta(df,14).iloc[-1]

    print(last_rsi)
    print("MFI indicator")
    if(last_mfi>=80):
        print("Sat")
    elif (last_mfi<=20):
        print("Al")
    else:
        print("Nötr")

    print("RSI indicator")
    if(last_rsi>=50):
        print("Sat")
    elif (last_rsi<50):
        print("Al")




if __name__ == "__main__":
    main()
