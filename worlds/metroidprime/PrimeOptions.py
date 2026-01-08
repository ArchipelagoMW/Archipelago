from enum import Enum
from typing import List
from Options import (
    DeathLink,
    DefaultOnToggle,
    OptionSet,
    Toggle,
    Range,
    StartInventoryPool,
    Choice,
    PerGameCommonOptions,
    OptionGroup,
)
from dataclasses import dataclass

from .Enum import StartRoomDifficulty
from .LogicCombat import CombatLogicDifficulty
from .data.Tricks import TrickInfo, Tricks


class HudColor(Enum):
    DEFAULT = [102 / 255, 174 / 255, 225 / 255]
    RED = [1.0, 0.0, 0.0]
    GREEN = [0.0, 1.0, 0.0]
    BLUE = [0.0, 0.0, 1.0]
    VIOLET = [1.0, 0.0, 1.0]
    YELLOW = [1.0, 1.0, 0.0]
    CYAN = [0.0, 1.0, 1.0]
    WHITE = [1.0, 1.0, 1.0]
    ORANGE = [1.0, 0.5, 0.0]
    PINK = [1.0, 0.5, 1.0]
    LIME = [0.5, 1.0, 0.0]
    TEAL = [0.5, 1.0, 1.0]
    PURPLE = [0.5, 0.0, 1.0]


class SpringBall(DefaultOnToggle):
    """Enables the spring ball when you receive Morph Ball Bombs. This will allow you to jump while in morph ball form by pressing up on the c stick, reducing the complexity of double bomb jumps."""

    display_name = "Add Spring Ball"


class RequiredArtifacts(Range):
    """Determines the number of Artifacts needed to begin the endgame sequence."""

    display_name = "Required Artifacts"
    range_start = 1
    range_end = 12
    default = 12


class FinalBosses(Choice):
    """Determines the final bosses required to beat the seed. Choose from Meta Ridley, Metroid Prime,
    both, or neither."""

    display_name = "Final Boss Select"
    option_both = 0
    option_ridley = 1
    option_prime = 2
    option_none = 3
    default = 0


class ArtifactHints(DefaultOnToggle):
    """If enabled, scanning the artifact stones in the temple will give a hint to their location. Additionally, hints will be pre collected in the client."""

    display_name = "Artifact Hints"


class MissileLauncher(Toggle):
    """If enabled, the missile launcher will be added to the item pool. This will only allow you to use missiles once the missile launcher is found (regardless of missile expansions received)."""

    display_name = "Missile Launcher"


class MainPowerBomb(Toggle):
    """If enabled, the main power bomb will be added to the item pool. This will only allow you to use power bombs once the main power bombs is found (regardless of power bomb expansions received)."""

    display_name = "Main Power Bomb"


class ShuffleScanVisor(Toggle):
    """If enabled, the scan visor will be shuffled into the item pool and will need to be found in order to scan dash and open certain locks."""

    display_name = "Shuffle Scan Visor"


class NonVariaHeatDamage(DefaultOnToggle):
    """If enabled, the gravity suit and phazon suit will not protect against heat damage which will change the required logic of the game."""

    display_name = "Non-Varia Heat Damage"


class StaggeredSuitDamage(Choice):
    """Configure how suit damage reduction is calculated.
    Default: based on the strongest suit you have
    Progressive: based on the number of suits you have
    Additive: Individual suits provide their added damage reduction
    """

    display_name = "Staggered Suit Damage"
    option_default = 0
    option_progressive = 1
    option_additive = 2
    default = 1


class RemoveHiveMecha(Toggle):
    """If enabled, the trigger for the Hive Mecha boss will be removed from the game."""

    display_name = "Remove Hive Mecha"


class FusionSuit(Toggle):
    """If enabled, will replace all the suits in game with the Fusion Suit variants (cosmetic only). Suit color randomization will have no effect if this is enabled."""

    display_name = "Fusion Suit"


class TrickDifficulty(Choice):
    """Determines which tricks, if any, are required to complete the seed. This will affect the logic of the game"""

    display_name = "Trick Difficulty"
    option_no_tricks = -1
    option_easy = 0
    option_medium = 1
    option_hard = 2
    default = -1


