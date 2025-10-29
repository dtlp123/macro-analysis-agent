# """
#Test script to run the macro agent once for validation
#"""

import asyncio
import logging
from datetime import datetime
from main import SimpleMacroAgent

# Setup logging for test run
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

async def test_run():
    """Run the agent once for testing"""
    print("\n" + "="*60)
    print("SIMPLE MACRO AGENT - TEST RUN")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60 + "\n")
    
    try:
        # Initialize agent
        agent = SimpleMacroAgent()
        
        # Run once
        analysis = await agent.run_daily()
        
        # Print results
        print("\n" + "="*60)
        print("TEST RUN RESULTS")
        print("="*60)
        print(f"Signal: {analysis['signal']}")
        print(f"Bias: {analysis['bias']}")
        print(f"Confidence: {analysis['confidence']}")
        print(f"\nReasoning:\n{analysis['reasoning']}")
        
        if analysis['signal'] != 'WAIT':
            trade = analysis['trade_params']
            print(f"\nTrade Parameters:")
            print(f"  Entry: ${trade['entry']}")
            print(f"  Stop: ${trade['stop']}")
            print(f"  Target: ${trade['target']}")
            print(f"  Risk: ${trade['risk_amount']:.0f}")
        
        print("\n✅ Test run completed successfully!")
        print("Check your email for the signal report.\n")
        
    except Exception as e:
        print(f"\n❌ Test run failed: {e}")
        print("Please check your .env configuration.\n")
        raise

if __name__ == "__main__":
    asyncio.run(test_run())
