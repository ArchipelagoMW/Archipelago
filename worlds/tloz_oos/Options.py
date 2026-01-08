from dataclasses import dataclass
from datetime import datetime

from Options import Choice, DeathLink, DefaultOnToggle, PerGameCommonOptions, Range, Toggle, StartInventoryPool, \
    ItemDict, ItemsAccessibility, ItemSet, Visibility, OptionGroup, NamedRange
from worlds.tloz_oos.data.Items import ITEMS_DATA


class OracleOfSeasonsGoal(Choice):
    """
    The goal to accomplish in order to complete the seed.
    - Beat Onox: beat the usual final boss (same as vanilla)
    - Beat Ganon: teleport to the Room of Rites after beating Onox, then beat Ganon (same as linked game)
    """
    display_name = "Goal"

    option_beat_onox = 0
    option_beat_ganon = 1

    default = 0
    include_in_patch = True
    include_in_slot_data = True


class OracleOfSeasonsLogicDifficulty(Choice):
    """
    The difficulty of the logic used to generate the seed.
    - Casual: expects you to know what you would know when playing the game for the first time
    - Medium: expects you to know well the alternatives on how to do basic things, but won't expect any trick
    - Hard: expects you to know difficult tricks such as bomb jumps
    - Hell: expects you to use tricks and glitches that span over more than a few inputs
    """
    display_name = "Logic Difficulty"

    option_casual = 0
    option_medium = 1
    option_hard = 2
    option_hell = 3

    default = 0
    include_in_slot_data = True


class OracleOfSeasonsRequiredEssences(Range):
    """
    The amount of essences that need to be obtained in order to get the Maku Seed from the Maku Tree and be able
    to fight Onox in his castle
    """
    display_name = "Required Essences"

    range_start = 0
    range_end = 8

    default = 8
    include_in_patch = True
    include_in_slot_data = True


class OracleOfSeasonsPlacedEssences(Range):
    """
    The amount of essences that will be placed in the world. Removed essences are replaced by filler items instead, and
    if essences are not shuffled, those filler items will be placed on the pedestal where the essence would have been.
    If the value for "Placed Essences" is lower than "Required Essences" (which can happen when using random values
    for both), a new random value is automatically picked in the valid range.
    """
    display_name = "Placed Essences"

    range_start = 0
    range_end = 8

    default = 8


class OracleOfSeasonsDefaultSeasons(Choice):
    """
    The world of Holodrum is split in regions, each one having its own default season being forced when entering it.
    This options gives several ways of manipulating those default seasons.
    - Vanilla: default seasons for each region are the ones from the original game
    - Randomized: each region has its own random default season picked at generation time
    - Random Singularity: a single season is randomly picked and put as default season in every region in the game
    - Specific Singularity: the given season is put as default season in every region in the game
    """
    display_name = "Default Seasons"

    option_vanilla = 0
    option_randomized = 1
    option_random_singularity = 2
    option_spring_singularity = 3
    option_summer_singularity = 4
    option_winter_singularity = 5
    option_autumn_singularity = 6

    default = 1
    include_in_slot_data = True


class OracleOfSeasonsHoronSeason(DefaultOnToggle):
    """
    In the vanilla game, Horon Village default season is chaotic: every time you enter it, it sets a random season.
    This nullifies every condition where a season is required inside Horon Village, since you can leave and re-enter
    again and again until you get the season that suits you.
    Enabling this option disables that behavior and makes Horon Village behave like any other region in the game.
    This means it will have a default season picked at generation time that follows the global behavior defined
    in the "Default Seasons" option.
    """
    display_name = "Normalize Horon Village Season"


class OracleOfSeasonsAnimalCompanion(Choice):
    """
    Determines which animal companion you can summon using the Flute, as well as the layout of the Natzu region.
    - Ricky: the kangaroo with boxing skills
    - Dimitri: the swimming dinosaur who can eat anything
    - Moosh: the flying blue bear with a passion for Spring Bananas
    """
    display_name = "Animal Companion"

    option_ricky = 0
    option_dimitri = 1
    option_moosh = 2

    default = "random"
    include_in_patch = True
    include_in_slot_data = True


class OracleOfSeasonsDefaultSeedType(Choice):
    """
    Determines which of the 5 seed types will be the "default seed type", which is given:
    - when obtaining Seed Satchel
    - when obtaining Slingshot
    - by Horon Seed Tree
    """
    display_name = "Default Seed Type"

    option_ember = 0
    option_scent = 1
    option_pegasus = 2
    option_gale = 3
    option_mystery = 4

    default = 0
    include_in_patch = True
    include_in_slot_data = True


