import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
import random

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='.', intents=intents)


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
    messy_crit = False
    for i in range(h_dice):
        rand = random.randint(1, 10)
        hunger_rolls.append(rand)
        if rand in range(6, 10):
            success += 1
        elif rand == 10:
            critical += 1
            messy_crit = True
        elif rand == 1:
            bestial_failure = True

    # Find double crits (each pair of crits = 4 successes)
    double_crit = (critical // 2) * 4

    # Left-over crits
    leftover_crit = (critical % 2)

    # Tally the two
    crit_tally = double_crit + leftover_crit

    # Determine final successes
    final_success = success + crit_tally

    embed = discord.Embed(
        title='Results',
        color=discord.Colour.dark_red()
    )

    embed.add_field(name='Standard Dice', value=f'{s_dice} dice: {str(standard_rolls)}', inline=False)
    embed.add_field(name='Hunger Dice', value=f'{h_dice} dice: {str(hunger_rolls)}', inline=False)
    embed.add_field(name='Normal Successes', value=str(success), inline=True)
    embed.add_field(name='Critical Successes', value=str(critical), inline=True)
    embed.add_field(name='Total Successes', value=str(final_success), inline=False)
    embed.add_field(name='Messy Critical', value=str(messy_crit), inline=True)
    embed.add_field(name='Bestial Failure', value=str(bestial_failure), inline=True)

    await ctx.send(embed=embed)
bot.run(TOKEN)
