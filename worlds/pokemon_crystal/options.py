from collections.abc import Hashable
from dataclasses import dataclass
from typing import Type, override

from BaseClasses import PlandoOptions
from Options import Toggle, Choice, DefaultOnToggle, Range, PerGameCommonOptions, NamedRange, OptionSet, \
    StartInventoryPool, OptionDict, Visibility, DeathLink, OptionGroup, OptionList, FreeText, OptionError
from .data import data, MapPalette, MiscOption
from .maps import FLASH_MAP_GROUPS
from ..AutoWorld import World


class EnhancedOptionSet(OptionSet):

    def __init__(self, value):
        if isinstance(value, list):
            value = [x.title() if x.title() in ('_All', '_Random') else x for x in value]

            if "_All" in value:
                value = [k for k in self.valid_keys if not k.startswith("_")]

        super().__init__(value)

    def __init_subclass__(cls, **kwargs):
        super.__init_subclass__()
        cls.valid_keys += ["_Random", "_All"]
        cls._valid_keys = frozenset(set(cls.valid_keys) | {"_Random", "_All"})


class Goal(Choice):
    """
    Elite Four: Defeat the Champion and enter the Hall of Fame
    Red: Defeat Red in Mt. Silver
    Diploma: Catch all logically available Pokemon and receive the diploma in Celadon City
    Rival: Win all possible rival battles
    Defeat Team Rocket: Vanquish Team Rocket in Slowpoke Well, Mahogany Town, Radio Tower and defeat the grunt
    on Route 24 (if Kanto is accessible)
    Unown Hunt: Catch all 26 Unown forms that are attached to signs across the region(s) and show the completed Unown dex
     to the scientist in Ruins of Alph. In order to encounter the Unown you'll need to solve their corresponding tile puzzle.
     Each puzzle requires 16 pieces which must be found first.
    """
    display_name = "Goal"
    default = 0
    option_elite_four = 0
    option_red = 1
    option_diploma = 2
    option_rival = 3
    option_defeat_team_rocket = 4
    option_unown_hunt = 5


class JohtoOnly(Choice):
    """
    Excludes all of Kanto, disables Kanto access
    Forces Goal to Elite Four unless Silver Cave is included
    Goal badges will be limited to 8 if badges are shuffled or vanilla
    """
    display_name = "Johto Only"
    default = 0
    option_off = 0
    option_on = 1
    option_include_silver_cave = 2


class EliteFourRequirement(Choice):
    """
    Sets the requirement to pass the Victory Road badge check
    """
    display_name = "Elite Four Requirement"
    default = 0
    option_badges = 0
    option_gyms = 1
    option_johto_badges = 2


class EliteFourCount(Range):
    """
    Sets the number of badges/gyms required to enter Victory Road

    This will be limited to 8 if the requirement is Johto Badges
    """
    display_name = "Elite Four Count"
    default = 8
    range_start = 0
    range_end = 16


class RedRequirement(Choice):
    """
    Sets the requirement to battle Red
    """
    display_name = "Red Requirement"
    default = 0
    option_badges = 0
    option_gyms = 1


class RedCount(Range):
    """
    Number of badges/gyms required to battle Red
    """
    display_name = "Red Count"
    default = 16
    range_start = 0
    range_end = 16


class MtSilverRequirement(Choice):
    """
    Sets the requirement to access Mt. Silver and Silver Cave
    """
    display_name = "Mt. Silver Requirement"
    default = 0
    option_badges = 0
    option_gyms = 1


class MtSilverCount(Range):
    """
    Number of badges/gyms required to access Mt. Silver and Silver Cave
    """
    display_name = "Mt. Silver Count"
    default = 16
    range_start = 0
    range_end = 16


class RadioTowerRequirement(Choice):
    """
    Sets the requirement for Team Rocket to take over the Goldenrod Radio Tower
    """
    display_name = "Radio Tower Requirement"
    default = 0
    option_badges = 0
    option_gyms = 1


class RadioTowerCount(Range):
    """
    Number of badges/gyms at which Team Rocket takes over the Goldenrod Radio Tower
    """
    display_name = "Radio Tower Count"
    default = 7
    range_start = 0
    range_end = 16


class Route44AccessRequirement(Choice):
    """
    Sets the requirement to pass between Mahogany Town and Route 44
    """
    display_name = "Route 44 Access Requirement"
    default = 0
    option_badges = 0
    option_gyms = 1


class Route44AccessCount(Range):
    """
    Sets the number of badges/gyms required to pass between Mahogany Town and Route 44
    """
    display_name = "Route 44 Access Count"
    default = 7
    range_start = 0
    range_end = 16


class MagnetTrainAccess(Choice):
    """
    Sets the requirement to ride the Magnet Train

    - Pass requires only the Pass
    - Pass and Power requires the Pass and restoring power to Kanto by returning the Machine Part
    """
    display_name = "Magnet Train Access"
    default = 0
    option_pass = 0
    option_pass_and_power = 1


class RandomizeStartingTown(Toggle):
    """
    Randomly chooses a town to start in.
    Any Pokemon Center except Indigo Plateau, Cinnabar Island and Silver Cave can be chosen.
    Lake of Rage can also be chosen.

    Other settings may additionally restrict which Pokemon Centers can be chosen.

    WARNING: Some starting towns without level scaling may produce difficult starts.
    """
    display_name = "Randomize Starting Town"


class StartingTownBlocklist(OptionSet):
    """
    Specify places which cannot be chosen as a starting town. If you block every valid option, this list will do
    nothing.
    Indigo Plateau, Cinnabar Island and Silver Cave cannot be chosen as starting towns and are not valid options
    "_Johto" and "_Kanto" are shortcuts for all Johto and Kanto towns respectively
    """
    display_name = "Starting Town Blocklist"
    valid_keys = sorted(town.name for town in data.starting_towns) + ["_Johto", "_Kanto"]


class VanillaClair(Toggle):
    """
    Clair refuses to give you the Rising Badge until you prove your worth
    to the Elders in the Dragon's Den Shrine, which requires Whirlpool to access.
    """
    display_name = "Vanilla Clair"


class RandomizeBadges(Choice):
    """
    Shuffles gym badge locations into the pool
    - Vanilla: Does not randomize gym badges
    - Shuffle: Randomizes gym badges between gym leaders
    - Completely Random: Randomizes badges with all other items
    """
    display_name = "Randomize Badges"
    default = 2
    option_vanilla = 0
    option_shuffle = 1
    option_completely_random = 2


class RandomizeHiddenItems(Toggle):
    """
    Shuffles hidden item locations into the pool
    """
    display_name = "Randomize Hidden Items"


class RequireItemfinder(Choice):
    """
    Hidden items require Itemfinder in logic

    - Not Required: Hidden items do not require the Itemfinder at all
    - Logically Required: Hidden items will expect you to have Itemfinder for logic but can be picked up without it
    - Hard Required: Hidden items cannot be picked up without the Itemfinder
    """
    display_name = "Require Itemfinder"
    default = 1
    option_not_required = 0
    option_logically_required = 1
    option_hard_required = 2


class ItemPoolFill(Choice):
    """
    Changes how non-progression items are put into the pool.

    - Vanilla: item pool filled similarly to vanilla.
    - Balanced: all filler items uniformly randomized.
    - Youngster: item pool filled with items reflecting that of a young trainer.
    - Cooltrainer: item pool filled with items reflecting that of a cooltrainer.
    - Shuckle: item pool filled with items reflecting that of a Shuckle.
    """
    display_name = "Item Pool Fill"
    default = 0
    option_vanilla = 0
    option_balanced = 1
    option_youngster = 2
    option_cooltrainer = 3
    option_shuckle = 4


class AddMissingUsefulItems(Toggle):
    """
    Adds useful items which are unobtainable to the pool, these replace filler
    """
    display_name = "Add Missing Useful Items"


class Route32Condition(Choice):
    """
    Sets the condition required to pass between the north and south parts of Route 32
    - Egg from aide: Collect the Egg from the aide in the Violet City Pokemon Center after beating Falkner
    - Any badge: Obtain any badge
    - Any gym: Beat any gym
    - Zephyr Badge: Obtain the Zephyr Badge
    - None: No requirement
    """
    display_name = "Route 32 Access Condition"
    default = 0
    option_egg_from_aide = 0
    option_any_badge = 1
    option_any_gym = 2
    option_zephyr_badge = 3
    option_none = 4


class KantoAccessRequirement(Choice):
    """
    Sets the requirement to pass between Victory Road gate and Kanto
    - Wake Snorlax: Wake the Snorlax outside of Diglett's Cave
    - Badges: Requires the number of badges specified by kanto_access_count
    - Gyms: Requires beating the number of gyms specified by kanto_access_count
    - Become Champion: Defeat Lance and enter the Hall of Fame

    This setting does nothing if Johto Only is enabled
    """
    display_name = "Kanto Access Requirement"
    default = 0
    option_wake_snorlax = 0
    option_badges = 1
    option_gyms = 2
    option_become_champion = 3


class KantoAccessCount(Range):
    """
    Sets the number of badges/gyms required to pass between Victory Road gate and Kanto
    Only applies if Kanto Access Condition is set to badges or gyms
    """
    display_name = "Kanto Access Count"
    default = 8
    range_start = 0
    range_end = 16


class DarkAreas(EnhancedOptionSet):
    """
    Sets which areas are dark until Flash is used

    - _All includes all areas
    - _Random has a 50% chance to include each area that is not already included
    """
    display_name = "Dark Areas"
    default = sorted(area for area, maps in FLASH_MAP_GROUPS.items() if data.maps[maps[0]].palette is MapPalette.Dark)
    valid_keys = sorted(area for area in FLASH_MAP_GROUPS.keys())

    __doc__ = __doc__ + "\nAllowed areas: " + ", ".join(valid_keys)


