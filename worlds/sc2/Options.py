from typing import Dict, FrozenSet, Union, Set
from BaseClasses import MultiWorld
from Options import Choice, Option, Toggle, DefaultOnToggle, ItemSet, OptionSet, Range
from .MissionTables import SC2Campaign, SC2Mission


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

class DisableForcedCamera(Toggle):
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
    """Determines what version of All-In (final map) that will be generated for the campaign."""
    display_name = "All In Map"
    option_ground = 0
    option_air = 1


class MissionOrder(Choice):
    """
    Determines the order the missions are played in.  The last three mission orders end in a random mission.
    Vanilla (29): Keeps the standard mission order and branching from the WoL Campaign.
    Vanilla Shuffled (29): Keeps same branching paths from the WoL Campaign but randomizes the order of missions within.
    Mini Campaign (15): Shorter version of the campaign with randomized missions and optional branches.
    Medium Grid (16):  A 4x4 grid of random missions.  Start at the top-left and forge a path towards bottom-right mission to win.
    Mini Grid (9):  A 3x3 version of Grid.  Complete the bottom-right mission to win.
    Blitz (12):  12 random missions that open up very quickly.  Complete the bottom-right mission to win.
    Gauntlet (7): Linear series of 7 random missions to complete the campaign.
    Mini Gauntlet (4): Linear series of 4 random missions to complete the campaign.
    Tiny Grid (4): A 2x2 version of Grid.  Complete the bottom-right mission to win.
    Grid (variable): A grid that will resize to use all non-excluded missions.  Corners may be omitted to make the grid more square.  Complete the bottom-right mission to win.
    """
    display_name = "Mission Order"
    option_vanilla = 0
    option_vanilla_shuffled = 1
    option_mini_campaign = 2
    option_medium_grid = 3
    option_mini_grid = 4
    option_blitz = 5
    option_gauntlet = 6
    option_mini_gauntlet = 7
    option_tiny_grid = 8
    option_grid = 9


class MaximumCampaignSize(Range):
    """
    Sets an upper bound on how many missions to include when a variable-size mission order is selected.
    If a set-size mission order is selected, does nothing.
    """
    display_name = "Maximum Campaign Size"
    range_start = 1
    range_end = 74
    default = 74


class GridTwoStartPositions(Toggle):
    """
    If turned on and 'grid' mission order is selected, removes a mission from the starting
    corner sets the adjacent two missions as the starter missions.
    """
    display_name = "Start with two unlocked missions on grid"
    default = Toggle.option_false


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
    option_default = 17
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
    """
    display_name = "Enable Epilogue missions"


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
    range_end = 100
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
    resulting in 18 total upgrade items for Terran and 15 total items for Zerg.
    Bundle Weapon And Armor:  All types of weapon upgrades are one item per race,
    and all types of armor upgrades are one item per race,
    resulting in 12 total items.
    Bundle Unit Class:  Weapon and armor upgrades are merged,
    but upgrades are bundled separately for each race:
    Infantry, Vehicle, and Starship upgrades for Terran (9 items),
    Ground and Flyer upgrades for Zerg (6 items),
    resulting in 15 total items.
    Bundle All:  All weapon and armor upgrades are one item per race,
    resulting in 6 total items."""
    display_name = "Generic Upgrade Items"
    option_individual_items = 0
    option_bundle_weapon_and_armor = 1
    option_bundle_unit_class = 2
    option_bundle_all = 3


class NovaCovertOpsItems(Toggle):
    """If turned on, the equipment upgrades from Nova Covert Ops may be present in the world."""
    display_name = "Nova Covert Ops Items"
    default = Toggle.option_true


class BroodWarItems(Toggle):
    """If turned on, returning items from StarCraft: Brood War may appear in the world."""
    display_name = "Brood War Items"
    default = Toggle.option_true


class ExtendedItems(Toggle):
    """If turned on, original items that did not appear in Campaign mode may appear in the world."""
    display_name = "Extended Items"
    default = Toggle.option_true


# Current maximum number of upgrades for a unit
MAX_UPGRADES_OPTION = 12


class EnsureGenericItems(Range):
    """
    Specifies a minimum percentage of the generic item pool that will be present for the slot.
    The generic item pool is the pool of all generically useful items after all exclusions.
    Generically-useful items include: Worker upgrades, Building upgrades, economy upgrades,
    Mercenaries, Kerrigan levels and abilities, and Spear of Adun abilities
    Increasing this percentage will make units less common.
    """
    range_start = 0
    range_end = 100
    default = 25


