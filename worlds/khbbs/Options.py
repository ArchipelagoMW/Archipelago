from dataclasses import dataclass

from Options import Toggle, Range, NamedRange, PerGameCommonOptions, StartInventoryPool, OptionGroup

class StartingWorlds(Range):
    """
    Number of random worlds to start with.
    """
    display_name = "Starting Worlds"
    default = 0
    range_start = 0
    range_end = 11

class EXPMultiplier(NamedRange):
    """
    Determines the multiplier to apply to EXP gained
    """
    display_name = "EXP Multiplier"
    default = 48
    range_start = 16 // 4
    range_end = 160
    special_range_names = {
        "0.25x": 16 // 4,
        "0.5x":  16 // 2,
        "1x":    16,
        "2x":    16 * 2,
        "3x":    16 * 3,
        "4x":    16 * 4,
        "8x":    16 * 8,
        "10x":   16 * 10,
    }

class Character(NamedRange):
    """
    Determines the expected player character.
    0: Ventus
    1: Aqua
    2: Terra
    """
    display_name = "Character"
    default = 2
    range_start = 0
    range_end = 2
    special_range_names = {
        "ventus": 0,
        "aqua":   1,
        "terra":  2,
    }

class FinalTerraXehanortII(Toggle):
    """
    Determines if Aqua will need to defeat Final Terra Xehanort II to complete her seed.
    Does nothing if the player chooses a character other than Aqua
    """
    display_name = "Final Terra Xehanort II"

class MirageArena(Toggle):
    """
    Determines if Mirage Arena battle locations should be included.
    """
    display_name = "Mirage Arena Battles"

class CommandBoard(Toggle):
    """
    Determines if Mirage Arena Command Board locations should be included.
    """
    display_name = "Command Board"

class SuperBosses(Toggle):
    """
    Determines if Super Boss locations should be included.
    """
    display_name = "Super Bosses"

class MaxHPIncreases(Range):
    """
    Number of Max HP Increases are in the item pool.
    """
    display_name = "Max HP Increases"
    default = 8
    range_start = 0
    range_end = 9

class RandomizeKeybladeStats(Toggle):
    """
    Determines if Keyblade stats should be randomized
    """
    display_name = "Randomize Keyblade Stats"

class KeybladeMinStrength(Range):
    """
    Determines the minimum Strength bonus a keyblade can have.
    """
    display_name = "Keyblade Minimum STR Bonus"
    default = 2
    range_start = 2
    range_end = 10

class KeybladeMaxStrength(Range):
    """
    Determines the maximum Strength bonus a keyblade can have.
    """
    display_name = "Keyblade Maximum STR Bonus"
    default = 10
    range_start = 2
    range_end = 10

class KeybladeMinMagic(Range):
    """
    Determines the minimum Magic bonus a keyblade can have.
    """
    display_name = "Keyblade Minimum MP Bonus"
    default = -2
    range_start = -2
    range_end = 10

class KeybladeMaxMagic(Range):
    """
    Determines the maximum Magic bonus a keyblade can have.
    """
    display_name = "Keyblade Maximum MP Bonus"
    default = 7
    range_start = -2
    range_end = 10

class RealmOfDarkness(Toggle):
    """
    If your character is Aqua, determines if Realm of Darkness is included as a world.
    """
    display_name = "Realm of Darkness"

class AdvancedLogic(Toggle):
    """
    If enabled, using commands for tricky movement and precise jumps will be required to reach many locations
    """
    display_name = "Advanced Logic"

class Minigames(Toggle):
    """
    Determines whether to include locations for the Disney Town minigames and the racing minigames in Mirage Arena
    """
    display_name = "Minigames"

class ArenaMedals(Toggle):
    """
    Determines if there should be locations for Mirage Arena medal collecting. Currently these have no logic or shortcuts beyond having Mirage Arena.
    """
    display_name = "Mirage Arena Medals"

class ArenaGlobalLocations(Toggle):
    """
    Determines if there should be locations for the Mirage Arena missions that require beating the game with each character
    Also enables Combined Threat and Monster of the Deep without their respective worlds
    If playing on a fresh save leave this off or you'll have unreachable locations!
    """
    display_name = "Mirage Arena Global Locations"

@dataclass
class KHBBSOptions(PerGameCommonOptions):
    character:       Character
    starting_worlds: StartingWorlds
    exp_multiplier:  EXPMultiplier
    final_terra_xehanort_ii:  FinalTerraXehanortII
    mirage_arena: MirageArena
    command_board: CommandBoard
    super_bosses: SuperBosses
    max_hp_increases: MaxHPIncreases
    randomize_keyblade_stats: RandomizeKeybladeStats
    keyblade_min_str: KeybladeMinStrength
    keyblade_max_str: KeybladeMaxStrength
    keyblade_min_mgc: KeybladeMinMagic
    keyblade_max_mgc: KeybladeMaxMagic
    realm_of_darkness: RealmOfDarkness
    advanced_logic: AdvancedLogic
    minigames: Minigames
    arena_medals: ArenaMedals
    arena_global_locations: ArenaGlobalLocations
    start_inventory_from_pool: StartInventoryPool

khbbs_option_groups = [
    OptionGroup("Locations",[
        Character,
        FinalTerraXehanortII,
        RealmOfDarkness,
        MirageArena,
        ArenaGlobalLocations,
        CommandBoard,
        ArenaMedals,
        Minigames,
        SuperBosses,
    ]),
    OptionGroup("Stats",[
        EXPMultiplier,
        MaxHPIncreases,
    ]),
    OptionGroup("Keyblades",[
        RandomizeKeybladeStats,
        KeybladeMinStrength,
        KeybladeMaxStrength,
        KeybladeMinMagic,
        KeybladeMaxMagic,
    ]),
    OptionGroup("Misc",[
        StartingWorlds,
        AdvancedLogic,
    ]),
]