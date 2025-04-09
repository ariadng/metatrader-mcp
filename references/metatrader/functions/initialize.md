# MetaTrader 5 Python API: `initialize` Function

## Overview

The `initialize` function establishes a connection with the MetaTrader 5 terminal. This is a fundamental function that must be called before using any other MetaTrader 5 API functions.

## Function Syntax

There are three ways to call the `initialize` function:

### 1. Basic Call (No Parameters)

```python
initialize()
```

In this form, the function automatically finds the MetaTrader 5 terminal for connection.

### 2. Specifying Path to Terminal

```python
initialize(
   path                      # path to the MetaTrader 5 terminal EXE file
)
```

This form allows you to specify which MetaTrader 5 terminal installation to connect to.

### 3. Full Parameters (Path and Account Details)

```python
initialize(
   path,                     # path to the MetaTrader 5 terminal EXE file
   login=LOGIN,              # account number
   password="PASSWORD",      # password
   server="SERVER",          # server name as specified in the terminal
   timeout=TIMEOUT,          # timeout
   portable=False            # portable mode
)
```

This form provides full control over the connection, including login credentials.

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `path` | string | Path to the `metatrader.exe` or `metatrader64.exe` file. Optional unnamed parameter specified first without a parameter name. If not provided, the module attempts to find the executable file automatically. |
| `login` | integer | Trading account number. Optional named parameter. If not specified, the last trading account is used. |
| `password` | string | Trading account password. Optional named parameter. If not provided, the password for the specified trading account saved in the terminal database is applied automatically. |
| `server` | string | Trade server name. Optional named parameter. If not set, the server for the specified trading account saved in the terminal database is applied automatically. |
| `timeout` | integer | Connection timeout in milliseconds. Optional named parameter. If not specified, the default value of 60,000 (60 seconds) is applied. |
| `portable` | boolean | Flag for terminal launch in portable mode. Optional named parameter. Default value is `False`. |

## Return Value

- Returns `True` if the connection to the MetaTrader 5 terminal is successfully established.
- Returns `False` if the connection fails.

## Important Notes

- If necessary, the MetaTrader 5 terminal is automatically launched when executing the `initialize()` call.
- After you're done with the MetaTrader 5 operations, you should close the connection using the `shutdown()` function.

## Usage Example

```python
import MetaTrader5 as mt5

# Display data on the MetaTrader 5 package
print("MetaTrader5 package author: ", mt5.__author__)
print("MetaTrader5 package version: ", mt5.__version__)

# Establish MetaTrader 5 connection to a specified trading account
if not mt5.initialize(login=25115284, server="MetaQuotes-Demo", password="4zatlbqx"):
    print("initialize() failed, error code =", mt5.last_error())
    quit()

# Display data on connection status, server name and trading account
print(mt5.terminal_info())

# Display data on MetaTrader 5 version
print(mt5.version())

# When finished with MetaTrader 5, shut down the connection
mt5.shutdown()
```

## Related Functions

- `shutdown()`: Closes the connection to the MetaTrader 5 terminal
- `terminal_info()`: Gets information about the connected MetaTrader 5 terminal
- `version()`: Returns the MetaTrader 5 version
- `login()`: Connects to a trading account using the specified parameters

## Common Use Cases

1. **Initial Connection**: Always call `initialize()` before using any other MetaTrader 5 functionality.
2. **Changing Accounts**: Use the login parameter to switch between different trading accounts.
3. **Error Handling**: Always check the return value of `initialize()` to ensure a successful connection.
4. **Clean Disconnection**: Always use `shutdown()` when you're done to properly close the connection.

## Troubleshooting

If `initialize()` fails:
1. Check that MetaTrader 5 is properly installed
2. Verify your login credentials
3. Check your network connection
4. Use `last_error()` to get specific error information

## Error Codes

When `initialize()` fails, you can use `last_error()` to get detailed error information. Common error codes include:
- Connection issues to the server
- Invalid login credentials 
- Terminal launch failures
- Timeout issues

## Best Practices

1. Always check the return value of `initialize()`
2. Use proper error handling
3. Always call `shutdown()` when done
4. Store sensitive credentials securely
5. Consider using environment variables for credentials rather than hardcoding them