class OracleOfSeasonsDuplicateSeedTree(Choice):
    """
    The game contains 6 seed trees but only 5 seed types, which means two trees
    must contain the same seed type. This option enables choosing which tree will
    always contain a duplicate of one of the other 5 trees.
    It is strongly advised to set this to "Tarm Ruins Tree" since it's by far the hardest tree to reach
    (and being locked out of a useful seed type can lead to very frustrating situations).
    """
    display_name = "Duplicate Seed Tree"

    option_horon_village = 0
    option_woods_of_winter = 1
    option_north_horon = 2
    option_spool_swamp = 3
    option_sunken_city = 4
    option_tarm_ruins = 5

    default = 5


class OracleOfSeasonsDungeonShuffle(Toggle):
    """
    If enabled, each dungeon entrance will lead to a random dungeon picked at generation time.
    Otherwise, all dungeon entrances lead to their dungeon as intended.
    """
    display_name = "Shuffle Dungeons"

    include_in_slot_data = True


class OracleOfSeasonsPortalShuffle(Choice):
    """
    - Vanilla: pairs of portals are the same as in the original game
    - Shuffle Outwards: each portal is connected to a random portal in the opposite dimension picked at generation time
    - Shuffle: each portal is connected to a random portal, which might be in the same dimension (with the guarantee of
      having at least one portal going across dimensions)
    """
    display_name = "Shuffle Subrosia Portals"

    option_vanilla = 0
    option_shuffle_outwards = 1
    option_shuffle = 2

    default = 0
    include_in_slot_data = True


class OracleOfSeasonsOldMenShuffle(Choice):
    """
    Determine how the Old Men which give or take rupees are handled by the randomizer.
    - Vanilla: Each Old Man gives/takes the amount of rupees it usually does in the base game
    - Shuffled Values: The amount of given/taken rupees are shuffled between Old Men
    - Random Values: Each Old Man will give or take a random amount of rupees
    - Random Positive Values: Each Old Man will give a random amount of rupees, but never make you pay
    - Turn Into Locations: Each Old Man becomes a randomized check, and the total amount of rupees they usually give
      in vanilla is shuffled into the item pool
    """

    display_name = "Rupee Old Men"

    option_vanilla = 0
    option_shuffled_values = 1
    option_random_values = 2
    option_random_positive_values = 3
    option_turn_into_locations = 4

    default = 3
    include_in_patch = True
    include_in_slot_data = True


class OracleOfSeasonsBusinessScrubsShuffle(Toggle):
    """
    This option adds the 4 accessible business scrubs (Spool Swamp, Samasa Desert, D2, D4) to the pool of randomized
    locations. Just like any other shop, they ask for rupees in exchange of the randomized item,
    which can only be purchased once.
    Please note that scrubs inside dungeons can hold dungeon items, such as keys.
    """
    display_name = "Shuffle Business Scrubs"

    include_in_patch = True
    include_in_slot_data = True


class OracleOfSeasonsGoldenOreSpotsShuffle(Toggle):
    """
    This option adds the 7 hidden digging spots in Subrosia (containing 50 Ore Chunks each) to the pool
    of randomized locations.
    """
    display_name = "Shuffle Golden Ore Spots"

    include_in_patch = True
    include_in_slot_data = True


class OracleOfSeasonsEssenceSanity(Toggle):
    """
    If enabled, essences will be shuffled anywhere in the multiworld instead of being guaranteed to be found
    at the end their respective dungeons.
    """
    display_name = "Shuffle Essences"

    include_in_patch = True
    include_in_slot_data = True


class OracleOfSeasonsExcludeDungeonsWithoutEssence(DefaultOnToggle):
    """
    If enabled, all dungeons whose essence has been removed because of the "Placed Essences" option will be excluded,
    which means you can safely ignore them since they cannot contain an item that is required to complete the seed.
    If "Shuffle Essences" is enabled, this option has no effect.
    Hero's Cave is not considered to be a dungeon for this option, and therefore is never excluded.
    """
    display_name = "Exclude Dungeons Without Essence"


