def dig_to_mines_floor(floor: int) -> str:
    return f"Dig to The Mines - Floor {floor}"


def dig_to_dangerous_mines_floor(floor: int) -> str:
    return f"Dig to the Dangerous Mines - Floor {floor}"


def dig_to_skull_floor(floor: int) -> str:
    return f"Mine to Skull Cavern Floor {floor}"


def move_to_woods_depth(depth: int) -> str:
    return f"Enter Deep Woods Depth {depth}"


class Entrance:
    to_stardew_valley = "To Stardew Valley"
    to_farmhouse = "To Farmhouse"
    farmhouse_to_farm = "Farmhouse to Farm"
    downstairs_to_cellar = "Farmhouse to Cellar"
    farm_to_backwoods = "Farm to Backwoods"
    farm_to_bus_stop = "Farm to Bus Stop"
    bus_stop_to_tunnel_entrance = "Bus Stop to Tunnel Entrance"
    tunnel_entrance_to_bus_tunnel = "Tunnel Entrance to Bus Tunnel"
    farm_to_forest = "Farm to Forest"
    farm_to_farmcave = "Farm to Farmcave"
    enter_greenhouse = "Farm to Greenhouse"
    enter_coop = "Farm to Coop"
    enter_barn = "Farm to Barn"
    enter_shed = "Farm to Shed"
    enter_slime_hutch = "Farm to Slime Hutch"
    use_desert_obelisk = "Use Desert Obelisk"
    use_island_obelisk = "Use Island Obelisk"
    use_farm_obelisk = "Use Farm Obelisk"
    backwoods_to_mountain = "Backwoods to Mountain"
    bus_stop_to_town = "Bus Stop to Town"
    take_bus_to_desert = "Bus Stop to Desert"
    forest_to_town = "Forest to Town"
    enter_secret_woods = "Forest to Secret Woods"
    forest_to_wizard_tower = "Forest to Wizard Tower"
    forest_to_marnie_ranch = "Forest to Marnie's Ranch"
    forest_to_leah_cottage = "Forest to Leah's Cottage"
    forest_to_sewer = "Forest to Sewer"
    forest_to_mastery_cave = "Forest to Mastery Cave"
    mountain_to_railroad = "Mountain to Railroad"
    mountain_to_tent = "Mountain to Tent"
    mountain_to_carpenter_shop = "Mountain to Carpenter Shop"
    mountain_to_maru_room = "Mountain to Maru's Room"
    mountain_to_the_mines = "Mountain to The Mines"
    enter_quarry = "Mountain to Quarry"
    mountain_to_adventurer_guild = "Mountain to Adventurer's Guild"
    adventurer_guild_to_bedroom = "Adventurer's Guild to Marlon's Bedroom"
    mountain_to_town = "Mountain to Town"
    town_to_community_center = "Town to Community Center"
    access_crafts_room = "Access Crafts Room"
    access_pantry = "Access Pantry"
    access_fish_tank = "Access Fish Tank"
    access_boiler_room = "Access Boiler Room"
    access_bulletin_board = "Access Bulletin Board"
    access_vault = "Access Vault"
    town_to_beach = "Town to Beach"
    town_to_hospital = "Town to Hospital"
    town_to_pierre_general_store = "Town to Pierre's General Store"
    town_to_saloon = "Town to Saloon"
    town_to_alex_house = "Town to Alex's House"
    town_to_trailer = "Town to Trailer"
    town_to_mayor_manor = "Town to Mayor's Manor"
    enter_lewis_bedroom = "Enter Lewis's Bedroom"
    enter_shorts_maze = "Mayor's Manor to Purple Shorts Maze"
    town_to_sam_house = "Town to Sam's House"
    town_to_haley_house = "Town to Haley's House"
    town_to_sewer = "Town to Sewer"
    town_to_clint_blacksmith = "Town to Clint's Blacksmith"
    town_to_museum = "Town to Museum"
    town_to_jojamart = "Town to JojaMart"
    purchase_movie_ticket = "Purchase Movie Ticket"
    enter_abandoned_jojamart = "Enter Abandoned Joja Mart"
    enter_movie_theater = "Enter Movie Theater"
    beach_to_willy_fish_shop = "Beach to Willy's Fish Shop"
    fish_shop_to_boat_tunnel = "Fish Shop to Boat Tunnel"
    boat_to_ginger_island = "Take the Boat to Ginger Island"
    enter_elliott_house = "Beach to Elliott's House"
    enter_tide_pools = "Beach to Tide Pools"
    enter_bathhouse_entrance = "Railroad to Bathhouse Entrance"
    enter_witch_warp_cave = "Railroad to Witch Warp Cave"
    enter_perfection_cutscene_area = "Railroad to Perfection Cutscene Area"
    enter_sebastian_room = "Carpenter Shop to Sebastian's Room"
    enter_harvey_room = "Hospital to Harvey's Room"
    enter_sunroom = "Pierre's General Store to Sunroom"
    enter_mutant_bug_lair = "Sewer to Mutant Bug Lair"
    enter_wizard_basement = "Wizard Tower to Wizard Basement"
    play_journey_of_the_prairie_king = "Play Journey of the Prairie King"
    reach_jotpk_world_2 = "Reach JotPK World 2"
    reach_jotpk_world_3 = "Reach JotPK World 3"
    play_junimo_kart = "Play Junimo Kart"
    reach_junimo_kart_2 = "Reach Junimo Kart 2"
    reach_junimo_kart_3 = "Reach Junimo Kart 3"
    reach_junimo_kart_4 = "Reach Junimo Kart 4"
    enter_mens_locker_room = "Bathhouse Entrance to Men's Locker Room"
    enter_womens_locker_room = "Bathhouse Entrance to Women's Locker Room"
    mens_lockers_to_public_bath = "Men's Locker Room to Public Bath"
    womens_lockers_to_public_bath = "Women's Locker Room to Public Bath"
    enter_witch_swamp = "Witch Warp Cave to Witch's Swamp"
    enter_witch_hut = "Witch's Swamp to Witch's Hut"
    witch_warp_to_wizard_basement = "Witch's Hut to Wizard Basement"
    enter_quarry_mine_entrance = "Quarry to Quarry Mine Entrance"
    enter_quarry_mine = "Quarry Mine Entrance to Quarry Mine"
    enter_oasis = "Desert to Oasis"
    enter_casino = "Oasis to Casino"
    enter_skull_cavern_entrance = "Desert to Skull Cavern Entrance"
    enter_skull_cavern = "Skull Cavern Entrance to Skull Cavern"
    mine_in_skull_cavern = "Can Mine in Skull Cavern"
    mine_to_skull_cavern_floor_25 = dig_to_skull_floor(25)
    mine_to_skull_cavern_floor_50 = dig_to_skull_floor(50)
    mine_to_skull_cavern_floor_75 = dig_to_skull_floor(75)
    mine_to_skull_cavern_floor_100 = dig_to_skull_floor(100)
    mine_to_skull_cavern_floor_125 = dig_to_skull_floor(125)
    mine_to_skull_cavern_floor_150 = dig_to_skull_floor(150)
    mine_to_skull_cavern_floor_175 = dig_to_skull_floor(175)
    mine_to_skull_cavern_floor_200 = dig_to_skull_floor(200)
    enter_dangerous_skull_cavern = "Enter the Dangerous Skull Cavern"
    dig_to_mines_floor_5 = dig_to_mines_floor(5)
    dig_to_mines_floor_10 = dig_to_mines_floor(10)
    dig_to_mines_floor_15 = dig_to_mines_floor(15)
    dig_to_mines_floor_20 = dig_to_mines_floor(20)
    dig_to_mines_floor_25 = dig_to_mines_floor(25)
    dig_to_mines_floor_30 = dig_to_mines_floor(30)
    dig_to_mines_floor_35 = dig_to_mines_floor(35)
    dig_to_mines_floor_40 = dig_to_mines_floor(40)
    dig_to_mines_floor_45 = dig_to_mines_floor(45)
    dig_to_mines_floor_50 = dig_to_mines_floor(50)
    dig_to_mines_floor_55 = dig_to_mines_floor(55)
    dig_to_mines_floor_60 = dig_to_mines_floor(60)
    dig_to_mines_floor_65 = dig_to_mines_floor(65)
    dig_to_mines_floor_70 = dig_to_mines_floor(70)
    dig_to_mines_floor_75 = dig_to_mines_floor(75)
    dig_to_mines_floor_80 = dig_to_mines_floor(80)
    dig_to_mines_floor_85 = dig_to_mines_floor(85)
    dig_to_mines_floor_90 = dig_to_mines_floor(90)
    dig_to_mines_floor_95 = dig_to_mines_floor(95)
    dig_to_mines_floor_100 = dig_to_mines_floor(100)
    dig_to_mines_floor_105 = dig_to_mines_floor(105)
    dig_to_mines_floor_110 = dig_to_mines_floor(110)
    dig_to_mines_floor_115 = dig_to_mines_floor(115)
    dig_to_mines_floor_120 = dig_to_mines_floor(120)
    dig_to_dangerous_mines_20 = dig_to_dangerous_mines_floor(20)
    dig_to_dangerous_mines_60 = dig_to_dangerous_mines_floor(60)
    dig_to_dangerous_mines_100 = dig_to_dangerous_mines_floor(100)
    island_south_to_west = "Island South to West"
    island_south_to_north = "Island South to North"
    island_south_to_east = "Island South to East"
    island_south_to_southeast = "Island South to Southeast"
    use_island_resort = "Use Island Resort"
    island_west_to_islandfarmhouse = "Island West to Island Farmhouse"
    island_west_to_gourmand_cave = "Island West to Gourmand Cave"
    island_west_to_crystals_cave = "Island West to Crystal Cave"
    island_west_to_shipwreck = "Island West to Shipwreck"
    island_west_to_qi_walnut_room = "Island West to Qi Walnut Room"
    island_east_to_leo_hut = "Island East to Leo Hut"
    mountain_to_leo_treehouse = "Mountain to Leo TreeHouse"
    island_east_to_island_shrine = "Island East to Island Shrine"
    island_southeast_to_pirate_cove = "Island Southeast to Pirate Cove"
    island_north_to_field_office = "Island North to Field Office"
    island_north_to_dig_site = "Island North to Dig Site"
    dig_site_to_professor_snail_cave = "Dig Site to Professor Snail Cave"
    island_north_to_volcano = "Island North to Volcano Entrance"
    volcano_to_secret_beach = "Volcano River to Secret Beach"
    talk_to_island_trader = "Talk to Island Trader"
    climb_to_volcano_5 = "Climb to Volcano Floor 5"
    talk_to_volcano_dwarf = "Talk to Volcano Dwarf"
    climb_to_volcano_10 = "Climb to Volcano Floor 10"
    parrot_express_docks_to_volcano = "Parrot Express Docks to Volcano"
    parrot_express_jungle_to_volcano = "Parrot Express Jungle to Volcano"
    parrot_express_dig_site_to_volcano = "Parrot Express Dig Site to Volcano"
    parrot_express_docks_to_dig_site = "Parrot Express Docks to Dig Site"
    parrot_express_jungle_to_dig_site = "Parrot Express Jungle to Dig Site"
    parrot_express_volcano_to_dig_site = "Parrot Express Volcano to Dig Site"
    parrot_express_docks_to_jungle = "Parrot Express Docks to Jungle"
    parrot_express_dig_site_to_jungle = "Parrot Express Dig Site to Jungle"
    parrot_express_volcano_to_jungle = "Parrot Express Volcano to Jungle"
    parrot_express_jungle_to_docks = "Parrot Express Jungle to Docks"
    parrot_express_dig_site_to_docks = "Parrot Express Dig Site to Docks"
    parrot_express_volcano_to_docks = "Parrot Express Volcano to Docks"
    mountain_to_outside_adventure_guild = "Mountain to Outside Adventure Guild"

    forest_beach_shortcut = "Forest to Beach Shortcut"
    mountain_jojamart_shortcut = "Mountain to Jojamart Shortcut"
    mountain_town_shortcut = "Mountain to Town Shortcut"
    town_tidepools_shortcut = "Town to Tide Pools Shortcut"
    tunnel_backwoods_shortcut = "Tunnel to Backwoods Shortcut"
    mountain_lake_to_outside_adventure_guild_shortcut = "Mountain Lake to Outside Adventure Guild"

    feed_trash_bear = "Feed Trash Bear"


