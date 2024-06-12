import math
from typing import List

from BaseClasses import Entrance, MultiWorld, Region
from . import Options
from .Locations import DLCQuestLocation, location_table
from .Rules import create_event

DLCQuestRegion = ["Movement Pack", "Behind Tree", "Psychological Warfare", "Double Jump Left",
                  "Double Jump Behind the Tree", "The Forest", "Final Room"]


def add_coin_lfod(region: Region, coin: int, player: int):
    add_coin(region, coin, player, " coins freemium")


def add_coin_dlcquest(region: Region, coin: int, player: int):
    add_coin(region, coin, player, " coins")


def add_coin(region: Region, coin: int, player: int, suffix: str):
    number_coin = f"{coin}{suffix}"
    location_coin = f"{region.name}{suffix}"
    location = DLCQuestLocation(player, location_coin, None, region)
    region.locations.append(location)
    event = create_event(player, number_coin)
    event.coins = coin
    event.coin_suffix = suffix
    location.place_locked_item(event)


def create_regions(multiworld: MultiWorld, player: int, world_options: Options.DLCQuestOptions):
    region_menu = Region("Menu", player, multiworld)
    has_campaign_basic = world_options.campaign == Options.Campaign.option_basic or world_options.campaign == Options.Campaign.option_both
    has_campaign_lfod = world_options.campaign == Options.Campaign.option_live_freemium_or_die or world_options.campaign == Options.Campaign.option_both
    has_coinsanity = world_options.coinsanity == Options.CoinSanity.option_coin
    coin_bundle_size = world_options.coinbundlequantity.value
    has_item_shuffle = world_options.item_shuffle == Options.ItemShuffle.option_shuffled

    multiworld.regions.append(region_menu)

    create_regions_basic_campaign(has_campaign_basic, region_menu, has_item_shuffle, has_coinsanity, coin_bundle_size, player, multiworld)

    create_regions_lfod_campaign(coin_bundle_size, has_campaign_lfod, has_coinsanity, has_item_shuffle, multiworld, player, region_menu)


def create_regions_basic_campaign(has_campaign_basic: bool, region_menu: Region, has_item_shuffle: bool, has_coinsanity: bool,
                                  coin_bundle_size: int, player: int, world: MultiWorld):
    if not has_campaign_basic:
        return

    region_menu.exits += [Entrance(player, "DLC Quest Basic", region_menu)]
    locations_move_right = ["Movement Pack", "Animation Pack", "Audio Pack", "Pause Menu Pack"]
    region_move_right = create_region_and_locations_basic("Move Right", locations_move_right, ["Moving"], player, world, 4)
    create_coinsanity_locations_dlc_quest(has_coinsanity, coin_bundle_size, player, region_move_right)
    locations_movement_pack = ["Time is Money Pack", "Psychological Warfare Pack", "Armor for your Horse Pack", "Shepherd Sheep"]
    locations_movement_pack += conditional_location(has_item_shuffle, "Sword")
    create_region_and_locations_basic("Movement Pack", locations_movement_pack, ["Tree", "Cloud"], player, world, 46)
    locations_behind_tree = ["Double Jump Pack", "Map Pack", "Between Trees Sheep", "Hole in the Wall Sheep"] + conditional_location(has_item_shuffle, "Gun")
    create_region_and_locations_basic("Behind Tree", locations_behind_tree, ["Behind Tree Double Jump", "Forest Entrance"], player, world, 60)
    create_region_and_locations_basic("Psychological Warfare", ["West Cave Sheep"], ["Cloud Double Jump"], player, world, 100)
    locations_double_jump_left = ["Pet Pack", "Top Hat Pack", "North West Alcove Sheep"]
    create_region_and_locations_basic("Double Jump Total Left", locations_double_jump_left, ["Cave Tree", "Cave Roof"], player, world, 50)
    create_region_and_locations_basic("Double Jump Total Left Cave", ["Top Hat Sheep"], [], player, world, 9)
    create_region_and_locations_basic("Double Jump Total Left Roof", ["North West Ceiling Sheep"], [], player, world, 10)
    locations_double_jump_left_ceiling = ["Sexy Outfits Pack", "Double Jump Alcove Sheep", "Sexy Outfits Sheep"]
    create_region_and_locations_basic("Double Jump Behind Tree", locations_double_jump_left_ceiling, ["True Double Jump"], player, world, 89)
    create_region_and_locations_basic("True Double Jump Behind Tree", ["Double Jump Floating Sheep", "Cutscene Sheep"], [], player, world, 7)
    create_region_and_locations_basic("The Forest", ["Gun Pack", "Night Map Pack"], ["Behind Ogre", "Forest Double Jump"], player, world, 171)
    create_region_and_locations_basic("The Forest with double Jump", ["The Zombie Pack", "Forest Low Sheep"], ["Forest True Double Jump"], player, world, 76)
    create_region_and_locations_basic("The Forest with double Jump Part 2", ["Forest High Sheep"], [], player, world, 203)
    region_final_boss_room = create_region_and_locations_basic("The Final Boss Room", ["Finish the Fight Pack"], [], player, world)

    create_victory_event(region_final_boss_room, "Winning Basic", "Victory Basic", player)

    connect_entrances_basic(player, world)


