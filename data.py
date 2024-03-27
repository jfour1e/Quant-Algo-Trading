import yfinance as yf
import pandas as pd
import numpy as np

def get_data(stock):
    #get historical stock data 
    YEARS = 3
    start = (pd.Timestamp.now() - pd.DateOffset(years=YEARS)).strftime('%Y-%m-%d')
    END = pd.Timestamp.now().strftime('%Y-%m-%d')
    stock_data = yf.download(stock, start=start, end=END)
    stock_data.reset_index(inplace=True)

    # Calculate daily returns
    stock_data['Daily Return'] = stock_data['Close'].pct_change()
    
    
    # Separate gains and losses
    stock_data['Gain'] = stock_data['Daily Return'].apply(lambda x: x if x > 0 else 0)
    stock_data['Loss'] = stock_data['Daily Return'].apply(lambda x: -x if x < 0 else 0)
    
    # Calculate average gain and loss
    window = 14
    stock_data['Avg Gain'] = stock_data['Gain'].rolling(window=window).mean()
    stock_data['Avg Loss'] = stock_data['Loss'].rolling(window=window).mean()
    
    # Calculate RS and RSI
    stock_data['RS'] = stock_data['Avg Gain'] / stock_data['Avg Loss']
    stock_data['RSI'] = 100 - (100 / (1 + stock_data['RS']))
    
    # Calculate the 26-day moving average of the closing prices
    stock_data['MA_26_Day'] = stock_data['Close'].rolling(window=26).mean()

    # Return the final DataFrame
    return stock_data[['Date', 'MA_26_Day', 'RSI', 'Volume']]