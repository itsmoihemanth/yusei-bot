from discord import Embed
from discord.ext.commands import Cog
from discord.ext import commands

from helpers import checks, manager

class Reactions(commands.Cog, name="reactions"):
	def __init__(self, bot):
		self.bot = bot

@Cog.listener()
async def on_raw_reaction_add(self,payload):
    print("here")
    message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
    if payload.emoji.name == "⭐" and payload.member.bot!=True:
        
        if message.content != "" or message.attachments != []: 

            with open("guild.json") as file:
                guild = json.load(file)

            if interaction.channel.is_nsfw():
                if interaction.guild.id in guild["nsfw"]:
                    channel = self.bot.get_channel(guild["nsfw"][interaction.guild.id])
                else:
                    await interaction.respond("Please set the channel to use for nsfw quotes using /set")
                nsfw = True
            else:
                if interaction.guild.id in guild["sfw"]:
                    channel = self.bot.get_channel(guild["sfw"][interaction.guild.id])
                else:
                    await interaction.respond("Please set the channel to use for sfw quotes using /set")
                nsfw = False

            embed = Embed(description=f"{message.content}\n\n[Jump to message]({message.jump_url})",
                                    colour=0xe0a8cf)
                                
            data = {
                    "table": "quotes",
                    "user_id": author.id,
                    "name": author.display_name,
                    "nsfw": nsfw,
                    "guild_id": interaction.guild.id
                    }

            if message.attachments != []:
                image = message.attachments[0]
                embed.set_image(url=image.url,)
                quote = message.content + f" \n[view image]({image.url})"
                data["quote"]=quote
                
            if message.content != "":
                
                data["quote"]=smessage.content
                quote_exists = db_api.check_exists(data)                                           
                
                if quote_exists==True:
                    return
                else:
                    db_api.insert(data) 
            
            embed.set_footer(text=f"#{message.channel} | {Id}") 
            if message.guild.icon != None:
                embed.set_author(name=message.author, icon_url=message.guild.icon.url)
            else:
                embed.set_author(name=message.author)
                
            embed.set_thumbnail(url=message.author.display_avatar.url)

            if payload.channel_id != c_id:
                await message.reply("Quoted to <#"+str(channel.id)+">")
            
            await channel.send(embed=embed)
            
            
        else:
            await message.reply(f"Ummm hmmm Ummm hmmm, yep just as i thought \n\n Yeeeeeaaaahhhhh {ctx.author.name} i can't add that as a quote.")


def setup(bot):
	bot.add_cog(Reactions(bot))