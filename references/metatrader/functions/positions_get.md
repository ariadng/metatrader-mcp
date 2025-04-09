# MetaTrader 5 Python API: `positions_get` Function

## Overview

The `positions_get` function retrieves detailed information about currently open positions in the trading account. This function allows for filtering positions by symbol, group of symbols, or specific position ticket. It provides comprehensive data about each position, including order type, volume, open price, stop loss, take profit, and more. This function is essential for position management, risk assessment, and trading algorithm development.

## Function Syntax

The function has multiple call variants depending on the filtering requirements:

### Variant 1: Get all open positions
```python
positions_get()
```

### Variant 2: Get positions for a specific symbol
```python
positions_get(
   symbol="SYMBOL"      # symbol name
)
```

### Variant 3: Get positions for a group of symbols
```python
positions_get(
   group="GROUP"        # filter for selecting positions by symbols
)
```

### Variant 4: Get a position by its ticket number
```python
positions_get(
   ticket=TICKET        # position ticket
)
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `symbol` | string | Optional. Symbol name to filter positions. If specified, the `ticket` parameter is ignored. |
| `group` | string | Optional. Filter for arranging a group of necessary symbols. If specified, the function returns only positions meeting the specified criteria for symbol names. |
| `ticket` | integer | Optional. Position ticket (POSITION_TICKET). Ignored if `symbol` is specified. |

## Return Value

Returns information in the form of a named tuple structure (namedtuple) containing an array of position objects. Each position object contains the following fields:

| Field | Description |
|-------|-------------|
| `ticket` | Position ticket number |
| `time` | Position open time |
| `type` | Position type (0 - buy, 1 - sell) |
| `magic` | Position magic number (used for identifying positions placed by an EA) |
| `identifier` | Position identifier |
| `reason` | Position opening reason |
| `volume` | Position volume |
| `price_open` | Position open price |
| `sl` | Stop Loss level |
| `tp` | Take Profit level |
| `price_current` | Current price of the position's symbol |
| `swap` | Accumulated swap |
| `profit` | Current profit |
| `symbol` | Position symbol |
| `comment` | Position comment |
| `time_update` | Position update time (server time) |
| `time_msc` | Position opening time in milliseconds (since 1970.01.01) |
| `time_update_msc` | Position change time in milliseconds (since 1970.01.01) |
| `external_id` | Position identifier in an external trading system |

Returns `None` in case of an error. The error information can be obtained using the `last_error()` function.

## Important Notes

- You must call `initialize()` to establish a connection to the MetaTrader 5 terminal before using `positions_get()`
- The function is similar to the MQL5 functions combination of `PositionsTotal` and `PositionSelect`
- This function allows receiving all open positions within one call
- For the `group` parameter, multiple conditions can be separated by commas
- The `group` parameter can use wildcards with the asterisk (*) symbol for pattern matching
- The logical negation symbol (!) can be used for exclusion in the `group` parameter
- In the `group` parameter, inclusion conditions should be specified first, followed by exclusion conditions
- For example, `group="*, !EUR"` means all positions should be selected except those containing "EUR" in the symbol names
- The function is optimized for retrieving multiple positions at once
- It's more efficient to use this function instead of making multiple individual position requests
- When working with the returned data, consider using pandas DataFrame for easier data manipulation

## Usage Examples

### Example 1: Basic Usage - Get All Positions

```python
import MetaTrader5 as mt5
import pandas as pd

# Set up pandas display options
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1500)

# Establish connection to MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

# Get all open positions
positions = mt5.positions_get()

if positions is None:
    print("No positions, error code =", mt5.last_error())
elif len(positions) > 0:
    print("Total positions:", len(positions))
    
    # Convert the data to a pandas DataFrame for better presentation
    df = pd.DataFrame(list(positions), columns=positions[0]._asdict().keys())
    
    # Convert time in seconds to datetime format
    df['time'] = pd.to_datetime(df['time'], unit='s')
    
    # Optional: Drop some less frequently used columns
    df.drop(['time_update', 'time_msc', 'time_update_msc', 'external_id'], axis=1, inplace=True)
    
    # Display the positions data
    print(df)

