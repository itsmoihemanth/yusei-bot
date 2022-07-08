import discord
from discord.ext import commands
from discord.ext.commands import Context
import platform

from helpers import checks


class General(commands.Cog, name="general-normal"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="botinfo",
        description="Get some useful (or not) information about the bot.",
    )
    @checks.not_blacklisted()
    async def botinfo(self, context: Context):
        """
        Get some useful (or not) information about the bot.
        :param context: The context in which the command has been executed.
        """
        embed = discord.Embed(
            description="Made by reapur ™",
            colour=14942490
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
            value=f"/ (Slash Commands) or ** for normal commands",
            inline=False
        )
        embed.set_footer(
            text=f"Requested by {context.author}"
        )
        await context.send(embed=embed)

    @commands.command(
        name="serverinfo",
        description="Get some useful (or not) information about the server.",
    )
    @checks.not_blacklisted()
    async def serverinfo(self, context: Context):
        """
        Get some useful (or not) information about the server.
        :param context: The context in which the command has been executed.
        """
        roles = [role.name for role in context.guild.roles]
        if len(roles) > 50:
            roles = roles[:50]
            roles.append(f">>>> Displaying[50/{len(roles)}] Roles")
        roles = ", ".join(roles)

        embed = discord.Embed(
            title="**Server Name:**",
            description=f"{context.guild}",
            colour=14942490
        )
        embed.set_thumbnail(
            url=context.guild.icon.url
        )
        embed.add_field(
            name="Server ID",
            value=context.guild.id
        )
        embed.add_field(
            name="Member Count",
            value=context.guild.member_count
        )
        embed.add_field(
            name="Text/Voice Channels",
            value=f"{len(context.guild.channels)}"
        )
        embed.add_field(
            name=f"Roles ({len(context.guild.roles)})",
            value=roles
        )
        embed.set_footer(
            text=f"Created at: {context.guild.created_at}"
        )
        await context.send(embed=embed)

    @commands.command(
        name="ping",
        description="Check if the bot is alive.",
    )
    @checks.not_blacklisted()
    async def ping(self, context: Context):
        """
        Check if the bot is alive.
        :param context: The context in which the command has been executed.
        """
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"The bot latency is {round(self.bot.latency * 1000)}ms.",
            colour=14942490
        )
        await context.send(embed=embed)

    # @commands.command(
        # name="invite",
        # description="Get the invite link of the bot to be able to invite it.",
    # )
    # @checks.not_blacklisted()
    # async def invite(self, context: Context) -> None:
        # """
        # Get the invite link of the bot to be able to invite it.
        # :param context: The context in which the command has been executed.
        # """
        # embed = discord.Embed(
            # description=f"Invite me by clicking [here](https://discordapp.com/oauth2/authorize?&client_id={config['application_id']}&scope=bot+applications.commands&permissions={config['permissions']}).",
            # color=0xD75BF4
        # )
        # try:
            # To know what permissions to give to your bot, please see here: https://discordapi.com/permissions.html and remember to not give Administrator permissions.
            # await context.author.send(embed=embed)
            # await context.send("I sent you a private message!")
        # except discord.Forbidden:
            # await context.send(embed=embed)

    # @commands.command(
        # name="server",
        # description="Get the invite link of the discord server of the bot for some support.",
    # )
    # @checks.not_blacklisted()
    # async def server(self, context: Context) -> None:
        # """
        # Get the invite link of the discord server of the bot for some support.
        # :param context: The context in which the command has been executed.
        # """
        # embed = discord.Embed(
            # description=f"Join the support server for the bot by clicking [here](https://discord.gg/).",
            # color=0xD75BF4
        # )
        # try:
            # await context.author.send(embed=embed)
            # await context.send("I sent you a private message!")
        # except discord.Forbidden:
            # await context.send(embed=embed)


def setup(bot):
    bot.add_cog(General(bot))
