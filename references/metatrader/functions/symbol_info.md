# MetaTrader 5 Python API: `symbol_info` Function

## Overview

The `symbol_info` function retrieves detailed information about a specified financial instrument (symbol) from the MetaTrader 5 terminal. This function provides comprehensive data about a trading instrument's properties, specifications, and current market conditions in a single call.

## Function Syntax

```python
symbol_info(
   symbol      # financial instrument name
)
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `symbol` | string | Financial instrument name (e.g., "EURUSD", "AAPL", etc.). Required unnamed parameter. |

## Return Value

The function returns a named tuple structure (namedtuple) containing detailed information about the specified symbol. Returns `None` in case of an error, which can be checked using the `last_error()` function.

The named tuple contains numerous properties describing the symbol, including but not limited to:

### General Properties
- `name` - Symbol name
- `custom` - Custom symbol flag
- `chart_mode` - Price type used for generating symbol's bars
- `select` - Symbol selection in Market Watch
- `visible` - Symbol visibility in Market Watch
- `description` - Symbol description
- `path` - Path in the symbol tree

### Price Properties
- `bid` - Current bid price
- `ask` - Current ask price
- `last` - Last deal price
- `point` - Symbol point value
- `digits` - Number of decimal places
- `spread` - Spread value in points

### Trading Properties
- `trade_mode` - Order execution type
- `trade_calc_mode` - Contract price calculation mode
- `trade_tick_value` - Value of a tick
- `trade_tick_size` - Minimal price change
- `trade_contract_size` - Contract size
- `volume_min` - Minimal volume for a deal
- `volume_max` - Maximal volume for a deal
- `volume_step` - Minimal volume change step

### Margin and Swap Properties
- `margin_initial` - Initial margin
- `margin_maintenance` - Maintenance margin
- `margin_hedged` - Hedged margin
- `swap_mode` - Swap calculation mode
- `swap_long` - Long swap value
- `swap_short` - Short swap value

### Currency Information
- `currency_base` - Base currency
- `currency_profit` - Profit currency
- `currency_margin` - Margin currency

## Important Notes

- You must call `initialize()` to establish a connection to the MetaTrader 5 terminal before calling `symbol_info()`
- The symbol should preferably be visible in the Market Watch to get all its properties
- The function retrieves all data that would normally require multiple calls to SymbolInfoInteger, SymbolInfoDouble, and SymbolInfoString functions in MQL5
- The returned named tuple can be converted to a dictionary using the `_asdict()` method for easier data manipulation

## Usage Examples

### Basic Symbol Information Retrieval

```python
import MetaTrader5 as mt5

# Establish connection to the MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

# Make sure the symbol is available in Market Watch
if not mt5.symbol_select("EURUSD", True):
    print("Failed to select EURUSD in Market Watch")
    mt5.shutdown()
    quit()

# Get symbol information
symbol_info = mt5.symbol_info("EURUSD")
if symbol_info is not None:
    # Display key symbol properties
    print("EURUSD:", symbol_info.name)
    print("Bid:", symbol_info.bid)
    print("Ask:", symbol_info.ask)
    print("Spread:", symbol_info.spread, "points")
    print("Digits:", symbol_info.digits)
    print("Min volume:", symbol_info.volume_min)
    print("Max volume:", symbol_info.volume_max)
    print("Contract size:", symbol_info.trade_contract_size)
    print("Base currency:", symbol_info.currency_base)
    print("Profit currency:", symbol_info.currency_profit)
else:
    print("Failed to get EURUSD info, error code =", mt5.last_error())

# Shut down the connection when done
mt5.shutdown()
```

### Converting to Dictionary and Analyzing Properties

```python
import MetaTrader5 as mt5
import pandas as pd

# Establish connection to the MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

# Make sure the symbol is available in Market Watch
selected = mt5.symbol_select("EURJPY", True)
if not selected:
    print("Failed to select EURJPY")
    mt5.shutdown()
    quit()

# Get symbol information and convert to dictionary
symbol_info = mt5.symbol_info("EURJPY")
if symbol_info is not None:
    # Convert to dictionary
    symbol_info_dict = symbol_info._asdict()
    
    # Display all symbol properties
    print("Symbol Information:")
    for prop in symbol_info_dict:
        print(f"  {prop}={symbol_info_dict[prop]}")
    
    # Convert selected properties to DataFrame for analysis
    selected_props = {
        'name': symbol_info.name,
        'bid': symbol_info.bid,
        'ask': symbol_info.ask,
        'spread': symbol_info.spread,
        'point': symbol_info.point,
        'volume_min': symbol_info.volume_min,
        'trade_contract_size': symbol_info.trade_contract_size,
        'trade_tick_value': symbol_info.trade_tick_value
    }
    
    df = pd.DataFrame([selected_props])
    print("\nSelected properties as DataFrame:")
    print(df)
else:
    print("Failed to get EURJPY info, error code =", mt5.last_error())

# Shut down the connection when done
mt5.shutdown()
```

## Symbol Selection and Visibility

Before using `symbol_info()`, it's recommended to ensure that the symbol is available and visible in the MarketWatch window using the `symbol_select()` function:

```python
# Make the symbol available in Market Watch (select=True)
if not mt5.symbol_select("EURUSD", True):
    print("Failed to select EURUSD")
    mt5.shutdown()
    quit()
```

This helps ensure that all symbol properties are properly initialized and available.

## Symbol Information Analysis

The symbol information can be used for various trading and analysis purposes:

1. **Price Analysis**: Use `bid`, `ask`, and `last` to analyze current market prices
2. **Spread Analysis**: Evaluate `spread` to assess trading costs
3. **Volume Sizing**: Use `volume_min`, `volume_max`, and `volume_step` to determine valid order sizes
4. **Contract Specifications**: Analyze `trade_contract_size` and `trade_tick_value` for risk calculations
5. **Swap Analysis**: Evaluate overnight holding costs using `swap_long` and `swap_short`

## Related Functions

- `symbol_select()`: Selects a symbol in the MarketWatch window or removes a symbol from the window
- `symbols_get()`: Gets information about multiple symbols based on filtering criteria
- `symbol_info_tick()`: Gets the last tick data for a specified symbol
- `initialize()`: Establishes a connection to the MetaTrader 5 terminal
- `shutdown()`: Closes the connection to the MetaTrader 5 terminal
- `last_error()`: Returns the last error code and description

## Common Use Cases

1. **Trading Automation**: Retrieve symbol data for trading decisions
2. **Risk Management**: Calculate position sizes based on symbol specifications
3. **Market Analysis**: Analyze real-time pricing data
4. **Symbol Validation**: Verify that a symbol exists and check its trading properties
5. **Cost Analysis**: Calculate trading costs based on spread and commission information

## Error Handling

When `symbol_info()` fails:
1. It returns `None`
2. Check the error with `last_error()`
3. Verify that the symbol name is correct
4. Ensure the symbol is available in the Market Watch using `symbol_select()`

## Best Practices

1. Always check that the return value is not `None` before accessing properties
2. Use `symbol_select()` to ensure the symbol is available in Market Watch
3. Use `_asdict()` for more flexible data handling
4. Consider caching symbol specifications that don't change frequently
5. Always call `shutdown()` when finished with MetaTrader 5 operations

## Implementation Notes

The `symbol_info` function is an essential tool for accessing detailed symbol information in a single call, which is far more efficient than retrieving individual properties one by one.
