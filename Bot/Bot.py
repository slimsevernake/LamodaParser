import discord
from discord import Embed
from discord.ext.commands import Bot

TOKEN = "https://discord.com/api/webhooks/863035045953142815/bO2O8DDqbvL-MALvNPJqcfyvtyI__1HMrYRdG_MdkAw2rSwzztuX_G6nw7t3lMWIlijw"
bot = Bot(command_prefix="!")


@bot.command()
async def product(ctx, product_name: str):
    embed = Embed(title="adasdasd")
    embed.add_field("Title", product.title)
    #TODO: embed.add_field("URL", ..)
    #TODO: emdeb.add_field("Image", ..)
    await ctx.send(embed)

bot.run(TOKEN)