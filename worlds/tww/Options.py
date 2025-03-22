from dataclasses import dataclass

from Options import (
    Choice,
    DeathLink,
    DefaultOnToggle,
    OptionGroup,
    OptionSet,
    PerGameCommonOptions,
    Range,
    StartInventoryPool,
    Toggle,
)

from .Locations import DUNGEON_NAMES


class Dungeons(DefaultOnToggle):
    """
    This controls whether dungeon locations are randomized.
    """

    display_name = "Dungeons"


class TingleChests(Toggle):
    """
    Tingle Chests are hidden in dungeons and must be bombed to make them appear. (2 in DRC, 1 each in FW, TotG, ET, and
    WT). This controls whether they are randomized.
    """

    display_name = "Tingle Chests"


class DungeonSecrets(Toggle):
    """
    DRC, FW, TotG, ET, and WT each contain 2-3 secret items (11 in total). This controls whether these are randomized.

    The items are relatively well-hidden (they aren't in chests), so don't select this option unless you're prepared to
    search each dungeon high and low!
    """

    display_name = "Dungeon Secrets"


class PuzzleSecretCaves(DefaultOnToggle):
    """
    This controls whether the rewards from puzzle-focused secret caves are randomized locations.
    """

    display_name = "Puzzle Secret Caves"


class CombatSecretCaves(Toggle):
    """
    This controls whether the rewards from combat-focused secret caves (besides Savage Labyrinth) are randomized
    locations.
    """

    display_name = "Combat Secret Caves"


class SavageLabyrinth(Toggle):
    """
    This controls whether the two locations in Savage Labyrinth are randomized.
    """

    display_name = "Savage Labyrinth"


class GreatFairies(DefaultOnToggle):
    """
    This controls whether the items given by Great Fairies are randomized.
    """

    display_name = "Great Fairies"


class ShortSidequests(Toggle):
    """
    This controls whether sidequests that can be completed quickly are randomized.
    """

    display_name = "Short Sidequests"


class LongSidequests(Toggle):
    """
    This controls whether long sidequests (e.g., Lenzo's assistant, withered trees, goron trading) are randomized.
    """

    display_name = "Long Sidequests"


class SpoilsTrading(Toggle):
    """
    This controls whether the items you get by trading in spoils to NPCs are randomized.
    """

    display_name = "Spoils Trading"


class Minigames(Toggle):
    """
    This controls whether most minigames are randomized (auctions, mail sorting, barrel shooting, bird-man contest).
    """

    display_name = "Minigames"


class Battlesquid(Toggle):
    """
    This controls whether the Windfall battleship minigame is randomized.
    """

    display_name = "Battlesquid Minigame"


class FreeGifts(DefaultOnToggle):
    """
    This controls whether gifts freely given by NPCs are randomized (Tott, Salvage Corp, imprisoned Tingle).
    """

    display_name = "Free Gifts"


class Mail(Toggle):
    """
    This controls whether items received from the mail are randomized.
    """

    display_name = "Mail"


class PlatformsRafts(Toggle):
    """
    This controls whether lookout platforms and rafts are randomized.
    """

    display_name = "Lookout Platforms and Rafts"


class Submarines(Toggle):
    """
    This controls whether submarines are randomized.
    """

    display_name = "Submarines"


class EyeReefChests(Toggle):
    """
    This controls whether the chests that appear after clearing out the eye reefs are randomized.
    """

    display_name = "Eye Reef Chests"


class BigOctosGunboats(Toggle):
    """
    This controls whether the items dropped by Big Octos and Gunboats are randomized.
    """

    display_name = "Big Octos and Gunboats"


class TriforceCharts(Toggle):
    """
    This controls whether the sunken treasure chests marked on Triforce Charts are randomized.
    """

    display_name = "Sunken Treasure (From Triforce Charts)"


class TreasureCharts(Toggle):
    """
    This controls whether the sunken treasure chests marked on Treasure Charts are randomized.
    """

    display_name = "Sunken Treasure (From Treasure Charts)"


