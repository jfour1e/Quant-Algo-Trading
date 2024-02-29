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
    import yfinance as yf
import pandas as pd

def get_stock_data_with_rsi(stock_symbol):
    # Fetch historical data for the last 5 years
    stock_data = yf.download(stock_symbol, period="5y")
    
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
    
    # Return the final DataFrame
    return stock_data[['Close', 'RSI']]

# Example usage
stock_symbol = "AAPL" # Apple Inc.
stock_data_with_rsi = get_stock_data_with_rsi(stock_symbol)
print(stock_data_with_rsi.tail()) # Print the last few rows to verify

print(get_data('TSM'))

