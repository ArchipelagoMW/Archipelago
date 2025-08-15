from dataclasses import dataclass
from datetime import datetime

from Options import Choice, DeathLink, DefaultOnToggle, PerGameCommonOptions, Range, Toggle, StartInventoryPool, \
    ItemDict, ItemsAccessibility, ItemSet, Visibility
from worlds.tloz_st.data.Items import ITEMS_DATA

# YAML options

class SpiritTracksGoal(Choice):
    """
    The goal to accomplish in order to complete the seed.
    - ToS Section 1: Finish the 1st section of Tower of Spirits and retrieve the Forest Glyph
    """
    display_name = "Goal"
    option_beat_ToS_section_1 = 0
    default = 0


class SpiritTracksRemoveItemsFromPool(ItemDict):
    """
    Removes specified amount of given items from the item pool, replacing them with random filler items.
    This option has significant chances to break generation if used carelessly, so test your preset several times
    before using it on long generations. Use at your own risk!
    """
    display_name = "remove_items_from_pool"
    verify_item_name = False


class SpiritTracksLogic(Choice):
    """
    Logic options:
    - Normal: Glitches not in logic.
    - Medium: Includes some cool uses of pots aren't hard, bun unconventional
    - Glitched: Hammer clips, chu camera displacement and clever use of items in logic
    Be careful, using glitches on normal logic can cause key-related softlocks
    """
    display_name = "logic"
    option_normal = 0
    option_hard = 1
    option_glitched = 2
    default = 0


# class SpiritTracksPhantomCombatDifficulty(Choice):
#     """
#     Option for what you need to kill phantoms in logic
#     - require_phantom_sword: need phantom sword
#     - require_traps: need a pit trap or boulder
#     - require_stun: require a method of stunning, and an open pit to push into. Includes bow, hammer,
#     and sword + 2 progressive spirits of power
#     - require_weapon: all of the above plus grappling hook
#     """
#     display_name = "phantom_combat_difficulty"
#     option_require_phantom_sword = 0
#     option_require_traps = 1
#     option_require_stun = 2
#     option_require_weapon = 3
#     default = 0


class SpiritTracksKeyRandomization(Choice):
    """
    Small Key Logic options:
    - vanilla: Keys are not randomized
    - in_own_dungeon: Keys can be found in their own dungeon
    - anywhere: Keysanity. Keys can be found anywhere
    """
    display_name = "Key Settings"
    option_vanilla = 0
    option_in_own_dungeon = 1
    option_anywhere = 2
    default = 1


# class SpiritTracksDungeonsRequired(Range):
#     """
#     How many dungeons are required to access the endgame.
#     Max is 6 unless you add Ghost ship and TotOK with their own options below
#     """
#     display_name = "dungeons_required"
#     range_start = 0
#     range_end = 8
#     default = 3


# class SpiritTracksFrogRandomization(Choice):
#     """
#     Ramdomize golden cyclone frogs
#     - vanilla: shooting a frog gives their warp spot
#     - start_with: start with all warps unlocked. Frogs are not checks. You don't start with cyclone slate unless it's
#     in starting_items. You also need their respective sea charts to actually warp.
#     - randomize: frog glyphs are random and frogs are checks
#     """
#     display_name = "randomize_frogs"
#     option_vanilla = 0
#     option_start_with = 1
#     option_randomize = 2
#     default = 0


class SpiritTracksTrainRequiresForestGlyph(Toggle):
    """
    If True, heading out to sea from aboda requires the Forest Realm Glyph.
    WARNING! If set to False and you travel without a glyph, you can softlock by crossing to another glyph.
    Warp Gates require their glyph to work
    """
    display_name = "Train requires Forest Glyph"
    default = 1

# class SpiritTracksDungeonHints(Choice):
#     """
#     Receive hints for your required dungeons
#     - false: no hints
#     - oshus: oshus gives dungeon hints
#     - totok: entering totok gives dungeon hints
#     """
#     display_name = "dungeon_hints"
#     option_false = 0
#     option_oshus = 1
#     option_totok = 2
#     default = 1

class SpiritTracksExcludeNonRequiredDungeons(Toggle):
    """
    Non-required dungeons won't have progression or useful items. Does not apply to TotOK.
    """
    display_name = "exclude_non_required_dungeons"
    default = 1


class SpiritTracksShopHints(Toggle):
    """
    Get hints for shop items you currently can buy
    Includes island shops, Beedle, masked Beedle and Eddo
    """
    display_name = "hint_shops"
    default = 1

@dataclass
class SpiritTracksOptions(PerGameCommonOptions):
    # Accessibility
    accessibility: ItemsAccessibility

    # Goal
    goal: SpiritTracksGoal
    #dungeons_required: SpiritTracksDungeonsRequired
    exclude_non_required_dungeons: SpiritTracksExcludeNonRequiredDungeons

    # Logic options
    logic: SpiritTracksLogic
    #phantom_combat_difficulty: SpiritTracksPhantomCombatDifficulty
    train_requires_forest_glyph: SpiritTracksTrainRequiresForestGlyph

    # Item Randomization
    keysanity: SpiritTracksKeyRandomization
    #randomize_frogs: SpiritTracksFrogRandomization

    # Hint Options
    #dungeon_hints: SpiritTracksDungeonHints
    shop_hints: SpiritTracksShopHints

    # World Options

    # Generic
    start_inventory_from_pool: StartInventoryPool
    remove_items_from_pool: SpiritTracksRemoveItemsFromPool
    death_link: DeathLink
