import yfinance as yf
import pandas as pd
import numpy as np
from talib import RSI, MACD

def fetch_stock_prices(symbol, start_date, end_date):
    try:
        # Fetch historical data from Yahoo Finance
        stock_data = yf.download(symbol, start=start_date, end=end_date, interval='15m')
        return stock_data
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def fetch_rsi(ticker, start_date, end_date):
    stock_data = fetch_stock_prices(ticker, start_date, end_date)
    if stock_data is not None:
        close_prices = stock_data['Close'].values
        rsi_values = RSI(close_prices, timeperiod=14)
        stock_data['RSI'] = rsi_values
        return stock_data[['RSI']]
    else:
        return None

def fetch_macd(ticker, start_date, end_date):
    stock_data = fetch_stock_prices(ticker, start_date, end_date)
    if stock_data is not None:
        close_prices = stock_data['Close'].values
        macd, signal, _ = MACD(close_prices, fastperiod=12, slowperiod=26, signalperiod=9)
        stock_data['MACD'] = macd
        stock_data['MACD Signal'] = signal
        return stock_data[['MACD', 'MACD Signal']]
    else:
        return None

# def get_data(stock):
#     #get historical stock data 
#     YEARS = 3
#     start = (pd.Timestamp.now() - pd.DateOffset(years=YEARS)).strftime('%Y-%m-%d')
#     END = pd.Timestamp.now().strftime('%Y-%m-%d')
#     stock_data = yf.download(stock, start=start, end=END)
#     stock_data.reset_index(inplace=True)

#     # Calculate daily returns
#     stock_data['Daily Return'] = stock_data['Close'].pct_change()
    
    
#     # Separate gains and losses
#     stock_data['Gain'] = stock_data['Daily Return'].apply(lambda x: x if x > 0 else 0)
#     stock_data['Loss'] = stock_data['Daily Return'].apply(lambda x: -x if x < 0 else 0)
    
#     # Calculate average gain and loss
#     window = 14
#     stock_data['Avg Gain'] = stock_data['Gain'].rolling(window=window).mean()
#     stock_data['Avg Loss'] = stock_data['Loss'].rolling(window=window).mean()
    
#     # Calculate RS and RSI
#     stock_data['RS'] = stock_data['Avg Gain'] / stock_data['Avg Loss']
#     stock_data['RSI'] = 100 - (100 / (1 + stock_data['RS']))
    
#     # Calculate the 26-day moving average of the closing prices
#     stock_data['MA_26_Day'] = stock_data['Close'].rolling(window=26).mean()

#     # Return the final DataFrame
#     return stock_data[['Date', 'MA_26_Day', 'RSI', 'Volume']]