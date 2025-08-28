from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os
import re

BOT_TOKEN = os.environ.get("BOT_TOKEN")

# Store users who started bot
started_users = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user.username:
        started_users[user.username] = user.id
        await update.message.reply_text("🤖 Whisper bot ready! Ab aapko koi group me secret message bhej sakta hai.")
    else:
        await update.message.reply_text("❗ Aapka Telegram username set nahi hai.")

async def whisper_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    pattern = r"@whisperbot\s+@(\w+)\s+(.+)"
    match = re.match(pattern, text)

    if match:
        target_username = match.group(1)
        message = match.group(2)

        sender = update.effective_user.username or update.effective_user.first_name

        if target_username in started_users:
            await context.bot.send_message(
                chat_id=started_users[target_username],
                text=f"💬 Whisper from @{sender}:\n{message}"
            )
            await update.message.reply_text("✅ Message sent privately!")
        else:
            await update.message.reply_text(f"❌ @{target_username} ne /start nahi kiya hai.")
    else:
        pass

if __name__ == '__main__':
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), whisper_handler))
    app.run_polling()
    
