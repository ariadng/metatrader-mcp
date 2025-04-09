# MetaTrader 5 Python API: `history_deals_get` Function

## Overview

The `history_deals_get` function retrieves detailed information about deals from the trading history with the ability to filter by time interval, symbol group, order ticket, or position ticket. This function is essential for analyzing historical trade executions, calculating performance metrics, and conducting detailed trade analysis. A deal in MetaTrader 5 represents an actual execution of an order, which may include opening a position, closing a position, or a partial close operation.

## Function Syntax

The function has multiple call variants depending on the filtering requirements:

### Variant 1: Get deals within a time interval with optional group filtering
```python
history_deals_get(
   date_from,            # date the deals are requested from
   date_to,              # date, up to which the deals are requested
   group="GROUP"         # optional filter for selecting deals by symbols
)
```

### Variant 2: Get deals by order ticket
```python
history_deals_get(
   ticket=TICKET         # order ticket
)
```

### Variant 3: Get deals by position ticket
```python
history_deals_get(
   position=POSITION     # position ticket
)
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `date_from` | datetime or int | Date from which deals are requested. Can be set as a `datetime` object or as the number of seconds elapsed since January 1, 1970 (Unix timestamp). Required unnamed parameter in Variant 1. |
| `date_to` | datetime or int | Date up to which deals are requested. Can be set as a `datetime` object or as the number of seconds elapsed since January 1, 1970 (Unix timestamp). Required unnamed parameter in Variant 1. |
| `group` | string | Optional named parameter. Filter for arranging a group of necessary symbols. If specified, the function returns only deals meeting the specified criteria for symbol names. |
| `ticket` | integer | Optional named parameter. Ticket of an order (stored in DEAL_ORDER) for which all deals should be received. If specified, other filters are not applied. |
| `position` | integer | Optional named parameter. Ticket of a position (stored in DEAL_POSITION_ID) for which all deals should be received. If specified, other filters are not applied. |

## Return Value

Returns information in the form of a named tuple structure (namedtuple) containing an array of deal objects. Each deal object contains the following fields:

| Field | Description |
|-------|-------------|
| `ticket` | Deal ticket number |
| `order` | Order ticket that triggered the deal |
| `time` | Deal execution time (in seconds since 1970.01.01) |
| `time_msc` | Deal execution time in milliseconds (since 1970.01.01) |
| `type` | Deal type (0-BUY, 1-SELL, etc.) |
| `entry` | Deal entry type (0-IN, 1-OUT, 2-INOUT) |
| `magic` | Magic number (ID assigned by an expert advisor) |
| `position_id` | Position ID this deal affects |
| `reason` | Deal execution reason code |
| `volume` | Deal volume |
| `price` | Deal price |
| `commission` | Deal commission |
| `swap` | Accumulated swap at the moment of the deal |
| `profit` | Financial result of the deal |
| `fee` | Additional fees |
| `symbol` | Deal symbol |
| `comment` | Deal comment |
| `external_id` | Deal ID in an external trading system |

Returns `None` in case of an error. The error information can be obtained using the `last_error()` function.

## Important Notes

- You must call `initialize()` to establish a connection to the MetaTrader 5 terminal before using `history_deals_get()`
- The function is similar to the MQL5 functions combination of `HistoryDealsTotal` and `HistoryDealSelect`
- This function allows receiving all historical deals within a specified period with a single call
- For the `group` parameter, multiple conditions can be separated by commas
- The `group` parameter can use wildcards with the asterisk (*) symbol for pattern matching
- The logical negation symbol (!) can be used for exclusion in the `group` parameter
- In the `group` parameter, inclusion conditions should be specified first, followed by exclusion conditions
- For example, `group="*, !EUR"` means deals for all symbols should be selected first and the ones containing "EUR" in symbol names should be excluded afterwards
- When filtering by order ticket, all deals executed as part of that order will be returned
- When filtering by position ID, all deals related to that position will be returned, including opening, partial closing, and full closing deals
- The function is optimized for retrieving multiple deals at once
- It's more efficient to use this function instead of making multiple individual deal requests
- When working with the returned data, consider using pandas DataFrame for easier data manipulation and analysis

## Usage Examples

### Example 1: Retrieving Historical Deals for a Specific Symbol Group

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

# Get historical deals for GBP pairs
gbp_deals = mt5.history_deals_get(from_date, to_date, group="*GBP*")

if gbp_deals is None:
    print("No history deals with GBP pairs, error code =", mt5.last_error())
elif len(gbp_deals) > 0:
    print(f"Retrieved {len(gbp_deals)} historical deals for GBP pairs")
    
    # Convert the data to a pandas DataFrame for better presentation
    df = pd.DataFrame(list(gbp_deals), columns=gbp_deals[0]._asdict().keys())
    
    # Convert time in seconds to datetime format
    df['time'] = pd.to_datetime(df['time'], unit='s')
    
    # Display the deals data
    print(df)
    
    # Calculate total profit for these deals
    total_profit = df['profit'].sum()
    print(f"Total profit from GBP pairs: {total_profit}")

# Shut down connection to the MetaTrader 5 terminal
mt5.shutdown()
```

