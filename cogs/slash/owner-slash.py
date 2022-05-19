import discord
from discord.commands import SlashCommandGroup
from discord import Option
from discord.ext import commands
import json

from helpers import json_manager, checks, converters

class Owner(commands.Cog, name="owner-slash"):
    def __init__(self, bot):
        self.bot = bot
    
    blacklist = SlashCommandGroup("blacklist", "Get the list of all blacklisted users.")

    @blacklist.command(
        name="add",
        description="Lets you add a user from not being able to use the bot.",
        guild=["736101194300129390"]
        )
    @checks.is_owner()
    async def blacklist_add(self, interaction: discord.ApplicationContext, member_or_channel: Option(converters.ChannelOrMemberConverter, "The @user/#channel you want to add to the blacklist.", default = None)) -> None:
        """
        Lets you add a user/channel from not being able to use the bot.
        :param interaction: The application command interaction.
        :param user: The user/channel that should be added to the blacklist.
        """
        Object = member_or_channel
        try:
            if isinstance(Object,discord.TextChannel):
                json_key = 'channel_ids'
                object_id = Object.id
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
                return await interaction.respond(embed=embed)
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
            await interaction.respond(embed=embed)
        except Exception as exception:
            embed = discord.Embed(
                title="Error!",
                description=f"An **{exception}** occurred when trying to add **{Object.name}** to the blacklist.",
                color=0xE02B2B
            )
            await interaction.respond(embed=embed)

    @blacklist.command(
        name="remove",
        description="Lets you remove a user from not being able to use the bot.",
        guild=["736101194300129390"]
        )
        
    @checks.is_owner()
    async def blacklist_remove(self, interaction: discord.ApplicationContext, member_or_channel: Option(converters.ChannelOrMemberConverter, "The @user/#channel you want to remove from the blacklist.", default = None)):
        """
        Lets you remove a user/channel from not being able to use the bot.
        :param interaction: The application command interaction.
        :param user: The user/channel that should be removed from the blacklist.
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
                return await interaction.respond(embed=embed)
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
            await interaction.respond(embed=embed)
        except Exception as exception:
            embed = discord.Embed(
                title="Error!",
                description=f"An **{exception}** occurred when trying to add **{Object.name}** to the blacklist.",
                color=0xE02B2B
            )
            await interaction.respond(embed=embed)

def setup(bot):
    bot.add_cog(Owner(bot))
