# MetaTrader 5 Python API: `history_orders_get` Function

## Overview

The `history_orders_get` function retrieves detailed information about orders from the trading history with the ability to filter by time interval, order ticket, or position ticket. This function is essential for analyzing historical trading activity, auditing trading performance, and evaluating the execution of trading strategies. It provides comprehensive data about each historical order, including type, status, execution time, and price information.

## Function Syntax

The function has multiple call variants depending on the filtering requirements:

### Variant 1: Get orders within a time interval with optional group filtering
```python
history_orders_get(
   date_from,            # date the orders are requested from
   date_to,              # date, up to which the orders are requested
   group="GROUP"         # optional filter for selecting orders by symbols
)
```

### Variant 2: Get a specific order by ticket
```python
history_orders_get(
   ticket=TICKET         # order ticket
)
```

### Variant 3: Get all orders associated with a specific position
```python
history_orders_get(
   position=POSITION     # position ticket
)
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `date_from` | datetime or int | Date from which orders are requested. Can be set as a `datetime` object or as the number of seconds elapsed since January 1, 1970 (Unix timestamp). Required unnamed parameter in Variant 1. |
| `date_to` | datetime or int | Date up to which orders are requested. Can be set as a `datetime` object or as the number of seconds elapsed since January 1, 1970 (Unix timestamp). Required unnamed parameter in Variant 1. |
| `group` | string | Optional named parameter. Filter for arranging a group of necessary symbols. If specified, the function returns only orders meeting the specified criteria for symbol names. |
| `ticket` | integer | Optional named parameter. Order ticket that should be received. If specified, other filters are not applied. |
| `position` | integer | Optional named parameter. Ticket of a position (stored in ORDER_POSITION_ID) for which all orders should be received. If specified, other filters are not applied. |

## Return Value

Returns information in the form of a named tuple structure (namedtuple) containing an array of order objects. Each order object contains the following fields:

| Field | Description |
|-------|-------------|
| `ticket` | Order ticket number |
| `time_setup` | Order setup time |
| `time_setup_msc` | Order setup time in milliseconds |
| `time_done` | Order execution or cancellation time |
| `time_done_msc` | Order execution or cancellation time in milliseconds |
| `time_expiration` | Order expiration time |
| `type` | Order type (0-BUY, 1-SELL, 2-BUY_LIMIT, 3-SELL_LIMIT, 4-BUY_STOP, 5-SELL_STOP, etc.) |
| `type_time` | Order lifetime type |
| `type_filling` | Order filling type |
| `state` | Order state |
| `magic` | Order magic number (ID assigned by an expert advisor) |
| `position_id` | Position ID |
| `position_by_id` | Opposite position ID |
| `reason` | Order creation reason |
| `volume_initial` | Initial order volume |
| `volume_current` | Current order volume |
| `price_open` | Order price |
| `price_current` | Current price of the order symbol |
| `price_stoplimit` | Stop limit order price |
| `sl` | Stop Loss level |
| `tp` | Take Profit level |
| `symbol` | Order symbol |
| `comment` | Order comment |
| `external_id` | Order identifier in an external trading system |

Returns `None` in case of an error. The error information can be obtained using the `last_error()` function.

## Important Notes

- You must call `initialize()` to establish a connection to the MetaTrader 5 terminal before using `history_orders_get()`
- The function is similar to the MQL5 functions combination of `HistoryOrdersTotal` and `HistoryOrderSelect`
- This function allows receiving all historical orders within a specified period with a single call
- For the `group` parameter, multiple conditions can be separated by commas
- The `group` parameter can use wildcards with the asterisk (*) symbol for pattern matching
- The logical negation symbol (!) can be used for exclusion in the `group` parameter
- In the `group` parameter, inclusion conditions should be specified first, followed by exclusion conditions
- For example, `group="*, !EUR"` means orders for all symbols should be selected first and the ones containing "EUR" in symbol names should be excluded afterwards
- When filtering by position ID, all orders related to that position will be returned, including opening, modification, and closing orders
- The function is optimized for retrieving multiple orders at once
- It's more efficient to use this function instead of making multiple individual order requests
- When working with the returned data, consider using pandas DataFrame for easier data manipulation and analysis

## Usage Examples

### Example 1: Retrieving Historical Orders for a Specific Symbol Group

```python
from datetime import datetime
import MetaTrader5 as mt5
import pandas as pd

