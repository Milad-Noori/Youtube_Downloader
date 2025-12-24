
import os
from pathlib import Path
import asyncio
from yt_dlp import YoutubeDL
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

from utils import is_youtube, cleanup
from join_check import check_join

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
FORCE_CHANNEL = os.getenv("FORCE_JOIN_CHANNEL")
TMP = Path("downloads")
TMP.mkdir(exist_ok=True)
MAX_UPLOAD = 1800 * 1024 * 1024

ydl_opts = {
    "format": "bestvideo+bestaudio/best",
    "outtmpl": str(TMP / "%(id)s.%(ext)s"),
    "noplaylist": True,
    "quiet": True,
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام ✋\nلینک یوتیوب بفرست تا برات دانلود کنم.")

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_join(update, context):
        return

    url = update.message.text

    if not is_youtube(url):
        await update.message.reply_text("لینک معتبر یوتیوب بده.")
        return

    msg = await update.message.reply_text("در حال دانلود... ⏳")
    loop = asyncio.get_event_loop()

    def download():
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)
            return file_path, info

    try:
        file_path, info = await loop.run_in_executor(None, download)
    except Exception as e:
        await msg.edit_text(f"خطا در دانلود ❌\n{e}")
        return

    size = Path(file_path).stat().st_size

    if size < MAX_UPLOAD:
        await msg.edit_text("در حال آپلود به تلگرام... ⏳")
        try:
            await update.message.reply_document(open(file_path, "rb"))
            cleanup(file_path)
            await msg.delete()
        except Exception as e:
            await msg.edit_text(f"خطا در ارسال ❌\n{e}")
    else:
        await msg.edit_text("فایل بزرگه. ارسال مستقیم ممکن نیست.")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
