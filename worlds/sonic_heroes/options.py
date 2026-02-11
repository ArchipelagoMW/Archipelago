
from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from worlds.sonic_heroes import SonicHeroesWorld

from dataclasses import dataclass
from Options import *
from .constants import *

class MakePuml(Toggle):
    """
    Should This APWorld Make a Puml File?
    """
    display_name = "Make Puml"
    visibility = Visibility.spoiler


class UnlockType(Choice):
    """
    How should the entire run be structured?
    Ability Character Unlocks has all levels open from the start and locks characters and abilities behind items.
    Legacy Gates has all abilities and characters unlocked from the start and instead locks level access behind level gates (like SA2).
    """
    display_name = "Unlock Type"
    option_ability_character_unlocks = 0
    option_legacy_level_gates = 1
    default = 0


class FinalBoss(Choice):
    """
    What should the final boss be?
    Metal Madness requires both Metal Madness and Metal Overlord (in one go).
    This is accessed from Metal Overlord in level select regardless of choice.
    Sea Gate is the scariest final boss of all time.
    """
    display_name = "Final Boss"
    option_metal_madness = 0
    option_metal_overlord = 1
    option_sea_gate = 2
    default = 1

class RequiredRank(Choice):
    """
    What Minimum Rank should be required to send level complete checks?
    This option is ignored when Ability and Character Unlocks is enabled.
    This also affects Bonus/Emerald stage unlocking as well.
    """
    display_name = "Required Rank"
    option_rank_e = 0
    option_rank_d = 1
    option_rank_c = 2
    option_rank_b = 3
    option_rank_a = 4
    default = 0


class GoalUnlockConditions(OptionSet):
    """
    How should Metal Madness/Overlord be unlocked?
    Adding Multiple will require all of them.

    Valid Choices:
        - 'Emblems'
        - 'Emeralds'
        - 'Level Completions All Teams'
        - 'Level Completions Per Story'


    Note: All Characters are required to be unlocked if Unlock Type is Ability Character Unlocks as well.
    Note: There are no Emblems added to the item pool if Unlock Type is Ability Character Unlocks
    """
    display_name = "Goal Unlock Conditions"
    #valid_keys_casefold = True
    valid_keys = {name for name in goal_unlock_options}
    # noinspection PyClassVar
    default = {name for name in goal_unlock_options if name != EMBLEMS}  # type: ignore


class GoalLevelCompletions(Range):
    """
    How Many Level Completions are needed across all Stories to unlock Metal Madness/Overlord?
    Completing Both Acts of a level will not count as a second Completion.
    This Requires Level Completion Goal Unlock Condition.
    This is capped to 14 * the number of stories enabled.
    This is in addition to Goal Unlock Conditions Per Story.
    """
    display_name = "Goal Level Completions"
    range_start = 0
    range_end = 70
    default = 0


class GoalLevelCompletionsPerStory(Range):
    """
    How Many Level Completions are needed per Story to unlock Metal Madness/Overlord?
    This Requires Level Completion Per Story Goal Unlock Condition.
    Each Story will require at least this many completed levels.
    This is in addition to Goal Level Completions.
    """
    display_name = "Goal Level Completions Per Story"
    range_start = 0
    range_end = 14
    default = 7


class AbilityUnlocks(Choice):
    """
    How should Ability Unlocks be Handled (if enabled)?
    Entire Story will make there be a "Homing Attack" item for each Team that unlocks Homing Attack on all levels for that team.
    All Regions Separate will have 7 sets of ability items (Per Team) that unlock the ability for that respective region. (A Region is a set of levels that follow the same theme)
    For example, Seaside Hill and Ocean Palace are both in the Ocean Region

    Dev Note: All Regions Separate can cause significant BK in syncs (depending on speed of other games)
    Recommended for asyncs only (or with proper consideration)
    """
    display_name = "Ability Unlocks"
    option_all_regions_separate = 0
    option_entire_story = 1
    default = 1


class LegacyNumberOfLevelGates(Range):
    """
    How many Level Gates should there be?
    This option is ignored if set to Ability and Character Unlocks.

    This will result in this many groups of levels locked behind emblems and boss completions and 1 additional group unlocked from the start.
    """
    display_name = "Legacy Number Of Level Gates"
    range_start = 0
    range_end = 7
    default = 3

