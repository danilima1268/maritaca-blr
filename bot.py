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
          f"Esta posição no Time {time_alvo} já está ocupada por {alvo_dict[posicao]}!",
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
