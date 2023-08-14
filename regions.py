import typing

from BaseClasses import MultiWorld, Region, Entrance

from .locations import WL4Location
from .names import LocationName, ItemName, RegionName


def create_regions(world: MultiWorld, player: int, location_table: dict):
    menu_region = create_region(world, player, location_table, "Menu")
    map_region = create_region(world, player, location_table, RegionName.map)

    entry_passage = create_region(
        world,
        player,
        location_table,
        RegionName.entry_passage
    )
    hall_of_hieroglyphs = create_region(
        world,
        player,
        location_table,
        RegionName.hall_of_hieroglyphs,
        LocationName.hall_of_hieroglyphs.locations(),
    )
    spoiled_rotten = create_region(
        world,
        player,
        location_table,
        RegionName.spoiled_rotten,
        [LocationName.spoiled_rotten],
    )

    emerald_passage = create_region(
        world,
        player,
        location_table,
        RegionName.emerald_passage
    )
    palm_tree_paradise = create_region(
        world,
        player,
        location_table,
        RegionName.palm_tree_paradise,
        LocationName.palm_tree_paradise.locations(),
    )
    wildflower_fields = create_region(
        world,
        player,
        location_table,
        RegionName.wildflower_fields,
        LocationName.wildflower_fields.locations(),
    )
    mystic_lake = create_region(
        world,
        player,
        location_table,
        RegionName.mystic_lake,
        LocationName.mystic_lake.locations(),
    )
    monsoon_jungle = create_region(
        world,
        player,
        location_table,
        RegionName.monsoon_jungle,
        LocationName.monsoon_jungle.locations(),
    )
    cractus = create_region(
        world,
        player,
        location_table,
        RegionName.cractus,
        [LocationName.cractus],
    )

    ruby_passage = create_region(
        world,
        player,
        location_table,
        RegionName.ruby_passage
    )
    curious_factory = create_region(
        world,
        player,
        location_table,
        RegionName.curious_factory,
        LocationName.curious_factory.locations(),
    )
    toxic_landfill = create_region(
        world,
        player,
        location_table,
        RegionName.toxic_landfill,
        LocationName.toxic_landfill.locations(),
    )
    forty_below_fridge = create_region(
        world,
        player,
        location_table,
        RegionName.forty_below_fridge,
        LocationName.forty_below_fridge.locations(),
    )
    pinball_zone = create_region(
        world,
        player,
        location_table,
        RegionName.pinball_zone,
        LocationName.pinball_zone.locations(),
    )
    cuckoo_condor = create_region(
        world,
        player,
        location_table,
        RegionName.cuckoo_condor,
        [LocationName.cuckoo_condor],
    )

    topaz_passage = create_region(
        world,
        player,
        location_table,
        RegionName.topaz_passage
    )
    toy_block_tower = create_region(
        world,
        player,
        location_table,
        RegionName.toy_block_tower,
        LocationName.toy_block_tower.locations(),
    )
    big_board = create_region(
        world,
        player,
        location_table,
        RegionName.big_board,
        LocationName.big_board.locations(),
    )
    doodle_woods = create_region(
        world,
        player,
        location_table,
        RegionName.doodle_woods,
        LocationName.doodle_woods.locations(),
    )
    domino_row = create_region(
        world,
        player,
        location_table,
        RegionName.domino_row,
        LocationName.domino_row.locations(),
    )
    aerodent = create_region(
        world,
        player,
        location_table,
        RegionName.aerodent,
        [LocationName.aerodent],
    )

    sapphire_passage = create_region(
        world,
        player,
        location_table,
        RegionName.sapphire_passage
    )
    crescent_moon_village = create_region(
        world,
        player,
        location_table,
        RegionName.crescent_moon_village,
        LocationName.crescent_moon_village.locations(),
    )
    arabian_night = create_region(
        world,
        player,
        location_table,
        RegionName.arabian_night,
        LocationName.arabian_night.locations(),
    )
    fiery_cavern = create_region(
        world,
        player,
        location_table,
        RegionName.fiery_cavern,
        LocationName.fiery_cavern.locations(),
    )
    hotel_horror = create_region(
        world,
        player,
        location_table,
        RegionName.hotel_horror,
        LocationName.hotel_horror.locations(),
    )
    catbat = create_region(
        world,
        player,
        location_table,
        RegionName.catbat,
        [LocationName.catbat],
    )

    golden_pyramid = create_region(
        world,
        player,
        location_table,
        RegionName.golden_pyramid
    )
    golden_passage = create_region(
        world,
        player,
        location_table,
        RegionName.golden_passage,
        LocationName.golden_passage.jewels,
    )
    golden_diva = create_region(
        world,
        player,
        location_table,
        RegionName.golden_diva,
        [LocationName.golden_diva],
    )

    world.regions += [
        menu_region,
        map_region,
        entry_passage,
        hall_of_hieroglyphs,
        spoiled_rotten,
        emerald_passage,
        palm_tree_paradise,
        wildflower_fields,
        mystic_lake,
        monsoon_jungle,
        cractus,
        ruby_passage,
        curious_factory,
        toxic_landfill,
        forty_below_fridge,
        pinball_zone,
        cuckoo_condor,
        topaz_passage,
        toy_block_tower,
        big_board,
        doodle_woods,
        domino_row,
        aerodent,
        sapphire_passage,
        crescent_moon_village,
        arabian_night,
        fiery_cavern,
        hotel_horror,
        catbat,
        golden_pyramid,
        golden_passage,
        golden_diva,
    ]


