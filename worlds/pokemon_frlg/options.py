"""
Option definitions for Pokémon FireRed/LeafGreen
"""
from dataclasses import dataclass
from schema import And, Optional, Or, Schema
from Options import (Choice, DeathLink, DefaultOnToggle, NamedRange, OptionDict, OptionSet, PerGameCommonOptions, Range,
                     Toggle)
from .data import (data, ability_name_map, fly_blacklist_map, fly_plando_maps, move_name_map,
                   starting_town_blacklist_map, GAME_OPTIONS)


class GameVersion(Choice):
    """
    Select FireRed or LeafGreen version.
    """
    display_name = "Game Version"
    option_firered = 0
    option_leafgreen = 1
    default = "random"


class Goal(Choice):
    """
    Sets what your goal is to consider the game beaten.

    - Champion: Defeat the Champion
    - Champion Rematch: Defeat the Champion Rematch
    """
    display_name = "Goal"
    default = 0
    option_champion = 0
    option_champion_rematch = 1


class SkipEliteFour(Toggle):
    """
    Set whether to skip the Elite Four fights and go straight to the Champion fight when entering the Pokemon League.
    """
    display_name = "Skip Elite Four"


class KantoOnly(Toggle):
    """
    Excludes all the Sevii Island locations. Navel Rock and Birth Island are still included.
    HM06 Rock Smash, HM07 Waterfall, and the Sun Stone will still be in the item pool.
    The Move Reminder will be moved from Two Island to the Move Deleter's House in Fuchsia City.
    """
    display_name = "Kanto Only"


class RandomStartingTown(Toggle):
    """
    Randomizes the town that you start in. This includes any area that has a Pokemon Center except for Indigo Plateau.
    """
    display_name = "Random Starting Town"


class StartingTownBlacklist(OptionSet):
    """
    Prevents certain towns from being chosen as your random starting town.

    Has no effect if the starting town is not randomized.
    """
    display_name = "Starting Town Blacklist"
    valid_keys = list(starting_town_blacklist_map.keys())


class ShufflePokemonCenterEntrances(Toggle):
    """
    Shuffles the Pokemon Center entrances amongst each other.

    The Player's House is included in this pool but will not be shuffled.
    """
    display_name = "Shuffle Pokemon Center Entrances"


class ShuffleGymEntrances(Toggle):
    """
    Shuffles the gym entrances amongst each other.
    """
    display_name = "Shuffle Gym Entrances"


class ShuffleMartEntrances(Toggle):
    """
    Shuffles the Poke Mart entrances amongst each other.

    This does not include the Celadon Department Store entrances.
    """
    display_name = "Shuffle Mart Entrances"


class ShuffleHarborEntrances(Toggle):
    """
    Shuffles the harbor entrances amongst each other.
    """
    display_name = "Shuffle Harbor Entrances"


class ShuffleBuildingEntrances(Choice):
    """
    Shuffles the building entrances amongst each other.

    The Celadon Department Store entrances are included in this pool.

    A building is considered a multi entrance building if the two entrances are normally connected inside the building.
    For instance, the Celadon Condominium is not considered a multi entrance building and the Route 16 Gate counts as
    two separate multi entrance buildings.

    - Off: Building entrances are not shuffled
    - Simple: Single entrance buildings and multi entrance buildings are shuffled separately from each other. Both entrances for multi entrance buildings will connect to the same building
    - Restricted: Single entrance buildings and multi entrance buildings are shuffled separately from each other. Both entrances for multi entrance buildings do not need to lead to the same building
    - Full: All building entrances are shuffled together
    """
    display_name = "Shuffle Building Entrances"
    default = 0
    option_off = 0
    option_simple = 1
    option_restricted = 2
    option_full = 3


class ShuffleDungeonEntrances(Choice):
    """
    Shuffles the dungeon entrances amongst each other.

    - Off: Dungeon entrances are not shuffled
    - Seafoam: Swaps the two Seafoam Island entrances.
    - Simple: Single entrance dungeons and multi entrance dungeons are shuffled separately from each other. Both entrances for multi entrance dungeons will connect to the same dungeon
    - Restricted: Single entrance dungeons and multi entrance dungeons are shuffled separately from each other. Both entrances for multi entrance dungeons do not need to lead to the same dungeon
    - Full: All dungeon entrances are shuffled together
    """
    display_name = "Shuffle Dungeon Entrances"
    default = 0
    option_off = 0
    option_seafoam = 1
    option_simple = 2
    option_restricted = 3
    option_full = 4


class ShuffleInteriorWarps(Toggle):
    """
    Shuffles the interior warps of buildings and dungeons amongst each other.

    The Safari Zone will behave like a normal dungeon when interiors are shuffled.

    The elevator warps in the Celadon Department Store, Rocket Hideout, and Silph Co. are not shuffled.

    The Safari Zone Entrance <-> Safari Zone Center warp is not shuffled.

    The only warps in Lost Cave that are shuffled are the two ladders.
    """
    display_name = "Shuffle Interior Warps"


class ShuffleWarpTiles(Choice):
    """
    Shuffles the warp tiles in buildings and dungeons amongst each other.

    - Off: Warp tiles are not shuffled
    - Simple: All warp tiles in a building or dungeon are shuffled amongst each other, but they will never lead to another building or dungeon
    - Full: All warp tiles are shuffled together
    """
    display_name = "Shuffle Warp Tiles"
    default = 0
    option_off = 0
    option_simple = 1
    option_full = 2


class ShuffleDropdowns(Choice):
    """
    Shuffles the dropdowns in dungeons amongst each other.

    The incorrect dropdowns in Dotted Hole are not shuffled.

    - Off: Dropdowns are not shuffled
    - Simple: All dropdowns of a dungeon are shuffled amongst each other, but they will never lead to another dungeon
    - Full: All dropdowns are shuffled together
    """
    display_name = "Shuffle Dropdowns"
    default = 0
    option_off = 0
    option_simple = 1
    option_full = 2


class MixEntranceWarpPools(OptionSet):
    """
    Shuffle the selected entrances/warps into a mixed pool instead of separate ones. Has no effect on pools whose
    entrances/warps aren't shuffled. Entrances/warps can only be mixed with other entrance/warps that have the same
    restrictions. Can specify "All" as a shortcut for adding in all entrances/warps that can be mixed.

    The avaialble pools that can be mixed are:
    - Gyms
    - Marts
    - Harbors
    - Buildings
    - Dungeons
    - Interiors
    """
    display_name = "Mix Entrance/Warp Pools"
    valid_keys = ["Gyms", "Marts", "Harbors", "Buildings", "Dungeons", "Interiors", "All"]


class DecoupleEntrancesWarps(Toggle):
    """
    Decouple entrances/warps when shuffling them. This means that you are no longer guaranteed to end up back where you
    came from when you go back through an entrance/warp.

    Simple Building/Dungeon shuffle are not compatible with this option and will be changed to Restricted shuffle.
    """
    display_name = "Decouple Entrances/Warps"

class RandomizeFlyDestinations(Choice):
    """
    Randomizes where each fly point takes you. The new fly destinations can be almost any outdoor warp point in the
    game with a few exceptions (Cycling Road Gates for example).

    - Off: Fly destinations are not randomized
    - Area: Fly destinations will be randomized to a location in the same area as its original location (e.g. Vermilion Fly Destination would go to either Vermilion City, Route 6, or Route 11)
    - Map: Fly destinations will be randomized to a location on the same map as its original location (e.g. One Island Fly Destination would go to either One Island, Two Island, or Three Island)
    - Region: Fly destinations will be randomized to a location in the same region as its original location (e.g. Sevii fly destinations would go to another location on the Sevii Islands)
    - Completely Random: Fly destinations are completely random
    """
    display_name = "Randomize Fly Destinations"
    default = 0
    option_off = 0
    option_area = 1
    option_map = 2
    option_region = 3
    option_completely_random = 4