# Set up pandas display options
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1500)

# Establish connection to MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

# Define the time range
from_date = datetime(2023, 1, 1)
to_date = datetime.now()

# Get historical orders for GBP pairs
gbp_orders = mt5.history_orders_get(from_date, to_date, group="*GBP*")

if gbp_orders is None:
    print("No history orders with GBP pairs, error code =", mt5.last_error())
elif len(gbp_orders) > 0:
    print(f"Retrieved {len(gbp_orders)} historical orders for GBP pairs")
    
    # Convert the data to a pandas DataFrame for better presentation
    df = pd.DataFrame(list(gbp_orders), columns=gbp_orders[0]._asdict().keys())
    
    # Convert time in seconds to datetime format
    df['time_setup'] = pd.to_datetime(df['time_setup'], unit='s')
    df['time_done'] = pd.to_datetime(df['time_done'], unit='s')
    
    # Optional: Drop some less frequently used columns
    df.drop(['time_expiration', 'type_time', 'state', 'position_by_id', 'reason', 
             'volume_current', 'price_stoplimit', 'sl', 'tp'], axis=1, inplace=True)
    
    # Display the order data
    print(df)

# Shut down connection to the MetaTrader 5 terminal
mt5.shutdown()
```

### Example 2: Retrieving and Analyzing Order Details by Order Ticket

```python
import MetaTrader5 as mt5
import pandas as pd

# Establish connection to MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

# Define the order ticket to look up
order_ticket = 530218319  # Replace with an actual order ticket

# Get the specific order
order = mt5.history_orders_get(ticket=order_ticket)

if order is None:
    print(f"Order with ticket {order_ticket} not found, error code =", mt5.last_error())
elif len(order) > 0:
    # Get the order (should be only one)
    order = order[0]
    
    # Define order type mapping for better readability
    order_types = {
        0: "BUY",
        1: "SELL", 
        2: "BUY_LIMIT", 
        3: "SELL_LIMIT", 
        4: "BUY_STOP", 
        5: "SELL_STOP",
        6: "BUY_STOP_LIMIT",
        7: "SELL_STOP_LIMIT"
    }
    
    # Define order state mapping
    order_states = {
        0: "STARTED",
        1: "PLACED",
        2: "CANCELED",
        3: "PARTIAL",
        4: "FILLED",
        5: "REJECTED",
        6: "EXPIRED",
        7: "REQUEST_ADD",
        8: "REQUEST_MODIFY",
        9: "REQUEST_CANCEL"
    }
    
    # Print comprehensive order information
    print(f"Order Information for Ticket #{order.ticket}:")
    print(f"Symbol: {order.symbol}")
    print(f"Type: {order_types.get(order.type, f'Unknown ({order.type})')}")
    print(f"State: {order_states.get(order.state, f'Unknown ({order.state})')}")
    print(f"Volume: {order.volume_initial}")
    print(f"Price: {order.price_open}")
    
    # Convert timestamps to readable format
    setup_time = pd.to_datetime(order.time_setup, unit='s')
    done_time = pd.to_datetime(order.time_done, unit='s')
    
    print(f"Setup Time: {setup_time}")
    print(f"Done Time: {done_time}")
    
    # Calculate execution time if applicable
    if order.time_done > order.time_setup:
        execution_seconds = order.time_done - order.time_setup
        print(f"Execution Time: {execution_seconds} seconds")
    
    print(f"Magic Number: {order.magic}")
    print(f"Position ID: {order.position_id}")
    
    if order.sl > 0:
        print(f"Stop Loss: {order.sl}")
    if order.tp > 0:
        print(f"Take Profit: {order.tp}")
    
    if order.comment:
        print(f"Comment: {order.comment}")

