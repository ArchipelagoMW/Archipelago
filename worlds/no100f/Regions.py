from typing import List, Dict

from . import NO100FOptions
from .Locations import NO100FLocation, location_table, \
    upgrade_location_table, monstertoken_location_table, key_location_table, warpgate_location_table, \
    snack_location_table
from .names import ConnectionNames, LevelNames, RegionNames, LocationNames

from BaseClasses import MultiWorld, Region, Entrance


def create_region(multiworld: MultiWorld, player: int, name: str, locations=None, exits=None) -> Region:
    ret = Region(name, player, multiworld)
    if locations:
        for location in locations:
            loc_id = location_table[location]
            location = NO100FLocation(player, location, loc_id, ret)
            ret.locations.append(location)

    if exits:
        for _exit in exits:
            ret.exits.append(Entrance(player, _exit, ret))
    return ret


def _get_locations_for_region(options: NO100FOptions, name: str) -> List[str]:
    result = [k for k in upgrade_location_table if f"{name}:" in k]
    if name == RegionNames.hub1:
        result += [k for k in upgrade_location_table if f"{LevelNames.hub}:" in k]
    if name == RegionNames.s005:
        result += [LocationNames.Credits]
    if options.include_monster_tokens.value:
        result += [k for k in monstertoken_location_table if f"{name}:" in k]
    if options.include_keys.value:
        result += [k for k in key_location_table if f"{name}:" in k]
    if options.include_warpgates.value:
        result += [k for k in warpgate_location_table if f"{name}:" in k]
    if options.include_snacks.value:
        result += [k for k in snack_location_table if f"{name}:" in k]
    return result


