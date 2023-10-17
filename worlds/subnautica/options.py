import typing

from Options import Choice, Range, DeathLink, Toggle, DefaultOnToggle, StartInventoryPool
from .creatures import all_creatures, Definitions


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
    """When you die, everyone dies. Of course the reverse is true too.
    Note: can be toggled via in-game console command "deathlink"."""


option_definitions = {
    "swim_rule": SwimRule,
    "early_seaglide": EarlySeaglide,
    "free_samples": FreeSamples,
    "goal": Goal,
    "creature_scans": CreatureScans,
    "creature_scan_logic": AggressiveScanLogic,
    "death_link": SubnauticaDeathLink,
    "start_inventory_from_pool": StartInventoryPool,
}
