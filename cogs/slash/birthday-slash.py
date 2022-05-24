import discord
import datetime
import json
from discord.ext import pages
from discord.ext import commands
from discord.commands import Option, SlashCommandGroup
from helpers import checks, db_api
        
class Birthday(commands.Cog, name="birthday-slash"):
    def __init__(self, bot):
        self.bot = bot
    
    bday = SlashCommandGroup("bday", "Birthday related commands")

    @bday.command(
        name="set",
        description="Add your birthday"
        )
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @checks.not_blacklisted()
    async def bday_set(self, interaction: discord.ApplicationContext,
        day: Option(int, "Enter your birthday",min_value=1,max_value=31,required=True),
        month_name: Option(str, name="month", description="Enter your birthday",choices=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],required=True),
        year: Option(int, "Enter your birthday",min_value=1920,max_value=2009,default=None)):

        if day in [1, 21, 31, 41, 51, 61, 71]:
            Dsuffix = "st"
        elif day in [2, 22, 32, 42, 52, 62, 72]:
            Dsuffix = "nd"
        elif day in [3, 23, 33, 43, 53, 63, 73]:
            Dsuffix = "rd"
        else:
            Dsuffix = "th"
            
        member = interaction.user

        month_object = datetime.datetime.strptime(month_name, "%B")
        month_number = month_object.month
        
        try:
            date_object = datetime.datetime.strptime(f"{day}/{month_number}", "%d/%m")

        except Exception as e:
            print(f"Error in birthday object: {e}")
            await interaction.respond(f"Please enter a valid birthday **{day}{Dsuffix} {month_name}** doesn't make sense",ephemeral=True)
            return

        data = {
            "table": "birthday",
            "user_id": member.id,
            "name": member.display_name,
            "day": day,
            "month": month_number,
            "year": year
        }

        birthday_exists = db_api.check_exists(data)

        if birthday_exists:
            response = f"**Birthday has already been set** \n\n You can use \"\/bday remove\" to remove your birthday"
        else:
            data = db_api.insert(data)

            today = datetime.datetime.now()
            DMtoday = datetime.datetime.strptime(today.strftime("%d/%m"), "%d/%m")

            if today.month > month_number or (today.month == month_number and today.day > day):
                difference = DMtoday.date() - date_object.date()
            else:
                difference = date_object.date() - DMtoday.date()
        
            if year:
                age = today.year - year
                if age in [1, 21, 31, 41, 51, 61, 71]:
                    suffix = "st"
                elif age in [2, 22, 32, 42, 52, 62, 72]:
                    suffix = "nd"
                elif age in [3, 23, 33, 43, 53, 63, 73]:
                    suffix = "rd"
                else:
                    suffix = "th"

                response = f"Succesfully set your birthday to **{day}{Dsuffix} {month_name} {year}**\n i will wish your **{age}{suffix}** birthday in **{difference.days}** days"

            else:
    
                response = f"Succesfully set your birthday to **{day}{Dsuffix} {month_name}**\n i will wish you in **{difference.days}** days"
        
        make_embed = discord.Embed(title=member.display_name,
                                    description=response,
                                    color=0xe0a8cf)
        if member.display_avatar:
            make_embed.set_thumbnail(url=member.display_avatar.url)
        await interaction.respond(embed=make_embed)

    @bday.command(
        name="view",
        description="View birthdays"
        )
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @checks.not_blacklisted()
    async def bday_view(self, interaction: discord.ApplicationContext,
                              member: Option(discord.User, "Person whose birthday you want to see", required=False)):
        
        
        today = datetime.datetime.now()
        data = {'user_id':member.id if member else None}
        birthdays = db_api.get_birthdays(data)
        
        with open("guild.json") as file:
            guild = json.load(file)

        if member:
            birthday_dict = birthdays[0]
            name = birthday_dict["name"]
            day = birthday_dict["day"]
            month = birthday_dict["month"]
            dat = datetime.datetime(today.year, month, day)
            dat = dat.strftime("%B")
            if day in [1, 21, 31, 41, 51, 61, 71]:
                suffix = "st"
            elif day in [2, 22, 32, 42, 52, 62, 72]:
                suffix = "nd"
            elif day in [3, 23, 33, 43, 53, 63, 73]:
                suffix = "rd"
            else:
                suffix = "th"
            make_embed = discord.Embed(description=f"{name}'s birthday is on {day}{suffix} {dat}",
                                        color=guild[str(interaction.guild.id)]["color"])
              
            if interaction.guild.icon != None:
                make_embed.set_thumbnail(url=interaction.guild.icon.url)
            await interaction.respond(embed=make_embed)

        else:
            n = len(birthdays)
            paginationList = []

            k = 10
            for i in range(0, n, 10):
                response = "*To set your birthday use `/bday set`*\n\n"
                
                for num in range(i, k):
                    if k > n and num == n:
                        break
                
                    birthday_dict = birthdays[num]
                    name = birthday_dict["name"]
                    day = birthday_dict["day"]
                    month = birthday_dict["month"]
                    dat = datetime.datetime(today.year, month, day)
                    dat = dat.strftime("%B")
                    if day in [1, 21, 31, 41, 51, 61, 71]:
                        suffix = "st"
                    elif day in [2, 22, 32, 42, 52, 62, 72]:
                        suffix = "nd"
                    elif day in [3, 23, 33, 43, 53, 63, 73]:
                        suffix = "rd"
                    else:
                        suffix = "th"
                    response = response + f"__{day}{suffix} {dat}__: **{name}**\n" 
                    
                make_embed = discord.Embed(title="__Birthdays__",
                                        description=response,
                                        color=guild[str(interaction.guild.id)]["color"])
              
                if interaction.guild.icon != None:
                    make_embed.set_thumbnail(url=interaction.guild.icon.url)
                make_embed.set_footer(text=f"Total Birthdays: {n} | 10 per page")
                paginationList.append(make_embed)
                if k > n:
                    break
                k += 10

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

    @bday.command(
    name="upcoming",
    description="upcoming birthdays"
    )
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @checks.not_blacklisted()
    async def bday_upcoming(self, interaction: discord.ApplicationContext,
                        number: Option(int, "How many upcoming birthdays do you want to see?",min_value=1,max_value=10,default=1)):

        today = datetime.datetime.now()
        data = {'date':today.month,'limit':number}
        birthdays = db_api.get_birthdays(data)

        response = "*To set your birthday use `/bday set`*\n\n"
                
        for num in range(0, len(birthdays)):
                
            birthday_dict = birthdays[num]
            name = birthday_dict["name"]
            day = birthday_dict["day"]
            month = birthday_dict["month"]
            dat = datetime.datetime(today.year, month, day)
            dat = dat.strftime("%B")
            if day in [1, 21, 31, 41, 51, 61, 71]:
                suffix = "st"
            elif day in [2, 22, 32, 42, 52, 62, 72]:
                suffix = "nd"
            elif day in [3, 23, 33, 43, 53, 63, 73]:
                suffix = "rd"
            else:
                suffix = "th"
            response = response + f"__{day}{suffix} {dat}__: **{name}**\n" 
        
        with open("guild.json") as file:
            guild = json.load(file)
        make_embed = discord.Embed(title="__Birthdays__",
                                description=response,
                                color=guild[str(interaction.guild.id)]["color"])
              
        if interaction.guild.icon != None:
            make_embed.set_thumbnail(url=interaction.guild.icon.url)
        
        await interaction.respond(embed=make_embed)
    
    @bday.command(
    name="remove",
    description="remove birthday"
    )
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @checks.not_blacklisted()
    async def bday_view(self, interaction: discord.ApplicationContext):
        
        data = {
            "table": "birthday",
            "user_id": interaction.author.id,
        }
        birthday_exists = db_api.check_exists(data)

        if not birthday_exists:
            response = "**You never saved your birthday** \n\n You can set your birthday using /set"
        else:
            flag = db_api.remove(data)
            if flag==True:
                response = "**Your birthday has been removed** \n\n You can use \"bday set\" to set your birthday"
            else:
                await interaction.respond("Failed to remove your birthday")
                return

        with open("guild.json") as file:
            guild = json.load(file)
        
        make_embed = discord.Embed(title=interaction.author.nick,
                                   description=response,
                                   color=guild[str(interaction.guild.id)]["color"])
        make_embed.set_thumbnail(url=interaction.author.avatar.url)
        make_embed.set_author(name=interaction.author)
        await interaction.respond(embed=make_embed)

def setup(bot):
    bot.add_cog(Birthday(bot))