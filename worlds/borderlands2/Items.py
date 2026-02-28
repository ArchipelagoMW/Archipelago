# TODO delete this file?
# from typing import Dict, NamedTuple, Optional

from BaseClasses import Item, ItemClassification
# from .archi_defs import item_name_to_id

# bl2_base_id: int = 2388000


class Borderlands2Item(Item):
    game = "Borderlands 2"


# class Borderlands2ItemData(NamedTuple):
#     code: Optional[int] = None
#     type: ItemClassification = ItemClassification.filler
#     description: Optional[str] = None
#     name: str = ""


# p_items = {
#     "Melee", "Crouch", "Common Pistol", "Vehicle Fire",
#     "Progressive Jump", "Progressive Money Cap", "Progressive Sprint",
#     "Unique Relic", "Reward Agony: The Amulet"
# }
# p_items = {}
# u_items = {"Gear Leveler", "Common Shield", "Common Pistol", "Common SMG"}

    

# u_items = {}

# item_data_table: Dict[str, Borderlands2ItemData] = {
#     name: Borderlands2ItemData(
#         code=bl2_base_id + item_id,
#         type=ItemClassification.progression if name in p_items or name.startswith("Travel")
#         else ItemClassification.useful if name in u_items
#         else ItemClassification.trap if name.startswith("Trap")
#         else ItemClassification.filler,
#         description="",
#         name=name,
#     )
#     for name, item_id in item_name_to_id.items()
# }

# gear_rarities = [
#     "Common",
#     "Uncommon",
#     "Rare",
#     "VeryRare",
#     "Legendary",
#     "Seraph",
#     "Rainbow",
#     "Pearlescent",
#     "Unique",
# ]
#
# gear_kinds = [
#     "Shield",
#     "GrenadeMod",
#     "ClassMod",
#     "Relic",
#     "Pistol",
#     "Shotgun",
#     "SMG",
#     "SniperRifle",
#     "AssaultRifle",
#     "RocketLauncher",
# ]
