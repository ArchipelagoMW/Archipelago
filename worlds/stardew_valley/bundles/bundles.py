from random import Random
from typing import List, Tuple

from .bundle import Bundle
from .bundle_room import BundleRoom, BundleRoomTemplate
from ..content import StardewContent
from ..data.bundles_data.bundle_data import pantry_remixed, \
    crafts_room_remixed, fish_tank_remixed, boiler_room_remixed, bulletin_board_remixed, vault_remixed, \
    all_bundle_items_except_money, \
    abandoned_joja_mart_remixed, giant_stump_remixed
from ..data.bundles_data.bundle_set import vanilla_bundles, remixed_bundles, thematic_bundles
from ..data.bundles_data.meme_bundles import community_center_meme_bundles, pantry_meme, crafts_room_meme, \
    fish_tank_meme, bulletin_board_meme, \
    boiler_room_meme, vault_meme
from ..data.bundles_data.remixed_anywhere_bundles import community_center_remixed_anywhere
from ..logic.logic import StardewLogic
from ..options import BundleRandomization, StardewValleyOptions
from ..strings.bundle_names import CCRoom


def get_all_bundles(random: Random, logic: StardewLogic, content: StardewContent, options: StardewValleyOptions, player_name: str) -> List[BundleRoom]:
    if options.bundle_randomization == BundleRandomization.option_vanilla:
        return get_vanilla_bundles(random, content, options)
    elif options.bundle_randomization == BundleRandomization.option_thematic:
        return get_thematic_bundles(random, content, options)
    elif options.bundle_randomization == BundleRandomization.option_remixed:
        return get_remixed_bundles(random, content, options)
    elif options.bundle_randomization == BundleRandomization.option_remixed_anywhere:
        return get_remixed_bundles_anywhere(random, content, options)
    elif options.bundle_randomization == BundleRandomization.option_shuffled:
        return get_shuffled_bundles(random, logic, content, options)
    elif options.bundle_randomization == BundleRandomization.option_meme:
        return get_meme_bundles(random, content, options, player_name)

    raise NotImplementedError


def get_vanilla_bundles(random: Random, content: StardewContent, options: StardewValleyOptions) -> List[BundleRoom]:
    generated_bundle_rooms = {room_name: vanilla_bundles.bundles_by_room[room_name].create_bundle_room(random, content, options) for room_name in vanilla_bundles.bundles_by_room}
    fix_raccoon_bundle_names(generated_bundle_rooms[CCRoom.raccoon_requests])
    return list(generated_bundle_rooms.values())


def get_thematic_bundles(random: Random, content: StardewContent, options: StardewValleyOptions) -> List[BundleRoom]:
    generated_bundle_rooms = {room_name: thematic_bundles.bundles_by_room[room_name].create_bundle_room(random, content, options) for room_name in thematic_bundles.bundles_by_room}
    fix_raccoon_bundle_names(generated_bundle_rooms[CCRoom.raccoon_requests])
    return list(generated_bundle_rooms.values())


def get_remixed_bundles(random: Random, content: StardewContent, options: StardewValleyOptions) -> List[BundleRoom]:
    generated_bundle_rooms = {room_name: remixed_bundles.bundles_by_room[room_name].create_bundle_room(random, content, options) for room_name in remixed_bundles.bundles_by_room}
    fix_raccoon_bundle_names(generated_bundle_rooms[CCRoom.raccoon_requests])
    return list(generated_bundle_rooms.values())


def get_remixed_bundles_anywhere(random: Random, content: StardewContent, options: StardewValleyOptions) -> List[BundleRoom]:
    big_room = community_center_remixed_anywhere.create_bundle_room(random, content, options)
    all_chosen_bundles = big_room.bundles
    random.shuffle(all_chosen_bundles)

    end_index = 0

    pantry, end_index = create_room_from_bundles(pantry_remixed, all_chosen_bundles, options, end_index)
    crafts_room, end_index = create_room_from_bundles(crafts_room_remixed, all_chosen_bundles, options, end_index)
    fish_tank, end_index = create_room_from_bundles(fish_tank_remixed, all_chosen_bundles, options, end_index)
    boiler_room, end_index = create_room_from_bundles(boiler_room_remixed, all_chosen_bundles, options, end_index)
    bulletin_board, end_index = create_room_from_bundles(bulletin_board_remixed, all_chosen_bundles, options, end_index)
    vault, end_index = create_room_from_bundles(vault_remixed, all_chosen_bundles, options, end_index)

    abandoned_joja_mart = abandoned_joja_mart_remixed.create_bundle_room(random, content, options)
    raccoon = giant_stump_remixed.create_bundle_room(random, content, options)
    fix_raccoon_bundle_names(raccoon)
    return [pantry, crafts_room, fish_tank, boiler_room, bulletin_board, vault, abandoned_joja_mart, raccoon]


def get_meme_bundles(random: Random, content: StardewContent, options: StardewValleyOptions, player_name: str) -> List[BundleRoom]:
    big_room = community_center_meme_bundles.create_bundle_room(random, content, options, player_name)
    all_chosen_bundles = big_room.bundles
    random.shuffle(all_chosen_bundles)

    end_index = 0

    pantry, end_index = create_room_from_bundles(pantry_meme, all_chosen_bundles, options, end_index)
    crafts_room, end_index = create_room_from_bundles(crafts_room_meme, all_chosen_bundles, options, end_index)
    fish_tank, end_index = create_room_from_bundles(fish_tank_meme, all_chosen_bundles, options, end_index)
    boiler_room, end_index = create_room_from_bundles(boiler_room_meme, all_chosen_bundles, options, end_index)
    bulletin_board, end_index = create_room_from_bundles(bulletin_board_meme, all_chosen_bundles, options, end_index)
    vault, end_index = create_room_from_bundles(vault_meme, all_chosen_bundles, options, end_index)

    abandoned_joja_mart = abandoned_joja_mart_remixed.create_bundle_room(random, content, options)
    raccoon = giant_stump_remixed.create_bundle_room(random, content, options)
    fix_raccoon_bundle_names(raccoon)
    return [pantry, crafts_room, fish_tank, boiler_room, bulletin_board, vault, abandoned_joja_mart, raccoon]


def create_room_from_bundles(template: BundleRoomTemplate, all_bundles: List[Bundle], options: StardewValleyOptions, end_index: int) -> Tuple[BundleRoom, int]:
    start_index = end_index
    end_index += template.number_bundles + options.bundle_per_room.value
    return BundleRoom(template.name, all_bundles[start_index:end_index]), end_index


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
    for room in rooms:
        for bundle in room.bundles:
            num_items = len(bundle.items)
            bundle.items = chosen_bundle_items[:num_items]
            chosen_bundle_items = chosen_bundle_items[num_items:]

    vault = vault_remixed.create_bundle_room(random, content, options)
    return [*rooms, vault]


def fix_raccoon_bundle_names(raccoon):
    for i in range(len(raccoon.bundles)):
        raccoon_bundle = raccoon.bundles[i]
        raccoon_bundle.name = f"Raccoon Request {i + 1}"