class TrickAllowList(OptionSet):
    """A list of trick names to explicitly allow in logic, regardless of selected difficulty. For example, "Crashed Frigate Scan Dash" or "Alcove Escape"."""

    display_name = "Trick Allow List"
    default = []
    valid_keys: List[str] = [  # type: ignore
        getattr(Tricks, trick).name
        for trick in vars(Tricks)
        if isinstance(getattr(Tricks, trick), TrickInfo)
    ]


class TrickDenyList(OptionSet):
    """A list of trick names to explicitly deny in logic, regardless of selected difficulty.  For example, "Crashed Frigate Scan Dash" or "Alcove Escape"."""

    display_name = "Trick Deny List"
    valid_keys: List[str] = [  # type: ignore
        getattr(Tricks, trick).name
        for trick in vars(Tricks)
        if isinstance(getattr(Tricks, trick), TrickInfo)
    ]


class BackwardsLowerMines(Toggle):
    """If enabled, allows you to progress through the lower mines in reverse by removing the locks in the PCA room."""

    display_name = "Backwards Lower Mines"


class FlaahgraPowerBombs(Toggle):
    """If enabled, makes the sandstone block at the top of arboretum breakable with power bombs. Note that this will require you to have 4 power bombs in order to defeat Flaahgra."""

    display_name = "Flaahgra Power Bombs"


class RemoveXrayRequirements(Choice):
    """Determines the xray visor requirements.
    Remove None: No xray visor requirements are removed.
    Remove Most: All xray visor requirements are removed except for metroid prime, chozo ghosts (normal/minimal combat difficulty), and omega pirate.
    Remove All But Omega Pirate: All xray visor requirements are removed except for omega pirate.
    """

    display_name = "Remove Xray Visor Requirements"
    option_remove_none = 0
    alias_false = 0
    option_remove_most = 1
    alias_true = 1
    option_remove_all_but_omega_pirate = 2
    default = 0


class RemoveThermalRequirements(Choice):
    """Determines the thermal visor requirements.
    Remove None: No thermal visor requirements are removed.
    Remove Most: All thermal visor requirements are removed except for metroid prime (note this means wave beam panels will be in logic without the visor to see them).
    Remove All: All thermal visor requirements are removed (note this means wave beam panels will be in logic without the visor to see them).
    """

    display_name = "Remove Thermal Visor Requirements"
    option_remove_none = 0
    alias_false = 0
    option_remove_most = 1
    alias_true = 1
    option_remove_all = 2
    default = 0


class StartingRoom(Choice):
    """Determines the starting room of the game. This will change your starting loadout depending on the room.
    Normal: Start at the Talon Overworld Landing Site. Most randomization options, when enabled, will move the starting room to Save Station 1 in Chozo Ruins due to the restrictive nature of the landing site starting room.
    Safe: Start in rooms that will not require a significant combat challenge to progress from.
    Buckle Up: Start in rooms that will pose a significant challenge to players with no energy tanks or suit upgrades. Fun for the aspiring masochist (less fun for their friends waiting in BK).
    """

    display_name = "Starting Room Randomization"
    option_normal = StartRoomDifficulty.Normal.value
    option_safe = StartRoomDifficulty.Safe.value
    option_buckle_up = StartRoomDifficulty.Buckle_Up.value
    default = StartRoomDifficulty.Normal.value


class CombatLogicDifficultyOption(Choice):
    """When enabled, the game will include energy tanks and the charge beam as requirements for certain combat heavy rooms."""

    display_name = "Combat Logic Difficulty"
    default = CombatLogicDifficulty.NORMAL.value
    option_no_logic = CombatLogicDifficulty.NO_LOGIC.value
    option_normal_logic = CombatLogicDifficulty.NORMAL.value
    option_minimal_logic = CombatLogicDifficulty.MINIMAL.value


class ElevatorRandomization(Toggle):
    """Randomizes the elevators between regions."""

    display_name = "Elevator Randomization"


class DoorColorRandomization(Choice):
    """Determine if/how door colors are randomized.
    None: No door colors will be randomized
    Global: All door colors of a given color will be randomized to another color
    Regional: Each Region will have its door colors randomized to another color
    """

    display_name = "Door Color Randomization"
    option_none = 0
    option_global = 1
    option_regional = 2
    default = 0