class RedGyaradosAccess(Choice):
    """
    Sets the access requirement for the red Gyarados
    - Vanilla requires Surf
    - Whirlpool requires Surf and Whirlpool
    - Shore requires nothing
    """
    display_name = "Red Gyarados Access"
    default = 0
    option_vanilla = 0
    option_whirlpool = 1
    option_shore = 2


class Route2Access(Choice):
    """
    Sets the roadblock for moving between the west of Route 2 and Diglett's cave
    - Vanilla: Cut is required
    - Ledge: A ledge is added north of Diglett's cave allowing east -> west access without Cut
    - Open: No requirement
    """
    display_name = "Route 2 Access"
    default = 1
    option_vanilla = 0
    option_ledge = 1
    option_open = 2


class Route3Access(Choice):
    """
    Sets the roadblock for moving between Pewter City and Route 3
    - Vanilla: No requirement
    - Boulder Badge: The Boulder Badge is required to pass
    """
    display_name = "Route 3 Access"
    default = 0
    option_vanilla = 0
    option_boulder_badge = 1


class BlackthornDarkCaveAccess(Choice):
    """
    Sets the roadblock for travelling from Route 31 to Blackthorn City through Dark Cave
    - Vanilla: Traversal is not possible
    - Waterfall: A waterfall is added to the Violet side of Dark Cave and a ledge is removed on the Blackthorn side,
    allowing passage with Flash, Surf and Waterfall
    """
    display_name = "Blackthorn Dark Cave Access"
    default = 0
    option_vanilla = 0
    option_waterfall = 1


class NationalParkAccess(Choice):
    """
    Sets the requirement to enter National Park
    - Vanilla: No requirement
    - Bicycle: The Bicycle is required
    """
    display_name = "National Park Access"
    default = 0
    option_vanilla = 0
    option_bicycle = 1


class Route42Access(Choice):
    """
    Sets the requirement to traverse the water on Route 42
    - Vanilla: Route 42 can be traversed with Surf
    - Whirlpool: Access to Central Route 42 is blocked by a whirlpool
    - Blocked: Access to Central Route 42 is completely blocked, requiring going through Mount Mortar instead.
    Mount Mortar 1F gets an extra map connection between the Inside and Central Outside
    - Whirlpool Open Mortar: Route 42 has whirlpools and Mount Mortar 1F has the extra map connection.
    """
    display_name = "Route 42 Access"
    default = 0
    option_vanilla = 0
    option_whirlpool = 1
    option_blocked = 2
    option_whirlpool_open_mortar = 3


class MountMortarAccess(Choice):
    """
    Sets the requirement to pass through Mount Mortar east <> west
    - Vanilla: No requirement
    - Rock Smash: Rock Smash is required
    """
    display_name = "Mount Mortar Access"
    default = 0
    option_vanilla = 0
    option_rock_smash = 1


class VictoryRoadAccess(Choice):
    """
    Sets the requirement to pass through Victory Road to Indigo Plateau
    - Vanilla: No requirement
    - Strength: Strength is required
    """
    display_name = "Victory Road Access"
    default = 0
    option_vanilla = 0
    option_strength = 1


class Route12Access(Choice):
    """
    Sets the requirement to pass between the north and south parts of Route 12
    - Vanilla: No requirement
    - Weird Tree: Requires Squirtbottle

    The roadblock is north of the path to Route 11 and can be bypassed with Surf
    """
    display_name = "Route 12 Access"
    default = 0
    option_vanilla = 0
    option_weird_tree = 1


class SSAquaAccess(Choice):
    """
    Sets the requirement to sail on the S.S. Aqua
    - Vanilla: S.S. Ticket is required
    - Lighthouse and Ticket: Healing Amphy in the Olivine lighthouse and the S.S Ticket are required
    """
    display_name = "S.S. Aqua Access"
    default = 0
    option_vanilla = 0
    option_lighthouse_and_ticket = 1


class Route30Battle(Choice):
    """
    Sets which directions the battle on Route 30 blocks
    """
    display_name = "Route 30 Battle"
    default = 0
    option_blocks_northbound = 0
    option_blocks_both = 1


class JohtoTrainersanity(NamedRange):
    """
    Adds checks for defeating Johto trainers.

    You can turn trainers that have checks grayscale by setting the "trainersanity_indication" in-game option.

    Trainers are no longer missable. Each trainer will add a random filler item into the pool.
    """
    display_name = "Johto Trainersanity"
    default = 0
    range_start = 0
    range_end = len([loc_id for loc_id, loc_data in data.locations.items() if
                     "Trainersanity" in loc_data.tags and "Johto" in loc_data.tags])
    special_range_names = {
        "none": 0,
        "full": range_end
    }


class KantoTrainersanity(NamedRange):
    """
    Adds checks for defeating Kanto trainers.

    You can turn trainers that have checks grayscale by setting the "trainersanity_indication" in-game option.

    Trainers are no longer missable. Each trainer will add a random filler item into the pool.
    """
    display_name = "Kanto Trainersanity"
    default = 0
    range_start = 0
    range_end = len([loc_id for loc_id, loc_data in data.locations.items() if
                     "Trainersanity" in loc_data.tags and "Johto" not in loc_data.tags])
    special_range_names = {
        "none": 0,
        "full": range_end
    }


class Rematchsanity(Toggle):
    """
    Adds rematch fights to the level scaling pool
    Note: This is extremely beta, and the logic and patch aren't fully fleshed out.
    This means that the game requires you beat the rematches in vanilla order,
    but the ap logic might have them in a different order, so earlier rematches might
    be higher level than later ones.
    """
    display_name = "Rematchsanity"
    visibility = Visibility.none


class Dexsanity(NamedRange):
    """
    Adds checks for catching Pokemon
    Pokemon that cannot be logically obtained will never be included
    """
    display_name = "Dexsanity"
    default = 0
    range_start = 0
    range_end = 251
    special_range_names = {
        "none": default,
        "full": range_end
    }


class Dexcountsanity(NamedRange):
    """
    Adds checks for completing Pokedex milestones
    This setting specifies number of caught Pokemon on which you'll get your last check
    """
    display_name = "Dexcountsanity"
    default = 0
    range_start = 0
    range_end = 251
    special_range_names = {
        "none": default,
        "full": range_end
    }


class DexcountsanityStep(Range):
    """
    If Dexcountsanity is enabled, specifies the step interval at which your checks are placed.
    For example, if you have Dexcountsanity 50 and Dexcountsanity Step 10, you will have checks at
    10, 20, 30, 40 and 50 total Pokemon caught.
    """
    display_name = "Dexcountsanity Step"
    default = 1
    range_start = 1
    range_end = 251


class DexcountsanityLeniency(Range):
    """
    If Dexcountsanity is enabled, specifies the logic leniency for checks.
    For example, if you set Dexcountsanity Leniency to 5 and have a Dexcountsanity check at 10, you will not be
    logically required to obtain this check until you can obtain 15 Pokemon

    Checks that would go over the total number of logically available Pokemon will be clamped to that limit
    """
    display_name = "Dexcountsanity Leniency"
    default = 0
    range_start = 0
    range_end = 251


class DexsanityStarters(Choice):
    """
    Controls how Dexsanity treats starter Pokemon
    - Allow: Starter Pokemon will be allowed as Dexsanity checks
    - Block: Starter Pokemon will not be allowed as Dexsanity Checks
    - Available Early: Starter Pokemon will all be obtainable in the wild immediately, unless there is nowhere to obtain
    wild Pokemon immediately
    """
    display_name = "Dexsanity Starters"
    default = 0
    option_allow = 0
    option_block = 1
    option_available_early = 2


class WildEncounterMethodsRequired(EnhancedOptionSet):
    """
    Sets which wild encounter types may be logically required

    _Random has a 50% chance to include types which are not already included
    _All will include all types

    Swarms and roamers are NEVER in logic
    """
    display_name = "Wild Encounter Methods Required"
    valid_keys = ["Land", "Surfing", "Fishing", "Headbutt", "Rock Smash", "Bug Catching Contest"]
    default = ["Land", "Surfing", "Fishing", "Headbutt", "Rock Smash", "Bug Catching Contest"]


class EnforceWildEncounterMethodsLogic(Toggle):
    """
    Sets whether the game will prevent capture of Pokemon found through disabled wild encounter methods
    Statics, roamers and contest encounters can always be caught

    You can always re-catch Pokemon you have already caught
    """
    display_name = "Enforce Wild Encounter Methods Logic"


class EvolutionMethodsRequired(EnhancedOptionSet):
    """
    Sets which types of evolutions may be logically required

    _Random has a 50% chance to include types which are not already included
    _All will include all types
    """
    display_name = "Evolution Methods Required"
    valid_keys = ["Level", "Level Tyrogue", "Use Item", "Happiness"]
    default = ["Level", "Level Tyrogue", "Use Item", "Happiness"]


class StaticPokemonRequired(DefaultOnToggle):
    """
    Sets whether static Pokemon may be logically required
    """
    display_name = "Static Pokemon Required"


class TradesRequired(Toggle):
    """
    Specifies if in-game trades may be logically required
    """
    display_name = "Trades Required"


class BreedingMethodsRequired(Choice):
    """
    Specifies which breeding methods may be logically required.
    """
    display_name = "Breeding Method Required"
    default = 1
    option_none = 0
    option_with_ditto = 1
    option_any = 2


