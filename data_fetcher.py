"""
Data Fetcher Module
Handles FRED API and Yahoo Finance data retrieval with enhanced GitHub Actions support
"""

import asyncio
import aiohttp
import logging
from datetime import datetime, timedelta
from typing import Dict, Optional
import pandas as pd
import time

logger = logging.getLogger(__name__)

# Import config for rate limits and defaults
try:
    import config
    YAHOO_DELAY = config.YAHOO_RATE_LIMIT_DELAY
    DEFAULT_VALUES = config.DEFAULT_VALUES
    MAX_RETRIES = config.MAX_RETRIES
    RETRY_DELAY = config.RETRY_DELAY
except ImportError:
    YAHOO_DELAY = 2.0  # Increased delay for GitHub Actions
    MAX_RETRIES = 5
    RETRY_DELAY = 3
    DEFAULT_VALUES = {
        'fed_rate': 5.25,
        'treasury_10y': 4.3,
        'cpi': 3.0,
        'dxy_level': 103.5
    }


class DataFetcher:
    """
    Fetches only the 4 essential data points needed for gold signal generation:
    1. Fed Funds Rate (FRED)
    2. 10Y Treasury Yield (FRED)
    3. Latest CPI (FRED)
    4. DXY Level (Yahoo Finance)
    
    Enhanced with better error handling for GitHub Actions environment.
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
        """Fetch all 4 essential data points with error tracking"""
        try:
            await self.initialize()
            
            # Track warnings and errors
            warnings = []
            errors = []
            
            # Fetch FRED data with individual error tracking
            fed_rate, fed_warning = await self.get_fed_funds_rate_with_status()
            if fed_warning:
                warnings.append(fed_warning)
            
            treasury_10y, treasury_warning = await self.get_10y_treasury_with_status()
            if treasury_warning:
                warnings.append(treasury_warning)
            
            cpi, cpi_warning = await self.get_latest_cpi_with_status()
            if cpi_warning:
                warnings.append(cpi_warning)
            
            # Fetch market data with error tracking and retries
            dxy_level, dxy_warning = await self.get_dxy_level_with_status_async()
            if dxy_warning:
                warnings.append(dxy_warning)
            
            data = {
                'fed_rate': fed_rate,
                'treasury_10y': treasury_10y,
                'cpi': cpi,
                'dxy_level': dxy_level,
                'timestamp': datetime.now().isoformat(),
                'warnings': warnings,
                'has_warnings': len(warnings) > 0
            }
            
            if warnings:
                logger.warning(f"Data fetched with {len(warnings)} warning(s)")
                for warning in warnings:
                    logger.warning(f"  - {warning}")
            else:
                logger.info(f"All data fetched successfully: Fed={fed_rate}%, "
                           f"10Y={treasury_10y}%, CPI={cpi}%, DXY={dxy_level}")
            
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
    
    async def get_fed_funds_rate_with_status(self) -> tuple[float, Optional[str]]:
        """Get Federal Funds Rate with error status"""
        rate = await self._fetch_fred_series(self.fred_series['fed_funds'])
        if rate is not None:
            return rate, None
        else:
            warning = f"Fed Funds Rate unavailable (FRED API), using fallback: {DEFAULT_VALUES['fed_rate']}%"
            return DEFAULT_VALUES['fed_rate'], warning
    
    async def get_10y_treasury(self) -> float:
        """Get 10-Year Treasury Yield from FRED"""
        yield_10y = await self._fetch_fred_series(self.fred_series['treasury_10y'])
        return yield_10y if yield_10y is not None else DEFAULT_VALUES['treasury_10y']
    
    async def get_10y_treasury_with_status(self) -> tuple[float, Optional[str]]:
        """Get 10-Year Treasury with error status"""
        yield_10y = await self._fetch_fred_series(self.fred_series['treasury_10y'])
        if yield_10y is not None:
            return yield_10y, None
        else:
            warning = f"10Y Treasury unavailable (FRED API), using fallback: {DEFAULT_VALUES['treasury_10y']}%"
            return DEFAULT_VALUES['treasury_10y'], warning
    
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
    
    async def get_latest_cpi_with_status(self) -> tuple[float, Optional[str]]:
        """Get latest CPI with error status"""
        try:
            params = {
                'series_id': self.fred_series['cpi'],
                'api_key': self.fred_api_key,
                'file_type': 'json',
                'limit': 13,
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
                        return round(cpi_yoy, 1), None
            
            warning = f"CPI data unavailable (FRED API), using fallback: {DEFAULT_VALUES['cpi']}%"
            return DEFAULT_VALUES['cpi'], warning
            
        except Exception as e:
            logger.error(f"Error calculating CPI YoY: {e}")
            warning = f"CPI calculation failed ({str(e)}), using fallback: {DEFAULT_VALUES['cpi']}%"
            return DEFAULT_VALUES['cpi'], warning
    
    async def get_dxy_level_with_status_async(self) -> tuple[float, Optional[str]]:
        """
        Get DXY level asynchronously with enhanced retry logic for GitHub Actions.
        Uses aiohttp instead of yfinance for better timeout control.
        """
        dxy_sources = [
            {
                'name': 'Yahoo Finance API',
                'url': 'https://query1.finance.yahoo.com/v8/finance/chart/DX-Y.NYB',
                'params': {'interval': '1d', 'range': '5d'},
                'parser': self._parse_yahoo_api_response
            },
            {
                'name': 'Yahoo Finance API (DXY)',
                'url': 'https://query1.finance.yahoo.com/v8/finance/chart/DXY',
                'params': {'interval': '1d', 'range': '5d'},
                'parser': self._parse_yahoo_api_response
            }
        ]
        
        for attempt in range(MAX_RETRIES):
            for source in dxy_sources:
                try:
                    logger.info(f"Attempt {attempt + 1}/{MAX_RETRIES}: Trying {source['name']}")
                    
                    # Add delay between attempts
                    if attempt > 0:
                        await asyncio.sleep(RETRY_DELAY * attempt)
                    
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                        'Accept': 'application/json',
                        'Accept-Language': 'en-US,en;q=0.9'
                    }
                    
                    timeout = aiohttp.ClientTimeout(total=30, connect=10)
                    
                    async with aiohttp.ClientSession(timeout=timeout) as session:
                        async with session.get(
                            source['url'],
                            params=source['params'],
                            headers=headers
                        ) as response:
                            if response.status == 200:
                                data = await response.json()
                                level = source['parser'](data)
                                
                                if level is not None:
                                    logger.info(f"DXY level from {source['name']}: {level:.2f}")
                                    return round(level, 2), None
                            else:
                                logger.warning(f"{source['name']} returned status {response.status}")
                
                except asyncio.TimeoutError:
                    logger.warning(f"{source['name']} timed out (attempt {attempt + 1})")
                except Exception as e:
                    logger.warning(f"{source['name']} failed: {str(e)[:100]}")
                
                # Small delay between different sources
                await asyncio.sleep(1)
        
        # All attempts failed, use fallback
        warning = f"DXY level unavailable (all sources failed after {MAX_RETRIES} attempts), using fallback: {DEFAULT_VALUES['dxy_level']}"
        logger.error(warning)
        return DEFAULT_VALUES['dxy_level'], warning
    
    def _parse_yahoo_api_response(self, data: dict) -> Optional[float]:
        """Parse Yahoo Finance API response to extract DXY level"""
        try:
            chart = data.get('chart', {})
            result = chart.get('result', [])
            
            if result and len(result) > 0:
                indicators = result[0].get('indicators', {})
                quote = indicators.get('quote', [])
                
                if quote and len(quote) > 0:
                    close_prices = quote[0].get('close', [])
                    
                    # Get the most recent non-null close price
                    for price in reversed(close_prices):
                        if price is not None:
                            return float(price)
            
            return None
            
        except Exception as e:
            logger.error(f"Error parsing Yahoo API response: {e}")
            return None
    
    # Keep synchronous version for backwards compatibility
    def get_dxy_level_with_status(self) -> tuple[float, Optional[str]]:
        """Synchronous wrapper for async DXY fetching"""
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # If called from async context, create new loop
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(
                        asyncio.run,
                        self.get_dxy_level_with_status_async()
                    )
                    return future.result(timeout=60)
            else:
                return asyncio.run(self.get_dxy_level_with_status_async())
        except Exception as e:
            logger.error(f"Error in synchronous DXY wrapper: {e}")
            warning = f"DXY fetch failed: {str(e)}, using fallback: {DEFAULT_VALUES['dxy_level']}"
            return DEFAULT_VALUES['dxy_level'], warning


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
    def get_dxy_level() -> float:
        fetcher = DataFetcher("")
        level, _ = fetcher.get_dxy_level_with_status()
        return level