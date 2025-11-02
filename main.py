#!/usr/bin/env python3
"""
Web3 Token Analytics Bot - Main Entry Point
"""

import asyncio
import logging 
import argparse
from src.dexscreener_client import DexScreenerClient
from src.telegram_bot import TelegramBot
from src.analytics import TokenAnalytics
from config import *

# Configure logging
logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
logger = logging.getLogger(__name__)

class Web3AnalyticsBot:
    def __init__(self):
        self.dex_client = DexScreenerClient(DEXSCREENER_API_KEY)
        self.analytics = TokenAnalytics()
        self.telegram_bot = TelegramBot(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID)
        
    async def analyze_new_tokens(self, hours=24, min_volume=MIN_VOLUME_THRESHOLD):
        """Main analysis function for new tokens"""
        try:
            logger.info(f"Analyzing new tokens from past {hours} hours...")
            
            # Fetch recent pairs from DexScreener
            pairs = await self.dex_client.get_recent_pairs(hours)
            
            if not pairs:
                logger.warning("No pairs found in the specified timeframes")
                return None
            
            # Perform comprehensive analysis
            analysis = self.analytics.comprehensive_analysis(pairs, min_volume)
            
            # Generate insights report
            report = self.analytics.generate_insights_report(analysis)
            
            # Send to Telegram
            await self.telegram_bot.send_analysis_report(report)
            
            logger.info("Analysis completed successfully")
            return analysis
            
        except Exception as e:
            logger.error(f"Error in analysis: {str(e)}")
            await self.telegram_bot.send_message(f"❌ Analysis failed: {str(e)}")
            return None

    async def run_continuous_monitoring(self, interval=3600):
        """Run continuous monitoring with specified interval"""
        logger.info(f"Starting continuous monitoring with {interval}s interval")
        
        while True:
            try:
                await self.analyze_new_tokens()
                logger.info(f"Sleeping for {interval} seconds...")
                await asyncio.sleep(interval)
            except Exception as e:
                logger.error(f"Monitoring error: {str(e)}")
                await asyncio.sleep(60)  # Wait 1 minute before retry

def main():
    parser = argparse.ArgumentParser(description='Web3 Token Analytics Bot')
    parser.add_argument('--hours', type=int, default=TIME_WINDOW_HOURS, 
                       help='Time window in hours for analysis')
    parser.add_argument('--min-volume', type=float, default=MIN_VOLUME_THRESHOLD,
                       help='Minimum volume threshold in USD')
    parser.add_argument('--continuous', action='store_true',
                       help='Run in continuous monitoring mode')
    parser.add_argument('--interval', type=int, default=3600,
                       help='Interval for continuous monitoring (seconds)')
    
    args = parser.parse_args()
    
    bot = Web3AnalyticsBot()
    
    if args.continuous:
        asyncio.run(bot.run_continuous_monitoring(args.interval))
    else:
        asyncio.run(bot.analyze_new_tokens(args.hours, args.min_volume))

if __name__ == "__main__":
    main()
