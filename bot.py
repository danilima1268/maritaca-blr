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

# Variável global para guardar o último painel de escalação criado
ultimo_painel = None


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


# 4. Comandos de Barra
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
  global ultimo_painel

  cf_str = cf.display_name if cf else "Vaga Disponível"
  lw_str = lw.display_name if lw else "Vaga Disponível"
  rw_str = rw.display_name if rw else "Vaga Disponível"
  cm_str = cm.display_name if cm else "Vaga Disponível"
  gk_str = gk.display_name if gk else "Vaga Disponível"

  nova_view = EscalacaoView(
      cf=cf_str, lw=lw_str, rw=rw_str, cm=cm_str, gk=gk_str
  )

  if ultimo_painel:
    try:
      await ultimo_painel.edit(
          content=nova_view.gerar_mensagem(), view=nova_view
      )
      await interaction.response.send_message(
          "✅ Escalação moldada e atualizada com sucesso no painel principal!",
          ephemeral=True,
      )
      return
    except discord.HTTPException:
      pass

  await interaction.response.send_message(
      nova_view.gerar_mensagem(), view=nova_view
  )
  ultimo_painel = await interaction.original_response()


@bot.tree.command(name="ping", description="Verifica o estado do bot")
async def ping(interaction: discord.Interaction):
  await interaction.response.send_message("Pong! ⚽ Bot operacional.")


# 5. Arranque do Bot
if __name__ == "__main__":
  keep_alive()
  token = os.getenv("DISCORD_TOKEN")
  if token:
    bot.run(token)
  else:
    print("Erro: A variável de ambiente DISCORD_TOKEN não está definida!")
    import discord
from discord import app_commands


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
