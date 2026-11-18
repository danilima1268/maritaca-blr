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

# Variáveis globais para guardar o último painel criado de cada tipo
ultimo_painel = None


@bot.event
async def on_ready():
  print(f"Bot ligado com sucesso como {bot.user}")
  try:
    synced = await bot.tree.sync()
    print(f"Sincronizados {len(synced)} comandos de barra com sucesso.")
  except Exception as e:
    print(f"Erro ao sincronizar comandos: {e}")


# 3. View do Painel de Escalação Normal
class EscalacaoView(discord.ui.View):

  def __init__(
      self,
      cf="Vaga Disponível",
      lw="Vaga Disponível",
      rw="Vaga Disponível",
      cm="Vaga Disponível",
      gk="Vaga Disponível",
  ):
    super().__init__(timeout=None)
    self.vagas = {"CF": cf, "LW": lw, "RW": rw, "CM": cm, "GK": gk}

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

    for pos, ocupante in self.vagas.items():
      if ocupante == user_nome:
        self.vagas[pos] = "Vaga Disponível"

    if self.vagas[posicao] == "Vaga Disponível":
      self.vagas[posicao] = user_nome
      await interaction.response.edit_message(
          content=self.gerar_mensagem(), view=self
      )
    elif self.vagas[posicao] == user_nome:
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


# 4. View do Painel de Tryout com Time A em cima e Time B embaixo
class TryoutView(discord.ui.View):

  def __init__(self):
    super().__init__(timeout=None)
    self.time_a = {
        "CF": "Vaga Disponível",
        "LW": "Vaga Disponível",
        "RW": "Vaga Disponível",
        "CM": "Vaga Disponível",
        "GK": "Vaga Disponível",
    }
    self.time_b = {
        "CF": "Vaga Disponível",
        "LW": "Vaga Disponível",
        "RW": "Vaga Disponível",
        "CM": "Vaga Disponível",
        "GK": "Vaga Disponível",
    }

  def gerar_mensagem(self):
    return (
        "⚔️ **TRYOUT / TREINO INTERNO — TIME A vs TIME B** ⚔️\n\n"
        "**Time A:**\n"
        f"🔸 **CF:** {self.time_a['CF']}\n"
        f"🔸 **LW:** {self.time_a['LW']}\n"
        f"🔸 **RW:** {self.time_a['RW']}\n"
        f"🔸 **CM:** {self.time_a['CM']}\n"
        f"🔸 **GK:** {self.time_a['GK']}\n\n"
        "**Time B:**\n"
        f"🔸 **CF:** {self.time_b['CF']}\n"
        f"🔸 **LW:** {self.time_b['LW']}\n"
        f"🔸 **RW:** {self.time_b['RW']}\n"
        f"🔸 **CM:** {self.time_b['CM']}\n"
        f"🔸 **GK:** {self.time_b['GK']}"
    )

  async def processar_tryout(
      self, interaction: discord.Interaction, time_alvo: str, posicao: str
  ):
    user_nome = interaction.user.display_name

    for pos in self.time_a:
      if self.time_a[pos] == user_nome:
        self.time_a[pos] = "Vaga Disponível"
    for pos in self.time_b:
      if self.time_b[pos] == user_nome:
        self.time_b[pos] = "Vaga Disponível"

    alvo_dict = self.time_a if time_alvo == "A" else self.time_b

    if alvo_dict[posicao] == "Vaga Disponível":
      alvo_dict[posicao] = user_nome
      await interaction.response.edit_message(
          content=self.gerar_mensagem(), view=self
      )
    else:
      await interaction.response.send_message(
          f"Esta posição no Time {time_alvo} já está ocupada por"
          f" {alvo_dict[posicao]}!",
          ephemeral=True,
      )

  # --- BOTÕES DO TIME A (Linha 0) ---
  @discord.ui.button(
      label="A: CF",
      style=discord.ButtonStyle.green,
      custom_id="try_a_cf",
      row=0,
  )
  async def a_cf(
      self, interaction: discord.Interaction, button: discord.ui.Button
  ):
    await self.processar_tryout(interaction, "A", "CF")

  @discord.ui.button(
      label="A: LW",
      style=discord.ButtonStyle.blurple,
      custom_id="try_a_lw",
      row=0,
  )
  async def a_lw(
      self, interaction: discord.Interaction, button: discord.ui.Button
  ):
    await self.processar_tryout(interaction, "A", "LW")

  @discord.ui.button(
      label="A: RW",
      style=discord.ButtonStyle.blurple,
      custom_id="try_a_rw",
      row=0,
  )
  async def a_rw(
      self, interaction: discord.Interaction, button: discord.ui.Button
  ):
    await self.processar_tryout(interaction, "A", "RW")

  @discord.ui.button(
      label="A: CM",
      style=discord.ButtonStyle.blurple,
      custom_id="try_a_cm",
      row=0,
  )
  async def a_cm(
      self, interaction: discord.Interaction, button: discord.ui.Button
  ):
    await self.processar_tryout(interaction, "A", "CM")

  @discord.ui.button(
      label="A: GK",
      style=discord.ButtonStyle.red,
      custom_id="try_a_gk",
      row=0,
  )
  async def a_gk(
      self, interaction: discord.Interaction, button: discord.ui.Button
  ):
    await self.processar_tryout(interaction, "A", "GK")

  # --- BOTÕES DO TIME B (Linha 1) ---
  @discord.ui.button(
      label="B: CF",
      style=discord.ButtonStyle.green,
      custom_id="try_b_cf",
      row=1,
  )
  async def b_cf(
      self, interaction: discord.Interaction, button: discord.ui.Button
  ):
    await self.processar_tryout(interaction, "B", "CF")

  @discord.ui.button(
      label="B: LW",
      style=discord.ButtonStyle.blurple,
      custom_id="try_b_lw",
      row=1,
  )
  async def b_lw(
      self, interaction: discord.Interaction, button: discord.ui.Button
  ):
    await self.processar_tryout(interaction, "B", "LW")

  @discord.ui.button(
      label="B: RW",
      style=discord.ButtonStyle.blurple,
      custom_id="try_b_rw",
      row=1,
  )
  async def b_rw(
      self, interaction: discord.Interaction, button: discord.ui.Button
  ):
    await self.processar_tryout(interaction, "B", "RW")

  @discord.ui.button(
      label="B: CM",
      style=discord.ButtonStyle.blurple,
      custom_id="try_b_cm",
      row=1,
  )
  async def b_cm(
      self, interaction: discord.Interaction, button: discord.ui.Button
  ):
    await self.processar_tryout(interaction, "B", "CM")

  @discord.ui.button(
      label="B: GK",
      style=discord.ButtonStyle.red,
      custom_id="try_b_gk",
      row=1,
  )
  async def b_gk(
      self, interaction: discord.Interaction, button: discord.ui.Button
  ):
    await self.processar_tryout(interaction, "B", "GK")


