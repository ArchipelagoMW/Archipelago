from BaseClasses import Item, ItemClassification
import itertools
from .game_data.local_data import item_id_table
from Options import OptionError
from .Items import item_table
from typing import Dict, TextIO
import typing


class EBItem(Item):
    game: str = "Castlevania: Portrait of Ruin"


def generate_early(world) -> None:  # Todo: place locked items in generate_early
    from .setup_game import setup_gamevars
    from .modules.flavor_data import create_flavors
    from .modules.enemy_data import initialize_enemies
    world.starting_character = world.options.starting_character.current_key.capitalize()
    world.locals = []
    local_space_count = 0
    max_counts = {
        "Ness": 12,
        "Paula": 11,
        "Jeff": 9,
        "Poo": 12
    }

    max_count = max_counts[world.starting_character]
    for item_name, amount in itertools.chain(world.options.start_inventory.items(),
                                             world.options.start_inventory_from_pool.items()):
        if item_name in item_id_table:
            local_space_count += amount
            if local_space_count > max_count and not world.options.remote_items:
                player = world.multiworld.get_player_name(world.player)
                raise OptionError(
                    f"{player}: starting inventory cannot place more than {max_count} items into 'Goods' for {world.starting_character}. Attempted to place {local_space_count} Goods items.")

    setup_gamevars(world)
    create_flavors(world)
    initialize_enemies(world)

    world.pre_fill_count = 0
    if not world.options.character_shuffle:
        world.options.local_items.value.update(["Paula", "Jeff", "Poo", "Flying Man"])
        world.pre_fill_count = 6

    if world.options.local_teleports:
        world.options.local_items.value |= world.item_name_groups["PSI"]


def pre_fill(world) -> None:
    from worlds.generic.Rules import add_item_rule
    from Fill import fill_restrictive
    from .modules.hint_data import setup_hints
    prefill_locations = []
    prefill_items = []

    if not world.options.character_shuffle:
        main_characters = ["Ness", "Paula", "Jeff", "Poo"]
        for character in main_characters:
            if character != world.starting_character:
                prefill_items.append(world.create_item(character))

        prefill_items.extend([
            world.create_item("Flying Man"),
            world.create_item("Teddy Bear"),
            world.create_item("Super Plush Bear")
        ])

        prefill_locations.extend([
            world.get_location("Happy-Happy Village - Prisoner"),
            world.get_location("Threed - Zombie Prisoner"),
            world.get_location("Snow Wood - Bedroom"),
            world.get_location("Monotoli Building - Monotoli Character"),
            world.get_location("Dalaam - Throne Character"),
            world.get_location("Deep Darkness - Barf Character"),
        ])
        world.random.shuffle(prefill_locations)

        add_item_rule(world.get_location("Happy-Happy Village - Prisoner"), lambda item: item.name in world.item_name_groups["Characters"])
        add_item_rule(world.get_location("Threed - Zombie Prisoner"), lambda item: item.name in world.item_name_groups["Characters"])
        add_item_rule(world.get_location("Snow Wood - Bedroom"), lambda item: item.name in world.item_name_groups["Characters"])
        add_item_rule(world.get_location("Monotoli Building - Monotoli Character"), lambda item: item.name in world.item_name_groups["Characters"])
        add_item_rule(world.get_location("Dalaam - Throne Character"), lambda item: item.name in world.item_name_groups["Characters"])
        add_item_rule(world.get_location("Deep Darkness - Barf Character"), lambda item: item.name in world.item_name_groups["Characters"])

    fill_restrictive(world.multiworld, world.multiworld.get_all_state(False, collect_pre_fill_items=False), prefill_locations, prefill_items, True, True)
    setup_hints(world)


def get_pre_fill_items(self) -> list[Item]:
    characters = ["Ness", "Paula", "Jeff", "Poo"]
    prefill_items = []
    for character in characters:
        if character != self.starting_character:
            prefill_items.append(self.create_item(f"{character}"))
    return prefill_items


def create_regions(world) -> None:
    from .Locations import get_locations
    from .Regions import init_areas, connect_area_exits
    from .setup_game import place_static_items
    init_areas(world, get_locations(world))
    connect_area_exits(world)
    place_static_items(world)


def create_items(world) -> None:
    from .generator_items import get_excluded_items, fill_item_pool, get_item_pool
    pool = get_item_pool(world, get_excluded_items(world))
    for item in world.item_pool:
        pool.append(set_classifications(world, item))

    fill_item_pool(world, pool)
    world.multiworld.itempool += pool


def create_item(world, name: str) -> EBItem:
    data = item_table[name]
    return EBItem(name, data.classification, data.code, world.player)


