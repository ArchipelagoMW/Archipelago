from .blockers import Blockers
from .diy import DIYItems
from .events import Events
from .expansion import Expansions
from .filler import Fillers
from .ghost import RandomGhosts
from .shop_licenses import BoosterPackItems, AccessoriesItems, FigurineItems, TableTopItems
from .traps import Traps
from .workers import Workers
from .. import ItemTypeEnum, ItemData


def get_shop_items(shop: type[ItemTypeEnum]) -> list[ItemData]:
    return [
        ItemData(
            type=item,
            amount=2 if item.value.startswith("Progressive ") else 1
        )
        for item in shop
    ]


booster_pack_items: list[ItemData] = get_shop_items(BoosterPackItems)
accessories_items: list[ItemData] = get_shop_items(AccessoriesItems)
figurine_items: list[ItemData] = get_shop_items(FigurineItems)
tabletop_items: list[ItemData] = get_shop_items(TableTopItems)


diy_items: list[ItemData] = [
    ItemData(DIYItems.PROGRESSIVE_CARD_TABLE, 2),
    ItemData(DIYItems.PROGRESSIVE_CARD_DISPLAY, 3),
    ItemData(DIYItems.PROGRESSIVE_PERSONAL_SHELF, 3),
    ItemData(DIYItems.PROGRESSIVE_AUTO_SCENT, 3),
    ItemData(DIYItems.PROGRESSIVE_WAREHOUSE_SHELF, 2),
    ItemData(DIYItems.PROGRESSIVE_WALL_DISPLAY_CASE, 5),
    ItemData(DIYItems.PROGRESSIVE_CARD_PROJECTOR, 3),
    ItemData(DIYItems.PROGRESSIVE_PACK_OPENER, 3),
    ItemData(DIYItems.PROGRESSIVE_SHELF, 5),
    ItemData(DIYItems.PROGRESSIVE_PLAY_TABLE, 3),
    ItemData(DIYItems.WORKBENCH),
    ItemData(DIYItems.TRASH_BIN),
    ItemData(DIYItems.CHECKOUT_COUNTER),
    ItemData(DIYItems.PROGRESSIVE_LARGE_SHELF, 4),
    ItemData(DIYItems.TOURNAMENT_PRIZE_SHELF),
    ItemData(DIYItems.SCANNER),
    ItemData(DIYItems.EMPTY_BOX_STORAGE),
    ItemData(DIYItems.BULK_DONATION_BOX),
    ItemData(DIYItems.CARD_STORAGE_SHELF),
]

expansion_items: list[ItemData] = [
    ItemData(Expansions.SHOP_EXPANSION, 30),
    ItemData(Expansions.WAREHOUSE_EXPANSION, 15),
]

worker_items: list[ItemData] = [
    ItemData(worker) for worker in Workers
]


event_items: list[ItemData] = [
    ItemData(event) for event in Events
]

all_items: list[ItemTypeEnum] = [
    *Blockers,
    *DIYItems,
    *Events,
    *Expansions,
    *Fillers,
    *RandomGhosts,
    *BoosterPackItems,
    *AccessoriesItems,
    *FigurineItems,
    *TableTopItems,
    *Traps,
    *Workers,
]
