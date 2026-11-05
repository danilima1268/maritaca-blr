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


# 3. Painel de Escalação (Estilo antigo com proteção anti-roubo)
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

  def gerar_embed(self):
    embed = discord.Embed(
        title="⚽ ESCALAÇÃO — BLUE LOCK RIVALS",
        description="Clique no botão correspondente para garantir a sua posição:",
        color=discord.Color.from_rgb(0, 162, 255),
    )
    embed.add_field(
        name="",
        value=(
            f"🔹 **CF**: {self.vagas['CF']}\n"
            f"🔹 **LW**: {self.vagas['LW']}\n"
            f"🔹 **RW**: {self.vagas['RW']}\n"
            f"🔹 **CM**: {self.vagas['CM']}\n"
            f"🔹 **GK**: {self.vagas['GK']}"
        ),
        inline=False,
    )
    return embed

  async def ocupar_vaga(
      self, interaction: discord.Interaction, posicao: str
  ):
    user_nome = interaction.user.display_name

    # Se a vaga estiver livre, o utilizador ocupa-a
    if self.vagas[posicao] == "Vaga Disponível":
      self.vagas[posicao] = user_nome
      await interaction.response.edit_message(
          embed=self.gerar_embed(), view=self
      )
    else:
      # Se o próprio utilizador já estiver na vaga, ele sai (liberta a vaga)
      if self.vagas[posicao] == user_nome:
        self.vagas[posicao] = "Vaga Disponível"
        await interaction.response.edit_message(
            embed=self.gerar_embed(), view=self
        )
      else:
        # Se estiver ocupado por outra pessoa, bloqueia e avisa
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


# 4. View Interativa para o X1
class X1View(discord.ui.View):

  def __init__(self, desafiante: discord.Member, adversario: discord.Member):
    super().__init__(timeout=60)
    self.desafiante = desafiante
    self.adversario = adversario

  @discord.ui.button(
      label="Aceitar", style=discord.ButtonStyle.green, emoji="✅"
  )
  async def aceitar(
      self, interaction: discord.Interaction, button: discord.ui.Button
  ):
    if interaction.user.id != self.adversario.id:
      await interaction.response.send_message(
          "Apenas o jogador desafiado pode responder a este convite!",
          ephemeral=True,
      )
      return

    for child in self.children:
      child.disabled = True

    embed = discord.Embed(
        title="⚔️ X1 ACEITE — BLUE LOCK RIVALS",
        description=(
            f"O duelo entre {self.desafiante.mention} e"
            f" {self.adversario.mention} foi **CONFIRMADO**! ⚽🔥"
        ),
        color=discord.Color.green(),
    )
    await interaction.response.edit_message(embed=embed, view=self)
    self.stop()

  @discord.ui.button(
      label="Rejeitar", style=discord.ButtonStyle.red, emoji="✖️"
  )
  async def rejeitar(
      self, interaction: discord.Interaction, button: discord.ui.Button
  ):
    if interaction.user.id != self.adversario.id:
      await interaction.response.send_message(
          "Apenas o jogador desafiado pode responder a este convite!",
          ephemeral=True,
      )
      return

    for child in self.children:
      child.disabled = True

    embed = discord.Embed(
        title="❌ DESAFIO RECUSADO",
        description=(
            f"{self.adversario.mention} recusou o desafio de X1 de"
            f" {self.desafiante.mention}."
        ),
        color=discord.Color.red(),
    )
    await interaction.response.edit_message(embed=embed, view=self)
    self.stop()


# 5. Comandos de Barra (Slash Commands)
@bot.tree.command(
    name="escalacao", description="Abre o painel de escalação do Blue Lock Rivals"
)
async def escalacao(interaction: discord.Interaction):
  view = EscalacaoView()
  await interaction.response.send_message(embed=view.gerar_embed(), view=view)


