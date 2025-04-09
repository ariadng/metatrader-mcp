# MetaTrader 5 Python API: `order_send` Function

## Overview

The `order_send` function sends a trading request to the server for execution. It allows you to perform various trading operations such as opening and closing positions, placing pending orders, modifying existing orders, and setting stop loss and take profit levels. This function is the primary mechanism for executing all types of trading operations in the MetaTrader 5 platform through the Python API.

## Function Syntax

```python
order_send(
   request      # request structure
)
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `request` | MqlTradeRequest structure | Trading request structure describing the desired trading operation. Required unnamed parameter. Contains all parameters needed for the trade action such as symbol, volume, price, stop levels, etc. |

## Return Value

Returns execution result as the `MqlTradeResult` structure, which contains the following fields:

| Field | Type | Description |
|-------|------|-------------|
| `retcode` | int | Operation return code. Zero means successful execution |
| `deal` | int | Deal ticket if it is performed |
| `order` | int | Order ticket if it is placed |
| `volume` | float | Deal volume confirmed by broker |
| `price` | float | Deal price confirmed by broker |
| `bid` | float | Current bid price |
| `ask` | float | Current ask price |
| `comment` | string | Broker comment on operation (usually error description if failed) |
| `request` | MqlTradeRequest | The original trading request structure that was passed to the function |
| `request_id` | int | Request ID set by the terminal during dispatching |
| `retcode_external` | int | Return code of an external trading system |
| `balance` | float | Balance value after the execution of the deal |
| `equity` | float | Equity value after the execution of the deal |
| `profit` | float | The profit of the performed deal |
| `margin` | float | Margin required for the deal |
| `margin_free` | float | Free margin remaining after the deal |
| `margin_level` | float | Margin level after the deal |
| `comment` | string | Comment on the operation |

In case of failure, you can get the error code using the `last_error()` function.

## The Trade Request Structure (MqlTradeRequest)

The trading request structure contains fields that define the parameters for executing a trade. Here is a detailed description of each field:

| Field | Type | Description |
|-------|------|-------------|
| `action` | int | Trading operation type from the TRADE_REQUEST_ACTIONS enum |
| `magic` | int | Expert Advisor ID (magic number) to identify which EA sent the order |
| `order` | int | Order ticket for modifying existing orders |
| `symbol` | string | Trading instrument name (e.g., "EURUSD") |
| `volume` | float | Requested volume for a deal in lots |
| `price` | float | Price at which the order should be executed |
| `stoplimit` | float | Price level for placing a limit order when the price reaches the `price` parameter (Stop Limit orders) |
| `sl` | float | Stop Loss level |
| `tp` | float | Take Profit level |
| `deviation` | int | Maximum acceptable deviation from the requested price (in points) |
| `type` | int | Order type from ORDER_TYPE enum |
| `type_filling` | int | Order filling type from ORDER_TYPE_FILLING enum |
| `type_time` | int | Order lifetime type from ORDER_TYPE_TIME enum |
| `expiration` | datetime | Order expiration time (for orders with type_time=ORDER_TIME_SPECIFIED) |
| `comment` | string | Order comment |
| `position` | int | Position ticket for position operations (required when modifying or closing positions) |
| `position_by` | int | Opposite position ticket for position close by operations |

## Trading Operation Types (TRADE_REQUEST_ACTIONS)

Values for the `action` parameter in the trading request:

| Constant | Value | Description |
|----------|-------|-------------|
| TRADE_ACTION_DEAL | 1 | Place an order for an instant deal (market order) |
| TRADE_ACTION_PENDING | 5 | Place a pending order |
| TRADE_ACTION_SLTP | 6 | Modify Stop Loss and Take Profit for an open position |
| TRADE_ACTION_MODIFY | 7 | Modify parameters of a previously placed order |
| TRADE_ACTION_REMOVE | 8 | Delete a previously placed pending order |
| TRADE_ACTION_CLOSE_BY | 10 | Close a position by an opposite one |

## Order Types (ORDER_TYPE)

Values for the `type` parameter:

| Constant | Value | Description |
|----------|-------|-------------|
| ORDER_TYPE_BUY | 0 | Market Buy order |
| ORDER_TYPE_SELL | 1 | Market Sell order |
| ORDER_TYPE_BUY_LIMIT | 2 | Buy Limit pending order |
| ORDER_TYPE_SELL_LIMIT | 3 | Sell Limit pending order |
| ORDER_TYPE_BUY_STOP | 4 | Buy Stop pending order |
| ORDER_TYPE_SELL_STOP | 5 | Sell Stop pending order |
| ORDER_TYPE_BUY_STOP_LIMIT | 6 | Upon reaching the price, a Buy Limit pending order is placed with the `stoplimit` price |
| ORDER_TYPE_SELL_STOP_LIMIT | 7 | Upon reaching the price, a Sell Limit pending order is placed with the `stoplimit` price |
| ORDER_TYPE_CLOSE_BY | 8 | Order to close a position by an opposite one |

## Order Filling Types (ORDER_TYPE_FILLING)

Values for the `type_filling` parameter:

| Constant | Value | Description |
|----------|-------|-------------|
| ORDER_FILLING_FOK | 0 | Fill or Kill - order can be executed only in the specified volume, otherwise it will be canceled |
| ORDER_FILLING_IOC | 1 | Immediate or Cancel - execute as much as possible and cancel the remaining volume |
| ORDER_FILLING_RETURN | 2 | Return execution - if filled partially, a market or limit order with remaining volume is not canceled but processed further |

## Order Lifetime Types (ORDER_TYPE_TIME)

Values for the `type_time` parameter:

| Constant | Value | Description |
|----------|-------|-------------|
| ORDER_TIME_GTC | 0 | Good Till Cancelled - order stays in the queue until manually canceled |
| ORDER_TIME_DAY | 1 | Day Order - order is active only during the current trading day |
| ORDER_TIME_SPECIFIED | 2 | Order is active until the specified date |
| ORDER_TIME_SPECIFIED_DAY | 3 | The order is active until 23:59:59 of the specified day |

## Order Execution Scenarios

The `order_send` function handles various execution scenarios based on broker execution mode:

### 1. Request Execution
For brokers with Request Execution mode, you must specify:
- action
- symbol
- volume
- price
- sl (optional)
- tp (optional)
- deviation
- type
- type_filling

### 2. Instant Execution
For brokers with Instant Execution mode, you must specify:
- action
- symbol
- volume
- price
- sl (optional)
- tp (optional)
- deviation
- type
- type_filling

### 3. Market Execution
For brokers with Market Execution mode, you must specify:
- action
- symbol
- volume
- type
- type_filling

### 4. Exchange Execution
For brokers with Exchange Execution mode, you must specify:
- action
- symbol
- volume
- type
- type_filling

## Important Notes

- You must call `initialize()` to establish a connection to the MetaTrader 5 terminal before using `order_send()`
- The symbol must be selected in Market Watch for the function to work correctly (use `symbol_select()` if needed)
- Fill all required fields in the request structure for your specific trading operation type
- Different brokers may support different execution modes and filling types
- The function is similar to the MQL5 function `OrderSend()`
- Successful sending of a request does not guarantee that the requested trading operation will be executed successfully
- Always check the return code in the result structure to verify if the operation was successful
- If the operation fails, check the `comment` field in the result structure for error details
- Use unique magic numbers to identify orders from different trading systems or strategies
- Market orders in Market Execution mode do not require a price specification
- For modifying positions, you must provide the position ticket

## Usage Examples

### Example 1: Opening and Closing a Market Order

```python
import time
import MetaTrader5 as mt5

