from .Logic import MetroidPrimeLogic as logic
from BaseClasses import Region
from .PrimeOptions import MetroidPrimeOptions
from .Locations import tallon_location_table, magmoor_location_table, mines_location_table, chozo_location_table, \
    phen_location_table, MetroidPrimeLocation


def create_regions(self, final_boss_selection):
    # create all regions and populate with locations
    menu = Region("Menu", self.player, self.multiworld)
    self.multiworld.regions.append(menu)

    tallon_overworld = Region("Tallon Overworld", self.player, self.multiworld)
    tallon_overworld.add_locations(tallon_location_table, MetroidPrimeLocation)
    self.multiworld.regions.append(tallon_overworld)

    chozo_ruins = Region("Chozo Ruins", self.player, self.multiworld)
    chozo_ruins.add_locations(chozo_location_table, MetroidPrimeLocation)
    self.multiworld.regions.append(chozo_ruins)

    magmoor_caverns = Region("Magmoor Caverns", self.player, self.multiworld)
    magmoor_caverns.add_locations(magmoor_location_table, MetroidPrimeLocation)
    self.multiworld.regions.append(magmoor_caverns)

    phendrana_drifts = Region("Phendrana Drifts", self.player, self.multiworld)
    phendrana_drifts.add_locations(phen_location_table, MetroidPrimeLocation)
    self.multiworld.regions.append(phendrana_drifts)

    phazon_mines = Region("Phazon Mines", self.player, self.multiworld)
    phazon_mines.add_locations(mines_location_table, MetroidPrimeLocation)
    self.multiworld.regions.append(phazon_mines)

    impact_crater = Region("Impact Crater", self.player, self.multiworld)
    self.multiworld.regions.append(impact_crater)

    mission_complete = Region("Mission Complete", self.player, self.multiworld)
    self.multiworld.regions.append(mission_complete)

    # entrances
    menu.connect(tallon_overworld)

    tallon_overworld.connect(chozo_ruins, "West Chozo Elevator")
    tallon_overworld.connect(magmoor_caverns, "East Magmoor Elevator", lambda state: (
            logic.prime_has_missiles(state, self.multiworld, self.player) and
            logic.prime_can_heat(state, self.multiworld, self.player)))
    tallon_overworld.connect(phazon_mines, "East Mines Elevator", lambda state: (
        logic.prime_frigate(state, self.multiworld, self.player)))
    if (final_boss_selection == 0 or
            final_boss_selection == 2):
        tallon_overworld.connect(impact_crater, "Crater Access", lambda state: (
                logic.prime_has_missiles(state, self.multiworld, self.player) and
                (logic.prime_artifact_count(state, self.multiworld, self.player) == 12) and
                state.has_all({"Wave Beam", "Ice Beam", "Plasma Beam", "Thermal Visor", "X-Ray Visor", "Phazon Suit",
                               "Space Jump Boots"}, self.player) and
                logic.prime_etank_count(state, self.multiworld, self.player) >= 8))
    elif final_boss_selection == 1:
        tallon_overworld.connect(mission_complete, "Mission Complete", lambda state: (
                logic.prime_has_missiles(state, self.multiworld, self.player) and
                (logic.prime_artifact_count(state, self.multiworld, self.player) == 12) and
                (state.has("Plasma Beam", self.player) or logic.prime_can_super(state, self.multiworld,
                                                                                  self.player)) and
                logic.prime_etank_count(state, self.multiworld, self.player) >= 8))
    elif self.MetroidPrimeOptions.final_bosses == 3:
        tallon_overworld.connect(mission_complete, "Mission Complete", lambda state: (
                logic.prime_has_missiles(state, self.multiworld, self.player) and
                (logic.prime_artifact_count(state, self.multiworld, self.player) == 12)))

    chozo_ruins.connect(magmoor_caverns, "North Magmoor Elevator", lambda state: (
            logic.prime_has_missiles(state, self.multiworld, self.player) and
            logic.prime_can_heat(state, self.multiworld, self.player) and
            state.has("Morph Ball", self.player)))

    magmoor_caverns.connect(phendrana_drifts, "Magmoor-Phendrana Elevators", lambda state: (
            logic.prime_front_phen(state, self.multiworld, self.player) or
            logic.prime_late_magmoor(state, self.multiworld, self.player)))
    magmoor_caverns.connect(phazon_mines, "West Mines Elevator", lambda state: (
            logic.prime_late_magmoor(state, self.multiworld, self.player) and state.has("Ice Beam", self.player)))

    if (final_boss_selection == 0 or
            final_boss_selection == 2):
        impact_crater.connect(mission_complete)