class FlyDestinationPlando(OptionDict):
    """
    Plando what warp certain fly unlocks will take you to.

    For example \"Pallet Town Fly Destination\": \"Player's House\" will make it so that unlocking the Pallet Town fly
    point will let you fly to in front of the Player's House.

    A full list of supported warps can be found at:
    https://github.com/vyneras/Archipelago/blob/frlg-stable/worlds/pokemon_frlg/docs/fly_plando.md

    Has no effect if fly destinations aren't randomized.
    """
    display_name = "Fly Destination Plando"
    schema = Schema({
        Optional("Pallet Town Fly Destination"): And(str, lambda s: s in fly_plando_maps.keys()),
        Optional("Viridian City Fly Destination"): And(str, lambda s: s in fly_plando_maps.keys()),
        Optional("Pewter City Fly Destination"): And(str, lambda s: s in fly_plando_maps.keys()),
        Optional("Route 4 Fly Destination"): And(str, lambda s: s in fly_plando_maps.keys()),
        Optional("Cerulean City Fly Destination"): And(str, lambda s: s in fly_plando_maps.keys()),
        Optional("Vermilion City Fly Destination"): And(str, lambda s: s in fly_plando_maps.keys()),
        Optional("Route 10 Fly Destination"): And(str, lambda s: s in fly_plando_maps.keys()),
        Optional("Lavender Town Fly Destination"): And(str, lambda s: s in fly_plando_maps.keys()),
        Optional("Celadon City Fly Destination"): And(str, lambda s: s in fly_plando_maps.keys()),
        Optional("Fuchsia City Fly Destination"): And(str, lambda s: s in fly_plando_maps.keys()),
        Optional("Saffron City Fly Destination"): And(str, lambda s: s in fly_plando_maps.keys()),
        Optional("Cinnabar Island Fly Destination"): And(str, lambda s: s in fly_plando_maps.keys()),
        Optional("Indigo Plateau Fly Destination"): And(str, lambda s: s in fly_plando_maps.keys()),
        Optional("One Island Fly Destination"): And(str, lambda s: s in fly_plando_maps.keys()),
        Optional("Two Island Fly Destination"): And(str, lambda s: s in fly_plando_maps.keys()),
        Optional("Three Island Fly Destination"): And(str, lambda s: s in fly_plando_maps.keys()),
        Optional("Four Island Fly Destination"): And(str, lambda s: s in fly_plando_maps.keys()),
        Optional("Five Island Fly Destination"): And(str, lambda s: s in fly_plando_maps.keys()),
        Optional("Six Island Fly Destination"): And(str, lambda s: s in fly_plando_maps.keys()),
        Optional("Seven Island Fly Destination"): And(str, lambda s: s in fly_plando_maps.keys()),
    })


class ShuffleBadges(DefaultOnToggle):
    """
    Shuffle Gym Badges into the general item pool. If turned off, Badges will be shuffled among themselves.
    """
    display_name = "Shuffle Badges"


class ShuffleHiddenItems(Choice):
    """
    Shuffle Hidden Items into the general item pool.

    - Off: Hidden Items are not shuffled
    - Nonrecurring: Nonrecurring Hidden Items are shuffled
    - All: All Hidden Items are shuffled. Recurring Hidden Items will always appear and will not regenerate
    """
    display_name = "Shuffle Hidden Items"
    default = 0
    option_off = 0
    option_nonrecurring = 1
    option_all = 2


class ExtraKeyItems(Toggle):
    """
    Adds key items that are required to access the Rocket Hideout, Safari Zone, Pokemon Mansion, and Power Plant.

    Adds four new locations:
    - Item in the Celadon Rocket House
    - Item given by a Worker in the Fuchsia Safari Office
    - Item given by the Scientist in the Cinnabar Pokemon Lab Research Room
    - Hidden Item in the Cerulean Gym (requires Surf & Itemfinder)
    """
    display_name = "Extra Key Items"


class Shopsanity(Toggle):
    """
    Shuffles shop items into the general item pool. The Celadon Department Store 4F Held Items Shop is not shuffled.

    IMPORTANT NOTE: There is a non-randomized shop on the Pokecenter 2F where you can always buy Poke Balls, Potions, etc.
    """
    display_name = "Shopsanity"


class VendingMachines(Toggle):
    """
    Shuffles the Celadon Department Store vending machine items into the general item pool.

    At least one Fresh Water, Soda Pop, and Lemonade are guaranteed to be placed in a shop location.
    """
    display_name = "Vending Machines"


class Prizesanity(Toggle):
    """
    Shuffles the Celadon Game Corner Prize Room items and TMs into the general item pool.
    """
    display_name = "Prizesanity"

class ShopSlots(NamedRange):
    """
    Sets the number of slots per shop that can have progression items when shopsanity is on. Shop slots that cannot be
    progression items will be filled with a random normal shop item from your world.
    """
    display_name = "Shop Slots"
    default = 9
    range_start = 0
    range_end = 9
    special_range_names = {
        "none": 0,
        "all": 9,
    }


class ShopPrices(Choice):
    """
    Sets how shop item's prices are randomized.

    - Vanilla: Items cost their base price
    - Cheap: Items cost 50% of their base price
    - Affordable: Items cost between 50% - 100% of their base price
    - Standard: Items cost 50% - 150% of their base price
    - Expensive: Items cost 100% - 150% of their base price
    """
    display_name = "Shop Prices"
    default = 0
    option_vanilla = 0
    option_cheap = 1
    option_affordable = 2
    option_standard = 3
    option_expensive = 4


class ConsistentShopPrices(Toggle):
    """
    Sets whether all instances of an item will cost the same price in every shop (e.g. if a Potion's price in a shop is
    200 then all Potions in shops will cost 200).
    """
    display_name = "Consistent Shop Prices"


class Trainersanity(NamedRange):
    """
    Beating a trainer gives you an item.

    You can specify how many Trainers should be a check between 0 and 456. If you have Kanto Only on, the amount of
    Trainer checks might be lower than the amount you specify. Trainers that have checks will periodically have an
    exclamation mark appear above their head in game.

    Trainers are no longer missable. Each trainer will add a random filler item into the pool.
    """
    display_name = "Trainersanity"
    default = 0
    range_start = 0
    range_end = 456
    special_range_names = {
        "none": 0,
        "all": 456,
    }


class Rematchsanity(Toggle):
    """
    Beating each of a trainer's rematches gives you an item. Only the rematches for trainers who have a trainersanity
    item will give an item for rematchsanity.

    Each trainer rematch will add a random filler item into the pool.
    """
    display_name = "Rematchsanity"


class RematchRequirements(Choice):
    """
    Sets the requirement for being able to battle trainer's rematches.

    - Badges: Obtain some number of Badges
    - Gyms: Beat some number of Gyms
    """
    display_name = "Rematch Requirements"
    default = 1
    option_badges = 0
    option_gyms = 1


