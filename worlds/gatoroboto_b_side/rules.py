from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import CollectionState
from worlds.generic.Rules import add_rule, set_rule

if TYPE_CHECKING:
    from .world import GatoRobotoWorld


def set_all_rules(world: GatoRobotoWorld) -> None:
    # In order for AP to generate an item layout that is actually possible for the player to complete,
    # we need to define rules for our Entrances and Locations.
    # Note: Regions do not have rules, the Entrances connecting them do!
    # We'll do entrances first, then locations, and then finally we set our victory condition.

    set_all_entrance_rules(world)
    set_all_location_rules(world)
    set_completion_condition(world)

def set_all_entrance_rules(world: GatoRobotoWorld) -> None:
    to_nexus = world.get_entrance("Zu Nexus")
    to_landing_site = world.get_entrance("Zu Landing Site")
    #to_aqueducts = world.get_entrance("Zu Aqueducts")
    to_heater_core = world.get_entrance("Zu Heater Core")
    to_ventilation = world.get_entrance("Zu Ventilation")
    to_incubator = world.get_entrance("Zu Incubator")

    set_rule(to_nexus, lambda state: state.has("Rocket", world.player))
    set_rule(to_landing_site, lambda state: state.has("Rocket", world.player))
    #set_rule(to_aqueducts, labda state: True)
    set_rule(to_heater_core, lambda state: state.has_any(("Rocket", "Spin Jump"), world.player))
    set_rule(to_ventilation, lambda state: ((world.options.gato_tech <= 2) and state.has("Rocket", world.player)) or ((world.options.gato_tech == 3) and world.options.use_smallmech and state.has("Rocket", world.player)) or ((world.options.gato_tech == 3) and state.has("Dash", world.player) and state.has("Rocket", world.player)))
    '''if world.options.use_smallmech:
        set_rule(to_ventilation, lambda state: state.has("Rocket", world.player))
    else:
        set_rule(to_ventilation, lambda state: state.has_all(("Rocket", "Dash"), world.player))'''
    set_rule(to_incubator, lambda state: state.has("<Completed all areas>", world.player) and state.has("Decoder", world.player))

