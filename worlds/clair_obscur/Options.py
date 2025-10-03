from dataclasses import dataclass

from Options import Choice, PerGameCommonOptions, StartInventory, OptionGroup, Toggle, Range, DeathLinkMixin


class Goal(Choice):
    """
    The victory condition for your run
    """

    display_name = "Goal"
    option_paintress = 0
    option_curator = 1
    option_painted_love = 2
    option_simon = 3

    default = 1

class ExcludeEndgameLocations(Choice):
    """
    Determines how to handle locations higher level than the set goal, if the goal is Paintress or Curator.
    Excluded: Locations won't be added to the pool.
    Filler: Locations will only contain filler items.
    Included: All locations are included.
    """
    internal_name = "exclude_endgame_locations"
    display_name = "Exclude Endgame Locations"
    option_excluded = 0
    option_filler = 1
    option_included = 2
    default = 0

class ExcludeEndlessTower(Choice):
    """
    Determines how to handle Endless Tower locations.
    Excluded: Locations won't be added to the pool.
    Filler: Locations will only contain filler items.
    Included: All locations are included.
    """
    internal_name = "exclude_endless_tower"
    display_name = "Exclude Endless Tower"
    option_excluded = 0
    option_filler = 1
    option_included = 2
    default = 2

class ShuffleLostGestrals(Toggle):
    """
    Shuffles the lost gestrals into the item pool.
    """
    internal_name = "shuffle_lost_gestrals"
    display_name = "Shuffle Lost Gestrals"

class ShuffleFreeAim(Toggle):
    """
    Shuffles the ability to shoot outside of battle into the pool.
    """
    internal_name = "shuffle_free_aim"
    display_name = "Shuffle Free Aim"
    default = 0

class AreaLogic(Choice):
    """
    Determines how many major area unlock items will be placed how early.
    Normal: Act 1 major areas won't be placed past Act 1; Forgotten Battlefield and Old Lumiere won't be placed behind
    Visages/Sirene; Visages and Sirene won't be placed behind The Monolith.
    Hard: Only half of the major areas will be placed in those segments.
    No Logic: Areas could be anywhere. You may need to grind world map enemies for a long time.
    """
    internal_name = "area_logic"
    display_name = "Area logic"
    option_normal = 1
    option_hard = 2
    option_no_logic = 0
    default = 1

class ShuffleCharacters(Toggle):
    """Shuffles characters into the item pool."""
    display_name = "Shuffle characters"

class StartingCharacter(Choice):
    """Determines which character you start with. Does nothing if Shuffle Characters is set to false."""
    internal_name = "starting_character"
    display_name = "Starting character"
    option_gustave = 0
    option_lune = 1
    option_maelle = 2
    option_sciel = 3
    option_monoco = 4
    option_verso = 5
    default = 0

class GearScaling(Choice):
    """How the levels of pictos and weapons you receive are determined.
    Sphere placement: Roughly scales pictos/weapons by the logical sphere they're placed in.
    Order received: As you receive more pictos/weapons, the levels of the next ones you receive will go up.
    Balanced random: Pictos/weapons have random levels assigned in an even spread.
    Full random: Exaclty what it says. There's no guarantee that you'll get high-level pictos... but you probably will."""
    internal_name = "gear_scaling"
    display_name = "Gear Scaling"
    option_sphere_placement = 0
    option_order_received = 1
    option_balanced_random = 2
    option_full_random = 3
    default = 0

class TrapChance(Range):
    """
    The chance for any filler item to be replaced with a trap.
    Currently, the only implemented trap is the Feet Trap.
    Feet Trap: plays the "My, what lovely feet" voice line and shows you some feet pics. Are you sure about this....?
    """
    display_name = "Trap Chance"
    range_start = 0
    range_end = 100
    default = 0

class ClairObscurStartInventory(StartInventory):
    """
    Start with these items
    """

@dataclass
class ClairObscurOptions(DeathLinkMixin, PerGameCommonOptions):
    goal: Goal
    char_shuffle: ShuffleCharacters
    shuffle_free_aim: ShuffleFreeAim
    exclude_endgame_locations: ExcludeEndgameLocations
    exclude_endless_tower: ExcludeEndlessTower
    gestral_shuffle: ShuffleLostGestrals
    starting_char: StartingCharacter
    gear_scaling: GearScaling
    area_logic: AreaLogic
    trap_chance: TrapChance

    start_inventory: ClairObscurStartInventory

OPTIONS_GROUP = [
    OptionGroup(
        "Item & Location Options", [
            ClairObscurStartInventory,
        ], False,
    ),
]