class Dexsanity(NamedRange):
    """
    Adding a "caught" Pokedex entry gives you an item (catching, evolving, trading, etc.).

    You can specify how many Pokedex entries should be a check between 0 and 386. Depending on your settings for
    randomizing wild Pokemon, there might not actually be as many locations as you specify. Pokemon that have checks
    will have a black silhouette of a pokeball in the Pokedex and in the battle HUD if you have seen them already.

    Defeating Gym Leaders provides seen Pokedex info, allowing you to see on the map where a Pokemon can be found in
    the wild.

    Each entry will add a random filler item into the pool.
    """
    display_name = "Dexsanity"
    default = 0
    range_start = 0
    range_end = 386
    special_range_names = {
        "none": 0,
        "all": 386,
    }


class Famesanity(Toggle):
    """
    Unlocking entries in the Fame Checker gives you an item.

    Each entry will add a random filler item into the pool.
    """
    display_name = "Famesanity"


class ShuffleFlyUnlocks(Choice):
    """
    Shuffles the ability to fly to Pokemon Centers into the pool. Entering the map that normally would unlock the
    fly point on the map gives a random item.

    - Off: Fly Unlocks are not shuffled
    - Exclude Indigo: Fly Unlocks are shuffled. Indigo Plateau Fly Unlock is vanilla
    - All: Fly Unlocks are shuffled
    """
    display_name = "Shuffle Fly Unlocks"
    default = 0
    option_off = 0
    option_exclude_indigo = 1
    option_all = 2


class PokemonRequestLocations(Toggle):
    """
    Shuffle the locations that require you to show a specific Pokemon to an NPC. If turned on, the Pokemon that are
    required will be found somewhere in the wild. Talking to the NPC that wants to see the Pokemon will provide you with
    the Pokedex info for where to find it as well as tell you the item they'll give.
    """
    display_name = "Pokemon Request Locations"


class ShufflePokedex(Choice):
    """
    Shuffle the Pokedex into the item pool, or start with it.

    The Pokedex is hard required for any of the Oak's Aide or Dexsanity locations and is logically required for any of
    the Pokemon Request Locations and In-Game Trades.
    """
    display_name = "Shuffle Pokedex"
    default = 2
    option_vanilla = 0
    option_shuffle = 1
    option_start_with = 2


class ShuffleRunningShoes(Choice):
    """
    Shuffle the running shoes into the item pool, or start with it.
    """
    display_name = "Shuffle Running Shoes"
    default = 2
    option_vanilla = 0
    option_shuffle = 1
    option_start_with = 2


class ShuffleBerryPouch(Toggle):
    """
    Shuffles the berry pouch into the item pool. If not shuffled then you will start with it.
    """
    display_name = "Shuffle Berry Pouch"


class ShuffleTMCase(Toggle):
    """
    Shuffles the TM case into the item pool. If not shuffled then you will start with it.
    """
    display_name = "Shuffle TM Case"


class ShuffleJumpingShoes(Toggle):
    """
    Shuffles the Jumping Shoes into the item pool. If not shuffled then you will start with it.

    The Jumping Shoes are a new item that grants you the ability to jump down ledges.
    """
    display_name = "Shuffle Jumping Shoes"


class PostGoalLocations(Toggle):
    """
    Shuffles locations into the item pool that are only accessible after your goal is completed.

    If Cerulean Cave access is locked by your goal then Cerulean Cave won't be included in Shuffled Dungeons.
    """
    display_name = "Post Goal Locations"


class CardKey(Choice):
    """
    Sets how the card key that unlocks the doors in Silph Co. is handled. If Split or Progressive, nine new locations
    will be added to Silph Co. in the form of item balls on floors 2 through 11 (except for floor five).

    - Vanilla: There is one Card Key in the pool that unlocks every door in Silph Co.
    - Split: The Card Key is split into ten items, one for each floor of Silph Co. that has doors
    - Progressive: The Card Key is split into ten items, and you will always obtain them in order from 2F to 11F
    """
    display_name = "Silph Co. Card Key"
    default = 0
    option_vanilla = 0
    option_split = 1
    option_progressive = 2


class IslandPasses(Choice):
    """
    Sets how the passes that allow you to travel to the Sevii Islands are handled. If Split or Progressive, five new
    locations will be added to events related to the Sevii Islands.

    - Vanilla: The Tri Pass and Rainbow Pass are two separate items in the pool and can be found in any order
    - Progressive: There are two Progressive Passes in the pool. You will always obtain the Tri Pass before the Rainbow Pass
    - Split: The Tri Pass and Rainbow Pass are split into seven items, one for each island
    - Progressive Split: The Tri Pass and Rainbow Pass are split into seven items, and you will always obtain the Passes in order from the First Pass to the Seventh Pass
    """
    display_name = "Sevii Island Passes"
    default = 0
    option_vanilla = 0
    option_progressive = 1
    option_split = 2
    option_progressive_split = 3


class FishingRods(Choice):
    """
    Sets how the fishing rods are handled.

    - Vanilla: The fishing rods are all separate items in the pool and can be found in any order
    - Progressive: There are three Progressive Rods in the pool, and you will always obtain them in order from Old Rod to Super Rod
    """
    display_name = "Fishing Rods"
    default = 0
    option_vanilla = 0
    option_progressive = 1


class SplitTeas(Toggle):
    """
    Splits the Tea item into four different items. Each guard to Saffron City will require a different Tea to pass.
    Brock, Misty, and Erika will appear in the Celadon Condominiums after beating them and give you a randomized item.

    The Tea required to get past each guard are as follows:
    - Route 5: Blue Tea
    - Route 6: Red Tea
    - Route 7: Green Tea
    - Route 8: Purple Tea
    """
    display_name = "Split Teas"


class GymKeys(Toggle):
    """
    Adds keys that are needed to enter each of the gyms similar to the Secret Key. Renames the Secret Key to the
    Cinnabar Key.

    Adds seven new locations:
    - Item in the Pewter Museum 2F
    - Item from Man on a Date at Route 25
    - Item in Diglett's Cave B1F
    - Item in the Celadon Hotel
    - Item in the Safari Zone East Rest House
    - Item in the Saffron Dojo
    - Item from the Old Man near Viridian Gym
    """
    display_name = "Gym Keys"


class ItemfinderRequired(Choice):
    """
    Sets whether the Itemfinder if required for Hidden Items. Some items cannot be picked up without using the
    Itemfinder regardless of this setting (e.g. the Leftovers under Snorlax on Route 12 & 16).

    - Off: The Itemfinder is not required to pickup Hidden Items
    - Logic: The Itemfinder is logically required to pickup Hidden Items
    - Required: The Itemfinder is required to pickup Hidden Items
    """
    display_name = "Itemfinder Required"
    default = 1
    option_off = 0
    option_logic = 1
    option_required = 2


class FlashRequired(Choice):
    """
    Sets whether HM05 Flash is logically required to navigate dark caves.

    - Off: Flash is not required to navigate dark caves
    - Logic: Flash is logically required to navigate dark caves
    - Required: Flash is required to navigate dark caves
    """
    display_name = "Flash Required"
    default = 1
    option_off = 0
    option_logic = 1
    option_required = 2


class FameCheckerRequired(DefaultOnToggle):
    """
    Sets whether it is required to have the Fame Checker in order to unlock entries.

    All Fame Checker entries that are one time occurences have been changed so that you can trigger them repeatedly.
    """
    display_name = "Fame Checker Required"


class BicycleRequiresJumpingShoes(DefaultOnToggle):
    """
    Sets whether the Bicycle requires you to have the Jumping Shoes in order to jump down ledges while on the Bicycle.
    """
    display_name = "Bicycle Requires Jumping Shoes"


