import discord
from discord import Option
from discord.ext import commands

from helpers import checks

class Moderation(commands.Cog, name="moderation-slash"):
    def __init__(self, bot):
        self.bot = bot
            
    @commands.slash_command(
        name="kick",
        description="Kick a user out of the server.",
    )
    @commands.has_permissions(kick_members=True)
    @checks.not_blacklisted()
    async def kick(self, interaction: discord.ApplicationContext, user: Option(discord.User, "The user you want to kick."),
                   reason: Option(str, "The reason you kicked the user.",default= "Not specified")) -> None:
        """
        Kick a user out of the server.
        :param interaction: The application command interaction.
        :param user: The user that should be kicked from the server.
        :param reason: The reason for the kick. Default is "Not specified".
        """
        member = await interaction.guild.get_or_fetch_member(user.id)
        if member.guild_permissions.administrator:
            embed = discord.Embed(
                title="Error!",
                description="User has Admin permissions.",
                color=0xE02B2B
            )
            await interaction.respond(embed=embed)
        else:
            try:
                embed = discord.Embed(
                    title="User Kicked!",
                    description=f"**{member}** was kicked by **{interaction.author}**!",
                    color=0x9C84EF
                )
                embed.add_field(
                    name="Reason:",
                    value=reason
                )
                await interaction.send(embed=embed)
                try:
                    await member.send(
                        f"You were kicked by **{interaction.author}**!\nReason: {reason}"
                    )
                except discord.Forbidden:
                    await interaction.respond("Couldn't send a message in the private messages of the user")
                    pass
                await member.kick(reason=reason)
            except:
                embed = discord.Embed(
                    title="Error!",
                    description="An error occurred while trying to kick the user. Make sure my role is above the role of the user you want to kick.",
                    color=0xE02B2B
                )
                await interaction.respond(embed=embed)

    @commands.slash_command(
        name="nick",
        description="Change the nickname of a user on a server."
        )
    @commands.has_permissions(manage_nicknames=True)
    @checks.not_blacklisted()
    async def nick(self, interaction: discord.ApplicationContext, user: Option(discord.User,"The user you want to change the nickname."), nickname: Option(str,"The new nickname of the user, leave empty to remove nickname",default= None)) -> None:
        """
        Change the nickname of a user on a server.
        :param interaction: The application command interaction.
        :param user: The user that should have its nickname changed.
        :param nickname: The new nickname of the user. Default is None, which will reset the nickname.
        """
        member = await interaction.guild.get_or_fetch_member(user.id)
        try:
            await member.edit(nick=nickname)
            embed = discord.Embed(
                title="Changed Nickname!",
                description=f"**{member}'s** new nickname is **{nickname}**!",
                color=0x9C84EF
            )
            await interaction.respond(embed=embed)
        except:
            embed = discord.Embed(
                title="Error!",
                description="An error occurred while trying to change the nickname of the user. Make sure my role is above the role of the user you want to change the nickname.",
                color=0xE02B2B
            )
            await interaction.respond(embed=embed)

    @commands.slash_command(
        name="ban",
        description="Bans a user from the server."
        )
    @commands.has_permissions(ban_members=True)
    @checks.not_blacklisted()
    async def ban(self, interaction: discord.ApplicationContext, user: Option(discord.User,"The user you want to ban."),
                  reason: Option(str, "The reason you banned the user.",default = "Not specified")) -> None:
        """
        Bans a user from the server.
        :param interaction: The application command interaction.
        :param user: The user that should be banned from the server.
        :param reason: The reason for the ban. Default is "Not specified".
        """
        member = await interaction.guild.get_or_fetch_member(user.id)
        try:
            if member.guild_permissions.administrator:
                embed = discord.Embed(
                    title="Error!",
                    description="User has Admin permissions.",
                    color=0xE02B2B
                )
                await interaction.respond(embed=embed)
            else:
                embed = discord.Embed(
                    title="User Banned!",
                    description=f"**{member}** was banned by **{interaction.author}**!",
                    color=0x9C84EF
                )
                embed.add_field(
                    name="Reason:",
                    value=reason
                )
                await interaction.respond(embed=embed)
                try:
                    await member.send(f"You were banned by **{interaction.author}**!\nReason: {reason}")
                except discord.Forbidden:
                    # Couldn't send a message in the private messages of the user
                    pass
                await member.ban(reason=reason)
        except:
            embed = discord.Embed(
                title="Error!",
                description="An error occurred while trying to ban the user. Make sure my role is above the role of the user you want to ban.",
                color=0xE02B2B
            )
            await interaction.respond(embed=embed)

    @commands.slash_command(
        name="warn",
        description="Warns a user in the server."
        )
    @commands.has_permissions(manage_messages=True)
    @checks.not_blacklisted()
    async def warn(self, interaction: discord.ApplicationContext, user: Option(discord.User,"The user you want to warn."),
                  reason: Option(str, "The reason you warned the user.",default = "Not specified")) -> None:
        """
        Warns a user in his private messages.
        :param interaction: The application command interaction.
        :param user: The user that should be warned.
        :param reason: The reason for the warn. Default is "Not specified".
        """
        member = await interaction.guild.get_or_fetch_member(user.id)
        embed = discord.Embed(
            title="User Warned!",
            description=f"**{member}** was warned by **{interaction.author}**!",
            color=0x9C84EF
        )
        embed.add_field(
            name="Reason:",
            value=reason
        )
        await interaction.respond(embed=embed)
        try:
            await member.send(f"You were warned by **{interaction.author}**!\nReason: {reason}")
        except discord.Forbidden:
            # Couldn't send a message in the private messages of the user
            await interaction.respond(f"{member.mention}, you were warned by **{interaction.author}**!\nReason: {reason}")

    @commands.slash_command(
        name="purge",
        description="Delete a number of messages."
        )
    @commands.has_guild_permissions(manage_messages=True)
    @checks.not_blacklisted()
    async def purge(self, interaction: discord.ApplicationContext, amount: Option(int,"The amount of messages you want to delete. (Must be between 1 and 100.)",default=1)) -> None:
        """
        Delete a number of messages.

        :param interaction: The application command interaction.
        :param amount: The number of messages that should be deleted.
        """
        purged_messages = await interaction.channel.purge(limit=amount)
        embed = discord.Embed(
            title="Chat Cleared!",
            description=f"**{interaction.author}** cleared **{len(purged_messages)}** messages!",
            color=0x9C84EF
        )
        await interaction.respond(embed=embed)

    @commands.slash_command(
        name="hackban",
        description="Bans a user without the user having to be in the server."
        )
    @commands.has_permissions(ban_members=True)
    @checks.not_blacklisted()
    async def hackban(self, interaction: discord.ApplicationContext, user_id: Option(discord.User,"The ID of the user that should be banned."),
                  reason: Option(str, "The reason you banned the user.",default = "Not specified")) -> None:
        """
        Bans a user without the user having to be in the server.
        :param interaction: The application command interaction.
        :param user_id: The ID of the user that should be banned.
        :param reason: The reason for the ban. Default is "Not specified".
        """
        try:
            await self.bot.http.ban(user_id, interaction.guild.id, reason=reason)
            user = await self.bot.get_or_fetch_user(int(user_id))
            embed = discord.Embed(
                title="User Banned!",
                description=f"**{user} (ID: {user_id}) ** was banned by **{interaction.author}**!",
                color=0x9C84EF
            )
            embed.add_field(
                name="Reason:",
                value=reason
            )
            await interaction.respond(embed=embed)
        except Exception as e:
            embed = discord.Embed(
                title="Error!",
                description="An error occurred while trying to ban the user. Make sure ID is an existing ID that belongs to a user.",
                color=0xE02B2B
            )
            await interaction.respond(embed=embed)
            print(e)

def setup(bot):
    bot.add_cog(Moderation(bot))
