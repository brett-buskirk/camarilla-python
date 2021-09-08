import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
import random
from db_connect import connect_db

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='.', intents=intents)
db = connect_db()


@bot.event
async def on_ready():
    print(f'Bot connected as {bot.user.name} {bot.user.id}')
    print('------------')


@bot.command(help='Rolls dice in N or N -h N format, where -h N are hunger dice.')
async def roll(ctx, s_dice: str = '0', op: str = '-h', h_dice: str = '0'):
    """Rolls dice in N -h N format."""
    from dice import dice_roll
    embed = dice_roll(s_dice, op, h_dice)
    await ctx.send(embed=embed)


@bot.command(help="Retrieves information about specified clan.")
async def clan(ctx, clan=""):
    """Returns the requested clan information"""
    from clans import clan_details
    embed = clan_details(clan, db)
    await ctx.send(embed=embed)


bot.run(TOKEN)