# Shut down connection to the MetaTrader 5 terminal
mt5.shutdown()
```

### Example 2: Filtering by Symbol Name

```python
import MetaTrader5 as mt5
import pandas as pd

# Set up pandas display options
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1500)

# Establish connection to MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

# Get open positions for a specific symbol
symbol = "EURUSD"
positions = mt5.positions_get(symbol=symbol)

if positions is None:
    print(f"No positions on {symbol}, error code =", mt5.last_error())
elif len(positions) > 0:
    print(f"Total positions on {symbol}:", len(positions))
    
    # Display all positions for the symbol
    for position in positions:
        print(f"Ticket: {position.ticket}, Type: {'Buy' if position.type == 0 else 'Sell'}, "
              f"Volume: {position.volume}, Open Price: {position.price_open}, "
              f"Current Price: {position.price_current}, Profit: {position.profit}")

# Shut down connection to the MetaTrader 5 terminal
mt5.shutdown()
```

### Example 3: Using Group Filtering and Data Processing

```python
import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

# Set up pandas display options
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1500)

# Establish connection to MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

# Get positions for all USD pairs
usd_positions = mt5.positions_get(group="*USD*")

if usd_positions is None:
    print("No positions with USD pairs, error code =", mt5.last_error())
elif len(usd_positions) > 0:
    print(f"Found {len(usd_positions)} positions with USD pairs")
    
    # Convert the data to a pandas DataFrame
    df = pd.DataFrame(list(usd_positions), columns=usd_positions[0]._asdict().keys())
    
    # Convert time in seconds to datetime format
    df['time'] = pd.to_datetime(df['time'], unit='s')
    
    # Calculate the duration of each position
    current_time = datetime.now()
    df['duration_days'] = (current_time - df['time']).dt.total_seconds() / (24 * 60 * 60)
    
    # Separate buy and sell positions
    buy_positions = df[df['type'] == 0]
    sell_positions = df[df['type'] == 1]
    
    # Display summary statistics
    print("\nTotal Profit/Loss for USD pairs:", df['profit'].sum())
    print("Average Profit/Loss per position:", df['profit'].mean())
    print("\nBuy Positions:", len(buy_positions))
    print("Buy Positions P/L:", buy_positions['profit'].sum())
    print("\nSell Positions:", len(sell_positions))
    print("Sell Positions P/L:", sell_positions['profit'].sum())
    
    # Calculate risk exposure
    total_buy_volume = buy_positions['volume'].sum()
    total_sell_volume = sell_positions['volume'].sum()
    net_exposure = total_buy_volume - total_sell_volume
    
    print(f"\nNet Market Exposure: {net_exposure:.2f} lots")
    
    # Optional: Create a simple visualization of profit distribution
    plt.figure(figsize=(10, 6))
    plt.bar(df['symbol'], df['profit'])
    plt.title('Profit/Loss by Currency Pair')
    plt.xlabel('Currency Pair')
    plt.ylabel('Profit/Loss')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Shut down connection to the MetaTrader 5 terminal
mt5.shutdown()
```

### Example 4: Retrieving a Specific Position by Ticket

```python
import MetaTrader5 as mt5

# Establish connection to MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

# Define the position ticket to look up
ticket = 548297723  # Replace with an actual position ticket

# Get the specific position
position = mt5.positions_get(ticket=ticket)

if position is None:
    print(f"Position with ticket {ticket} not found, error code =", mt5.last_error())
