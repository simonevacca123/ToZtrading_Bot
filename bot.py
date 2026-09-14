import os
import logging
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from news_fetcher import fetch_all_news
from ai_analyzer import (
    analyze_market_opportunities,
    butterfly_effect,
    analyze_fomo,
    roast_portfolio,
    plan_investment
)

# --- MINI SERVER PER MANTENERE IL BOT SU RENDER FREE ($0/mese) ---
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running 24/7!")

def run_health_check():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), HealthCheckHandler)
    server.serve_forever()

threading.Thread(target=run_health_check, daemon=True).start()
# -----------------------------------------------------------------

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    benvenuto = (
        "🤖 **ToZtrading_Bot - Advanced Financial AI**\n\n"
        "Comandi disponibili:\n"
        "📊 `/top_picks` - Analisi quotidiana dei mercati.\n"
        "🦋 `/effetto_farfalla [evento]` - Reazioni a catena macroeconomiche.\n"
        "🫧 `/fomo_meter [ticker]` - Misura il rischio bolla speculativa.\n"
        "🔥 `/roast [titoli]` - Analisi spietata del portafoglio.\n"
        "💼 `/investi [importo]` - Portafoglio ottimizzato e stima rendimento.\n"
    )
    await update.message.reply_text(benvenuto, parse_mode="Markdown")

async def top_picks_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔎 Elaborazione analisi base in corso...")
    try:
        raw_news = fetch_all_news(limit_per_feed=3)
        analysis = analyze_market_opportunities(raw_news)
        await update.message.reply_text(analysis)
    except Exception as e:
        await update.message.reply_text(f"❌ Errore: {str(e)}")

async def farfalla_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("⚠️ Scrivi l'evento! Es: /effetto_farfalla taglio dei tassi FED")
        return
    evento = " ".join(context.args)
    await update.message.reply_text(f"🦋 Calcolo le reazioni a catena per: '{evento}'...")
    risposta = butterfly_effect(evento)
    await update.message.reply_text(risposta)

async def fomo_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("⚠️ Scrivi il ticker! Es: /fomo_meter NVDA")
        return
    ticker = context.args[0]
    await update.message.reply_text(f"🫧 Analizzo l'hype sui social e i fondamentali di {ticker}...")
    risposta = analyze_fomo(ticker)
    await update.message.reply_text(risposta)

async def roast_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("⚠️ Scrivi il tuo portafoglio! Es: /roast AAPL, TSLA, BTC")
        return
    portfolio = " ".join(context.args)
    await update.message.reply_text("🔥 Invio il tuo portafoglio ai lupi di Wall Street...")
    risposta = roast_portfolio(portfolio)
    await update.message.reply_text(risposta)

async def investi_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("⚠️ Inserisci un importo! Es: /investi 10000€")
        return
    importo = " ".join(context.args)
    await update.message.reply_text(f"💼 Costruisco il portafoglio ottimizzato per {importo}...")
    try:
        news = fetch_all_news(limit_per_feed=2)
        risposta = plan_investment(importo, news)
        await update.message.reply_text(risposta)
    except Exception as e:
        await update.message.reply_text(f"❌ Errore durante il calcolo: {str(e)}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("top_picks", top_picks_command))
    app.add_handler(CommandHandler("effetto_farfalla", farfalla_command))
    app.add_handler(CommandHandler("fomo_meter", fomo_command))
    app.add_handler(CommandHandler("roast", roast_command))
    app.add_handler(CommandHandler("investi", investi_command))
    
    print("🚀 ToZtrading_Bot PRO è online!")
    app.run_polling()