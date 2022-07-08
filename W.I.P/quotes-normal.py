import uuid
import discord
import asyncio
import random
import pandas as pd
from discord.ext import pages
from discord.ext import commands
from discord.ext.commands import Context
from discord.commands import Option, SlashCommandGroup

from helpers import checks, manager

from pyairtable import Base
from pyairtable.formulas import match

table = Base('keyVi17QIe7zvkTJR', 'app9n3eybocElyjB5')
guild_info = manager.convert_to_dataframe(table.all("guild_info"))

class Quotes(commands.Cog, name="quotes-normal"):
    def __init__(self, bot):
        self.bot = bot
    
    @Cog.listener()   
    @commands.group(
        name="quotes"
        )
    @checks.not_blacklisted()
    async def quotes(self, context: Context) -> None

        embed=discord.Embed(title="__**Quote command work:**__", color=0xe0a8cf)
        embed.add_field(name="__Add subcommand__", value="Use this to add new quotes into the system, If you try to add stuff that already exists, I bonk you. This is how you use the command, \n\n**quotes add <quote> <name> \n\n You can also now react with ⭐ to a message to add it", inline=False)
        embed.add_field(name="\n__View subcommand__", value="Use to view quotes of everyone or a specific person it will show you a list of quotes by the person.\n You can now add multiple names with a ,\n\n**quotes view  or **quotes view @sky or **quotes view @sky,@cebs,@REAP3R", inline=False)
        await context.send(embed=embed)

    @quotes.command(
        name="add",
        description="Add new quotes"
        )
    @checks.not_blacklisted()
    async def quotes_add(self, interaction: discord.ApplicationContext,
        quote: Option(str, "The quote"),
        name: Option(str, "Person who said the quote.")) -> None:
        
        file = manager.check_channel(interaction,guild_info)

        if file == "Wrong_channel":
          response = "**you sussy baka! you can't use this command here:raised_hand:**\ngo to the quotes channel to use it :rolling_eyes:"
          embed = discord.Embed(description=response, color=0xe0a8cf)
          await interaction.send(embed = embed)

        else:
            formula = match({"Guild_id": str(interaction.guild.id)})
            quotes_df = manager.convert_to_dataframe(table.all(file,formula=formula))

            new_quote = quote.strip()                                                                   ## remove any spaces at end and start of string
            Author = name.strip()                                                                       ## remove any spaces at end and start of string
            if not quotes_df.empty:
                temp_df = quotes_df[quotes_df["Quote"].str.upper().str.contains("^"+new_quote.upper()+"$")]
                check = temp_df[temp_df["Author"].str.upper().str.contains("^"+name.upper()+"$")]
                check2 = temp_df[temp_df["Name"].str.upper().str.contains("^"+name.upper()+"$")] ## Check if quote already exists

            if not check.empty or not check2.empty:
                response = "BAKA!! That quote by "+Author+ " is already there."                         ## output if quote already exists
                name = ""
            if check.empty or quotes_df.empty or check2.empty:
                Id = uuid.uuid4().hex[:5]
                table.create(file, {"Id":Id,"Quote":new_quote,"Author":Author,"Name":Author,"Guild_id":str(interaction.guild.id)})
                response = "**Added: " + new_quote +"** \n"+ "~" + Author
                    
            embed = discord.Embed(description=response, color=0xe0a8cf)
            embed.set_footer(text=f"{Id}")
            
            await interaction.send(embed = embed)
    
                 
    @quotes.command(
        name='view',
        description="Replies with a list of quotes."
        )
    async def quotes_view(interaction: discord.ApplicationContext,
        name: Option(str, "Person whose quotes you want to see.<optional>",default="")):
          
        file = manager.check_channel(interaction)
          
        if file == "Wrong_channel":
          response = "**you sussy baka! you can't use this command here:raised_hand:**\ngo to quotes channel to use it :rolling_eyes:"
          make_embed = discord.Embed(description=response, color=0xe0a8cf)
          await interaction.send(embed = make_embed)
        
        else:
            formula = match({"Guild_id": str(interaction.guild.id)})
            quotes_df = manager.convert_to_dataframe(table.all(file,formula=formula))
            
            if not quotes_df.empty:     
                title="__QUOTES__"
                flag=0
                name = name.strip()
                if name!="":
                    quotes_final_df = pd.DataFrame()
                  
                    names = name.split(",")
                    for name_split in names:
                        candidate = name_split.lstrip(" <@!")
                        candidate = candidate.rstrip(">")
                        
                        quotes1_df = quotes_df[quotes_df["Name"].str.upper().str.contains(candidate.upper())]       ## save all quotes by person to a new dataframe
                        quotes2_df = quotes_df[quotes_df["Author"].str.upper().str.contains(candidate.upper())]
                        quotes_final_df = pd.concat([quotes_final_df,quotes1_df,quotes2_df]).drop_duplicates()  
                        if candidate.isdigit():
                            dm = await bot.fetch_user(candidate)
                            user = str(dm).split('#', 1)[0]
                            name = name.replace(name_split,user)
                            
                    quotes_df = quotes_final_df
                    name = name.upper()
                    name = remove_duplicate_words(name)
                  
                    if len(quotes_df)>0:
                        flag=0
                        title="__QUOTES BY "+ name+"__"
                    else:
                        flag=1
                        
                if flag==0:
                    n=quotes_df.shape[0]
                    
                    paginationList = []
                    k = 5
                    for i in range(0,n,5):
                        response=""
                        for num in range(i,k):
                            if k>n and num==n:
                                break
                            row=num+1

                            Quote = quotes_df["Quote"].iloc[num]                                                      ## Dataframe Quote value to string
                            Author = quotes_df["Author"].iloc[num]                                                    ## Dataframe Author value to string
                            response = response +"**__Quote "+ str(row)+"__**\n*"+str(Quote) +"\n~ "+str(Author)+"*\n\n"           ## Output formatting 
                        paginationList.append(discord.Embed(title=title, description = response, color=0xe0a8cf))
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
                    await paginator.send(interaction.interaction)
                    
                elif flag==1:
                    await interaction.send("<a:oofbar:688428578185936969>, " + name + " was never quoted!!")
            
            else:
                await interaction.send(f"This server has no {file}")

def setup(bot):
    bot.add_cog(Quotes(bot))
