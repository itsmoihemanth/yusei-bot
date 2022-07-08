import discord

class embeds():
    def build_embed(description,title=""):
        with open("guild.json") as file:
            guild = json.load(file)

        embed = discord.Embed(title=title,
                                    description=description,
                                    color=guild[str(interaction.guild.id)]["color"])