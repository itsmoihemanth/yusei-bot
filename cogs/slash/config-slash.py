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
        view1 = views.Modules_View()
        view2 = views.Channels_View()
        await interaction.respond("Which module would you like to setup first?",view=view1)

        '''await view1.wait()
        if view1.value is None:
            await interaction.send("You took too long to respond")
            return
        elif view1.value == "birthday":
             await interaction.send("Would you like to create a new channel or select an existing channel",view=view2)
        elif view1.value == "quotes":
            await interaction.send("Would you like to create a new channel or select an existing channel",view=view2)

        await view2.wait()
        if view2.value is None:
            await interaction.respond("You took too long to respond")
            return
        elif view2.value == "new":
            await interaction.send("New Channel created")
        elif view2.value == "existing":
            await interaction.send("type which channel you want")
        elif view2.value == False:
            await interaction.send("Setup cancelled")'''

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
         
        try:
            color = color_hex.strip()
            color = color.lstrip('#')
            color = int(color,16)
        except:
            await interaction.respond(f"Enter a valid color",ephemeral=True)
            return

        with open("guild.json") as file:
            guild = json.load(file)

        guild[str(interaction.guild.id)]['color'] = color

        with open("guild.json", "w") as p:
            json.dump(guild, p,indent=6)

        await interaction.respond(f"The Color for embeds has been set to {color_hex}",ephemeral=True)

def setup(bot):
    bot.add_cog(Config(bot))
