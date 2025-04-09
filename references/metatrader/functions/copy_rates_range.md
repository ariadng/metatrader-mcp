# MetaTrader 5 Python API: `copy_rates_range` Function

## Overview

The `copy_rates_range` function retrieves historical price data (bars/candles) for a specified financial instrument from the MetaTrader 5 terminal within a specific date range. This function is particularly useful for historical analysis, backtesting, and analyzing market behavior during specific time periods of interest.

## Function Syntax

```python
copy_rates_range(
   symbol,       # symbol name
   timeframe,    # timeframe
   date_from,    # date the bars are requested from
   date_to       # date, up to which the bars are requested
)
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `symbol` | string | Financial instrument name (e.g., "EURUSD", "AAPL", etc.). Required unnamed parameter. |
| `timeframe` | TIMEFRAME enum | Timeframe for which the bars are requested. Set by a value from the TIMEFRAME enumeration. Required unnamed parameter. |
| `date_from` | datetime or int | Start date from which bars are requested. Can be specified as a 'datetime' object or as the number of seconds elapsed since January 1, 1970 (Unix time). Bars with open time >= date_from are returned. Required unnamed parameter. |
| `date_to` | datetime or int | End date up to which bars are requested. Can be specified as a 'datetime' object or as the number of seconds elapsed since January 1, 1970 (Unix time). Bars with open time <= date_to are returned. Required unnamed parameter. |

## Return Value

The function returns bars as a numpy array with the following named columns:
- `time` - Bar open time (in seconds since January 1, 1970)
- `open` - Open price
- `high` - High price
- `low` - Low price
- `close` - Close price
- `tick_volume` - Tick volume
- `spread` - Spread
- `real_volume` - Trade volume (if available)

Returns `None` in case of an error, which can be checked using the `last_error()` function.

## TIMEFRAME Enumeration

The timeframe parameter specifies the period of each bar and should be one of the following values:

| Constant | Description |
|----------|-------------|
| TIMEFRAME_M1 | 1 minute |
| TIMEFRAME_M2 | 2 minutes |
| TIMEFRAME_M3 | 3 minutes |
| TIMEFRAME_M4 | 4 minutes |
| TIMEFRAME_M5 | 5 minutes |
| TIMEFRAME_M6 | 6 minutes |
| TIMEFRAME_M10 | 10 minutes |
| TIMEFRAME_M12 | 12 minutes |
| TIMEFRAME_M15 | 15 minutes |
| TIMEFRAME_M20 | 20 minutes |
| TIMEFRAME_M30 | 30 minutes |
| TIMEFRAME_H1 | 1 hour |
| TIMEFRAME_H2 | 2 hours |
| TIMEFRAME_H3 | 3 hours |
| TIMEFRAME_H4 | 4 hours |
| TIMEFRAME_H6 | 6 hours |
| TIMEFRAME_H8 | 8 hours |
| TIMEFRAME_H12 | 12 hours |
| TIMEFRAME_D1 | 1 day |
| TIMEFRAME_W1 | 1 week |
| TIMEFRAME_MN1 | 1 month |

## Important Notes

- You must call `initialize()` to establish a connection to the MetaTrader 5 terminal before using `copy_rates_range()`
- MetaTrader 5 terminal provides bars only within the history available to a user on charts, limited by the "Max. bars in chart" setting
- MetaTrader 5 stores tick and bar open time in UTC time zone, while Python's datetime uses the local time zone by default
- For accurate data retrieval, create datetime objects in UTC time zone to avoid local time zone offsets
- Data received from the MetaTrader 5 terminal has UTC time
- Only bars within the specified date range are returned: bars with open time >= date_from and <= date_to

## Usage Examples

### Basic Date Range Data Retrieval

```python
import MetaTrader5 as mt5
from datetime import datetime
import pytz

# Establish connection to the MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

# Set time zone to UTC
timezone = pytz.timezone("Etc/UTC")

# Create 'datetime' objects in UTC time zone to avoid local time zone offset
from_date = datetime(2023, 1, 1, tzinfo=timezone)
to_date = datetime(2023, 1, 31, tzinfo=timezone)

# Get USDJPY M5 bars within the specified date range
rates = mt5.copy_rates_range("USDJPY", mt5.TIMEFRAME_H1, from_date, to_date)

if rates is not None:
    # Display the data
    print(f"Received {len(rates)} USDJPY H1 bars for January 2023")
    print(f"First bar time: {datetime.fromtimestamp(rates[0][0], tz=timezone)}")
    print(f"Last bar time: {datetime.fromtimestamp(rates[-1][0], tz=timezone)}")
    
    # Show first 5 bars
    print("\nFirst 5 bars:")
    for i in range(min(5, len(rates))):
        bar_time = datetime.fromtimestamp(rates[i][0], tz=timezone)
        print(f"{bar_time}: Open: {rates[i][1]}, High: {rates[i][2]}, Low: {rates[i][3]}, Close: {rates[i][4]}")
