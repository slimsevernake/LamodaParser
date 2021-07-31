import asyncio
import aiohttp
from discord import Embed, Webhook, AsyncWebhookAdapter
import datetime

import LamodaBot.bot_settings as settings


async def async_send_embed(embed: Embed):
    print(f"{datetime.datetime.now()} | Sending embed!")
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(settings.bot_settings['webhook'], adapter=AsyncWebhookAdapter(session))
        await webhook.send(embed=embed)


def send_embed(embed: Embed):
    asyncio.run(async_send_embed(embed))
