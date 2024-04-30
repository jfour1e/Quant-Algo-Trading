import yfinance as yf
from talib import RSI, MACD
import pandas as pd

#fetching and calculating indicators 

def fetch_data(symbol, start_date, end_date):
    try:
        # Fetch historical data from Yahoo Finance
        stock_data = yf.download(symbol, start=start_date, end=end_date, interval='15m')
        stock_data.drop(columns=['Adj Close', 'Volume'], inplace=True)

        close_prices = stock_data['Close'].values
        rsi_values = RSI(close_prices, timeperiod=14)
        stock_data['RSI'] = rsi_values

        close_prices = stock_data['Close'].values
        macd, signal, _ = MACD(close_prices, fastperiod=12, slowperiod=26, signalperiod=9)
        stock_data['MACD'] = macd
        stock_data['MACD Signal'] = signal

        stock_data['EMA_5'] = stock_data['Close'].ewm(span=5, min_periods=0, adjust=False).mean()
        stock_data['EMA_8'] = stock_data['Close'].ewm(span=8, min_periods=0, adjust=False).mean()
        stock_data['EMA_13'] = stock_data['Close'].ewm(span=13, min_periods=0, adjust=False).mean()

        stock_data.fillna(0, inplace=True)
        
        return stock_data
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def calculate_fibonacci_levels(data, row):

    previous_40_rows = data.iloc[max(0, row - 39):row + 1]

    high = previous_40_rows['High'].max()
    low = previous_40_rows['Low'].min()

    # Calculate Fibonacci retracement levels
    levels = [0, 23.6, 38.2, 50, 61.8, 78.6, 100]

    # Calculate price range
    price_range = high - low

    # Calculate retracement levels
    retracement_levels = [high - level / 100.0 * price_range for level in levels]

    return retracement_levels

def find_positions_fibonacci(data, row, fibonacci_levels):
    current_price = data.iloc[row]['Close']
    entry_level = None
    min_distance = float('inf')

    for level in fibonacci_levels:
        distance = abs(level - current_price)
        if (distance.min() == min_distance):  # Check if the minimum distance in the Series is equal to min_distance
            entry_level = level
            break

    if entry_level is None:
        return None, None

    entry_index = fibonacci_levels.index(entry_level)
    stop_loss = fibonacci_levels[max(0, entry_index - 1)]  # One level below
    target_profit = fibonacci_levels[min(len(fibonacci_levels) - 1, entry_index + 1)]  # One level above

    return entry_level, stop_loss, target_profit