# Shut down connection to the MetaTrader 5 terminal
mt5.shutdown()
```

### Example 3: Analyzing All Orders Associated with a Position

```python
import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime

# Establish connection to MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

# Define the position ID to analyze
position_id = 530218319  # Replace with an actual position ID

# Get all orders related to this position
position_orders = mt5.history_orders_get(position=position_id)

if position_orders is None:
    print(f"No orders found for position #{position_id}, error code =", mt5.last_error())
elif len(position_orders) > 0:
    print(f"Found {len(position_orders)} orders for position #{position_id}")
    
    # Convert to DataFrame for analysis
    df = pd.DataFrame(list(position_orders), columns=position_orders[0]._asdict().keys())
    
    # Convert times to datetime
    df['time_setup'] = pd.to_datetime(df['time_setup'], unit='s')
    df['time_done'] = pd.to_datetime(df['time_done'], unit='s')
    
    # Define order type mapping for better readability
    order_types = {
        0: "BUY",
        1: "SELL", 
        2: "BUY_LIMIT", 
        3: "SELL_LIMIT", 
        4: "BUY_STOP", 
        5: "SELL_STOP",
        6: "BUY_STOP_LIMIT",
        7: "SELL_STOP_LIMIT"
    }
    
    # Add a more readable order type column
    df['order_type'] = df['type'].map(lambda x: order_types.get(x, f"Unknown ({x})"))
    
    # Sort by setup time
    df = df.sort_values('time_setup')
    
    # Analyze the position lifecycle
    print("\nPosition Lifecycle Analysis:")
    
    if len(df) > 0:
        # Get the first and last order
        first_order = df.iloc[0]
        last_order = df.iloc[-1]
        
        # Position duration
        if first_order['time_setup'] != last_order['time_done']:
            position_duration = last_order['time_done'] - first_order['time_setup']
            print(f"Position Duration: {position_duration}")
        
        # Initial volume and symbol
        print(f"Symbol: {first_order['symbol']}")
        print(f"Initial Volume: {first_order['volume_initial']}")
        
        # Check for modifications
        modifications = df[(df['type'] > 1) & (df['time_setup'] > first_order['time_setup'])]
        if len(modifications) > 0:
            print(f"Number of Modifications: {len(modifications)}")
            for i, mod in modifications.iterrows():
                print(f"  - {mod['time_setup']}: {mod['order_type']} at {mod['price_open']}")
        
        # Display the basic DataFrame
        print("\nOrder Details:")
        display_cols = ['ticket', 'time_setup', 'time_done', 'order_type', 
                        'volume_initial', 'price_open', 'sl', 'tp', 'comment']
        print(df[display_cols])

# Shut down connection to the MetaTrader 5 terminal
mt5.shutdown()
```

### Example 4: Statistical Analysis of Historical Orders by Symbol

```python
from datetime import datetime, timedelta
import MetaTrader5 as mt5
import pandas as pd
import matplotlib.pyplot as plt

# Establish connection to MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

# Define the time range (last 3 months)
to_date = datetime.now()
from_date = to_date - timedelta(days=90)

# Get all historical orders
orders = mt5.history_orders_get(from_date, to_date)

if orders is None:
    print("No history orders found, error code =", mt5.last_error())
