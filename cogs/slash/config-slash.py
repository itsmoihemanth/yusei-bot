import discord
import json
from discord.ext import pages
from discord.ext import commands
from discord.commands import Option, SlashCommandGroup
from helpers import checks, db_api


class Config(commands.Cog, name="quotes-slash"):
    def __init__(self, bot):
        self.bot = bot
    
    config = SlashCommandGroup("config", "config related commands")

    @quotes.command(
        name="quotes",
        description="Config the quotes module"
        )
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @checks.not_blacklisted()
    async def config_quotes(self, interaction: discord.ApplicationContext, 
                            sfw_channel: Option(discord.TextChannel, "Set the quotes channel", required=True),
                            nsfw_channel: Option(discord.TextChannel, "Set the nsfw quotes channel", default=None)):


        with open("guild.json") as file:
            guild = json.load(file)

        if str(interaction.guild.id) in guild:
            guild[str(interaction.guild.id)]["sfw"]=sfw_channel.id
            response = f"Quotes channel set to <#{sfw_channel.id}> for sfw quotes\n"

            if nsfw_channel!=None:
                guild[str(interaction.guild.id)]["nsfw"]=nsfw_channel.id
                response = response + f" Quotes channel set to <#{nsfw_channel.id}> for nsfw quotes"
        else:
            guild[f"{interaction.guild.id}"]={"name":f"{interaction.guild.name}","sfw":sfw_channel.id,"nsfw":nsfw_channel.id if nsfw_channel else None}
            response = f"Quotes channel set to <#{sfw_channel.id}> for sfw quotes"
            if nsfw_channel:
                response = response + f" and <#{nsfw_channel.id}> for nsfw quotes"

        with open("guild.json", "w") as p:
            json.dump(guild, p,indent=6)

        await interaction.respond(response,ephemeral=True)
         
   @quotes.command(
        name="color",
        description="Config the embed color module"
        )
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @checks.not_blacklisted()
    async def config_color(self, interaction: discord.ApplicationContext, 
                            color: 

def setup(bot):
    bot.add_cog(Quotes(bot))
