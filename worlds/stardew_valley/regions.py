from random import Random
from typing import Iterable, Dict, Protocol, List, Tuple, Set

from BaseClasses import Region, Entrance
from .options import EntranceRandomization, ExcludeGingerIsland, Museumsanity, StardewValleyOptions
from .strings.entrance_names import Entrance
from .strings.region_names import Region
from .region_classes import RegionData, ConnectionData, RandomizationFlag, ModificationFlag
from .mods.mod_regions import ModDataList, vanilla_connections_to_remove_by_mod


class RegionFactory(Protocol):
    def __call__(self, name: str, regions: Iterable[str]) -> Region:
        raise NotImplementedError


vanilla_regions = [
    RegionData(Region.menu, [Entrance.to_stardew_valley]),
    RegionData(Region.stardew_valley, [Entrance.to_farmhouse]),
    RegionData(Region.farm_house, [Entrance.farmhouse_to_farm, Entrance.downstairs_to_cellar, Entrance.farmhouse_cooking, Entrance.watch_queen_of_sauce]),
    RegionData(Region.cellar),
    RegionData(Region.kitchen),
    RegionData(Region.queen_of_sauce),
    RegionData(Region.farm,
               [Entrance.farm_to_backwoods, Entrance.farm_to_bus_stop, Entrance.farm_to_forest,
                Entrance.farm_to_farmcave, Entrance.enter_greenhouse,
                Entrance.enter_coop, Entrance.enter_barn,
                Entrance.enter_shed, Entrance.enter_slime_hutch,
                Entrance.farming, Entrance.shipping]),
    RegionData(Region.farming),
    RegionData(Region.shipping),
    RegionData(Region.backwoods, [Entrance.backwoods_to_mountain]),
    RegionData(Region.bus_stop,
               [Entrance.bus_stop_to_town, Entrance.take_bus_to_desert, Entrance.bus_stop_to_tunnel_entrance]),
    RegionData(Region.forest,
               [Entrance.forest_to_town, Entrance.enter_secret_woods, Entrance.forest_to_wizard_tower,
                Entrance.forest_to_marnie_ranch,
                Entrance.forest_to_leah_cottage, Entrance.forest_to_sewer,
                Entrance.buy_from_traveling_merchant,
                Entrance.attend_flower_dance, Entrance.attend_festival_of_ice]),
    RegionData(Region.traveling_cart, [Entrance.buy_from_traveling_merchant_sunday,
                                       Entrance.buy_from_traveling_merchant_monday,
                                       Entrance.buy_from_traveling_merchant_tuesday,
                                       Entrance.buy_from_traveling_merchant_wednesday,
                                       Entrance.buy_from_traveling_merchant_thursday,
                                       Entrance.buy_from_traveling_merchant_friday,
                                       Entrance.buy_from_traveling_merchant_saturday]),
    RegionData(Region.traveling_cart_sunday),
    RegionData(Region.traveling_cart_monday),
    RegionData(Region.traveling_cart_tuesday),
    RegionData(Region.traveling_cart_wednesday),
    RegionData(Region.traveling_cart_thursday),
    RegionData(Region.traveling_cart_friday),
    RegionData(Region.traveling_cart_saturday),
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
                Entrance.town_to_jojamart, Entrance.purchase_movie_ticket,
                Entrance.attend_egg_festival, Entrance.attend_fair, Entrance.attend_spirit_eve, Entrance.attend_winter_star]),
    RegionData(Region.beach, [Entrance.beach_to_willy_fish_shop, Entrance.enter_elliott_house, Entrance.enter_tide_pools,
                              Entrance.fishing,
                              Entrance.attend_luau, Entrance.attend_moonlight_jellies, Entrance.attend_night_market]),
    RegionData(Region.fishing),
    RegionData(Region.railroad, [Entrance.enter_bathhouse_entrance, Entrance.enter_witch_warp_cave]),
    RegionData(Region.ranch),
    RegionData(Region.leah_house),
    RegionData(Region.sewer, [Entrance.enter_mutant_bug_lair]),
    RegionData(Region.mutant_bug_lair),
    RegionData(Region.wizard_tower, [Entrance.enter_wizard_basement,
                                     Entrance.use_desert_obelisk, Entrance.use_island_obelisk]),
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
    RegionData(Region.jotpk_world_1, [Entrance.reach_jotpk_world_2]),
    RegionData(Region.jotpk_world_2, [Entrance.reach_jotpk_world_3]),
    RegionData(Region.jotpk_world_3),
    RegionData(Region.junimo_kart_1, [Entrance.reach_junimo_kart_2]),
    RegionData(Region.junimo_kart_2, [Entrance.reach_junimo_kart_3]),
    RegionData(Region.junimo_kart_3),
    RegionData(Region.alex_house),
    RegionData(Region.trailer),
    RegionData(Region.mayor_house),
    RegionData(Region.sam_house),
    RegionData(Region.haley_house),
    RegionData(Region.blacksmith, [Entrance.blacksmith_copper]),
    RegionData(Region.blacksmith_copper, [Entrance.blacksmith_iron]),
    RegionData(Region.blacksmith_iron, [Entrance.blacksmith_gold]),
    RegionData(Region.blacksmith_gold, [Entrance.blacksmith_iridium]),
    RegionData(Region.blacksmith_iridium),
    RegionData(Region.museum),
    RegionData(Region.jojamart, [Entrance.enter_abandoned_jojamart]),
    RegionData(Region.abandoned_jojamart, [Entrance.enter_movie_theater]),
    RegionData(Region.movie_ticket_stand),
    RegionData(Region.movie_theater),
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
    RegionData(Region.skull_cavern, [Entrance.mine_to_skull_cavern_floor_25]),
    RegionData(Region.skull_cavern_25, [Entrance.mine_to_skull_cavern_floor_50]),
    RegionData(Region.skull_cavern_50, [Entrance.mine_to_skull_cavern_floor_75]),
    RegionData(Region.skull_cavern_75, [Entrance.mine_to_skull_cavern_floor_100]),
    RegionData(Region.skull_cavern_100, [Entrance.mine_to_skull_cavern_floor_125]),
    RegionData(Region.skull_cavern_125, [Entrance.mine_to_skull_cavern_floor_150]),
    RegionData(Region.skull_cavern_150, [Entrance.mine_to_skull_cavern_floor_175]),
    RegionData(Region.skull_cavern_175, [Entrance.mine_to_skull_cavern_floor_200]),
    RegionData(Region.skull_cavern_200, [Entrance.enter_dangerous_skull_cavern]),
    RegionData(Region.dangerous_skull_cavern),
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
    RegionData(Region.island_farmhouse, [Entrance.island_cooking]),
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
    RegionData(Region.mines, [Entrance.talk_to_mines_dwarf,
                              Entrance.dig_to_mines_floor_5]),
    RegionData(Region.mines_dwarf_shop),
    RegionData(Region.mines_floor_5, [Entrance.dig_to_mines_floor_10]),
    RegionData(Region.mines_floor_10, [Entrance.dig_to_mines_floor_15]),
    RegionData(Region.mines_floor_15, [Entrance.dig_to_mines_floor_20]),
    RegionData(Region.mines_floor_20, [Entrance.dig_to_mines_floor_25]),
    RegionData(Region.mines_floor_25, [Entrance.dig_to_mines_floor_30]),
    RegionData(Region.mines_floor_30, [Entrance.dig_to_mines_floor_35]),
    RegionData(Region.mines_floor_35, [Entrance.dig_to_mines_floor_40]),
    RegionData(Region.mines_floor_40, [Entrance.dig_to_mines_floor_45]),
    RegionData(Region.mines_floor_45, [Entrance.dig_to_mines_floor_50]),
    RegionData(Region.mines_floor_50, [Entrance.dig_to_mines_floor_55]),
    RegionData(Region.mines_floor_55, [Entrance.dig_to_mines_floor_60]),
    RegionData(Region.mines_floor_60, [Entrance.dig_to_mines_floor_65]),
    RegionData(Region.mines_floor_65, [Entrance.dig_to_mines_floor_70]),
    RegionData(Region.mines_floor_70, [Entrance.dig_to_mines_floor_75]),
    RegionData(Region.mines_floor_75, [Entrance.dig_to_mines_floor_80]),
    RegionData(Region.mines_floor_80, [Entrance.dig_to_mines_floor_85]),
    RegionData(Region.mines_floor_85, [Entrance.dig_to_mines_floor_90]),
    RegionData(Region.mines_floor_90, [Entrance.dig_to_mines_floor_95]),
    RegionData(Region.mines_floor_95, [Entrance.dig_to_mines_floor_100]),
    RegionData(Region.mines_floor_100, [Entrance.dig_to_mines_floor_105]),
    RegionData(Region.mines_floor_105, [Entrance.dig_to_mines_floor_110]),
    RegionData(Region.mines_floor_110, [Entrance.dig_to_mines_floor_115]),
    RegionData(Region.mines_floor_115, [Entrance.dig_to_mines_floor_120]),
    RegionData(Region.mines_floor_120, [Entrance.dig_to_dangerous_mines_20, Entrance.dig_to_dangerous_mines_60, Entrance.dig_to_dangerous_mines_100]),
    RegionData(Region.dangerous_mines_20),
    RegionData(Region.dangerous_mines_60),
    RegionData(Region.dangerous_mines_100),
    RegionData(Region.coop),
    RegionData(Region.barn),
    RegionData(Region.shed),
    RegionData(Region.slime_hutch),
    RegionData(Region.egg_festival),
    RegionData(Region.flower_dance),
    RegionData(Region.luau),
    RegionData(Region.moonlight_jellies),
    RegionData(Region.fair),
    RegionData(Region.spirit_eve),
    RegionData(Region.festival_of_ice),
    RegionData(Region.night_market),
    RegionData(Region.winter_star),
]

