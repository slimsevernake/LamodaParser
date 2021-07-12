from discord.ext import tasks
from discord.ext.commands import Bot, Context

from settings import settings

from Master.Master import Master

LOOP_TIME = 10  # seconds TODO: change to minutes or hours

bot = Bot(command_prefix=settings['bot_prefix'])
master = Master()


@bot.command()
async def product(ctx: Context, *, product_tag: str):
    data = await master.async_parse_product_by_tag(product_tag)
    for product in data:
        await ctx.send(embed=product.to_embed())


@tasks.loop(hours=LOOP_TIME)
async def async_monitor_products():
    # пройти по всем сохраненным элементам и проверить на изменения
    master.monitor_products()


bot.run(settings['token'])
