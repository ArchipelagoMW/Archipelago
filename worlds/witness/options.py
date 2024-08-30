from dataclasses import dataclass

from schema import And, Schema

from Options import Choice, DefaultOnToggle, OptionDict, OptionGroup, PerGameCommonOptions, Range, Toggle, Visibility

from .data import static_logic as static_witness_logic
from .data.item_definition_classes import ItemCategory, WeightedItemDefinition


class DisableNonRandomizedPuzzles(Toggle):
    """
    Disables puzzles that cannot be randomized.
    This includes many puzzles that heavily involve the environment, such as Shadows, Monastery or Orchard.

    The lasers for those areas will activate as you solve optional puzzles, such as Discarded Panels.
    Additionally, the panel activating the Jungle Popup Wall will be on from the start.
    """
    display_name = "Disable non randomized puzzles"


class EarlyCaves(Choice):
    """
    Adds an item that opens the Caves Shortcuts to Swamp and Mountain, allowing early access to the Caves even if you are not playing a remote Door Shuffle mode.
    You can either add this item to the pool to be found in the multiworld, or you can outright start with it and have immediate access to the Caves.

    If you choose "Add To Pool" and you are already playing a remote Door Shuffle mode, this option will do nothing.
    """
    display_name = "Early Caves"
    option_off = 0
    alias_false = 0
    option_add_to_pool = 1
    option_starting_inventory = 2
    alias_true = 2
    alias_on = 2


class EarlySymbolItem(DefaultOnToggle):
    """
    Put a random helpful symbol item on an early check, specifically Tutorial Gate Open if it is available early.
    """

    visibility = Visibility.none


class ShuffleSymbols(DefaultOnToggle):
    """
    If on, you will need to unlock puzzle symbols as items to be able to solve the panels that contain those symbols.

    Please note that there is no minimum set of progression items in this randomizer.
    If you turn this option off and don't turn on door shuffle or obelisk keys, there will be no progression items, which will disallow you from adding your yaml to a multiworld generation.
    """
    display_name = "Shuffle Symbols"


class ShuffleLasers(Choice):
    """
    If on, the 11 lasers are turned into items and will activate on their own upon receiving them.
    """
    display_name = "Shuffle Lasers"
    option_off = 0
    alias_false = 0
    option_local = 1
    option_anywhere = 2
    alias_true = 2
    alias_on = 2


class ShuffleDoors(Choice):
    """
    If on, opening doors, moving bridges etc. will require a "key".
    - Panels: The panel on the door will be locked until receiving its corresponding key.
    - Doors: The door will open immediately upon receiving its key. Door panels are added as location checks.
    - Mixed: Includes all doors from "doors", and all control panels (bridges, elevators etc.) from "panels".
    """
    display_name = "Shuffle Doors"
    option_off = 0
    option_panels = 1
    option_doors = 2
    option_mixed = 3


class DoorGroupings(Choice):
    """
    Controls how door items are grouped.

    - Off: There will be one key for each door, potentially resulting in upwards of 120 keys being added to the item pool.
    - Regional: All doors in the same general region will open at once with a single key, reducing the amount of door items and complexity.
    """
    display_name = "Door Groupings"
    option_off = 0
    option_regional = 1


class ShuffleBoat(DefaultOnToggle):
    """
    If on, adds a "Boat" item to the item pool. Before receiving this item, you will not be able to use the boat.
    """
    display_name = "Shuffle Boat"


class ShuffleDiscardedPanels(Toggle):
    """
    Adds Discarded Panels into the location pool.

    Even if this is off, solving certain Discarded Panels may still be necessary to beat the game - The main example of this being the alternate activation triggers in "Disable non randomized puzzles".
    """
    display_name = "Shuffle Discarded Panels"


class ShuffleVaultBoxes(Toggle):
    """
    Adds Vault Boxes to the location pool.
    """
    display_name = "Shuffle Vault Boxes"


class ShuffleEnvironmentalPuzzles(Choice):
    """
    Adds Environmental/Obelisk Puzzles into the location pool.
    - Individual: Every Environmental Puzzle sends an item.
    - Obelisk Sides: Completing every puzzle on one side of an Obelisk sends an item.

    Note: In Obelisk Sides, any EPs excluded through another option will be pre-completed on their Obelisk.
    """
    display_name = "Shuffle Environmental Puzzles"
    option_off = 0
    option_individual = 1
    option_obelisk_sides = 2