elif len(orders) > 0:
    print(f"Retrieved {len(orders)} historical orders")
    
    # Convert to DataFrame
    df = pd.DataFrame(list(orders), columns=orders[0]._asdict().keys())
    
    # Convert times to datetime
    df['time_setup'] = pd.to_datetime(df['time_setup'], unit='s')
    
    # Define order type mapping
    order_types = {
        0: "BUY",
        1: "SELL", 
        2: "BUY_LIMIT", 
        3: "SELL_LIMIT", 
        4: "BUY_STOP", 
        5: "SELL_STOP",
        6: "BUY_STOP_LIMIT",
        7: "SELL_STOP_LIMIT"
    }
    df['order_type'] = df['type'].map(lambda x: order_types.get(x, f"Unknown ({x})"))
    
    # Basic statistics by symbol
    symbol_stats = df.groupby('symbol').agg({
        'ticket': 'count',
        'volume_initial': 'sum',
        'time_setup': ['min', 'max']
    }).reset_index()
    
    # Rename columns for clarity
    symbol_stats.columns = ['Symbol', 'Order Count', 'Total Volume', 'First Order', 'Last Order']
    
    print("\nOrder Statistics by Symbol:")
    print(symbol_stats)
    
    # Order type distribution
    order_type_counts = df['order_type'].value_counts()
    
    print("\nOrder Type Distribution:")
    print(order_type_counts)
    
    # Plot order distribution by symbol
    plt.figure(figsize=(12, 6))
    symbol_stats.sort_values('Order Count', ascending=False).plot(
        x='Symbol', y='Order Count', kind='bar', title='Orders by Symbol')
    plt.tight_layout()
    plt.show()
    
    # Plot order type distribution
    plt.figure(figsize=(10, 6))
    order_type_counts.plot(kind='pie', autopct='%1.1f%%', title='Order Types Distribution')
    plt.tight_layout()
    plt.show()
    
    # Order volume analysis
    plt.figure(figsize=(12, 6))
    symbol_stats.sort_values('Total Volume', ascending=False).plot(
        x='Symbol', y='Total Volume', kind='bar', title='Total Volume by Symbol')
    plt.tight_layout()
    plt.show()

# Shut down connection to the MetaTrader 5 terminal
mt5.shutdown()
```

## Advantages of Using `history_orders_get()`

1. **Comprehensive Data**: Provides complete information about historical orders in a single call
2. **Flexible Filtering**: Allows filtering orders by time period, symbol group, order ticket, or position ID
3. **Efficient Retrieval**: Optimized for retrieving multiple orders with a single API call
4. **Powerful Grouping**: The group parameter with wildcards enables complex order filtering
5. **Structured Data**: Returns data in a structured format that can be easily converted to pandas DataFrame
6. **Historical Analysis**: Essential for analyzing past trading decisions and outcomes
7. **Performance Auditing**: Facilitates evaluation of trading strategy performance over time
8. **System Verification**: Helps verify that automated trading systems executed as expected
9. **Time-Based Analysis**: Enables examination of trading patterns across different time periods
10. **Position Tracking**: Allows retrieving all orders associated with a specific position
11. **Documentation**: Supports comprehensive record-keeping for compliance and tax purposes
12. **Research**: Provides data for backtesting and strategy improvement research

## Comparison with Related Functions

| Function | Purpose | Key Difference |
|----------|---------|----------------|
| `history_orders_get()` | Get detailed info about orders in history | Returns complete information about historical orders with filtering options |
| `history_orders_total()` | Get count of orders in history | Returns only the count, not order details |
| `history_deals_get()` | Get detailed info about deals in history | Retrieves information about deals (executions), not orders |
| `positions_get()` | Get detailed info about open positions | Deals with current open positions, not historical orders |
| `orders_get()` | Get detailed info about active orders | Retrieves information about active (pending) orders, not historical ones |

## Related Functions

- `history_orders_total()`: Gets the number of orders in the trading history
- `history_deals_total()`: Gets the number of deals in history
- `history_deals_get()`: Retrieves detailed information about deals in history
- `positions_total()`: Gets the number of open positions
- `positions_get()`: Retrieves detailed information about open positions
- `orders_total()`: Gets the number of active orders
- `orders_get()`: Retrieves detailed information about active orders
- `account_info()`: Gets information about the current trading account
- `order_send()`: Sends trading orders to the server
- `order_check()`: Validates order parameters before sending
- `initialize()`: Establishes a connection to the MetaTrader 5 terminal
- `shutdown()`: Closes the connection to the MetaTrader 5 terminal

## Common Use Cases

1. **Trading Performance Analysis**: Analyzing historical trading decisions and outcomes
2. **Strategy Evaluation**: Evaluating the execution of trading strategies over time
3. **Order Execution Analysis**: Examining how orders were filled, modified, or canceled
4. **Transaction Cost Analysis**: Analyzing execution prices versus requested prices
5. **Position Lifecycle Tracking**: Tracking all orders associated with a specific position
6. **Trade Auditing**: Auditing historical trading activity for compliance purposes
7. **Pattern Recognition**: Identifying patterns in order placement and execution
8. **Market Condition Analysis**: Correlating order behavior with market conditions
9. **Trading Journal Creation**: Creating detailed trading journals with order information
10. **Risk Management Assessment**: Assessing how risk management rules were applied
11. **Behavioral Analysis**: Analyzing trading behavior over different time periods
12. **System Verification**: Verifying that trading systems executed as expected
13. **Reporting**: Generating comprehensive trading reports for stakeholders

## Error Handling

Proper error handling is essential when working with the `history_orders_get()` function:

```python
from datetime import datetime, timedelta
import MetaTrader5 as mt5

