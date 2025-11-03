import functools
from dataclasses import fields, Field, dataclass
from typing import *
from datetime import timedelta

from Options import (
    Choice, Toggle, DefaultOnToggle, OptionSet, Range,
    PerGameCommonOptions, Option, VerifyKeys, StartInventory,
    is_iterable_except_str, OptionGroup, Visibility, ItemDict,
    Accessibility, ProgressionBalancing
)
from Utils import get_fuzzy_results
from BaseClasses import PlandoOptions
from .item import item_names, item_tables
from .item.item_groups import kerrigan_active_abilities, kerrigan_passives, nova_weapons, nova_gadgets
from .mission_tables import (
    SC2Campaign, SC2Mission, lookup_name_to_mission, MissionPools, get_missions_with_any_flags_in_list,
    campaign_mission_table, SC2Race, MissionFlag
)
from .mission_groups import mission_groups, MissionGroupNames
from .mission_order.options import CustomMissionOrder

if TYPE_CHECKING:
    from worlds.AutoWorld import World
    from . import SC2World


class Sc2MissionSet(OptionSet):
    """Option set made for handling missions and expanding mission groups"""
    valid_keys: Iterable[str] = [x.mission_name for x in SC2Mission]

    @classmethod
    def from_any(cls, data: Any):
        if is_iterable_except_str(data):
            return cls(data)
        return cls.from_text(str(data))

    def verify(self, world: Type['World'], player_name: str, plando_options: PlandoOptions) -> None:
        """Overridden version of function from Options.VerifyKeys for a better error message"""
        new_value: set[str] = set()
        case_insensitive_group_mapping = {
            group_name.casefold(): group_value for group_name, group_value in mission_groups.items()
        }
        case_insensitive_group_mapping.update({mission.mission_name.casefold(): [mission.mission_name] for mission in SC2Mission})
        for group_name in self.value:
            item_names = case_insensitive_group_mapping.get(group_name.casefold(), {group_name})
            new_value.update(item_names)
        self.value = new_value
        for item_name in self.value:
            if item_name not in self.valid_keys:
                picks = get_fuzzy_results(
                    item_name,
                    list(self.valid_keys) + list(MissionGroupNames.get_all_group_names()),
                    limit=1,
                )
                raise Exception(f"Mission {item_name} from option {self} "
                                f"is not a valid mission name from {world.game}. "
                                f"Did you mean '{picks[0][0]}' ({picks[0][1]}% sure)")

    def __iter__(self) -> Iterator[str]:
        return self.value.__iter__()

    def __len__(self) -> int:
        return self.value.__len__()


class SelectedRaces(OptionSet):
    """
    Pick which factions' missions and items can be shuffled into the world.
    """
    display_name = "Select Playable Races"
    valid_keys = {race.get_title() for race in SC2Race if race != SC2Race.ANY}
    default = valid_keys


class GameDifficulty(Choice):
    """
    The difficulty of the campaign, affects enemy AI, starting units, and game speed.

    For those unfamiliar with the Archipelago randomizer, the recommended settings are one difficulty level
    lower than the vanilla game
    """
    display_name = "Game Difficulty"
    option_casual = 0
    option_normal = 1
    option_hard = 2
    option_brutal = 3
    default = 1


class DifficultyDamageModifier(DefaultOnToggle):
    """
    Enables or disables vanilla difficulty-based damage received modifier
    Handles the 1.25 Brutal damage modifier in HotS and Prologue and 0.5 Casual damage modifier outside WoL and Prophecy
    """
    display_name = "Difficulty Damage Modifier"


class GameSpeed(Choice):
    """Optional setting to override difficulty-based game speed."""
    display_name = "Game Speed"
    option_default = 0
    option_slower = 1
    option_slow = 2
    option_normal = 3
    option_fast = 4
    option_faster = 5
    default = option_default


class DisableForcedCamera(DefaultOnToggle):
    """
    Prevents the game from moving or locking the camera without the player's consent.
    """
    display_name = "Disable Forced Camera Movement"


class SkipCutscenes(Toggle):
    """
    Skips all cutscenes and prevents dialog from blocking progress.
    """
    display_name = "Skip Cutscenes"


class AllInMap(Choice):
    """Determines what version of All-In (WoL final map) that will be generated for the campaign."""
    display_name = "All In Map"
    option_ground = 0
    option_air = 1
    default = 'random'


class MissionOrder(Choice):
    """
    Determines the order the missions are played in.  The first three mission orders ignore the Maximum Campaign Size option.
    Vanilla (83 total if all campaigns enabled): Keeps the standard mission order and branching from the vanilla Campaigns.
    Vanilla Shuffled (83 total if all campaigns enabled): Keeps same branching paths from the vanilla Campaigns but randomizes the order of missions within.
    Mini Campaign (47 total if all campaigns enabled): Shorter version of the campaign with randomized missions and optional branches.
    Blitz:  Missions are divided into sets. Complete one mission from a set to advance to the next set.
    Gauntlet: A linear path of missions to complete the campaign.
    Grid: Missions are arranged into a grid. Completing a mission unlocks the adjacent missions. Corners may be omitted to make the grid more square. Complete the bottom-right mission to win.
    Golden Path: A required line of missions with several optional branches, similar to the Wings of Liberty campaign.
    Hopscotch: Missions alternate between mandatory missions and pairs of optional missions.
    Custom: Uses the YAML's custom mission order option. See documentation for usage.
    """
    display_name = "Mission Order"
    option_vanilla = 0
    option_vanilla_shuffled = 1
    option_mini_campaign = 2
    option_blitz = 5
    option_gauntlet = 6
    option_grid = 9
    option_golden_path = 10
    option_hopscotch = 11
    option_custom = 99
    default = option_golden_path


class MaximumCampaignSize(Range):
    """
    Sets an upper bound on how many missions to include when a variable-size mission order is selected.
    If a set-size mission order is selected, does nothing.
    """
    display_name = "Maximum Campaign Size"
    range_start = 1
    range_end = len(SC2Mission)
    default = 83


class TwoStartPositions(Toggle):
    """
    If turned on and 'grid', 'hopscotch', or 'golden_path' mission orders are selected,
    removes the first mission and allows both of the next two missions to be played from the start.
    """
    display_name = "Two start missions"
    default = Toggle.option_false


class KeyMode(Choice):
    """
    Optionally creates Key items that must be found in the multiworld to unlock parts of the mission order,
    in addition to any regular requirements a mission may have.

    "Questline" options will only work for Vanilla, Vanilla Shuffled, Mini Campaign, and Golden Path mission orders.

    Disabled: Don't create any keys.
    Questlines: Create keys for questlines besides the starter ones, eg. "Colonist (Wings of Liberty) Questline Key".
    Missions: Create keys for missions besides the starter ones, eg. "Zero Hour Mission Key".
    Progressive Questlines: Create one type of progressive key for questlines within each campaign, eg. "Progressive Key #1".
    Progressive Missions: Create one type of progressive key for all missions, "Progressive Mission Key".
    Progressive Per Questline: All questlines besides the starter ones get a unique progressive key for their missions, eg. "Progressive Key #1".
    """
    display_name = "Key Mode"
    option_disabled = 0
    option_questlines = 1
    option_missions = 2
    option_progressive_questlines = 3
    option_progressive_missions = 4
    option_progressive_per_questline = 5
    default = option_disabled


class ColorChoice(Choice):
    option_white = 0
    option_red = 1
    option_blue = 2
    option_teal = 3
    option_purple = 4
    option_yellow = 5
    option_orange = 6
    option_green = 7
    option_light_pink = 8
    option_violet = 9
    option_light_grey = 10
    option_dark_green = 11
    option_brown = 12
    option_light_green = 13
    option_dark_grey = 14
    option_pink = 15
    option_rainbow = 16
    option_mengsk = 17
    option_bright_lime = 18
    option_arcane = 19
    option_ember = 20
    option_hot_pink = 21
    option_default = 22
    default = option_default


class PlayerColorTerranRaynor(ColorChoice):
    """Determines in-game player team color in Wings of Liberty missions."""
    display_name = "Terran Player Color (Raynor)"


class PlayerColorProtoss(ColorChoice):
    """Determines in-game player team color in Legacy of the Void missions."""
    display_name = "Protoss Player Color"


class PlayerColorZerg(ColorChoice):
    """Determines in-game player team color in Heart of the Swarm missions before unlocking Primal Kerrigan."""
    display_name = "Zerg Player Color"


