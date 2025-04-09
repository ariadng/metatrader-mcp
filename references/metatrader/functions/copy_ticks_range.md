# MetaTrader 5 Python API: `copy_ticks_range` Function

## Overview

The `copy_ticks_range` function retrieves tick data for a specified financial instrument from the MetaTrader 5 terminal within a specific date range. Tick data represents the most granular level of market price information, providing raw quotes rather than aggregated bars. This function is particularly useful for analyzing market microstructure, performing detailed historical analysis, and backtesting high-frequency trading strategies for a precise time period.

## Function Syntax

```python
copy_ticks_range(
   symbol,       # symbol name
   date_from,    # date the ticks are requested from
   date_to,      # date, up to which the ticks are requested
   flags         # combination of flags defining the type of requested ticks
)
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `symbol` | string | Financial instrument name (e.g., "EURUSD", "AAPL", etc.). Required unnamed parameter. |
| `date_from` | datetime or int | Start date from which ticks are requested. Can be specified as a 'datetime' object or as the number of seconds elapsed since January 1, 1970 (Unix time). Required unnamed parameter. |
| `date_to` | datetime or int | End date up to which ticks are requested. Can be specified as a 'datetime' object or as the number of seconds elapsed since January 1, 1970 (Unix time). Required unnamed parameter. |
| `flags` | COPY_TICKS enum | Flag to define the type of requested ticks. Set by a value from the COPY_TICKS enumeration. Required unnamed parameter. |

## Return Value

The function returns ticks as a numpy array with the following named columns:
- `time` - Tick time (in seconds since January 1, 1970)
- `bid` - Bid price
- `ask` - Ask price
- `last` - Last price (for securities)
- `volume` - Volume
- `time_msc` - Tick time in milliseconds (milliseconds since January 1, 1970)
- `flags` - Flags from the TICK_FLAG enumeration
- `volume_real` - Real volume (with higher precision)

Returns `None` in case of an error, which can be checked using the `last_error()` function.

## COPY_TICKS Enumeration

The flags parameter defines the type of ticks to retrieve:

| Constant | Description |
|----------|-------------|
| COPY_TICKS_ALL | All ticks |
| COPY_TICKS_INFO | Ticks containing Bid and/or Ask price changes |
| COPY_TICKS_TRADE | Ticks containing Last and/or Volume price changes |

## TICK_FLAG Enumeration

The flags value in the returned data can be a combination of the following flags:

| Constant | Description |
|----------|-------------|
| TICK_FLAG_BID | Bid price changed |
| TICK_FLAG_ASK | Ask price changed |
| TICK_FLAG_LAST | Last price changed |
| TICK_FLAG_VOLUME | Volume changed |
| TICK_FLAG_BUY | Last Buy price changed |
| TICK_FLAG_SELL | Last Sell price changed |

## Important Notes

- You must call `initialize()` to establish a connection to the MetaTrader 5 terminal before using `copy_ticks_range()`
- MetaTrader 5 stores tick time in UTC time zone, while Python's datetime uses the local time zone by default
- For accurate data retrieval, create datetime objects in UTC time zone to avoid local time zone offsets
- Data received from the MetaTrader 5 terminal has UTC time
- Retrieving tick data for a long date range can result in large data volumes, so be careful with your date range specifications
- Use the `flags` parameter to filter for only the types of ticks you need to reduce data volume

## Usage Examples

### Basic Date Range Tick Data Retrieval

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
to_date = datetime(2023, 1, 2, tzinfo=timezone)  # 1 day of data

# Get AUDUSD ticks within the specified date range
ticks = mt5.copy_ticks_range("AUDUSD", from_date, to_date, mt5.COPY_TICKS_ALL)

if ticks is not None:
    # Display the data
    print(f"Received {len(ticks)} AUDUSD ticks for January 1, 2023")
    
    # Show first 5 ticks
    print("\nFirst 5 ticks:")
    for i in range(min(5, len(ticks))):
        tick_time = datetime.fromtimestamp(ticks[i][0], tz=timezone)
        print(f"{tick_time}: Bid: {ticks[i][1]}, Ask: {ticks[i][2]}")
    
    # Show last 5 ticks
    print("\nLast 5 ticks:")
    for i in range(max(0, len(ticks)-5), len(ticks)):
        tick_time = datetime.fromtimestamp(ticks[i][0], tz=timezone)
        print(f"{tick_time}: Bid: {ticks[i][1]}, Ask: {ticks[i][2]}")
else:
    print("Failed to get tick data, error code =", mt5.last_error())

# Shut down the connection when done
mt5.shutdown()
```

