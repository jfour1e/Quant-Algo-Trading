import yfinance as yf
from talib import RSI, MACD

#fetching and calculating indicators 

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

def calculate_emas(ticker, start_date, end_date):
    prices = fetch_stock_prices(ticker, start_date, end_date)
    prices['EMA_5'] = prices['Close'].ewm(span=5, min_periods=0, adjust=False).mean()
    prices['EMA_8'] = prices['Close'].ewm(span=8, min_periods=0, adjust=False).mean()
    prices['EMA_13'] = prices['Close'].ewm(span=13, min_periods=0, adjust=False).mean()
    return prices[['EMA_5', 'EMA_8', 'EMA_13']]

def calculate_fibonacci_levels(high, low):
    # Calculate Fibonacci retracement levels
    levels = [0, 23.6, 38.2, 50, 61.8, 78.6, 100]

    # Calculate price range
    price_range = high - low

    # Calculate retracement levels
    retracement_levels = [high - level / 100.0 * price_range for level in levels]

    return retracement_levels

def fetch_volume(ticker, start_date, end_date):
    # Fetch historical stock data at 15-minute intervals using yfinance
    stock_data = yf.download(ticker, start=start_date, end=end_date, interval="15m")
    
    # Extract volume data from the fetched stock data
    volume_data = stock_data['Volume']
    
    return volume_data
