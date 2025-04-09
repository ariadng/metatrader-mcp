# MetaTrader 5 Python API: `market_book_get` Function

## Overview

The `market_book_get` function retrieves the current Market Depth (Order Book) data for a specified financial instrument from the MetaTrader 5 terminal. This function returns detailed information about pending buy and sell orders at different price levels, which is essential for analyzing market liquidity, order flow, and potential price movements.

## Function Syntax

```python
market_book_get(
   symbol      # financial instrument name
)
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `symbol` | string | Financial instrument name (e.g., "EURUSD", "AAPL", etc.). Required unnamed parameter. |

## Return Value

The function returns a tuple of BookInfo entries (similar to the MQL5 `MqlBookInfo` structure), each containing:
- `type` - Order type (0 - sell order/Ask, 1 - buy order/Bid)
- `price` - Price level
- `volume` - Volume in lots at the specified price level
- `volume_real` - Volume with greater precision (when available)

Returns `None` in case of an error, which can be checked using the `last_error()` function.

## Important Notes

- You must call `initialize()` to establish a connection to the MetaTrader 5 terminal before using `market_book_get()`
- Before calling `market_book_get()`, you must first subscribe to Market Depth updates using the `market_book_add()` function
- Not all brokers and financial instruments provide Market Depth data
- When you're finished using Market Depth data, unsubscribe using the `market_book_release()` function
- The function is similar to the MQL5 `MarketBookGet()` function

## BookInfo Structure

Each entry in the Market Depth returned by `market_book_get()` contains the following fields:

| Field | Type | Description |
|-------|------|-------------|
| `type` | int | Order type: 0 - sell order (Offer/Ask), 1 - buy order (Bid) |
| `price` | float | Price specified in the order |
| `volume` | float | Volume (in lots) at the specified price level |
| `volume_real` | float | Volume with greater precision (when available) |

## Usage Examples

### Basic Market Depth Retrieval

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
if not mt5.market_book_add("EURUSD"):
    print("Failed to subscribe to EURUSD market depth, error code =", mt5.last_error())
    mt5.shutdown()
    quit()

# Get market depth data
market_depth = mt5.market_book_get("EURUSD")
if market_depth:
    print("\nEURUSD Market Depth:")
    print("Total orders in book:", len(market_depth))
    
    # Separate buy and sell orders
    buy_orders = [order for order in market_depth if order.type == 1]
    sell_orders = [order for order in market_depth if order.type == 0]
    
    # Sort buy orders by price (descending)
    buy_orders = sorted(buy_orders, key=lambda order: order.price, reverse=True)
    
    # Sort sell orders by price (ascending)
    sell_orders = sorted(sell_orders, key=lambda order: order.price)
    
    print("\nBuy Orders (Bids):")
    for i, order in enumerate(buy_orders, 1):
        print(f"{i}. Price: {order.price}, Volume: {order.volume}")
        
    print("\nSell Orders (Asks):")
    for i, order in enumerate(sell_orders, 1):
        print(f"{i}. Price: {order.price}, Volume: {order.volume}")
    
    # Calculate market depth statistics
    total_bid_volume = sum(order.volume for order in buy_orders)
    total_ask_volume = sum(order.volume for order in sell_orders)
    
    print("\nMarket Depth Statistics:")
    print(f"Total Bid Volume: {total_bid_volume}")
    print(f"Total Ask Volume: {total_ask_volume}")
    print(f"Volume Ratio (Bid/Ask): {total_bid_volume/total_ask_volume:.2f}" if total_ask_volume > 0 else "Volume Ratio: N/A")
    print(f"Current Spread: {sell_orders[0].price - buy_orders[0].price:.5f}" if buy_orders and sell_orders else "Current Spread: N/A")
else:
    print("Failed to get market depth, error code =", mt5.last_error())

# Unsubscribe from market depth updates
mt5.market_book_release("EURUSD")

# Shut down the connection when done
mt5.shutdown()
```

### Converting Market Depth to DataFrame