class AcrobaticBicycle(Toggle):
    """
    Sets whether the Bicycle is able to jump up ledges in addition to jumping down ledges. If the Bicycle Requires
    Jumping Shoes setting is on then the Jumping Shoes is necessary in order to jump up ledges as well.
    """
    display_name = "Acrobatic Bicycle"

class EvolutionsRequired(OptionSet):
    """
    Sets which types of locations and/or access rules that evolutions may be logically required for.
    """
    display_name = "Evolutions Required"
    valid_keys = ["HM Requirement", "Oak's Aides", "Dexsanity"]
    default = ["HM Requirement", "Oak's Aides", "Dexsanity"]


class EvolutionMethodsRequired(OptionSet):
    """
    Sets which types of evolutions may be logically required.
    """
    display_name = "Evolution Methods Required"
    valid_keys = ["Level", "Level Tyrogue", "Level Wurmple", "Evo Item", "Evo & Held Item", "Friendship"]
    default = ["Level", "Level Tyrogue", "Level Wurmple", "Evo Item", "Evo & Held Item", "Friendship"]


class ViridianCityRoadblock(Choice):
    """
    Sets the requirement for passing the Viridian City Roadblock.

    - Vanilla: The Old Man moves out of the way after delivering Oak's Parcel
    - Early Parcel: Same as Vanilla but Oak's Parcel will be available at the beginning of your game. This option will have no effect and be treated as Vanilla if Random Starting Town is on
    - Open: The Old Man is moved out of the way at the start of the game
    """
    display_name = "Viridian City Roadblock"
    default = 1
    option_vanilla = 0
    option_early_parcel = 1
    option_open = 2


class PewterCityRoadblock(Choice):
    """
    Sets the requirement for passing the Pewter City Roadblock.

    - Open: The boy will not stop you from entering Route 3
    - Brock: The boy will stop you from entering Route 3 until you defeat Brock
    - Any Gym Leader: The boy will stop you from entering Route 3 until you defeat any Gym Leader
    - Boulder Badge: The boy will stop you from entering Route 3 until you have the Boulder Badge
    - Any Badge: The boy will stop you from entering Route 3 until you have a Badge
    """
    display_name = "Pewter City Roadblock"
    default = 1
    option_open = 0
    option_brock = 1
    option_any_gym = 2
    option_boulder_badge = 3
    option_any_badge = 4


class ModifyWorldState(OptionSet):
    """
    Set various changes to the world's state that changes how you can access various regions and locations.

    The valid options and their effects are the following:
    - Modify Route 2: Replaces the northmost cuttable tree with a smashable rock
    - Remove Cerulean Roadblocks: Removes the policeman and slowpoke that block the exits of the city
    - Block Tunnels: Blocks the entrances to the underground tunnels with smashable rocks
    - Modify Route 9: Replaces the cuttable tree with a smashable rock
    - Modify Route 10: Adds a waterfall to Route 10 that connects the north and south sides
    - Block Tower: Blocks the 1F stairs of Pokemon Tower with a ghost battle
    - Route 12 Boulders: Adds boulders to Route 12 that block the exits to Route 11 & 13
    - Modify Route 12: Adds impassable rocks to Route 12 that prevent surfing around Snorlax
    - Modify Route 16: Adds a smashable rock to Route 16 that allows you to bypass the Snorlax
    - Open Silph: Moves the Team Rocket Grunt that blocks the entrance to Silph Co.
    - Remove Saffron Rockets: Removed the Team Rocket Grunts from Saffron City
    - Route 23 Trees: Adds cuttable trees to Route 23 under the sixth checkpoint
    - Modify Route 23: Adds a waterfall to Route 23 at the end of the water section
    - Victory Road Rocks: Adds smashable rocks to Victory Road that block the floor switches
    - Early Gossipers: Removes the requirement to have entered the Hall of Fame from various Famesanity locations
    - Total Darkness: Changes dark caves to be completely black and provide no vision without Flash
    - Block Vermilion Sailing: Prevents you from sailing to Vermilion City on the Seagallop until you have gotten
                               the S.S. Ticket
    - All Elevators Locked: Prevents you from using the elevators in the Celadon Department Store and Silph Co. until
                            you have gotten the Lift Key
    """
    display_name = "Modify World State"
    valid_keys = ["Modify Route 2", "Remove Cerulean Roadblocks", "Block Tunnels", "Modify Route 9",
                  "Modify Route 10", "Block Tower", "Route 12 Boulders", "Modify Route 12", "Modify Route 16",
                  "Open Silph", "Remove Saffron Rockets", "Route 23 Trees", "Modify Route 23", "Victory Road Rocks",
                  "Early Gossipers", "Total Darkness", "Block Vermilion Sailing", "All Elevators Locked"]


class AdditionalDarkCaves(OptionSet):
    """
    Set additional caves to be dark caves, potentially requiring Flash to navigate them.

    The caves that can be turned into dark caves are:
    - Mt. Moon
    - Diglett's Cave
    - Victory Road
    """
    display_name = "Additional Dark Caves"
    valid_keys = ["Mt. Moon", "Diglett's Cave", "Victory Road"]


class RemoveBadgeRequirement(OptionSet):
    """
    Removes the badge requirement to use any of the HMs listed.

    HMs need to be listed by the move name (e.g. Cut, Fly, Surf, etc.).
    """
    display_name = "Remove Badge Requirement"
    valid_keys = ["Cut", "Fly", "Surf", "Strength", "Flash", "Rock Smash", "Waterfall"]


class OaksAideRoute2(Range):
    """
    Sets the number of Pokemon that need to be registered in the Pokedex to receive the item from Professor Oak's Aide
    on Route 2. Vanilla is 10.
    """
    display_name = "Oak's Aide Route 2"
    default = 5
    range_start = 0
    range_end = 50


class OaksAideRoute10(Range):
    """
    Sets the number of Pokemon that need to be registered in the Pokedex to receive the item from Professor Oak's Aide
    on Route 10. Vanilla is 20.
    """
    display_name = "Oak's Aide Route 10"
    default = 10
    range_start = 0
    range_end = 50


class OaksAideRoute11(Range):
    """
    Sets the number of Pokemon that need to be registered in the Pokedex to receive the item from Professor Oak's Aide
    on Route 11. Vanilla is 30.
    """
    display_name = "Oak's Aide Route 11"
    default = 15
    range_start = 0
    range_end = 50


class OaksAideRoute16(Range):
    """
    Sets the number of Pokemon that need to be registered in the Pokedex to receive the item from Professor Oak's Aide
    on Route 16. Vanilla is 40.
    """
    display_name = "Oak's Aide Route 16"
    default = 20
    range_start = 0
    range_end = 50


class OaksAideRoute15(Range):
    """
    Sets the number of Pokemon that need to be registered in the Pokedex to receive the item from Professor Oak's Aide
    on Route 15. Vanilla is 50.
    """
    display_name = "Oak's Aide Route 15"
    default = 25
    range_start = 0
    range_end = 50


class PokemonLabFossilCount(Range):
    """
    Sets the number of fossils you need to revive at the Pokemon Lab in order to obtain the second fossil.
    """
    display_name = "Pokemon Lab Fossil Count"
    default = 3
    range_start = 0
    range_end = 3


class ViridianGymRequirement(Choice):
    """
    Sets the requirement for opening the Viridian Gym.

    - Badges: Obtain some number of Badges
    - Gyms: Beat some number of Gyms
    """
    display_name = "Viridian Gym Requirement"
    default = 0
    option_badges = 0
    option_gyms = 1