elif len(position) > 0:
    # Display the retrieved position details
    position = position[0]  # Extract from tuple, as positions_get always returns a tuple
    
    # Print comprehensive position information
    print(f"Position Information for Ticket #{position.ticket}:")
    print(f"Symbol: {position.symbol}")
    print(f"Type: {'Buy' if position.type == 0 else 'Sell'}")
    print(f"Volume: {position.volume}")
    print(f"Open Price: {position.price_open}")
    print(f"Current Price: {position.price_current}")
    print(f"Stop Loss: {position.sl}")
    print(f"Take Profit: {position.tp}")
    print(f"Swap: {position.swap}")
    print(f"Profit: {position.profit}")
    print(f"Open Time: {pd.to_datetime(position.time, unit='s')}")
    print(f"Magic Number: {position.magic}")
    print(f"Comment: {position.comment}")

# Shut down connection to the MetaTrader 5 terminal
mt5.shutdown()
```

## Advantages of Using `positions_get()`

1. **Comprehensive Data**: Provides complete information about open positions in a single call
2. **Flexible Filtering**: Allows filtering positions by symbol, group of symbols, or ticket number
3. **Efficient Retrieval**: Optimized for retrieving multiple positions with a single API call
4. **Powerful Grouping**: The group parameter with wildcards enables complex position filtering
5. **Structured Data**: Returns data in a structured format that can be easily converted to pandas DataFrame
6. **Position Monitoring**: Essential for real-time monitoring of trading system performance
7. **Risk Management**: Facilitates calculation of exposure, margin usage, and potential losses
8. **Portfolio Analysis**: Enables detailed analysis of the current trading portfolio
9. **Order Verification**: Helps verify that positions were opened according to strategy specifications
10. **Integration Potential**: Data can be easily integrated with other Python libraries for analysis

## Comparison with Related Functions

| Function | Purpose | Key Difference |
|----------|---------|----------------|
| `positions_get()` | Get detailed info about open positions | Returns complete information about positions with filtering options |
| `positions_total()` | Get number of open positions | Only returns the count, not position details |
| `orders_get()` | Get detailed info about pending orders | Deals with pending orders, not active positions |
| `history_orders_get()` | Get detailed info about historical orders | Retrieves closed orders from history, not current open positions |
| `history_deals_get()` | Get detailed info about executed deals | Retrieves completed deals/transactions, not current open positions |
| `account_info()` | Get trading account information | Provides account-level information, not position-specific details |

## Related Functions

- `positions_total()`: Gets the number of open positions
- `orders_total()`: Gets the number of active pending orders
- `orders_get()`: Retrieves detailed information about pending orders
- `history_orders_total()`: Gets the number of orders in history
- `history_orders_get()`: Retrieves orders from trade history
- `history_deals_total()`: Gets the number of deals in history
- `history_deals_get()`: Retrieves deals from trade history
- `account_info()`: Gets information about the current trading account
- `order_send()`: Sends trading orders to the server
- `order_check()`: Validates order parameters before sending
- `symbol_info()`: Gets information about financial instruments
- `symbol_info_tick()`: Gets the latest price data for a symbol
- `initialize()`: Establishes a connection to the MetaTrader 5 terminal
- `shutdown()`: Closes the connection to the MetaTrader 5 terminal

## Common Use Cases

1. **Position Monitoring**: Tracking all open positions in real-time
2. **Risk Assessment**: Calculating total exposure across all or specific currency pairs
3. **Portfolio Management**: Analyzing the distribution of positions across different instruments
4. **Performance Analysis**: Evaluating the profitability of open positions
5. **Position Adjustment**: Identifying positions that need stop-loss or take-profit adjustments
6. **Strategy Validation**: Verifying that positions adhere to strategy rules
7. **Hedging Analysis**: Evaluating the balance between long and short positions
8. **Position Aging**: Monitoring how long positions have been open
9. **Exposure Reporting**: Generating reports on market exposure by instrument or direction
10. **Position Reconciliation**: Reconciling expected positions with actual open positions
11. **Trade System Diagnostics**: Troubleshooting automated trading systems
12. **Correlation Analysis**: Studying the relationship between positions in different instruments

## Error Handling

Proper error handling is essential when working with the `positions_get()` function:

```python
import MetaTrader5 as mt5
import pandas as pd

# Establish connection to MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