### Analyzing Market Activity by Hour

```python
import MetaTrader5 as mt5
from datetime import datetime
import pandas as pd
import pytz
import matplotlib.pyplot as plt

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
from_date = datetime(2023, 1, 2, tzinfo=timezone)  # Monday
to_date = datetime(2023, 1, 7, tzinfo=timezone)    # Saturday (full trading week)

# Get EURUSD ticks for a full trading week
ticks = mt5.copy_ticks_range("EURUSD", from_date, to_date, mt5.COPY_TICKS_INFO)

# Shut down the connection when done
mt5.shutdown()

if ticks is not None:
    # Create DataFrame from the array
    df = pd.DataFrame(ticks)
    
    # Convert time in seconds into the datetime format
    df['time'] = pd.to_datetime(df['time'], unit='s')
    
    # Extract hour
    df['hour'] = df['time'].dt.hour
    df['day'] = df['time'].dt.day_name()
    
    # Calculate spread
    df['spread'] = df['ask'] - df['bid']
    
    # Analyze hourly activity
    hourly_stats = df.groupby('hour').agg({
        'time': 'count',
        'spread': ['mean', 'min', 'max', 'std']
    })
    
    # Rename columns for clarity
    hourly_stats.columns = ['tick_count', 'avg_spread', 'min_spread', 'max_spread', 'spread_std']
    
    # Calculate normalized activity (percentage of total ticks)
    hourly_stats['activity_percent'] = hourly_stats['tick_count'] / hourly_stats['tick_count'].sum() * 100
    
    # Display results
    print("EURUSD Hourly Market Activity Analysis")
    print("-" * 50)
    print(f"Total ticks analyzed: {len(df)}")
    print(f"Date range: {df['time'].min()} to {df['time'].max()}")
    
    # Top 5 most active hours
    most_active = hourly_stats.sort_values('tick_count', ascending=False).head(5)
    print("\nTop 5 Most Active Hours (UTC):")
    for hour, data in most_active.iterrows():
        print(f"{hour:02d}:00 - {hour:02d}:59: {data['tick_count']} ticks ({data['activity_percent']:.2f}%), Avg Spread: {data['avg_spread']:.6f}")
    
    # Hours with widest average spread
    widest_spread = hourly_stats.sort_values('avg_spread', ascending=False).head(3)
    print("\nHours with Widest Average Spread:")
    for hour, data in widest_spread.iterrows():
        print(f"{hour:02d}:00 - {hour:02d}:59: Avg Spread: {data['avg_spread']:.6f}, Max: {data['max_spread']:.6f}")
    
    # Hours with narrowest average spread
    narrowest_spread = hourly_stats.sort_values('avg_spread').head(3)
    print("\nHours with Narrowest Average Spread:")
    for hour, data in narrowest_spread.iterrows():
        print(f"{hour:02d}:00 - {hour:02d}:59: Avg Spread: {data['avg_spread']:.6f}, Min: {data['min_spread']:.6f}")
    
    # The actual plotting would typically be done here in a real application
    print("\nHourly tick count analysis could be visualized as a bar chart.")
else:
    print("Failed to get tick data, error code =", mt5.last_error())
```

### Analyzing Specific Market Events