```python
import MetaTrader5 as mt5
import pandas as pd

# Establish connection to the MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

# Select the symbol in MarketWatch
if not mt5.symbol_select("EURUSD", True):
    print("Failed to select EURUSD")
    mt5.shutdown()
    quit()

# Subscribe to market depth updates
if not mt5.market_book_add("EURUSD"):
    print("Failed to subscribe to EURUSD market depth, error code =", mt5.last_error())
    mt5.shutdown()
    quit()

# Get market depth data
market_depth = mt5.market_book_get("EURUSD")
if market_depth:
    # Convert to list of dictionaries
    book_data = []
    for item in market_depth:
        book_dict = item._asdict()
        book_dict['side'] = 'Bid' if item.type == 1 else 'Ask'
        book_data.append(book_dict)
    
    # Create DataFrame
    df = pd.DataFrame(book_data)
    
    # Add additional columns
    if not df.empty:
        # Calculate cumulative volume
        bids = df[df['side'] == 'Bid'].sort_values(by='price', ascending=False).copy()
        asks = df[df['side'] == 'Ask'].sort_values(by='price').copy()
        
        if not bids.empty:
            bids['cumulative_volume'] = bids['volume'].cumsum()
        
        if not asks.empty:
            asks['cumulative_volume'] = asks['volume'].cumsum()
        
        # Recombine the data
        dom_df = pd.concat([bids, asks]).reset_index(drop=True)
        
        print("Market Depth as DataFrame:")
        print(dom_df[['side', 'price', 'volume', 'cumulative_volume']])
        
        # Summary statistics
        print("\nSummary Statistics:")
        summary = dom_df.groupby('side').agg({
            'volume': 'sum',
            'price': ['count', 'min', 'max']
        })
        print(summary)
        
        # Calculate spread
        if not bids.empty and not asks.empty:
            best_bid = bids.iloc[0]['price']
            best_ask = asks.iloc[0]['price']
            spread = best_ask - best_bid
            spread_pips = spread * 10000  # For 4-digit forex pairs
            
            print(f"\nBest Bid: {best_bid}")
            print(f"Best Ask: {best_ask}")
            print(f"Spread: {spread:.5f} ({spread_pips:.1f} pips)")
else:
    print("Failed to get market depth, error code =", mt5.last_error())

# Unsubscribe from market depth updates
mt5.market_book_release("EURUSD")

# Shut down the connection when done
mt5.shutdown()
```

### Continuous Market Depth Monitoring

```python
import MetaTrader5 as mt5
import pandas as pd
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

# Subscribe to market depth updates
if not mt5.market_book_add("EURUSD"):
    print("Failed to subscribe to EURUSD market depth, error code =", mt5.last_error())
    mt5.shutdown()
    quit()

try:
    print("Monitoring EURUSD market depth for 30 seconds (Ctrl+C to stop)...")
    start_time = time.time()
    
    while time.time() - start_time < 30:
        # Get market depth data
        market_depth = mt5.market_book_get("EURUSD")
        
        if market_depth:
            # Separate buy and sell orders
            buy_orders = [order for order in market_depth if order.type == 1]
            sell_orders = [order for order in market_depth if order.type == 0]
            
            # Get best bid and ask
            if buy_orders and sell_orders:
                best_bid = max(order.price for order in buy_orders)
                best_ask = min(order.price for order in sell_orders)
                spread = best_ask - best_bid
                
                # Calculate volumes
                bid_volume = sum(order.volume for order in buy_orders)
                ask_volume = sum(order.volume for order in sell_orders)
                
                # Print current state
                print(f"\n[{time.strftime('%H:%M:%S')}] Market Depth Overview:")
                print(f"Best Bid: {best_bid:.5f}, Best Ask: {best_ask:.5f}, Spread: {spread:.5f}")
                print(f"Bid Volume: {bid_volume:.2f}, Ask Volume: {ask_volume:.2f}")
                print(f"Bid/Ask Ratio: {(bid_volume/ask_volume):.2f}" if ask_volume > 0 else "Bid/Ask Ratio: N/A")
                print(f"Order Book Imbalance: {((bid_volume - ask_volume) / (bid_volume + ask_volume)):.2%}" if (bid_volume + ask_volume) > 0 else "Order Book Imbalance: N/A")
                
                # Display top levels
                print("\nTop 3 Bid Levels:")
                sorted_bids = sorted(buy_orders, key=lambda x: x.price, reverse=True)
                for i, order in enumerate(sorted_bids[:3], 1):
                    print(f"{i}. Price: {order.price:.5f}, Volume: {order.volume:.2f}")
                
                print("\nTop 3 Ask Levels:")
                sorted_asks = sorted(sell_orders, key=lambda x: x.price)
                for i, order in enumerate(sorted_asks[:3], 1):
                    print(f"{i}. Price: {order.price:.5f}, Volume: {order.volume:.2f}")
            else:
                print("Incomplete market depth data (missing bids or asks)")
        else:
            print("Failed to get market depth, error code =", mt5.last_error())
            
        time.sleep(5)  # Update every 5 seconds
        
except KeyboardInterrupt:
    print("\nMonitoring interrupted by user")
finally:
    # Unsubscribe from market depth updates
    mt5.market_book_release("EURUSD")
    print("Unsubscribed from EURUSD market depth")
    
    # Shut down the connection when done
    mt5.shutdown()
```