class OracleOfSeasonsShowDungeonsWithEssence(Choice):
    """
    Determines the condition required to highlight dungeons having an essence on their end pedestal
    (with a sparkle on the in-game map).
    This is especially useful when using "Exclude Dungeons Without Essence" to know which dungeons you can ignore.
    If "Shuffle Essences" is enabled, this option has no effect.
    - Disabled: Dungeons with an essence are never shown on the map
    - With Compass: Dungeons with an essence can only be highlighted after obtaining their Compass
    - Always: Dungeons with an essence are always shown on the map
    """
    # TODO: - With Treasure Map: Dungeons with an essence all become highlighted when you obtain the unique Treasure Map item
    display_name = "Show Dungeons With Essence"

    option_disabled = 0
    option_with_compass = 1
    option_always = 2

    default = 1
    include_in_patch = True


class OracleOfSeasonsMasterKeys(Choice):
    """
    - Disabled: All dungeon keys must be obtained individually, just like in vanilla
    - All Small Keys: Small Keys are replaced by a single Master Key for each dungeon which is capable of opening
      every small keydoor for that dungeon
    - All Dungeon Keys: the Master Key for each dungeon is also capable of opening the boss keydoor,
      removing Boss Keys from the item pool
    Master Keys placement is determined following the "Keysanity (Small Keys)" option.
    """
    display_name = "Master Keys"

    option_disabled = 0
    option_all_small_keys = 1
    option_all_dungeon_keys = 2

    default = 0
    include_in_patch = True
    include_in_slot_data = True


class OracleOfSeasonsSmallKeyShuffle(Toggle):
    """
    If enabled, dungeon Small Keys can be found anywhere instead of being confined in their dungeon of origin.
    """
    display_name = "Keysanity (Small Keys)"

    include_in_patch = True
    include_in_slot_data = True


class OracleOfSeasonsBossKeyShuffle(Toggle):
    """
    If enabled, dungeon Boss Keys can be found anywhere instead of being confined in their dungeon of origin.
    """
    display_name = "Keysanity (Boss Keys)"

    include_in_patch = True
    include_in_slot_data = True


class OracleOfSeasonsMapCompassShuffle(Toggle):
    """
    If enabled, Dungeon Maps and Compasses can be found anywhere instead of being confined in their dungeon of origin.
    """
    display_name = "Maps & Compasses Outside Dungeon"

    include_in_patch = True
    include_in_slot_data = True


class OracleOfSeasonsD0AltEntrance(Toggle):
    """
    If enabled, remove the hole acting as an alternate entrance to Hero’s Cave. Stairs will be added inside the dungeon to make the chest reachable.
    This is especially useful when shuffling dungeons, since only main dungeon entrances are shuffled.
    If this option is not set in such a case, you could potentially have two distant entrances leading to the same dungeon.
    """
    display_name = "Remove Hero's Cave Alt. Entrance"

    include_in_patch = True
    include_in_slot_data = True


class OracleOfSeasonsD2AltEntrance(Toggle):
    """
    If enabled, remove both stairs acting as alternate entrances to Snake’s Remains and connect them together inside the dungeon.
    This is especially useful when shuffling dungeons, since only main dungeon entrances are shuffled.
    If this option is not set in such a case, you could potentially have two distant entrances leading to the same dungeon.
    """
    display_name = "Remove D2 Alt. Entrance"

    include_in_patch = True
    include_in_slot_data = True


class OraclesOfSeasonsTreehouseOldManRequirement(Range):
    """
    The amount of essences that you need to bring to the treehouse old man for him to give his item.
    """
    display_name = "Treehouse Old Man Requirement"

    range_start = 0
    range_end = 8

    default = 5
    include_in_patch = True
    include_in_slot_data = True


class OraclesOfSeasonsTarmGateRequirement(Range):
    """
    The number of jewels that you need to bring to Tarm Ruins gate to be able to open it.
    """
    display_name = "Tarm Ruins Gate Required Jewels"

    range_start = 0
    range_end = 4

    default = 4
    include_in_patch = True
    include_in_slot_data = True


class OraclesOfSeasonsGoldenBeastsRequirement(Range):
    """
    The amount of golden beasts that need to be beaten for the golden old man to give his item.
    Golden beasts are 4 unique enemies that appear at specific spots on specific seasons, and beating all four of them
    requires all seasons and having access to most of the overworld.
    """
    display_name = "Golden Beasts Requirement"

    range_start = 0
    range_end = 4

    default = 1
    include_in_patch = True
    include_in_slot_data = True


