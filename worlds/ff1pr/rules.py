from os import access
from typing import Dict, TYPE_CHECKING

from worlds.generic.Rules import set_rule, forbid_item, add_rule
from .items import item_table
from .options import FF1pixelOptions
from .entrances import global_entrances
from .data import regnames, entnames, itemnames, eventnames
from BaseClasses import CollectionState
if TYPE_CHECKING:
    from . import FF1pixelWorld, FF1pixelOptions

mystic_key_locked_locations = [
    "Chaos Shrine - Locked Single",
    "Chaos Shrine - Locked Duo 1",
    "Chaos Shrine - Locked Duo 2",
    "Castle Cornelia - Treasury 1",
    "Castle Cornelia - Treasury 2",
    "Castle Cornelia - Treasury 3",
    "Castle Cornelia - Treasury 4",
    "Castle Cornelia - Treasury 5",
    "Castle Cornelia - Treasury Major",
    "Marsh Cave B3 (Bottom) - Locked Corner",
    "Marsh Cave B3 (Bottom) - Locked Middle",
    "Marsh Cave B3 (Bottom) - Locked Cross",
    "Western Keep - Treasury 1",
    "Western Keep - Treasury 2",
    "Western Keep - Treasury 3",
    "Elven Castle - Treasury 1",
    "Elven Castle - Treasury 2",
    "Elven Castle - Treasury 3",
    "Elven Castle - Treasury 4",
    "Mount Duergar - Treasury 1",
    "Mount Duergar - Treasury 2",
    "Mount Duergar - Treasury 3",
    "Mount Duergar - Treasury 4",
    "Mount Duergar - Treasury 5",
    "Mount Duergar - Treasury 6",
    "Mount Duergar - Treasury 7",
    "Mount Duergar - Treasury 8",
]

titan_fed_locked_locations = [
    "Giant's Cave - Chest 1",
    "Giant's Cave - Chest 2",
    "Giant's Cave - Chest 3",
    "Giant's Cave - Chest 4",
]

def has_tablatures(state: CollectionState, options: FF1pixelOptions, player: int) -> bool:
    return state.has(itemnames.lute_tablature, player, options.lute_tablatures.value)

def has_crystals(state: CollectionState, options: FF1pixelOptions, player: int) -> bool:
    return (state.has(eventnames.earth_crystal, player) + state.has(eventnames.fire_crystal, player) +
        state.has(eventnames.water_crystal, player) + state.has(eventnames.air_crystal, player)) >= options.crystals_required