class EvolutionGymLevels(Range):
    """
    Sets how many levels each accessible gym puts into logic for level (and Tyrogue) evolutions

    For example, if you set this to 4 and have access to 5 gyms, evolutions up to level 20 would be in logic.

    If Johto only is enabled the minimum for this setting is 8.
    """
    display_name = "Evolution Gym Levels"
    default = 8
    range_start = 4
    range_end = 69


class Shopsanity(EnhancedOptionSet):
    """
    Adds shop purchases as locations, items in shops are added to the item pool
    - Johto Marts: Adds Johto Poke Marts, including the Goldenrod Dept. Store.
    - Kanto Marts: Adds Kanto Poke Marts, including the Celadon Dept. Store.
    - Blue Card: Adds the Blue Card prize shop, accessing this shop requires the Blue Card and buying items requires
    points. Five Blue Card Points are added to the item pool. Points are not spent when purchasing.
    - Game Corners: The Game Corner TM shops are added.
    - Apricorns: Kurt's Apricorn Ball shop is added, each slot requires a different Apricorn. Apricorns are progression.
    - _All: Includes all valid options.
    - _Random: Each option that is not included has a 50% chance to be additionally included.

    IMPORTANT NOTE: There is a non-randomized shop on Pokecenter 2F, you can always buy Poke Balls and Escape Ropes there.
    """
    display_name = "Shopsanity"
    default = []

    johto_marts = "Johto Marts"
    kanto_marts = "Kanto Marts"
    blue_card = "Blue Card"
    apricorns = "Apricorns"
    game_corners = "Game Corners"

    valid_keys = [johto_marts, kanto_marts, blue_card, apricorns, game_corners]


class ShopsanityPrices(Choice):
    """
    Sets how shop item prices are determined when Shopsanity is enabled
    - Vanilla: Shop prices are unchanged
    - Item Price: Shop prices are determined by the value of the item being sold
    - Spheres: Shop prices are determined by sphere access
    - Classification: Shop prices are determined by item classifications (Progression, Useful, Filler/Trap)
    - Spheres and Classifications: Shop prices are determined by both sphere access and item classifications
    - Completely Random: Shop prices will be completely random
    """
    display_name = "Shopsanity Prices"
    default = 0
    option_vanilla = 0
    option_item_price = 1
    option_spheres = 2
    option_classification = 3
    option_spheres_and_classification = 4
    option_completely_random = 5


class MinimumShopsanityPrice(Range):
    """
    Sets the minimum cost of shop items when Shopsanity is enabled
    """
    display_name = "Minimum Shopsanity Price"
    default = 100
    range_start = 0
    range_end = 10000


class MaximumShopsanityPrice(Range):
    """
    Sets the maximum cost of shop items when Shopsanity is enabled
    """
    display_name = "Maximum Shopsanity Price"
    default = 3000
    range_start = 0
    range_end = 10000


class ProvideShopHints(Choice):
    """
    Sends out hints when a randomized shop is accessed
    """
    display_name = "Provide Shop Hints"
    default = 0
    option_off = 0
    option_progression = 1
    option_progression_and_useful = 2
    option_all = 3


class ShopsanityRestrictRareCandies(Toggle):
    """
    Makes Rare Candies in shops only purchasable once
    """
    display_name = "Shopsanity Restrict Rare Candies"


class ShopsanityXItems(Choice):
    """
    Determines how Shopsanity treats X Items
    - Anywhere: X Items will be shuffled into the multiworld pool
    - Any Shop: At least one of each X Item will be available for purchase in a local shop

    NOTE: You cannot purchase any shop item repeatedly when Remote Items is active
    """
    display_name = "Shopsanity X Items"
    default = 0
    option_anywhere = 0
    option_any_shop = 1


class RandomizePokegear(Toggle):
    """
    Shuffles the Pokegear and cards into the pool
    """
    display_name = "Randomize Pokegear"


class RandomizeBerryTrees(Toggle):
    """
    Shuffles berry tree locations into the pool
    """
    display_name = "Randomize Berry Trees"


class RandomizePokemonRequests(Choice):
    """
    Shuffles the items given by Bill's Grandpa after showing him specific Pokemon into the pool, as well as the reward
    for showing a Magikarp to the fisher in the house at Lake of Rage

    Optionally also randomizes the requested Pokemon, except the Magikarp

    Trainers which need you to show them a Pokemon to get their phone number require both this option and Randomize Phone Call Items to be enabled.
    """
    display_name = "Randomize Pokemon Requests"
    default = 0
    option_off = 0
    option_items = 1
    option_pokemon = 2
    option_items_and_pokemon = 3


class RandomizeFlyUnlocks(Choice):
    """
    Shuffles Fly destination unlocks into the pool

    Indigo Plateau is not included.
    """
    display_name = "Randomize Fly Unlocks"
    default = 0
    option_off = 0
    option_on = 1
    option_exclude_silver_cave = 2


class RandomizeBugCatchingContest(Choice):
    """
    Shuffles the bug catching contest prizes into the pool
    - All: shuffles all prizes into the pool. WARNING: It can be very difficult to get second or third place.
    - Combine second and third: Combines second and third place into a single prize. Shuffles 1st, 2nd+3rd and 4th.
    - Participate: Shuffles a single participation award into the pool, which is obtained by completing the contest.
    """
    display_name = "Randomize Bug Catching Contest"
    default = 0
    option_off = 0
    option_all = 1
    option_combine_second_third = 2
    option_participate = 3


class RandomizePhoneCalls(Choice):
    """
    Shuffles items given by trainers after registering their phone numbers into the pool
    - On Vanilla: Trainers will only call you and allow you to call them at specific times and after their
      condition has been met. Whether the correct phone call triggers can be random depending on the trainer.
      IMPORTANT: Triggering phone calls this way can require resetting the clock, toggling DST and a lot of patience.

    - On Simple: Trainers will allow you to call them for their item any time after their condition has been met.
      They will always have an item ready in this case.

    The Pokegear is required to register trainer phone numbers and the Phone Card is required to make and receive calls.

    Trainers that need you to show them a Pokemon require both this option and Randomize Pokemon Requests to be enabled.
    """
    display_name = "Randomize Phone Calls"
    default = 0
    option_off = 0
    option_on_vanilla = 1
    option_on_simple = 2


class RandomizeStarters(Choice):
    """
    Randomizes species of starter Pokemon
    """
    display_name = "Randomize Starters"
    default = 0
    option_vanilla = 0
    option_unevolved_only = 1
    option_completely_random = 2
    option_first_stage_can_evolve = 3
    option_base_stat_mode = 4


class StarterBlocklist(OptionSet):
    """
    These Pokemon will not be chosen as starter Pokemon
    Does nothing if starter Pokemon are not randomized
    You can use "_Legendaries" as a shortcut for all legendary Pokemon
    Blocklists are best effort, other constraints may cause them to be ignored
    """
    display_name = "Starter Blocklist"
    valid_keys = sorted(pokemon.friendly_name for pokemon in data.pokemon.values()) + ["_Legendaries"]


class StarterBST(NamedRange):
    """
    If you chose Base Stat Mode for your starters, what is the average base stat total you want your available starters to be?
    """
    display_name = "Starter BST Range"
    default = 310
    range_start = 195
    range_end = 680
    special_range_names = {
        "normal_starters": 310
    }


class RandomizeWilds(Choice):
    """
    Randomizes species of wild Pokemon

    Base Forms: Ensures that at least every Pokemon that cannot be obtained through evolution is available in the wild
    Evolution Lines: Ensures that at least one Pokemon from each evolutionary line can be obtained in the wild
    Catch 'em All: Ensures that every Pokemon will be obtainable in the wild

    If this setting is anything other than vanilla, bug catching contest encounters will be completely random.
    """
    display_name = "Randomize Wilds"
    default = 0
    option_vanilla = 0
    option_completely_random = 1
    option_base_forms = 2
    option_evolution_lines = 3
    option_catch_em_all = 4


class WildEncounterBlocklist(OptionSet):
    """
    These Pokemon will not appear in the wild
    Does nothing if wild Pokemon are not randomized
    You can use "_Legendaries" as a shortcut for all legendary Pokemon
    Blocklists are best effort, other constraints may cause them to be ignored
    This setting does not affect the bug catching contest.
    """
    display_name = "Wild Encounter Blocklist"
    valid_keys = sorted(pokemon.friendly_name for pokemon in data.pokemon.values()) + ["_Legendaries"]


class EncounterGrouping(Choice):
    """
    Determines how randomized wild Pokemon are grouped in encounter tables.

    - All Split: Each encounter area will have each slot randomized separately. For example, grass areas will have seven
    randomized encounter slots.
    - One to One: Each encounter area will retain its vanilla slot grouping. For example, if an area has two encounters
    in vanilla, it will be randomized as two slots.
    - One per Method: Each encounter method on a route will be treated as a single slot. For example, the grass on a route
    will contain only a single encounter. Each rod is a separate encounter.

    This setting has no effect if wild Pokemon are not randomized.
    This setting does not affect the bug catching contest.
    """
    display_name = "Encounter Grouping"
    default = 0
    option_all_split = 0
    option_one_to_one = 1
    option_one_per_method = 2


class ForceFullyEvolved(NamedRange):
    """
    When an opponent uses a Pokemon of the specified level or higher, restricts the species to only fully evolved Pokemon.

    Only applies when trainer parties are randomized.
    """
    display_name = "Force Fully Evolved"
    range_start = 0
    range_end = 100
    default = 0
    special_range_names = {
        "disabled": 0
    }


