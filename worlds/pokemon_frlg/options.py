"""
Option definitions for Pokémon FireRed/LeafGreen
"""
from dataclasses import dataclass
from schema import Optional, Schema, And, Use
from Options import (Choice, DeathLink, DefaultOnToggle, NamedRange, OptionDict, OptionSet, PerGameCommonOptions, Range,
                     Toggle)
from .data import data, ability_name_map, fly_blacklist_map, fly_plando_maps, move_name_map, starting_town_blacklist_map


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


class DungeonEntranceShuffle(Choice):
    """
    Shuffles dungeon entrances.

    - Off: Dungeon entrances are not shuffled
    - Simple: Single entrance dungeons and multi entrance dungeons are shuffled separately from each other. Both entrances for multi entrance dungeons will connect to the same dungeon
    - Restricted: Single entrance dungeons and multi entrance dungeons are shuffled separately from each other. Both entrances for multi entrance dungeons do not need to lead to the same dungeon
    - Full: All dungeon entrances are shuffled together
    """
    display_name = "Dungeon Entrance Shuffle"
    default = 0
    option_off = 0
    option_simple = 1
    option_restricted = 2
    option_full = 3


class RandomizeFlyDestinations(Toggle):
    """
    Randomizes where each fly point takes you. The new fly destinations can be almost any outdoor warp point in the
    game with a few exceptions (Cycling Road Gates for example).
    """
    display_name = "Randomize Fly Destinations"


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
    """
    display_name = "Shopsanity"


class ShopPrices(Choice):
    """
    Sets how Shop Item's prices are determined when Shopsanity is on.

    - Spheres: Shop prices are determined by sphere access
    - Classification: Shop prices are determined by item classifications (Progression, Useful, Filler/Trap)
    - Spheres and Classifications: Shop prices are determined by both sphere access and item classifications
    - Completely Random: Shop prices will be completely random
    """
    display_name = "Shop Prices"
    default = 2
    option_spheres = 0
    option_classification = 1
    option_spheres_and_classification = 2
    option_completely_random = 3


class MinimumShopPrice(Range):
    """
    Sets the minimum cost of Shop Items when Shopsanity is on.
    """
    display_name = "Minimum Shop Price"
    default = 100
    range_start = 1
    range_end = 9999


class MaximumShopPrice(Range):
    """
    Sets the maximum cost of Shop Items when Shopsanity is on.
    """
    display_name = "Maximum Shop Price"
    default = 3000
    range_start = 1
    range_end = 9999


class Trainersanity(NamedRange):
    """
    Defeating a trainer gives you an item.

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
    """
    display_name = "Modify World State"
    valid_keys = ["Modify Route 2", "Remove Cerulean Roadblocks", "Block Tunnels", "Modify Route 9",
                  "Modify Route 10", "Block Tower", "Route 12 Boulders", "Modify Route 12", "Modify Route 16",
                  "Open Silph", "Remove Saffron Rockets", "Route 23 Trees", "Modify Route 23", "Victory Road Rocks",
                  "Early Gossipers", "Total Darkness", "Block Vermilion Sailing"]


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
    range_start = 1
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
    Prevents species from learning these moves via learnsets, TMs, and move tutors.

    Has no effect is moves are not randomized.
    """
    display_name = "Move Blacklist"
    valid_keys = sorted(move_name_map.keys())


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
    range_start = 0
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
    range_start = 0
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


