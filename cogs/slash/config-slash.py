import discord, json
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

    @config.command(
    name="quotes",
    description="config quotes module"
    )
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @checks.not_blacklisted()
    async def config_quotes(self, interaction: discord.ApplicationContext,
                            disable : Option(str,description="Turn disable/enable the quotes commands",choices=["True","False"],required=False),
                            sfw_channel: Option(discord.TextChannel, "Set the sfw quotes channel",required=False),
                            nsfw_channel: Option(discord.TextChannel, "Set the nsfw quotes channel",required=False)):

        with open("guild.json") as file:
            guild = json.load(file)
            
        server = guild[str(interaction.guild.id)]
        
        response = ""
        if (disable and disable=='False') or server["quotes"]["enabled"] == True and (sfw_channel or nsfw_channel):
            if "quotes" not in server:
                server["quotes"]={}
                server["quotes"]["enabled"] = True
                
                response = response + "> **quotes commands have been enabled**\n\n"
                
            if server["quotes"]["enabled"] == False:
                server["quotes"]["enabled"] = True
                response = response + "> **quotes commands have been re-enabled**\n\n"

            if sfw_channel:
                server["quotes"]["channel"] = sfw_channel.id
                response = response + f"> **quotes Channel has been set to <#{sfw_channel.id}>**\n\n"

            if nsfw_channel:
                server["quotes"]["channel"] = nsfw_channel.id
                response = response + f"> **quotes Channel has been set to <#{nsfw_channel.id}>**\n\n"
                
        elif disable and disable == 'True':
            if "quotes" in server:
                server["quotes"]["enabled"] = False
                response = response + "> **quotes commands have been disabled**\n\n"
        
        elif server["quotes"]["enabled"] == False:
            response = "> **Quotes Module is disabled, re-enable it first to make changes to config**"

        with open("guild.json", "w") as p:
            json.dump(guild, p,indent=6)

        if response=="":
            response="> **No changes were made to config**"
        await interaction.respond(embed=discord.Embed(description=response, color=guild[str(interaction.guild.id)]["color"]))


    @config.command(
    name="birthday",
    description="config birthday module"
    )
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @checks.not_blacklisted()
    async def config_bday(self, interaction: discord.ApplicationContext,
                            disable : Option(str,description="Turn disable/enable the birthday commands",choices=["True","False"],required=False),
                            channel: Option(discord.TextChannel, "Set the birthday channel",required=False),
                            message: Option(str, "Set the birthday message. {user},{user.mention},{server}",required=False),
                            mention: Option(str, "Set the role to ping. {user.mention} or @role",required=False),
                            role: Option(discord.Role, "Set the role to assign to birthday user.",required=False)):

        with open("guild.json") as file:
            guild = json.load(file)
            
        server = guild[str(interaction.guild.id)]

        response = ""
        if (disable and disable=='False') or server["birthday"]["enabled"] == True and (channel or message or role or mention):
            if (disable and disable=='False'):
                if "birthday" not in server:
                    server["birthday"]={}
                    server["birthday"]["enabled"] = True
                
                    response = response + "> **Birthday commands have been enabled**\n\n"
                
                if server["birthday"]["enabled"] == False:
                    server["birthday"]["enabled"] = True
                    response = response + "> **Birthday commands have been re-enabled**\n\n"

                if channel:
                    server["birthday"]["channel"] = channel.id
                    response = response + f"> **Birthday Channel has been set to <#{channel.id}>**\n\n"

                if message:
                    server["birthday"]["message"] = message
                    response = response + f"> **Birthday Message has been set to `{message}`**\n\n"

                if mention:
                    server["birthday"]["mention"] = mention
                    response = response + f"> **mention has been set to `{mention}`**\n\n"

                if role:
                    server["birthday"]["role"] = role.id
                    response = response + f"> **Birthday Role has been set to <@&{role.id}>**\n\n"

        if disable and disable == 'True':
            if "birthday" in server:
                server["birthday"]["enabled"] = False
                response = response + "> **Birthday commands have been disabled**\n\n"

        if server["birthday"]["enabled"] == False:
            response = "> **birthday Module is disabled, re-enable it first to make changes to config**"

        with open("guild.json", "w") as p:
            json.dump(guild, p,indent=6)

        if response=="":
            response="No changes were made"
        await interaction.respond(embed=discord.Embed(description=response, color=guild[str(interaction.guild.id)]["color"]))


def setup(bot):
    bot.add_cog(Config(bot))
