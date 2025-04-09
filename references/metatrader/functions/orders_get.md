# MetaTrader 5 Python API: `orders_get` Function

## Overview

The `orders_get` function retrieves detailed information about active orders (pending orders) from the MetaTrader 5 terminal. It provides flexibility to retrieve all orders or filter orders by symbol name, groups of symbols, or a specific order ticket. This function is essential for order management, trading automation, and comprehensive account monitoring as it provides detailed information about all pending orders waiting to be executed.

## Function Syntax

There are four ways to call this function:

```python
# Get all active orders on all symbols
orders_get()

# Get active orders for a specific symbol
orders_get(
   symbol="SYMBOL"      # symbol name
)

# Get active orders for a group of symbols matching a pattern
orders_get(
   group="GROUP"        # filter for selecting orders for symbols
)

# Get a specific order by its ticket number
orders_get(
   ticket=TICKET        # order ticket
)
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `symbol` | string | Optional named parameter. Symbol name (e.g., "EURUSD"). If specified, the function returns only active orders for this symbol. If a symbol is specified, the ticket parameter is ignored. |
| `group` | string | Optional named parameter. Filter for arranging a group of necessary symbols. If specified, the function returns only active orders meeting the specified criteria for symbol names. |
| `ticket` | integer | Optional named parameter. Order ticket number. If specified and the symbol parameter is not set, the function returns only the order with this ticket. |

## Return Value

Returns information in the form of a named tuple structure (`namedtuple`). Each named tuple contains the following fields:

| Field | Description |
|-------|-------------|
| `ticket` | Order ticket number |
| `time_setup` | Order setup time |
| `time_setup_msc` | Order setup time in milliseconds |
| `time_done` | Order execution time (0 for active orders) |
| `time_done_msc` | Order execution time in milliseconds (0 for active orders) |
| `time_expiration` | Order expiration time |
| `type` | Order type |
| `type_time` | Order lifetime type |
| `type_filling` | Order filling type |
| `state` | Order state |
| `magic` | Order magic number |
| `volume_current` | Current order volume |
| `volume_initial` | Initial order volume |
| `price_open` | Order price |
| `sl` | Stop Loss level |
| `tp` | Take Profit level |
| `price_current` | Current price of the order symbol |
| `price_stoplimit` | Stop Limit order price |
| `symbol` | Order symbol |
| `comment` | Order comment |
| `external_id` | External system ID (from an exchange) |
| `position_id` | Position identifier |
| `position_by_id` | Identifier of an opposite position |
| `reason` | Reason or source for placing an order |

Returns `None` in case of an error, which can be checked using the `last_error()` function.

## Order Types (type field)

| Constant | Value | Description |
|----------|-------|-------------|
| `ORDER_TYPE_BUY` | 0 | Market Buy order |
| `ORDER_TYPE_SELL` | 1 | Market Sell order |
| `ORDER_TYPE_BUY_LIMIT` | 2 | Buy Limit pending order |
| `ORDER_TYPE_SELL_LIMIT` | 3 | Sell Limit pending order |
| `ORDER_TYPE_BUY_STOP` | 4 | Buy Stop pending order |
| `ORDER_TYPE_SELL_STOP` | 5 | Sell Stop pending order |
| `ORDER_TYPE_BUY_STOP_LIMIT` | 6 | Upon reaching the order price, a pending Buy Limit order is placed at the StopLimit price |
| `ORDER_TYPE_SELL_STOP_LIMIT` | 7 | Upon reaching the order price, a pending Sell Limit order is placed at the StopLimit price |

## Order Lifetime Types (type_time field)

| Constant | Value | Description |
|----------|-------|-------------|
| `ORDER_TIME_GTC` | 0 | Good till canceled |
| `ORDER_TIME_DAY` | 1 | Good till day |
| `ORDER_TIME_SPECIFIED` | 2 | Good till specified date |
| `ORDER_TIME_SPECIFIED_DAY` | 3 | Good till specified day |

## Order Filling Types (type_filling field)

| Constant | Value | Description |
|----------|-------|-------------|
| `ORDER_FILLING_FOK` | 0 | Fill or Kill - execute in full volume or cancel |
| `ORDER_FILLING_IOC` | 1 | Immediate or Cancel - execute as much as possible and cancel the rest |
| `ORDER_FILLING_RETURN` | 2 | Return - partially filled orders remain active |

## Order States (state field)

| Constant | Value | Description |
|----------|-------|-------------|
| `ORDER_STATE_STARTED` | 0 | Order checked, but not yet accepted by broker |
| `ORDER_STATE_PLACED` | 1 | Order accepted |
| `ORDER_STATE_CANCELED` | 2 | Order canceled by client |
| `ORDER_STATE_PARTIAL` | 3 | Order partially executed |
| `ORDER_STATE_FILLED` | 4 | Order fully executed |
| `ORDER_STATE_REJECTED` | 5 | Order rejected |
| `ORDER_STATE_EXPIRED` | 6 | Order expired |
| `ORDER_STATE_REQUEST_ADD` | 7 | Order being registered (placing) |
| `ORDER_STATE_REQUEST_MODIFY` | 8 | Order being modified (modifying) |
| `ORDER_STATE_REQUEST_CANCEL` | 9 | Order being deleted (deleting) |

## Important Notes

- You must call `initialize()` to establish a connection to the MetaTrader 5 terminal before using `orders_get()`
- The function allows retrieving all active orders within one call, similar to the OrdersTotal and OrderSelect tandem in MQL5
- For symbol filtering using the `group` parameter:
  - `*` can be used at the beginning and the end of a string for wildcards
  - Multiple comma-separated conditions can be specified
  - The logical negation symbol `!` can be used for exclusion
  - All conditions are applied sequentially
  - Example: `group="*, !EUR"` means select orders for all symbols first, then exclude those containing "EUR"
- Active orders are those with order states other than FILLED, CANCELED, REJECTED, or EXPIRED

## Usage Examples

### Example 1: Getting All Active Orders

```python
import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime
import pytz

