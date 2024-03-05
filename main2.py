import yfinance as yf

def get_historical_option_prices(ticker_symbol, expiration_date=None):
    """
    Returns the historical option prices for a given ticker and expiration date.
    
    :param ticker_symbol: The ticker symbol as a string.
    :param expiration_date: The expiration date for the options in 'YYYY-MM-DD' format. 
                            If None, the nearest expiration date is used.
    :return: A dictionary with call and put option dataframes.
    """
    # Create a Ticker object
    ticker = yf.Ticker(ticker_symbol)
    
    # If no expiration date is provided, use the nearest one
    if expiration_date is None:
        expiration_dates = ticker.options
        if not expiration_dates:
            raise ValueError("No expiration dates available for this ticker.")
        expiration_date = expiration_dates[0]  # Use the first (nearest) expiration date
    
    # Get option chain for the given expiration date
    option_chain = ticker.option_chain(expiration_date)
    
    # Option chain includes calls and puts
    calls = option_chain.calls
    puts = option_chain.puts
    
    return {'calls': calls, 'puts': puts}

# Example usage
ticker_symbol = 'AAPL'  # Example ticker
expiration_date = '2023-12-15'  # Example expiration date
option_prices = get_historical_option_prices(ticker_symbol, expiration_date)
print(option_prices['calls'])  # Print call options dataframe
print(option_prices['puts'])   # Print put options dataframe

def get_historical_option_prices(stock, exp_date):
    return None