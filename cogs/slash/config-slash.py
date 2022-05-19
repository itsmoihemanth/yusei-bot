import discord
import json
from discord.ext import pages
from discord.ext import commands
from discord.commands import Option, SlashCommandGroup
from helpers import checks, db_api


<<<<<<< HEAD
class Config(commands.Cog, name="config-slash"):
=======
class Config(commands.Cog, name="quotes-slash"):
>>>>>>> db4dee1dc97a935820133c731344b21f18e1c29d
    def __init__(self, bot):
        self.bot = bot
    
    config = SlashCommandGroup("config", "config related commands")

<<<<<<< HEAD
    @config.command(
        name="channels",
=======
    @quotes.command(
        name="quotes",
>>>>>>> db4dee1dc97a935820133c731344b21f18e1c29d
        description="Config the quotes module"
        )
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @checks.not_blacklisted()
<<<<<<< HEAD
    @commands.has_permissions(administrator=True)
    async def config_quotes(self, interaction: discord.ApplicationContext, 
                            sfw_channel: Option(discord.TextChannel, "Set the quotes channel", default=None),
                            nsfw_channel: Option(discord.TextChannel, "Set the nsfw quotes channel", default=None),
                            birthday_channel: Option(discord.TextChannel, "Set the birthday channel", default=None)):

        
        response = ""
=======
    async def config_quotes(self, interaction: discord.ApplicationContext, 
                            sfw_channel: Option(discord.TextChannel, "Set the quotes channel", required=True),
                            nsfw_channel: Option(discord.TextChannel, "Set the nsfw quotes channel", default=None)):

>>>>>>> db4dee1dc97a935820133c731344b21f18e1c29d

        with open("guild.json") as file:
            guild = json.load(file)

<<<<<<< HEAD
        if sfw_channel!=None:
            guild[str(interaction.guild.id)]["sfw"]=sfw_channel.id

        if nsfw_channel!=None:
            guild[str(interaction.guild.id)]["nsfw"]=nsfw_channel.id
            
        if birthday_channel!=None:
            guild[str(interaction.guild.id)]["birthday"]=birthday_channel.id
=======
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
>>>>>>> db4dee1dc97a935820133c731344b21f18e1c29d

        with open("guild.json", "w") as p:
            json.dump(guild, p,indent=6)

<<<<<<< HEAD
        embed = discord.Embed(description=response, color=guild[str(interaction.guild.id)]["color"])

        await interaction.respond(embed=embed)

    @config.command(
=======
        await interaction.respond(response,ephemeral=True)
         
   @quotes.command(
>>>>>>> db4dee1dc97a935820133c731344b21f18e1c29d
        name="color",
        description="Config the embed color module"
        )
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @checks.not_blacklisted()
<<<<<<< HEAD
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
=======
    async def config_color(self, interaction: discord.ApplicationContext, 
                            color: 

def setup(bot):
    bot.add_cog(Quotes(bot))
>>>>>>> db4dee1dc97a935820133c731344b21f18e1c29d
