import logging
import LamodaBot.bot_settings as settings
from discord.ext import tasks
from discord.ext.commands import Bot, Context
import app_logger
from Monitor import Monitor
from Manifests import manifest


logger = app_logger.get_logger("common", logging.DEBUG)

monitor = Monitor(manifest)
bot = Bot(command_prefix=settings.bot_settings['bot_prefix'])


@bot.command()
async def ping(ctx: Context):
    logger.info("pinged")
    monitor.product_db[list(monitor.product_db.keys())[0]].price = 100000000
    await ctx.send(content="pong")


@bot.event
async def on_ready():
    logger.info("bot initiated")


@tasks.loop()
async def async_monitor_products():
    logger.info("bot started monitoring cycle")
    await monitor.run()


try:
    async_monitor_products.before_loop(bot.wait_until_ready)
    async_monitor_products.start()
    bot.run(settings.bot_settings['token'])
except Exception as ex:
    logger.exception(ex)
