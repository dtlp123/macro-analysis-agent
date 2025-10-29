"""
Configuration settings for Simple Macro Agent
"""

# Claude AI Model Configuration
# Update this if the model name changes
CLAUDE_MODEL = "claude-sonnet-4-5-20250929"  # Current working model

# Alternative models (in case of issues)
CLAUDE_MODEL_ALTERNATIVES = [
   "claude-opus-4-1-20250805",
   "claude-opus-4-20250514",
   "claude-sonnet-4-20250514",
   "claude-3-7-sonnet-20250219",
   "claude-3-5-haiku-20241022",
   "claude-3-haiku-20240307"
]

# Yahoo Finance Settings
YAHOO_RATE_LIMIT_DELAY = 1.5  # Seconds between Yahoo requests to avoid 429 errors

# Data fetch retries
MAX_RETRIES = 3
RETRY_DELAY = 2  # Seconds between retries

# Default fallback values
DEFAULT_VALUES = {
    'fed_rate': 0,    # Current approximate Fed rate
    'treasury_10y': 0,  # Current approximate 10Y yield
    'cpi': 0,          # Current approximate CPI
    'gold_price': 0, # Current approximate gold price
    'dxy_level': 0   # Current approximate DXY level
}

# Email settings
EMAIL_SUBJECT_PREFIX = "Gold Signal"
EMAIL_TIME_SYDNEY = "08:00"  # 8 AM Sydney time

# Trading parameters
DEFAULT_STOP_LOSS_PERCENT = 1.0  # 1% stop loss
DEFAULT_RISK_REWARD_RATIO = 2.0  # 2:1 risk-reward