class ExpensivePurchases(DefaultOnToggle):
    """
    This controls whether items that cost many Rupees are randomized (Rock Spire shop, auctions, Tingle's letter,
    trading quest).
    """

    display_name = "Expensive Purchases"


class IslandPuzzles(Toggle):
    """
    This controls whether various island puzzles are randomized (e.g., chests hidden in unusual places).
    """

    display_name = "Island Puzzles"


class Misc(Toggle):
    """
    Miscellaneous locations that don't fit into any of the above categories (outdoors chests, wind shrine, Cyclos, etc).
    This controls whether these are randomized.
    """

    display_name = "Miscellaneous"


class DungeonItem(Choice):
    """
    This is the base class for the shuffle options for dungeon items.
    """

    value: int
    option_startwith = 0
    option_vanilla = 1
    option_dungeon = 2
    option_any_dungeon = 3
    option_local = 4
    option_keylunacy = 5
    default = 2

    @property
    def in_dungeon(self) -> bool:
        """
        Return whether the item should be shuffled into a dungeon.

        :return: Whether the item is shuffled into a dungeon.
        """
        return self.value in (2, 3)


class RandomizeMapCompass(DungeonItem):
    """
    Controls how dungeon maps and compasses are randomized.

    - **Start With Maps & Compasses:** You will start the game with the dungeon maps and compasses for all dungeons.
    - **Vanilla Maps & Compasses:** Dungeon maps and compasses will be kept in their vanilla location (non-randomized).
    - **Own Dungeon Maps & Compasses:** Dungeon maps and compasses will be randomized locally within their own dungeon.
    - **Any Dungeon Maps & Compasses:** Dungeon maps and compasses will be randomized locally within any dungeon.
    - **Local Maps & Compasses:** Dungeon maps and compasses will be randomized locally anywhere.
    - **Key-Lunacy:** Dungeon maps and compasses can be found anywhere, without restriction.
    """

    item_name_group = "Dungeon Items"
    display_name = "Randomize Maps & Compasses"
    default = 2


class RandomizeSmallKeys(DungeonItem):
    """
    Controls how small keys are randomized.

    - **Start With Small Keys:** You will start the game with the small keys for all dungeons.
    - **Vanilla Small Keys:** Small keys will be kept in their vanilla location (non-randomized).
    - **Own Dungeon Small Keys:** Small keys will be randomized locally within their own dungeon.
    - **Any Dungeon Small Keys:** Small keys will be randomized locally within any dungeon.
    - **Local Small Keys:** Small keys will be randomized locally anywhere.
    - **Key-Lunacy:** Small keys can be found in any progression location, if dungeons are randomized.
    """

    item_name_group = "Small Keys"
    display_name = "Randomize Small Keys"
    default = 2


class RandomizeBigKeys(DungeonItem):
    """
    Controls how big keys are randomized.

    - **Start With Big Keys:** You will start the game with the big keys for all dungeons.
    - **Vanilla Big Keys:** Big keys will be kept in their vanilla location (non-randomized).
    - **Own Dungeon Big Keys:** Big keys will be randomized locally within their own dungeon.
    - **Any Dungeon Big Keys:** Big keys will be randomized locally within any dungeon.
    - **Local Big Keys:** Big keys will be randomized locally anywhere.
    - **Key-Lunacy:** Big keys can be found in any progression location, if dungeons are randomized.
    """

    item_name_group = "Big Keys"
    display_name = "Randomize Big Keys"
    default = 2


