import typing
import string


from BaseClasses import Item, ItemClassification
from typing import Dict, Set

class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    classification: ItemClassification


class YachtDiceItem(Item):
    game: str = "Watery Words"


# the starting index is chosen semi-randomly to be 16871244000

letters = list(string.ascii_uppercase)
trap_letters = ["J", "Q", "X", "Z"]
item_table = {l: ItemData(1000209000+n, ItemClassification.progression | ItemClassification.trap) if l in trap_letters 
              else ItemData(1000209000+n, ItemClassification.progression) for n,l in enumerate(letters)}

item_table["Extra turn"] = ItemData(1000208999, ItemClassification.progression)
item_table["Word Length Bonus"] = ItemData(1000208998, ItemClassification.filler)
item_table["5 Letters"] = ItemData(1000208997, ItemClassification.progression)
item_table["5 Bonus Tiles"] = ItemData(1000208996, ItemClassification.progression)

possible_bonuses = ["×3W", "×2W", "×3L", "×2L"]
bonus_locations = [f"{i},{i}" for i in range(15)] \
                    + [f"{i},{i+8}" for i in range(7)] \
                    + [f"{i+8},{i}" for i in range(7)] \
                    + [f"{6-i},{i}" for i in range(7)] \
                    + [f"{14-i},{i}" for i in range(15)] \
                    + [f"{14-i},{8+i}" for i in range(7)] \
                    + ["7,1", "7,13"]
bonus_locations = list(set(bonus_locations))

bonus_item_list = []  # list of lists
id = 1000209100
for bl in bonus_locations:
    for pb in possible_bonuses:
        item_table[f"{pb} {bl}"] = ItemData(id, ItemClassification.progression)
        id += 1
    bonus_item_list.append([f"{pb} {bl}" for pb in possible_bonuses])  # add list

group_table: Dict[str, Set[str]] = {
    "Letters": letters,
    "Bonuses": [item for sublist in bonus_item_list for item in sublist]
}