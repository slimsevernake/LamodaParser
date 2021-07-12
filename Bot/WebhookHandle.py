import asyncio
import aiohttp
from discord import Embed, Webhook, AsyncWebhookAdapter

from settings import settings


async def async_send_embed(embed: Embed):
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(settings['webhook'], adapter=AsyncWebhookAdapter(session))
        await webhook.send(embed=embed)


def send_embed(embed: Embed):
    asyncio.run(async_send_embed(embed))
