import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import requests
from bs4 import BeautifulSoup

# 🔑 Your Telegram bot token
BOT_TOKEN = "8480441379:AAEgI49dZlKOxemh2ChXcRWhK2sUbcwyi6s"

logging.basicConfig(level=logging.INFO)

def get_latest_tournaments():
    url = "https://www.upca.tv/news.html"
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")

    tournaments = []
    for item in soup.select(".news-item")[:5]:
        title = item.get_text(strip=True)
        link = item.find("a")["href"] if item.find("a") else "No link"
        tournaments.append({"name": title, "registration": link})
    return tournaments

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🏏 Welcome! I’ll keep you updated about UPCA tournaments.\n\n"
        "Use /tournaments to see the latest."
    )

async def tournaments(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = get_latest_tournaments()
    if not data:
        await update.message.reply_text("⚠️ No tournaments found right now.")
        return
    reply = "📅 Latest UPCA Tournaments:\n\n"
    for t in data:
        reply += f"🏆 {t['name']}\n🔗 {t['registration']}\n\n"
    await update.message.reply_text(reply)

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("tournaments", tournaments))
    app.run_polling()

if __name__ == "__main__":
    main()
