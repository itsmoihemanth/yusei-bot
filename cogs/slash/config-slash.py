import discord
import json
from discord.ext import pages
from discord.ext import commands
from discord.commands import Option, SlashCommandGroup
from helpers import checks, db_api


class Config(commands.Cog, name="config-slash"):
    def __init__(self, bot):
        self.bot = bot
    
    config = SlashCommandGroup("config", "config related commands")

    @config.command(
        name="channels",
        description="Config the quotes module"
        )
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @checks.not_blacklisted()
    @commands.has_permissions(administrator=True)
    async def config_quotes(self, interaction: discord.ApplicationContext, 
                            sfw_channel: Option(discord.TextChannel, "Set the quotes channel", default=None),
                            nsfw_channel: Option(discord.TextChannel, "Set the nsfw quotes channel", default=None),
                            birthday_channel: Option(discord.TextChannel, "Set the birthday channel", default=None)):

        
        response = ""

        with open("guild.json") as file:
            guild = json.load(file)

        if sfw_channel!=None:
            guild[str(interaction.guild.id)]["sfw"]=sfw_channel.id

        if nsfw_channel!=None:
            guild[str(interaction.guild.id)]["nsfw"]=nsfw_channel.id
            
        if birthday_channel!=None:
            guild[str(interaction.guild.id)]["birthday"]=birthday_channel.id

        with open("guild.json", "w") as p:
            json.dump(guild, p,indent=6)

        embed = discord.Embed(description=response, color=guild[str(interaction.guild.id)]["color"])

        await interaction.respond(embed=embed)

    @config.command(
        name="color",
        description="Config the embed color module"
        )
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @checks.not_blacklisted()
    @commands.has_permissions(administrator=True)
    async def config_color(self, interaction: discord.ApplicationContext, 
                            color_hex: Option(str, "The Hex color for embeds to use", required = False)):
        
        with open("guild.json") as file:
            guild = json.load(file)

        color = color_hex.strip()
        color = color.lstrip('#')
        color = int(color,16)
        
        guild[f"{interaction.guild.id}"]['color'] = color

        with open("guild.json", "w") as p:
            json.dump(guild, p,indent=6)

        await interaction.respond(f"The Color for embeds has been set to {color_hex}",ephemeral=True)

def setup(bot):
    bot.add_cog(Config(bot))