class PlayerColorZergPrimal(ColorChoice):
    """Determines in-game player team color in Heart of the Swarm after unlocking Primal Kerrigan."""
    display_name = "Zerg Player Color (Primal)"


class PlayerColorNova(ColorChoice):
    """Determines in-game player team color in Nova Covert Ops missions."""
    display_name = "Terran Player Color (Nova)"


class EnabledCampaigns(OptionSet):
    """
    Determines which campaign's missions will be used.
    Wings of Liberty, Prophecy, and Prologue are the only free-to-play campaigns.
    Valid campaign names:
    - 'Wings of Liberty'
    - 'Prophecy'
    - 'Heart of the Swarm'
    - 'Whispers of Oblivion (Legacy of the Void: Prologue)'
    - 'Legacy of the Void'
    - 'Into the Void (Legacy of the Void: Epilogue)'
    - 'Nova Covert Ops'
    """
    display_name = "Enabled Campaigns"
    valid_keys = {campaign.campaign_name for campaign in SC2Campaign if campaign != SC2Campaign.GLOBAL}
    default = set((SC2Campaign.WOL.campaign_name,))


class EnableRaceSwapVariants(Choice):
    """
    Allow mission variants where you play a faction other than the one the map was initially
    designed for. NOTE: Cutscenes are always skipped on race-swapped mission variants.

    Disabled: Don't shuffle any non-vanilla map variants into the pool.
    Pick One: Shuffle up to 1 valid version of each map into the pool, depending on other settings.
    Pick One Non-Vanilla: Shuffle up to 1 valid version other than the original one of each map into the pool, depending on other settings.
    Shuffle All: Each version of a map can appear in the same pool (so a map can appear up to 3 times as different races)
    Shuffle All Non-Vanilla: Each version of a map besides the original can appear in the same pool (so a map can appear up to 2 times as different races)
    """
    display_name = "Enable Race-Swapped Mission Variants"
    option_disabled = 0
    option_pick_one = 1
    option_pick_one_non_vanilla = 2
    option_shuffle_all = 3
    option_shuffle_all_non_vanilla = 4
    default = option_disabled


class EnableMissionRaceBalancing(Choice):
    """
    If enabled, picks missions in such a way that the appearance rate of races is roughly equal.
    The final rates may deviate if there are not enough missions enabled to accommodate each race.

    Disabled: Pick missions at random.
    Semi Balanced: Use a weighting system to pick missions in a random, but roughly equal ratio.
    Fully Balanced: Pick missions to preserve equal race counts whenever possible.
    """
    display_name = "Enable Mission Race Balancing"
    option_disabled = 0
    option_semi_balanced = 1
    option_fully_balanced = 2
    default = option_semi_balanced


class ShuffleCampaigns(DefaultOnToggle):
    """
    Shuffles the missions between campaigns if enabled.
    Only available for Vanilla Shuffled and Mini Campaign mission order
    """
    display_name = "Shuffle Campaigns"


class ShuffleNoBuild(DefaultOnToggle):
    """
    Determines if the no-build missions are included in the shuffle.
    If turned off, the no-build missions will not appear. Has no effect for Vanilla mission order.
    """
    display_name = "Shuffle No-Build Missions"


class StarterUnit(Choice):
    """
    Unlocks a random unit at the start of the game.

    Off: No units are provided, the first unit must be obtained from the randomizer
    Balanced: A unit that doesn't give the player too much power early on is given
    Any Starter Unit: Any starter unit can be given
    """
    display_name = "Starter Unit"
    option_off = 0
    option_balanced = 1
    option_any_starter_unit = 2


class RequiredTactics(Choice):
    """
    Determines the maximum tactical difficulty of the world (separate from mission difficulty).
    Higher settings increase randomness.

    Standard:  All missions can be completed with good micro and macro.
    Advanced:  Completing missions may require relying on starting units and micro-heavy units.
    Any Units: Logic guarantees faction-appropriate units appear early without regard to what those units are.
               i.e. if the third mission is a protoss build mission,
               logic guarantees at least 2 protoss units are reachable before starting it.
               May render the run impossible on harder difficulties.
    No Logic:  Units and upgrades may be placed anywhere. LIKELY TO RENDER THE RUN IMPOSSIBLE ON HARDER DIFFICULTIES!
               Locks Grant Story Tech option to true.
    """
    display_name = "Required Tactics"
    option_standard = 0
    option_advanced = 1
    option_any_units = 2
    option_no_logic = 3


class EnableVoidTrade(Toggle):
    """
    Enables the Void Trade Wormhole to be built from the Advanced Construction tab of SCVs, Drones and Probes.  
    This structure allows sending units to the Archipelago server, as well as buying random units from the server.  
    
    Note: Always disabled if there is no other Starcraft II world with Void Trade enabled in the multiworld.  You cannot receive units that you send.
    """
    display_name = "Enable Void Trade"


class VoidTradeAgeLimit(Choice):
    """
    Determines the maximum allowed age for units you can receive from Void Trade.
    Units that are older than your choice will still be available to other players, but not to you.

    This does not put a time limit on units you send to other players. Your own units are only affected by other players' choices for this option.
    """
    display_name = "Void Trade Age Limit"
    option_disabled = 0
    option_1_week = 1
    option_1_day = 2
    option_4_hours = 3
    option_2_hours = 4
    option_1_hour = 5
    option_30_minutes = 6
    option_5_minutes = 7
    default = option_30_minutes


class VoidTradeWorkers(Toggle):
    """
    If enabled, you are able to send and receive workers via Void Trade.

    Sending workers is a cheap way to get a lot of units from other players,
    at the cost of reducing the strength of received units for other players.

    Receiving workers allows you to build units of other races, but potentially skips large parts of your multiworld progression.
    """
    display_name = "Allow Workers in Void Trade"


class MaxUpgradeLevel(Range):
    """Controls the maximum number of weapon/armor upgrades that can be found or unlocked."""
    display_name = "Maximum Upgrade Level"
    range_start = 3
    range_end = 5
    default = 3


class GenericUpgradeMissions(Range):
    """
    Determines the percentage of missions in the mission order that must be completed before
    level 1 of all weapon and armor upgrades is unlocked.  Level 2 upgrades require double the amount of missions,
    and level 3 requires triple the amount.  The required amounts are always rounded down.
    If set to 0, upgrades are instead added to the item pool and must be found to be used.

    If the mission order is unable to be beaten by this value (if above 0), the generator will place additional
    weapon / armor upgrades into start inventory
    """
    display_name = "Generic Upgrade Missions"
    range_start = 0
    range_end = 100 # Higher values lead to fails often
    default = 0


class GenericUpgradeResearch(Choice):
    """Determines how weapon and armor upgrades affect missions once unlocked.

    Vanilla:  Upgrades must be researched as normal.
    Auto In No-Build:  In No-Build missions, upgrades are automatically researched.
    In all other missions, upgrades must be researched as normal.
    Auto In Build:  In No-Build missions, upgrades are unavailable as normal.
    In all other missions, upgrades are automatically researched.
    Always Auto:  Upgrades are automatically researched in all missions."""
    display_name = "Generic Upgrade Research"
    option_vanilla = 0
    option_auto_in_no_build = 1
    option_auto_in_build = 2
    option_always_auto = 3


class GenericUpgradeResearchSpeedup(Toggle):
    """
    If turned on, the weapon and armor upgrades are researched more quickly if level 4 or higher is unlocked.
    The research times of upgrades are cut proportionally, so you're able to hit the maximum available level
    at the same time, as you'd hit level 3 normally.

    Turning this on will help you to be able to research level 4 or 5 upgrade levels in timed missions.

    Has no effect if Maximum Upgrade Level is set to 3
    or Generic Upgrade Research doesn't require you to research upgrades in build missions.
    """
    display_name = "Generic Upgrade Research Speedup"


class GenericUpgradeItems(Choice):
    """Determines how weapon and armor upgrades are split into items.

    All options produce a number of levels of each item equal to the Maximum Upgrade Level.
    The examples below consider a Maximum Upgrade Level of 3.

    Does nothing if upgrades are unlocked by completed mission counts.

    Individual Items:  All weapon and armor upgrades are each an item,
    resulting in 18 total upgrade items for Terran and 15 total items for Zerg and Protoss each.
    Bundle Weapon And Armor:  All types of weapon upgrades are one item per race,
    and all types of armor upgrades are one item per race,
    resulting in 18 total items.
    Bundle Unit Class:  Weapon and armor upgrades are merged,
    but upgrades are bundled separately for each race:
    Infantry, Vehicle, and Starship upgrades for Terran (9 items),
    Ground and Flyer upgrades for Zerg (6 items),
    Ground and Air upgrades for Protoss (6 items),
    resulting in 21 total items.
    Bundle All:  All weapon and armor upgrades are one item per race,
    resulting in 9 total items."""
    display_name = "Generic Upgrade Items"
    option_individual_items = 0
    option_bundle_weapon_and_armor = 1
    option_bundle_unit_class = 2
    option_bundle_all = 3


