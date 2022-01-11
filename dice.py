import discord
import random


def error_embed(error_type, detail=""):
    """Error message detailing the format requrired"""

    embed = discord.Embed(
        title='Input Error',
        color=discord.Colour.dark_red()
    )
    # Error for something other than a positive number listed as the dice pool
    if error_type == 'dice_pool_error':
        embed.add_field(
            name="Dice Pool Error",
            value=f"{detail} is not a positive integer. The value immediately following .roll must be a positive integer.",
            inline=False
        )
    # Error for having the incorrect number of arguments
    if error_type == 'arg_length':
        embed.add_field(
            name="Incorrect Number of Arguments",
            value="The command must be formatted as .roll <num> -h <num> -d <num>",
            inline=False
        )
        embed.add_field(
            name="Note",
            value="The -h <num> and -d <num> arguments are optional and can be in any order",
            inline=False
        )
    # Error message for unacceptable flag
    if error_type == 'unacceptable_flag':
        embed.add_field(
            name="Unacceptable Flag",
            value=f"{detail} is an unacceptable flag. Please use either -h or -d.",
            inline=False
        )
    # Error message for a non-positive integer value
    if error_type == 'not_a_digit':
        embed.add_field(
            name="Positive Integer Required",
            value=f"{detail} is not a positive integer. This flag requires a positive integer.",
            inline=False
        )
    # Error message for hunger value being out of range
    if error_type == 'hunger_value':
        embed.add_field(
            name="Hunger Value Out of Range",
            value="The hunger value must be a number between 0 and 5.",
            inline=False
        )
        
    embed.set_footer(text='For help with commands, type .help')
    return embed


def dice_roll(dice_pool, *args):
    
    # Check for non-integer dice_pool entries
    if not dice_pool.isdigit():
        return error_embed('dice_pool_error', dice_pool)
    else:
        dice_pool = int(dice_pool)
    
    # Check to see if additional arguments are evenly divisible by two
    if (len(args) % 2 != 0):
        return error_embed('arg_length')

    # List of acceptable input flags
    acceptable_flags = ['-h', '-d']
    
    # Create a tuple of flag tuples, i.e. (('-h', '2'), ('-d', '3'))
    flags = tuple(args[x:x + 2] for x in range(0, len(args), 2))
    
    # Create variables
    hunger = 0
    difficulty = 1
    standard_rolls = []
    hunger_rolls = []
    success = 0
    critical = 0
    standard_dice = 0
    hunger_dice = 0
    margin = 'N/A'

    
    # Check for appropriate flags and values, and assign variables
    for flag in flags:
        if flag[0] not in acceptable_flags:
            return error_embed('unacceptable_flag', flag[0])
        if not flag[1].isdigit():
            return error_embed('not_a_digit', flag[1])
        # Check to make sure hunger is between 0 and 5
        if flag[0] == '-h' and int(flag[1]) > 5:
            return error_embed('hunger_value')
        if flag[0] == '-h':
            hunger = int(flag[1])
        if flag[0] == '-d':
            difficulty = int(flag[1])

    # Calculate dice totals
    if dice_pool > hunger:
        standard_dice = dice_pool - hunger
        hunger_dice = hunger
    if dice_pool < hunger:
        hunger_dice = dice_pool
    if dice_pool == hunger:
        hunger_dice = hunger
    
    # Determine the rolls for standard dice
    for i in range(standard_dice):
        rand = random.randint(1, 10)
        standard_rolls.append(rand)
        if rand in range(6, 10):
            success += 1
        elif rand == 10:
            critical += 1
    
    # Determine the rolls of the hunger dice
    bestial_failure = False
    messy_critical = False
    for i in range(hunger_dice):
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
    
    # Determine the result
    if final_success >= difficulty:
        if messy_critical and double_critical > 0:
            results = 'Messy Critical!'
        elif not messy_critical and double_critical > 0:
            results = 'Critical Win!'
        else:
            results = 'Win!'
        margin = final_success - difficulty
    else:
        if final_success == 0 and bestial_failure:
            results = 'Total Bestial Failure!'
        elif final_success == 0 and not bestial_failure:
            results = 'Total Failure!'
        elif final_success > 0 and bestial_failure:
            results = 'Bestial Failure!'
        else:
            results = 'Fail!'
    
    #Format rolls for output
    f_standard = ", ".join([str(int) for int in standard_rolls]) if len(standard_rolls) > 0 else "None"
    f_hunger = ", ".join([str(int) for int in hunger_rolls]) if len(hunger_rolls) > 0 else "None"
    
    # Format embed to send to server
    embed = discord.Embed(
        title='Results',
        color=discord.Colour.dark_red()
    )
    embed.set_thumbnail(url="https://i.imgur.com/C0IhAEr.jpg")
    embed.add_field(name=f'Factors', value=f'Pool: {dice_pool} | Hunger: {hunger} | Difficulty: {difficulty}', inline=False)
    embed.add_field(name='Standard Dice', value=f'{f_standard}', inline=False)
    embed.add_field(name='Hunger Dice', value=f'{f_hunger}', inline=False)
    embed.add_field(name='Successes', value=str(final_success), inline=True)
    embed.add_field(name='Margin', value=f'{margin}', inline=True)
    embed.add_field(name='Outcome', value=f'{results}', inline=False)


    # Return the embed
    return embed