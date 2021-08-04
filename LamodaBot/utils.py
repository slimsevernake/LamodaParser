import LamodaBot.bot_settings as settings


def is_sku(tag: str):
    splitted = tag.split()
    if len(splitted) == 2:
        if splitted[0] == "SKU:":
            return True, splitted[1]
        else:
            return False, None
    else:
        return False, None


async def process_product(product_tag: str, master: 'Master'):
    condition, sku = is_sku(product_tag)
    if condition:
        await master.async_process_product_by_sku(sku)
    else:
        await master.async_parse_product_by_tag(product_tag)


def has_forbidden_piece(product: 'Product') -> bool:
    for piece in settings.forbidden_pieces:
        if product.name.find(piece.lower()) != -1:
            return True
    return False
