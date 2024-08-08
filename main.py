import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from functions import *
from isyatirimhisse import StockData, Financials
import ta
import time


def main():
    Hisseler=Hisse_Temel_Veriler()

    stock_data = StockData()
    for hisse in Hisseler:
        try:
            df = stock_data.get_data(
                symbols=[hisse],
                start_date='31-05-2023',
                end_date='07-08-2024',
                exchange='0',
                frequency='1d',
                return_type='0',
                save_to_excel=False
            )
            last_mfi = calculate_mfi(df, 14).iloc[-1]
            last_rsi = calculate_rsi_with_ta(df, 14).iloc[-1]
            if (last_mfi >= 80):
                print(f'{hisse}, MFI ya göre Sat')
            elif (last_mfi <= 20):
                print(f'{hisse}, MFI ya göre Al')
            else:
                print(f'{hisse}, MFI ya göre Nötr')
            if (last_rsi >= 50):
                print(f'{hisse}, RSI ya göre Sat')
            elif (last_rsi < 50):
                print(f'{hisse}, RSI ya göre Al')

        except Exception as e:
            print(f'Hisse {hisse} hata : {e}')
            continue
    #
    # """ To get all stock prices in excel we used upper codes."""
    # print(df.iloc[-1])
    # print("MFI")
    # print(calculate_mfi(df,14))
    # print("EMA")
    # print(calculate_ema(df,10))
    # print("RSI")
    # print(calculate_rsi_with_ta(df,14))
    # print("MACD")
    # print(calculate_macd(df))
    # print("FISHER")
    # print(calculate_fisher(df,14))
    # print("STOCHASTIC")
    # print(calculate_stochastic(df,14,3,3))
    # print("PIVOT")
    # print(calculate_pivot_point(df))



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