class VanillaItemsOnly(Toggle):
    """If turned on, the item pool is limited only to items that appear in the main 3 vanilla campaigns.
    Weapon/Armor upgrades are unaffected; use max_upgrade_level to control maximum level.
    Locked Items may override these exclusions."""
    display_name = "Vanilla Items Only"


class ExcludeOverpoweredItems(Toggle):
    """
    If turned on, a curated list of very strong items are excluded.
    These items were selected for promoting repetitive strategies, or for providing a lot of power in a boring way.
    Recommended off for players looking for a challenge or for repeat playthroughs.
    Excluding an OP item overrides the exclusion from this item rather than add to it.
    OP items may be unexcluded or locked with Unexcluded Items or Locked Items options.
    Enabling this can force a unit nerf even if Allow Unit Nerfs is set to false for some units.
    """
    display_name = "Exclude Overpowered Items"


# Current maximum number of upgrades for a unit
MAX_UPGRADES_OPTION = 13


class EnsureGenericItems(Range):
    """
    Specifies a minimum percentage of the generic item pool that will be present for the slot.
    The generic item pool is the pool of all generically useful items after all exclusions.
    Generically-useful items include: Worker upgrades, Building upgrades, economy upgrades,
    Mercenaries, Kerrigan levels and abilities, and Spear of Adun abilities
    Increasing this percentage will make units less common.
    """
    display_name = "Ensure Generic Items"
    range_start = 0
    range_end = 100
    default = 25


class MinNumberOfUpgrades(Range):
    """
    Set a minimum to the number of upgrade items a unit/structure can have.
    Note that most units have 4 to 6 upgrades.
    If a unit has fewer upgrades than the minimum, it will have all of its upgrades.

    Doesn't affect shared unit upgrades.
    """
    display_name = "Minimum number of upgrades per unit/structure"
    range_start = 0
    range_end = MAX_UPGRADES_OPTION
    default = 2


class MaxNumberOfUpgrades(Range):
    """
    Set a maximum to the number of upgrade items a unit/structure can have.
    -1 is used to define unlimited.
    Note that most units have 4 to 6 upgrades.

    Doesn't affect shared unit upgrades.
    """
    display_name = "Maximum number of upgrades per unit/structure"
    range_start = -1
    range_end = MAX_UPGRADES_OPTION
    default = -1


class MercenaryHighlanders(DefaultOnToggle):
    """
    If enabled, it limits the controllable amount of certain mercenaries to 1, even if you have unlimited mercenaries upgrade.
    With this upgrade you can still call the mercenary again if it dies.

    Affected mercenaries: Jackson's Revenge (Battlecruiser), Wise Old Torrasque (Ultralisk)
    """
    display_name = "Mercenary Highlanders"


class KerriganPresence(Choice):
    """
    Determines whether Kerrigan is playable outside of missions that require her.

    Vanilla: Kerrigan is playable as normal, appears in the same missions as in vanilla game.
    Not Present:  Kerrigan is not playable, unless the mission requires her to be present.  Other hero units stay playable,
        and locations normally requiring Kerrigan can be checked by any unit.
        Kerrigan level items, active abilities and passive abilities affecting her will not appear.
        In missions where the Kerrigan unit is required, story abilities are given in same way as Grant Story Tech is set to true

    Note: Always set to "Not Present" if Heart of the Swarm campaign is disabled.
    """
    display_name = "Kerrigan Presence"
    option_vanilla = 0
    option_not_present = 1


class KerriganLevelsPerMissionCompleted(Range):
    """
    Determines how many levels Kerrigan gains when a mission is beaten.
    """
    display_name = "Levels Per Mission Beaten"
    range_start = 0
    range_end = 20
    default = 0


class KerriganLevelsPerMissionCompletedCap(Range):
    """
    Limits how many total levels Kerrigan can gain from beating missions.  This does not affect levels gained from items.  
    Set to -1 to disable this limit.

    NOTE: The following missions have these level requirements:
    Supreme: 35
    The Infinite Cycle: 70
    See Grant Story Levels for more details.
    """
    display_name = "Levels Per Mission Beaten Cap"
    range_start = -1
    range_end = 140
    default = -1


class KerriganLevelItemSum(Range):
    """
    Determines the sum of the level items in the world.  This does not affect levels gained from beating missions.

    NOTE: The following missions have these level requirements:
    Supreme: 35
    The Infinite Cycle: 70
    See Grant Story Levels for more details.
    """
    display_name = "Kerrigan Level Item Sum"
    range_start = 0
    range_end = 140
    default = 70


class KerriganLevelItemDistribution(Choice):
    """Determines the amount and size of Kerrigan level items.

    Vanilla:  Uses the distribution in the vanilla campaign.
    This entails 32 individual levels and 6 packs of varying sizes.
    This distribution always adds up to 70, ignoring the Level Item Sum setting.
    Smooth:  Uses a custom, condensed distribution of 10 items between sizes 4 and 10,
    intended to fit more levels into settings with little room for filler while keeping some variance in level gains.
    This distribution always adds up to 70, ignoring the Level Item Sum setting.
    Size 70:  Uses items worth 70 levels each.
    Size 35:  Uses items worth 35 levels each.
    Size 14:  Uses items worth 14 levels each.
    Size 10:  Uses items worth 10 levels each.
    Size 7:  Uses items worth 7 levels each.
    Size 5:  Uses items worth 5 levels each.
    Size 2:  Uses items worth 2 level eachs.
    Size 1:  Uses individual levels.  As there are not enough locations in the game for this distribution,
    this will result in a greatly reduced total level, and is likely to remove many other items."""
    display_name = "Kerrigan Level Item Distribution"
    option_vanilla = 0
    option_smooth = 1
    option_size_70 = 2
    option_size_35 = 3
    option_size_14 = 4
    option_size_10 = 5
    option_size_7 = 6
    option_size_5 = 7
    option_size_2 = 8
    option_size_1 = 9
    default = option_smooth


class KerriganTotalLevelCap(Range):
    """
    Limits how many total levels Kerrigan can gain from any source.
    Depending on your other settings, there may be more levels available in the world,
    but they will not affect Kerrigan.
    Set to -1 to disable this limit.

    NOTE: The following missions have these level requirements:
    Supreme: 35
    The Infinite Cycle: 70
    See Grant Story Levels for more details.
    """
    display_name = "Total Level Cap"
    range_start = -1
    range_end = 140
    default = -1


class StartPrimaryAbilities(Range):
    """Number of Primary Abilities (Kerrigan Tier 1, 2, and 4) to start the game with.
    If set to 4, a Tier 7 ability is also included."""
    display_name = "Starting Primary Abilities"
    range_start = 0
    range_end = 4
    default = 0


class KerriganPrimalStatus(Choice):
    """Determines when Kerrigan appears in her Primal Zerg form.
    This greatly increases her energy regeneration.

    Vanilla:  Kerrigan is human in missions that canonically appear before The Crucible,
    and zerg thereafter.
    Always Zerg:  Kerrigan is always zerg.
    Always Human:  Kerrigan is always human.
    Level 35:  Kerrigan is human until reaching level 35, and zerg thereafter.
    Half Completion:  Kerrigan is human until half of the missions in the world are completed,
    and zerg thereafter.
    Item:  Kerrigan's Primal Form is an item. She is human until it is found, and zerg thereafter."""
    display_name = "Kerrigan Primal Status"
    option_vanilla = 0
    option_always_zerg = 1
    option_always_human = 2
    option_level_35 = 3
    option_half_completion = 4
    option_item = 5


class KerriganMaxActiveAbilities(Range):
    """
    Determines the maximum number of Kerrigan active abilities that can be present in the game
    Additional abilities may spawn if those are required to beat the game.
    """
    display_name = "Kerrigan Maximum Active Abilities"
    range_start = 0
    range_end = len(kerrigan_active_abilities)
    default = range_end


