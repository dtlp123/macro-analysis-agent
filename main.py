"""
Simple Macro Analysis Agent for Gold Trading
Focused on Fed Policy + DXY correlation signals
"""

import os
import json
import logging
import asyncio
from datetime import datetime, time
from typing import Dict, Optional, Tuple
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import anthropic
from dotenv import load_dotenv

from data_fetcher import DataFetcher
from signal_generator import SignalGenerator
import config

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('macro_agent.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class SimpleMacroAgent:
    """
    Minimal macro analysis agent for gold trading signals.
    Daily analysis of Fed policy + DXY to generate LONG/SHORT/WAIT signals.
    """
    
    def __init__(self):
        """Initialize the agent with minimal required components"""
        # API Keys
        self.fred_api_key = os.getenv('FRED_API_KEY')
        self.anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
        
        # Email Configuration
        self.email_from = os.getenv('EMAIL_FROM')
        self.email_to = os.getenv('EMAIL_TO')
        self.email_password = os.getenv('EMAIL_PASSWORD')
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        
        # Validate configuration
        self._validate_config()
        
        # Initialize components
        self.data_fetcher = DataFetcher(self.fred_api_key)
        self.signal_generator = SignalGenerator(anthropic_api_key=self.anthropic_api_key)
        self.ai_client = anthropic.Anthropic(api_key=self.anthropic_api_key)
        
        logger.info("Simple Macro Agent initialized successfully")
    
    def _validate_config(self):
        """Validate required configuration is present"""
        required_vars = [
            'FRED_API_KEY', 'ANTHROPIC_API_KEY', 
            'EMAIL_FROM', 'EMAIL_TO', 'EMAIL_PASSWORD'
        ]
        
        missing = [var for var in required_vars if not os.getenv(var)]
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")
    
    async def get_macro_data(self) -> Dict:
        """
        Fetch the 5 essential data points:
        1. Fed Funds Rate
        2. 10Y Treasury Yield  
        3. Latest CPI
        4. Gold Price
        5. DXY Level
        """
        try:
            logger.info("Fetching macro data...")
            
            # Fetch all data points
            data = await self.data_fetcher.get_all_data()
            
            # Log summary
            logger.info(f"Data fetched - Fed Rate: {data.get('fed_rate')}%, "
                       f"DXY: {data.get('dxy_level')}, "
                       f"Gold: ${data.get('gold_price')}")
            
            # Store to JSON for record keeping
            self._save_data_snapshot(data)
            
            return data
            
        except Exception as e:
            logger.error(f"Error fetching macro data: {e}")
            raise
    
    def _save_data_snapshot(self, data: Dict):
        """Save data snapshot to JSON file"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"data_snapshots/snapshot_{timestamp}.json"
            
            os.makedirs("data_snapshots", exist_ok=True)
            
            with open(filename, 'w') as f:
                json.dump({
                    'timestamp': datetime.now().isoformat(),
                    'data': data
                }, f, indent=2)
                
        except Exception as e:
            logger.warning(f"Failed to save data snapshot: {e}")
    
    async def generate_daily_analysis(self, data: Dict) -> Dict:
        """
        Generate trading signal using simple Fed + DXY logic.
        Single AI call for complete analysis.
        """
        try:
            logger.info("Generating daily analysis...")
            
            # Log the data we received for debugging
            logger.info(f"Data received: Fed={data.get('fed_rate')}, "
                       f"DXY={data.get('dxy_level')}, "
                       f"Gold=${data.get('gold_price')}, "
                       f"CPI={data.get('cpi')}, "
                       f"10Y={data.get('treasury_10y')}")
            
            # Generate signal using rule-based logic
            signal = self.signal_generator.generate_signal(data)
            logger.info(f"Signal generated: {signal['signal']} (confidence: {signal['confidence']})")
            
            # Get AI analysis for reasoning (1 API call)
            ai_analysis = await self._get_ai_analysis(data, signal)
            
            analysis = {
                'signal': signal['signal'],
                'bias': signal['bias'],
                'confidence': signal['confidence'],
                'reasoning': ai_analysis['reasoning'],
                'data': data,
                'timestamp': datetime.now().isoformat()
            }
            
            logger.info(f"Analysis complete - Signal: {signal['signal']}, "
                       f"Confidence: {signal['confidence']}")
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error generating analysis: {e}")
            raise
    
    async def _get_ai_analysis(self, data: Dict, signal: Dict) -> Dict:
        """
        Single AI call to provide reasoning for the signal.
        Focused on practical trading insights.
        """
        prompt = f"""
        You are a professional gold trader analyzing macro conditions.
        
        CURRENT MACRO DATA:
        - Fed Funds Rate: {data.get('fed_rate')}%
        - 10Y Treasury: {data.get('treasury_10y')}%
        - Latest CPI: {data.get('cpi')}%
        - Gold Price: ${data.get('gold_price')}
        - DXY Level: {data.get('dxy_level')}
        
        SIGNAL GENERATED: {signal['signal']}
        BIAS: {signal['bias']}
        
        Based on your proven trading approach:
        - Fed policy is the primary driver of gold over weeks/months
        - Strong dollar (DXY > 103.22) usually overrides other bullish factors
        - Simple directional bias is more reliable than complex analysis
        
        Provide a 2-3 sentence explanation of why this signal makes sense
        in the current macro environment. Focus on:
        1. What the Fed stance means for gold
        2. How DXY confirms or conflicts with Fed signal
        3. The key risk to watch for this trade
        
        Be concise and practical. No fluff.
        """
        
        try:
            message = self.ai_client.messages.create(
                model=config.CLAUDE_MODEL,  # Use model from config
                max_tokens=300,
                messages=[{"role": "user", "content": prompt}]
            )
            
            reasoning = message.content[0].text
            
            return {
                'reasoning': reasoning,
                'api_calls_used': 1
            }
            
        except Exception as e:
            logger.error(f"AI analysis failed: {e}")
            return {
                'reasoning': f"Fed at {data.get('fed_rate')}% with DXY at {data.get('dxy_level')} "
                            f"suggests {signal['bias'].lower()} bias for gold.",
                'api_calls_used': 0
            }
    
    def send_daily_email(self, analysis: Dict):
        """Send plain text email with analysis"""
        try:
            subject = f"Gold Signal - {datetime.now().strftime('%Y-%m-%d')} - {analysis['signal']}"
            
            # Build email body
            body = self._build_email_body(analysis)
            
            # Send email
            self._send_email(subject, body)
            
            logger.info(f"Daily email sent successfully to {self.email_to}")
            
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            raise
    
    def _build_email_body(self, analysis: Dict) -> str:
        """Build clean email body with just signal and analysis"""
        data = analysis['data']
        
        # Determine DXY strength
        dxy_level = data.get('dxy_level', 0)
        if dxy_level > 105:
            dxy_status = 'Strong'
        elif dxy_level < 100:
            dxy_status = 'Weak'
        else:
            dxy_status = 'Neutral'
        
        body = f"""
DAILY GOLD MACRO ANALYSIS
{datetime.now().strftime('%A, %B %d, %Y')}

SIGNAL: {analysis['signal']}
Confidence: {analysis['confidence']}

MACRO ENVIRONMENT
• Fed Funds Rate: {data.get('fed_rate')}%
• Fed Bias: {analysis['bias']}
• DXY Level: {dxy_level} ({dxy_status} vs gold)
• Gold Price: ${data.get('gold_price'):,.2f}
• 10Y Treasury: {data.get('treasury_10y')}%
• Latest CPI: {data.get('cpi')}%

ANALYSIS
{analysis['reasoning']}

---
Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        return body
    
    def _send_email(self, subject: str, body: str):
        """Send email via SMTP"""
        msg = MIMEMultipart()
        msg['From'] = self.email_from
        msg['To'] = self.email_to
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'plain'))
        
        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(self.email_from, self.email_password)
            server.send_message(msg)
    
    async def run_daily(self):
        """Execute daily analysis and send email"""
        try:
            logger.info("=" * 50)
            logger.info("Starting daily macro analysis run")
            
            # 1. Fetch data
            data = await self.get_macro_data()
            
            # 2. Generate analysis
            analysis = await self.generate_daily_analysis(data)
            
            # 3. Send email
            self.send_daily_email(analysis)
            
            logger.info("Daily run completed successfully")
            logger.info("=" * 50)
            
            return analysis
            
        except Exception as e:
            logger.error(f"Daily run failed: {e}")
            
            # Send error notification
            try:
                self._send_email(
                    "Gold Signal - ERROR",
                    f"The daily analysis failed with error:\n\n{str(e)}\n\nPlease check the system."
                )
            except:
                pass
            
            raise
    
    async def run_scheduler(self):
        """Run the agent on schedule (8 AM Sydney time daily)"""
        logger.info("Macro Agent scheduler started")
        logger.info("Will run daily at 8:00 AM Sydney time")
        
        while True:
            now = datetime.now()
            
            # Calculate next 8 AM Sydney time
            target_time = now.replace(hour=8, minute=0, second=0, microsecond=0)
            if now >= target_time:
                target_time = target_time.replace(day=target_time.day + 1)
            
            # Wait until target time
            wait_seconds = (target_time - now).total_seconds()
            logger.info(f"Next run in {wait_seconds/3600:.1f} hours")
            
            await asyncio.sleep(wait_seconds)
            
            # Run daily analysis
            try:
                await self.run_daily()
            except Exception as e:
                logger.error(f"Scheduled run failed: {e}")
            
            # Wait a minute to avoid double runs
            await asyncio.sleep(60)


async def main():
    """Main entry point"""
    agent = SimpleMacroAgent()
    
    # Run once immediately for testing
    # await agent.run_daily()
    
    # Then run on schedule
    await agent.run_scheduler()


if __name__ == "__main__":
    asyncio.run(main())