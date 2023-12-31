from random import Random
from typing import List

from .bundle_room import BundleRoom
from ..data.bundle_data import pantry_vanilla, crafts_room_vanilla, fish_tank_vanilla, boiler_room_vanilla, bulletin_board_vanilla, vault_vanilla, \
    pantry_thematic, crafts_room_thematic, fish_tank_thematic, boiler_room_thematic, bulletin_board_thematic, vault_thematic, pantry_remixed, \
    crafts_room_remixed, fish_tank_remixed, boiler_room_remixed, bulletin_board_remixed, vault_remixed, all_bundle_items_except_money, \
    abandoned_joja_mart_thematic, abandoned_joja_mart_vanilla, abandoned_joja_mart_remixed
from ..logic.logic import StardewLogic
from ..options import BundleRandomization, StardewValleyOptions, ExcludeGingerIsland


def get_all_bundles(random: Random, logic: StardewLogic, options: StardewValleyOptions) -> List[BundleRoom]:
    if options.bundle_randomization == BundleRandomization.option_vanilla:
        return get_vanilla_bundles(random, options)
    elif options.bundle_randomization == BundleRandomization.option_thematic:
        return get_thematic_bundles(random, options)
    elif options.bundle_randomization == BundleRandomization.option_remixed:
        return get_remixed_bundles(random, options)
    elif options.bundle_randomization == BundleRandomization.option_shuffled:
        return get_shuffled_bundles(random, logic, options)

    raise NotImplementedError


def get_vanilla_bundles(random: Random, options: StardewValleyOptions) -> List[BundleRoom]:
    pantry = pantry_vanilla.create_bundle_room(options.bundle_price, random, options)
    crafts_room = crafts_room_vanilla.create_bundle_room(options.bundle_price, random, options)
    fish_tank = fish_tank_vanilla.create_bundle_room(options.bundle_price, random, options)
    boiler_room = boiler_room_vanilla.create_bundle_room(options.bundle_price, random, options)
    bulletin_board = bulletin_board_vanilla.create_bundle_room(options.bundle_price, random, options)
    vault = vault_vanilla.create_bundle_room(options.bundle_price, random, options)
    abandoned_joja_mart = abandoned_joja_mart_vanilla.create_bundle_room(options.bundle_price, random, options)
    return [pantry, crafts_room, fish_tank, boiler_room, bulletin_board, vault, abandoned_joja_mart]


def get_thematic_bundles(random: Random, options: StardewValleyOptions) -> List[BundleRoom]:
    pantry = pantry_thematic.create_bundle_room(options.bundle_price, random, options)
    crafts_room = crafts_room_thematic.create_bundle_room(options.bundle_price, random, options)
    fish_tank = fish_tank_thematic.create_bundle_room(options.bundle_price, random, options)
    boiler_room = boiler_room_thematic.create_bundle_room(options.bundle_price, random, options)
    bulletin_board = bulletin_board_thematic.create_bundle_room(options.bundle_price, random, options)
    vault = vault_thematic.create_bundle_room(options.bundle_price, random, options)
    abandoned_joja_mart = abandoned_joja_mart_thematic.create_bundle_room(options.bundle_price, random, options)
    return [pantry, crafts_room, fish_tank, boiler_room, bulletin_board, vault, abandoned_joja_mart]


def get_remixed_bundles(random: Random, options: StardewValleyOptions) -> List[BundleRoom]:
    pantry = pantry_remixed.create_bundle_room(options.bundle_price, random, options)
    crafts_room = crafts_room_remixed.create_bundle_room(options.bundle_price, random, options)
    fish_tank = fish_tank_remixed.create_bundle_room(options.bundle_price, random, options)
    boiler_room = boiler_room_remixed.create_bundle_room(options.bundle_price, random, options)
    bulletin_board = bulletin_board_remixed.create_bundle_room(options.bundle_price, random, options)
    vault = vault_remixed.create_bundle_room(options.bundle_price, random, options)
    abandoned_joja_mart = abandoned_joja_mart_remixed.create_bundle_room(options.bundle_price, random, options)
    return [pantry, crafts_room, fish_tank, boiler_room, bulletin_board, vault, abandoned_joja_mart]


def get_shuffled_bundles(random: Random, logic: StardewLogic, options: StardewValleyOptions) -> List[BundleRoom]:
    valid_bundle_items = [bundle_item for bundle_item in all_bundle_items_except_money if bundle_item.can_appear(options)]

    rooms = [room for room in get_remixed_bundles(random, options) if room.name != "Vault"]
    required_items = 0
    for room in rooms:
        for bundle in room.bundles:
            required_items += len(bundle.items)
        random.shuffle(room.bundles)
    random.shuffle(rooms)

    chosen_bundle_items = random.sample(valid_bundle_items, required_items)
    sorted_bundle_items = sorted(chosen_bundle_items, key=lambda x: logic.has(x.item_name).get_difficulty())
    for room in rooms:
        for bundle in room.bundles:
            num_items = len(bundle.items)
            bundle.items = sorted_bundle_items[:num_items]
            sorted_bundle_items = sorted_bundle_items[num_items:]

    vault = vault_remixed.create_bundle_room(options.bundle_price, random, options)
    return [*rooms, vault]