def create_regions_lfod_campaign(coin_bundle_size, has_campaign_lfod, has_coinsanity, has_item_shuffle, multiworld, player, region_menu):
    if not has_campaign_lfod:
        return

    region_menu.exits += [Entrance(player, "Live Freemium or Die", region_menu)]
    locations_lfod_start = ["Particles Pack", "Day One Patch Pack", "Checkpoint Pack", "Incredibly Important Pack",
                            "Nice Try", "Story is Important", "I Get That Reference!"] + conditional_location(has_item_shuffle, "Wooden Sword")
    region_lfod_start = create_region_and_locations_lfod("Freemium Start", locations_lfod_start, ["Vines"], player, multiworld, 50)
    create_coinsanity_locations_lfod(has_coinsanity, coin_bundle_size, player, region_lfod_start)
    locations_behind_vines = ["Wall Jump Pack", "Health Bar Pack", "Parallax Pack"] + conditional_location(has_item_shuffle, "Pickaxe")
    create_region_and_locations_lfod("Behind the Vines", locations_behind_vines, ["Wall Jump Entrance"], player, multiworld, 95)
    locations_wall_jump = ["Harmless Plants Pack", "Death of Comedy Pack", "Canadian Dialog Pack", "DLC NPC Pack"]
    create_region_and_locations_lfod("Wall Jump", locations_wall_jump, ["Harmless Plants", "Pickaxe Hard Cave"], player, multiworld, 150)
    create_region_and_locations_lfod("Fake Ending", ["Cut Content Pack", "Name Change Pack"], ["Name Change Entrance", "Cut Content Entrance"], player,
                                     multiworld)
    create_region_and_locations_lfod("Hard Cave", [], ["Hard Cave Wall Jump"], player, multiworld, 20)
    create_region_and_locations_lfod("Hard Cave Wall Jump", ["Increased HP Pack"], [], player, multiworld, 130)
    create_region_and_locations_lfod("Cut Content", conditional_location(has_item_shuffle, "Humble Indie Bindle"), [], player, multiworld, 200)
    create_region_and_locations_lfod("Name Change", conditional_location(has_item_shuffle, "Box of Various Supplies"), ["Behind Rocks"], player, multiworld)
    create_region_and_locations_lfod("Top Right", ["Season Pass", "High Definition Next Gen Pack"], ["Blizzard"], player, multiworld, 90)
    create_region_and_locations_lfod("Season", ["Remove Ads Pack", "Not Exactly Noble"], ["Boss Door"], player, multiworld, 154)
    region_final_boss = create_region_and_locations_lfod("Final Boss", ["Big Sword Pack", "Really Big Sword Pack", "Unfathomable Sword Pack"], [], player, multiworld)

    create_victory_event(region_final_boss, "Winning Freemium", "Victory Freemium", player)

    connect_entrances_lfod(multiworld, player)


def conditional_location(condition: bool, location: str) -> List[str]:
    return conditional_locations(condition, [location])


def conditional_locations(condition: bool, locations: List[str]) -> List[str]:
    return locations if condition else []


def create_region_and_locations_basic(region_name: str, locations: List[str], exits: List[str], player: int, multiworld: MultiWorld,
                                      number_coins: int = 0) -> Region:
    return create_region_and_locations(region_name, locations, exits, player, multiworld, number_coins, 0)


def create_region_and_locations_lfod(region_name: str, locations: List[str], exits: List[str], player: int, multiworld: MultiWorld,
                                     number_coins: int = 0) -> Region:
    return create_region_and_locations(region_name, locations, exits, player, multiworld, 0, number_coins)


def create_region_and_locations(region_name: str, locations: List[str], exits: List[str], player: int, multiworld: MultiWorld,
                                number_coins_basic: int, number_coins_lfod: int) -> Region:
    region = Region(region_name, player, multiworld)
    region.exits = [Entrance(player, exit_name, region) for exit_name in exits]
    region.locations += [DLCQuestLocation(player, name, location_table[name], region) for name in locations]
    if number_coins_basic > 0:
        add_coin_dlcquest(region, number_coins_basic, player)
    if number_coins_lfod > 0:
        add_coin_lfod(region, number_coins_lfod, player)
    multiworld.regions.append(region)
    return region