class EncounterSlotDistribution(Choice):
    """
    Sets how the Pokemon encounter slots in an area are distributed.

    Remove 1%'s modifies grass/cave encounters to 30%/25%/20%/10%/5%/5%/5% and does not modify any others.
    Balanced sets the following:
        Grass/Cave: 20%/20%/15%/15%/10%/10%/10%
        Surf (unchanged): 60%/30%/10%
        Headbutt:  20%/20%/20%/15%/15%/10%
        Rock Smash: 70%/30%
        Fishing (unchanged):
            Old Rod: 70%/15%/15%
            Good Rod: 35%/35%/20%/10%
            Super Rod: 40%/30%/20%/10%
        Bug Catching Contest (unchanged): 20%/20%/10%/10%/10%/10%/5%/5%/5%/5%
    Equal sets all encounter slots to have (almost) equal probability.
    """
    display_name = "Encounter Slot Distribution"
    default = 1
    option_vanilla = 0
    option_remove_one_percents = 1
    option_balanced = 2
    option_equal = 3


class RandomizeStaticPokemon(Toggle):
    """
    Randomizes species of static Pokemon encounters
    This includes overworld Pokemon, gift Pokemon and gift egg Pokemon

    NOTE: If this setting is disabled, the Odd Egg will still be fixed to a single possible Pokemon
    """
    display_name = "Randomize Static Pokemon"


class StaticBlocklist(OptionSet):
    """
    These Pokemon will not appear as static overworld encounters, gift eggs or gift Pokemon
    Does nothing if static Pokemon are not randomized
    You can use "_Legendaries" as a shortcut for all legendary Pokemon
    Blocklists are best effort, other constraints may cause them to be ignored
    """
    display_name = "Static Blocklist"
    valid_keys = sorted(pokemon.friendly_name for pokemon in data.pokemon.values()) + ["_Legendaries"]


class RandomizeTrades(Choice):
    """
    Randomizes species of in-game trades
    """
    display_name = "Randomize Trades"
    default = 0
    option_vanilla = 0
    option_received = 1
    option_requested = 2
    option_both = 3


class RandomizeTrainerParties(Choice):
    """
    Randomizes Pokemon in enemy trainer parties
    """
    display_name = "Randomize Trainer Parties"
    default = 0
    option_vanilla = 0
    option_match_types = 1
    option_completely_random = 2


class TrainerPartyBlocklist(OptionSet):
    """
    These Pokemon will not appear in enemy trainer parties
    Does nothing if trainer parties are not randomized
    You can use "_Legendaries" as a shortcut for all legendary Pokemon
    Blocklists are best effort, other constraints may cause them to be ignored
    """
    display_name = "Trainer Party Blocklist"
    valid_keys = sorted(pokemon.friendly_name for pokemon in data.pokemon.values()) + ["_Legendaries"]


class LevelScaling(Choice):
    """
    Sets whether Trainer, Wild Pokemon and Static Pokemon levels are scaled based on sphere access.

    - Off: Vanilla levels are used.
    - Spheres: Levels are scaled based on sphere access only.
    - Spheres and Distance: Levels are scaled based on both sphere access and distance from starting town.
    """
    display_name = "Level Scaling"
    default = 0
    option_off = 0
    option_spheres = 1
    option_spheres_and_distance = 2


class LockKantoGyms(Choice):
    """
    Logically lock entering all Kanto gyms and Mt. Moon behind access to a high level Pokemon, included locations:
    - Snorlax
    - Ho-oh
    - Lugia
    - Suicune
    - Silver Cave entrance
    - Victory Road

    You can still enter gyms and Mt. Moon without access to any of these.

    NOTE: It's not recommended to use this option with Level Scaling, as the Gym and wild Pokemon levels will be scaled
    """
    display_name = "Lock Kanto Gyms"
    option_off = 0
    option_high_level_pokemon = 1


class BoostTrainerPokemonLevels(Choice):
    """
    Boost levels of every trainer's Pokemon. There are 2 different boost modes:
    Percentage Boost: Increases every trainer Pokemon's level by the boost percentage.
    Set Min Level: Trainer Pokemon will be the specified level or higher.
    """
    display_name = "Boost Trainer Pokemon Levels"
    default = 0
    option_vanilla = 0
    option_percentage_boost = 1
    option_set_min_level = 2


class TrainerLevelBoostValue(Range):
    """
    This Value only works if Boost Trainer Pokemon Levels is being used.
    The meaning of this value depends on Trainer Boost Mode.

    Percentage Boost: This value represents the boost amount percentage
    Set Min Level: Trainer Pokemon will never be lower than this level
    """
    display_name = "Trainer Level Boost Value"
    default = 1
    range_start = 1
    range_end = 100


class RandomizeLearnsets(Choice):
    """
    - Vanilla: Vanilla learnsets
    - Randomize: Random learnsets
    - Start With Four Moves: Random learnsets with 4 starting moves
    """
    display_name = "Randomize Learnsets"
    default = 0
    option_vanilla = 0
    option_randomize = 1
    option_start_with_four_moves = 2


class MetronomeOnly(Toggle):
    """
    Only Metronome is usable in battle, PP is infinite
    You can still teach HMs and useful TMs
    """
    display_name = "Metronome Only"


class LearnsetTypeBias(NamedRange):
    """
    This option will have an effect only if Randomize Learnset option is enabled.

    Percent chance of each move in a Pokemon's learnset to match its type.
    Default value is vanilla (-1). This means there will be no bias.
    The lowest possible type matching value is 0. There will be no STAB moves in a Pokemon's learnset
    If set to 100 all moves that a Pokemon will learn by leveling up will match one of its types
    """
    display_name = "Move Learnset Type Bias"
    default = -1
    range_start = -1
    range_end = 100
    special_range_names = {
        "vanilla": -1,
    }


class RandomizeMoveValues(Choice):
    """
    - Restricted: Generates values based on vanilla move values
    Multiplies the power of each move by a random number between 0.5 and 1.5
    Adds or subtracts 0, 5 or 10 from original PP | Min 5, Max 40

    - Full Exclude Accuracy: Fully randomizes move Power and PP
    Randomizes each move's Power [20-150], PP [5-40] linearly. All possible values have the same weight.
    Multi-hit moves have their power divided by their average hit count.

    - Full: Previous + also randomizes accuracy.
    Accuracy has a flat chance of 70% to be 100%, if not it is linearly distributed between 30-100.
    Does not randomize accuracy of OHKO moves, status moves (e.g. Toxic) and unique damage moves (e.g. Seismic Toss)
    """
    display_name = "Randomize Move Values"
    default = 0
    option_vanilla = 0
    option_restricted = 1
    option_full_exclude_accuracy = 2
    option_full = 3


class RandomizeMoveTypes(Toggle):
    """
    Randomizes each move's Type
    """
    display_name = "Randomize Move Types"


class RandomizeTypeChart(Choice):
    """
    Randomizes the type matchup chart
    - Vanilla: Type matchups are unchanged
    - Shuffle: Shuffles type matchups around, keeping the same number of each possible matchup
    - Completely Random: Generates a random matchup for each type pair. WARNING: This can result in a lot of immunities
    """
    display_name = "Randomize Type Chart"
    default = 0
    option_vanilla = 0
    option_shuffle = 1
    option_completely_random = 2


class PhysicalSpecialSplit(Choice):
    """
    Sets how moves are determined to be Physical or Special
    - Vanilla: Determined by move type, for example: all Fire moves are Special
    - Modern: Determined by the move, for example: Flame Wheel is Physical and Ember is Special
    - Random by type: Vanilla, but shuffled randomly for each type
    - Random by move: Modern, but shuffled randomly for each move
    """
    display_name = "Physical/Special Split"
    default = 0
    option_vanilla = 0
    option_modern = 1
    option_random_by_type = 2
    option_random_by_move = 3


class RandomizeTMMoves(Toggle):
    """
    Randomizes the moves available as TMs
    """
    display_name = "Randomize TM Moves"


class TMPlando(OptionDict):
    """
    Specify what move a TM will contain.
    TMs 02 and 08 can never be plandoed. This also means Headbutt and Rock Smash cannot be plandoed onto other TMs.
    If Dexsanity or Dexcountsanity are enabled, and Sweet Scent hasn't been plandoed, it will be forced to TM12.
    This option takes priority over the TM Blocklist and vanilla TMs, and is ignored in Metronome Only mode.

    Uses the following format:
    tm_plando:
      1: Dynamicpunch
      3: Curse
      10: Hidden Power
      ...
    """
    display_name = "TM Plando"
    valid_keys = set(range(1, 51)) - {2, 8}
    valid_values = set(sorted(move.name.title() for id, move in data.moves.items() if id not in ("NO_MOVE", "STRUGGLE",
                                                                                                 "HEADBUTT",
                                                                                                 "ROCK_SMASH", "CUT",
                                                                                                 "FLY", "SURF",
                                                                                                 "STRENGTH", "FLASH",
                                                                                                 "WHIRLPOOL",
                                                                                                 "WATERFALL")))

    def verify_keys(self) -> None:
        super(OptionDict, self).verify_keys()
        data = set(self.value.values())
        extra = data - self.valid_values
        if extra:
            raise OptionError(
                f"Found unexpected value {', '.join(extra)} in {getattr(self, 'display_name', self)}. "
                f"Allowed values: {self.valid_values}."
            )


class TMCompatibility(NamedRange):
    """
    Percent chance for Pokemon to be compatible with each TM
    Headbutt and Rock Smash are considered HMs when applying compatibility
    """
    display_name = "TM Compatibility"
    default = -1
    range_start = -1
    range_end = 100
    special_range_names = {
        "vanilla": -1,
        "none": 0,
        "fully_compatible": 100
    }


