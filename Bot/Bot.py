import random
import settings

from discord.ext import tasks
from discord.ext.commands import Bot, Context

from Master.Master import Master
from WebhookHandle import async_send_embed

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


@bot.event
async def on_ready():
    print("==================| Bot initiated |====================")
    for product_tag in settings.products_to_monitor:
        await master.async_parse_product_by_tag(product_tag)

    print("==================| Bot started parsing products |====================")
    for product in master.product_db:
        await async_send_embed(product.to_embed())
        # DEBUG
        print(product)
    print("==================| Bot parsed all products |====================")


@tasks.loop(seconds=settings.bot_settings['monitor_loop_time'])
async def async_monitor_products():
    # пройти по всем сохраненным элементам и проверить на изменения
    print("==================| Bot started monitoring cycle |====================")
    await master.monitor_products()


# @tasks.loop(minutes=settings.bot_settings['update_tags_loop_time'])
# async def async_monitor_update():
#     for product_tag in settings.products_to_monitor:
#         await master.async_parse_product_by_tag(product_tag)


# TODO: REMOVE METHOD!!!
@tasks.loop(hours=10)
async def async_update_products_test():
    if len(master.product_db) == 0:
        return
    random_product = random.randint(0, len(master.product_db) - 1)
    master.product_db[random_product].price = random.randint(100, 500000)


# async_monitor_products.before_loop(bot.wait_until_ready)
# async_monitor_update.before_loop(bot.wait_until_ready)
async_update_products_test.before_loop(bot.wait_until_ready)

async_monitor_products.start()
# async_monitor_update.start()
async_update_products_test.start()

bot.run(settings.bot_settings['token'])
