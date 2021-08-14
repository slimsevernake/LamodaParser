from discord import Embed
from Master.ProductChangeEvent import *


class EmbedEditor:
    @staticmethod
    def update_embed_field(embed: 'Embed', value: str, name: 'str'):
        field_index = EmbedEditor.get_field_index_by_name(embed, name)
        if field_index == -1:
            return None
        embed.insert_field_at(field_index,
                              name=name,
                              value=value,
                              inline=False)
        embed.remove_field(field_index + 1)

    @staticmethod
    def get_field_index_by_name(embed: Embed, name: str) -> int:
        for field_index in range(len(embed.fields)):
            if embed.fields[field_index].name == name:
                return field_index
        return -1