class KerriganMaxPassiveAbilities(Range):
    """
    Determines the maximum number of Kerrigan passive abilities that can be present in the game
    Additional abilities may spawn if those are required to beat the game.
    """
    display_name = "Kerrigan Maximum Passive Abilities"
    range_start = 0
    range_end = len(kerrigan_passives)
    default = range_end


class EnableMorphling(Toggle):
    """
    Determines whether the player can build Morphlings, which allow for inefficient morphing of advanced units
    like Ravagers and Lurkers without requiring the base unit to be unlocked first.
    """
    display_name = "Enable Morphling"


class WarCouncilNerfs(Toggle):
    """
    Controls whether most Protoss units can initially be found in a nerfed state, with upgrades restoring their stronger power level.
    For example, nerfed Zealots will lack the whirlwind upgrade until it is found as an item.
    """
    display_name = "Allow Unit Nerfs"


class SpearOfAdunPresence(Choice):
    """
    Determines in which missions Spear of Adun calldowns will be available.
    Affects only abilities used from Spear of Adun top menu.

    Not Present: Spear of Adun calldowns are unavailable.
    Vanilla: Spear of Adun calldowns are only available where they appear in the basegame (Protoss missions after The Growing Shadow)
    Protoss: Spear of Adun calldowns are available in any Protoss mission
    Everywhere: Spear of Adun calldowns are available in any mission of any race
    Any Race LotV: Spear of Adun calldowns are available in any race-swapped variant of a LotV mission
    """
    display_name = "Spear of Adun Presence"
    option_not_present = 0
    option_vanilla = 4
    option_protoss = 2
    option_everywhere = 3
    option_any_race_lotv = 1
    default = option_vanilla

    # Fix case
    @classmethod
    def get_option_name(cls, value: int) -> str:
        if value == SpearOfAdunPresence.option_any_race_lotv:
            return "Any Race LotV"
        else:
            return super().get_option_name(value)


class SpearOfAdunPresentInNoBuild(Toggle):
    """
    Determines if Spear of Adun calldowns are available in no-build missions.

    If turned on, Spear of Adun calldown powers are available in missions specified under "Spear of Adun Presence".
    If turned off, Spear of Adun calldown powers are unavailable in all no-build missions
    """
    display_name = "Spear of Adun Present in No-Build"


class SpearOfAdunPassiveAbilityPresence(Choice):
    """
    Determines availability of Spear of Adun passive powers.
    Affects abilities like Reconstruction Beam or Overwatch.
    Does not affect building abilities like Orbital Assimilators or Warp Harmonization.

    Not Present: Autocasts are not available.
    Vanilla: Spear of Adun calldowns are only available where it appears in the basegame (Protoss missions after The Growing Shadow)
    Protoss: Spear of Adun autocasts are available in any Protoss mission
    Everywhere: Spear of Adun autocasts are available in any mission of any race
    Any Race LotV: Spear of Adun autocasts are available in any race-swapped variant of a LotV mission
    """
    display_name = "Spear of Adun Passive Ability Presence"
    option_not_present = 0
    option_any_race_lotv = 1
    option_protoss = 2
    option_everywhere = 3
    option_vanilla = 4
    default = option_vanilla

    # Fix case
    @classmethod
    def get_option_name(cls, value: int) -> str:
        if value == SpearOfAdunPresence.option_any_race_lotv:
            return "Any Race LotV"
        else:
            return super().get_option_name(value)


class SpearOfAdunPassivesPresentInNoBuild(Toggle):
    """
    Determines if Spear of Adun autocasts are available in no-build missions.

    If turned on, Spear of Adun autocasts are available in missions specified under "Spear of Adun Passive Ability Presence".
    If turned off, Spear of Adun autocasts are unavailable in all no-build missions
    """
    display_name = "Spear of Adun Passive Abilities Present in No-Build"


class SpearOfAdunMaxActiveAbilities(Range):
    """
    Determines the maximum number of Spear of Adun active abilities (top bar) that can be present in the game
    Additional abilities may spawn if those are required to beat the game.

    Note: Warp in Reinforcements is treated as a second level of Warp in Pylon
    """
    display_name = "Spear of Adun Maximum Active Abilities"
    range_start = 0
    range_end = sum([item.quantity for item_name, item in item_tables.get_full_item_list().items() if item_name in item_tables.spear_of_adun_calldowns])
    default = range_end


class SpearOfAdunMaxAutocastAbilities(Range):
    """
    Determines the maximum number of Spear of Adun passive abilities that can be present in the game
    Additional abilities may spawn if those are required to beat the game.
    Does not affect building abilities like Orbital Assimilators or Warp Harmonization.
    """
    display_name = "Spear of Adun Maximum Passive Abilities"
    range_start = 0
    range_end = sum(item.quantity for item_name, item in item_tables.get_full_item_list().items() if item_name in item_tables.spear_of_adun_castable_passives)
    default = range_end


class GrantStoryTech(Choice):
    """
    Controls handling of no-build missions that may require very specific items, such as Kerrigan or Nova abilities.

    no_grant: don't grant anything special; the player must find items to play the missions
    grant: grant a minimal inventory that will allow the player to beat the mission, in addition to other items found
    allow_substitutes: Reworks the most constrained mission - Supreme - to allow other items to substitute for Leaping Strike and Mend

    Locked to "grant" if Required Tactics is set to no logic.
    """
    display_name = "Grant Story Tech"
    option_no_grant = 0
    option_grant = 1
    option_allow_substitutes = 2


class GrantStoryLevels(Choice):
    """
    If enabled, grants Kerrigan the required minimum levels for the following missions:
    Supreme: 35
    The Infinite Cycle: 70
    The bonus levels only apply during the listed missions, and can exceed the Total Level Cap.

    If disabled, either of these missions is included, and there are not enough levels in the world, generation may fail.
    To prevent this, either increase the amount of levels in the world, or enable this option.

    If disabled and Required Tactics is set to no logic, this option is forced to Minimum.

    Disabled: Kerrigan does not get bonus levels for these missions,
              instead the levels must be gained from items or beating missions.
    Additive: Kerrigan gains bonus levels equal to the mission's required level.
    Minimum: Kerrigan is either at her real level, or at the mission's required level,
             depending on which is higher.
    """
    display_name = "Grant Story Levels"
    option_disabled = 0
    option_additive = 1
    option_minimum = 2
    default = option_minimum


class NovaMaxWeapons(Range):
    """
    Determines maximum number of Nova weapons that can be present in the game
    Additional weapons may spawn if those are required to beat the game.

    Note: Nova can swap between unlocked weapons anytime during the gameplay.
    """
    display_name = "Nova Maximum Weapons"
    range_start = 0
    range_end = len(nova_weapons)
    default = range_end


class NovaMaxGadgets(Range):
    """
    Determines maximum number of Nova gadgets that can be present in the game.
    Gadgets are a vanilla category including 2 grenade abilities, Stim, Holo Decoy, and Ionic Force Field.
    Additional gadgets may spawn if those are required to beat the game.

    Note: Nova can use any unlocked ability anytime during gameplay.
    """
    display_name = "Nova Maximum Gadgets"
    range_start = 0
    range_end = len(nova_gadgets)
    default = range_end


class NovaGhostOfAChanceVariant(Choice):
    """
    Determines which variant of Nova should be used in Ghost of a Chance mission.

    WoL: Uses Nova from Wings of Liberty campaign (vanilla)
    NCO: Uses Nova from Nova Covert Ops campaign
    Auto: Uses NCO if a mission from Nova Covert Ops is actually shuffled, if not uses WoL
    """
    display_name = "Nova Ghost of Chance Variant"
    option_wol = 0
    option_nco = 1
    option_auto = 2
    default = option_wol

    # Fix case
    @classmethod
    def get_option_name(cls, value: int) -> str:
        if value == NovaGhostOfAChanceVariant.option_wol:
            return "WoL"
        elif value == NovaGhostOfAChanceVariant.option_nco:
            return "NCO"
        return super().get_option_name(value)


class TakeOverAIAllies(Toggle):
    """
    On maps supporting this feature allows you to take control over an AI Ally.
    """
    display_name = "Take Over AI Allies"


