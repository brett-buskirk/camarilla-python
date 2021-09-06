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
async def roll(ctx, s_dice='0', op='-h', h_dice='0'):
    """Rolls dice in N -h N format."""

    # Check for non-integer entries
    try:
        s_dice = int(s_dice)
        h_dice = int(h_dice)
    except Exception:
        await ctx.send('Format has to be either N or N -h N')
        return

    # Check for the correct flag
    if not op == '-h':
        await ctx.send('Format has to be either N or N -h N')
        return

    # Determine standard successes and critical successes
    standard_rolls = []
    success = 0
    critical = 0
    for i in range(s_dice):
        rand = random.randint(1, 10)
        standard_rolls.append(rand)
        if rand in range(6, 10):
            success += 1
        elif rand == 10:
            critical += 1

    # Determine the results of the hunger dice, if any
    hunger_rolls = []
    bestial_failure = False
    messy_critical = False
    for i in range(h_dice):
        rand = random.randint(1, 10)
        hunger_rolls.append(rand)
        if rand in range(6, 10):
            success += 1
        elif rand == 10:
            critical += 1
            messy_critical = True
        elif rand == 1:
            bestial_failure = True

    # Find double critical rolls (each pair of critical rolls = 4 successes)
    double_critical = (critical // 2) * 4

    # Left-over critical rolls
    leftover_critical = (critical % 2)

    # Tally the two
    critical_tally = double_critical + leftover_critical

    # Determine final successes
    final_success = success + critical_tally

    # Format embed to send to server
    embed = discord.Embed(
        title='Results',
        color=discord.Colour.dark_red()
    )
    embed.set_thumbnail(url="https://i.imgur.com/C0IhAEr.jpg")
    embed.add_field(name='Standard Dice', value=f'{s_dice} dice: {str(standard_rolls)}', inline=False)
    embed.add_field(name='Hunger Dice', value=f'{h_dice} dice: {str(hunger_rolls)}', inline=False)
    embed.add_field(name='Normal Successes', value=str(success), inline=True)
    embed.add_field(name='Critical Successes', value=str(critical), inline=True)
    embed.add_field(name='Total Successes', value=str(final_success), inline=False)
    embed.add_field(name='Messy Critical', value=str(messy_critical), inline=True)
    embed.add_field(name='Bestial Failure', value=str(bestial_failure), inline=True)

    # Send embed to server
    await ctx.send(embed=embed)


@bot.command(help="Retrieves information about specified clan.")
async def clan(ctx, clan=""):
    # Retrieve the clan collection
    collection_name = db['clans']

    # Make sure clan exists in collection
    try:
        details = collection_name.find_one({"name": clan.lower()})
        clan_name = details["name"]
    except Exception:
        await ctx.send("Sorry, cannot find that clan...")
        return

    # Create the embed to send to server
    embed = discord.Embed(
        title=f'{clan_name.upper()}: {details["title"]}',
        color=discord.Colour.dark_red()
    )
    embed.set_thumbnail(url=details["icon"])
    embed.add_field(name="Description", value=details["description"], inline=False)
    embed.add_field(name="Nicknames", value=", ".join(details["nicknames"]), inline=False)
    embed.add_field(name="Disciplines", value=", ".join(details["disciplines"]), inline=False)
    embed.add_field(name="Bane", value=details["bane"], inline=False)
    embed.set_footer(text=details["page"])

    # Send embed to server
    await ctx.send(embed=embed)


bot.run(TOKEN)