```python
import MetaTrader5 as mt5
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import pytz

# Establish connection to the MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

# Set time zone to UTC
timezone = pytz.timezone("Etc/UTC")

# Example: Analyzing a specific economic news event
# Non-Farm Payrolls release (example date, replace with actual event date)
event_date = datetime(2023, 2, 3, 13, 30, tzinfo=timezone)  # NFP typically at 13:30 UTC
before_event = event_date - timedelta(minutes=30)
after_event = event_date + timedelta(minutes=30)

# Dictionary to store data for multiple symbols
symbols_data = {}

# Analyze multiple symbols around the event
for symbol in ["EURUSD", "GBPUSD", "USDJPY", "XAUUSD"]:
    # Make sure symbol is available in Market Watch
    mt5.symbol_select(symbol, True)
    
    # Get ticks around the event (30 minutes before and after)
    ticks = mt5.copy_ticks_range(symbol, before_event, after_event, mt5.COPY_TICKS_ALL)
    
    if ticks is not None and len(ticks) > 0:
        # Convert to DataFrame
        df = pd.DataFrame(ticks)
        
        # Convert time in seconds into the datetime format
        df['time'] = pd.to_datetime(df['time'], unit='s')
        df['time_msc'] = pd.to_datetime(df['time_msc'], unit='ms')
        
        # Calculate mid price and spread
        df['mid'] = (df['bid'] + df['ask']) / 2
        df['spread'] = df['ask'] - df['bid']
        
        # Mark pre/post event
        df['period'] = np.where(df['time'] < event_date, 'pre_event', 'post_event')
        
        # Add to dictionary
        symbols_data[symbol] = df
        
        print(f"Retrieved {len(df)} ticks for {symbol}")
    else:
        print(f"No data available for {symbol}, error code = {mt5.last_error()}")

# Shut down the connection when done
mt5.shutdown()

# Analyze the event impact
print("\nMarket Reaction to Economic Event (NFP Release)")
print("=" * 60)

for symbol, df in symbols_data.items():
    if len(df) == 0:
        continue
        
    # Separate pre and post event data
    pre_event_data = df[df['period'] == 'pre_event']
    post_event_data = df[df['period'] == 'post_event']
    
    if len(pre_event_data) == 0 or len(post_event_data) == 0:
        print(f"{symbol}: Insufficient data to analyze event impact")
        continue
    
    # Calculate statistics
    pre_price = pre_event_data['mid'].iloc[0]
    post_price = post_event_data['mid'].iloc[-1]
    price_change = post_price - pre_price
    price_change_pct = (price_change / pre_price) * 100
    
    pre_spread_avg = pre_event_data['spread'].mean()
    post_spread_avg = post_event_data['spread'].mean()
    spread_change_pct = (post_spread_avg / pre_spread_avg - 1) * 100
    
    # Volatility measured by price range
    pre_volatility = pre_event_data['mid'].max() - pre_event_data['mid'].min()
    post_volatility = post_event_data['mid'].max() - post_event_data['mid'].min()
    volatility_change_pct = (post_volatility / pre_volatility - 1) * 100 if pre_volatility > 0 else float('inf')
    
    # Tick frequency (ticks per second)
    pre_duration = (pre_event_data['time'].max() - pre_event_data['time'].min()).total_seconds()
    post_duration = (post_event_data['time'].max() - post_event_data['time'].min()).total_seconds()
    pre_tick_freq = len(pre_event_data) / pre_duration if pre_duration > 0 else 0
    post_tick_freq = len(post_event_data) / post_duration if post_duration > 0 else 0
    tick_freq_change_pct = (post_tick_freq / pre_tick_freq - 1) * 100 if pre_tick_freq > 0 else float('inf')
    
    # Print results
    print(f"\n{symbol} Analysis:")
    print(f"  Price Change: {price_change:.5f} ({price_change_pct:.2f}%)")
    print(f"  Spread: {pre_spread_avg:.6f} → {post_spread_avg:.6f} ({spread_change_pct:.2f}%)")
    print(f"  Volatility: {pre_volatility:.6f} → {post_volatility:.6f} ({volatility_change_pct:.2f}%)")
    print(f"  Tick Frequency: {pre_tick_freq:.2f} → {post_tick_freq:.2f} ticks/sec ({tick_freq_change_pct:.2f}%)")
    
    # Maximum price movements
    max_up_move = post_event_data['mid'].max() - post_event_data['mid'].iloc[0]
    max_down_move = post_event_data['mid'].iloc[0] - post_event_data['mid'].min()
    print(f"  Maximum Up Move: {max_up_move:.5f}")
    print(f"  Maximum Down Move: {max_down_move:.5f}")
```

