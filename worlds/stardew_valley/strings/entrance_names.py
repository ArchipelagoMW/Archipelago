from typing import final


def dig_to_mines_floor(floor: int) -> str:
    return f"Dig to The Mines - Floor {floor}"


def dig_to_dangerous_mines_floor(floor: int) -> str:
    return f"Dig to the Dangerous Mines - Floor {floor}"


def dig_to_skull_floor(floor: int) -> str:
    return f"Mine to Skull Cavern Floor {floor}"


def move_to_woods_depth(depth: int) -> str:
    return f"Enter Deep Woods Depth {depth}"


@final
class Entrance:
    to_stardew_valley = "To Stardew Valley"
    to_farm = "To Farm"
    farmhouse_to_farm = "Farmhouse to Farm"
    farm_to_farmhouse = "Farm to Farmhouse"
    downstairs_to_cellar = "Farmhouse to Cellar"
    cellar_to_downstairs = "Cellar to Farmhouse"
    farm_to_backwoods = "Farm to Backwoods"
    backwoods_to_farm = "Backwoods to Farm"
    farm_to_bus_stop = "Farm to Bus Stop"
    bus_stop_to_farm = "Bus Stop to Farm"
    bus_stop_to_tunnel_entrance = "Bus Stop to Tunnel Entrance"
    tunnel_entrance_to_bus_stop = "Tunnel Entrance to Bus Stop"
    tunnel_entrance_to_bus_tunnel = "Tunnel Entrance to Bus Tunnel"
    bus_tunnel_to_tunnel_entrance = "Bus Tunnel to Tunnel Entrance"
    farm_to_forest = "Farm to Forest"
    forest_to_farm = "Forest to Farm"
    farm_to_farmcave = "Farm to Farmcave"
    farmcave_to_farm = "Farmcave to Farm"
    enter_greenhouse = "Farm to Greenhouse"
    leave_greenhouse = "Greenhouse to Farm"
    enter_coop = "Farm to Coop"
    enter_barn = "Farm to Barn"
    enter_shed = "Farm to Shed"
    enter_slime_hutch = "Farm to Slime Hutch"
    use_earth_obelisk = "Use Earth Obelisk"
    use_water_obelisk = "Use Water Obelisk"
    use_desert_obelisk = "Use Desert Obelisk"
    use_island_obelisk = "Use Island Obelisk"
    use_farm_obelisk = "Use Farm Obelisk"
    backwoods_to_mountain = "Backwoods to Mountain"
    mountain_to_backwoods = "Mountain to Backwoods"
    bus_stop_to_town = "Bus Stop to Town"
    town_to_bus_stop = "Town to Bus Stop"
    take_bus_to_desert = "Bus Stop to Desert"
    take_bus_from_desert = "Desert to Bus Stop"
    forest_to_town = "Forest to Town"
    town_to_forest = "Town to Forest"
    enter_secret_woods = "Forest to Secret Woods"
    leave_secret_woods = "Secret Woods to Forest"
    forest_to_wizard_tower = "Forest to Wizard Tower"
    wizard_tower_to_forest = "Wizard Tower to Forest"
    forest_to_marnie_ranch = "Forest to Marnie's Ranch"
    marnie_ranch_to_forest = "Marnie's Ranch to Forest"
    forest_to_leah_cottage = "Forest to Leah's Cottage"
    leah_cottage_to_forest = "Leah's Cottage to Forest"
    forest_to_sewer = "Forest to Sewer"
    sewer_to_forest = "Sewer to Forest"
    forest_to_mastery_cave = "Forest to Mastery Cave"
    mastery_cave_to_forest = "Mastery Cave to Forest"
    mountain_to_railroad = "Mountain to Railroad"
    railroad_to_mountain = "Railroad to Mountain"
    mountain_to_tent = "Mountain to Tent"
    tent_to_mountain = "Tent to Mountain"
    mountain_to_carpenter_shop = "Mountain to Carpenter Shop"
    carpenter_shop_to_mountain = "Carpenter Shop to Mountain"
    mountain_to_maru_room = "Mountain to Maru's Room"
    maru_room_to_mountain = "Maru's Room to Mountain"
    carpenter_shop_to_maru_room = "Carpenter Shop to Maru's Room"
    maru_room_to_carpenter_shop = "Maru's Room to Carpenter Shop"
    mountain_to_the_mines = "Mountain to The Mines"
    the_mines_to_mountain = "The Mines to Mountain"
    mountain_to_adventurer_guild = "Mountain to Adventurer's Guild"
    adventurer_guild_to_mountain = "Adventurer's Guild to Mountain"
    mountain_to_town = "Mountain to Town"
    town_to_mountain = "Town to Mountain"
    enter_quarry = "Mountain to Quarry"
    leave_quarry = "Quarry to Mountain"
    adventurer_guild_to_bedroom = "Adventurer's Guild to Marlon's Bedroom"
    town_to_community_center = "Town to Community Center"
    community_center_to_town = "Community Center to Town"
    access_crafts_room = "Access Crafts Room"
    access_pantry = "Access Pantry"
    access_fish_tank = "Access Fish Tank"
    access_boiler_room = "Access Boiler Room"
    access_bulletin_board = "Access Bulletin Board"
    access_vault = "Access Vault"
    town_to_beach = "Town to Beach"
    beach_to_town = "Beach to Town"
    town_to_hospital = "Town to Hospital"
    hospital_to_town = "Hospital to Town"
    town_to_pierre_general_store = "Town to Pierre's General Store"
    pierre_general_store_to_town = "Pierre's General Store to Town"
    town_to_saloon = "Town to Saloon"
    saloon_to_town = "Saloon to Town"
    town_to_alex_house = "Town to Alex's House"
    alex_house_to_town = "Alex's House to Town"
    town_to_trailer = "Town to Trailer"
    trailer_to_town = "Trailer to Town"
    town_to_mayor_manor = "Town to Mayor's Manor"
    mayor_manor_to_town = "Mayor's Manor to Town"
    enter_lewis_bedroom = "Enter Lewis's Bedroom"
    leave_lewis_bedroom = "Leave Lewis's Bedroom"
    enter_shorts_maze = "Mayor's Manor to Purple Shorts Maze"
    leave_shorts_maze = "Purple Shorts Maze to Mayor's Manor"
    town_to_sam_house = "Town to Sam's House"
    sam_house_to_town = "Sam's House to Town"
    town_to_haley_house = "Town to Haley's House"
    haley_house_to_town = "Haley's House to Town"
    town_to_sewer = "Town to Sewer"
    sewer_to_town = "Sewer to Town"
    town_to_clint_blacksmith = "Town to Clint's Blacksmith"
    clint_blacksmith_to_town = "Clint's Blacksmith to Town"
    town_to_museum = "Town to Museum"
    museum_to_town = "Museum to Town"
    town_to_jojamart = "Town to JojaMart"
    jojamart_to_town = "JojaMart to Town"
    enter_abandoned_jojamart = "Enter Abandoned Joja Mart"
    enter_movie_theater = "Enter Movie Theater"
    beach_to_willy_fish_shop = "Beach to Willy's Fish Shop"
    willy_fish_shop_to_beach = "Willy's Fish Shop to Beach"
    fish_shop_to_boat_tunnel = "Fish Shop to Boat Tunnel"
    boat_tunnel_to_fish_shop = "Boat Tunnel to Fish Shop"
    boat_to_ginger_island = "Boat Tunnel to Island South"
    boat_from_ginger_island = "Island South to Boat Tunnel"
    enter_elliott_house = "Beach to Elliott's House"
    leave_elliott_house = "Elliott's House to Beach"
    enter_tide_pools = "Beach to Tide Pools"
    leave_tide_pools = "Tide Pools to Beach"
    enter_bathhouse_entrance = "Railroad to Bathhouse Entrance"
    leave_bathhouse_entrance = "Bathhouse Entrance to Railroad"
    enter_witch_warp_cave = "Railroad to Witch Warp Cave"
    leave_witch_warp_cave = "Witch Warp Cave to Railroad"
    enter_perfection_cutscene_area = "Railroad to Perfection Cutscene Area"
    leave_perfection_cutscene_area = "Perfection Cutscene Area to Railroad"
    enter_sebastian_room = "Carpenter Shop to Sebastian's Room"
    leave_sebastian_room = "Sebastian's Room to Carpenter Shop"
    enter_harvey_room = "Hospital to Harvey's Room"
    leave_harvey_room = "Harvey's Room to Hospital"
    enter_sunroom = "Pierre's General Store to Sunroom"
    leave_sunroom = "Sunroom to Pierre's General Store"
    enter_mutant_bug_lair = "Sewer to Mutant Bug Lair"
    leave_mutant_bug_lair = "Mutant Bug Lair to Sewer"
    enter_wizard_basement = "Wizard Tower to Wizard Basement"
    leave_wizard_basement = "Wizard Basement to Wizard Tower"
    play_journey_of_the_prairie_king = "Play Journey of the Prairie King"
    reach_jotpk_world_2 = "Reach JotPK World 2"
    reach_jotpk_world_3 = "Reach JotPK World 3"
    play_junimo_kart = "Play Junimo Kart"
    reach_junimo_kart_2 = "Reach Junimo Kart 2"
    reach_junimo_kart_3 = "Reach Junimo Kart 3"
    reach_junimo_kart_4 = "Reach Junimo Kart 4"
    enter_mens_locker_room = "Bathhouse Entrance to Men's Locker Room"
    leave_mens_locker_room = "Men's Locker Room to Bathhouse Entrance"
    enter_womens_locker_room = "Bathhouse Entrance to Women's Locker Room"
    leave_womens_locker_room = "Women's Locker Room to Bathhouse Entrance"
    mens_lockers_to_public_bath = "Men's Locker Room to Public Bath"
    public_bath_to_mens_lockers = "Public Bath to Men's Locker Room"
    womens_lockers_to_public_bath = "Women's Locker Room to Public Bath"
    public_bath_to_womens_lockers = "Public Bath to Women's Locker Room"
    enter_witch_swamp = "Witch Warp Cave to Witch's Swamp"
    leave_witch_swamp = "Witch's Swamp to Witch Warp Cave"
    enter_witch_hut = "Witch's Swamp to Witch's Hut"
    leave_witch_hut = "Witch's Hut to Witch's Swamp"
    witch_warp_to_wizard_basement = "Witch's Hut to Wizard Basement"
    wizard_basement_to_witch_warp = "Wizard Basement to Witch's Hut"
    enter_quarry_mine_entrance = "Quarry to Quarry Mine Entrance"
    leave_quarry_mine_entrance = "Quarry Mine Entrance to Quarry"
    enter_quarry_mine = "Quarry Mine Entrance to Quarry Mine"
    enter_oasis = "Desert to Oasis"
    leave_oasis = "Oasis to Desert"
    enter_casino = "Oasis to Casino"
    leave_casino = "Casino to Oasis"
    enter_skull_cavern_entrance = "Desert to Skull Cavern Entrance"
    leave_skull_cavern_entrance = "Skull Cavern Entrance to Desert"
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
    island_south_to_west = "Island South to Island West"
    island_west_to_south = "Island West to Island South"
    island_south_to_north = "Island South to Island North"
    island_north_to_south = "Island North to Island South"
    island_south_to_east = "Island South to Island East"
    island_east_to_south = "Island East to Island South"
    island_south_to_southeast = "Island South to Island Southeast"
    island_southeast_to_south = "Island Southeast to Island South"
    use_island_resort = "Use Island Resort"
    island_west_to_island_farmhouse = "Island West to Island Farmhouse"
    island_farmhouse_to_island_west = "Island Farmhouse to Island West"
    island_west_to_gourmand_cave = "Island West to Gourmand Cave"
    gourmand_cave_to_island_west = "Gourmand Cave to Island West"
    island_west_to_crystals_cave = "Island West to Crystal Cave"
    crystals_cave_to_island_west = "Crystal Cave to Island West"
    island_west_to_shipwreck = "Island West to Shipwreck"
    shipwreck_to_island_west = "Shipwreck to Island West"
    island_west_to_qi_walnut_room = "Island West to Qi Walnut Room"
    qi_walnut_room_to_island_west = "Qi Walnut Room to Island West"
    island_east_to_leo_hut = "Island East to Leo Hut"
    leo_hut_to_island_east = "Leo Hut to Island East"
    mountain_to_leo_treehouse = "Mountain to Leo TreeHouse"
    leo_treehouse_to_mountain = "Leo TreeHouse to Mountain"
    island_east_to_island_shrine = "Island East to Island Shrine"
    island_shrine_to_island_east = "Island Shrine to Island East"
    island_southeast_to_pirate_cove = "Island Southeast to Pirate Cove"
    pirate_cove_to_island_southeast = "Pirate Cove to Island Southeast"
    island_north_to_field_office = "Island North to Field Office"
    field_office_to_island_north = "Field Office to Island North"
    island_north_to_dig_site = "Island North to Dig Site"
    island_north_to_island_south_ridge = "Island North to Island South Ridge"
    island_south_ridge_to_island_north = "Island South Ridge to Island North"
    dig_site_to_island_north = "Dig Site to Island North"
    dig_site_to_professor_snail_cave = "Dig Site to Professor Snail Cave"
    professor_snail_cave_to_dig_site = "Professor Snail Cave to Dig Site"
    island_north_to_volcano = "Island North to Volcano Entrance"
    volcano_to_island_north = "Volcano Entrance to Island North"
    volcano_to_secret_beach = "Volcano River to Secret Beach"
    secret_beach_to_volcano = "Secret Beach to Volcano River"
    talk_to_island_trader = "Talk to Island Trader"
    climb_to_volcano_5 = "Climb to Volcano Floor 5"
    talk_to_volcano_dwarf = "Talk to Volcano Dwarf"
    volcano_5_to_island_north = "Volcano Floor 5 to Island North"
    climb_to_volcano_10 = "Climb to Volcano Floor 10"
    parrot_express_docks_to_volcano = "Parrot Express Docks to Parrot Express Volcano"
    parrot_express_jungle_to_volcano = "Parrot Express Jungle to Parrot Express Volcano"
    parrot_express_dig_site_to_volcano = "Parrot Express Dig Site to Parrot Express Volcano"
    parrot_express_farm_to_volcano = "Parrot Express Farm to Parrot Express Volcano"
    parrot_express_docks_to_dig_site = "Parrot Express Docks to Parrot Express Dig Site"
    parrot_express_jungle_to_dig_site = "Parrot Express Jungle to Parrot Express Dig Site"
    parrot_express_volcano_to_dig_site = "Parrot Express Volcano to Parrot Express Dig Site"
    parrot_express_farm_to_dig_site = "Parrot Express Farm to Parrot Express Dig Site"
    parrot_express_docks_to_jungle = "Parrot Express Docks to Parrot Express Jungle"
    parrot_express_dig_site_to_jungle = "Parrot Express Dig Site to Parrot Express Jungle"
    parrot_express_volcano_to_jungle = "Parrot Express Volcano to Parrot Express Jungle"
    parrot_express_farm_to_jungle = "Parrot Express Farm to Parrot Express Jungle"
    parrot_express_jungle_to_docks = "Parrot Express Jungle to Parrot Express Docks"
    parrot_express_dig_site_to_docks = "Parrot Express Dig Site to Parrot Express Docks"
    parrot_express_volcano_to_docks = "Parrot Express Volcano to Parrot Express Docks"
    parrot_express_farm_to_docks = "Parrot Express Farm to Parrot Express Docks"
    parrot_express_volcano_to_farm = "Parrot Express Volcano to Parrot Express Farm"
    parrot_express_dig_site_to_farm = "Parrot Express Dig Site to Parrot Express Farm"
    parrot_express_jungle_to_farm = "Parrot Express Jungle to Parrot Express Farm"
    parrot_express_docks_to_farm = "Parrot Express Docks to Parrot Express Farm"
    mountain_to_outside_adventure_guild = "Mountain to Outside Adventure Guild"
    outside_adventure_guild_to_mountain = "Outside Adventure Guild to Mountain"

    forest_beach_shortcut = "Forest Shortcut to Beach Shortcut"
    beach_forest_shortcut = "Beach Shortcut to Forest Shortcut"
    mountain_jojamart_shortcut = "Mountain Shortcut near Quarry Bridge to Town Shortcut through Cave"
    jojamart_mountain_shortcut = "Town Shortcut through Cave to Mountain Shortcut near Quarry Bridge"
    mountain_town_shortcut = "Mountain Shortcut at Fence to Town Shortcut at Fence"
    town_mountain_shortcut = "Town Shortcut at Fence to Mountain Shortcut at Fence"
    town_tidepools_shortcut = "Town Shortcut below Museum to Tide Pools Shortcut"
    tidepools_town_shortcut = "Tide Pools Shortcut to Town Shortcut below Museum"
    tunnel_backwoods_shortcut = "Tunnel Shortcut to Backwoods Shortcut"
    backwoods_tunnel_shortcut = "Backwoods Shortcut to Tunnel Shortcut"
    mountain_lake_to_outside_adventure_guild_shortcut = "Mountain Lake Shortcut to Outside Adventure Guild Shortcut"
    outside_adventure_guild_to_mountain_lake_shortcut = "Outside Adventure Guild Shortcut to Mountain Lake Shortcut"

    minecart_bus_stop_to_mines = "Minecart Bus Stop to Minecart Mines"
    minecart_bus_stop_to_quarry = "Minecart Bus Stop to Minecart Quarry"
    minecart_bus_stop_to_town = "Minecart Bus Stop to Minecart Town"
    minecart_mines_to_bus_stop = "Minecart Mines to Minecart Bus Stop"
    minecart_mines_to_quarry = "Minecart Mines to Minecart Quarry"
    minecart_mines_to_town = "Minecart Mines to Minecart Town"
    minecart_quarry_to_bus_stop = "Minecart Quarry to Minecart Bus Stop"
    minecart_quarry_to_mines = "Minecart Quarry to Minecart Mines"
    minecart_quarry_to_town = "Minecart Quarry to Minecart Town"
    minecart_town_to_bus_stop = "Minecart Town to Minecart Bus Stop"
    minecart_town_to_quarry = "Minecart Town to Minecart Quarry"
    minecart_town_to_mines = "Minecart Town to Minecart Mines"


