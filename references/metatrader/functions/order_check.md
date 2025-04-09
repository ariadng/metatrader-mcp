# MetaTrader 5 Python API: `order_check` Function

## Overview

The `order_check` function checks whether there are sufficient funds to perform a requested trading operation without actually executing it. It validates all aspects of a potential trade, including margin requirements, available funds, stop loss and take profit levels, and broker-specific rules. The function returns detailed results of the check in a structured format, allowing traders to verify if a trading operation can be successfully executed before sending it to the server.

## Function Syntax

```python
order_check(
   request      # request structure
)
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `request` | MqlTradeRequest structure | Trading request structure describing the desired trading operation. Required unnamed parameter. Includes action type, symbol, volume, price, stop levels, and other order parameters. |

## Return Value

Returns check result as the `MqlTradeCheckResult` structure, which contains the following fields:

| Field | Type | Description |
|-------|------|-------------|
| `retcode` | int | Return code (0 if successful) |
| `balance` | float | Balance value that will be after the execution of the trading operation |
| `equity` | float | Equity value that will be after the execution of the trading operation |
| `profit` | float | Floating profit value that will be after the execution of the trading operation |
| `margin` | float | Margin required for the trading operation |
| `margin_free` | float | Free margin that will be left after the execution of the trading operation |
| `margin_level` | float | Margin level that will be set after the execution of the trading operation |
| `comment` | string | Comment to the reply code (description of the error if any) |
| `request` | MqlTradeRequest | The original trading request structure passed to the function |

## Trade Request Structure (MqlTradeRequest)

The trading request structure contains the following fields:

| Field | Type | Description |
|-------|------|-------------|
| `action` | int | Trading operation type from the TRADE_REQUEST_ACTIONS enum |
| `magic` | int | Expert Advisor ID (magic number) |
| `order` | int | Order ticket for modifying orders |
| `symbol` | string | Trading instrument name |
| `volume` | float | Requested volume for a deal in lots |
| `price` | float | Price at which to execute order |
| `stoplimit` | float | Price for stop limit order activation |
| `sl` | float | Stop Loss level |
| `tp` | float | Take Profit level |
| `deviation` | int | Maximum acceptable deviation from requested price (in points) |
| `type` | int | Order type from ORDER_TYPE enum |
| `type_filling` | int | Order filling type from ORDER_TYPE_FILLING enum |
| `type_time` | int | Order lifetime type from ORDER_TYPE_TIME enum |
| `expiration` | datetime | Order expiration time (for orders with type_time=ORDER_TIME_SPECIFIED) |
| `comment` | string | Order comment |
| `position` | int | Position ticket for position operations |
| `position_by` | int | Opposite position ticket for position close by operations |

## TRADE_REQUEST_ACTIONS Enum

Values for the `action` parameter in the trading request:

| Constant | Value | Description |
|----------|-------|-------------|
| TRADE_ACTION_DEAL | 1 | Place an order for an instant deal with the specified parameters (market order) |
| TRADE_ACTION_PENDING | 5 | Place an order for performing a deal at specified conditions (pending order) |
| TRADE_ACTION_SLTP | 6 | Change open position Stop Loss and Take Profit |
| TRADE_ACTION_MODIFY | 7 | Change parameters of the previously placed trading order |
| TRADE_ACTION_REMOVE | 8 | Remove previously placed pending order |
| TRADE_ACTION_CLOSE_BY | 10 | Close a position by an opposite one |

## ORDER_TYPE_FILLING Enum

Values for the `type_filling` parameter, which determines how an order is filled:

| Constant | Value | Description |
|----------|-------|-------------|
| ORDER_FILLING_FOK | 0 | Fill or Kill - order can be executed only in the specified volume, otherwise it will be canceled |
| ORDER_FILLING_IOC | 1 | Immediate or Cancel - execute as much as possible and cancel the remaining volume |
| ORDER_FILLING_RETURN | 2 | Return execution - if filled partially, a market or limit order with remaining volume is not canceled but processed further |

## ORDER_TYPE_TIME Enum

Values for the `type_time` parameter, which determines how long an order is active:

| Constant | Value | Description |
|----------|-------|-------------|
| ORDER_TIME_GTC | 0 | Good Till Cancelled - order stays in the queue until manually canceled |
| ORDER_TIME_DAY | 1 | Day Order - order is active only during the current trading day |
| ORDER_TIME_SPECIFIED | 2 | Order is active until the specified date |
| ORDER_TIME_SPECIFIED_DAY | 3 | The order is active until 23:59:59 of the specified day |

## Important Notes

- The function is similar to the MQL5 function `OrderCheck()`
- Successful check does not guarantee successful execution - market conditions might change between check and execution
- The function validates margin requirements, broker restrictions, available balance, and other trading limitations
- All fields in the trading request must be properly filled with valid values
- The symbol must be available in the Market Watch for the check to work correctly
- The request structure passed to `order_check()` is included in the result structure in the `request` field
- When checking market orders, current market prices are used for calculations

## Usage Examples

### Example 1: Basic Order Validation

```python
import MetaTrader5 as mt5
import pprint

