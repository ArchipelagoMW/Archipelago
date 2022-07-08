from Options import Choice


class ItemPool(Choice):
    """Valuable item pool moves all not progression relevant items to starting inventory and
    creates random duplicates of important items in their place."""
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


options = {
    "item_pool": ItemPool,
    "goal": Goal,
}