try:
    # Attempt to get positions for a specific symbol
    symbol = "EURUSD"
    positions = mt5.positions_get(symbol=symbol)
    
    if positions is None:
        error_code = mt5.last_error()
        if error_code:
            print(f"Error getting positions: error code = {error_code}")
        else:
            print(f"No positions found for {symbol}")
    else:
        print(f"Successfully retrieved {len(positions)} positions for {symbol}")
        # Process the positions data
        
except Exception as e:
    print(f"An unexpected error occurred: {e}")
    
    # Check if connection is still active and try to reconnect if needed
    if not mt5.terminal_info().connected:
        print("Connection to MetaTrader 5 lost, attempting to reconnect...")
        if not mt5.initialize():
            print("Failed to reconnect, error code =", mt5.last_error())

finally:
    # Always ensure proper shutdown
    mt5.shutdown()
```

Common error scenarios:
1. **Connection Issues**: The terminal is not running or connection was lost
2. **Invalid Symbol**: The specified symbol does not exist or is not available
3. **Invalid Ticket**: The specified position ticket does not exist
4. **Syntax Errors**: Incorrect use of the group parameter syntax
5. **Memory Limitations**: Too many positions or insufficient memory to process the request
6. **Permission Issues**: The application doesn't have sufficient permissions to access the data

## Best Practices

1. **Connection Management**: Always establish a connection with `initialize()` before using position functions
2. **Resource Cleanup**: Always call `shutdown()` when finished with MetaTrader 5 operations
3. **Error Checking**: Always check if the function returns `None` and handle errors appropriately
4. **Data Organization**: Use pandas DataFrames for easier manipulation of the returned data
5. **Time Conversion**: Convert the Unix timestamp to datetime for better readability
6. **Efficient Filtering**: Use the group parameter to filter positions at the API level rather than in Python
7. **Memory Optimization**: Drop unnecessary columns if working with large position sets
8. **Batch Processing**: Process positions in batches if dealing with a large number of positions
9. **Regular Updates**: Implement a regular refresh mechanism for real-time monitoring
10. **Context Information**: Store additional context with positions, such as strategy information in comments

## Implementation Notes

When working with the `positions_get()` function, consider these implementation details:

1. **Position Identification**: Each position has a unique ticket number
2. **Position Types**: Type 0 is Buy (long), Type 1 is Sell (short)
3. **Position Volume**: Represented in lots, specific value depends on the broker's lot size
4. **Time Fields**: Time values are returned as Unix timestamps (seconds since January 1, 1970)
5. **Profit Calculation**: The profit field already includes swap costs
6. **Symbol Normalization**: Symbol names may vary between brokers, ensure consistent naming
7. **Data Structure**: The function returns a tuple of namedtuples, not a list of dictionaries
8. **Missing Values**: Some fields may have default values (0, empty string) if not set
9. **Update Frequency**: Position data is updated by the terminal at regular intervals, not instantly
10. **Account Types**: Behavior may differ slightly between netting (one position per symbol) and hedging (multiple positions per symbol) account types

## Advanced Group Parameter Examples

The `group` parameter in `positions_get()` is powerful for filtering positions:

1. **All USD pairs**: `group="*USD*"`
2. **EUR or GBP pairs**: `group="*EUR*,*GBP*"`
3. **Major pairs excluding JPY**: `group="*USD*,*EUR*,*GBP*,*AUD*,*NZD*,*CAD*,!*JPY*"`
4. **Only index CFDs**: `group="*INDEX*,*IDX*"`
5. **Cryptocurrency only**: `group="*BTC*,*ETH*,*LTC*,*XRP*"`
6. **Specific symbols**: `group="EURUSD,GBPUSD,USDJPY"`
7. **All except specific symbols**: `group="*,!EURUSD,!GBPUSD"`
8. **All symbols with a prefix**: `group="FX_*"`
9. **Complex filtering**: `group="*USD*,!EURUSD,!GBPUSD"`
10. **Selecting all**: `group="*"`

These patterns allow for flexible and precise position filtering directly at the API level.