# Establish connection to MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

# Prepare the trading request for a market buy order
symbol = "EURUSD"
lot = 0.1
point = mt5.symbol_info(symbol).point
price = mt5.symbol_info_tick(symbol).ask
deviation = 20

# Make sure the symbol is available in Market Watch
if not mt5.symbol_info(symbol).visible:
    mt5.symbol_select(symbol, True)

# Create the request structure
request = {
    "action": mt5.TRADE_ACTION_DEAL,
    "symbol": symbol,
    "volume": lot,
    "type": mt5.ORDER_TYPE_BUY,
    "price": price,
    "sl": price - 100 * point,
    "tp": price + 100 * point,
    "deviation": deviation,
    "magic": 12345,
    "comment": "Python order check example",
    "type_time": mt5.ORDER_TIME_GTC,
    "type_filling": mt5.ORDER_FILLING_IOC,
}

# Perform the check
result = mt5.order_check(request)

# Display results
print("Order check result:")
print("  Return Code:", result.retcode)
if result.retcode == 0:
    print("  Available Balance:", result.balance)
    print("  Equity After Order:", result.equity)
    print("  Profit:", result.profit)
    print("  Margin Required:", result.margin)
    print("  Free Margin Remaining:", result.margin_free)
    print("  Margin Level After Order:", result.margin_level, "%")
    print("  Comment:", result.comment)
    print("\nThe order can be placed successfully.")
else:
    print("  Comment:", result.comment)
    print("\nThe order check failed. The order cannot be placed.")

# Shut down connection to MetaTrader 5
mt5.shutdown()
```

### Example 2: Check Multiple Order Types

```python
import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime, timedelta

# Establish connection to MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

def check_order(request):
    """
    Perform order check and return results in a formatted way
    
    Args:
        request: Trading request dictionary
        
    Returns:
        Dictionary with check results
    """
    # Perform the check
    result = mt5.order_check(request)
    
    # Convert the result to a dictionary
    result_dict = result._asdict() if result is not None else {}
    
    # Add request type info for clearer output
    if 'type' in request:
        order_type_map = {
            mt5.ORDER_TYPE_BUY: "BUY",
            mt5.ORDER_TYPE_SELL: "SELL",
            mt5.ORDER_TYPE_BUY_LIMIT: "BUY LIMIT",
            mt5.ORDER_TYPE_SELL_LIMIT: "SELL LIMIT",
            mt5.ORDER_TYPE_BUY_STOP: "BUY STOP",
            mt5.ORDER_TYPE_SELL_STOP: "SELL STOP",
            mt5.ORDER_TYPE_BUY_STOP_LIMIT: "BUY STOP LIMIT",
            mt5.ORDER_TYPE_SELL_STOP_LIMIT: "SELL STOP LIMIT",
        }
        result_dict['order_type'] = order_type_map.get(request['type'], "UNKNOWN")
    
    # Add action info
    if 'action' in request:
        action_map = {
            mt5.TRADE_ACTION_DEAL: "MARKET ORDER",
            mt5.TRADE_ACTION_PENDING: "PENDING ORDER",
            mt5.TRADE_ACTION_SLTP: "MODIFY SL/TP",
            mt5.TRADE_ACTION_MODIFY: "MODIFY ORDER",
            mt5.TRADE_ACTION_REMOVE: "REMOVE ORDER",
            mt5.TRADE_ACTION_CLOSE_BY: "CLOSE BY",
        }
        result_dict['action_type'] = action_map.get(request['action'], "UNKNOWN")
    
    return result_dict

# Define the symbol to test
symbol = "EURUSD"
point = mt5.symbol_info(symbol).point
price = mt5.symbol_info_tick(symbol).ask
expiration = datetime.now() + timedelta(days=1)

