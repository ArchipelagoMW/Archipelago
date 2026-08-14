from random import Random
from typing import List, Tuple, Dict

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
    boiler_room_meme, vault_meme, community_center_easy_meme_bundles
from ..data.bundles_data.remixed_anywhere_bundles import community_center_remixed_anywhere
from ..data.game_item import ItemTag
from ..locations import LocationTags, locations_by_tag
from ..logic.logic import StardewLogic
from ..options import BundleRandomization, StardewValleyOptions
from ..strings.animal_product_names import AnimalProduct
from ..strings.bundle_names import CCRoom
from ..strings.material_names import Material
from ..strings.metal_names import MetalBar, Mineral
from ..strings.monster_names import Monster
from ..strings.villager_names import NPC


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
        return get_meme_bundles(random, content, options, player_name, True)
    elif options.bundle_randomization == BundleRandomization.option_meme_easy:
        return get_meme_bundles(random, content, options, player_name, False)

    raise NotImplementedError


def get_vanilla_bundles(random: Random, content: StardewContent, options: StardewValleyOptions) -> List[BundleRoom]:
    generated_bundle_rooms = {room_name: vanilla_bundles.bundles_by_room[room_name].create_bundle_room(random, content, options) for room_name in
                              vanilla_bundles.bundles_by_room}
    fix_raccoon_bundle_names(generated_bundle_rooms[CCRoom.raccoon_requests])
    return list(generated_bundle_rooms.values())


def get_thematic_bundles(random: Random, content: StardewContent, options: StardewValleyOptions) -> List[BundleRoom]:
    generated_bundle_rooms = {room_name: thematic_bundles.bundles_by_room[room_name].create_bundle_room(random, content, options) for room_name in
                              thematic_bundles.bundles_by_room}
    fix_raccoon_bundle_names(generated_bundle_rooms[CCRoom.raccoon_requests])
    return list(generated_bundle_rooms.values())


def get_remixed_bundles(random: Random, content: StardewContent, options: StardewValleyOptions) -> List[BundleRoom]:
    generated_bundle_rooms = {room_name: remixed_bundles.bundles_by_room[room_name].create_bundle_room(random, content, options) for room_name in
                              remixed_bundles.bundles_by_room}
    fix_raccoon_bundle_names(generated_bundle_rooms[CCRoom.raccoon_requests])
    return list(generated_bundle_rooms.values())


def get_remixed_bundles_anywhere(random: Random, content: StardewContent, options: StardewValleyOptions) -> List[BundleRoom]:
    big_room = community_center_remixed_anywhere.create_bundle_room(random, content, options, is_entire_cc=True)
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


def get_meme_bundles(random: Random, content: StardewContent, options: StardewValleyOptions, player_name: str, allow_hard_meme_bundles: bool) -> List[BundleRoom]:
    if allow_hard_meme_bundles:
        big_room = community_center_meme_bundles.create_bundle_room(random, content, options, player_name, is_entire_cc=True)
    else:
        big_room = community_center_easy_meme_bundles.create_bundle_room(random, content, options, player_name, is_entire_cc=True)

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


def get_trash_bear_requests(random: Random, content: StardewContent, options: StardewValleyOptions) -> Dict[str, List[str]]:
    trash_bear_requests = dict()
    num_per_type = 2
    if options.bundle_price < 0:
        num_per_type = 1
    elif options.bundle_price > 0:
        num_per_type = min(4, num_per_type + options.bundle_price)

    trash_bear_requests["Foraging"] = pick_trash_bear_items(ItemTag.FORAGE, content, num_per_type, random)
    if options.bundle_per_room >= 0:
        # Cooking items are not in content packs yet. This can be simplified once they are
        # trash_bear_requests["Cooking"] = pick_trash_bear_items(ItemTag.COOKING, content, num_per_type, random)
        trash_bear_requests["Cooking"] = random.sample([recipe.name for recipe in content.cooking_recipes.values()], num_per_type)
    if options.bundle_per_room >= 1:
        trash_bear_requests["Farming"] = pick_trash_bear_items(ItemTag.CROPSANITY, content, num_per_type, random)
    if options.bundle_per_room >= 2:
        # Fish items are not tagged properly in content packs yet. This can be simplified once they are
        # trash_bear_requests["Fishing"] = pick_trash_bear_items(ItemTag.FISH, content, num_per_type, random)
        trash_bear_requests["Fishing"] = random.sample([fish for fish in content.fishes], num_per_type)
    return trash_bear_requests


def pick_trash_bear_items(item_tag: ItemTag, content: StardewContent, number_items: int, random: Random):
    forage_items = [item.name for item in content.find_tagged_items(item_tag)]
    return random.sample(forage_items, number_items)

def get_help_wanted_quests(random: Random, content: StardewContent, options: StardewValleyOptions) -> Dict[str, str]:
    help_wanted_quests = dict()
    if options.quest_locations.value <= 0:
        return help_wanted_quests

    num_help_wanteds = options.quest_locations.value
    available_locations = locations_by_tag[LocationTags.HELP_WANTED]
    picked_locations = random.sample(available_locations, num_help_wanteds)

    slaying_requesters = [NPC.clint, NPC.lewis, NPC.demetrius, NPC.wizard]

    forages = [item.name for item in content.find_tagged_items(ItemTag.FORAGE)]
    crops = [item.name for item in content.find_tagged_items(ItemTag.CROPSANITY)]
    minerals = [MetalBar.copper, MetalBar.iron, MetalBar.gold, MetalBar.iridium, Mineral.quartz, Mineral.amethyst, Mineral.topaz, Mineral.emerald, Mineral.ruby, Mineral.earth_crystal, Mineral.aquamarine, Mineral.diamond, Mineral.fire_quartz, Mineral.frozen_tear, Mineral.jade]
    animal_prodcts = [AnimalProduct.egg, AnimalProduct.brown_egg, AnimalProduct.milk, AnimalProduct.goat_milk, AnimalProduct.wool, AnimalProduct.duck_egg, AnimalProduct.truffle]
    all_fish = [fish for fish in content.fishes]
    item_delivery_items = list(sorted({*forages, *crops, *minerals, *animal_prodcts, *all_fish}))

    for location in picked_locations:
        location_name = location.name
        if LocationTags.HELP_WANTED_HELLO in location.tags:
            help_wanted_quests[location_name] = NPC.emily
        elif LocationTags.HELP_WANTED_SLAYING in location.tags:
            if "Crab" in location_name:
                help_wanted_quests[location_name] = NPC.demetrius
            elif Monster.green_slime in location_name or Monster.blue_slime in location_name or Monster.red_slime in location_name:
                help_wanted_quests[location_name] = random.choice(slaying_requesters)
            else:
                help_wanted_quests[location_name] = NPC.wizard
        elif LocationTags.HELP_WANTED_GATHERING in location.tags:
            requester = NPC.robin if (Material.wood in location_name or Material.stone in location_name) else NPC.clint
            help_wanted_quests[location_name] = requester
        elif LocationTags.HELP_WANTED_FISHING in location.tags:
            season = location_name.split(" ")[-1]
            seasonal_fish = [fish for fish in all_fish if season in content.fishes[fish].seasons]
            help_wanted_quests[location_name] = random.choice(seasonal_fish)
        elif LocationTags.HELP_WANTED_ITEM_DELIVERY in location.tags:
            help_wanted_quests[location_name] = random.choice(item_delivery_items)

    return help_wanted_quests