class OracleOfSeasonsSignGuyRequirement(NamedRange):
    """
    In Subrosia, a NPC will "punish" you if you break more than 100 signs in the vanilla game by giving you an item.
    This option lets you configure how many signs are required to obtain that item, since breaking 100 signs is not
    everyone's cup of tea.
    """
    display_name = "Sign Guy Requirement"

    range_start = 0
    range_end = 250

    default = 10
    special_range_names = {
        "vanilla": 100
    }
    include_in_patch = True


class OracleOfSeasonsGashaNutKillRequirement(NamedRange):
    """
    This option lets you configure how many kills are required to make a gasha tree grow.
    Using a gasha ring halves this number.
    """
    display_name = "Gasha Nut Requirement"

    range_start = 0
    range_end = 250

    default = 20
    special_range_names = {
        "vanilla": 40
    }
    include_in_patch = True


class OracleOfSeasonsLostWoodsItemSequence(DefaultOnToggle):
    """
    If enabled, the secret sequence leading to the Noble Sword pedestal will be randomized (both directions to
    take and seasons to use).
    To know the randomized combination, you will need to bring the Phonograph to the Deku Scrub near the stump, just
    like in the vanilla game.
    """
    display_name = "Randomize Lost Woods Item Sequence"

    include_in_slot_data = True


class OracleOfSeasonsLostWoodsMainSequence(Toggle):
    """
    If enabled, the secret sequence leading to D6 sector will be randomized (both directions to take and
    seasons to use).
    To know the randomized combination, you will need to stun the Deku Scrub near the jewel gate using a shield, just
    like in the vanilla game.
    """
    display_name = "Randomize Lost Woods Main Sequence"

    include_in_slot_data = True


class OracleOfSeasonsSamasaGateCode(Toggle):
    """
    This option defines if the secret combination which opens the gate to Samasa Desert should be randomized.
    You can then configure the length of the sequence with the next option.
    """
    display_name = "Randomize Samasa Desert Gate Code"


class OracleOfSeasonsSamasaGateCodeLength(Range):
    """
    The length of the randomized combination for Samasa Desert gate.
    This option has no effect if "Randomize Samasa Desert Gate Code" is disabled.
    """
    display_name = "Samasa Desert Gate Code Length"

    range_start = 1
    range_end = 40

    default = 8


class OracleOfSeasonsGashaLocations(Range):
    """
    When set to a non-zero value, planting a Gasha tree on a unique soil gives a deterministic item which is taken
    into account by logic. Once an item has been obtained this way, the soil disappears forever to avoid any chance
    of softlocking by wasting several Gasha Seeds on the same soil.
    The value of this option is the number of items that can be obtained that way, the maximum value expecting you
    to plant a tree on each one of the 16 Gasha spots in the game.
    """
    display_name = "Deterministic Gasha Locations"

    range_start = 0
    range_end = 16

    default = 0
    include_in_patch = True
    include_in_slot_data = True


class OracleOfSeasonsRequiredRings(ItemSet):
    """
    Forces a specified set of rings to appear somewhere in the seed.
    Adding too many rings to this list can cause generation failures.
    List of ring names can be found here: https://zeldawiki.wiki/wiki/Magic_Ring
    """
    display_name = "Required Rings"
    valid_keys = {name for name, idata in ITEMS_DATA.items() if "ring" in idata}


class OracleOfSeasonsExcludedRings(ItemSet):
    """
    Forces a specified set of rings to not appear in the seed.
    List of ring names can be found here: https://zeldawiki.wiki/wiki/Magic_Ring
    """
    display_name = "Excluded Rings"
    default = {name for name, idata in ITEMS_DATA.items() if "ring" in idata and idata["ring"] == "useless"}
    valid_keys = {name for name, idata in ITEMS_DATA.items() if "ring" in idata}


class OracleOfSeasonsShopPrices(Choice):
    """
    Determine the cost of items found in shops of all sorts (including Subrosian Market and Business Scrubs):
    - Vanilla: shop items have the same cost as in the base game
    - Free: all shop items can be obtained for free
    - Cheap: shop prices are randomized with an average cost of 50 Rupees
    - Reasonable: shop prices are randomized with an average cost of 100 Rupees
    - Expensive: shop prices are randomized with an average cost of 200 Rupees
    - Outrageous: shop prices are randomized with an average cost of 350 Rupees
    """
    display_name = "Shop Prices"

    option_vanilla = 0
    option_free = 1
    option_cheap = 2
    option_reasonable = 3
    option_expensive = 4
    option_outrageous = 5

    default = 0


