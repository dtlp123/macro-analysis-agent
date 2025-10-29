 
"""
Test script to debug Yahoo Finance tickers and find working alternatives
"""

import yfinance as yf
import time
from datetime import datetime, timedelta

def test_ticker(symbol, description):
    """Test a single ticker"""
    print(f"\nTesting {symbol} ({description})...")
    print("-" * 50)
    
    methods_tried = []
    success = False
    
    # Method 1: Using download()
    try:
        print(f"Method 1: yf.download('{symbol}')... ", end="")
        data = yf.download(symbol, period="5d", interval="1d", progress=False, show_errors=False)
        
        if not data.empty and len(data) > 0:
            latest_price = data['Close'].iloc[-1]
            latest_date = data.index[-1]
            print(f"✅ SUCCESS!")
            print(f"  Latest price: {latest_price:.2f}")
            print(f"  Date: {latest_date}")
            methods_tried.append(("download", True, latest_price))
            success = True
        else:
            print("❌ No data returned")
            methods_tried.append(("download", False, None))
    except Exception as e:
        print(f"❌ Error: {str(e)[:100]}")
        methods_tried.append(("download", False, str(e)[:50]))
    
    time.sleep(1)  # Rate limit
    
    # Method 2: Using Ticker.history()
    try:
        print(f"Method 2: yf.Ticker('{symbol}').history()... ", end="")
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="5d")
        
        if not hist.empty and len(hist) > 0:
            latest_price = hist['Close'].iloc[-1]
            latest_date = hist.index[-1]
            print(f"✅ SUCCESS!")
            print(f"  Latest price: {latest_price:.2f}")
            print(f"  Date: {latest_date}")
            methods_tried.append(("history", True, latest_price))
            success = True
        else:
            print("❌ No data returned")
            methods_tried.append(("history", False, None))
    except Exception as e:
        print(f"❌ Error: {str(e)[:100]}")
        methods_tried.append(("history", False, str(e)[:50]))
    
    time.sleep(1)  # Rate limit
    
    # Method 3: Using Ticker.info
    try:
        print(f"Method 3: yf.Ticker('{symbol}').info... ", end="")
        ticker = yf.Ticker(symbol)
        info = ticker.info
        
        if info and 'regularMarketPrice' in info:
            latest_price = info['regularMarketPrice']
            print(f"✅ SUCCESS!")
            print(f"  Latest price: {latest_price:.2f}")
            methods_tried.append(("info", True, latest_price))
            success = True
        else:
            print("❌ No price in info")
            methods_tried.append(("info", False, None))
    except Exception as e:
        print(f"❌ Error: {str(e)[:100]}")
        methods_tried.append(("info", False, str(e)[:50]))
    
    return success, methods_tried


def main():
    print("="*60)
    print("YAHOO FINANCE TICKER TESTING")
    print(f"Time: {datetime.now()}")
    print("="*60)
    
    # Gold tickers to test
    gold_tickers = [
        ("GC=F", "Gold Futures"),
       # ("GLD", "SPDR Gold ETF"),
       # ("IAU", "iShares Gold Trust"),
       # ("GLDM", "SPDR Gold MiniShares"),
       # ("GOLD", "Barrick Gold Corp"),
       # ("NEM", "Newmont Mining"),
    ]
    
    # DXY/Dollar tickers to test
    dxy_tickers = [
        ("DX-Y.NYB", "US Dollar Index (Full)"),
        #("DX=F", "Dollar Index Futures"),
        #("DXY", "Dollar Index Simple"),
        #("UUP", "USD Bullish ETF"),
        #("USDU", "USD ETF"),
        #("DLR", "Dollar ETF"),
    ]
    
    print("\n" + "="*60)
    print("TESTING GOLD TICKERS")
    print("="*60)
    
    working_gold = []
    for symbol, desc in gold_tickers:
        success, methods = test_ticker(symbol, desc)
        if success:
            working_gold.append((symbol, desc))
        time.sleep(1)
    
    print("\n" + "="*60)
    print("TESTING DOLLAR/DXY TICKERS")
    print("="*60)
    
    working_dxy = []
    for symbol, desc in dxy_tickers:
        success, methods = test_ticker(symbol, desc)
        if success:
            working_dxy.append((symbol, desc))
        time.sleep(1)
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY OF WORKING TICKERS")
    print("="*60)
    
    print("\n✅ WORKING GOLD TICKERS:")
    if working_gold:
        for symbol, desc in working_gold:
            print(f"  - {symbol}: {desc}")
    else:
        print("  ❌ None found! Will use default values.")
    
    print("\n✅ WORKING DXY TICKERS:")
    if working_dxy:
        for symbol, desc in working_dxy:
            print(f"  - {symbol}: {desc}")
    else:
        print("  ❌ None found! Will use default values.")
    
    # Recommendations
    print("\n" + "="*60)
    print("RECOMMENDED CONFIGURATION")
    print("="*60)
    
    if working_gold:
        print(f"\nGold: Use '{working_gold[0][0]}' as primary ticker")
    else:
        print("\nGold: Use default value (2650.0) - no tickers working")
    
    if working_dxy:
        print(f"DXY: Use '{working_dxy[0][0]}' as primary ticker")
    else:
        print("DXY: Use default value (106.5) - no tickers working")
    
    print("\n💡 TIP: If no tickers work, you might be rate limited or need a VPN.")
    print("The system will use default values as fallback.")


if __name__ == "__main__":
    main()