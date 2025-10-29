"""
Advanced analytics engine for token data
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
import logging
from datetime import datetime, timedelta
from config import *

logger = logging.getLogger(__name__)

class TokenAnalytics:
    def __init__(self):
        self.metrics_history = []
        
    def comprehensive_analysis(self, pairs: List[Dict], min_volume: float = 10000) -> Dict:
        """Perform comprehensive analysis on token pairs"""
        if not pairs:
            return {}
            
        # Convert to DataFrame for easier analysis
        df = self._prepare_dataframe(pairs)
        
        # Filter by minimum volume
        df = df[df['volume_h24'] >= min_volume]
        
        analysis = {
            'total_pairs': len(df),
            'new_tokens_count': len([p for p in pairs if self._is_new_token(p)]),
            'highest_volume': self._get_highest_volume(df),
            'most_holders': self._get_most_holders(df),
            'price_movements': self._analyze_price_movements(df),
            'holder_growth': self._analyze_holder_growth(df),
            'chain_distribution': self._get_chain_distribution(df),
            'pump_signals': self._detect_pump_signals(df),
            'dump_warnings': self._detect_dump_warnings(df),
            'growing_holders': self._count_growing_holders(df),
            'timestamp': datetime.now().isoformat()
        }
        
        return analysis
    
    def _prepare_dataframe(self, pairs: List[Dict]) -> pd.DataFrame:
        """Convert pairs data to DataFrame"""
        data = []
        for pair in pairs:
            try:
                row = {
                    'pair_address': pair.get('pairAddress'),
                    'base_token_symbol': pair.get('baseToken', {}).get('symbol'),
                    'base_token_address': pair.get('baseToken', {}).get('address'),
                    'quote_token_symbol': pair.get('quoteToken', {}).get('symbol'),
                    'chain_id': pair.get('chainId'),
                    'dex_id': pair.get('dexId'),
                    'price_usd': float(pair.get('priceUsd', 0)),
                    'volume_h24': float(pair.get('volume', {}).get('h24', 0)),
                    'price_change_h24': float(pair.get('priceChange', {}).get('h24', 0)),
                    'liquidity_usd': float(pair.get('liquidity', {}).get('usd', 0)),
                    'fdv': float(pair.get('fdv', 0)),
                    'market_cap': float(pair.get('marketCap', 0)),
                    'pair_created_at': pair.get('pairCreatedAt'),
                    'txns_h24': pair.get('txns', {}).get('h24', {}).get('buys', 0) + 
                               pair.get('txns', {}).get('h24', {}).get('sells', 0),
                    'holders': pair.get('holders', 0)
                }
                data.append(row)
            except (ValueError, TypeError) as e:
                logger.warning(f"Error processing pair: {e}")
                continue
                
        return pd.DataFrame(data)
    
    def _is_new_token(self, pair: Dict) -> bool:
        """Check if token was created in last 24 hours"""
        created_at = pair.get('pairCreatedAt')
        if not created_at:
            return False
            
        try:
            created_time = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
            return datetime.now().astimezone() - created_time < timedelta(hours=24)
        except:
            return False
    
    def _get_highest_volume(self, df: pd.DataFrame) -> Dict:
        """Get token with highest volume"""
        if df.empty:
            return {}
            
        max_volume = df.loc[df['volume_h24'].idxmax()]
        return {
            'symbol': max_volume['base_token_symbol'],
            'volume': max_volume['volume_h24'],
            'price': max_volume['price_usd'],
            'chain': max_volume['chain_id']
        }
    
    def _get_most_holders(self, df: pd.DataFrame) -> Dict:
        """Get token with most holders"""
        if df.empty or 'holders' not in df.columns:
            return {}
            
        df_with_holders = df[df['holders'] > 0]
        if df_with_holders.empty:
            return {}
            
        max_holders = df_with_holders.loc[df_with_holders['holders'].idxmax()]
        return {
            'symbol': max_holders['base_token_symbol'],
            'holders': max_holders['holders'],
            'price': max_holders['price_usd'],
            'chain': max_holders['chain_id']
        }
    
    def _analyze_price_movements(self, df: pd.DataFrame) -> Dict:
        """Analyze price movements across tokens"""
        if df.empty:
            return {}
            
        return {
            'average_change': df['price_change_h24'].mean(),
            'positive_movers': len(df[df['price_change_h24'] > 0]),
            'negative_movers': len(df[df['price_change_h24'] < 0]),
            'top_gainer': df.loc[df['price_change_h24'].idxmax()]['price_change_h24'] if not df.empty else 0,
            'top_loser': df.loc[df['price_change_h24'].idxmin()]['price_change_h24'] if not df.empty else 0
        }
    
    def _analyze_holder_growth(self, df: pd.DataFrame) -> Dict:
        """Analyze holder growth patterns"""
        # This would typically require historical data
        # For now, we'll return basic stats
        if df.empty or 'holders' not in df.columns:
            return {}
            
        return {
            'average_holders': df['holders'].mean(),
            'median_holders': df['holders'].median(),
            'tokens_with_holders': len(df[df['holders'] > 0])
        }
    
    def _get_chain_distribution(self, df: pd.DataFrame) -> Dict:
        """Get distribution of tokens across chains"""
        return df['chain_id'].value_counts().to_dict()
    
    def _detect_pump_signals(self, df: pd.DataFrame) -> int:
        """Detect potential pump signals"""
        if df.empty:
            return 0
            
        pump_conditions = (
            (df['price_change_h24'] > PUMP_THRESHOLD) &
            (df['volume_h24'] > MIN_VOLUME_THRESHOLD) &
            (df['txns_h24'] > 100)  # Minimum transactions
        )
        return len(df[pump_conditions])
    
    def _detect_dump_warnings(self, df: pd.DataFrame) -> int:
        """Detect potential dump warnings"""
        if df.empty:
            return 0
            
        dump_conditions = (
            (df['price_change_h24'] < DUMP_THRESHOLD) &
            (df['volume_h24'] > MIN_VOLUME_THRESHOLD) &
            (df['txns_h24'] > 50)  # Minimum transactions
        )
        return len(df[dump_conditions])
    
    def _count_growing_holders(self, df: pd.DataFrame) -> int:
        """Count tokens with growing holder base"""
        # This is a simplified version - real implementation would need historical data
        if df.empty:
            return 0
        # Assume tokens with high volume and positive price movement have growing holders
        growing_conditions = (
            (df['price_change_h24'] > 0) &
            (df['volume_h24'] > MIN_VOLUME_THRESHOLD) &
            (df['holders'] > MIN_HOLDERS_THRESHOLD)
        )
        return len(df[growing_conditions])
    
    def generate_insights_report(self, analysis: Dict) -> Dict:
        """Generate human-readable insights from analysis"""
        insights = analysis.copy()
        
        # Add insights text
        insights['summary'] = self._generate_summary(analysis)
        insights['recommendations'] = self._generate_recommendations(analysis)
        
        return insights
    
    def _generate_summary(self, analysis: Dict) -> str:
        """Generate summary text"""
        parts = []
        
        if analysis.get('new_tokens_count', 0) > 0:
            parts.append(f"🆕 {analysis['new_tokens_count']} new tokens launched")
            
        if analysis.get('pump_signals', 0) > 0:
            parts.append(f"🚀 {analysis['pump_signals']} potential pump signals")
            
        if analysis.get('dump_warnings', 0) > 0:
            parts.append(f"⚠️  {analysis['dump_warnings']} dump warnings")
            
        return ". ".join(parts) if parts else "Market appears stable"
    
    def _generate_recommendations(self, analysis: Dict) -> List[str]:
        """Generate trading recommendations"""
        recommendations = []
        
        if analysis.get('pump_signals', 0) > 3:
            recommendations.append("High pump activity detected - consider careful monitoring")
            
        if analysis.get('dump_warnings', 0) > 5:
            recommendations.append("Multiple dump warnings - exercise caution with new positions")
            
        if analysis.get('growing_holders', 0) > 10:
            recommendations.append("Strong holder growth observed in multiple tokens")
            
        return recommendations if recommendations else ["Market conditions appear normal"]