class SwordMode(Choice):
    """
    Controls whether you start with the Hero's Sword, the Hero's Sword is randomized, or if there are no swords in the
    entire game.

    - **Start with Hero's Sword:** You will start the game with the basic Hero's Sword already in your inventory.
    - **No Starting Sword:** You will start the game with no sword, and have to find it somewhere in the world like
      other randomized items.
    - **Swords Optional:** You will start the game with no sword, but they'll still be randomized. However, they are not
      necessary to beat the game. The Hyrule Barrier will be gone, Phantom Ganon in FF is vulnerable to Skull Hammer,
      and the logic does not expect you to have a sword.
    - **Swordless:** You will start the game with no sword, and won't be able to find it anywhere. You have to beat the
      entire game using other items as weapons instead of the sword. (Note that Phantom Ganon in FF becomes vulnerable
      to Skull Hammer in this mode.)
    """

    display_name = "Sword Mode"
    option_start_with_sword = 0
    option_no_starting_sword = 1
    option_swords_optional = 2
    option_swordless = 3
    default = 0


class RequiredBosses(Toggle):
    """
    In this mode, you will not be allowed to beat the game until certain randomly-chosen bosses are defeated. Nothing in
    dungeons for other bosses will ever be required.

    You can see which islands have the required bosses on them by opening the sea chart and checking which islands have
    blue quest markers.
    """

    display_name = "Required Bosses Mode"


class NumRequiredBosses(Range):
    """
    Select the number of randomly-chosen bosses that are required in Required Bosses Mode.

    The door to Puppet Ganon will not unlock until you've defeated all of these bosses. Nothing in dungeons for other
    bosses will ever be required.
    """

    display_name = "Number of Required Bosses"
    range_start = 1
    range_end = 6
    default = 4


class IncludedDungeons(OptionSet):
    """
    A list of dungeons that should always be included when required bosses mode is on.
    """

    display_name = "Included Dungeons"
    valid_keys = frozenset(DUNGEON_NAMES)


class ExcludedDungeons(OptionSet):
    """
    A list of dungeons that should always be excluded when required bosses mode is on.
    """

    display_name = "Excluded Dungeons"
    valid_keys = frozenset(DUNGEON_NAMES)


class ChestTypeMatchesContents(Toggle):
    """
    Changes the chest type to reflect its contents. A metal chest has a progress item, a wooden chest has a non-progress
    item or a consumable, and a green chest has a potentially required dungeon key.
    """

    display_name = "Chest Type Matches Contents"


class TrapChests(Toggle):
    """
    **DEV NOTE:** This option is currently unimplemented and will be ignored.

    Allows the randomizer to place several trapped chests across the game that do not give you items. Perfect for
    spicing up any run!
    """

    display_name = "Enable Trap Chests"


class HeroMode(Toggle):
    """
    In Hero Mode, you take four times more damage than normal and heart refills will not drop.
    """

    display_name = "Hero Mode"


class LogicObscurity(Choice):
    """
    Obscure tricks are ways of obtaining items that are not obvious and may involve thinking outside the box.

    This option controls the maximum difficulty of obscure tricks the randomizer will require you to do to beat the
    game.
    """

    display_name = "Obscure Tricks Required"
    option_none = 0
    option_normal = 1
    option_hard = 2
    option_very_hard = 3
    default = 0


class LogicPrecision(Choice):
    """
    Precise tricks are ways of obtaining items that involve difficult inputs such as accurate aiming or perfect timing.

    This option controls the maximum difficulty of precise tricks the randomizer will require you to do to beat the
    game.
    """

    display_name = "Precise Tricks Required"
    option_none = 0
    option_normal = 1
    option_hard = 2
    option_very_hard = 3
    default = 0


class EnableTunerLogic(Toggle):
    """
    If enabled, the randomizer can logically expect the Tingle Tuner for Tingle Chests.

    The randomizer behavior of logically expecting Bombs/bomb flowers to spawn in Tingle Chests remains unchanged.
    """

    display_name = "Enable Tuner Logic"


class RandomizeDungeonEntrances(Toggle):
    """
    Shuffles around which dungeon entrances take you into which dungeons.

    (No effect on Forsaken Fortress or Ganon's Tower.)
    """

    display_name = "Randomize Dungeons"


class RandomizeSecretCavesEntrances(Toggle):
    """
    Shuffles around which secret cave entrances take you into which secret caves.
    """

    display_name = "Randomize Secret Caves"


