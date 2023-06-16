from random import Random
from typing import Iterable, Dict, Protocol, List, Tuple, Set

from BaseClasses import Region, Entrance
from . import options
from worlds.stardew_valley.strings.entrance_names import SVEntrance
from worlds.stardew_valley.strings.region_names import Region
from .region_classes import RegionData, ConnectionData, RandomizationFlag
from .options import StardewOptions
from .mods.mod_regions import ModDataList


class RegionFactory(Protocol):
    def __call__(self, name: str, regions: Iterable[str]) -> Region:
        raise NotImplementedError


vanilla_regions = [
    RegionData(Region.menu, [SVEntrance.to_stardew_valley]),
    RegionData(Region.stardew_valley, [SVEntrance.to_farmhouse]),
    RegionData(Region.farm_house, [SVEntrance.farmhouse_to_farm, SVEntrance.downstairs_to_cellar]),
    RegionData(Region.cellar),
    RegionData(Region.farm,
               [SVEntrance.farm_to_backwoods, SVEntrance.farm_to_bus_stop, SVEntrance.farm_to_forest,
                SVEntrance.farm_to_farmcave, SVEntrance.enter_greenhouse,
                SVEntrance.use_desert_obelisk, SVEntrance.use_island_obelisk]),
    RegionData(Region.backwoods, [SVEntrance.backwoods_to_mountain]),
    RegionData(Region.bus_stop,
               [SVEntrance.bus_stop_to_town, SVEntrance.take_bus_to_desert, SVEntrance.bus_stop_to_tunnel_entrance]),
    RegionData(Region.forest,
               [SVEntrance.forest_to_town, SVEntrance.enter_secret_woods, SVEntrance.forest_to_wizard_tower,
                SVEntrance.forest_to_marnie_ranch,
                SVEntrance.forest_to_leah_cottage, SVEntrance.forest_to_sewers,
                SVEntrance.buy_from_traveling_merchant]),
    RegionData(Region.traveling_cart),
    RegionData(Region.farm_cave),
    RegionData(Region.greenhouse),
    RegionData(Region.mountain,
               [SVEntrance.mountain_to_railroad, SVEntrance.mountain_to_tent, SVEntrance.mountain_to_carpenter_shop,
                SVEntrance.mountain_to_the_mines, SVEntrance.enter_quarry, SVEntrance.mountain_to_adventurer_guild,
                SVEntrance.mountain_to_town, SVEntrance.mountain_to_maru_room]),
    RegionData(Region.maru_room),
    RegionData(Region.tunnel_entrance, [SVEntrance.enter_tunnel]),
    RegionData(Region.tunnel),
    RegionData(Region.town,
               [SVEntrance.town_to_community_center, SVEntrance.town_to_beach, SVEntrance.town_to_hospital,
                SVEntrance.town_to_pierre_general_store, SVEntrance.town_to_saloon, SVEntrance.town_to_alex_house,
                SVEntrance.town_to_trailer,
                SVEntrance.town_to_mayor_manor,
                SVEntrance.town_to_sam_house, SVEntrance.town_to_haley_house, SVEntrance.town_to_sewers,
                SVEntrance.town_to_clint_blacksmith,
                SVEntrance.town_to_museum,
                SVEntrance.town_to_jojamart]),
    RegionData(Region.beach,
               [SVEntrance.beach_to_willy_fish_shop, SVEntrance.enter_elliott_house, SVEntrance.enter_tide_pools]),
    RegionData(Region.railroad, [SVEntrance.enter_bathhouse_entrance, SVEntrance.enter_witch_warp_cave]),
    RegionData(Region.ranch),
    RegionData(Region.leah_house),
    RegionData(Region.sewers, [SVEntrance.enter_mutant_bug_lair]),
    RegionData(Region.mutant_bug_lair),
    RegionData(Region.wizard_tower, [SVEntrance.enter_wizard_basement]),
    RegionData(Region.wizard_basement),
    RegionData(Region.tent),
    RegionData(Region.carpenter, [SVEntrance.enter_sebastian_room]),
    RegionData(Region.sebastian_room),
    RegionData(Region.adventurer_guild),
    RegionData(Region.community_center,
               [SVEntrance.access_crafts_room, SVEntrance.access_pantry, SVEntrance.access_fish_tank,
                SVEntrance.access_boiler_room, SVEntrance.access_bulletin_board, SVEntrance.access_vault]),
    RegionData(Region.crafts_room),
    RegionData(Region.pantry),
    RegionData(Region.fish_tank),
    RegionData(Region.boiler_room),
    RegionData(Region.bulletin_board),
    RegionData(Region.vault),
    RegionData(Region.hospital, [SVEntrance.enter_harvey_room]),
    RegionData(Region.harvey_room),
    RegionData(Region.pierre_store, [SVEntrance.enter_sunroom]),
    RegionData(Region.sunroom),
    RegionData(Region.saloon, [SVEntrance.play_journey_of_the_prairie_king, SVEntrance.play_junimo_kart]),
    RegionData(Region.alex_house),
    RegionData(Region.trailer),
    RegionData(Region.mayor_house),
    RegionData(Region.sam_house),
    RegionData(Region.haley_house),
    RegionData(Region.blacksmith),
    RegionData(Region.museum),
    RegionData(Region.jojamart),
    RegionData(Region.fish_shop, [SVEntrance.fish_shop_to_boat_tunnel]),
    RegionData(Region.boat_tunnel, [SVEntrance.boat_to_ginger_island]),
    RegionData(Region.elliott_house),
    RegionData(Region.tide_pools),
    RegionData(Region.bathhouse_entrance, [SVEntrance.enter_locker_room]),
    RegionData(Region.locker_room, [SVEntrance.enter_public_bath]),
    RegionData(Region.public_bath),
    RegionData(Region.witch_warp_cave, [SVEntrance.enter_witch_swamp]),
    RegionData(Region.witch_swamp, [SVEntrance.enter_witch_hut]),
    RegionData(Region.witch_hut),
    RegionData(Region.quarry, [SVEntrance.enter_quarry_mine_entrance]),
    RegionData(Region.quarry_mine_entrance, [SVEntrance.enter_quarry_mine]),
    RegionData(Region.quarry_mine),
    RegionData(Region.secret_woods),
    RegionData(Region.desert, [SVEntrance.enter_skull_cavern_entrance, SVEntrance.enter_oasis]),
    RegionData(Region.oasis, [SVEntrance.enter_casino]),
    RegionData(Region.casino),
    RegionData(Region.skull_cavern_entrance, [SVEntrance.enter_skull_cavern]),
    RegionData(Region.skull_cavern, [SVEntrance.mine_to_skull_cavern_floor_25]),
    RegionData(Region.skull_cavern_25, [SVEntrance.mine_to_skull_cavern_floor_100]),
    RegionData(Region.skull_cavern_100),
    RegionData(Region.island_south, [SVEntrance.island_south_to_west, SVEntrance.island_south_to_north,
                                     SVEntrance.island_south_to_east, SVEntrance.island_south_to_southeast,
                                     SVEntrance.parrot_express_docks_to_volcano,
                                     SVEntrance.parrot_express_docks_to_dig_site,
                                     SVEntrance.parrot_express_docks_to_jungle]),
    RegionData(Region.island_west,
               [SVEntrance.island_west_to_islandfarmhouse, SVEntrance.island_west_to_gourmand_cave,
                SVEntrance.island_west_to_crystals_cave, SVEntrance.island_west_to_shipwreck,
                SVEntrance.island_west_to_qi_walnut_room, SVEntrance.use_farm_obelisk,
                SVEntrance.parrot_express_jungle_to_docks, SVEntrance.parrot_express_jungle_to_dig_site,
                SVEntrance.parrot_express_jungle_to_volcano]),
    RegionData(Region.island_east, [SVEntrance.island_east_to_leo_hut, SVEntrance.island_east_to_island_shrine]),
    RegionData(Region.island_shrine),
    RegionData(Region.island_south_east, [SVEntrance.island_southeast_to_pirate_cove]),
    RegionData(Region.island_north, [SVEntrance.talk_to_island_trader, SVEntrance.island_north_to_field_office,
                                     SVEntrance.island_north_to_dig_site, SVEntrance.island_north_to_volcano,
                                     SVEntrance.parrot_express_volcano_to_dig_site,
                                     SVEntrance.parrot_express_volcano_to_jungle,
                                     SVEntrance.parrot_express_volcano_to_docks]),
    RegionData(Region.volcano, [SVEntrance.climb_to_volcano_5, SVEntrance.volcano_to_secret_beach]),
    RegionData(Region.volcano_secret_beach),
    RegionData(Region.volcano_floor_5, [SVEntrance.climb_to_volcano_10]),
    RegionData(Region.volcano_floor_10),
    RegionData(Region.island_trader),
    RegionData(Region.island_farmhouse),
    RegionData(Region.gourmand_frog_cave),
    RegionData(Region.colored_crystals_cave),
    RegionData(Region.shipwreck),
    RegionData(Region.qi_walnut_room),
    RegionData(Region.leo_hut),
    RegionData(Region.pirate_cove),
    RegionData(Region.field_office),
    RegionData(Region.dig_site,
               [SVEntrance.parrot_express_dig_site_to_volcano, SVEntrance.parrot_express_dig_site_to_docks,
                SVEntrance.parrot_express_dig_site_to_jungle]),
    RegionData(Region.jotpk_world_1, [SVEntrance.reach_jotpk_world_2]),
    RegionData(Region.jotpk_world_2, [SVEntrance.reach_jotpk_world_3]),
    RegionData(Region.jotpk_world_3),
    RegionData(Region.junimo_kart_1, [SVEntrance.reach_junimo_kart_2]),
    RegionData(Region.junimo_kart_2, [SVEntrance.reach_junimo_kart_3]),
    RegionData(Region.junimo_kart_3),
    RegionData(Region.mines, [SVEntrance.dig_to_mines_floor_5, SVEntrance.dig_to_mines_floor_10,
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
    RegionData(Region.mines_floor_5),
    RegionData(Region.mines_floor_10),
    RegionData(Region.mines_floor_15),
    RegionData(Region.mines_floor_20),
    RegionData(Region.mines_floor_25),
    RegionData(Region.mines_floor_30),
    RegionData(Region.mines_floor_35),
    RegionData(Region.mines_floor_40),
    RegionData(Region.mines_floor_45),
    RegionData(Region.mines_floor_50),
    RegionData(Region.mines_floor_55),
    RegionData(Region.mines_floor_60),
    RegionData(Region.mines_floor_65),
    RegionData(Region.mines_floor_70),
    RegionData(Region.mines_floor_75),
    RegionData(Region.mines_floor_80),
    RegionData(Region.mines_floor_85),
    RegionData(Region.mines_floor_90),
    RegionData(Region.mines_floor_95),
    RegionData(Region.mines_floor_100),
    RegionData(Region.mines_floor_105),
    RegionData(Region.mines_floor_110),
    RegionData(Region.mines_floor_115),
    RegionData(Region.mines_floor_120),
]

# Exists and where they lead
vanilla_connections = [
    ConnectionData(SVEntrance.to_stardew_valley, Region.stardew_valley),
    ConnectionData(SVEntrance.to_farmhouse, Region.farm_house),
    ConnectionData(SVEntrance.farmhouse_to_farm, Region.farm),
    ConnectionData(SVEntrance.downstairs_to_cellar, Region.cellar),
    ConnectionData(SVEntrance.farm_to_backwoods, Region.backwoods),
    ConnectionData(SVEntrance.farm_to_bus_stop, Region.bus_stop),
    ConnectionData(SVEntrance.farm_to_forest, Region.forest),
    ConnectionData(SVEntrance.farm_to_farmcave, Region.farm_cave, flag=RandomizationFlag.NON_PROGRESSION),
    ConnectionData(SVEntrance.enter_greenhouse, Region.greenhouse),
    ConnectionData(SVEntrance.use_desert_obelisk, Region.desert),
    ConnectionData(SVEntrance.use_island_obelisk, Region.island_south),
    ConnectionData(SVEntrance.use_farm_obelisk, Region.farm),
    ConnectionData(SVEntrance.backwoods_to_mountain, Region.mountain),
    ConnectionData(SVEntrance.bus_stop_to_town, Region.town),
    ConnectionData(SVEntrance.bus_stop_to_tunnel_entrance, Region.tunnel_entrance),
    ConnectionData(SVEntrance.take_bus_to_desert, Region.desert),
    ConnectionData(SVEntrance.enter_tunnel, Region.tunnel),
    ConnectionData(SVEntrance.forest_to_town, Region.town),
    ConnectionData(SVEntrance.forest_to_wizard_tower, Region.wizard_tower,
                   flag=RandomizationFlag.NON_PROGRESSION | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(SVEntrance.enter_wizard_basement, Region.wizard_basement, flag=RandomizationFlag.BUILDINGS),
    ConnectionData(SVEntrance.forest_to_marnie_ranch, Region.ranch,
                   flag=RandomizationFlag.NON_PROGRESSION | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(SVEntrance.forest_to_leah_cottage, Region.leah_house,
                   flag=RandomizationFlag.BUILDINGS | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(SVEntrance.enter_secret_woods, Region.secret_woods),
    ConnectionData(SVEntrance.forest_to_sewers, Region.sewers),
    ConnectionData(SVEntrance.buy_from_traveling_merchant, Region.traveling_cart),
    ConnectionData(SVEntrance.town_to_sewers, Region.sewers),
    ConnectionData(SVEntrance.enter_mutant_bug_lair, Region.mutant_bug_lair),
    ConnectionData(SVEntrance.mountain_to_railroad, Region.railroad),
    ConnectionData(SVEntrance.mountain_to_tent, Region.tent,
                   flag=RandomizationFlag.NON_PROGRESSION | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(SVEntrance.mountain_to_carpenter_shop, Region.carpenter,
                   flag=RandomizationFlag.BUILDINGS | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(SVEntrance.mountain_to_maru_room, Region.maru_room,
                   flag=RandomizationFlag.BUILDINGS | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(SVEntrance.enter_sebastian_room, Region.sebastian_room, flag=RandomizationFlag.BUILDINGS),
    ConnectionData(SVEntrance.mountain_to_adventurer_guild, Region.adventurer_guild,
                   flag=RandomizationFlag.BUILDINGS | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(SVEntrance.enter_quarry, Region.quarry),
    ConnectionData(SVEntrance.enter_quarry_mine_entrance, Region.quarry_mine_entrance,
                   flag=RandomizationFlag.BUILDINGS),
    ConnectionData(SVEntrance.enter_quarry_mine, Region.quarry_mine),
    ConnectionData(SVEntrance.mountain_to_town, Region.town),
    ConnectionData(SVEntrance.town_to_community_center, Region.community_center,
                   flag=RandomizationFlag.PELICAN_TOWN | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(SVEntrance.access_crafts_room, Region.crafts_room),
    ConnectionData(SVEntrance.access_pantry, Region.pantry),
    ConnectionData(SVEntrance.access_fish_tank, Region.fish_tank),
    ConnectionData(SVEntrance.access_boiler_room, Region.boiler_room),
    ConnectionData(SVEntrance.access_bulletin_board, Region.bulletin_board),
    ConnectionData(SVEntrance.access_vault, Region.vault),
    ConnectionData(SVEntrance.town_to_hospital, Region.hospital,
                   flag=RandomizationFlag.PELICAN_TOWN | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(SVEntrance.enter_harvey_room, Region.harvey_room, flag=RandomizationFlag.BUILDINGS),
    ConnectionData(SVEntrance.town_to_pierre_general_store, Region.pierre_store,
                   flag=RandomizationFlag.PELICAN_TOWN | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(SVEntrance.enter_sunroom, Region.sunroom, flag=RandomizationFlag.BUILDINGS),
    ConnectionData(SVEntrance.town_to_clint_blacksmith, Region.blacksmith,
                   flag=RandomizationFlag.PELICAN_TOWN | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(SVEntrance.town_to_saloon, Region.saloon,
                   flag=RandomizationFlag.PELICAN_TOWN | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(SVEntrance.play_journey_of_the_prairie_king, Region.jotpk_world_1),
    ConnectionData(SVEntrance.reach_jotpk_world_2, Region.jotpk_world_2),
    ConnectionData(SVEntrance.reach_jotpk_world_3, Region.jotpk_world_3),
    ConnectionData(SVEntrance.play_junimo_kart, Region.junimo_kart_1),
    ConnectionData(SVEntrance.reach_junimo_kart_2, Region.junimo_kart_2),
    ConnectionData(SVEntrance.reach_junimo_kart_3, Region.junimo_kart_3),
    ConnectionData(SVEntrance.town_to_sam_house, Region.sam_house,
                   flag=RandomizationFlag.PELICAN_TOWN | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(SVEntrance.town_to_haley_house, Region.haley_house,
                   flag=RandomizationFlag.PELICAN_TOWN | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(SVEntrance.town_to_mayor_manor, Region.mayor_house,
                   flag=RandomizationFlag.PELICAN_TOWN | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(SVEntrance.town_to_alex_house, Region.alex_house,
                   flag=RandomizationFlag.PELICAN_TOWN | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(SVEntrance.town_to_trailer, Region.trailer,
                   flag=RandomizationFlag.PELICAN_TOWN | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(SVEntrance.town_to_museum, Region.museum,
                   flag=RandomizationFlag.PELICAN_TOWN | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(SVEntrance.town_to_jojamart, Region.jojamart,
                   flag=RandomizationFlag.PELICAN_TOWN | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(SVEntrance.town_to_beach, Region.beach),
    ConnectionData(SVEntrance.enter_elliott_house, Region.elliott_house,
                   flag=RandomizationFlag.BUILDINGS | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(SVEntrance.beach_to_willy_fish_shop, Region.fish_shop,
                   flag=RandomizationFlag.NON_PROGRESSION | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(SVEntrance.fish_shop_to_boat_tunnel, Region.boat_tunnel,
                   flag=RandomizationFlag.BUILDINGS | RandomizationFlag.GINGER_ISLAND),
    ConnectionData(SVEntrance.boat_to_ginger_island, Region.island_south),
    ConnectionData(SVEntrance.enter_tide_pools, Region.tide_pools),
    ConnectionData(SVEntrance.mountain_to_the_mines, Region.mines,
                   flag=RandomizationFlag.NON_PROGRESSION | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(SVEntrance.dig_to_mines_floor_5, Region.mines_floor_5),
    ConnectionData(SVEntrance.dig_to_mines_floor_10, Region.mines_floor_10),
    ConnectionData(SVEntrance.dig_to_mines_floor_15, Region.mines_floor_15),
    ConnectionData(SVEntrance.dig_to_mines_floor_20, Region.mines_floor_20),
    ConnectionData(SVEntrance.dig_to_mines_floor_25, Region.mines_floor_25),
    ConnectionData(SVEntrance.dig_to_mines_floor_30, Region.mines_floor_30),
    ConnectionData(SVEntrance.dig_to_mines_floor_35, Region.mines_floor_35),
    ConnectionData(SVEntrance.dig_to_mines_floor_40, Region.mines_floor_40),
    ConnectionData(SVEntrance.dig_to_mines_floor_45, Region.mines_floor_45),
    ConnectionData(SVEntrance.dig_to_mines_floor_50, Region.mines_floor_50),
    ConnectionData(SVEntrance.dig_to_mines_floor_55, Region.mines_floor_55),
    ConnectionData(SVEntrance.dig_to_mines_floor_60, Region.mines_floor_60),
    ConnectionData(SVEntrance.dig_to_mines_floor_65, Region.mines_floor_65),
    ConnectionData(SVEntrance.dig_to_mines_floor_70, Region.mines_floor_70),
    ConnectionData(SVEntrance.dig_to_mines_floor_75, Region.mines_floor_75),
    ConnectionData(SVEntrance.dig_to_mines_floor_80, Region.mines_floor_80),
    ConnectionData(SVEntrance.dig_to_mines_floor_85, Region.mines_floor_85),
    ConnectionData(SVEntrance.dig_to_mines_floor_90, Region.mines_floor_90),
    ConnectionData(SVEntrance.dig_to_mines_floor_95, Region.mines_floor_95),
    ConnectionData(SVEntrance.dig_to_mines_floor_100, Region.mines_floor_100),
    ConnectionData(SVEntrance.dig_to_mines_floor_105, Region.mines_floor_105),
    ConnectionData(SVEntrance.dig_to_mines_floor_110, Region.mines_floor_110),
    ConnectionData(SVEntrance.dig_to_mines_floor_115, Region.mines_floor_115),
    ConnectionData(SVEntrance.dig_to_mines_floor_120, Region.mines_floor_120),
    ConnectionData(SVEntrance.enter_skull_cavern_entrance, Region.skull_cavern_entrance,
                   flag=RandomizationFlag.BUILDINGS | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(SVEntrance.enter_oasis, Region.oasis,
                   flag=RandomizationFlag.BUILDINGS | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(SVEntrance.enter_casino, Region.casino, flag=RandomizationFlag.BUILDINGS),
    ConnectionData(SVEntrance.enter_skull_cavern, Region.skull_cavern),
    ConnectionData(SVEntrance.mine_to_skull_cavern_floor_25, Region.skull_cavern_25),
    ConnectionData(SVEntrance.mine_to_skull_cavern_floor_100, Region.skull_cavern_100),
    ConnectionData(SVEntrance.enter_witch_warp_cave, Region.witch_warp_cave, flag=RandomizationFlag.BUILDINGS),
    ConnectionData(SVEntrance.enter_witch_swamp, Region.witch_swamp, flag=RandomizationFlag.BUILDINGS),
    ConnectionData(SVEntrance.enter_witch_hut, Region.witch_hut, flag=RandomizationFlag.BUILDINGS),
    ConnectionData(SVEntrance.enter_bathhouse_entrance, Region.bathhouse_entrance,
                   flag=RandomizationFlag.BUILDINGS | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(SVEntrance.enter_locker_room, Region.locker_room, flag=RandomizationFlag.BUILDINGS),
    ConnectionData(SVEntrance.enter_public_bath, Region.public_bath, flag=RandomizationFlag.BUILDINGS),
    ConnectionData(SVEntrance.island_south_to_west, Region.island_west, flag=RandomizationFlag.GINGER_ISLAND),
    ConnectionData(SVEntrance.island_south_to_north, Region.island_north, flag=RandomizationFlag.GINGER_ISLAND),
    ConnectionData(SVEntrance.island_south_to_east, Region.island_east, flag=RandomizationFlag.GINGER_ISLAND),
    ConnectionData(SVEntrance.island_south_to_southeast, Region.island_south_east,
                   flag=RandomizationFlag.GINGER_ISLAND),
    ConnectionData(SVEntrance.island_west_to_islandfarmhouse, Region.island_farmhouse,
                   flag=RandomizationFlag.BUILDINGS | RandomizationFlag.GINGER_ISLAND),
    ConnectionData(SVEntrance.island_west_to_gourmand_cave, Region.gourmand_frog_cave,
                   flag=RandomizationFlag.BUILDINGS | RandomizationFlag.GINGER_ISLAND),
    ConnectionData(SVEntrance.island_west_to_crystals_cave, Region.colored_crystals_cave,
                   flag=RandomizationFlag.BUILDINGS | RandomizationFlag.GINGER_ISLAND),
    ConnectionData(SVEntrance.island_west_to_shipwreck, Region.shipwreck,
                   flag=RandomizationFlag.BUILDINGS | RandomizationFlag.GINGER_ISLAND),
    ConnectionData(SVEntrance.island_west_to_qi_walnut_room, Region.qi_walnut_room,
                   flag=RandomizationFlag.BUILDINGS | RandomizationFlag.GINGER_ISLAND),
    ConnectionData(SVEntrance.island_east_to_leo_hut, Region.leo_hut,
                   flag=RandomizationFlag.BUILDINGS | RandomizationFlag.GINGER_ISLAND),
    ConnectionData(SVEntrance.island_east_to_island_shrine, Region.island_shrine,
                   flag=RandomizationFlag.BUILDINGS | RandomizationFlag.GINGER_ISLAND),
    ConnectionData(SVEntrance.island_southeast_to_pirate_cove, Region.pirate_cove,
                   flag=RandomizationFlag.BUILDINGS | RandomizationFlag.GINGER_ISLAND),
    ConnectionData(SVEntrance.island_north_to_field_office, Region.field_office,
                   flag=RandomizationFlag.BUILDINGS | RandomizationFlag.GINGER_ISLAND),
    ConnectionData(SVEntrance.island_north_to_dig_site, Region.dig_site, flag=RandomizationFlag.GINGER_ISLAND),
    ConnectionData(SVEntrance.island_north_to_volcano, Region.volcano,
                   flag=RandomizationFlag.BUILDINGS | RandomizationFlag.GINGER_ISLAND),
    ConnectionData(SVEntrance.volcano_to_secret_beach, Region.volcano_secret_beach,
                   flag=RandomizationFlag.BUILDINGS | RandomizationFlag.GINGER_ISLAND),
    ConnectionData(SVEntrance.talk_to_island_trader, Region.island_trader, flag=RandomizationFlag.GINGER_ISLAND),
    ConnectionData(SVEntrance.climb_to_volcano_5, Region.volcano_floor_5),
    ConnectionData(SVEntrance.climb_to_volcano_10, Region.volcano_floor_10),
    ConnectionData(SVEntrance.parrot_express_jungle_to_docks, Region.island_south),
    ConnectionData(SVEntrance.parrot_express_dig_site_to_docks, Region.island_south),
    ConnectionData(SVEntrance.parrot_express_volcano_to_docks, Region.island_south),
    ConnectionData(SVEntrance.parrot_express_volcano_to_jungle, Region.island_west),
    ConnectionData(SVEntrance.parrot_express_docks_to_jungle, Region.island_west),
    ConnectionData(SVEntrance.parrot_express_dig_site_to_jungle, Region.island_west),
    ConnectionData(SVEntrance.parrot_express_docks_to_dig_site, Region.dig_site),
    ConnectionData(SVEntrance.parrot_express_volcano_to_dig_site, Region.dig_site),
    ConnectionData(SVEntrance.parrot_express_jungle_to_dig_site, Region.dig_site),
    ConnectionData(SVEntrance.parrot_express_dig_site_to_volcano, Region.island_north),
    ConnectionData(SVEntrance.parrot_express_docks_to_volcano, Region.island_north),
    ConnectionData(SVEntrance.parrot_express_jungle_to_volcano, Region.island_north),
]


def create_final_regions(world_options: StardewOptions) -> List[RegionData]:
    final_regions = []
    final_regions.extend(vanilla_regions)
    if world_options[options.Mods] is None:
        return final_regions
    for mod in world_options[options.Mods]:
        if mod not in ModDataList:
            continue
        for mod_region in ModDataList[mod].regions:
            existing_region = next(
                (region for region in final_regions if region.name == mod_region.name), None)
            if existing_region:
                final_regions.remove(existing_region)
                final_regions.append(existing_region.get_merged_with(mod_region.exits))
                continue

            final_regions.append(mod_region.get_clone())
    return final_regions


def create_final_connections(world_options: StardewOptions) -> List[ConnectionData]:
    final_connections = []
    final_connections.extend(vanilla_connections)
    if world_options[options.Mods] is None:
        return final_connections
    for mod in world_options[options.Mods]:
        if mod not in ModDataList:
            continue
        final_connections.extend(ModDataList[mod].connections)
    return final_connections


def create_regions(region_factory: RegionFactory, random: Random, world_options: StardewOptions) -> Tuple[
    Iterable[Region], Dict[str, str]]:
    final_regions = create_final_regions(world_options)
    regions: Dict[str: Region] = {region.name: region_factory(region.name, region.exits) for region in
                                  final_regions}
    entrances: Dict[str: Entrance] = {entrance.name: entrance
                                      for region in regions.values()
                                      for entrance in region.exits}

    regions_by_name: Dict[str, RegionData] = {region.name: region for region in final_regions}
    connections, randomized_data = randomize_connections(random, world_options, regions_by_name)

    for connection in connections:
        if connection.name in entrances:
            entrances[connection.name].connect(regions[connection.destination])

    return regions.values(), randomized_data


def randomize_connections(random: Random, world_options: StardewOptions, regions_by_name) -> Tuple[
    List[ConnectionData], Dict[str, str]]:
    connections_to_randomize = []
    final_connections = create_final_connections(world_options)
    connections_by_name: Dict[str, ConnectionData] = {connection.name: connection for connection in final_connections}
    if world_options[options.EntranceRandomization] == options.EntranceRandomization.option_pelican_town:
        connections_to_randomize = [connection for connection in final_connections if
                                    RandomizationFlag.PELICAN_TOWN in connection.flag]
    elif world_options[options.EntranceRandomization] == options.EntranceRandomization.option_non_progression:
        connections_to_randomize = [connection for connection in final_connections if
                                    RandomizationFlag.NON_PROGRESSION in connection.flag]
    elif world_options[options.EntranceRandomization] == options.EntranceRandomization.option_buildings:
        connections_to_randomize = [connection for connection in final_connections if
                                    RandomizationFlag.BUILDINGS in connection.flag]
    elif world_options[options.EntranceRandomization] == options.EntranceRandomization.option_chaos:
        connections_to_randomize = [connection for connection in final_connections if
                                    RandomizationFlag.BUILDINGS in connection.flag]
        connections_to_randomize = exclude_island_if_necessary(connections_to_randomize, world_options)

        # On Chaos, we just add the connections to randomize, unshuffled, and the client does it every day
        randomized_data_for_mod = {}
        for connection in connections_to_randomize:
            randomized_data_for_mod[connection.name] = connection.name
            randomized_data_for_mod[connection.reverse] = connection.reverse
        return final_connections, randomized_data_for_mod
    exclude_island = world_options[options.ExcludeGingerIsland] == options.ExcludeGingerIsland.option_true
    if exclude_island:
        connections_to_randomize = [connection for connection in connections_to_randomize if
                                    RandomizationFlag.GINGER_ISLAND not in connection.flag]
    random.shuffle(connections_to_randomize)
    destination_pool = list(connections_to_randomize)
    random.shuffle(destination_pool)

    randomized_connections = randomize_chosen_connections(connections_to_randomize, destination_pool)
    add_non_randomized_connections(final_connections, connections_to_randomize, randomized_connections)

    swap_connections_until_valid(regions_by_name, connections_by_name, randomized_connections, random)
    randomized_connections_for_generation = create_connections_for_generation(randomized_connections)
    randomized_data_for_mod = create_data_for_mod(randomized_connections, connections_to_randomize)

    return randomized_connections_for_generation, randomized_data_for_mod


def exclude_island_if_necessary(connections_to_randomize: List[ConnectionData], world_options) -> List[ConnectionData]:
    exclude_island = world_options[options.ExcludeGingerIsland] == options.ExcludeGingerIsland.option_true
    if exclude_island:
        connections_to_randomize = [connection for connection in connections_to_randomize if
                                    RandomizationFlag.GINGER_ISLAND not in connection.flag]
    return connections_to_randomize


def randomize_chosen_connections(connections_to_randomize: List[ConnectionData],
                                 destination_pool: List[ConnectionData]) -> Dict[ConnectionData, ConnectionData]:
    randomized_connections = {}
    for connection in connections_to_randomize:
        destination = destination_pool.pop()
        randomized_connections[connection] = destination
    return randomized_connections


def create_connections_for_generation(randomized_connections: Dict[ConnectionData, ConnectionData]) -> List[
    ConnectionData]:
    connections = []
    for connection in randomized_connections:
        destination = randomized_connections[connection]
        connections.append(ConnectionData(connection.name, destination.destination, destination.reverse))
    return connections


def create_data_for_mod(randomized_connections: Dict[ConnectionData, ConnectionData],
                        connections_to_randomize: List[ConnectionData]) -> Dict[str, str]:
    randomized_data_for_mod = {}
    for connection in randomized_connections:
        if connection not in connections_to_randomize:
            continue
        destination = randomized_connections[connection]
        add_to_mod_data(connection, destination, randomized_data_for_mod)
    return randomized_data_for_mod

def add_to_mod_data(connection: ConnectionData, destination: ConnectionData, randomized_data_for_mod: Dict[str, str]):
    randomized_data_for_mod[connection.name] = destination.name
    randomized_data_for_mod[destination.reverse] = connection.reverse


def add_non_randomized_connections(connections, connections_to_randomize: List[ConnectionData],
                                   randomized_connections: Dict[ConnectionData, ConnectionData]):
    for connection in connections:
        if connection in connections_to_randomize:
            continue
        randomized_connections[connection] = connection


def swap_connections_until_valid(regions_by_name, connections_by_name,
                                 randomized_connections: Dict[ConnectionData, ConnectionData], random: Random):
    while True:
        reachable_regions, unreachable_regions = find_reachable_regions(regions_by_name, connections_by_name, randomized_connections)
        if not unreachable_regions:
            return randomized_connections
        swap_one_connection(regions_by_name, connections_by_name, randomized_connections, reachable_regions,
                            unreachable_regions, random)


def find_reachable_regions(regions_by_name, connections_by_name,
                           randomized_connections: Dict[ConnectionData, ConnectionData]):
    reachable_regions = {Region.menu}
    unreachable_regions = {region for region in regions_by_name.keys()}
    unreachable_regions.remove(Region.menu)
    exits_to_explore = list(regions_by_name[Region.menu].exits)
    while exits_to_explore:
        exit_name = exits_to_explore.pop()
        exit_connection = connections_by_name[exit_name]
        replaced_connection = randomized_connections[exit_connection]
        target_region_name = replaced_connection.destination
        if target_region_name in reachable_regions:
            continue

        target_region = regions_by_name[target_region_name]
        reachable_regions.add(target_region_name)
        unreachable_regions.remove(target_region_name)
        exits_to_explore.extend(target_region.exits)
    return reachable_regions, unreachable_regions


def swap_one_connection(regions_by_name, connections_by_name,
                        randomized_connections: Dict[ConnectionData, ConnectionData],
                        reachable_regions: Set[str], unreachable_regions: Set[str], random: Random):
    randomized_connections_already_shuffled = {connection: randomized_connections[connection]
                                               for connection in randomized_connections
                                               if connection != randomized_connections[connection]}
    unreachable_regions_leading_somewhere = tuple([region for region in unreachable_regions
                                                   if len(regions_by_name[region].exits) > 0])
    chosen_unreachable_region_name = random.choice(unreachable_regions_leading_somewhere)
    chosen_unreachable_region = regions_by_name[chosen_unreachable_region_name]
    chosen_unreachable_entrance_name = random.choice(chosen_unreachable_region.exits)
    chosen_unreachable_entrance = connections_by_name[chosen_unreachable_entrance_name]

    chosen_reachable_entrance = None
    while chosen_reachable_entrance is None or chosen_reachable_entrance not in randomized_connections_already_shuffled:
        chosen_reachable_region_name = random.choice(tuple(reachable_regions))
        chosen_reachable_region = regions_by_name[chosen_reachable_region_name]
        if not any(chosen_reachable_region.exits):
            continue
        chosen_reachable_entrance_name = random.choice(chosen_reachable_region.exits)
        chosen_reachable_entrance = connections_by_name[chosen_reachable_entrance_name]

    reachable_destination = randomized_connections[chosen_reachable_entrance]
    unreachable_destination = randomized_connections[chosen_unreachable_entrance]
    randomized_connections[chosen_reachable_entrance] = unreachable_destination
    randomized_connections[chosen_unreachable_entrance] = reachable_destination
