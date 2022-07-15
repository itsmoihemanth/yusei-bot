import discord, json, platform
from discord import Option
from discord.ext import commands
from helpers import checks, json_manager

with open("config.json") as file:
    config = json.load(file)

class General(commands.Cog, name="general-slash"):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="botinfo",
        description="Get some useful (or not) information about the bot.",
    )
    @checks.not_blacklisted()
    async def botinfo(self, interaction: discord.ApplicationContext) -> None:
        """
        Get some useful (or not) information about the bot.
        :param interaction: The application command interaction.
        """
        embed = discord.Embed(
            description="Made by reapur ™",
            colour=json_manager.get_color(str(interaction.guild.id))
        )
        embed.set_author(
            name="Bot Information"
        )
        embed.add_field(
            name="Owner:",
            value="<@440433975396401152>",
            inline=True
        )
        embed.add_field(
            name="Python Version:",
            value=f"{platform.python_version()}",
            inline=True
        )
        embed.add_field(
            name="Prefix:",
            value=f"/ (Slash Commands) or {config['prefix']} for normal commands",
            inline=False
        )
        embed.set_footer(
            text=f"Requested by {interaction.author}"
        )
        await interaction.respond(embed=embed)

    @commands.slash_command(
        name="serverinfo",
        description="Get some useful (or not) information about the server.",
    )
    @checks.not_blacklisted()
    async def serverinfo(self, interaction: discord.ApplicationContext) -> None:
        """
        Get some useful (or not) information about the server.
        :param interaction: The application command interaction.
        """
        roles = [role.name for role in interaction.guild.roles]
        if len(roles) > 50:
            roles = roles[:50]
            roles.append(f">>>> Displaying[50/{len(roles)}] Roles")
        roles = ", ".join(roles)

        embed = discord.Embed(
            title="**Server Name:**",
            description=f"{interaction.guild}",
            color=json_manager.get_color(str(interaction.guild.id))
        )
        embed.set_thumbnail(
            url=interaction.guild.icon.url if interaction.guild.icon else ""
        )
        embed.add_field(
            name="Server ID",
            value=interaction.guild.id
        )
        embed.add_field(
            name="Member Count",
            value=interaction.guild.member_count
        )
        embed.add_field(
            name="Text/Voice Channels",
            value=f"{len(interaction.guild.channels)}"
        )
        embed.add_field(
            name=f"Roles ({len(interaction.guild.roles)})",
            value=roles
        )
        embed.set_footer(
            text=f"Created at: {interaction.guild.created_at}"
        )
        await interaction.respond(embed=embed)

    @commands.slash_command(
        name="ping",
        description="Check if the bot is alive.",
    )
    @checks.not_blacklisted()
    async def ping(self, interaction: discord.ApplicationContext) -> None:
        """
        Check if the bot is alive.
        :param interaction: The application command interaction.
        """
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"The bot latency is {round(self.bot.latency * 1000)}ms.",
            color=json_manager.get_color(str(interaction.guild.id))
        )
        await interaction.respond(embed=embed)

    @commands.slash_command(
        name="invite",
        description="Get the invite link of the bot to be able to invite it.",
    )
    @checks.not_blacklisted()
    async def invite(self, interaction: discord.ApplicationContext) -> None:
        
        #Get the invite link of the bot to be able to invite it.
        #:param interaction: The application command interaction.
        
        embed = discord.Embed(
            description=f"Invite me by clicking [here](https://discordapp.com/oauth2/authorize?&client_id={config['application_id']}&scope=bot+applications.commands&permissions={config['permissions']}).",
            color=json_manager.get_color(str(interaction.guild.id))
        )
        try:
            # To know what permissions to give to your bot, please see here: https://discordapi.com/permissions.html and remember to not give Administrator permissions.
            await interaction.author.send(embed=embed)
            await interaction.respond("I sent you a private message!")
        except discord.Forbidden:
            await interaction.respond(embed=embed)

    @commands.slash_command(
        name="server",
        description="Get the invite link of the owners discord server.",
    )
    @checks.not_blacklisted()
    async def server(self, interaction: discord.ApplicationContext) -> None:
        #Get the invite link of the discord server of the bot for some support.
        #:param interaction: The application command interaction.
        embed = discord.Embed(
            description=f"Join my server by clicking [here](https://discord.gg/PgT5WVKGmG).",
            color=json_manager.get_color(str(interaction.guild.id))
        )
        try:
            await interaction.author.send(embed=embed)
            await interaction.respond("I sent you a private message!")
        except discord.Forbidden:
            await interaction.respond(embed=embed)


    @commands.slash_command(name='bug_report',                                                         
                 description="Bot bug reporting")

    async def bug_report(self, interaction: discord.ApplicationContext, 
                        description: Option(str, "Detail of what went wrong")):

        dm = await self.bot.fetch_user(440433975396401152)
        await dm.send(f"bug report from {interaction.author.mention} in {interaction.guild}:\n\n {description}")
        await interaction.respond(f"Thank you for the report {interaction.author.mention}, we will look into it")


    @commands.slash_command(name='suggest',                                                               
                 description="Suggest a new feature for the bot")

    async def suggest(self, interaction: discord.ApplicationContext, 
                    suggestion: Option(str, "What you want to suggest")):

        dm = await self.bot.fetch_user(440433975396401152)
        await dm.send(f"suggestion from {interaction.author.mention} in {interaction.guild}:\n\n {suggestion}")
        await interaction.respond(f"Thank you for the suggestion {interaction.author.mention}")


def setup(bot):
    bot.add_cog(General(bot))
     