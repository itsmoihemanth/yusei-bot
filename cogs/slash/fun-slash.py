import random
import aiohttp
import discord
from discord.ext import commands
from discord.commands import Option

from helpers import checks

class Fun(commands.Cog, name="fun-slash"):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.slash_command(
        name="8ball",
        description="Ask any question to the bot."
        )
    @checks.not_blacklisted()
    async def eight_ball(self, interaction: discord.ApplicationContext, question: Option(str,"The question you want to ask.")):
        """
        Ask any question to the bot.
        :param interaction: The application command interaction.
        :param question: The question that should be asked by the user.
        """
        answers = ["It is certain.", "It is decidedly so.", "You may rely on it.", "Without a doubt.",
                   "Yes - definitely.", "As I see, yes.", "Most likely.", "Outlook good.", "Yes.",
                   "Signs point to yes.", "Reply hazy, try again.", "Ask again later.", "Better not tell you now.",
                   "Cannot predict now.", "Concentrate and ask again later.", "Don't count on it.", "My reply is no.",
                   "My sources say no.", "Outlook not so good.", "Very doubtful."]
        embed = discord.Embed(
            title="**My Answer:**",
            description=f"{random.choice(answers)}",
            color=14942490
        )
        embed.set_footer(
            text=f"The question was: {question}"
        )
        await interaction.respond(embed=embed)
        
    @commands.slash_command(
        name="randomfact",
        description="Get a random fact."
    )
    @checks.not_blacklisted()
    async def randomfact(self, interaction: discord.ApplicationContext):
        """
        Get a random fact.
        :param interaction: The application command interaction.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get("https://uselessfacts.jsph.pl/random.json?language=en") as request:
                if request.status == 200:
                    data = await request.json()
                    embed = discord.Embed(
                        description=data["text"],
                        color=14942490
                    )
                else:
                    embed = discord.Embed(
                        title="Error!",
                        description="There is something wrong with the API, please try again later",
                        color=14942490
                    )
                await interaction.respond(embed=embed)





def setup(bot):
    bot.add_cog(Fun(bot))
