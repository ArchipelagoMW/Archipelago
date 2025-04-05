import typing
from dataclasses import dataclass
from functools import cached_property

from Options import (
    Choice,
    Range,
    DeathLink,
    Toggle,
    DefaultOnToggle,
    StartInventoryPool,
    ItemDict,
    PerGameCommonOptions,
)

from .creatures import all_creatures, Definitions
from .items import ItemType, item_names_by_type


class SwimRule(Choice):
    """What logic considers ok swimming distances.
    Easy: +200 depth from any max vehicle depth.
    Normal: +400 depth from any max vehicle depth.
    Warning: Normal can expect you to death run to a location (No viable return trip).
    Hard: +600 depth from any max vehicle depth.
    Warning: Hard may require bases, deaths, glitches, multi-tank inventory or other depth extending means.
    Items: Expected depth is extended by items like seaglide, ultra glide fins and capacity tanks.
    """
    display_name = "Swim Rule"
    option_easy = 0
    option_normal = 1
    option_hard = 2
    option_items_easy = 3
    option_items_normal = 4
    option_items_hard = 5

    @property
    def base_depth(self) -> int:
        return [200, 400, 600][self.value % 3]

    @property
    def consider_items(self) -> bool:
        return self.value > 2


class EarlySeaglide(DefaultOnToggle):
    """Make sure 2 of the Seaglide Fragments are available in or near the Safe Shallows (Sphere 1 Locations)."""
    display_name = "Early Seaglide"


class FreeSamples(Toggle):
    """Get free items with your blueprints.
    Items that can go into your inventory are awarded when you unlock their blueprint through Archipelago."""
    display_name = "Free Samples"


class Goal(Choice):
    """Goal to complete.
    Launch: Leave the planet.
    Free: Disable quarantine.
    Infected: Reach maximum infection level.
    Drive: Repair the Aurora's Drive Core"""
    auto_display_name = True
    display_name = "Goal"
    option_launch = 0
    option_free = 1
    option_infected = 2
    option_drive = 3

    def get_event_name(self) -> str:
        return {
            self.option_launch: "Neptune Launch",
            self.option_infected: "Full Infection",
            self.option_free: "Disable Quarantine",
            self.option_drive: "Repair Aurora Drive"
        }[self.value]


class CreatureScans(Range):
    """Place items on specific, randomly chosen, creature scans.
    Warning: Includes aggressive Leviathans."""
    display_name = "Creature Scans"
    range_end = len(all_creatures)


class AggressiveScanLogic(Choice):
    """By default (Stasis), aggressive Creature Scans are logically expected only with a Stasis Rifle.
    Containment: Removes Stasis Rifle as expected solution and expects Alien Containment instead.
    Either: Creatures may be expected to be scanned via Stasis Rifle or Containment, whichever is found first.
    None: Aggressive Creatures are assumed to not need any tools to scan.
    Removed: No Creatures needing Stasis or Containment will be in the pool at all.

    Note: Containment, Either and None adds Cuddlefish as an option for scans.
    Note: Stasis, Either and None adds unhatchable aggressive species, such as Warper.
    Note: This is purely a logic expectation, and does not affect gameplay, only placement."""
    display_name = "Aggressive Creature Scan Logic"
    option_stasis = 0
    option_containment = 1
    option_either = 2
    option_none = 3
    option_removed = 4

    def get_pool(self) -> typing.List[str]:
        if self == self.option_removed:
            return Definitions.all_creatures_presorted_without_aggressive_and_containment
        elif self == self.option_stasis:
            return Definitions.all_creatures_presorted_without_containment
        elif self == self.option_containment:
            return Definitions.all_creatures_presorted_without_stasis
        else:
            return Definitions.all_creatures_presorted


class SubnauticaDeathLink(DeathLink):
    __doc__ = DeathLink.__doc__ + "\n\n    Note: can be toggled via in-game console command \"deathlink\"."


class FillerItemsDistribution(ItemDict):
    """Random chance weights of various filler resources that can be obtained.
    Available items: """
    __doc__ += ", ".join(f"\"{item_name}\"" for item_name in item_names_by_type[ItemType.resource])
    valid_keys = sorted(item_names_by_type[ItemType.resource])
    default = {item_name: 1 for item_name in item_names_by_type[ItemType.resource]}
    display_name = "Filler Items Distribution"

    @cached_property
    def weights_pair(self) -> typing.Tuple[typing.List[str], typing.List[int]]:
        from itertools import accumulate
        return list(self.value.keys()), list(accumulate(self.value.values()))


class RadiationRule(Choice):
    """By default (None), checks inside the radiation zone are logically expected only with a Radiation Suit.
    None: Always require the Radiation Suit inside the radiation zone.
    Outer: Checks may be expected on the outer parts of the radiation zone (but still inside it)
    Inner: As Outer, but checks may also be expected on the inner parts of the radiation zone (i.e., Lifepod 4)
    All: All locations will be considered accessible without a Radiation Suit (including inside the Aurora).
    Warning: 'All' can be _very_ hard.
    """

    display_name = "Radiation Rule"
    option_none = 0
    option_outer = 1
    option_inner = 2
    option_all = 3

    @property
    def distance(self) -> int:
        # Distances were computed using the locations of the databoxes in locations.py
        # Outer includes the following locations:
        # - Bulb Zone West Wreck (800 units from Aurora)
        # - Bulb Zone East Wreck (827 units from Aurora)
        # - Grassy Plateaus East Wreck (940 units from Aurora)
        # - Lifepod 6 (830 units from Aurora)
        # - Lifepod 12 (780 units from Aurora)
        # Inner adds Lifepod 4 (460 units) to the accessible locations
        return [950, 750, 450, 0][self.value]


@dataclass
class SubnauticaOptions(PerGameCommonOptions):
    swim_rule: SwimRule
    early_seaglide: EarlySeaglide
    free_samples: FreeSamples
    goal: Goal
    creature_scans: CreatureScans
    creature_scan_logic: AggressiveScanLogic
    death_link: SubnauticaDeathLink
    start_inventory_from_pool: StartInventoryPool
    filler_items_distribution: FillerItemsDistribution
    radiation_rule: RadiationRule
