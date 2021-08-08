import datetime
import logging
from datetime import time

import LamodaBot.bot_settings as settings
from discord.ext import tasks
from discord.ext.commands import Bot, Context
import LamodaBot.utils as utils
import app_logger
from Master.monitor import Monitor
from Master.WebhookHandle import async_send_embed
import manifests.test_manifest as manifest


logger = app_logger.get_logger("common", logging.INFO)

monitor = Monitor(manifest)
bot = Bot(command_prefix=settings.bot_settings['bot_prefix'])


@bot.command()
async def ping(ctx: Context):
    logger.info("pinged")
    await ctx.send(content="pong")


@bot.event
async def on_ready():
    logger.info("bot initiated")


@tasks.loop(seconds=settings.bot_settings['monitor_loop_time'])
async def async_monitor_products():
    logger.info("bot started monitoring cycle")

    monitor.monitor_cycle()


@tasks.loop(seconds=settings.bot_settings['update_tags_loop_time'])
async def async_monitor_update():
    for product_tag in settings.products_to_monitor:
        await utils.process_product(product_tag, monitor)

# async_monitor_products.before_loop(bot.wait_until_ready)
# async_monitor_update.before_loop(bot.wait_until_ready)

try:
    async_monitor_products.start()
    async_monitor_update.start()

    bot.run(settings.bot_settings['token'])
except Exception as ex:
    logger.exception(ex)
    # print(ex)


# @bot.command()
# async def product(ctx: Context, *, product_tag: str):
#     data = await master.async_parse_product_by_tag(product_tag)
#     for product in data:
#         await ctx.send(embed=product.to_embed())