class OracleOfSeasonsAdvanceShop(Toggle):
    """
    In the vanilla game, there is a house northwest of Horon Village hosting the secret "Advance Shop" that can only
    be accessed if the game is being played on a Game Boy Advance console.
    If enabled, this option makes this shop always open, adding 3 shop locations to the game (and some rupees to the
    item pool to compensate for the extra purchases that might be required)
    """
    display_name = "Open Advance Shop"

    include_in_patch = True
    include_in_slot_data = True


class OracleOfSeasonsFoolsOre(Choice):
    """
    In the vanilla game, the Fool's Ore is the item "given" by the strange brothers in "exchange" for your feather.
    The way the vanilla game is done means you never get to use it, but it's by far the strongest weapon in the game
    (dealing 4 times more damage than an L-2 sword!)
    - Vanilla: Fool's Ore appears in the item pool with its stats unchanged
    - Balanced: Fool's Ore appears in the item pool but its stats are lowered to become comparable to an L-2 sword
    - Excluded: Fool's Ore doesn't appear in the item pool at all. Problem solved!
    """
    display_name = "Fool's Ore"

    option_vanilla = 0
    option_balanced = 1
    option_excluded = 2

    default = 1
    include_in_patch = True


class OracleOfSeasonsEnforcePotionInShop(Toggle):
    """
    When enabled, you are guaranteed to have a renewable Potion for 300 rupees inside Horon shop
    """
    display_name = "Enforce Potion in Shop"

    include_in_patch = True
    include_in_slot_data = True


class OracleOfSeasonsCombatDifficulty(Choice):
    """
    Modifies the damage taken during combat to make this aspect of the game easier or harder depending on the
    type of experience you want to have
    """
    display_name = "Combat Difficulty"

    option_peaceful = 4
    option_easier = 2
    option_vanilla = 0
    option_harder = -2
    option_insane = -4

    default = 0
    include_in_patch = True


class OracleOfSeasonsQuickFlute(DefaultOnToggle):
    """
    When enabled, playing the flute will immobilize you during a very small amount of time compared to vanilla game.
    """
    display_name = "Quick Flute"

    include_in_patch = True


class OracleOfSeasonsRosaQuickUnlock(Toggle):
    """
    When enabled, Rosa will instantly unlock all subrosia locks when given the Ribbon
    """
    display_name = "Rosa Quick Unlock"

    include_in_patch = True


class OracleOfSeasonsStartingMapsCompasses(Toggle):
    """
    When enabled, you will start the game with maps and compasses for every dungeon in the game.
    This makes navigation easier and removes those items for the pool, which are replaced with random filler items.
    """
    display_name = "Start with Dungeon Maps & Compasses"

    include_in_patch = True
    include_in_slot_data = True


class OracleOfSeasonsRandomizeAi(Toggle):
    """
    When enabled, enemy AI will be randomized.
    This option is only visible on yamls generated in April.

    ⚠ This option may cause logic issues or unbeatable seeds due to some untested combos caused
    by the high number of possibilities. Some graphical oddities are also to be expected.
    ⚠ Required golden beasts is 0 because you are not guaranteed to get an enemy
    with a golden beast AI that would be counted for the old man
    """
    display_name = "Randomize AI"

    include_in_patch = True
    visibility = Visibility.all if (datetime.now().month == 4) else Visibility.none  # Only visible in april


class OracleOfSeasonsRemoveItemsFromPool(ItemDict):
    """
    Removes specified amount of given items from the item pool, replacing them with random filler items.
    This option has significant chances to break generation if used carelessly, so test your preset several times
    before using it on long generations. Use at your own risk!
    """
    display_name = "Remove Items from Pool"
    verify_item_name = False


class OracleOfSeasonsIncludeCrossItems(Toggle):
    """
    When enabled, add the cane of somaria to the item pool
    ⚠ Requires the Oracles of Ages US ROM on patch, you won't be able to play without
    """
    display_name = "Cross Items"
    include_in_patch = True


class OracleOfSeasonsIncludeSecretLocations(Toggle):
    """
    When enabled, add the linked game secrets to the list of locations
    """
    display_name = "Secret Locations"

    include_in_patch = True
    include_in_slot_data = True