def set_region_rules(world: "FF1pixelWorld") -> None:
    player = world.player
    options = world.options

    if world.options.early_progression.value == 0: # bikke ship
        world.get_entrance(regnames.overworld + " -> " + regnames.innersea_region).access_rule = \
            lambda state: state.has(itemnames.ship, player) or state.has(itemnames.airship, player)
        world.get_entrance(regnames.overworld + " -> " + regnames.ice_region).access_rule = \
            lambda state: state.has(itemnames.canoe, player) or state.has(itemnames.airship, player)
        world.get_entrance(regnames.overworld + " -> " + regnames.crescent_region).access_rule = \
            lambda state: (state.has_all({itemnames.ship, eventnames.canal}, player)
                           or state.has_all({itemnames.ship, itemnames.canoe}, player)
                           or state.has(itemnames.airship, player))
        world.get_entrance(regnames.overworld + " -> " + regnames.gulg_region).access_rule = \
            lambda state: (state.has_all({itemnames.ship, itemnames.canoe}, player)
                           or state.has(itemnames.airship, player))
        world.get_entrance(regnames.overworld + " -> " + regnames.ryukhan_desert).access_rule = \
            lambda state: (state.has_all({itemnames.ship, itemnames.canoe, eventnames.canal}, player)
                           or state.has(itemnames.airship, player))
    else:
        world.get_entrance(regnames.overworld + " -> " + regnames.pravoka_region).access_rule = \
            lambda state: state.has(itemnames.ship, player) or state.has(itemnames.airship, player)
        world.get_entrance(regnames.overworld + " -> " + regnames.ice_region).access_rule = \
            lambda state: (state.has_all({itemnames.ship, itemnames.canoe}, player)
                           or state.has(itemnames.airship, player))
        world.get_entrance(regnames.overworld + " -> " + regnames.crescent_region).access_rule = \
            lambda state: (state.has_all({itemnames.ship, eventnames.canal}, player)
                           or state.has(itemnames.canoe, player)
                           or state.has(itemnames.airship, player))
        world.get_entrance(regnames.overworld + " -> " + regnames.gulg_region).access_rule = \
            lambda state: state.has(itemnames.canoe, player) or state.has(itemnames.airship, player)
        world.get_entrance(regnames.overworld + " -> " + regnames.ryukhan_desert).access_rule = \
            lambda state: (state.has_all({itemnames.canoe, itemnames.ship, eventnames.canal}, player)
                           or state.has(itemnames.airship, player))

    world.get_entrance(regnames.overworld + " -> " + regnames.melmond_region).access_rule = \
        lambda state: state.has_all({itemnames.ship, eventnames.canal}, player) or state.has(itemnames.airship, player)
    world.get_entrance(regnames.overworld + " -> " + regnames.sage_region).access_rule = \
        lambda state: state.has(itemnames.airship, player) #or state.has_all({ship, canal, titan_fed}, player)
    world.get_entrance(regnames.overworld + " -> " + regnames.bahamuts_island).access_rule = \
        lambda state: state.has(itemnames.airship, player)
    world.get_entrance(regnames.overworld + " -> " + regnames.dragon_forest_island).access_rule = \
        lambda state: state.has(itemnames.airship, player)
    world.get_entrance(regnames.overworld + " -> " + regnames.dragon_marsh_island).access_rule = \
        lambda state: state.has(itemnames.airship, player)
    world.get_entrance(regnames.overworld + " -> " + regnames.dragon_small_island).access_rule = \
        lambda state: state.has(itemnames.airship, player)
    world.get_entrance(regnames.overworld + " -> " + regnames.dragon_plains_island).access_rule = \
        lambda state: state.has(itemnames.airship, player)
    world.get_entrance(regnames.overworld + " -> " + regnames.onrac_region).access_rule = \
        lambda state: state.has(itemnames.airship, player)
    world.get_entrance(regnames.overworld + " -> " + regnames.trials_region).access_rule = \
        lambda state: (state.has_all({itemnames.airship, itemnames.canoe}, player)
                       or state.has_all({itemnames.ship, eventnames.canal, itemnames.canoe}, player))
    world.get_entrance(regnames.overworld + " -> " + regnames.gaia_region).access_rule = \
        lambda state: state.has(itemnames.airship, player)
    world.get_entrance(regnames.overworld + " -> " + regnames.mirage_desert).access_rule = \
        lambda state: state.has(itemnames.airship, player)
    world.get_entrance(regnames.overworld + " -> " + regnames.lufenia_region).access_rule = \
        lambda state: state.has(itemnames.airship, player)

    if world.options.northern_docks.value:
        world.get_entrance(regnames.overworld + " -> " + regnames.onrac_region).access_rule = \
            lambda state: (state.has(itemnames.airship, player)
                           or state.has_all({itemnames.ship, eventnames.canal}, player))
        world.get_entrance(regnames.overworld + " -> " + regnames.mirage_desert).access_rule = \
            lambda state: (state.has(itemnames.airship, player)
                           or state.has_all({itemnames.ship, eventnames.canal}, player))

    # Entrance Rules
    world.get_entrance(entnames.overworld_waterfall).access_rule = \
        lambda state: (state.has(itemnames.canoe, player))
    world.get_entrance(entnames.overworld_mirage_tower).access_rule = \
        lambda state: (state.has(itemnames.chime, player))
    world.get_entrance(entnames.onrac_submarine_dock).access_rule = \
        lambda state: (state.has(eventnames.submarine, player))
    world.get_entrance(entnames.cavern_of_earth_b3_center_stairs).access_rule = \
        lambda state: (state.has(itemnames.earth_rod, player))
    world.get_entrance(entnames.citadel_of_trials_1f_throne).access_rule = \
        lambda state: (state.has(itemnames.crown, player))
    world.get_entrance(entnames.mirage_tower_3f_center_warp).access_rule = \
        lambda state: (state.has(itemnames.warp_cube, player))
    # Even if Lute req is a bit deeper, we don't want it to land in Chaos Shrine Beyond
    world.get_entrance(entnames.chaos_shrine_black_orb_warp).access_rule = \
        lambda state: (state.has_all({eventnames.black_orb_destroyed, itemnames.lute}, player)
                       and has_tablatures(state, options, player))

    # Titan
    titan_region = world.get_region(regnames.giants_cavern)
    titan_exits: Dict[str: str] = {}
    for entrance in titan_region.entrances:
        titan_exits[entrance.parent_region.name] = entrance.name + " Exit"

    titan_region.add_exits(titan_exits)

    for titan_exit in titan_exits.values():
        world.get_entrance(titan_exit).access_rule = lambda state: (state.has(eventnames.titan_fed, player))

