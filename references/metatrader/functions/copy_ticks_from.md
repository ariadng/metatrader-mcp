# MetaTrader 5 Python API: `copy_ticks_from` Function

## Overview

The `copy_ticks_from` function retrieves tick data for a specified financial instrument from the MetaTrader 5 terminal starting from a specified date. Tick data represents the most granular level of market price information, containing individual price quotes rather than aggregated OHLC bars. This function is essential for detailed market microstructure analysis, high-frequency trading strategies, and precise backtesting.

## Function Syntax

```python
copy_ticks_from(
   symbol,       # symbol name
   date_from,    # date the ticks are requested from
   count,        # number of requested ticks
   flags         # combination of flags defining the type of requested ticks
)
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `symbol` | string | Financial instrument name (e.g., "EURUSD", "AAPL", etc.). Required unnamed parameter. |
| `date_from` | datetime or int | Date from which ticks are requested. Can be specified as a 'datetime' object or as the number of seconds elapsed since January 1, 1970 (Unix time). Required unnamed parameter. |
| `count` | int | Number of ticks to retrieve. Required unnamed parameter. |
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

- You must call `initialize()` to establish a connection to the MetaTrader 5 terminal before using `copy_ticks_from()`
- MetaTrader 5 stores tick time in UTC time zone, while Python's datetime uses the local time zone by default
- For accurate data retrieval, create datetime objects in UTC time zone to avoid local time zone offsets
- Data received from the MetaTrader 5 terminal has UTC time
- Tick data can be much larger in volume than bar data, so be careful with the `count` parameter to avoid memory issues
- Use the `flags` parameter to filter for only the types of ticks you need

## Usage Examples

### Basic Tick Data Retrieval

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

# Create 'datetime' object in UTC time zone to avoid local time zone offset
start_date = datetime(2023, 1, 1, tzinfo=timezone)

# Get 1000 EURUSD ticks starting from January 1, 2023
ticks = mt5.copy_ticks_from("EURUSD", start_date, 1000, mt5.COPY_TICKS_ALL)

if ticks is not None:
    # Display the data
    print(f"Received {len(ticks)} EURUSD ticks")
    
    # Show first 5 ticks
    print("\nFirst 5 ticks:")
    for i in range(min(5, len(ticks))):
        tick_time = datetime.fromtimestamp(ticks[i][0], tz=timezone)
        print(f"{tick_time}: Bid: {ticks[i][1]}, Ask: {ticks[i][2]}")
else:
    print("Failed to get tick data, error code =", mt5.last_error())

# Shut down the connection when done
mt5.shutdown()
```

### Filtering Ticks and Converting to DataFrame

```python
import MetaTrader5 as mt5
from datetime import datetime
import pandas as pd
import pytz

# Set pandas display options
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1500)

# Establish connection to the MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

# Set time zone to UTC
timezone = pytz.timezone("Etc/UTC")

# Create 'datetime' object in UTC time zone
start_date = datetime(2023, 1, 10, tzinfo=timezone)

# Get 10,000 EURUSD informational ticks (Bid/Ask changes only)
ticks = mt5.copy_ticks_from("EURUSD", start_date, 10000, mt5.COPY_TICKS_INFO)

# Shut down the connection when done
mt5.shutdown()

if ticks is not None:
    # Create DataFrame from the array
    ticks_frame = pd.DataFrame(ticks)
    
    # Convert time in seconds into the datetime format
    ticks_frame['time'] = pd.to_datetime(ticks_frame['time'], unit='s')
    
    # Convert millisecond time to datetime format
    ticks_frame['time_msc'] = pd.to_datetime(ticks_frame['time_msc'], unit='ms')
    
    # Calculate some basic statistics
    print("EURUSD Tick Data Analysis:")
    print(f"Total ticks: {len(ticks_frame)}")
    print(f"Date range: {ticks_frame['time'].min()} to {ticks_frame['time'].max()}")
    print(f"Average Bid price: {ticks_frame['bid'].mean():.5f}")
    print(f"Average Ask price: {ticks_frame['ask'].mean():.5f}")
    print(f"Average spread: {(ticks_frame['ask'] - ticks_frame['bid']).mean():.6f}")
    
    # Display first 10 rows
    print("\nFirst 10 ticks:")
    print(ticks_frame.head(10))
else:
    print("Failed to get tick data, error code =", mt5.last_error())
```

### Analyzing Tick Data for Market Microstructure