# Establish connection to MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

# Define the symbol to trade
symbol = "EURUSD"

# Make sure the symbol is available in Market Watch
symbol_info = mt5.symbol_info(symbol)
if symbol_info is None:
    print(f"{symbol} not found, cannot call order_send()")
    mt5.shutdown()
    quit()

# If the symbol is not visible in MarketWatch, add it
if not symbol_info.visible:
    print(f"{symbol} is not visible, trying to switch it on")
    if not mt5.symbol_select(symbol, True):
        print(f"symbol_select({symbol}) failed, exit")
        mt5.shutdown()
        quit()

# Prepare trading parameters
lot = 0.1  # trading volume in lots
point = mt5.symbol_info(symbol).point  # symbol point value
price = mt5.symbol_info_tick(symbol).ask  # current ask price
deviation = 20  # allowed deviation in points

# Create a request to open a BUY position
request = {
    "action": mt5.TRADE_ACTION_DEAL,
    "symbol": symbol,
    "volume": lot,
    "type": mt5.ORDER_TYPE_BUY,
    "price": price,
    "sl": price - 100 * point,  # stop loss at 100 points
    "tp": price + 100 * point,  # take profit at 100 points
    "deviation": deviation,
    "magic": 234000,  # unique identifier (magic number)
    "comment": "python script open",
    "type_time": mt5.ORDER_TIME_GTC,  # good till canceled
    "type_filling": mt5.ORDER_FILLING_IOC,  # immediate or cancel
}