class ShuffleDog(Choice):
    """
    Adds petting the dog statue in Town into the location pool.
    Alternatively, you can force it to be a Puzzle Skip.
    """
    display_name = "Pet the Dog"

    option_off = 0
    option_puzzle_skip = 1
    option_random_item = 2
    default = 1


class EnvironmentalPuzzlesDifficulty(Choice):
    """
    When "Shuffle Environmental Puzzles" is on, this setting governs which EPs are eligible for the location pool.
    - Eclipse: Every EP in the game is eligible, including the 1-hour-long "Theater Eclipse EP".
    - Tedious Theater Eclipse EP is excluded from the location pool.
    - Normal: several other difficult or long EPs are excluded as well.
    """
    display_name = "Environmental Puzzles Difficulty"
    option_normal = 0
    option_tedious = 1
    option_eclipse = 2


class ObeliskKeys(DefaultOnToggle):
    """
    Add one Obelisk Key item per Obelisk, locking you out of solving any of the associated Environmental Puzzles.

    Does nothing if "Shuffle Environmental Puzzles" is set to "off".
    """
    display_name = "Obelisk Keys"


class ShufflePostgame(Toggle):
    """
    Adds locations into the pool that are guaranteed to become accessible after or at the same time as your goal.
    Use this if you don't play with release on victory.
    """
    display_name = "Shuffle Postgame"


class VictoryCondition(Choice):
    """
    Set the victory condition for this world.
    - Elevator: Start the elevator at the bottom of the mountain (requires Mountain Lasers).
    - Challenge: Beat the secret Challenge (requires Challenge Lasers).
    - Mountain Box Short: Input the short solution to the Mountaintop Box (requires Mountain Lasers).
    - Mountain Box Long: Input the long solution to the Mountaintop Box (requires Challenge Lasers).
    - Panel Hunt: Solve a specific number of randomly selected panels before going to the secret ending in Tutorial.

    It is important to note that while the Mountain Box requires Desert Laser to be redirected in Town for that laser
    to count, the laser locks on the Elevator and Challenge Timer panels do not.
    """
    display_name = "Victory Condition"
    option_elevator = 0
    option_challenge = 1
    option_mountain_box_short = 2
    option_mountain_box_long = 3
    option_panel_hunt = 4


class PanelHuntTotal(Range):
    """
    Sets the number of random panels that will get marked as "Panel Hunt" panels in the "Panel Hunt" game mode.
    """
    display_name = "Total Panel Hunt panels"
    range_start = 5
    range_end = 100
    default = 40


class PanelHuntRequiredPercentage(Range):
    """
    Determines the percentage of "Panel Hunt" panels that need to be solved to win.
    """
    display_name = "Percentage of required Panel Hunt panels"
    range_start = 20
    range_end = 100
    default = 63


class PanelHuntPostgame(Choice):
    """
    In panel hunt, there are technically no postgame locations.
    Depending on your options, this can leave Mountain and Caves as two huge areas with Hunt Panels in them that cannot be reached until you get enough lasers to go through the very linear Mountain descent.
    Panel Hunt tends to be more fun when the world is open.
    This option lets you force anything locked by lasers to be disabled, and thus ineligible for Hunt Panels.
    To compensate, the respective mountain box solution (short box / long box) will be forced to be a Hunt Panel.
    Does nothing if Panel Hunt is not your victory condition.

    Note: The "Mountain Lasers" option may also affect locations locked by challenge lasers if the only path to those locations leads through the Mountain Entry.
    """

    display_name = "Force postgame in Panel Hunt"

    option_everything_is_eligible = 0
    option_disable_mountain_lasers_locations = 1
    option_disable_challenge_lasers_locations = 2
    option_disable_anything_locked_by_lasers = 3
    default = 3