```python
import MetaTrader5 as mt5
from datetime import datetime, timedelta
import pandas as pd
import pytz
import numpy as np

# Establish connection to the MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

# Set time zone to UTC
timezone = pytz.timezone("Etc/UTC")

# Create 'datetime' object in UTC time zone
start_date = datetime(2023, 1, 1, 8, 0, tzinfo=timezone)  # Starting at 8:00 AM UTC

# Get 50,000 USDJPY ticks starting from the specified time
ticks = mt5.copy_ticks_from("USDJPY", start_date, 50000, mt5.COPY_TICKS_ALL)

# Shut down the connection when done
mt5.shutdown()

if ticks is not None:
    # Convert to DataFrame
    df = pd.DataFrame(ticks)
    
    # Convert time in seconds into the datetime format
    df['time'] = pd.to_datetime(df['time'], unit='s')
    
    # Create millisecond-precise time
    df['time_msc'] = pd.to_datetime(df['time_msc'], unit='ms')
    
    # Calculate derived features
    df['spread'] = df['ask'] - df['bid']
    df['mid_price'] = (df['ask'] + df['bid']) / 2
    
    # Analyze tick arrival patterns
    df['time_diff'] = df['time_msc'].diff().dt.total_seconds() * 1000  # Time difference in milliseconds
    
    # Analyze bid-ask bounce
    df['price_direction'] = np.sign(df['mid_price'].diff())
    
    # Group by minute for analysis
    df['minute'] = df['time'].dt.floor('1min')
    minute_stats = df.groupby('minute').agg({
        'spread': ['mean', 'min', 'max'],
        'time_diff': ['mean', 'min', 'max', 'count'],
        'mid_price': ['first', 'last', 'min', 'max']
    })
    
    # Print overall statistics
    print("USDJPY Tick Data Microstructure Analysis")
    print("-" * 50)
    print(f"Total ticks: {len(df)}")
    print(f"Date range: {df['time'].min()} to {df['time'].max()}")
    print(f"Average spread: {df['spread'].mean():.6f}")
    print(f"Average time between ticks: {df['time_diff'].mean():.2f} ms")
    
    # Identify periods of high activity
    active_minutes = minute_stats['time_diff']['count'].sort_values(ascending=False).head(5)
    print("\nTop 5 most active minutes (by tick count):")
    for minute, count in active_minutes.items():
        price_range = minute_stats.loc[minute, ('mid_price', 'max')] - minute_stats.loc[minute, ('mid_price', 'min')]
        print(f"{minute}: {count} ticks, price range: {price_range:.5f}")
    
    # Analyze spread distribution
    print("\nSpread Distribution:")
    spread_distribution = df['spread'].value_counts().sort_index().head(10)
    for spread, count in spread_distribution.items():
        print(f"Spread {spread:.6f}: {count} ticks ({count/len(df)*100:.2f}%)")
    
    # Direction changes analysis
    direction_changes = (df['price_direction'].diff() != 0).sum()
    print(f"\nNumber of price direction changes: {direction_changes}")
    print(f"Average ticks between direction changes: {len(df)/direction_changes:.2f}")
else:
    print("Failed to get tick data, error code =", mt5.last_error())
```

## Advantages of Tick Data Analysis

Tick data provides several distinct advantages over bar data:

1. **Maximum Precision**: Represents the actual quotes received by the terminal, not an aggregation
2. **Market Microstructure Insights**: Allows analysis of spread dynamics, order flow, and price formation
3. **High-Frequency Trading**: Essential for developing and testing high-frequency trading strategies
4. **Accurate Backtesting**: Enables more realistic simulation of trade execution and slippage
5. **Volatility Analysis**: Better measurement of intraday volatility and price jumps

## Comparison with Other Historical Data Functions

| Function | Data Type | Use Case | Key Advantage |
|----------|-----------|----------|---------------|
| `copy_ticks_from` | Tick data | When you need the most granular price data from a specific date forward | Highest level of detail for precise analysis |
| `copy_ticks_range` | Tick data | When you need tick data between two specific dates | Complete tick data for a specific period |
| `copy_rates_from` | OHLC bars | When you need aggregated price data from a specific date | More compact data for trend analysis |
| `copy_rates_range` | OHLC bars | When you need bar data between two specific dates | Efficient analysis of a specific period |

## Related Functions

- `copy_ticks_range()`: Gets ticks from the MetaTrader 5 terminal for the specified date range
- `copy_rates_from()`: Gets bars from the MetaTrader 5 terminal starting from the specified date
- `copy_rates_from_pos()`: Gets bars from the MetaTrader 5 terminal starting from the specified position
- `copy_rates_range()`: Gets bars from the MetaTrader 5 terminal for the specified date range
- `symbol_info_tick()`: Gets the latest prices for a specified symbol
- `initialize()`: Establishes a connection to the MetaTrader 5 terminal
- `shutdown()`: Closes the connection to the MetaTrader 5 terminal
- `last_error()`: Returns the last error code and description

## Common Use Cases

1. **Market Microstructure Analysis**: Study bid-ask spreads, tick frequency, and price formation
2. **High-Frequency Strategy Development**: Test strategies that operate on tick-by-tick data
3. **Liquidity Analysis**: Analyze market depth and liquidity throughout the trading day
4. **Volatility Measurement**: Calculate realized volatility using high-precision data
5. **Event Studies**: Analyze market reaction to news events at the millisecond level
6. **Order Book Reconstruction**: Partially reconstruct order book dynamics from tick data

## Error Handling

When `copy_ticks_from()` fails:
1. It returns `None`
2. Check the error with `last_error()`
3. Verify that the symbol name is correct
4. Ensure the symbol is available in the terminal
5. Check if the requested tick data is available in the terminal

Common errors:
- Symbol not found in the list of available symbols
- Tick data not available for the specified date
- Terminal connectivity issues
- Memory limitations when requesting too many ticks

## Best Practices

1. Always use UTC timezone for datetime objects to avoid time zone issues
2. Request a reasonable number of ticks to avoid memory issues
3. Use the appropriate COPY_TICKS flag to filter for only the types of ticks you need
4. Convert the numeric time values to datetime format for better readability and analysis
5. Consider using pandas DataFrame for advanced data analysis and manipulation
6. For large analyses, process the data in chunks rather than requesting millions of ticks at once
7. Always call `shutdown()` when finished with MetaTrader 5 operations

## Implementation Notes

The `copy_ticks_from` function is limited by the amount of tick data available in the MetaTrader 5 terminal. Tick data storage is typically more limited than bar data due to its larger volume.

For extensive tick data analysis, you may need to:
1. Request data in smaller chunks
2. Store retrieved data externally for future use
3. Be aware that older tick data might not be available for some symbols

The millisecond precision in 'time_msc' provides more accurate timing than the second-level 'time' field, which is important for high-frequency analysis.
