from BaseClasses import PlandoOptions
from Options import (
    Choice,
    DefaultOnToggle,
    FreeText,
    NamedRange,
    NumericOption,
    Option,
    OptionGroup,
    OptionSet,
    PerGameCommonOptions,
    Range,
    TextChoice,
    Toggle,
    Visibility,
)
from Utils import get_fuzzy_results
from worlds.AutoWorld import World

# These helper methods allow you to determine if an option has been set, or what its value is, for any player in the multiworld
from ..Helpers import get_option_value, is_option_enabled


class OceanFishing(Toggle):
    """
    Ocean Fishing departs once every two real-world hours on a specified route.
    There are six total routes, four in Eorzea, two in the East.  They do not loop evenly, you may see duplicates before you see all six.
    This means it will take at least 12 hours to complete all the relevant checks.
    This option is absolutely not sync-viable.
    """
    display_name = "Enable Ocean Fishing"
    default = False

class Fatesanity(Toggle):
    """
    Include individual FATEs in the location pool.

    If enabled, each named FATE is a check.  If disabled, you only need to complete 5 FATEs of your choice per zone.
    """
    display_name = "Fatesanity"
    default = False

class UnreasonableFates(Toggle):
    """
    Include World Bosses and other FATEs that are not reasonable to complete.

    These fates often spawn once every 2-3 days, don't show up on the map, and can require a large number of players to defeat.
    If you use this option, keep an eye on Faloop (or your DC's equivalent) to know when they're up.
    """
    display_name = "Include Unreasonable FATEs"
    default = False

class DutyDifficulty(Choice):
    """
    Maximum difficulty of the duty content.
    [normal] Dungeons, trials, normal raids, and alliance raids are included in the location pool.
    [extreme] As above, but extreme trials are included in the location pool.
    [savage] As above, but old savage raids are included in the location pool.
    [endgame] As above, but the current savage tier is included in the location pool.
    """
    default = 1
    display_name = "Duty Difficulty"
    option_no_duties = 0
    option_normal = 1
    option_extreme = 2
    option_savage = 3
    option_endgame = 4

class MaxPartySize(Choice):
    """
    Maximum party size for duty content.

    This does not stop you from entering undersized, but simply prevents duties that would expect more players from being in the location pool.
    """
    default = 2
    display_name = "Max Party Size"
    option_solo = 0
    option_light_party = 1
    option_full_party = 2
    option_alliance = 3

class IncludeDungeons(DefaultOnToggle):
    """
    Dungeons are generally longer than other locations. You may want to exclude them in a sync.
    """

class ExtraDungeonChecks(Range):
    """
    Number of checks per dungeon to include in the location pool.

    Each dungeon has a base of 1 check.  This option adds additional checks to each dungeon.

    These can be sent when you open chests, defeat minibosses, or just all at the end.
    """
    display_name = "Extra Dungeons"
    default = 0
    range_start = 0
    range_end = 10


class DungeonCount(Range):
    """
    Number of Dungeons per expansion to include in the location pool
    """
    display_name = "Dungeon Count"
    default = 31
    range_start = 0
    range_end = 31

class VariantDungeonCount(Range):
    """
    Number of Variant Dungeons per expansion to include in the location pool
    """
    display_name = "Dungeon Count"
    default = 3
    range_start = 0
    range_end = 3

class TrialCount(Range):
    """
    Number of Trials per expansion to include in the location pool
    """
    display_name = "Trial Count"
    default = 18
    range_start = 0
    range_end = 18

class ExtremeTrialCount(Range):
    """
    Number of Extreme Trials per expansion to include in the location pool
    """
    display_name = "Extreme Trial Count"
    default = 8
    range_start = 0
    range_end = 8

class EndgameTrialCount(Range):
    """
    Number of Current Extreme Trials to include in the location pool
    """
    display_name = "Extreme Trial Count"
    default = 8
    range_start = 0
    range_end = 8

class AllianceRaidCount(Range):
    """
    Number of Alliance Raids per expansion to include in the location pool
    """
    display_name = "Alliance Raid Count"
    default = 3
    range_start = 0
    range_end = 3

class NormalRaidCount(Range):
    """
    Number of Normal Raids per expansion to include in the location pool
    """
    display_name = "Normal Raid Count"
    default = 12
    range_start = 0
    range_end = 12

class SavageRaidCount(Range):
    """
    Number of Savage Raids per expansion to include in the location pool
    """
    display_name = "Savage Raid Count"
    default = 17
    range_start = 0
    range_end = 17

class EndgameRaidCount(Range):
    """
    Number of Endgame Savage Raids to include in the location pool
    """
    display_name = "Savage Raid Count"
    default = 12
    range_start = 0
    range_end = 12

class UltimateCount(Range):
    """
    Number of Ultimate Raids to include in the location pool
    """
    display_name = "Ultimate Raid Count"
    default = 10
    range_start = 0
    range_end = 10

