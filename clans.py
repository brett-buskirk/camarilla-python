import discord


def clan_details(clan, db):
    # Retrieve the clan collection
    collection_name = db['clans']

    # Make sure clan exists in collection
    try:
        details = collection_name.find_one({"name": clan.lower()})
        clan_name = details["name"]
    except Exception:
        embed = discord.Embed(
            title=f'Sorry, cannot find clan {clan}',
            color=discord.Colour.dark_red()
        )
        return embed

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

    return embed
