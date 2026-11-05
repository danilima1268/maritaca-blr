# Vamos guardar a referência do último painel de escalação ativo globalmente no bot
ultimo_painel = None


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
    self.mensagem_referencia = None

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

    # Remove o utilizador de outra posição se já estiver nalguma
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


# Comando /escalacao atualizado para guardar a referência global
@bot.tree.command(
    name="escalacao", description="Abre o painel de escalação do Blue Lock Rivals"
)
async def escalacao(interaction: discord.Interaction):
  global ultimo_painel
  view = EscalacaoView()
  await interaction.response.send_message(view.gerar_mensagem(), view=view)
  ultimo_painel = await interaction.original_response()


# Novo comando /moldar_escalacao para definir os jogadores manualmente
@bot.tree.command(
    name="moldar_escalacao",
    description="Molda a escalação definindo os jogadores para cada posição",
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

  # Converte os membros mencionados para o nome de exibição (ou mantém "Vaga Disponível")
  cf_str = cf.display_name if cf else "Vaga Disponível"
  lw_str = lw.display_name if lw else "Vaga Disponível"
  rw_str = rw.display_name if rw else "Vaga Disponível"
  cm_str = cm.display_name if cm else "Vaga Disponível"
  gk_str = gk.display_name if gk else "Vaga Disponível"

  nova_view = EscalacaoView(
      cf=cf_str, lw=lw_str, rw=rw_str, cm=cm_str, gk=gk_str
  )

  # Se já existir um painel criado anteriormente, edita-o diretamente!
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
      pass  # Se a mensagem antiga tiver sido apagada, cria uma nova abaixo

  # Caso contrário, envia um novo painel moldado
  await interaction.response.send_message(
      nova_view.gerar_mensagem(), view=nova_view
  )
  ultimo_painel = await interaction.original_response()
