import logging
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)
import rss_processor
import cohere_generator
import blogger_poster
import database
import config

# লগিং সেটআপ
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# মেইন কিবোর্ড
def get_main_keyboard():
    keyboard = [
        [KeyboardButton("📝 Generate Post")],
        [KeyboardButton("➕ Add Feed"), KeyboardButton("🛠️ Help")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# /start কমান্ড
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    welcome_msg = (
        f"🤖 স্বাগতম {user.first_name}!\n\n"
        "🚀 আমি আপনার স্বয়ংক্রিয় ব্লগার বট\n"
        "📰 RSS ফিড থেকে নিউজ সংগ্রহ ➡️ AI দিয়ে আর্টিকেল তৈরি ➡️ ব্লগারে পোস্ট\n\n"
        "👇 নিচের বাটন ব্যবহার করুন"
    )
    await update.message.reply_text(
        welcome_msg,
        reply_markup=get_main_keyboard()
    )

# 📝 Generate Post হ্যান্ডলার
async def generate_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_text("🔍 সর্বশেষ নিউজ খুঁজছি...")
        
        # RSS থেকে নিউজ সংগ্রহ
        news = rss_processor.get_latest_news()
        if not news:
            await update.message.reply_text("⚠️ কোন নিউজ পাওয়া যায়নি! নতুন RSS ফিড যোগ করুন")
            return
        
        await update.message.reply_text(f"📰 পেয়েছি: {news['title']}")
        await update.message.reply_text("🤖 AI দিয়ে আর্টিকেল তৈরি করা হচ্ছে...")
        
        # Cohere AI দিয়ে আর্টিকেল জেনারেট
        article = cohere_generator.generate_seo_article(news['title'], news['summary'], news['region'])
        
        await update.message.reply_text("🚀 ব্লগারে পোস্ট করা হচ্ছে...")
        
        # ব্লগারে পোস্ট
        result = blogger_poster.create_post(
            news['title'], 
            article, 
            news.get('image')
        )
        
        if result['success']:
            await update.message.reply_text(
                f"✅ সফল!\n\n"
                f"📝 {result['title']}\n"
                f"🔗 {result['url']}"
            )
        else:
            await update.message.reply_text(f"❌ ত্রুটি: {result['error']}")
            
    except Exception as e:
        logger.error(f"ত্রুটি: {str(e)}")
        await update.message.reply_text(f"⚠️ ত্রুটি: {str(e)}")

# Help কমান্ড
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "🆘 সাহায্য:\n\n"
        "• '📝 Generate Post' - নতুন পোস্ট তৈরি করুন\n"
        "• '➕ Add Feed' - RSS ফিড যোগ করুন\n\n"
        "কমান্ড:\n"
        "/add_feed [url] [region] - নতুন RSS ফিড\n"
        "/set_blog [id] - ব্লগ আইডি সেট করুন"
    )
    await update.message.reply_text(help_text)

# ➕ Add Feed হ্যান্ডলার
async def add_feed(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "➕ RSS ফিড যোগ করতে:\n\n"
        "ফরম্যাট: /add_feed [URL] [region]\n"
        "উদাহরণ: /add_feed https://example.com/rss.xml usa\n\n"
        "Region: usa বা eu"
    )

# মেইন ফাংশন
def main():
    # ডাটাবেস ইনিশিয়ালাইজ
    database.init_db()
    
    # বট অ্যাপ্লিকেশন তৈরি
    application = Application.builder().token(config.TELEGRAM_TOKEN).build()
    
    # হ্যান্ডলার রেজিস্টার
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("add_feed", add_feed_command))
    
    # বাটন হ্যান্ডলার
    application.add_handler(MessageHandler(filters.Regex(r'^📝 Generate Post$'), generate_post))
    application.add_handler(MessageHandler(filters.Regex(r'^➕ Add Feed$'), add_feed))
    application.add_handler(MessageHandler(filters.Regex(r'^🛠️ Help$'), help_command))
    
    # বট চালু করুন
    application.run_polling()
    logger.info("🤖 বট সচল...")

if __name__ == '__main__':
    main()
