from discord import Embed


def get_field_index_by_name(embed: Embed, name: str) -> int:
    for field_index in range(len(embed.fields)):
        if embed.fields[field_index].name == name:
            return field_index
    return -1
