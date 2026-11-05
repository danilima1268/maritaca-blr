import os
from threading import Thread
from flask import Flask
import discord
from discord import app_commands
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
    synced = await bot.tree.sync()
    print(f"Sincronizados {len(synced)} comandos de barra com sucesso.")
  except Exception as e:
    print(f"Erro ao sincronizar comandos: {e}")


# 3. Views Interativas (Botões e Menus para Escalabilidade e X1)
class EscalacaoView(discord.ui.View):

  def __init__(self):
    super().__init__(timeout=180)

  @discord.ui.button(
      label="Avançado",
      style=discord.ButtonStyle.green,
      emoji="⚽",
      custom_id="pos_avancado",
  )
  async def avancado_callback(
      self, interaction: discord.Interaction, button: discord.ui.Button
  ):
    await interaction.response.send_message(
        "Posição **Avançado** selecionada para a tua escalação!", ephemeral=True
    )

  @discord.ui.button(
      label="Meio-Campista",
      style=discord.ButtonStyle.blurple,
      emoji="🎯",
      custom_id="pos_meio",
  )
  async def meio_callback(
      self, interaction: discord.Interaction, button: discord.ui.Button
  ):
    await interaction.response.send_message(
        "Posição **Meio-Campista** selecionada!", ephemeral=True
    )

  @discord.ui.button(
      label="Defesa",
      style=discord.ButtonStyle.grey,
      emoji="🛡️",
      custom_id="pos_defesa",
  )
  async def defesa_callback(
      self, interaction: discord.Interaction, button: discord.ui.Button
  ):
    await interaction.response.send_message(
        "Posição **Defesa** selecionada!", ephemeral=True
    )


# 4. Comandos de Barra (Slash Commands)
@bot.tree.command(
    name="escalacao",
    description="Abre o painel interativo de escalação do Blue Lock Rivals",
)
async def escalacao(interaction: discord.Interaction):
  view = EscalacaoView()
  await interaction.response.send_message(
      "⚽ **Painel de Escalação - Blue Lock Rivals**\nEscolhe a tua posição abaixo:",
      view=view,
  )


@bot.tree.command(
    name="moldar_escalacao",
    description="Modifica ou molda a tática da tua equipa",
)
@app_commands.describe( tatica="Ex: 4-3-3, 3-2-1, etc." )
async def moldar_escalacao(interaction: discord.Interaction, tatica: str):
  await interaction.response.send_message(
      f"📋 Tática moldada com sucesso para: **{tatica}**! Equipa pronta para o jogo."
  )


@bot.tree.command(
    name="x1", description="Envia um desafio de X1 para outro jogador"
)
@app_commands.describe(adversario="Menciona o jogador para o X1")
async def x1(interaction: discord.Interaction, adversario: discord.Member):
  await interaction.response.send_message(
      f"⚔️ {interaction.user.mention} desafiou {adversario.mention} para um **X1 épico** no Blue Lock Rivals!"
  )


@bot.tree.command(name="ping", description="Verifica o estado do bot")
async def ping(interaction: discord.Interaction):
  await interaction.response.send_message(
      "Pong! ⚽ O bot está online e operacional."
  )


# 5. Arranque do Servidor e do Bot
if __name__ == "__main__":
  keep_alive()
  token = os.getenv("DISCORD_TOKEN")
  if token:
    bot.run(token)
  else:
    print("Erro: A variável de ambiente DISCORD_TOKEN não está definida!")
