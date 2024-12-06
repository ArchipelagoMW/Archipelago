import logging

from BaseClasses import Item, ItemClassification
from .data import iname
from .locations import BASE_ID
from .options import IronMaidenBehavior

from typing import TYPE_CHECKING, Dict, NamedTuple, Optional
from collections import Counter

if TYPE_CHECKING:
    from . import CVCotMWorld


class CVCotMItem(Item):
    game: str = "Castlevania - Circle of the Moon"


class CVCotMItemData(NamedTuple):
    code: Optional[int]
    text_id: Optional[bytes]
    default_classification: ItemClassification
    tutorial_id: Optional[bytes] = None
# "code" = The unique part of the Item's AP code attribute, as well as the value to call the in-game "prepare item
#          textbox" function with to give the Item in-game. Add this + base_id to get the actual AP code.
# "text_id" = The textbox ID for the vanilla message for receiving the Item. Used when receiving an Item through the
#             client that was not sent by a different player.
# "default_classification" = The AP Item Classification that gets assigned to instances of that Item in create_item
#                            by default, unless I deliberately override it (as is the case for the Cleansing on the
#                            Ignore Cleansing option).
# "tutorial_id" = The textbox ID for the item's tutorial. Used by the client if tutorials are not skipped.


cvcotm_item_info: Dict[str, CVCotMItemData] = {
    iname.heart_max:      CVCotMItemData(0xE400, b"\x57\x81", ItemClassification.filler),
    iname.hp_max:         CVCotMItemData(0xE401, b"\x55\x81", ItemClassification.filler),
    iname.mp_max:         CVCotMItemData(0xE402, b"\x56\x81", ItemClassification.filler),
    iname.salamander:     CVCotMItemData(0xE600, b"\x1E\x82", ItemClassification.useful),
    iname.serpent:        CVCotMItemData(0xE601, b"\x1F\x82", ItemClassification.useful |
                                         ItemClassification.progression),
    iname.mandragora:     CVCotMItemData(0xE602, b"\x20\x82", ItemClassification.useful),
    iname.golem:          CVCotMItemData(0xE603, b"\x21\x82", ItemClassification.useful),
    iname.cockatrice:     CVCotMItemData(0xE604, b"\x22\x82", ItemClassification.useful |
                                         ItemClassification.progression),
    iname.manticore:      CVCotMItemData(0xE605, b"\x23\x82", ItemClassification.useful),
    iname.griffin:        CVCotMItemData(0xE606, b"\x24\x82", ItemClassification.useful),
    iname.thunderbird:    CVCotMItemData(0xE607, b"\x25\x82", ItemClassification.useful),
    iname.unicorn:        CVCotMItemData(0xE608, b"\x26\x82", ItemClassification.useful),
    iname.black_dog:      CVCotMItemData(0xE609, b"\x27\x82", ItemClassification.useful),
    iname.mercury:        CVCotMItemData(0xE60A, b"\x28\x82", ItemClassification.useful |
                                         ItemClassification.progression),
    iname.venus:          CVCotMItemData(0xE60B, b"\x29\x82", ItemClassification.useful),
    iname.jupiter:        CVCotMItemData(0xE60C, b"\x2A\x82", ItemClassification.useful),
    iname.mars:           CVCotMItemData(0xE60D, b"\x2B\x82", ItemClassification.useful |
                                         ItemClassification.progression),
    iname.diana:          CVCotMItemData(0xE60E, b"\x2C\x82", ItemClassification.useful),
    iname.apollo:         CVCotMItemData(0xE60F, b"\x2D\x82", ItemClassification.useful),
    iname.neptune:        CVCotMItemData(0xE610, b"\x2E\x82", ItemClassification.useful),
    iname.saturn:         CVCotMItemData(0xE611, b"\x2F\x82", ItemClassification.useful),
    iname.uranus:         CVCotMItemData(0xE612, b"\x30\x82", ItemClassification.useful),
    iname.pluto:          CVCotMItemData(0xE613, b"\x31\x82", ItemClassification.useful),
    # Dash Boots
    iname.double:         CVCotMItemData(0xE801, b"\x59\x81", ItemClassification.useful |
                                         ItemClassification.progression, b"\xF4\x84"),
    iname.tackle:         CVCotMItemData(0xE802, b"\x5A\x81", ItemClassification.progression, b"\xF5\x84"),
    iname.kick_boots:     CVCotMItemData(0xE803, b"\x5B\x81", ItemClassification.progression, b"\xF6\x84"),
    iname.heavy_ring:     CVCotMItemData(0xE804, b"\x5C\x81", ItemClassification.progression, b"\xF7\x84"),
    # Map
    iname.cleansing:      CVCotMItemData(0xE806, b"\x5D\x81", ItemClassification.progression, b"\xF8\x84"),
    iname.roc_wing:       CVCotMItemData(0xE807, b"\x5E\x81", ItemClassification.useful |
                                         ItemClassification.progression, b"\xF9\x84"),
    iname.last_key:       CVCotMItemData(0xE808, b"\x5F\x81", ItemClassification.progression_skip_balancing,
                                         b"\xFA\x84"),
    iname.ironmaidens:    CVCotMItemData(0xE809, b"\xF1\x84", ItemClassification.progression),
    iname.dracula:        CVCotMItemData(None, None, ItemClassification.progression),
    iname.shinning_armor: CVCotMItemData(None, None, ItemClassification.progression),
}

ACTION_CARDS = {iname.mercury, iname.venus, iname.jupiter, iname.mars, iname.diana, iname.apollo, iname.neptune,
                iname.saturn, iname.uranus, iname.pluto}

