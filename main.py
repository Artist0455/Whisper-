from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Application, CommandHandler, InlineQueryHandler, MessageHandler, filters, ContextTypes
import os
import re

BOT_TOKEN = os.environ.get("BOT_TOKEN")

# Store users who started bot
started_users = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user.username:
        started_users[user.username] = user.id
        welcome_message = (
            "🤖 **Welcome to WhisperBot!**\n\n"
            "Aap apne group me kisi bhi user ko **secret message** bhejna chahte ho, "
            "to bas aise likhein:\n\n"
            "`@whisperbot @username aapka message`\n\n"
            "Example: `@whisperbot @mithlesh Hello! Ye secret hai!`\n\n"
            "Main aapke messages ko **private** me send karunga, agar recipient ne mujhe **/start** kiya ho."
        )
        await update.message.reply_text(welcome_message, parse_mode="Markdown")
    else:
        await update.message.reply_text("❗ Aapka Telegram username set nahi hai.")

async def inline_query_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    inline_query = update.inline_query.query
    match = re.match(r"@whisperbot\s+@(\w+)\s+(.+)", inline_query)
    
    if match:
        target_username = match.group(1)
        message = match.group(2)

        # Check if the recipient has started the bot
        if target_username in started_users:
            # Generate inline result
            result = InlineQueryResultArticle(
                id=1,
                title="Send Whisper",
                input_message_content=InputTextMessageContent(f"💬 Whisper to @{target_username}: {message}")
            )
            await update.inline_query.answer([result])
        else:
            result = InlineQueryResultArticle(
                id=2,
                title="Error",
                input_message_content=InputTextMessageContent(f"❌ @{target_username} ne /start nahi kiya hai. Whisper message nahi bheja ja sakta.")
            )
            await update.inline_query.answer([result])
    else:
        result = InlineQueryResultArticle(
            id=3,
            title="Invalid Format",
            input_message_content=InputTextMessageContent("⚠️ Please use the correct format: `@whisperbot @username Your message`")
        )
        await update.inline_query.answer([result])

if __name__ == '__main__':
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(InlineQueryHandler(inline_query_handler))
    app.run_polling()
    