def set_all_location_rules(world: GatoRobotoWorld) -> None:
    vhs = ("Palette 02", "Palette 03", "Palette 04", "Palette 05", "Palette 06", "Palette 07", "Palette 08",
           "Palette 09", "Palette 10", "Palette 11", "Palette 12", "Palette 13", "Palette 14", "Palette 15")

    current_location = world.get_location("VHS (Landing Site-1810)")
    set_rule(current_location, lambda state: state.has("Rocket", world.player))
    current_location = world.get_location("Health Upgrade (Landing Site-1812)")
    set_rule(current_location, lambda state: state.has("Rocket", world.player))
    current_location = world.get_location("Decoder (Landing Site-0807)")
    set_rule(current_location, lambda state: state.has("<Completed all areas>", world.player) or (state.has("Spin Jump", world.player) and state.has("Dash", world.player) and state.has("Hopper", world.player)) or (state.has("Spin Jump", world.player) and state.has("Rocket", world.player)) or ((world.options.gato_tech >= 2) and state.has("Dash", world.player) and state.has("Rocket", world.player) and world.options.use_smallmech))

    current_location = world.get_location("VHS (Nexus-0914)")
    set_rule(current_location, lambda state: (state.has("Water Level", world.player, 2) and state.has("Rocket", world.player)) or (world.options.use_watermech and state.has("Rocket", world.player)))
    current_location = world.get_location("Health Upgrade (Nexus-1014)")
    set_rule(current_location, lambda state: (state.has("Rocket", world.player) and state.has("Cooler", world.player)) or (state.has("Dash", world.player) and state.has("Spin Jump", world.player)) or (state.has("Rocket", world.player) and state.has("Spin Jump", world.player)) or ((world.options.gato_tech >= 2) and state.has("Dash", world.player) and state.has("Rocket", world.player)) or ((world.options.gato_tech >= 2) and state.has("Water Level", world.player, 2) and state.has("Rocket", world.player) and world.options.use_smallmech and "Upwarp") or ((world.options.gato_tech >= 2) and state.has("Spin Jump", world.player)) or (False and "Ultrahard" and state.has("Rocket", world.player)))
    current_location = world.get_location("VHS (Nexus-1413)")
    set_rule(current_location, lambda state: (state.has("Spin Jump", world.player) and state.has("Rocket", world.player)) or (world.options.use_smallmech and state.has("Rocket", world.player) and state.has("Dash", world.player)) or (state.has("Cooler", world.player) and state.has("Rocket", world.player) and state.has("Dash", world.player)) or (state.has("Spin Jump", world.player) and state.has("Dash", world.player) and state.has("Hopper", world.player)) or ((world.options.gato_tech >= 2) and state.has("Spin Jump", world.player)) or ((world.options.gato_tech >= 2)) or ((world.options.gato_tech == 3) and state.has("Dash", world.player) and state.has("Rocket", world.player)))
    current_location = world.get_location("VHS (Nexus-2113)")
    set_rule(current_location, lambda state: ((world.options.gato_tech == 3)) or (state.has("Vent Level", world.player, 3) and state.has("Rocket", world.player)) or (state.has("Vent Level", world.player, 3) and state.has("Spin Jump", world.player)))
    current_location = world.get_location("Health Upgrade (Nexus-2314)")
    set_rule(current_location, lambda state: (state.has("Rocket", world.player)))
    current_location = world.get_location("Rebba quest 1 (Nexus-1716)")
    set_rule(current_location, lambda state: state.has_from_list(vhs, world.player, 7))
    current_location = world.get_location("Rebba quest 2 (Nexus-1716)")
    set_rule(current_location, lambda state: state.has_all(vhs, world.player))
    current_location = world.get_location("Completed all areas (Nexus)")
    set_rule(current_location, lambda state: (state.has("Water Level", world.player, 3) and state.has("Lava Cooled", world.player) and state.has("Vent Level", world.player, 3)))

    current_location = world.get_location("Health Upgrade (Aqueducts-0406)")
    set_rule(current_location, lambda state: (state.has("Water Level", world.player, 1) and state.has("Rocket", world.player)) or (world.options.use_watermech and state.has("Rocket", world.player)))
    current_location = world.get_location("VHS (Aqueducts-1106)")
    set_rule(current_location, lambda state: (state.has("Water Level", world.player, 2) and state.has("Rocket", world.player)) or (world.options.use_watermech and state.has("Rocket", world.player)))
    current_location = world.get_location("Health Upgrade (Aqueducts-1606)")
    set_rule(current_location, lambda state: (state.has("Water Level", world.player, 2) and state.has("Rocket", world.player)) or (world.options.use_watermech and state.has("Rocket", world.player)))
    current_location = world.get_location("VHS (Aqueducts-2106)")
    set_rule(current_location, lambda state: (state.has("Water Level", world.player, 2) and state.has("Rocket", world.player)))
    current_location = world.get_location("Water Level (Aqueducts-1603)")
    set_rule(current_location, lambda state: (state.has("Water Level", world.player, 1) and state.has("Rocket", world.player)) or (world.options.use_watermech and state.has("Rocket", world.player)))
    current_location = world.get_location("Water Level (Aqueducts-1908)")
    set_rule(current_location, lambda state: (state.has("Water Level", world.player, 2) and state.has("Rocket", world.player)) or (world.options.use_watermech and state.has("Rocket", world.player)))
    current_location = world.get_location("Spin Jump (Aqueducts-2410)")
    set_rule(current_location, lambda state: (state.has("Water Level", world.player, 2) and state.has("Rocket", world.player)) or (world.options.use_watermech and state.has("Rocket", world.player)))
    current_location = world.get_location("VHS (Aqueducts-0707)")
    set_rule(current_location, lambda state: (state.has("Water Level", world.player, 3) and state.has("Rocket", world.player) and state.has("Spin Jump", world.player)) or (world.options.use_watermech and state.has("Rocket", world.player) and state.has("Spin Jump", world.player)))

    current_location = world.get_location("VHS (Heater Core-1916)")
    set_rule(current_location, lambda state: (state.has("Lava Cooled", world.player) and state.has("Rocket", world.player)))
    current_location = world.get_location("VHS (Heater Core-1318)")
    set_rule(current_location, lambda state: (state.has("Lava Cooled", world.player) and state.has("Rocket", world.player)))
    current_location = world.get_location("Health Upgrade (Heater Core-1713)")
    set_rule(current_location, lambda state: (state.has("Lava Cooled", world.player) and state.has("Rocket", world.player)))
    current_location = world.get_location("Health Upgrade (Heater Core-0417)")
    set_rule(current_location, lambda state: (state.has("Lava Cooled", world.player) and state.has("Rocket", world.player)))
    current_location = world.get_location("Dash (Heater Core-1114)")
    set_rule(current_location, lambda state: (state.has("Rocket", world.player)))
    current_location = world.get_location("VHS (Heater Core-0414)")
    set_rule(current_location, lambda state: ((world.options.gato_tech == 3) and state.has("Lava Cooled", world.player) and state.has("Rocket", world.player) and world.options.use_smallmech) or ((world.options.gato_tech == 3) and state.has("Lava Cooled", world.player) and state.has("Rocket", world.player) and state.has("Dash", world.player)) or ((world.options.gato_tech <= 2) and state.has("Lava Cooled", world.player) and state.has("Rocket", world.player)))
    if (world.options.gato_tech == 3) and not world.options.use_smallmech:
        current_location = world.get_location("Cooler (Heater Core-0113)")
        set_rule(current_location, lambda state: (world.options.use_smallmech and state.has("Rocket", world.player)) or (state.has("Rocket", world.player) and state.has("Dash", world.player)) or (state.has("Spin Jump", world.player) and state.has("Dash", world.player)))
        current_location = world.get_location("Lava Cooled (Heater Core-0015)")
        set_rule(current_location, lambda state: (world.options.use_smallmech and state.has("Rocket", world.player)) or (state.has("Rocket", world.player) and state.has("Dash", world.player)) or (state.has("Spin Jump", world.player) and state.has("Dash", world.player)))
    else:
        current_location = world.get_location("Cooler (Heater Core-0113)")
        set_rule(current_location, lambda state: (world.options.use_smallmech and state.has("Rocket", world.player)) or (state.has("Dash", world.player) and state.has("Rocket", world.player)))
        current_location = world.get_location("Lava Cooled (Heater Core-0015)")
        set_rule(current_location, lambda state: (world.options.use_smallmech and state.has("Rocket", world.player)) or (state.has("Dash", world.player) and state.has("Rocket", world.player)))

    current_location = world.get_location("Vent Level (Ventilation-1113)")
    set_rule(current_location, lambda state: True)
    current_location = world.get_location("Vent Level (Ventilation-0521)")
    set_rule(current_location, lambda state: (state.has("<Smallmech entry>", world.player)) or (state.has("Vent Level", world.player, 1)) or ((world.options.gato_tech == 3)))
    current_location = world.get_location("VHS (Ventilation-0517)")
    set_rule(current_location, lambda state: (state.has("Vent Level", world.player, 1)) or ((world.options.gato_tech >= 2) and state.has("<Smallmech entry>", world.player)) or ((world.options.gato_tech == 3)))
    current_location = world.get_location("Vent Level (Ventilation-1122)")
    set_rule(current_location, lambda state: (state.has("<RightSide entry>", world.player) and state.has("Spin Jump", world.player)) or (world.options.use_smallmech and state.has("Spin Jump", world.player) and state.has("Dash", world.player) and state.has("Hopper", world.player)) or ((world.options.gato_tech >= 2) and state.has("<RightSide entry>", world.player)) or ((world.options.gato_tech >= 2) and state.has("<Smallmech entry>", world.player) and state.has("Spin Jump", world.player)))
    current_location = world.get_location("Health Upgrade (Ventilation-0815)")
    set_rule(current_location, lambda state: (state.has("Vent Level", world.player, 1)) or (state.has("<RightSide entry>", world.player)))
    current_location = world.get_location("VHS (Ventilation-1613)")
    set_rule(current_location, lambda state: (state.has("<RightSide entry>", world.player)))
    current_location = world.get_location("Bigshot (Ventilation-1718)")
    set_rule(current_location, lambda state: (state.has("<RightSide entry>", world.player)))

    if world.options.use_smallmech:
        current_location = world.get_location("Smallmech entry (Ventilation)")
        set_rule(current_location, lambda state:  (world.options.use_smallmech and state.has("Spin Jump", world.player) and state.has("Water Level", world.player, 3) and state.has("Cooler", world.player)) or (world.options.use_smallmech and state.has("Spin Jump", world.player) and state.has("Water Level", world.player, 3) and state.has("Dash", world.player) and state.has("Hopper", world.player)) or ((world.options.gato_tech >= 2) and world.options.use_smallmech and state.has("Spin Jump", world.player) and state.has("Water Level", world.player, 3)))
    current_location = world.get_location("RightSide entry (Ventilation)")
    set_rule(current_location, lambda state: (state.has("Vent Level", world.player, 3)) or (state.has("Vent Level", world.player, 1) and state.has("<Smallmech entry>", world.player) and state.has("Cooler", world.player) and state.has("Dash", world.player)) or ((world.options.gato_tech >= 2) and state.has("Vent Level", world.player, 1) and state.has("<Smallmech entry>", world.player) and state.has("Spin Jump", world.player)))

    current_location = world.get_location("VHS (Incubator-1513)")
    set_rule(current_location, lambda state: (state.has("Rocket", world.player)))
    current_location = world.get_location("Health Upgrade (Incubator-2413)")
    set_rule(current_location, lambda state: (state.has("Hopper", world.player)))

    current_location = world.get_location("Victory")
    set_rule(current_location, lambda state: state.has("Rocket", world.player) and state.has("Dash", world.player))

def set_completion_condition(world: GatoRobotoWorld) -> None:
    world.multiworld.completion_condition[world.player] = lambda state: state.has("Victory", world.player)
