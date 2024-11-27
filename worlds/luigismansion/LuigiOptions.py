from dataclasses import dataclass

from Options import Toggle, Range, Option, PerGameCommonOptions, Choice, StartInventoryPool


# Will look into feasibility of options later.

class LuigiWalkSpeed(Choice):
    """Choose how fast Luigi moves"""
    display_name = "Walk Speed"
    option_normal_speed = 0
    option_kinda_fast = 1
    option_schmoovin = 2
    default = 0


class RandomMusic(Toggle):
    """Randomize Music"""
    display_name = "Music Randomization"


class BetterVacuum(Choice):
    """Choose whether to include the Poltergust 4000"""
    display_name = "Poltergust 4000"
    option_start_with = 0
    option_include = 1
    option_exclude = 2
    default = 1


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


class Plants(Toggle):
    """Adds all plants to location pool"""
    display_name = "Plantsanity"


class PickupAnim(Toggle):
    """Disable Luigi's pickup animations"""
    display_name = "Pickup Animation"


class Toadsanity(Toggle):
    """Add Toads as locations to be checked"""
    display_name = "Toadsanity"


class Furnisanity(Toggle):
    """
    Adds every interactable, such a dressers, paintings, candles, and light fixtures, to the location pool
    """
    display_name = "Furnisanity"


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
    display_name = "Balcony Boo Count"
    range_start = 0
    range_end = 35
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


class Enemizer(Choice):
    """
    Choose if and how ghosts are randomized.
    0 = No ghost randomization
    1 = Randomized ghost elements and waves
    2 = Remove ghost elements, randomize waves
    """
    display_name = "Enemizer"
    option_vanilla = 0
    option_randomized_elements = 1
    option_no_elements = 2


class DoorRando(Toggle):
    """Randomize which doors are locked or unlocked in the mansion."""
    display_name = "Door Randomization"


class LuigiFearAnim(Toggle):
    """Turn off Luigi being scared by ghosts if they spawn close to him"""
    display_name = "Courageous Luigi"


class Goal(Choice):
    """
    Determines when victory is achieved in your playthrough.

    King Boo: Defeat King Boo in the Secret Altar
    Rank Requirement: Gather enough money to reach the specified rank before beating King Boo *experimental
    """
    display_name = "Goal"
    option_king_boo = 0
    option_rank_requirement = 1
    default = 0


class RankRequirement(Choice):
    """
    If Rank Requirement is chosen as goal, choose the required rank (H to A) with A being the highest
    """
    display_name = "Rank Requirement"
    option_rank_h = 0
    option_rank_g = 1
    option_rank_f = 2
    option_rank_e = 3
    option_rank_d = 4
    option_rank_c = 5
    option_rank_b = 6
    option_rank_a = 7


@dataclass
class LMOptions(PerGameCommonOptions):
    goal: Goal
    rank_requirement: RankRequirement
    walk_speed: LuigiWalkSpeed
    good_vacuum: BetterVacuum
    boo_radar: StartWithBooRadar
    hidden_mansion: StartHiddenMansion
    fear_animation: LuigiFearAnim
    pickup_animation: PickupAnim
    random_music: RandomMusic
    door_rando: DoorRando
    toadsanity: Toadsanity
    plantsanity: Plants
    furnisanity: Furnisanity
    boosanity: Boosanity
    portrait_ghosts: PortraitGhosts
    speedy_spirits: SpeedySpirits
    mario_items: MarioItems
    washroom_boo_count: WashroomBooCount
    balcony_boo_count: BalconyBooCount
    final_boo_count: FinalBooCount
    enemizer: Enemizer
    start_inventory_from_pool: StartInventoryPool
