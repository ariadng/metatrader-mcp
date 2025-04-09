# MetaTrader 5 Python API: `version` Function

## Overview

The `version` function returns the MetaTrader 5 terminal version information. This function provides details about the terminal version, build number, and release date, which can be useful for compatibility checks and debugging.

## Function Syntax

```python
version()
```

The `version` function takes no parameters.

## Return Value

The function returns a tuple with three elements:

| Index | Type | Description | Example Value |
|-------|------|-------------|---------------|
| 0 | integer | MetaTrader 5 terminal version | 500 |
| 1 | integer | Build number | 2367 |
| 2 | string | Build release date | '23 Mar 2020' |

Returns `None` in case of an error. The error information can be obtained using the `last_error()` function.

## Important Notes

- You must call `initialize()` to establish a connection to the MetaTrader 5 terminal before calling `version()`
- The version information can be useful for ensuring compatibility with specific MetaTrader 5 features
- This function is often used to verify that a successful connection has been established

## Usage Example

### Basic Usage

```python
import MetaTrader5 as mt5

# Establish connection to the MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

# Display data on MetaTrader 5 version
version_info = mt5.version()
if version_info is not None:
    print("MetaTrader 5 version:", version_info[0])
    print("Build number:", version_info[1])
    print("Release date:", version_info[2])
else:
    print("Failed to get version info, error code =", mt5.last_error())

# Shut down the connection when done
mt5.shutdown()
```

### With Pandas DataFrame Integration

```python
import MetaTrader5 as mt5
import pandas as pd

# Establish connection to the MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

# Display data on MetaTrader 5 version
print(mt5.version())

# Display data on connection status, server name and trading account
terminal_info = mt5.terminal_info()
print(terminal_info)

# Get properties in the form of a dictionary
terminal_info_dict = terminal_info._asdict()

# Convert the dictionary into DataFrame and print
df = pd.DataFrame(list(terminal_info_dict.items()), columns=['property', 'value'])
print("terminal_info() as dataframe:")
print(df)

# Shut down the connection when done
mt5.shutdown()
```

## Terminal Information

The `version()` function is often used alongside `terminal_info()` to get comprehensive details about the MetaTrader 5 environment. Terminal information includes properties such as:

- Connection status
- Build number
- Maximum number of bars in charts
- Path to the terminal executable
- Language
- Company name
- And many other terminal properties

## Related Functions

- `initialize()`: Establishes a connection to the MetaTrader 5 terminal
- `shutdown()`: Closes the connection to the MetaTrader 5 terminal
- `terminal_info()`: Gets detailed information about the connected MetaTrader 5 terminal
- `last_error()`: Returns the last error code

## Common Use Cases

1. **Compatibility Checks**: Verify that the terminal version supports specific features
2. **Connection Verification**: Confirm that a connection to the terminal has been successfully established
3. **Debugging**: Include version information in logs for troubleshooting purposes
4. **Application Requirements**: Ensure that the minimum required terminal version is available

## Error Handling

When `version()` fails:
1. It returns `None` instead of the version tuple
2. Use `last_error()` to get specific error information
3. Make sure that `initialize()` was called and returned `True` before calling `version()`

## Best Practices

1. Always check that the return value is not `None` before attempting to access elements of the tuple
2. Include version checks in your application if specific features require a minimum terminal version
3. Use the terminal information alongside version data for comprehensive environment details
4. Always call `shutdown()` when finished with MetaTrader 5 operations
