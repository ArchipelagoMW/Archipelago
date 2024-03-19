import logging

from BaseClasses import Item
from .data import iname
from .locations import base_id

from typing import TYPE_CHECKING, Dict, Union, List

if TYPE_CHECKING:
    from . import CVCotMWorld


class CVCotMItem(Item):
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

action_cards = {iname.mercury, iname.venus, iname.jupiter, iname.mars, iname.diana, iname.apollo, iname.neptune,
                iname.saturn, iname.uranus, iname.pluto}

attribute_cards = {iname.salamander, iname.serpent, iname.mandragora, iname.golem, iname.cockatrice, iname.griffin,
                   iname.manticore, iname.thunderbird, iname.unicorn, iname.black_dog}

filler_item_names = [iname.heart_max, iname.hp_max, iname.mp_max]


def get_item_info(item: str, info: str) -> Union[str, int, None]:
    return item_info[item].get(info, None)


def get_item_names_to_ids() -> Dict[str, int]:
    return {name: get_item_info(name, "code")+base_id for name in item_info if get_item_info(name, "code") is not None}


def get_item_counts(world: "CVCotMWorld") -> Dict[str, Dict[str, int]]:

    item_counts = {
        "progression": {},
        "progression_skip_balancing": {},
        "useful": {},
        "filler": {},
    }
    total_items = 0
    excluded_cards = []

    # If Halve DSS Cards Placed is on, determine which cards we will exclude here.
    if world.options.halve_dss_cards_placed:
        excluded_cards = list(action_cards.union(attribute_cards))
        freeze_actions = [iname.mercury, iname.mars]
        freeze_attrs = [iname.serpent, iname.cockatrice]
        has_freeze_action = False
        has_freeze_attr = False
        start_card_cap = 8

        start_cards = [item for item in world.options.start_inventory_from_pool.value if "Card" in item]

        # Check for ice/stone cards that are in the player's starting cards. Increase the starting card capacity by 1
        # for each card type satisfied.
        for card in start_cards:
            if card in freeze_actions and not has_freeze_action:
                has_freeze_action = True
                start_card_cap += 1
            if card in freeze_attrs and not has_freeze_attr:
                has_freeze_attr = True
                start_card_cap += 1

        # If we are over our starting card capacity, some starting cards will need to be removed...
        if len(start_cards) > start_card_cap:
            kept_start_cards = []
            removed_start_cards = []

            # Remove all but the ice/stone cards; these we'll keep no matter what.
            for card in start_cards:
                if card in freeze_actions + freeze_attrs:
                    kept_start_cards.append(card)
                else:
                    removed_start_cards.append(card)

            # Continue re-adding the removed start cards at random until we are back at the starting card capacity.
            while len(kept_start_cards) < start_card_cap:
                returned_card = world.random.choice(removed_start_cards)
                kept_start_cards.append(returned_card)
                removed_start_cards.remove(returned_card)

            # Remove the cards we're not keeping from start_inventory_from_pool.
            for card in removed_start_cards:
                del world.options.start_inventory_from_pool.value[card]
            start_cards = kept_start_cards

            logging.warning(f"[{world.multiworld.player_name[world.player]}] Too many DSS Cards in "
                            f"start_inventory_from_pool to satisfy the Halve DSS Cards Placed option. The following "
                            f"{len(removed_start_cards)} card(s) were removed: {removed_start_cards}")

        # Remove the starting cards from the excluded cards.
        for card in action_cards.union(attribute_cards):
            if card in start_cards:
                excluded_cards.remove(card)

        # Remove a valid ice/stone action and/or attribute card if the player isn't starting with one.
        if not has_freeze_action:
            excluded_cards.remove(world.random.choice(freeze_actions))
        if not has_freeze_attr:
            excluded_cards.remove(world.random.choice(freeze_attrs))

        # Remove 10 random cards from the exclusions.
        excluded_cards = world.random.sample(excluded_cards, 10)

    # Add one of each Item to the pool that is not filler or progression skip balancing.
    for item in item_info:
        classification = get_item_info(item, "default classification")
        code = get_item_info(item, "code")

        # Skip event Items and cards that are excluded with Halve DSS Cards Placed.
        if code is None or item in excluded_cards:
            continue

        # Classify the Cleansing as Useful instead of Progression if Ignore Cleansing is on.
        if item == iname.cleansing and world.options.ignore_cleansing:
            classification = "useful"

        if classification in ["filler", "progression_skip_balancing"]:
            item_counts[classification][item] = 0
            continue
        item_counts[classification][item] = 1
        total_items += 1

    # Add the total Last Keys.
    if not world.options.require_all_bosses:
        item_counts["progression_skip_balancing"][iname.last_key] = world.options.available_last_keys.value
        total_items += world.options.available_last_keys.value

    # Add filler items at random until the total Items = the total Locations.
    while total_items < len(world.multiworld.get_unfilled_locations(world.player)):
        item_counts["filler"][world.random.choice(filler_item_names)] += 1
        total_items += 1

    return item_counts


# //ENEMY DATA TABLE START: 0x000CB2B8
