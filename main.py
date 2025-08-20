from flask import Flask, request
import discord
from discord.ext import commands
import threading
import os

# 🔑 Le token du bot est stocké dans les variables d'environnement Render
TOKEN = os.environ.get("DISCORD_TOKEN")

# ⚠️ Remplace par l'ID du salon #musique
CHANNEL_ID = 1388870274018971648  

# Intents nécessaires
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True

# Initialisation bot
bot = commands.Bot(command_prefix="!", intents=intents)

# Flask
app = Flask(__name__)

@app.route("/")
def home():
    return {"status": "ok", "message": "Bot en ligne 🚀"}

@app.route("/play", methods=["POST"])
def play():
    data = request.json
    titre = data.get("title")
    if not titre:
        return {"status": "error", "message": "Aucun titre fourni"}

    async def send_play():
        channel = bot.get_channel(CHANNEL_ID)
        if channel:
            # ⚡ Ici on envoie exactement la commande que tu veux
            await channel.send(f"!play query:{titre}")
        else:
            print("Salon non trouvé")

    bot.loop.create_task(send_play())
    return {"status": "ok", "message": f"Commande envoyée : {titre}"}

@bot.event
async def on_ready():
    print(f"✅ Bot connecté en tant que {bot.user}")

# Lancer Flask + Discord ensemble
def run():
    threading.Thread(target=lambda: app.run(host="0.0.0.0", port=8080)).start()
    bot.run(TOKEN)

if __name__ == "__main__":
    run()