class MinNumberOfUpgrades(Range):
    """
    Set a minimum to the number of upgrades a unit/structure can have.
    Note that most units have 4 or 6 upgrades.
    If a unit has fewer upgrades than the minimum, it will have all of its upgrades.
    """
    display_name = "Minimum number of upgrades per unit/structure"
    range_start = 0
    range_end = MAX_UPGRADES_OPTION
    default = 2


class MaxNumberOfUpgrades(Range):
    """
    Set a maximum to the number of upgrades a unit/structure can have. -1 is used to define unlimited.
    Note that most unit have 4 or 6 upgrades.
    """
    display_name = "Maximum number of upgrades per unit/structure"
    range_start = -1
    range_end = MAX_UPGRADES_OPTION
    default = -1



class IncludeMutations(Range):
    """Determines how many of the 3 mutations for the 7 units that have them can appear."""
    display_name = "Include Mutations"
    range_start = 0
    range_end = 3
    default = 1


class IncludeStrains(Range):
    """Determines how many of the 2 strains for the 7 units that have them can appear."""
    display_name = "Include Strains"
    range_start = 0
    range_end = 2
    default = 1


class KerriganPresence(Choice):
    """
    Determines whether Kerrigan is playable outside of missions that require her.

    Vanilla: Kerrigan is playable as normal, appears in the same missions as in vanilla game.
    Not Present:  Kerrigan is not playable, unless the mission requires her to be present.  Other hero units stay playable,
        and locations normally requiring Kerrigan can be checked by any unit.
        Kerrigan level items, active abilities and passive abilities affecting her will not appear.
        In missions where the Kerrigan unit is required, story abilities are given in same way as Grant Story Tech is set to true
    Not Present And No Passives:  In addition to the above, Kerrigan's passive abilities affecting other units (such as Twin Drones) will not appear.
    """
    display_name = "Kerrigan Presence"
    option_vanilla = 0
    option_not_present = 1
    option_not_present_and_no_passives = 2


class KerriganChecksPerLevelPack(Range):
    """Determines how many locations need to be checked for a level pack to be received.  Missions have between 4 and 5 locations each."""
    display_name = "Checks Per Kerrigan Level Pack"
    range_start = 1
    range_end = 10
    default = 1


class KerriganCheckLevelPackSize(Range):
    """Determines how many levels Kerrigan gains when enough locations are checked."""
    display_name = "Check Level Pack Size"
    range_start = 0
    range_end = 5
    default = 0


class KerriganLevelItemSum(Range):
    """Determines the sum of the level items in the world.  This does not affect levels gained from checks."""
    display_name = "Kerrigan Level Item Sum"
    range_start = 0
    range_end = 140
    default = 70


class KerriganLevelItemDistribution(Choice):
    """Determines the amount and size of Kerrigan level items.

    Vanilla:  Uses the distribution in the vanilla campaign.
    This entails 32 individual levels and 6 packs of varying sizes.
    This distribution always adds up to 70, ignoring the Level Item Sum setting.
    Smooth:  Uses a custom, condensed distribution of items between sizes 4 and 10,
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


class IncludeAllKerriganAbilities(DefaultOnToggle):
    """If turned on, all abilities from every Kerrigan ability tier will be able to appear.
    If turned off, one random passive or active ability per tier will be included."""
    display_name = "Include All Kerrigan Abilities"


class StartPrimaryAbilities(Range):
    """Number of Primary Abilities (Kerrigan Tier 1, 2, and 4) to start the game with.
    If set to 4, a Tier 7 ability is also included."""
    display_name = "Starting Primary Abilities"
    range_start = 0
    range_end = 4
    default = 0


class KerriganPrimalStatus(Choice):
    """Determines when Kerrigan appears in her Primal Zerg form.
    This halves her maximum energy, but greatly increases her energy regeneration.

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