class Sc2ItemDict(Option[Dict[str, int]], VerifyKeys, Mapping[str, int]):
    """A branch of ItemDict that supports item counts of 0"""
    default = {}
    supports_weighting = False
    verify_item_name = True
    # convert_name_groups = True
    display_name = 'Unnamed dictionary'
    minimum_value: int = 0

    def __init__(self, value: Dict[str, int]):
        self.value = {key: val for key, val in value.items()}

    @classmethod
    def from_any(cls, data: Union[List[str], Dict[str, int]]) -> 'Sc2ItemDict':
        if isinstance(data, list):
            # This is a little default that gets us backwards compatibility with lists.
            # It doesn't play nice with trigger merging dicts and lists together, though, so best not to advertise it overmuch.
            data = {item: 0 for item in data}
        if isinstance(data, dict):
            for key, value in data.items():
                if not isinstance(value, int):
                    raise ValueError(f"Invalid type in '{cls.display_name}': element '{key}' maps to '{value}', expected an integer")
                if value < cls.minimum_value:
                    raise ValueError(f"Invalid value for '{cls.display_name}': element '{key}' maps to {value}, which is less than the minimum ({cls.minimum_value})")
            return cls(data)
        else:
            raise NotImplementedError(f"Cannot Convert from non-dictionary, got {type(data)}")

    def verify(self, world: Type['World'], player_name: str, plando_options: PlandoOptions) -> None:
        """Overridden version of function from Options.VerifyKeys for a better error message"""
        new_value: dict[str, int] = {}
        case_insensitive_group_mapping = {
            group_name.casefold(): group_value for group_name, group_value in world.item_name_groups.items()
        }
        case_insensitive_group_mapping.update({item.casefold(): {item} for item in world.item_names})
        for group_name in self.value:
            item_names = case_insensitive_group_mapping.get(group_name.casefold(), {group_name})
            for item_name in item_names:
                new_value[item_name] = new_value.get(item_name, 0) + self.value[group_name]
        self.value = new_value
        for item_name in self.value:
            if item_name not in world.item_names:
                from .item import item_groups
                picks = get_fuzzy_results(
                    item_name,
                    list(world.item_names) + list(item_groups.ItemGroupNames.get_all_group_names()),
                    limit=1,
                )
                raise Exception(f"Item {item_name} from option {self} "
                                f"is not a valid item name from {world.game}. "
                                f"Did you mean '{picks[0][0]}' ({picks[0][1]}% sure)")

    def get_option_name(self, value):
        return ", ".join(f"{key}: {v}" for key, v in value.items())

    def __getitem__(self, item: str) -> int:
        return self.value.__getitem__(item)

    def __iter__(self) -> Iterator[str]:
        return self.value.__iter__()

    def __len__(self) -> int:
        return self.value.__len__()


class Sc2StartInventory(Sc2ItemDict):
    """Start with these items."""
    display_name = StartInventory.display_name


class LockedItems(Sc2ItemDict):
    """Guarantees that these items will be unlockable, in the amount specified.
    Specify an amount of 0 to lock all copies of an item."""
    display_name = "Locked Items"


class ExcludedItems(Sc2ItemDict):
    """Guarantees that these items will not be unlockable, in the amount specified.
    Specify an amount of 0 to exclude all copies of an item."""
    display_name = "Excluded Items"


class UnexcludedItems(Sc2ItemDict):
    """Undoes an item exclusion; useful for whitelisting or fine-tuning a category.
    Specify an amount of 0 to unexclude all copies of an item."""
    display_name = "Unexcluded Items"


class ExcludedMissions(Sc2MissionSet):
    """Guarantees that these missions will not appear in the campaign
    Doesn't apply to vanilla mission order.
    It may be impossible to build a valid campaign if too many missions are excluded."""
    display_name = "Excluded Missions"
    valid_keys = {mission.mission_name for mission in SC2Mission}


class DifficultyCurve(Choice):
    """
    Determines whether campaign missions will be placed with a smooth difficulty curve.
    Standard: The campaign will start with easy missions and end with challenging missions.  Short campaigns will be more difficult.
    Uneven: The campaign will start with easy missions, but easy missions can still appear later in the campaign.  Short campaigns will be easier.
    """
    display_name = "Difficulty Curve"
    option_standard = 0
    option_uneven = 1


class ExcludeVeryHardMissions(Choice):
    """
    Excludes Very Hard missions outside of Epilogue campaign (All-In, The Reckoning, Salvation, and all Epilogue missions are considered Very Hard).
    Doesn't apply to "Vanilla" mission order.

    Default: Not excluded for mission orders "Vanilla Shuffled" or "Grid" with Maximum Campaign Size >= 20,
             excluded for any other order
    Yes: Non-Epilogue Very Hard missions are excluded and won't be generated
    No: Non-Epilogue Very Hard missions can appear normally. Not recommended for too short mission orders.

    See also: Excluded Missions, Enabled Campaigns, Maximum Campaign Size
    """
    display_name = "Exclude Very Hard Missions"
    option_default = 0
    option_true = 1
    option_false = 2

    @classmethod
    def get_option_name(cls, value):
        return ["Default", "Yes", "No"][int(value)]


class VictoryCache(Range):
    """
    Controls how many additional checks are awarded for completing a mission.
    Goal missions are unaffected by this option.
    """
    display_name = "Victory Cache"
    range_start = 0
    range_end = 10
    default = 0


class LocationInclusion(Choice):
    option_enabled = 0
    option_half_chance = 3
    option_filler = 1
    option_disabled = 2


class VanillaLocations(LocationInclusion):
    """
    Enables or disables checks for completing vanilla objectives.
    Vanilla objectives are bonus objectives from the vanilla game,
    along with some additional objectives to balance the missions.
    Enable these locations for a balanced experience.

    Enabled: Locations of this type give normal rewards.
    Half Chance: Locations of this type have a 50% chance of being excluded.
    Filler: Forces these locations to contain filler items.
    Disabled: Removes item rewards from these locations.

    Note: Individual locations subject to plando are always enabled, so the plando can be placed properly.
    See also: Excluded Locations, Item Plando (https://archipelago.gg/tutorial/Archipelago/plando/en#item-plando)
    """
    display_name = "Vanilla Locations"


class ExtraLocations(LocationInclusion):
    """
    Enables or disables checks for mission progress and minor objectives.
    This includes mandatory mission objectives,
    collecting reinforcements and resource pickups,
    destroying structures, and overcoming minor challenges.
    Enables these locations to add more checks and items to your world.

    Enabled: Locations of this type give normal rewards.
    Half Chance: Locations of this type have a 50% chance of being excluded.
    Filler: Forces these locations to contain filler items.
    Disabled: Removes item rewards from these locations.

    Note: Individual locations subject to plando are always enabled, so the plando can be placed properly.
    See also: Excluded Locations, Item Plando (https://archipelago.gg/tutorial/Archipelago/plando/en#item-plando)
    """
    display_name = "Extra Locations"


class ChallengeLocations(LocationInclusion):
    """
    Enables or disables checks for completing challenge tasks.
    Challenges are tasks that are more difficult than completing the mission, and are often based on achievements.
    You might be required to visit the same mission later after getting stronger in order to finish these tasks.
    Enable these locations to increase the difficulty of completing the multiworld.

    Enabled: Locations of this type give normal rewards.
    Half Chance: Locations of this type have a 50% chance of being excluded.
    Filler: Forces these locations to contain filler items.
    Disabled: Removes item rewards from these locations.

    Note: Individual locations subject to plando are always enabled, so the plando can be placed properly.
    See also: Excluded Locations, Item Plando (https://archipelago.gg/tutorial/Archipelago/plando/en#item-plando)
    """
    display_name = "Challenge Locations"


class MasteryLocations(LocationInclusion):
    """
    Enables or disables checks for overcoming especially difficult challenges.
    These challenges are often based on Mastery achievements and Feats of Strength.
    Enable these locations to add the most difficult checks to the world.

    Enabled: Locations of this type give normal rewards.
    Half Chance: Locations of this type have a 50% chance of being excluded.
    Filler: Forces these locations to contain filler items.
    Disabled: Removes item rewards from these locations.

    Note: Individual locations subject to plando are always enabled, so the plando can be placed properly.
    See also: Excluded Locations, Item Plando (https://archipelago.gg/tutorial/Archipelago/plando/en#item-plando)
    """
    display_name = "Mastery Locations"