class LogicEntrance:
    talk_to_mines_dwarf = "Talk to Mines Dwarf"

    buy_from_traveling_merchant = "Buy from Traveling Merchant"
    buy_from_traveling_merchant_sunday = "Buy from Traveling Merchant Sunday"
    buy_from_traveling_merchant_monday = "Buy from Traveling Merchant Monday"
    buy_from_traveling_merchant_tuesday = "Buy from Traveling Merchant Tuesday"
    buy_from_traveling_merchant_wednesday = "Buy from Traveling Merchant Wednesday"
    buy_from_traveling_merchant_thursday = "Buy from Traveling Merchant Thursday"
    buy_from_traveling_merchant_friday = "Buy from Traveling Merchant Friday"
    buy_from_traveling_merchant_saturday = "Buy from Traveling Merchant Saturday"
    farmhouse_cooking = "Farmhouse Cooking"
    island_cooking = "Island Cooking"
    shipping = "Use Shipping Bin"
    watch_queen_of_sauce = "Watch Queen of Sauce"

    @staticmethod
    def blacksmith_upgrade(material: str) -> str:
        return f"Upgrade {material} Tools"

    blacksmith_copper = blacksmith_upgrade("Copper")
    blacksmith_iron = blacksmith_upgrade("Iron")
    blacksmith_gold = blacksmith_upgrade("Gold")
    blacksmith_iridium = blacksmith_upgrade("Iridium")

    grow_spring_crops = "Grow Spring Crops"
    grow_summer_crops = "Grow Summer Crops"
    grow_fall_crops = "Grow Fall Crops"
    grow_winter_crops = "Grow Winter Crops"
    grow_spring_crops_in_greenhouse = "Grow Spring Crops in Greenhouse"
    grow_summer_crops_in_greenhouse = "Grow Summer Crops in Greenhouse"
    grow_fall_crops_in_greenhouse = "Grow Fall Crops in Greenhouse"
    grow_winter_crops_in_greenhouse = "Grow Winter Crops in Greenhouse"
    grow_indoor_crops_in_greenhouse = "Grow Indoor Crops in Greenhouse"
    grow_spring_crops_on_island = "Grow Spring Crops on Island"
    grow_summer_crops_on_island = "Grow Summer Crops on Island"
    grow_fall_crops_on_island = "Grow Fall Crops on Island"
    grow_winter_crops_on_island = "Grow Winter Crops on Island"
    grow_indoor_crops_on_island = "Grow Indoor Crops on Island"
    grow_summer_fall_crops_in_summer = "Grow Summer Fall Crops in Summer"
    grow_summer_fall_crops_in_fall = "Grow Summer Fall Crops in Fall"

    fishing = "Start Fishing"
    attend_egg_festival = "Attend Egg Festival"
    attend_desert_festival = "Attend Desert Festival"
    attend_flower_dance = "Attend Flower Dance"
    attend_luau = "Attend Luau"
    attend_trout_derby = "Attend Trout Derby"
    attend_moonlight_jellies = "Attend Dance of the Moonlight Jellies"
    attend_fair = "Attend Stardew Valley Fair"
    attend_spirit_eve = "Attend Spirit's Eve"
    attend_festival_of_ice = "Attend Festival of Ice"
    buy_from_hat_mouse = "Buy From Hat Mouse"
    buy_from_lost_items_shop = "Buy From Lost Items Shop"
    attend_night_market = "Attend Night Market"
    attend_winter_star = "Attend Feast of the Winter Star"
    attend_squidfest = "Attend SquidFest"
    buy_books = "Buy from the bookseller"
    buy_permanent_books = "Buy Permanent Books"
    buy_rare_books = "Buy Rare Books"
    buy_experience_books = "Buy Experience Books"
    has_giant_stump = "Has Giant Stump"
    can_complete_raccoon_requests_1 = "Can Complete Raccoon Request 1"
    can_complete_raccoon_requests_2 = "Can Complete Raccoon Request 2"
    can_complete_raccoon_requests_3 = "Can Complete Raccoon Request 3"
    can_complete_raccoon_requests_4 = "Can Complete Raccoon Request 4"
    can_complete_raccoon_requests_5 = "Can Complete Raccoon Request 5"
    can_complete_raccoon_requests_6 = "Can Complete Raccoon Request 6"
    can_complete_raccoon_requests_7 = "Can Complete Raccoon Request 7"
    can_complete_raccoon_requests_8 = "Can Complete Raccoon Request 8"
    buy_from_raccoon_1 = "Buy From Raccoon After 1 Request"
    buy_from_raccoon_2 = "Buy From Raccoon After 2 Requests"
    buy_from_raccoon_3 = "Buy From Raccoon After 3 Requests"
    buy_from_raccoon_4 = "Buy From Raccoon After 4 Requests"
    buy_from_raccoon_5 = "Buy From Raccoon After 5 Requests"
    buy_from_raccoon_6 = "Buy From Raccoon After 6 Requests"
    fish_in_waterfall = "Fish In Waterfall"
    find_secret_notes = "Find Secret Notes"
    search_garbage_cans = "Search Garbage Cans"
    purchase_wizard_blueprints = "Purchase Wizard Blueprints"


