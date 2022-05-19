import uuid
import discord
import asyncio
import random
import datetime
from discord.ext import pages
from discord.ext import commands
from discord.ext.commands import Context
from discord.commands import Option, SlashCommandGroup
from helpers import checks, db_api
        
def check(day, month, year):
    today = datetime.datetime.now()
    age = int(today.year) - year
    if month > 12 or month < 1:
        return False

    elif month in (1, 3, 5, 7, 8, 10, 12):
        if day > 31 or day < 1:
            return False

    elif month in (4, 6, 9, 11):
        if day > 30 or day < 1:
            return False

    elif month == 2:
        if day > 29 or day < 1:
            return False
    elif age < 10 or age > 80:
        return False
    else:
        return True

class Birthday(commands.Cog, name="quotes-slash"):
    def __init__(self, bot):
        self.bot = bot
    
    quotes = SlashCommandGroup("bday", "Birthday related commands")

    @quotes.command(
        name="set",
        description="Add your birthday",
        guilds=[736101194300129390]
        )
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @checks.not_blacklisted()
    async def quotes_add(self, interaction: discord.ApplicationContext,
        quote: Option(str, "Enter the quote"),
        author: Option(discord.Member, "Person who said the quote.")):
        
        # file = manager.check_channel(interaction,guild_info)

        # if file == "Wrong_channel":
          # response = "**you sussy baka! you can't use this command here:raised_hand:**\ngo to the quotes channel to use it :rolling_eyes:"
          # embed = discord.Embed(description=response, color=0xe0a8cf)
          # await interaction.respond(embed = embed)

        # else:

        if interaction.channel.is_nsfw():
            nsfw = True
        else:
            nsfw = False

        data = {
            "table": "quotes",
            "user_id": author.id,
            "name": author.display_name,
            "quote": quote,
            "nsfw": nsfw,
            "guild_id": interaction.guild.id
            }
        
        quote_exists = db_api.check_exists(data)
        quote = quote.strip()                                                                   
        
        if quote_exists==True:
            response = "BAKA!! That quote by "+str(author.name)+ " is already there."
            
        else:
            data = db_api.insert(data)
            response = "**"+quote+"**"
                
        embed = discord.Embed(description=response, color=14942490)
        
        if quote_exists==False:
            embed.set_footer(text=f"Id:{data['id']}")
            embed.set_author(name=author.name)
            if author.avatar != None:
                embed.set_thumbnail(url=author.avatar.url)
            
        await interaction.respond(embed = embed)
         
    @quotes.command(
        name="view",
        description="Replies with a list of quotes",
        guilds=[736101194300129390]
        )
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @checks.not_blacklisted()
    async def quotes_view(self, interaction: discord.ApplicationContext, 
                                author: Option(discord.User, "Person whose quotes you want to see", required=False)):
        
        if interaction.channel.is_nsfw():
            nsfw = 1
        else:
            nsfw = 0

        data={
            "user_id": author.id if author else "",
            "nsfw": nsfw,
            "guild_id": interaction.guild.id
            }

        quotes = db_api.get_quotes(data)
        if type(quotes)==str:
            await interaction.respond(quotes)
        else:
            title="__QUOTES__"
            if author:
                title="__QUOTES BY "+ str(author.display_name)+"__"

            paginationList = []
            n=len(quotes)
            k = 5
            for i in range(0,n,5):
                response=""
                for num in range(i,k):
                    if k>n and num==n:
                        break
                    row=num+1
                    quote_dict = quotes[num]
                    Quote = quote_dict["quote"]                                                      ## Dataframe Quote value to string
                    Author = quote_dict["name"]                                                      ## Dataframe Author value to string
                    response = response +"**__Quote "+ str(row)+"__**\n*"+Quote +"\n~ "+Author+"*\n\n"           ## Output formatting 

                paginationList.append(discord.Embed(title=title, description = response, color=14942490))
                if k>n:
                    break
                k+=5
                    
            paginator = pages.Paginator(pages=paginationList, use_default_buttons=False, show_menu=False, loop_pages=False, timeout=40.0)
            paginator.add_button(
                pages.PaginatorButton("first", label="<<", style=discord.ButtonStyle.red)
            )
            paginator.add_button(
            pages.PaginatorButton("prev", label="<", style=discord.ButtonStyle.red)
            )
            paginator.add_button(
                pages.PaginatorButton(
                    "page_indicator", style=discord.ButtonStyle.gray, disabled=True
                )
            )
            paginator.add_button(
                pages.PaginatorButton("next", label=">", style=discord.ButtonStyle.red)
            )
            paginator.add_button(
                pages.PaginatorButton("last", label=">>", style=discord.ButtonStyle.red)
            )
            await paginator.respond(interaction.interaction)

def setup(bot):
    bot.add_cog(Quotes(bot))