class ViridianGymCount(Range):
    """
    Sets the number of Badges/Gyms required to open the Viridian Gym.
    """
    display_name = "Viridian Gym Count"
    default = 7
    range_start = 0
    range_end = 7


class Route22GateRequirement(Choice):
    """
    Sets the requirement for passing through the Route 22 Gate.

    - Badges: Obtain some number of Badges
    - Gyms: Beat some number of Gyms
    """
    display_name = "Route 22 Gate Requirement"
    default = 0
    option_badges = 0
    option_gyms = 1


class Route22GateCount(Range):
    """
    Sets the number of Badges/Gyms required to pass through the Route 22 Gate.
    """
    display_name = "Route 22 Gate Count"
    default = 7
    range_start = 0
    range_end = 8


class Route23GuardRequirement(Choice):
    """
    Sets the requirement for passing the Route 23 Guard.

    - Badges: Obtain some number of Badges
    - Gyms: Beat some number of Gyms
    """
    display_name = "Route 23 Guard Requirement"
    default = 0
    option_badges = 0
    option_gyms = 1


class Route23GuardCount(Range):
    """
    Sets the number of Badges/Gyms required to pass the Route 23 Guard.
    """
    display_name = "Route 23 Guard Count"
    default = 7
    range_start = 0
    range_end = 8


class EliteFourRequirement(Choice):
    """
    Sets the requirement for challenging the Elite Four.

    - Badges: Obtain some number of Badges
    - Gyms: Beat some number of Gyms
    """
    display_name = "Elite Four Requirement"
    default = 0
    option_badges = 0
    option_gyms = 1


class EliteFourCount(Range):
    """
    Sets the number of Badges/Gyms required to challenge the Elite Four.
    """
    display_name = "Elite Four Count"
    default = 8
    range_start = 0
    range_end = 8


class EliteFourRematchCount(Range):
    """
    Sets the number of Badges/Gyms required to challenge the Elite Four Rematch.
    """
    display_name = "Elite Four Rematch Count"
    default = 8
    range_start = 0
    range_end = 8


class CeruleanCaveRequirement(Choice):
    """
    Sets the requirement for being able to enter Cerulean Cave.

    - Vanilla: Become the Champion and restore the Network Machine on the Sevii Islands
    - Champion: Become the Champion
    - Network Machine: Restore the Network Machine on the Sevii Islands
    - Badges: Obtain some number of Badges
    - Gyms: Beat some number of Gyms
    """
    display_name = "Cerulean Cave Requirement"
    default = 0
    option_vanilla = 0
    option_champion = 1
    option_restore_network = 2
    option_badges = 3
    option_gyms = 4


class CeruleanCaveCount(Range):
    """
    Sets the number of Badges/Gyms required to enter Cerulean Cave. This setting only matters if the Cerulean Cave
    Requirement is set to either Badges or Gyms.
    """
    display_name = "Cerulean Cave Count"
    default = 8
    range_start = 0
    range_end = 8


class LevelScaling(Choice):
    """
    Sets whether encounter levels are scaled by sphere access.

    - Off: Vanilla levels are used
    - Spheres: Levels are scaled based on sphere access
    - Spheres and Distance: Levels are scaled based on sphere access and the distance they are from your starting town
    """
    display_name = "Level Scaling"
    default = 0
    option_off = 0
    option_spheres = 1
    option_spheres_and_distance = 2


class ModifyTrainerLevels(Range):
    """
    Modifies the level of all Trainer's Pokemon by the specified percentage.
    """
    display_name = "Modify Trainer Levels"
    default = 100
    range_start = 0
    range_end = 200


class ForceFullyEvolved(NamedRange):
    """
    Forces opponent's Pokemon to be fully evolved if they are greater than or equal to the specified level.

    If set to "species" will force opponent's Pokemon to be evolved based on the level the species would normally
    evolve. For species that don't evolve based on levels, the level they will be evolved at is determined by their BST.

    Only applies when trainer parties are randomized.
    """
    display_name = "Force Fully Evolved"
    default = 0
    range_start = -1
    range_end = 100
    special_range_names = {
        "never": 0,
        "species": -1
    }


class RandomizeWildPokemon(Choice):
    """
    Randomizes wild Pokemon encounters (grass, caves, water, fishing)

    - Vanilla: Wild Pokemon are unchanged
    - Match Base Stats: Wild Pokemon are replaced with species with approximately the same BST
    - Match Type: Wild Pokemon are replaced with species that share a type with the original
    - Match Base Stats and Type: Apply both Match Base Stats and Match Type
    - Completely Random: There are no restrictions
    """
    display_name = "Randomize Wild Pokemon"
    default = 0
    option_vanilla = 0
    option_match_base_stats = 1
    option_match_type = 2
    option_match_base_stats_and_type = 3
    option_completely_random = 4


class WildPokemonGroups(Choice):
    """
    If wild Pokemon are not vanilla, they will be randomized according to the grouping specified.

    - None: Pokemon are not randomized together based on any groupings
    - Dungeons: All Pokemon of the same species in a dungeon are randomized together
    - Species: All Pokemon of the same species are randomized together
    """
    display_name = "Wild Pokemon Groups"
    default = 0
    option_none = 0
    option_dungeons = 1
    option_species = 2


class WildPokemonBlacklist(OptionSet):
    """
    Prevents listed species from appearing in the wild when wild Pokemon are randomized.

    May be overridden if enforcing other restrictions in combination with this blacklist is impossible.

    Use "Legendaries" as a shortcut for all legendary Pokemon.
    """
    display_name = "Wild Pokemon Blacklist"
    valid_keys = ["Legendaries"] + sorted([species.name for species in data.species.values()])


class RandomizeStarters(Choice):
    """
    Randomizes the starter Pokemon in Professor Oak's Lab.

    - Vanilla: Starters are unchanged
    - Match Base Stats: Starters are replaced with species with approximately the same BST
    - Match Type: Starters are replaced with species that share a type with the original
    - Match Base Stats and Type: Apply both Match Base Stats and Match Type
    - Completely Random: There are no restrictions
    """
    display_name = "Randomize Starters"
    default = 0
    option_vanilla = 0
    option_match_base_stats = 1
    option_match_type = 2
    option_match_base_stats_and_type = 3
    option_completely_random = 4


class StarterBlacklist(OptionSet):
    """
    Prevents listed species from appearing as a starter when starters are randomized.

    May be overridden if enforcing other restrictions in combination with this blacklist is impossible.

    Use "Legendaries" as a shortcut for all legendary Pokemon.
    """
    display_name = "Starter Blacklist"
    valid_keys = ["Legendaries"] + sorted([species.name for species in data.species.values()])


class RandomizeTrainerParties(Choice):
    """
    Randomizes the Pokemon in all trainer's parties.

    - Vanilla: Parties are unchanged
    - Match Base Stats: Trainer Pokemon are replaced with species with approximately the same BST
    - Match Type: Trainer Pokemon are replaced with species that share a type with the original
    - Match Base Stats and Type: Apply both Match Base Stats and Match Type
    - Completely Random: There are no restrictions
    """
    display_name = "Randomize Trainer Parties"
    default = 0
    option_vanilla = 0
    option_match_base_stats = 1
    option_match_type = 2
    option_match_base_stats_and_type = 3
    option_completely_random = 4


class TrainerPartyBlacklist(OptionSet):
    """
    Prevents listed species from appearing in trainer's parties when trainer's parties are randomized.

    May be overridden if enforcing other restrictions in combination with this blacklist is impossible.

    Use "Legendaries" as a shortcut for all legendary Pokemon.
    """
    display_name = "Trainer Party Blacklist"
    valid_keys = ["Legendaries"] + sorted([species.name for species in data.species.values()])


