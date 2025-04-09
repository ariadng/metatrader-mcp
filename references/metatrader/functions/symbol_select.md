# MetaTrader 5 Python API: `symbol_select` Function

## Overview

The `symbol_select` function enables or disables a financial instrument (symbol) in the MetaTrader 5 terminal's MarketWatch window. This function is crucial for making symbols available for trading operations and data retrieval, as certain MetaTrader 5 operations require symbols to be visible in the MarketWatch.

## Function Syntax

```python
symbol_select(
   symbol,      # financial instrument name
   enable=None  # enable or disable
)
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `symbol` | string | Financial instrument name (e.g., "EURUSD", "AAPL", etc.). Required unnamed parameter. |
| `enable` | bool | Switch to enable or disable the symbol. Optional parameter. If `True`, the symbol is selected in the MarketWatch window. If `False`, the symbol is removed from the MarketWatch window. |

## Return Value

Returns `True` if successful, otherwise returns `False`.

## Important Notes

- You must call `initialize()` to establish a connection to the MetaTrader 5 terminal before calling `symbol_select()`
- A symbol cannot be removed from MarketWatch if there are open charts with this symbol or if there are open positions on it
- The function is similar to the MQL5 `SymbolSelect()` function
- Before retrieving detailed information about a symbol using `symbol_info()` or `symbol_info_tick()`, it's generally recommended to ensure the symbol is selected in MarketWatch using this function
- Selecting a symbol in MarketWatch enables data streaming and ensures all symbol properties are properly initialized

## Usage Examples

### Basic Symbol Selection

```python
import MetaTrader5 as mt5

# Establish connection to the MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

# Select EURUSD in MarketWatch
if mt5.symbol_select("EURUSD", True):
    print("EURUSD selected successfully in MarketWatch")
    
    # Now we can get symbol information
    symbol_info = mt5.symbol_info("EURUSD")
    print("EURUSD bid:", symbol_info.bid)
    print("EURUSD ask:", symbol_info.ask)
else:
    print("Failed to select EURUSD, error code =", mt5.last_error())

# Shut down the connection when done
mt5.shutdown()
```

### Removing a Symbol from MarketWatch

```python
import MetaTrader5 as mt5

# Establish connection to the MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

# Attempt to remove USDJPY from MarketWatch
if mt5.symbol_select("USDJPY", False):
    print("USDJPY removed successfully from MarketWatch")
else:
    print("Failed to remove USDJPY, error code =", mt5.last_error())
    print("Note: Symbol cannot be removed if charts are open or positions exist")

# Shut down the connection when done
mt5.shutdown()
```

### Working with Multiple Symbols

```python
import MetaTrader5 as mt5
import pandas as pd

# Establish connection to the MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

# List of symbols to add to MarketWatch
symbols = ["EURUSD", "GBPUSD", "USDJPY", "AUDUSD"]
symbols_info = []

# Select all symbols and get their information
for symbol in symbols:
    # Select the symbol in MarketWatch
    if mt5.symbol_select(symbol, True):
        # Get symbol information
        info = mt5.symbol_info(symbol)
        if info is not None:
            symbols_info.append({
                'symbol': symbol,
                'bid': info.bid,
                'ask': info.ask,
                'spread': info.spread,
                'digits': info.digits,
                'currency_base': info.currency_base,
                'currency_profit': info.currency_profit
            })
        else:
            print(f"Failed to get {symbol} info, error code =", mt5.last_error())
    else:
        print(f"Failed to select {symbol}, error code =", mt5.last_error())

# Convert to DataFrame for analysis
if symbols_info:
    df = pd.DataFrame(symbols_info)
    print("Selected symbols information:")
    print(df)

# Shut down the connection when done
mt5.shutdown()
```

## Symbol Selection Best Practices

To effectively work with symbols in MetaTrader 5 Python API:

1. **Select Before Use**: Always select a symbol before attempting to retrieve its information or place orders.
2. **Verify Selection**: Check the return value of `symbol_select()` to confirm successful selection.
3. **Maintain Selection**: For frequently used symbols, select them once at the beginning of your script.
4. **Handle Removal Failures**: Be aware that symbols with open charts or positions cannot be removed.
5. **Error Handling**: Always check the error code when `symbol_select()` returns `False`.

## Related Functions

- `symbol_info()`: Gets comprehensive information about a symbol
- `symbol_info_tick()`: Gets the latest price tick for a symbol
- `symbols_get()`: Gets information about multiple symbols based on filtering criteria
- `symbols_total()`: Gets the number of all financial instruments in the terminal
- `initialize()`: Establishes a connection to the MetaTrader 5 terminal
- `shutdown()`: Closes the connection to the MetaTrader 5 terminal
- `last_error()`: Returns the last error code and description

## Common Use Cases

1. **Symbol Preparation**: Select symbols before retrieving their data or placing orders
2. **Custom Symbol Lists**: Create custom watchlists by selecting specific symbols
3. **Automated Trading**: Ensure required symbols are available for trading operations
4. **Market Analysis**: Select symbols to get up-to-date pricing information
5. **Symbol Visibility Management**: Control which symbols appear in the MarketWatch window

## Error Handling

When `symbol_select()` fails:
1. It returns `False`
2. Check the error with `last_error()`
3. Verify that the symbol name is correct
4. Check for situations that prevent removal (open charts, open positions)
5. Verify terminal connectivity

Common errors:
- Symbol not found in the list of available symbols
- Cannot remove symbol due to open charts or positions
- Terminal connectivity issues

## Best Practices

1. Select symbols at the beginning of your script before performing any operations on them
2. Always check the return value of `symbol_select()` to confirm success
3. Handle potential failures gracefully
4. Use `True` as the second parameter when you need symbol data, even if you don't need it visible in the UI
5. Always call `shutdown()` when finished with MetaTrader 5 operations

## Implementation Notes

The `symbol_select` function is a simple but essential function for preparing symbols for use in trading operations, data retrieval, and market analysis. By ensuring symbols are selected in the MarketWatch window, you can access their complete information and perform all available operations on them.

When working with multiple symbols, consider selecting all required symbols at the start of your script to improve efficiency and ensure all data is available when needed.