@bot.tree.command(
    name="moldar_escalacao",
    description="Define manualmente os jogadores para cada posição da equipa",
)
@app_commands.describe(
    cf="Jogador para a posição CF",
    lw="Jogador para a posição LW",
    rw="Jogador para a posição RW",
    cm="Jogador para a posição CM",
    gk="Jogador para a posição GK",
)
async def moldar_escalacao(
    interaction: discord.Interaction,
    cf: discord.Member = None,
    lw: discord.Member = None,
    rw: discord.Member = None,
    cm: discord.Member = None,
    gk: discord.Member = None,
):
  cf_str = cf.mention if cf else "Vaga Disponível"
  lw_str = lw.mention if lw else "Vaga Disponível"
  rw_str = rw.mention if rw else "Vaga Disponível"
  cm_str = cm.mention if cm else "Vaga Disponível"
  gk_str = gk.mention if gk else "Vaga Disponível"

  embed = discord.Embed(
      title="⚽ ESCALAÇÃO MOLDADA — BLUE LOCK RIVALS",
      description=(
          "Clique no botão correspondente para garantir a sua posição:\n\n"
          f"🔹 **CF**: {cf_str}\n"
          f"🔹 **LW**: {lw_str}\n"
          f"🔹 **RW**: {rw_str}\n"
          f"🔹 **CM**: {cm_str}\n"
          f"🔹 **GK**: {gk_str}\n\n"
          f"Escalação definida por: {interaction.user.mention}"
      ),
      color=discord.Color.gold(),
  )
  await interaction.response.send_message(embed=embed)


@bot.tree.command(
    name="rank", description="Cria e exibe o Ranking Top 10 do Blue Lock Rivals"
)
@app_commands.describe(
    top1="Jogador em 1º lugar",
    top2="Jogador em 2º lugar",
    top3="Jogador em 3º lugar",
    top4="Jogador em 4º lugar",
    top5="Jogador em 5º lugar",
    top6="Jogador em 6º lugar",
    top7="Jogador em 7º lugar",
    top8="Jogador em 8º lugar",
    top9="Jogador em 9º lugar",
    top10="Jogador em 10º lugar",
)
async def rank(
    interaction: discord.Interaction,
    top1: discord.Member = None,
    top2: discord.Member = None,
    top3: discord.Member = None,
    top4: discord.Member = None,
    top5: discord.Member = None,
    top6: discord.Member = None,
    top7: discord.Member = None,
    top8: discord.Member = None,
    top9: discord.Member = None,
    top10: discord.Member = None,
):
  posicoes = [
      ("👑 1º Lugar", top1),
      ("🥈 2º Lugar", top2),
      ("🥉 3º Lugar", top3),
      ("4º Lugar", top4),
      ("5º Lugar", top5),
      ("6º Lugar", top6),
      ("7º Lugar", top7),
      ("8º Lugar", top8),
      ("9º Lugar", top9),
      ("10º Lugar", top10),
  ]

  descricao = ""
  for label, membro in posicoes:
    mencao = membro.mention if membro else "*(Vago)*"
    descricao += f"**{label}:** {mencao}\n"

  embed = discord.Embed(
      title="🏆 RANKING OFICIAL — TOP 10 BLUE LOCK RIVALS",
      description=descricao,
      color=discord.Color.from_rgb(255, 215, 0),
  )
  embed.set_footer(
      text=f"Ranking atualizado por {interaction.user.display_name}"
  )

  await interaction.response.send_message(embed=embed)


@bot.tree.command(
    name="x1", description="Envia um desafio de X1 para outro jogador"
)
@app_commands.describe(adversario="Menciona o jogador para o X1")
async def x1(interaction: discord.Interaction, adversario: discord.Member):
  if adversario.id == interaction.user.id:
    await interaction.response.send_message(
        "Não podes desafiar-te a ti próprio para um X1!", ephemeral=True
    )
    return

  if adversario.bot:
    await interaction.response.send_message(
        "Não podes desafiar um bot para um X1!", ephemeral=True
    )
    return

  view = X1View(interaction.user, adversario)
  embed = discord.Embed(
      title="👀 NOVO DESAFIO DE X1",
      description=(
          f"{adversario.mention}, foste desafiado por {interaction.user.mention}"
          " para um X1 no Blue Lock Rivals!"
      ),
      color=discord.Color.from_rgb(255, 140, 0),
  )

  await interaction.response.send_message(
      content=adversario.mention, embed=embed, view=view
  )


@bot.tree.command(name="ping", description="Verifica o estado do bot")
async def ping(interaction: discord.Interaction):
  await interaction.response.send_message("Pong! ⚽ Bot operacional.")


# 6. Arranque
if __name__ == "__main__":
  keep_alive()
  token = os.getenv("DISCORD_TOKEN")
  if token:
    bot.run(token)
  else:
    print("Erro: A variável de ambiente DISCORD_TOKEN não está definida!")