def set_location_rules(world: "FF1pixelWorld") -> None:
    player = world.player

    # NPCs
    set_rule(world.get_location("Castle Cornelia - Princess"),
             lambda state: state.has(eventnames.garland_defeated, player))
    set_rule(world.get_location("Matoya's Cave - Matoya"),
             lambda state: state.has(itemnames.crystal_eye, player))
    set_rule(world.get_location("Western Keep - Astos"),
             lambda state: state.has(itemnames.crown, player))
    set_rule(world.get_location("Elven Castle - Elf Prince"),
             lambda state: state.has(itemnames.jolt_tonic, player))
    set_rule(world.get_location("Mount Duergar - Smitt"),
             lambda state: state.has(itemnames.adamantite, player))
    set_rule(world.get_location("Sage's Cave - Sarda"),
             lambda state: state.has(eventnames.vampire_defeated, player))
    set_rule(world.get_location("Crescent Lake - Canoe Sage"),
             lambda state: state.has(eventnames.earth_crystal, player))
    set_rule(world.get_location("Gaia - Fairy"),
             lambda state: state.has(itemnames.bottled_faerie, player))
    set_rule(world.get_location("Lufenia - Lufenian Man"),
             lambda state: state.has(eventnames.lufenian_learned, player))

    # Mystic Key locations
    for loc_name in mystic_key_locked_locations:
        set_rule(world.get_location(loc_name),
                 lambda state: state.has(itemnames.mystic_key, player))

    # Star Ruby locations
    for loc_name in titan_fed_locked_locations:
        set_rule(world.get_location(loc_name),
                 lambda state: state.has(eventnames.titan_fed, player))

    # Event Location
    world.get_location("Chaos Shrine - Garland").place_locked_item(world.create_event(eventnames.garland_defeated))
    world.get_location("Mount Duergar - Nerrick").place_locked_item(world.create_event(eventnames.canal))
    set_rule(world.get_location("Mount Duergar - Nerrick"),
             lambda state: state.has(itemnames.nitro_powder, player))
    world.get_location("Cavern of Earth - Vampire").place_locked_item(world.create_event(eventnames.vampire_defeated))
    world.get_location("Giant's Cave - Titan").place_locked_item(world.create_event(eventnames.titan_fed))
    set_rule(world.get_location("Giant's Cave - Titan"),
             lambda state: state.has(itemnames.star_ruby, player))
    world.get_location("Cavern of Earth - Lich").place_locked_item(world.create_event(eventnames.earth_crystal))
    world.get_location("Ryukhan Desert - Airship").place_locked_item(world.create_event(itemnames.airship))
    set_rule(world.get_location("Ryukhan Desert - Airship"),
             lambda state: state.has(itemnames.levistone, player))
    world.get_location("Mount Gulg - Kary").place_locked_item(world.create_event(eventnames.fire_crystal))
    #world.get_location("Caravan").place_locked_item(world.create_event(bottle))
    world.get_location("Onrac - Sub Engineer").place_locked_item(world.create_event(eventnames.submarine))
    set_rule(world.get_location("Onrac - Sub Engineer"),
             lambda state: state.has(itemnames.oxyale, player))
    world.get_location("Sunken Shrine - Kraken").place_locked_item(world.create_event(eventnames.water_crystal))
    world.get_location("Melmond - Dr Unne").place_locked_item(world.create_event(eventnames.lufenian_learned))
    set_rule(world.get_location("Melmond - Dr Unne"),
             lambda state: state.has(itemnames.rosetta_stone, player))
    world.get_location("Flying Fortress - Tiamat").place_locked_item(world.create_event(eventnames.air_crystal))
    world.get_location("Chaos Shrine - Black Orb").place_locked_item(world.create_event(eventnames.black_orb_destroyed))
    set_rule(world.get_location("Chaos Shrine - Black Orb"),
             lambda state: has_crystals(state, world.options, player))
    world.get_location("Chaos Shrine - Chaos").place_locked_item(world.create_event(eventnames.chaos_defeated))

    # Ship Logic
    if world.options.early_progression.value == 0 and not world.spawn_ship:
        world.get_location("Pravoka - Bikke").place_locked_item(world.create_item(itemnames.ship))

    # Bahamut
    set_rule(world.get_location("Dragon Caves - Bahamut"),
        lambda state: state.has(itemnames.rats_tail, player))
    if world.options.job_promotion.value == 0:
        world.get_location("Dragon Caves - Bahamut").place_locked_item(world.create_item(itemnames.all_promo_jobs))

    # Prevent Gil landing in the Caravan
    for item_name, item_value in item_table.items():
        if item_value.item_id_offset == 1:
            forbid_item(world.get_location("Onrac Desert - Caravan"), item_name, player)

    # Victory Condition
    world.multiworld.completion_condition[world.player] = lambda state: state.has(eventnames.chaos_defeated, world.player)