# Set up pandas display options
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1500)

# Establish connection to the MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

# Get all active orders
orders = mt5.orders_get()

if orders is None:
    print("No active orders, error code =", mt5.last_error())
else:
    print("Total active orders:", len(orders))
    
    # Convert to pandas DataFrame for better display
    orders_df = pd.DataFrame(list(orders), columns=orders[0]._asdict().keys())
    
    # Convert time fields to datetime
    timezone = pytz.timezone("Etc/UTC")
    orders_df['time_setup'] = pd.to_datetime(orders_df['time_setup'], unit='s')
    
    # Display key information
    print("\nActive Orders:")
    print(orders_df[['ticket', 'symbol', 'type', 'volume_current', 'price_open', 'sl', 'tp', 'state']])

# Shut down the connection
mt5.shutdown()
```

### Example 2: Filtering Orders by Symbol and Group

```python
import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime
import pytz

# Set up pandas display options
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1500)

# Establish connection to the MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

# Get orders for a specific symbol
symbol = "EURUSD"
symbol_orders = mt5.orders_get(symbol=symbol)

if symbol_orders is None or len(symbol_orders) == 0:
    print(f"No active orders for {symbol}, error code =", mt5.last_error())
else:
    print(f"Active orders for {symbol}: {len(symbol_orders)}")
    
    # Convert to pandas DataFrame
    symbol_orders_df = pd.DataFrame(list(symbol_orders), columns=symbol_orders[0]._asdict().keys())
    
    # Convert time fields to datetime
    timezone = pytz.timezone("Etc/UTC")
    symbol_orders_df['time_setup'] = pd.to_datetime(symbol_orders_df['time_setup'], unit='s')
    
    # Display key information
    print(f"\nActive Orders for {symbol}:")
    print(symbol_orders_df[['ticket', 'type', 'volume_current', 'price_open', 'sl', 'tp', 'state']])

# Get orders for currency pairs (group filter)
currency_orders = mt5.orders_get(group="*USD*,*EUR*")

