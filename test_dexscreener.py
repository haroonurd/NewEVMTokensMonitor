"""
Tests for DexScreener client
"""

import pytest
import asyncio
from src.dexscreener_client import DexScreenerClient

@pytest.mark.asyncio
async def test_client_initialization():
    """Test client initialization"""
    client = DexScreenerClient("test_key")
    assert client.api_key == "test_key"
    assert client.base_url == "https://api.dexscreener.com/latest/dex"

@pytest.mark.asyncio
async def test_make_request_invalid_endpoint():
    """Test request to invalid endpoint"""
    client = DexScreenerClient("test_key")
    async with client:
        result = await client._make_request("invalid_endpoint")
        assert result is None

def test_format_number():
    """Test number formatting utility"""
    from src.utils import format_number
    
    assert format_number(1500000) == "1.50M"
    assert format_number(2500) == "2.50K"
    assert format_number(500) == "500.00"

def test_safe_float_conversion():
    """Test safe float conversion"""
    from src.utils import safe_float_conversion
    
    assert safe_float_conversion("123.45") == 123.45
    assert safe_float_conversion(None) == 0.0
    assert safe_float_conversion("invalid") == 0.0