class RandomizeMinibossEntrances(Toggle):
    """
    Allows dungeon miniboss doors to act as entrances to be randomized.

    If on with random dungeon entrances, dungeons may nest within each other, forming chains of connected dungeons.
    """

    display_name = "Randomize Nested Minibosses"


class RandomizeBossEntrances(Toggle):
    """
    Allows dungeon boss doors to act as entrances to be randomized.

    If on with random dungeon entrances, dungeons may nest within each other, forming chains of connected dungeons.
    """

    display_name = "Randomize Nested Bosses"


class RandomizeSecretCaveInnerEntrances(Toggle):
    """
    Allows the pit in Ice Ring Isle's secret cave and the rear exit out of Cliff Plateau Isles' secret cave to act as
    entrances to be randomized."""

    display_name = "Randomize Inner Secret Caves"


class RandomizeFairyFountainEntrances(Toggle):
    """
    Allows the pits that lead down into Fairy Fountains to act as entrances to be randomized.
    """

    display_name = "Randomize Fairy Fountains"


class MixEntrances(Choice):
    """
    Controls how the different types (pools) of randomized entrances should be shuffled.

    - **Separate Pools:** Each pool of randomized entrances will shuffle into itself (e.g., dungeons into dungeons).
    - **Mix Pools:** All pools of randomized entrances will be combined into one pool to be shuffled.
    """

    display_name = "Mix Entrances"
    option_separate_pools = 0
    option_mix_pools = 1
    default = 0


class RandomizeEnemies(Toggle):
    """
    Randomizes the placement of non-boss enemies.

    This option is an *incomplete* option from the base randomizer and **may result in unbeatable seeds! Use at your own
    risk!**
    """

    display_name = "Randomize Enemies"


# class RandomizeMusic(Toggle):
#     """
#     Shuffles around all the music in the game. This affects background music, combat music, fanfares, etc.
#     """

#     display_name = "Randomize Music"


class RandomizeStartingIsland(Toggle):
    """
    Randomizes which island you start the game on.
    """

    display_name = "Randomize Starting Island"


class RandomizeCharts(Toggle):
    """
    Randomizes which sector is drawn on each Triforce/Treasure Chart.
    """

    display_name = "Randomize Charts"


class HoHoHints(DefaultOnToggle):
    """
    **DEV NOTE:** This option is currently unimplemented and will be ignored.

    Places hints on Old Man Ho Ho. Old Man Ho Ho appears at 10 different islands in the game. Talk to Old Man Ho Ho to
    get hints.
    """

    display_name = "Place Hints on Old Man Ho Ho"


class FishmenHints(DefaultOnToggle):
    """
    **DEV NOTE:** This option is currently unimplemented and will be ignored.

    Places hints on the fishmen. There is one fishman at each of the 49 islands of the Great Sea. Each fishman must be
    fed an All-Purpose Bait before he will give a hint.
    """

    display_name = "Place Hints on Fishmen"


class KoRLHints(Toggle):
    """
    **DEV NOTE:** This option is currently unimplemented and will be ignored.

    Places hints on the King of Red Lions. Talk to the King of Red Lions to get hints.
    """

    display_name = "Place Hints on King of Red Lions"


class NumItemHints(Range):
    """
    **DEV NOTE:** This option is currently unimplemented and will be ignored.

    The number of item hints that will be placed. Item hints tell you which area contains a particular progress item in
    this seed.

    If multiple hint placement options are selected, the hint count will be split evenly among the placement options.
    """

    display_name = "Item Hints"
    range_start = 0
    range_end = 15
    default = 15


class NumLocationHints(Range):
    """
    **DEV NOTE:** This option is currently unimplemented and will be ignored.

    The number of location hints that will be placed. Location hints tell you what item is at a specific location in
    this seed.

    If multiple hint placement options are selected, the hint count will be split evenly among the placement options.
    """

    display_name = "Location Hints"
    range_start = 0
    range_end = 15
    default = 5


