import os
from threading import Thread
from flask import Flask
import discord
from discord.ext import commands

# 1. Configurar o servidor web Flask para o Render detetar a porta
app = Flask("")


@app.route("/")
def home():
  return "Bot online e a funcionar!"


def run():
  port = int(os.environ.get("PORT", 8080))
  app.run(host="0.0.0.0", port=port)


def keep_alive():
  t = Thread(target=run)
  t.daemon = True
  t.start()


# 2. Configuração do Bot e das Intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Dicionários de dados para o Blue Lock Rivals
player_stats = {}
active_matches = {}


@bot.event
async def on_ready():
  print(f"Bot ligado com sucesso como {bot.user}")


@bot.command(name="ping")
async def ping(ctx):
  await ctx.send("Pong! ⚽ O bot está online e operacional.")


# Podes adicionar os teus outros comandos aqui em baixo

# 3. Arrancar primeiro o servidor web e logo a seguir o bot
if __name__ == "__main__":
  keep_alive()
  token = os.getenv("DISCORD_TOKEN")
  if token:
    bot.run(token)
  else:
    print("Erro: A variável de ambiente DISCORD_TOKEN não está definida!")