def get_filler_item_name(world) -> str:  # Todo: make this suck less
    weights = {"rare": world.options.rare_filler_weight.value, "uncommon": world.options.uncommon_filler_weight.value,
               "common": world.options.common_filler_weight.value,
               "rare_gear": int(world.options.rare_filler_weight.value * 0.5),
               "uncommon_gear": int(world.options.uncommon_filler_weight.value * 0.5),
               "common_gear": int(world.options.common_filler_weight.value * 0.5),
               "money": world.options.money_weight.value}

    filler_type = world.random.choices(list(weights), weights=list(weights.values()), k=1)[0]
    weight_table = {
        "common": world.common_items,
        "common_gear": world.common_gear,
        "uncommon": world.uncommon_items,
        "uncommon_gear": world.uncommon_gear,
        "rare": world.rare_items,
        "rare_gear": world.rare_gear,
        "money": world.money
    }
    return world.random.choice(weight_table[filler_type])


def set_rules(world) -> None:
    from .Rules import set_location_rules
    set_location_rules(world)


def set_classifications(world, name: str) -> EBItem:
    data = item_table[name]
    item = EBItem(name, data.classification, data.code, world.player)

    if name == "Magicant Teleport" and world.options.magicant_mode == 3:
        item.classification = ItemClassification.useful
    return item


def generate_output(world, output_directory: str) -> None:
    import os
    import pkgutil

    from .Rom import EBProcPatch, patch_rom
    world.has_generated_output = True  # Make sure data defined in generate output doesn't get added to spoiler only mode
    try:
        patch = EBProcPatch(player=world.player, player_name=world.multiworld.player_name[world.player])
        patch.write_file("earthbound_basepatch.bsdiff4", pkgutil.get_data(__name__, "src/earthbound_basepatch.bsdiff4"))
        patch_rom(world, patch, world.player)

        world.rom_name = patch.name

        patch.write(os.path.join(output_directory,
                                 f"{world.multiworld.get_out_file_name_base(world.player)}{patch.patch_file_ending}"))
    except Exception:
        raise
    finally:
        world.rom_name_available_event.set()  # make sure threading continues and errors are collected


def modify_multidata(world, multidata: dict) -> None:
    import base64
    # wait for self.rom_name to be available.
    world.rom_name_available_event.wait()
    rom_name = getattr(world, "rom_name", None)
    if rom_name:
        new_name = base64.b64encode(bytes(world.rom_name)).decode()
        multidata["connect_names"][new_name] = multidata["connect_names"][world.multiworld.player_name[world.player]]


def extend_hint_information(world, hint_data: Dict[int, Dict[int, str]]) -> None:
    if world.options.dungeon_shuffle:
        dungeon_entrances = {}
        dungeon_mapping = {}
        for dungeon in world.dungeon_connections:
            dungeon_entrances[world.dungeon_connections[dungeon]] = dungeon

        for dungeon in dungeon_entrances:
            for location in world.get_region(dungeon).locations:
                if location.address:
                    dungeon_mapping[location.address] = dungeon_entrances[dungeon]

        hint_data[world.player] = dungeon_mapping


def fill_slot_data(world) -> Dict[str, typing.Any]:
    return {
        "starting_area": world.start_location,
        "pizza_logic": world.options.monkey_caves_mode.value,
        "free_sancs": world.options.no_free_sanctuaries.value,
        "shopsanity": world.options.shop_randomizer.value,
        "hint_man_hints": world.hint_man_hints
    }


