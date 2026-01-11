from dataclasses import dataclass
from typing import Dict, Any, TYPE_CHECKING

from Options import DefaultOnToggle, Toggle, StartInventoryPool, Choice, Range, TextChoice, PlandoConnections, \
                     PerGameCommonOptions, OptionGroup, Removed, Visibility, NamedRange
if TYPE_CHECKING:
    from . import FF1pixelWorld


class ShuffleGearShops(DefaultOnToggle):
    """
    Shuffle the content of all Weapon Shops together, and do the same for Armor Shops.
    """
    internal_name = "shuffle_gear_shops"
    display_name = "Shuffle Gear Shops"

class ShuffleSpells(DefaultOnToggle):
    """
    Shuffle Spells amongst their own School.
    """
    internal_name = "shuffle_spells"
    display_name = "Shuffle Spells"

class JobPromotion(Choice):
    """
    Set how Promotion Jobs are handled.

    Bahamut: Giving the Rat's Tail to Bahamut promote all Characters.

    Promote All Item: A Promote All Item is added to the Item Pool, when found all Characters promote.
    Bahamut becomes a Location.

    Job Item: All six Promotion Jobs become an individual Item added to the Item Pool.
    When acquired, all characters of the corresponding base Job promote. Bahamut becomes a Location.
    """
    internal_name = "job_promotion"
    display_name = "Job Promotion"
    option_bahamut = 0
    option_promote_all_item = 1
    option_job_item = 2
    default = 0

class LuteTablatures(NamedRange):
    """
    Playing the Lute requires a fixed number of Tablatures; 40 are shuffled in the Item Pool.
    This sets the number required to play the Lute and open the path in the Temple of Fiends.
    Set to 0 to disable this feature.
    If the required number is higher than 0, the Lute is in your starting inventory.
    The Item description will reveal the required number.
    """
    internal_name = "lute_tablatures"
    display_name = "Lute Tablatures"
    range_start = 0
    range_end = 40
    default = 0
    special_range_names = {
        "disable": 0,
        "low_count": 16,
        "mid_count": 24,
        "high_count": 32,
    }

class CrystalsRequired(Range):
    """
    Set the number of Crystals that must be restored so the Black Orb can be destroyed.
    Talking to the Black Orb will reveal the required number.
    """
    internal_name = "crystals_required"
    display_name = "Crystals Required"
    range_start = 0
    range_end = 4
    default = 4


class ShuffleTrialsMaze(DefaultOnToggle):
    """
    Shuffle the Pillars Maze on floor 2F of the Citadel of Trials.
    """
    internal_name = "shuffle_trials_maze"
    display_name = "Shuffle Trials' Maze"

class ShuffleOverworld(Toggle):
    """
    Shuffle all Overworld entrances, except the Towns.

    NOTE: The Princess won't teleport you to Cornelia Castle when this is enabled.
    """
    internal_name = "shuffle_overworld"
    display_name = "Shuffle Overworld"
    default = False

class ShuffleEntrances(Choice):
    """
    Shuffle all non-Overworld entrances.

    No Shuffle: Entrances stay the same.
    Dungeon Internal: Only shuffle the Dungeons' entrances, and keep them inside their respective dungeon.
    Dungeon Mixed: Only shuffle the Dungeons' entrances amongst all dungeons.
    All: Shuffle all locations' entrances except Towns.
    """
    internal_name = "shuffle_entrances"
    display_name = "Shuffle Entrances"
    option_no_shuffle = 0
    option_dungeon_internal = 1
    option_dungeon_mixed = 2
    option_all = 3
    default = 0

class ShuffleTowns(Choice):
    """
    Shuffle all Town entrances, except Cornelia; if Early Progression is set to Bikke's Ship, Pravoka is also excluded.
    No Shuffle: Entrances stay the same.
    Between Towns: Towns are shuffled only amongst themselves.
    Shallow Shuffle: If Overworld or Entrances are shuffled, Towns will be included with them, but will always be
    on the first floor of any location.
    Deep Shuffle: If Overworld or Entrances are shuffled, Towns will be included with them and can end up
    at any floor inside a location.
    """
    internal_name = "shuffle_towns"
    display_name = "Shuffle Towns"
    option_no_shuffle = 0
    option_shuffle_between_towns = 1
    option_mixed_shuffle_shallow = 2
    option_mixed_shuffle_deep = 3
    default = 0

class EarlyProgression(Choice):
    """
    Set how the world is opened at the start of the game.

    Bikke's Ship: The Bridge is built from the start and Bikke will always give the Ship.

    Marsh Cave Path: Open a path to the West of Cornelia that allows you to reach the Marsh Cave area by foot.
    The Bridge is never built. The Ship is shuffled with other items and Bikke is a Location.
    """
    internal_name = "early_progression"
    display_name = "Early Progression"
    option_bikke_ship = 0
    option_marsh_cave_path = 1
    default = 0

class NorthernDocks(Toggle):
    """
    Add docks to the Onrac Continent and the Mirage Desert Continent to make them accessible by Ship.
    """
    internal_name = "northern_docks"
    display_name = "Northern Docks"
    default = False

class NerfChaos(DefaultOnToggle):
    """
    Halve Chaos' HP and reduce his Intelligence and Attack Power by 25%.
    """
    internal_name = "nerf_chaos"
    display_name = "Nerf Chaos"

class BossMinions(Choice):
    """
    Add Minions to Bosses and Extend some Minibosses party.
    None: Original Parties are maintained.
    Weak Minions: Add relatively weak minions to Bosses and extend Minibosses by 1-2 members.
    Strong Minions: Add relatively strong minions to Bosses and extend Minibosses by 2-3 members.
    Weak-Strong Minions: Minions can be weak or strong.
    """
    internal_name = "boss_minions"
    display_name = "Boss Minions"
    option_none = 0
    option_weak_minions = 1
    option_strong_minions = 2
    option_weak_strong_minions = 3
    default = 0

