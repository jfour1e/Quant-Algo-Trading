import yfinance as yf
import pandas as pd
import numpy as np

tickers = ['PANW', 'SHOP', 'META', 'TSM', 'NET', 'DELL', 'ON', 'CRM', 'SONY', 'CRWD', 'AMAT']

def get_data(stock):
    #get historical stock data 
    YEARS = 5
    start = (pd.Timestamp.now() - pd.DateOffset(years=YEARS)).strftime('%Y-%m-%d')
    END = pd.Timestamp.now().strftime('%Y-%m-%d')
    stock_data = yf.download(stock, start=start, end=END)
    
    #
    delta = stock_data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    
    # Add RSI to the dataframe
    stock_data['RSI'] = rsi
    return stock_data

print(get_data('TSM'))
