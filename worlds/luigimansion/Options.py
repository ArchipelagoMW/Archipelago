from dataclasses import dataclass

from Options import Toggle, Range, Option, PerGameCommonOptions


# Will look into feasibility of options later.


class StartWithBetterVacuum(Toggle):
    """Start with Poltergust 4000"""
    display_name = "Better Vacuum"


# These might end up being the same
class StartHiddenMansion(Toggle):
    """Begin in the Hidden Mansion"""
    display_name = "Hidden Mansion"


class SpeedySpirits(Toggle):
    """Adds Blue Ghosts and Gold Mice to location pool"""
    display_name = "Speedy Spirits"


class StartWithBooRadar(Toggle):
    """Start with Boo Radar"""
    display_name = "Boo Radar"


#   class DoorRando(Toggle):
#   "Keys wil open different doors than normal, and doors may require elements instead of keys"
#   display_name = "Door Randomization"
# Heavy logic editing required

class Toadsanity(Toggle):
    """Adds Toads to location pool"""
    display_name = "Toadsanity"


class Plants(Toggle):
    """Adds all plants to location pool"""
    display_name = "Plantsanity"


class Knocksanity(Toggle):
    """Adds every interactable, such a dressers and light fixtures, to the location pool"""
    display_name = "Interactables"


class MarioItems(Range):
    """How many Mario Items it takes to capture the Fortune-Teller. 0 = Starts Capturable"""
    display_name = "Fortune-Teller Requirements"
    range_start = 0
    range_end = 5
    default = 5


class WashroomBooCount(Range):
    """Set the number of Boos required to reach the 1F Washroom. 0 = Starts Open"""
    display_name = "Washroom Boo Count"
    range_start = 0
    range_end = 50
    default = 5


class BalconyBooCount(Range):
    """Set the number of Boos required to reach the Balcony. 0 = Starts Open"""
    display_name = "Washroom Boo Count"
    range_start = 0
    range_end = 45
    default = 20


class FinalBooCount(Range):
    """Set the number of Boos required to reach the Secret Altar. 0 = Starts Open"""
    display_name = "Altar Boo Count"
    range_start = 0
    range_end = 50
    default = 40


class Boosanity(Toggle):
    """Turns Boos into Items and Locations"""
    display_name = "Boosanity"


class PortraitGhosts(Toggle):
    """Turn Portrait Ghosts into checks in addition to their clear chests"""
    display_name = "Portrait Ghosts"


class Enemizer(Toggle):
    """
    Ghosts in room encounters have random elements. Be aware that softlocks are possible and common with this option on.
    Be Ready.
    """
    display_name = "Enemizer"


@dataclass
class LMOptions(PerGameCommonOptions):
    good_vacuum: StartWithBetterVacuum
    boo_radar: StartWithBooRadar
    hidden_mansion: StartHiddenMansion
    speedy_spirits: SpeedySpirits
    toadsanity: Toadsanity
    plantsanity: Plants
    knocksanity: Knocksanity
    mario_items: MarioItems
    washroom_boo_count: WashroomBooCount
    balcony_boo_count: BalconyBooCount
    final_boo_count: FinalBooCount
    boosanity: Boosanity
    portrait_ghosts: PortraitGhosts
    enemizer: Enemizer
