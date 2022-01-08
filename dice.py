import discord
import random


def error_embed():
    """Error message detailing the format requrired"""

    embed = discord.Embed(
        title='Format has to be either N or N -h N',
        color=discord.Colour.dark_red()
    )
    embed.add_field(
        name="Notes",
        value="The first N is for standard dice; the second N is for hunger level.",
        inline=False
    )
    embed.add_field(
        name="Standard Dice",
        value="The number of standard dice must be greater than 0.",
        inline=False
    )
    embed.add_field(
        name="Hunger Dice",
        value="The level of hunger must be between 0 and 5.",
        inline=False
    )
    return embed


def dice_roll(s_dice, op, h_dice):
    """Rolls dice in N -h N format"""

    # Check for non-integer entries
    try:
        s_dice = int(s_dice)
        h_dice = int(h_dice)
    except ValueError:
        return error_embed()

    # Check to make sure a positive number is entered for s_dice
    if s_dice <= 0:
        return error_embed()

    # Check to make sure the hunger level is between 0 and 5
    if h_dice < 0 or h_dice > 5:
        return error_embed()

    # Check for the correct flag
    if not op == '-h':
        return error_embed()

    # Determine standard successes and critical successes
    standard_rolls = []
    success = 0
    critical = 0
    
    # Calculate dice totals
    if s_dice > h_dice:
        s_dice = s_dice - h_dice
        h_dice = h_dice
    elif s_dice < h_dice:
        h_dice = s_dice
        s_dice = 0
    else:
        s_dice = 0
        h_dice = h_dice
    
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

    # Return the embed
    return embed