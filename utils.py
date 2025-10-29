"""
Utility functions for Web3 Analytics Bot
"""

import json
import time
import hashlib
from typing import Any, Dict
from datetime import datetime

def format_number(value: float, decimals: int = 2) -> str:
    """Format number with appropriate suffixes"""
    if value >= 1e9:
        return f"{value/1e9:.{decimals}f}B"
    elif value >= 1e6:
        return f"{value/1e6:.{decimals}f}M"
    elif value >= 1e3:
        return f"{value/1e3:.{decimals}f}K"
    else:
        return f"{value:.{decimals}f}"

def calculate_percentage_change(old_value: float, new_value: float) -> float:
    """Calculate percentage change between two values"""
    if old_value == 0:
        return 0
    return ((new_value - old_value) / old_value) * 100

def generate_token_hash(token_address: str, chain_id: str) -> str:
    """Generate unique hash for token identification"""
    return hashlib.md5(f"{chain_id}_{token_address}".encode()).hexdigest()

def safe_float_conversion(value: Any, default: float = 0.0) -> float:
    """Safely convert value to float"""
    try:
        return float(value) if value is not None else default
    except (ValueError, TypeError):
        return default

def timestamp_to_datetime(timestamp: str) -> datetime:
    """Convert various timestamp formats to datetime"""
    try:
        # Handle ISO format with Z
        if timestamp.endswith('Z'):
            timestamp = timestamp[:-1] + '+00:00'
        return datetime.fromisoformat(timestamp)
    except:
        return datetime.now()

class Cache:
    """Simple in-memory cache implementation"""
    def __init__(self, ttl: int = 300):
        self.ttl = ttl
        self._cache = {}
        
    def get(self, key: str) -> Any:
        """Get value from cache"""
        if key in self._cache:
            data, timestamp = self._cache[key]
            if time.time() - timestamp < self.ttl:
                return data
            else:
                del self._cache[key]
        return None
        
    def set(self, key: str, value: Any):
        """Set value in cache"""
        self._cache[key] = (value, time.time())
        
    def clear(self):
        """Clear cache"""
        self._cache.clear()
