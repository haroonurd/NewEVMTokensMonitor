"""
DexScreener API Client for fetching token and pair data
"""

import aiohttp
import asyncio
import logging 
from typing import Dict, List, Optional
from config import *

logger = logging.getLogger(__name__)

class DexScreenerClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.dexscreener.com/latest/dex"
        self.session = None
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
            
    async def _make_request(self, endpoint: str, params: Dict = None) -> Optional[Dict]:
        """Make API request to DexScreener"""
        headers = {}
        if self.api_key:
            headers['Authorization'] = f'Bearer {self.api_key}'
            
        url = f"{self.base_url}/{endpoint}"
        
        for attempt in range(MAX_RETRIES):
            try:
                async with self.session.get(url, params=params, headers=headers) as response:
                    if response.status == 200:
                        return await response.json()
                    elif response.status == 429:
                        logger.warning("Rate limit hit, waiting...")
                        await asyncio.sleep(RETRY_DELAY * (attempt + 1))
                    else:
                        logger.error(f"API error {response.status}: {await response.text()}")
                        return None
            except Exception as e:
                logger.error(f"Request failed: {str(e)}")
                if attempt == MAX_RETRIES - 1:
                    return None
                await asyncio.sleep(RETRY_DELAY * (attempt + 1))
                
        return None
    
    async def get_recent_pairs(self, hours: int = 24) -> List[Dict]:
        """Get recently created trading pairs"""
        params = {
            'timeframe': f'{hours}h',
            'sort': 'createdAt',
            'order': 'desc'
        }
        
        data = await self._make_request('pairs', params)
        return data.get('pairs', []) if data else []
    
    async def search_pairs(self, query: str) -> List[Dict]:
        """Search for pairs by token address or symbol"""
        params = {'q': query}
        data = await self._make_request('search', params)
        return data.get('pairs', []) if data else []
    
    async def get_token_info(self, chain: str, address: str) -> Optional[Dict]:
        """Get detailed token information"""
        endpoint = f'tokens/{chain}/{address}'
        return await self._make_request(endpoint)
    
    async def get_trending_tokens(self) -> List[Dict]:
        """Get trending tokens across all chains"""
        data = await self._make_request('trending')
        return data.get('pairs', []) if data else []