class HMCompatibility(NamedRange):
    """
    Percent chance for Pokemon to be compatible with each HM
    Headbutt and Rock Smash are considered HMs when applying compatibility

    Minimal compatibility will ensure only the minimum required number of Pokemon can learn each HM, usually one

    You can look up HM compatible Pokemon in the Pokedex using the search function
    """
    display_name = "HM Compatibility"
    default = -1
    range_start = -1
    range_end = 100
    special_range_names = {
        "vanilla": -1,
        "minimal": 0,
        "fully_compatible": 100
    }


class HMPowerCap(NamedRange):
    """
    Lowers the power of damaging HM moves that exceed the set power down to match it.
    Headbutt and Rock Smash are considered HMs for this setting.
    """
    display_name = "HM Power Cap"
    default = 255
    range_start = 20
    range_end = 255
    special_range_names = {
        "none": range_end
    }


class FieldMovesAlwaysUsable(Toggle):
    """
    Decouples TM/HM Compatibility for Battle Moves and Field Moves.
    If enabled, Field Moves will always be considered usable, regardless of TM or HM compatibility. Badge requirements still apply.
    """
    display_name = "Field Moves Always Usable"


class RandomizeBaseStats(Choice):
    """
    - Vanilla: Vanilla base stats
    - Keep BST: Random base stats, but base stat total is preserved
    - Completely Random: Base stats and BST are completely random
    """
    display_name = "Randomize Base Stats"
    default = 0
    option_vanilla = 0
    option_keep_bst = 1
    option_completely_random = 2


class RandomizeTypes(Choice):
    """
    - Vanilla: Vanilla Pokemon types
    - Follow Evolutions: Types are randomized but preserved when evolved
    - Completely Random: Types are completely random
    """
    display_name = "Randomize Types"
    default = 0
    option_vanilla = 0
    option_follow_evolutions = 1
    option_completely_random = 2


class SharedPrimaryType(Choice):
    """
    If types are randomized, all Pokemon will share this type
    """
    display_name = "Shared Primary Type"
    default = 0
    option_off = 0
    option_normal = 1
    option_fighting = 2
    option_flying = 3
    option_poison = 4
    option_ground = 5
    option_rock = 6
    option_bug = 8
    option_ghost = 9
    option_steel = 10
    option_fire = 21
    option_water = 22
    option_grass = 23
    option_electric = 24
    option_psychic = 25
    option_ice = 26
    option_dragon = 27
    option_dark = 28


class RandomizeEvolution(Choice):
    """
    - Vanilla: Pokemon evolve into the same Pokemon they do in vanilla
    - Match a Type: Pokemon evolve into a random Pokemon with a higher base stat total, that shares at least one type with it.
    - Increase BST: Pokemon evolve into a random Pokemon with a higher base stat total.

    Note: If random BST, random types, or the evolution blocklist cause a Pokemon to have no valid evolution within
    your chosen setting here, it will evolve into the closest available thing to a valid evolution.

    Note: All Pokemon will be standardized to the medium-fast EXP curve when any evolution randomization is enabled.
    """
    display_name = "Randomize Evolution"
    default = 0
    option_vanilla = 0
    option_match_a_type = 1
    option_increase_bst = 2


class ConvergentEvolution(Choice):
    """
    Random evolution can cause multiple Pokemon to evolve into the same Pokemon.
    - Avoid: Each Pokemon can only evolve from one Pokemon.
    - Allow: Multiple Pokemon can evolve into the same Pokemon.
    """
    display_name = "Convergent Evolution"
    default = 0
    option_avoid = 0
    option_allow = 1


class EvolutionBlocklist(OptionSet):
    """
    No Pokemon will evolve into these Pokemon. Does nothing if evolution is not randomized.
    You can use "_Legendaries" as a shortcut for all legendary Pokemon.
    Blocklists are best effort, other constraints may cause them to be ignored.
    """
    display_name = "Evolution Blocklist"
    valid_keys = sorted(pokemon.friendly_name for pokemon in data.pokemon.values()) + ["_Legendaries"]


class RandomizeBreeding(Choice):
    """
    - Vanilla: Breeding is unchanged
    - Random Line Base: Each Pokemon will produce eggs for a random base Pokemon that evolves into it
    - Random Any Base: Each Pokemon will produce eggs for a random base Pokemon
    - Random Lower BST: Each Pokemon will produce eggs for a random Pokemon with equal or lower BST
    - Completely Random: Each Pokemon will produce eggs for a random Pokemon
    """
    display_name = "Randomize Breeding"
    default = 0
    option_vanilla = 0
    option_line_base = 1
    option_any_base = 2
    option_decrease_bst = 3
    option_completely_random = 4


class BreedingBlocklist(OptionSet):
    """
    No Pokemon will produce eggs containing these Pokemon.
    You can use "_Legendaries" as a shortcut for all legendary Pokemon.
    Blocklists are best effort, other constraints may cause them to be ignored.
    """
    display_name = "Breeding Blocklist"
    valid_keys = sorted(pokemon.friendly_name for pokemon in data.pokemon.values()) + ["_Legendaries"]


class RandomizePalettes(Choice):
    """
    - Vanilla: Vanilla Pokemon color palettes
    - Match Types: Color palettes match Pokemon Type
    - Completely Random: Color palettes are completely random
    """
    display_name = "Randomize Palettes"
    default = 0
    option_vanilla = 0
    option_match_types = 1
    option_completely_random = 2


class RandomizeMusic(Choice):
    """
    Randomize all music
    - Shuffle will map each music track to a new track
    - Completely Random will map each music area to a new track
    """
    display_name = "Randomize Music"
    default = 0
    option_off = 0
    option_shuffle = 1
    option_completely_random = 2


class FreeFlyLocation(Choice):
    """
    - Free Fly: Unlocks a random Fly destination when Fly is obtained.
    - Free Fly and Map Card: Additionally unlocks a random Fly destination after obtaining both the Pokegear and Map Card.
    - Map Card: Unlocks a single random Fly destination only after obtaining both the Pokegear and Map card.

    Indigo Plateau cannot be chosen as a free Fly location.
    """
    display_name = "Free Fly Location"
    default = 0
    option_off = 0
    option_free_fly = 1
    option_free_fly_and_map_card = 2
    option_map_card = 3


class EarlyFly(Toggle):
    """
    HM02 Fly will be placed early in the game
    If this option is enabled, you will be able to Fly before being forced to use an item to progress
    Early Fly is a best effort setting, if Fly and its badge cannot be placed early, then they will be placed
        randomly
    """
    display_name = "Early Fly"


class FlyCheese(Choice):
    """
    Determines whether the Vermilion and Mahogany Fly unlocks can be accessed from behind Snorlax and the
    Ragecandybar salesman respectively
    - Out of logic allows access but does not consider them in logic
    - Disallow prevents access to Fly unlocks beyond the roadblocks
    - In logic allows access and considers them in logic
    """
    display_name = "Fly Cheese"
    default = 0
    option_out_of_logic = 0
    option_disallow = 1
    option_in_logic = 2


class HMBadgeRequirements(Choice):
    """
    - Vanilla: HMs require their vanilla badges
    - No Badges: HMs do not require a badge to use
    - Add Kanto: HMs can be used with the Johto or Kanto badge
    - Regional: HMs can be used in Johto with the Johto badge or in Kanto with the Kanto badge
        This does not apply to Fly which will accept either badge
        Routes 26, 27, 28 and Tohjo Falls are in Johto for HM purposes
    """
    display_name = "HM Badge Requirements"
    default = 0
    option_vanilla = 0
    option_no_badges = 1
    option_add_kanto = 2
    option_regional = 3


class RemoveBadgeRequirement(EnhancedOptionSet):
    """
    Specify which HMs do not require a badge to use. This overrides the HM Badge Requirements setting.

    _Random has a 50% chance to include HMs which are not already included
    _All will include all HMs

    HMs should be provided in the form: "Fly".
    """
    display_name = "Remove Badge Requirement"
    valid_keys = ["Cut", "Fly", "Surf", "Strength", "Flash", "Whirlpool", "Waterfall"]


class RequireFlash(Choice):
    """
    Determines if the ability to use Flash is required to traverse dark areas

    - Not Required: Dark areas do not require Flash at all
    - Logically Required: Dark areas will expect you to be able to use Flash for logic, but you can traverse them without
    - Hard Required: You will not be able to traverse dark areas without the ability to use Flash there
    """
    display_name = "Require Flash"
    default = 1
    option_not_required = 0
    option_logically_required = 1
    option_hard_required = 2


class RemoveIlexCutTree(DefaultOnToggle):
    """
    Removes the Cut tree in Ilex Forest
    """
    display_name = "Remove Ilex Forest Cut Tree"


class SaffronGatehouseTea(EnhancedOptionSet):
    """
    Sets which Saffron City gatehouses require Tea to pass. Obtaining the Tea will unlock them all.
    If any gatehouses are enabled, adds a new location in Celadon Mansion 1F and adds Tea to the item pool.
    Valid options are: North, East, South and West in any combination.
    _Random gives each gate that is not already included a 50% chance to be included.
    _All is shorthand for all valid options except _Random of course.
    """
    display_name = "Saffron Gatehouse Tea"
    valid_keys = ["North", "East", "South", "West"]


class EastWestUnderground(Toggle):
    """
    Adds an Underground Pass between Route 7 and Route 8 in Kanto.
    """
    display_name = "East - West Underground"


