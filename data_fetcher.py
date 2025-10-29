"""
Data Fetcher Module
Handles FRED API and Yahoo Finance data retrieval
"""

import asyncio
import aiohttp
import logging
from datetime import datetime, timedelta
from typing import Dict, Optional
import yfinance as yf
import pandas as pd
import time

logger = logging.getLogger(__name__)

# Import config for rate limits and defaults
try:
    import config
    YAHOO_DELAY = config.YAHOO_RATE_LIMIT_DELAY
    DEFAULT_VALUES = config.DEFAULT_VALUES
except ImportError:
    YAHOO_DELAY = 1.5
    DEFAULT_VALUES = {
        'fed_rate': 5.25,
        'treasury_10y': 4.3,
        'cpi': 3.0,
        'gold_price': 2050.0,
        'dxy_level': 103.5
    }


class DataFetcher:
    """
    Fetches only the 5 essential data points needed for gold signal generation:
    1. Fed Funds Rate (FRED)
    2. 10Y Treasury Yield (FRED)
    3. Latest CPI (FRED)
    4. Gold Price (Yahoo Finance)
    5. DXY Level (Yahoo Finance)
    """
    
    def __init__(self, fred_api_key: str):
        self.fred_api_key = fred_api_key
        self.fred_base_url = "https://api.stlouisfed.org/fred"
        self.session: Optional[aiohttp.ClientSession] = None
        
        # FRED series IDs
        self.fred_series = {
            'fed_funds': 'DFF',        # Federal Funds Rate
            'treasury_10y': 'GS10',     # 10-Year Treasury
            'cpi': 'CPIAUCSL'          # CPI All Urban Consumers
        }
        
        logger.info("DataFetcher initialized")
    
    async def initialize(self):
        """Initialize HTTP session"""
        if not self.session:
            self.session = aiohttp.ClientSession()
    
    async def cleanup(self):
        """Cleanup HTTP session"""
        if self.session:
            await self.session.close()
    
    async def get_all_data(self) -> Dict:
        """Fetch all 5 essential data points"""
        try:
            await self.initialize()
            
            # Fetch FRED data
            fed_rate = await self.get_fed_funds_rate()
            treasury_10y = await self.get_10y_treasury()
            cpi = await self.get_latest_cpi()
            
            # Fetch market data
            gold_price = self.get_gold_price()
            dxy_level = self.get_dxy_level()
            
            data = {
                'fed_rate': fed_rate,
                'treasury_10y': treasury_10y,
                'cpi': cpi,
                'gold_price': gold_price,
                'dxy_level': dxy_level,
                'timestamp': datetime.now().isoformat()
            }
            
            logger.info(f"All data fetched successfully: Fed={fed_rate}%, "
                       f"10Y={treasury_10y}%, CPI={cpi}%, "
                       f"Gold=${gold_price}, DXY={dxy_level}")
            
            return data
            
        except Exception as e:
            logger.error(f"Error fetching data: {e}")
            raise
        finally:
            await self.cleanup()
    
    async def _fetch_fred_series(self, series_id: str) -> Optional[float]:
        """Generic FRED series fetcher"""
        try:
            params = {
                'series_id': series_id,
                'api_key': self.fred_api_key,
                'file_type': 'json',
                'limit': 1,
                'sort_order': 'desc'
            }
            
            url = f"{self.fred_base_url}/series/observations"
            
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get('observations'):
                        value = float(data['observations'][0]['value'])
                        logger.debug(f"FRED {series_id}: {value}")
                        return value
                else:
                    logger.error(f"FRED API error for {series_id}: {response.status}")
                    return None
                    
        except Exception as e:
            logger.error(f"Error fetching FRED series {series_id}: {e}")
            return None
    
    async def get_fed_funds_rate(self) -> float:
        """Get Federal Funds Rate from FRED"""
        rate = await self._fetch_fred_series(self.fred_series['fed_funds'])
        return rate if rate is not None else DEFAULT_VALUES['fed_rate']
    
    async def get_10y_treasury(self) -> float:
        """Get 10-Year Treasury Yield from FRED"""
        yield_10y = await self._fetch_fred_series(self.fred_series['treasury_10y'])
        return yield_10y if yield_10y is not None else DEFAULT_VALUES['treasury_10y']
    
    async def get_latest_cpi(self) -> float:
        """Get latest CPI YoY from FRED"""
        try:
            # Get CPI data for YoY calculation
            params = {
                'series_id': self.fred_series['cpi'],
                'api_key': self.fred_api_key,
                'file_type': 'json',
                'limit': 13,  # Need 13 months for YoY
                'sort_order': 'desc'
            }
            
            url = f"{self.fred_base_url}/series/observations"
            
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    observations = data.get('observations', [])
                    
                    if len(observations) >= 13:
                        latest = float(observations[0]['value'])
                        year_ago = float(observations[12]['value'])
                        cpi_yoy = ((latest / year_ago) - 1) * 100
                        logger.debug(f"CPI YoY: {cpi_yoy:.1f}%")
                        return round(cpi_yoy, 1)
                    
            return DEFAULT_VALUES['cpi']
            
        except Exception as e:
            logger.error(f"Error calculating CPI YoY: {e}")
            return DEFAULT_VALUES['cpi']
    
    def get_gold_price(self) -> float:
        """Get current gold price from Yahoo Finance with multiple ticker attempts"""
        # Try multiple gold tickers in order of preference
        gold_tickers = [
            "GLD",      # SPDR Gold ETF (most liquid, always available)
            "GC=F",     # Gold futures (might have issues)
        ]
        
        for ticker in gold_tickers:
            try:
                time.sleep(YAHOO_DELAY)  # Add delay to avoid rate limits
                
                logger.debug(f"Trying gold ticker: {ticker}")
                data = yf.download(ticker, period="5d", interval="1d", progress=False)
                
                if not data.empty and len(data) > 0:
                    price = float(data['Close'].iloc[-1])
                    
                    # Adjust for GLD (ETF is ~1/10th of gold price)
                    if ticker == "GLD":
                        price = price * 10  # Approximate conversion
                    # Adjust for GOLD (Barrick stock, use multiplier)
                    elif ticker == "GOLD":
                        price = price * 100  # Very rough approximation
                    
                    logger.info(f"Gold price from {ticker}: ${price:.2f}")
                    return round(price, 2)
                    
            except Exception as e:
                logger.warning(f"Failed to fetch {ticker}: {e}")
                continue
        
        # If all fail, use fallback
        logger.warning("All gold tickers failed, using fallback value")
        return DEFAULT_VALUES['gold_price']
    
    def get_dxy_level(self) -> float:
        """Get current DXY level from Yahoo Finance with multiple ticker attempts"""
        # Try multiple USD index tickers
        dxy_tickers = [
            "DXY",       # Try simple DXY first
            "DX-Y.NYB",  # Full ticker
            "UUP",       # USD ETF as proxy
            "USDU",      # Another USD ETF
        ]
        
        for ticker in dxy_tickers:
            try:
                time.sleep(YAHOO_DELAY)  # Add delay to avoid rate limits
                
                logger.debug(f"Trying DXY ticker: {ticker}")
                data = yf.download(ticker, period="5d", interval="1d", progress=False)
                
                if not data.empty and len(data) > 0:
                    level = float(data['Close'].iloc[-1])
                    
                    # Adjust for ETFs (they track DXY but at different scales)
                    if ticker == "UUP":
                        level = level * 3.7  # UUP to DXY approximate conversion
                    elif ticker == "USDU":
                        level = level * 3.9  # USDU to DXY approximate conversion
                    
                    logger.info(f"DXY level from {ticker}: {level:.2f}")
                    return round(level, 2)
                    
            except Exception as e:
                logger.warning(f"Failed to fetch {ticker}: {e}")
                continue
        
        # If all fail, use fallback
        logger.warning("All DXY tickers failed, using fallback value")
        return DEFAULT_VALUES['dxy_level']


class FREDConnector:
    """Simplified FRED connector for backwards compatibility"""
    
    def __init__(self, api_key: str):
        self.fetcher = DataFetcher(api_key)
    
    async def get_fed_funds_rate(self) -> float:
        await self.fetcher.initialize()
        result = await self.fetcher.get_fed_funds_rate()
        await self.fetcher.cleanup()
        return result
    
    async def get_10y_treasury(self) -> float:
        await self.fetcher.initialize()
        result = await self.fetcher.get_10y_treasury()
        await self.fetcher.cleanup()
        return result
    
    async def get_latest_cpi(self) -> float:
        await self.fetcher.initialize()
        result = await self.fetcher.get_latest_cpi()
        await self.fetcher.cleanup()
        return result


class YahooConnector:
    """Simplified Yahoo Finance connector for backwards compatibility"""
    
    @staticmethod
    def get_gold_price() -> float:
        fetcher = DataFetcher("")
        return fetcher.get_gold_price()
    
    @staticmethod
    def get_dxy_level() -> float:
        fetcher = DataFetcher("")
        return fetcher.get_dxy_level()