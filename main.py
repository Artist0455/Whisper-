from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Application, CommandHandler, InlineQueryHandler, ContextTypes
import os
import re
import uuid  # 👈 unique ID generate karne ke liye

BOT_TOKEN = os.environ.get("BOT_TOKEN")

# Store users who started bot
started_users = {}

# /start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user.username:
        started_users[user.username] = user.id
        welcome_message = (
            "🤖 **Welcome to Artisthidebot!**\n\n"
            "Aap apne group me kisi bhi user ko **secret message** bhejna chahte ho, "
            "to bas aise likhein:\n\n"
            "`@Artisthidebot @username aapka message`\n\n"
            "Example: `@Artisthidebot @mithlesh Hello! Ye secret hai!`\n\n"
            "Main aapke messages ko **private** me send karunga, agar recipient ne mujhe **/start** kiya ho."
        )
        await update.message.reply_text(welcome_message, parse_mode="Markdown")
    else:
        await update.message.reply_text("❗ Aapka Telegram username set nahi hai.")

# Inline query handler
async def inline_query_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    inline_query = update.inline_query.query
    print(f"Received inline query: {inline_query}")

    pattern = r"@Artisthidebot\s+@(\w+)\s+([\s\S]+)"
    match = re.match(pattern, inline_query)

    results = []

    if match:
        target_username = match.group(1)
        message = match.group(2)
        print(f"Extracted username: {target_username}, Message: {message}")

        if target_username in started_users:
            results.append(
                InlineQueryResultArticle(
                    id=str(uuid.uuid4()),   # 👈 unique ID
                    title="Send Whisper",
                    description=f"Send secret message to @{target_username}",
                    input_message_content=InputTextMessageContent(
                        f"💬 Whisper to @{target_username}: {message}"
                    )
                )
            )
        else:
            results.append(
                InlineQueryResultArticle(
                    id=str(uuid.uuid4()),
                    title="Error",
                    description="Recipient has not started the bot",
                    input_message_content=InputTextMessageContent(
                        f"❌ @{target_username} ne /start nahi kiya hai. Whisper message nahi bheja ja sakta."
                    )
                )
            )
    else:
        results.append(
            InlineQueryResultArticle(
                id=str(uuid.uuid4()),
                title="Invalid Format",
                description="Use @Artisthidebot @username message",
                input_message_content=InputTextMessageContent(
                    "⚠️ Please use the correct format: `@Artisthidebot @username Your message`"
                )
            )
        )

    await update.inline_query.answer(results, cache_time=0)  # 👈 fresh result force

if __name__ == '__main__':
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(InlineQueryHandler(inline_query_handler))
    app.run_polling()
    
