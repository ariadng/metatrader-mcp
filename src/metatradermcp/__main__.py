import asyncio
import argparse

def main():
    """
    Main entry point for the MetaTrader MCP server.
    
    Parses command line arguments and starts the server.
    """
    parser = argparse.ArgumentParser(
        description="MetaTrader 5 MCP Server - Trading platform integration for LLMs"
    )
    parser.add_argument("--mt5-path", type=str, help="Path to MetaTrader 5 terminal executable")
    parser.add_argument("--login", type=int, help="MetaTrader 5 account login")
    parser.add_argument("--password", type=str, help="MetaTrader 5 account password")
    parser.add_argument("--server", type=str, help="MetaTrader 5 trading server")
    
    args = parser.parse_args()
    
    print(args)

if __name__ == "__main__":
    main()
