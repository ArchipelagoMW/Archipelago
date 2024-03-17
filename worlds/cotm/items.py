from BaseClasses import Item
from .data import iname
from .locations import base_id

from typing import TYPE_CHECKING, Dict, Union

if TYPE_CHECKING:
    from . import CotMWorld


class CotMItem(Item):
    game: str = "Castlevania Circle of the Moon"


# # #    KEY    # # #
# "code" = The unique part of the Item's AP code attribute, as well as the value to call the in-game "prepare item
#          textbox" function with to give the Item in-game. Add this + base_id to get the actual AP code.
# "default classification" = The AP Item Classification that gets assigned to instances of that Item in create_item
#                            by default, unless I deliberately override it (as is the case for some Special1s).
item_info = {
    iname.heart_max:   {"code": 0xE400, "default classification": "filler"},
    iname.hp_max:      {"code": 0xE401, "default classification": "filler"},
    iname.mp_max:      {"code": 0xE402, "default classification": "filler"},
    iname.salamander:  {"code": 0xE600, "default classification": "useful"},
    iname.serpent:     {"code": 0xE601, "default classification": "progression"},
    iname.mandragora:  {"code": 0xE602, "default classification": "useful"},
    iname.golem:       {"code": 0xE603, "default classification": "useful"},
    iname.cockatrice:  {"code": 0xE604, "default classification": "progression"},
    iname.griffin:     {"code": 0xE605, "default classification": "useful"},
    iname.manticore:   {"code": 0xE606, "default classification": "useful"},
    iname.thunderbird: {"code": 0xE607, "default classification": "useful"},
    iname.unicorn:     {"code": 0xE608, "default classification": "useful"},
    iname.black_dog:   {"code": 0xE609, "default classification": "useful"},
    iname.mercury:     {"code": 0xE60A, "default classification": "progression"},
    iname.venus:       {"code": 0xE60B, "default classification": "useful"},
    iname.jupiter:     {"code": 0xE60C, "default classification": "useful"},
    iname.mars:        {"code": 0xE60D, "default classification": "progression"},
    iname.diana:       {"code": 0xE60E, "default classification": "useful"},
    iname.apollo:      {"code": 0xE60F, "default classification": "useful"},
    iname.neptune:     {"code": 0xE610, "default classification": "useful"},
    iname.saturn:      {"code": 0xE611, "default classification": "useful"},
    iname.uranus:      {"code": 0xE612, "default classification": "useful"},
    iname.pluto:       {"code": 0xE613, "default classification": "useful"},
    iname.double:      {"code": 0xE801, "default classification": "progression"},
    iname.tackle:      {"code": 0xE802, "default classification": "progression"},
    iname.kick_boots:  {"code": 0xE803, "default classification": "progression"},
    iname.heavy_ring:  {"code": 0xE804, "default classification": "progression"},
    # Map
    iname.cleansing:   {"code": 0xE806, "default classification": "progression"},
    iname.roc_wing:    {"code": 0xE807, "default classification": "progression"},
    iname.last_key:    {"code": 0xE808, "default classification": "progression_skip_balancing"},
    iname.ironmaidens: {"default classification": "progression"},
    iname.victory:     {"default classification": "progression"}
}

filler_item_names = [iname.heart_max, iname.hp_max, iname.mp_max]


def get_item_info(item: str, info: str) -> Union[str, int, None]:
    return item_info[item].get(info, None)


def get_item_names_to_ids() -> Dict[str, int]:
    return {name: get_item_info(name, "code")+base_id for name in item_info if get_item_info(name, "code") is not None}


def get_item_counts(world: "CotMWorld") -> Dict[str, Dict[str, int]]:

    item_counts = {
        "progression": {},
        "progression_skip_balancing": {},
        "useful": {},
        "filler": {},
    }
    total_items = 0

    # Add one of each Item to the pool that is not filler or progression skip balancing.
    for item in item_info:
        classification = get_item_info(item, "default classification")
        code = get_item_info(item, "code")
        # Skip event Items.
        if code is None:
            continue
        if classification in ["filler", "progression_skip_balancing"]:
            item_counts[classification][item] = 0
            continue
        item_counts[classification][item] = 1
        total_items += 1

    # Add the total Last Keys.
    if not world.options.require_all_bosses:
        item_counts["progression_skip_balancing"][iname.last_key] = world.options.available_last_keys.value
        total_items += world.options.available_last_keys.value

    # Add filler items at random until the total items = the total locations.
    while total_items < len(world.multiworld.get_unfilled_locations(world.player)):
        item_counts["filler"][world.random.choice(filler_item_names)] += 1
        total_items += 1

    return item_counts


# //ENEMY DATA TABLE START: 0x000CB2B8
