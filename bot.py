class TryoutTimeAView(discord.ui.View):

  def __init__(self, tryout_manager):
    super().__init__(timeout=None)
    self.manager = tryout_manager

  @discord.ui.button(
      label="CF", style=discord.ButtonStyle.green, custom_id="try_a_cf"
  )
  async def a_cf(
      self, interaction: discord.Interaction, button: discord.ui.Button
  ):
    await self.manager.processar_tryout(interaction, "A", "CF")

  @discord.ui.button(
      label="LW", style=discord.ButtonStyle.blurple, custom_id="try_a_lw"
  )
  async def a_lw(
      self, interaction: discord.Interaction, button: discord.ui.Button
  ):
    await self.manager.processar_tryout(interaction, "A", "LW")

  @discord.ui.button(
      label="RW", style=discord.ButtonStyle.blurple, custom_id="try_a_rw"
  )
  async def a_rw(
      self, interaction: discord.Interaction, button: discord.ui.Button
  ):
    await self.manager.processar_tryout(interaction, "A", "RW")

  @discord.ui.button(
      label="CM", style=discord.ButtonStyle.blurple, custom_id="try_a_cm"
  )
  async def a_cm(
      self, interaction: discord.Interaction, button: discord.ui.Button
  ):
    await self.manager.processar_tryout(interaction, "A", "CM")

  @discord.ui.button(
      label="GK", style=discord.ButtonStyle.red, custom_id="try_a_gk"
  )
  async def a_gk(
      self, interaction: discord.Interaction, button: discord.ui.Button
  ):
    await self.manager.processar_tryout(interaction, "A", "GK")


class TryoutTimeBView(discord.ui.View):

  def __init__(self, tryout_manager):
    super().__init__(timeout=None)
    self.manager = tryout_manager

  @discord.ui.button(
      label="CF", style=discord.ButtonStyle.green, custom_id="try_b_cf"
  )
  async def b_cf(
      self, interaction: discord.Interaction, button: discord.ui.Button
  ):
    await self.manager.processar_tryout(interaction, "B", "CF")

  @discord.ui.button(
      label="LW", style=discord.ButtonStyle.blurple, custom_id="try_b_lw"
  )
  async def b_lw(
      self, interaction: discord.Interaction, button: discord.ui.Button
  ):
    await self.manager.processar_tryout(interaction, "B", "LW")

  @discord.ui.button(
      label="RW", style=discord.ButtonStyle.blurple, custom_id="try_b_rw"
  )
  async def b_rw(
      self, interaction: discord.Interaction, button: discord.ui.Button
  ):
    await self.manager.processar_tryout(interaction, "B", "RW")

  @discord.ui.button(
      label="CM", style=discord.ButtonStyle.blurple, custom_id="try_b_cm"
  )
  async def b_cm(
      self, interaction: discord.Interaction, button: discord.ui.Button
  ):
    await self.manager.processar_tryout(interaction, "B", "CM")

  @discord.ui.button(
      label="GK", style=discord.ButtonStyle.red, custom_id="try_b_gk"
  )
  async def b_gk(
      self, interaction: discord.Interaction, button: discord.ui.Button
  ):
    await self.manager.processar_tryout(interaction, "B", "GK")


class TryoutManager:

  def __init__(self):
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
    self.msg_a = None
    self.msg_b = None

  def gerar_texto_a(self):
    return (
        "⚔️ **TRYOUT — TIME A** ⚔️\n"
        f"🔸 **CF:** {self.time_a['CF']}\n"
        f"🔸 **LW:** {self.time_a['LW']}\n"
        f"🔸 **RW:** {self.time_a['RW']}\n"
        f"🔸 **CM:** {self.time_a['CM']}\n"
        f"🔸 **GK:** {self.time_a['GK']}"
    )

  def gerar_texto_b(self):
    return (
        "⚔️ **TRYOUT — TIME B** ⚔️\n"
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
      if self.msg_a:
        await self.msg_a.edit(
            content=self.gerar_texto_a(),
            view=TryoutTimeAView(self),
        )
      if self.msg_b:
        await self.msg_b.edit(
            content=self.gerar_texto_b(),
            view=TryoutTimeBView(self),
        )
      await interaction.response.defer()
    else:
      await interaction.response.send_message(
          f"Esta posição no Time {time_alvo} já está ocupada por"
          f" {alvo_dict[posicao]}!",
          ephemeral=True,
      )


@bot.tree.command(
    name="tryout",
    description="Abre o painel de treino interno (Time A e Time B separados)",
)
async def tryout(interaction: discord.Interaction):
  manager = TryoutManager()
  view_a = TryoutTimeAView(manager)
  view_b = TryoutTimeBView(manager)

  await interaction.response.send_message(
      manager.gerar_texto_a(), view=view_a
  )
  manager.msg_a = await interaction.original_response()

  sub_msg = await interaction.channel.send(
      manager.gerar_texto_b(), view=view_b
  )
  manager.msg_b = sub_msg
