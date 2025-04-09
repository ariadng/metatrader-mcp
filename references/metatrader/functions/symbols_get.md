# MetaTrader 5 Python API: `symbols_get` Function

## Overview

The `symbols_get` function retrieves information about all available financial instruments (symbols) from the MetaTrader 5 terminal. It provides powerful filtering capabilities to select specific groups of symbols based on their names.

## Function Syntax

```python
symbols_get(
   group="GROUP"      # symbol selection filter 
)
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `group` | string | Optional. Filter for arranging a group of necessary symbols. If specified, the function returns only symbols meeting the criteria. Can be used as a named or unnamed parameter. |

## Return Value

The function returns symbols in the form of a tuple of objects, each containing detailed information about a symbol. Returns `None` in case of an error, which can be checked using the `last_error()` function.

Each symbol object in the returned tuple contains numerous properties describing the trading instrument, including:
- `name` - Symbol name
- `custom` - Custom symbol flag
- `chart_mode` - Price type used for generating symbols bars
- `select` - Symbol selection in Market Watch
- `visible` - Symbol visibility in Market Watch
- And many other properties describing trading conditions and specifications

## Group Parameter Usage

The `group` parameter allows for powerful filtering of symbols based on their names:

- `*` can be used at the beginning and the end of a string as a wildcard
- Multiple conditions can be comma-separated
- The logical negation symbol `!` can be used for exclusion
- Conditions are applied sequentially (inclusion first, then exclusion)

### Examples of Group Filters:

- `"*"` - All symbols
- `"*USD*"` - All symbols containing "USD" in their names
- `"*,!*USD*,!*EUR*"` - All symbols except those containing "USD" or "EUR"
- `"EUR*"` - All symbols starting with "EUR"
- `"*JPY"` - All symbols ending with "JPY"

## Important Notes

- You must call `initialize()` to establish a connection to the MetaTrader 5 terminal before calling `symbols_get()`
- Unlike `symbol_info()`, the `symbols_get()` function returns data on all requested symbols within a single call
- For a large number of symbols, considerable time might be needed to retrieve all the data
- Consider using filters to reduce the number of symbols when only specific ones are needed

## Usage Examples

### Get All Symbols

```python
import MetaTrader5 as mt5

# Establish connection to the MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

# Get all symbols
symbols = mt5.symbols_get()
print('Total symbols:', len(symbols))

# Display the first five symbols
for i, symbol in enumerate(symbols[:5], 1):
    print(f"{i}. {symbol.name}")

# Shut down the connection when done
mt5.shutdown()
```

### Get Symbols with Filtering

```python
import MetaTrader5 as mt5

# Establish connection to the MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

# Get symbols containing "RU" in their names
ru_symbols = mt5.symbols_get("*RU*")
print('Symbols containing "RU":', len(ru_symbols))
for symbol in ru_symbols:
    print(symbol.name)

# Get symbols excluding major currency pairs
filtered_symbols = mt5.symbols_get(group="*,!*USD*,!*EUR*,!*JPY*,!*GBP*")
print('\nSymbols excluding major currencies:', len(filtered_symbols))
for symbol in filtered_symbols:
    print(symbol.name)

# Shut down the connection when done
mt5.shutdown()
```

### Using with Pandas for Analysis

```python
import MetaTrader5 as mt5
import pandas as pd

# Establish connection to the MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

# Get all forex symbols
forex_symbols = mt5.symbols_get("*")

# Convert to list of dictionaries
symbols_data = []
for symbol in forex_symbols:
    symbol_dict = symbol._asdict()
    # Extract key properties
    symbols_data.append({
        'name': symbol_dict['name'],
        'bid': symbol_dict['bid'],
        'ask': symbol_dict['ask'],
        'spread': symbol_dict['spread'],
        'digits': symbol_dict['digits'],
        'trade_mode': symbol_dict['trade_mode'],
        'volume_min': symbol_dict['volume_min'],
        'volume_step': symbol_dict['volume_step']
    })

# Create a DataFrame for analysis
df = pd.DataFrame(symbols_data)
print(df.head())

# Shut down the connection when done
mt5.shutdown()
```

## Symbol Properties

The symbols returned by `symbols_get()` contain many properties, including:

- Trading specifications (`volume_min`, `volume_max`, `volume_step`)
- Price information (`bid`, `ask`, `point`, `tick_size`, `tick_value`)
- Trading session times
- Contract specifications
- Margin requirements
- Swap rates
- And many more trading parameters

## Related Functions

- `symbols_total()`: Gets the number of all financial instruments in the terminal
- `symbol_select()`: Selects a symbol in the MarketWatch window or removes a symbol from the window
- `symbol_info()`: Gets information about a specific symbol
- `initialize()`: Establishes a connection to the MetaTrader 5 terminal
- `shutdown()`: Closes the connection to the MetaTrader 5 terminal
- `last_error()`: Returns the last error code and description

## Common Use Cases

1. **Market Analysis**: Retrieve symbols for price analysis across multiple instruments
2. **Symbol Filtering**: Get specific groups of symbols (e.g., only forex pairs, only indices)
3. **Portfolio Management**: Retrieve data on all instruments in a portfolio for monitoring
4. **Symbol Property Comparison**: Compare properties across multiple symbols
5. **Custom Instrument Groups**: Create custom groups of instruments for specialized trading strategies

## Error Handling

When `symbols_get()` fails:
1. It returns `None`
2. Check the error with `last_error()`
3. Verify that the terminal connection was successfully initialized
4. Ensure that the filter syntax is correct

## Best Practices

1. Use appropriate filters to limit the number of symbols returned
2. Check that the return value is not `None` before processing
3. For large symbol sets, consider processing in batches or limiting the fields you analyze
4. Cache symbol information that doesn't change frequently to improve performance
5. Always call `shutdown()` when finished with MetaTrader 5 operations

## Implementation Notes

The `symbols_get` function is a powerful tool for retrieving comprehensive information about multiple trading instruments in a single call. By using effective filtering, you can create targeted analyses and trading systems that work with specific groups of symbols.
