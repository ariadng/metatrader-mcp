# MetaTrader 5 Python API: `account_info` Function

## Overview

The `account_info` function retrieves comprehensive information about the current trading account. It provides a convenient way to access all account properties in a single function call, including balance, equity, margin, leverage, and other essential trading account details.

## Function Syntax

```python
account_info()
```

The `account_info` function takes no parameters.

## Return Value

The function returns a named tuple structure (namedtuple) containing all account information. Returns `None` in case of an error, which can be checked using the `last_error()` function.

The named tuple contains many properties, including but not limited to:

| Property | Type | Description |
|----------|------|-------------|
| login | integer | Account number |
| trade_mode | integer | Account trade mode (0 - real account, 1 - demo account, 2 - contest) |
| leverage | integer | Account leverage |
| limit_orders | integer | Maximum allowed number of active pending orders |
| margin_so_mode | integer | Mode for setting the minimal allowed margin |
| trade_allowed | boolean | Permission to trade for the current account |
| trade_expert | boolean | Permission to trade for an Expert Advisor |
| margin_mode | integer | Margin calculation mode |
| currency_digits | integer | Number of digits after decimal point in the currency |
| fifo_close | boolean | Flag indicating that positions can only be closed by FIFO rule |
| balance | float | Account balance in the deposit currency |
| credit | float | Credit in the deposit currency |
| profit | float | Current profit in the deposit currency |
| equity | float | Equity in the deposit currency |
| margin | float | Margin used in the deposit currency |
| margin_free | float | Free margin in the deposit currency |
| margin_level | float | Margin level as a percentage |
| margin_so_call | float | Margin call level |
| margin_so_so | float | Margin stop out level |
| margin_initial | float | Initial margin reserved |
| margin_maintenance | float | Maintenance margin |
| assets | float | Current assets |
| liabilities | float | Current liabilities |
| commission_blocked | float | Current commission blocked |
| name | string | Client name |
| server | string | Trade server name |
| currency | string | Account currency |
| company | string | Name of the company that serves the account |

## Important Notes

- You must successfully call `initialize()` and `login()` before using `account_info()`
- The function retrieves all data that would normally require multiple calls to AccountInfoInteger, AccountInfoDouble, and AccountInfoString functions in MQL5
- The returned named tuple can be converted to a dictionary using the `_asdict()` method for easier data manipulation

## Usage Examples

### Basic Account Information Retrieval

```python
import MetaTrader5 as mt5

# Establish connection to the MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

# Connect to the trading account
if mt5.login(12345, password="password", server="server"):
    # Get account information
    account_info = mt5.account_info()
    if account_info is not None:
        # Display trading account data
        print("Account balance:", account_info.balance)
        print("Account equity:", account_info.equity)
        print("Account profit:", account_info.profit)
        print("Account leverage:", account_info.leverage)
        print("Account margin level:", account_info.margin_level)
    else:
        print("Failed to get account info, error code =", mt5.last_error())
else:
    print("Failed to connect to account, error code =", mt5.last_error())

# Shut down the connection when done
mt5.shutdown()
```

### Converting to Dictionary and Using with Pandas

```python
import MetaTrader5 as mt5
import pandas as pd

# Establish connection to the MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

# Connect to the trading account
if mt5.login(12345, password="password", server="server"):
    # Get account information
    account_info = mt5.account_info()
    if account_info is not None:
        # Convert to dictionary
        account_info_dict = account_info._asdict()
        
        # Display all account properties
        print("Account Information:")
        for prop in account_info_dict:
            print(f"  {prop}={account_info_dict[prop]}")
        
        # Convert the dictionary into DataFrame for analysis
        df = pd.DataFrame(list(account_info_dict.items()), columns=['property', 'value'])
        print("\nAccount information as DataFrame:")
        print(df)
    else:
        print("Failed to get account info, error code =", mt5.last_error())
else:
    print("Failed to connect to account, error code =", mt5.last_error())

# Shut down the connection when done
mt5.shutdown()
```

## Account Information Analysis

The account information can be used for various trading and risk management purposes:

1. **Risk Management**: Use `balance`, `equity`, and `margin_level` to assess current risk exposure
2. **Position Sizing**: Calculate appropriate position sizes based on `equity` and risk parameters
3. **Trading Permissions**: Check `trade_allowed` and `trade_expert` before executing trades
4. **Margin Monitoring**: Compare `margin_level` against `margin_so_call` to monitor margin status
5. **Account Verification**: Verify account type via `trade_mode` and other properties

## Related Functions

- `initialize()`: Establishes a connection to the MetaTrader 5 terminal
- `login()`: Connects to a specific trading account
- `terminal_info()`: Gets information about the MetaTrader 5 terminal
- `last_error()`: Returns the last error code and description

## Common Use Cases

1. **Trading Automation**: Check account status before placing trades
2. **Risk Management Systems**: Monitor account health and margin levels
3. **Performance Tracking**: Record balance, equity, and profit for performance analysis
4. **Trading Dashboards**: Display account information in user interfaces
5. **Trade Validation**: Verify that account has sufficient margin before executing trades

## Error Handling

When `account_info()` fails:
1. It returns `None`
2. Check the error with `last_error()` 
3. Verify that you've successfully connected to the account with `login()`
4. Ensure that the terminal connection is still active

## Best Practices

1. Always check that the return value is not `None` before accessing properties
2. Use `_asdict()` for more flexible data handling
3. Consider using pandas for complex data analysis of account information
4. Regularly poll account information in automated trading systems to monitor account status
5. Always call `shutdown()` when finished with MetaTrader 5 operations
