import discord
import json
from discord.ext import commands
from discord.ext.commands import Context

from helpers import checks

class Quotes(commands.Cog, name="quotes-normal"):
    def __init__(self, bot):
        self.bot = bot
               
    @commands.group(
        name="quotes",
        invoke_without_command=True
        )
    @checks.not_blacklisted()
    async def quotes(self, context: Context):
        embed=discord.Embed(title="__**Quote command work:**__", color=0xe0a8cf)
        embed.add_field(name="__Add subcommand__", value="Use this to add new quotes into the system, If you try to add stuff that already exists, I bonk you. This is how you use the command, \n\n**quotes add <quote> <name> \n\n You can also now react with ⭐ to a message to add it", inline=False)
        embed.add_field(name="\n__View subcommand__", value="Use to view quotes of everyone or a specific person it will show you a list of quotes by the person.\n You can now add multiple names with a ,\n\n**quotes view  or **quotes view @sky or **quotes view @sky,@cebs,@REAP3R", inline=False)
        await context.send(embed=embed)

    @quotes.command(
        name="set",
        description="set quotes channels"
        )
    @checks.not_blacklisted()
    async def quotes_set(self, context: Context,
        sfw_channel: discord.TextChannel,
        nsfw_channel: discord.TextChannel=None):

        with open("guild.json") as file:
            guild = json.load(file)

        if str(context.guild.id) in guild:
            guild[str(context.guild.id)]["sfw"]=sfw_channel.id
            response = f"Quotes channel set to <#{sfw_channel.id}> for sfw quotes\n"

            if nsfw_channel!=None:
                guild[str(context.guild.id)]["nsfw"]=nsfw_channel.id
                response = response + f" Quotes channel set to <#{nsfw_channel.id}> for nsfw quotes"
        else:
            guild[f"{context.guild.id}"]={"name":f"{context.guild.name}","sfw":sfw_channel.id,"nsfw":nsfw_channel.id if nsfw_channel else None}
            response = f"Quotes channel set to <#{sfw_channel.id}> for sfw quotes"
            if nsfw_channel:
                response = response + f" and <#{nsfw_channel.id}> for nsfw quotes"

        with open("guild.json", "w") as p:
            json.dump(guild, p,indent=6)

        await context.reply(response)

def setup(bot):
    bot.add_cog(Quotes(bot))