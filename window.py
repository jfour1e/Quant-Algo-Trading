import yfinance as yf
import numpy as np
import plotly.express as px

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

def plot_stock_prices_with_plotly(stock_data, retracement_levels):
    # Plotting the closing prices
    fig = px.line(stock_data, x=stock_data.index, y='Close', title='Microsoft Stock Prices with Fibonacci Retracement Levels')

    # Adding Fibonacci retracement levels as horizontal lines
    for level in retracement_levels:
        fig.add_hline(y=level, line_dash="dash", line_color="orange", annotation_text=f'Fib {int(level)}%', annotation_position="bottom right")

    fig.update_xaxes(title_text='Date')
    fig.update_yaxes(title_text='Price (USD)')
    fig.show()