class LegacyLevelGatesAllowedBosses(OptionSet):
    """
    Which Bosses should be allowed to be level gate bosses?
    This option is ignored if set to Ability and Character Unlocks.
    This needs to be equal to the number of level gates or larger.

    Valid Choices:

        - 'Egg Hawk'
        - 'Team Fight 1'
        - 'Robot Carnival'
        - 'Egg Albatross'
        - 'Team Fight 2'
        - 'Robot Storm'
        - 'Egg Emperor'
    """
    display_name = "Legacy Level Gates Allowed Bosses"
    # valid_keys_casefold = True
    valid_keys = {name for name in sonic_heroes_extra_names.values()}
    # noinspection PyClassVar
    default = {name for name in sonic_heroes_extra_names.values()}  # type: ignore


class IncludedLevelsAndSanities(OptionSet):
    """
    Which Levels and Sanities should be included?
    Note that some of these (like Sonic Act 2 and Super Hard Mode are mutually exclusive)

    Valid Choices:
    [
        'Sonic Act A',
        'Sonic Act B',
        'Sonic KeySanity 1 Set',
        'Sonic KeySanity Both Acts',
        'Sonic CheckpointSanity 1 Set',
        'Sonic CheckpointSanity Both Acts',
        
        'Dark Act A',
        'Dark Act B',
        'Dark ObjSanity',
        'Dark KeySanity 1 Set',
        'Dark KeySanity Both Acts',
        'Dark CheckpointSanity 1 Set',
        'Dark CheckpointSanity Both Acts',
        
        'Rose Act A',
        'Rose Act B',
        'Rose ObjSanity',
        'Rose KeySanity 1 Set',
        'Rose KeySanity Both Acts',
        'Rose CheckpointSanity 1 Set',
        'Rose CheckpointSanity Both Acts',
        
        'Chaotix Act A',
        'Chaotix Act B',
        'Chaotix ObjSanity',
        'Chaotix KeySanity 1 Set',
        'Chaotix KeySanity Both Acts',
        'Chaotix CheckpointSanity 1 Set',
        'Chaotix CheckpointSanity Both Acts',
        
        'Super Hard Mode',
        'Super Hard Mode CheckpointSanity',
    ]
    """
    display_name = "Included Levels and Sanities"
    # valid_keys_casefold = True
    valid_keys = {name for name in features_in_rando}
    # noinspection PyClassVar
    default = {name for name in features_in_rando_default}  # type: ignore


class SonicStoryStartingCharacter(Choice):
    """
    If Ability and Character Unlocks are enabled, which Character should be unlocked for Sonic Story from the Start?
    Knuckles has the largest sphere 1
    Sonic and Tails are even though Tails is slightly more restrictive logically
    """
    display_name = "Sonic Story Starting Character"
    option_sonic = 0
    option_tails = 1
    option_knuckles = 2
    # noinspection PyClassVar
    default = 'random'  # type: ignore


class DarkSanity(Choice):
    """
    How many enemies are needed for a sanity check?
    Requires Mission B and Dark ObjSanity to be enabled
    1 results in 1400 checks
    20 results in 70 checks
    """
    display_name = "Dark Sanity"
    #option_disabled = 0
    option_1 = 1
    option_5 = 5
    option_10 = 10
    option_20 = 20
    default = 20


class DarkStoryStartingCharacter(Choice):
    """
    If Ability and Character Unlocks are enabled, which Character should be unlocked for Dark Story from the Start?
    """
    display_name = "Dark Story Starting Character"
    option_shadow = 0
    option_rouge = 1
    option_omega = 2
    # noinspection PyClassVar
    default = 'random'  # type: ignore


class RoseSanity(Choice):
    """
    How many rings are needed for a sanity check?
    Requires Mission B and Rose ObjSanity to be enabled
    1 results in 2800 checks
    20 results in 140 checks
    """
    display_name = "Rose Sanity"
    #option_disabled = 0
    option_1 = 1
    option_5 = 5
    option_10 = 10
    option_20 = 20
    default = 20


class RoseStoryStartingCharacter(Choice):
    """
    If Ability and Character Unlocks are enabled, which Character should be unlocked for Rose Story from the Start?
    """
    display_name = "Rose Story Starting Character"
    option_amy = 0
    option_cream = 1
    option_big = 2
    # noinspection PyClassVar
    default = 'random'  # type: ignore



