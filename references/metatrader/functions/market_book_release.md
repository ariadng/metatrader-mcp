# MetaTrader 5 Python API: `market_book_release` Function

## Overview

The `market_book_release` function cancels the subscription of the MetaTrader 5 terminal to the Market Depth change events for a specified financial instrument (symbol). This function is used to clean up resources and stop receiving Market Depth updates when they are no longer needed.

## Function Syntax

```python
market_book_release(
   symbol      # financial instrument name
)
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `symbol` | string | Financial instrument name (e.g., "EURUSD", "AAPL", etc.). Required unnamed parameter. |

## Return Value

Returns `True` if successful, otherwise returns `False`.

## Important Notes

- You must call `initialize()` to establish a connection to the MetaTrader 5 terminal before calling `market_book_release()`
- This function should be called when you no longer need Market Depth data for a symbol to free up resources
- The function is similar to the MQL5 `MarketBookRelease()` function
- It's good practice to always call this function when you're done with Market Depth data, especially in applications that run for extended periods

## Market Depth Function Workflow

The Market Depth functions in the MetaTrader 5 API work together in a specific sequence:

1. `market_book_add(symbol)` - Subscribe to Market Depth updates for a symbol
2. `market_book_get(symbol)` - Retrieve the current Market Depth data (can be called multiple times)
3. `market_book_release(symbol)` - Unsubscribe from Market Depth updates when finished

This workflow ensures proper resource management when working with Market Depth data.

## Usage Examples

### Basic Market Depth Workflow

```python
import MetaTrader5 as mt5

# Establish connection to the MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

# Select the symbol in MarketWatch to ensure it's available
if not mt5.symbol_select("EURUSD", True):
    print("Failed to select EURUSD")
    mt5.shutdown()
    quit()

# Subscribe to market depth updates
if mt5.market_book_add("EURUSD"):
    print("Successfully subscribed to EURUSD market depth")
    
    # Get market depth data
    market_depth = mt5.market_book_get("EURUSD")
    if market_depth:
        print("\nEURUSD Market Depth:")
        print("Total orders in book:", len(market_depth))
        
        # Display first few orders
        for i, order in enumerate(market_depth[:5], 1):
            order_type = "Buy" if order.type == 1 else "Sell"
            print(f"{i}. Type: {order_type}, Price: {order.price}, Volume: {order.volume}")
    else:
        print("Failed to get market depth, error code =", mt5.last_error())
    
    # Unsubscribe from market depth updates when done
    if mt5.market_book_release("EURUSD"):
        print("\nSuccessfully unsubscribed from EURUSD market depth")
    else:
        print("\nFailed to unsubscribe from EURUSD market depth, error code =", mt5.last_error())
else:
    print("Failed to subscribe to EURUSD market depth, error code =", mt5.last_error())

# Shut down the connection when done
mt5.shutdown()
```

### Using Market Depth in a Try-Finally Block

```python
import MetaTrader5 as mt5
import time

# Establish connection to the MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

# Select the symbol in MarketWatch
if not mt5.symbol_select("EURUSD", True):
    print("Failed to select EURUSD")
    mt5.shutdown()
    quit()

# Try block ensures we always release resources even if an exception occurs
try:
    # Subscribe to market depth updates
    if not mt5.market_book_add("EURUSD"):
        print("Failed to subscribe to EURUSD market depth, error code =", mt5.last_error())
        raise Exception("Subscription failed")
        
    print("Monitoring EURUSD market depth for 10 seconds...")
    
    # Monitor market depth for 10 seconds
    start_time = time.time()
    while time.time() - start_time < 10:
        market_depth = mt5.market_book_get("EURUSD")
        if market_depth:
            # Calculate market statistics
            buy_orders = [order for order in market_depth if order.type == 1]
            sell_orders = [order for order in market_depth if order.type == 0]
            
            bid_volume = sum(order.volume for order in buy_orders)
            ask_volume = sum(order.volume for order in sell_orders)
            
            print(f"\n[{time.strftime('%H:%M:%S')}] Market Depth Summary:")
            print(f"Bid volume: {bid_volume:.2f}, Ask volume: {ask_volume:.2f}")
            print(f"Ratio: {bid_volume/ask_volume:.2f}" if ask_volume > 0 else "Ratio: N/A")
        
        time.sleep(2)  # Check every 2 seconds
        