else:
    print("Failed to get historical data, error code =", mt5.last_error())

# Shut down the connection when done
mt5.shutdown()
```

### Analyzing Data with Pandas

```python
import MetaTrader5 as mt5
from datetime import datetime
import pandas as pd
import pytz
import numpy as np

# Set pandas display options
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1500)

# Establish connection to the MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

# Set time zone to UTC
timezone = pytz.timezone("Etc/UTC")

# Create 'datetime' objects in UTC time zone
from_date = datetime(2023, 1, 1, tzinfo=timezone)
to_date = datetime(2023, 3, 31, tzinfo=timezone)

# Get EURUSD D1 bars for Q1 2023
rates = mt5.copy_rates_range("EURUSD", mt5.TIMEFRAME_D1, from_date, to_date)

# Shut down the connection when done
mt5.shutdown()

if rates is not None:
    # Create DataFrame from the array
    rates_frame = pd.DataFrame(rates)
    
    # Convert time in seconds into the datetime format
    rates_frame['time'] = pd.to_datetime(rates_frame['time'], unit='s')
    
    # Calculate additional statistics
    rates_frame['daily_range'] = rates_frame['high'] - rates_frame['low']
    rates_frame['daily_return'] = rates_frame['close'].pct_change() * 100
    rates_frame['month'] = rates_frame['time'].dt.month
    
    # Display summary
    print("EURUSD Q1 2023 Summary:")
    print(f"Total trading days: {len(rates_frame)}")
    print(f"Starting price: {rates_frame['close'].iloc[0]:.5f}")
    print(f"Ending price: {rates_frame['close'].iloc[-1]:.5f}")
    print(f"Change: {rates_frame['close'].iloc[-1] - rates_frame['close'].iloc[0]:.5f} ({(rates_frame['close'].iloc[-1]/rates_frame['close'].iloc[0] - 1) * 100:.2f}%)")
    print(f"Highest price: {rates_frame['high'].max():.5f} on {rates_frame.loc[rates_frame['high'].idxmax(), 'time'].strftime('%Y-%m-%d')}")
    print(f"Lowest price: {rates_frame['low'].min():.5f} on {rates_frame.loc[rates_frame['low'].idxmin(), 'time'].strftime('%Y-%m-%d')}")
    print(f"Average daily range: {rates_frame['daily_range'].mean():.5f}")
    print(f"Average daily return: {rates_frame['daily_return'].mean():.2f}%")
    
    # Monthly statistics
    print("\nMonthly Performance:")
    monthly_stats = rates_frame.groupby('month').agg({
        'close': ['first', 'last'],
        'high': 'max',
        'low': 'min',
        'daily_range': 'mean',
        'daily_return': 'mean'
    })
    
    for month in monthly_stats.index:
        month_name = {1: 'January', 2: 'February', 3: 'March'}[month]
        month_data = monthly_stats.loc[month]
        month_change = (month_data[('close', 'last')] / month_data[('close', 'first')] - 1) * 100
        print(f"{month_name}: {month_change:.2f}% change, Range: {month_data[('high', 'max')]:.5f}-{month_data[('low', 'min')]:.5f}")
else:
    print("Failed to get historical data, error code =", mt5.last_error())
```

### Analyzing Special Events or Market Conditions

```python
import MetaTrader5 as mt5
from datetime import datetime, timedelta
import pandas as pd
import pytz
import matplotlib.pyplot as plt

# Establish connection to the MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

# Set time zone to UTC
timezone = pytz.timezone("Etc/UTC")

# Define a specific event date (example: a major economic announcement)
event_date = datetime(2023, 6, 14, 18, 0, tzinfo=timezone)  # Example: Fed rate decision

# Get data for 1 day before and after the event
from_date = event_date - timedelta(days=1)
to_date = event_date + timedelta(days=1)

# Get 5-minute bars around the event for multiple symbols
symbols = ["EURUSD", "USDJPY", "XAUUSD", "US30"]
symbol_data = {}

for symbol in symbols:
    # Make sure symbol is available in Market Watch
    mt5.symbol_select(symbol, True)
    
    # Get the data
    rates = mt5.copy_rates_range(symbol, mt5.TIMEFRAME_M5, from_date, to_date)
    
    if rates is not None:
        # Convert to DataFrame
        df = pd.DataFrame(rates)
        df['time'] = pd.to_datetime(df['time'], unit='s')
        
        # Normalize prices to the value at event time for comparison
        event_price_idx = df['time'].searchsorted(event_date)
        if event_price_idx < len(df):
            event_price = df.iloc[event_price_idx]['close']
            df['normalized_price'] = df['close'] / event_price
            symbol_data[symbol] = df
        else:
            print(f"Event time not found in data for {symbol}")
    else:
        print(f"Failed to get data for {symbol}, error code = {mt5.last_error()}")

# Shut down the connection when done
mt5.shutdown()

