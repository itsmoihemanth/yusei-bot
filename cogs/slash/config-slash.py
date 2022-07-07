import discord
import json
from discord.ext import pages
from discord.ext import commands
from discord.commands import Option, SlashCommandGroup
from helpers import checks, views

class Config(commands.Cog, name="config-slash"):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.slash_command( 
        name="setup",
        description="Setup the bot"
    )
    @checks.not_blacklisted()
    async def setup(self, interaction: discord.ApplicationContext):
        view = views.Modules_View()
        await interaction.respond("Which module would you like to setup first?",view=view)

        await view.wait()
        if view.value is None:
            print("Timed out...")
        elif view.value == "birthday":
            print("birthday module")
        elif view.value == "quotes":
            print("quotes module")

        await interaction.respond(view.value)
        
    config = SlashCommandGroup("config", "config related commands")

    @config.command(
        name="color",
        description="Config the embed color module"
        )
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @checks.not_blacklisted()
    @commands.has_permissions(administrator=True)
    async def config_color(self, interaction: discord.ApplicationContext, 
                            color_hex: Option(str, "The Hex color for embeds to use", required = True)):
         
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
