import aiohttp
import discord
from discord.ext import commands
from discord.commands import Option, SlashCommandGroup

from helpers import checks, views

class Fun(commands.Cog, name="fun-slash"):
    def __init__(self, bot):
        self.bot = bot
   
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

    @commands.slash_command( 
        name="tic",
        description="tic tac toe."
    )
    @checks.not_blacklisted()
    async def tic(self, ctx: discord.ApplicationContext):
        """Starts a tic-tac-toe game with yourself."""
        # Setting the reference message to ctx.message makes the bot reply to the member's message.
        await ctx.respond("Tic Tac Toe: X goes first", view=views.TicTacToe())

    send = SlashCommandGroup("send", "Send custom msgs")

    @send.command(
        name="embed",
        description="sends an embed"
        )
    @checks.not_blacklisted()
    async def send_embed(self, interaction: discord.ApplicationContext,
                    description : Option(str, "The desc of the embed",required=True),
                    title : Option(str, "The title of the embed",default=None),
                    color : Option(str, "The color of the embed in hex",default="FF0000")):

        try:
            color = color.strip()
            color = color.lstrip('#')
            color = int(color,16)
        except Exception as e:
            await interaction.respond("Enter a valid hex color",ephemeral=True)
            return

        embed = discord.Embed(
                title=title,
                description=description,
                color=color
            )
        await interaction.send(embed=embed)
        await interaction.respond("Embed Sent",ephemeral=True)

    @send.command(
        name="message",
        description="Sends a message as the bot"
        )
    @checks.not_blacklisted()
    async def send_message(self, interaction: discord.ApplicationContext,
                    message : Option(str, "Text to send")):
        
        await interaction.send(message)
        
        await interaction.respond("Message Sent",ephemeral=True)

def setup(bot):
    bot.add_cog(Fun(bot)) 
