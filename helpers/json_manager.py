import json

def add_to_blacklist(guild_id: int,json_key: str,object_id: int) -> None:
    """
    This function will add a user/channel based on its ID in the blacklist.json file.
    :param user_id: The ID of the user/channel that should be added into the blacklist.json file.
    """
    with open("blacklist.json", "r+") as file:
        file_data = json.load(file)
        file_data[guild_id][json_key].append(object_id)
    with open("blacklist.json", "w") as file:
        file.seek(0)
        json.dump(file_data, file, indent=4)


def remove_from_blacklist(guild_id: int,json_key: str,object_id: int) -> None:
    """
    This function will remove a user/channel based on its ID from the blacklist.json file.
    :param user_id: The ID of the user/channel that should be removed from the blacklist.json file.
    """
    with open("blacklist.json", "r") as file:
        file_data = json.load(file)
        file_data[guild_id][json_key].remove(object_id)
    with open("blacklist.json", "w") as file:
        file.seek(0)
        json.dump(file_data, file, indent=4)

def get_color(guild_id):
        with open("guild.json") as file:
            guild = json.load(file)

        color=guild[str(guild_id)]["color"]

        return color