exit_table: Dict[str, List[str]] = {

    RegionNames.menu: [ConnectionNames.start_game],

    RegionNames.hub1: [ConnectionNames.hub1_f001, ConnectionNames.hub1_hub2, ConnectionNames.hub1_hub3,
                       ConnectionNames.hub1_e001, ConnectionNames.hub1_i001,
                       ConnectionNames.hub1_b004, ConnectionNames.hub1_c004, ConnectionNames.hub1_e004,
                       ConnectionNames.hub1_e006, ConnectionNames.hub1_e009, ConnectionNames.hub1_f003,
                       ConnectionNames.hub1_f007, ConnectionNames.hub1_o001, ConnectionNames.hub1_o004,
                       ConnectionNames.hub1_o006, ConnectionNames.hub1_g001, ConnectionNames.hub1_g005,
                       ConnectionNames.hub1_g008, ConnectionNames.hub1_i003, ConnectionNames.hub1_i006,
                       ConnectionNames.hub1_l014, ConnectionNames.hub1_l015, ConnectionNames.hub1_l018,
                       ConnectionNames.hub1_p003, ConnectionNames.hub1_p005, ConnectionNames.hub1_r003,
                       ConnectionNames.hub1_s002, ConnectionNames.hub1_w022, ConnectionNames.hub1_w026,],
    RegionNames.hub2: [ConnectionNames.hub2_hub1],
    RegionNames.hub3: [ConnectionNames.hub3_hub1],

    # (B)asement
    RegionNames.b001: [ConnectionNames.b001_b002, ConnectionNames.b001_p005],
    RegionNames.b002: [ConnectionNames.b002_b001, ConnectionNames.b002_b003],
    RegionNames.b003: [ConnectionNames.b003_b001, ConnectionNames.b003_b002, ConnectionNames.b003_b004,
                       ConnectionNames.b003_p004],
    RegionNames.b004: [ConnectionNames.b004_i003],

    # (C)liff
    RegionNames.c001: [ConnectionNames.c001_c002, ConnectionNames.c001_e009],
    RegionNames.c002: [ConnectionNames.c002_c001, ConnectionNames.c002_c003],
    RegionNames.c003: [ConnectionNames.c003_c002, ConnectionNames.c003_c004],
    RegionNames.c004: [ConnectionNames.c004_c003, ConnectionNames.c004_c005],
    RegionNames.c005: [ConnectionNames.c005_c004, ConnectionNames.c005_c006, ConnectionNames.c005_e003],
    RegionNames.c006: [ConnectionNames.c006_c005, ConnectionNames.c006_c007],
    RegionNames.c007: [ConnectionNames.c007_c006, ConnectionNames.c007_g001],

    # H(e)dge Maze
    RegionNames.e001: [ConnectionNames.e001_e002, ConnectionNames.e001_hub1],
    RegionNames.e002: [ConnectionNames.e002_e001, ConnectionNames.e002_e003],
    RegionNames.e003: [ConnectionNames.e003_e002, ConnectionNames.e003_e004, ConnectionNames.e003_c005],
    RegionNames.e004: [ConnectionNames.e004_e005],
    RegionNames.e005: [ConnectionNames.e005_e004, ConnectionNames.e005_e006],
    RegionNames.e006: [ConnectionNames.e006_e005, ConnectionNames.e006_e007],
    RegionNames.e007: [ConnectionNames.e007_e006, ConnectionNames.e007_e008],
    RegionNames.e008: [ConnectionNames.e008_e007, ConnectionNames.e008_e009],
    RegionNames.e009: [ConnectionNames.e009_e001, ConnectionNames.e009_e008, ConnectionNames.e009_c001],

    # Fishing Village
    RegionNames.f001: [ConnectionNames.f001_f003, ConnectionNames.f001_hub1],
    RegionNames.f003: [ConnectionNames.f003_f004, ConnectionNames.f003_f009,
                       ConnectionNames.f003_p001],
    RegionNames.f004: [ConnectionNames.f004_f003, ConnectionNames.f004_f005],
    RegionNames.f005: [ConnectionNames.f005_f004, ConnectionNames.f005_f006],
    RegionNames.f006: [ConnectionNames.f006_f005, ConnectionNames.f006_f007],
    RegionNames.f007: [ConnectionNames.f007_f006, ConnectionNames.f007_f008],
    RegionNames.f008: [ConnectionNames.f008_f007, ConnectionNames.f008_f009, ConnectionNames.f008_l011,
                       ConnectionNames.f008_hub1],
    RegionNames.f009: [ConnectionNames.f009_f003, ConnectionNames.f009_f008, ConnectionNames.f009_f010],
    RegionNames.f010: [ConnectionNames.f010_f009],

    # Graveyard
    RegionNames.g001: [ConnectionNames.g001_g002],
    RegionNames.g002: [ConnectionNames.g002_g001, ConnectionNames.g002_g003],
    RegionNames.g003: [ConnectionNames.g003_g002, ConnectionNames.g003_g004, ConnectionNames.g003_g005,
                       ConnectionNames.g003_g006],
    RegionNames.g004: [ConnectionNames.g004_g003],
    RegionNames.g005: [ConnectionNames.g005_g003, ConnectionNames.g005_g006, ConnectionNames.g005_g007],
    RegionNames.g006: [ConnectionNames.g006_g003, ConnectionNames.g006_g005],
    RegionNames.g007: [ConnectionNames.g007_g005, ConnectionNames.g007_g008],
    RegionNames.g008: [ConnectionNames.g008_g003, ConnectionNames.g008_g007, ConnectionNames.g008_g009],
    RegionNames.g009: [ConnectionNames.g009_g008, ConnectionNames.g009_hub1],

    # Myst(i)c Manor
    RegionNames.i001: [ConnectionNames.i001_i020, ConnectionNames.i001_hub1],
    RegionNames.i003: [ConnectionNames.i003_i004, ConnectionNames.i003_i021, ConnectionNames.i003_b004],
    RegionNames.i004: [ConnectionNames.i004_o001, ConnectionNames.i004_i003, ConnectionNames.i004_i005],
    RegionNames.i005: [ConnectionNames.i005_i004, ConnectionNames.i005_i006],
    RegionNames.i006: [ConnectionNames.i006_i005, ConnectionNames.i006_r001],
    RegionNames.i020: [ConnectionNames.i020_i001, ConnectionNames.i020_i021],
    RegionNames.i021: [ConnectionNames.i021_i003, ConnectionNames.i021_i020],

    # Lighthouse
    RegionNames.l011: [ConnectionNames.l011_f008, ConnectionNames.l011_l013],
    RegionNames.l013: [ConnectionNames.l013_l014, ConnectionNames.l013_l011],
    RegionNames.l014: [ConnectionNames.l014_l013, ConnectionNames.l014_l015],
    RegionNames.l015: [ConnectionNames.l015_l014, ConnectionNames.l015_l018, ConnectionNames.l015_l017,
                       ConnectionNames.l015_l019, ConnectionNames.l015_w020],
    RegionNames.l017: [ConnectionNames.l017_l015, ConnectionNames.l017_l018],
    RegionNames.l018: [ConnectionNames.l018_l015, ConnectionNames.l018_p001],
    RegionNames.l019: [ConnectionNames.l019_l015, ConnectionNames.l019_l018],

    # R(O)oftops
    RegionNames.o001: [ConnectionNames.o001_o002, ConnectionNames.o001_o008, ConnectionNames.o001_r005],
    RegionNames.o002: [ConnectionNames.o002_o001, ConnectionNames.o002_o003],
    RegionNames.o003: [ConnectionNames.o003_o002, ConnectionNames.o003_o004],
    RegionNames.o004: [ConnectionNames.o004_o003, ConnectionNames.o004_o005],
    RegionNames.o005: [ConnectionNames.o005_o004, ConnectionNames.o005_o006],
    RegionNames.o006: [ConnectionNames.o006_o005, ConnectionNames.o006_o008, ConnectionNames.o006_sn],
    RegionNames.o006_sn: [],
    RegionNames.o008: [ConnectionNames.o008_o001, ConnectionNames.o008_o006],

    # Secret (P)assage
    RegionNames.p001: [ConnectionNames.p001_p002, ConnectionNames.p001_l018],
    RegionNames.p002: [ConnectionNames.p002_p001, ConnectionNames.p002_p003, ConnectionNames.p002_s001],
    RegionNames.p003: [ConnectionNames.p003_p002, ConnectionNames.p003_p004],
    RegionNames.p004: [ConnectionNames.p004_p005],
    RegionNames.p005: [ConnectionNames.p005_p001, ConnectionNames.p005_p004, ConnectionNames.p005_b001],

    # Balcony (R)
    RegionNames.r001: [ConnectionNames.r001_r020, ConnectionNames.r001_i001, ConnectionNames.r001_i006],
    RegionNames.r003: [ConnectionNames.r003_r004, ConnectionNames.r003_r021],
    RegionNames.r004: [ConnectionNames.r004_r003, ConnectionNames.r004_r005],
    RegionNames.r005: [ConnectionNames.r005_o001, ConnectionNames.r005_r004],
    RegionNames.r020: [ConnectionNames.r020_r001, ConnectionNames.r020_r021],
    RegionNames.r021: [ConnectionNames.r021_r003, ConnectionNames.r021_r020],

    # Super Secret Lab
    RegionNames.s001: [ConnectionNames.s001_s002, ConnectionNames.s001_p002],
    RegionNames.s002: [ConnectionNames.s002_s003, ConnectionNames.s002_s004],
    RegionNames.s003: [ConnectionNames.s003_s002],
    RegionNames.s004: [ConnectionNames.s004_s002, ConnectionNames.s004_s005],
    RegionNames.s005: [ConnectionNames.s005_s004, ConnectionNames.s005_s006],
    RegionNames.s006: [ConnectionNames.s006_s005],

    # Wrecked Ships
    RegionNames.w020: [ConnectionNames.w020_w021],
    RegionNames.w021: [ConnectionNames.w021_w020, ConnectionNames.w021_w022],
    RegionNames.w022: [ConnectionNames.w022_w021, ConnectionNames.w022_w023],
    RegionNames.w023: [ConnectionNames.w023_w022, ConnectionNames.w023_w025],
    RegionNames.w025: [ConnectionNames.w025_w023, ConnectionNames.w025_w026],
    RegionNames.w026: [ConnectionNames.w026_w020, ConnectionNames.w026_w027, ConnectionNames.w026_w028],
    RegionNames.w027: [ConnectionNames.w027_w026, ConnectionNames.w027_w028],
    RegionNames.w028: [ConnectionNames.w028_w026],

}


def create_regions(world: MultiWorld, options: NO100FOptions, player: int):
    # create regions
    world.regions += [
        create_region(world, player, k, _get_locations_for_region(options, k), v) for k, v in exit_table.items()
    ]

    # connect regions
    world.get_entrance(ConnectionNames.start_game, player).connect(world.get_region(RegionNames.hub1, player))
    for k, v in exit_table.items():
        if k == RegionNames.menu:
            continue
        for _exit in v:
            exit_regions = _exit.split('->')
            assert len(exit_regions) == 2
            target = world.get_region(exit_regions[1], player)
            world.get_entrance(_exit, player).connect(target)