# Skull Cavern Elevator


class DeepWoodsEntrance:
    secret_woods_to_deep_woods = "Woods to Deep Woods"
    use_woods_obelisk = "Use Woods Obelisk"
    deep_woods_house = "Deep Woods to Deep Woods House"
    deep_woods_depth_1 = move_to_woods_depth(1)
    deep_woods_depth_10 = move_to_woods_depth(10)
    deep_woods_depth_20 = move_to_woods_depth(20)
    deep_woods_depth_30 = move_to_woods_depth(30)
    deep_woods_depth_40 = move_to_woods_depth(40)
    deep_woods_depth_50 = move_to_woods_depth(50)
    deep_woods_depth_60 = move_to_woods_depth(60)
    deep_woods_depth_70 = move_to_woods_depth(70)
    deep_woods_depth_80 = move_to_woods_depth(80)
    deep_woods_depth_90 = move_to_woods_depth(90)
    deep_woods_depth_100 = move_to_woods_depth(100)


class EugeneEntrance:
    forest_to_garden = "Forest to Eugene's Garden"
    garden_to_bedroom = "Eugene's Garden to Eugene's Bedroom"


class MagicEntrance:
    store_to_altar = "Pierre's General Store to Magic Altar"


class JasperEntrance:
    museum_to_bedroom = "Museum to Jasper's Bedroom"