ATTRIBUTE_CARDS = {iname.salamander, iname.serpent, iname.mandragora, iname.golem, iname.cockatrice, iname.griffin,
                   iname.manticore, iname.thunderbird, iname.unicorn, iname.black_dog}

FREEZE_ACTIONS = [iname.mercury, iname.mars]
FREEZE_ATTRS = [iname.serpent, iname.cockatrice]

FILLER_ITEM_NAMES = [iname.heart_max, iname.hp_max, iname.mp_max]

MAJORS_CLASSIFICATIONS = ItemClassification.progression | ItemClassification.useful


def get_item_names_to_ids() -> Dict[str, int]:
    return {name: cvcotm_item_info[name].code + BASE_ID for name in cvcotm_item_info
            if cvcotm_item_info[name].code is not None}


def get_item_counts(world: "CVCotMWorld") -> Dict[ItemClassification, Dict[str, int]]:

    item_counts: Dict[ItemClassification, Counter[str, int]] = {
        ItemClassification.progression: Counter(),
        ItemClassification.progression_skip_balancing: Counter(),
        ItemClassification.useful | ItemClassification.progression: Counter(),
        ItemClassification.useful: Counter(),
        ItemClassification.filler: Counter(),
    }
    total_items = 0
    # Items to be skipped over in the main Item creation loop.
    excluded_items = [iname.hp_max, iname.mp_max, iname.heart_max, iname.last_key]

    # If Halve DSS Cards Placed is on, determine which cards we will exclude here.
    if world.options.halve_dss_cards_placed:
        excluded_cards = list(ACTION_CARDS.union(ATTRIBUTE_CARDS))

        has_freeze_action = False
        has_freeze_attr = False
        start_card_cap = 8

        # Get out all cards from start_inventory_from_pool that the player isn't starting with 0 of.
        start_cards = [item for item in world.options.start_inventory_from_pool.value if "Card" in item]

        # Check for ice/stone cards that are in the player's starting cards. Increase the starting card capacity by 1
        # for each card type satisfied.
        for card in start_cards:
            if card in FREEZE_ACTIONS and not has_freeze_action:
                has_freeze_action = True
                start_card_cap += 1
            if card in FREEZE_ATTRS and not has_freeze_attr:
                has_freeze_attr = True
                start_card_cap += 1

        # If we are over our starting card capacity, some starting cards will need to be removed...
        if len(start_cards) > start_card_cap:

            # Ice/stone cards will be kept no matter what. As for the others, put them in a list of possible candidates
            # to remove.
            kept_start_cards = []
            removal_candidates = []
            for card in start_cards:
                if card in FREEZE_ACTIONS + FREEZE_ATTRS:
                    kept_start_cards.append(card)
                else:
                    removal_candidates.append(card)

            # Add a random sample of the removal candidate cards to our kept cards list.
            kept_start_cards += world.random.sample(removal_candidates, start_card_cap - len(kept_start_cards))

            # Make a list of the cards we are not keeping.
            removed_start_cards = [card for card in removal_candidates if card not in kept_start_cards]

            # Remove the cards we're not keeping from start_inventory_from_pool.
            for card in removed_start_cards:
                del world.options.start_inventory_from_pool.value[card]

            logging.warning(f"[{world.player_name}] Too many DSS Cards in "
                            f"Start Inventory from Pool to satisfy the Halve DSS Cards Placed option. The following "
                            f"{len(removed_start_cards)} card(s) were removed: {removed_start_cards}")

            start_cards = kept_start_cards

        # Remove the starting cards from the excluded cards.
        for card in ACTION_CARDS.union(ATTRIBUTE_CARDS):
            if card in start_cards:
                excluded_cards.remove(card)

        # Remove a valid ice/stone action and/or attribute card if the player isn't starting with one.
        if not has_freeze_action:
            excluded_cards.remove(world.random.choice(FREEZE_ACTIONS))
        if not has_freeze_attr:
            excluded_cards.remove(world.random.choice(FREEZE_ATTRS))

        # Remove 10 random cards from the exclusions.
        excluded_items += world.random.sample(excluded_cards, 10)

    # Exclude the Maiden Detonator from creation if the maidens start broken.
    if world.options.iron_maiden_behavior == IronMaidenBehavior.option_start_broken:
        excluded_items += [iname.ironmaidens]

    # Add one of each Item to the pool that is not filler or progression skip balancing.
    for item in cvcotm_item_info:
        classification = cvcotm_item_info[item].default_classification
        code = cvcotm_item_info[item].code

        # Skip event Items and Items that are excluded from creation.
        if code is None or item in excluded_items:
            continue

        # Classify the Cleansing as Useful instead of Progression if Ignore Cleansing is on.
        if item == iname.cleansing and world.options.ignore_cleansing:
            classification = ItemClassification.useful

        # Classify the Kick Boots as Progression + Useful if Nerf Roc Wing is on.
        if item == iname.kick_boots and world.options.nerf_roc_wing:
            classification |= ItemClassification.useful

        item_counts[classification][item] = 1
        total_items += 1

    # Add the total Last Keys if no skirmishes are required (meaning they're not forced anywhere).
    if not world.options.required_skirmishes:
        item_counts[ItemClassification.progression_skip_balancing][iname.last_key] = \
            world.options.available_last_keys.value
        total_items += world.options.available_last_keys.value

    # Add filler items at random until the total Items = the total Locations.
    while total_items < len(world.multiworld.get_unfilled_locations(world.player)):
        filler_to_add = world.random.choice(FILLER_ITEM_NAMES)
        item_counts[ItemClassification.filler][filler_to_add] += 1
        total_items += 1

    return item_counts
