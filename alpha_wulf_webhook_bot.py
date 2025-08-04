import logging
import os
from flask import Flask, request, jsonify
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Configuration
BOT_TOKEN = os.getenv("BOT_TOKEN", "7814915502:AAEvJYdzy79cvZnGEP8BqlC1MF0yvAgTsXo")
WEB_APP_URL = os.getenv("WEB_APP_URL", "https://alphawulf-frontend-xn9o.onrender.com")
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "")  # Set this to your deployed webhook URL
PORT = int(os.getenv("PORT", 5000))

# Flask app
app = Flask(__name__)

class AlphaWulfBot:
    def __init__(self, token: str, web_app_url: str):
        self.token = token
        self.web_app_url = web_app_url
        self.application = Application.builder().token(token).build()
        self.setup_handlers()

    def setup_handlers(self):
        """Set up all command and message handlers"""
        # Command handlers
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("play", self.play_command))
        self.application.add_handler(CommandHandler("game", self.play_command))
        self.application.add_handler(CommandHandler("earn", self.play_command))
        self.application.add_handler(CommandHandler("tap", self.play_command))
        self.application.add_handler(CommandHandler("coins", self.play_command))
        self.application.add_handler(CommandHandler("stats", self.stats_command))
        self.application.add_handler(CommandHandler("referral", self.referral_command))
        self.application.add_handler(CommandHandler("withdraw", self.withdraw_command))
        self.application.add_handler(CommandHandler("upgrade", self.upgrade_command))
        self.application.add_handler(CommandHandler("admin", self.admin_command))

        # Message handler for any text (fallback to web app)
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle the /start command - Launch web app automatically"""
        user = update.effective_user
        logger.info(f"User {user.id} ({user.username}) started the bot")

        # Create web app button
        keyboard = [
            [InlineKeyboardButton("🐺 Play Alpha Wulf", web_app=WebAppInfo(url=self.web_app_url))]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        welcome_message = f"""🐺 **Welcome to Alpha Wulf, {user.first_name}!**

🎮 **Tap to Earn Wolf Coins**
⚡ **Regenerate Energy Every 30 Seconds**
🪙 **Collect Coins and Upgrade Your Power**
💰 **Withdraw Real Money via UPI**
👥 **Invite Friends and Earn Referral Rewards**

🚀 **Click the button below to start playing!**