# Exists and where they lead
vanilla_connections = [
    ConnectionData(Entrance.to_stardew_valley, Region.stardew_valley),
    ConnectionData(Entrance.to_farmhouse, Region.farm_house),
    ConnectionData(Entrance.farmhouse_to_farm, Region.farm),
    ConnectionData(Entrance.downstairs_to_cellar, Region.cellar),
    ConnectionData(Entrance.farmhouse_cooking, Region.kitchen),
    ConnectionData(Entrance.watch_queen_of_sauce, Region.queen_of_sauce),
    ConnectionData(Entrance.farm_to_backwoods, Region.backwoods),
    ConnectionData(Entrance.farm_to_bus_stop, Region.bus_stop),
    ConnectionData(Entrance.farm_to_forest, Region.forest),
    ConnectionData(Entrance.farm_to_farmcave, Region.farm_cave, flag=RandomizationFlag.NON_PROGRESSION),
    ConnectionData(Entrance.farming, Region.farming),
    ConnectionData(Entrance.enter_greenhouse, Region.greenhouse),
    ConnectionData(Entrance.enter_coop, Region.coop),
    ConnectionData(Entrance.enter_barn, Region.barn),
    ConnectionData(Entrance.enter_shed, Region.shed),
    ConnectionData(Entrance.enter_slime_hutch, Region.slime_hutch),
    ConnectionData(Entrance.shipping, Region.shipping),
    ConnectionData(Entrance.use_desert_obelisk, Region.desert),
    ConnectionData(Entrance.use_island_obelisk, Region.island_south, flag=RandomizationFlag.GINGER_ISLAND),
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
    ConnectionData(Entrance.buy_from_traveling_merchant_sunday, Region.traveling_cart_sunday),
    ConnectionData(Entrance.buy_from_traveling_merchant_monday, Region.traveling_cart_monday),
    ConnectionData(Entrance.buy_from_traveling_merchant_tuesday, Region.traveling_cart_tuesday),
    ConnectionData(Entrance.buy_from_traveling_merchant_wednesday, Region.traveling_cart_wednesday),
    ConnectionData(Entrance.buy_from_traveling_merchant_thursday, Region.traveling_cart_thursday),
    ConnectionData(Entrance.buy_from_traveling_merchant_friday, Region.traveling_cart_friday),
    ConnectionData(Entrance.buy_from_traveling_merchant_saturday, Region.traveling_cart_saturday),
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
    ConnectionData(Entrance.blacksmith_copper, Region.blacksmith_copper),
    ConnectionData(Entrance.blacksmith_iron, Region.blacksmith_iron),
    ConnectionData(Entrance.blacksmith_gold, Region.blacksmith_gold),
    ConnectionData(Entrance.blacksmith_iridium, Region.blacksmith_iridium),
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
    ConnectionData(Entrance.purchase_movie_ticket, Region.movie_ticket_stand),
    ConnectionData(Entrance.enter_abandoned_jojamart, Region.abandoned_jojamart),
    ConnectionData(Entrance.enter_movie_theater, Region.movie_theater),
    ConnectionData(Entrance.town_to_beach, Region.beach),
    ConnectionData(Entrance.enter_elliott_house, Region.elliott_house,
                   flag=RandomizationFlag.BUILDINGS | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(Entrance.beach_to_willy_fish_shop, Region.fish_shop,
                   flag=RandomizationFlag.NON_PROGRESSION | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(Entrance.fish_shop_to_boat_tunnel, Region.boat_tunnel,
                   flag=RandomizationFlag.BUILDINGS | RandomizationFlag.GINGER_ISLAND),
    ConnectionData(Entrance.boat_to_ginger_island, Region.island_south, flag=RandomizationFlag.GINGER_ISLAND),
    ConnectionData(Entrance.enter_tide_pools, Region.tide_pools),
    ConnectionData(Entrance.fishing, Region.fishing),
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
    ConnectionData(Entrance.dig_to_dangerous_mines_20, Region.dangerous_mines_20, flag=RandomizationFlag.GINGER_ISLAND),
    ConnectionData(Entrance.dig_to_dangerous_mines_60, Region.dangerous_mines_60, flag=RandomizationFlag.GINGER_ISLAND),
    ConnectionData(Entrance.dig_to_dangerous_mines_100, Region.dangerous_mines_100, flag=RandomizationFlag.GINGER_ISLAND),
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
    ConnectionData(Entrance.enter_dangerous_skull_cavern, Region.dangerous_skull_cavern, flag=RandomizationFlag.GINGER_ISLAND),
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
    ConnectionData(Entrance.use_island_resort, Region.island_resort, flag=RandomizationFlag.GINGER_ISLAND),
    ConnectionData(Entrance.island_west_to_islandfarmhouse, Region.island_farmhouse,
                   flag=RandomizationFlag.BUILDINGS | RandomizationFlag.GINGER_ISLAND),
    ConnectionData(Entrance.island_cooking, Region.kitchen),
    ConnectionData(Entrance.island_west_to_gourmand_cave, Region.gourmand_frog_cave,
                   flag=RandomizationFlag.BUILDINGS | RandomizationFlag.GINGER_ISLAND),
    ConnectionData(Entrance.island_west_to_crystals_cave, Region.colored_crystals_cave,
                   flag=RandomizationFlag.BUILDINGS | RandomizationFlag.GINGER_ISLAND),
    ConnectionData(Entrance.island_west_to_shipwreck, Region.shipwreck,
                   flag=RandomizationFlag.BUILDINGS | RandomizationFlag.GINGER_ISLAND),
    ConnectionData(Entrance.island_west_to_qi_walnut_room, Region.qi_walnut_room, flag=RandomizationFlag.BUILDINGS | RandomizationFlag.GINGER_ISLAND),
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
    ConnectionData(Entrance.climb_to_volcano_5, Region.volcano_floor_5, flag=RandomizationFlag.GINGER_ISLAND),
    ConnectionData(Entrance.talk_to_volcano_dwarf, Region.volcano_dwarf_shop, flag=RandomizationFlag.GINGER_ISLAND),
    ConnectionData(Entrance.climb_to_volcano_10, Region.volcano_floor_10, flag=RandomizationFlag.GINGER_ISLAND),
    ConnectionData(Entrance.parrot_express_jungle_to_docks, Region.island_south, flag=RandomizationFlag.GINGER_ISLAND),
    ConnectionData(Entrance.parrot_express_dig_site_to_docks, Region.island_south, flag=RandomizationFlag.GINGER_ISLAND),
    ConnectionData(Entrance.parrot_express_volcano_to_docks, Region.island_south, flag=RandomizationFlag.GINGER_ISLAND),
    ConnectionData(Entrance.parrot_express_volcano_to_jungle, Region.island_west, flag=RandomizationFlag.GINGER_ISLAND),
    ConnectionData(Entrance.parrot_express_docks_to_jungle, Region.island_west, flag=RandomizationFlag.GINGER_ISLAND),
    ConnectionData(Entrance.parrot_express_dig_site_to_jungle, Region.island_west, flag=RandomizationFlag.GINGER_ISLAND),
    ConnectionData(Entrance.parrot_express_docks_to_dig_site, Region.dig_site, flag=RandomizationFlag.GINGER_ISLAND),
    ConnectionData(Entrance.parrot_express_volcano_to_dig_site, Region.dig_site, flag=RandomizationFlag.GINGER_ISLAND),
    ConnectionData(Entrance.parrot_express_jungle_to_dig_site, Region.dig_site, flag=RandomizationFlag.GINGER_ISLAND),
    ConnectionData(Entrance.parrot_express_dig_site_to_volcano, Region.island_north, flag=RandomizationFlag.GINGER_ISLAND),
    ConnectionData(Entrance.parrot_express_docks_to_volcano, Region.island_north, flag=RandomizationFlag.GINGER_ISLAND),
    ConnectionData(Entrance.parrot_express_jungle_to_volcano, Region.island_north, flag=RandomizationFlag.GINGER_ISLAND),
    ConnectionData(Entrance.attend_egg_festival, Region.egg_festival),
    ConnectionData(Entrance.attend_flower_dance, Region.flower_dance),
    ConnectionData(Entrance.attend_luau, Region.luau),
    ConnectionData(Entrance.attend_moonlight_jellies, Region.moonlight_jellies),
    ConnectionData(Entrance.attend_fair, Region.fair),
    ConnectionData(Entrance.attend_spirit_eve, Region.spirit_eve),
    ConnectionData(Entrance.attend_festival_of_ice, Region.festival_of_ice),
    ConnectionData(Entrance.attend_night_market, Region.night_market),
    ConnectionData(Entrance.attend_winter_star, Region.winter_star),
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
                if ModificationFlag.MODIFIED in mod_region.flag:
                    mod_region = modify_vanilla_regions(existing_region, mod_region)
                final_regions.append(existing_region.get_merged_with(mod_region.exits))
                continue
            final_regions.append(mod_region.get_clone())

    return final_regions


def create_final_connections_and_regions(world_options) -> Tuple[Dict[str, ConnectionData], Dict[str, RegionData]]:
    regions_data: Dict[str, RegionData] = {region.name: region for region in create_final_regions(world_options)}
    connections = {connection.name: connection for connection in vanilla_connections}
    connections = modify_connections_for_mods(connections, world_options.mods)
    include_island = world_options.exclude_ginger_island == ExcludeGingerIsland.option_false
    return remove_ginger_island_regions_and_connections(regions_data, connections, include_island)


def remove_ginger_island_regions_and_connections(regions_by_name: Dict[str, RegionData], connections: Dict[str, ConnectionData], include_island: bool):
    if include_island:
        return connections, regions_by_name
    for connection_name in list(connections):
        connection = connections[connection_name]
        if connection.flag & RandomizationFlag.GINGER_ISLAND:
            regions_by_name.pop(connection.destination, None)
            connections.pop(connection_name)
            regions_by_name = {name: regions_by_name[name].get_without_exit(connection_name) for name in regions_by_name}
    return connections, regions_by_name


def modify_connections_for_mods(connections: Dict[str, ConnectionData], mods) -> Dict[str, ConnectionData]:
    if mods is None:
        return connections
    for mod in mods.value:
        if mod not in ModDataList:
            continue
        if mod in vanilla_connections_to_remove_by_mod:
            for connection_data in vanilla_connections_to_remove_by_mod[mod]:
                connections.pop(connection_data.name)
        connections.update({connection.name: connection for connection in ModDataList[mod].connections})
    return connections


def modify_vanilla_regions(existing_region: RegionData, modified_region: RegionData) -> RegionData:

    updated_region = existing_region
    region_exits = updated_region.exits
    modified_exits = modified_region.exits
    for exits in modified_exits:
        region_exits.remove(exits)

    return updated_region


def create_regions(region_factory: RegionFactory, random: Random, world_options: StardewValleyOptions) -> Tuple[
    Dict[str, Region], Dict[str, Entrance], Dict[str, str]]:
    entrances_data, regions_data = create_final_connections_and_regions(world_options)
    regions_by_name: Dict[str: Region] = {region_name: region_factory(region_name, regions_data[region_name].exits) for region_name in regions_data}
    entrances_by_name: Dict[str: Entrance] = {entrance.name: entrance for region in regions_by_name.values() for entrance in region.exits
                                              if entrance.name in entrances_data}

    connections, randomized_data = randomize_connections(random, world_options, regions_data, entrances_data)

    for connection in connections:
        if connection.name in entrances_by_name:
            entrances_by_name[connection.name].connect(regions_by_name[connection.destination])
    return regions_by_name, entrances_by_name, randomized_data


def randomize_connections(random: Random, world_options: StardewValleyOptions, regions_by_name: Dict[str, RegionData],
                          connections_by_name: Dict[str, ConnectionData]) -> Tuple[List[ConnectionData], Dict[str, str]]:
    connections_to_randomize: List[ConnectionData] = []
    if world_options.entrance_randomization == EntranceRandomization.option_pelican_town:
        connections_to_randomize = [connections_by_name[connection] for connection in connections_by_name if
                                    RandomizationFlag.PELICAN_TOWN in connections_by_name[connection].flag]
    elif world_options.entrance_randomization == EntranceRandomization.option_non_progression:
        connections_to_randomize = [connections_by_name[connection] for connection in connections_by_name if
                                    RandomizationFlag.NON_PROGRESSION in connections_by_name[connection].flag]
    elif world_options.entrance_randomization == EntranceRandomization.option_buildings:
        connections_to_randomize = [connections_by_name[connection] for connection in connections_by_name if
                                    RandomizationFlag.BUILDINGS in connections_by_name[connection].flag]
    elif world_options.entrance_randomization == EntranceRandomization.option_chaos:
        connections_to_randomize = [connections_by_name[connection] for connection in connections_by_name if
                                    RandomizationFlag.BUILDINGS in connections_by_name[connection].flag]
        connections_to_randomize = remove_excluded_entrances(connections_to_randomize, world_options)

        # On Chaos, we just add the connections to randomize, unshuffled, and the client does it every day
        randomized_data_for_mod = {}
        for connection in connections_to_randomize:
            randomized_data_for_mod[connection.name] = connection.name
            randomized_data_for_mod[connection.reverse] = connection.reverse
        return list(connections_by_name.values()), randomized_data_for_mod

    connections_to_randomize = remove_excluded_entrances(connections_to_randomize, world_options)
    random.shuffle(connections_to_randomize)
    destination_pool = list(connections_to_randomize)
    random.shuffle(destination_pool)

    randomized_connections = randomize_chosen_connections(connections_to_randomize, destination_pool)
    add_non_randomized_connections(list(connections_by_name.values()), connections_to_randomize, randomized_connections)

    swap_connections_until_valid(regions_by_name, connections_by_name, randomized_connections, connections_to_randomize, random)
    randomized_connections_for_generation = create_connections_for_generation(randomized_connections)
    randomized_data_for_mod = create_data_for_mod(randomized_connections, connections_to_randomize)

    return randomized_connections_for_generation, randomized_data_for_mod


def remove_excluded_entrances(connections_to_randomize: List[ConnectionData], world_options: StardewValleyOptions) -> List[ConnectionData]:
    exclude_island = world_options.exclude_ginger_island == ExcludeGingerIsland.option_true
    if exclude_island:
        connections_to_randomize = [connection for connection in connections_to_randomize if RandomizationFlag.GINGER_ISLAND not in connection.flag]

    return connections_to_randomize


def randomize_chosen_connections(connections_to_randomize: List[ConnectionData],
                                 destination_pool: List[ConnectionData]) -> Dict[ConnectionData, ConnectionData]:
    randomized_connections = {}
    for connection in connections_to_randomize:
        destination = destination_pool.pop()
        randomized_connections[connection] = destination
    return randomized_connections


def create_connections_for_generation(randomized_connections: Dict[ConnectionData, ConnectionData]) -> List[ConnectionData]:
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


def add_non_randomized_connections(all_connections: List[ConnectionData], connections_to_randomize: List[ConnectionData],
                                   randomized_connections: Dict[ConnectionData, ConnectionData]):
    for connection in all_connections:
        if connection in connections_to_randomize:
            continue
        randomized_connections[connection] = connection


def swap_connections_until_valid(regions_by_name, connections_by_name: Dict[str, ConnectionData], randomized_connections: Dict[ConnectionData, ConnectionData],
                                 connections_to_randomize: List[ConnectionData], random: Random):
    while True:
        reachable_regions, unreachable_regions = find_reachable_regions(regions_by_name, connections_by_name, randomized_connections)
        if not unreachable_regions:
            return randomized_connections
        swap_one_random_connection(regions_by_name, connections_by_name, randomized_connections, reachable_regions,
                                   unreachable_regions, connections_to_randomize, random)


def region_should_be_reachable(region_name: str, connections_in_slot: Iterable[ConnectionData]) -> bool:
    if region_name == Region.menu:
        return True
    for connection in connections_in_slot:
        if region_name == connection.destination:
            return True
    return False


def find_reachable_regions(regions_by_name, connections_by_name,
                           randomized_connections: Dict[ConnectionData, ConnectionData]):
    reachable_regions = {Region.menu}
    unreachable_regions = {region for region in regions_by_name.keys()}
    # unreachable_regions = {region for region in regions_by_name.keys() if region_should_be_reachable(region, connections_by_name.values())}
    unreachable_regions.remove(Region.menu)
    exits_to_explore = list(regions_by_name[Region.menu].exits)
    while exits_to_explore:
        exit_name = exits_to_explore.pop()
        # if exit_name not in connections_by_name:
        #     continue
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


def swap_one_random_connection(regions_by_name, connections_by_name, randomized_connections: Dict[ConnectionData, ConnectionData],
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

    swap_two_connections(chosen_reachable_entrance, chosen_unreachable_entrance, randomized_connections)


def swap_two_connections(entrance_1, entrance_2, randomized_connections):
    reachable_destination = randomized_connections[entrance_1]
    unreachable_destination = randomized_connections[entrance_2]
    randomized_connections[entrance_1] = unreachable_destination
    randomized_connections[entrance_2] = reachable_destination
