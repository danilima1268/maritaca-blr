import os
from threading import Thread
from flask import Flask
import discord
from discord.ext import commands

# 1. Servidor web Flask para o Render manter a porta aberta
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


# 2. Configuração do Bot e Intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
  print(f"Bot ligado com sucesso como {bot.user}")
  try:
    # Sincroniza os comandos de barra (slash commands) com o Discord
    synced = await bot.tree.sync()
    print(f"Sincronizados {len(synced)} comandos de barra com sucesso.")
  except Exception as e:
    print(f"Erro ao sincronizar comandos: {e}")


# 3. Definição do Comando de Barra /escalacao
@bot.tree.command(
    name="escalacao", description="Faz a escalação para o Blue Lock Rivals"
)
async def escalacao(interaction: discord.Interaction):
  await interaction.response.send_message(
      "⚽ Painel de escalação do Blue Lock Rivals ativado!"
  )


@bot.tree.command(name="ping", description="Verifica a latência e estado do bot")
async def ping(interaction: discord.Interaction):
  await interaction.response.send_message("Pong! ⚽ O bot está online e operacional.")


# 4. Arranque do Servidor e do Bot
if __name__ == "__main__":
  keep_alive()
  token = os.getenv("DISCORD_TOKEN")
  if token:
    bot.run(token)
  else:
    print("Erro: A variável de ambiente DISCORD_TOKEN não está definida!")