class MonsterParties(Choice):
    """
    Randomize Monster Parties.
    Standard: Original Monster Parties are maintained.
    No Variance: Monsters will be replaced by Monsters of roughly the same power.
    Low Variance: Monsters can be replaced by slightly weaker or slightly stronger Monsters.
    High Variance: Monsters can be replaced by much weaker or much stronger Monsters.
    """
    internal_name = "monster_parties"
    display_name = "Monster Parties"
    option_standard = 0
    option_random_no_variance = 1
    option_random_low_variance = 2
    option_random_high_variance = 3
    default = 1

class MonstersCap(Choice):
    """
    If Monster Parties are randomized, bound Power Variance.
    This option doesn't do anything for Standard and No Variance choices.
    None: Variance is unbounded, Randomized Monster Parties can be weaker or stronger.
    Upper Bound: Randomized Monsters cannot be more powerful than the replaced Monsters, but they can be weaker.
    Lower Bound: Randomized Monsters cannot be weaker than the replaced Monsters, but they can be more powerful.
    """
    internal_name = "monsters_cap"
    display_name = "Variance Cap"
    option_none = 0
    option_upper_bound = 1
    option_lower_bound = 2
    default = 0

class DungeonEncounterRate(Choice):
    """
    Modify the Encounter Rate in dungeons by the multiplier selected.
    NOTE: This option doesn't affect the Boost setting to disable/enable encounters.
    """
    internal_name = "dungeon_encounter_rate"
    display_name = "Dungeon Encounter Rate"
    option_0_00x = 0
    option_0_25x = 1
    option_0_50x = 2
    option_0_75x = 3
    option_1_00x = 4
    option_1_25x = 5
    option_1_50x = 6
    default = 3

class OverworldEncounterRate(Choice):
    """
    Modify the Encounter Rate on the Overworld by the multiplier selected.
    NOTE: This option doesn't affect the Boost setting to disable/enable encounters.
    """
    internal_name = "overworld_encounter_rate"
    display_name = "Overworld Encounter Rate"
    option_0_00x = 0
    option_0_25x = 1
    option_0_50x = 2
    option_0_75x = 3
    option_1_00x = 4
    option_1_25x = 5
    option_1_50x = 6
    default = 3

class ExperienceBoost(Choice):
    """
    Set the default Experience Boost multiplier. This can still be modified in the Boost menu.
    """
    internal_name = "xp_boost"
    display_name = "Experience Boost"
    option_0_5x = 0
    option_1_0x = 1
    option_2_0x = 2
    option_3_0x = 3
    option_4_0x = 4
    default = 2

class GilBoost(Choice):
    """
    Set the default Gil Boost multiplier. This can still be modified in the Boost menu.
    """
    internal_name = "gil_boost"
    display_name = "Gil Boost"
    option_0_5x = 0
    option_1_0x = 1
    option_2_0x = 2
    option_3_0x = 3
    option_4_0x = 4
    default = 2

class BoostMenu(DefaultOnToggle):
    """
    Enable/Disable the in-game Boost menu. This will lock you to your current XP, Gil and Encounter Rate options.
    """
    internal_name = "boost_menu"
    display_name = "Boost Menu"

@dataclass
class FF1pixelOptions(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool

    # generation options
    shuffle_gear_shops: ShuffleGearShops
    shuffle_spells: ShuffleSpells
    job_promotion: JobPromotion
    lute_tablatures: LuteTablatures
    crystals_required: CrystalsRequired
    nerf_chaos: NerfChaos
    boss_minions: BossMinions
    monster_parties: MonsterParties
    monsters_cap: MonstersCap
    dungeon_encounter_rate: DungeonEncounterRate
    overworld_encounter_rate: OverworldEncounterRate
    shuffle_trials_maze: ShuffleTrialsMaze
    shuffle_overworld: ShuffleOverworld
    shuffle_entrances: ShuffleEntrances
    shuffle_towns: ShuffleTowns
    early_progression: EarlyProgression
    northern_docks: NorthernDocks
    xp_boost: ExperienceBoost
    gil_boost: GilBoost
    boost_menu: BoostMenu


grouped_options = [
    OptionGroup("Items Options", [
        ShuffleGearShops,
        ShuffleSpells,
        JobPromotion
    ]),
    OptionGroup("End Options", [
        LuteTablatures,
        CrystalsRequired
    ]),
    OptionGroup("Map Options", [
        ShuffleOverworld,
        ShuffleEntrances,
        ShuffleTowns,
        ShuffleTrialsMaze,
        EarlyProgression,
        NorthernDocks
    ]),
    OptionGroup("Monsters Options", [
        NerfChaos,
        BossMinions,
        MonsterParties,
        MonstersCap
    ]),
    OptionGroup("Scaling Options", [
        DungeonEncounterRate,
        OverworldEncounterRate,
        ExperienceBoost,
        GilBoost,
        BoostMenu
    ])
]

presets = {
    "Starter": {
        "shuffle_gear_shops": True,
        "shuffle_spells": True,
        "job_promotion": 0,
        "lute_tablatures": 0,
        "crystals_required": 4,
        "shuffle_trials_maze": True,
        "early_progression": 0,
        "shuffle_overworld": False,
        "shuffle_entrances": 0,
        "shuffle_towns": 0,
        "northern_docks": False,
        "nerf_chaos": True,
        "boss_minions": 0,
        "monster_parties": 1,
        "monsters_cap": 0,
        "dungeon_encounter_rate": 2,
        "overworld_encounter_rate": 2,
        "xp_boost": 3,
        "gil_boost": 3,
        "boost_menu": True,
    }}