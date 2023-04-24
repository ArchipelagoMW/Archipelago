from dataclasses import dataclass, field
from enum import IntFlag
from random import Random
from typing import Iterable, Dict, Protocol, Optional, List, Tuple

from BaseClasses import Region, Entrance
from . import options
from .data.entrance_data import SVEntrance
from .data.region_data import SVRegion
from .options import StardewOptions


class RegionFactory(Protocol):
    def __call__(self, name: str, regions: Iterable[str]) -> Region:
        raise NotImplementedError


class RandomizationFlag(IntFlag):
    NOT_RANDOMIZED = 0b0
    PELICAN_TOWN = 0b11111
    NON_PROGRESSION = 0b11110
    BUILDINGS = 0b11100
    EVERYTHING = 0b11000
    CHAOS = 0b10000


@dataclass(frozen=True)
class RegionData:
    name: str
    exits: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class ConnectionData:
    name: str
    destination: str
    reverse: Optional[str] = None
    flag: RandomizationFlag = RandomizationFlag.NOT_RANDOMIZED

    def __post_init__(self):
        if self.reverse is None and " to " in self.name:
            origin, destination = self.name.split(" to ")
            super().__setattr__("reverse", f"{destination} to {origin}")


stardew_valley_regions = [
    RegionData(SVRegion.menu, [SVEntrance.to_stardew_valley]),
    RegionData(SVRegion.stardew_valley, [SVEntrance.to_farmhouse]),
    RegionData(SVRegion.farm_house, [SVEntrance.outside_to_farm, SVEntrance.downstairs_to_cellar]),
    RegionData(SVRegion.cellar),
    RegionData(SVRegion.farm,
               [SVEntrance.farm_to_backwoods, SVEntrance.farm_to_bus_stop, SVEntrance.farm_to_forest, SVEntrance.farm_to_farmcave, SVEntrance.enter_greenhouse,
                SVEntrance.use_desert_obelisk, SVEntrance.use_island_obelisk]),
    RegionData(SVRegion.backwoods, [SVEntrance.backwoods_to_mountain]),
    RegionData(SVRegion.bus_stop, [SVEntrance.bus_stop_to_town, SVEntrance.take_bus_to_desert, SVEntrance.bus_stop_to_tunnel_entrance]),
    RegionData(SVRegion.forest, [SVEntrance.forest_to_town, SVEntrance.enter_secret_woods, SVEntrance.forest_to_wizard_tower, SVEntrance.forest_to_marnie_ranch,
                                 SVEntrance.forest_to_leah_cottage, SVEntrance.forest_to_sewers, SVEntrance.talk_to_traveling_merchant]),
    RegionData(SVRegion.traveling_cart),
    RegionData(SVRegion.farm_cave),
    RegionData(SVRegion.greenhouse),
    RegionData(SVRegion.mountain,
               [SVEntrance.mountain_to_railroad, SVEntrance.mountain_to_tent, SVEntrance.mountain_to_carpenter_shop, SVEntrance.mountain_to_the_mines,
                SVEntrance.enter_quarry, SVEntrance.mountain_to_adventurer_guild, SVEntrance.mountain_to_town]),
    RegionData(SVRegion.tunnel_entrance, [SVEntrance.enter_tunnel]),
    RegionData(SVRegion.tunnel),
    RegionData(SVRegion.town, [SVEntrance.town_to_community_center, SVEntrance.town_to_beach, SVEntrance.town_to_hospital,
                               SVEntrance.town_to_pierre_general_store, SVEntrance.town_to_saloon, SVEntrance.town_to_alex_house, SVEntrance.town_to_trailer,
                               SVEntrance.town_to_mayor_manor,
                               SVEntrance.town_to_sam_house, SVEntrance.town_to_haley_house, SVEntrance.town_to_sewers, SVEntrance.town_to_clint_blacksmith,
                               SVEntrance.town_to_museum,
                               SVEntrance.town_to_jojamart]),
    RegionData(SVRegion.beach, [SVEntrance.beach_to_willy_fish_shop, SVEntrance.enter_elliott_house, SVEntrance.enter_tide_pools]),
    RegionData(SVRegion.railroad, [SVEntrance.enter_bathhouse_entrance, SVEntrance.enter_witch_warp_cave]),
    RegionData(SVRegion.ranch),
    RegionData(SVRegion.leah_house),
    RegionData(SVRegion.sewers, [SVEntrance.enter_mutant_bug_lair]),
    RegionData(SVRegion.mutant_bug_lair),
    RegionData(SVRegion.wizard_tower, [SVEntrance.enter_wizard_basement]),
    RegionData(SVRegion.wizard_basement),
    RegionData(SVRegion.tent),
    RegionData(SVRegion.carpenter, [SVEntrance.enter_sebastian_room]),
    RegionData(SVRegion.sebastian_room),
    RegionData(SVRegion.adventurer_guild),
    RegionData(SVRegion.community_center,
               [SVEntrance.access_crafts_room, SVEntrance.access_pantry, SVEntrance.access_fish_tank,
                SVEntrance.access_boiler_room, SVEntrance.access_bulletin_board, SVEntrance.access_vault]),
    RegionData(SVRegion.crafts_room),
    RegionData(SVRegion.pantry),
    RegionData(SVRegion.fish_tank),
    RegionData(SVRegion.boiler_room),
    RegionData(SVRegion.bulletin_board),
    RegionData(SVRegion.vault),
    RegionData(SVRegion.hospital, [SVEntrance.enter_harvey_room]),
    RegionData(SVRegion.harvey_room),
    RegionData(SVRegion.pierre_store, [SVEntrance.enter_sunroom]),
    RegionData(SVRegion.sunroom),
    RegionData(SVRegion.saloon, [SVEntrance.play_journey_of_the_prairie_king, SVEntrance.play_junimo_kart]),
    RegionData(SVRegion.alex_house),
    RegionData(SVRegion.trailer),
    RegionData(SVRegion.mayor_house),
    RegionData(SVRegion.sam_house),
    RegionData(SVRegion.haley_house),
    RegionData(SVRegion.blacksmith),
    RegionData(SVRegion.museum),
    RegionData(SVRegion.jojamart),
    RegionData(SVRegion.fish_shop, [SVEntrance.fish_shop_to_boat_tunnel]),
    RegionData(SVRegion.boat_tunnel, [SVEntrance.boat_to_ginger_island]),
    RegionData(SVRegion.elliott_house),
    RegionData(SVRegion.tide_pools),
    RegionData(SVRegion.bathhouse_entrance, [SVEntrance.enter_locker_room]),
    RegionData(SVRegion.locker_room, [SVEntrance.enter_public_bath]),
    RegionData(SVRegion.public_bath),
    RegionData(SVRegion.witch_warp_cave, [SVEntrance.enter_witch_swamp]),
    RegionData(SVRegion.witch_swamp),
    RegionData(SVRegion.quarry, [SVEntrance.enter_quarry_mine_entrance]),
    RegionData(SVRegion.quarry_mine_entrance, [SVEntrance.enter_quarry_mine]),
    RegionData(SVRegion.quarry_mine),
    RegionData(SVRegion.secret_woods),
    RegionData(SVRegion.desert, [SVEntrance.enter_skull_cavern_entrance, SVEntrance.enter_oasis]),
    RegionData(SVRegion.oasis, [SVEntrance.enter_casino]),
    RegionData(SVRegion.casino),
    RegionData(SVRegion.skull_cavern_entrance, [SVEntrance.enter_skull_cavern]),
    RegionData(SVRegion.skull_cavern, [SVEntrance.mine_to_skull_cavern_floor_25]),
    RegionData(SVRegion.skull_cavern_25, [SVEntrance.mine_to_skull_cavern_floor_100]),
    RegionData(SVRegion.skull_cavern_100),
    RegionData(SVRegion.island_south, [SVEntrance.island_south_to_west, SVEntrance.island_south_to_north,
                                       SVEntrance.island_south_to_east, SVEntrance.island_south_to_southeast]),
    RegionData(SVRegion.island_west, [SVEntrance.island_west_to_islandfarmhouse, SVEntrance.island_west_to_gourmand_cave,
                                      SVEntrance.island_west_to_crystals_cave, SVEntrance.island_west_to_shipwreck,
                                      SVEntrance.island_west_to_qi_walnut_room, SVEntrance.use_farm_obelisk]),
    RegionData(SVRegion.island_east, [SVEntrance.island_east_to_leo_hut]),
    RegionData(SVRegion.island_south_east, [SVEntrance.island_southeast_to_pirate_cove]),
    RegionData(SVRegion.island_north, [SVEntrance.talk_to_island_trader, SVEntrance.island_north_to_field_office,
                                       SVEntrance.island_north_to_dig_site, SVEntrance.island_north_to_volcano]),
    RegionData(SVRegion.volcano, [SVEntrance.climb_to_volcano_5]),
    RegionData(SVRegion.volcano_floor_5, [SVEntrance.climb_to_volcano_10]),
    RegionData(SVRegion.volcano_floor_10),
    RegionData(SVRegion.island_trader),
    RegionData(SVRegion.island_farmhouse),
    RegionData(SVRegion.gourmand_frog_cave),
    RegionData(SVRegion.colored_crystals_cave),
    RegionData(SVRegion.shipwreck),
    RegionData(SVRegion.qi_walnut_room),
    RegionData(SVRegion.leo_hut),
    RegionData(SVRegion.pirate_cove),
    RegionData(SVRegion.field_office),
    RegionData(SVRegion.dig_site),
    RegionData(SVRegion.jotpk_world_1, [SVEntrance.reach_jotpk_world_2]),
    RegionData(SVRegion.jotpk_world_2, [SVEntrance.reach_jotpk_world_3]),
    RegionData(SVRegion.jotpk_world_3),
    RegionData(SVRegion.junimo_kart_1, [SVEntrance.reach_junimo_kart_2]),
    RegionData(SVRegion.junimo_kart_2, [SVEntrance.reach_junimo_kart_3]),
    RegionData(SVRegion.junimo_kart_3),
    RegionData(SVRegion.mines, [SVEntrance.dig_to_mines_floor_5, SVEntrance.dig_to_mines_floor_10,
                                SVEntrance.dig_to_mines_floor_15, SVEntrance.dig_to_mines_floor_20,
                                SVEntrance.dig_to_mines_floor_25, SVEntrance.dig_to_mines_floor_30,
                                SVEntrance.dig_to_mines_floor_35, SVEntrance.dig_to_mines_floor_40,
                                SVEntrance.dig_to_mines_floor_45, SVEntrance.dig_to_mines_floor_50,
                                SVEntrance.dig_to_mines_floor_55, SVEntrance.dig_to_mines_floor_60,
                                SVEntrance.dig_to_mines_floor_65, SVEntrance.dig_to_mines_floor_70,
                                SVEntrance.dig_to_mines_floor_75, SVEntrance.dig_to_mines_floor_80,
                                SVEntrance.dig_to_mines_floor_85, SVEntrance.dig_to_mines_floor_90,
                                SVEntrance.dig_to_mines_floor_95, SVEntrance.dig_to_mines_floor_100,
                                SVEntrance.dig_to_mines_floor_105, SVEntrance.dig_to_mines_floor_110,
                                SVEntrance.dig_to_mines_floor_115, SVEntrance.dig_to_mines_floor_120]),
    RegionData(SVRegion.mines_floor_5),
    RegionData(SVRegion.mines_floor_10),
    RegionData(SVRegion.mines_floor_15),
    RegionData(SVRegion.mines_floor_20),
    RegionData(SVRegion.mines_floor_25),
    RegionData(SVRegion.mines_floor_30),
    RegionData(SVRegion.mines_floor_35),
    RegionData(SVRegion.mines_floor_40),
    RegionData(SVRegion.mines_floor_45),
    RegionData(SVRegion.mines_floor_50),
    RegionData(SVRegion.mines_floor_55),
    RegionData(SVRegion.mines_floor_60),
    RegionData(SVRegion.mines_floor_65),
    RegionData(SVRegion.mines_floor_70),
    RegionData(SVRegion.mines_floor_75),
    RegionData(SVRegion.mines_floor_80),
    RegionData(SVRegion.mines_floor_85),
    RegionData(SVRegion.mines_floor_90),
    RegionData(SVRegion.mines_floor_95),
    RegionData(SVRegion.mines_floor_100),
    RegionData(SVRegion.mines_floor_105),
    RegionData(SVRegion.mines_floor_110),
    RegionData(SVRegion.mines_floor_115),
    RegionData(SVRegion.mines_floor_120),
]

