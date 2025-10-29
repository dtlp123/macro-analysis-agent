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
    from simple_macro_agent import SimpleMacroAgent
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
        
        # Run the analysis
        logger.info("📡 Running complete macro analysis...")
        success = await agent.run_daily_analysis()
        
        if success:
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            logger.info("🎉 ANALYSIS COMPLETED SUCCESSFULLY!")
            logger.info(f"⏱️  Total Duration: {duration:.1f} seconds")
            logger.info("=" * 60)
            return True
        else:
            raise Exception("Analysis returned failure status")
            
    except Exception as e:
        logger.error(f"💥 Production run failed: {e}")
        logger.error(traceback.format_exc())
        return False


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
            
    except Exception as e:
        logger.error(f"💥 Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()