## Advantages of Date Range Tick Data Retrieval

The `copy_ticks_range` function offers several distinct advantages:

1. **Precise Period Analysis**: Allows examination of tick data within exact datetime boundaries
2. **Event Studies**: Perfect for analyzing market microstructure around important events
3. **Complete Data Set**: Retrieves all available ticks within the specified range, not limited by count
4. **Flexible Data Selection**: Can filter by different tick types to focus on specific market activities
5. **High-Resolution Data**: Provides millisecond-precise timing for detailed analysis

## Comparison with Other Historical Data Functions

| Function | Data Type | Use Case | Key Advantage |
|----------|-----------|----------|---------------|
| `copy_ticks_range` | Tick data | When you need tick data between two specific dates | Complete tick data for a specific period |
| `copy_ticks_from` | Tick data | When you need a specific number of ticks from a date | Control over the amount of data retrieved |
| `copy_rates_range` | OHLC bars | When you need bar data between two specific dates | Efficient analysis of a specific period with aggregated data |
| `copy_rates_from` | OHLC bars | When you need bars starting from a specific date | More compact data for trend analysis |

## Related Functions

- `copy_ticks_from()`: Gets a specified number of ticks from the MetaTrader 5 terminal starting from a specified date
- `copy_rates_range()`: Gets bars from the MetaTrader 5 terminal for the specified date range
- `copy_rates_from()`: Gets bars from the MetaTrader 5 terminal starting from the specified date
- `copy_rates_from_pos()`: Gets bars from the MetaTrader 5 terminal starting from the specified position
- `symbol_info_tick()`: Gets the latest prices for a specified symbol
- `initialize()`: Establishes a connection to the MetaTrader 5 terminal
- `shutdown()`: Closes the connection to the MetaTrader 5 terminal
- `last_error()`: Returns the last error code and description

## Common Use Cases

1. **Event Analysis**: Study market reaction to economic announcements or news events
2. **Market Microstructure Analysis**: Analyze bid-ask spreads, tick frequency, and price formation during specific periods
3. **Liquidity Analysis**: Examine market depth and liquidity conditions for certain trading sessions
4. **Volatility Studies**: Calculate precise volatility metrics during specific time windows
5. **Arbitrage Detection**: Identify price discrepancies across different instruments during specific periods
6. **Historical Pattern Analysis**: Find recurring tick patterns at specific times or market conditions
7. **Trading Session Comparison**: Compare market activity across different trading sessions (Asian, European, US)

## Error Handling

When `copy_ticks_range()` fails:
1. It returns `None`
2. Check the error with `last_error()`
3. Verify that the symbol name is correct
4. Ensure the symbol is available in the terminal
5. Check if the requested tick data is available in the terminal
6. Verify that the date range is valid (date_from is less than date_to)

Common errors:
- Symbol not found in the list of available symbols
- Tick data not available for the specified date range
- Terminal connectivity issues
- Memory limitations when requesting data for a very wide date range

## Best Practices

1. Always use UTC timezone for datetime objects to avoid time zone issues
2. Request data for reasonably narrow date ranges to avoid memory issues
3. Use the appropriate COPY_TICKS flag to filter for only the types of ticks you need
4. Convert the numeric time values to datetime format for better readability and analysis
5. Consider using pandas DataFrame for advanced data analysis and manipulation
6. For large date ranges, consider breaking up the request into smaller chunks
7. Always call `shutdown()` when finished with MetaTrader 5 operations
8. Consider storing retrieved tick data in a database for future use if conducting extensive research

## Implementation Notes

The `copy_ticks_range` function is limited by the amount of tick data available in the MetaTrader 5 terminal. Tick data storage is typically more limited than bar data due to its larger volume.

For extensive tick data analysis, you may need to:
1. Break large date ranges into smaller segments
2. Store retrieved data externally for future use
3. Be aware that older tick data might not be available for some symbols

The millisecond precision in 'time_msc' provides more accurate timing than the second-level 'time' field, which is important for high-frequency analysis and event studies.
