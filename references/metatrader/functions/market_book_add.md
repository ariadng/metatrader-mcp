# MetaTrader 5 Python API: `market_book_add` Function

## Overview

The `market_book_add` function subscribes the MetaTrader 5 terminal to the Market Depth change events for a specified financial instrument (symbol). Market Depth (also known as the Order Book or Depth of Market/DOM) shows pending buy and sell orders at different price levels, providing valuable insights into market liquidity and order flow.

## Function Syntax

```python
market_book_add(
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

- You must call `initialize()` to establish a connection to the MetaTrader 5 terminal before calling `market_book_add()`
- Not all brokers and financial instruments provide Market Depth data
- This function only subscribes to Market Depth events; to retrieve the actual Market Depth data, use the `market_book_get()` function
- When you no longer need Market Depth data, unsubscribe using the `market_book_release()` function to free up resources
- The function is similar to the MQL5 `MarketBookAdd()` function

## Related Market Depth Functions

### `market_book_get`

Retrieves the current Market Depth data for a symbol after subscribing with `market_book_add()`.

```python
market_book_get(
   symbol      # financial instrument name
)
```

Returns a tuple of BookInfo entries (similar to the MQL5 `MqlBookInfo` structure), each containing:
- `type` - Order type (0 - sell, 1 - buy)
- `price` - Price
- `volume` - Volume in lots

Returns `None` if an error occurs.

### `market_book_release`

Cancels the subscription to Market Depth change events for a specified symbol.

```python
market_book_release(
   symbol      # financial instrument name
)
```

Returns `True` if successful, otherwise returns `False`.

## Usage Examples

### Basic Market Depth Retrieval

```python
import MetaTrader5 as mt5
import time

# Establish connection to the MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

# Select the symbol in MarketWatch to ensure it's available
if not mt5.symbol_select("EURUSD", True):
    print("Failed to select EURUSD")
    mt5.shutdown()
    quit()

# Subscribe to market depth updates for EURUSD
if mt5.market_book_add("EURUSD"):
    print("Successfully subscribed to EURUSD market depth")
    
    # Get market depth data
    market_depth = mt5.market_book_get("EURUSD")
    if market_depth:
        print("\nEURUSD Market Depth:")
        print("Total orders in book:", len(market_depth))
        
        # Display first 5 buy and sell orders
        buy_orders = [order for order in market_depth if order.type == 1]
        sell_orders = [order for order in market_depth if order.type == 0]
        
        print("\nTop 5 Buy Orders (Bids):")
        for i, order in enumerate(buy_orders[:5], 1):
            print(f"{i}. Price: {order.price}, Volume: {order.volume}")
            
        print("\nTop 5 Sell Orders (Asks):")
        for i, order in enumerate(sell_orders[:5], 1):
            print(f"{i}. Price: {order.price}, Volume: {order.volume}")
    else:
        print("Failed to get market depth, error code =", mt5.last_error())
    
    # Unsubscribe from market depth updates
    mt5.market_book_release("EURUSD")
    print("\nUnsubscribed from EURUSD market depth")
else:
    print("Failed to subscribe to EURUSD market depth, error code =", mt5.last_error())
    print("Note: Market depth may not be available for this symbol or broker")

