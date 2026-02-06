import os
import logging
from flask import Flask
from threading import Thread
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Flask setup for Render
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=8080)

# --- BOT LOGIC ---

ADMIN_ID = 6503849855  # <--- Apni ID yahan daalein
CHANNEL_URL = "https://t.me/nation_growth_ai_bot" # <--- Apne channel ka link

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🇮🇳 **The Power of Us**\n"
        "The root of our challenges isn't just politics—it’s our mindset. 🧠 "
        "Leaders reflect our choices; to change the nation, we must first change ourselves. 🤝\n\n"
        "Stop the blame game. Shift your perspective. 🚀\n"
        "This Bot is here to help you grow so our country can thrive."
    )
    keyboard = [[InlineKeyboardButton("Join Channel 📢", url=CHANNEL_URL)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def on_group_added(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Jab bot group me add ho, admin ko notify kare
    for member in update.message.new_chat_members:
        if member.id == context.bot.id:
            group_name = update.effective_chat.title
            group_id = update.effective_chat.id
            await context.bot.send_message(
                chat_id=ADMIN_ID,
                text=f"📌 **New Group Added!**\n\nName: {group_name}\nID: `{group_id}`",
                parse_mode='Markdown'
            )

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    if not update.message.reply_to_message:
        await update.message.reply_text("❌ Please reply to a message/photo with `/brodcastto {id1, id2}`")
        return

    # Extract IDs from command
    try:
        cmd_text = update.message.text.replace('/brodcastto', '').strip()
        # Clean braces and split by comma
        ids_str = cmd_text.replace('{', '').replace('}', '').split(',')
        target_ids = [i.strip() for i in ids_str if i.strip()]
    except Exception as e:
        await update.message.reply_text("❌ Format galat hai. Use: `/brodcastto {id1, id2}`")
        return

    success = 0
    failed = 0
    original_msg = update.message.reply_to_message

    for chat_id in target_ids:
        try:
            await context.bot.copy_message(
                chat_id=chat_id,
                from_chat_id=original_msg.chat_id,
                message_id=original_msg.message_id
            )
            success += 1
        except Exception:
            failed += 1

    await update.message.reply_text(f"✅ Broadcast Complete!\nSent: {success}\nFailed: {failed}")

if __name__ == '__main__':
    # Start Flask thread
    Thread(target=run).start()

    # Start Telegram Bot
    TOKEN = "8201721627:AAEVSME33bzcFDdCpUGMuHKxdAIKg_zRaCs" # <--- Bot Token daalein
    app_bot = ApplicationBuilder().token(TOKEN).build()

    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(CommandHandler("brodcastto", broadcast))
    app_bot.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, on_group_added))

    print("Bot is alive...")
    app_bot.run_polling()