class ChaotixSanity(Choice):
    """
    Should Chaotix Sanity be enabled, and if so, how many rings are needed for a check on Casino Park? (All non-Casino Park levels are the same if enabled)
    Mission A only Check Count: 223 + 200 / value (if enabled)
    Mission B only Check Count: 266 + 500 / value (if enabled)
    Both Missions Check Count: 489 + 700 / value (if enabled)
    """
    display_name = "Chaotix Sanity"
    #option_disabled = 0
    option_1 = 1
    option_5 = 5
    option_10 = 10
    option_20 = 20
    default = 20


class ChaotixStoryStartingCharacter(Choice):
    """
    If Ability and Character Unlocks are enabled, which Character should be unlocked for Chaotix Story from the Start?
    """
    display_name = "Chaotix Story Starting Character"
    option_espio = 0
    option_charmy = 1
    option_vector = 2
    # noinspection PyClassVar
    default = 'random'  # type: ignore


class SuperHardModeStartingCharacter(Choice):
    """
    If Ability and Character Unlocks are enabled, which Character should be unlocked for Super Hard Mode from the Start?
    """
    display_name = "Super Hard Mode Starting Character"
    option_super_hard_sonic = 0
    option_super_hard_tails = 1
    option_super_hard_knuckles = 2
    # noinspection PyClassVar
    default = 'random'   # type: ignore


class SanityExcludedPercent(Range):
    """
    How much percent of sanity checks should be excluded (only have filler/trap items)?
    This does not affect Key or Checkpoint Sanity.
    This helps with large amounts of sanity checks having all of the progressive items in a sync.
    """
    display_name = "Sanity Excluded Percent"
    range_start = 0
    range_end = 100
    default = 80



class RemoveCasinoParkVIPTableLaserGate(DefaultOnToggle):
    """
    This Option will Remove the Laser Gate in front of the ramp before the VIP Table in Casino Park.
    This allows access to the Bonus Key there and the VIP table without having to get the switch on the pinball table before.
    """
    display_name = "Remove Casino Park VIP Table Laser Gate"


class RingLink(Toggle):
    """
    Ring Link
    """
    display_name = "Ring Link"


class RingLinkMetalOverlord(Toggle):
    """
    Should Ring Link be enabled on Metal Overlord?
    This requires Ring Link to be enabled to have any effect
    """
    display_name = "Ring Link on Metal Overlord"


class TrapFill(Range):
    """
    What percent of filler items should be replaced with trap items?
    """
    display_name = "Trap Fill"
    range_start = 0
    range_end = 100
    default = 0

class StealthTrapWeight(Range):
    """
    Determines the weight (not percent) for Stealth Trap.
    Traps must be enabled for this to have any effect.
    """
    display_name = "Stealth Trap Weight"
    range_start = 0
    range_end = 100
    default = 50

class FreezeTrapWeight(Range):
    """
    Determines the weight (not percent) for Freeze Trap.
    Traps must be enabled for this to have any effect.
    """
    display_name = "Freeze Trap Weight"
    range_start = 0
    range_end = 100
    default = 50

class NoSwapTrapWeight(Range):
    """
    Determines the weight (not percent) for No Swap Trap.
    Traps must be enabled for this to have any effect.
    """
    display_name = "No Swap Trap Weight"
    range_start = 0
    range_end = 100
    default = 50

class RingTrapWeight(Range):
    """
    Determines the weight (not percent) for Ring Trap.
    Traps must be enabled for this to have any effect.
    """
    display_name = "Ring Trap Weight"
    range_start = 0
    range_end = 100
    default = 50

class CharmyTrapWeight(Range):
    """
    Determines the weight (not percent) for Charmy Trap.
    Traps must be enabled for this to have any effect.
    """
    display_name = "Charmy Trap Weight"
    range_start = 0
    range_end = 100
    default = 50




