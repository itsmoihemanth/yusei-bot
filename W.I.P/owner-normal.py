import discord
from discord.ext import commands
from discord.ext.commands import Context
import json
import typing

from helpers import json_manager, checks, converters

class Owner(commands.Cog, name="owner-normal"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="shutdown",
        description="Make the bot shutdown.",
    )
    @checks.is_owner()
    async def shutdown(self, context: Context):
        """
        Makes the bot shutdown.
        """
        embed = discord.Embed(
            description="Shutting down. Bye! :wave:",
            color=0x9C84EF
        )
        await context.send(embed=embed)
        await self.bot.close()

    @commands.command(
        name="say",
        description="The bot will say anything you want.",
    )
    @checks.is_owner()
    async def say(self, context: Context, *, message: str):
        """
        The bot will say anything you want.
        """
        await context.send(message)

    @commands.command(
        name="embed",
        description="The bot will say anything you want, but within embeds.",
    )
    @checks.is_owner()
    async def embed(self, context: Context, *, message: str):
        """
        The bot will say anything you want, but within embeds.
        """
        embed = discord.Embed(
            description=message,
            color=0x9C84EF
        )
        await context.send(embed=embed)

    @commands.group(
        name="blacklist"
    )
    async def blacklist(self, context: Context):
        """
        Lets you add or remove a user from not being able to use the bot.
        """
        if context.invoked_subcommand is None:
            with open("blacklist.json") as file:
                blacklist = json.load(file)
            embed = discord.Embed(
                title=f"There are currently {len(blacklist['user_ids'])} user's and {len(blacklist['channel_ids'])} channel's blacklisted",
                description=f"{', '.join(str(id) for id in blacklist['user_ids'])}",
                color=0x9C84EF
            )
            await context.send(embed=embed)

    @blacklist.command(
        name="add"
    )
    async def blacklist_add(self, context: Context, member_or_channel: converters.ChannelOrMemberConverter):
        """
        Lets you add a user from not being able to use the bot.
        """
        Object = member_or_channel
        try:
            if isinstance(Object,discord.TextChannel):
                json_key = 'channel_ids'
            else:
                json_key = 'user_ids'
                
            object_id = Object.id
            with open("blacklist.json") as file:
                blacklist = json.load(file)
            if object_id in blacklist[json_key]:
                embed = discord.Embed(
                    title="Error!",
                    description=f"**{Object.name}** is already in the blacklist.",
                    color=0xE02B2B
                )
                return await context.send(embed=embed)
            json_manager.add_to_blacklist(json_key,object_id)
            
            embed = discord.Embed(
                title="User Blacklisted",
                description=f"**{Object.name}** has been successfully added to the blacklist",
                color=0x9C84EF
            )
            with open("blacklist.json") as file:
                blacklist = json.load(file)
            embed.set_footer(
                text=f"There are now {len(blacklist[json_key])} {json_key}'s in the blacklist"
            )
            await context.send(embed=embed)
        except Exception as exception:
            embed = discord.Embed(
                title="Error!",
                description=f"An **{exception}** occurred when trying to add **{Object.name}** to the blacklist.",
                color=0xE02B2B
            )
            await context.send(embed=embed)

    @blacklist.command(
        name="remove"
    )
    async def blacklist_remove(self, context, member_or_channel: converters.ChannelOrMemberConverter):
        """
        Lets you remove a user/channel from not being able to use the bot.
        """
        Object = member_or_channel
        try:
            if isinstance(Object,discord.TextChannel):
                json_key = 'channel_ids'
            else:
                json_key = 'user_ids'

            object_id = Object.id
            with open("blacklist.json") as file:
                blacklist = json.load(file)
            if object_id not in blacklist[json_key]:
                embed = discord.Embed(
                    title="Error!",
                    description=f"**{Object.name}** is not in the blacklist.",
                    color=0xE02B2B
                )
                return await context.send(embed=embed)
            json_manager.remove_from_blacklist(json_key,object_id)
            embed = discord.Embed(
                title="User removed from blacklist",
                description=f"**{Object.name}** has been successfully removed from the blacklist",
                color=0x9C84EF
            )
            with open("blacklist.json") as file:
                blacklist = json.load(file)
            embed.set_footer(
                text=f"There are now {len(blacklist[json_key])} {json_key} users in the blacklist"
            )
            await context.send(embed=embed)
        except Exception as exception:
            embed = discord.Embed(
                title="Error!",
                description=f"An **{exception}** occurred when trying to add **{Object.name}** to the blacklist.",
                color=0xE02B2B
            )
            await context.send(embed=embed)

    @blacklist.command(
        name="show"
    )
    async def blacklist_show(self, context):
        """
        shows all users & channels blacklisted.
        """
        try:
            if isinstance(Object,discord.TextChannel):
                json_key = 'channel_ids'
            
            json_key = 'user_ids'

            with open("blacklist.json") as file:
                blacklist = json.load(file)
            for object_id in blacklist[json_key]:
                embed = discord.Embed(
                    title="Blacklist",
                    description=f"**{Object.name}** is not in the blacklist.",
                    color=0xE02B2B
                )
                return await context.send(embed=embed)
            json_manager.remove_from_blacklist(json_key,object_id)
            embed = discord.Embed(
                title="User removed from blacklist",
                description=f"**{Object.name}** has been successfully removed from the blacklist",
                color=0x9C84EF
            )
            with open("blacklist.json") as file:
                blacklist = json.load(file)
            embed.set_footer(
                text=f"There are now {len(blacklist[json_key])} {json_key} users in the blacklist"
            )
            await context.send(embed=embed)
        except Exception as exception:
            embed = discord.Embed(
                title="Error!",
                description=f"An **{exception}** occurred when trying to add **{Object.name}** to the blacklist.",
                color=0xE02B2B
            )
            await context.send(embed=embed)
        
def setup(bot):
    bot.add_cog(Owner(bot))