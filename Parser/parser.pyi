from logging import Logger
import Modules.Product
from typing import Optional

def search(tag : str, pages: int) -> list[Modules.Product]: ...
def parse_product(url : str, short_url : bool) -> Optional[Modules.Product]: ...
def product_by_sku(sku: str, ) -> Optional[Modules.Product]: ...
def smart_search(pattern: str, pages: int) -> list[Modules.Product]: ...