class NumBarrenHints(Range):
    """
    **DEV NOTE:** This option is currently unimplemented and will be ignored.

    The number of barren hints that will be placed. Barren hints tell you that an area does not contain any required
    items in this seed.

    If multiple hint placement options are selected, the hint count will be split evenly among the placement options.
    """

    display_name = "Barren Hints"
    range_start = 0
    range_end = 15
    default = 0


class NumPathHints(Range):
    """
    **DEV NOTE:** This option is currently unimplemented and will be ignored.

    The number of path hints that will be placed. Path hints tell you that an area contains an item that is required to
    reach a particular goal in this seed.

    If multiple hint placement options are selected, the hint count will be split evenly among the placement options.
    """

    display_name = "Path Hints"
    range_start = 0
    range_end = 15
    default = 0


class PrioritizeRemoteHints(Toggle):
    """
    **DEV NOTE:** This option is currently unimplemented and will be ignored.

    When this option is selected, certain locations that are out of the way and time-consuming to complete will take
    precedence over normal location hints."""

    display_name = "Prioritize Remote Location Hints"


class SwiftSail(DefaultOnToggle):
    """
    Sailing speed is doubled and the direction of the wind is always at your back as long as the sail is out.
    """

    display_name = "Swift Sail"


class InstantTextBoxes(DefaultOnToggle):
    """
    Text appears instantly. Also, the B button is changed to instantly skip through text as long as you hold it down.
    """

    display_name = "Instant Text Boxes"


class RevealFullSeaChart(DefaultOnToggle):
    """
    Start the game with the sea chart fully drawn out.
    """

    display_name = "Reveal Full Sea Chart"


class AddShortcutWarpsBetweenDungeons(Toggle):
    """
    Adds new warp pots that act as shortcuts connecting dungeons to each other directly. (DRC, FW, TotG, and separately
    FF, ET, WT.)

    Each pot must be unlocked before it can be used, so you cannot use them to access dungeons
    you wouldn't already have access to.
    """

    display_name = "Add Shortcut Warps Between Dungeons"


class SkipRematchBosses(DefaultOnToggle):
    """
    Removes the door in Ganon's Tower that only unlocks when you defeat the rematch versions of Gohma, Kalle Demos,
    Jalhalla, and Molgera.
    """

    display_name = "Skip Boss Rematches"


class RemoveMusic(Toggle):
    """
    Mutes all ingame music.
    """

    display_name = "Remove Music"


@dataclass
class TWWOptions(PerGameCommonOptions):
    """
    A data class that encapsulates all configuration options for The Wind Waker.
    """

    start_inventory_from_pool: StartInventoryPool
    progression_dungeons: Dungeons
    progression_tingle_chests: TingleChests
    progression_dungeon_secrets: DungeonSecrets
    progression_puzzle_secret_caves: PuzzleSecretCaves
    progression_combat_secret_caves: CombatSecretCaves
    progression_savage_labyrinth: SavageLabyrinth
    progression_great_fairies: GreatFairies
    progression_short_sidequests: ShortSidequests
    progression_long_sidequests: LongSidequests
    progression_spoils_trading: SpoilsTrading
    progression_minigames: Minigames
    progression_battlesquid: Battlesquid
    progression_free_gifts: FreeGifts
    progression_mail: Mail
    progression_platforms_rafts: PlatformsRafts
    progression_submarines: Submarines
    progression_eye_reef_chests: EyeReefChests
    progression_big_octos_gunboats: BigOctosGunboats
    progression_triforce_charts: TriforceCharts
    progression_treasure_charts: TreasureCharts
    progression_expensive_purchases: ExpensivePurchases
    progression_island_puzzles: IslandPuzzles
    progression_misc: Misc
    randomize_mapcompass: RandomizeMapCompass
    randomize_smallkeys: RandomizeSmallKeys
    randomize_bigkeys: RandomizeBigKeys
    sword_mode: SwordMode
    required_bosses: RequiredBosses
    num_required_bosses: NumRequiredBosses
    included_dungeons: IncludedDungeons
    excluded_dungeons: ExcludedDungeons
    chest_type_matches_contents: ChestTypeMatchesContents
    # trap_chests: TrapChests
    hero_mode: HeroMode
    logic_obscurity: LogicObscurity
    logic_precision: LogicPrecision
    enable_tuner_logic: EnableTunerLogic
    randomize_dungeon_entrances: RandomizeDungeonEntrances
    randomize_secret_cave_entrances: RandomizeSecretCavesEntrances
    randomize_miniboss_entrances: RandomizeMinibossEntrances
    randomize_boss_entrances: RandomizeBossEntrances
    randomize_secret_cave_inner_entrances: RandomizeSecretCaveInnerEntrances
    randomize_fairy_fountain_entrances: RandomizeFairyFountainEntrances
    mix_entrances: MixEntrances
    randomize_enemies: RandomizeEnemies
    # randomize_music: RandomizeMusic
    randomize_starting_island: RandomizeStartingIsland
    randomize_charts: RandomizeCharts
    # hoho_hints: HoHoHints
    # fishmen_hints: FishmenHints
    # korl_hints: KoRLHints
    # num_item_hints: NumItemHints
    # num_location_hints: NumLocationHints
    # num_barren_hints: NumBarrenHints
    # num_path_hints: NumPathHints
    # prioritize_remote_hints: PrioritizeRemoteHints
    swift_sail: SwiftSail
    instant_text_boxes: InstantTextBoxes
    reveal_full_sea_chart: RevealFullSeaChart
    add_shortcut_warps_between_dungeons: AddShortcutWarpsBetweenDungeons
    skip_rematch_bosses: SkipRematchBosses
    remove_music: RemoveMusic
    death_link: DeathLink


