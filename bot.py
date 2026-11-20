
import os
import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(level=logging.INFO)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
API_FOOTBALL_KEY = os.getenv("API_FOOTBALL_KEY")

HEADERS = {"x-apisports-key": API_FOOTBALL_KEY}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "⚽🏀 ¡Bienvenido a LiveSuperBot!\n\n"
        "Comandos disponibles:\n"
        "/futbol - Partidos de fútbol en vivo\n"
        "/nba - Próximamente: NBA\n"
        "/live - Partidos en directo"
    )

async def futbol(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        response = requests.get(
            "https://v3.football.api-sports.io/fixtures",
            headers=HEADERS,
            params={"live": "all"},
            timeout=20
        )
        response.raise_for_status()
        partidos = response.json().get("response", [])

        if not partidos:
            await update.message.reply_text("⚽ No hay partidos en vivo en este momento.")
            return

        for partido in partidos[:10]:
            local = partido["teams"]["home"]["name"]
            visitante = partido["teams"]["away"]["name"]
            goles_local = partido["goals"]["home"]
            goles_visitante = partido["goals"]["away"]
            minuto = partido["fixture"]["status"]["elapsed"]

            await update.message.reply_text(
                f"⚽ {local} {goles_local}-{goles_visitante} {visitante}\n"
                f"⏱️ Minuto: {minuto or 'Sin dato'}"
            )

    except Exception:
        logging.exception("Error consultando API-Football")
        await update.message.reply_text("No pude consultar los partidos. Revisá la API.")

async def nba(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🏀 La sección NBA estará disponible en la próxima actualización."
    )

async def main():
    if not TELEGRAM_TOKEN or not API_FOOTBALL_KEY:
        raise RuntimeError("Faltan las variables TELEGRAM_TOKEN o API_FOOTBALL_KEY")

    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("futbol", futbol))
    app.add_handler(CommandHandler("live", futbol))
    app.add_handler(CommandHandler("nba", nba))

    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await app.updater.idle()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
          