class BlastShieldRandomization(Choice):
    """Determine if/how blast shields are randomized. Note that this will have a difficult time generating in solo worlds with no tricks enabled.
    None: No blast shields will be randomized
    Replace Existing: Each existing Missile Blast Shield will be replaced with a different Blast Shield type
    Mix It Up: Each Region will remove all existing blast shields and instead add a specified number to new doors
    """

    display_name = "Blast Shield Randomization"
    option_none = 0
    option_replace_existing = 1
    option_mix_it_up = 2
    default = 0


class BlastShieldAvailableTypes(Choice):
    """Which blast shield types are available for randomization.
    All: All blast shield types are available, including beam combos, bomb, power bomb, charge beam, and super missiles
    No beam combos: Flamethrower, Wavebuster, and Ice Spreader will not be included as blast shield types (Super Missiles will still be included)
    """

    display_name = "Blast Shield Available Types"
    option_all = 1
    option_no_beam_combos = 0
    default = 0


class BlastShieldFrequency(Choice):
    """If using 'Mix It Up' for blast shield randomization, how many blast shields should be added per region? These are added using a percentage of total possible placements so exact numbers will vary by region. Higher numbers will have more difficulty genning in solo worlds with less tricks.
    Low: 10%
    Medium: 30%
    High: 50%
    """

    display_name = "Blast Shield Frequency"
    option_low = 1
    option_medium = 4
    option_high = 6
    default = 4


class LockedDoorCount(Range):
    """If greater than 0, locked doors will be placed in the game (maximum of 1 per level). These will only be placed in spots that will not prevent progression but may force alternate paths."""

    display_name = "Number of Locked Doors to Include"
    range_start = 0
    range_end = 2
    default = 0


class IncludePowerBeamDoors(Toggle):
    """If enabled, Power Beam doors will be an available door color for randomization. If the starting beam is also randomized, it will remove the new starting beam's color from the pool of available door colors."""

    display_name = "Include Power Beam Doors"


class IncludeMorphBallBombDoors(Toggle):
    """If enabled, Morph Ball Bomb doors will be added as an available door color for door randomization."""

    display_name = "Include Morph Ball Bomb Doors"


class RandomizeStartingBeam(Toggle):
    """If enabled, the starting beam will be randomized to a random beam that is not the Power Beam."""

    display_name = "Randomize Starting Beam"


class PreScanElevators(DefaultOnToggle):
    """Pre scans the elevators in the game, allowing for faster transitions between regions. Makes for more interesting gameplay if disabled when the scan visor is shuffled."""

    display_name = "Pre Scan Elevators"


class ProgressiveBeamUpgrades(Toggle):
    """If enabled, 3 progressive beam items will be added into the item pool per beam. These unlock the beam itself, charging capabilities, and the associated missile combo."""

    display_name = "Progressive Beam Upgrades"


# COSMETIC OPTIONS


class RandomizeSuitColors(Toggle):
    """Randomize the colors of the suits. Is overridden if any of the color overrides are greater than 0. Note: This is not compatible with the Fusion Suit and will have no effect."""

    display_name = "Randomize Suit Colors"


class PowerSuitColorOverride(Range):
    """Override the color of the Power Suit using an index from the game's color wheel."""

    display_name = "Power Suit Color Override"
    range_start = 0
    range_end = 359
    default = 0


class VariaSuitColorOverride(Range):
    """Override the color of the Varia Suit using an index from the game's color wheel."""

    display_name = "Varia Suit Color Override"
    range_start = 0
    range_end = 359
    default = 0


class GravitySuitColorOverride(Range):
    """Override the color of the Gravity Suit using an index from the game's color wheel."""

    display_name = "Gravity Suit Color Override"
    range_start = 0
    range_end = 359
    default = 0


class PhazonSuitColorOverride(Range):
    """Override the color of the Phazon Suit using an index from the game's color wheel."""

    display_name = "Phazon Suit Color Override"
    range_start = 0
    range_end = 359
    default = 0


class HudColorOption(Choice):
    """Determines the color of the HUD in the game. Will be overridden if any of the color overrides are greater than 0. Note: Certain colors will change the colors of the beam icons."""

    display_name = "HUD Color"
    default = 0
    option_default = 0
    option_red = 1
    option_green = 2
    option_blue = 3
    option_violet = 4
    option_yellow = 5
    option_cyan = 6
    option_white = 7
    option_orange = 8
    option_pink = 9
    option_lime = 10
    option_teal = 11
    option_purple = 12


