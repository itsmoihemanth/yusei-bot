import discord
import json
from discord.ext import pages
from discord.ext import commands
from discord.commands import Option, SlashCommandGroup
from helpers import checks, db_api

class Quotes(commands.Cog, name="quotes-slash"):
    def __init__(self, bot):
        self.bot = bot
    
    quotes = SlashCommandGroup("quotes", "Quotes related commands")

    @quotes.command(
        name="add",
        description="Add new quotes"
        )
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @checks.not_blacklisted()
    async def quotes_add(self, interaction: discord.ApplicationContext,
        quote: Option(str, "Enter the quote"),
        author: Option(discord.Member, "Person who said the quote.")):

        with open("guild.json") as file:
            guild = json.load(file)
            
        if interaction.channel.is_nsfw():
            nsfw = 1
        else:
            nsfw = 0
        
        quote = quote.strip()      

        data = {
            "table": "quotes",
            "user_id": author.id,
            "name": author.display_name,
            "quote": quote,
            "nsfw": nsfw,
            "guild_id": interaction.guild.id
            }
        
        quote_exists = db_api.check_exists(data)                                                             
        
        if quote_exists==True:
            response = f"BAKA!! That quote by {author.name} is already there."

            
        else:
            data = db_api.insert(data)
            response = f"**{quote}**"
                
        embed = discord.Embed(description=response, color=guild[str(interaction.guild.id)]["color"])
        
        if quote_exists==False:
            embed.set_footer(text=f"Id:{data['id']}")
            if interaction.guild.icon != None:
                embed.set_author(name=author, icon_url=interaction.guild.icon.url)
            else: 
                embed.set_author(name=author)
            if author.display_avatar != None:
                embed.set_thumbnail(url=author.display_avatar.url)
            
        await interaction.respond(embed = embed)
         
    @quotes.command(
        name="view",
        description="Replies with a list of quotes"
        )
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @checks.not_blacklisted()
    async def quotes_view(self, interaction: discord.ApplicationContext, 
                                author: Option(discord.User, "Person whose quotes you want to see", required=False)):
        

        with open("guild.json") as file:
            guild = json.load(file)

        if "nsfw" in guild[str(interaction.guild.id)]["quotes"]:
            if interaction.channel.is_nsfw():
                nsfw = 1
            else:
                nsfw = 0
        else:
            nsfw = None

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
                title=f"__QUOTES BY {author.display_name}__"

            paginationList = []
            n=len(quotes)
            k = 5
            for i in range(0,n,5):
                embed = discord.Embed(title=title, color=guild[str(interaction.guild.id)]["color"])
                for num in range(i,k):
                    if k>n and num==n:
                        break
                    row=num+1
                    quote_dict = quotes[num]
                    Quote = quote_dict["quote"]
                    Author = quote_dict["name"]           
                    embed.add_field(name=f"__Quote {row}__", value=f"*{Quote} \n~ {Author}*", inline=False)

                paginationList.append(embed)
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

    @quotes.command(
    name="config",
    description="config quotes module"
    )
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @checks.not_blacklisted()
    async def bday_config(self, interaction: discord.ApplicationContext,
                            disable : Option(str,description="Turn disable/enable the quotes commands",choices=["True","False"],required=True),
                            sfw_channel: Option(discord.TextChannel, "Set the sfw quotes channel",required=False),
                            nsfw_channel: Option(discord.TextChannel, "Set the nsfw quotes channel",required=False)):

        with open("guild.json") as file:
            guild = json.load(file)
            
        server = guild[str(interaction.guild.id)]

        
        response = ""
        if disable=='False' and (sfw_channel or nsfw_channel):
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
                
        elif disable == 'True':
            if "quotes" in server:
                server["quotes"]["enabled"] = False
                response = response + "> **quotes commands have been disabled**\n\n"

        with open("guild.json", "w") as p:
            json.dump(guild, p,indent=6)

        
        if response=="":
            response="No changes were made"
        await interaction.respond(embed=discord.Embed(description=response, color=guild[str(interaction.guild.id)]["color"]))

def setup(bot):
    bot.add_cog(Quotes(bot))