# Exists and where they lead
mandatory_connections = [
    ConnectionData(SVEntrance.to_stardew_valley, SVRegion.stardew_valley),
    ConnectionData(SVEntrance.to_farmhouse, SVRegion.farm_house),
    ConnectionData(SVEntrance.outside_to_farm, SVRegion.farm),
    ConnectionData(SVEntrance.downstairs_to_cellar, SVRegion.cellar),
    ConnectionData(SVEntrance.farm_to_backwoods, SVRegion.backwoods),
    ConnectionData(SVEntrance.farm_to_bus_stop, SVRegion.bus_stop),
    ConnectionData(SVEntrance.farm_to_forest, SVRegion.forest),
    ConnectionData(SVEntrance.farm_to_farmcave, SVRegion.farm_cave, flag=RandomizationFlag.NON_PROGRESSION),
    ConnectionData(SVEntrance.enter_greenhouse, SVRegion.greenhouse),
    ConnectionData(SVEntrance.use_desert_obelisk, SVRegion.desert),
    ConnectionData(SVEntrance.use_island_obelisk, SVRegion.island_south),
    ConnectionData(SVEntrance.use_farm_obelisk, SVRegion.farm),
    ConnectionData(SVEntrance.backwoods_to_mountain, SVRegion.mountain),
    ConnectionData(SVEntrance.bus_stop_to_town, SVRegion.town),
    ConnectionData(SVEntrance.bus_stop_to_tunnel_entrance, SVRegion.tunnel_entrance),
    ConnectionData(SVEntrance.take_bus_to_desert, SVRegion.desert),
    ConnectionData(SVEntrance.enter_tunnel, SVRegion.tunnel),
    ConnectionData(SVEntrance.forest_to_town, SVRegion.town),
    ConnectionData(SVEntrance.forest_to_wizard_tower, SVRegion.wizard_tower, flag=RandomizationFlag.NON_PROGRESSION),
    ConnectionData(SVEntrance.enter_wizard_basement, SVRegion.wizard_basement),
    ConnectionData(SVEntrance.forest_to_marnie_ranch, SVRegion.ranch, flag=RandomizationFlag.NON_PROGRESSION),
    ConnectionData(SVEntrance.forest_to_leah_cottage, SVRegion.leah_house),
    ConnectionData(SVEntrance.enter_secret_woods, SVRegion.secret_woods),
    ConnectionData(SVEntrance.forest_to_sewers, SVRegion.sewers),
    ConnectionData(SVEntrance.talk_to_traveling_merchant, SVRegion.traveling_cart),
    ConnectionData(SVEntrance.town_to_sewers, SVRegion.sewers),
    ConnectionData(SVEntrance.enter_mutant_bug_lair, SVRegion.mutant_bug_lair),
    ConnectionData(SVEntrance.mountain_to_railroad, SVRegion.railroad),
    ConnectionData(SVEntrance.mountain_to_tent, SVRegion.tent, flag=RandomizationFlag.NON_PROGRESSION),
    ConnectionData(SVEntrance.mountain_to_carpenter_shop, SVRegion.carpenter, flag=RandomizationFlag.NON_PROGRESSION),
    ConnectionData(SVEntrance.enter_sebastian_room, SVRegion.sebastian_room),
    ConnectionData(SVEntrance.mountain_to_adventurer_guild, SVRegion.adventurer_guild),
    ConnectionData(SVEntrance.enter_quarry, SVRegion.quarry),
    ConnectionData(SVEntrance.enter_quarry_mine_entrance, SVRegion.quarry_mine_entrance),
    ConnectionData(SVEntrance.enter_quarry_mine, SVRegion.quarry_mine),
    ConnectionData(SVEntrance.mountain_to_town, SVRegion.town),
    ConnectionData(SVEntrance.town_to_community_center, SVRegion.community_center, flag=RandomizationFlag.PELICAN_TOWN),
    ConnectionData(SVEntrance.access_crafts_room, SVRegion.crafts_room),
    ConnectionData(SVEntrance.access_pantry, SVRegion.pantry),
    ConnectionData(SVEntrance.access_fish_tank, SVRegion.fish_tank),
    ConnectionData(SVEntrance.access_boiler_room, SVRegion.boiler_room),
    ConnectionData(SVEntrance.access_bulletin_board, SVRegion.bulletin_board),
    ConnectionData(SVEntrance.access_vault, SVRegion.vault),
    ConnectionData(SVEntrance.town_to_hospital, SVRegion.hospital, flag=RandomizationFlag.PELICAN_TOWN),
    ConnectionData(SVEntrance.enter_harvey_room, SVRegion.harvey_room),
    ConnectionData(SVEntrance.town_to_pierre_general_store, SVRegion.pierre_store, flag=RandomizationFlag.PELICAN_TOWN),
    ConnectionData(SVEntrance.enter_sunroom, SVRegion.sunroom),
    ConnectionData(SVEntrance.town_to_clint_blacksmith, SVRegion.blacksmith, flag=RandomizationFlag.PELICAN_TOWN),
    ConnectionData(SVEntrance.town_to_saloon, SVRegion.saloon, flag=RandomizationFlag.PELICAN_TOWN),
    ConnectionData(SVEntrance.play_journey_of_the_prairie_king, SVRegion.jotpk_world_1),
    ConnectionData(SVEntrance.reach_jotpk_world_2, SVRegion.jotpk_world_2),
    ConnectionData(SVEntrance.reach_jotpk_world_3, SVRegion.jotpk_world_3),
    ConnectionData(SVEntrance.play_junimo_kart, SVRegion.junimo_kart_1),
    ConnectionData(SVEntrance.reach_junimo_kart_2, SVRegion.junimo_kart_2),
    ConnectionData(SVEntrance.reach_junimo_kart_3, SVRegion.junimo_kart_3),
    ConnectionData(SVEntrance.town_to_sam_house, SVRegion.sam_house, flag=RandomizationFlag.PELICAN_TOWN),
    ConnectionData(SVEntrance.town_to_haley_house, SVRegion.haley_house, flag=RandomizationFlag.PELICAN_TOWN),
    ConnectionData(SVEntrance.town_to_mayor_manor, SVRegion.mayor_house, flag=RandomizationFlag.PELICAN_TOWN),
    ConnectionData(SVEntrance.town_to_alex_house, SVRegion.alex_house, flag=RandomizationFlag.PELICAN_TOWN),
    ConnectionData(SVEntrance.town_to_trailer, SVRegion.trailer, flag=RandomizationFlag.PELICAN_TOWN),
    ConnectionData(SVEntrance.town_to_museum, SVRegion.museum, flag=RandomizationFlag.PELICAN_TOWN),
    ConnectionData(SVEntrance.town_to_jojamart, SVRegion.jojamart, flag=RandomizationFlag.PELICAN_TOWN),
    ConnectionData(SVEntrance.town_to_beach, SVRegion.beach),
    ConnectionData(SVEntrance.enter_elliott_house, SVRegion.elliott_house),
    ConnectionData(SVEntrance.beach_to_willy_fish_shop, SVRegion.fish_shop, flag=RandomizationFlag.NON_PROGRESSION),
    ConnectionData(SVEntrance.fish_shop_to_boat_tunnel, SVRegion.boat_tunnel),
    ConnectionData(SVEntrance.boat_to_ginger_island, SVRegion.island_south),
    ConnectionData(SVEntrance.enter_tide_pools, SVRegion.tide_pools),
    ConnectionData(SVEntrance.mountain_to_the_mines, SVRegion.mines, flag=RandomizationFlag.NON_PROGRESSION),
    ConnectionData(SVEntrance.dig_to_mines_floor_5, SVRegion.mines_floor_5),
    ConnectionData(SVEntrance.dig_to_mines_floor_10, SVRegion.mines_floor_10),
    ConnectionData(SVEntrance.dig_to_mines_floor_15, SVRegion.mines_floor_15),
    ConnectionData(SVEntrance.dig_to_mines_floor_20, SVRegion.mines_floor_20),
    ConnectionData(SVEntrance.dig_to_mines_floor_25, SVRegion.mines_floor_25),
    ConnectionData(SVEntrance.dig_to_mines_floor_30, SVRegion.mines_floor_30),
    ConnectionData(SVEntrance.dig_to_mines_floor_35, SVRegion.mines_floor_35),
    ConnectionData(SVEntrance.dig_to_mines_floor_40, SVRegion.mines_floor_40),
    ConnectionData(SVEntrance.dig_to_mines_floor_45, SVRegion.mines_floor_45),
    ConnectionData(SVEntrance.dig_to_mines_floor_50, SVRegion.mines_floor_50),
    ConnectionData(SVEntrance.dig_to_mines_floor_55, SVRegion.mines_floor_55),
    ConnectionData(SVEntrance.dig_to_mines_floor_60, SVRegion.mines_floor_60),
    ConnectionData(SVEntrance.dig_to_mines_floor_65, SVRegion.mines_floor_65),
    ConnectionData(SVEntrance.dig_to_mines_floor_70, SVRegion.mines_floor_70),
    ConnectionData(SVEntrance.dig_to_mines_floor_75, SVRegion.mines_floor_75),
    ConnectionData(SVEntrance.dig_to_mines_floor_80, SVRegion.mines_floor_80),
    ConnectionData(SVEntrance.dig_to_mines_floor_85, SVRegion.mines_floor_85),
    ConnectionData(SVEntrance.dig_to_mines_floor_90, SVRegion.mines_floor_90),
    ConnectionData(SVEntrance.dig_to_mines_floor_95, SVRegion.mines_floor_95),
    ConnectionData(SVEntrance.dig_to_mines_floor_100, SVRegion.mines_floor_100),
    ConnectionData(SVEntrance.dig_to_mines_floor_105, SVRegion.mines_floor_105),
    ConnectionData(SVEntrance.dig_to_mines_floor_110, SVRegion.mines_floor_110),
    ConnectionData(SVEntrance.dig_to_mines_floor_115, SVRegion.mines_floor_115),
    ConnectionData(SVEntrance.dig_to_mines_floor_120, SVRegion.mines_floor_120),
    ConnectionData(SVEntrance.enter_skull_cavern_entrance, SVRegion.skull_cavern_entrance),
    ConnectionData(SVEntrance.enter_oasis, SVRegion.oasis),
    ConnectionData(SVEntrance.enter_casino, SVRegion.casino),
    ConnectionData(SVEntrance.enter_skull_cavern, SVRegion.skull_cavern),
    ConnectionData(SVEntrance.mine_to_skull_cavern_floor_25, SVRegion.skull_cavern_25),
    ConnectionData(SVEntrance.mine_to_skull_cavern_floor_100, SVRegion.skull_cavern_100),
    ConnectionData(SVEntrance.enter_witch_warp_cave, SVRegion.witch_warp_cave),
    ConnectionData(SVEntrance.enter_witch_swamp, SVRegion.witch_swamp),
    ConnectionData(SVEntrance.enter_bathhouse_entrance, SVRegion.bathhouse_entrance),
    ConnectionData(SVEntrance.enter_locker_room, SVRegion.locker_room),
    ConnectionData(SVEntrance.enter_public_bath, SVRegion.public_bath),
    ConnectionData(SVEntrance.island_south_to_west, SVRegion.island_west),
    ConnectionData(SVEntrance.island_south_to_north, SVRegion.island_north),
    ConnectionData(SVEntrance.island_south_to_east, SVRegion.island_east),
    ConnectionData(SVEntrance.island_south_to_southeast, SVRegion.island_south_east),
    ConnectionData(SVEntrance.island_west_to_islandfarmhouse, SVRegion.island_farmhouse),
    ConnectionData(SVEntrance.island_west_to_gourmand_cave, SVRegion.gourmand_frog_cave),
    ConnectionData(SVEntrance.island_west_to_crystals_cave, SVRegion.colored_crystals_cave),
    ConnectionData(SVEntrance.island_west_to_shipwreck, SVRegion.shipwreck),
    ConnectionData(SVEntrance.island_west_to_qi_walnut_room, SVRegion.qi_walnut_room),
    ConnectionData(SVEntrance.island_east_to_leo_hut, SVRegion.leo_hut),
    ConnectionData(SVEntrance.island_southeast_to_pirate_cove, SVRegion.pirate_cove),
    ConnectionData(SVEntrance.island_north_to_field_office, SVRegion.field_office),
    ConnectionData(SVEntrance.island_north_to_dig_site, SVRegion.dig_site),
    ConnectionData(SVEntrance.island_north_to_volcano, SVRegion.volcano),
    ConnectionData(SVEntrance.talk_to_island_trader, SVRegion.island_trader),
    ConnectionData(SVEntrance.climb_to_volcano_5, SVRegion.volcano_floor_5),
    ConnectionData(SVEntrance.climb_to_volcano_10, SVRegion.volcano_floor_10),
]


