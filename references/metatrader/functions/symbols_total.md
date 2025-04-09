# MetaTrader 5 Python API: `symbols_total` Function

## Overview

The `symbols_total` function retrieves the number of all financial instruments (symbols) available in the MetaTrader 5 terminal. This includes all symbols that are available for trading, as well as custom symbols and those disabled in the MarketWatch window.

## Function Syntax

```python
symbols_total()
```

The `symbols_total` function takes no parameters.

## Return Value

The function returns an integer value representing the total number of symbols available in the terminal.

## Important Notes

- You must call `initialize()` to establish a connection to the MetaTrader 5 terminal before calling `symbols_total()`
- The function returns the count of all symbols, including custom ones and those disabled in MarketWatch
- This function is similar to the MQL5 `SymbolsTotal()` function but provides a more comprehensive count

## Usage Example

```python
import MetaTrader5 as mt5

# Establish connection to the MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

# Get the number of financial instruments
symbols_count = mt5.symbols_total()
if symbols_count > 0:
    print("Total symbols =", symbols_count)
else:
    print("Symbols not found")

# Shut down the connection when done
mt5.shutdown()
```

## Common Use Cases

1. **Initial Market Assessment**: Quickly determine how many trading instruments are available
2. **Symbol Management**: Verify that a terminal has sufficient symbols before proceeding with symbol-dependent operations
3. **Custom Symbol Detection**: Gauge if custom symbols have been loaded properly
4. **Market Coverage**: Assess the breadth of market coverage provided by the connected terminal

## Related Functions

- `symbols_get()`: Retrieves all symbols available in the MetaTrader 5 terminal
- `symbol_select()`: Selects a symbol in the MarketWatch window or removes a symbol from the window
- `symbol_info()`: Gets information about a specific symbol
- `terminal_info()`: Gets information about the connected MetaTrader 5 terminal
- `initialize()`: Establishes a connection to the MetaTrader 5 terminal
- `shutdown()`: Closes the connection to the MetaTrader 5 terminal
- `last_error()`: Returns the last error code and description

## Workflow Integration

The `symbols_total` function is typically used as part of a workflow for symbol enumeration and management:

1. Call `initialize()` to connect to the terminal
2. Use `symbols_total()` to get the count of available symbols
3. Call `symbols_get()` to retrieve the complete list of symbols
4. Process individual symbols using `symbol_info()` or other symbol-specific functions
5. Call `shutdown()` when done

## Error Handling

The function doesn't return any specific error values but may fail if:
- The terminal is not initialized (call `initialize()` first)
- The connection to the terminal has been lost

Always check the return value to ensure it's greater than 0 before proceeding with symbol-related operations.

## Best Practices

1. Always call `initialize()` before using `symbols_total()`
2. Use `symbols_total()` as a preliminary check before attempting to retrieve specific symbols
3. Handle the case where no symbols are available gracefully in your application
4. Always call `shutdown()` when finished with MetaTrader 5 operations
5. For large symbol sets, remember that retrieving and processing all symbols might be resource-intensive

## Implementation Notes

The `symbols_total` function provides a quick way to determine if symbols are available without having to retrieve the entire symbol list. This can be useful for preliminary checks before proceeding with more detailed symbol processing operations.
