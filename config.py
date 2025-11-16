"""
Configuration settings for Web3 Token Analytics Bot
""" 

import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
DEXSCREENER_API_KEY = os.getenv('DEXSCREENER_API_KEY', '')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '')

# Analytics Settings
TIME_WINDOW_HOURS = 24
MIN_VOLUME_THRESHOLD = 10000  # USD
MIN_HOLDERS_THRESHOLD = 100
PUMP_THRESHOLD = 0.15  # 15% price increase
DUMP_THRESHOLD = -0.10  # 10% price decrease

# Chain Support
SUPPORTED_CHAINS = [
    'ethereum',
    'bsc', 
    'polygon',
    'arbitrum',
    'optimism',
    'solana',
    'avalanche'
]

# Cache Settings
CACHE_DURATION = 300  # 5 minutes
MAX_RETRIES = 3
RETRY_DELAY = 1

# Logging
LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
