from dataclasses import dataclass

from Options import Toggle, Range, Choice, PerGameCommonOptions, DefaultOnToggle, StartInventoryPool, OptionGroup, \
    DeathLink, Removed


# Main Options

class GameMode(Choice):
    """Determines starting location and accessibility.
    Vanilla starts you in the Docking Bay with no items.
    Open Sector Hub starts you in the Sector Hub with one E-Tank and one random item. All sector elevators will be open.
    Custom will apply the settings in the Custom Game Mode section."""
    display_name = "Game Mode"
    option_vanilla = 0
    option_open_sector_hub = 1
    option_custom = 2
    default = 0

class InfantMetroidsInPool(Range):
    """How many Infant Metroids will be in the item pool."""
    display_name = "Infant Metroids in Pool"
    range_start = 1
    range_end = 20
    default = 5

class InfantMetroidsRequired(Range):
    """How many Infant Metroids will be required to beat the game.
    If set to more than the number in the pool, will instead become however many are present."""
    display_name = "Infant Metroids Required"
    range_start = 1
    range_end = 20
    default = 5

class InfantMetroidLocations(Choice):
    """Where Infant Metroids can be located.
    Anywhere allows them to be anywhere in the multiworld.
    Bosses Encouraged increases the chances of them being located on local boss locations.
    Only Bosses means Infant Metroids can only be on your boss locations. Will limit the number of Infant Metroids
    in the pool. if greater than the number of bosses."""
    display_name = "Infant Metroid Locations"
    option_anywhere = 0
    option_bosses_encouraged = 1
    option_only_bosses = 2
    default = 0

# Logic Options

class EarlyProgression(Choice):
    """Determines if an early progression item guaranteed in one of your first locations.
    Normal restricts the starting item pool to Morph Ball and Missiles.
    Advanced expands the pool to Screw Attack.
    If Shinespark Tricks are set to Advanced, adds Speed Booster as well
    Option is in testing and may increase generation failures."""
    display_name = "Early Progression"
    option_none = 0
    option_normal = 1
    option_advanced = 2
    default = 1

class PointOfNoReturnsInLogic(DefaultOnToggle):
    """Should Point of No Return locations be in logic.
    If disabled, you will never be required to enter an area without the items to exit out."""
    display_name = "Point of No Returns in Logic"

class SectorTubeShuffle(Toggle):
    """If enabled, shuffles the tube connections between sectors.
    Does not affect the non-glass tube connections."""
    display_name = "Sector Tube Shuffle"

class ElevatorShuffle(Choice):
    """If enabled, shuffles the various elevator connections.
     Sectors will shuffle the six sector elevators in the Sector Hub.
     All will include all elevator connections in the game.
     Note that if enabled, logical energy tank requirements will be relaxed."""
    display_name = "Elevator Shuffle"
    option_none = 0
    option_sectors = 1
    option_all = 2
    default = 0

# Trick Options

class WallJumpTrickDifficulty(Choice):
    """What level of wall jump trick difficulty may be required to navigate around."""
    display_name = "Wall Jump Trick Difficulty"
    option_none = 0
    option_beginner = 1
    option_advanced = 2
    default = 0

class ShinesparkTrickDifficulty(Choice):
    """What level of shinespark trick difficulty may be required to navigate around.
    Note that this does not exclude items that require shinesparking in vanilla to obtain.
    Use the ShinesparkLocations location group for that."""
    display_name = "Shinespark Trick Difficulty"
    option_none = 0
    option_beginner = 1
    option_advanced = 2
    default = 0

class CombatDifficulty(Choice):
    """What level of combat tools are logically expected for later game bosses."""
    display_name = "Combat Difficulty"
    option_beginner = 0
    option_advanced = 1
    option_expert = 2
    default = 0

# Custom Game Mode options

class StartingLocation(Choice):
    """Your starting location.
    This is a Custom Game Mode option and will only be applied if GameMode is set to Custom."""
    display_name = "Starting Location"
    option_docking_bay = 0
    option_operations_deck = 1
    option_sector_hub = 2
    option_concourse_save_station = 3
    default = 0

class StartingMajorUpgrades(Range):
    """How many major upgrades you begin with.
    Note that depending on your StartingLocation and EarlyProgression settings, you may receive more than specified here
    in order to successfully generate the game. Upgrades are taken from the general item pool and will be replaced
    by a random minor tank.
    These will be applied in addition to your start_inventory and start_inventory_from_pool items.
    These will be sent by the client once you're connected.
    This is a Custom Game Mode option and will only be applied if GameMode is set to Custom."""
    display_name = "Starting Major Upgrades"
    range_start = 0
    range_end = 22
    default = 0

class StartingEnergyTanks(Range):
    """How many Energy Tanks you begin with.
    This will be overridden by the number specified in start_inventory and start_inventory_from_pool, if applicable.
    Energy tanks are taken from the general item pool and will be replaced by a random minor tank.
    These will be sent by the client once you're connected.
    This is a Custom Game Mode option and will only be applied if GameMode is set to Custom."""
    display_name = "Starting Energy Tanks"
    range_start = 0
    range_end = 20
    default = 0

class OpenSectorElevators(Toggle):
    """Determines if the sector elevators in the Sector Hub are locked by their vanilla keycard requirements.
    This is a Custom Game Mode option and will only be applied if GameMode is set to Custom."""
    display_name = "Open Sector Elevators"

