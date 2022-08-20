from Options import Choice, Range, DeathLink
from .Creatures import all_creatures


class ItemPool(Choice):
    """Valuable item pool leaves all filler items in their vanilla locations and
    creates random duplicates of important items into freed spots."""
    display_name = "Item Pool"
    option_standard = 0
    option_valuable = 1


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
    """Place items on specific creature scans.
    Warning: Includes aggressive Leviathans."""
    display_name = "Creature Scans"
    range_end = len(all_creatures)


class SubnauticaDeathLink(DeathLink):
    """When you die, everyone dies. Of course the reverse is true too.
    Note: can be toggled via in-game console command "deathlink"."""


options = {
    "item_pool": ItemPool,
    "goal": Goal,
    "creature_scans": CreatureScans,
    "death_link": SubnauticaDeathLink,
}