class BasebustLocations(LocationInclusion):
    """
    Enables or disables checks for killing non-objective bases.
    These challenges are about destroying enemy bases that you normally don't have to fight to win a mission.
    Enable these locations if you like sieges or being rewarded for achieving alternate win conditions.

    Enabled: Locations of this type give normal rewards.
    Half Chance: Locations of this type have a 50% chance of being excluded.
      *Note setting this for both challenge and basebust will have a 25% of a challenge-basebust location spawning.
    Filler: Forces these locations to contain filler items.
    Disabled: Removes item rewards from these locations.

    Note: Individual locations subject to plando are always enabled, so the plando can be placed properly.
    See also: Excluded Locations, Item Plando (https://archipelago.gg/tutorial/Archipelago/plando/en#item-plando)
    """
    display_name = "Base-Bust Locations"


class SpeedrunLocations(LocationInclusion):
    """
    Enables or disables checks for overcoming speedrun challenges.
    These challenges are often based on speed achievements or community challenges.
    Enable these locations if you want to be rewarded for going fast.

    Enabled: Locations of this type give normal rewards.
    Half Chance: Locations of this type have a 50% chance of being excluded.
      *Note setting this for both challenge and speedrun will have a 25% of a challenge-speedrun location spawning.
    Filler: Forces these locations to contain filler items.
    Disabled: Removes item rewards from these locations.

    Note: Individual locations subject to plando are always enabled, so the plando can be placed properly.
    See also: Excluded Locations, Item Plando (https://archipelago.gg/tutorial/Archipelago/plando/en#item-plando)
    """
    display_name = "Speedrun Locations"


class PreventativeLocations(LocationInclusion):
    """
    Enables or disables checks for overcoming preventative challenges.
    These challenges are about winning or achieving something while preventing something else from happening,
    such as beating Evacuation without losing a colonist.
    Enable these locations if you want to be rewarded for achieving a higher standard on some locations.

    Enabled: Locations of this type give normal rewards.
    Half Chance: Locations of this type have a 50% chance of being excluded.
      *Note setting this for both challenge and preventative will have a 25% of a challenge-preventative location spawning.
    Filler: Forces these locations to contain filler items.
    Disabled: Removes item rewards from these locations.

    Note: Individual locations subject to plando are always enabled, so the plando can be placed properly.
    See also: Excluded Locations, Item Plando (https://archipelago.gg/tutorial/Archipelago/plando/en#item-plando)
    """
    display_name = "Preventative Locations"


class MissionOrderScouting(Choice):
    """
    Allow the Sc2 mission order client tabs to indicate the type of item (i.e., progression, useful, etc.) available at each location of a mission.
    The option defines when this information will be available for the player.
    By default, this option is deactivated.

    None: Never provide information
    Completed: Only for missions that were completed
    Available: Only for missions that are available to play
    Layout: Only for missions that are in an accessible layout (e.g. Char, Mar Sara, etc.)
    Campaign: Only for missions that are in an accessible campaign (e.g. WoL, HotS, etc.)
    All: All missions
    """
    display_name = "Mission Order Scouting"
    option_none = 0
    option_completed = 1
    option_available = 2
    option_layout = 3
    option_campaign = 4
    option_all = 5

    default = option_none


class FillerPercentage(Range):
    """
    Percentage of the item pool filled with filler items.
    If the world has more locations than items, additional filler items may be generated.
    """
    display_name = "Filler Percentage"
    range_start = 0
    range_end = 70
    default = 0


class MineralsPerItem(Range):
    """
    Configures how many minerals are given per resource item.
    """
    display_name = "Minerals Per Item"
    range_start = 0
    range_end = 200
    default = 25


class VespenePerItem(Range):
    """
    Configures how much vespene gas is given per resource item.
    """
    display_name = "Vespene Per Item"
    range_start = 0
    range_end = 200
    default = 25


class StartingSupplyPerItem(Range):
    """
    Configures how much starting supply per is given per item.
    """
    display_name = "Starting Supply Per Item"
    range_start = 0
    range_end = 16
    default = 2


class MaximumSupplyPerItem(Range):
    """
    Configures how much the maximum supply limit increases per item.
    """
    display_name = "Maximum Supply Per Item"
    range_start = 0
    range_end = 10
    default = 1


class MaximumSupplyReductionPerItem(Range):
    """
    Configures how much maximum supply is reduced per trap item.
    """
    display_name = "Maximum Supply Reduction Per Item"
    range_start = 1
    range_end = 10
    default = 1


class LowestMaximumSupply(Range):
    """Controls how far max supply reduction traps can reduce maximum supply."""
    display_name = "Lowest Maximum Supply"
    range_start = 100
    range_end = 200
    default = 180

class ResearchCostReductionPerItem(Range):
    """
    Controls how much weapon/armor research cost is cut per research cost filler item.
    Affects both minerals and vespene.
    """
    display_name = "Upgrade Cost Discount Per Item"
    range_start = 0
    range_end = 10
    default = 2


class FillerItemsDistribution(ItemDict):
    """
    Controls the relative probability of each filler item being generated over others.
    Items that are bound to specific race or option are automatically eliminated.
    Kerrigan levels generated this way don't go against Kerrigan level item sum
    """
    default = {
        item_names.STARTING_MINERALS: 1,
        item_names.STARTING_VESPENE: 1,
        item_names.STARTING_SUPPLY: 1,
        item_names.MAX_SUPPLY: 1,
        item_names.SHIELD_REGENERATION: 1,
        item_names.BUILDING_CONSTRUCTION_SPEED: 1,
        item_names.KERRIGAN_LEVELS_1: 0,
        item_names.UPGRADE_RESEARCH_SPEED: 1,
        item_names.UPGRADE_RESEARCH_COST: 1,
        item_names.REDUCED_MAX_SUPPLY: 0,
    }
    valid_keys = default.keys()
    display_name = "Filler Items Distribution"

    def __init__(self, value: Dict[str, int]):
        # Allow zeros that the parent class doesn't allow
        if any(item_count < 0 for item_count in value.values()):
            raise Exception("Cannot have negative item weight.")
        super(ItemDict, self).__init__(value)


@dataclass
class Starcraft2Options(PerGameCommonOptions):
    start_inventory: Sc2StartInventory  # type: ignore
    game_difficulty: GameDifficulty
    difficulty_damage_modifier: DifficultyDamageModifier
    game_speed: GameSpeed
    disable_forced_camera: DisableForcedCamera
    skip_cutscenes: SkipCutscenes
    all_in_map: AllInMap
    mission_order: MissionOrder
    maximum_campaign_size: MaximumCampaignSize
    two_start_positions: TwoStartPositions
    key_mode: KeyMode
    player_color_terran_raynor: PlayerColorTerranRaynor
    player_color_protoss: PlayerColorProtoss
    player_color_zerg: PlayerColorZerg
    player_color_zerg_primal: PlayerColorZergPrimal
    player_color_nova: PlayerColorNova
    selected_races: SelectedRaces
    enabled_campaigns: EnabledCampaigns
    enable_race_swap: EnableRaceSwapVariants
    mission_race_balancing: EnableMissionRaceBalancing
    shuffle_campaigns: ShuffleCampaigns
    shuffle_no_build: ShuffleNoBuild
    starter_unit: StarterUnit
    required_tactics: RequiredTactics
    enable_void_trade: EnableVoidTrade
    void_trade_age_limit: VoidTradeAgeLimit
    void_trade_workers: VoidTradeWorkers
    ensure_generic_items: EnsureGenericItems
    min_number_of_upgrades: MinNumberOfUpgrades
    max_number_of_upgrades: MaxNumberOfUpgrades
    mercenary_highlanders: MercenaryHighlanders
    max_upgrade_level: MaxUpgradeLevel
    generic_upgrade_missions: GenericUpgradeMissions
    generic_upgrade_research: GenericUpgradeResearch
    generic_upgrade_research_speedup: GenericUpgradeResearchSpeedup
    generic_upgrade_items: GenericUpgradeItems
    kerrigan_presence: KerriganPresence
    kerrigan_levels_per_mission_completed: KerriganLevelsPerMissionCompleted
    kerrigan_levels_per_mission_completed_cap: KerriganLevelsPerMissionCompletedCap
    kerrigan_level_item_sum: KerriganLevelItemSum
    kerrigan_level_item_distribution: KerriganLevelItemDistribution
    kerrigan_total_level_cap: KerriganTotalLevelCap
    start_primary_abilities: StartPrimaryAbilities
    kerrigan_primal_status: KerriganPrimalStatus
    kerrigan_max_active_abilities: KerriganMaxActiveAbilities
    kerrigan_max_passive_abilities: KerriganMaxPassiveAbilities
    enable_morphling: EnableMorphling
    war_council_nerfs: WarCouncilNerfs
    spear_of_adun_presence: SpearOfAdunPresence
    spear_of_adun_present_in_no_build: SpearOfAdunPresentInNoBuild
    spear_of_adun_passive_ability_presence: SpearOfAdunPassiveAbilityPresence
    spear_of_adun_passive_present_in_no_build: SpearOfAdunPassivesPresentInNoBuild
    spear_of_adun_max_active_abilities: SpearOfAdunMaxActiveAbilities
    spear_of_adun_max_passive_abilities: SpearOfAdunMaxAutocastAbilities
    grant_story_tech: GrantStoryTech
    grant_story_levels: GrantStoryLevels
    nova_max_weapons: NovaMaxWeapons
    nova_max_gadgets: NovaMaxGadgets
    nova_ghost_of_a_chance_variant: NovaGhostOfAChanceVariant
    take_over_ai_allies: TakeOverAIAllies
    locked_items: LockedItems
    excluded_items: ExcludedItems
    unexcluded_items: UnexcludedItems
    excluded_missions: ExcludedMissions
    difficulty_curve: DifficultyCurve
    exclude_very_hard_missions: ExcludeVeryHardMissions
    vanilla_items_only: VanillaItemsOnly
    exclude_overpowered_items: ExcludeOverpoweredItems
    victory_cache: VictoryCache
    vanilla_locations: VanillaLocations
    extra_locations: ExtraLocations
    challenge_locations: ChallengeLocations
    mastery_locations: MasteryLocations
    basebust_locations: BasebustLocations
    speedrun_locations: SpeedrunLocations
    preventative_locations: PreventativeLocations
    filler_percentage: FillerPercentage
    minerals_per_item: MineralsPerItem
    vespene_per_item: VespenePerItem
    starting_supply_per_item: StartingSupplyPerItem
    maximum_supply_per_item: MaximumSupplyPerItem
    maximum_supply_reduction_per_item: MaximumSupplyReductionPerItem
    lowest_maximum_supply: LowestMaximumSupply
    research_cost_reduction_per_item: ResearchCostReductionPerItem
    filler_items_distribution: FillerItemsDistribution
    mission_order_scouting: MissionOrderScouting

    custom_mission_order: CustomMissionOrder

