# MetaTrader 5 Python API: `history_deals_total` Function

## Overview

The `history_deals_total` function retrieves the number of deals in the trading history within a specified time interval. This function is essential for analyzing historical trading activity, assessing trading frequency, and conducting performance analysis. A deal in MetaTrader 5 represents an actual execution of an order, which may include opening a position, closing a position, or a partial close operation.

## Function Syntax

```python
history_deals_total(
   date_from,    # date the deals are requested from
   date_to       # date, up to which the deals are requested
)
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `date_from` | datetime or int | Date from which deals are requested. Can be set as a `datetime` object or as the number of seconds elapsed since January 1, 1970 (Unix timestamp). This is a required unnamed parameter. |
| `date_to` | datetime or int | Date up to which deals are requested. Can be set as a `datetime` object or as the number of seconds elapsed since January 1, 1970 (Unix timestamp). This is a required unnamed parameter. |

## Return Value

Returns an integer value representing the total number of deals in the trading history within the specified time interval.

## Important Notes

- You must call `initialize()` to establish a connection to the MetaTrader 5 terminal before using `history_deals_total()`
- The function is similar to the MQL5 function `HistoryDealsTotal()`
- Both parameters (`date_from` and `date_to`) are mandatory
- The function counts all types of deals, including opening positions, closing positions, and partial closes
- The time range is inclusive of both the start and end dates
- Deals are counted based on their execution time
- Each trade operation may involve multiple deals (for example, closing a position might generate a separate deal for the position close and another for the profit/loss)
- To get detailed information about the counted deals, use the `history_deals_get()` function
- The function accesses the trade server's database, which may have limitations on the history period
- Excessive requests for historical data may impact the performance of the trading terminal

## Usage Examples

### Example 1: Basic Usage - Count Deals in History

```python
from datetime import datetime
import MetaTrader5 as mt5

# Establish connection to MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

# Define the time range
from_date = datetime(2023, 1, 1)
to_date = datetime.now()

# Get the number of deals in history
deals_count = mt5.history_deals_total(from_date, to_date)

if deals_count > 0:
    print(f"Total deals in history from {from_date} to {to_date}: {deals_count}")
else:
    print("No deals found in the specified history period")

# Shut down connection to the MetaTrader 5 terminal
mt5.shutdown()
```

### Example 2: Monthly Trading Activity Analysis

```python
from datetime import datetime, timedelta
import MetaTrader5 as mt5
import pandas as pd
import matplotlib.pyplot as plt

# Establish connection to MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