class OracleOfSeasonsDeathLink(DeathLink):
    """
    When you die, everyone who enabled death link dies. Of course, the reverse is true too.
    """
    include_in_slot_data = True  # This is for the bizhawk client


class OracleOfSeasonsMoveLink(Toggle):
    """
    When enabled, movement will be linked between games that enabled this option.
    This option is only visible on yamls generated in April.

    ⚠ This option may easily cause softlocks and may cause some issues. Some graphical oddities are also to be expected.
    """
    display_name = "Randomize AI"
    visibility = Visibility.all if (datetime.now().month == 4) else Visibility.none  # Only visible in april

    include_in_slot_data = True  # This is for the bizhawk client


class OracleOfSeasonsBirdHint(Choice):
    """
    Disabled: The Owls and Know-it-all birds say their vanilla text when talked to
    Know-it-all: Enable region hints from the birds in the house next to the advance shop
    Owl: Enable owls to give hints about items from your world
    """
    display_name = "Bird Hint"

    option_disabled = 0b00
    option_know_it_all = 0b01
    option_owl = 0b10
    option_both = 0b11

    default = option_both

    def know_it_all(self) -> bool:
        return bool(self.value & OracleOfSeasonsBirdHint.option_know_it_all)

    def owl(self) -> bool:
        return bool(self.value & OracleOfSeasonsBirdHint.option_owl)


@dataclass
class OracleOfSeasonsOptions(PerGameCommonOptions):
    accessibility: ItemsAccessibility
    goal: OracleOfSeasonsGoal
    logic_difficulty: OracleOfSeasonsLogicDifficulty
    death_link: OracleOfSeasonsDeathLink

    # Optional locations
    advance_shop: OracleOfSeasonsAdvanceShop
    shuffle_old_men: OracleOfSeasonsOldMenShuffle
    shuffle_business_scrubs: OracleOfSeasonsBusinessScrubsShuffle
    shuffle_golden_ore_spots: OracleOfSeasonsGoldenOreSpotsShuffle
    deterministic_gasha_locations: OracleOfSeasonsGashaLocations
    secret_locations: OracleOfSeasonsIncludeSecretLocations

    # Essences
    required_essences: OracleOfSeasonsRequiredEssences
    shuffle_essences: OracleOfSeasonsEssenceSanity
    placed_essences: OracleOfSeasonsPlacedEssences
    exclude_dungeons_without_essence: OracleOfSeasonsExcludeDungeonsWithoutEssence
    show_dungeons_with_essence: OracleOfSeasonsShowDungeonsWithEssence

    # Seasons
    default_seasons: OracleOfSeasonsDefaultSeasons
    normalize_horon_village_season: OracleOfSeasonsHoronSeason

    # Overworld layout options
    animal_companion: OracleOfSeasonsAnimalCompanion
    shuffle_portals: OracleOfSeasonsPortalShuffle
    shuffle_dungeons: OracleOfSeasonsDungeonShuffle
    remove_d0_alt_entrance: OracleOfSeasonsD0AltEntrance
    remove_d2_alt_entrance: OracleOfSeasonsD2AltEntrance
    default_seed: OracleOfSeasonsDefaultSeedType
    duplicate_seed_tree: OracleOfSeasonsDuplicateSeedTree

    # Dungeon items
    master_keys: OracleOfSeasonsMasterKeys
    keysanity_small_keys: OracleOfSeasonsSmallKeyShuffle
    keysanity_boss_keys: OracleOfSeasonsBossKeyShuffle
    keysanity_maps_compasses: OracleOfSeasonsMapCompassShuffle
    starting_maps_compasses: OracleOfSeasonsStartingMapsCompasses

    # Numeric requirements for some checks / access to regions
    treehouse_old_man_requirement: OraclesOfSeasonsTreehouseOldManRequirement
    tarm_gate_required_jewels: OraclesOfSeasonsTarmGateRequirement
    golden_beasts_requirement: OraclesOfSeasonsGoldenBeastsRequirement
    sign_guy_requirement: OracleOfSeasonsSignGuyRequirement
    gasha_nut_kill_requirement: OracleOfSeasonsGashaNutKillRequirement

    # Other randomizable stuff
    randomize_lost_woods_item_sequence: OracleOfSeasonsLostWoodsItemSequence
    randomize_lost_woods_main_sequence: OracleOfSeasonsLostWoodsMainSequence
    randomize_samasa_gate_code: OracleOfSeasonsSamasaGateCode
    samasa_gate_code_length: OracleOfSeasonsSamasaGateCodeLength

    # QOL
    quick_flute: OracleOfSeasonsQuickFlute
    rosa_quick_unlock: OracleOfSeasonsRosaQuickUnlock

    # Miscellaneous options
    shop_prices: OracleOfSeasonsShopPrices
    enforce_potion_in_shop: OracleOfSeasonsEnforcePotionInShop
    required_rings: OracleOfSeasonsRequiredRings
    excluded_rings: OracleOfSeasonsExcludedRings
    fools_ore: OracleOfSeasonsFoolsOre
    cross_items: OracleOfSeasonsIncludeCrossItems
    combat_difficulty: OracleOfSeasonsCombatDifficulty
    bird_hint: OracleOfSeasonsBirdHint
    randomize_ai: OracleOfSeasonsRandomizeAi
    move_link: OracleOfSeasonsMoveLink

    start_inventory_from_pool: StartInventoryPool
    remove_items_from_pool: OracleOfSeasonsRemoveItemsFromPool


