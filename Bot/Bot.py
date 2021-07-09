import asyncio
import aiohttp
from discord import Embed, Webhook, AsyncWebhookAdapter
from discord.ext.commands import Bot, Context

from Master.Master import Master

TOKEN = "ODYzMDY0ODUxMzIzNjgyODM3.YOhdxw.8gojlvpfcXGV9NSZRa12uEdXEbo"
WEBHOOK = "https://discord.com/api/webhooks/863035045953142815/bO2O8DDqbvL" \
          "-MALvNPJqcfyvtyI__1HMrYRdG_MdkAw2rSwzztuX_G6nw7t3lMWIlijw "

bot = Bot(command_prefix="!")
master = Master()


@bot.command()
async def product(ctx: Context, product_tag: str):
    data = master.parse_product_by_tag(product_tag)
    await ctx.send(data)


async def async_send_embed(embed: Embed):
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(WEBHOOK, adapter=AsyncWebhookAdapter(session))
        await webhook.send(embed=embed)


def send_embed(embed: Embed):
    asyncio.run(async_send_embed(embed))


bot.run(TOKEN)
