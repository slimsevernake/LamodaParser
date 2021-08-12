import LamodaBot.bot_settings as settings


def handle_tag(tag: str) -> None:
    splitted = tag.split()
    if len(splitted) > 1:
        if splitted[0] == "SKU:":
            return sku_handler(splitted[1])
        elif splitted[0] == "EXTENDED:":
            return smart_search_handler(splitted[1:])
        else:
            return standard_search_handler(tag)
    else:
        return None


# TODO: Remove with master. sku_handler method()
def standard_search_handler(tag):
    pass


# TODO: Remove with master. sku_search() method()
def sku_handler(tag: str):
    pass


# TODO: Remove with master. smart_search method()
def smart_search_handler(tags: list[str]):
    pass


# TODO: replace with handle_tag method.
async def process_product(product_tag: str, master: 'Master'):
    condition, sku = is_sku(product_tag)
    if condition:
        await master.async_process_product_by_sku(sku)
    else:
        await master.async_parse_product_by_tag(product_tag)


# TODO: remove this method.
def is_sku(tag: str):
    splitted = tag.split()
    if len(splitted) == 2:
        if splitted[0] == "SKU:":
            return True, splitted[1]
        else:
            return False, None
    else:
        return False, None