if currency_orders is None:
    print("No active orders for currencies, error code =", mt5.last_error())
else:
    print(f"\nActive orders for currency pairs (USD and EUR): {len(currency_orders)}")
    
    # Convert to pandas DataFrame
    currency_orders_df = pd.DataFrame(list(currency_orders), columns=currency_orders[0]._asdict().keys())
    
    # Convert time fields to datetime
    currency_orders_df['time_setup'] = pd.to_datetime(currency_orders_df['time_setup'], unit='s')
    
    # Display key information with grouping by symbol
    print("\nOrders by Symbol:")
    symbol_count = currency_orders_df.groupby('symbol').size()
    print(symbol_count)
    
    # Display detailed information
    print("\nDetailed Currency Orders:")
    print(currency_orders_df[['ticket', 'symbol', 'type', 'volume_current', 'price_open', 'state']])

# Shut down the connection
mt5.shutdown()
```

### Example 3: Advanced Order Analysis and Management

```python
import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime, timedelta
import pytz

# Establish connection to the MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

def get_order_type_description(order_type):
    """Convert order type numeric value to descriptive string"""
    types = {
        mt5.ORDER_TYPE_BUY: "Buy",
        mt5.ORDER_TYPE_SELL: "Sell",
        mt5.ORDER_TYPE_BUY_LIMIT: "Buy Limit",
        mt5.ORDER_TYPE_SELL_LIMIT: "Sell Limit",
        mt5.ORDER_TYPE_BUY_STOP: "Buy Stop",
        mt5.ORDER_TYPE_SELL_STOP: "Sell Stop",
        mt5.ORDER_TYPE_BUY_STOP_LIMIT: "Buy Stop Limit",
        mt5.ORDER_TYPE_SELL_STOP_LIMIT: "Sell Stop Limit"
    }
    return types.get(order_type, "Unknown")

def get_order_state_description(order_state):
    """Convert order state numeric value to descriptive string"""
    states = {
        mt5.ORDER_STATE_STARTED: "Started",
        mt5.ORDER_STATE_PLACED: "Placed",
        mt5.ORDER_STATE_CANCELED: "Canceled",
        mt5.ORDER_STATE_PARTIAL: "Partial",
        mt5.ORDER_STATE_FILLED: "Filled",
        mt5.ORDER_STATE_REJECTED: "Rejected",
        mt5.ORDER_STATE_EXPIRED: "Expired",
        mt5.ORDER_STATE_REQUEST_ADD: "Processing",
        mt5.ORDER_STATE_REQUEST_MODIFY: "Modifying",
        mt5.ORDER_STATE_REQUEST_CANCEL: "Canceling"
    }
    return states.get(order_state, "Unknown")

