from . import databases
from .address import *

def apply(env):
    prices = []
    megaprices = {}

    items_dbview = databases.get_items_dbview()
    altered_item_prices = env.meta.get('altered_item_prices', {})
    for item_code in range(0x100):
        if env.options.flags.has('shops_free'):
            price = 0
        elif item_code in altered_item_prices:
            price = altered_item_prices[item_code]
        else:
            item = items_dbview.find_one(lambda it: it.code == item_code)
            price = (item.price if item else 0)

        if price > 126000:
            prices.append(0xFF)
            megaprices[item_code] = price
        elif price > 1270:
            if price % 1000:
                new_price = 1000 * (price // 1000)
                print(f"WARNING: {item.const} has non-representable cost {price}; rounding to {new_price}")
                price = new_price
            prices.append(0x80 | (price // 1000))
        else:
            if price % 10:
                new_price = 10 * (price // 10)
                print(f"WARNING: {item.const} has non-representable cost {price}; rounding to {new_price}")
                price = new_price
            prices.append(price // 10)

    env.add_binary(UnheaderedAddress(0x7A450), prices, as_script=True)
    
    megaprice_bytes = []
    for item_code in megaprices:
        price = megaprices[item_code]
        megaprice_bytes.append(item_code)
        megaprice_bytes.extend([((price >> (i * 8)) & 0xFF) for i in range(3)])
    megaprice_bytes.append(0x00)

    env.add_binary(BusAddress(0x218080), megaprice_bytes, as_script=True)
