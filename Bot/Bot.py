from discord import Webhook, AsyncWebhookAdapter
import aiohttp
import asyncio
from Parser import parser
import time
WEBHOOK = "https://discord.com/api/webhooks/863035045953142815/bO2O8DDqbvL-MALvNPJqcfyvtyI__1HMrYRdG_MdkAw2rSwzztuX_G6nw7t3lMWIlijw"


async def kek(product):
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(WEBHOOK, adapter=AsyncWebhookAdapter(session))
        e = product.to_embed()
        await webhook.send(embed=e)


res = parser.search("CHUCK 70")
for i in res:
    asyncio.run(kek(i))
    time.sleep(1)
