import discord
import json, datetime
from discord.ext import pages, commands, tasks
from discord.commands import Option, SlashCommandGroup
from helpers import checks, db_api, json_manager

def suffix_helper(val):
    if val in [1, 21, 31, 41, 51, 61, 71]:
        suffix = "st"
    elif val in [2, 22, 32, 42, 52, 62, 72]:
        suffix = "nd"
    elif val in [3, 23, 33, 43, 53, 63, 73]:
        suffix = "rd"
    else:
        suffix = "th"
        
    return suffix

IST = datetime.time(second=5)
class Birthday(commands.Cog, name="birthday-slash"):
    def __init__(self, bot):
        self.bot = bot
        self.wish.start()
    
    @tasks.loop(hours=1)
    async def wish(self):
        
        today = datetime.datetime.now()
        if IST.hour == today.hour:

            data = {
            'month':today.month,
            'day':today.day
            }
   
            with open("guild.json") as file:
                guild_json = json.load(file)
                
            birthdays_today = db_api.get_birthdays(data)
            
            for server_key in guild_json:
                
                guild = self.bot.get_guild(int(server_key))
                
                role=None
                server = guild_json[server_key]
                if 'birthday' not in server:
                    continue

                if 'role' in server['birthday']:
                    role = guild.get_role(guild_json[server_key]['birthday']['role'])
                            
                for guild_member in guild.members:
                                
                    if 'role' in server['birthday'] and role in guild_member.roles and not any(d['user_id'] == guild_member.id for d in birthdays_today):
                        print(f"removed {role} from {guild_member} in {guild.name}\n")
                        await guild_member.remove_roles(role)

                for i in range(0,len(birthdays_today)):
                    bday = birthdays_today[i]
                    user_id = bday["user_id"]
                        
                    channel = self.bot.get_channel(server['birthday']['channel'])

                    for guild_member in guild.members:
                        if user_id != guild_member.id:
                            continue
                            
                        response = server['birthday']['message'] if 'message' in server['birthday'] else "Happy Birthday {user}!"
                        mention_role = server['birthday']['mention'] if 'mention' in server['birthday'] else ""
                        mapping = {'{user}': f"{guild_member.display_name}",'{user.mention}' : f"{guild_member.mention}",'{server}' : f"{guild.name}"}
                            
                        for key in mapping:
                            response = response.replace(key, mapping[key])
                            mention_role = mention_role.replace(key, mapping[key])


                        make_embed = discord.Embed(description=response, color=guild_json[server_key]["color"])
                        await channel.send(f"{mention_role}",embed=make_embed)

                        if role!=None:
                                
                            print(f"Added {role} to {guild_member} in {guild.name}\n")
                            await guild_member.add_roles(role)
                        
                        

    @wish.before_loop
    async def before_wish(self):
        print('waiting.......')
        await self.bot.wait_until_ready()

    bday = SlashCommandGroup("bday", "Birthday related commands")

    @bday.command(
        name="set",
        description="Add your birthday"
        )
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @checks.not_blacklisted()
    async def bday_set(self, interaction: discord.ApplicationContext,
        day: Option(int, "Enter your birthday",min_value=1,max_value=31,required=True),
        month_name: Option(str, name="month", description="Enter your birthday",choices=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],required=True)):

        suffix = suffix_helper(day)
            
        member = interaction.user

        month_object = datetime.datetime.strptime(month_name, "%B")
        month_number = month_object.month
        
        try:
            date_object = datetime.datetime.strptime(f"{day}/{month_number}", "%d/%m")

        except Exception as e:
            print(f"Error in birthday object: {e}")
            await interaction.respond(f"Please enter a valid birthday **{day}{suffix} {month_name}** doesn't make sense",ephemeral=True)
            return

        data = {
            "table": "birthday",
            "user_id": member.id,
            "name": member.display_name,
            "day": day,
            "month": month_number
        }

        birthday_exists = db_api.check_exists(data)

        if birthday_exists:
            response = f"**Birthday has already been set** \n\n You can use \"\/bday remove\" to remove your birthday"
        else:
            data = db_api.insert(data)

            today = datetime.datetime.now()
             
            if today.month > month_number or (today.month == month_number and today.day > day):
                date_object = datetime.datetime.strptime(f"{day}/{month_number}/{today.year+1}", "%d/%m/%y")
                DMtoday = datetime.datetime.strptime(today.strftime("%d/%m/%y"), "%d/%m/%y")
                difference = date_object.date() - DMtoday.date()
            else:
                DMtoday = datetime.datetime.strptime(today.strftime("%d/%m"), "%d/%m")
                difference = date_object.date() - DMtoday.date()
            
            response = f"Succesfully set your birthday to **{day}{suffix} {month_name}**\n i will wish you in **{difference.days}** days" if int(difference.days)>0 else "Succesfully set your birthday to **{day}{suffix} {month_name}**\n **Have the happiest of birthdays {member.mention}"
        
        make_embed = discord.Embed(title=member.display_name,
                                    description=response,
                                    color=json_manager.get_color(str(interaction.guild.id)))
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
        birthday_list = db_api.get_birthdays(data)
        birthdays =[]
        for user in birthday_list:
            flag=False
            for guild_member in interaction.guild.members:
                if user["user_id"] == guild_member.id:
                    flag=True
            if flag==True:
                birthdays.append(user)
                
        del birthday_list
        
        with open("guild.json") as file:
            guild = json.load(file)
            
        if not birthdays:
        	await interaction.respond(f"User <@!{data['user_id']}> did not set their birthday here or is not in the server" if data['user_id'] else "No birthdays have been set")

        else:
            if member:
                
                birthday_dict = birthdays[0]
                user_id = birthday_dict["user_id"]
                name = birthday_dict["name"]
                day = birthday_dict["day"]
                month = birthday_dict["month"]
                dat = datetime.datetime(today.year, month, day)
                dat = dat.strftime("%B")
                suffix = suffix_helper(day)

                date_object = datetime.datetime.strptime(f"{day}/{month}", "%d/%m")
                DMtoday = datetime.datetime.strptime(today.strftime("%d/%m"), "%d/%m")

                if today.month > month or (today.month == month and today.day > day):
                    difference = DMtoday.date() - date_object.date()
                else:
                    difference = date_object.date() - DMtoday.date()

                make_embed = discord.Embed(title=f"{name}",description=f"<@{user_id}>'s birthday is on **{day}{suffix} {dat}** in **{difference.days}** days",
                                            color=json_manager.get_color(str(interaction.guild.id)))

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
                        suffix = suffix_helper(day)
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
    async def bday_upcoming(self, interaction: discord.ApplicationContext):

        today = datetime.datetime.now()
        data = {'date':today.month,'limit':5}
        birthday_list = db_api.get_birthdays(data)
        birthdays =[]
        for user in birthday_list:
            flag=False
            for guild_member in interaction.guild.members:
                if user["user_id"] == guild_member.id:
                    flag=True
            if flag==True:
                birthdays.append(user)

        if not birthdays:
        	await interaction.respond(f"No birthdays are set in the server")
        
        else:
            response = "*To set your birthday use `/bday set`*\n\n"
                
            for num in range(0, len(birthdays)):
                
                birthday_dict = birthdays[num]
                name = birthday_dict["name"]
                day = birthday_dict["day"]
                month = birthday_dict["month"]
                dat = datetime.datetime(today.year, month, day)
                dat = dat.strftime("%B")
                suffix = suffix_helper(day)
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
    async def bday_remove(self, interaction: discord.ApplicationContext):
        
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