class RandomizeLegendaryPokemon(Choice):
    """
    Randomizes legendary Pokemon (Mewtwo, Zapdos, Deoxys, etc.). Does not randomize the roamer.

    - Vanilla: Legendary encounters are unchanged
    - Legendaries: Legendary encounters are replaced with another legendary Pokemon
    - Match Base Stats: Legendary encounters are replaced with species with approximately the same BST
    - Match Type: Legendary encounters are replaced with species that share a type with the original
    - Match Base Stats and Type: Apply both Match Base Stats and Match Type
    - Completely Random: There are no restrictions
    """
    display_name = "Randomize Legendary Pokemon"
    default = 0
    option_vanilla = 0
    option_legendaries = 1
    option_match_base_stats = 2
    option_match_type = 3
    option_match_base_stats_and_type = 4
    option_completely_random = 5


class LegendaryPokemonBlacklist(OptionSet):
    """
    Prevents the listed species from appearing as a legenary Pokemon when legendary Pokemon are randomized.

    May be overridden if enforcing other restrictions in combination with this blacklist is impossible.

    Use "Legendaries" as a shortcut for all legendary Pokemon.
    """
    display_name = "Legendary Pokemon Blacklist"
    valid_keys = ["Legendaries"] + sorted([species.name for species in data.species.values()])


class RandomizeMiscPokemon(Choice):
    """
    Randomizes misc Pokemon. This includes non-legendary static encounters, gift Pokemon, and trade Pokemon.

    - Vanilla: Species are unchanged
    - Match Base Stats: Species are replaced with species with approximately the same bst
    - Match Type: Species are replaced with species that share a type with the original
    - Match Base Stats and Type: Apply both Match Base Stats and Match Type
    - Completely Random: There are no restrictions
    """
    display_name = "Randomize Misc Pokemon"
    default = 0
    option_vanilla = 0
    option_match_base_stats = 1
    option_match_type = 2
    option_match_base_stats_and_type = 3
    option_completely_random = 4


class MiscPokemonBlacklist(OptionSet):
    """
    Prevents the listed species from appearing as a miscellaneous Pokemon when miscellaneous Pokemon are randomized.

    May be overridden if enforcing other restrictions in combination with this blacklist is impossible.

    Use "Legendaries" as a shortcut for all legendary Pokemon.
    """
    display_name = "Misc Pokemon Blacklist"
    valid_keys = ["Legendaries"] + sorted([species.name for species in data.species.values()])


class RandomizeTypes(Choice):
    """
    Randomizes the type(s) of every Pokemon. Each species will have the same number of types.

    - Vanilla: Types are unchanged
    - Shuffle: Types are shuffled globally for all species (e.g. every Water-type Pokemon becomes Fire-type)
    - Completely Random: Each species has its type(s) randomized
    - Follow Evolutions: Types are randomized per evolution line instead of per species
    """
    display_name = "Randomize Types"
    default = 0
    option_vanilla = 0
    option_shuffle = 1
    option_completely_random = 2
    option_follow_evolutions = 3


class RandomizeAbilities(Choice):
    """
    Randomizes abilities of every species. Each species will have the same number of abilities.

    - Vanilla: Abilities are unchanged
    - Completely Random: Each species has its abilities randomized
    - Follow Evolutions: Abilities are randomized, but evolutions that normally retain abilities will still do so
    """
    display_name = "Randomize Abilities"
    default = 0
    option_vanilla = 0
    option_completely_random = 1
    option_follow_evolutions = 2


class AbilityBlacklist(OptionSet):
    """
    Prevent species from being given these abilities.

    Has no effect if abilities are not randomized.
    """
    display_name = "Ability Blacklist"
    valid_keys = sorted(ability_name_map.keys())


class RandomizeMoves(Choice):
    """
    Randomizes the moves a Pokemon learns through leveling.
    Your starter is guaranteed to have a usable damaging move.

    - Vanilla: Learnset is unchanged
    - Randomized: Moves are randomized
    - Start with Four Moves: Moves are randomized and all Pokemon know 4 moves at level 1
    """
    display_name = "Randomize Moves"
    default = 0
    option_vanilla = 0
    option_randomized = 1
    option_start_with_four_moves = 2


class MoveMatchTypeBias(Range):
    """
    Sets the probability that a learned move will be forced to match one of the types of a Pokemon.

    If a move is not forced to match type, it will roll for Normal type bias.
    """
    display_name = "Move Match Type Bias"
    default = 0
    range_start = 0
    range_end = 100


class MoveNormalTypeBias(Range):
    """
    Sets the probability that a learned move will be forced to be a Normal type move.

    If a move is not forced to be Normal, it will be completely random.
    """
    display_name = "Move Normal Type Bias"
    default = 0
    range_start = 0
    range_end = 100


class MoveBlacklist(OptionSet):
    """
    Prevents species from learning these moves via learnsets.

    Has no effect if moves are not randomized.
    """
    display_name = "Move Blacklist"
    valid_keys = sorted(move_name_map.keys())


class RandomizeBaseStats(Choice):
    """
    Randomize the base stats for every species.

    - Vanilla: Base stats are unchanged
    - Shuffle: Base stats are shuffled amongst each other
    - Keep BST: Random base stats, but base stat total is preserved
    - Completely Random: Random base stats and base stat total
    """
    display_name = "Randomize Base Stats"
    default = 0
    option_vanilla = 0
    option_shuffle = 1
    option_keep_bst = 2
    option_completely_random = 3


class PhysicalSpecialSplit(Toggle):
    """
    Changes the damage category that moves use to match the categories since the Gen IV physical/special split instead
    of the damage category being determined by the move's type.
    """
    display_name = "Physical/Special Split"


class RandomizeMoveTypes(Choice):
    """
    Randomizes the type for each move.

    - Vanilla: Move types are unchanged
    - Shuffle: Move types are shuffled globally for all moves (e.g. every Water-type Move becomes Fire-type)
    - Completely Random: Each move has its type randomized
    """
    display_name = "Randomize Move Types"
    default = 0
    option_vanilla = 0
    option_shuffle = 1
    option_completely_random = 2


class RandomizeDamageCategories(Choice):
    """
    Randomizes the damage category for each move/type. Will randomized the damage category of the moves individually or
    by each type depending on if the Physical/Special Split option is on.

    - Vanilla: Damage Categories are unchanged
    - Shuffle: Damage Categories for moves/types are shuffled so the amount of physical and special moves/types will remain the same
    - Completely Random: Each moves/types damage category is chosen at random with no regard to maintaining the same amount of physical and special moves/types
    """
    display_name = "Randomize Damage Categories"
    default = 0
    option_vanilla = 0
    option_shuffle = 1
    option_completely_random = 2


class HmCompatibility(NamedRange):
    """
    Sets the percent chance that a given HM is compatible with a species.

    If you have seen a Pokemon already, the HMs it can use are listed in the Pokedex.
    """
    display_name = "HM Compatibility"
    default = -1
    range_start = -1
    range_end = 100
    special_range_names = {
        "vanilla": -1,
        "none": 0,
        "full": 100,
    }


class TmTutorCompatibility(NamedRange):
    """
    Sets the percent chance that a given TM or move tutor is compatible with a species.
    """
    display_name = "TM/Tutor Compatibility"
    default = -1
    range_start = -1
    range_end = 100
    special_range_names = {
        "vanilla": -1,
        "none": 0,
        "full": 100,
    }


