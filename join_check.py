
from telegram import Update
from telegram.ext import ContextTypes
import os

FORCE_CHANNEL = os.getenv("FORCE_JOIN_CHANNEL")

async def check_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    if not FORCE_CHANNEL:
        return True

    try:
        member = await context.bot.get_chat_member(FORCE_CHANNEL, user.id)
        if member.status in ("member", "administrator", "creator"):
            return True
        else:
            await update.message.reply_text(
                f"برای استفاده از ربات باید در کانال عضو شوی:\n{FORCE_CHANNEL}"
            )
            return False
    except:
        await update.message.reply_text(
            f"برای استفاده از ربات باید عضو کانال شوی:\n{FORCE_CHANNEL}"
        )
        return False
