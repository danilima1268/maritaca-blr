import os
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Dicionários de dados para gerir o estado do Blue Lock Rivals
player_stats = {}
active_matches = {}

@bot.event
async def on_ready():
    print(f"Bot ligado com sucesso como {bot.user}")

@bot.command(name="ping")
async def ping(ctx):
    await ctx.send("Pong! O bot está online e operacional.")

@bot.tree.command(name="escalacao", description="Define a escalação tática para o Blue Lock Rivals")
async def escalacao(interaction: discord.Interaction, atacante: str, meio: str, defesa: str):
    embed = discord.Embed(
        title="⚡ Nova Escalação Tática - Blue Lock Rivals",
        color=discord.Color.blue()
    )
    embed.add_field(name="Atacante (FW)", value=atacante, inline=False)
    embed.add_field(name="Meio-Campo (MF)", value=meio, inline=False)
    embed.add_field(name="Defesa (DF)", value=defesa, inline=False)
    embed.set_footer(text=f"Escalação criada por {interaction.user.name}")
    
    await interaction.response.send_message(embed=embed)

bot.run(os.getenv("DISCORD_TOKEN"))
