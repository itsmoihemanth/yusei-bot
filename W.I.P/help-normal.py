import discord
from discord.ext import commands
from discord.ext.commands import Context

from helpers import checks

class Help(commands.Cog, name="help-normal"):
    def __init__(self, bot):
        self.bot = bot

    # @commands.group(
        # name="help"
    # )
    # async def blacklist(self, context: Context):
        
        
        
    @commands.command(name="helpme", description="Returns all commands available")
    @checks.not_blacklisted()
    async def helpme(self, context: Context,):
        counter = 0
        for command in self.bot.commands:
            counter += 1
        

        response = """
        My current prefix in this server is ** Type **help <command name> to get information about a specific command.
        You can also use slash commands """
        embed = discord.Embed(description=response,colour=14942490) 
        
        #`coinflip`   Make a coin flip, but give your bet before.
        #`rps`        Play the rock paper scissors game against the bot."""

        fun = """`8ball`      Ask any question to the bot.
        `randomfact` Get a random fact."""
        
        general ="""`botinfo`    Get some useful (or not) information about the bot.
          `ping`       Check if the bot is alive.
          `serverinfo` Get some useful (or not) information about the server."""

        
        moderation ="""`ban`        Bans a user from the server.
          `hackban`    Bans a user without the user having to be in the server.
          `kick`       Kick a user out of the server.
          `nick`       Change the nickname of a user on a server.
          `warn`       Warns a user in his private messages."""
          
        
        quotes="""`add`        Add new quotes
          `view`       Replies with the list of quotes"""
              

       
        embed.add_field(
            name="fun:",
            value=fun,
            inline=False
        )
        
        embed.add_field(
            name="general:",
            value=general,
            inline=False
        )
        
        embed.add_field(
            name="moderation:",
            value=moderation,
            inline=False
        )
        
        embed.add_field(
            name="quotes:",
            value=quotes,
            inline=False
        )
        
        embed.add_field(
            name="help",
            value="Shows this message",
            inline=False
        )

        embed.set_author(name="Jackbot Commands")
        if context.guild.icon != None:
            embed.set_thumbnail(url=context.guild.icon.url)
        embed.set_footer(text="Type **help command for more info on a command.")
        
        await context.send(embed=embed)

def setup(bot):
    bot.add_cog(Help(bot))