class PanelHuntDiscourageSameAreaFactor(Range):
    """
    The greater this value, the less likely it is that many Hunt Panels show up in the same area.

    At 0, Hunt Panels will be selected randomly.
    At 100, Hunt Panels will be almost completely evenly distributed between areas.
    """
    display_name = "Panel Hunt Discourage Same Area Factor"

    range_start = 0
    range_end = 100
    default = 40


class PuzzleRandomization(Choice):
    """
    Puzzles in this randomizer are randomly generated. This option changes the difficulty/types of puzzles.
    """
    display_name = "Puzzle Randomization"
    option_sigma_normal = 0
    option_sigma_expert = 1
    option_none = 2


class MountainLasers(Range):
    """
    Sets the number of lasers required to enter the Mountain.
    If set to a higher number than 7, the mountaintop box will be slightly rotated to make it possible to solve without the hatch being opened.
    This change will also be applied logically to the long solution ("Challenge Lasers" option).
    """
    display_name = "Required Lasers for Mountain Entry"
    range_start = 1
    range_end = 11
    default = 7


class ChallengeLasers(Range):
    """
    Sets the number of lasers required to enter the Caves through the Mountain Bottom Floor Discard and to unlock the Challenge Timer Panel.
    """
    display_name = "Required Lasers for Challenge"
    range_start = 1
    range_end = 11
    default = 11


class ElevatorsComeToYou(Toggle):
    """
    If on, the Quarry Elevator, Bunker Elevator and Swamp Long Bridge will "come to you" if you approach them.
    This does actually affect logic as it allows unintended backwards / early access into these areas.
    """
    display_name = "All Bridges & Elevators come to you"


class TrapPercentage(Range):
    """
    Replaces junk items with traps, at the specified rate.
    """
    display_name = "Trap Percentage"
    range_start = 0
    range_end = 100
    default = 20


class TrapWeights(OptionDict):
    """
    Specify the weights determining how many copies of each trap item will be in your itempool.
    If you don't want a specific type of trap, you can set the weight for it to 0 (Do not delete the entry outright!).
    If you set all trap weights to 0, you will get no traps, bypassing the "Trap Percentage" option.
    """
    display_name = "Trap Weights"
    schema = Schema({
        trap_name: And(int, lambda n: n >= 0)
        for trap_name, item_definition in static_witness_logic.ALL_ITEMS.items()
        if isinstance(item_definition, WeightedItemDefinition) and item_definition.category is ItemCategory.TRAP
    })
    default = {
        trap_name: item_definition.weight
        for trap_name, item_definition in static_witness_logic.ALL_ITEMS.items()
        if isinstance(item_definition, WeightedItemDefinition) and item_definition.category is ItemCategory.TRAP
    }


class PuzzleSkipAmount(Range):
    """
    Adds this many Puzzle Skips into the pool, if there is room. Puzzle Skips let you skip one panel.
    """
    display_name = "Puzzle Skips"
    range_start = 0
    range_end = 30
    default = 10


class HintAmount(Range):
    """
    Adds hints to Audio Logs. If set to a low amount, up to 2 additional duplicates of each hint will be added.
    Remaining Audio Logs will have junk hints.
    """
    display_name = "Hints on Audio Logs"
    range_start = 0
    range_end = 49
    default = 12


class VagueHints(Choice):
    """Make Location Hints a bit more vague, where they only tell you about the general area the item is in.
    Area Hints will be generated as normal.

    If set to "stable", only location groups will be used. If location groups aren't implemented for the game your item ended up in, your hint will instead only tell you that the item is "somewhere in" that game.
    If set to "experimental", region names will be eligible as well, and you will never receive a "somewhere in" hint. Keep in mind that region names are not always intended to be comprehensible to players — only turn this on if you are okay with a bit of chaos.


    The distinction does not matter in single player, as Witness implements location groups for every location.

    Also, please don't pester any devs about implementing location groups. Bring it up nicely, accept their response even if it is "No".
    """
    display_name = "Vague Hints"

    option_off = 0
    option_stable = 1
    option_experimental = 2


class AreaHintPercentage(Range):
    """
    There are two types of hints for The Witness.
    "Location hints" hint one location in your world or one location containing an item for your world.
    "Area hints" tell you some general info about the items you can find in one of the main geographic areas on the island.
    Use this option to specify how many of your hints you want to be area hints. The rest will be location hints.
    """
    display_name = "Area Hint Percentage"
    range_start = 0
    range_end = 100
    default = 33


