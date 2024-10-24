from dataclasses import dataclass, fields, Field
from typing import *

from Utils import is_iterable_except_str
from Options import *
from Utils import get_fuzzy_results
from BaseClasses import PlandoOptions
from .mission_tables import SC2Campaign, SC2Mission, lookup_name_to_mission, MissionPools, get_missions_with_any_flags_in_list, \
    campaign_mission_table, SC2Race, MissionFlag
from .mission_groups import mission_groups, MissionGroupNames
from .mission_order.options import CustomMissionOrder
from . import item_names

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


class SelectRaces(Choice):
    """
    Pick which factions' missions and items can be shuffled into the world.
    """
    display_name = "Select Playable Races"
    option_all = (MissionFlag.Terran|MissionFlag.Zerg|MissionFlag.Protoss).value
    option_terran = MissionFlag.Terran.value
    option_zerg = MissionFlag.Zerg.value
    option_protoss = MissionFlag.Protoss.value
    option_terran_and_zerg = (MissionFlag.Terran|MissionFlag.Zerg).value
    option_terran_and_protoss = (MissionFlag.Terran|MissionFlag.Protoss).value
    option_zerg_and_protoss = (MissionFlag.Zerg|MissionFlag.Protoss).value
    option_plando = 0
    default = option_all


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


class MaximumCampaignSize(Range):
    """
    Sets an upper bound on how many missions to include when a variable-size mission order is selected.
    If a set-size mission order is selected, does nothing.
    """
    display_name = "Maximum Campaign Size"
    range_start = 1
    range_end = 113
    default = 83


class GridTwoStartPositions(Toggle):
    """
    If turned on and 'grid' or 'hopscotch' mission orders are selected,
    removes a mission from the starting corner and sets the adjacent two missions as the starter missions.
    """
    display_name = "Start with two unlocked missions on grid"
    default = Toggle.option_false


class KeyMode(Choice):
    """
    Optionally creates Key items that must be found in the multiworld to unlock parts of the mission order,
    in addition to any regular requirements a mission may have.
    Disabled: Don't create any keys.
    Questlines: Create keys for questlines besides the starter ones, eg. "Colonist (Wings of Liberty) Questline Key".
    Only works for Vanilla, Vanilla Shuffled, Mini Campaign, and Golden Path mission orders.
    Missions: Create keys for missions besides the starter ones, eg. "Zero Hour Mission Key".
    """
    display_name = "Key Mode"
    option_disabled = 0
    option_questlines = 1
    option_missions = 2
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
    """Determines in-game team color for playable Raynor's Raiders (Terran) factions."""
    display_name = "Terran Player Color (Raynor)"


class PlayerColorProtoss(ColorChoice):
    """Determines in-game team color for playable Protoss factions."""
    display_name = "Protoss Player Color"


class PlayerColorZerg(ColorChoice):
    """Determines in-game team color for playable Zerg factions before Kerrigan becomes Primal Kerrigan."""
    display_name = "Zerg Player Color"


class PlayerColorZergPrimal(ColorChoice):
    """Determines in-game team color for playable Zerg factions after Kerrigan becomes Primal Kerrigan."""
    display_name = "Zerg Player Color (Primal)"


class PlayerColorNova(ColorChoice):
    """Determines in-game team color for playable Zerg factions after Kerrigan becomes Primal Kerrigan."""
    display_name = "Terran Player Color (Nova)"


class EnableWolMissions(DefaultOnToggle):
    """
    Enables missions from main Wings of Liberty campaign.
    """
    display_name = "Enable Wings of Liberty missions"


class EnableProphecyMissions(DefaultOnToggle):
    """
    Enables missions from Prophecy mini-campaign.
    """
    display_name = "Enable Prophecy missions"


class EnableHotsMissions(DefaultOnToggle):
    """
    Enables missions from Heart of the Swarm campaign.
    """
    display_name = "Enable Heart of the Swarm missions"


class EnableLotVPrologueMissions(DefaultOnToggle):
    """
    Enables missions from Prologue campaign.
    """
    display_name = "Enable Prologue (Legacy of the Void) missions"


class EnableLotVMissions(DefaultOnToggle):
    """
    Enables missions from Legacy of the Void campaign.
    """
    display_name = "Enable Legacy of the Void (main campaign) missions"