@final
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
    island_shipping = "Use Island Shipping Bin"
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
    wearing_hats = "Wearing Hats"
    crafting = "Crafting"
    eating = "Eating"
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

    purchase_movie_ticket = "Purchase Movie Ticket"
    feed_trash_bear = "Feed Trash Bear"


# Skull Cavern Elevator


@final
class DeepWoodsEntrance:
    secret_woods_to_deep_woods = "Woods to Deep Woods"
    use_woods_obelisk = "Use Woods Obelisk"
    deep_woods_house = "Deep Woods to Deep Woods House"
    from_deep_woods_house = "Deep Woods House to Deep Woods"
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


@final
class EugeneEntrance:
    forest_to_garden = "Forest to Eugene's Garden"
    garden_to_forest = "Eugene's Garden to Forest"
    garden_to_bedroom = "Eugene's Garden to Eugene's Bedroom"
    bedroom_to_garden = "Eugene's Bedroom to Eugene's Garden"


@final
class MagicEntrance:
    store_to_altar = "Pierre's General Store to Magic Altar"


@final
class JasperEntrance:
    museum_to_bedroom = "Museum to Jasper's Bedroom"
    bedroom_to_museum = "Jasper's Bedroom to Museum"


@final
class AlecEntrance:
    forest_to_petshop = "Forest to Alec's Pet Shop"
    petshop_to_forest = "Alec's Pet Shop to Forest"
    petshop_to_bedroom = "Alec's Pet Shop to Alec's Bedroom"
    bedroom_to_petshop = "Alec's Bedroom to Alec's Pet Shop"