class LaserHints(Toggle):
    """
    If on, lasers will tell you where their items are if you walk close to them in-game.
    Only applies if Laser Shuffle is enabled.
    """
    display_name = "Laser Hints"


class DeathLink(Toggle):
    """
    If on, whenever you fail a puzzle (with some exceptions), you and everyone who is also on Death Link dies.
    The effect of a "death" in The Witness is a Bonk Trap.
    """
    display_name = "Death Link"


class DeathLinkAmnesty(Range):
    """
    The number of panel fails to allow before sending a death through Death Link.
    0 means every panel fail will send a death, 1 means every other panel fail will send a death, etc.
    """
    display_name = "Death Link Amnesty"
    range_start = 0
    range_end = 5
    default = 1


@dataclass
class TheWitnessOptions(PerGameCommonOptions):
    puzzle_randomization: PuzzleRandomization
    shuffle_symbols: ShuffleSymbols
    shuffle_doors: ShuffleDoors
    door_groupings: DoorGroupings
    shuffle_boat: ShuffleBoat
    shuffle_lasers: ShuffleLasers
    disable_non_randomized_puzzles: DisableNonRandomizedPuzzles
    shuffle_discarded_panels: ShuffleDiscardedPanels
    shuffle_vault_boxes: ShuffleVaultBoxes
    obelisk_keys: ObeliskKeys
    shuffle_EPs: ShuffleEnvironmentalPuzzles  # noqa: N815
    EP_difficulty: EnvironmentalPuzzlesDifficulty
    shuffle_postgame: ShufflePostgame
    victory_condition: VictoryCondition
    mountain_lasers: MountainLasers
    challenge_lasers: ChallengeLasers
    panel_hunt_total: PanelHuntTotal
    panel_hunt_required_percentage: PanelHuntRequiredPercentage
    panel_hunt_postgame: PanelHuntPostgame
    panel_hunt_discourage_same_area_factor: PanelHuntDiscourageSameAreaFactor
    early_caves: EarlyCaves
    early_symbol_item: EarlySymbolItem
    elevators_come_to_you: ElevatorsComeToYou
    trap_percentage: TrapPercentage
    trap_weights: TrapWeights
    puzzle_skip_amount: PuzzleSkipAmount
    hint_amount: HintAmount
    vague_hints: VagueHints
    area_hint_percentage: AreaHintPercentage
    laser_hints: LaserHints
    death_link: DeathLink
    death_link_amnesty: DeathLinkAmnesty
    shuffle_dog: ShuffleDog


witness_option_groups = [
    OptionGroup("Puzzles & Goal", [
        PuzzleRandomization,
        VictoryCondition,
        MountainLasers,
        ChallengeLasers,
    ]),
    OptionGroup("Panel Hunt Settings", [
        PanelHuntRequiredPercentage,
        PanelHuntTotal,
        PanelHuntPostgame,
        PanelHuntDiscourageSameAreaFactor,
    ], start_collapsed=True),
    OptionGroup("Locations", [
        ShuffleDiscardedPanels,
        ShuffleVaultBoxes,
        ShuffleEnvironmentalPuzzles,
        EnvironmentalPuzzlesDifficulty,
        ShufflePostgame,
        DisableNonRandomizedPuzzles,
    ]),
    OptionGroup("Progression Items", [
        ShuffleSymbols,
        ShuffleDoors,
        DoorGroupings,
        ShuffleLasers,
        ShuffleBoat,
        ObeliskKeys,
    ]),
    OptionGroup("Filler Items", [
        PuzzleSkipAmount,
        TrapPercentage,
        TrapWeights
    ]),
    OptionGroup("Hints", [
        HintAmount,
        VagueHints,
        AreaHintPercentage,
        LaserHints
    ]),
    OptionGroup("Misc", [
        EarlyCaves,
        ElevatorsComeToYou,
        DeathLink,
        DeathLinkAmnesty,
    ]),
    OptionGroup("Silly Options", [
        ShuffleDog,
    ])
]