# Make sure the symbol is available in Market Watch
if not mt5.symbol_info(symbol).visible:
    mt5.symbol_select(symbol, True)

# Prepare different request types to check
requests = [
    # Market Buy order
    {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": 0.1,
        "type": mt5.ORDER_TYPE_BUY,
        "price": price,
        "sl": price - 100 * point,
        "tp": price + 100 * point,
        "deviation": 20,
        "magic": 12345,
        "comment": "Python market buy",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    },
    # Market Sell order
    {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": 0.1,
        "type": mt5.ORDER_TYPE_SELL,
        "price": mt5.symbol_info_tick(symbol).bid,
        "sl": mt5.symbol_info_tick(symbol).bid + 100 * point,
        "tp": mt5.symbol_info_tick(symbol).bid - 100 * point,
        "deviation": 20,
        "magic": 12345,
        "comment": "Python market sell",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    },
    # Buy Limit order
    {
        "action": mt5.TRADE_ACTION_PENDING,
        "symbol": symbol,
        "volume": 0.1,
        "type": mt5.ORDER_TYPE_BUY_LIMIT,
        "price": price - 20 * point,
        "sl": price - 120 * point,
        "tp": price + 80 * point,
        "deviation": 0,
        "magic": 12345,
        "comment": "Python buy limit",
        "type_time": mt5.ORDER_TIME_SPECIFIED,
        "expiration": expiration,
        "type_filling": mt5.ORDER_FILLING_IOC,
    },
    # Buy Stop order
    {
        "action": mt5.TRADE_ACTION_PENDING,
        "symbol": symbol,
        "volume": 0.1,
        "type": mt5.ORDER_TYPE_BUY_STOP,
        "price": price + 20 * point,
        "sl": price - 80 * point,
        "tp": price + 120 * point,
        "deviation": 0,
        "magic": 12345,
        "comment": "Python buy stop",
        "type_time": mt5.ORDER_TIME_DAY,
        "type_filling": mt5.ORDER_FILLING_IOC,
    },
]

# Check all orders and gather results
check_results = []
for request in requests:
    check_results.append(check_order(request))

# Convert to DataFrame for nice display
if check_results:
    df = pd.DataFrame(check_results)
    
    # Display the results
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1000)
    print("Order Check Results:")
    print(df[['action_type', 'order_type', 'retcode', 'comment', 'margin', 'margin_free']])

# Shut down connection to MetaTrader 5
mt5.shutdown()
```

### Example 3: Risk Management with Order Check

```python
import MetaTrader5 as mt5
import pandas as pd
import numpy as np

# Establish connection to MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

def calculate_safe_lot_size(symbol, risk_percent, stop_loss_points):
    """
    Calculate the safe lot size based on account balance, risk percentage and stop loss
    
    Args:
        symbol: Trading symbol
        risk_percent: Risk percentage (1-100)
        stop_loss_points: Stop loss distance in points
        
    Returns:
        tuple: (safe_lot_size, margin_required, potential_loss)
    """
    # Get account info
    account_info = mt5.account_info()
    if account_info is None:
        return None
    
    balance = account_info.balance
    
    # Calculate max risk amount in account currency
    max_risk_amount = balance * (risk_percent / 100)
    
    # Get symbol info
    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is None:
        return None
    
    # Make sure the symbol is selected
    if not symbol_info.visible:
        mt5.symbol_select(symbol, True)
    
    # Get the contract size and point value
    contract_size = symbol_info.trade_contract_size
    point = symbol_info.point
    price = mt5.symbol_info_tick(symbol).ask
    
    # Calculate the value of one pip in the account currency
    pip_value = contract_size * 10 * point
    
    # Calculate potential loss per lot with the given stop loss
    loss_per_lot = None
    
    # Try increasing lot sizes until we find the maximum that fits our risk profile
    lot_step = symbol_info.volume_step
    min_lot = symbol_info.volume_min
    max_lot = symbol_info.volume_max
    
    current_lot = min_lot
    suitable_lot = 0
    margin_required = 0
    potential_loss = 0
    
    while current_lot <= max_lot:
        # Calculate expected loss based on stop loss
        potential_loss_check = calculate_potential_loss(symbol, current_lot, price, price - stop_loss_points * point)
        
        # Check if this lot size exceeds our risk tolerance
        if potential_loss_check > max_risk_amount:
            break
        
        # Check margin requirements
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": current_lot,
            "type": mt5.ORDER_TYPE_BUY,
            "price": price,
            "sl": price - stop_loss_points * point,
            "tp": price + stop_loss_points * point,  # 1:1 risk-reward
            "deviation": 10,
            "magic": 12345,
            "comment": "Python risk check",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        
        # Check if we have enough margin
        result = mt5.order_check(request)
        if result is None or result.retcode != 0:
            # We've reached our margin limit
            break
        
        # This lot size is suitable
        suitable_lot = current_lot
        margin_required = result.margin
        potential_loss = potential_loss_check
        
        # Increase the lot size for next check
        current_lot += lot_step
        # Round to avoid floating point issues
        current_lot = round(current_lot / lot_step) * lot_step
    
    return (suitable_lot, margin_required, potential_loss)