class TmTutorMoves(Toggle):
    """
    Randomizes the moves taught by TMs and move tutors.

    Some opponents like gym leaders are allowed to use TMs. This option can affect the moves they know.
    """
    display_name = "Randomize TM/Tutor Moves"


class TmTutorMoveBlacklist(OptionSet):
    """
    Prevents TMs and move tutors from teaching these moves.

    Has no effect if TM and tutor moves are not randomized.
    """
    display_name = "TM/Tutor Moves Blacklist"
    valid_keys = sorted(move_name_map.keys())


class ReusableTmsTutors(Toggle):
    """
    Sets TMs to not break after use (they remain sellable). Allows Move Tutors to be used infinitely.
    """
    display_name = "Reusable TMs/Move Tutors"


class MinCatchRate(Range):
    """
    Sets the minimum catch rate a Pokemon can have. It will raise any Pokemon's catch rate to this value if its normal
    catch rate is lower than the chosen value.
    """
    display_name = "Minimum Catch Rate"
    range_start = 3
    range_end = 255
    default = 3


class AllPokemonSeen(Toggle):
    """
    Start will all Pokemon seen in your Pokedex.
    This allows you to see where the Pokemon can be encountered in the wild.
    """
    display_name = "All Pokemon Seen"


class StartingMoney(Range):
    """
    Sets the amount of money that you start with.
    """
    display_name = "Starting Money"
    range_start = 0
    range_end = 999999
    default = 3000


class BetterShops(Toggle):
    """
    Most Pokemarts will sell all normal Pokemart items. The exceptions are the following:

    - Celadon Department Store 2F TM Pokemart
    - Celadon Department Store 4F Evo Stone Pokemart
    - Celadon Department Store 4F Held Items Pokemart
    - Celadon Department Store 5F Vitamin Pokemart
    - Two Island Market Stall
    """
    display_name = "Better Shops"


class FreeFlyLocation(Toggle):
    """
    Enables flying to one random location (excluding cities reachable with no items).
    """
    display_name = "Free Fly Location"


class FreeFlyBlacklist(OptionSet):
    """
    Prevents certain towns from being chosen as your free fly location.
    """
    display_name = "Free Fly Blacklist"
    valid_keys = list(fly_blacklist_map.keys())


class TownMapFlyLocation(Toggle):
    """
    Enables flying to one random location once the town map has been obtained (excluding cities reachable with no
    items).
    """
    display_name = "Town Map Fly Location"


class TownMapFlyBlacklist(OptionSet):
    """
    Prevents certain towns from being chosen as your town map fly location.
    """
    display_name = "Town Map Fly Blacklist"
    valid_keys = list(fly_blacklist_map.keys())


class RemoteItems(Toggle):
    """
    Instead of placing your own items directly into the ROM, all items are received from the server, including items you find for yourself.

    This enables co-op of a single slot and recovering more items after a lost save file (if you're so unlucky).

    But it changes pickup behavior slightly and requires connection to the server to receive any items.
    """
    display_name = "Remote Items"


class RandomizeMusic(Toggle):
    """
    Shuffles music played in any situation where it loops.
    """
    display_name = "Randomize Music"


class RandomizeFanfares(Toggle):
    """
    Shuffles fanfares for item pickups, healing at the Pokecenter, etc.
    """
    display_name = "Randomize Fanfares"


class GameOptions(OptionDict):
    """
    Allows you to preset the in game options.
    The available options and their allowed values are the following:

    - Text Speed: Slow, Mid, Fast, Instant
    - Turbo Button: Off, A, B, A/B
    - Auto Run: Off, On
    - Button Mode: Help, L/R, L=A
    - Frame: 1-10
    - Battle Scene: Off, On
    - Battle Style: Shift, Set
    - Show Effectiveness: Off, On
    - Experience Multiplier: 0-1000 in increments of 10 (0, 10, 20, etc.)
    - Experience Distribution: Gen III, Gen VI, Gen VIII
    - Sound: Mono, Stereo
    - Low HP Beep: Off, On
    - Skip Fanfares: Off, On
    - Bike Music: Off, On
    - Surf Music: Off, On
    - Guaranteed Catch: Off, On
    - Guaranteed Run: Off, On
    - Encounter Rates: Vanilla, Normalized
    - Blind Trainers: Off, On
    - Skip Nicknames: Off, On
    - Item Messages: All, Progression, None
    """
    display_name = "Game Options"
    schema = Schema({
        Optional("Text Speed"): And(str, lambda s: s in GAME_OPTIONS["Text Speed"].options.keys()),
        Optional("Turbo Button"): Or(And(str, lambda s: s in GAME_OPTIONS["Turbo Button"].options.keys()),
                                     And(bool, lambda s: s in GAME_OPTIONS["Turbo Button"].options.keys()),),
        Optional("Auto Run"): Or(And(str, lambda s: s in GAME_OPTIONS["Auto Run"].options.keys()),
                                 And(bool, lambda s: s in GAME_OPTIONS["Auto Run"].options.keys()),),
        Optional("Button Mode"): And(str, lambda s: s in GAME_OPTIONS["Button Mode"].options.keys()),
        Optional("Frame"): And(int, lambda i: i in GAME_OPTIONS["Frame"].options.keys()),
        Optional("Battle Scene"): Or(And(str, lambda s: s in GAME_OPTIONS["Battle Scene"].options.keys()),
                                     And(bool, lambda s: s in GAME_OPTIONS["Battle Scene"].options.keys()),),
        Optional("Battle Style"): And(str, lambda s: s in GAME_OPTIONS["Battle Style"].options.keys()),
        Optional("Show Effectiveness"): Or(And(str, lambda s: s in GAME_OPTIONS["Show Effectiveness"].options.keys()),
                                           And(bool, lambda s: s in GAME_OPTIONS["Show Effectiveness"].options.keys()),),
        Optional("Experience Multiplier"): And(int, lambda s: s in GAME_OPTIONS["Experience Multiplier"].options.keys()),
        Optional("Experience Distribution"): And(str, lambda s: s in GAME_OPTIONS["Experience Distribution"].options.keys()),
        Optional("Sound"): And(str, lambda s: s in GAME_OPTIONS["Sound"].options.keys()),
        Optional("Low HP Beep"): Or(And(str, lambda s: s in GAME_OPTIONS["Low HP Beep"].options.keys()),
                                    And(bool, lambda s: s in GAME_OPTIONS["Low HP Beep"].options.keys()),),
        Optional("Skip Fanfares"): Or(And(str, lambda s: s in GAME_OPTIONS["Skip Fanfares"].options.keys()),
                                      And(bool, lambda s: s in GAME_OPTIONS["Skip Fanfares"].options.keys()),),
        Optional("Bike Music"): Or(And(str, lambda s: s in GAME_OPTIONS["Bike Music"].options.keys()),
                                   And(bool, lambda s: s in GAME_OPTIONS["Bike Music"].options.keys()),),
        Optional("Surf Music"): Or(And(str, lambda s: s in GAME_OPTIONS["Surf Music"].options.keys()),
                                   And(bool, lambda s: s in GAME_OPTIONS["Surf Music"].options.keys()),),
        Optional("Guaranteed Catch"): Or(And(str, lambda s: s in GAME_OPTIONS["Guaranteed Catch"].options.keys()),
                                         And(bool, lambda s: s in GAME_OPTIONS["Guaranteed Catch"].options.keys()),),
        Optional("Guaranteed Run"): Or(And(str, lambda s: s in GAME_OPTIONS["Guaranteed Run"].options.keys()),
                                       And(bool, lambda s: s in GAME_OPTIONS["Guaranteed Run"].options.keys()),),
        Optional("Encounter Rates"): And(str, lambda s: s in GAME_OPTIONS["Encounter Rates"].options.keys()),
        Optional("Blind Trainers"): Or(And(str, lambda s: s in GAME_OPTIONS["Blind Trainers"].options.keys()),
                                       And(bool, lambda s: s in GAME_OPTIONS["Blind Trainers"].options.keys()),),
        Optional("Skip Nicknames"): Or(And(str, lambda s: s in GAME_OPTIONS["Skip Nicknames"].options.keys()),
                                       And(bool, lambda s: s in GAME_OPTIONS["Skip Nicknames"].options.keys()),),
        Optional("Item Messages"): And(str, lambda s: s in GAME_OPTIONS["Item Messages"].options.keys()),
    })


