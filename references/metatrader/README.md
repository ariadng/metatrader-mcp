# MetaTrader 5 Python Documentation

MetaTrader package for Python is designed for convenient and fast obtaining of exchange data via interprocessor communication directly from the MetaTrader 5 terminal. The data received this way can be further used for statistical calculations and machine learning. This documentation is based on [the official website](https://www.mql5.com/en/docs/python_metatrader5).

## Table of Contents

- [Gettings Started](#getting-started)
- [Initialization and Connection](#initialization-and-connection)
- [Account Information](#account-information)
- [Symbol Information](#symbol-information)
- [Market Data](#market-data)
- [Trading Operations](#trading-operations)
- [History Data](#history-data)
- [Error Handling](#error-handling)
- [Terminal Information](#terminal-information)

## Getting Started

Install the package to your python project:

```bash
pip install MetaTrader5
```

## Initialization and Connection

- [`initialize`](functions/initialize.md): Establishes a connection to the MetaTrader 5 terminal.
- [`login`](functions/login.md): Authorizes access to a trading account.
- [`shutdown`](functions/shutdown.md): Closes the connection to the MetaTrader 5 terminal.

## Account Information

- [`account_info`](functions/account_info.md): Retrieves comprehensive information about the current trading account.

## Symbol Information

- [`symbols_total`](functions/symbols_total.md): Retrieves the total number of available trading symbols.
- [`symbols_get`](functions/symbols_get.md): Retrieves a list of trading symbols based on specified criteria.
- [`symbol_info`](functions/symbol_info.md): Retrieves detailed information about a specific trading symbol.
- [`symbol_info_tick`](functions/symbol_info_tick.md): Retrieves the last tick data for a specific trading symbol.
- [`symbol_select`](functions/symbol_select.md): Adds or removes a symbol from the Market Watch window.

## Market Data

- [`market_book_add`](functions/market_book_add.md): Subscribes to market depth updates for a specific symbol.
- [`market_book_get`](functions/market_book_get.md): Retrieves the current market depth for a specific symbol.
- [`market_book_release`](functions/market_book_release.md): Unsubscribes from market depth updates for a specific symbol.
- [`copy_rates_from`](functions/copy_rates_from.md): Copies historical price data (OHLCV) starting from a specific date.
- [`copy_rates_from_pos`](functions/copy_rates_from_pos.md): Copies historical price data (OHLCV) starting from a specific position.
- [`copy_rates_range`](functions/copy_rates_range.md): Copies historical price data (OHLCV) within a specified date range.
- [`copy_ticks_from`](functions/copy_ticks_from.md): Copies tick data starting from a specific date.
- [`copy_ticks_range`](functions/copy_ticks_range.md): Copies tick data within a specified date range.

## Trading Operations

- [`order_check`](functions/order_check.md): Checks if a trading request is valid before sending it to the server.
- [`order_send`](functions/order_send.md): Sends a trading request to the server for execution.
- [`order_calc_profit`](functions/order_calc_profit.md): Calculates the expected profit for a trading operation.
- [`order_calc_margin`](functions/order_calc_margin.md): Calculates the margin required for a trading operation.
- [`orders_total`](functions/orders_total.md): Retrieves the total number of active (pending) orders.
- [`orders_get`](functions/orders_get.md): Retrieves a list of active (pending) orders based on specified criteria.
- [`positions_total`](functions/positions_total.md): Retrieves the total number of open positions.
- [`positions_get`](functions/positions_get.md): Retrieves a list of open positions based on specified criteria.

## History Data

- [`history_orders_total`](functions/history_orders_total.md): Retrieves the total number of orders in the trading history.
- [`history_orders_get`](functions/history_orders_get.md): Retrieves a list of orders from the trading history based on specified criteria.
- [`history_deals_total`](functions/history_deals_total.md): Retrieves the total number of deals in the trading history.
- [`history_deals_get`](functions/history_deals_get.md): Retrieves a list of deals from the trading history based on specified criteria.

## Error Handling

- [`last_error`](functions/last_error.md): Retrieves the last error code and description.

## Terminal Information

- [`terminal_info`](functions/terminal_info.md): Retrieves information about the MetaTrader 5 terminal.
- [`version`](functions/version.md): Retrieves the version information of the MetaTrader 5 terminal.
