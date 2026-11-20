import os
import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("TELEGRAM_TOKEN")
API_KEY = os.getenv("API_FOOTBALL_KEY")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "⚽🏀 ¡Bienvenido a LiveSuperBot!\n\n"
        "/futbol - Partidos en vivo\n"
        "/live - Partidos en directo\n"
        "/nba - Sección NBA"
    )

async def futbol(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        response = requests.get(
            "https://v3.football.api-sports.io/fixtures",
            headers={"x-apisports-key": API_KEY},
            params={"live": "all"},
            timeout=20
        )
        response.raise_for_status()
        partidos = response.json().get("response", [])

        if not partidos:
            await update.message.reply_text("⚽ No hay partidos en vivo.")
            return

        for p in partidos[:10]:
            home = p["teams"]["home"]["name"]
            away = p["teams"]["away"]["name"]
            goals = p["goals"]
            minute = p["fixture"]["status"]["elapsed"]

            await update.message.reply_text(
                f"⚽ {home} {goals['home']}-{goals['away']} {away}\n"
                f"⏱️ Minuto: {minute or 'Sin dato'}"
            )
    except Exception:
        logging.exception("Error consultando API")
        await update.message.reply_text("Error consultando los partidos.")

async def nba(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🏀 La sección NBA estará disponible próximamente.")

def main():
    if not TOKEN or not API_KEY:
        raise RuntimeError("Faltan variables de entorno.")

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("futbol", futbol))
    app.add_handler(CommandHandler("live", futbol))
    app.add_handler(CommandHandler("nba", nba))
    app.run_polling()

if __name__ == "__main__":
    main()