def connect_regions(world, player):
    names: typing.Dict[str, int] = {}

    connect(world, player, names, "Menu", RegionName.entry_passage)
    connect(world, player, names, RegionName.entry_passage, RegionName.hall_of_hieroglyphs)
    connect(world, player, names, RegionName.hall_of_hieroglyphs, RegionName.spoiled_rotten,
        lambda state: state.wl4_has_full_jewels(player, ItemName.entry_passage_jewel, 1))
    connect(world, player, names, "Menu", RegionName.map,
        lambda state: state.has(ItemName.defeated_boss, player))

    connect(world, player, names, RegionName.map, RegionName.emerald_passage)
    connect(world, player, names, RegionName.emerald_passage, RegionName.palm_tree_paradise)
    connect(world, player, names, RegionName.palm_tree_paradise, RegionName.wildflower_fields)
    connect(world, player, names, RegionName.wildflower_fields, RegionName.mystic_lake)
    connect(world, player, names, RegionName.mystic_lake, RegionName.monsoon_jungle)
    connect(world, player, names, RegionName.monsoon_jungle, RegionName.cractus,
        lambda state: state.wl4_has_full_jewels(player, ItemName.emerald_passage_jewel, 4))

    connect(world, player, names, RegionName.map, RegionName.ruby_passage)
    connect(world, player, names, RegionName.ruby_passage, RegionName.curious_factory)
    connect(world, player, names, RegionName.curious_factory, RegionName.toxic_landfill)
    connect(world, player, names, RegionName.toxic_landfill, RegionName.forty_below_fridge)
    connect(world, player, names, RegionName.forty_below_fridge, RegionName.pinball_zone)
    connect(world, player, names, RegionName.pinball_zone, RegionName.cuckoo_condor,
        lambda state: state.wl4_has_full_jewels(player, ItemName.ruby_passage_jewel, 4))

    connect(world, player, names, RegionName.map, RegionName.topaz_passage)
    connect(world, player, names, RegionName.topaz_passage, RegionName.toy_block_tower)
    connect(world, player, names, RegionName.toy_block_tower, RegionName.big_board)
    connect(world, player, names, RegionName.big_board, RegionName.doodle_woods)
    connect(world, player, names, RegionName.doodle_woods, RegionName.domino_row)
    connect(world, player, names, RegionName.domino_row, RegionName.aerodent,
        lambda state: state.wl4_has_full_jewels(player, ItemName.topaz_passage_jewel, 4))

    connect(world, player, names, RegionName.map, RegionName.sapphire_passage)
    connect(world, player, names, RegionName.sapphire_passage, RegionName.crescent_moon_village)
    connect(world, player, names, RegionName.crescent_moon_village, RegionName.arabian_night)
    connect(world, player, names, RegionName.arabian_night, RegionName.fiery_cavern)
    connect(world, player, names, RegionName.fiery_cavern, RegionName.hotel_horror)
    connect(world, player, names, RegionName.hotel_horror, RegionName.catbat,
        lambda state: state.wl4_has_full_jewels(player, ItemName.sapphire_passage_jewel, 4))

    connect(world, player, names, RegionName.map, RegionName.golden_pyramid,
        lambda state: (state.has(ItemName.defeated_boss, player, 5)))
    connect(world, player, names, RegionName.golden_pyramid, RegionName.golden_passage)
    connect(world, player, names, RegionName.golden_passage, RegionName.golden_diva,
        lambda state: state.wl4_has_full_jewels(player, ItemName.golden_pyramid_jewel, 1))


def create_region(
    world: MultiWorld,
    player: int,
    location_table: dict,
    name: str,
    locations: typing.Sequence[str] = ()
):
    region = Region(name, player, world)
    for location in locations:
        try:
            id = location_table[location]
            region.locations.append(WL4Location(player, location, id, region))
        except KeyError:
            pass
    return region


def connect(
    world: MultiWorld,
    player: int,
    used_names: typing.Dict[str, int],
    source: str,
    target: str,
    rule: typing.Optional[typing.Callable] = None,
):
    source_region = world.get_region(source, player)
    target_region = world.get_region(target, player)

    if target not in used_names:
        used_names[target] = 1
        name = target
    else:
        used_names[target] += 1
        name = target + (' ' * used_names[target])
    
    connection = Entrance(player, name, source_region)

    if rule:
        connection.access_rule = rule
    
    source_region.exits.append(connection)
    connection.connect(target_region)