# Analyze trading activity over the past 12 months
def analyze_monthly_deals(months=12):
    """
    Analyze trading activity (deals) by month for the specified number of past months
    
    Args:
        months: Number of past months to analyze
        
    Returns:
        pandas DataFrame with monthly trading activity
    """
    current_date = datetime.now()
    monthly_activity = []
    
    for i in range(months):
        # Calculate month start and end dates
        end_month = current_date - timedelta(days=30*i)
        start_month = end_month.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        end_month = (start_month.replace(month=start_month.month % 12 + 1, 
                                         year=start_month.year + start_month.month // 12) -
                     timedelta(days=1))
        end_month = end_month.replace(hour=23, minute=59, second=59)
        
        # Get deal count for the month
        deal_count = mt5.history_deals_total(start_month, end_month)
        
        # Store the result
        monthly_activity.append({
            'Month': start_month.strftime('%Y-%m'),
            'DealCount': deal_count
        })
    
    # Convert to DataFrame and sort chronologically
    df = pd.DataFrame(monthly_activity)
    df = df.sort_values('Month')
    
    return df

# Get monthly activity data
monthly_data = analyze_monthly_deals(12)

# Display the results
print("Monthly Trading Activity - Deals (Past 12 Months):")
print(monthly_data)

# Create a bar chart visualization
plt.figure(figsize=(12, 6))
plt.bar(monthly_data['Month'], monthly_data['DealCount'])
plt.title('Number of Deals by Month')
plt.xlabel('Month')
plt.ylabel('Number of Deals')
plt.xticks(rotation=45)
plt.tight_layout()
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

# Shut down connection to the MetaTrader 5 terminal
mt5.shutdown()
```

### Example 3: Comparing Trading Frequency Between Time Periods

```python
from datetime import datetime, timedelta
import MetaTrader5 as mt5

# Establish connection to MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

def compare_trading_frequency():
    """
    Compare trading frequency (deals) between different time periods
    """
    now = datetime.now()
    
    # Define time periods to compare
    periods = {
        "Today": (now.replace(hour=0, minute=0, second=0), now),
        "Yesterday": ((now - timedelta(days=1)).replace(hour=0, minute=0, second=0),
                      (now - timedelta(days=1)).replace(hour=23, minute=59, second=59)),
        "This Week": ((now - timedelta(days=now.weekday())).replace(hour=0, minute=0, second=0), now),
        "Last Week": ((now - timedelta(days=now.weekday() + 7)).replace(hour=0, minute=0, second=0),
                      (now - timedelta(days=now.weekday() + 1)).replace(hour=23, minute=59, second=59)),
        "This Month": (now.replace(day=1, hour=0, minute=0, second=0), now),
        "Last Month": ((now.replace(day=1) - timedelta(days=1)).replace(day=1, hour=0, minute=0, second=0),
                       now.replace(day=1, hour=0, minute=0, second=0) - timedelta(seconds=1))
    }
    
    # Get deal counts for each period
    results = {}
    for period_name, (start_date, end_date) in periods.items():
        deal_count = mt5.history_deals_total(start_date, end_date)
        results[period_name] = {
            "Start Date": start_date,
            "End Date": end_date,
            "Deal Count": deal_count
        }
    
    # Calculate trading frequency (deals per day)
    for period_name, data in results.items():
        days_diff = (data["End Date"] - data["Start Date"]).total_seconds() / (24 * 3600)
        days_diff = max(days_diff, 1)  # Ensure at least 1 day for today
        data["Deals Per Day"] = data["Deal Count"] / days_diff
    
    # Display the results
    print("Trading Frequency Comparison")
    print("===========================")
    for period_name, data in results.items():
        print(f"{period_name}:")
        print(f"  Period: {data['Start Date']} to {data['End Date']}")
        print(f"  Deals: {data['Deal Count']}")
        print(f"  Deals Per Day: {data['Deals Per Day']:.2f}")
        print()
    
    # Compute some comparisons
    if results["This Week"]["Deal Count"] > 0 and results["Last Week"]["Deal Count"] > 0:
        week_change = ((results["This Week"]["Deals Per Day"] / results["Last Week"]["Deals Per Day"]) - 1) * 100
        print(f"Week-over-Week Change in Daily Trading Frequency: {week_change:.2f}%")
    
    if results["This Month"]["Deal Count"] > 0 and results["Last Month"]["Deal Count"] > 0:
        month_change = ((results["This Month"]["Deals Per Day"] / results["Last Month"]["Deals Per Day"]) - 1) * 100
        print(f"Month-over-Month Change in Daily Trading Frequency: {month_change:.2f}%")

# Run the comparison
compare_trading_frequency()

# Shut down connection to the MetaTrader 5 terminal
mt5.shutdown()
```

### Example 4: Calculating Average Daily Trading Volume

```python
from datetime import datetime, timedelta
import MetaTrader5 as mt5
import pandas as pd
import matplotlib.pyplot as plt

# Establish connection to MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

def calculate_trading_activity(days=90):
    """
    Calculate daily trading volume for the past specified number of days
    and analyze trends
    
    Args:
        days: Number of past days to analyze
    """
    current_date = datetime.now()
    daily_activity = []
    
    for i in range(days):
        # Calculate day start and end
        day_date = current_date - timedelta(days=i)
        day_start = day_date.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day_date.replace(hour=23, minute=59, second=59, microsecond=999999)
        
        # Get deal count for the day
        deal_count = mt5.history_deals_total(day_start, day_end)
        
        # Only include trading days (days with at least one deal)
        if deal_count > 0:
            # Store the result
            daily_activity.append({
                'Date': day_date.strftime('%Y-%m-%d'),
                'DealCount': deal_count,
                'WeekDay': day_date.strftime('%A')
            })
    
    # Convert to DataFrame
    df = pd.DataFrame(daily_activity)
    
    if df.empty:
        print("No trading activity found in the specified period")
        return
    
    # Calculate average daily trading volume
    avg_daily_volume = df['DealCount'].mean()
    print(f"Average Daily Trading Volume (last {days} days): {avg_daily_volume:.2f} deals")
    
    # Calculate trading volume by day of week
    day_of_week_stats = df.groupby('WeekDay')['DealCount'].agg(['mean', 'count', 'sum'])
    day_of_week_stats = day_of_week_stats.reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
    print("\nTrading Volume by Day of Week:")
    print(day_of_week_stats)
    
    # Plot daily trading volume
    plt.figure(figsize=(14, 7))
    plt.plot(df['Date'], df['DealCount'], marker='o')
    plt.axhline(y=avg_daily_volume, color='r', linestyle='--', label=f'Average: {avg_daily_volume:.2f}')
    plt.title('Daily Trading Volume')
    plt.xlabel('Date')
    plt.ylabel('Number of Deals')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.grid(True, alpha=0.3)
    plt.show()
    
    # Plot average trading volume by day of week
    plt.figure(figsize=(10, 6))
    day_of_week_stats['mean'].plot(kind='bar')
    plt.title('Average Trading Volume by Day of Week')
    plt.xlabel('Day of Week')
    plt.ylabel('Average Number of Deals')
    plt.tight_layout()
    plt.grid(axis='y', alpha=0.3)
    plt.show()

# Run the analysis
calculate_trading_activity(90)  # Analyze the past 90 days

# Shut down connection to the MetaTrader 5 terminal
mt5.shutdown()
```

## Advantages of Using `history_deals_total()`

1. **Performance Efficiency**: Quickly determines the number of historical deals without retrieving detailed data
2. **Resource Optimization**: Uses less memory and bandwidth compared to retrieving full deal details
3. **Initial Assessment**: Provides a quick overview of trading activity within a time period
4. **Time Period Analysis**: Facilitates analysis of trading frequency over different time periods
5. **Activity Validation**: Helps verify trading activity levels for automated systems
6. **Audit Preparation**: Useful for preliminary assessment before conducting detailed trade audits
7. **Trading Frequency Analysis**: Supports analysis of trading patterns and frequencies
8. **Documentation**: Supports record-keeping of trading activity volume
9. **System Monitoring**: Helps monitor automated trading system activity levels
10. **Performance Metrics**: Provides basic metrics for evaluating trading performance
11. **Client Reporting**: Useful for generating summary statistics for client reports
12. **Database Query Optimization**: Allows checking the deal count before making more resource-intensive queries

## Comparison with Related Functions

| Function | Purpose | Key Difference |
|----------|---------|----------------|
| `history_deals_total()` | Get count of deals in history | Returns only the count, not deal details |
| `history_deals_get()` | Get detailed info about deals in history | Returns complete information about historical deals, not just count |
| `history_orders_total()` | Get count of orders in history | Counts orders (trade requests) instead of deals (executions) |
| `positions_total()` | Get count of open positions | Counts current open positions, not historical deals |
| `orders_total()` | Get count of active orders | Counts pending orders, not historical deals |

## Related Functions

- `history_deals_get()`: Retrieves detailed information about deals in history
- `history_orders_total()`: Gets the number of orders in the trading history
- `history_orders_get()`: Retrieves detailed information about orders in history
- `positions_total()`: Gets the number of open positions
- `positions_get()`: Retrieves detailed information about open positions
- `orders_total()`: Gets the number of active orders
- `orders_get()`: Retrieves detailed information about active orders
- `account_info()`: Gets information about the current trading account
- `initialize()`: Establishes a connection to the MetaTrader 5 terminal
- `shutdown()`: Closes the connection to the MetaTrader 5 terminal

## Common Use Cases

1. **Trading Activity Analysis**: Analyzing trading frequency over different time periods
2. **Performance Monitoring**: Monitoring the execution activity levels of trading strategies
3. **System Validation**: Verifying that automated trading systems are executing deals as expected
4. **Historical Audits**: Preparing for detailed historical trade audits
5. **Reporting**: Generating summary statistics for trading reports
6. **Backtest Validation**: Verifying that backtesting generated the expected number of trades
7. **Trading Journal Analysis**: Supporting trading journal analysis of activity patterns
8. **Performance Evaluation**: Evaluating trading performance based on activity metrics
9. **Risk Assessment**: Initial assessment of trading activity for risk management
10. **Performance Tracking**: Tracking trading activity metrics over time
11. **System Monitoring**: Monitoring for unusual activity levels that might indicate issues
12. **API Query Optimization**: Optimizing resource usage by checking counts before retrieving full details

## Error Handling

Proper error handling is essential when working with the `history_deals_total()` function:

```python
from datetime import datetime, timedelta
import MetaTrader5 as mt5

# Establish connection to MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

try:
    # Define the time range
    to_date = datetime.now()
    from_date = to_date - timedelta(days=30)
    
    # Get the number of deals in history
    deals_count = mt5.history_deals_total(from_date, to_date)
    
    if deals_count is None:
        error_code = mt5.last_error()
        print(f"Failed to get history deals count, error code: {error_code}")
    else:
        print(f"Successfully retrieved history deals count: {deals_count}")
        
except Exception as e:
    print(f"An unexpected error occurred: {e}")
    
    # Check if connection is still active and try to reconnect if needed
    if not mt5.terminal_info().connected:
        print("Connection to MetaTrader 5 lost, attempting to reconnect...")
        if not mt5.initialize():
            print("Failed to reconnect, error code =", mt5.last_error())

finally:
    # Always ensure proper shutdown
    mt5.shutdown()
```

Common error scenarios:
1. **Connection Issues**: The terminal is not running or connection was lost
2. **Invalid Parameters**: Incorrect date format or range specification
3. **Server Limitations**: Attempting to access history outside the available range
4. **Permission Issues**: The application doesn't have sufficient permissions
5. **Memory Limitations**: Insufficient memory to process the request
6. **History Access Restrictions**: Some brokers may restrict access to full history

## Best Practices

1. **Connection Management**: Always establish a connection with `initialize()` before using history functions
2. **Resource Cleanup**: Always call `shutdown()` when finished with MetaTrader 5 operations
3. **Parameter Validation**: Ensure date parameters are in valid formats and logical ranges
4. **Error Checking**: Always implement proper error handling
5. **Date Range Optimization**: Use reasonable date ranges to avoid overloading the system
6. **Caching**: Consider caching results when making multiple calls for the same time period
7. **Performance Consideration**: Be mindful of history request frequency in high-performance systems
8. **Time Zone Awareness**: Be aware of potential time zone differences when working with dates
9. **Incremental Queries**: For very large date ranges, consider using smaller incremental queries
10. **Preliminary Check**: Use this function as a preliminary check before requesting detailed data

## Implementation Notes

When working with the `history_deals_total()` function, consider these implementation details:

1. **Date Range Inclusivity**: Both the start and end dates are inclusive in the count
2. **Time Precision**: Time values include hours, minutes, and seconds, not just dates
3. **History Depth**: The available history depth depends on the broker and server configuration
4. **Deal Definition**: In MetaTrader 5, a deal represents an actual execution of an order
5. **Deal Types**: Different deal types include entries, exits, and balance operations
6. **DateTime Format**: Both `datetime` objects and Unix timestamps are accepted for date parameters
7. **Synchronization**: The history database may have a delay in updating with the most recent activity
8. **Memory Usage**: The function is optimized for low memory consumption
9. **Account Specificity**: The function only counts deals for the currently logged-in account
10. **Request Throttling**: Some servers may throttle excessive history requests

## Date Range Specification Examples

```python
from datetime import datetime, timedelta
import MetaTrader5 as mt5

# Establish connection to MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

# Current time
now = datetime.now()

# Example 1: All deals today
today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
today_deals = mt5.history_deals_total(today_start, now)
print(f"Deals today: {today_deals}")

# Example 2: Last 24 hours
yesterday_same_time = now - timedelta(days=1)
last_24h_deals = mt5.history_deals_total(yesterday_same_time, now)
print(f"Deals in the last 24 hours: {last_24h_deals}")

# Example 3: This week
week_start = (now - timedelta(days=now.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
this_week_deals = mt5.history_deals_total(week_start, now)
print(f"Deals this week: {this_week_deals}")

# Example 4: Previous month
first_day_this_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
last_day_prev_month = first_day_this_month - timedelta(days=1)
first_day_prev_month = last_day_prev_month.replace(day=1)
prev_month_deals = mt5.history_deals_total(first_day_prev_month, last_day_prev_month)
print(f"Deals in previous month: {prev_month_deals}")

# Example 5: Year to date
year_start = datetime(now.year, 1, 1)
ytd_deals = mt5.history_deals_total(year_start, now)
print(f"Deals year to date: {ytd_deals}")

# Example 6: Specific quarter
quarter_start = datetime(now.year, ((now.month-1)//3)*3+1, 1)
quarter_end = (quarter_start.replace(month=quarter_start.month+3, day=1) - timedelta(days=1))
quarter_deals = mt5.history_deals_total(quarter_start, quarter_end)
print(f"Deals in current quarter: {quarter_deals}")

# Shut down connection to the MetaTrader 5 terminal
mt5.shutdown()
```

## Difference Between Deals and Orders

It's important to understand the distinction between deals and orders in MetaTrader 5:

1. **Orders**: Represent trade requests (instructions) to perform trading operations
2. **Deals**: Represent actual executions (implementations) of trade operations

A single order can generate multiple deals, and the `history_deals_total()` function counts the actual executions, not just the instructions. This makes it particularly useful for measuring actual trading activity and execution performance.
