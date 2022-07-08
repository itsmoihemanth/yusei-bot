import discord,json

class embeds():
    def build_embed(guild_id,description,title=""):
        with open("guild.json") as file:
            guild = json.load(file)

        embed = discord.Embed(title=title,
                                description=description,
                                color=guild[str(guild_id)]["color"])

        return embed