# Shut down the connection when done
mt5.shutdown()
```

### Real-time Market Depth Monitoring

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
if mt5.market_book_add("EURUSD"):
    print("Monitoring EURUSD market depth for 30 seconds...")
    
    # Function to convert market depth to DataFrame
    def depth_to_dataframe(market_depth):
        if not market_depth:
            return None
            
        # Separate buy and sell orders
        buy_orders = [order._asdict() for order in market_depth if order.type == 1]
        sell_orders = [order._asdict() for order in market_depth if order.type == 0]
        
        # Create DataFrames
        if buy_orders:
            bids_df = pd.DataFrame(buy_orders)
            bids_df = bids_df.sort_values(by='price', ascending=False)
            bids_df['side'] = 'Bid'
        else:
            bids_df = pd.DataFrame()
            
        if sell_orders:
            asks_df = pd.DataFrame(sell_orders)
            asks_df = asks_df.sort_values(by='price', ascending=True)
            asks_df['side'] = 'Ask'
        else:
            asks_df = pd.DataFrame()
            
        # Combine and return
        if not bids_df.empty and not asks_df.empty:
            return pd.concat([bids_df, asks_df])
        elif not bids_df.empty:
            return bids_df
        elif not asks_df.empty:
            return asks_df
        else:
            return None
    
    # Monitor market depth for 30 seconds
    start_time = time.time()
    try:
        while time.time() - start_time < 30:
            market_depth = mt5.market_book_get("EURUSD")
            df = depth_to_dataframe(market_depth)
            
            if df is not None:
                # Calculate total volume on each side
                bid_volume = df[df['side'] == 'Bid']['volume'].sum() if 'Bid' in df['side'].values else 0
                ask_volume = df[df['side'] == 'Ask']['volume'].sum() if 'Ask' in df['side'].values else 0
                
                print(f"\nTimestamp: {time.strftime('%H:%M:%S')}")
                print(f"Total Bid Volume: {bid_volume:.2f}")
                print(f"Total Ask Volume: {ask_volume:.2f}")
                print(f"Volume Ratio (Bid/Ask): {bid_volume/ask_volume:.2f}" if ask_volume > 0 else "Volume Ratio: N/A")
                print(f"Order Book Imbalance: {((bid_volume - ask_volume) / (bid_volume + ask_volume)):.2%}" if (bid_volume + ask_volume) > 0 else "Order Book Imbalance: N/A")
                
                # Display top 3 levels on each side
                top_bids = df[df['side'] == 'Bid'].head(3) if 'Bid' in df['side'].values else pd.DataFrame()
                top_asks = df[df['side'] == 'Ask'].head(3) if 'Ask' in df['side'].values else pd.DataFrame()
                
                if not top_bids.empty:
                    print("\nTop 3 Bid Levels:")
                    for i, (_, row) in enumerate(top_bids.iterrows(), 1):
                        print(f"{i}. Price: {row['price']}, Volume: {row['volume']}")
                
                if not top_asks.empty:
                    print("\nTop 3 Ask Levels:")
                    for i, (_, row) in enumerate(top_asks.iterrows(), 1):
                        print(f"{i}. Price: {row['price']}, Volume: {row['volume']}")
            
            time.sleep(5)  # Update every 5 seconds
            
    except KeyboardInterrupt:
        print("\nMarket depth monitoring interrupted by user")
    finally:
        # Unsubscribe from market depth updates
        mt5.market_book_release("EURUSD")
        print("Unsubscribed from EURUSD market depth")
else:
    print("Failed to subscribe to EURUSD market depth, error code =", mt5.last_error())

# Shut down the connection when done
mt5.shutdown()
```

## Market Depth Analysis Techniques

Market Depth data provides valuable trading insights:

1. **Liquidity Assessment**: Evaluate the volume of orders at different price levels to gauge market liquidity
2. **Order Imbalance**: Compare buy vs. sell order volumes to identify potential price direction
3. **Support/Resistance Levels**: Identify price levels with large order clusters that may act as barriers
4. **Market Sentiment**: Assess the overall balance of buying and selling interest
5. **Order Flow Analysis**: Track changes in the order book over time to predict price movements

## BookInfo Structure

Each entry in the Market Depth returned by `market_book_get()` contains the following fields:

| Field | Type | Description |
|-------|------|-------------|
| `type` | int | Order type: 0 - sell order (Offer/Ask), 1 - buy order (Bid) |
| `price` | float | Price specified in the order |
| `volume` | float | Volume (in lots) at the specified price level |
| `volume_real` | float | Volume with greater precision (when available) |

## Related Functions

- `symbol_select()`: Selects a symbol in the MarketWatch window (required before using Market Depth functions)
- `symbol_info()`: Gets comprehensive information about a symbol
- `symbol_info_tick()`: Gets the latest price tick for a symbol
- `initialize()`: Establishes a connection to the MetaTrader 5 terminal
- `shutdown()`: Closes the connection to the MetaTrader 5 terminal
- `last_error()`: Returns the last error code and description

## Common Use Cases

1. **Algorithmic Trading**: Make trading decisions based on order book imbalances
2. **Liquidity Analysis**: Assess market depth before placing large orders
3. **Market Microstructure Analysis**: Study order flow and market dynamics
4. **HFT (High-Frequency Trading)**: Respond quickly to changes in the order book
5. **Market Making**: Manage bid-ask spreads based on order book conditions

## Error Handling

When `market_book_add()` fails:
1. It returns `False`
2. Check the error with `last_error()`
3. Verify that the symbol name is correct
4. Ensure the symbol is available in the Market Watch using `symbol_select()`
5. Confirm that your broker provides Market Depth data for the symbol

Common errors:
- Symbol not found in the list of available symbols
- Market Depth data not available for the specified symbol
- Terminal connectivity issues

## Best Practices

1. Always select the symbol with `symbol_select()` before subscribing to its Market Depth
2. Check the return value of `market_book_add()` to confirm successful subscription
3. When finished, always unsubscribe with `market_book_release()` to free up resources
4. Implement error handling for cases where Market Depth data is unavailable
5. Be mindful of update frequency to avoid overwhelming your application
6. Always call `shutdown()` when finished with MetaTrader 5 operations

## Implementation Notes

The Market Depth functions (`market_book_add()`, `market_book_get()`, and `market_book_release()`) work together as a system:

1. `market_book_add()` - Subscribes to updates
2. `market_book_get()` - Retrieves the current state of the order book
3. `market_book_release()` - Unsubscribes from updates

Not all brokers and symbols provide Market Depth data, so your application should handle cases where these functions may not work as expected.
