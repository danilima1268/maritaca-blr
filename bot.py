import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Dicionários de dados para gerir o estado do Blue Lock Rivals
escalacoes = {}
rankings = {}

@bot.event
async def on_ready():
    print(f"Bot {bot.user} está online e pronto para o Blue Lock Rivals!")
    try:
        synced = await bot.tree.sync()
        print(f"Comandos sincronizados: {len(synced)}")
    except Exception as e:
        print(e)

# --- Comando /escalacao ---
@bot.tree.command(name="escalacao", description="Gere a tua escalação do Blue Lock Rivals")
async def escalacao(interaction: discord..Interaction, atacante: str, meio: str, defesa: str):
    user_id = interaction.user.id
    escalacoes[user_id] = {"atacante": atacante, "meio": meio, "defesa": defesa}
    
    embed = discord.Embed(
        title="⚽ Escalação Atualizada - Blue Lock Rivals",
        color=discord.Color.blue()
    )
    embed.add_field(name="Atacante", value=atacante, inline=False)
    embed.add_field(name="Meio-campista", value=meio, inline=False)
    embed.add_field(name="Defensor", value=defesa, inline=False)
    embed.set_footer(text=f"Escalação criada por {interaction.user.name}", icon_url=interaction.user.display_avatar.url)
    
    await interaction.response.send_message(embed=embed)

# --- Comando /criar_rank ---
@bot.tree.command(name="criar_rank", description="Mostra o ranking administrativo com o avatar do utilizador")
async def criar_rank(interaction: discord.Interaction, membro: discord.Member, posicao: int, pontos: int):
    embed = discord.Embed(
        title="🏆 Ranking Oficial - Blue Lock Rivals",
        color=discord.Color.gold()
    )
    embed.set_thumbnail(url=membro.display_avatar.url)
    embed.add_field(name="Jogador", value=membro.mention, inline=False)
    embed.add_field(name="Posição", value=f"#{posicao}", inline=True)
    embed.add_field(name="Pontos", value=f"{pontos} pts", inline=True)
    
    await interaction.response.send_message(embed=embed)

# --- View interativa para o Duelo /x1 ---
class X1View(discord.ui.View):
    def __init__(self, desafiado: discord.Member):
        super().__init__(timeout=60)
        self.desafiado = desafiado

    @discord.ui.button(label="Aceitar Duelo", style=discord.ButtonStyle.green)
    async def aceitar(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.desafiado:
            await interaction.response.send_message("Não podes aceitar um duelo que não é para ti!", ephemeral=True)
            return
        
        for child in self.children:
            child.disabled = True
            
        await interaction.response.edit_message(content=f"⚔️ **Duelo Aceite!** {interaction.user.mention} aceitou o desafio de 1v1!", view=self)
        self.stop()

    @discord.ui.button(label="Recusar", style=discord.ButtonStyle.red)
    async def recusar(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.desafiado:
            await interaction.response.send_message("Não podes recusar um duelo que não é para ti!", ephemeral=True)
            return
            
        for child in self.children:
            child.disabled = True
            
        await interaction.response.edit_message(content=f"❌ O duelo foi recusado por {interaction.user.mention}.", view=self)
        self.stop()

# --- Comando /x1 ---
@bot.tree.command(name="x1", description="Desafia outro jogador para um 1v1 no Blue Lock Rivals")
async def x1(interaction: discord.Interaction, oponente: discord.Member):
    if oponente == interaction.user:
        await interaction.response.send_message("Não podes desafiar a ti mesmo!", ephemeral=True)
        return
        
    if oponente.bot:
        await interaction.response.send_message("Não podes desafiar um bot!", ephemeral=True)
        return

    view = X1View(desafiado=oponente)
    embed = discord.Embed(
        title="⚔️ Novo Desafio de 1v1 (Blue Lock Rivals)",
        description=f"{interaction.user.mention} desafiou {oponente.mention} para um duelo eletrizante!",
        color=discord.Color.red()
    )
    
    await interaction.response.send_message(content=oponente.mention, embed=embed, view=view)

# Substitui pelo teu token ou usa variável de ambiente
bot.run("O_TEU_TOKEN_AQUI")
