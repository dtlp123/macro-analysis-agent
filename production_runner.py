#!/usr/bin/env python3
"""
Production Runner for Macro Analysis Agent V2
GitHub Actions compatible - runs weekday analysis only
"""

import os
import sys
import logging
import traceback
import asyncio
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import your V2 modules
try:
    from main import SimpleMacroAgent
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure your V2 modules are in the root directory")
    sys.exit(1)

# Setup production logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('macro_analysis_v2.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


def is_weekday():
    """Check if today is a trading day (Monday-Friday)"""
    today = datetime.now().weekday()  # 0=Monday, 6=Sunday
    return today < 5  # Monday(0) through Friday(4)


def verify_environment():
    """Verify all required environment variables are set"""
    required_vars = [
        'FRED_API_KEY',
        'ANTHROPIC_API_KEY', 
        'EMAIL_FROM',
        'EMAIL_PASSWORD',
        'EMAIL_TO'
    ]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        logger.error(f"❌ Missing environment variables: {missing_vars}")
        return False
    
    logger.info("✅ All environment variables verified")
    return True


async def run_v2_analysis():
    """Run the complete V2 macro analysis"""
    start_time = datetime.now()
    
    logger.info("=" * 60)
    logger.info("📊 MACRO ANALYSIS AGENT V2 - PRODUCTION RUN")
    logger.info(f"⏰ Start Time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 60)
    
    try:
        # Check if it's a weekday
        if not is_weekday():
            logger.info("📅 Weekend detected - skipping analysis")
            return True
        
        logger.info("📅 Weekday confirmed - proceeding with analysis")
        
        # Initialize the V2 agent
        logger.info("🚀 Initializing Macro Agent V2...")
        agent = SimpleMacroAgent()
        
        # Run the daily analysis using the correct method from main.py
        logger.info("📡 Running complete macro analysis...")
        analysis = await agent.run_daily()  # This matches the method in main.py!
        
        if analysis:
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            logger.info("🎉 ANALYSIS COMPLETED SUCCESSFULLY!")
            logger.info(f"⏱️  Total Duration: {duration:.1f} seconds")
            logger.info(f"📊 Signal: {analysis.get('signal', 'N/A')}")
            logger.info(f"🎯 Confidence: {analysis.get('confidence', 'N/A')}")
            logger.info("📧 Email sent successfully")
            logger.info("=" * 60)
            return True
        else:
            raise Exception("Analysis returned None")
            
    except Exception as e:
        logger.error(f"💥 Production run failed: {e}")
        logger.error(traceback.format_exc())
        
        # Try to send error notification email
        try:
            await send_error_notification(e)
        except:
            logger.error("Failed to send error notification email")
        
        return False


async def send_error_notification(error):
    """Send error notification email using the same SMTP setup"""
    try:
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        
        email_from = os.getenv('EMAIL_FROM')
        email_to = os.getenv('EMAIL_TO')
        email_password = os.getenv('EMAIL_PASSWORD')
        smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        smtp_port = int(os.getenv('SMTP_PORT', '587'))
        
        msg = MIMEMultipart()
        msg['From'] = email_from
        msg['To'] = email_to
        msg['Subject'] = f"🚨 Macro Agent ERROR - {datetime.now().strftime('%Y-%m-%d')}"
        
        body = f"""
MACRO ANALYSIS AGENT ERROR

Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Error: {str(error)}

The automated macro analysis failed to complete.
Please check the GitHub Actions logs for more details.

Traceback:
{traceback.format_exc()}

---
This is an automated error notification from your Macro Analysis Agent V2
"""
        
        msg.attach(MIMEText(body, 'plain'))
        
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(email_from, email_password)
            server.send_message(msg)
        
        logger.info("✅ Error notification email sent")
        
    except Exception as e:
        logger.error(f"Failed to send error notification: {e}")


def main():
    """Main entry point for GitHub Actions"""
    logger.info("🚀 Starting Macro Agent V2 Production Runner...")
    
    # Verify environment
    if not verify_environment():
        sys.exit(1)
    
    # Run analysis
    try:
        success = asyncio.run(run_v2_analysis())
        
        if success:
            logger.info("✅ Production run completed successfully!")
            sys.exit(0)
        else:
            logger.error("❌ Production run failed!")
            sys.exit(1)
            
    except KeyboardInterrupt:
        logger.info("⏹️  Production run interrupted")
        sys.exit(1)
    except Exception as e:
        logger.error(f"💥 Unexpected error: {e}")
        logger.error(traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    main()