from random import Random
from typing import Iterable, Dict, Protocol, List, Tuple, Set

from BaseClasses import Region, Entrance
from .content import content_packs, StardewContent
from .mods.mod_regions import ModDataList, vanilla_connections_to_remove_by_mod
from .options import EntranceRandomization, ExcludeGingerIsland, StardewValleyOptions
from .region_classes import RegionData, ConnectionData, RandomizationFlag, ModificationFlag
from .strings.entrance_names import Entrance, LogicEntrance
from .strings.region_names import Region as RegionName, LogicRegion


class RegionFactory(Protocol):
    def __call__(self, name: str, regions: Iterable[str]) -> Region:
        raise NotImplementedError


vanilla_regions = [
    RegionData(RegionName.menu, [Entrance.to_stardew_valley]),
    RegionData(RegionName.stardew_valley, [Entrance.to_farmhouse]),
    RegionData(RegionName.farm_house,
               [Entrance.farmhouse_to_farm, Entrance.downstairs_to_cellar, LogicEntrance.farmhouse_cooking, LogicEntrance.watch_queen_of_sauce]),
    RegionData(RegionName.cellar),
    RegionData(RegionName.farm,
               [Entrance.farm_to_backwoods, Entrance.farm_to_bus_stop, Entrance.farm_to_forest, Entrance.farm_to_farmcave, Entrance.enter_greenhouse,
                Entrance.enter_coop, Entrance.enter_barn, Entrance.enter_shed, Entrance.enter_slime_hutch, LogicEntrance.grow_spring_crops,
                LogicEntrance.grow_summer_crops, LogicEntrance.grow_fall_crops, LogicEntrance.grow_winter_crops, LogicEntrance.shipping]),
    RegionData(RegionName.backwoods, [Entrance.backwoods_to_mountain]),
    RegionData(RegionName.bus_stop,
               [Entrance.bus_stop_to_town, Entrance.take_bus_to_desert, Entrance.bus_stop_to_tunnel_entrance]),
    RegionData(RegionName.forest,
               [Entrance.forest_to_town, Entrance.enter_secret_woods, Entrance.forest_to_wizard_tower, Entrance.forest_to_marnie_ranch,
                Entrance.forest_to_leah_cottage, Entrance.forest_to_sewer, Entrance.forest_to_mastery_cave, LogicEntrance.buy_from_traveling_merchant,
                LogicEntrance.complete_raccoon_requests, LogicEntrance.fish_in_waterfall, LogicEntrance.attend_flower_dance, LogicEntrance.attend_trout_derby,
                LogicEntrance.attend_festival_of_ice]),
    RegionData(LogicRegion.forest_waterfall),
    RegionData(RegionName.farm_cave),
    RegionData(RegionName.greenhouse,
               [LogicEntrance.grow_spring_crops_in_greenhouse, LogicEntrance.grow_summer_crops_in_greenhouse, LogicEntrance.grow_fall_crops_in_greenhouse,
                LogicEntrance.grow_winter_crops_in_greenhouse, LogicEntrance.grow_indoor_crops_in_greenhouse]),
    RegionData(RegionName.mountain,
               [Entrance.mountain_to_railroad, Entrance.mountain_to_tent, Entrance.mountain_to_carpenter_shop,
                Entrance.mountain_to_the_mines, Entrance.enter_quarry, Entrance.mountain_to_adventurer_guild,
                Entrance.mountain_to_town, Entrance.mountain_to_maru_room,
                Entrance.mountain_to_leo_treehouse]),
    RegionData(RegionName.leo_treehouse, is_ginger_island=True),
    RegionData(RegionName.maru_room),
    RegionData(RegionName.tunnel_entrance, [Entrance.tunnel_entrance_to_bus_tunnel]),
    RegionData(RegionName.bus_tunnel),
    RegionData(RegionName.town,
               [Entrance.town_to_community_center, Entrance.town_to_beach, Entrance.town_to_hospital, Entrance.town_to_pierre_general_store,
                Entrance.town_to_saloon, Entrance.town_to_alex_house, Entrance.town_to_trailer, Entrance.town_to_mayor_manor, Entrance.town_to_sam_house,
                Entrance.town_to_haley_house, Entrance.town_to_sewer, Entrance.town_to_clint_blacksmith, Entrance.town_to_museum, Entrance.town_to_jojamart,
                Entrance.purchase_movie_ticket, LogicEntrance.buy_experience_books, LogicEntrance.attend_egg_festival, LogicEntrance.attend_fair,
                LogicEntrance.attend_spirit_eve, LogicEntrance.attend_winter_star]),
    RegionData(RegionName.beach,
               [Entrance.beach_to_willy_fish_shop, Entrance.enter_elliott_house, Entrance.enter_tide_pools, LogicEntrance.fishing, LogicEntrance.attend_luau,
                LogicEntrance.attend_moonlight_jellies, LogicEntrance.attend_night_market, LogicEntrance.attend_squidfest]),
    RegionData(RegionName.railroad, [Entrance.enter_bathhouse_entrance, Entrance.enter_witch_warp_cave]),
    RegionData(RegionName.ranch),
    RegionData(RegionName.leah_house),
    RegionData(RegionName.mastery_cave),
    RegionData(RegionName.sewer, [Entrance.enter_mutant_bug_lair]),
    RegionData(RegionName.mutant_bug_lair),
    RegionData(RegionName.wizard_tower, [Entrance.enter_wizard_basement, Entrance.use_desert_obelisk, Entrance.use_island_obelisk]),
    RegionData(RegionName.wizard_basement),
    RegionData(RegionName.tent),
    RegionData(RegionName.carpenter, [Entrance.enter_sebastian_room]),
    RegionData(RegionName.sebastian_room),
    RegionData(RegionName.adventurer_guild, [Entrance.adventurer_guild_to_bedroom]),
    RegionData(RegionName.adventurer_guild_bedroom),
    RegionData(RegionName.community_center,
               [Entrance.access_crafts_room, Entrance.access_pantry, Entrance.access_fish_tank,
                Entrance.access_boiler_room, Entrance.access_bulletin_board, Entrance.access_vault]),
    RegionData(RegionName.crafts_room),
    RegionData(RegionName.pantry),
    RegionData(RegionName.fish_tank),
    RegionData(RegionName.boiler_room),
    RegionData(RegionName.bulletin_board),
    RegionData(RegionName.vault),
    RegionData(RegionName.hospital, [Entrance.enter_harvey_room]),
    RegionData(RegionName.harvey_room),
    RegionData(RegionName.pierre_store, [Entrance.enter_sunroom]),
    RegionData(RegionName.sunroom),
    RegionData(RegionName.saloon, [Entrance.play_journey_of_the_prairie_king, Entrance.play_junimo_kart]),
    RegionData(RegionName.jotpk_world_1, [Entrance.reach_jotpk_world_2]),
    RegionData(RegionName.jotpk_world_2, [Entrance.reach_jotpk_world_3]),
    RegionData(RegionName.jotpk_world_3),
    RegionData(RegionName.junimo_kart_1, [Entrance.reach_junimo_kart_2]),
    RegionData(RegionName.junimo_kart_2, [Entrance.reach_junimo_kart_3]),
    RegionData(RegionName.junimo_kart_3, [Entrance.reach_junimo_kart_4]),
    RegionData(RegionName.junimo_kart_4),
    RegionData(RegionName.alex_house),
    RegionData(RegionName.trailer),
    RegionData(RegionName.mayor_house),
    RegionData(RegionName.sam_house),
    RegionData(RegionName.haley_house),
    RegionData(RegionName.blacksmith, [LogicEntrance.blacksmith_copper]),
    RegionData(RegionName.museum),
    RegionData(RegionName.jojamart, [Entrance.enter_abandoned_jojamart]),
    RegionData(RegionName.abandoned_jojamart, [Entrance.enter_movie_theater]),
    RegionData(RegionName.movie_ticket_stand),
    RegionData(RegionName.movie_theater),
    RegionData(RegionName.fish_shop, [Entrance.fish_shop_to_boat_tunnel]),
    RegionData(RegionName.boat_tunnel, [Entrance.boat_to_ginger_island], is_ginger_island=True),
    RegionData(RegionName.elliott_house),
    RegionData(RegionName.tide_pools),
    RegionData(RegionName.bathhouse_entrance, [Entrance.enter_locker_room]),
    RegionData(RegionName.locker_room, [Entrance.enter_public_bath]),
    RegionData(RegionName.public_bath),
    RegionData(RegionName.witch_warp_cave, [Entrance.enter_witch_swamp]),
    RegionData(RegionName.witch_swamp, [Entrance.enter_witch_hut]),
    RegionData(RegionName.witch_hut, [Entrance.witch_warp_to_wizard_basement]),
    RegionData(RegionName.quarry, [Entrance.enter_quarry_mine_entrance]),
    RegionData(RegionName.quarry_mine_entrance, [Entrance.enter_quarry_mine]),
    RegionData(RegionName.quarry_mine),
    RegionData(RegionName.secret_woods),
    RegionData(RegionName.desert, [Entrance.enter_skull_cavern_entrance, Entrance.enter_oasis, LogicEntrance.attend_desert_festival]),
    RegionData(RegionName.oasis, [Entrance.enter_casino]),
    RegionData(RegionName.casino),
    RegionData(RegionName.skull_cavern_entrance, [Entrance.enter_skull_cavern]),
    RegionData(RegionName.skull_cavern, [Entrance.mine_to_skull_cavern_floor_25]),
    RegionData(RegionName.skull_cavern_25, [Entrance.mine_to_skull_cavern_floor_50]),
    RegionData(RegionName.skull_cavern_50, [Entrance.mine_to_skull_cavern_floor_75]),
    RegionData(RegionName.skull_cavern_75, [Entrance.mine_to_skull_cavern_floor_100]),
    RegionData(RegionName.skull_cavern_100, [Entrance.mine_to_skull_cavern_floor_125]),
    RegionData(RegionName.skull_cavern_125, [Entrance.mine_to_skull_cavern_floor_150]),
    RegionData(RegionName.skull_cavern_150, [Entrance.mine_to_skull_cavern_floor_175]),
    RegionData(RegionName.skull_cavern_175, [Entrance.mine_to_skull_cavern_floor_200]),
    RegionData(RegionName.skull_cavern_200, [Entrance.enter_dangerous_skull_cavern]),
    RegionData(RegionName.dangerous_skull_cavern, is_ginger_island=True),
    RegionData(RegionName.island_south,
               [Entrance.island_south_to_west, Entrance.island_south_to_north, Entrance.island_south_to_east, Entrance.island_south_to_southeast,
                Entrance.use_island_resort, Entrance.parrot_express_docks_to_volcano, Entrance.parrot_express_docks_to_dig_site,
                Entrance.parrot_express_docks_to_jungle],
               is_ginger_island=True),
    RegionData(RegionName.island_resort, is_ginger_island=True),
    RegionData(RegionName.island_west,
               [Entrance.island_west_to_islandfarmhouse, Entrance.island_west_to_gourmand_cave, Entrance.island_west_to_crystals_cave,
                Entrance.island_west_to_shipwreck, Entrance.island_west_to_qi_walnut_room, Entrance.use_farm_obelisk, Entrance.parrot_express_jungle_to_docks,
                Entrance.parrot_express_jungle_to_dig_site, Entrance.parrot_express_jungle_to_volcano, LogicEntrance.grow_spring_crops_on_island,
                LogicEntrance.grow_summer_crops_on_island, LogicEntrance.grow_fall_crops_on_island, LogicEntrance.grow_winter_crops_on_island,
                LogicEntrance.grow_indoor_crops_on_island],
               is_ginger_island=True),
    RegionData(RegionName.island_east, [Entrance.island_east_to_leo_hut, Entrance.island_east_to_island_shrine], is_ginger_island=True),
    RegionData(RegionName.island_shrine, is_ginger_island=True),
    RegionData(RegionName.island_south_east, [Entrance.island_southeast_to_pirate_cove], is_ginger_island=True),
    RegionData(RegionName.island_north,
               [Entrance.talk_to_island_trader, Entrance.island_north_to_field_office, Entrance.island_north_to_dig_site, Entrance.island_north_to_volcano,
                Entrance.parrot_express_volcano_to_dig_site, Entrance.parrot_express_volcano_to_jungle, Entrance.parrot_express_volcano_to_docks],
               is_ginger_island=True),
    RegionData(RegionName.volcano, [Entrance.climb_to_volcano_5, Entrance.volcano_to_secret_beach], is_ginger_island=True),
    RegionData(RegionName.volcano_secret_beach, is_ginger_island=True),
    RegionData(RegionName.volcano_floor_5, [Entrance.talk_to_volcano_dwarf, Entrance.climb_to_volcano_10], is_ginger_island=True),
    RegionData(RegionName.volcano_dwarf_shop, is_ginger_island=True),
    RegionData(RegionName.volcano_floor_10, is_ginger_island=True),
    RegionData(RegionName.island_trader, is_ginger_island=True),
    RegionData(RegionName.island_farmhouse, [LogicEntrance.island_cooking], is_ginger_island=True),
    RegionData(RegionName.gourmand_frog_cave, is_ginger_island=True),
    RegionData(RegionName.colored_crystals_cave, is_ginger_island=True),
    RegionData(RegionName.shipwreck, is_ginger_island=True),
    RegionData(RegionName.qi_walnut_room, is_ginger_island=True),
    RegionData(RegionName.leo_hut, is_ginger_island=True),
    RegionData(RegionName.pirate_cove, is_ginger_island=True),
    RegionData(RegionName.field_office, is_ginger_island=True),
    RegionData(RegionName.dig_site,
               [Entrance.dig_site_to_professor_snail_cave, Entrance.parrot_express_dig_site_to_volcano,
                Entrance.parrot_express_dig_site_to_docks, Entrance.parrot_express_dig_site_to_jungle],
               is_ginger_island=True),
    RegionData(RegionName.professor_snail_cave, is_ginger_island=True),
    RegionData(RegionName.coop),
    RegionData(RegionName.barn),
    RegionData(RegionName.shed),
    RegionData(RegionName.slime_hutch),

    RegionData(RegionName.mines, [LogicEntrance.talk_to_mines_dwarf,
                                  Entrance.dig_to_mines_floor_5]),
    RegionData(RegionName.mines_floor_5, [Entrance.dig_to_mines_floor_10]),
    RegionData(RegionName.mines_floor_10, [Entrance.dig_to_mines_floor_15]),
    RegionData(RegionName.mines_floor_15, [Entrance.dig_to_mines_floor_20]),
    RegionData(RegionName.mines_floor_20, [Entrance.dig_to_mines_floor_25]),
    RegionData(RegionName.mines_floor_25, [Entrance.dig_to_mines_floor_30]),
    RegionData(RegionName.mines_floor_30, [Entrance.dig_to_mines_floor_35]),
    RegionData(RegionName.mines_floor_35, [Entrance.dig_to_mines_floor_40]),
    RegionData(RegionName.mines_floor_40, [Entrance.dig_to_mines_floor_45]),
    RegionData(RegionName.mines_floor_45, [Entrance.dig_to_mines_floor_50]),
    RegionData(RegionName.mines_floor_50, [Entrance.dig_to_mines_floor_55]),
    RegionData(RegionName.mines_floor_55, [Entrance.dig_to_mines_floor_60]),
    RegionData(RegionName.mines_floor_60, [Entrance.dig_to_mines_floor_65]),
    RegionData(RegionName.mines_floor_65, [Entrance.dig_to_mines_floor_70]),
    RegionData(RegionName.mines_floor_70, [Entrance.dig_to_mines_floor_75]),
    RegionData(RegionName.mines_floor_75, [Entrance.dig_to_mines_floor_80]),
    RegionData(RegionName.mines_floor_80, [Entrance.dig_to_mines_floor_85]),
    RegionData(RegionName.mines_floor_85, [Entrance.dig_to_mines_floor_90]),
    RegionData(RegionName.mines_floor_90, [Entrance.dig_to_mines_floor_95]),
    RegionData(RegionName.mines_floor_95, [Entrance.dig_to_mines_floor_100]),
    RegionData(RegionName.mines_floor_100, [Entrance.dig_to_mines_floor_105]),
    RegionData(RegionName.mines_floor_105, [Entrance.dig_to_mines_floor_110]),
    RegionData(RegionName.mines_floor_110, [Entrance.dig_to_mines_floor_115]),
    RegionData(RegionName.mines_floor_115, [Entrance.dig_to_mines_floor_120]),
    RegionData(RegionName.mines_floor_120, [Entrance.dig_to_dangerous_mines_20, Entrance.dig_to_dangerous_mines_60, Entrance.dig_to_dangerous_mines_100]),
    RegionData(RegionName.dangerous_mines_20, is_ginger_island=True),
    RegionData(RegionName.dangerous_mines_60, is_ginger_island=True),
    RegionData(RegionName.dangerous_mines_100, is_ginger_island=True),

    RegionData(LogicRegion.mines_dwarf_shop),
    RegionData(LogicRegion.blacksmith_copper, [LogicEntrance.blacksmith_iron]),
    RegionData(LogicRegion.blacksmith_iron, [LogicEntrance.blacksmith_gold]),
    RegionData(LogicRegion.blacksmith_gold, [LogicEntrance.blacksmith_iridium]),
    RegionData(LogicRegion.blacksmith_iridium),
    RegionData(LogicRegion.kitchen),
    RegionData(LogicRegion.queen_of_sauce),
    RegionData(LogicRegion.fishing),

    RegionData(LogicRegion.spring_farming),
    RegionData(LogicRegion.summer_farming, [LogicEntrance.grow_summer_fall_crops_in_summer]),
    RegionData(LogicRegion.fall_farming, [LogicEntrance.grow_summer_fall_crops_in_fall]),
    RegionData(LogicRegion.winter_farming),
    RegionData(LogicRegion.summer_or_fall_farming),
    RegionData(LogicRegion.indoor_farming),

    RegionData(LogicRegion.shipping),
    RegionData(LogicRegion.traveling_cart, [LogicEntrance.buy_from_traveling_merchant_sunday,
                                            LogicEntrance.buy_from_traveling_merchant_monday,
                                            LogicEntrance.buy_from_traveling_merchant_tuesday,
                                            LogicEntrance.buy_from_traveling_merchant_wednesday,
                                            LogicEntrance.buy_from_traveling_merchant_thursday,
                                            LogicEntrance.buy_from_traveling_merchant_friday,
                                            LogicEntrance.buy_from_traveling_merchant_saturday]),
    RegionData(LogicRegion.traveling_cart_sunday),
    RegionData(LogicRegion.traveling_cart_monday),
    RegionData(LogicRegion.traveling_cart_tuesday),
    RegionData(LogicRegion.traveling_cart_wednesday),
    RegionData(LogicRegion.traveling_cart_thursday),
    RegionData(LogicRegion.traveling_cart_friday),
    RegionData(LogicRegion.traveling_cart_saturday),
    RegionData(LogicRegion.raccoon_daddy, [LogicEntrance.buy_from_raccoon]),
    RegionData(LogicRegion.raccoon_shop),

    RegionData(LogicRegion.egg_festival),
    RegionData(LogicRegion.desert_festival),
    RegionData(LogicRegion.flower_dance),
    RegionData(LogicRegion.luau),
    RegionData(LogicRegion.trout_derby),
    RegionData(LogicRegion.moonlight_jellies),
    RegionData(LogicRegion.fair),
    RegionData(LogicRegion.spirit_eve),
    RegionData(LogicRegion.festival_of_ice),
    RegionData(LogicRegion.night_market),
    RegionData(LogicRegion.winter_star),
    RegionData(LogicRegion.squidfest),
    RegionData(LogicRegion.bookseller_1, [LogicEntrance.buy_year1_books]),
    RegionData(LogicRegion.bookseller_2, [LogicEntrance.buy_year3_books]),
    RegionData(LogicRegion.bookseller_3),
]