class McGuffinsNeeded(Range):
    """
    Number of Distant Memories needed to win the game.
    """
    display_name = "McGuffins Needed"
    default = 30
    range_start = 1
    range_end = 50

class ForceJob(OptionSet):
    """
    Choose which classes are progression.

    If none are selected, five (one tank, one healer, one melee, one phys range, one caster) are chosen at random.
    """
    display_name = "Force Progression Jobs"

    def verify(self, world: type[World], player_name: str, plando_options: PlandoOptions) -> None:
        from .Data import TANKS, HEALERS, MELEE, CASTER, RANGED, DOH, DOL
        all = TANKS + HEALERS + MELEE + CASTER + RANGED + DOH + DOL
        print(f"{repr(self.value)}/{repr(all)}")
        for item_name in self.value:
            if item_name not in all:
                picks = get_fuzzy_results(item_name, all, limit=1)
                raise Exception(f"Item {item_name} from option {self} "
                                f"is not a valid job from {world.game}. "
                                f"Did you mean '{picks[0][0]}' ({picks[0][1]}% sure)")


        return super().verify(world, player_name, plando_options)

class LevelCap(Range):
    """
    Maximum level of the player.
    """
    display_name = "Level Cap"
    default = 100
    range_start = 30
    range_end = 100

class AllowMainScenario(DefaultOnToggle):
    """
    Include Castrum Meridianum, Praetorium, and The Porta Decumana in the location pool.
    These duties are long and contain unskippable cutscenes.
    """

class Fishsanity(Choice):
    """
    Include individual fish in the location pool.

    Each tier of fish includes the previous tiers.  For example, if you select "timed fish", you will also get "normal fish".
    Big fish includes things like the "Ruby Dragon" and "Python Discus", which can be unavailable for weeks at a time.
    """
    option_disabled = 0
    option_normal_fish = 1
    option_timed_fish = 2
    option_big_fish = 3
    default = 0

class IncludePvP(Toggle):
    """
    Include PvP duties in the location pool.
    """

class IncludeBozja(Toggle):
    """
    Include Save the Queen content in the location pool.  This includes the Fates, Trials and Alliance Raids of the Bozjan Southern Front, Delubrum Reginae and Zadnor.
    """

class FatesPerZone(Range):
    """
    Number of FATEs required per zone.  Does not apply if Fatesanity is enabled.
    """
    display_name = "FATEs Per Zone"
    default = 5
    range_start = 0
    range_end = 10


# This is called before any manual options are defined, in case you want to define your own with a clean slate or let Manual define over them
def before_options_defined(options: dict) -> dict:
    # Goal
    options["mcguffins_needed"] = McGuffinsNeeded
    # Duties
    options["duty_difficulty"] = DutyDifficulty
    options["max_party_size"] = MaxPartySize
    options["include_dungeons"] = IncludeDungeons
    options["allow_main_scenario_duties"] = AllowMainScenario
    options["extra_dungeon_checks"] = ExtraDungeonChecks
    options["include_ocean_fishing"] = OceanFishing
    options["include_pvp"] = IncludePvP
    # options["include_bozja"] = IncludeBozja

    # Duty Counts
    options["dungeon_count"] = DungeonCount
    options["variant_dungeon_count"] = VariantDungeonCount
    options["trial_count"] = TrialCount
    options["extreme_trial_count"] = ExtremeTrialCount
    options["endgame_trial_count"] = EndgameTrialCount
    options["alliance_raid_count"] = AllianceRaidCount
    options["normal_raid_count"] = NormalRaidCount
    options["savage_raid_count"] = SavageRaidCount
    options["endgame_raid_count"] = EndgameRaidCount
    options["ultimate_count"] = UltimateCount

    # Fates
    options["fatesanity"] = Fatesanity
    options["include_unreasonable_fates"] = UnreasonableFates
    options["fates_per_zone"] = FatesPerZone
    # Fish
    options["fishsanity"] = Fishsanity
    # Jobs
    options["force_jobs"] = ForceJob
    options["level_cap"] = LevelCap
    return options

# This is called after any manual options are defined, in case you want to see what options are defined or want to modify the defined options
def after_options_defined(options: type[PerGameCommonOptions]) -> None:
    # To access a modifiable version of options check the dict in options.type_hints
    # For example if you want to change DLC_enabled's display name you would do:
    # options.type_hints["DLC_enabled"].display_name = "New Display Name"

    #  Here's an example on how to add your aliases to the generated goal
    # options.type_hints['goal'].aliases.update({"example": 0, "second_alias": 1})
    # options.type_hints['goal'].options.update({"example": 0, "second_alias": 1})  #for an alias to be valid it must also be in options

    pass

# Use this Hook if you want to add your Option to an Option group (existing or not)
def before_option_groups_created(groups: dict[str, list[Option]]) -> dict[str, list[Option]]:
    # Uses the format groups['GroupName'] = [TotalCharactersToWinWith]
    return groups

def after_option_groups_created(groups: list[OptionGroup]) -> list[OptionGroup]:
    return groups