def analyze_orders():
    """Analyze all active orders and provide insights"""
    # Get all active orders
    orders = mt5.orders_get()
    
    if orders is None or len(orders) == 0:
        print("No active orders found")
        return None
    
    # Convert to DataFrame
    df = pd.DataFrame(list(orders), columns=orders[0]._asdict().keys())
    
    # Add human-readable descriptions
    df['type_desc'] = df['type'].apply(get_order_type_description)
    df['state_desc'] = df['state'].apply(get_order_state_description)
    
    # Convert time fields
    timezone = pytz.timezone("Etc/UTC")
    df['time_setup'] = pd.to_datetime(df['time_setup'], unit='s')
    df['time_expiration'] = pd.to_datetime(df['time_expiration'], unit='s')
    
    # Calculate time waiting (how long the order has been active)
    now = datetime.now(timezone)
    df['waiting_hours'] = (now - df['time_setup']).dt.total_seconds() / 3600
    
    # Calculate current distance from order execution (as percentage)
    df['execution_distance_pct'] = 0.0
    
    # For buy limit, price_current should be above price_open to execute
    buy_limit_mask = df['type'] == mt5.ORDER_TYPE_BUY_LIMIT
    df.loc[buy_limit_mask, 'execution_distance_pct'] = (
        (df.loc[buy_limit_mask, 'price_open'] - df.loc[buy_limit_mask, 'price_current']) / 
        df.loc[buy_limit_mask, 'price_current'] * 100
    )
    
    # For sell limit, price_current should be below price_open to execute
    sell_limit_mask = df['type'] == mt5.ORDER_TYPE_SELL_LIMIT
    df.loc[sell_limit_mask, 'execution_distance_pct'] = (
        (df.loc[sell_limit_mask, 'price_current'] - df.loc[sell_limit_mask, 'price_open']) / 
        df.loc[sell_limit_mask, 'price_current'] * 100
    )
    
    # For buy stop, price_current should be below price_open to execute
    buy_stop_mask = df['type'] == mt5.ORDER_TYPE_BUY_STOP
    df.loc[buy_stop_mask, 'execution_distance_pct'] = (
        (df.loc[buy_stop_mask, 'price_open'] - df.loc[buy_stop_mask, 'price_current']) / 
        df.loc[buy_stop_mask, 'price_current'] * 100
    )
    
    # For sell stop, price_current should be above price_open to execute
    sell_stop_mask = df['type'] == mt5.ORDER_TYPE_SELL_STOP
    df.loc[sell_stop_mask, 'execution_distance_pct'] = (
        (df.loc[sell_stop_mask, 'price_current'] - df.loc[sell_stop_mask, 'price_open']) / 
        df.loc[sell_stop_mask, 'price_current'] * 100
    )
    
    # Categorize orders by age
    df['age_category'] = pd.cut(
        df['waiting_hours'], 
        bins=[0, 24, 72, float('inf')],
        labels=['Recent (< 1 day)', 'Medium (1-3 days)', 'Old (> 3 days)']
    )
    
    # Categorize orders by distance to execution
    df['distance_category'] = pd.cut(
        df['execution_distance_pct'].abs(), 
        bins=[0, 0.1, 0.5, 1, float('inf')],
        labels=['Very close (< 0.1%)', 'Close (0.1-0.5%)', 'Medium (0.5-1%)', 'Far (> 1%)']
    )
    
    # Print summary statistics
    print(f"Total active orders: {len(df)}")
    print("\nOrders by Type:")
    print(df.groupby('type_desc').size().sort_values(ascending=False))
    
    print("\nOrders by Symbol:")
    print(df.groupby('symbol').size().sort_values(ascending=False))
    
    print("\nOrders by Age:")
    print(df.groupby('age_category').size())
    
    print("\nOrders by Distance to Execution:")
    print(df.groupby('distance_category').size())
    
    # Find orders close to execution (within 0.1%)
    close_to_execution = df[df['execution_distance_pct'].abs() < 0.1]
    if len(close_to_execution) > 0:
        print("\nOrders Close to Execution (< 0.1% away):")
        for _, order in close_to_execution.iterrows():
            print(f"{order['symbol']} {order['type_desc']} at {order['price_open']:.5f}, "
                  f"current price: {order['price_current']:.5f}, "
                  f"distance: {order['execution_distance_pct']:.3f}%")
    
    # Find old orders (more than 3 days)
    old_orders = df[df['waiting_hours'] > 72]
    if len(old_orders) > 0:
        print("\nOld Orders (> 3 days):")
        for _, order in old_orders.iterrows():
            days_old = order['waiting_hours'] / 24
            print(f"Ticket #{order['ticket']}: {order['symbol']} {order['type_desc']} "
                  f"placed {days_old:.1f} days ago at {order['price_open']:.5f}")
    
    return df

# Run the analysis
orders_analysis = analyze_orders()

