# MetaTrader 5 Python API: `login` Function

## Overview

The `login` function connects to a trading account using specified parameters. This function is used to authenticate and access a specific trading account after establishing a connection to the MetaTrader 5 terminal.

## Function Syntax

```python
login(
   login,                    # account number
   password="PASSWORD",      # password
   server="SERVER",          # server name as it is specified in the terminal
   timeout=TIMEOUT           # timeout
)
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `login` | integer | Trading account number. **Required** unnamed parameter. |
| `password` | string | Trading account password. Optional named parameter. If the password is not set, the password saved in the terminal database is applied automatically. |
| `server` | string | Trade server name. Optional named parameter. If no server is set, the last used server is applied automatically. |
| `timeout` | integer | Connection timeout in milliseconds. Optional named parameter. If not specified, the default value of 60,000 (60 seconds) is applied. If the connection is not established within the specified time, the call is forcibly terminated and an exception is generated. |

## Return Value

- Returns `True` in case of a successful connection to the trading account
- Returns `False` if the connection fails

## Important Notes

- Before using the `login` function, you must establish a connection to the MetaTrader 5 terminal using `initialize()`
- If you've previously saved the login credentials in the terminal database, you can connect without specifying the password
- The function can throw an exception if the connection attempt times out

## Usage Examples

### Example 1: Connect without specifying password (using saved credentials)

```python
import MetaTrader5 as mt5

# Establish connection to the MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

# Connect to the trade account without specifying a password and server
account = 17221085
authorized = mt5.login(account)  # the terminal database password is applied if connection data is set to be remembered
if authorized:
    print("connected to account #{}".format(account))
else:
    print("failed to connect at account #{}, error code: {}".format(account, mt5.last_error()))
```

### Example 2: Connect with explicit password

```python
import MetaTrader5 as mt5

# Establish connection to the MetaTrader 5 terminal first
if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

# Connect to trading account with password
account = 25115284
authorized = mt5.login(account, password="your_password")
if authorized:
    # Display trading account data
    print(mt5.account_info())
    
    # Display trading account data in the form of a list
    print("Show account_info()._asdict():")
    account_info_dict = mt5.account_info()._asdict()
    for prop in account_info_dict:
        print("  {}={}".format(prop, account_info_dict[prop]))
else:
    print("failed to connect at account #{}, error code: {}".format(account, mt5.last_error()))

# Don't forget to shut down the connection when done
mt5.shutdown()
```

## Account Information

After successful login, you can access account information using the `account_info()` function, which returns details such as:

- Login number
- Trade mode
- Leverage
- Balance
- Equity
- Margin
- Free margin
- Currency
- Server name
- And many other account properties

## Related Functions

- `initialize()`: Establishes a connection to the MetaTrader 5 terminal
- `shutdown()`: Closes the connection to the MetaTrader 5 terminal
- `account_info()`: Gets information about the connected trading account
- `last_error()`: Returns the last error code

## Common Use Cases

1. **Initial Account Login**: Use `login()` after initializing to connect to your trading account
2. **Switching Accounts**: Switch between different trading accounts in the same session
3. **Automated Trading Systems**: Authenticate to begin automated trading operations
4. **Account Verification**: Verify account credentials before executing trades

## Error Handling

When `login()` fails:
1. Check that your account credentials are correct
2. Verify that the server name is correctly specified
3. Check your network connection
4. Use `last_error()` to get specific error information

## Best Practices

1. Always check the return value of `login()`
2. Use proper error handling with `last_error()`
3. Store sensitive credentials securely
4. Use saved credentials when possible (no explicit password)
5. Consider using environment variables for credentials rather than hardcoding them
6. Always call `shutdown()` when finished with MetaTrader 5 operations