## Market Depth Analysis Techniques

Market Depth data provided by `market_book_get()` can be analyzed in various ways:

1. **Supply and Demand Imbalance**: Compare total volume on the bid side versus the ask side to identify potential price direction
2. **Price Pressure Points**: Identify price levels with unusually large orders that may act as support or resistance
3. **Order Book Depth**: Assess the concentration of orders at different price levels to gauge market liquidity
4. **Order Flow Analysis**: Track changes in the order book over time to identify patterns
5. **Market Microstructure**: Analyze the distribution of orders to understand market participant behavior

## Related Functions

- `market_book_add()`: Subscribes to Market Depth change events (must be called before `market_book_get()`)
- `market_book_release()`: Cancels subscription to Market Depth change events
- `symbol_select()`: Selects a symbol in the MarketWatch window (required before using Market Depth functions)
- `symbol_info()`: Gets comprehensive information about a symbol
- `symbol_info_tick()`: Gets the latest price tick for a symbol
- `initialize()`: Establishes a connection to the MetaTrader 5 terminal
- `shutdown()`: Closes the connection to the MetaTrader 5 terminal
- `last_error()`: Returns the last error code and description

## Common Use Cases

1. **Algorithmic Trading**: Develop strategies based on order book imbalances and dynamics
2. **Risk Management**: Assess market liquidity before executing large orders
3. **Market Making**: Adjust pricing based on the current state of the order book
4. **Order Execution Analysis**: Understand the impact of your orders on the market
5. **Liquidity Analysis**: Identify times when markets have adequate depth for trading

## Error Handling

When `market_book_get()` fails:
1. It returns `None`
2. Check the error with `last_error()`
3. Verify that the symbol name is correct
4. Ensure you have first subscribed using `market_book_add()`
5. Confirm that your broker provides Market Depth data for the symbol

Common errors:
- Symbol not found in the list of available symbols
- Not subscribed to Market Depth events (forgot to call `market_book_add()`)
- Market Depth data not available for the specified symbol
- Terminal connectivity issues

## Best Practices

1. Always call `market_book_add()` before attempting to get Market Depth data
2. Check that the return value is not `None` before processing
3. Use appropriate exception handling when working with Market Depth data
4. Remember to unsubscribe with `market_book_release()` when finished
5. Consider caching Market Depth data if you need to analyze it extensively
6. Always call `shutdown()` when finished with MetaTrader 5 operations

## Implementation Notes

The `market_book_get` function provides a snapshot of the current Market Depth at the time it's called. For real-time updates, you need to call this function repeatedly in a loop with appropriate time intervals.

Market Depth data is particularly valuable for highly liquid markets where the order book changes frequently. However, it may be less useful for illiquid markets or instruments where the order book is sparse.