class ExpModifier(Range):
    """
    Sets the EXP multiplier that is used when the in game option for experience is set to Custom.

    100 is default
    50 is half
    200 is double
    etc.
    """
    display_name = "Exp Modifier"
    range_start = 1
    range_end = 1000
    default = 100


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
    Shuffles fanfares for item pickups, healing at the pokecenter, etc.
    """
    display_name = "Randomize Fanfares"


class GameOptions(OptionDict):
    """
    Allows you to preset the in game options.
    The available options and their allowed values are the following:

    - Auto Run: Off, On
    - Battle Scene: Off, On
    - Battle Style: Shift, Set
    - Bike Music: Off, On
    - Blind Trainers: Off, On
    - Button Mode: Help, LR, L=A
    - Encounter Rates: Vanilla, Normalized
    - Experience: None, Half, Normal, Double, Triple, Quadruple, Custom
    - Frame: 1-10
    - Guaranteed Catch: Off, On
    - Item Messages: All, Progression, None
    - Low HP Beep: Off, On
    - Show Effectiveness: Off, On
    - Skip Fanfares: Off, On
    - Sound: Mono, Stereo
    - Surf Music: Off, On
    - Text Speed: Slow, Mid, Fast, Instant
    - Turbo A: Off, On
    """
    display_name = "Game Options"
    default = {"Text Speed": "Instant", "Turbo A": "Off", "Auto Run": "Off", "Button Mode": "Help", "Frame": 1,
               "Battle Scene": "On", "Battle Style": "Shift", "Show Effectiveness": "On", "Experience": "Custom",
               "Sound": "Mono", "Low HP Beep": "On", "Skip Fanfares": "Off", "Bike Music": "On", "Surf Music": "On",
               "Guaranteed Catch": "Off", "Encounter Rates": "Vanilla", "Blind Trainers": "Off",
               "Item Messages": "Progression"}
    schema = Schema({
        "Text Speed": And(str, lambda s: s in ("Slow", "Mid", "Fast", "Instant")),
        "Turbo A": And(str, lambda s: s in ("Off", "On")),
        "Auto Run": And(str, lambda s: s in ("Off", "On")),
        "Button Mode": And(str, lambda s: s in ("Help", "LR", "L=A")),
        "Frame": And(Use(int), lambda n: 1 <= n <= 10),
        "Battle Scene": And(str, lambda s: s in ("Off", "On")),
        "Battle Style": And(str, lambda s: s in ("Shift", "Set")),
        "Show Effectiveness": And(str, lambda s: s in ("Off", "On")),
        "Experience": And(str, lambda s: s in ("None", "Half", "Normal", "Double", "Triple", "Quadruple", "Custom")),
        "Sound": And(str, lambda s: s in ("Mono", "Stereo")),
        "Low HP Beep": And(str, lambda s: s in ("Off", "On")),
        "Skip Fanfares": And(str, lambda s: s in ("Off", "On")),
        "Bike Music": And(str, lambda s: s in ("Off", "On")),
        "Surf Music": And(str, lambda s: s in ("Off", "On")),
        "Guaranteed Catch": And(str, lambda s: s in ("Off", "On")),
        "Encounter Rates": And(str, lambda s: s in ("Vanilla", "Normalized")),
        "Blind Trainers": And(str, lambda s: s in ("Off", "On")),
        "Item Messages": And(str, lambda s: s in ("All", "Progression", "None"))
    })


class ProvideHints(Toggle):
    """
    Provides an Archipelago Hint for locations that tell you what item they give once you've gotten the in game hint.

    This includes the Oak's Aides, Bicycle Shop, and Pokemon Request Locations.
    """
    display_name = "Provide Hints"


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
    dungeon_entrance_shuffle: DungeonEntranceShuffle
    randomize_fly_destinations: RandomizeFlyDestinations
    fly_destination_plando: FlyDestinationPlando

    shuffle_badges: ShuffleBadges
    shuffle_hidden: ShuffleHiddenItems
    extra_key_items: ExtraKeyItems
    shopsanity: Shopsanity
    shop_prices: ShopPrices
    minimum_shop_price: MinimumShopPrice
    maximum_shop_price: MaximumShopPrice
    trainersanity: Trainersanity
    dexsanity: Dexsanity
    famesanity: Famesanity
    shuffle_fly_unlocks: ShuffleFlyUnlocks
    pokemon_request_locations: PokemonRequestLocations
    shuffle_running_shoes: ShuffleRunningShoes
    shuffle_berry_pouch: ShuffleBerryPouch
    shuffle_tm_case: ShuffleTMCase
    card_key: CardKey
    island_passes: IslandPasses
    split_teas: SplitTeas
    gym_keys: GymKeys

    itemfinder_required: ItemfinderRequired
    flash_required: FlashRequired
    fame_checker_required: FameCheckerRequired
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
    misc_pokemon: RandomizeMiscPokemon
    types: RandomizeTypes
    abilities: RandomizeAbilities
    ability_blacklist: AbilityBlacklist
    moves: RandomizeMoves
    move_match_type_bias: MoveMatchTypeBias
    move_normal_type_bias: MoveNormalTypeBias
    move_blacklist: MoveBlacklist
    physical_special_split: PhysicalSpecialSplit
    move_types: RandomizeMoveTypes
    damage_categories: RandomizeDamageCategories
    hm_compatibility: HmCompatibility
    tm_tutor_compatibility: TmTutorCompatibility
    tm_tutor_moves: TmTutorMoves

    reusable_tm_tutors: ReusableTmsTutors
    min_catch_rate: MinCatchRate
    all_pokemon_seen: AllPokemonSeen
    exp_modifier: ExpModifier
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