sonic_heroes_option_groups = \
    [
        OptionGroup("Meta",
            [
                IncludedLevelsAndSanities,
                UnlockType,
                AbilityUnlocks,
                LegacyNumberOfLevelGates,
                LegacyLevelGatesAllowedBosses,
                RequiredRank,
            ]),
        OptionGroup("Goal",
            [
                FinalBoss,
                GoalUnlockConditions,
                GoalLevelCompletions,
                GoalLevelCompletionsPerStory,
            ]),
        OptionGroup("Team Sonic",
            [
                SonicStoryStartingCharacter,
            ]),
        OptionGroup("Team Dark",
            [
                DarkSanity,
                DarkStoryStartingCharacter,
            ]),
        OptionGroup("Team Rose",
            [
                RoseSanity,
                RoseStoryStartingCharacter,
            ]),
        OptionGroup("Team Chaotix",
            [
                ChaotixSanity,
                ChaotixStoryStartingCharacter,
            ]),
        OptionGroup("Team Super Hard Mode",
            [
                SuperHardModeStartingCharacter,
            ]),
        OptionGroup("Connection Tags",
            [
                #RingLink,
                #RingLinkMetalOverlord,
                #DeathLink,
            ]),
        OptionGroup("QOL",
            [
                RemoveCasinoParkVIPTableLaserGate,
            ]),
        OptionGroup("Traps",
            [
                TrapFill,
                StealthTrapWeight,
                FreezeTrapWeight,
                NoSwapTrapWeight,
                RingTrapWeight,
                CharmyTrapWeight,
            ]),
]


@dataclass
class SonicHeroesOptions(PerGameCommonOptions):

    #Main
    make_puml: MakePuml
    included_levels_and_sanities: IncludedLevelsAndSanities
    unlock_type: UnlockType
    ability_unlocks: AbilityUnlocks
    legacy_number_of_level_gates: LegacyNumberOfLevelGates
    legacy_level_gates_allowed_bosses: LegacyLevelGatesAllowedBosses
    required_rank: RequiredRank

    #Goal
    final_boss: FinalBoss
    goal_unlock_conditions: GoalUnlockConditions
    goal_level_completions: GoalLevelCompletions
    goal_level_completions_per_story: GoalLevelCompletionsPerStory

    #Sonic
    #sonic_story: SonicStory
    sonic_story_starting_character: SonicStoryStartingCharacter
    #sonic_key_sanity: SonicKeySanity
    #sonic_checkpoint_sanity: SonicCheckpointSanity

    #Dark
    #dark_story: DarkStory
    dark_sanity: DarkSanity
    dark_story_starting_character: DarkStoryStartingCharacter
    #dark_key_sanity: DarkKeySanity
    #dark_checkpoint_sanity: DarkCheckpointSanity

    #Rose
    #rose_story: RoseStory
    rose_sanity: RoseSanity
    rose_story_starting_character: RoseStoryStartingCharacter
    #rose_key_sanity: RoseKeySanity
    #rose_checkpoint_sanity: RoseCheckpointSanity

    #Chaotix
    #chaotix_story: ChaotixStory
    chaotix_sanity: ChaotixSanity
    chaotix_story_starting_character: ChaotixStoryStartingCharacter
    #chaotix_key_sanity: ChaotixKeySanity
    #chaotix_checkpoint_sanity: ChaotixCheckpointSanity

    #SuperHard
    #super_hard_mode: SuperHardMode
    super_hard_mode_starting_character: SuperHardModeStartingCharacter
    #super_hard_mode_checkpoint_sanity: SuperHardModeCheckpointSanity


    #Connection Tags
    #ring_link: RingLink
    #ring_link_metal_overlord: RingLinkMetalOverlord
    #death_link: DeathLink
    #traplink here (or in client)
    #taglink (swaplink) here (or in client)

    #QOL
    #bonus_keys_needed_for_bonus_or_emerald_stage: BonusKeysNeededForBonusOrEmeraldStage <- might add this later
    #dont_lose_bonus_key: DontLoseBonusKey <- doesn't exist anymore given spawn data changes
    #modern_ring_loss: ModernRingLoss
    remove_casino_park_vip_table_laser_gate: RemoveCasinoParkVIPTableLaserGate

    #Trap
    trap_fill: TrapFill
    stealth_trap_weight: StealthTrapWeight
    freeze_trap_weight: FreezeTrapWeight
    no_swap_trap_weight: NoSwapTrapWeight
    ring_trap_weight: RingTrapWeight
    charmy_trap_weight: CharmyTrapWeight