# Exists and where they lead
vanilla_connections = [
    ConnectionData(Entrance.to_stardew_valley, RegionName.stardew_valley),
    ConnectionData(Entrance.to_farmhouse, RegionName.farm_house),
    ConnectionData(Entrance.farmhouse_to_farm, RegionName.farm),
    ConnectionData(Entrance.downstairs_to_cellar, RegionName.cellar),
    ConnectionData(Entrance.farm_to_backwoods, RegionName.backwoods),
    ConnectionData(Entrance.farm_to_bus_stop, RegionName.bus_stop),
    ConnectionData(Entrance.farm_to_forest, RegionName.forest),
    ConnectionData(Entrance.farm_to_farmcave, RegionName.farm_cave, flag=RandomizationFlag.NON_PROGRESSION),
    ConnectionData(Entrance.enter_greenhouse, RegionName.greenhouse),
    ConnectionData(Entrance.enter_coop, RegionName.coop),
    ConnectionData(Entrance.enter_barn, RegionName.barn),
    ConnectionData(Entrance.enter_shed, RegionName.shed),
    ConnectionData(Entrance.enter_slime_hutch, RegionName.slime_hutch),
    ConnectionData(Entrance.use_desert_obelisk, RegionName.desert),
    ConnectionData(Entrance.use_island_obelisk, RegionName.island_south, flag=RandomizationFlag.GINGER_ISLAND),
    ConnectionData(Entrance.use_farm_obelisk, RegionName.farm),
    ConnectionData(Entrance.backwoods_to_mountain, RegionName.mountain),
    ConnectionData(Entrance.bus_stop_to_town, RegionName.town),
    ConnectionData(Entrance.bus_stop_to_tunnel_entrance, RegionName.tunnel_entrance),
    ConnectionData(Entrance.tunnel_entrance_to_bus_tunnel, RegionName.bus_tunnel, flag=RandomizationFlag.NON_PROGRESSION),
    ConnectionData(Entrance.take_bus_to_desert, RegionName.desert),
    ConnectionData(Entrance.forest_to_town, RegionName.town),
    ConnectionData(Entrance.forest_to_wizard_tower, RegionName.wizard_tower,
                   flag=RandomizationFlag.NON_PROGRESSION | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(Entrance.enter_wizard_basement, RegionName.wizard_basement, flag=RandomizationFlag.BUILDINGS),
    ConnectionData(Entrance.forest_to_marnie_ranch, RegionName.ranch,
                   flag=RandomizationFlag.NON_PROGRESSION | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(Entrance.forest_to_leah_cottage, RegionName.leah_house,
                   flag=RandomizationFlag.BUILDINGS | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(Entrance.enter_secret_woods, RegionName.secret_woods),
    ConnectionData(Entrance.forest_to_sewer, RegionName.sewer, flag=RandomizationFlag.BUILDINGS),
    ConnectionData(Entrance.forest_to_mastery_cave, RegionName.mastery_cave, flag=RandomizationFlag.BUILDINGS | RandomizationFlag.MASTERIES),
    ConnectionData(Entrance.town_to_sewer, RegionName.sewer, flag=RandomizationFlag.BUILDINGS),
    ConnectionData(Entrance.enter_mutant_bug_lair, RegionName.mutant_bug_lair, flag=RandomizationFlag.BUILDINGS),
    ConnectionData(Entrance.mountain_to_railroad, RegionName.railroad),
    ConnectionData(Entrance.mountain_to_tent, RegionName.tent,
                   flag=RandomizationFlag.NON_PROGRESSION | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(Entrance.mountain_to_leo_treehouse, RegionName.leo_treehouse,
                   flag=RandomizationFlag.BUILDINGS | RandomizationFlag.LEAD_TO_OPEN_AREA | RandomizationFlag.GINGER_ISLAND),
    ConnectionData(Entrance.mountain_to_carpenter_shop, RegionName.carpenter,
                   flag=RandomizationFlag.NON_PROGRESSION | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(Entrance.mountain_to_maru_room, RegionName.maru_room,
                   flag=RandomizationFlag.BUILDINGS | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(Entrance.enter_sebastian_room, RegionName.sebastian_room, flag=RandomizationFlag.BUILDINGS),
    ConnectionData(Entrance.mountain_to_adventurer_guild, RegionName.adventurer_guild,
                   flag=RandomizationFlag.BUILDINGS | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(Entrance.adventurer_guild_to_bedroom, RegionName.adventurer_guild_bedroom),
    ConnectionData(Entrance.enter_quarry, RegionName.quarry),
    ConnectionData(Entrance.enter_quarry_mine_entrance, RegionName.quarry_mine_entrance,
                   flag=RandomizationFlag.BUILDINGS),
    ConnectionData(Entrance.enter_quarry_mine, RegionName.quarry_mine),
    ConnectionData(Entrance.mountain_to_town, RegionName.town),
    ConnectionData(Entrance.town_to_community_center, RegionName.community_center,
                   flag=RandomizationFlag.PELICAN_TOWN | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(Entrance.access_crafts_room, RegionName.crafts_room),
    ConnectionData(Entrance.access_pantry, RegionName.pantry),
    ConnectionData(Entrance.access_fish_tank, RegionName.fish_tank),
    ConnectionData(Entrance.access_boiler_room, RegionName.boiler_room),
    ConnectionData(Entrance.access_bulletin_board, RegionName.bulletin_board),
    ConnectionData(Entrance.access_vault, RegionName.vault),
    ConnectionData(Entrance.town_to_hospital, RegionName.hospital,
                   flag=RandomizationFlag.PELICAN_TOWN | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(Entrance.enter_harvey_room, RegionName.harvey_room, flag=RandomizationFlag.BUILDINGS),
    ConnectionData(Entrance.town_to_pierre_general_store, RegionName.pierre_store,
                   flag=RandomizationFlag.PELICAN_TOWN | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(Entrance.enter_sunroom, RegionName.sunroom, flag=RandomizationFlag.BUILDINGS),
    ConnectionData(Entrance.town_to_clint_blacksmith, RegionName.blacksmith,
                   flag=RandomizationFlag.PELICAN_TOWN | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(Entrance.town_to_saloon, RegionName.saloon,
                   flag=RandomizationFlag.PELICAN_TOWN | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(Entrance.play_journey_of_the_prairie_king, RegionName.jotpk_world_1),
    ConnectionData(Entrance.reach_jotpk_world_2, RegionName.jotpk_world_2),
    ConnectionData(Entrance.reach_jotpk_world_3, RegionName.jotpk_world_3),
    ConnectionData(Entrance.play_junimo_kart, RegionName.junimo_kart_1),
    ConnectionData(Entrance.reach_junimo_kart_2, RegionName.junimo_kart_2),
    ConnectionData(Entrance.reach_junimo_kart_3, RegionName.junimo_kart_3),
    ConnectionData(Entrance.reach_junimo_kart_4, RegionName.junimo_kart_4),
    ConnectionData(Entrance.town_to_sam_house, RegionName.sam_house,
                   flag=RandomizationFlag.PELICAN_TOWN | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(Entrance.town_to_haley_house, RegionName.haley_house,
                   flag=RandomizationFlag.PELICAN_TOWN | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(Entrance.town_to_mayor_manor, RegionName.mayor_house,
                   flag=RandomizationFlag.PELICAN_TOWN | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(Entrance.town_to_alex_house, RegionName.alex_house,
                   flag=RandomizationFlag.PELICAN_TOWN | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(Entrance.town_to_trailer, RegionName.trailer,
                   flag=RandomizationFlag.PELICAN_TOWN | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(Entrance.town_to_museum, RegionName.museum,
                   flag=RandomizationFlag.PELICAN_TOWN | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(Entrance.town_to_jojamart, RegionName.jojamart,
                   flag=RandomizationFlag.PELICAN_TOWN | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(Entrance.purchase_movie_ticket, RegionName.movie_ticket_stand),
    ConnectionData(Entrance.enter_abandoned_jojamart, RegionName.abandoned_jojamart),
    ConnectionData(Entrance.enter_movie_theater, RegionName.movie_theater),
    ConnectionData(Entrance.town_to_beach, RegionName.beach),
    ConnectionData(Entrance.enter_elliott_house, RegionName.elliott_house,
                   flag=RandomizationFlag.BUILDINGS | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(Entrance.beach_to_willy_fish_shop, RegionName.fish_shop,
                   flag=RandomizationFlag.NON_PROGRESSION | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(Entrance.fish_shop_to_boat_tunnel, RegionName.boat_tunnel,
                   flag=RandomizationFlag.BUILDINGS | RandomizationFlag.GINGER_ISLAND),
    ConnectionData(Entrance.boat_to_ginger_island, RegionName.island_south, flag=RandomizationFlag.GINGER_ISLAND),
    ConnectionData(Entrance.enter_tide_pools, RegionName.tide_pools),
    ConnectionData(Entrance.mountain_to_the_mines, RegionName.mines,
                   flag=RandomizationFlag.NON_PROGRESSION | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(Entrance.dig_to_mines_floor_5, RegionName.mines_floor_5),
    ConnectionData(Entrance.dig_to_mines_floor_10, RegionName.mines_floor_10),
    ConnectionData(Entrance.dig_to_mines_floor_15, RegionName.mines_floor_15),
    ConnectionData(Entrance.dig_to_mines_floor_20, RegionName.mines_floor_20),
    ConnectionData(Entrance.dig_to_mines_floor_25, RegionName.mines_floor_25),
    ConnectionData(Entrance.dig_to_mines_floor_30, RegionName.mines_floor_30),
    ConnectionData(Entrance.dig_to_mines_floor_35, RegionName.mines_floor_35),
    ConnectionData(Entrance.dig_to_mines_floor_40, RegionName.mines_floor_40),
    ConnectionData(Entrance.dig_to_mines_floor_45, RegionName.mines_floor_45),
    ConnectionData(Entrance.dig_to_mines_floor_50, RegionName.mines_floor_50),
    ConnectionData(Entrance.dig_to_mines_floor_55, RegionName.mines_floor_55),
    ConnectionData(Entrance.dig_to_mines_floor_60, RegionName.mines_floor_60),
    ConnectionData(Entrance.dig_to_mines_floor_65, RegionName.mines_floor_65),
    ConnectionData(Entrance.dig_to_mines_floor_70, RegionName.mines_floor_70),
    ConnectionData(Entrance.dig_to_mines_floor_75, RegionName.mines_floor_75),
    ConnectionData(Entrance.dig_to_mines_floor_80, RegionName.mines_floor_80),
    ConnectionData(Entrance.dig_to_mines_floor_85, RegionName.mines_floor_85),
    ConnectionData(Entrance.dig_to_mines_floor_90, RegionName.mines_floor_90),
    ConnectionData(Entrance.dig_to_mines_floor_95, RegionName.mines_floor_95),
    ConnectionData(Entrance.dig_to_mines_floor_100, RegionName.mines_floor_100),
    ConnectionData(Entrance.dig_to_mines_floor_105, RegionName.mines_floor_105),
    ConnectionData(Entrance.dig_to_mines_floor_110, RegionName.mines_floor_110),
    ConnectionData(Entrance.dig_to_mines_floor_115, RegionName.mines_floor_115),
    ConnectionData(Entrance.dig_to_mines_floor_120, RegionName.mines_floor_120),
    ConnectionData(Entrance.dig_to_dangerous_mines_20, RegionName.dangerous_mines_20, flag=RandomizationFlag.GINGER_ISLAND),
    ConnectionData(Entrance.dig_to_dangerous_mines_60, RegionName.dangerous_mines_60, flag=RandomizationFlag.GINGER_ISLAND),
    ConnectionData(Entrance.dig_to_dangerous_mines_100, RegionName.dangerous_mines_100, flag=RandomizationFlag.GINGER_ISLAND),
    ConnectionData(Entrance.enter_skull_cavern_entrance, RegionName.skull_cavern_entrance,
                   flag=RandomizationFlag.BUILDINGS | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(Entrance.enter_oasis, RegionName.oasis,
                   flag=RandomizationFlag.BUILDINGS | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(Entrance.enter_casino, RegionName.casino, flag=RandomizationFlag.BUILDINGS),
    ConnectionData(Entrance.enter_skull_cavern, RegionName.skull_cavern),
    ConnectionData(Entrance.mine_to_skull_cavern_floor_25, RegionName.skull_cavern_25),
    ConnectionData(Entrance.mine_to_skull_cavern_floor_50, RegionName.skull_cavern_50),
    ConnectionData(Entrance.mine_to_skull_cavern_floor_75, RegionName.skull_cavern_75),
    ConnectionData(Entrance.mine_to_skull_cavern_floor_100, RegionName.skull_cavern_100),
    ConnectionData(Entrance.mine_to_skull_cavern_floor_125, RegionName.skull_cavern_125),
    ConnectionData(Entrance.mine_to_skull_cavern_floor_150, RegionName.skull_cavern_150),
    ConnectionData(Entrance.mine_to_skull_cavern_floor_175, RegionName.skull_cavern_175),
    ConnectionData(Entrance.mine_to_skull_cavern_floor_200, RegionName.skull_cavern_200),
    ConnectionData(Entrance.enter_dangerous_skull_cavern, RegionName.dangerous_skull_cavern, flag=RandomizationFlag.GINGER_ISLAND),
    ConnectionData(Entrance.enter_witch_warp_cave, RegionName.witch_warp_cave, flag=RandomizationFlag.BUILDINGS),
    ConnectionData(Entrance.enter_witch_swamp, RegionName.witch_swamp, flag=RandomizationFlag.BUILDINGS),
    ConnectionData(Entrance.enter_witch_hut, RegionName.witch_hut, flag=RandomizationFlag.BUILDINGS),
    ConnectionData(Entrance.witch_warp_to_wizard_basement, RegionName.wizard_basement, flag=RandomizationFlag.BUILDINGS),
    ConnectionData(Entrance.enter_bathhouse_entrance, RegionName.bathhouse_entrance,
                   flag=RandomizationFlag.BUILDINGS | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(Entrance.enter_locker_room, RegionName.locker_room, flag=RandomizationFlag.BUILDINGS),
    ConnectionData(Entrance.enter_public_bath, RegionName.public_bath, flag=RandomizationFlag.BUILDINGS),
    ConnectionData(Entrance.island_south_to_west, RegionName.island_west, flag=RandomizationFlag.GINGER_ISLAND),
    ConnectionData(Entrance.island_south_to_north, RegionName.island_north, flag=RandomizationFlag.GINGER_ISLAND),
    ConnectionData(Entrance.island_south_to_east, RegionName.island_east, flag=RandomizationFlag.GINGER_ISLAND),
    ConnectionData(Entrance.island_south_to_southeast, RegionName.island_south_east,
                   flag=RandomizationFlag.GINGER_ISLAND),
    ConnectionData(Entrance.use_island_resort, RegionName.island_resort, flag=RandomizationFlag.GINGER_ISLAND),
    ConnectionData(Entrance.island_west_to_islandfarmhouse, RegionName.island_farmhouse,
                   flag=RandomizationFlag.BUILDINGS | RandomizationFlag.GINGER_ISLAND),
    ConnectionData(Entrance.island_west_to_gourmand_cave, RegionName.gourmand_frog_cave,
                   flag=RandomizationFlag.BUILDINGS | RandomizationFlag.GINGER_ISLAND),
    ConnectionData(Entrance.island_west_to_crystals_cave, RegionName.colored_crystals_cave,
                   flag=RandomizationFlag.BUILDINGS | RandomizationFlag.GINGER_ISLAND),
    ConnectionData(Entrance.island_west_to_shipwreck, RegionName.shipwreck,
                   flag=RandomizationFlag.BUILDINGS | RandomizationFlag.GINGER_ISLAND),
    ConnectionData(Entrance.island_west_to_qi_walnut_room, RegionName.qi_walnut_room, flag=RandomizationFlag.BUILDINGS | RandomizationFlag.GINGER_ISLAND),
    ConnectionData(Entrance.island_east_to_leo_hut, RegionName.leo_hut,
                   flag=RandomizationFlag.BUILDINGS | RandomizationFlag.GINGER_ISLAND),
    ConnectionData(Entrance.island_east_to_island_shrine, RegionName.island_shrine,
                   flag=RandomizationFlag.BUILDINGS | RandomizationFlag.GINGER_ISLAND),
    ConnectionData(Entrance.island_southeast_to_pirate_cove, RegionName.pirate_cove,
                   flag=RandomizationFlag.BUILDINGS | RandomizationFlag.GINGER_ISLAND),
    ConnectionData(Entrance.island_north_to_field_office, RegionName.field_office,
                   flag=RandomizationFlag.BUILDINGS | RandomizationFlag.GINGER_ISLAND),
    ConnectionData(Entrance.island_north_to_dig_site, RegionName.dig_site, flag=RandomizationFlag.GINGER_ISLAND),
    ConnectionData(Entrance.dig_site_to_professor_snail_cave, RegionName.professor_snail_cave,
                   flag=RandomizationFlag.BUILDINGS | RandomizationFlag.GINGER_ISLAND),
    ConnectionData(Entrance.island_north_to_volcano, RegionName.volcano,
                   flag=RandomizationFlag.BUILDINGS | RandomizationFlag.GINGER_ISLAND),
    ConnectionData(Entrance.volcano_to_secret_beach, RegionName.volcano_secret_beach,
                   flag=RandomizationFlag.BUILDINGS | RandomizationFlag.GINGER_ISLAND),
    ConnectionData(Entrance.talk_to_island_trader, RegionName.island_trader, flag=RandomizationFlag.GINGER_ISLAND),
    ConnectionData(Entrance.climb_to_volcano_5, RegionName.volcano_floor_5, flag=RandomizationFlag.GINGER_ISLAND),
    ConnectionData(Entrance.talk_to_volcano_dwarf, RegionName.volcano_dwarf_shop, flag=RandomizationFlag.GINGER_ISLAND),
    ConnectionData(Entrance.climb_to_volcano_10, RegionName.volcano_floor_10, flag=RandomizationFlag.GINGER_ISLAND),
    ConnectionData(Entrance.parrot_express_jungle_to_docks, RegionName.island_south, flag=RandomizationFlag.GINGER_ISLAND),
    ConnectionData(Entrance.parrot_express_dig_site_to_docks, RegionName.island_south, flag=RandomizationFlag.GINGER_ISLAND),
    ConnectionData(Entrance.parrot_express_volcano_to_docks, RegionName.island_south, flag=RandomizationFlag.GINGER_ISLAND),
    ConnectionData(Entrance.parrot_express_volcano_to_jungle, RegionName.island_west, flag=RandomizationFlag.GINGER_ISLAND),
    ConnectionData(Entrance.parrot_express_docks_to_jungle, RegionName.island_west, flag=RandomizationFlag.GINGER_ISLAND),
    ConnectionData(Entrance.parrot_express_dig_site_to_jungle, RegionName.island_west, flag=RandomizationFlag.GINGER_ISLAND),
    ConnectionData(Entrance.parrot_express_docks_to_dig_site, RegionName.dig_site, flag=RandomizationFlag.GINGER_ISLAND),
    ConnectionData(Entrance.parrot_express_volcano_to_dig_site, RegionName.dig_site, flag=RandomizationFlag.GINGER_ISLAND),
    ConnectionData(Entrance.parrot_express_jungle_to_dig_site, RegionName.dig_site, flag=RandomizationFlag.GINGER_ISLAND),
    ConnectionData(Entrance.parrot_express_dig_site_to_volcano, RegionName.island_north, flag=RandomizationFlag.GINGER_ISLAND),
    ConnectionData(Entrance.parrot_express_docks_to_volcano, RegionName.island_north, flag=RandomizationFlag.GINGER_ISLAND),
    ConnectionData(Entrance.parrot_express_jungle_to_volcano, RegionName.island_north, flag=RandomizationFlag.GINGER_ISLAND),

    ConnectionData(LogicEntrance.talk_to_mines_dwarf, LogicRegion.mines_dwarf_shop),

    ConnectionData(LogicEntrance.buy_from_traveling_merchant, LogicRegion.traveling_cart),
    ConnectionData(LogicEntrance.buy_from_traveling_merchant_sunday, LogicRegion.traveling_cart_sunday),
    ConnectionData(LogicEntrance.buy_from_traveling_merchant_monday, LogicRegion.traveling_cart_monday),
    ConnectionData(LogicEntrance.buy_from_traveling_merchant_tuesday, LogicRegion.traveling_cart_tuesday),
    ConnectionData(LogicEntrance.buy_from_traveling_merchant_wednesday, LogicRegion.traveling_cart_wednesday),
    ConnectionData(LogicEntrance.buy_from_traveling_merchant_thursday, LogicRegion.traveling_cart_thursday),
    ConnectionData(LogicEntrance.buy_from_traveling_merchant_friday, LogicRegion.traveling_cart_friday),
    ConnectionData(LogicEntrance.buy_from_traveling_merchant_saturday, LogicRegion.traveling_cart_saturday),
    ConnectionData(LogicEntrance.complete_raccoon_requests, LogicRegion.raccoon_daddy),
    ConnectionData(LogicEntrance.fish_in_waterfall, LogicRegion.forest_waterfall),
    ConnectionData(LogicEntrance.buy_from_raccoon, LogicRegion.raccoon_shop),
    ConnectionData(LogicEntrance.farmhouse_cooking, LogicRegion.kitchen),
    ConnectionData(LogicEntrance.watch_queen_of_sauce, LogicRegion.queen_of_sauce),

    ConnectionData(LogicEntrance.grow_spring_crops, LogicRegion.spring_farming),
    ConnectionData(LogicEntrance.grow_summer_crops, LogicRegion.summer_farming),
    ConnectionData(LogicEntrance.grow_fall_crops, LogicRegion.fall_farming),
    ConnectionData(LogicEntrance.grow_winter_crops, LogicRegion.winter_farming),
    ConnectionData(LogicEntrance.grow_spring_crops_in_greenhouse, LogicRegion.spring_farming),
    ConnectionData(LogicEntrance.grow_summer_crops_in_greenhouse, LogicRegion.summer_farming),
    ConnectionData(LogicEntrance.grow_fall_crops_in_greenhouse, LogicRegion.fall_farming),
    ConnectionData(LogicEntrance.grow_winter_crops_in_greenhouse, LogicRegion.winter_farming),
    ConnectionData(LogicEntrance.grow_indoor_crops_in_greenhouse, LogicRegion.indoor_farming),
    ConnectionData(LogicEntrance.grow_spring_crops_on_island, LogicRegion.spring_farming, flag=RandomizationFlag.GINGER_ISLAND),
    ConnectionData(LogicEntrance.grow_summer_crops_on_island, LogicRegion.summer_farming, flag=RandomizationFlag.GINGER_ISLAND),
    ConnectionData(LogicEntrance.grow_fall_crops_on_island, LogicRegion.fall_farming, flag=RandomizationFlag.GINGER_ISLAND),
    ConnectionData(LogicEntrance.grow_winter_crops_on_island, LogicRegion.winter_farming, flag=RandomizationFlag.GINGER_ISLAND),
    ConnectionData(LogicEntrance.grow_indoor_crops_on_island, LogicRegion.indoor_farming, flag=RandomizationFlag.GINGER_ISLAND),
    ConnectionData(LogicEntrance.grow_summer_fall_crops_in_summer, LogicRegion.summer_or_fall_farming),
    ConnectionData(LogicEntrance.grow_summer_fall_crops_in_fall, LogicRegion.summer_or_fall_farming),

    ConnectionData(LogicEntrance.shipping, LogicRegion.shipping),
    ConnectionData(LogicEntrance.blacksmith_copper, LogicRegion.blacksmith_copper),
    ConnectionData(LogicEntrance.blacksmith_iron, LogicRegion.blacksmith_iron),
    ConnectionData(LogicEntrance.blacksmith_gold, LogicRegion.blacksmith_gold),
    ConnectionData(LogicEntrance.blacksmith_iridium, LogicRegion.blacksmith_iridium),
    ConnectionData(LogicEntrance.fishing, LogicRegion.fishing),
    ConnectionData(LogicEntrance.island_cooking, LogicRegion.kitchen),
    ConnectionData(LogicEntrance.attend_egg_festival, LogicRegion.egg_festival),
    ConnectionData(LogicEntrance.attend_desert_festival, LogicRegion.desert_festival),
    ConnectionData(LogicEntrance.attend_flower_dance, LogicRegion.flower_dance),
    ConnectionData(LogicEntrance.attend_luau, LogicRegion.luau),
    ConnectionData(LogicEntrance.attend_trout_derby, LogicRegion.trout_derby),
    ConnectionData(LogicEntrance.attend_moonlight_jellies, LogicRegion.moonlight_jellies),
    ConnectionData(LogicEntrance.attend_fair, LogicRegion.fair),
    ConnectionData(LogicEntrance.attend_spirit_eve, LogicRegion.spirit_eve),
    ConnectionData(LogicEntrance.attend_festival_of_ice, LogicRegion.festival_of_ice),
    ConnectionData(LogicEntrance.attend_night_market, LogicRegion.night_market),
    ConnectionData(LogicEntrance.attend_winter_star, LogicRegion.winter_star),
    ConnectionData(LogicEntrance.attend_squidfest, LogicRegion.squidfest),
    ConnectionData(LogicEntrance.buy_experience_books, LogicRegion.bookseller_1),
    ConnectionData(LogicEntrance.buy_year1_books, LogicRegion.bookseller_2),
    ConnectionData(LogicEntrance.buy_year3_books, LogicRegion.bookseller_3),
]


def create_final_regions(world_options) -> List[RegionData]:
    final_regions = []
    final_regions.extend(vanilla_regions)
    if world_options.mods is None:
        return final_regions
    for mod in sorted(world_options.mods.value):
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
    connections = modify_connections_for_mods(connections, sorted(world_options.mods.value))
    include_island = world_options.exclude_ginger_island == ExcludeGingerIsland.option_false
    return remove_ginger_island_regions_and_connections(regions_data, connections, include_island)


def remove_ginger_island_regions_and_connections(regions_by_name: Dict[str, RegionData], connections: Dict[str, ConnectionData], include_island: bool):
    if include_island:
        return connections, regions_by_name

    removed_connections = set()

    for connection_name in tuple(connections):
        connection = connections[connection_name]
        if connection.flag & RandomizationFlag.GINGER_ISLAND:
            connections.pop(connection_name)
            removed_connections.add(connection_name)

    for region_name in tuple(regions_by_name):
        region = regions_by_name[region_name]
        if region.is_ginger_island:
            regions_by_name.pop(region_name)
        else:
            regions_by_name[region_name] = region.get_without_exits(removed_connections)

    return connections, regions_by_name


def modify_connections_for_mods(connections: Dict[str, ConnectionData], mods: Iterable) -> Dict[str, ConnectionData]:
    for mod in mods:
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


def create_regions(region_factory: RegionFactory, random: Random, world_options: StardewValleyOptions, content: StardewContent) \
        -> Tuple[Dict[str, Region], Dict[str, Entrance], Dict[str, str]]:
    entrances_data, regions_data = create_final_connections_and_regions(world_options)
    regions_by_name: Dict[str: Region] = {region_name: region_factory(region_name, regions_data[region_name].exits) for region_name in regions_data}
    entrances_by_name: Dict[str: Entrance] = {
        entrance.name: entrance
        for region in regions_by_name.values()
        for entrance in region.exits
        if entrance.name in entrances_data
    }

    connections, randomized_data = randomize_connections(random, world_options, content, regions_data, entrances_data)

    for connection in connections:
        if connection.name in entrances_by_name:
            entrances_by_name[connection.name].connect(regions_by_name[connection.destination])
    return regions_by_name, entrances_by_name, randomized_data


def randomize_connections(random: Random, world_options: StardewValleyOptions, content: StardewContent, regions_by_name: Dict[str, RegionData],
                          connections_by_name: Dict[str, ConnectionData]) -> Tuple[List[ConnectionData], Dict[str, str]]:
    connections_to_randomize: List[ConnectionData] = []
    if world_options.entrance_randomization == EntranceRandomization.option_pelican_town:
        connections_to_randomize = [connections_by_name[connection] for connection in connections_by_name if
                                    RandomizationFlag.PELICAN_TOWN in connections_by_name[connection].flag]
    elif world_options.entrance_randomization == EntranceRandomization.option_non_progression:
        connections_to_randomize = [connections_by_name[connection] for connection in connections_by_name if
                                    RandomizationFlag.NON_PROGRESSION in connections_by_name[connection].flag]
    elif world_options.entrance_randomization == EntranceRandomization.option_buildings or world_options.entrance_randomization == EntranceRandomization.option_buildings_without_house:
        connections_to_randomize = [connections_by_name[connection] for connection in connections_by_name if
                                    RandomizationFlag.BUILDINGS in connections_by_name[connection].flag]
    elif world_options.entrance_randomization == EntranceRandomization.option_chaos:
        connections_to_randomize = [connections_by_name[connection] for connection in connections_by_name if
                                    RandomizationFlag.BUILDINGS in connections_by_name[connection].flag]
        connections_to_randomize = remove_excluded_entrances(connections_to_randomize, content)

        # On Chaos, we just add the connections to randomize, unshuffled, and the client does it every day
        randomized_data_for_mod = {}
        for connection in connections_to_randomize:
            randomized_data_for_mod[connection.name] = connection.name
            randomized_data_for_mod[connection.reverse] = connection.reverse
        return list(connections_by_name.values()), randomized_data_for_mod

    connections_to_randomize = remove_excluded_entrances(connections_to_randomize, content)
    random.shuffle(connections_to_randomize)
    destination_pool = list(connections_to_randomize)
    random.shuffle(destination_pool)

    randomized_connections = randomize_chosen_connections(connections_to_randomize, destination_pool)
    add_non_randomized_connections(list(connections_by_name.values()), connections_to_randomize, randomized_connections)

    swap_connections_until_valid(regions_by_name, connections_by_name, randomized_connections, connections_to_randomize, random)
    randomized_connections_for_generation = create_connections_for_generation(randomized_connections)
    randomized_data_for_mod = create_data_for_mod(randomized_connections, connections_to_randomize)

    return randomized_connections_for_generation, randomized_data_for_mod


def remove_excluded_entrances(connections_to_randomize: List[ConnectionData], content: StardewContent) -> List[ConnectionData]:
    # FIXME remove when regions are handled in content packs
    if content_packs.ginger_island_content_pack.name not in content.registered_packs:
        connections_to_randomize = [connection for connection in connections_to_randomize if RandomizationFlag.GINGER_ISLAND not in connection.flag]
    if not content.features.skill_progression.are_masteries_shuffled:
        connections_to_randomize = [connection for connection in connections_to_randomize if RandomizationFlag.MASTERIES not in connection.flag]

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
    if region_name == RegionName.menu:
        return True
    for connection in connections_in_slot:
        if region_name == connection.destination:
            return True
    return False


def find_reachable_regions(regions_by_name, connections_by_name,
                           randomized_connections: Dict[ConnectionData, ConnectionData]):
    reachable_regions = {RegionName.menu}
    unreachable_regions = {region for region in regions_by_name.keys()}
    # unreachable_regions = {region for region in regions_by_name.keys() if region_should_be_reachable(region, connections_by_name.values())}
    unreachable_regions.remove(RegionName.menu)
    exits_to_explore = list(regions_by_name[RegionName.menu].exits)
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
    unreachable_regions_names_leading_somewhere = [region for region in sorted(unreachable_regions) if len(regions_by_name[region].exits) > 0]
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
