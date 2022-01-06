import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from db_connect import connect_db

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='.', intents=intents, case_insensitive=True)
db = connect_db()
client = discord.Client()

@bot.event
async def on_ready():
    print(f'Bot connected as {bot.user.name} {bot.user.id}')
    print('------------')


@bot.command(help='Rolls dice in N or N -h N format, where -h N are hunger dice.')
async def roll(ctx, s_dice='0', op='-h', h_dice='0'):
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


@bot.command(help="Retrieves information about specific discipline.")
async def discipline(ctx, discipline=""):
    """Returns the requested discipline information"""
    from disciplines import discipline_details
    embed = discipline_details(discipline, db)
    await ctx.send(embed=embed)


@bot.command(help="Retrieves information about specific Animalism power.")
async def animalism(ctx, power=""):
    """Returns the requested power information"""
    from disciplines import discipline_power
    embed = discipline_power("animalism", power.lower(), db)
    await ctx.send(embed=embed)


@bot.command(help="Retrieves a specified rule or list.")
async def lookup(ctx, rule=""):
    """Returns the requested list"""
    if rule == 'clans':
        from clans import clans_list
        embed = clans_list(db)
    elif rule == 'disciplines':
        from disciplines import discipline_list
        embed = discipline_list(db)
    else:
        embed = discord.Embed(
            title=f'Cannot find {rule}',
            color=discord.Colour.dark_red()
        )

    await ctx.send(embed=embed)


@bot.command(help="Creates a scene break.")
async def br(ctx, kind="scene"):
    """Returns a scene break to control the flow of action"""
    await ctx.send(f'```\n {kind.upper()} BREAK \n```')
    

@bot.command(help="Displays a welcome message.")
async def welcome(ctx):
  """Returns a welcome message"""
  await ctx.send('Hello and welcome from Camarilla!')


@bot.event
async def on_message(message):
    """Delete commands from the channel"""
    if message.content and message.content[0] == '.':
        await bot.process_commands(message)
        await message.delete()


bot.run(TOKEN)