def check_invalid_options(world: SonicHeroesWorld):
    #for option in world.options.included_levels_and_sanities:
        #if option in features_in_rando_story_options:
            #has_story_enabled = True

    if DARKOBJSANITY in world.options.included_levels_and_sanities and not DARKACTB in world.options.included_levels_and_sanities:
        raise OptionError("Dark ObjSanity Requires Dark Act B")

    if ROSEOBJSANITY in world.options.included_levels_and_sanities and not ROSEACTB in world.options.included_levels_and_sanities:
        raise OptionError("Rose ObjSanity Requires Rose Act B")


    if SUPERHARDMODE in world.options.included_levels_and_sanities:
        if SONICACTB in world.options.included_levels_and_sanities:
            raise OptionError("Super Hard Mode and Sonic Act B cannot both be enabled.")

        temp_enabled_teams: int = 0
        for team in sonic_heroes_story_names.values():
            if team != SUPERHARDMODE:
                if world.is_this_team_enabled(team):
                    temp_enabled_teams += 1

        if temp_enabled_teams == 0:
            if EMERALDS in world.options.goal_unlock_conditions and not SUPERHARDCHECKPOINTSANITY in world.options.included_levels_and_sanities:
                raise OptionError("Super Hard Mode Only on the Legacy Level Gates option (with no Checkpoint Sanity) cannot have Emeralds placed as there is no access to the emerald stages.")



    temp_team: str = SONIC
    temp_sanity: str = KEYSANITY
    if SONICKEYSANITY1SET in world.options.goal_unlock_conditions and SONICKEYSANITYBOTHACTS in world.options.goal_unlock_conditions:
        temp_team = SONIC
        temp_sanity = KEYSANITY
        raise OptionError(f"Team {temp_team} has multiple enabled choices of this sanity: {temp_sanity}")

    if SONICCHECKPOINTSANITY1SET in world.options.goal_unlock_conditions and SONICCHECKPOINTSANITYBOTHACTS in world.options.goal_unlock_conditions:
        temp_team = SONIC
        temp_sanity = CHECKPOINTSANITY
        raise OptionError(f"Team {temp_team} has multiple enabled choices of this sanity: {temp_sanity}")

    if DARKKEYSANITY1SET in world.options.goal_unlock_conditions and DARKKEYSANITYBOTHACTS in world.options.goal_unlock_conditions:
        temp_team = DARK
        temp_sanity = KEYSANITY
        raise OptionError(f"Team {temp_team} has multiple enabled choices of this sanity: {temp_sanity}")

    if DARKCHECKPOINTSANITY1SET in world.options.goal_unlock_conditions and DARKCHECKPOINTSANITYBOTHACTS in world.options.goal_unlock_conditions:
        temp_team = DARK
        temp_sanity = CHECKPOINTSANITY
        raise OptionError(f"Team {temp_team} has multiple enabled choices of this sanity: {temp_sanity}")

    if ROSEKEYSANITY1SET in world.options.goal_unlock_conditions and ROSEKEYSANITYBOTHACTS in world.options.goal_unlock_conditions:
        temp_team = ROSE
        temp_sanity = KEYSANITY
        raise OptionError(f"Team {temp_team} has multiple enabled choices of this sanity: {temp_sanity}")

    if ROSECHECKPOINTSANITY1SET in world.options.goal_unlock_conditions and ROSECHECKPOINTSANITYBOTHACTS in world.options.goal_unlock_conditions:
        temp_team = ROSE
        temp_sanity = CHECKPOINTSANITY
        raise OptionError(f"Team {temp_team} has multiple enabled choices of this sanity: {temp_sanity}")

    if CHAOTIXKEYSANITY1SET in world.options.goal_unlock_conditions and CHAOTIXKEYSANITYBOTHACTS in world.options.goal_unlock_conditions:
        temp_team = CHAOTIX
        temp_sanity = KEYSANITY
        raise OptionError(f"Team {temp_team} has multiple enabled choices of this sanity: {temp_sanity}")

    if CHAOTIXCHECKPOINTSANITY1SET in world.options.goal_unlock_conditions and CHAOTIXCHECKPOINTSANITYBOTHACTS in world.options.goal_unlock_conditions:
        temp_team = CHAOTIX
        temp_sanity = CHECKPOINTSANITY
        raise OptionError(f"Team {temp_team} has multiple enabled choices of this sanity: {temp_sanity}")


    max_levels = 0

    for team in sonic_heroes_story_names.values():
        if world.is_this_team_enabled(team):
            max_levels += 14

            if not world.is_this_team_enabled(team, both_acts_required=True):
                if world.is_this_sanity_enabled(team, KEYSANITY, both_acts_required=True):
                    raise OptionError(f"Team {team} has {KEYSANITY} set to both acts with only 1 Act Enabled.")

                if world.is_this_sanity_enabled(team, CHECKPOINTSANITY, both_acts_required=True):
                    raise OptionError(f"Team {team} has {CHECKPOINTSANITY} set to both acts with only 1 Act Enabled.")

        else:
            #team not enabled
            if world.is_this_sanity_enabled(team, KEYSANITY) or world.is_this_sanity_enabled(team, CHECKPOINTSANITY) or world.is_this_sanity_enabled(team, OBJSANITY):
                raise OptionError(f"Team {team} has a Sanity option enabled while disabled.")

            if team != SONIC and team != SUPERHARDMODE:
                if world.is_this_sanity_enabled(team, OBJSANITY):
                    raise OptionError(f"Team {team} has a Sanity option enabled while disabled.")


    if max_levels == 0:
        raise OptionError("At least one Story must be enabled. You Goober.")


    world.options.goal_level_completions.value = min(world.options.goal_level_completions.value, max_levels)


    if world.options.unlock_type == UnlockType.option_ability_character_unlocks:
        world.options.required_rank.value = RequiredRank.option_rank_e

        if EMBLEMS in world.options.goal_unlock_conditions:
            raise OptionError("Emblems are not supported with Ability and Character Unlocks.")

        if world.options.accessibility == Accessibility.option_minimal:
            if not LEVELCOMPLETIONSALLTEAMS in world.options.goal_unlock_conditions or world.options.goal_level_completions.value == 0:
                if not LEVELCOMPLETIONSPERSTORY in world.options.goal_unlock_conditions or world.options.goal_level_completions_per_story.value == 0:  # type: ignore
                    raise OptionError("Minimal Accessibility (with Ability and Character Unlocks) requires at least 1 Level Completion or Level Completion per Story.")

        if world.is_this_team_enabled(DARK):
            raise OptionError("Ability and Character Unlocks currently does not support Team Dark.")
        if world.is_this_team_enabled(ROSE):
            raise OptionError("Ability and Character Unlocks currently does not support Team Rose.")
        if world.is_this_team_enabled(CHAOTIX):
            raise OptionError("Ability and Character Unlocks currently does not support Team Chaotix.")
        if world.is_this_team_enabled(SUPERHARDMODE):
            raise OptionError("Ability and Character Unlocks currently does not support Super Hard Mode.")


        if world.options.ability_unlocks == AbilityUnlocks.option_all_regions_separate:
            for team in sonic_heroes_story_names.values():
                if world.is_this_team_enabled(team):
                    if not world.is_this_team_enabled(team, both_acts_required=True):
                        if not world.is_this_sanity_enabled(team, KEYSANITY) or not world.is_this_sanity_enabled(team, CHECKPOINTSANITY):
                            raise OptionError(f"Region Based Ability Unlocks with only 1 Act Requires "
                                      f"Both Key Sanity and Checkpoint Sanity for team {team}.")
                    else:
                        if not world.is_this_sanity_enabled(team, KEYSANITY) or not world.is_this_sanity_enabled(team, CHECKPOINTSANITY):
                            raise OptionError(f"Region Based Ability Unlocks with both acts Requires "
                                              f"either Both Key Sanity and Checkpoint Sanity or one of "
                                              f"those with both sets (Set For Each Act) for team {team}.")

                        if not world.is_this_sanity_enabled(team, KEYSANITY, both_acts_required=True) and not world.is_this_sanity_enabled(team, CHECKPOINTSANITY, both_acts_required=True):
                            raise OptionError(f"Region Based Ability Unlocks with both acts Requires "
                                              f"either Both Key Sanity and Checkpoint Sanity or one of "
                                              f"those with both sets (Set For Each Act) for team {team}.")



        else:   #entire story ability unlocks
            for team in sonic_heroes_story_names.values():
                if world.is_this_team_enabled(team):
                    if not world.is_this_sanity_enabled(team, KEYSANITY) or not world.is_this_sanity_enabled(team, CHECKPOINTSANITY):
                        raise OptionError(f"Entire Story Ability Unlocks Requires Either Key Sanity "
                                          f"or Checkpoint Sanity To Be Enabled")


    elif world.options.unlock_type == UnlockType.option_legacy_level_gates:
        if world.options.legacy_number_of_level_gates > len(world.options.legacy_level_gates_allowed_bosses.value):
            raise OptionError("The Number of Level Gates is larger than the number of Bosses Allowed.")