@final
class YobaEntrance:
    secret_woods_to_clearing = "Woods to Yoba's Clearing"
    clearing_to_secret_woods = "Yoba's Clearing to Woods"


@final
class JunaEntrance:
    forest_to_juna_cave = "Forest to Juna's Cave"
    juna_cave_to_forest = "Juna's Cave to Forest"


@final
class AyeishaEntrance:
    bus_stop_to_mail_van = "Bus Stop to Ayeisha's Mail Van"
    mail_van_to_bus_stop = "Ayeisha's Mail Van to Bus Stop"


@final
class RileyEntrance:
    town_to_riley = "Town to Riley's House"
    riley_to_town = "Riley's House to Town"


@final
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
    grandpa_upstairs_to_interior = "Grandpa's Shed Upstairs to Grandpa's Shed Interior"
    forest_to_fairhaven = "Forest to Fairhaven Farm"
    fairhaven_to_forest = "Fairhaven Farm to Forest"
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
    sophia_to_bmv = "Sophia's House to Blue Moon Vineyard"
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
    from_susan_house = "Susan's House to Railroad"
    enter_summit = "Railroad to Summit"
    leave_summit = "Summit to Railroad"
    fable_reef_to_guild = "Fable Reef to First Slash Guild"
    highlands_to_lance = "Highlands Outside to Lance's House Main"
    lance_to_highlands = "Lance's House Main to Highlands Outside"
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
    scarlett_house_to_grampleton_suburbs = "Scarlett's House to Grampleton Suburbs"
    first_slash_guild_to_hallway = "First Slash Guild to First Slash Hallway"
    first_slash_hallway_to_room = "First Slash Hallway to First Slash Spare Room"
    sprite_spring_to_cave = "Sprite Spring to Sprite Spring Cave"
    cave_to_sprite_spring = "Sprite Spring Cave to Sprite Spring"
    fish_shop_to_willy_bedroom = "Willy's Fish Shop to Willy's Bedroom"
    museum_to_gunther_bedroom = "Museum to Gunther's Bedroom"
    highlands_to_pond = "Highlands to Highlands Pond"