# Send the trading request
result = mt5.order_send(request)

# Check if the order was successful
print(f"1. order_send(): by {symbol} {lot} lots at {price} with deviation={deviation} points")
if result.retcode != mt5.TRADE_RETCODE_DONE:
    print(f"2. order_send failed, retcode={result.retcode}")
    # Request the result as a dictionary and display it element by element
    result_dict = result._asdict()
    for field in result_dict.keys():
        print(f"   {field}={result_dict[field]}")
        # If this is a trading request structure, display it element by element as well
        if field == "request":
            traderequest_dict = result_dict[field]._asdict()
            for tradereq_field in traderequest_dict:
                print(f"       traderequest: {tradereq_field}={traderequest_dict[tradereq_field]}")
    print("shutdown() and quit")
    mt5.shutdown()
    quit()

print("2. order_send done,", result)
print(f"   opened position with POSITION_TICKET={result.order}")
print(f"   sleep 2 seconds before closing position #{result.order}")
time.sleep(2)  # wait for 2 seconds before closing

# Create a request to close the BUY position
position_id = result.order
price = mt5.symbol_info_tick(symbol).bid  # current bid price
request = {
    "action": mt5.TRADE_ACTION_DEAL,
    "symbol": symbol,
    "volume": lot,
    "type": mt5.ORDER_TYPE_SELL,  # sell to close a buy position
    "position": position_id,  # ticket of the position to close
    "price": price,
    "deviation": deviation,
    "magic": 234000,
    "comment": "python script close",
    "type_time": mt5.ORDER_TIME_GTC,
    "type_filling": mt5.ORDER_FILLING_IOC,
}

# Send the trading request
result = mt5.order_send(request)

# Check if the order was successful
print(f"3. close position #{position_id}: sell {symbol} {lot} lots at {price} with deviation={deviation} points")
if result.retcode != mt5.TRADE_RETCODE_DONE:
    print(f"4. order_send failed, retcode={result.retcode}")
    print("   result", result)
else:
    print(f"4. position #{position_id} closed, {result}")
    # Request the result as a dictionary and display it element by element
    result_dict = result._asdict()
    for field in result_dict.keys():
        print(f"   {field}={result_dict[field]}")
        # If this is a trading request structure, display it element by element as well
        if field == "request":
            traderequest_dict = result_dict[field]._asdict()
            for tradereq_field in traderequest_dict:
                print(f"       traderequest: {tradereq_field}={traderequest_dict[tradereq_field]}")

# Shut down connection to the MetaTrader 5 terminal
mt5.shutdown()
```

### Example 2: Placing a Pending Order

```python
import MetaTrader5 as mt5
from datetime import datetime, timedelta

# Establish connection to MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

