import yfinance as yf
import pandas as pd

# Define the ticker symbol, start date, and end date
ticker_symbol = 'AAPL'  # Example: Apple Inc.
start_date = '2023-01-01'
end_date = '2023-12-31'

# Fetch historical data from Yahoo Finance
data = yf.download(ticker_symbol, start=start_date, end=end_date)

# Calculate the 26-day moving average of the closing prices
data['26_Day_MA'] = data['Close'].rolling(window=26).mean()

# Display the data with the moving average
print(data[['Close', '26_Day_MA']])

