import os
from threading import Thread
from flask import Flask
import discord
from discord import app_commands
from discord.ext import commands

# 1. Servidor web Flask para o Render manter a porta aberta 24/7
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


# 3. View do Painel de Escalação
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

  async def processar_clique(
      self, interaction: discord.Interaction, posicao: str
  ):
    user_nome = interaction.user.display_name

    # Verifica se o utilizador já está noutra posição. Se estiver, remove-o de lá primeiro para permitir a troca.
    for pos, ocupante in self.vagas.items():
      if ocupante == user_nome:
        self.vagas[pos] = "Vaga Disponível"

    # Se a posição escolhida já estava ocupada por outra pessoa (e não era ele próprio)
    if self.vagas[posicao] != "Vaga Disponível" and self.vagas[posicao] != user_nome:
      # Como limpamos o user acima se ele já estivesse noutra, reatribuímos caso ele estivesse exatamente nesta (o que aciona o cancelamento)
      pass

    # Lógica de Ocupar / Cancelar
    if self.vagas[posicao] == "Vaga Disponível":
      self.vagas[posicao] = user_nome
      await interaction.response.edit_message(
          content=self.gerar_mensagem(), view=self
      )
    elif self.vagas[posicao] == user_nome:
      # Clicou na mesma posição onde já estava -> Cancela / Liberta a vaga
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
    await self.processar_clique(interaction, "CF")

  @discord.ui.button(
      label="LW", style=discord.ButtonStyle.blurple, custom_id="pos_lw"
  )
  async def lw_button(
      self, interaction: discord.Interaction, button: discord.ui.Button
  ):
    await self.processar_clique(interaction, "LW")

  @discord.ui.button(
      label="RW", style=discord.ButtonStyle.blurple, custom_id="pos_rw"
  )
  async def rw_button(
      self, interaction: discord.Interaction, button: discord.ui.Button
  ):
    await self.processar_clique(interaction, "RW")

  @discord.ui.button(
      label="CM", style=discord.ButtonStyle.blurple, custom_id="pos_cm"
  )
  async def cm_button(
      self, interaction: discord.Interaction, button: discord.ui.Button
  ):
    await self.processar_clique(interaction, "CM")

  @discord.ui.button(
      label="GK", style=discord.ButtonStyle.red, custom_id="pos_gk"
  )
  async def gk_button(
      self, interaction: discord.Interaction, button: discord.ui.Button
  ):
    await self.processar_clique(interaction, "GK")


# 4. Comando /escalacao
@bot.tree.command(
    name="escalacao", description="Abre o painel de escalação do Blue Lock Rivals"
)
async def escalacao(interaction: discord.Interaction):
  view = EscalacaoView()
  await interaction.response.send_message(view.gerar_mensagem(), view=view)


# 5. Arranque do Bot
if __name__ == "__main__":
  keep_alive()
  token = os.getenv("DISCORD_TOKEN")
  if token:
    bot.run(token)
  else:
    print("Erro: A variável de ambiente DISCORD_TOKEN não está definida!")
