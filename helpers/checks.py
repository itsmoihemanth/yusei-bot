import json
from typing import TypeVar,Callable

from discord.ext import commands

from exceptions import *

T = TypeVar("T")

def is_owner() -> Callable[[T], T]:
  
    async def predicate(context: commands.Context) -> bool:
        with open("config.json") as file:
            data = json.load(file)
        if context.author.id not in data["owners"] or context.author.id != context.guild.owner_id:
            raise UserNotOwner
        return True

    return commands.check(predicate)

def not_blacklisted() -> Callable[[T], T]:

    async def predicate(context: commands.Context) -> bool:
        with open("blacklist.json") as file:
            data = json.load(file)
        if context.author.id in data["user_ids"]:
            raise UserBlacklisted
        if context.channel.id in data["channel_ids"]:
            raise ChannelBlacklisted
        return True

    return commands.check(predicate)