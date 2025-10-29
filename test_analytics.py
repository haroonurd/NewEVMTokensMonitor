"""
Tests for analytics engine
"""

import pytest
import pandas as pd
from src.analytics import TokenAnalytics

def test_analytics_initialization():
    """Test analytics class initialization"""
    analytics = TokenAnalytics()
    assert analytics.metrics_history == []

def test_comprehensive_analysis_empty():
    """Test analysis with empty data"""
    analytics = TokenAnalytics()
    result = analytics.comprehensive_analysis([])
    assert result == {}

def test_prepare_dataframe():
    """Test DataFrame preparation"""
    analytics = TokenAnalytics()
    sample_data = [{
        'pairAddress': '0x123',
        'baseToken': {'symbol': 'TEST', 'address': '0x456'},
        'quoteToken': {'symbol': 'ETH'},
        'chainId': 'ethereum',
        'dexId': 'uniswap',
        'priceUsd': '1.5',
        'volume': {'h24': '100000'},
        'priceChange': {'h24': '10.5'},
        'liquidity': {'usd': '500000'},
        'fdv': '1000000',
        'marketCap': '750000',
        'pairCreatedAt': '2023-01-01T00:00:00Z',
        'txns': {'h24': {'buys': 50, 'sells': 30}},
        'holders': 1000
    }]
    
    df = analytics._prepare_dataframe(sample_data)
    assert len(df) == 1
    assert df.iloc[0]['base_token_symbol'] == 'TEST'
    assert df.iloc[0]['volume_h24'] == 100000.0