### Example 2: Complex Symbol Filtering and Profit Analysis

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

# Get deals excluding EUR and GBP pairs
deals = mt5.history_deals_get(from_date, to_date, group="*,!*EUR*,!*GBP*")

if deals is None:
    print("No deals found with the specified filter, error code =", mt5.last_error())
elif len(deals) > 0:
    print(f"Retrieved {len(deals)} deals excluding EUR and GBP pairs")
    
    # Convert to DataFrame
    df = pd.DataFrame(list(deals), columns=deals[0]._asdict().keys())
    
    # Convert time to datetime
    df['time'] = pd.to_datetime(df['time'], unit='s')
    
    # Filter out non-trading deals (such as deposits, withdrawals)
    trading_deals = df[df['symbol'] != '']
    
    if not trading_deals.empty:
        # Group by symbol and calculate statistics
        symbol_stats = trading_deals.groupby('symbol').agg({
            'ticket': 'count',
            'volume': 'sum',
            'profit': 'sum'
        }).reset_index()
        
        symbol_stats.columns = ['Symbol', 'Number of Deals', 'Total Volume', 'Total Profit']
        
        # Calculate win rate by symbol
        def calculate_win_rate(symbol_df):
            profitable_deals = len(symbol_df[symbol_df['profit'] > 0])
            total_deals = len(symbol_df)
            return (profitable_deals / total_deals * 100) if total_deals > 0 else 0
        
        for symbol in symbol_stats['Symbol']:
            symbol_df = trading_deals[trading_deals['symbol'] == symbol]
            win_rate = calculate_win_rate(symbol_df)
            symbol_stats.loc[symbol_stats['Symbol'] == symbol, 'Win Rate (%)'] = win_rate
        
        print("\nTrading Statistics by Symbol:")
        print(symbol_stats)
        
        # Plot profit by symbol
        plt.figure(figsize=(12, 6))
        plt.bar(symbol_stats['Symbol'], symbol_stats['Total Profit'])
        plt.title('Profit by Symbol (Excluding EUR and GBP Pairs)')
        plt.xlabel('Symbol')
        plt.ylabel('Profit')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.show()
        
        # Plot win rate by symbol
        plt.figure(figsize=(12, 6))
        plt.bar(symbol_stats['Symbol'], symbol_stats['Win Rate (%)'])
        plt.title('Win Rate by Symbol (Excluding EUR and GBP Pairs)')
        plt.xlabel('Symbol')
        plt.ylabel('Win Rate (%)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.show()
    else:
        print("No trading deals found in the selected data")

# Shut down connection to the MetaTrader 5 terminal
mt5.shutdown()
```

### Example 3: Analyzing All Deals Associated with a Position

```python
import MetaTrader5 as mt5
import pandas as pd

# Establish connection to MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

# Define the position ID to analyze
position_id = 530218319  # Replace with an actual position ID

# Get all deals related to this position
position_deals = mt5.history_deals_get(position=position_id)

if position_deals is None:
    print(f"No deals found for position #{position_id}, error code =", mt5.last_error())
elif len(position_deals) > 0:
    print(f"Found {len(position_deals)} deals for position #{position_id}")
    
    # Convert to DataFrame for analysis
    df = pd.DataFrame(list(position_deals), columns=position_deals[0]._asdict().keys())
    
    # Convert times to datetime
    df['time'] = pd.to_datetime(df['time'], unit='s')
    
    # Sort by time
    df = df.sort_values('time')
    
    # Define deal type mapping for better readability
    deal_types = {
        0: "BUY",
        1: "SELL",
        2: "BALANCE",
        3: "CREDIT",
        4: "CHARGE",
        5: "CORRECTION",
        6: "BONUS",
        7: "COMMISSION",
        8: "COMMISSION_DAILY",
        9: "COMMISSION_MONTHLY",
        10: "COMMISSION_AGENT_DAILY",
        11: "COMMISSION_AGENT_MONTHLY",
        12: "INTEREST",
        13: "BUY_CANCELED",
        14: "SELL_CANCELED",
    }
    
    # Define deal entry mapping
    deal_entries = {
        0: "IN",
        1: "OUT",
        2: "INOUT",
    }
    
    # Add readable deal type and entry columns
    df['deal_type'] = df['type'].map(lambda x: deal_types.get(x, f"Unknown ({x})"))
    df['deal_entry'] = df['entry'].map(lambda x: deal_entries.get(x, f"Unknown ({x})"))
    
    # Display position lifecycle
    print("\nPosition Lifecycle:")
    display_cols = ['ticket', 'time', 'deal_type', 'deal_entry', 'volume', 'price', 'profit', 'commission', 'swap']
    print(df[display_cols])
    
    # Calculate position metrics
    print("\nPosition Metrics:")
    
    # Get entry and exit deals
    entry_deals = df[df['entry'] == 0]  # IN deals
    exit_deals = df[df['entry'] == 1]   # OUT deals
    
    if not entry_deals.empty and not exit_deals.empty:
        # Entry details
        entry_deal = entry_deals.iloc[0]
        entry_time = entry_deal['time']
        entry_price = entry_deal['price']
        position_volume = entry_deal['volume']
        position_type = "Long" if entry_deal['type'] == 0 else "Short"
        
        # Exit details
        exit_deal = exit_deals.iloc[-1]
        exit_time = exit_deal['time']
        exit_price = exit_deal['price']
        
        # Calculate duration
        duration = exit_time - entry_time
        
        # Calculate results
        total_profit = df['profit'].sum()
        total_commission = df['commission'].sum()
        total_swap = df['swap'].sum()
        net_result = total_profit + total_commission + total_swap
        
        # Price change calculation based on position type
        if position_type == "Long":
            price_change = (exit_price - entry_price) / entry_price * 100
        else:  # Short
            price_change = (entry_price - exit_price) / entry_price * 100
        
        print(f"Symbol: {entry_deal['symbol']}")
        print(f"Position Type: {position_type}")
        print(f"Volume: {position_volume}")
        print(f"Entry Time: {entry_time}")
        print(f"Entry Price: {entry_price}")
        print(f"Exit Time: {exit_time}")
        print(f"Exit Price: {exit_price}")
        print(f"Duration: {duration}")
        print(f"Price Change: {price_change:.2f}%")
        print(f"Profit: {total_profit}")
        print(f"Commission: {total_commission}")
        print(f"Swap: {total_swap}")
        print(f"Net Result: {net_result}")
    else:
        print("Unable to identify complete entry and exit information for this position")

# Shut down connection to the MetaTrader 5 terminal
mt5.shutdown()
```

### Example 4: Period Performance Analysis with Deals Data

```python
from datetime import datetime, timedelta
import MetaTrader5 as mt5
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Establish connection to MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

# Define the time range (last 6 months)
to_date = datetime.now()
from_date = to_date - timedelta(days=180)

# Get all deals within the period
deals = mt5.history_deals_get(from_date, to_date)

if deals is None:
    print("No deals found in the specified period, error code =", mt5.last_error())
elif len(deals) > 0:
    print(f"Retrieved {len(deals)} deals from {from_date} to {to_date}")
    
    # Convert to DataFrame
    df = pd.DataFrame(list(deals), columns=deals[0]._asdict().keys())
    
    # Convert time to datetime
    df['time'] = pd.to_datetime(df['time'], unit='s')
    
    # Filter out non-trading deals
    trading_deals = df[df['symbol'] != '']
    
    if not trading_deals.empty:
        # Set the date as index for time series analysis
        trading_deals['date'] = trading_deals['time'].dt.date
        daily_performance = trading_deals.groupby('date')['profit'].sum().reset_index()
        daily_performance['date'] = pd.to_datetime(daily_performance['date'])
        
        # Calculate cumulative performance
        daily_performance['cumulative_profit'] = daily_performance['profit'].cumsum()
        
        # Calculate rolling metrics
        daily_performance['7d_avg'] = daily_performance['profit'].rolling(7).mean()
        daily_performance['30d_avg'] = daily_performance['profit'].rolling(30).mean()
        
        # Plot cumulative performance
        plt.figure(figsize=(14, 7))
        plt.plot(daily_performance['date'], daily_performance['cumulative_profit'], label='Cumulative Profit')
        plt.title('Cumulative Trading Performance')
        plt.xlabel('Date')
        plt.ylabel('Profit')
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.tight_layout()
        plt.show()
        
        # Plot daily profit with moving averages
        plt.figure(figsize=(14, 7))
        plt.bar(daily_performance['date'], daily_performance['profit'], alpha=0.5, label='Daily Profit')
        plt.plot(daily_performance['date'], daily_performance['7d_avg'], color='red', label='7-day MA')
        plt.plot(daily_performance['date'], daily_performance['30d_avg'], color='blue', label='30-day MA')
        plt.title('Daily Trading Performance with Moving Averages')
        plt.xlabel('Date')
        plt.ylabel('Profit')
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.tight_layout()
        plt.show()
        
        # Monthly performance
        trading_deals['year_month'] = trading_deals['time'].dt.to_period('M')
        monthly_performance = trading_deals.groupby('year_month')['profit'].sum().reset_index()
        monthly_performance['year_month'] = monthly_performance['year_month'].astype(str)
        
        plt.figure(figsize=(12, 6))
        plt.bar(monthly_performance['year_month'], monthly_performance['profit'])
        plt.title('Monthly Trading Performance')
        plt.xlabel('Month')
        plt.ylabel('Profit')
        plt.xticks(rotation=45)
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        plt.show()
        
        # Performance statistics
        print("\nPerformance Statistics:")
        total_profit = trading_deals['profit'].sum()
        win_deals = trading_deals[trading_deals['profit'] > 0]
        loss_deals = trading_deals[trading_deals['profit'] < 0]
        win_rate = len(win_deals) / len(trading_deals) * 100 if len(trading_deals) > 0 else 0
        
        avg_win = win_deals['profit'].mean() if not win_deals.empty else 0
        avg_loss = loss_deals['profit'].mean() if not loss_deals.empty else 0
        profit_factor = abs(win_deals['profit'].sum() / loss_deals['profit'].sum()) if not loss_deals.empty and loss_deals['profit'].sum() != 0 else float('inf')
        
        print(f"Total Profit: {total_profit:.2f}")
        print(f"Number of Trades: {len(trading_deals)}")
        print(f"Win Rate: {win_rate:.2f}%")
        print(f"Average Win: {avg_win:.2f}")
        print(f"Average Loss: {avg_loss:.2f}")
        print(f"Profit Factor: {profit_factor:.2f}")
    else:
        print("No trading deals found in the selected data")

# Shut down connection to the MetaTrader 5 terminal
mt5.shutdown()
```

## Advantages of Using `history_deals_get()`

1. **Comprehensive Data**: Provides complete information about historical deals in a single call
2. **Flexible Filtering**: Allows filtering deals by time period, symbol group, order ticket, or position ID
3. **Efficient Retrieval**: Optimized for retrieving multiple deals with a single API call
4. **Powerful Grouping**: The group parameter with wildcards enables complex deal filtering
5. **Structured Data**: Returns data in a structured format that can be easily converted to pandas DataFrame
6. **Historical Analysis**: Essential for analyzing past trading executions and outcomes
7. **Performance Metrics**: Facilitates calculation of key performance metrics like win rate and profit factor
8. **Trade Reconciliation**: Enables reconciliation of trading activity with account statements
9. **Time-Based Analysis**: Allows examination of trading patterns across different time periods
10. **Position Tracking**: Provides complete history of position lifecycle from opening to closing
11. **Documentation**: Supports comprehensive record-keeping for compliance and tax purposes
12. **Research**: Provides data for backtesting and strategy improvement research

## Comparison with Related Functions

| Function | Purpose | Key Difference |
|----------|---------|----------------|
| `history_deals_get()` | Get detailed info about deals in history | Returns complete information about historical deals with filtering options |
| `history_deals_total()` | Get count of deals in history | Returns only the count, not deal details |
| `history_orders_get()` | Get detailed info about orders in history | Retrieves information about orders (instructions), not deals (executions) |
| `positions_get()` | Get detailed info about open positions | Deals with current open positions, not historical deals |
| `orders_get()` | Get detailed info about active orders | Retrieves information about active (pending) orders, not historical deals |

## Related Functions

- `history_deals_total()`: Gets the number of deals in the trading history
- `history_orders_total()`: Gets the number of orders in the trading history
- `history_orders_get()`: Retrieves detailed information about orders in history
- `positions_total()`: Gets the number of open positions
- `positions_get()`: Retrieves detailed information about open positions
- `orders_total()`: Gets the number of active orders
- `orders_get()`: Retrieves detailed information about active orders
- `account_info()`: Gets information about the current trading account
- `order_send()`: Sends trading orders to the server
- `initialize()`: Establishes a connection to the MetaTrader 5 terminal
- `shutdown()`: Closes the connection to the MetaTrader 5 terminal

## Common Use Cases

1. **Performance Analysis**: Analyzing trading performance over specific time periods
2. **Trade Journal Creation**: Creating detailed trade journals with execution information
3. **Profit Analysis**: Calculating profit/loss by symbol, time period, or strategy
4. **Trade Verification**: Verifying that trades were executed as expected
5. **Position Lifecycle Tracking**: Tracking the complete lifecycle of positions
6. **Cost Analysis**: Analyzing trading costs including commissions and swaps
7. **Execution Quality Assessment**: Evaluating trade execution quality
8. **Pattern Recognition**: Identifying successful and unsuccessful trading patterns
9. **Risk Management Assessment**: Analyzing risk parameters across different trades
10. **Compliance Reporting**: Generating reports for compliance and regulatory purposes
11. **Tax Documentation**: Preparing data for tax reporting
12. **System Verification**: Verifying that automated trading systems executed as expected
13. **Broker Reconciliation**: Reconciling trade executions with broker statements
14. **Drawdown Analysis**: Analyzing periods of consecutive losses

## Error Handling

Proper error handling is essential when working with the `history_deals_get()` function:

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
    
    # Attempt to get historical deals
    deals = mt5.history_deals_get(from_date, to_date)
    
    if deals is None:
        error_code = mt5.last_error()
        if error_code:
            print(f"Failed to get history deals: error code = {error_code}")
        else:
            print("No deals found in the specified period")
    else:
        print(f"Successfully retrieved {len(deals)} historical deals")
        # Process the deals data
        
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
5. **Memory Limitations**: Insufficient memory to process a large number of deals
6. **Syntax Errors**: Incorrect use of the group parameter syntax
7. **Invalid Filter Combinations**: Attempting to use incompatible filter combinations

## Best Practices

1. **Connection Management**: Always establish a connection with `initialize()` before using history functions
2. **Resource Cleanup**: Always call `shutdown()` when finished with MetaTrader 5 operations
3. **Error Checking**: Always check if the function returns `None` and handle errors appropriately
4. **Data Organization**: Use pandas DataFrames for easier manipulation of the returned data
5. **Time Conversion**: Convert the Unix timestamp to datetime for better readability
6. **Efficient Filtering**: Use the group parameter to filter deals at the API level rather than in Python
7. **Time Range Optimization**: Use reasonable time ranges to avoid overloading the system
8. **Memory Management**: Consider processing large datasets in chunks
9. **Data Validation**: Validate returned data before performing complex operations
10. **Contextual Analysis**: Combine deal data with market data for more comprehensive analysis
11. **Documentation**: Document the purpose and context of historical data retrieval
12. **Regular Updates**: Use incremental updates for continuous monitoring applications

## Implementation Notes

When working with the `history_deals_get()` function, consider these implementation details:

1. **Deal Identification**: Each deal has a unique ticket number
2. **Deal Types**: Various deal types are represented by numeric codes (0-BUY, 1-SELL, etc.)
3. **Deal Entry Types**: Entry types indicate whether the deal is for entering (0-IN) or exiting (1-OUT) a position
4. **Time Fields**: Time values are returned as Unix timestamps (seconds since January 1, 1970)
5. **Position Linkage**: Deals are linked to positions via position_id
6. **Order Linkage**: Deals are linked to the orders that generated them via the order field
7. **Data Structure**: The function returns a tuple of namedtuples, not a list of dictionaries
8. **Filter Priority**: When multiple filters are provided, only one is applied according to priority
9. **History Depth**: The available history depth depends on the broker and server configuration
10. **Data Size Considerations**: Large date ranges can return substantial amounts of data

## Understanding Deal Properties

### Deal Types
- 0: BUY - Buy operation
- 1: SELL - Sell operation
- 2: BALANCE - Balance operation
- 3: CREDIT - Credit operation
- 4: CHARGE - Additional charge
- 5: CORRECTION - Correction operation
- 6: BONUS - Bonus accrual
- 7: COMMISSION - Additional commission
- 8: COMMISSION_DAILY - Daily commission
- 9: COMMISSION_MONTHLY - Monthly commission
- 10: COMMISSION_AGENT_DAILY - Daily agent commission
- 11: COMMISSION_AGENT_MONTHLY - Monthly agent commission
- 12: INTEREST - Interest rate accrual
- 13: BUY_CANCELED - Canceled buy operation
- 14: SELL_CANCELED - Canceled sell operation

### Deal Entry Types
- 0: ENTRY_IN - Entry into a position
- 1: ENTRY_OUT - Exit from a position
- 2: ENTRY_INOUT - Reversal

### Deal Execution Reasons
- 0: REASON_CLIENT - Deal performed as a result of activation of an order placed from a desktop terminal
- 1: REASON_MOBILE - Deal performed as a result of activation of an order placed from a mobile application
- 2: REASON_WEB - Deal performed as a result of activation of an order placed from the web platform
- 3: REASON_EXPERT - Deal performed as a result of activation of an order placed from an MQL5 program
- 4: REASON_SL - Deal performed as a result of Stop Loss activation
- 5: REASON_TP - Deal performed as a result of Take Profit activation
- 6: REASON_SO - Deal performed as a result of the Stop Out event

## Advanced Group Parameter Examples

The `group` parameter in `history_deals_get()` is powerful for filtering deals:

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

These patterns allow for flexible and precise deal filtering directly at the API level.