except Exception as e:
    print(f"An error occurred: {e}")
    
finally:
    # Always unsubscribe in the finally block to ensure cleanup
    print("\nUnsubscribing from market depth updates...")
    mt5.market_book_release("EURUSD")
    
    # Shut down the connection when done
    mt5.shutdown()
    print("Connection closed")
```

### Managing Multiple Symbol Subscriptions

```python
import MetaTrader5 as mt5
import time

# Establish connection to the MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

# List of symbols to monitor
symbols = ["EURUSD", "GBPUSD", "USDJPY"]
subscribed_symbols = []

try:
    # Subscribe to market depth for multiple symbols
    for symbol in symbols:
        # Select the symbol in MarketWatch
        if mt5.symbol_select(symbol, True):
            # Subscribe to market depth
            if mt5.market_book_add(symbol):
                print(f"Successfully subscribed to {symbol} market depth")
                subscribed_symbols.append(symbol)
            else:
                print(f"Failed to subscribe to {symbol} market depth, error code = {mt5.last_error()}")
        else:
            print(f"Failed to select {symbol}")
    
    # If we have subscriptions, monitor them
    if subscribed_symbols:
        print(f"\nMonitoring market depth for {len(subscribed_symbols)} symbols for 10 seconds...")
        
        start_time = time.time()
        while time.time() - start_time < 10:
            for symbol in subscribed_symbols:
                market_depth = mt5.market_book_get(symbol)
                if market_depth:
                    print(f"\n{symbol} has {len(market_depth)} orders in the Market Depth")
            
            time.sleep(2)  # Update every 2 seconds
    else:
        print("No symbols were successfully subscribed")
        
except KeyboardInterrupt:
    print("\nMonitoring interrupted by user")
    
finally:
    # Unsubscribe from all market depth subscriptions
    print("\nCleaning up resources...")
    for symbol in subscribed_symbols:
        if mt5.market_book_release(symbol):
            print(f"Successfully unsubscribed from {symbol} market depth")
        else:
            print(f"Failed to unsubscribe from {symbol} market depth, error code = {mt5.last_error()}")
    
    # Shut down the connection when done
    mt5.shutdown()
    print("Connection closed")
```

## Related Functions

- `market_book_add()`: Subscribes to Market Depth change events
- `market_book_get()`: Retrieves the current Market Depth data
- `symbol_select()`: Selects a symbol in the MarketWatch window (required before using Market Depth functions)
- `initialize()`: Establishes a connection to the MetaTrader 5 terminal
- `shutdown()`: Closes the connection to the MetaTrader 5 terminal
- `last_error()`: Returns the last error code and description

## Common Use Cases

1. **Resource Management**: Properly release Market Depth subscriptions when they're no longer needed
2. **Application Cleanup**: Close subscriptions before shutting down applications
3. **Symbol Rotation**: Unsubscribe from one symbol's Market Depth to subscribe to another
4. **Performance Optimization**: Manage system resources by limiting the number of active subscriptions
5. **Error Recovery**: Release subscriptions during error handling to maintain system stability

## Error Handling

When `market_book_release()` fails:
1. It returns `False`
2. Check the error with `last_error()`
3. Verify that the symbol name is correct
4. Confirm that you previously subscribed to the symbol with `market_book_add()`

Common errors:
- Symbol not found in the list of available symbols
- Not currently subscribed to Market Depth events for the specified symbol
- Terminal connectivity issues

## Best Practices

1. Always unsubscribe from Market Depth updates when they are no longer needed
2. Use try-finally blocks to ensure cleanup even if exceptions occur
3. Check the return value of `market_book_release()` to confirm successful unsubscription
4. Keep track of which symbols you've subscribed to for proper cleanup
5. Only maintain active subscriptions for symbols you're actively monitoring
6. Always call `shutdown()` when finished with MetaTrader 5 operations

## Implementation Notes

The Market Depth functions should be used in a proper sequence to ensure correct resource management:

1. First, establish a connection with `initialize()`
2. Select the symbol with `symbol_select()`
3. Subscribe to Market Depth with `market_book_add()`
4. Retrieve Market Depth data with `market_book_get()` as needed
5. Unsubscribe with `market_book_release()` when done
6. Close the connection with `shutdown()`

Following this sequence helps maintain system performance and stability, especially in long-running applications.
