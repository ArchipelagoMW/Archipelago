from BaseClasses import Region
from typing import TYPE_CHECKING
from .names import item_names, location_names
from .locations import (green_greens_locations, float_islands_locations, bubbly_clouds_locations, mt_dedede_locations,
                        peanut_plains_locations, mallow_castle_locations, cocoa_cave_locations, candy_mountain_locations,
                        dyna_blade_nest_locations, gourmet_race_locations, subtree_locations, crystal_locations,
                        old_tower_locations, garden_locations, romk_chapter_1_locations, romk_chapter_2_locations,
                        romk_chapter_3_locations, romk_chapter_4_locations, romk_chapter_5_locations,
                        romk_chapter_6_locations, romk_chapter_7_locations, floria_locations, aqualiss_locations,
                        skyhigh_locations, hotbeat_locations, cavios_locations, mecheye_locations, halfmoon_locations,
                        copy_planet_locations, space_locations, the_arena_locations, KSSLocation, LocationData,
                        bonus_1_locations, bonus_2_locations)
from .options import IncludedSubgames

if TYPE_CHECKING:
    from . import KSSWorld


class KSSRegion(Region):
    game = "Kirby Super Star"


def create_region(name, world: "KSSWorld") -> KSSRegion:
    return KSSRegion(name, world.player, world.multiworld)


def add_locations(world: "KSSWorld", region: KSSRegion, locations: dict[str, LocationData]) -> None:
    filter_list = [""]
    if "Maxim Tomato" in world.options.consumables:
        filter_list.append("maxim")
    if "1-Up" in world.options.consumables:
        filter_list.append("one_up")
    if "Invincibility Candy" in world.options.consumables:
        filter_list.append("candy")
    if "Arena Maxim Tomato" in world.options.consumables:
        filter_list.append("arena_maxim")
    if world.options.essences:
        filter_list.append("essence")

    filtered = {location: data.code for location, data in locations.items() if data.tag in filter_list}

    region.add_locations(filtered, KSSLocation)


def create_trivial_regions(world: "KSSWorld", menu: KSSRegion, included_subgames: set[str]) -> None:
    if "Gourmet Race" in included_subgames:
        gourmet_race = create_region("Gourmet Race", world)
        add_locations(world, gourmet_race, gourmet_race_locations)
        menu.connect(gourmet_race, None, lambda state: state.has(item_names.gourmet_race, world.player))
        world.get_location(location_names.gr_complete).place_locked_item(
            world.create_item(item_names.gourmet_race_complete))
        world.multiworld.regions.append(gourmet_race)

    if "The Arena" in included_subgames:
        arena = create_region("The Arena", world)
        add_locations(world, arena, the_arena_locations)
        menu.connect(arena, None, lambda state: state.has(item_names.the_arena, world.player))
        world.get_location(location_names.arena_complete).place_locked_item(
            world.create_item(item_names.the_arena_complete))
        world.multiworld.regions.append(arena)


def create_spring_breeze(world: "KSSWorld", menu: KSSRegion) -> None:
    spring_breeze = create_region("Spring Breeze", world)
    green_greens = create_region("Green Greens", world)
    float_islands = create_region("Float Islands", world)
    bubbly_clouds = create_region("Bubbly Clouds", world)
    mt_dedede = create_region("Mt. Dedede", world)

    for region, connection, locations in zip((green_greens, float_islands, bubbly_clouds, mt_dedede),
                                             (float_islands, bubbly_clouds, mt_dedede, None),
                                             (green_greens_locations, float_islands_locations, bubbly_clouds_locations,
                                              mt_dedede_locations)
                                             ):
        if connection:
            region.connect(connection)
        add_locations(world, region, locations)

    menu.connect(spring_breeze, None, lambda state: state.has(item_names.spring_breeze, world.player))
    spring_breeze.connect(green_greens)
    world.get_location(location_names.sb_complete).place_locked_item(
        world.create_item(item_names.spring_breeze_complete))
    world.multiworld.regions.extend([spring_breeze, green_greens, float_islands, bubbly_clouds, mt_dedede])


def create_dyna_blade(world: "KSSWorld", menu: KSSRegion) -> None:
    dyna_blade = create_region("Dyna Blade", world)
    peanut_plains = create_region("Peanut Plains", world)
    mallow_castle = create_region("Mallow Castle", world)
    cocoa_cave = create_region("Cocoa Cave", world)
    candy_mountain = create_region("Candy Mountain", world)
    dyna_blade_nest = create_region("Dyna Blade's Nest", world)

    region: KSSRegion
    connection: KSSRegion
    locations: dict[str, LocationData]

    for i, (region, connection, locations) in enumerate(
                                        zip((peanut_plains, mallow_castle, cocoa_cave, candy_mountain, dyna_blade_nest),
                                             (mallow_castle, cocoa_cave, candy_mountain, dyna_blade_nest, None),
                                             (peanut_plains_locations, mallow_castle_locations, cocoa_cave_locations,
                                              candy_mountain_locations, dyna_blade_nest_locations)
                                             )):
        if connection:
            access_rule = lambda state, x=i + 1: state.has(item_names.progressive_dyna_blade, world.player, x)
            region.connect(connection, rule=access_rule)
        add_locations(world, region, locations)

    menu.connect(dyna_blade, None, lambda state: state.has(item_names.dyna_blade, world.player))
    dyna_blade.connect(peanut_plains)
    world.get_location(location_names.db_complete).place_locked_item(world.create_item(item_names.dyna_blade_complete))
    world.multiworld.regions.extend([dyna_blade, peanut_plains, mallow_castle, cocoa_cave,
                                     candy_mountain, dyna_blade_nest])

    if world.options.essences or "Maxim Tomato" in world.options.consumables:
        extra1 = create_region("Dyna Blade Bonus 1", world)
        extra2 = create_region("Dyna Blade Bonus 2", world)
        for locations, region in zip((bonus_1_locations, bonus_2_locations), (extra1, extra2)):
            add_locations(world, region, locations)
            dyna_blade.connect(region)
            world.multiworld.regions.append(region)


