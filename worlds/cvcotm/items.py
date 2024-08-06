import logging

from BaseClasses import Item, ItemClassification
from .data import iname
from .locations import base_id

from typing import TYPE_CHECKING, Dict, NamedTuple, Optional

if TYPE_CHECKING:
    from . import CVCotMWorld


class CVCotMItem(Item):
    game: str = "Castlevania Circle of the Moon"


class CVCotMItemData(NamedTuple):
    code: Optional[int]
    default_classification: ItemClassification
# "code" = The unique part of the Item's AP code attribute, as well as the value to call the in-game "prepare item
#          textbox" function with to give the Item in-game. Add this + base_id to get the actual AP code.
# "default classification" = The AP Item Classification that gets assigned to instances of that Item in create_item
#                            by default, unless I deliberately override it (as is the case for the Cleansing on the
#                            Ignore Cleansing option).


cvcotm_item_info: Dict[str, CVCotMItemData] = {
    iname.heart_max:      CVCotMItemData(0xE400, ItemClassification.filler),
    iname.hp_max:         CVCotMItemData(0xE401, ItemClassification.filler),
    iname.mp_max:         CVCotMItemData(0xE402, ItemClassification.filler),
    iname.salamander:     CVCotMItemData(0xE600, ItemClassification.useful),
    iname.serpent:        CVCotMItemData(0xE601, ItemClassification.progression),
    iname.mandragora:     CVCotMItemData(0xE602, ItemClassification.useful),
    iname.golem:          CVCotMItemData(0xE603, ItemClassification.useful),
    iname.cockatrice:     CVCotMItemData(0xE604, ItemClassification.progression),
    iname.manticore:      CVCotMItemData(0xE605, ItemClassification.useful),
    iname.griffin:        CVCotMItemData(0xE606, ItemClassification.useful),
    iname.thunderbird:    CVCotMItemData(0xE607, ItemClassification.useful),
    iname.unicorn:        CVCotMItemData(0xE608, ItemClassification.useful),
    iname.black_dog:      CVCotMItemData(0xE609, ItemClassification.useful),
    iname.mercury:        CVCotMItemData(0xE60A, ItemClassification.progression),
    iname.venus:          CVCotMItemData(0xE60B, ItemClassification.useful),
    iname.jupiter:        CVCotMItemData(0xE60C, ItemClassification.useful),
    iname.mars:           CVCotMItemData(0xE60D, ItemClassification.progression),
    iname.diana:          CVCotMItemData(0xE60E, ItemClassification.useful),
    iname.apollo:         CVCotMItemData(0xE60F, ItemClassification.useful),
    iname.neptune:        CVCotMItemData(0xE610, ItemClassification.useful),
    iname.saturn:         CVCotMItemData(0xE611, ItemClassification.useful),
    iname.uranus:         CVCotMItemData(0xE612, ItemClassification.useful),
    iname.pluto:          CVCotMItemData(0xE613, ItemClassification.useful),
    # Dash Boots
    iname.double:         CVCotMItemData(0xE801, ItemClassification.progression),
    iname.tackle:         CVCotMItemData(0xE802, ItemClassification.progression),
    iname.kick_boots:     CVCotMItemData(0xE803, ItemClassification.progression),
    iname.heavy_ring:     CVCotMItemData(0xE804, ItemClassification.progression),
    # Map
    iname.cleansing:      CVCotMItemData(0xE806, ItemClassification.progression),
    iname.roc_wing:       CVCotMItemData(0xE807, ItemClassification.progression),
    iname.last_key:       CVCotMItemData(0xE808, ItemClassification.progression_skip_balancing),
    iname.ironmaidens:    CVCotMItemData(None, ItemClassification.progression),
    iname.dracula:        CVCotMItemData(None, ItemClassification.progression),
    iname.shinning_armor: CVCotMItemData(None, ItemClassification.progression),
}

action_cards = {iname.mercury, iname.venus, iname.jupiter, iname.mars, iname.diana, iname.apollo, iname.neptune,
                iname.saturn, iname.uranus, iname.pluto}

attribute_cards = {iname.salamander, iname.serpent, iname.mandragora, iname.golem, iname.cockatrice, iname.griffin,
                   iname.manticore, iname.thunderbird, iname.unicorn, iname.black_dog}

filler_item_names = [iname.heart_max, iname.hp_max, iname.mp_max]


def get_item_names_to_ids() -> Dict[str, int]:
    return {name: cvcotm_item_info[name].code + base_id for name in cvcotm_item_info
            if cvcotm_item_info[name].code is not None}


def get_item_counts(world: "CVCotMWorld") -> Dict[ItemClassification, Dict[str, int]]:

    item_counts = {
        ItemClassification.progression: {},
        ItemClassification.progression_skip_balancing: {},
        ItemClassification.useful: {},
        ItemClassification.filler: {},
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

            logging.warning(f"[{world.multiworld.player_name[world.player]}] Too many DSS Cards in "
                            f"start_inventory_from_pool to satisfy the Halve DSS Cards Placed option. The following "
                            f"{len(removed_start_cards)} card(s) were removed: {removed_start_cards}")

            start_cards = kept_start_cards

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
    for item in cvcotm_item_info:
        classification = cvcotm_item_info[item].default_classification
        code = cvcotm_item_info[item].code

        # Skip event Items and cards that are excluded with Halve DSS Cards Placed.
        if code is None or item in excluded_cards:
            continue

        # Classify the Cleansing as Useful instead of Progression if Ignore Cleansing is on.
        if item == iname.cleansing and world.options.ignore_cleansing:
            classification = ItemClassification.useful

        if classification in [ItemClassification.filler, ItemClassification.progression_skip_balancing]:
            item_counts[classification][item] = 0
            continue
        item_counts[classification][item] = 1
        total_items += 1

    # Add the total Last Keys.
    if not world.options.require_all_bosses:
        item_counts[ItemClassification.progression_skip_balancing][iname.last_key] = \
            world.options.available_last_keys.value
        total_items += world.options.available_last_keys.value

    # Add filler items at random until the total Items = the total Locations.
    while total_items < len(world.multiworld.get_unfilled_locations(world.player)):
        item_counts[ItemClassification.filler][world.random.choice(filler_item_names)] += 1
        total_items += 1

    return item_counts
