import json
import os
import sys
import platform
import random
import discord
from discord.ext import commands
from discord.ext.commands import Bot
from helpers import db_api

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)

intents = discord.Intents.all()
bot = Bot(command_prefix=commands.when_mentioned_or(config["prefix"]), intents=intents,help_command=None)

@bot.event
async def on_ready() -> None:
    """
    The code in this even is executed when the bot is ready
    """

    print(f"Logged in as {bot.user.name}")
    print(f"discord API version: {discord.__version__}")
    print(f"Python version: {platform.python_version()}")
    print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    print("-------------------")


def load_commands(command_type: str) -> None:
    for file in os.listdir(f"./cogs/{command_type}"):
        if file.endswith(".py"):
            extension = file[:-3]
            try:
                bot.load_extension(f"cogs.{command_type}.{extension}")
                print(f"Loaded extension '{extension}'")
            except Exception as e:
                exception = f"{type(e).__name__}: {e}"
                print(f"Failed to load extension {extension}\n{exception}")


if __name__ == "__main__":
    load_commands("slash")
    load_commands("normal")
    #load_commands("listeners")

@bot.event
async def on_application_command_error(context, error):

    if isinstance(error, commands.CommandOnCooldown):
        await context.respond(f"This command is on cooldown... try again in {error.retry_after:.2f} seconds.")
    elif isinstance(error, commands.errors.MissingPermissions):
        await context.send("You do not have permission to use this command")
    elif isinstance(error, commands.CheckFailure):
        await context.send(error)
    else:
        print(error, type(error))
        await context.respond("Whoops! Looks liks something's amiss")

@bot.event
async def on_command_error(context, error):
    if isinstance(error, commands.CommandOnCooldown):
        await context.respond(f"This command is on cooldown... try again in {error.retry_after:.2f} seconds.")
    elif isinstance(error, commands.errors.MissingRequiredArgument):
        print(error, type(error))
        await context.send(error)
    elif isinstance(error, commands.CommandNotFound):
        print(error, type(error))
        await context.send("That is not a valid command")
    elif isinstance(error, commands.errors.MissingPermissions):
        await context.send("You do not have permission to use this command")
    else:
        print(error, type(error))
        await context.send(f"Whoops! Looks liks something's amiss: {error}")

@bot.event
async def on_guild_join(guild):
    
    print(f"Bot joined {guild.name}")

    with open("guild.json") as file:
        guild_dict = json.load(file)

    guild_dict[str(guild.id)]={"name":f"{guild.name}", "sfw":None, "nsfw":None, "birthday":None,"color":14942490}
    
    with open("guild.json", "w") as p:
            json.dump(guild_dict, p,indent=6)

@bot.event
async def on_guild_remove(guild):

    with open("guild.json") as file:
            guild_dict = json.load(file)

    removed_value = guild_dict.pop(str(guild.id), 'Guild not found')
    print(f"Bot has been removed from {guild.name}")
    
    with open("guild.json", "w") as p:
            json.dump(guild_dict, p,indent=6)

@bot.event
async def on_raw_reaction_add(payload):
    message = await bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
    if payload.emoji.name == "⭐" and payload.member.bot!=True:
        if message.content != "" or message.attachments != []: 
            
            with open("guild.json") as file:
                guild = json.load(file)

            if message.channel.is_nsfw():
                if guild[str(payload.guild_id)]["nsfw"]:
                    channel = bot.get_channel(guild[str(payload.guild_id)]["nsfw"])
                else:
                    await message.reply("Please set the channel to use for nsfw quotes using /config")
                nsfw = 1
            else:
                if guild[str(payload.guild_id)]["sfw"]:
                    channel = bot.get_channel(guild[str(payload.guild_id)]["sfw"])
                else:
                    await message.reply("Please set the channel to use for sfw quotes using /config")
                nsfw = 0

            embed = discord.Embed(description=f"{message.content}\n\n[Jump to message]({message.jump_url})",
                                    colour=guild[str(payload.guild_id)]["color"])
                                
            data = {
                    "table": "quotes",
                    "user_id": message.author.id,
                    "name": message.author.display_name,
                    "nsfw": nsfw,
                    "guild_id": payload.guild_id
                    }

            if message.attachments != []:
                image = message.attachments[0]
                embed.set_image(url=image.url,)
                quote = message.content + f" \n[view image]({image.url})"
                data["quote"]=quote
                
            if message.content != "":
                
                data["quote"]=message.content
                quote_exists = db_api.check_exists(data)                                           
                
                if quote_exists==True:
                    return
                else:
                    data = db_api.insert(data) 
            
            embed.set_footer(text=f"#{message.channel} | {data['id']}") 
            if message.guild.icon != None:
                embed.set_author(name=message.author, icon_url=message.guild.icon.url)
            else:
                embed.set_author(name=message.author)
                
            embed.set_thumbnail(url=message.author.display_avatar.url)
            
            c_id = channel.id if channel else payload.channel_id
            if payload.channel_id != c_id:
                await message.reply("Quoted to <#"+str(channel.id)+">")
            
            await channel.send(embed=embed)
            
            
        else:
            await message.reply(f"Ummm hmmm Ummm hmmm, yep just as i thought \n\n Yeeeeeaaaahhhhh {message.author.name} i can't add that as a quote.")

"""class PersistentView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Wave To Say Hi!!",
        custom_id="persistent_view:greet",
    )
    async def greet(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message(random.choice(["https://c.tenor.com/-Kgr-uW4GA8AAAAi/hello.gif","https://c.tenor.com/qLMpwF42khIAAAAi/hi-brown.gif","https://c.tenor.com/y1enbfpHMTEAAAAi/hi-cute.gif","https://c.tenor.com/ftqs42Yna-oAAAAi/mochi-mochi-hello-white-mochi-mochi.gif"]))
"""

@bot.event
async def on_member_join(member):
    if member.guild.id == 959379487718510592:
        channel = bot.get_channel(974192528704274432)
        await channel.send(random.choice([f"{member.mention} just entered the city, say hi!",f"Glad you could make it {member.mention}!!",f"Well, Hello there {member.mention}"])) #,view=PersistentView())
    
bot.run(config["token"])