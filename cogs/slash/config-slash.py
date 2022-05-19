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

        embed = discord.Embed(title="Server Configuration", color=guild[str(interaction.guild.id)]["color"])
        embed.set_author(name="yusei", icon_url="https://cdn.discordapp.com/avatars/974218172054007809/935d0b2037631baaa14b434f65f4cde2.webp")
        embed.add_field(name="__**Sfw Quotes Channel**__", value=f"<#{guild[str(interaction.guild.id)]['sfw']}>" if guild[str(interaction.guild.id)]['sfw'] else "Not set")
        embed.add_field(name="__**Nsfw Quotes Channel**__", value=f"<#{guild[str(interaction.guild.id)]['nsfw']}>" if guild[str(interaction.guild.id)]['nsfw'] else "Not set")
        embed.add_field(name="__**Birthday Channel**__", value=f"<#{guild[str(interaction.guild.id)]['birthday']}>" if guild[str(interaction.guild.id)]['birthday'] else "Not set")
        embed.add_field(name="__**Embed Color**__", value=f"#{hex(guild[str(interaction.guild.id)]['color']).lstrip('0x')}", inline=True)
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
        
        
        color = color_hex.strip()
        color = color.lstrip('#')
        color = int(color,16)
        
        with open("guild.json") as file:
            guild = json.load(file)

        guild[str(interaction.guild.id)]['color'] = color

        with open("guild.json", "w") as p:
            json.dump(guild, p,indent=6)

        await interaction.respond(f"The Color for embeds has been set to {color_hex}",ephemeral=True)

def setup(bot):
    bot.add_cog(Config(bot))