@final
class AlectoEntrance:
    witch_hut_to_witch_attic = "Witch's Hut to Witch's Attic"
    witch_attic_to_witch_hut = "Witch's Attic to Witch's Hut"


@final
class LaceyEntrance:
    forest_to_hat_house = "Forest to Mouse House"
    hat_house_to_forest = "Mouse House to Forest"


@final
class BoardingHouseEntrance:
    bus_stop_to_boarding_house_plateau = "Bus Stop to Boarding House Outside"
    boarding_house_plateau_to_boarding_house_first = "Boarding House Outside to Boarding House - First Floor"
    boarding_house_first_to_boarding_house_plateau = "Boarding House - First Floor to Boarding House Outside"
    boarding_house_first_to_boarding_house_second = "Boarding House - First Floor to Boarding House - Second Floor"
    boarding_house_second_to_boarding_house_first = "Boarding House - Second Floor to Boarding House - First Floor"
    boarding_house_plateau_to_abandoned_mines_entrance = "Boarding House Outside to Abandoned Mines Entrance"
    abandoned_mines_entrance_to_boarding_house_plateau = "Abandoned Mines Entrance to Boarding House Outside"
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
    buffalo_ranch_to_boarding_house_plateau = "Buffalo's Ranch to Boarding House Outside"