class AlecEntrance:
    forest_to_petshop = "Forest to Alec's Pet Shop"
    petshop_to_bedroom = "Alec's Pet Shop to Alec's Bedroom"


class YobaEntrance:
    secret_woods_to_clearing = "Woods to Yoba's Clearing"


class JunaEntrance:
    forest_to_juna_cave = "Forest to Juna's Cave"


class AyeishaEntrance:
    bus_stop_to_mail_van = "Bus Stop to Ayeisha's Mail Van"


class RileyEntrance:
    town_to_riley = "Town to Riley's House"


class SVEEntrance:
    backwoods_to_grove = "Backwoods to Enchanted Grove"
    grove_to_outpost_warp = "Enchanted Grove to Grove Outpost Warp"
    outpost_warp_to_outpost = "Grove Outpost Warp to Galmoran Outpost"
    grove_to_wizard_warp = "Enchanted Grove to Grove Wizard Warp"
    wizard_warp_to_wizard = "Grove Wizard Warp to Wizard Basement"
    grove_to_aurora_warp = "Enchanted Grove to Grove Aurora Vineyard Warp"
    aurora_warp_to_aurora = "Grove Aurora Vineyard Warp to Aurora Vineyard Basement"
    grove_to_farm_warp = "Enchanted Grove to Grove Farm Warp"
    farm_warp_to_farm = "Grove Farm Warp to Farm"
    grove_to_guild_warp = "Enchanted Grove to Grove Guild Warp"
    guild_warp_to_guild = "Grove Guild Warp to Guild Summit"
    grove_to_junimo_warp = "Enchanted Grove to Grove Junimo Woods Warp"
    junimo_warp_to_junimo = "Grove Junimo Woods Warp to Junimo Woods"
    grove_to_spring_warp = "Enchanted Grove to Grove Sprite Spring Warp"
    spring_warp_to_spring = "Grove Sprite Spring Warp to Sprite Spring"
    wizard_to_fable_reef = "Wizard Basement to Fable Reef"
    bus_stop_to_shed = "Bus Stop to Grandpa's Shed"
    grandpa_shed_to_interior = "Grandpa's Shed to Grandpa's Shed Interior"
    grandpa_shed_to_town = "Grandpa's Shed to Town"
    grandpa_interior_to_upstairs = "Grandpa's Shed Interior to Grandpa's Shed Upstairs"
    forest_to_fairhaven = "Forest to Fairhaven Farm"
    forest_to_west = "Forest to Forest West"
    forest_to_lost_woods = "Forest to Lost Woods"
    lost_woods_to_junimo_woods = "Lost Woods to Junimo Woods"
    use_purple_junimo = "Talk to Purple Junimo"
    forest_to_bmv = "Forest to Blue Moon Vineyard"
    forest_to_marnie_shed = "Forest to Marnie's Shed"
    town_to_bmv = "Town to Blue Moon Vineyard"
    town_to_jenkins = "Town to Jenkins' Residence"
    town_to_bridge = "Town to Shearwater Bridge"
    town_to_plot = "Town to Unclaimed Plot"
    bmv_to_sophia = "Blue Moon Vineyard to Sophia's House"
    bmv_to_beach = "Blue Moon Vineyard to Beach"
    jenkins_to_cellar = "Jenkins' Residence to Jenkins' Cellar"
    plot_to_bridge = "Unclaimed Plot to Shearwater Bridge"
    mountain_to_guild_summit = "Mountain to Guild Summit"
    guild_to_interior = "Guild Summit to Adventurer's Guild"
    guild_to_mines = "Guild Summit to The Mines"
    summit_to_boat = "Guild Summit to Marlon's Boat"
    summit_to_highlands = "Guild Summit to Highlands Outside"
    to_aurora_basement = "Aurora Vineyard to Aurora Vineyard Basement"
    outpost_to_badlands_entrance = "Galmoran Outpost to Badlands Entrance"
    use_alesia_shop = "Talk to Alesia"
    use_isaac_shop = "Talk to Isaac"
    badlands_entrance_to_badlands = "Badlands Entrance to Crimson Badlands"
    badlands_to_cave = "Crimson Badlands to Badlands Cave"
    to_susan_house = "Railroad to Susan's House"
    enter_summit = "Railroad to Summit"
    fable_reef_to_guild = "Fable Reef to First Slash Guild"
    highlands_to_lance = "Highlands Outside to Lance's House Main"
    lance_to_ladder = "Lance's House Main to Lance's House Ladder"
    highlands_to_cave = "Highlands Outside to Highlands Cavern"
    to_dwarf_prison = "Highlands Cavern to Highlands Cavern Prison"
    lance_ladder_to_highlands = "Lance's House Ladder to Highlands Outside"
    forest_west_to_spring = "Forest West to Sprite Spring"
    west_to_aurora = "Forest West to Aurora Vineyard"
    use_bear_shop = "Talk to Bear Shop"
    secret_woods_to_west = "Secret Woods to Forest West"
    to_outpost_roof = "Galmoran Outpost to Galmoran Outpost Roof"
    railroad_to_grampleton_station = "Railroad to Grampleton Station"
    grampleton_station_to_grampleton_suburbs = "Grampleton Station to Grampleton Suburbs"
    grampleton_suburbs_to_scarlett_house = "Grampleton Suburbs to Scarlett's House"
    first_slash_guild_to_hallway = "First Slash Guild to First Slash Hallway"
    first_slash_hallway_to_room = "First Slash Hallway to First Slash Spare Room"
    sprite_spring_to_cave = "Sprite Spring to Sprite Spring Cave"
    fish_shop_to_willy_bedroom = "Willy's Fish Shop to Willy's Bedroom"
    museum_to_gunther_bedroom = "Museum to Gunther's Bedroom"
    highlands_to_pond = "Highlands to Highlands Pond"