class HudColorOverrideRed(Range):
    """0 to 255, sets the Red channel of the HUD color."""

    display_name = "HUD Color Red"
    range_start = 0
    range_end = 255
    default = 0


class HudColorOverrideGreen(Range):
    """0 to 255, sets the Green channel of the HUD color."""

    display_name = "HUD Color Green"
    range_start = 0
    range_end = 255
    default = 0


class HudColorOverrideBlue(Range):
    """0 to 255, sets the Blue channel of the HUD color."""

    display_name = "HUD Color Blue"
    range_start = 0
    range_end = 255
    default = 0


@dataclass
class MetroidPrimeOptions(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    required_artifacts: RequiredArtifacts
    final_bosses: FinalBosses
    artifact_hints: ArtifactHints
    missile_launcher: MissileLauncher
    main_power_bomb: MainPowerBomb
    shuffle_scan_visor: ShuffleScanVisor
    pre_scan_elevators: PreScanElevators
    elevator_randomization: ElevatorRandomization
    door_color_randomization: DoorColorRandomization
    blast_shield_randomization: BlastShieldRandomization
    blast_shield_frequency: BlastShieldFrequency
    blast_shield_available_types: BlastShieldAvailableTypes
    locked_door_count: LockedDoorCount
    include_power_beam_doors: IncludePowerBeamDoors
    include_morph_ball_bomb_doors: IncludeMorphBallBombDoors
    randomize_starting_beam: RandomizeStartingBeam
    starting_room: StartingRoom
    progressive_beam_upgrades: ProgressiveBeamUpgrades
    non_varia_heat_damage: NonVariaHeatDamage
    staggered_suit_damage: StaggeredSuitDamage
    combat_logic_difficulty: CombatLogicDifficultyOption
    trick_difficulty: TrickDifficulty
    trick_allow_list: TrickAllowList
    trick_deny_list: TrickDenyList
    flaahgra_power_bombs: FlaahgraPowerBombs
    backwards_lower_mines: BackwardsLowerMines
    remove_xray_requirements: RemoveXrayRequirements
    remove_thermal_requirements: RemoveThermalRequirements
    remove_hive_mecha: RemoveHiveMecha
    spring_ball: SpringBall

    # Cosmetic options
    fusion_suit: FusionSuit
    hud_color: HudColorOption
    hud_color_red: HudColorOverrideRed
    hud_color_green: HudColorOverrideGreen
    hud_color_blue: HudColorOverrideBlue
    randomize_suit_colors: RandomizeSuitColors
    power_suit_color: PowerSuitColorOverride
    varia_suit_color: VariaSuitColorOverride
    gravity_suit_color: GravitySuitColorOverride
    phazon_suit_color: PhazonSuitColorOverride

    death_link: DeathLink


prime_option_groups = [
    OptionGroup(
        "General",
        [
            RequiredArtifacts,
            ArtifactHints,
            FinalBosses,
            StartingRoom,
            CombatLogicDifficultyOption,
        ],
    ),
    OptionGroup(
        "Gameplay Tweaks",
        [
            ProgressiveBeamUpgrades,
            MissileLauncher,
            MainPowerBomb,
            RandomizeStartingBeam,
            ShuffleScanVisor,
            PreScanElevators,
            NonVariaHeatDamage,
            StaggeredSuitDamage,
            SpringBall,
        ],
    ),
    OptionGroup(
        "Door Randomization",
        [
            ElevatorRandomization,
            DoorColorRandomization,
            BlastShieldRandomization,
            BlastShieldFrequency,
            BlastShieldAvailableTypes,
            LockedDoorCount,
            IncludePowerBeamDoors,
            IncludeMorphBallBombDoors,
        ],
    ),
    OptionGroup(
        "Tricks",
        [
            TrickDifficulty,
            RemoveHiveMecha,
            BackwardsLowerMines,
            RemoveXrayRequirements,
            RemoveThermalRequirements,
            FlaahgraPowerBombs,
            TrickAllowList,
            TrickDenyList,
        ],
    ),
    OptionGroup(
        "Cosmetic",
        [
            FusionSuit,
            HudColorOption,
            HudColorOverrideRed,
            HudColorOverrideGreen,
            HudColorOverrideBlue,
            RandomizeSuitColors,
            PowerSuitColorOverride,
            VariaSuitColorOverride,
            GravitySuitColorOverride,
            PhazonSuitColorOverride,
        ],
    ),
]
