import discord
from discord.ext import commands
from discord.ext.commands import Context

from helpers import checks

class Quotes(commands.Cog, name="quotes-normal"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="add", description="Add new quotes")
    @checks.not_blacklisted()
    async def add(self, ctx: Context, quote: str, name: str) -> None:
        
        file = helper_funcs.check_channel(ctx)

        if file == "Wrong_channel":
          response = "**you sussy baka! you can't use this command here :raised_hand:**\ngo to the quotes channel to use it :rolling_eyes:"
          embed = discord.Embed(description=response, color=0xe0a8cf)
          await ctx.respond(embed = embed)

        else:
            formula = match({"Guild_id": str(ctx.guild.id)})
            quotes_df = helper.convert_to_dataframe(table.all(file,formula=formula))

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
                table.create(file, {"Id":Id,"Quote":new_quote,"Author":Author,"Name":Author,"Guild_id":str(ctx.guild.id)})
                response = "**Added: " + new_quote +"** \n"+ "~" + Author
                    
            embed = discord.Embed(description=response, color=0xe0a8cf)
            embed.set_footer(text=f"{Id}")
            
            await ctx.send(embed = embed)
    
# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
def setup(bot):
    bot.add_cog(Template(bot))