def create_victory_event(region_victory: Region, event_name: str, item_name: str, player: int):
    location_victory = DLCQuestLocation(player, event_name, None, region_victory)
    region_victory.locations.append(location_victory)
    location_victory.place_locked_item(create_event(player, item_name))


def connect_entrances_basic(player, world):
    world.get_entrance("DLC Quest Basic", player).connect(world.get_region("Move Right", player))
    world.get_entrance("Moving", player).connect(world.get_region("Movement Pack", player))
    world.get_entrance("Tree", player).connect(world.get_region("Behind Tree", player))
    world.get_entrance("Cloud", player).connect(world.get_region("Psychological Warfare", player))
    world.get_entrance("Cloud Double Jump", player).connect(world.get_region("Double Jump Total Left", player))
    world.get_entrance("Cave Tree", player).connect(world.get_region("Double Jump Total Left Cave", player))
    world.get_entrance("Cave Roof", player).connect(world.get_region("Double Jump Total Left Roof", player))
    world.get_entrance("Forest Entrance", player).connect(world.get_region("The Forest", player))
    world.get_entrance("Behind Tree Double Jump", player).connect(world.get_region("Double Jump Behind Tree", player))
    world.get_entrance("Behind Ogre", player).connect(world.get_region("The Final Boss Room", player))
    world.get_entrance("Forest Double Jump", player).connect(world.get_region("The Forest with double Jump", player))
    world.get_entrance("Forest True Double Jump", player).connect(world.get_region("The Forest with double Jump Part 2", player))
    world.get_entrance("True Double Jump", player).connect(world.get_region("True Double Jump Behind Tree", player))


def connect_entrances_lfod(multiworld, player):
    multiworld.get_entrance("Live Freemium or Die", player).connect(multiworld.get_region("Freemium Start", player))
    multiworld.get_entrance("Vines", player).connect(multiworld.get_region("Behind the Vines", player))
    multiworld.get_entrance("Wall Jump Entrance", player).connect(multiworld.get_region("Wall Jump", player))
    multiworld.get_entrance("Harmless Plants", player).connect(multiworld.get_region("Fake Ending", player))
    multiworld.get_entrance("Pickaxe Hard Cave", player).connect(multiworld.get_region("Hard Cave", player))
    multiworld.get_entrance("Hard Cave Wall Jump", player).connect(multiworld.get_region("Hard Cave Wall Jump", player))
    multiworld.get_entrance("Name Change Entrance", player).connect(multiworld.get_region("Name Change", player))
    multiworld.get_entrance("Cut Content Entrance", player).connect(multiworld.get_region("Cut Content", player))
    multiworld.get_entrance("Behind Rocks", player).connect(multiworld.get_region("Top Right", player))
    multiworld.get_entrance("Blizzard", player).connect(multiworld.get_region("Season", player))
    multiworld.get_entrance("Boss Door", player).connect(multiworld.get_region("Final Boss", player))


def create_coinsanity_locations_dlc_quest(has_coinsanity: bool, coin_bundle_size: int, player: int, region_move_right: Region):
    create_coinsanity_locations(has_coinsanity, coin_bundle_size, player, region_move_right, 825, "DLC Quest")


def create_coinsanity_locations_lfod(has_coinsanity: bool, coin_bundle_size: int, player: int, region_lfod_start: Region):
    create_coinsanity_locations(has_coinsanity, coin_bundle_size, player, region_lfod_start, 889, "Live Freemium or Die")


def create_coinsanity_locations(has_coinsanity: bool, coin_bundle_size: int, player: int, region: Region, last_coin_number: int, campaign_prefix: str):
    if not has_coinsanity:
        return
    if coin_bundle_size == -1:
        create_coinsanity_piece_locations(player, region, last_coin_number, campaign_prefix)
        return


    coin_bundle_needed = math.ceil(last_coin_number / coin_bundle_size)
    for i in range(1, coin_bundle_needed + 1):
        number_coins = min(last_coin_number, coin_bundle_size * i)
        item_coin = f"{campaign_prefix}: {number_coins} Coin"
        region.locations += [DLCQuestLocation(player, item_coin, location_table[item_coin], region)]


def create_coinsanity_piece_locations(player: int, region: Region, total_coin: int, campaign_prefix:str):

    pieces_needed = total_coin * 10
    for i in range(1, pieces_needed + 1):
        number_piece = i
        item_piece = f"{campaign_prefix}: {number_piece} Coin Piece"
        region.locations += [DLCQuestLocation(player, item_piece, location_table[item_piece], region)]