class UndergroundsRequirePower(Choice):
    """
    Specifies which of the Kanto Underground Passes require the Machine Part to be returned to access.
    """
    display_name = "Undergrounds Require Power"
    default = 0
    option_both = 0
    option_north_south = 1
    option_east_west = 2
    option_neither = 3


class ReusableTMs(Toggle):
    """
    TMs can be used an infinite number of times
    """
    display_name = "Reusable TMs"


class MinimumCatchRate(Range):
    """
    Sets a minimum catch rate for wild Pokemon
    """
    display_name = "Minimum Catch Rate"
    default = 0
    range_start = 0
    range_end = 255


class SkipEliteFour(Toggle):
    """
    Go straight to Lance when challenging the Elite Four
    """
    display_name = "Skip Elite Four"


class BetterMarts(Toggle):
    """
    Improves the selection of items at Pokemarts
    """
    display_name = "Better Marts"


class BuildAMart(OptionList):
    """
    Create a custom shop in place of the better mart with your own item selection, this also affects the final upgraded
    Pokecenter 2F mart.
    The first two shop items will always be Poke Ball and Escape Rope.
    Maximum of 14 items, any extra items will be discarded.
    
    Available items: Antidote, Awakening, Burn Heal, Calcium, Carbos, Dire Hit, Elixer, Ether, Fresh Water, 
    Full Heal, Full Restore, Great Ball, Guard Spec, HP Up, Hyper Potion, Ice Heal, Iron, Lemonade, Max Elixer, 
    Max Ether, Max Potion, Max Repel, Max Revive, Park Ball, Parlyz Heal, Potion, Protein, PP Up, Rare Candy, Repel, 
    Revive, Soda Pop, Super Potion, Super Repel, Ultra Ball, X Accuracy, X Attack, X Defend, X Special, X Speed.
    """
    display_name = "Build-a-Mart"
    valid_keys = sorted(item.label for item in data.items.values() if "CustomShop" in item.tags)


class ExpModifier(NamedRange):
    """
    Scale the amount of Experience Points given in battle
    Default is 20, for double set to 40, for half set to 10, etc

    You can modify this value in-game, the CUSTOM option will use the value provided here.
    """
    display_name = "Experience Modifier"
    default = 20
    range_start = 1
    range_end = 255
    special_range_names = {
        "half": default // 2,
        "normal": default,
        "double": default * 2,
        "triple": default * 3,
        "quadruple": default * 4,
        "quintuple": default * 5,
        "sextuple": default * 6,
        "septuple": default * 7,
        "octuple": default * 8,
    }


class StartingMoney(NamedRange):
    """
    Sets your starting money.
    """
    display_name = "Starting Money"
    default = 3000
    range_start = 0
    range_end = 999999
    special_range_names = {
        "vanilla": 3000
    }


class AllPokemonSeen(Toggle):
    """
    Start with all Pokemon seen in your Pokedex.
    This allows you to see where the Pokemon can be encountered in the wild.
    """
    display_name = "All Pokemon Seen"


class TrapWeight(Range):
    """
    Percentage chance each filler item is replaced with a trap

    If no traps have any weight, this option does nothing

    NOTE: This option has a maximum of 20 by default, this can be changed by setting maximum_filler_trap_percentage in host.yaml
    """
    display_name = "Filler Trap Percentage"
    default = 0
    range_start = 0
    range_end = 100


class PhoneTrapWeight(Range):
    """
    Adds random Pokegear calls that acts as traps
    Specifies the weight at which traps become Phone Traps

    NOTE: Phone traps will loop after you receive 32 of them
    """
    display_name = "Phone Trap Weight"
    default = 0
    range_start = 0
    range_end = 100


class SleepTrapWeight(Range):
    """
    Trap that causes Sleep status on your party
    Specifies the weight at which traps become Sleep Traps
    """
    display_name = "Sleep Trap Weight"
    default = 0
    range_start = 0
    range_end = 100


class PoisonTrapWeight(Range):
    """
    Trap that causes Poison status on your party
    Specifies the weight at which traps become Poison Traps
    """
    display_name = "Poison Trap Weight"
    default = 0
    range_start = 0
    range_end = 100


class BurnTrapWeight(Range):
    """
    Trap that causes Burn status on your party
    Specifies the weight at which traps become Burn Traps
    """
    display_name = "Burn Trap Weight"
    default = 0
    range_start = 0
    range_end = 100


class FreezeTrapWeight(Range):
    """
    Trap that causes Freeze status on your party
    Specifies the weight at which traps become Freeze Traps
    """
    display_name = "Freeze Trap Weight"
    default = 0
    range_start = 0
    range_end = 100


class ParalysisTrapWeight(Range):
    """
    Trap that causes Paralysis status on your party
    Specifies the weight at which traps become Paralysis Traps
    """
    display_name = "Paralysis Trap Weight"
    default = 0
    range_start = 0
    range_end = 100


class TrapLink(Toggle):
    """
    Games that support traplink will all receive similar traps when a matching trap is sent from another traplink game

    This only applies to traps you have enabled
    """
    display_name = "Trap Link"


class EnableMischief(Choice):
    """
    If I told you what this does, it would ruin the surprises :)
    """
    display_name = "Enable Mischief"
    default = 0
    option_off = 0
    alias_false = option_off  # For compatibility
    alias_no = option_off  # For compatibility
    option_mild = 1
    option_wild = 2
    alias_true = option_wild  # For compatibility
    alias_on = option_wild  # For compatibility
    alias_yes = option_wild  # For compatibility


class CustomMischiefPool(OptionSet):
    """Only allow specific Mischief options"""
    display_name = "Custom Mischief Pool"
    visibility = Visibility.none
    valid_keys = [misc_option.name for misc_option in list(MiscOption)] + ["_Mild", "_Wild"]


class MischiefLowerBound(Range):
    """
    Lower bound of selectable mischief, in percentage
    """
    display_name = "Mischief Lower Bound"
    visibility = Visibility.none
    default = 50
    range_start = 0
    range_end = 100


class MischiefUpperBound(Range):
    """
    Upper bound of selectable mischief, in percentage
    """
    display_name = "Mischief Upper Bound"
    visibility = Visibility.none
    default = 75
    range_start = 0
    range_end = 100


class MoveBlocklist(OptionSet):
    """
    Pokemon won't learn these moves via learnsets.
    Moves should be provided in the form: "Ice Beam"
    Does not apply to vanilla learnsets
    """
    display_name = "Move Blocklist"
    valid_keys = sorted(move.name.title() for id, move in data.moves.items() if id not in ("NO_MOVE", "STRUGGLE"))


class TMBlocklist(OptionSet):
    """
    No TM will contain these moves.
    Moves should be provided in the form: "Ice Beam"
    Does not apply to vanilla TMs
    """
    display_name = "TM Blocklist"
    valid_keys = sorted(move.name.title() for id, move in data.moves.items() if id not in ("NO_MOVE", "STRUGGLE"))


class FlyLocationBlocklist(OptionSet):
    """
    These locations won't be given to you as fly locations, either as your free one or from receiving the map card.
    Locations should be provided in the form: "Ecruteak City"
    Indigo Plateau cannot be chosen as a free fly location and is not a valid option
    If you blocklist enough locations that there aren't enough locations left for your total number of free fly locations, the blocklist will simply do nothing
    "_Johto" and "_Kanto" are shortcuts for all Johto and Kanto towns respectively
    """
    display_name = "Fly Location Blocklist"
    valid_keys = sorted(region.name for region in data.fly_regions) + ["_Johto", "_Kanto"]


class RemoteItems(Toggle):
    """
    Instead of placing your own items directly into the ROM, all items are received from the server, including items you find for yourself.
    This enables co-op of a single slot and recovering more items after a lost save file (if you're so unlucky).
    But it changes pickup behavior slightly and requires connection to the server to receive any items.
    """
    display_name = "Remote Items"


class AlwaysUnlockFly(Toggle):
    """
    Always unlock Fly destinations when entering a town, even if Randomize Fly Unlocks is enabled
    """
    display_name = "Always Unlock Fly Destinations"


class TrainerName(FreeText):
    """
    Preset your trainer name, this skips the name prompt.

    Only the first seven characters will be used, unsupported characters will be replaced with '?'.
    """
    display_name = "Trainer Name"