def place_pending_order(
    symbol, order_type, volume, price, 
    stop_loss=0.0, take_profit=0.0, 
    comment="python pending order", 
    expiration_days=7
):
    """
    Place a pending order
    
    Args:
        symbol: Trading symbol
        order_type: Order type (mt5.ORDER_TYPE_BUY_LIMIT, mt5.ORDER_TYPE_SELL_LIMIT, etc.)
        volume: Trading volume in lots
        price: Order price level
        stop_loss: Stop Loss level (0 means not set)
        take_profit: Take Profit level (0 means not set)
        comment: Order comment
        expiration_days: Number of days until the order expires
        
    Returns:
        Result dictionary with operation status
    """
    # Ensure symbol is available
    if not mt5.symbol_select(symbol, True):
        print(f"Failed to select {symbol}")
        return None
    
    # Get symbol information
    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is None:
        print(f"Symbol {symbol} not found")
        return None
    
    # Calculate expiration date (if needed)
    expiration = None
    if expiration_days > 0:
        expiration = datetime.now() + timedelta(days=expiration_days)
    
    # Create order request
    request = {
        "action": mt5.TRADE_ACTION_PENDING,
        "symbol": symbol,
        "volume": volume,
        "type": order_type,
        "price": price,
        "sl": stop_loss,
        "tp": take_profit,
        "deviation": 10,
        "magic": 123456,
        "comment": comment,
        "type_time": mt5.ORDER_TIME_SPECIFIED if expiration else mt5.ORDER_TIME_GTC,
        "expiration": expiration,
        "type_filling": mt5.ORDER_FILLING_FOK,
    }
    
    # Send the order
    result = mt5.order_send(request)
    
    # Process the result
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"Failed to place order: {result.retcode}, {result.comment}")
        return None
    
    # Convert result to dictionary for better display
    result_dict = result._asdict()
    
    return result_dict

# Define trading parameters
symbol = "EURUSD"
current_price = mt5.symbol_info_tick(symbol).ask
point = mt5.symbol_info(symbol).point

# Place a buy limit order 20 points below current price
buy_price = current_price - 20 * point
sl_price = buy_price - 50 * point
tp_price = buy_price + 100 * point

# Place the pending order
result = place_pending_order(
    symbol=symbol,
    order_type=mt5.ORDER_TYPE_BUY_LIMIT,
    volume=0.1,
    price=buy_price,
    stop_loss=sl_price,
    take_profit=tp_price,
    comment="Python script buy limit",
    expiration_days=3
)

# Display the result
if result:
    print(f"Pending order placed successfully:")
    print(f"  Order ticket: {result['order']}")
    print(f"  Type: Buy Limit")
    print(f"  Price: {buy_price}")
    print(f"  Stop Loss: {sl_price}")
    print(f"  Take Profit: {tp_price}")
    print(f"  Expiration: 3 days")

# Shut down connection to the MetaTrader 5 terminal
mt5.shutdown()
```

### Example 3: Modifying Stop Loss and Take Profit for an Open Position

```python
import MetaTrader5 as mt5

# Establish connection to MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

def modify_position_stops(position_ticket, new_sl, new_tp):
    """
    Modify Stop Loss and Take Profit for an open position
    
    Args:
        position_ticket: Ticket of the position to modify
        new_sl: New Stop Loss price (0 to remove)
        new_tp: New Take Profit price (0 to remove)
        
    Returns:
        True if modification was successful, False otherwise
    """
    # Get the position details
    positions = mt5.positions_get(ticket=position_ticket)
    if positions is None or len(positions) == 0:
        print(f"Position #{position_ticket} not found, error code: {mt5.last_error()}")
        return False
    
    position = positions[0]
    
    # Prepare the request
    request = {
        "action": mt5.TRADE_ACTION_SLTP,
        "symbol": position.symbol,
        "position": position_ticket,
        "sl": new_sl,
        "tp": new_tp,
    }
    
    # Send the request
    result = mt5.order_send(request)
    
    # Check the result
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"Failed to modify position #{position_ticket}, error code: {result.retcode}")
        print(f"Error description: {result.comment}")
        return False
    
    print(f"Position #{position_ticket} successfully modified")
    print(f"New SL: {new_sl}, New TP: {new_tp}")
    return True

# Get all open positions
positions = mt5.positions_get()

if positions is None:
    print("No positions, error code:", mt5.last_error())
elif len(positions) == 0:
    print("No positions")
