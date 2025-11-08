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

# Yahoo Finance Settings (Enhanced for GitHub Actions)
YAHOO_RATE_LIMIT_DELAY = 2.0  # Increased for GitHub Actions reliability

# Data fetch retries (Increased for GitHub Actions environment)
MAX_RETRIES = 5  # Try 5 times before giving up
RETRY_DELAY = 3  # Wait 3 seconds between retries (increases with each attempt)

# Default fallback values
DEFAULT_VALUES = {
    'fed_rate': 5.25,      # Current approximate Fed rate
    'treasury_10y': 4.5,   # Current approximate 10Y yield
    'cpi': 3.0,            # Current approximate CPI
    'dxy_level': 106.0     # Current approximate DXY level
}

# Email settings
EMAIL_SUBJECT_PREFIX = "Gold Signal"
EMAIL_TIME_SYDNEY = "08:00"  # 8 AM Sydney time

# Network timeout settings (for GitHub Actions)
NETWORK_TIMEOUT_SECONDS = 30
NETWORK_CONNECT_TIMEOUT_SECONDS = 10