class GameOptions(OptionDict):
    """
    Presets in-game options. These can be changed in-game later. Any omitted options will use their default.

    Allowed options and values, with default first:

    ap_item_sound: on/off - Sets whether a sound is played when a remote item is received
    auto_hms: off/on - HMs will be used automatically where possible, if their usage conditions are met
    auto_run: off/on - Sets whether run activates automatically, if on you can hold B to walk
    battle_animations: all/no_scene/no_bars/speedy - Sets which battle animations are played:
        all: All animations play, including entry and moves
        no_scene: Entry and move animations do not play
        no_bars: Entry, move and HP/EXP bar animations do not play
        speedy: No battle animations play and many delays are removed to make battles faster
    battle_move_stats: off/on - Sets whether or not to display power and accuracy of moves in battle
    battle_shift: shift/set - Sets whether you are asked to switch between trainer Pokemon
    bike_music: on/off - Sets whether the bike music will play
    blind_trainers: off/on - Sets whether trainers will see you without talking to them directly
    catch_exp: off/on - Sets whether or not you get EXP for catching a Pokemon
    dex_area_beep: off/on - Sets whether the Pokedex beeps for land and Surf encounters in the current area
    exp_distribution: gen2/gen6/gen8/no_exp - Sets the EXP distribution method:
        gen2: EXP is split evenly among battle participants, EXP Share splits evenly between participants and non-participants
        gen6: Participants earn 100% of EXP, non-participants earn 50% of EXP when EXP Share is enabled
        gen8: Participants earn 100% of EXP, non-participants earn 100% of EXP when EXP Share is enabled
        no_exp: EXP is disabled
    fast_egg_hatch: off/on - Sets whether eggs take a single cycle to hatch
    fast_egg_make: off/on - Sets whether eggs are guaranteed after one cycle at the day care
    guaranteed_catch: off/on - Sets whether balls have a 100% success rate
    hms_require_teaching: on/off - Sets whether it is required to teach field moves to use them in the field
    item_notification: popup/sound/none - Sets how Trainersanity, Dex(count)sanity and Grasssanity locations show item notifications
    low_hp_beep: on/off - Sets whether the low HP beep is played in battle
    menu_account: on/off - Sets whether your start menu selection is remembered
    more_uncaught_encounters: on/off - Sets whether wild encounters of Pokemon you have not caught are more likely
    poison_flicker: on/off - Sets whether the overworld poison flash effect is played
    rods_always_work: off/on - Sets whether the fishing rods always succeed
    short_fanfares: off/on - Sets whether item receive fanfares are shortened
    skip_dex_registration: off/on - Sets whether the Pokedex registration screen is skipped
    skip_nicknames: off/on - Sets whether you are asked to nickname a Pokemon upon receiving it
    sound: mono/stereo - Sets the sound mode
    spinners: normal/rotators/heck/hell - Sets the overworld behaviour of trainers
        normal: Trainers will behave as they do in vanilla
        rotators: Trainers that spin randomly will rotate consistently
        heck: All trainers with vision rotate consistently, they have their original vision range but can spot you through obstacles
        hell: All trainers with vision will spin randomly, have max vision and can spot you through obstacles
    surf_music: on/off - Sets whether the surf music will play
    text_frame: 1-8 - Sets the textbox frame, "random" will pick a random frame
    text_speed: mid/slow/fast/instant - Sets the speed at which text advances
    time_of_day: auto/morn/day/nite - Sets a time of day override, auto follows the clock, "random" will pick a random time
    trainersanity_indication: off/on - Sets whether Trainersanity trainers have grayscale sprites until they are beaten
    turbo_button: none/a/b/a_or_b - Sets which buttons auto advance text when held
    """
    display_name = "Game Options"
    default = {
        "text_speed": "mid",
        "battle_shift": "shift",
        "battle_animations": "all",
        "sound": "mono",
        "menu_account": "on",
        "text_frame": 1,
        "bike_music": "on",
        "surf_music": "on",
        "skip_nicknames": "off",
        "auto_run": "off",
        "spinners": "normal",
        "fast_egg_hatch": "off",
        "fast_egg_make": "off",
        "rods_always_work": "off",
        "exp_distribution": "gen2",
        "catch_exp": "off",
        "poison_flicker": "on",
        "turbo_button": "none",
        "low_hp_beep": "on",
        "time_of_day": "auto",
        "battle_move_stats": "off",
        "short_fanfares": "off",
        "dex_area_beep": "off",
        "skip_dex_registration": "off",
        "blind_trainers": "off",
        "guaranteed_catch": "off",
        "ap_item_sound": "on",
        "trainersanity_indication": "off",
        "more_uncaught_encounters": "off",
        "auto_hms": "off",
        "hms_require_teaching": "on",
        "item_notification": "popup",
    }

    @override
    def verify(self, world: Type[World], player_name: str, plando_options: PlandoOptions) -> None:
        for key, value in self.value.items():
            if not isinstance(value, Hashable):
                raise OptionError(f"Invalid game option value for {key}.")


class FieldMoveMenuOrder(OptionList):
    """
    Defines which order the entries of the Field Move Menu (accessible if hms_require_teaching is set to 'off') appear in.

    Provided values will appear on top of the menu in the given order.
    Omitted values will appear below in the following order: Cut, Fly, Surf, Strength, Flash, Whirlpool, Waterfall, Rock Smash, Headbutt, Dig, Teleport, Sweet Scent.
    Duplicates will be omitted.
    """
    display_name = "Field Move Menu Order"
    valid_keys = ["Cut", "Fly", "Surf", "Strength", "Flash", "Whirlpool", "Waterfall", "Rock Smash", "Headbutt",
                  "Dig", "Teleport", "Sweet Scent"]
    default = valid_keys

    def __init__(self, value):
        super(FieldMoveMenuOrder, self).__init__(value)
        self.value = list(dict.fromkeys(self.value))
        self.value += [key for key in self.valid_keys if key not in self.value]
        assert len(self.value) == len(self.valid_keys)

    def __bool__(self):
        return super(FieldMoveMenuOrder, self).__bool__() and self.value != self.default


class ExcludePostGoalLocations(DefaultOnToggle):
    """
    Excludes locations which require becoming champion when goal is becoming champion
    """
    display_name = "Exclude Post Goal Locations"


class Grasssanity(Choice):
    """
    Adds Cutting grass tiles as locations, each one adds a Grass to the item pool, Grass smells good and sells for ¥1
    Long grass tiles in National Park must be Cut twice and as such contribute two locations

    - One Per Area: Selects a random grass tile in each Route or Area to be a location
    - Full: Every grass tile is a location

    WARNING: This option is dumb, it can add over 700 locations and over 700 useless filler items
    """
    display_name = "Grasssanity"
    default = 0
    option_off = 0
    option_one_per_area = 1
    option_full = 2


class DefaultPokedexMode(Choice):
    """
    Sets the default Pokedex mode
    """
    display_name = "Default Pokedex Mode"
    default = 0
    option_new = 0
    option_old = 1
    option_a_to_z = 2


class RequirePokegearForPhoneNumbers(DefaultOnToggle):
    """
    Sets whether the Pokegear is required to register trainer phone numbers and whether the Pokegear and Phone Card
    are required to receive calls

    The Pokegear and Phone Card will always be logically required for phone call locations
    """
    display_name = "Require Pokegear for Phone Numbers"


class TrainerPalette(Choice):
    """
    Sets the palette used for the player character
    """
    display_name = "Trainer Palette"
    default = 0
    option_vanilla = 0
    option_red = 1
    option_blue = 2
    option_green = 3
    option_brown = 4


class ProgressiveRods(Toggle):
    """
    Sets whether fishing rods are always received in order (Old -> Good -> Super)
    """
    display_name = "Progressive Rods"


class PokemonCrystalDeathLink(DeathLink):
    __doc__ = DeathLink.__doc__ + "\n\n    In Pokemon Crystal, whiting out sends a death and receiving a death causes you to white out.\n\n    Being seen by a trainer when spinner heck or hell is enabled will send a deathlink."