else:
    # Modify the first position in the list for demonstration
    position = positions[0]
    symbol = position.symbol
    position_id = position.ticket
    
    # Get symbol information
    symbol_info = mt5.symbol_info(symbol)
    point = symbol_info.point
    
    # Calculate new stop loss and take profit levels
    if position.type == mt5.POSITION_TYPE_BUY:
        # For buy positions, set SL below current price, TP above
        current_price = mt5.symbol_info_tick(symbol).bid
        new_sl = current_price - 75 * point
        new_tp = current_price + 150 * point
    else:
        # For sell positions, set SL above current price, TP below
        current_price = mt5.symbol_info_tick(symbol).ask
        new_sl = current_price + 75 * point
        new_tp = current_price - 150 * point
    
    print(f"Position to modify: #{position_id}, {symbol}, {'Buy' if position.type == 0 else 'Sell'}")
    print(f"Current SL: {position.sl}, Current TP: {position.tp}")
    print(f"New SL: {new_sl}, New TP: {new_tp}")
    
    # Modify the position
    result = modify_position_stops(position_id, new_sl, new_tp)
    print("Modification result:", "Success" if result else "Failed")

# Shut down connection to the MetaTrader 5 terminal
mt5.shutdown()
```

## Advantages of Using `order_send()`

1. **Complete Trading Control**: Provides full control over all aspects of trading operations including opening and closing positions, placing and modifying orders
2. **Comprehensive Feedback**: Returns detailed information about the execution result, including order/deal tickets, confirmation price, and error messages
3. **Versatility**: Supports all types of trading operations through a single, consistent interface
4. **Execution Options**: Allows specification of execution parameters like filling type and price deviation to handle different market conditions
5. **Automated Trading**: Enables building of fully automated trading systems by coupling with other analytical functions
6. **Risk Management**: Supports setting Stop Loss and Take Profit levels at the time of order placement
7. **Order Identification**: Allows setting magic numbers and comments for easy identification and management of orders
8. **Error Handling**: Provides detailed error codes and descriptions for troubleshooting failed orders

## Comparison with Related Functions

| Function | Purpose | Key Difference |
|----------|---------|----------------|
| `order_send()` | Execute trading operations | Actually executes trades and modifies positions/orders |
| `order_check()` | Validate if a trade can be executed | Only checks if a trade can be executed without actually executing it |
| `order_calc_margin()` | Calculate margin for a trade | Only calculates margin without executing any trade |
| `order_calc_profit()` | Calculate profit for a trade | Only calculates potential profit without executing any trade |
| `positions_total()` | Gets the number of open positions | Retrieves information about existing positions but doesn't create new ones |
| `positions_get()` | Retrieves information about open positions | Retrieves information about existing positions but doesn't create new ones |
| `orders_total()` | Gets the number of active orders | Retrieves information about existing orders but doesn't create new ones |
| `orders_get()` | Retrieves information about active orders | Retrieves information about existing orders but doesn't create new ones |
| `history_orders_get()` | Retrieves orders from trade history | Retrieves orders from trade history but doesn't create new ones |
| `history_deals_get()` | Retrieves deals from trade history | Retrieves deals from trade history but doesn't create new ones |
| `symbol_info()` | Gets information about a trading symbol | Retrieves information about a symbol but doesn't execute trades |
| `symbol_info_tick()` | Gets the latest price data for a symbol | Retrieves the latest price data but doesn't execute trades |
| `account_info()` | Gets information about the current trading account | Retrieves information about the account but doesn't execute trades |
| `initialize()` | Establishes a connection to the MetaTrader 5 terminal | Establishes a connection but doesn't execute trades |
| `shutdown()` | Closes the connection to the MetaTrader 5 terminal | Closes the connection but doesn't execute trades |
| `last_error()` | Returns information about the last error | Returns error information but doesn't execute trades |

## Common Use Cases

1. **Market Order Execution**: Opening Buy and Sell positions at current market prices
2. **Pending Order Placement**: Setting Buy Limit, Sell Limit, Buy Stop, and Sell Stop orders
3. **Position Modification**: Adjusting Stop Loss and Take Profit levels for open positions
4. **Position Closure**: Closing open positions partially or completely
5. **Order Modification**: Changing parameters of pending orders
6. **Order Cancellation**: Removing pending orders from the market
7. **Automated Trading**: Implementing algorithmic trading strategies with precise execution
8. **Risk Management**: Automating the setting and updating of stop levels based on market conditions
9. **Portfolio Management**: Managing multiple positions across different instruments
10. **Hedging**: Opening positions in opposite directions for hedging purposes

## Error Handling

Proper error handling is critical when using the `order_send()` function:

1. **Primary Result Check**: Always check the `retcode` field in the result structure
2. **Complete Error Information**: If `retcode` is not TRADE_RETCODE_DONE, examine the `comment` field
3. **Custom Error Handling**: Implement custom error handling for different return codes
4. **Retry Logic**: For some errors (like price changed or timeout), implement a retry mechanism
5. **Market Condition Validation**: Before sending orders, validate market conditions (like trading hours)
6. **Parameter Validation**: Verify all request parameters meet the broker's requirements
7. **Connection Check**: Ensure the terminal is connected before sending trading requests
8. **Last Error Retrieval**: Use `last_error()` for additional error information

Example of error handling:

```python
# Send a trading request
result = mt5.order_send(request)

