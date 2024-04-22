#signals Library of functions
import matplotlib.pyplot as plt

def generate_ema_signals(ema_data):
    signals = []
    for i in range(1, len(ema_data)):
        if ema_data['EMA_5'][i] > ema_data['EMA_8'][i] and ema_data['EMA_5'][i - 1] < ema_data['EMA_8'][i - 1]:
            signals.append((ema_data.index[i], 'Buy'))
        elif ema_data['EMA_5'][i] < ema_data['EMA_8'][i] and ema_data['EMA_5'][i - 1] > ema_data['EMA_8'][i - 1]:
            signals.append((ema_data.index[i], 'Sell'))
        else:
            signals.append((ema_data.index[i], ''))
    return signals


def generate_macd_signals(macd_data):
    signals = []
    
    for i in range(1, len(macd_data)):
        # MACD-based signals
        if macd_data['MACD'][i] > macd_data['MACD Signal'][i] and macd_data['MACD'][i-1] < macd_data['MACD Signal'][i-1]:
            signals.append((macd_data.index[i], 'Buy')) 
        
        elif macd_data['MACD'][i] < macd_data['MACD Signal'][i] and macd_data['MACD'][i-1] > macd_data['MACD Signal'][i-1]:
            signals.append((macd_data.index[i], 'Sell')) 
        
        else:
            signals.append((macd_data.index[i], ''))  # No signal

    return signals


def generate_rsi_signals(rsi_data):
    rsi_signals = []
    
    for i in range(1, len(rsi_data)):
        # RSI-based signals
        if rsi_data['RSI'][i] < 30:
            rsi_signals.append((rsi_data.index[i], 'Buy')) 
        
        elif rsi_data['RSI'][i] > 70:
            rsi_signals.append((rsi_data.index[i], 'Sell')) 
        
        else:
            rsi_signals.append((rsi_data.index[i], '')) 

    return rsi_signals


def generate_fibonacci_signals(price, fibonacci_levels):
    closest_level = min(fibonacci_levels, key=lambda x: abs(x - price))
    entry_level_index = fibonacci_levels.index(closest_level)
    
    if entry_level_index < len(fibonacci_levels) - 1:
        target_level = fibonacci_levels[entry_level_index + 1]
    else:
        target_level = None
    
    if entry_level_index > 0:
        stop_loss_level = fibonacci_levels[entry_level_index - 1]
    else:
        stop_loss_level = None
    
    return closest_level, target_level, stop_loss_level


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

