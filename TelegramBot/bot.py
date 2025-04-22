from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from telegram import Update
import requests

TELEGRAM_TOKEN = '7930371864:AAFGyZfv1e8rSHW_f8BDfHv9WQP67i43BWk'
GOOGLE_API_KEY = 'AIzaSyCcRgrXrhQ3Em_sK1athBpqCaqEBOwSVF0'

def check_url_safety(url):
    api_url = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={GOOGLE_API_KEY}"
    payload = {
        "client": {"clientId": "url-check-bot", "clientVersion": "1.0"},
        "threatInfo": {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{"url": url}]
        }
    }
    response = requests.post(api_url, json=payload)
    result = response.json()
    return "⚠️ Опасная ссылка!" if result.get("matches") else "✅ Ссылка безопасна."

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text.startswith("http"):
        result = check_url_safety(text)
        await update.message.reply_text(result)
    else:
        await update.message.reply_text("Пожалуйста, отправь ссылку для проверки.")

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
app.run_polling()
