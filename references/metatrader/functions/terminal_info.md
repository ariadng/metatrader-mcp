# MetaTrader 5 Python API: `terminal_info` Function

## Overview

The `terminal_info` function retrieves comprehensive information about the connected MetaTrader 5 client terminal's status and settings. This function provides details about the terminal configuration, connection status, permissions, and environmental settings in a single function call.

## Function Syntax

```python
terminal_info()
```

The `terminal_info` function takes no parameters.

## Return Value

The function returns a named tuple structure (namedtuple) containing detailed information about the MetaTrader 5 terminal. Returns `None` in case of an error, which can be checked using the `last_error()` function.

The named tuple contains many properties, including but not limited to:

| Property | Type | Description |
|----------|------|-------------|
| community_account | boolean | Flag indicating if connection to MetaQuotes ID is authorized |
| community_connection | boolean | Connection to MQL5.community status |
| connected | boolean | Connection to a trade server status |
| dlls_allowed | boolean | Permission to use DLL |
| trade_allowed | boolean | Permission to trade |
| tradeapi_disabled | boolean | Permission to use TradeAPI |
| email_enabled | boolean | Permission to send emails using SMTP-server and login specified in the terminal settings |
| ftp_enabled | boolean | Permission to send reports using FTP-server and login specified in the terminal settings |
| notifications_enabled | boolean | Permission to send notifications to smartphone |
| mqid | boolean | Flag indicating presence of MetaQuotes ID data for Push notifications |
| build | integer | Terminal build number |
| maxbars | integer | Maximum bars count in a chart |
| codepage | integer | Codepage of the language installed in the client terminal |
| ping_last | integer | Last known ping to a trade server in microseconds |
| community_balance | float | Balance in MQL5.community |
| retransmission | float | Percentage of resent network packets |
| company | string | Company name |
| name | string | Terminal name |
| language | string | Language of the terminal |
| path | string | Folder from which the terminal is started |
| data_path | string | Folder in which terminal data are stored |
| commondata_path | string | Common path for all terminals installed on a computer |

## Important Notes

- You must call `initialize()` to establish a connection to the MetaTrader 5 terminal before calling `terminal_info()`
- The function retrieves all data that would normally require multiple calls to TerminalInfoInteger, TerminalInfoDouble, and TerminalInfoString functions in MQL5
- The returned named tuple can be converted to a dictionary using the `_asdict()` method for easier data manipulation

## Usage Examples

### Basic Terminal Information Retrieval

```python
import MetaTrader5 as mt5

# Establish connection to the MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

# Get terminal information
terminal_info = mt5.terminal_info()
if terminal_info is not None:
    # Display key terminal properties
    print("Terminal connected:", terminal_info.connected)
    print("Trade allowed:", terminal_info.trade_allowed)
    print("Terminal build:", terminal_info.build)
    print("Terminal name:", terminal_info.name)
    print("Terminal path:", terminal_info.path)
else:
    print("Failed to get terminal info, error code =", mt5.last_error())

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

# Get terminal information
terminal_info = mt5.terminal_info()
if terminal_info is not None:
    # Convert to dictionary
    terminal_info_dict = terminal_info._asdict()
    
    # Display all terminal properties
    print("Terminal Information:")
    for prop in terminal_info_dict:
        print(f"  {prop}={terminal_info_dict[prop]}")
    
    # Convert the dictionary into DataFrame for analysis
    df = pd.DataFrame(list(terminal_info_dict.items()), columns=['property', 'value'])
    print("\nTerminal information as DataFrame:")
    print(df)
else:
    print("Failed to get terminal info, error code =", mt5.last_error())

# Shut down the connection when done
mt5.shutdown()
```

## Terminal Status Analysis

The terminal information can be used for various application purposes:

1. **Connection Status**: Verify that the terminal is properly connected to the trade server
2. **Permissions Check**: Determine if trading is allowed before attempting to execute trades
3. **Environment Information**: Access paths and language settings for application localization
4. **Performance Monitoring**: Check ping and retransmission values to monitor network performance
5. **MQL5 Community Access**: Verify community account status and balance

## Related Functions

- `initialize()`: Establishes a connection to the MetaTrader 5 terminal
- `shutdown()`: Closes the connection to the MetaTrader 5 terminal
- `version()`: Returns the MetaTrader 5 version information
- `account_info()`: Gets information about the trading account
- `last_error()`: Returns the last error code and description

## Common Use Cases

1. **Configuration Checks**: Verify that the terminal is set up correctly before operations
2. **Trading Permission Checks**: Ensure trading is allowed before executing trades
3. **Application Localization**: Adapt your application based on terminal language and paths
4. **Network Diagnostics**: Monitor connection quality with ping_last and retransmission values
5. **Feature Availability**: Check for permission to use specific features like notifications or emails

## Error Handling

When `terminal_info()` fails:
1. It returns `None`
2. Check the error with `last_error()` 
3. Verify that the terminal connection was successfully initialized
4. Check the terminal is running and not in a shutdown state

## Best Practices

1. Always check that the return value is not `None` before accessing properties
2. Use `_asdict()` for more flexible data handling
3. Consider using pandas for complex analysis of terminal information
4. Cache terminal settings that don't change frequently to improve performance
5. Always verify connection status before attempting trading operations
6. Always call `shutdown()` when finished with MetaTrader 5 operations

## Implementation Notes

The `terminal_info` function is particularly useful for creating robust applications that adapt to the terminal environment. By checking permissions, paths, and connection status, you can ensure your application functions correctly across different terminal configurations and environments.
