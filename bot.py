import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

async def filme(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Use: /filme genero")
        return

    genero = " ".join(context.args)

    url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={genero}&language=pt-BR"
    response = requests.get(url)
    data = response.json()

    if not data["results"]:
        await update.message.reply_text("Nenhum filme encontrado.")
        return

    resposta = f"🎬 Recomendações de {genero.upper()}:\n\n"

    for filme in data["results"][:3]:
        titulo = filme["title"]
        nota = filme["vote_average"]
        sinopse = (filme["overview"][:150] + "...") if filme["overview"] else "Sem descrição disponível."

        resposta += f"🎥 {titulo}\n"
        resposta += f"⭐ Nota: {nota}\n"
        resposta += f"🧠 {sinopse}\n\n"

    await update.message.reply_text(resposta)

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("filme", filme))

print("Bot rodando...")
app.run_polling()