option_groups = [
    OptionGroup("Difficulty Settings", [
        GameDifficulty,
        GameSpeed,
        StarterUnit,
        RequiredTactics,
        WarCouncilNerfs,
        DifficultyCurve,
    ]),
    OptionGroup("Primary Campaign Settings", [
        MissionOrder,
        MaximumCampaignSize,
        EnabledCampaigns,
        EnableRaceSwapVariants,
        ShuffleNoBuild,
    ]),
    OptionGroup("Optional Campaign Settings", [
        KeyMode,
        ShuffleCampaigns,
        AllInMap,
        TwoStartPositions,
        SelectedRaces,
        ExcludeVeryHardMissions,
        EnableMissionRaceBalancing,
    ]),
    OptionGroup("Unit Upgrades", [
        EnsureGenericItems,
        MinNumberOfUpgrades,
        MaxNumberOfUpgrades,
        MaxUpgradeLevel,
        GenericUpgradeMissions,
        GenericUpgradeResearch,
        GenericUpgradeResearchSpeedup,
        GenericUpgradeItems,
    ]),
    OptionGroup("Kerrigan", [
        KerriganPresence,
        GrantStoryLevels,
        KerriganLevelsPerMissionCompleted,
        KerriganLevelsPerMissionCompletedCap,
        KerriganLevelItemSum,
        KerriganLevelItemDistribution,
        KerriganTotalLevelCap,
        StartPrimaryAbilities,
        KerriganPrimalStatus,
        KerriganMaxActiveAbilities,
        KerriganMaxPassiveAbilities,
    ]),
    OptionGroup("Spear of Adun", [
        SpearOfAdunPresence,
        SpearOfAdunPresentInNoBuild,
        SpearOfAdunPassiveAbilityPresence,
        SpearOfAdunPassivesPresentInNoBuild,
        SpearOfAdunMaxActiveAbilities,
        SpearOfAdunMaxAutocastAbilities,
    ]),
    OptionGroup("Nova", [
        NovaMaxWeapons,
        NovaMaxGadgets,
        NovaGhostOfAChanceVariant,
    ]),
    OptionGroup("Race Specific Options", [
        EnableMorphling,
        MercenaryHighlanders,
    ]),
    OptionGroup("Check Locations", [
        VictoryCache,
        VanillaLocations,
        ExtraLocations,
        ChallengeLocations,
        MasteryLocations,
        BasebustLocations,
        SpeedrunLocations,
        PreventativeLocations,
    ]),
    OptionGroup("Filler Options", [
        FillerPercentage,
        MineralsPerItem,
        VespenePerItem,
        StartingSupplyPerItem,
        MaximumSupplyPerItem,
        MaximumSupplyReductionPerItem,
        LowestMaximumSupply,
        ResearchCostReductionPerItem,
        FillerItemsDistribution,
    ]),
    OptionGroup("Inclusions & Exclusions", [
        LockedItems,
        ExcludedItems,
        UnexcludedItems,
        VanillaItemsOnly,
        ExcludeOverpoweredItems,
        ExcludedMissions,
    ]),
    OptionGroup("Advanced Gameplay", [
        MissionOrderScouting,
        DifficultyDamageModifier,
        TakeOverAIAllies,
        EnableVoidTrade,
        VoidTradeAgeLimit,
        VoidTradeWorkers,
        GrantStoryTech,
        CustomMissionOrder,
    ]),
    OptionGroup("Cosmetics", [
        PlayerColorTerranRaynor,
        PlayerColorProtoss,
        PlayerColorZerg,
        PlayerColorZergPrimal,
        PlayerColorNova,
    ])
]

def get_option_value(world: Union['SC2World', None], name: str) -> int:
    """
    You should basically never use this unless `world` can be `None`.
    Use `world.options.<option_name>.value` instead for better typing, autocomplete, and error messages.
    """
    if world is None:
        field: Field = [class_field for class_field in fields(Starcraft2Options) if class_field.name == name][0]
        if isinstance(field.type, str):
            if field.type in globals():
                return globals()[field.type].default
            import Options
            return Options.__dict__[field.type].default
        return field.type.default

    player_option = getattr(world.options, name)

    return player_option.value


def get_enabled_races(world: Optional['SC2World']) -> Set[SC2Race]:
    race_names = world.options.selected_races.value if world and len(world.options.selected_races.value) > 0 else SelectedRaces.valid_keys
    return {race for race in SC2Race if race.get_title() in race_names}


def get_enabled_campaigns(world: Optional['SC2World']) -> Set[SC2Campaign]:
    if world is None:
        return {campaign for campaign in SC2Campaign if campaign.campaign_name in EnabledCampaigns.default}
    campaign_names = world.options.enabled_campaigns
    campaigns = {campaign for campaign in SC2Campaign if campaign.campaign_name in campaign_names}
    if (world.options.mission_order.value == MissionOrder.option_vanilla
        and get_enabled_races(world) != {SC2Race.TERRAN, SC2Race.ZERG, SC2Race.PROTOSS}
        and SC2Campaign.EPILOGUE in campaigns
    ):
        campaigns.remove(SC2Campaign.EPILOGUE)
    if len(campaigns) == 0:
        # Everything is disabled, roll as everything enabled
        return {campaign for campaign in SC2Campaign if campaign != SC2Campaign.GLOBAL}
    return campaigns


def get_disabled_campaigns(world: 'SC2World') -> Set[SC2Campaign]:
    all_campaigns = set(SC2Campaign)
    enabled_campaigns = get_enabled_campaigns(world)
    disabled_campaigns = all_campaigns.difference(enabled_campaigns)
    disabled_campaigns.remove(SC2Campaign.GLOBAL)
    return disabled_campaigns


def get_disabled_flags(world: 'SC2World') -> MissionFlag:
    excluded = (
            (MissionFlag.Terran | MissionFlag.Zerg | MissionFlag.Protoss)
            ^ functools.reduce(lambda a, b: a | b, [race.get_mission_flag() for race in get_enabled_races(world)])
    )
    # filter out no-build missions
    if not world.options.shuffle_no_build.value:
        excluded |= MissionFlag.NoBuild
    raceswap_option = world.options.enable_race_swap.value
    if raceswap_option == EnableRaceSwapVariants.option_disabled:
        excluded |= MissionFlag.RaceSwap
    elif raceswap_option in [EnableRaceSwapVariants.option_pick_one_non_vanilla, EnableRaceSwapVariants.option_shuffle_all_non_vanilla]:
        excluded |= MissionFlag.HasRaceSwap
    # TODO: add more flags to potentially exclude once we have a way to get that from the player
    return MissionFlag(excluded)


