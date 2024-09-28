import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from functions import *
from isyatirimhisse import StockData, Financials
import ta
from datetime import date, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

def process_stock(hisse):
    stock_data = StockData()
    try:
        end_date = (date.today()).strftime('%d-%m-%Y')
        start_date = (date.today() - timedelta(weeks=5)).strftime('%d-%m-%Y')
        df = stock_data.get_data(
            symbols=[hisse],
            start_date=start_date,
            #start_date="02-09-2024",
            #end_date="19-09-2024",
            end_date=end_date,
            exchange='0',
            frequency='1d',
            return_type='0',
            save_to_excel=False
        )

        last_mfi = calculate_mfi(df, 14).iloc[-1]
        last_rsi = calculate_rsi_with_ta(df, 14).iloc[-1]
        last_ema = calculate_ema(df,14).iloc[-1]
        last_fisher = calculate_fisher(df,14).iloc[-1]
        last_macd = 0 #calculate_macd_with_ta(df).iloc[-1]
        last_stochastic = 0 #calculate_stochastic(df,14,3,3).iloc[-1]

        if last_mfi >= 80:
            decision_mfi = f'{hisse}, MFI ya göre Sat'
        elif last_mfi <= 20:
            decision_mfi = f'{hisse}, MFI ya göre Al'
        else:
            decision_mfi = f'{hisse}, MFI ya göre Nötr'
        
        if last_rsi >= 70:
            decision_rsi = f'{hisse}, RSI ya göre Sat'
        elif last_rsi <= 30:
            decision_rsi = f'{hisse}, RSI ya göre Al'
        else:
            decision_rsi = f'{hisse}, RSI ya göre Nötr'
        if last_fisher >= 70:
            decision_fisher = f'{hisse}, RSI ya göre Sat'
        elif last_fisher <= 30:
            decision_fisher = f'{hisse}, RSI ya göre Al'
        else:
            decision_fisher = f'{hisse}, RSI ya göre Nötr'

        if last_ema >= 70:
            decision_ema = f'{hisse}, RSI ya göre Sat'
        elif last_ema <= 30:
            decision_ema = f'{hisse}, RSI ya göre Al'
        else:
            decision_ema = f'{hisse}, RSI ya göre Nötr'

        if last_macd >= 70:
            decision_macd = f'{hisse}, RSI ya göre Sat'
        elif last_macd <= 30:
            decision_macd = f'{hisse}, RSI ya göre Al'
        else:
            decision_macd = f'{hisse}, RSI ya göre Nötr'

        if last_stochastic >= 70:
            decision_stochastic = f'{hisse}, RSI ya göre Sat'
        elif last_stochastic <= 30:
            decision_stochastic = f'{hisse}, RSI ya göre Al'
        else:
            decision_stochastic = f'{hisse}, RSI ya göre Nötr'


        # print("**********************")
        # print("**********************")
        # print(f"hisse:{hisse}\n"
        #       f"Last mfi :{last_mfi}\n"
        #       f"Last rsi : {last_rsi}\n"
        #       f"last ema:{last_ema}\n"
        #       f"last fisher:{last_macd}\n"
        #       f"last fisher:{last_fisher}\n"
        #       f"last fisher:{last_stochastic}\n"
        #
        #       f"Decision_mfi:{decision_mfi}\n"
        #       f"Decision_rsi:{decision_rsi}\n"
        #       f"Decision_ema:{decision_ema}\n"
        #       f"Decision_macd:{decision_macd}\n"
        #       f"Decision_fisher:{decision_fisher}\n"
        #       f"Decision_fisher:{decision_stochastic}\n"
        #       f"End_date:{end_date} \n")
        # print("----------------------------------")
        # print("----------------------------------")

        return {
            'Hisse': hisse,
            'MFI': last_mfi,
            'RSI': last_rsi,
            'EMA':last_ema,
            'Fisher':last_fisher,
            'Decision_Mfi': decision_mfi,
            'Decision_Rsi': decision_rsi,
            'Date': end_date
        }
    except Exception as e:
        print(f'Hisse {hisse} hata : {e}')
        return None

def main():
    Hisseler = Hisse_Temel_Veriler()
    print(Hisseler)
    #decisions = []
    for hisse in Hisseler:
        print(process_stock(hisse))
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for i in range(0, 10):
            for hisse in Hisseler:
                futures.append(executor.submit(process_stock, hisse, i))
        
        for future in as_completed(futures):
            result = future.result()
            if result:
                #decisions.append(result)
                pass
    end_time = time.time()
    print(f'Geçen süre: {end_time - start_time}')
    """
    decision_df = pd.DataFrame(decisions)
    decision_df.to_excel('decisions.xlsx', index=False)
    """

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

    """
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
    """

if __name__ == "__main__":
    main()