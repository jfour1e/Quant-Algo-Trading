#signals Library of functions
import matplotlib.pyplot as plt
import pandas as pd
from data import * 

def generate_ema_signals(data, row):

    last_row = data.iloc[row]

    ema_5_current = pd.Series(last_row['EMA_5'])
    ema_8_current = pd.Series(last_row['EMA_8'])

    # Get the previous row
    prev_row = data.iloc[row-1]

    ema_5_prev = pd.Series(prev_row['EMA_5'])
    ema_8_prev = pd.Series(prev_row['EMA_8'])

    buy_conditions_met = (ema_5_current > ema_8_current) & (ema_5_prev < ema_8_prev)

    sell_conditions_met = (ema_5_current < ema_8_current) & (ema_5_prev > ema_8_prev)
    
    if (buy_conditions_met.all() == True): 
         return 'Buy'

    elif(sell_conditions_met.all()):
        return 'Sell'
    else: 
        return ' '


def generate_macd_signals(data, row):
    # MACD-based signals

    if data.iloc[row]['MACD'] > data.iloc[row]['MACD Signal'] and data.iloc[row-1]['MACD'] < data.iloc[row-1]['MACD Signal']:
        return 'Buy'
    
    elif data.iloc[row]['MACD'] < data.iloc[row]['MACD Signal'] and data.iloc[row-1]['MACD'] > data.iloc[row-1]['MACD Signal']:
        return 'Sell'
    
    else:
        return ''  # No signal


def generate_rsi_signals(data, row):
    
    # RSI-based signals
    if data.iloc[row]['RSI'] < 50:
        return 'Buy'
    
    elif data.iloc[row]['RSI'] > 50:
        return 'Sell'
    
    else:
        return '' 


def generate_signals(data, row): 
    #fibonacci_levels = calculate_fibonacci_levels(data, row)
    #find_positions_fibonacci(row, fibonacci_levels)

    ema_signal = generate_ema_signals(data, row)
    most_recent_macd_signal = None
    rsi_signal = generate_rsi_signals(data, row)

    #print(find_positions_fibonacci(data, row, fibonacci_levels))

    for i in range(row, -1, -1):
        macd_signal = generate_macd_signals(data, i)
        if macd_signal != '':
            most_recent_macd_signal = macd_signal
            break
    
    buy_conditions = ((ema_signal == 'Buy') & ((most_recent_macd_signal == 'Buy') | (rsi_signal == 'Buy')))
    
    sell_conditions = ((ema_signal == 'Sell') & (((most_recent_macd_signal == 'Sell') | (rsi_signal == 'Sell')))) 

    if buy_conditions == True: 

        return 'Buy'#, entry_level, stop_loss, target_profit

    elif sell_conditions == True:
        return 'Sell'
    else: 
        return ' '


def update_stop_loss(current_price, fibonacci_levels):
    # Find the closest Fibonacci level to the current price
    closest_fibonacci_level = min(fibonacci_levels, key=lambda x: abs(x - current_price))
    closest_fibonacci_index = fibonacci_levels.index(closest_fibonacci_level)
    
    # Calculate stop loss level
    if closest_fibonacci_index > 0:
        stop_loss_level = fibonacci_levels[closest_fibonacci_index - 1]
        # Check if the current price reaches one higher Fibonacci level than the entry point
        if current_price >= fibonacci_levels[closest_fibonacci_index]:
            # If yes, increase the stop loss level to the next highest Fibonacci level
            stop_loss_level = fibonacci_levels[min(closest_fibonacci_index + 1, len(fibonacci_levels) - 1)]
    else:
        stop_loss_level = None  # No Fibonacci level below the current closest level
    
    return stop_loss_level


def plot_fibonacci_levels(price, fibonacci_levels, entry_level, target_level, stop_loss_level):
    plt.figure(figsize=(10, 6))
    
    for level in fibonacci_levels:
        plt.hlines(level, 0, len(fibonacci_levels), color='blue', linestyle='--', label='Fibonacci Levels')
    
    # Plot entry, target, and stop loss levels as horizontal lines
    plt.hlines(entry_level, 0, len(fibonacci_levels), color='green', linestyle='--', label='Entry Level')
    plt.hlines(target_level, 0, len(fibonacci_levels), color='red', linestyle='--', label='Target Level')
    plt.hlines(stop_loss_level, 0, len(fibonacci_levels), color='orange', linestyle='--', label='Stop Loss Level')
    
    # Plot current price as a horizontal line
    plt.hlines(price, 0, len(fibonacci_levels), color='gray', linestyle='--', label='Current Price')
    
    plt.xlabel('Fibonacci Levels')
    plt.ylabel('Price')
    plt.title('Fibonacci Levels with Entry, Target, and Stop Loss')
    plt.legend()
    plt.grid(True)
    
    plt.show()

