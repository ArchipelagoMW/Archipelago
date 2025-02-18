from dataclasses import dataclass

from Options import Toggle, Range, Option, PerGameCommonOptions, Choice, StartInventoryPool


# Will look into feasibility of options later.

class Deathlink(Toggle):
    """All players who have deathlink enabled will die when one person with deathlink on does"""
    display_name = "Deathlink"


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


class BundleWeight(Range):
    """Set the weight for how often coin & bill bundles get chosen as filler. Default is 10"""
    display_name = "Money Bundle Weight"
    range_start = 0
    range_end = 100
    default = 10


class CoinWeight(Range):
    """Set the weight for how often coins get chosen as filler. Default is 15"""
    display_name = "Coin Weight"
    range_start = 0
    range_end = 100
    default = 15


class BillWeight(Range):
    """Set the weight for how often bills get chosen as filler. Default is 10"""
    display_name = "Bill Weight"
    range_start = 0
    range_end = 100
    default = 10


class BarsWeight(Range):
    """Set the weight for how often gold bars get chosen as filler. Default is 10"""
    display_name = "Gold Bars Weight"
    range_start = 0
    range_end = 100
    default = 10


class GemsWeight(Range):
    """Set the weight for how often gemstones get chosen as filler. Default is 5"""
    display_name = "Gems Weight"
    range_start = 0
    range_end = 100
    default = 5


class PoisonTrapWeight(Range):
    """Set the weight for how often poison mushrooms get chosen as traps. Default is 15"""
    display_name = "Poison Trap Weight"
    range_start = 0
    range_end = 100
    default = 15


class BombWeight(Range):
    """Set the weight for how often bombs get chosen as traps. Default is 15"""
    display_name = "Bomb Weight"
    range_start = 0
    range_end = 100
    default = 15


class IceTrapWeight(Range):
    """Set the weight for how often ice traps get chosen as traps. Default is 15"""
    display_name = "Ice Trap Weight"
    range_start = 0
    range_end = 100
    default = 15


class BananaTrapWeight(Range):
    """Set the weight for how often bananas get chosen as traps. Default is 15"""
    display_name = "Banana Trap Weight"
    range_start = 0
    range_end = 100
    default = 15

class NothingWeight(Range):
    """Set the weight for how often nothing is chosen as filler. Default is 40"""
    display_name = "'Nothing' Weight"
    range_start = 0
    range_end = 100
    default = 40

class HeartWeight(Range):
    """Set the weight for how often hearts get chosen as filler. Default is 10"""
    display_name = "Heart Weight"
    range_start = 0
    range_end = 100
    default = 10


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
    """Adds Blue Ghosts to location pool"""
    display_name = "Speedy Spirits"


class StartWithBooRadar(Choice):
    """
    Start with Boo Radar
    0 = Start with Boo Radar
    1 = Boo Radar in pool
    2 = No Boo Radar - Boo Gates and Boosanity will be disabled if excluded
    """
    display_name = "Boo Radar"
    option_start_with = 0
    option_include = 1
    option_exclude = 2
    default = 1


class PortraitHints(Toggle):
    """Choose to add hints to the scans of the Portrait Ghosts in the mansions"""
    display_name = "Portrait Ghost Hints"


class HintDistribution(Choice):
    """Choose the level of hint from in-game hints. Will affect Portrait Ghost hints if the option is on."""
    display_name = "Hint Distribution"
    option_balanced = 0
    option_junk = 1
    option_chaos = 2
    option_strong = 3
    option_vague = 4
    option_disabled = 5
    default = 0


class Plants(Toggle):
    """Adds all plants to location pool"""
    display_name = "Plantsanity"


class PickupAnim(Toggle):
    """Disable Luigi's pickup animations"""
    display_name = "Pickup Animation"


class Toadsanity(Toggle):
    """Add Toads as locations to be checked. These are remote only checks."""
    display_name = "Toadsanity"


class Lightsanity(Toggle):
    """Adds the act of lighting up rooms as locations. These are remote only checks"""
    display_name = "Lightsanity"


class Walksanity(Toggle):
    """Adds the act of visiting rooms as locations. These are remote only checks"""
    display_name = "Walksanity"


class Furnisanity(Toggle):
    """
    Adds interactable objects, such a dressers, paintings, candles, and light fixtures, to the location pool
    """
    display_name = "Furnisanity"


class BooGates(Toggle):
    """
    Toggle the events that prevent progress unless a certain number of boos have been caught

    Default to on. If this is turned off, the Boo Count options are ignored, and Boo Radar becomes filler.
    """
    display_name = "Boo Gates"
    default = 1


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
    range_end = 36
    default = 20


class FinalBooCount(Range):
    """Set the number of Boos required to reach the Secret Altar. 0 = Starts Open"""
    display_name = "Altar Boo Count"
    range_start = 0
    range_end = 50
    default = 40


class Boosanity(Toggle):
    """Turns Boos into Items and Locations. These are remote only checks."""
    display_name = "Boosanity"

class Portrification(Toggle):
    """Turn Portrait Ghosts into checks in addition to their clear chests. These are remote only checks."""
    display_name = "Portrification"


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
    default = 0


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
    portrait_hints: PortraitHints
    hint_distribution: HintDistribution
    toadsanity: Toadsanity
    plantsanity: Plants
    furnisanity: Furnisanity
    boosanity: Boosanity
    portrification: Portrification
    lightsanity: Lightsanity
    walksanity: Walksanity
    speedy_spirits: SpeedySpirits
    boo_gates: BooGates
    mario_items: MarioItems
    washroom_boo_count: WashroomBooCount
    balcony_boo_count: BalconyBooCount
    final_boo_count: FinalBooCount
    bundle_weight: BundleWeight
    coin_weight: CoinWeight
    bill_weight: BillWeight
    bars_weight: BarsWeight
    gems_weight: GemsWeight
    poison_trap_weight: PoisonTrapWeight
    bomb_trap_weight: BombWeight
    ice_trap_weight: IceTrapWeight
    banana_trap_weight: BananaTrapWeight
    nothing_weight: NothingWeight
    heart_weight: HeartWeight
    enemizer: Enemizer
    deathlink: Deathlink
    start_inventory_from_pool: StartInventoryPool
