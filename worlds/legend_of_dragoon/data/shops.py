from dataclasses import dataclass
from enum import Enum


class ShopType(Enum):
    EQUIPMENT= 0
    ITEM = 1
    NONE= 2
    OTHER = 3

@dataclass
class Shop:
    key: str
    display_name: str
    slot_count: int
    shop_type: ShopType

shop_locations = [
    Shop("bale_equipment_shop", "Bale Equipment Shop", 10, ShopType.EQUIPMENT),
    Shop("serdio_item_shop", "Serdio Item Shop", 7, ShopType.ITEM),
    Shop("lohan_equipment_shop", "Lohan Equipment Shop", 12, ShopType.EQUIPMENT),
    Shop("lohan_item_shop", "Lohan Item Shop", 8, ShopType.ITEM),
    Shop("kazas_equipment_shop", "Kazas Equipment Shop", 4, ShopType.EQUIPMENT),
    Shop("kazas_fort_item_shop", "Kazas Item Shop", 5, ShopType.ITEM),
    Shop("fletz_equipment_shop", "Fletz Equipment Shop", 10, ShopType.EQUIPMENT),
    Shop("fletz_item_shop", "Fletz Item Shop", 9, ShopType.ITEM),
    Shop("donau_equipment_shop", "Donau Equipment Shop", 2, ShopType.EQUIPMENT),
    Shop("donau_item_shop", "Donau Item Shop", 6, ShopType.ITEM),
    Shop("queen_fury_equipment_shop", "Queen Fury Equipment Shop", 5, ShopType.EQUIPMENT),
    Shop("queen_fury_item_shop", "Queen Fury Item Shop", 8, ShopType.ITEM),
    Shop("fueno_equipment_shop", "Fueno Equipment Shop", 6, ShopType.EQUIPMENT),
    Shop("fueno_item_shop", "Fueno Item Shop", 8, ShopType.ITEM),
    Shop("furni_equipment_shop", "Furni Equipment Shop", 6, ShopType.EQUIPMENT),
    Shop("furni_item_shop", "Furni Item Shop", 5, ShopType.ITEM),
    Shop("deningrad_equipment_shop", "Deningrad Equipment Shop", 12, ShopType.EQUIPMENT),
    Shop("deningrad_item_shop", "Deningrad Item Shop", 10, ShopType.ITEM),
    Shop("wingly_forest_equipment_shop", "Wingly Forest Equipment Shop", 4, ShopType.EQUIPMENT),
    Shop("wingly_forest_item_shop", "Wingly Forest Item Shop", 8, ShopType.ITEM),
    Shop("vellweb_equipment_shop", "Vellweb Equipment Shop", 5, ShopType.EQUIPMENT),
    Shop("vellweb_item_shop", "Vellweb Item Shop", 7, ShopType.ITEM),
    Shop("ulara_equipment_shop", "Ulara Equipment Shop", 9, ShopType.EQUIPMENT),
    Shop("ulara_item_shop", "Ulara Item Shop", 11, ShopType.ITEM),
    Shop("rouge_equipment_shop", "Rouge Equipment Shop", 3, ShopType.EQUIPMENT),
    Shop("rouge_item_shop", "Rouge Item Shop", 7, ShopType.ITEM),
    Shop("moon_equipment_shop", "Moon Equipment Shop", 16, ShopType.EQUIPMENT),
    Shop("moon_item_shop", "Moon Item Shop", 9, ShopType.ITEM),
    Shop("hellena_01_item_shop", "Hellena 01 Item Shop", 3, ShopType.OTHER),
    Shop("kashua_equipment_shop", "Kashua Equipment Shop", 7, ShopType.EQUIPMENT),
    Shop("kashua_item_shop", "Kashua Item Shop", 6, ShopType.ITEM),
    Shop("fletz_accessory_shop", "Fletz Accessory Shop", 4, ShopType.EQUIPMENT),
    Shop("forest_item_shop", "Forest Item Shop", 4, ShopType.ITEM),
    Shop("kazas_fort_equipment_shop", "Kazas Fort Equipment Shop", 2, ShopType.EQUIPMENT),
    Shop("volcano_item_shop", "Volcano Item Shop", 7, ShopType.ITEM),
    Shop("zenebatos_equipment_shop", "Zenebatos Equipment Shop", 9, ShopType.EQUIPMENT),
    Shop("zenebatos_item_shop", "Zenebatos Item Shop", 8, ShopType.ITEM),
    Shop("hellena_02_item_shop", "Hellena 02 Item Shop", 6, ShopType.OTHER),
    Shop("unknown_shop_01", "Unknown Shop 01", 3, ShopType.EQUIPMENT),
    Shop("empty_shop", "Empty Shop", 0, ShopType.EQUIPMENT),
]