class EnableEpilogueMissions(DefaultOnToggle):
    """
    Enables missions from Epilogue campaign.
    These missions are considered very hard.

    Enabling Wings of Liberty, Heart of the Swarm and Legacy of the Void is strongly recommended in order to play Epilogue.
    Not recommended for short mission orders.
    See also: Exclude Very Hard Missions
    """
    display_name = "Enable Epilogue missions"


class EnableNCOMissions(DefaultOnToggle):
    """
    Enables missions from Nova Covert Ops campaign.

    Note: For best gameplay experience it's recommended to also enable Wings of Liberty campaign.
    """
    display_name = "Enable Nova Covert Ops missions"


class EnableRaceSwapVariants(Choice):
    """
    Allow mission variants where you play a faction other than the one the map was initially
    designed for. NOTE: Cutscenes are always skipped on race-swapped mission variants.

    Disabled: Don't shuffle any non-vanilla map variants into the pool.
    Pick One: Shuffle up to 1 valid version of each map into the pool, depending on other settings.
    Shuffle All: Each version of a map can appear in the same pool (so a map can appear up to 3 times as different races)
    """
    display_name = "Enable Race-Swapped Mission Variants"
    option_disabled = 0
    option_pick_one = 1
    option_shuffle_all = 2
    default = option_disabled


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
    Determines the maximum tactical difficulty of the world (separate from mission difficulty).  Higher settings
    increase randomness.

    Standard:  All missions can be completed with good micro and macro.
    Advanced:  Completing missions may require relying on starting units and micro-heavy units.
    No Logic:  Units and upgrades may be placed anywhere.  LIKELY TO RENDER THE RUN IMPOSSIBLE ON HARDER DIFFICULTIES!
               Locks Grant Story Tech option to true.
    """
    display_name = "Required Tactics"
    option_standard = 0
    option_advanced = 1
    option_no_logic = 2


class GenericUpgradeMissions(Range):
    """Determines the percentage of missions in the mission order that must be completed before
    level 1 of all weapon and armor upgrades is unlocked.  Level 2 upgrades require double the amount of missions,
    and level 3 requires triple the amount.  The required amounts are always rounded down.
    If set to 0, upgrades are instead added to the item pool and must be found to be used."""
    display_name = "Generic Upgrade Missions"
    range_start = 0
    range_end = 25 # Higher values lead to fails often
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


class GenericUpgradeItems(Choice):
    """Determines how weapon and armor upgrades are split into items.  All options produce 3 levels of each item.
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
    locked_items may override these exclusions."""
    display_name = "Vanilla Items Only"


# Current maximum number of upgrades for a unit
MAX_UPGRADES_OPTION = 14


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
    Set a minimum to the number of upgrades a unit/structure can have.
    Note that most units have 4 or 6 upgrades.
    If a unit has fewer upgrades than the minimum, it will have all of its upgrades.

    Doesn't affect shared unit upgrades.
    """
    display_name = "Minimum number of upgrades per unit/structure"
    range_start = 0
    range_end = MAX_UPGRADES_OPTION
    default = 2


class MaxNumberOfUpgrades(Range):
    """
    Set a maximum to the number of upgrades a unit/structure can have. -1 is used to define unlimited.
    Note that most unit have 4 to 6 upgrades.

    Doesn't affect shared unit upgrades.
    """
    display_name = "Maximum number of upgrades per unit/structure"
    range_start = -1
    range_end = MAX_UPGRADES_OPTION
    default = -1


class KerriganPresence(Choice):
    """
    Determines whether Kerrigan is playable outside of missions that require her.

    Vanilla: Kerrigan is playable as normal, appears in the same missions as in vanilla game.
    Not Present:  Kerrigan is not playable, unless the mission requires her to be present.  Other hero units stay playable,
        and locations normally requiring Kerrigan can be checked by any unit.
        Kerrigan level items, active abilities and passive abilities affecting her will not appear.
        In missions where the Kerrigan unit is required, story abilities are given in same way as Grant Story Tech is set to true
    Not Present And No Passives:  In addition to the above, Kerrigan's passive abilities affecting other units (such as Twin Drones) will not appear.

    Note: Always set to "Not Present" if Heart of the Swarm campaign is disabled.
    """
    display_name = "Kerrigan Presence"
    option_vanilla = 0
    option_not_present = 1