option_groups = [
    OptionGroup("General", [
        ItemsAccessibility,
        OracleOfSeasonsGoal,
        OracleOfSeasonsLogicDifficulty,
        OracleOfSeasonsIncludeCrossItems,
        OracleOfSeasonsDeathLink,
    ]),
    OptionGroup("Optional Locations", [
        OracleOfSeasonsAdvanceShop,
        OracleOfSeasonsOldMenShuffle,
        OracleOfSeasonsBusinessScrubsShuffle,
        OracleOfSeasonsGoldenOreSpotsShuffle,
        OracleOfSeasonsGashaLocations,
        OracleOfSeasonsIncludeSecretLocations
    ]),
    OptionGroup("Essences", [
        OracleOfSeasonsRequiredEssences,
        OracleOfSeasonsEssenceSanity,
        OracleOfSeasonsPlacedEssences,
        OracleOfSeasonsExcludeDungeonsWithoutEssence,
        OracleOfSeasonsShowDungeonsWithEssence,
    ]),
    OptionGroup("Seasons", [
        OracleOfSeasonsDefaultSeasons,
        OracleOfSeasonsHoronSeason,
    ]),
    OptionGroup("Overworld Layout Options", [
        OracleOfSeasonsAnimalCompanion,
        OracleOfSeasonsPortalShuffle,
        OracleOfSeasonsDungeonShuffle,
        OracleOfSeasonsD0AltEntrance,
        OracleOfSeasonsD2AltEntrance,
        OracleOfSeasonsDefaultSeedType,
        OracleOfSeasonsDuplicateSeedTree,
    ]),
    OptionGroup("Dungeon Items", [
        OracleOfSeasonsMasterKeys,
        OracleOfSeasonsSmallKeyShuffle,
        OracleOfSeasonsBossKeyShuffle,
        OracleOfSeasonsMapCompassShuffle,
        OracleOfSeasonsStartingMapsCompasses
    ]),
    OptionGroup("Numeric Requirements", [
        OraclesOfSeasonsTreehouseOldManRequirement,
        OraclesOfSeasonsTarmGateRequirement,
        OraclesOfSeasonsGoldenBeastsRequirement,
        OracleOfSeasonsSignGuyRequirement,
        OracleOfSeasonsGashaNutKillRequirement,
    ]),
    OptionGroup("Randomizable Sequences", [
        OracleOfSeasonsLostWoodsItemSequence,
        OracleOfSeasonsLostWoodsMainSequence,
        OracleOfSeasonsSamasaGateCode,
        OracleOfSeasonsSamasaGateCodeLength,
    ]),
    OptionGroup("QOL", [
        OracleOfSeasonsQuickFlute,
        OracleOfSeasonsRosaQuickUnlock,
    ]),
    OptionGroup("Others", [
        OracleOfSeasonsShopPrices,
        OracleOfSeasonsEnforcePotionInShop,
        OracleOfSeasonsRequiredRings,
        OracleOfSeasonsExcludedRings,
        OracleOfSeasonsFoolsOre,
        OracleOfSeasonsCombatDifficulty,
        OracleOfSeasonsBirdHint,
        OracleOfSeasonsRandomizeAi,
        OracleOfSeasonsMoveLink,
        OracleOfSeasonsRemoveItemsFromPool
    ]),
]