# Analyze market reaction
if symbol_data:
    print("Market Reaction Analysis:")
    for symbol, df in symbol_data.items():
        # Find the event time index
        event_idx = df['time'].searchsorted(event_date)
        if event_idx < len(df):
            # Pre-event and post-event periods
            pre_event = df.iloc[max(0, event_idx-12):event_idx]  # 1 hour before (12 5-min bars)
            post_event = df.iloc[event_idx:min(len(df), event_idx+12)]  # 1 hour after
            
            # Calculate volatility and price change
            pre_volatility = (pre_event['high'].max() - pre_event['low'].min()) / pre_event['close'].iloc[0] * 100
            post_volatility = (post_event['high'].max() - post_event['low'].min()) / post_event['close'].iloc[0] * 100
            price_change = (post_event['close'].iloc[-1] - df.iloc[event_idx]['close']) / df.iloc[event_idx]['close'] * 100
            
            print(f"\n{symbol}:")
            print(f"  Pre-event volatility (1h): {pre_volatility:.2f}%")
            print(f"  Post-event volatility (1h): {post_volatility:.2f}%")
            print(f"  Price change after 1h: {price_change:.2f}%")
            
            # Volume increase
            pre_vol_avg = pre_event['tick_volume'].mean()
            post_vol_avg = post_event['tick_volume'].mean()
            vol_change_pct = (post_vol_avg / pre_vol_avg - 1) * 100 if pre_vol_avg > 0 else float('inf')
            print(f"  Volume change: {vol_change_pct:.2f}%")
    
    # The actual plotting would typically be done here in a real application
    print("\nPlotting would show price movements around the event time.")
else:
    print("No data available for analysis")
```

## Advantages of Date Range Retrieval

The `copy_rates_range` function offers several distinct advantages:

1. **Precise Historical Analysis**: Allows examination of specific time periods or events
2. **Event Studies**: Perfect for analyzing market behavior around important economic events
3. **Seasonal Analysis**: Easy to retrieve data for the same period across different years
4. **Correlation Studies**: Compare market behavior across instruments during the same time period
5. **Complete Data Sets**: Ensures you get all available data between two specific dates

## Comparison with Other Historical Data Functions

| Function | Use Case | Key Advantage |
|----------|----------|---------------|
| `copy_rates_range` | When you need all bars between two specific dates | Complete data for a specific historical period |
| `copy_rates_from` | When you need bars starting from a specific date | Precise historical analysis from a specific point forward |
| `copy_rates_from_pos` | When you need recent bars relative to current bar | Simple retrieval of recent data without date calculations |

## Related Functions

- `copy_rates_from()`: Gets bars from the MetaTrader 5 terminal starting from the specified date
- `copy_rates_from_pos()`: Gets bars from the MetaTrader 5 terminal starting from the specified position
- `copy_ticks_from()`: Gets ticks from the MetaTrader 5 terminal starting from the specified date
- `copy_ticks_range()`: Gets ticks from the MetaTrader 5 terminal for the specified date range
- `symbol_info()`: Gets information about a specified symbol
- `initialize()`: Establishes a connection to the MetaTrader 5 terminal
- `shutdown()`: Closes the connection to the MetaTrader 5 terminal
- `last_error()`: Returns the last error code and description

## Common Use Cases

1. **Historical Event Analysis**: Analyze market behavior around specific economic events
2. **Seasonal Analysis**: Study market patterns during specific seasons or recurring periods
3. **Backtesting Strategies**: Test trading strategies over specific historical periods
4. **Performance Comparison**: Compare instrument performance during specific market conditions
5. **Correlation Studies**: Analyze how different instruments behave during the same time periods

## Error Handling

When `copy_rates_range()` fails:
1. It returns `None`
2. Check the error with `last_error()`
3. Verify that the symbol name is correct
4. Ensure the symbol is available in the terminal
5. Check if the requested historical data is available in the terminal
6. Verify that the date range is valid (date_from is less than date_to)

Common errors:
- Symbol not found in the list of available symbols
- Historical data not available for the specified date range
- Terminal connectivity issues

## Best Practices

1. Always use UTC timezone for datetime objects to avoid time zone issues
2. Set reasonable date ranges to avoid excessive data retrieval
3. Convert the numeric time values to datetime format for better readability and manipulation
4. Consider using pandas DataFrame for advanced data analysis and manipulation
5. Be aware of the historical data limitations in the terminal
6. Always call `shutdown()` when finished with MetaTrader 5 operations

## Implementation Notes

The `copy_rates_range` function is limited by the amount of historical data available in the MetaTrader 5 terminal. The number of bars available to users is limited by the "Max. bars in chart" parameter in the terminal settings.

For working with very long historical periods, you may need to:
1. Adjust the "Max. bars in chart" setting in the MetaTrader 5 terminal
2. Split the date range into smaller chunks and make multiple calls
3. Store retrieved data externally for future use

Additionally, when working with higher timeframes (like W1 or MN1), be aware that the number of bars will be smaller, but each bar represents a longer period.