class SpearOfAdunPresence(Choice):
    """
    Determines in which missions Spear of Adun calldowns will be available.
    Affects only abilities used from Spear of Adun top menu.

    Not Present: Spear of Adun calldowns are unavailable.
    LotV Protoss: Spear of Adun calldowns are only available in LotV main campaign
    Protoss: Spear od Adun calldowns are available in any Protoss mission
    Everywhere: Spear od Adun calldowns are available in any mission of any race
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
    Protoss: Spear od Adun autocasts are available in any Protoss mission
    Everywhere: Spear od Adun autocasts are available in any mission of any race
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


class TakeOverAIAllies(Toggle):
    """
    On maps supporting this feature allows you to take control over an AI Ally.
    """
    display_name = "Take Over AI Allies"


class LockedItems(ItemSet):
    """Guarantees that these items will be unlockable"""
    display_name = "Locked Items"


class ExcludedItems(ItemSet):
    """Guarantees that these items will not be unlockable"""
    display_name = "Excluded Items"


class ExcludedMissions(OptionSet):
    """Guarantees that these missions will not appear in the campaign
    Doesn't apply to vanilla mission order.
    It may be impossible to build a valid campaign if too many missions are excluded."""
    display_name = "Excluded Missions"
    valid_keys = {mission.mission_name for mission in SC2Mission}


class LocationInclusion(Choice):
    option_enabled = 0
    option_resources = 1
    option_disabled = 2


class MissionProgressLocations(LocationInclusion):
    """
    Enables or disables item rewards for progressing (not finishing) a mission.
    Progressing a mission is usually a task of completing or progressing into a main objective.
    Clearing an expansion base also counts here.

    Enabled: All locations fitting into this do their normal rewards
    Resources: Forces these locations to contain Starting Resources
    Disabled: Removes item rewards from these locations.

    Note: Individual locations subject to plando are always enabled, so the plando can be placed properly.
    See also: Excluded Locations, Item Plando (https://archipelago.gg/tutorial/Archipelago/plando/en#item-plando)
    """
    display_name = "Mission Progress Locations"


class BonusLocations(LocationInclusion):
    """
    Enables or disables item rewards for completing bonus tasks.
    Bonus tasks are those giving you a campaign-wide or mission-wide bonus in vanilla game:
    Research, credits, bonus units or resources, etc.

    Enabled: All locations fitting into this do their normal rewards
    Resources: Forces these locations to contain Starting Resources
    Disabled: Removes item rewards from these locations.

    Note: Individual locations subject to plando are always enabled, so the plando can be placed properly.
    See also: Excluded Locations, Item Plando (https://archipelago.gg/tutorial/Archipelago/plando/en#item-plando)
    """
    display_name = "Bonus Locations"


class ChallengeLocations(LocationInclusion):
    """
    Enables or disables item rewards for completing challenge tasks.
    Challenges are tasks that have usually higher requirements to be completed
    than to complete the mission they're in successfully.
    You might be required to visit the same mission later when getting stronger in order to finish these tasks.

    Enabled: All locations fitting into this do their normal rewards
    Resources: Forces these locations to contain Starting Resources
    Disabled: Removes item rewards from these locations.

    Note: Individual locations subject to plando are always enabled, so the plando can be placed properly.
    See also: Excluded Locations, Item Plando (https://archipelago.gg/tutorial/Archipelago/plando/en#item-plando)
    """
    display_name = "Challenge Locations"


class OptionalBossLocations(LocationInclusion):
    """
    Enables or disables item rewards for defeating optional bosses.
    An optional boss is any boss that's not required to kill in order to finish the mission successfully.
    All Brutalisks, Loki, etc. belongs here.

    Enabled: All locations fitting into this do their normal rewards
    Resources: Forces these locations to contain Starting Resources
    Disabled: Removes item rewards from these locations.

    Note: Individual locations subject to plando are always enabled, so the plando can be placed properly.
    See also: Excluded Locations, Item Plando (https://archipelago.gg/tutorial/Archipelago/plando/en#item-plando)
    """
    display_name = "Optional Boss Locations"


# noinspection PyTypeChecker
sc2_options: Dict[str, Option] = {
    "game_difficulty": GameDifficulty,
    "game_speed": GameSpeed,
    "disable_forced_camera": DisableForcedCamera,
    "skip_cutscenes": SkipCutscenes,
    "all_in_map": AllInMap,
    "mission_order": MissionOrder,
    "maximum_campaign_size": MaximumCampaignSize,
    "grid_two_start_positions": GridTwoStartPositions,
    "player_color_terran_raynor": PlayerColorTerranRaynor,
    "player_color_protoss": PlayerColorProtoss,
    "player_color_zerg": PlayerColorZerg,
    "player_color_zerg_primal": PlayerColorZergPrimal,
    "enable_wol_missions": EnableWolMissions,
    "enable_prophecy_missions": EnableProphecyMissions,
    "enable_hots_missions": EnableHotsMissions,
    "enable_lotv_prologue_missions": EnableLotVPrologueMissions,
    "enable_lotv_missions": EnableLotVMissions,
    "enable_epilogue_missions": EnableEpilogueMissions,
    "shuffle_campaigns": ShuffleCampaigns,
    "shuffle_no_build": ShuffleNoBuild,
    "starter_unit": StarterUnit,
    "required_tactics": RequiredTactics,
    "ensure_generic_items": EnsureGenericItems,
    "min_number_of_upgrades": MinNumberOfUpgrades,
    "max_number_of_upgrades": MaxNumberOfUpgrades,
    "generic_upgrade_missions": GenericUpgradeMissions,
    "generic_upgrade_research": GenericUpgradeResearch,
    "generic_upgrade_items": GenericUpgradeItems,
    "include_mutations": IncludeMutations,
    "include_strains": IncludeStrains,
    "kerrigan_presence": KerriganPresence,
    "kerrigan_checks_per_level_pack": KerriganChecksPerLevelPack,
    "kerrigan_check_level_pack_size": KerriganCheckLevelPackSize,
    "kerrigan_level_item_sum": KerriganLevelItemSum,
    "kerrigan_level_item_distribution": KerriganLevelItemDistribution,
    "include_all_kerrigan_abilities": IncludeAllKerriganAbilities,
    "start_primary_abilities": StartPrimaryAbilities,
    "kerrigan_primal_status": KerriganPrimalStatus,
    "spear_of_adun_presence": SpearOfAdunPresence,
    "spear_of_adun_present_in_no_build": SpearOfAdunPresentInNoBuild,
    "spear_of_adun_autonomously_cast_ability_presence": SpearOfAdunAutonomouslyCastAbilityPresence,
    "spear_of_adun_autonomously_cast_present_in_no_build": SpearOfAdunAutonomouslyCastPresentInNoBuild,
    "grant_story_tech": GrantStoryTech,
    "take_over_ai_allies": TakeOverAIAllies,
    "locked_items": LockedItems,
    "excluded_items": ExcludedItems,
    "excluded_missions": ExcludedMissions,
    "nco_items": NovaCovertOpsItems,
    "bw_items": BroodWarItems,
    "ext_items": ExtendedItems,
    "mission_progress_locations": MissionProgressLocations,
    "bonus_locations": BonusLocations,
    "challenge_locations": ChallengeLocations,
    "optional_boss_locations": OptionalBossLocations
}


def get_option_value(multiworld: MultiWorld, player: int, name: str) -> Union[int,  FrozenSet]:
    if multiworld is None:
        return sc2_options[name].default

    player_option = getattr(multiworld, name)[player]

    return player_option.value


def get_enabled_campaigns(multiworld: MultiWorld, player: int) -> Set[SC2Campaign]:
    enabled_campaigns = set()
    if get_option_value(multiworld, player, "enable_wol_missions"):
        enabled_campaigns.add(SC2Campaign.WOL)
    if get_option_value(multiworld, player, "enable_prophecy_missions"):
        enabled_campaigns.add(SC2Campaign.PROPHECY)
    if get_option_value(multiworld, player, "enable_hots_missions"):
        enabled_campaigns.add(SC2Campaign.HOTS)
    if get_option_value(multiworld, player, "enable_lotv_prologue_missions"):
        enabled_campaigns.add(SC2Campaign.PROLOGUE)
    if get_option_value(multiworld, player, "enable_lotv_missions"):
        enabled_campaigns.add(SC2Campaign.LOTV)
    if get_option_value(multiworld, player, "enable_epilogue_missions"):
        enabled_campaigns.add(SC2Campaign.EPILOGUE)
    return enabled_campaigns


def get_disabled_campaigns(multiworld: MultiWorld, player: int) -> Set[SC2Campaign]:
    all_campaigns = set(SC2Campaign)
    enabled_campaigns = get_enabled_campaigns(multiworld, player)
    disabled_campaigns = all_campaigns.difference(enabled_campaigns)
    disabled_campaigns.remove(SC2Campaign.GLOBAL)
    return disabled_campaigns


campaign_depending_orders = [
    MissionOrder.option_vanilla,
    MissionOrder.option_vanilla_shuffled,
    MissionOrder.option_mini_campaign
]

kerrigan_unit_available = [
    KerriganPresence.option_vanilla,
]