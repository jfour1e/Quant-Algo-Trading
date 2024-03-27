import yfinance as yf
import pandas as pd
import numpy as np

#import functions
from data import get_data
from window import fetch_stock_prices, calculate_fibonacci_levels, plot_stock_prices

if __name__ == "__main__":
    # Define the stock symbol (Microsoft)
    stock_symbol = 'MSFT'

    # Define the time period for which you want historical data
    start_date = '2024-03-01'
    end_date = '2024-03-25'

    # Fetch historical stock prices
    msft_data = fetch_stock_prices(stock_symbol, start_date, end_date)

    # If data is successfully fetched, calculate and plot Fibonacci retracement levels
    if msft_data is not None:
        # Calculate Fibonacci retracement levels using the highest and lowest prices
        high_price = np.max(msft_data['High'])
        low_price = np.min(msft_data['Low'])
        retracement_levels = calculate_fibonacci_levels(high_price, low_price)

        # Plot stock prices with Fibonacci retracement levels
        plot_stock_prices(msft_data, retracement_levels)

        


#tickers = ['PANW', 'SHOP', 'META', 'TSM', 'NET', 'DELL', 'ON', 'CRM', 'SONY', 'CRWD', 'AMAT']
#print(get_data('TSM'))






