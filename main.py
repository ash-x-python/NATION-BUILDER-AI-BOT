
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Logging setup
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# --- CONFIGURATION ---
TOKEN = "8201721627:AAEVSME33bzcFDdCpUGMuHKxdAIKg_zRaCs"
ADMIN_ID = 6503849855  # Apni numeric ID yahan dalein
CHANNEL_URL = "https://t.me/+neCqNC1JO4thYTdl"

# --- HANDLERS ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🇮🇳 **The Power of Us**\n\n"
        "The root of our challenges isn't just politics—it’s our mindset. 🧠\n"
        "Leaders reflect our choices; to change the nation, we must first change ourselves. 🤝\n\n"
        "Stop the blame game. Shift your perspective. 🚀\n"
        "This Bot is here to help you grow so our country can thrive."
    )
    keyboard = [[InlineKeyboardButton("Join Channel 📢", url=CHANNEL_URL)]]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

async def on_group_add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Jab bot group mein add hoga, Admin ko ID bhej dega"""
    for member in update.message.new_chat_members:
        if member.id == context.bot.id:
            group_name = update.effective_chat.title
            group_id = update.effective_chat.id
            alert_text = f"✅ **Naye Group Mein Add Hua!**\n\nNAME: `{group_name}`\nID: `{group_id}`"
            await context.bot.send_message(chat_id=ADMIN_ID, text=alert_text, parse_mode="Markdown")

async def broadcast_to(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Usage: /broadcastto ID1, ID2 Hello friends"""
    if update.effective_user.id != ADMIN_ID:
        return

    # Command parsing: /broadcastto {id1, id2} message
    if not context.args:
        await update.message.reply_text("Format: `/broadcastto ID1,ID2 Message Text`", parse_mode="Markdown")
        return

    try:
        # IDs nikalne ke liye (comma separated)
        arg_str = " ".join(context.args)
        if "}" in arg_str:
            ids_part = arg_str[arg_str.find("{")+1 : arg_str.find("}")]
            message_text = arg_str[arg_str.find("}")+1 :].strip()
            target_ids = [i.strip() for i in ids_part.split(",")]
        else:
            await update.message.reply_text("Error: IDs ko { } ke andar rakhein.")
            return

        success, failed = 0, 0
        for g_id in target_ids:
            try:
                await context.bot.send_message(chat_id=g_id, text=message_text)
                success += 1
            except Exception:
                failed += 1

        await update.message.reply_text(f"Done! ✅ {success} groups ko gaya, ❌ {failed} failed.")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("broadcastto", broadcast_to))
    # Naye group members track karne ke liye
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, on_group_add))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