class ProvideHints(Choice):
    """
    Provides an Archipelago Hint for locations that tell you what item they give once you've gotten the in game hint.

    This includes the Oak's Aides, Bicycle Shop, Shops, and Pokemon Request Locations.
    """
    display_name = "Provide Hints"
    default = 0
    option_off = 0
    option_progression = 1
    option_progression_and_useful = 2
    option_all = 3


class PokemonFRLGDeathLink(DeathLink):
    __doc__ = DeathLink.__doc__ + "\n\n    In Pokemon FireRed/LeafGreen, whiting out sends a death and receiving a death causes you to white out."


@dataclass
class PokemonFRLGOptions(PerGameCommonOptions):
    game_version: GameVersion

    goal: Goal
    skip_elite_four: SkipEliteFour
    kanto_only: KantoOnly
    random_starting_town: RandomStartingTown
    starting_town_blacklist: StartingTownBlacklist
    shuffle_pokemon_centers: ShufflePokemonCenterEntrances
    shuffle_gyms: ShuffleGymEntrances
    shuffle_marts: ShuffleMartEntrances
    shuffle_harbors: ShuffleHarborEntrances
    shuffle_buildings: ShuffleBuildingEntrances
    shuffle_dungeons: ShuffleDungeonEntrances
    shuffle_interiors: ShuffleInteriorWarps
    shuffle_warp_tiles: ShuffleWarpTiles
    shuffle_dropdowns: ShuffleDropdowns
    mix_entrance_warp_pools: MixEntranceWarpPools
    decouple_entrances_warps: DecoupleEntrancesWarps
    randomize_fly_destinations: RandomizeFlyDestinations
    fly_destination_plando: FlyDestinationPlando

    shuffle_badges: ShuffleBadges
    shuffle_hidden: ShuffleHiddenItems
    extra_key_items: ExtraKeyItems
    shopsanity: Shopsanity
    vending_machines: VendingMachines
    prizesanity: Prizesanity
    shop_slots: ShopSlots
    shop_prices: ShopPrices
    consistent_shop_prices: ConsistentShopPrices
    trainersanity: Trainersanity
    rematchsanity: Rematchsanity
    rematch_requirements: RematchRequirements
    dexsanity: Dexsanity
    famesanity: Famesanity
    shuffle_fly_unlocks: ShuffleFlyUnlocks
    pokemon_request_locations: PokemonRequestLocations
    shuffle_pokedex: ShufflePokedex
    shuffle_running_shoes: ShuffleRunningShoes
    shuffle_berry_pouch: ShuffleBerryPouch
    shuffle_tm_case: ShuffleTMCase
    shuffle_jumping_shoes: ShuffleJumpingShoes
    post_goal_locations: PostGoalLocations
    card_key: CardKey
    island_passes: IslandPasses
    fishing_rods: FishingRods
    split_teas: SplitTeas
    gym_keys: GymKeys

    itemfinder_required: ItemfinderRequired
    flash_required: FlashRequired
    fame_checker_required: FameCheckerRequired
    bicycle_requires_jumping_shoes: BicycleRequiresJumpingShoes
    acrobatic_bicycle: AcrobaticBicycle
    evolutions_required: EvolutionsRequired
    evolution_methods_required: EvolutionMethodsRequired
    viridian_city_roadblock: ViridianCityRoadblock
    pewter_city_roadblock: PewterCityRoadblock
    modify_world_state: ModifyWorldState
    additional_dark_caves: AdditionalDarkCaves
    remove_badge_requirement: RemoveBadgeRequirement

    oaks_aide_route_2: OaksAideRoute2
    oaks_aide_route_10: OaksAideRoute10
    oaks_aide_route_11: OaksAideRoute11
    oaks_aide_route_16: OaksAideRoute16
    oaks_aide_route_15: OaksAideRoute15
    fossil_count: PokemonLabFossilCount

    viridian_gym_requirement: ViridianGymRequirement
    viridian_gym_count: ViridianGymCount
    route22_gate_requirement: Route22GateRequirement
    route22_gate_count: Route22GateCount
    route23_guard_requirement: Route23GuardRequirement
    route23_guard_count: Route23GuardCount
    elite_four_requirement: EliteFourRequirement
    elite_four_count: EliteFourCount
    elite_four_rematch_count: EliteFourRematchCount
    cerulean_cave_requirement: CeruleanCaveRequirement
    cerulean_cave_count: CeruleanCaveCount

    level_scaling: LevelScaling
    modify_trainer_levels: ModifyTrainerLevels
    force_fully_evolved: ForceFullyEvolved

    wild_pokemon: RandomizeWildPokemon
    wild_pokemon_groups: WildPokemonGroups
    wild_pokemon_blacklist: WildPokemonBlacklist
    starters: RandomizeStarters
    starter_blacklist: StarterBlacklist
    trainers: RandomizeTrainerParties
    trainer_blacklist: TrainerPartyBlacklist
    legendary_pokemon: RandomizeLegendaryPokemon
    legendary_pokemon_blacklist: LegendaryPokemonBlacklist
    misc_pokemon: RandomizeMiscPokemon
    misc_pokemon_blacklist: MiscPokemonBlacklist
    types: RandomizeTypes
    abilities: RandomizeAbilities
    ability_blacklist: AbilityBlacklist
    moves: RandomizeMoves
    move_match_type_bias: MoveMatchTypeBias
    move_normal_type_bias: MoveNormalTypeBias
    move_blacklist: MoveBlacklist
    base_stats: RandomizeBaseStats
    physical_special_split: PhysicalSpecialSplit
    move_types: RandomizeMoveTypes
    damage_categories: RandomizeDamageCategories
    hm_compatibility: HmCompatibility
    tm_tutor_compatibility: TmTutorCompatibility
    tm_tutor_moves: TmTutorMoves
    tm_tutor_moves_blacklist: TmTutorMoveBlacklist

    reusable_tm_tutors: ReusableTmsTutors
    min_catch_rate: MinCatchRate
    all_pokemon_seen: AllPokemonSeen
    starting_money: StartingMoney
    better_shops: BetterShops
    free_fly_location: FreeFlyLocation
    free_fly_blacklist: FreeFlyBlacklist
    town_map_fly_location: TownMapFlyLocation
    town_map_fly_blacklist: TownMapFlyBlacklist

    remote_items: RemoteItems
    randomize_music: RandomizeMusic
    randomize_fanfares: RandomizeFanfares
    game_options: GameOptions
    provide_hints: ProvideHints

    death_link: PokemonFRLGDeathLink