# Check the execution result
if result is None:
    print(f"order_send() failed, error code: {mt5.last_error()}")
    # Handle complete failure
elif result.retcode != mt5.TRADE_RETCODE_DONE:
    # Handle specific error codes
    if result.retcode == mt5.TRADE_RETCODE_PRICE_CHANGED:
        print("Price changed, retrying with updated price...")
        # Update price and retry
    elif result.retcode == mt5.TRADE_RETCODE_INVALID_STOPS:
        print(f"Invalid stop levels: {result.comment}")
        # Recalculate stop levels and retry
    elif result.retcode == mt5.TRADE_RETCODE_TIMEOUT:
        print("Request timed out, retrying...")
        # Simple retry
    else:
        print(f"Order failed with error code: {result.retcode}")
        print(f"Error description: {result.comment}")
        # General error handling
else:
    print("Order executed successfully")
```

## Best Practices

1. **Connection Management**: Always establish a connection with `initialize()` before using trading functions
2. **Symbol Selection**: Ensure the symbol is visible in Market Watch with `symbol_select()` before trading
3. **Pre-Trade Validation**: Use `order_check()` to validate trades before execution with `order_send()`
4. **Current Prices**: Always get the latest prices with `symbol_info_tick()` before creating requests
5. **Unique Identification**: Set unique magic numbers for each trading strategy for easier tracking
6. **Descriptive Comments**: Use meaningful comments in orders to help identify their purpose
7. **Error Handling**: Implement comprehensive error handling and recovery mechanisms
8. **Resource Cleanup**: Always call `shutdown()` when finished with MetaTrader 5 operations
9. **Position Sizing**: Calculate appropriate position sizes based on account balance and risk parameters
10. **Broker Limitations**: Be aware of broker-specific limitations and minimum distance requirements
11. **Position Queue**: When executing multiple orders, implement a queue with proper error handling
12. **Transaction Logging**: Log all trading requests and results for audit and debugging purposes

## Implementation Notes

The `order_send()` function implementation considers several factors:

1. **Broker Execution Models**: Different brokers support different execution models (Market, Instant, Request, Exchange)
2. **Symbol Properties**: Different symbols have different trading parameters (contract size, minimum volume, price steps)
3. **Account Types**: Trading conditions vary between demo and real accounts
4. **Broker Rules**: Some brokers impose specific rules on stop levels, minimum volumes, and maximum number of orders
5. **Pending Order Conditions**: Pending orders require proper price levels, expiration times, and filling types
6. **Market Hours**: Orders may behave differently during market hours and off-market hours
7. **Price Gaps**: Market gaps may affect order execution, especially for pending orders
8. **Spread Considerations**: Wide spreads may impact the execution of market orders and trigger levels of pending orders
9. **Slippage**: Actual execution price may differ from requested price due to slippage
10. **Fast Markets**: Execution speed and accuracy may vary during fast-moving markets

For optimal results:

1. **Test on Demo**: Always test trading algorithms on demo accounts before using real money
2. **Continuous Monitoring**: Monitor trading operations to ensure they're executing as expected
3. **Transaction Optimization**: Minimize the number of requests to avoid overloading the server
4. **Proper Timeouts**: Set appropriate timeouts for trading operations
5. **Backup Strategies**: Have backup strategies in case primary trading operations fail
6. **Account Status Verification**: Verify account status before sending trading requests
7. **Risk Controls**: Implement proper risk controls to avoid excessive losses
8. **API Rate Limits**: Be aware of rate limits imposed by brokers on API requests

## Return Codes (ENUM_TRADE_RETCODE)

The `retcode` field in the result structure can contain one of the following values:

| Constant | Value | Description |
|----------|-------|-------------|
| TRADE_RETCODE_DONE | 10008 | Request completed successfully |
| TRADE_RETCODE_REJECT | 10009 | Request rejected |
| TRADE_RETCODE_CANCEL | 10010 | Request canceled by trader |
| TRADE_RETCODE_PLACED | 10011 | Order placed |
| TRADE_RETCODE_DONE_PARTIAL | 10012 | Request executed partially |
| TRADE_RETCODE_ERROR | 10013 | Request processing error |
| TRADE_RETCODE_TIMEOUT | 10014 | Request canceled by timeout |
| TRADE_RETCODE_INVALID | 10015 | Invalid request |
| TRADE_RETCODE_INVALID_VOLUME | 10016 | Invalid volume in the request |
| TRADE_RETCODE_INVALID_PRICE | 10017 | Invalid price in the request |
| TRADE_RETCODE_INVALID_STOPS | 10018 | Invalid stops in the request |
| TRADE_RETCODE_TRADE_DISABLED | 10019 | Trading is disabled |
| TRADE_RETCODE_MARKET_CLOSED | 10020 | Market is closed |
| TRADE_RETCODE_NO_MONEY | 10021 | Not enough money to complete the request |
| TRADE_RETCODE_PRICE_CHANGED | 10022 | Prices changed |
| TRADE_RETCODE_PRICE_OFF | 10023 | No quotes to process the request |
| TRADE_RETCODE_INVALID_EXPIRATION | 10024 | Invalid order expiration date in the request |
| TRADE_RETCODE_ORDER_CHANGED | 10025 | Order state changed |
| TRADE_RETCODE_TOO_MANY_REQUESTS | 10026 | Too frequent requests |
| TRADE_RETCODE_NO_CHANGES | 10027 | No changes in request |
| TRADE_RETCODE_SERVER_DISABLES_AT | 10028 | Autotrading disabled by server |
| TRADE_RETCODE_CLIENT_DISABLES_AT | 10029 | Autotrading disabled by client terminal |
| TRADE_RETCODE_LOCKED | 10030 | Request locked for processing |
| TRADE_RETCODE_FROZEN | 10031 | Order or position frozen |
| TRADE_RETCODE_INVALID_FILL | 10032 | Invalid order filling type |
| TRADE_RETCODE_CONNECTION | 10033 | No connection with the trade server |
| TRADE_RETCODE_ONLY_REAL | 10034 | Operation is allowed only for real accounts |
| TRADE_RETCODE_LIMIT_ORDERS | 10035 | The number of pending orders has reached the limit |
| TRADE_RETCODE_LIMIT_VOLUME | 10036 | The volume of orders and positions has reached the limit |

## Related Functions

- `order_check()`: Checks funds sufficiency for performing a trading operation
- `order_calc_margin()`: Calculates the margin required for a trading operation
- `order_calc_profit()`: Calculates the potential profit for a trading operation
- `positions_total()`: Gets the number of open positions
- `positions_get()`: Retrieves information about open positions
- `orders_total()`: Gets the number of active orders
- `orders_get()`: Retrieves information about active orders
- `history_orders_get()`: Retrieves orders from trade history
- `history_deals_get()`: Retrieves deals from trade history
- `symbol_info()`: Gets information about a trading symbol
- `symbol_info_tick()`: Gets the latest price data for a symbol
- `account_info()`: Gets information about the current trading account
- `initialize()`: Establishes a connection to the MetaTrader 5 terminal
- `shutdown()`: Closes the connection to the MetaTrader 5 terminal
- `last_error()`: Returns information about the last error
