def calculate_fibonacci_levels(high, low):
    fib_ratios = [0.236, 0.382, 0.5, 0.618, 0.786]
    return {f"{int(ratio * 100)}%": high - (high - low) * ratio for ratio in fib_ratios}

def determine_entry_position(fib_levels):
    # Example: Choosing 61.8% level as entry, this can be adjusted
    return fib_levels["618%"]

def calculate_stop_loss_and_target(entry, fib_levels, fib_ratios):
    # Assuming stop loss just below the next level down (50% for this example) and target profit at 23.6%
    stop_loss = fib_levels["50%"] - (entry - fib_levels["50%"]) * 0.05 # 5% below the 50% level for buffer
    target_profit = entry + (entry - fib_levels["786%"]) # Targeting just above the entry level for profit
    return stop_loss, target_profit

high_price = float(input("Enter the recent high price of the stock: "))
low_price = float(input("Enter the recent low price of the stock: "))

fib_levels = calculate_fibonacci_levels(high_price, low_price)
print("Fibonacci Levels:", fib_levels)

entry_price = determine_entry_position(fib_levels)
print("Suggested Entry Position:", entry_price)

stop_loss, target_profit = calculate_stop_loss_and_target(entry_price, fib_levels, [0.236, 0.382, 0.5, 0.618, 0.786])
print("Stop Loss:", stop_loss)
print("Target Profit:", target_profit)