tww_option_groups: list[OptionGroup] = [
    OptionGroup(
        "Progression Locations",
        [
            Dungeons,
            DungeonSecrets,
            TingleChests,
            PuzzleSecretCaves,
            CombatSecretCaves,
            SavageLabyrinth,
            IslandPuzzles,
            GreatFairies,
            Submarines,
            PlatformsRafts,
            ShortSidequests,
            LongSidequests,
            SpoilsTrading,
            EyeReefChests,
            BigOctosGunboats,
            Misc,
            Minigames,
            Battlesquid,
            FreeGifts,
            Mail,
            ExpensivePurchases,
            TriforceCharts,
            TreasureCharts,
        ],
    ),
    OptionGroup(
        "Item Randomizer Modes",
        [
            SwordMode,
            RandomizeMapCompass,
            RandomizeSmallKeys,
            RandomizeBigKeys,
            ChestTypeMatchesContents,
            # TrapChests,
        ],
    ),
    OptionGroup(
        "Entrance Randomizer Options",
        [
            RandomizeDungeonEntrances,
            RandomizeBossEntrances,
            RandomizeMinibossEntrances,
            RandomizeSecretCavesEntrances,
            RandomizeSecretCaveInnerEntrances,
            RandomizeFairyFountainEntrances,
            MixEntrances,
        ],
    ),
    OptionGroup(
        "Other Randomizers",
        [
            RandomizeStartingIsland,
            RandomizeCharts,
            # RandomizeMusic,
        ],
    ),
    OptionGroup(
        "Convenience Tweaks",
        [
            SwiftSail,
            InstantTextBoxes,
            RevealFullSeaChart,
            SkipRematchBosses,
            AddShortcutWarpsBetweenDungeons,
            RemoveMusic,
        ],
    ),
    OptionGroup(
        "Required Bosses",
        [
            RequiredBosses,
            NumRequiredBosses,
            IncludedDungeons,
            ExcludedDungeons,
        ],
        start_collapsed=True,
    ),
    OptionGroup(
        "Difficulty Options",
        [
            HeroMode,
            LogicObscurity,
            LogicPrecision,
            EnableTunerLogic,
        ],
        start_collapsed=True,
    ),
    OptionGroup(
        "Work-in-Progress Options",
        [
            RandomizeEnemies,
        ],
        start_collapsed=True,
    ),
]