class AlectoEntrance:
    witch_hut_to_witch_attic = "Witch's Hut to Witch's Attic"


class LaceyEntrance:
    forest_to_hat_house = "Forest to Mouse House"


class BoardingHouseEntrance:
    bus_stop_to_boarding_house_plateau = "Bus Stop to Boarding House Outside"
    boarding_house_plateau_to_boarding_house_first = "Boarding House Outside to Boarding House - First Floor"
    boarding_house_first_to_boarding_house_second = "Boarding House - First Floor to Boarding House - Second Floor"
    boarding_house_plateau_to_abandoned_mines_entrance = "Boarding House Outside to Abandoned Mines Entrance"
    abandoned_mines_entrance_to_abandoned_mines_1a = "Abandoned Mines Entrance to Abandoned Mines - 1A"
    abandoned_mines_1a_to_abandoned_mines_1b = "Abandoned Mines - 1A to Abandoned Mines - 1B"
    abandoned_mines_1b_to_abandoned_mines_2a = "Abandoned Mines - 1B to Abandoned Mines - 2A"
    abandoned_mines_2a_to_abandoned_mines_2b = "Abandoned Mines - 2A to Abandoned Mines - 2B"
    abandoned_mines_2b_to_abandoned_mines_3 = "Abandoned Mines - 2B to Abandoned Mines - 3"
    abandoned_mines_3_to_abandoned_mines_4 = "Abandoned Mines - 3 to Abandoned Mines - 4"
    abandoned_mines_4_to_abandoned_mines_5 = "Abandoned Mines - 4 to Abandoned Mines - 5"
    abandoned_mines_5_to_the_lost_valley = "Abandoned Mines - 5 to The Lost Valley"
    lost_valley_to_lost_valley_minecart = "The Lost Valley to Lost Valley Minecart"
    abandoned_mines_entrance_to_the_lost_valley = "Abandoned Mines Entrance to The Lost Valley"
    the_lost_valley_to_gregory_tent = "The Lost Valley to Gregory's Tent"
    the_lost_valley_to_lost_valley_ruins = "The Lost Valley to Lost Valley Ruins"
    lost_valley_ruins_to_lost_valley_house_1 = "Lost Valley Ruins to Lost Valley Ruins - First House"
    lost_valley_ruins_to_lost_valley_house_2 = "Lost Valley Ruins to Lost Valley Ruins - Second House"
    boarding_house_plateau_to_buffalo_ranch = "Boarding House Outside to Buffalo's Ranch"
