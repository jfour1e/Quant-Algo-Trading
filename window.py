import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

def fetch_stock_prices(symbol, start_date, end_date):
    try:
        # Fetch historical data from Yahoo Finance
        stock_data = yf.download(symbol, start=start_date, end=end_date, interval='1h')
        return stock_data
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

#test for fetch_stock_prices
#print(fetch_stock_prices('MSFT','2024-03-18','2024-03-25'))

def calculate_fibonacci_levels(high, low):
    # Calculate Fibonacci retracement levels
    levels = [0, 23.6, 38.2, 50, 61.8, 78.6, 100]

    # Calculate price range
    price_range = high - low

    # Calculate retracement levels
    retracement_levels = [high - level / 100.0 * price_range for level in levels]

    return retracement_levels

def plot_stock_prices(stock_data, retracement_levels):
    # Plotting the closing prices
    plt.figure(figsize=(10, 6))
    plt.plot(stock_data['Close'], label='Close Price', color='blue')

    # Plotting Fibonacci retracement levels
    for level in retracement_levels:
        plt.axhline(y=level, linestyle='--', color='orange', label=f'Fib {int(level)}%')

    plt.title('Microsoft Stock Prices with Fibonacci Retracement Levels')
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.legend()
    plt.show()
