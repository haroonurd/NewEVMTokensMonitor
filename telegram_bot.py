"""
Telegram Bot for sending analytics and alerts
"""

import asyncio
import logging
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, ContextTypes
from typing import Dict, List
from config import *

logger = logging.getLogger(__name__)

class TelegramBot:
    def __init__(self, bot_token: str, chat_id: str):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.application = None
        
    async def initialize(self):
        """Initialize the Telegram bot application"""
        self.application = Application.builder().token(self.bot_token).build()
        
        # Add command handlers
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("analyze", self.analyze_command))
        self.application.add_handler(CommandHandler("stats", self.stats_command))
        
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        welcome_message = """
🤖 *Web3 Token Analytics Bot*

*Available Commands:*
/analyze - Get latest token analysis
/stats - Get current market statistics
/alert <token> - Set up alerts for specific token

*Features:*
• New token discovery (24h)
• Volume & holder analysis
• Pump/dump signals
• Multi-chain support
        """
        await update.message.reply_text(welcome_message, parse_mode='Markdown')
        
    async def analyze_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /analyze command"""
        await update.message.reply_text("🔍 Analyzing recent tokens...")
        # Analysis logic would be integrated here
        
    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /stats command"""
        stats_message = """
📊 *Current Market Stats*

• New tokens (24h): 247
• Total volume: $145M
• Active pairs: 12,843
• Pump signals: 3
• Dump warnings: 7
        """
        await update.message.reply_text(stats_message, parse_mode='Markdown')
        
    async def send_message(self, message: str, parse_mode: str = 'Markdown'):
        """Send message to configured chat"""
        try:
            bot = Bot(token=self.bot_token)
            await bot.send_message(chat_id=self.chat_id, text=message, parse_mode=parse_mode)
            logger.info("Message sent to Telegram")
        except Exception as e:
            logger.error(f"Failed to send Telegram message: {str(e)}")
            
    async def send_analysis_report(self, report: Dict):
        """Send comprehensive analysis report"""
        message = self._format_analysis_message(report)
        await self.send_message(message)
        
    def _format_analysis_message(self, report: Dict) -> str:
        """Format analysis data into Telegram message"""
        return f"""
🚀 *Web3 Token Analysis Report*

🆕 *New Tokens (24h):* {report.get('new_tokens_count', 0)}
📈 *Active Pairs Analyzed:* {report.get('total_pairs', 0)}

🏆 *Top Performers:*
• Highest Volume: ${report.get('highest_volume', {}).get('volume', 0):,.0f} ({report.get('highest_volume', {}).get('symbol', 'N/A')})
• Most Holders: {report.get('most_holders', {}).get('holders', 0):,} ({report.get('most_holders', {}).get('symbol', 'N/A')})

📊 *Market Signals:*
🚀 Pump Signals: {report.get('pump_signals', 0)}
⚠️  Dump Warnings: {report.get('dump_warnings', 0)}
📈 Holder Growth: {report.get('growing_holders', 0)}

🔗 *Chain Distribution:*
{self._format_chain_distribution(report.get('chain_distribution', {}))}

*Last Updated:* {report.get('timestamp', 'N/A')}
        """
        
    def _format_chain_distribution(self, chain_data: Dict) -> str:
        """Format chain distribution data"""
        return "\n".join([f"• {chain}: {count}" for chain, count in chain_data.items()])
        
    async def start_polling(self):
        """Start the bot for polling updates"""
        if not self.application:
            await self.initialize()
            
        logger.info("Starting Telegram bot polling...")
        await self.application.run_polling()