def get_excluded_missions(world: 'SC2World') -> Set[SC2Mission]:
    mission_order_type = world.options.mission_order.value
    excluded_mission_names = world.options.excluded_missions.value
    disabled_campaigns = get_disabled_campaigns(world)
    disabled_flags = get_disabled_flags(world)

    excluded_missions: Set[SC2Mission] = set([lookup_name_to_mission[name] for name in excluded_mission_names])

    # Excluding Very Hard missions depending on options
    if (mission_order_type != MissionOrder.option_vanilla and
            (
                    world.options.exclude_very_hard_missions == ExcludeVeryHardMissions.option_true
                    or (
                            world.options.exclude_very_hard_missions == ExcludeVeryHardMissions.option_default
                            and (
                                    (
                                            mission_order_type in dynamic_mission_orders
                                            and world.options.maximum_campaign_size < 20
                                    )
                                    or mission_order_type == MissionOrder.option_mini_campaign
                            )
                    )
            )
    ):
        excluded_missions = excluded_missions.union(
            [mission for mission in SC2Mission if
             mission.pool == MissionPools.VERY_HARD and mission.campaign != SC2Campaign.EPILOGUE]
        )
    # Omitting missions with flags we don't want
    if disabled_flags:
        excluded_missions = excluded_missions.union(get_missions_with_any_flags_in_list(disabled_flags))
    # Omitting missions not in enabled campaigns
    for campaign in disabled_campaigns:
        excluded_missions = excluded_missions.union(campaign_mission_table[campaign])
    # Omitting unwanted mission variants
    if world.options.enable_race_swap.value in [EnableRaceSwapVariants.option_pick_one, EnableRaceSwapVariants.option_pick_one_non_vanilla]:
        swaps = [
            mission for mission in SC2Mission
            if mission not in excluded_missions
            and mission.flags & (MissionFlag.HasRaceSwap|MissionFlag.RaceSwap)
        ]
        while len(swaps) > 0:
            curr = swaps[0]
            variants = [mission for mission in swaps if mission.map_file == curr.map_file]
            variants.sort(key=lambda mission: mission.id)
            swaps = [mission for mission in swaps if mission not in variants]
            if len(variants) > 1:
                variants.pop(world.random.randint(0, len(variants)-1))
                excluded_missions = excluded_missions.union(variants)

    return excluded_missions


def is_mission_in_soa_presence(
    spear_of_adun_presence: int,
    mission: SC2Mission,
    option_class: Type[SpearOfAdunPresence] | Type[SpearOfAdunPassiveAbilityPresence] = SpearOfAdunPresence
) -> bool:
    """
    Returns True if the mission can have Spear of Adun abilities.
    No-build presence must be checked separately.
    """
    return (
        (spear_of_adun_presence == option_class.option_everywhere)
        or (spear_of_adun_presence == option_class.option_protoss and MissionFlag.Protoss in mission.flags)
        or (spear_of_adun_presence == option_class.option_any_race_lotv
            and (mission.campaign == SC2Campaign.LOTV or MissionFlag.VanillaSoa in mission.flags)
        )
        or (spear_of_adun_presence == option_class.option_vanilla
            and (MissionFlag.VanillaSoa in mission.flags  # Keeps SOA off on Growing Shadow, as that's vanilla behaviour
                or (MissionFlag.NoBuild in mission.flags and mission.campaign == SC2Campaign.LOTV)
            )
        )
    )



static_mission_orders = [
    MissionOrder.option_vanilla,
    MissionOrder.option_vanilla_shuffled,
    MissionOrder.option_mini_campaign,
]

dynamic_mission_orders = [
    MissionOrder.option_golden_path,
    MissionOrder.option_grid,
    MissionOrder.option_gauntlet,
    MissionOrder.option_blitz,
    MissionOrder.option_hopscotch,
]

LEGACY_GRID_ORDERS = {3, 4, 8}  # Medium Grid, Mini Grid, and Tiny Grid respectively

kerrigan_unit_available = [
    KerriganPresence.option_vanilla,
]

# Names of upgrades to be included for different options
upgrade_included_names: Dict[int, Set[str]] = {
    GenericUpgradeItems.option_individual_items: {
        item_names.PROGRESSIVE_TERRAN_INFANTRY_WEAPON,
        item_names.PROGRESSIVE_TERRAN_INFANTRY_ARMOR,
        item_names.PROGRESSIVE_TERRAN_VEHICLE_WEAPON,
        item_names.PROGRESSIVE_TERRAN_VEHICLE_ARMOR,
        item_names.PROGRESSIVE_TERRAN_SHIP_WEAPON,
        item_names.PROGRESSIVE_TERRAN_SHIP_ARMOR,
        item_names.PROGRESSIVE_ZERG_MELEE_ATTACK,
        item_names.PROGRESSIVE_ZERG_MISSILE_ATTACK,
        item_names.PROGRESSIVE_ZERG_GROUND_CARAPACE,
        item_names.PROGRESSIVE_ZERG_FLYER_ATTACK,
        item_names.PROGRESSIVE_ZERG_FLYER_CARAPACE,
        item_names.PROGRESSIVE_PROTOSS_GROUND_WEAPON,
        item_names.PROGRESSIVE_PROTOSS_GROUND_ARMOR,
        item_names.PROGRESSIVE_PROTOSS_SHIELDS,
        item_names.PROGRESSIVE_PROTOSS_AIR_WEAPON,
        item_names.PROGRESSIVE_PROTOSS_AIR_ARMOR,
    },
    GenericUpgradeItems.option_bundle_weapon_and_armor: {
        item_names.PROGRESSIVE_TERRAN_WEAPON_UPGRADE,
        item_names.PROGRESSIVE_TERRAN_ARMOR_UPGRADE,
        item_names.PROGRESSIVE_ZERG_WEAPON_UPGRADE,
        item_names.PROGRESSIVE_ZERG_ARMOR_UPGRADE,
        item_names.PROGRESSIVE_PROTOSS_WEAPON_UPGRADE,
        item_names.PROGRESSIVE_PROTOSS_ARMOR_UPGRADE,
    },
    GenericUpgradeItems.option_bundle_unit_class: {
        item_names.PROGRESSIVE_TERRAN_INFANTRY_UPGRADE,
        item_names.PROGRESSIVE_TERRAN_VEHICLE_UPGRADE,
        item_names.PROGRESSIVE_TERRAN_SHIP_UPGRADE,
        item_names.PROGRESSIVE_ZERG_GROUND_UPGRADE,
        item_names.PROGRESSIVE_ZERG_FLYER_UPGRADE,
        item_names.PROGRESSIVE_PROTOSS_GROUND_UPGRADE,
        item_names.PROGRESSIVE_PROTOSS_AIR_UPGRADE,
    },
    GenericUpgradeItems.option_bundle_all: {
        item_names.PROGRESSIVE_TERRAN_WEAPON_ARMOR_UPGRADE,
        item_names.PROGRESSIVE_ZERG_WEAPON_ARMOR_UPGRADE,
        item_names.PROGRESSIVE_PROTOSS_WEAPON_ARMOR_UPGRADE,
    }
}

# Mapping trade age limit options to their millisecond equivalents
void_trade_age_limits_ms: Dict[int, int] = {
    VoidTradeAgeLimit.option_5_minutes: 1000 * int(timedelta(minutes = 5).total_seconds()),
    VoidTradeAgeLimit.option_30_minutes: 1000 * int(timedelta(minutes = 30).total_seconds()),
    VoidTradeAgeLimit.option_1_hour: 1000 * int(timedelta(hours = 1).total_seconds()),
    VoidTradeAgeLimit.option_2_hours: 1000 * int(timedelta(hours = 2).total_seconds()),
    VoidTradeAgeLimit.option_4_hours: 1000 * int(timedelta(hours = 4).total_seconds()),
    VoidTradeAgeLimit.option_1_day: 1000 * int(timedelta(days = 1).total_seconds()),
    VoidTradeAgeLimit.option_1_week: 1000 * int(timedelta(weeks = 1).total_seconds()),
}

# Store the names of all options
OPTION_NAME = {option_type: name for name, option_type in Starcraft2Options.type_hints.items()}