class KerriganLevelsPerMissionCompleted(Range):
    """
    Determines how many levels Kerrigan gains when a mission is beaten.

    NOTE: Setting this too low can result in generation failures if The Infinite Cycle or Supreme are in the mission pool.
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

class EnableMorphling(Toggle):
    """
    Determines whether the player can build Morphlings, which allow for inefficient morphing of advanced units
    like Ravagers and Lurkers without requiring the base unit to be unlocked first.
    """
    display_name = "Enable Morphling"


class NerfUnitBaselines(Toggle):
    """
    Controls whether some units can initially be found in a nerfed state, with upgrades restoring their stronger power level.
    For example, nerfed Zealots will lack the whirlwind upgrade until it is found as an item.
    """
    display_name = "Allow Unit Nerfs"


class SpearOfAdunPresence(Choice):
    """
    Determines in which missions Spear of Adun calldowns will be available.
    Affects only abilities used from Spear of Adun top menu.

    Not Present: Spear of Adun calldowns are unavailable.
    LotV Protoss: Spear of Adun calldowns are only available in LotV main campaign
    Protoss: Spear of Adun calldowns are available in any Protoss mission
    Everywhere: Spear of Adun calldowns are available in any mission of any race
    """
    display_name = "Spear of Adun Presence"
    option_not_present = 0
    option_lotv_protoss = 1
    option_protoss = 2
    option_everywhere = 3
    default = option_lotv_protoss

    # Fix case
    @classmethod
    def get_option_name(cls, value: int) -> str:
        if value == SpearOfAdunPresence.option_lotv_protoss:
            return "LotV Protoss"
        else:
            return super().get_option_name(value)


class SpearOfAdunPresentInNoBuild(Toggle):
    """
    Determines if Spear of Adun calldowns are available in no-build missions.

    If turned on, Spear of Adun calldown powers are available in missions specified under "Spear of Adun Presence".
    If turned off, Spear of Adun calldown powers are unavailable in all no-build missions
    """
    display_name = "Spear of Adun Present in No-Build"


class SpearOfAdunAutonomouslyCastAbilityPresence(Choice):
    """
    Determines availability of Spear of Adun powers, that are autonomously cast.
    Affects abilities like Reconstruction Beam or Overwatch

    Not Presents: Autocasts are not available.
    LotV Protoss: Spear of Adun autocasts are only available in LotV main campaign
    Protoss: Spear of Adun autocasts are available in any Protoss mission
    Everywhere: Spear of Adun autocasts are available in any mission of any race
    """
    display_name = "Spear of Adun Autonomously Cast Powers Presence"
    option_not_present = 0
    option_lotv_protoss = 1
    option_protoss = 2
    option_everywhere = 3
    default = option_lotv_protoss

    # Fix case
    @classmethod
    def get_option_name(cls, value: int) -> str:
        if value == SpearOfAdunPresence.option_lotv_protoss:
            return "LotV Protoss"
        else:
            return super().get_option_name(value)


class SpearOfAdunAutonomouslyCastPresentInNoBuild(Toggle):
    """
    Determines if Spear of Adun autocasts are available in no-build missions.

    If turned on, Spear of Adun autocasts are available in missions specified under "Spear of Adun Autonomously Cast Powers Presence".
    If turned off, Spear of Adun autocasts are unavailable in all no-build missions
    """
    display_name = "Spear of Adun Autonomously Cast Powers Present in No-Build"


class GrantStoryTech(Toggle):
    """
    If set true, grants special tech required for story mission completion for duration of the mission.
    Otherwise, you need to find these tech by a normal means as items.
    Affects story missions like Back in the Saddle and Supreme

    Locked to true if Required Tactics is set to no logic.
    """
    display_name = "Grant Story Tech"


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
                from . import item_groups
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


class ExcludeVeryHardMissions(Choice):
    """
    Excludes Very Hard missions outside of Epilogue campaign (All-In, The Reckoning, Salvation, and all Epilogue missions are considered Very Hard).
    Doesn't apply to "Vanilla" mission order.

    Default: Not excluded for mission orders "Vanilla Shuffled" or "Grid" with Maximum Campaign Size >= 20,
             excluded for any other order
    Yes: Non-Epilogue Very Hard missions are excluded and won't be generated
    No: Non-Epilogue Very Hard missions can appear normally. Not recommended for too short mission orders.

    See also: Excluded Missions, Enable Epilogue Missions, Maximum Campaign Size
    """
    display_name = "Exclude Very Hard Missions"
    option_default = 0
    option_true = 1
    option_false = 2

    @classmethod
    def get_option_name(cls, value):
        return ["Default", "Yes", "No"][int(value)]


class LocationInclusion(Choice):
    option_enabled = 0
    option_resources = 1
    option_disabled = 2


class VanillaLocations(LocationInclusion):
    """
    Enables or disables item rewards for completing vanilla objectives.
    Vanilla objectives are bonus objectives from the vanilla game,
    along with some additional objectives to balance the missions.
    Enable these locations for a balanced experience.

    Enabled: All locations fitting into this do their normal rewards
    Resources: Forces these locations to contain Starting Resources
    Disabled: Removes item rewards from these locations.

    Note: Individual locations subject to plando are always enabled, so the plando can be placed properly.
    See also: Excluded Locations, Item Plando (https://archipelago.gg/tutorial/Archipelago/plando/en#item-plando)
    """
    display_name = "Vanilla Locations"


class ExtraLocations(LocationInclusion):
    """
    Enables or disables item rewards for mission progress and minor objectives.
    This includes mandatory mission objectives,
    collecting reinforcements and resource pickups,
    destroying structures, and overcoming minor challenges.
    Enables these locations to add more checks and items to your world.

    Enabled: All locations fitting into this do their normal rewards
    Resources: Forces these locations to contain Starting Resources
    Disabled: Removes item rewards from these locations.

    Note: Individual locations subject to plando are always enabled, so the plando can be placed properly.
    See also: Excluded Locations, Item Plando (https://archipelago.gg/tutorial/Archipelago/plando/en#item-plando)
    """
    display_name = "Extra Locations"


class ChallengeLocations(LocationInclusion):
    """
    Enables or disables item rewards for completing challenge tasks.
    Challenges are tasks that are more difficult than completing the mission, and are often based on achievements.
    You might be required to visit the same mission later after getting stronger in order to finish these tasks.
    Enable these locations to increase the difficulty of completing the multiworld.

    Enabled: All locations fitting into this do their normal rewards
    Resources: Forces these locations to contain Starting Resources
    Disabled: Removes item rewards from these locations.

    Note: Individual locations subject to plando are always enabled, so the plando can be placed properly.
    See also: Excluded Locations, Item Plando (https://archipelago.gg/tutorial/Archipelago/plando/en#item-plando)
    """
    display_name = "Challenge Locations"


class MasteryLocations(LocationInclusion):
    """
    Enables or disables item rewards for overcoming especially difficult challenges.
    These challenges are often based on Mastery achievements and Feats of Strength.
    Enable these locations to add the most difficult checks to the world.

    Enabled: All locations fitting into this do their normal rewards
    Resources: Forces these locations to contain Starting Resources
    Disabled: Removes item rewards from these locations.

    Note: Individual locations subject to plando are always enabled, so the plando can be placed properly.
    See also: Excluded Locations, Item Plando (https://archipelago.gg/tutorial/Archipelago/plando/en#item-plando)
    """
    display_name = "Mastery Locations"


class SpeedrunLocations(LocationInclusion):
    """
    Enables or disables item rewards for overcoming speedrun challenges.
    These challenges are often based on speed achievements or community challenges.
    Enable these locations if you want to be rewarded for going fast.

    Enabled: All locations fitting into this do their normal rewards
    Resources: Forces these locations to contain Starting Resources
    Disabled: Removes item rewards from these locations.

    Note: Individual locations subject to plando are always enabled, so the plando can be placed properly.
    See also: Excluded Locations, Item Plando (https://archipelago.gg/tutorial/Archipelago/plando/en#item-plando)
    """
    display_name = "Speedrun Locations"


class PreventativeLocations(LocationInclusion):
    """
    Enables or disables item rewards for overcoming preventative challenges.
    These challenges are about winning or achieving something while preventing something else from happening,
    such as beating Evacuation without losing a colonist.
    Enable these locations if you want to be rewarded for achieving a higher standard on some locations.

    Enabled: All locations fitting into this do their normal rewards
    Resources: Forces these locations to contain Starting Resources
    Disabled: Removes item rewards from these locations.

    Note: Individual locations subject to plando are always enabled, so the plando can be placed properly.
    See also: Excluded Locations, Item Plando (https://archipelago.gg/tutorial/Archipelago/plando/en#item-plando)
    """
    display_name = "Preventative Locations"


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


@dataclass
class Starcraft2Options(PerGameCommonOptions):
    game_difficulty: GameDifficulty
    game_speed: GameSpeed
    disable_forced_camera: DisableForcedCamera
    skip_cutscenes: SkipCutscenes
    all_in_map: AllInMap
    mission_order: MissionOrder
    maximum_campaign_size: MaximumCampaignSize
    grid_two_start_positions: GridTwoStartPositions
    key_mode: KeyMode
    player_color_terran_raynor: PlayerColorTerranRaynor
    player_color_protoss: PlayerColorProtoss
    player_color_zerg: PlayerColorZerg
    player_color_zerg_primal: PlayerColorZergPrimal
    player_color_nova: PlayerColorNova
    selected_races: SelectRaces
    enable_wol_missions: EnableWolMissions
    enable_prophecy_missions: EnableProphecyMissions
    enable_hots_missions: EnableHotsMissions
    enable_lotv_prologue_missions: EnableLotVPrologueMissions
    enable_lotv_missions: EnableLotVMissions
    enable_epilogue_missions: EnableEpilogueMissions
    enable_nco_missions: EnableNCOMissions
    enable_race_swap: EnableRaceSwapVariants
    shuffle_campaigns: ShuffleCampaigns
    shuffle_no_build: ShuffleNoBuild
    starter_unit: StarterUnit
    required_tactics: RequiredTactics
    ensure_generic_items: EnsureGenericItems
    min_number_of_upgrades: MinNumberOfUpgrades
    max_number_of_upgrades: MaxNumberOfUpgrades
    generic_upgrade_missions: GenericUpgradeMissions
    generic_upgrade_research: GenericUpgradeResearch
    generic_upgrade_items: GenericUpgradeItems
    kerrigan_presence: KerriganPresence
    kerrigan_levels_per_mission_completed: KerriganLevelsPerMissionCompleted
    kerrigan_levels_per_mission_completed_cap: KerriganLevelsPerMissionCompletedCap
    kerrigan_level_item_sum: KerriganLevelItemSum
    kerrigan_level_item_distribution: KerriganLevelItemDistribution
    kerrigan_total_level_cap: KerriganTotalLevelCap
    start_primary_abilities: StartPrimaryAbilities
    kerrigan_primal_status: KerriganPrimalStatus
    enable_morphling: EnableMorphling
    nerf_unit_baselines: NerfUnitBaselines
    spear_of_adun_presence: SpearOfAdunPresence
    spear_of_adun_present_in_no_build: SpearOfAdunPresentInNoBuild
    spear_of_adun_autonomously_cast_ability_presence: SpearOfAdunAutonomouslyCastAbilityPresence
    spear_of_adun_autonomously_cast_present_in_no_build: SpearOfAdunAutonomouslyCastPresentInNoBuild
    grant_story_tech: GrantStoryTech
    grant_story_levels: GrantStoryLevels
    take_over_ai_allies: TakeOverAIAllies
    locked_items: LockedItems
    excluded_items: ExcludedItems
    unexcluded_items: UnexcludedItems
    excluded_missions: ExcludedMissions
    exclude_very_hard_missions: ExcludeVeryHardMissions
    vanilla_items_only: VanillaItemsOnly
    vanilla_locations: VanillaLocations
    extra_locations: ExtraLocations
    challenge_locations: ChallengeLocations
    mastery_locations: MasteryLocations
    speedrun_locations: SpeedrunLocations
    preventative_locations: PreventativeLocations
    minerals_per_item: MineralsPerItem
    vespene_per_item: VespenePerItem
    starting_supply_per_item: StartingSupplyPerItem

    custom_mission_order: CustomMissionOrder

def get_option_value(world: Union['SC2World', None], name: str) -> Union[int, FrozenSet]:
    if world is None:
        field: Field = [class_field for class_field in fields(Starcraft2Options) if class_field.name == name][0]
        if isinstance(field.type, str):
            if field.type in globals():
                return globals()[field.type].default
        return field.type.default

    player_option = getattr(world.options, name)

    return player_option.value


def get_enabled_races(world: 'SC2World') -> Set[SC2Race]:
    selection = get_option_value(world, 'selected_races')
    if selection == SelectRaces.option_all:
        return set(SC2Race)
    enabled = {SC2Race.ANY}
    if selection & MissionFlag.Terran:
        enabled.add(SC2Race.TERRAN)
    if selection & MissionFlag.Zerg:
        enabled.add(SC2Race.ZERG)
    if selection & MissionFlag.Protoss:
        enabled.add(SC2Race.PROTOSS)
    return enabled


def get_enabled_campaigns(world: 'SC2World') -> Set[SC2Campaign]:
    enabled_campaigns = set()
    if get_option_value(world, "enable_wol_missions"):
        enabled_campaigns.add(SC2Campaign.WOL)
    if get_option_value(world, "enable_prophecy_missions"):
        enabled_campaigns.add(SC2Campaign.PROPHECY)
    if get_option_value(world, "enable_hots_missions"):
        enabled_campaigns.add(SC2Campaign.HOTS)
    if get_option_value(world, "enable_lotv_prologue_missions"):
        enabled_campaigns.add(SC2Campaign.PROLOGUE)
    if get_option_value(world, "enable_lotv_missions"):
        enabled_campaigns.add(SC2Campaign.LOTV)
    # Force-disable epilogue missions if vanilla mission order with at least 1 disabled faction
    if get_option_value(world, "enable_epilogue_missions") \
            and (get_option_value(world, "mission_order") != MissionOrder.option_vanilla
                 or get_option_value(world, "selected_races") == SelectRaces.option_all):
        enabled_campaigns.add(SC2Campaign.EPILOGUE)
    if get_option_value(world, "enable_nco_missions"):
        enabled_campaigns.add(SC2Campaign.NCO)
    return enabled_campaigns


def get_disabled_campaigns(world: 'SC2World') -> Set[SC2Campaign]:
    all_campaigns = set(SC2Campaign)
    enabled_campaigns = get_enabled_campaigns(world)
    disabled_campaigns = all_campaigns.difference(enabled_campaigns)
    disabled_campaigns.remove(SC2Campaign.GLOBAL)
    return disabled_campaigns


def get_disabled_flags(world: 'SC2World') -> MissionFlag:
    excluded = (MissionFlag.Terran|MissionFlag.Zerg|MissionFlag.Protoss) ^ MissionFlag(get_option_value(world, "selected_races"))
    # filter out no-build missions
    if not get_option_value(world, "shuffle_no_build"):
        excluded |= MissionFlag.NoBuild
    if get_option_value(world, "enable_race_swap") == EnableRaceSwapVariants.option_disabled:
        excluded |= MissionFlag.RaceSwap
    # TODO: add more flags to potentially exclude once we have a way to get that from the player
    return MissionFlag(excluded)


def get_excluded_missions(world: 'SC2World') -> Set[SC2Mission]:
    mission_order_type = world.options.mission_order.value
    excluded_mission_names = world.options.excluded_missions.value
    disabled_campaigns = get_disabled_campaigns(world)
    disabled_flags = get_disabled_flags(world)

    excluded_missions: Set[SC2Mission] = set([lookup_name_to_mission[name] for name in excluded_mission_names])

    # Excluding Very Hard missions depending on options
    if world.options.exclude_very_hard_missions == ExcludeVeryHardMissions.option_true or (
        world.options.exclude_very_hard_missions == ExcludeVeryHardMissions.option_default and (
            mission_order_type in dynamic_mission_orders and world.options.maximum_campaign_size < 20 or
            mission_order_type == MissionOrder.option_mini_campaign
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
    if get_option_value(world, "enable_race_swap") == EnableRaceSwapVariants.option_pick_one:
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


static_mission_orders = [
    MissionOrder.option_vanilla,
    MissionOrder.option_vanilla_shuffled,
    MissionOrder.option_mini_campaign
]

dynamic_mission_orders = [
    MissionOrder.option_golden_path,
    MissionOrder.option_grid,
    MissionOrder.option_gauntlet,
    MissionOrder.option_blitz,
    MissionOrder.option_hopscotch
]

LEGACY_GRID_ORDERS = {3, 4, 8}  # Medium Grid, Mini Grid, and Tiny Grid respectively

kerrigan_unit_available = [
    KerriganPresence.option_vanilla,
]

# Names of upgrades to be included for different options
upgrade_included_names: Dict[GenericUpgradeItems, Set[str]] = {
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
