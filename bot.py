import json
import os
import sys
import platform
import random
import discord
from discord.ext import commands
from discord.ext.commands import Bot
from helpers import db_api
import logging

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)

intents = discord.Intents.all()
bot = Bot(command_prefix=commands.when_mentioned_or(config["prefix"]), intents=intents)

@bot.event
async def on_ready() -> None:
    """
    The code in this even is executed when the bot is ready
    """
    today = discord.utils.utcnow()
    print(f"Logged in as {bot.user.name} at {today}")
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
                print(f"Loaded extension 'cogs.{command_type}.{extension}'")
            except Exception as e:
                exception = f"{type(e).__name__}: {e}"
                print(f"Failed to load extension {extension}\n{exception}")


if __name__ == "__main__":
    load_commands("slash")
    #load_commands("normal")
    #load_commands("listeners")

@bot.event
async def on_application_command_error(Interaction, error):

    if isinstance(error, commands.CommandOnCooldown):
        await Interaction.respond(f"This command is on cooldown... try again in {error.retry_after:.2f} seconds.",ephemeral=True)
    elif isinstance(error, commands.errors.MissingPermissions):
        await Interaction.respond(error,ephemeral=True)
    elif isinstance(error, commands.CheckFailure):
        pass
    else:
        print(error, type(error))
        await Interaction.respond(f"Whoops! Looks liks something's amiss: {error}",ephemeral=True)

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

    with open("blacklist.json") as file:
        blacklist_json = json.load(file)

    with open("guild.json") as file:
        guild_json = json.load(file)

    blacklist_json[str(guild.id)]={"name":f"{guild.name}","user_ids":[],"channel_ids":[]}
    guild_json[str(guild.id)]= {"name":f"{guild.name}","color":14942490}

    with open("guild.json", "w") as g:
            json.dump(guild_json, g,indent=6)

    with open("blacklist.json", "w") as b:
            json.dump(blacklist_json, b,indent=6)
            
@bot.event
async def on_guild_remove(guild):

    with open("blacklist.json") as file:
            blacklist_json = json.load(file)

    with open("guild.json") as file:
        guild_json = json.load(file)

    blacklist_json.pop(str(guild.id), 'Guild not found')
    guild_json.pop(str(guild.id), 'Guild not found')

    with open("guild.json", "w") as g:
            json.dump(guild_json, g,indent=6)
            
    with open("blacklist.json", "w") as p:
            json.dump(blacklist_json, p,indent=6)

    
    print(f"Bot has been removed from {guild.name}")

@bot.event
async def on_raw_reaction_add(payload):
    message = await bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
    if payload.emoji.name == "⭐" and payload.member.bot!=True:
        commands.cooldown(1, 5, commands.BucketType.guild)
        if message.content != "" or message.attachments != []: 
            with open("guild.json") as file:
                guild = json.load(file)

            server = guild[str(payload.guild_id)]
            if "quotes" not in server:
                return
            if message.channel.is_nsfw():
                if "nsfw" in server["quotes"]:
                    channel = bot.get_channel(server["quotes"]["nsfw"])
                else:
                    await message.reply("Please set the channel to use for nsfw quotes using /config")
                nsfw = 1
            else:
                if "sfw" in server["quotes"]:
                    channel = bot.get_channel(server["quotes"]["sfw"])
                else:
                    await message.reply("Please set the channel to use for sfw quotes using /config")
                nsfw = 0

            embed = discord.Embed(description=f"{message.content}\n\n[Jump to message]({message.jump_url})",
                                    colour=server["color"])
                                
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
                
            if message.content != "":
                
                data["quote"]=message.content
                quote_exists = db_api.check_exists(data)                                           
                
                if quote_exists==True:
                    return
                else:
                    data = db_api.insert(data) 
            
            embed.set_footer(text=f"#{message.channel} | {data['id']}" if message.content!="" else f"#{message.channel}") 
            if message.guild.icon != None:
                embed.set_author(name=message.author, icon_url=message.guild.icon.url)
            else:
                embed.set_author(name=message.author)
            if message.author.display_avatar:   
                embed.set_thumbnail(url=message.author.display_avatar.url)
            
            
            await channel.send(embed=embed)
            if payload.channel_id != channel.id:
                await message.reply("Quoted to <#"+str(payload.channel_id)+">")
            
        else:
            await message.reply(f"I can not add that as a quote yet.")

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
    if member.guild.id == 959379487718510592 and member.bot!=True:
        channel = bot.get_channel(974192528704274432)
        await channel.send(random.choice([f"{member.mention} just entered the city, say hi!",f"Glad you could make it {member.mention}!!",f"Well, Hello there {member.mention}",f"Hi {member.mention} welcome to the city, hope you enjoy your stay"])) #,view=PersistentView())

        
@bot.command()
async def reload(ctx, cog: str):
    """Re-evaluate the cog's code. Useful if working on the cog's code
    and you want to quickly test your changes. Can only be used by bot
    admins
    """
    if ctx.message.author.id in config["owners"]:
        try:
            bot.reload_extension(f"cogs.{cog}")
            await ctx.message.add_reaction('\U0001F44D')
        except Exception as error:
            print(error, file=sys.stderr)
            await ctx.send(f"```python\n{error}```")
            

@bot.command()
async def announce(ctx, *, message: str):

    if ctx.message.author.id in config["owners"]:
        for guild in bot.guilds:
            print(bot.guilds)
            print(guild)
            print(guild.owner)
            print(guild.owner.dm_channel)
            try:
                await guild.owner.send(message)
                await ctx.reply(f"Dm sent to `{guild.owner}` of `{guild}`")
            except Exception as error:
                await ctx.reply(f"Dm to `{guild.owner}` of `{guild}` raised an error : ```{error}```")


bot.run(config["token"])