# 5. View para o sistema de X1 com restrição de utilizador
class X1View(discord.ui.View):

  def __init__(self, desafiado_id: int):
    super().__init__(timeout=180)
    self.desafiado_id = desafiado_id

  @discord.ui.button(
      label="Aceitar", style=discord.ButtonStyle.green, custom_id="x1_aceitar"
  )
  async def aceitar(
      self, interaction: discord.Interaction, button: discord.ui.Button
  ):
    if interaction.user.id != self.desafiado_id:
      await interaction.response.send_message(
          "Apenas o jogador desafiado pode responder a este convite!",
          ephemeral=True,
      )
      return

    for child in self.children:
      child.disabled = True

    await interaction.response.edit_message(
        content=(
            f"✅ **X1 ACEITE!** {interaction.user.mention} aceitou o desafio!"
            " Que comece o duelo! ⚔️"
        ),
        view=self,
    )
    self.stop()

  @discord.ui.button(
      label="Recusar", style=discord.ButtonStyle.red, custom_id="x1_recusar"
  )
  async def recusar(
      self, interaction: discord.Interaction, button: discord.ui.Button
  ):
    if interaction.user.id != self.desafiado_id:
      await interaction.response.send_message(
          "Apenas o jogador desafiado pode responder a este convite!",
          ephemeral=True,
      )
      return

    for child in self.children:
      child.disabled = True

    await interaction.response.edit_message(
        content=(
            f"❌ **X1 RECUSADO.** {interaction.user.mention} recusou o desafio."
        ),
        view=self,
    )
    self.stop()


# 6. Comandos de Barra (Slash Commands)
@bot.tree.command(
    name="escalacao", description="Abre o painel de escalação do Blue Lock Rivals"
)
async def escalacao(interaction: discord.Interaction):
  global ultimo_painel
  view = EscalacaoView()
  await interaction.response.send_message(view.gerar_mensagem(), view=view)
  ultimo_painel = await interaction.original_response()


@bot.tree.command(
    name="moldar_escalacao",
    description=(
        "Molda a escalação e atualiza o painel principal diretamente"
    ),
)
@app_commands.describe(
    cf="Jogador para a posição