def create_regions(region_factory: RegionFactory, random: Random, world_options: StardewOptions) -> Tuple[
    Iterable[Region], Dict[str, str]]:
    regions: Dict[str: Region] = {region.name: region_factory(region.name, region.exits) for region in
                                  stardew_valley_regions}
    entrances: Dict[str: Entrance] = {entrance.name: entrance
                                      for region in regions.values()
                                      for entrance in region.exits}

    connections, randomized_data = randomize_connections(random, world_options)

    for connection in connections:
        if connection.name not in entrances:
            continue
        entrances[connection.name].connect(regions[connection.destination])

    return regions.values(), randomized_data


def randomize_connections(random: Random, world_options: StardewOptions) -> Tuple[List[ConnectionData], Dict[str, str]]:
    connections_to_randomize = []
    if world_options[options.EntranceRandomization] == options.EntranceRandomization.option_pelican_town:
        connections_to_randomize = [connection for connection in mandatory_connections if
                                    RandomizationFlag.PELICAN_TOWN in connection.flag]
    elif world_options[options.EntranceRandomization] == options.EntranceRandomization.option_non_progression:
        connections_to_randomize = [connection for connection in mandatory_connections if
                                    RandomizationFlag.NON_PROGRESSION in connection.flag]
    random.shuffle(connections_to_randomize)

    destination_pool = list(connections_to_randomize)
    random.shuffle(destination_pool)

    randomized_connections = []
    randomized_data = {}
    for connection in connections_to_randomize:
        destination = destination_pool.pop()
        randomized_connections.append(ConnectionData(connection.name, destination.destination, destination.reverse))
        randomized_data[connection.name] = destination.name
        randomized_data[destination.reverse] = connection.reverse

    return mandatory_connections, randomized_data