def calculate_potential_loss(symbol, lot_size, open_price, close_price):
    """
    Calculate potential loss using order_calc_profit
    
    Args:
        symbol: Trading symbol
        lot_size: Position size in lots
        open_price: Opening price
        close_price: Closing price (stop loss level)
        
    Returns:
        float: Potential loss in account currency
    """
    profit = mt5.order_calc_profit(mt5.ORDER_TYPE_BUY, symbol, lot_size, open_price, close_price)
    if profit is None:
        return 0
    return abs(profit)

# Risk parameters
symbol = "EURUSD"
risk_percentage = 2  # Risk 2% of account balance
stop_loss_pips = 50  # 50 pips stop loss
stop_loss_points = stop_loss_pips * 10  # Convert pips to points (5-digit broker)

# Calculate safe lot size
result = calculate_safe_lot_size(symbol, risk_percentage, stop_loss_points)

if result:
    safe_lot, margin_required, potential_loss = result
    
    # Get account info for display
    account_info = mt5.account_info()
    
    print(f"Risk Management Analysis for {symbol}")
    print(f"Account Balance: {account_info.balance:.2f} {account_info.currency}")
    print(f"Risk Percentage: {risk_percentage}%")
    print(f"Stop Loss: {stop_loss_pips} pips")
    print(f"Maximum Risk Amount: {account_info.balance * risk_percentage / 100:.2f} {account_info.currency}")
    print("-" * 50)
    print(f"Safe Lot Size: {safe_lot:.2f}")
    print(f"Margin Required: {margin_required:.2f} {account_info.currency}")
    print(f"Potential Loss: {potential_loss:.2f} {account_info.currency}")
    print(f"Margin to Equity Ratio: {margin_required / account_info.equity * 100:.2f}%")
    
    # Display order check result for the suggested lot size
    price = mt5.symbol_info_tick(symbol).ask
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": safe_lot,
        "type": mt5.ORDER_TYPE_BUY,
        "price": price,
        "sl": price - stop_loss_points * mt5.symbol_info(symbol).point,
        "tp": price + stop_loss_points * mt5.symbol_info(symbol).point,
        "deviation": 10,
        "magic": 12345,
        "comment": "Python risk management",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    
    result = mt5.order_check(request)
    if result and result.retcode == 0:
        print("\nOrder Check Results:")
        print(f"  Return Code: {result.retcode}")
        print(f"  Balance After: {result.balance:.2f}")
        print(f"  Equity After: {result.equity:.2f}")
        print(f"  Margin Required: {result.margin:.2f}")
        print(f"  Free Margin After: {result.margin_free:.2f}")
        print(f"  Margin Level After: {result.margin_level:.2f}%")
        print("\nThe order passes all risk management checks and can be placed.")
    else:
        print("\nOrder check failed. The order cannot be placed with these parameters.")
        if result:
            print(f"Error: {result.comment}")

