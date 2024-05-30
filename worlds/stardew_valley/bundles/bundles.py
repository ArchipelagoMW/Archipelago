from random import Random
from typing import List

from .bundle_room import BundleRoom
from ..content import StardewContent
from ..data.bundle_data import pantry_vanilla, crafts_room_vanilla, fish_tank_vanilla, boiler_room_vanilla, bulletin_board_vanilla, vault_vanilla, \
    pantry_thematic, crafts_room_thematic, fish_tank_thematic, boiler_room_thematic, bulletin_board_thematic, vault_thematic, pantry_remixed, \
    crafts_room_remixed, fish_tank_remixed, boiler_room_remixed, bulletin_board_remixed, vault_remixed, all_bundle_items_except_money, \
    abandoned_joja_mart_thematic, abandoned_joja_mart_vanilla, abandoned_joja_mart_remixed, raccoon_vanilla, raccoon_thematic, raccoon_remixed
from ..logic.logic import StardewLogic
from ..options import BundleRandomization, StardewValleyOptions


def get_all_bundles(random: Random, logic: StardewLogic, content: StardewContent, options: StardewValleyOptions) -> List[BundleRoom]:
    if options.bundle_randomization == BundleRandomization.option_vanilla:
        return get_vanilla_bundles(random, content, options)
    elif options.bundle_randomization == BundleRandomization.option_thematic:
        return get_thematic_bundles(random, content, options)
    elif options.bundle_randomization == BundleRandomization.option_remixed:
        return get_remixed_bundles(random, content, options)
    elif options.bundle_randomization == BundleRandomization.option_shuffled:
        return get_shuffled_bundles(random, logic, content, options)

    raise NotImplementedError


def get_vanilla_bundles(random: Random, content: StardewContent, options: StardewValleyOptions) -> List[BundleRoom]:
    pantry = pantry_vanilla.create_bundle_room(options.bundle_price, random, content, options)
    crafts_room = crafts_room_vanilla.create_bundle_room(options.bundle_price, random, content, options)
    fish_tank = fish_tank_vanilla.create_bundle_room(options.bundle_price, random, content, options)
    boiler_room = boiler_room_vanilla.create_bundle_room(options.bundle_price, random, content, options)
    bulletin_board = bulletin_board_vanilla.create_bundle_room(options.bundle_price, random, content, options)
    vault = vault_vanilla.create_bundle_room(options.bundle_price, random, content, options)
    abandoned_joja_mart = abandoned_joja_mart_vanilla.create_bundle_room(options.bundle_price, random, content, options)
    raccoon = raccoon_vanilla.create_bundle_room(options.bundle_price, random, content, options)
    fix_raccoon_bundle_names(raccoon)
    return [pantry, crafts_room, fish_tank, boiler_room, bulletin_board, vault, abandoned_joja_mart, raccoon]


def get_thematic_bundles(random: Random, content: StardewContent, options: StardewValleyOptions) -> List[BundleRoom]:
    pantry = pantry_thematic.create_bundle_room(options.bundle_price, random, content, options)
    crafts_room = crafts_room_thematic.create_bundle_room(options.bundle_price, random, content, options)
    fish_tank = fish_tank_thematic.create_bundle_room(options.bundle_price, random, content, options)
    boiler_room = boiler_room_thematic.create_bundle_room(options.bundle_price, random, content, options)
    bulletin_board = bulletin_board_thematic.create_bundle_room(options.bundle_price, random, content, options)
    vault = vault_thematic.create_bundle_room(options.bundle_price, random, content, options)
    abandoned_joja_mart = abandoned_joja_mart_thematic.create_bundle_room(options.bundle_price, random, content, options)
    raccoon = raccoon_thematic.create_bundle_room(options.bundle_price, random, content, options)
    fix_raccoon_bundle_names(raccoon)
    return [pantry, crafts_room, fish_tank, boiler_room, bulletin_board, vault, abandoned_joja_mart, raccoon]


def get_remixed_bundles(random: Random, content: StardewContent, options: StardewValleyOptions) -> List[BundleRoom]:
    pantry = pantry_remixed.create_bundle_room(options.bundle_price, random, content, options)
    crafts_room = crafts_room_remixed.create_bundle_room(options.bundle_price, random, content, options)
    fish_tank = fish_tank_remixed.create_bundle_room(options.bundle_price, random, content, options)
    boiler_room = boiler_room_remixed.create_bundle_room(options.bundle_price, random, content, options)
    bulletin_board = bulletin_board_remixed.create_bundle_room(options.bundle_price, random, content, options)
    vault = vault_remixed.create_bundle_room(options.bundle_price, random, content, options)
    abandoned_joja_mart = abandoned_joja_mart_remixed.create_bundle_room(options.bundle_price, random, content, options)
    raccoon = raccoon_remixed.create_bundle_room(options.bundle_price, random, content, options)
    fix_raccoon_bundle_names(raccoon)
    return [pantry, crafts_room, fish_tank, boiler_room, bulletin_board, vault, abandoned_joja_mart, raccoon]


def get_shuffled_bundles(random: Random, logic: StardewLogic, content: StardewContent, options: StardewValleyOptions) -> List[BundleRoom]:
    valid_bundle_items = [bundle_item for bundle_item in all_bundle_items_except_money if bundle_item.can_appear(content, options)]

    rooms = [room for room in get_remixed_bundles(random, content, options) if room.name != "Vault"]
    required_items = 0
    for room in rooms:
        for bundle in room.bundles:
            required_items += len(bundle.items)
        random.shuffle(room.bundles)
    random.shuffle(rooms)

    # Remove duplicates of the same item
    valid_bundle_items = [item1 for i, item1 in enumerate(valid_bundle_items)
                          if not any(item1.item_name == item2.item_name and item1.quality == item2.quality for item2 in valid_bundle_items[:i])]
    chosen_bundle_items = random.sample(valid_bundle_items, required_items)
    # sorted_bundle_items = sorted(chosen_bundle_items, key=lambda x: logic.has(x.item_name).get_difficulty())
    sorted_bundle_items = chosen_bundle_items
    for room in rooms:
        for bundle in room.bundles:
            num_items = len(bundle.items)
            bundle.items = sorted_bundle_items[:num_items]
            sorted_bundle_items = sorted_bundle_items[num_items:]

    vault = vault_remixed.create_bundle_room(options.bundle_price, random, content, options)
    return [*rooms, vault]


def fix_raccoon_bundle_names(raccoon):
    for i in range(len(raccoon.bundles)):
        raccoon_bundle = raccoon.bundles[i]
        raccoon_bundle.name = f"Raccoon Request {i + 1}"