def write_spoiler_header(world, spoiler_handle: TextIO) -> None:
    from .game_data.text_data import spoiler_psi, spoiler_starts, spoiler_badges
    spoiler_handle.write(f"\nStarting Location:    {spoiler_starts[world.start_location]}\n")
    spoiler_handle.write(f"Franklin Badge Protection:    {spoiler_badges[world.franklin_protection]}\n")
    if world.options.psi_shuffle:
        spoiler_handle.write("\nPSI Shuffle:\n")
        spoiler_handle.write(f" Favorite Thing PSI Slot:    {spoiler_psi[world.offensive_psi_slots[0]]}\n")
        spoiler_handle.write(f" Ness Offensive PSI Middle Slot:    {spoiler_psi[world.offensive_psi_slots[1]]}\n")
        spoiler_handle.write(f" Paula Offensive PSI Top Slot:    {spoiler_psi[world.offensive_psi_slots[2]]}\n")
        spoiler_handle.write(
            f" Paula/Poo Offensive PSI Middle Slot:    {spoiler_psi[world.offensive_psi_slots[3]]}\n")
        spoiler_handle.write(
            f" Paula/Poo Offensive PSI Bottom Slot:    {spoiler_psi[world.offensive_psi_slots[4]]}\n")
        spoiler_handle.write(f" Poo Progressive PSI Slot:    {spoiler_psi[world.offensive_psi_slots[5]]}\n")

        spoiler_handle.write(f" Ness/Poo Shield Slot:    {spoiler_psi[world.shield_slots[0]]}\n")
        spoiler_handle.write(f" Paula Shield Slot:    {spoiler_psi[world.shield_slots[1]]}\n")

        spoiler_handle.write(f" Ness Assist PSI Middle Slot:    {spoiler_psi[world.assist_psi_slots[0]]}\n")
        spoiler_handle.write(f" Ness Assist PSI Bottom Slot:    {spoiler_psi[world.assist_psi_slots[1]]}\n")
        spoiler_handle.write(f" Paula Assist PSI Middle Slot:    {spoiler_psi[world.assist_psi_slots[2]]}\n")
        spoiler_handle.write(f" Paula Assist PSI Bottom Slot:    {spoiler_psi[world.assist_psi_slots[3]]}\n")
        spoiler_handle.write(f" Poo Assist PSI Slot:    {spoiler_psi[world.assist_psi_slots[4]]}\n")
    if world.options.psi_shuffle == 2:
        spoiler_handle.write(f" Bomb/Bazooka Slot:    {spoiler_psi[world.jeff_offense_items[0]]}\n")
        spoiler_handle.write(f" Bottle Rocket Slot:    {spoiler_psi[world.jeff_offense_items[1]]}\n")

        spoiler_handle.write(f" Spray Can Slot:    {spoiler_psi[world.jeff_assist_items[0]]}\n")
        spoiler_handle.write(f" Multi-Level Gadget Slot 1:    {spoiler_psi[world.jeff_assist_items[1]]}\n")
        spoiler_handle.write(f" Single-Level Gadget Slot 1:    {spoiler_psi[world.jeff_assist_items[2]]}\n")
        spoiler_handle.write(f" Single-Level Gadget Slot 2:    {spoiler_psi[world.jeff_assist_items[3]]}\n")
        spoiler_handle.write(f" Multi-Level Gadget Slot 2:    {spoiler_psi[world.jeff_assist_items[4]]}\n")

    if world.options.boss_shuffle:
        spoiler_handle.write("\nBoss Randomization:\n" +
                             f" Frank => {world.boss_list[0]}\n" +
                             f" Frankystein Mark II => {world.boss_list[1]}\n" +
                             f" Titanic Ant => {world.boss_list[2]}\n" +
                             f" Captain Strong => {world.boss_list[3]}\n" +
                             f" Everdred => {world.boss_list[4]}\n" +
                             f" Mr. Carpainter => {world.boss_list[5]}\n" +
                             f" Mondo Mole => {world.boss_list[6]}\n" +
                             f" Boogey Tent => {world.boss_list[7]}\n" +
                             f" Mini Barf => {world.boss_list[8]}\n" +
                             f" Master Belch => {world.boss_list[9]}\n" +
                             f" Trillionage Sprout => {world.boss_list[10]}\n" +
                             f" Guardian Digger => {world.boss_list[11]}\n" +
                             f" Dept. Store Spook => {world.boss_list[12]}\n" +
                             f" Evil Mani-Mani => {world.boss_list[13]}\n" +
                             f" Clumsy Robot => {world.boss_list[14]}\n" +
                             f" Shrooom! => {world.boss_list[15]}\n" +
                             f" Plague Rat of Doom => {world.boss_list[16]}\n" +
                             f" Thunder and Storm => {world.boss_list[17]}\n" +
                             f" Kraken => {world.boss_list[18]}\n" +
                             f" Guardian General => {world.boss_list[19]}\n" +
                             f" Master Barf => {world.boss_list[20]}\n" +
                             f" Starman Deluxe => {world.boss_list[21]}\n" +
                             f" Electro Specter => {world.boss_list[22]}\n" +
                             f" Carbon Dog => {world.boss_list[23]}\n" +
                             f" Ness's Nightmare => {world.boss_list[24]}\n" +
                             f" Heavily Armed Pokey => {world.boss_list[25]}\n" +
                             f" Starman Junior => {world.boss_list[26]}\n" +
                             f" Diamond Dog => {world.boss_list[27]}\n" +
                             f" Giygas (Phase 2) => {world.boss_list[28]}\n")

    if world.options.dungeon_shuffle:
        spoiler_handle.write("\nDungeon Entrances:\n")
        for dungeon in world.dungeon_connections:
            spoiler_handle.write(
                f" {dungeon} => {world.dungeon_connections[dungeon]}\n"
            )

    if world.has_generated_output:
        spoiler_handle.write("\nArea Levels:\n")
        spoiler_excluded_areas = ["Ness's Mind", "Global ATM Access", "Common Condiment Shop"]
        for area in world.area_levels:
            if area not in spoiler_excluded_areas:
                spoiler_handle.write(f" {area}: Level {world.area_levels[area]}\n")
