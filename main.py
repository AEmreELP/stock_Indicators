import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from functions import *

def main():
    # Create sample price data
    #print(generate_sample_stock_data(start_date=datetime(2023, 1, 1), num_days=100, initial_price=100, initial_volume=1000,
    #                           seed=42))

    data = generate_sample_stock_data(start_date=datetime(2023, 1, 1), num_days=100, initial_price=100, initial_volume=1000,
                               seed=42)
    print(data.iloc[0])

    print(calculate_mfi(data,periods=4))

if __name__ == "__main__":
    main()