# Shut down the connection
mt5.shutdown()
```

## Advantages of Using `orders_get()`

1. **Comprehensive Data**: Provides complete information about each active order in a single call
2. **Flexible Filtering**: Allows filtering by symbol, group patterns, or specific order ticket
3. **Efficient Processing**: Returns all matching orders in a single call, avoiding multiple API requests
4. **Detailed Analysis**: Enables detailed order analysis and management due to the wealth of information provided
5. **Consistent Structure**: Returns data in a structured format (named tuple) that can be easily converted to pandas DataFrame
6. **Advanced Filtering**: The group parameter supports complex filtering with wildcards and exclusions

## Comparison with Related Functions

| Function | Purpose | Key Difference |
|----------|---------|----------------|
| `orders_get()` | Get detailed information about active orders | Returns complete order details, with filtering options |
| `orders_total()` | Get the count of active orders | Returns only a number, not details |
| `positions_get()` | Get information about open positions | Returns executed trades (positions), not pending orders |
| `order_send()` | Send a trade request to place, modify, or delete an order | Performs an action rather than retrieving information |

## Related Functions

- `orders_total()`: Gets the number of active orders
- `positions_get()`: Gets detailed information about open positions
- `positions_total()`: Gets the number of open positions
- `order_send()`: Sends a trade request to place, modify, or delete an order
- `order_calc_margin()`: Calculates the margin required for a specified order type
- `account_info()`: Gets information about the current trading account
- `initialize()`: Establishes a connection to the MetaTrader 5 terminal
- `shutdown()`: Closes the connection to the MetaTrader 5 terminal
- `last_error()`: Returns information about the last error

## Common Use Cases

1. **Order Management Systems**: Building comprehensive order management interfaces and dashboards
2. **Automated Trading**: Monitoring and managing orders placed by trading algorithms
3. **Risk Management**: Analyzing pending orders to assess potential risk exposure
4. **Order Monitoring**: Tracking the status and execution distance of pending orders
5. **Symbol-Specific Analysis**: Analyzing orders for specific symbols or groups of symbols
6. **Order Cleanup**: Identifying and managing old or potentially unwanted orders
7. **Order Modification**: Finding orders that need to be modified based on current market conditions
8. **Performance Analysis**: Tracking order placement and execution patterns over time

## Error Handling

When `orders_get()` encounters errors:
1. It returns `None`
2. Check for errors with `last_error()`
3. Verify that initialization was successful before calling this function
4. Ensure the account has proper permissions to view orders

Common errors include:
- Terminal connectivity issues
- Authentication problems
- Insufficient permissions to access trading functions
- Invalid symbol or group pattern syntax

## Best Practices

1. **Connection Management**: Always establish a connection with `initialize()` before using trading functions
2. **Error Checking**: Always check if the return value is `None` and handle errors appropriately
3. **Efficient Filtering**: Use the appropriate filter parameters to minimize data transfer and processing
4. **Data Conversion**: Convert timestamps to datetime objects for easier manipulation and analysis
5. **DataFrame Usage**: Use pandas DataFrame for easier data manipulation, filtering, and visualization
6. **Descriptive Mappings**: Create mappings for numeric codes to make outputs more human-readable
7. **Resource Cleanup**: Always call `shutdown()` when finished with MetaTrader 5 operations
8. **Batch Processing**: Process all orders in a single call rather than iterative API requests
9. **Regular Monitoring**: Implement regular order monitoring to detect stale or forgotten orders

## Implementation Notes

The `orders_get()` function returns data in the form of a named tuple, which offers several advantages:

1. **Data Structure**: Each field has a meaningful name, making it easy to access specific attributes
2. **Immutability**: Named tuples are immutable, ensuring data integrity
3. **Efficiency**: They are memory-efficient compared to dictionaries
4. **Convertibility**: Can be easily converted to other data structures like dictionaries or DataFrames

For large accounts with many active orders, consider implementing:

1. **Incremental Processing**: Process orders in batches to manage memory usage
2. **Caching**: Cache order information to reduce repeated API calls
3. **Parallel Processing**: For complex analyses, implement parallel processing of order data
4. **Selective Field Access**: Access only the specific fields needed to reduce memory consumption

The `group` parameter is particularly powerful for filtering orders. For example:
- `"*USD*"` - All orders for symbols containing "USD"
- `"*USD*, *EUR*"` - All orders for symbols containing either "USD" or "EUR"
- `"*, !*JPY*"` - All orders except for symbols containing "JPY"
- `"*USD*, !EURUSD"` - All USD symbols except for EURUSD