def create_great_cave_offensive(world: "KSSWorld", menu: KSSRegion) -> None:
    tgco = create_region("The Great Cave Offensive", world)
    subtree = create_region("Sub-Tree", world)
    crystal = create_region("Crystal", world)
    old_tower = create_region("Old Tower", world)
    garden = create_region("Garden", world)

    for region, connection, locations in zip((subtree, crystal, old_tower, garden),
                                             (crystal, old_tower, garden, None),
                                             (subtree_locations, crystal_locations, old_tower_locations,
                                              garden_locations)
                                             ):
        if connection:
            region.connect(connection)
        add_locations(world, region, locations)

    menu.connect(tgco, None, lambda state: state.has(item_names.great_cave_offensive, world.player))
    tgco.connect(subtree)
    world.get_location(location_names.tgco_complete).place_locked_item(
        world.create_item(item_names.great_cave_offensive_complete))
    world.multiworld.regions.extend([tgco, subtree, crystal, old_tower, garden])


def create_revenge_meta_knight(world: "KSSWorld", menu: KSSRegion) -> None:
    revenge_of_meta_knight = create_region("Revenge of Meta Knight", world)
    chapter_1 = create_region("RoMK - Chapter 1", world)
    chapter_2 = create_region("RoMK - Chapter 2", world)
    chapter_3 = create_region("RoMK - Chapter 3", world)
    chapter_4 = create_region("RoMK - Chapter 4", world)
    chapter_5 = create_region("RoMK - Chapter 5", world)
    chapter_6 = create_region("RoMK - Chapter 6", world)
    chapter_7 = create_region("RoMK - Chapter 7", world)

    for region, connection, locations in zip((chapter_1, chapter_2, chapter_3, chapter_4,
                                              chapter_5, chapter_6, chapter_7),
                                             (chapter_2, chapter_3, chapter_4, chapter_5,
                                              chapter_6, chapter_7, None),
                                             (romk_chapter_1_locations, romk_chapter_2_locations,
                                              romk_chapter_3_locations, romk_chapter_4_locations,
                                              romk_chapter_5_locations, romk_chapter_6_locations,
                                              romk_chapter_7_locations)
                                             ):
        if connection:
            region.connect(connection)
        add_locations(world, region, locations)

    menu.connect(revenge_of_meta_knight, None, lambda state: state.has(item_names.revenge_of_meta_knight, world.player))
    revenge_of_meta_knight.connect(chapter_1)
    world.get_location(location_names.romk_complete).place_locked_item(
        world.create_item(item_names.revenge_of_meta_knight_complete))

    world.multiworld.regions.extend([revenge_of_meta_knight, chapter_1, chapter_2, chapter_3, chapter_4, chapter_5,
                                     chapter_6, chapter_7])


def create_milky_way_wishes(world: "KSSWorld", menu: KSSRegion) -> None:
    milky_way_wishes = create_region("Milky Way Wishes", world)
    floria = create_region("Floria", world)
    aqualiss = create_region("Aqualiss", world)
    skyhigh = create_region("Skyhigh", world)
    hotbeat = create_region("Hotbeat", world)
    cavios = create_region("Cavios", world)
    mecheye = create_region("Mecheye", world)
    halfmoon = create_region("Halfmoon", world)
    copy_planet = create_region("???", world)

    for region, locations, item in zip((floria, aqualiss, skyhigh, hotbeat, cavios, mecheye, halfmoon, copy_planet),
                                       (floria_locations, aqualiss_locations, skyhigh_locations, hotbeat_locations,
                                        cavios_locations, mecheye_locations, halfmoon_locations, copy_planet_locations),
                                       (item_names.floria, item_names.aqualiss, item_names.skyhigh, item_names.hotbeat,
                                        item_names.cavios, item_names.mecheye, item_names.halfmoon,
                                        item_names.copy_planet)
                                 ):
        add_locations(world, region, locations)
        milky_way_wishes.connect(region, None, lambda state, required=item: state.has(required, world.player))

    add_locations(world, milky_way_wishes, space_locations)
    menu.connect(milky_way_wishes, None, lambda state: state.has(item_names.milky_way_wishes, world.player))

    world.get_location(location_names.mww_complete).place_locked_item(
        world.create_item(item_names.milky_way_wishes_complete))

    world.multiworld.regions.extend([milky_way_wishes, floria, aqualiss, skyhigh, hotbeat, cavios,
                                     mecheye, halfmoon, copy_planet])


def create_regions(world: "KSSWorld") -> None:
    menu = create_region("Menu", world)
    world.multiworld.regions.append(menu)
    included_subgames = world.options.included_subgames.value
    create_trivial_regions(world, menu, included_subgames)
    if "Spring Breeze" in included_subgames:
        create_spring_breeze(world, menu)
    if "Dyna Blade" in included_subgames:
        create_dyna_blade(world, menu)
    if "The Great Cave Offensive" in included_subgames:
        create_great_cave_offensive(world, menu)
    if "Revenge of Meta Knight" in included_subgames:
        create_revenge_meta_knight(world, menu)
    if "Milky Way Wishes" in included_subgames:
        create_milky_way_wishes(world, menu)
