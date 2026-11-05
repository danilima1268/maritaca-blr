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


# 3. Painel de Escalação com o formato original
class EscalacaoView(discord.ui.View):

  def __init__(self):
    super().__init__(timeout=None)
    self.vagas = {
        "CF": "Vaga Disponível",
        "LW": "Vaga Disponível",
        "RW": "Vaga Disponível",
        "CM": "Vaga Disponível",
        "GK": "Vaga Disponível",
    }

  def gerar_mensagem(self):
    return (
        "⚽ **ESCALAÇÃO - BLUE LOCK RIVALS** ⚽\n\n"
        "Clique no botão correspondente para garantir a sua posição:\n\n"
        f"🔸 **CF**: {self.vagas['CF']}\n"
        f"🔸 **LW**: {self.vagas['LW']}\n"
        f"🔸 **RW**: {self.vagas['RW']}\n"
        f"🔸 **CM**: {self.vagas['CM']}\n"
        f"🔸 **GK**: {self.vagas['GK']}"
    )

  async def ocupar_vaga(
      self, interaction: discord.Interaction, posicao: str
  ):
    user_nome = interaction.user.display_name
    if self.vagas[posicao] == "Vaga Disponível":
      self.vagas[posicao] = user_nome
      await interaction.response.edit_message(
          content=self.gerar_mensagem(), view=self
      )
    else:
      # Se já estiver ocupado, permite retirar ou avisa
      if self.vagas[posicao] == user_nome:
        self.vagas[posicao] = "Vaga Disponível"
        await interaction.response.edit_message(
            content=self.gerar_mensagem(), view=self
        )
      else:
        await interaction.response.send_message(
            f"Esta posição já está ocupada por {self.vagas[posicao]}!",
            ephemeral=True,
        )

  @discord.ui.button(
      label="CF", style=discord.ButtonStyle.green, custom_id="pos_cf"
  )
  async def cf_button(
      self, interaction: discord.Interaction, button: discord.ui.Button
  ):
    await self.ocupar_vaga(interaction, "CF")

  @discord.ui.button(
      label="LW", style=discord.ButtonStyle.blurple, custom_id="pos_lw"
  )
  async def lw_button(
      self, interaction: discord.Interaction, button: discord.ui.Button
  ):
    await self.ocupar_vaga(interaction, "LW")

  @discord.ui.button(
      label="RW", style=discord.ButtonStyle.blurple, custom_id="pos_rw"
  )
  async def rw_button(
      self, interaction: discord.Interaction, button: discord.ui.Button
  ):
    await self.ocupar_vaga(interaction, "RW")

  @discord.ui.button(
      label="CM", style=discord.ButtonStyle.blurple, custom_id="pos_cm"
  )
  async def cm_button(
      self, interaction: discord.Interaction, button: discord.ui.Button
  ):
    await self.ocupar_vaga(interaction, "CM")

  @discord.ui.button(
      label="GK", style=discord.ButtonStyle.red, custom_id="pos_gk"
  )
  async def gk_button(
      self, interaction: discord.Interaction, button: discord.ui.Button
  ):
    await self.ocupar_vaga(interaction, "GK")


# 4. Comandos de Barra
@bot.tree.command(
    name="escalacao", description="Abre o painel de escalação do Blue Lock Rivals"
)
async def escalacao(interaction: discord.Interaction):
  view = EscalacaoView()
  await interaction.response.send_message(view.gerar_mensagem(), view=view)


@bot.tree.command(
    name="moldar_escalacao",
    description="Modifica ou molda a tática da tua equipa",
)
@app_commands.describe(tatica="Ex: 4-3-3, 3-2-1, etc.")
async def moldar_escalacao(interaction: discord.Interaction, tatica: str):
  await interaction.response.send_message(
      f"📋 Tática moldada com sucesso para: **{tatica}**!"
  )


@bot.tree.command(
    name="x1", description="Envia um desafio de X1 para outro jogador"
)
@app_commands.describe(adversario="Menciona o jogador para o X1")
async def x1(interaction: discord.Interaction, adversario: discord.Member):
  await interaction.response.send_message(
      f"⚔️ {interaction.user.mention} desafiou {adversario.mention} para um **X1** no Blue Lock Rivals!"
  )


@bot.tree.command(name="ping", description="Verifica o estado do bot")
async def ping(interaction: discord.Interaction):
  await interaction.response.send_message("Pong! ⚽ Bot operacional.")


# 5. Arranque
if __name__ == "__main__":
  keep_alive()
  token = os.getenv("DISCORD_TOKEN")
  if token:
    bot.run(token)
  else:
    print("Erro: A variável de ambiente DISCORD_TOKEN não está definida!")