# Shut down connection to MetaTrader 5
mt5.shutdown()
```

## Advantages of Using `order_check()`

1. **Risk Management**: Test trades before execution to ensure they comply with your risk management rules
2. **Error Prevention**: Identify potential issues (insufficient funds, invalid parameters) before they cause trade failures
3. **Strategy Validation**: Verify that trading algorithms will have sufficient margin for planned operations
4. **Order Optimization**: Test different combinations of order parameters to find optimal trade configurations
5. **Simulation**: Simulate the effect of trades on account balance, equity, and margin without actual execution
6. **Broker Restriction Testing**: Check if broker-specific rules allow your intended trade
7. **Market Condition Analysis**: Determine if current market conditions support your trading plan

## Comparison with Related Functions

| Function | Purpose | Key Difference |
|----------|---------|----------------|
| `order_check()` | Validate if a trade can be executed | Checks all aspects of a trade but doesn't execute it |
| `order_send()` | Send a trade request to the server | Actually executes the trading operation |
| `order_calc_margin()` | Calculate margin for a trade | Only calculates margin without checking other requirements |
| `order_calc_profit()` | Calculate profit for a trade | Only calculates potential profit without checking execution feasibility |

## Related Functions

- `order_send()`: Sends trading requests to the server after validation with `order_check()`
- `order_calc_margin()`: Calculates the margin required for a trading operation
- `order_calc_profit()`: Calculates the potential profit for a specific trading operation
- `positions_total()`: Gets the number of open positions
- `positions_get()`: Retrieves information about open positions
- `orders_total()`: Gets the number of active orders
- `orders_get()`: Retrieves information about active orders
- `account_info()`: Gets information about the current trading account
- `symbol_info()`: Gets information about a trading symbol
- `symbol_info_tick()`: Gets the latest price data for a symbol
- `initialize()`: Establishes a connection to the MetaTrader 5 terminal
- `shutdown()`: Closes the connection to the MetaTrader 5 terminal
- `last_error()`: Returns information about the last error

## Common Use Cases

1. **Pre-Trade Validation**: Validate trades before execution to ensure they meet all requirements
2. **Position Sizing**: Determine the maximum lot size that can be traded with available margin
3. **Risk Management**: Verify that a trade complies with risk management parameters
4. **Strategy Testing**: Test if automated strategy orders can be executed in current market conditions
5. **Broker Rule Compliance**: Check if the trade complies with broker-specific rules and limitations
6. **Account Simulation**: Simulate the effect of a trade on account balance and margin
7. **Multi-Order Validation**: Verify that a sequence of orders can be executed with available resources
8. **API Integration**: Use as a safety check in external trading systems before sending orders

## Error Handling

When using `order_check()`, the primary error information is contained in the returned structure:

1. The `retcode` field contains the error code (0 means success)
2. The `comment` field provides a description of any error that occurred
3. If `order_check()` returns `None`, check for errors with `last_error()`

Common errors include:
- Insufficient funds or margin
- Invalid symbol name or symbol not found
- Invalid order parameters (price, volume, stops)
- Trading for the symbol is disabled
- Symbol is not visible in Market Watch
- Invalid filling or execution type for the symbol
- Stop levels too close to current price

## Best Practices

1. **Always Check First**: Validate trades with `order_check()` before sending with `order_send()`
2. **Complete Request Structure**: Ensure all required fields in the request structure are properly filled
3. **Symbol Selection**: Make sure the symbol is added to Market Watch with `symbol_select()` before checking
4. **Error Analysis**: Always check the return code and comment to understand why a check failed
5. **Current Prices**: Use current market prices from `symbol_info_tick()` for realistic validation
6. **Proper Initialization**: Always initialize the connection with `initialize()` before using trading functions
7. **Resource Cleanup**: Close the connection with `shutdown()` when finished
8. **Parameter Validation**: Verify that order parameters (lot size, price levels) are within allowed ranges
9. **Request Reuse**: If a check is successful, you can reuse the same request structure with `order_send()`

## Implementation Notes

The `order_check()` function validation considers several factors:

1. **Account State**: Current balance, equity, and existing positions
2. **Margin Requirements**: Free margin available and margin required for the new position
3. **Stop Levels**: Minimum allowed distance for stop loss and take profit levels
4. **Lot Size Restrictions**: Minimum and maximum allowed lot sizes
5. **Price Limitations**: Maximum deviation from current price (for market orders)
6. **Fill Policy**: Order execution policy (Fill or Kill, Immediate or Cancel, Return)
7. **Symbol Trading Status**: Whether trading is enabled for the symbol
8. **Symbol Visibility**: Whether the symbol is in Market Watch
9. **Order Lifetime**: Order expiration settings for pending orders
10. **Broker-Specific Rules**: Other limitations imposed by the broker

Important considerations when using `order_check()`:
- The check is performed based on current market conditions, which may change by the time the order is actually sent
- Some broker-specific rules may not be fully validated by `order_check()`
- For market orders, spread and slippage may affect actual execution compared to the check
- The function does not account for trading session hours or upcoming market events
- Currency conversions may be applied if the profit currency differs from the account currency