*The game will open directly in Telegram - no external apps needed!*"""

        await update.message.reply_text(
            welcome_message,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle the /help command"""
        keyboard = [
            [InlineKeyboardButton("🐺 Play Game", web_app=WebAppInfo(url=self.web_app_url))]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        help_message = """🐺 **Alpha Wulf - Help**

**Available Commands:**
• `/start` - Start the game
• `/play` - Launch the game
• `/help` - Show this help message
• `/stats` - View your statistics
• `/referral` - Get your referral link
• `/withdraw` - Access withdrawal options
• `/upgrade` - View upgrade options

**How to Play:**
1. 🎯 Tap the wolf to earn coins
2. ⚡ Energy regenerates automatically (1 per 30 seconds)
3. 💪 Upgrade your tap power to earn more coins
4. 💰 Withdraw real money when you reach minimum threshold
5. 👥 Invite friends to earn referral bonuses

**Game Features:**
• Real-time energy regeneration
• Multiple upgrade options
• UPI withdrawal system
• Referral rewards program
• Cross-platform compatibility

Click the button below to start playing!"""

        await update.message.reply_text(
            help_message,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )

    async def play_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle play-related commands - Launch web app"""
        keyboard = [
            [InlineKeyboardButton("🐺 Launch Alpha Wulf", web_app=WebAppInfo(url=self.web_app_url))]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            "🎮 **Ready to Play Alpha Wulf?**\n\n"
            "Click the button below to launch the game!\n"
            "🐺 Tap to earn Wolf Coins\n"
            "⚡ Energy regenerates automatically\n"
            "💰 Withdraw real money",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )

    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle the /stats command"""
        keyboard = [
            [InlineKeyboardButton("📊 View Stats in Game", web_app=WebAppInfo(url=self.web_app_url))]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            "📊 **Your Alpha Wulf Statistics**\n\n"
            "View your detailed statistics in the game:\n"
            "• 🪙 Total coins earned\n"
            "• ⚡ Current energy level\n"
            "• 💪 Tap power level\n"
            "• 👥 Referral count\n"
            "• 💰 Total earnings\n\n"
            "Click the button below to see your stats!",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )

    async def referral_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle the /referral command"""
        user = update.effective_user
        referral_link = f"https://t.me/your_bot_username?start=ref_{user.id}"
        
        keyboard = [
            [InlineKeyboardButton("👥 Manage Referrals", web_app=WebAppInfo(url=self.web_app_url))]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        referral_message = f"""👥 **Alpha Wulf Referral Program**

🎁 **Earn 500 coins for each friend you invite!**
🎁 **Your friend gets 1000 bonus coins!**

📎 **Your Referral Link:**
`{referral_link}`

**How it works:**
1. Share your referral link with friends
2. When they join and start playing, you both get rewards
3. Track your referrals in the game
4. Earn passive income from referral bonuses

Click the button below to manage your referrals!"""

        await update.message.reply_text(
            referral_message,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )

    async def withdraw_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle the /withdraw command"""
        keyboard = [
            [InlineKeyboardButton("💰 Withdraw Coins", web_app=WebAppInfo(url=self.web_app_url))]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            "💰 **Alpha Wulf Withdrawal**\n\n"
            "**Withdrawal Information:**\n"
            "• Minimum: 1,000 coins (₹10)\n"
            "• Processing: 24-48 hours\n"
            "• Method: UPI (Instant)\n"
            "• Fee: 2% of amount\n\n"
            "**Exchange Rate:**\n"
            "• 1,000 coins = ₹10\n"
            "• 2,500 coins = ₹25\n"
            "• 5,000 coins = ₹50\n\n"
            "Click the button below to withdraw your coins!",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )

    async def upgrade_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle the /upgrade command"""
        keyboard = [
            [InlineKeyboardButton("⬆️ View Upgrades", web_app=WebAppInfo(url=self.web_app_url))]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            "⬆️ **Alpha Wulf Upgrades**\n\n"
            "**Available Upgrades:**\n"
            "• 💪 Tap Power - Earn more coins per tap\n"
            "• ⚡ Energy Capacity - Store more energy\n"
            "• 🔄 Regen Rate - Faster energy regeneration\n"
            "• 🎯 Auto Tapper - Automatic coin generation\n\n"
            "**Benefits:**\n"
            "• Increase your earning potential\n"
            "• Play more efficiently\n"
            "• Maximize your profits\n\n"
            "Click the button below to upgrade your wolf!",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )

    async def admin_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle the /admin command"""
        user = update.effective_user
        
        # Check if user is admin (you should implement proper admin checking)
        admin_ids = [123456789]  # Replace with actual admin user IDs
        
        if user.id not in admin_ids:
            await update.message.reply_text(
                "❌ **Access Denied**\n\n"
                "You don't have permission to access admin features.",
                parse_mode='Markdown'
            )
            return

        keyboard = [
            [InlineKeyboardButton("🔧 Admin Panel", web_app=WebAppInfo(url=f"{self.web_app_url}/admin"))]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            "🔧 **Alpha Wulf Admin Panel**\n\n"
            "**Admin Features:**\n"
            "• 👥 User Management\n"
            "• 💰 Withdrawal Requests\n"
            "• 📊 System Statistics\n"
            "• 🔧 Configuration Settings\n\n"
            "Click the button below to access the admin panel!",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle any text message - Redirect to web app"""
        keyboard = [
            [InlineKeyboardButton("🐺 Play Alpha Wulf", web_app=WebAppInfo(url=self.web_app_url))]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            "🐺 **Alpha Wulf**\n\n"
            "I didn't understand that command, but you can always play the game!\n\n"
            "Use `/help` to see available commands or click the button below to play:",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )

    async def error_handler(self, update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle errors"""
        logger.error(f"Exception while handling an update: {context.error}")

    async def setup_webhook(self, webhook_url: str):
        """Set up webhook for the bot"""
        await self.application.bot.set_webhook(url=webhook_url)
        logger.info(f"Webhook set to: {webhook_url}")

    async def process_update(self, update_data):
        """Process incoming webhook update"""
        update = Update.de_json(update_data, self.application.bot)
        await self.application.process_update(update)

# Initialize bot
bot = AlphaWulfBot(BOT_TOKEN, WEB_APP_URL)

# Add error handler
bot.application.add_error_handler(bot.error_handler)

@app.route('/')
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "Alpha Wulf Bot is running", "version": "1.0.0"})

@app.route('/webhook', methods=['POST'])
async def webhook():
    """Handle incoming webhook from Telegram"""
    try:
        update_data = request.get_json()
        if update_data:
            await bot.process_update(update_data)
        return jsonify({"status": "ok"})
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/set_webhook', methods=['POST'])
async def set_webhook():
    """Set webhook URL for the bot"""
    try:
        webhook_url = request.json.get('webhook_url')
        if not webhook_url:
            return jsonify({"status": "error", "message": "webhook_url is required"}), 400
        
        await bot.setup_webhook(webhook_url)
        return jsonify({"status": "success", "message": f"Webhook set to {webhook_url}"})
    except Exception as e:
        logger.error(f"Error setting webhook: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/bot_info')
def bot_info():
    """Get bot information"""
    return jsonify({
        "bot_token": BOT_TOKEN[:10] + "..." if BOT_TOKEN else "Not set",
        "web_app_url": WEB_APP_URL,
        "webhook_url": WEBHOOK_URL,
        "port": PORT
    })

if __name__ == '__main__':
    logger.info("Starting Alpha Wulf Bot Web Service...")
    logger.info(f"Bot Token: {BOT_TOKEN[:10]}..." if BOT_TOKEN else "Bot Token: Not set")
    logger.info(f"Web App URL: {WEB_APP_URL}")
    logger.info(f"Port: {PORT}")
    
    # Run Flask app
    app.run(host='0.0.0.0', port=PORT, debug=False)