class SectorNavigationRoomHintLocks(Toggle):
    """Determines if the Navigation Rooms at the start of each sector have their hints locked by keycard requirements.
    If set, the keycard required for the hint will be one level higher than the level needed to access the sector
    in vanilla. Has no effect if EnableHints is disabled.
    This is a Custom Game Mode option and will only be applied if GameMode is set to Custom."""
    display_name = "Sector Navigation Room Hint Locks"

# Minor Options

class PaletteRandomization(Toggle):
    """Randomize the ingame palettes."""
    display_name = "Palette Randomization"

class EnableHints(DefaultOnToggle):
    """Enable ingame hints at Navigation Stations."""
    display_name = "Enable Hints"

class RevealHiddenBlocks(DefaultOnToggle):
    """Enables whether destructible blocks are revealed from the start."""
    display_name = "Reveal Hidden Blocks"

class FastDoorTransitions(DefaultOnToggle):
    """Enables fast door transitions between rooms."""
    display_name = "Fast Door Transitions"

class MissileDataAmmo(Range):
    """The amount of missiles provided by a Missile Data item."""
    display_name = "Missile Data Ammo"
    range_start = 5
    range_end = 100
    default = 10

class PowerBombDataAmmo(Range):
    """The amount of power bombs provided by a Power Bomb Data item."""
    display_name = "Power Bomb Data Ammo"
    range_start = 5
    range_end = 100
    default = 10

class MissileTankAmmo(Range):
    """The amount of missiles provided by a Missile Tank item."""
    display_name = "Missile Tank Ammo"
    range_start = 0
    range_end = 100
    default = 5

class PowerBombTankAmmo(Range):
    """The amount of power bombs provided by a Power Bomb Tank item."""
    display_name = "Power Bomb Tank Ammo"
    range_start = 0
    range_end = 100
    default = 2

# Deprecated options

class TrickyShinesparksInRegionLogic(Removed):
    """DEPRECATED OPTION. WILL BE REMOVED IN A FUTURE VERSION.
    Use ShinesparkTrickDifficulty instead."""
    display_name = "Tricky Shinesparks in Region Logic"

    def __init__(self, value: str):
        if value:
            raise Exception("TrickyShinesparksInRegionLogic option removed. "
                            "Please use ShinesparkTrickDifficulty instead.")
        super().__init__(value)

class SimpleWallJumpsInRegionLogic(Removed):
    """DEPRECATED OPTION. WILL BE REMOVED IN A FUTURE VERSION.
    Use WallJumpTrickDifficulty instead."""
    display_name = "Simple Wall Jumps in Region Logic"

    def __init__(self, value: str):
        if value:
            raise Exception("SimpleWallJumpsInRegionLogic option removed. Please use WallJumpTrickDifficulty instead.")
        super().__init__(value)

@dataclass
class MetroidFusionOptions(PerGameCommonOptions):
    GameMode: GameMode
    InfantMetroidsInPool: InfantMetroidsInPool
    InfantMetroidsRequired: InfantMetroidsRequired
    InfantMetroidLocations: InfantMetroidLocations

    EarlyProgression: EarlyProgression
    SectorTubeShuffle: SectorTubeShuffle
    ElevatorShuffle: ElevatorShuffle
    PointOfNoReturnsInLogic: PointOfNoReturnsInLogic

    ShinesparkTrickDifficulty: ShinesparkTrickDifficulty
    WallJumpTrickDifficulty: WallJumpTrickDifficulty
    CombatDifficulty: CombatDifficulty

    StartingLocation: StartingLocation
    StartingMajorUpgrades: StartingMajorUpgrades
    StartingEnergyTanks: StartingEnergyTanks
    OpenSectorElevators: OpenSectorElevators
    SectorNavigationRoomHintLocks: SectorNavigationRoomHintLocks

    PaletteRandomization: PaletteRandomization
    EnableHints: EnableHints
    RevealHiddenBlocks: RevealHiddenBlocks
    FastDoorTransitions: FastDoorTransitions
    MissileDataAmmo: MissileDataAmmo
    MissileTankAmmo: MissileTankAmmo
    PowerBombDataAmmo: PowerBombDataAmmo
    PowerBombTankAmmo: PowerBombTankAmmo

    TrickyShinesparksInRegionLogic: TrickyShinesparksInRegionLogic
    SimpleWallJumpsInRegionLogic: SimpleWallJumpsInRegionLogic

    start_inventory_from_pool: StartInventoryPool
    death_link: DeathLink

metroid_fusion_option_groups = [
    OptionGroup("Main Options", [
        GameMode,
        InfantMetroidsInPool,
        InfantMetroidsRequired,
        InfantMetroidLocations
    ]),
    OptionGroup("Logic Options", [
        EarlyProgression,
        SectorTubeShuffle,
        ElevatorShuffle,
        PointOfNoReturnsInLogic
    ]),
    OptionGroup("Trick Options", [
        ShinesparkTrickDifficulty,
        WallJumpTrickDifficulty,
        CombatDifficulty
    ]),
    OptionGroup("Custom Game Mode Options", [
        StartingLocation,
        StartingMajorUpgrades,
        StartingEnergyTanks,
        OpenSectorElevators,
        SectorNavigationRoomHintLocks
    ]),
    OptionGroup("Minor Options", [
        PaletteRandomization,
        EnableHints,
        RevealHiddenBlocks,
        FastDoorTransitions,
        MissileDataAmmo,
        MissileTankAmmo,
        PowerBombDataAmmo,
        PowerBombTankAmmo,
    ])
]