@dataclass
class PokemonCrystalOptions(PerGameCommonOptions):
    goal: Goal
    johto_only: JohtoOnly
    elite_four_requirement: EliteFourRequirement
    elite_four_count: EliteFourCount
    red_requirement: RedRequirement
    red_count: RedCount
    mt_silver_requirement: MtSilverRequirement
    mt_silver_count: MtSilverCount
    radio_tower_requirement: RadioTowerRequirement
    radio_tower_count: RadioTowerCount
    route_44_access_requirement: Route44AccessRequirement
    route_44_access_count: Route44AccessCount
    magnet_train_access: MagnetTrainAccess
    vanilla_clair: VanillaClair
    randomize_starting_town: RandomizeStartingTown
    starting_town_blocklist: StartingTownBlocklist
    randomize_badges: RandomizeBadges
    randomize_hidden_items: RandomizeHiddenItems
    require_itemfinder: RequireItemfinder
    item_pool_fill: ItemPoolFill
    add_missing_useful_items: AddMissingUsefulItems
    route_32_condition: Route32Condition
    dark_areas: DarkAreas
    victory_road_access: VictoryRoadAccess
    kanto_access_requirement: KantoAccessRequirement
    kanto_access_count: KantoAccessCount
    red_gyarados_access: RedGyaradosAccess
    route_2_access: Route2Access
    route_3_access: Route3Access
    blackthorn_dark_cave_access: BlackthornDarkCaveAccess
    national_park_access: NationalParkAccess
    route_42_access: Route42Access
    mount_mortar_access: MountMortarAccess
    route_12_access: Route12Access
    ss_aqua_access: SSAquaAccess
    route_30_battle: Route30Battle
    johto_trainersanity: JohtoTrainersanity
    kanto_trainersanity: KantoTrainersanity
    rematchsanity: Rematchsanity
    randomize_wilds: RandomizeWilds
    dexsanity: Dexsanity
    dexsanity_starters: DexsanityStarters
    dexcountsanity: Dexcountsanity
    dexcountsanity_step: DexcountsanityStep
    dexcountsanity_leniency: DexcountsanityLeniency
    wild_encounter_methods_required: WildEncounterMethodsRequired
    enforce_wild_encounter_methods_logic: EnforceWildEncounterMethodsLogic
    trades_required: TradesRequired
    static_pokemon_required: StaticPokemonRequired
    evolution_methods_required: EvolutionMethodsRequired
    evolution_gym_levels: EvolutionGymLevels
    breeding_methods_required: BreedingMethodsRequired
    shopsanity: Shopsanity
    shopsanity_prices: ShopsanityPrices
    shopsanity_minimum_price: MinimumShopsanityPrice
    shopsanity_maximum_price: MaximumShopsanityPrice
    provide_shop_hints: ProvideShopHints
    shopsanity_restrict_rare_candies: ShopsanityRestrictRareCandies
    shopsanity_x_items: ShopsanityXItems
    randomize_pokegear: RandomizePokegear
    randomize_berry_trees: RandomizeBerryTrees
    randomize_pokemon_requests: RandomizePokemonRequests
    randomize_phone_call_items: RandomizePhoneCalls
    randomize_fly_unlocks: RandomizeFlyUnlocks
    randomize_bug_catching_contest: RandomizeBugCatchingContest
    randomize_starters: RandomizeStarters
    starter_blocklist: StarterBlocklist
    starters_bst_average: StarterBST
    wild_encounter_blocklist: WildEncounterBlocklist
    encounter_grouping: EncounterGrouping
    force_fully_evolved: ForceFullyEvolved
    encounter_slot_distribution: EncounterSlotDistribution
    randomize_static_pokemon: RandomizeStaticPokemon
    static_blocklist: StaticBlocklist
    level_scaling: LevelScaling
    lock_kanto_gyms: LockKantoGyms
    randomize_trades: RandomizeTrades
    randomize_trainer_parties: RandomizeTrainerParties
    trainer_party_blocklist: TrainerPartyBlocklist
    boost_trainers: BoostTrainerPokemonLevels
    trainer_level_boost: TrainerLevelBoostValue
    randomize_learnsets: RandomizeLearnsets
    metronome_only: MetronomeOnly
    learnset_type_bias: LearnsetTypeBias
    randomize_move_values: RandomizeMoveValues
    randomize_move_types: RandomizeMoveTypes
    randomize_type_chart: RandomizeTypeChart
    physical_special_split: PhysicalSpecialSplit
    randomize_tm_moves: RandomizeTMMoves
    tm_plando: TMPlando
    tm_compatibility: TMCompatibility
    hm_compatibility: HMCompatibility
    hm_power_cap: HMPowerCap
    field_moves_always_usable: FieldMovesAlwaysUsable
    randomize_base_stats: RandomizeBaseStats
    randomize_types: RandomizeTypes
    shared_primary_type: SharedPrimaryType
    randomize_evolution: RandomizeEvolution
    convergent_evolution: ConvergentEvolution
    evolution_blocklist: EvolutionBlocklist
    randomize_breeding: RandomizeBreeding
    breeding_blocklist: BreedingBlocklist
    randomize_palettes: RandomizePalettes
    randomize_music: RandomizeMusic
    move_blocklist: MoveBlocklist
    tm_blocklist: TMBlocklist
    free_fly_location: FreeFlyLocation
    free_fly_blocklist: FlyLocationBlocklist
    early_fly: EarlyFly
    fly_cheese: FlyCheese
    require_flash: RequireFlash
    hm_badge_requirements: HMBadgeRequirements
    remove_badge_requirement: RemoveBadgeRequirement
    remove_ilex_cut_tree: RemoveIlexCutTree
    saffron_gatehouse_tea: SaffronGatehouseTea
    east_west_underground: EastWestUnderground
    undergrounds_require_power: UndergroundsRequirePower
    reusable_tms: ReusableTMs
    minimum_catch_rate: MinimumCatchRate
    skip_elite_four: SkipEliteFour
    better_marts: BetterMarts
    build_a_mart: BuildAMart
    experience_modifier: ExpModifier
    starting_money: StartingMoney
    all_pokemon_seen: AllPokemonSeen
    filler_trap_percentage: TrapWeight
    phone_trap_weight: PhoneTrapWeight
    sleep_trap_weight: SleepTrapWeight
    poison_trap_weight: PoisonTrapWeight
    burn_trap_weight: BurnTrapWeight
    freeze_trap_weight: FreezeTrapWeight
    paralysis_trap_weight: ParalysisTrapWeight
    remote_items: RemoteItems
    game_options: GameOptions
    field_move_menu_order: FieldMoveMenuOrder
    trainer_name: TrainerName
    enable_mischief: EnableMischief
    custom_mischief_pool: CustomMischiefPool
    mischief_lower_bound: MischiefLowerBound
    mischief_upper_bound: MischiefUpperBound
    start_inventory_from_pool: StartInventoryPool
    death_link: PokemonCrystalDeathLink
    always_unlock_fly_destinations: AlwaysUnlockFly
    exclude_post_goal_locations: ExcludePostGoalLocations
    grasssanity: Grasssanity
    default_pokedex_mode: DefaultPokedexMode
    trap_link: TrapLink
    require_pokegear_for_phone_numbers: RequirePokegearForPhoneNumbers
    trainer_palette: TrainerPalette
    progressive_rods: ProgressiveRods


OPTION_GROUPS = [
    OptionGroup(
        "Map",
        [RandomizeStartingTown,
         StartingTownBlocklist,
         JohtoOnly]
    ),
    OptionGroup(
        "Roadblocks",
        [EliteFourRequirement, EliteFourCount,
         RedRequirement, RedCount,
         MtSilverRequirement, MtSilverCount,
         RadioTowerRequirement, RadioTowerCount,
         Route44AccessRequirement, Route44AccessCount,
         KantoAccessRequirement, KantoAccessCount,
         VictoryRoadAccess,
         DarkAreas,
         Route32Condition,
         Route2Access,
         Route3Access,
         Route42Access,
         MountMortarAccess,
         RedGyaradosAccess,
         BlackthornDarkCaveAccess,
         NationalParkAccess,
         SaffronGatehouseTea,
         RemoveIlexCutTree,
         UndergroundsRequirePower,
         EastWestUnderground,
         VanillaClair,
         Route12Access,
         MagnetTrainAccess,
         SSAquaAccess,
         Route30Battle]
    ),
    OptionGroup(
        "Items",
        [RandomizeBadges,
         RandomizePokegear,
         RandomizeHiddenItems,
         RandomizeBerryTrees,
         RandomizePokemonRequests,
         RandomizeFlyUnlocks,
         RandomizeBugCatchingContest,
         RandomizePhoneCalls,
         RequireItemfinder,
         RemoteItems,
         ItemPoolFill,
         AddMissingUsefulItems,
         ExcludePostGoalLocations,
         Grasssanity]
    ),
    OptionGroup(
        "Shopsanity",
        [Shopsanity,
         ShopsanityPrices,
         MinimumShopsanityPrice,
         MaximumShopsanityPrice,
         ProvideShopHints,
         ShopsanityRestrictRareCandies,
         ShopsanityXItems]
    ),
    OptionGroup(
        "HMs",
        [HMCompatibility,
         HMBadgeRequirements,
         RemoveBadgeRequirement,
         RequireFlash,
         FieldMovesAlwaysUsable,
         FreeFlyLocation,
         FlyLocationBlocklist,
         EarlyFly,
         FlyCheese]
    ),
    OptionGroup(
        "Pokemon",
        [RandomizeWilds,
         WildEncounterBlocklist,
         RandomizeStaticPokemon,
         StaticBlocklist,
         RandomizeBaseStats,
         RandomizeTypes,
         SharedPrimaryType,
         RandomizeEvolution,
         ConvergentEvolution,
         EvolutionBlocklist,
         RandomizeBreeding,
         BreedingBlocklist,
         RandomizeTrades,
         EncounterGrouping,
         EncounterSlotDistribution]
    ),
    OptionGroup(
        "Starters",
        [RandomizeStarters,
         StarterBST,
         StarterBlocklist]
    ),
    OptionGroup(
        "Moves",
        [RandomizeLearnsets,
         LearnsetTypeBias,
         MetronomeOnly,
         RandomizeMoveTypes,
         RandomizeMoveValues,
         RandomizeTypeChart,
         PhysicalSpecialSplit,
         HMPowerCap,
         RandomizeTMMoves,
         TMPlando,
         TMCompatibility,
         ReusableTMs,
         MoveBlocklist,
         TMBlocklist]
    ),
    OptionGroup(
        "Trainers",
        [RandomizeTrainerParties,
         TrainerPartyBlocklist,
         BoostTrainerPokemonLevels,
         TrainerLevelBoostValue,
         ForceFullyEvolved]
    ),
    OptionGroup(
        "Dexsanities",
        [Dexsanity,
         Dexcountsanity,
         DexcountsanityStep,
         DexcountsanityLeniency,
         DexsanityStarters]
    ),
    OptionGroup(
        "Trainersanity",
        [JohtoTrainersanity,
         KantoTrainersanity]
    ),
    OptionGroup(
        "Pokemon Logic",
        [WildEncounterMethodsRequired,
         EnforceWildEncounterMethodsLogic,
         StaticPokemonRequired,
         TradesRequired,
         EvolutionMethodsRequired,
         EvolutionGymLevels,
         BreedingMethodsRequired]
    ),
    OptionGroup(
        "Traps",
        [TrapWeight,
         PhoneTrapWeight,
         SleepTrapWeight,
         PoisonTrapWeight,
         BurnTrapWeight,
         FreezeTrapWeight,
         ParalysisTrapWeight,
         TrapLink]
    ),
    OptionGroup(
        "Quality of Life",
        [GameOptions,
         LevelScaling,
         LockKantoGyms,
         AllPokemonSeen,
         StartingMoney,
         BetterMarts,
         BuildAMart,
         ExpModifier,
         SkipEliteFour,
         MinimumCatchRate,
         AlwaysUnlockFly,
         TrainerName,
         FieldMoveMenuOrder,
         DefaultPokedexMode,
         ProgressiveRods,
         RequirePokegearForPhoneNumbers,
         PokemonCrystalDeathLink]
    ),
    OptionGroup(
        "Cosmetic",
        [RandomizePalettes,
         RandomizeMusic,
         TrainerPalette]
    ),
    OptionGroup(
        ":3",
        [EnableMischief,
         CustomMischiefPool,
         MischiefLowerBound,
         MischiefUpperBound],
        False
    )
]
