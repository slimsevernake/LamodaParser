import LamodaBot.bot_settings as settings
from discord.ext import tasks
from discord.ext.commands import Bot, Context

import app_logger
from Master.Master import Master
from Master.WebhookHandle import async_send_embed


logger = app_logger.get_logger(__name__)
bot = Bot(command_prefix=settings.bot_settings['bot_prefix'])
master = Master()


@bot.command()
async def product(ctx: Context, *, product_tag: str):
    data = await master.async_parse_product_by_tag(product_tag)
    for product in data:
        await ctx.send(embed=product.to_embed())


@bot.command()
async def check(ctx: Context):
    # print(master.product_db)
    print(len(master.product_db))
    # for el in master.product_db:
    #     await async_send_embed(el.to_embed())
    #     print(el)


def is_sku(tag: str):
    splitted = tag.split()
    if len(splitted) == 2:
        if splitted[0] == "SKU:":
            return True, splitted[1]
        else:
            return False, None
    else:
        return False, None


@bot.event
async def on_ready():
    logger.info("bot initiated")
    for product_tag in settings.products_to_monitor:
        condition, sku = is_sku(product_tag)
        if condition:
            await master.async_process_product_by_sku(sku)
        else:
            await master.async_parse_product_by_tag(product_tag)

    logger.info("bot started parsing products")

    for product in master.product_db:
        await async_send_embed(product.to_embed())
        # DEBUG
        logger.debug(product)

    logger.info("bot parsed all products")


@tasks.loop(seconds=settings.bot_settings['monitor_loop_time'])
async def async_monitor_products():
    # пройти по всем сохраненным элементам и проверить на изменения
    logger.info("bot started monitoring cycle")
    await master.monitor_products()


@tasks.loop(minutes=settings.bot_settings['update_tags_loop_time'])
async def async_monitor_update():
    for product_tag in settings.products_to_monitor:
        await master.async_parse_product_by_tag(product_tag)

# async_monitor_products.before_loop(bot.wait_until_ready)
# async_monitor_update.before_loop(bot.wait_until_ready)

async_monitor_products.start()
async_monitor_update.start()

bot.run(settings.bot_settings['token'])
