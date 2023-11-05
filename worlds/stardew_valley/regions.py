from random import Random
from typing import Iterable, Dict, Protocol, List, Tuple, Set

from BaseClasses import Region, Entrance
from .options import EntranceRandomization, ExcludeGingerIsland, Museumsanity
from .strings.entrance_names import Entrance
from .strings.region_names import Region
from .region_classes import RegionData, ConnectionData, RandomizationFlag
from .mods.mod_regions import ModDataList


class RegionFactory(Protocol):
    def __call__(self, name: str, regions: Iterable[str]) -> Region:
        raise NotImplementedError


vanilla_regions = [
    RegionData(Region.menu, [Entrance.to_stardew_valley]),
    RegionData(Region.stardew_valley, [Entrance.to_farmhouse]),
    RegionData(Region.farm_house, [Entrance.farmhouse_to_farm, Entrance.downstairs_to_cellar]),
    RegionData(Region.cellar),
    RegionData(Region.farm,
               [Entrance.farm_to_backwoods, Entrance.farm_to_bus_stop, Entrance.farm_to_forest,
                Entrance.farm_to_farmcave, Entrance.enter_greenhouse,
                Entrance.use_desert_obelisk, Entrance.use_island_obelisk]),
    RegionData(Region.backwoods, [Entrance.backwoods_to_mountain]),
    RegionData(Region.bus_stop,
               [Entrance.bus_stop_to_town, Entrance.take_bus_to_desert, Entrance.bus_stop_to_tunnel_entrance]),
    RegionData(Region.forest,
               [Entrance.forest_to_town, Entrance.enter_secret_woods, Entrance.forest_to_wizard_tower,
                Entrance.forest_to_marnie_ranch,
                Entrance.forest_to_leah_cottage, Entrance.forest_to_sewer,
                Entrance.buy_from_traveling_merchant]),
    RegionData(Region.traveling_cart),
    RegionData(Region.farm_cave),
    RegionData(Region.greenhouse),
    RegionData(Region.mountain,
               [Entrance.mountain_to_railroad, Entrance.mountain_to_tent, Entrance.mountain_to_carpenter_shop,
                Entrance.mountain_to_the_mines, Entrance.enter_quarry, Entrance.mountain_to_adventurer_guild,
                Entrance.mountain_to_town, Entrance.mountain_to_maru_room,
                Entrance.mountain_to_leo_treehouse]),
    RegionData(Region.leo_treehouse),
    RegionData(Region.maru_room),
    RegionData(Region.tunnel_entrance, [Entrance.tunnel_entrance_to_bus_tunnel]),
    RegionData(Region.bus_tunnel),
    RegionData(Region.town,
               [Entrance.town_to_community_center, Entrance.town_to_beach, Entrance.town_to_hospital,
                Entrance.town_to_pierre_general_store, Entrance.town_to_saloon, Entrance.town_to_alex_house,
                Entrance.town_to_trailer,
                Entrance.town_to_mayor_manor,
                Entrance.town_to_sam_house, Entrance.town_to_haley_house, Entrance.town_to_sewer,
                Entrance.town_to_clint_blacksmith,
                Entrance.town_to_museum,
                Entrance.town_to_jojamart]),
    RegionData(Region.beach,
               [Entrance.beach_to_willy_fish_shop, Entrance.enter_elliott_house, Entrance.enter_tide_pools]),
    RegionData(Region.railroad, [Entrance.enter_bathhouse_entrance, Entrance.enter_witch_warp_cave]),
    RegionData(Region.ranch),
    RegionData(Region.leah_house),
    RegionData(Region.sewer, [Entrance.enter_mutant_bug_lair]),
    RegionData(Region.mutant_bug_lair),
    RegionData(Region.wizard_tower, [Entrance.enter_wizard_basement]),
    RegionData(Region.wizard_basement),
    RegionData(Region.tent),
    RegionData(Region.carpenter, [Entrance.enter_sebastian_room]),
    RegionData(Region.sebastian_room),
    RegionData(Region.adventurer_guild),
    RegionData(Region.community_center,
               [Entrance.access_crafts_room, Entrance.access_pantry, Entrance.access_fish_tank,
                Entrance.access_boiler_room, Entrance.access_bulletin_board, Entrance.access_vault]),
    RegionData(Region.crafts_room),
    RegionData(Region.pantry),
    RegionData(Region.fish_tank),
    RegionData(Region.boiler_room),
    RegionData(Region.bulletin_board),
    RegionData(Region.vault),
    RegionData(Region.hospital, [Entrance.enter_harvey_room]),
    RegionData(Region.harvey_room),
    RegionData(Region.pierre_store, [Entrance.enter_sunroom]),
    RegionData(Region.sunroom),
    RegionData(Region.saloon, [Entrance.play_journey_of_the_prairie_king, Entrance.play_junimo_kart]),
    RegionData(Region.alex_house),
    RegionData(Region.trailer),
    RegionData(Region.mayor_house),
    RegionData(Region.sam_house),
    RegionData(Region.haley_house),
    RegionData(Region.blacksmith),
    RegionData(Region.museum),
    RegionData(Region.jojamart),
    RegionData(Region.fish_shop, [Entrance.fish_shop_to_boat_tunnel]),
    RegionData(Region.boat_tunnel, [Entrance.boat_to_ginger_island]),
    RegionData(Region.elliott_house),
    RegionData(Region.tide_pools),
    RegionData(Region.bathhouse_entrance, [Entrance.enter_locker_room]),
    RegionData(Region.locker_room, [Entrance.enter_public_bath]),
    RegionData(Region.public_bath),
    RegionData(Region.witch_warp_cave, [Entrance.enter_witch_swamp]),
    RegionData(Region.witch_swamp, [Entrance.enter_witch_hut]),
    RegionData(Region.witch_hut, [Entrance.witch_warp_to_wizard_basement]),
    RegionData(Region.quarry, [Entrance.enter_quarry_mine_entrance]),
    RegionData(Region.quarry_mine_entrance, [Entrance.enter_quarry_mine]),
    RegionData(Region.quarry_mine),
    RegionData(Region.secret_woods),
    RegionData(Region.desert, [Entrance.enter_skull_cavern_entrance, Entrance.enter_oasis]),
    RegionData(Region.oasis, [Entrance.enter_casino]),
    RegionData(Region.casino),
    RegionData(Region.skull_cavern_entrance, [Entrance.enter_skull_cavern]),
    RegionData(Region.skull_cavern, [Entrance.mine_to_skull_cavern_floor_25, Entrance.mine_to_skull_cavern_floor_50,
                                     Entrance.mine_to_skull_cavern_floor_75, Entrance.mine_to_skull_cavern_floor_100,
                                     Entrance.mine_to_skull_cavern_floor_125, Entrance.mine_to_skull_cavern_floor_150,
                                     Entrance.mine_to_skull_cavern_floor_175, Entrance.mine_to_skull_cavern_floor_200]),
    RegionData(Region.skull_cavern_25),
    RegionData(Region.skull_cavern_50),
    RegionData(Region.skull_cavern_75),
    RegionData(Region.skull_cavern_100),
    RegionData(Region.skull_cavern_125),
    RegionData(Region.skull_cavern_150),
    RegionData(Region.skull_cavern_175),
    RegionData(Region.skull_cavern_200),
    RegionData(Region.island_south, [Entrance.island_south_to_west, Entrance.island_south_to_north,
                                     Entrance.island_south_to_east, Entrance.island_south_to_southeast,
                                     Entrance.use_island_resort,
                                     Entrance.parrot_express_docks_to_volcano,
                                     Entrance.parrot_express_docks_to_dig_site,
                                     Entrance.parrot_express_docks_to_jungle]),
    RegionData(Region.island_resort),
    RegionData(Region.island_west,
               [Entrance.island_west_to_islandfarmhouse, Entrance.island_west_to_gourmand_cave,
                Entrance.island_west_to_crystals_cave, Entrance.island_west_to_shipwreck,
                Entrance.island_west_to_qi_walnut_room, Entrance.use_farm_obelisk,
                Entrance.parrot_express_jungle_to_docks, Entrance.parrot_express_jungle_to_dig_site,
                Entrance.parrot_express_jungle_to_volcano]),
    RegionData(Region.island_east, [Entrance.island_east_to_leo_hut, Entrance.island_east_to_island_shrine]),
    RegionData(Region.island_shrine),
    RegionData(Region.island_south_east, [Entrance.island_southeast_to_pirate_cove]),
    RegionData(Region.island_north, [Entrance.talk_to_island_trader, Entrance.island_north_to_field_office,
                                     Entrance.island_north_to_dig_site, Entrance.island_north_to_volcano,
                                     Entrance.parrot_express_volcano_to_dig_site,
                                     Entrance.parrot_express_volcano_to_jungle,
                                     Entrance.parrot_express_volcano_to_docks]),
    RegionData(Region.volcano, [Entrance.climb_to_volcano_5, Entrance.volcano_to_secret_beach]),
    RegionData(Region.volcano_secret_beach),
    RegionData(Region.volcano_floor_5, [Entrance.talk_to_volcano_dwarf, Entrance.climb_to_volcano_10]),
    RegionData(Region.volcano_dwarf_shop),
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
               [Entrance.dig_site_to_professor_snail_cave, Entrance.parrot_express_dig_site_to_volcano,
                Entrance.parrot_express_dig_site_to_docks, Entrance.parrot_express_dig_site_to_jungle]),
    RegionData(Region.professor_snail_cave),
    RegionData(Region.jotpk_world_1, [Entrance.reach_jotpk_world_2]),
    RegionData(Region.jotpk_world_2, [Entrance.reach_jotpk_world_3]),
    RegionData(Region.jotpk_world_3),
    RegionData(Region.junimo_kart_1, [Entrance.reach_junimo_kart_2]),
    RegionData(Region.junimo_kart_2, [Entrance.reach_junimo_kart_3]),
    RegionData(Region.junimo_kart_3),
    RegionData(Region.mines, [Entrance.talk_to_mines_dwarf,
                              Entrance.dig_to_mines_floor_5, Entrance.dig_to_mines_floor_10,
                              Entrance.dig_to_mines_floor_15, Entrance.dig_to_mines_floor_20,
                              Entrance.dig_to_mines_floor_25, Entrance.dig_to_mines_floor_30,
                              Entrance.dig_to_mines_floor_35, Entrance.dig_to_mines_floor_40,
                              Entrance.dig_to_mines_floor_45, Entrance.dig_to_mines_floor_50,
                              Entrance.dig_to_mines_floor_55, Entrance.dig_to_mines_floor_60,
                              Entrance.dig_to_mines_floor_65, Entrance.dig_to_mines_floor_70,
                              Entrance.dig_to_mines_floor_75, Entrance.dig_to_mines_floor_80,
                              Entrance.dig_to_mines_floor_85, Entrance.dig_to_mines_floor_90,
                              Entrance.dig_to_mines_floor_95, Entrance.dig_to_mines_floor_100,
                              Entrance.dig_to_mines_floor_105, Entrance.dig_to_mines_floor_110,
                              Entrance.dig_to_mines_floor_115, Entrance.dig_to_mines_floor_120]),
    RegionData(Region.mines_dwarf_shop),
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
    ConnectionData(Entrance.to_stardew_valley, Region.stardew_valley),
    ConnectionData(Entrance.to_farmhouse, Region.farm_house),
    ConnectionData(Entrance.farmhouse_to_farm, Region.farm),
    ConnectionData(Entrance.downstairs_to_cellar, Region.cellar),
    ConnectionData(Entrance.farm_to_backwoods, Region.backwoods),
    ConnectionData(Entrance.farm_to_bus_stop, Region.bus_stop),
    ConnectionData(Entrance.farm_to_forest, Region.forest),
    ConnectionData(Entrance.farm_to_farmcave, Region.farm_cave, flag=RandomizationFlag.NON_PROGRESSION),
    ConnectionData(Entrance.enter_greenhouse, Region.greenhouse),
    ConnectionData(Entrance.use_desert_obelisk, Region.desert),
    ConnectionData(Entrance.use_island_obelisk, Region.island_south),
    ConnectionData(Entrance.use_farm_obelisk, Region.farm),
    ConnectionData(Entrance.backwoods_to_mountain, Region.mountain),
    ConnectionData(Entrance.bus_stop_to_town, Region.town),
    ConnectionData(Entrance.bus_stop_to_tunnel_entrance, Region.tunnel_entrance),
    ConnectionData(Entrance.tunnel_entrance_to_bus_tunnel, Region.bus_tunnel, flag=RandomizationFlag.NON_PROGRESSION),
    ConnectionData(Entrance.take_bus_to_desert, Region.desert),
    ConnectionData(Entrance.forest_to_town, Region.town),
    ConnectionData(Entrance.forest_to_wizard_tower, Region.wizard_tower,
                   flag=RandomizationFlag.NON_PROGRESSION | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(Entrance.enter_wizard_basement, Region.wizard_basement, flag=RandomizationFlag.BUILDINGS),
    ConnectionData(Entrance.forest_to_marnie_ranch, Region.ranch,
                   flag=RandomizationFlag.NON_PROGRESSION | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(Entrance.forest_to_leah_cottage, Region.leah_house,
                   flag=RandomizationFlag.BUILDINGS | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(Entrance.enter_secret_woods, Region.secret_woods),
    ConnectionData(Entrance.forest_to_sewer, Region.sewer, flag=RandomizationFlag.BUILDINGS),
    ConnectionData(Entrance.buy_from_traveling_merchant, Region.traveling_cart),
    ConnectionData(Entrance.town_to_sewer, Region.sewer, flag=RandomizationFlag.BUILDINGS),
    ConnectionData(Entrance.enter_mutant_bug_lair, Region.mutant_bug_lair, flag=RandomizationFlag.BUILDINGS),
    ConnectionData(Entrance.mountain_to_railroad, Region.railroad),
    ConnectionData(Entrance.mountain_to_tent, Region.tent,
                   flag=RandomizationFlag.NON_PROGRESSION | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(Entrance.mountain_to_leo_treehouse, Region.leo_treehouse,
                   flag=RandomizationFlag.BUILDINGS | RandomizationFlag.LEAD_TO_OPEN_AREA | RandomizationFlag.GINGER_ISLAND),
    ConnectionData(Entrance.mountain_to_carpenter_shop, Region.carpenter,
                   flag=RandomizationFlag.NON_PROGRESSION | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(Entrance.mountain_to_maru_room, Region.maru_room,
                   flag=RandomizationFlag.BUILDINGS | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(Entrance.enter_sebastian_room, Region.sebastian_room, flag=RandomizationFlag.BUILDINGS),
    ConnectionData(Entrance.mountain_to_adventurer_guild, Region.adventurer_guild,
                   flag=RandomizationFlag.BUILDINGS | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(Entrance.enter_quarry, Region.quarry),
    ConnectionData(Entrance.enter_quarry_mine_entrance, Region.quarry_mine_entrance,
                   flag=RandomizationFlag.BUILDINGS),
    ConnectionData(Entrance.enter_quarry_mine, Region.quarry_mine),
    ConnectionData(Entrance.mountain_to_town, Region.town),
    ConnectionData(Entrance.town_to_community_center, Region.community_center,
                   flag=RandomizationFlag.PELICAN_TOWN | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(Entrance.access_crafts_room, Region.crafts_room),
    ConnectionData(Entrance.access_pantry, Region.pantry),
    ConnectionData(Entrance.access_fish_tank, Region.fish_tank),
    ConnectionData(Entrance.access_boiler_room, Region.boiler_room),
    ConnectionData(Entrance.access_bulletin_board, Region.bulletin_board),
    ConnectionData(Entrance.access_vault, Region.vault),
    ConnectionData(Entrance.town_to_hospital, Region.hospital,
                   flag=RandomizationFlag.PELICAN_TOWN | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(Entrance.enter_harvey_room, Region.harvey_room, flag=RandomizationFlag.BUILDINGS),
    ConnectionData(Entrance.town_to_pierre_general_store, Region.pierre_store,
                   flag=RandomizationFlag.PELICAN_TOWN | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(Entrance.enter_sunroom, Region.sunroom, flag=RandomizationFlag.BUILDINGS),
    ConnectionData(Entrance.town_to_clint_blacksmith, Region.blacksmith,
                   flag=RandomizationFlag.PELICAN_TOWN | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(Entrance.town_to_saloon, Region.saloon,
                   flag=RandomizationFlag.PELICAN_TOWN | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(Entrance.play_journey_of_the_prairie_king, Region.jotpk_world_1),
    ConnectionData(Entrance.reach_jotpk_world_2, Region.jotpk_world_2),
    ConnectionData(Entrance.reach_jotpk_world_3, Region.jotpk_world_3),
    ConnectionData(Entrance.play_junimo_kart, Region.junimo_kart_1),
    ConnectionData(Entrance.reach_junimo_kart_2, Region.junimo_kart_2),
    ConnectionData(Entrance.reach_junimo_kart_3, Region.junimo_kart_3),
    ConnectionData(Entrance.town_to_sam_house, Region.sam_house,
                   flag=RandomizationFlag.PELICAN_TOWN | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(Entrance.town_to_haley_house, Region.haley_house,
                   flag=RandomizationFlag.PELICAN_TOWN | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(Entrance.town_to_mayor_manor, Region.mayor_house,
                   flag=RandomizationFlag.PELICAN_TOWN | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(Entrance.town_to_alex_house, Region.alex_house,
                   flag=RandomizationFlag.PELICAN_TOWN | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(Entrance.town_to_trailer, Region.trailer,
                   flag=RandomizationFlag.PELICAN_TOWN | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(Entrance.town_to_museum, Region.museum,
                   flag=RandomizationFlag.PELICAN_TOWN | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(Entrance.town_to_jojamart, Region.jojamart,
                   flag=RandomizationFlag.PELICAN_TOWN | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(Entrance.town_to_beach, Region.beach),
    ConnectionData(Entrance.enter_elliott_house, Region.elliott_house,
                   flag=RandomizationFlag.BUILDINGS | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(Entrance.beach_to_willy_fish_shop, Region.fish_shop,
                   flag=RandomizationFlag.NON_PROGRESSION | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(Entrance.fish_shop_to_boat_tunnel, Region.boat_tunnel,
                   flag=RandomizationFlag.BUILDINGS | RandomizationFlag.GINGER_ISLAND),
    ConnectionData(Entrance.boat_to_ginger_island, Region.island_south),
    ConnectionData(Entrance.enter_tide_pools, Region.tide_pools),
    ConnectionData(Entrance.mountain_to_the_mines, Region.mines,
                   flag=RandomizationFlag.NON_PROGRESSION | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(Entrance.talk_to_mines_dwarf, Region.mines_dwarf_shop),
    ConnectionData(Entrance.dig_to_mines_floor_5, Region.mines_floor_5),
    ConnectionData(Entrance.dig_to_mines_floor_10, Region.mines_floor_10),
    ConnectionData(Entrance.dig_to_mines_floor_15, Region.mines_floor_15),
    ConnectionData(Entrance.dig_to_mines_floor_20, Region.mines_floor_20),
    ConnectionData(Entrance.dig_to_mines_floor_25, Region.mines_floor_25),
    ConnectionData(Entrance.dig_to_mines_floor_30, Region.mines_floor_30),
    ConnectionData(Entrance.dig_to_mines_floor_35, Region.mines_floor_35),
    ConnectionData(Entrance.dig_to_mines_floor_40, Region.mines_floor_40),
    ConnectionData(Entrance.dig_to_mines_floor_45, Region.mines_floor_45),
    ConnectionData(Entrance.dig_to_mines_floor_50, Region.mines_floor_50),
    ConnectionData(Entrance.dig_to_mines_floor_55, Region.mines_floor_55),
    ConnectionData(Entrance.dig_to_mines_floor_60, Region.mines_floor_60),
    ConnectionData(Entrance.dig_to_mines_floor_65, Region.mines_floor_65),
    ConnectionData(Entrance.dig_to_mines_floor_70, Region.mines_floor_70),
    ConnectionData(Entrance.dig_to_mines_floor_75, Region.mines_floor_75),
    ConnectionData(Entrance.dig_to_mines_floor_80, Region.mines_floor_80),
    ConnectionData(Entrance.dig_to_mines_floor_85, Region.mines_floor_85),
    ConnectionData(Entrance.dig_to_mines_floor_90, Region.mines_floor_90),
    ConnectionData(Entrance.dig_to_mines_floor_95, Region.mines_floor_95),
    ConnectionData(Entrance.dig_to_mines_floor_100, Region.mines_floor_100),
    ConnectionData(Entrance.dig_to_mines_floor_105, Region.mines_floor_105),
    ConnectionData(Entrance.dig_to_mines_floor_110, Region.mines_floor_110),
    ConnectionData(Entrance.dig_to_mines_floor_115, Region.mines_floor_115),
    ConnectionData(Entrance.dig_to_mines_floor_120, Region.mines_floor_120),
    ConnectionData(Entrance.enter_skull_cavern_entrance, Region.skull_cavern_entrance,
                   flag=RandomizationFlag.BUILDINGS | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(Entrance.enter_oasis, Region.oasis,
                   flag=RandomizationFlag.BUILDINGS | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(Entrance.enter_casino, Region.casino, flag=RandomizationFlag.BUILDINGS),
    ConnectionData(Entrance.enter_skull_cavern, Region.skull_cavern),
    ConnectionData(Entrance.mine_to_skull_cavern_floor_25, Region.skull_cavern_25),
    ConnectionData(Entrance.mine_to_skull_cavern_floor_50, Region.skull_cavern_50),
    ConnectionData(Entrance.mine_to_skull_cavern_floor_75, Region.skull_cavern_75),
    ConnectionData(Entrance.mine_to_skull_cavern_floor_100, Region.skull_cavern_100),
    ConnectionData(Entrance.mine_to_skull_cavern_floor_125, Region.skull_cavern_125),
    ConnectionData(Entrance.mine_to_skull_cavern_floor_150, Region.skull_cavern_150),
    ConnectionData(Entrance.mine_to_skull_cavern_floor_175, Region.skull_cavern_175),
    ConnectionData(Entrance.mine_to_skull_cavern_floor_200, Region.skull_cavern_200),
    ConnectionData(Entrance.enter_witch_warp_cave, Region.witch_warp_cave, flag=RandomizationFlag.BUILDINGS),
    ConnectionData(Entrance.enter_witch_swamp, Region.witch_swamp, flag=RandomizationFlag.BUILDINGS),
    ConnectionData(Entrance.enter_witch_hut, Region.witch_hut, flag=RandomizationFlag.BUILDINGS),
    ConnectionData(Entrance.witch_warp_to_wizard_basement, Region.wizard_basement, flag=RandomizationFlag.BUILDINGS),
    ConnectionData(Entrance.enter_bathhouse_entrance, Region.bathhouse_entrance,
                   flag=RandomizationFlag.BUILDINGS | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(Entrance.enter_locker_room, Region.locker_room, flag=RandomizationFlag.BUILDINGS),
    ConnectionData(Entrance.enter_public_bath, Region.public_bath, flag=RandomizationFlag.BUILDINGS),
    ConnectionData(Entrance.island_south_to_west, Region.island_west, flag=RandomizationFlag.GINGER_ISLAND),
    ConnectionData(Entrance.island_south_to_north, Region.island_north, flag=RandomizationFlag.GINGER_ISLAND),
    ConnectionData(Entrance.island_south_to_east, Region.island_east, flag=RandomizationFlag.GINGER_ISLAND),
    ConnectionData(Entrance.island_south_to_southeast, Region.island_south_east,
                   flag=RandomizationFlag.GINGER_ISLAND),
    ConnectionData(Entrance.use_island_resort, Region.island_resort),
    ConnectionData(Entrance.island_west_to_islandfarmhouse, Region.island_farmhouse,
                   flag=RandomizationFlag.BUILDINGS | RandomizationFlag.GINGER_ISLAND),
    ConnectionData(Entrance.island_west_to_gourmand_cave, Region.gourmand_frog_cave,
                   flag=RandomizationFlag.BUILDINGS | RandomizationFlag.GINGER_ISLAND),
    ConnectionData(Entrance.island_west_to_crystals_cave, Region.colored_crystals_cave,
                   flag=RandomizationFlag.BUILDINGS | RandomizationFlag.GINGER_ISLAND),
    ConnectionData(Entrance.island_west_to_shipwreck, Region.shipwreck,
                   flag=RandomizationFlag.BUILDINGS | RandomizationFlag.GINGER_ISLAND),
    ConnectionData(Entrance.island_west_to_qi_walnut_room, Region.qi_walnut_room,
                   flag=RandomizationFlag.BUILDINGS | RandomizationFlag.GINGER_ISLAND),
    ConnectionData(Entrance.island_east_to_leo_hut, Region.leo_hut,
                   flag=RandomizationFlag.BUILDINGS | RandomizationFlag.GINGER_ISLAND),
    ConnectionData(Entrance.island_east_to_island_shrine, Region.island_shrine,
                   flag=RandomizationFlag.BUILDINGS | RandomizationFlag.GINGER_ISLAND),
    ConnectionData(Entrance.island_southeast_to_pirate_cove, Region.pirate_cove,
                   flag=RandomizationFlag.BUILDINGS | RandomizationFlag.GINGER_ISLAND),
    ConnectionData(Entrance.island_north_to_field_office, Region.field_office,
                   flag=RandomizationFlag.BUILDINGS | RandomizationFlag.GINGER_ISLAND),
    ConnectionData(Entrance.island_north_to_dig_site, Region.dig_site, flag=RandomizationFlag.GINGER_ISLAND),
    ConnectionData(Entrance.dig_site_to_professor_snail_cave, Region.professor_snail_cave, flag=RandomizationFlag.BUILDINGS | RandomizationFlag.GINGER_ISLAND),
    ConnectionData(Entrance.island_north_to_volcano, Region.volcano,
                   flag=RandomizationFlag.BUILDINGS | RandomizationFlag.GINGER_ISLAND),
    ConnectionData(Entrance.volcano_to_secret_beach, Region.volcano_secret_beach,
                   flag=RandomizationFlag.BUILDINGS | RandomizationFlag.GINGER_ISLAND),
    ConnectionData(Entrance.talk_to_island_trader, Region.island_trader, flag=RandomizationFlag.GINGER_ISLAND),
    ConnectionData(Entrance.climb_to_volcano_5, Region.volcano_floor_5),
    ConnectionData(Entrance.talk_to_volcano_dwarf, Region.volcano_dwarf_shop),
    ConnectionData(Entrance.climb_to_volcano_10, Region.volcano_floor_10),
    ConnectionData(Entrance.parrot_express_jungle_to_docks, Region.island_south),
    ConnectionData(Entrance.parrot_express_dig_site_to_docks, Region.island_south),
    ConnectionData(Entrance.parrot_express_volcano_to_docks, Region.island_south),
    ConnectionData(Entrance.parrot_express_volcano_to_jungle, Region.island_west),
    ConnectionData(Entrance.parrot_express_docks_to_jungle, Region.island_west),
    ConnectionData(Entrance.parrot_express_dig_site_to_jungle, Region.island_west),
    ConnectionData(Entrance.parrot_express_docks_to_dig_site, Region.dig_site),
    ConnectionData(Entrance.parrot_express_volcano_to_dig_site, Region.dig_site),
    ConnectionData(Entrance.parrot_express_jungle_to_dig_site, Region.dig_site),
    ConnectionData(Entrance.parrot_express_dig_site_to_volcano, Region.island_north),
    ConnectionData(Entrance.parrot_express_docks_to_volcano, Region.island_north),
    ConnectionData(Entrance.parrot_express_jungle_to_volcano, Region.island_north),
]


def create_final_regions(world_options) -> List[RegionData]:
    final_regions = []
    final_regions.extend(vanilla_regions)
    if world_options.mods is None:
        return final_regions
    for mod in world_options.mods.value:
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


def create_final_connections(world_options) -> List[ConnectionData]:
    final_connections = []
    final_connections.extend(vanilla_connections)
    if world_options.mods is None:
        return final_connections
    for mod in world_options.mods.value:
        if mod not in ModDataList:
            continue
        final_connections.extend(ModDataList[mod].connections)
    return final_connections


def create_regions(region_factory: RegionFactory, random: Random, world_options) -> Tuple[
    Dict[str, Region], Dict[str, str]]:
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

    return regions, randomized_data


def randomize_connections(random: Random, world_options, regions_by_name) -> Tuple[
    List[ConnectionData], Dict[str, str]]:
    connections_to_randomize = []
    final_connections = create_final_connections(world_options)
    connections_by_name: Dict[str, ConnectionData] = {connection.name: connection for connection in final_connections}
    if world_options.entrance_randomization == EntranceRandomization.option_pelican_town:
        connections_to_randomize = [connection for connection in final_connections if
                                    RandomizationFlag.PELICAN_TOWN in connection.flag]
    elif world_options.entrance_randomization == EntranceRandomization.option_non_progression:
        connections_to_randomize = [connection for connection in final_connections if
                                    RandomizationFlag.NON_PROGRESSION in connection.flag]
    elif world_options.entrance_randomization == EntranceRandomization.option_buildings:
        connections_to_randomize = [connection for connection in final_connections if
                                    RandomizationFlag.BUILDINGS in connection.flag]
    elif world_options.entrance_randomization == EntranceRandomization.option_chaos:
        connections_to_randomize = [connection for connection in final_connections if
                                    RandomizationFlag.BUILDINGS in connection.flag]
        connections_to_randomize = exclude_island_if_necessary(connections_to_randomize, world_options)

        # On Chaos, we just add the connections to randomize, unshuffled, and the client does it every day
        randomized_data_for_mod = {}
        for connection in connections_to_randomize:
            randomized_data_for_mod[connection.name] = connection.name
            randomized_data_for_mod[connection.reverse] = connection.reverse
        return final_connections, randomized_data_for_mod

    connections_to_randomize = remove_excluded_entrances(connections_to_randomize, world_options)

    random.shuffle(connections_to_randomize)
    destination_pool = list(connections_to_randomize)
    random.shuffle(destination_pool)

    randomized_connections = randomize_chosen_connections(connections_to_randomize, destination_pool)
    add_non_randomized_connections(final_connections, connections_to_randomize, randomized_connections)

    swap_connections_until_valid(regions_by_name, connections_by_name, randomized_connections, connections_to_randomize, random)
    randomized_connections_for_generation = create_connections_for_generation(randomized_connections)
    randomized_data_for_mod = create_data_for_mod(randomized_connections, connections_to_randomize)

    return randomized_connections_for_generation, randomized_data_for_mod


def remove_excluded_entrances(connections_to_randomize, world_options):
    exclude_island = world_options.exclude_ginger_island == ExcludeGingerIsland.option_true
    exclude_sewers = world_options.museumsanity == Museumsanity.option_none
    if exclude_island:
        connections_to_randomize = [connection for connection in connections_to_randomize if RandomizationFlag.GINGER_ISLAND not in connection.flag]
    if exclude_sewers:
        connections_to_randomize = [connection for connection in connections_to_randomize if Region.sewer not in connection.name or Region.sewer not in connection.reverse]

    return connections_to_randomize


def exclude_island_if_necessary(connections_to_randomize: List[ConnectionData], world_options) -> List[ConnectionData]:
    exclude_island = world_options.exclude_ginger_island == ExcludeGingerIsland.option_true
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


def swap_connections_until_valid(regions_by_name, connections_by_name, randomized_connections: Dict[ConnectionData, ConnectionData],
                                 connections_to_randomize: List[ConnectionData], random: Random):
    while True:
        reachable_regions, unreachable_regions = find_reachable_regions(regions_by_name, connections_by_name, randomized_connections)
        if not unreachable_regions:
            return randomized_connections
        swap_one_connection(regions_by_name, connections_by_name, randomized_connections, reachable_regions,
                            unreachable_regions, connections_to_randomize, random)


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


def swap_one_connection(regions_by_name, connections_by_name,randomized_connections: Dict[ConnectionData, ConnectionData],
                        reachable_regions: Set[str], unreachable_regions: Set[str],
                        connections_to_randomize: List[ConnectionData], random: Random):
    randomized_connections_already_shuffled = {connection: randomized_connections[connection]
                                               for connection in randomized_connections
                                               if connection != randomized_connections[connection]}
    unreachable_regions_names_leading_somewhere = tuple([region for region in unreachable_regions
                                                   if len(regions_by_name[region].exits) > 0])
    unreachable_regions_leading_somewhere = [regions_by_name[region_name] for region_name in unreachable_regions_names_leading_somewhere]
    unreachable_regions_exits_names = [exit_name for region in unreachable_regions_leading_somewhere for exit_name in region.exits]
    unreachable_connections = [connections_by_name[exit_name] for exit_name in unreachable_regions_exits_names]
    unreachable_connections_that_can_be_randomized = [connection for connection in unreachable_connections if connection in connections_to_randomize]

    chosen_unreachable_entrance = random.choice(unreachable_connections_that_can_be_randomized)

    chosen_reachable_entrance = None
    while chosen_reachable_entrance is None or chosen_reachable_entrance not in randomized_connections_already_shuffled:
        chosen_reachable_region_name = random.choice(sorted(reachable_regions))
        chosen_reachable_region = regions_by_name[chosen_reachable_region_name]
        if not any(chosen_reachable_region.exits):
            continue
        chosen_reachable_entrance_name = random.choice(chosen_reachable_region.exits)
        chosen_reachable_entrance = connections_by_name[chosen_reachable_entrance_name]

    reachable_destination = randomized_connections[chosen_reachable_entrance]
    unreachable_destination = randomized_connections[chosen_unreachable_entrance]
    randomized_connections[chosen_reachable_entrance] = unreachable_destination
    randomized_connections[chosen_unreachable_entrance] = reachable_destination