# Establish connection to MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

try:
    # Define the time range
    to_date = datetime.now()
    from_date = to_date - timedelta(days=30)
    
    # Attempt to get historical orders
    orders = mt5.history_orders_get(from_date, to_date)
    
    if orders is None:
        error_code = mt5.last_error()
        if error_code:
            print(f"Failed to get history orders: error code = {error_code}")
        else:
            print("No orders found in the specified period")
    else:
        print(f"Successfully retrieved {len(orders)} historical orders")
        # Process the orders data
        
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
2. **Invalid Parameters**: Incorrect date format, invalid ticket number, or invalid position ID
3. **Server Limitations**: Attempting to access history outside the available range
4. **Permission Issues**: The application doesn't have sufficient permissions
5. **Memory Limitations**: Insufficient memory to process a large number of orders
6. **Syntax Errors**: Incorrect use of the group parameter syntax
7. **Invalid Filter Combinations**: Attempting to use incompatible filter combinations

## Best Practices

1. **Connection Management**: Always establish a connection with `initialize()` before using history functions
2. **Resource Cleanup**: Always call `shutdown()` when finished with MetaTrader 5 operations
3. **Error Checking**: Always check if the function returns `None` and handle errors appropriately
4. **Data Organization**: Use pandas DataFrames for easier manipulation of the returned data
5. **Time Conversion**: Convert the Unix timestamp to datetime for better readability
6. **Efficient Filtering**: Use the group parameter to filter orders at the API level rather than in Python
7. **Time Range Optimization**: Use reasonable time ranges to avoid overloading the system
8. **Memory Management**: Consider processing large datasets in chunks
9. **Data Validation**: Validate returned data before performing complex operations
10. **Contextual Analysis**: Combine order data with market data for more comprehensive analysis
11. **Documentation**: Document the purpose and context of historical data retrieval
12. **Regular Updates**: Use incremental updates for continuous monitoring applications

## Implementation Notes

When working with the `history_orders_get()` function, consider these implementation details:

1. **Order Identification**: Each order has a unique ticket number
2. **Order Types**: Various order types are represented by numeric codes (0-BUY, 1-SELL, etc.)
3. **Order States**: States indicate order status (placed, canceled, filled, etc.)
4. **Time Fields**: Time values are returned as Unix timestamps (seconds since January 1, 1970)
5. **Position Linkage**: Orders are linked to positions via position_id
6. **Data Structure**: The function returns a tuple of namedtuples, not a list of dictionaries
7. **Filter Priority**: When multiple filters are provided, only one is applied according to priority
8. **History Depth**: The available history depth depends on the broker and server configuration
9. **Data Size Considerations**: Large date ranges can return substantial amounts of data
10. **Query Performance**: Performance may vary based on the size of the history database

## Advanced Group Parameter Examples

The `group` parameter in `history_orders_get()` is powerful for filtering orders:

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

These patterns allow for flexible and precise order filtering directly at the API level.
