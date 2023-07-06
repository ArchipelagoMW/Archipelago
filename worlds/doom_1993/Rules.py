# This file is auto generated. More info: https://github.com/Daivuk/apdoom

from typing import TYPE_CHECKING
from worlds.generic.Rules import set_rule

if TYPE_CHECKING:
    from . import DOOM1993World


def set_rules(doom_1993_world: "DOOM1993World"):
    player = doom_1993_world.player
    world = doom_1993_world.multiworld

    # Hangar (E1M1) - E1M1
    set_rule(world.get_entrance("Mars -> Hangar (E1M1) Main", player), lambda state: state.has("Hangar (E1M1)", player, 1))

    # Nuclear Plant (E1M2) - E1M2
    set_rule(world.get_entrance("Mars -> Nuclear Plant (E1M2) Main", player), lambda state: state.has("Nuclear Plant (E1M2)", player, 1) and state.has("Shotgun", player, 1))
    set_rule(world.get_entrance("Mars -> Nuclear Plant (E1M2) Red", player), lambda state: state.has("Nuclear Plant (E1M2)", player, 1) and state.has("Shotgun", player, 1) and (state.has("Nuclear Plant (E1M2) - Red keycard", player, 1)))

    # Toxin Refinery (E1M3) - E1M3
    set_rule(world.get_entrance("Mars -> Toxin Refinery (E1M3) Blue", player), lambda state: state.has("Toxin Refinery (E1M3)", player, 1) and state.has("Shotgun", player, 1) and (state.has("Toxin Refinery (E1M3) - Blue keycard", player, 1)))
    set_rule(world.get_entrance("Mars -> Toxin Refinery (E1M3) Main", player), lambda state: state.has("Toxin Refinery (E1M3)", player, 1) and state.has("Shotgun", player, 1))
    set_rule(world.get_entrance("Mars -> Toxin Refinery (E1M3) Yellow", player), lambda state: state.has("Toxin Refinery (E1M3)", player, 1) and state.has("Shotgun", player, 1)and state.has("Toxin Refinery (E1M3) - Blue keycard", player, 1)and state.has("Toxin Refinery (E1M3) - Yellow keycard", player, 1))

    # Command Control (E1M4) - E1M4
    set_rule(world.get_entrance("Mars -> Command Control (E1M4) Blue Yellow", player), lambda state: state.has("Command Control (E1M4)", player, 1) and state.has("Shotgun", player, 1) and state.has("Chaingun", player, 1) and (state.has("Command Control (E1M4) - Blue keycard", player, 1) or state.has("Command Control (E1M4) - Yellow keycard", player, 1)))
    set_rule(world.get_entrance("Mars -> Command Control (E1M4) Main", player), lambda state: state.has("Command Control (E1M4)", player, 1) and state.has("Shotgun", player, 1) and state.has("Chaingun", player, 1))

    # Phobos Lab (E1M5) - E1M5
    set_rule(world.get_entrance("Mars -> Phobos Lab (E1M5) Blue Yellow", player), lambda state: state.has("Phobos Lab (E1M5)", player, 1) and state.has("Shotgun", player, 1) and state.has("Chaingun", player, 1) and (state.has("Phobos Lab (E1M5) - Yellow keycard", player, 1) or state.has("Phobos Lab (E1M5) - Blue keycard", player, 1)))
    set_rule(world.get_entrance("Mars -> Phobos Lab (E1M5) Main", player), lambda state: state.has("Phobos Lab (E1M5)", player, 1) and state.has("Shotgun", player, 1) and state.has("Chaingun", player, 1))
    set_rule(world.get_entrance("Mars -> Phobos Lab (E1M5) Yellow", player), lambda state: state.has("Phobos Lab (E1M5)", player, 1) and state.has("Shotgun", player, 1) and state.has("Chaingun", player, 1) and (state.has("Phobos Lab (E1M5) - Yellow keycard", player, 1)))

    # Central Processing (E1M6) - E1M6
    set_rule(world.get_entrance("Mars -> Central Processing (E1M6) Blue", player), lambda state: state.has("Central Processing (E1M6)", player, 1) and state.has("Shotgun", player, 1) and state.has("Chaingun", player, 1) and (state.has("Central Processing (E1M6) - Blue keycard", player, 1)))
    set_rule(world.get_entrance("Mars -> Central Processing (E1M6) Blue Yellow", player), lambda state: state.has("Central Processing (E1M6)", player, 1) and state.has("Shotgun", player, 1) and state.has("Chaingun", player, 1) and (state.has("Central Processing (E1M6) - Yellow keycard", player, 1) or state.has("Central Processing (E1M6) - Blue keycard", player, 1)))
    set_rule(world.get_entrance("Mars -> Central Processing (E1M6) Main", player), lambda state: state.has("Central Processing (E1M6)", player, 1) and state.has("Shotgun", player, 1) and state.has("Chaingun", player, 1))
    set_rule(world.get_entrance("Mars -> Central Processing (E1M6) Red", player), lambda state: state.has("Central Processing (E1M6)", player, 1) and state.has("Shotgun", player, 1) and state.has("Chaingun", player, 1) and (state.has("Central Processing (E1M6) - Red keycard", player, 1)))

    # Computer Station (E1M7) - E1M7
    set_rule(world.get_entrance("Mars -> Computer Station (E1M7) Blue", player), lambda state: state.has("Computer Station (E1M7)", player, 1) and state.has("Shotgun", player, 1) and state.has("Chaingun", player, 1)and state.has("Computer Station (E1M7) - Blue keycard", player, 1)and state.has("Computer Station (E1M7) - Yellow keycard", player, 1))
    set_rule(world.get_entrance("Mars -> Computer Station (E1M7) Main", player), lambda state: state.has("Computer Station (E1M7)", player, 1) and state.has("Shotgun", player, 1) and state.has("Chaingun", player, 1))
    set_rule(world.get_entrance("Mars -> Computer Station (E1M7) Red", player), lambda state: state.has("Computer Station (E1M7)", player, 1) and state.has("Shotgun", player, 1) and state.has("Chaingun", player, 1) and (state.has("Computer Station (E1M7) - Red keycard", player, 1)))
    set_rule(world.get_entrance("Mars -> Computer Station (E1M7) Yellow", player), lambda state: state.has("Computer Station (E1M7)", player, 1) and state.has("Shotgun", player, 1) and state.has("Chaingun", player, 1) and (state.has("Computer Station (E1M7) - Yellow keycard", player, 1)))
    set_rule(world.get_entrance("Mars -> Computer Station (E1M7) Yellow Red", player), lambda state: state.has("Computer Station (E1M7)", player, 1) and state.has("Shotgun", player, 1) and state.has("Chaingun", player, 1)and state.has("Computer Station (E1M7) - Yellow keycard", player, 1)and state.has("Computer Station (E1M7) - Red keycard", player, 1))

    # Phobos Anomaly (E1M8) - E1M8
    set_rule(world.get_entrance("Mars -> Phobos Anomaly (E1M8) Main", player), lambda state: state.has("Phobos Anomaly (E1M8)", player, 1) and state.has("Shotgun", player, 1) and state.has("Chaingun", player, 1) and (state.has("Rocket launcher", player, 1) or state.has("Plasma gun", player, 1) or state.has("BFG9000", player, 1)))

    # Military Base (E1M9) - E1M9
    set_rule(world.get_entrance("Mars -> Military Base (E1M9) Blue", player), lambda state: state.has("Military Base (E1M9)", player, 1) and state.has("Shotgun", player, 1) and state.has("Chaingun", player, 1) and (state.has("Military Base (E1M9) - Blue keycard", player, 1)))
    set_rule(world.get_entrance("Mars -> Military Base (E1M9) Main", player), lambda state: state.has("Military Base (E1M9)", player, 1) and state.has("Shotgun", player, 1) and state.has("Chaingun", player, 1))
    set_rule(world.get_entrance("Mars -> Military Base (E1M9) Red", player), lambda state: state.has("Military Base (E1M9)", player, 1) and state.has("Shotgun", player, 1) and state.has("Chaingun", player, 1) and (state.has("Military Base (E1M9) - Red keycard", player, 1)))
    set_rule(world.get_entrance("Mars -> Military Base (E1M9) Yellow", player), lambda state: state.has("Military Base (E1M9)", player, 1) and state.has("Shotgun", player, 1) and state.has("Chaingun", player, 1) and (state.has("Military Base (E1M9) - Yellow keycard", player, 1)))

    # Deimos Anomaly (E2M1) - E2M1
    set_rule(world.get_entrance("Mars -> Deimos Anomaly (E2M1) Blue", player), lambda state: state.has("Deimos Anomaly (E2M1)", player, 1) and (state.has("Deimos Anomaly (E2M1) - Blue keycard", player, 1)))
    set_rule(world.get_entrance("Mars -> Deimos Anomaly (E2M1) Main", player), lambda state: state.has("Deimos Anomaly (E2M1)", player, 1))
    set_rule(world.get_entrance("Mars -> Deimos Anomaly (E2M1) Red", player), lambda state: state.has("Deimos Anomaly (E2M1)", player, 1) and (state.has("Deimos Anomaly (E2M1) - Red keycard", player, 1)))

    # Containment Area (E2M2) - E2M2
    set_rule(world.get_entrance("Mars -> Containment Area (E2M2) Blue", player), lambda state: state.has("Containment Area (E2M2)", player, 1) and state.has("Shotgun", player, 1) and (state.has("Containment Area (E2M2) - Blue keycard", player, 1)))
    set_rule(world.get_entrance("Mars -> Containment Area (E2M2) Main", player), lambda state: state.has("Containment Area (E2M2)", player, 1) and state.has("Shotgun", player, 1))
    set_rule(world.get_entrance("Mars -> Containment Area (E2M2) Red", player), lambda state: state.has("Containment Area (E2M2)", player, 1) and state.has("Shotgun", player, 1) and (state.has("Containment Area (E2M2) - Red keycard", player, 1)))
    set_rule(world.get_entrance("Mars -> Containment Area (E2M2) Yellow", player), lambda state: state.has("Containment Area (E2M2)", player, 1) and state.has("Shotgun", player, 1) and (state.has("Containment Area (E2M2) - Yellow keycard", player, 1)))

    # Refinery (E2M3) - E2M3
    set_rule(world.get_entrance("Mars -> Refinery (E2M3) Blue", player), lambda state: state.has("Refinery (E2M3)", player, 1) and state.has("Shotgun", player, 1) and (state.has("Refinery (E2M3) - Blue keycard", player, 1)))
    set_rule(world.get_entrance("Mars -> Refinery (E2M3) Main", player), lambda state: state.has("Refinery (E2M3)", player, 1) and state.has("Shotgun", player, 1))

    # Deimos Lab (E2M4) - E2M4
    set_rule(world.get_entrance("Mars -> Deimos Lab (E2M4) Blue", player), lambda state: state.has("Deimos Lab (E2M4)", player, 1) and state.has("Shotgun", player, 1) and state.has("Chaingun", player, 1) and (state.has("Deimos Lab (E2M4) - Blue keycard", player, 1)))
    set_rule(world.get_entrance("Mars -> Deimos Lab (E2M4) Blue Yellow", player), lambda state: state.has("Deimos Lab (E2M4)", player, 1) and state.has("Shotgun", player, 1) and state.has("Chaingun", player, 1)and state.has("Deimos Lab (E2M4) - Blue keycard", player, 1)and state.has("Deimos Lab (E2M4) - Yellow keycard", player, 1))
    set_rule(world.get_entrance("Mars -> Deimos Lab (E2M4) Main", player), lambda state: state.has("Deimos Lab (E2M4)", player, 1) and state.has("Shotgun", player, 1) and state.has("Chaingun", player, 1))

    # Command Center (E2M5) - E2M5
    set_rule(world.get_entrance("Mars -> Command Center (E2M5) Main", player), lambda state: state.has("Command Center (E2M5)", player, 1) and state.has("Shotgun", player, 1) and state.has("Chaingun", player, 1))

    # Halls of the Damned (E2M6) - E2M6
    set_rule(world.get_entrance("Mars -> Halls of the Damned (E2M6) Blue Yellow Red", player), lambda state: state.has("Halls of the Damned (E2M6)", player, 1) and state.has("Shotgun", player, 1) and state.has("Chaingun", player, 1)and state.has("Halls of the Damned (E2M6) - Red skull key", player, 1)and state.has("Halls of the Damned (E2M6) - Blue skull key", player, 1)and state.has("Halls of the Damned (E2M6) - Yellow skull key", player, 1))
    set_rule(world.get_entrance("Mars -> Halls of the Damned (E2M6) Main", player), lambda state: state.has("Halls of the Damned (E2M6)", player, 1) and state.has("Shotgun", player, 1) and state.has("Chaingun", player, 1))
    set_rule(world.get_entrance("Mars -> Halls of the Damned (E2M6) Yellow", player), lambda state: state.has("Halls of the Damned (E2M6)", player, 1) and state.has("Shotgun", player, 1) and state.has("Chaingun", player, 1) and (state.has("Halls of the Damned (E2M6) - Yellow skull key", player, 1)))

    # Spawning Vats (E2M7) - E2M7
    set_rule(world.get_entrance("Mars -> Spawning Vats (E2M7) Blue", player), lambda state: state.has("Spawning Vats (E2M7)", player, 1) and state.has("Shotgun", player, 1) and state.has("Chaingun", player, 1) and (state.has("Spawning Vats (E2M7) - Blue keycard", player, 1)))
    set_rule(world.get_entrance("Mars -> Spawning Vats (E2M7) Blue Red", player), lambda state: state.has("Spawning Vats (E2M7)", player, 1) and state.has("Shotgun", player, 1) and state.has("Chaingun", player, 1)and state.has("Spawning Vats (E2M7) - Blue keycard", player, 1)and state.has("Spawning Vats (E2M7) - Red keycard", player, 1))
    set_rule(world.get_entrance("Mars -> Spawning Vats (E2M7) Main", player), lambda state: state.has("Spawning Vats (E2M7)", player, 1) and state.has("Shotgun", player, 1) and state.has("Chaingun", player, 1))
    set_rule(world.get_entrance("Mars -> Spawning Vats (E2M7) Red", player), lambda state: state.has("Spawning Vats (E2M7)", player, 1) and state.has("Shotgun", player, 1) and state.has("Chaingun", player, 1) and (state.has("Spawning Vats (E2M7) - Red keycard", player, 1)))
    set_rule(world.get_entrance("Mars -> Spawning Vats (E2M7) Yellow", player), lambda state: state.has("Spawning Vats (E2M7)", player, 1) and state.has("Shotgun", player, 1) and state.has("Chaingun", player, 1) and (state.has("Spawning Vats (E2M7) - Yellow keycard", player, 1)))

    # Tower of Babel (E2M8) - E2M8
    set_rule(world.get_entrance("Mars -> Tower of Babel (E2M8) Main", player), lambda state: state.has("Tower of Babel (E2M8)", player, 1) and state.has("Shotgun", player, 1) and state.has("Chaingun", player, 1) and (state.has("Rocket launcher", player, 1) or state.has("Plasma gun", player, 1) or state.has("BFG9000", player, 1)))

    # Fortress of Mystery (E2M9) - E2M9
    set_rule(world.get_entrance("Mars -> Fortress of Mystery (E2M9) Blue", player), lambda state: state.has("Fortress of Mystery (E2M9)", player, 1) and state.has("Shotgun", player, 1) and state.has("Chaingun", player, 1) and (state.has("Fortress of Mystery (E2M9) - Blue skull key", player, 1)))
    set_rule(world.get_entrance("Mars -> Fortress of Mystery (E2M9) Main", player), lambda state: state.has("Fortress of Mystery (E2M9)", player, 1) and state.has("Shotgun", player, 1) and state.has("Chaingun", player, 1))
    set_rule(world.get_entrance("Mars -> Fortress of Mystery (E2M9) Red", player), lambda state: state.has("Fortress of Mystery (E2M9)", player, 1) and state.has("Shotgun", player, 1) and state.has("Chaingun", player, 1) and (state.has("Fortress of Mystery (E2M9) - Red skull key", player, 1)))
    set_rule(world.get_entrance("Mars -> Fortress of Mystery (E2M9) Yellow", player), lambda state: state.has("Fortress of Mystery (E2M9)", player, 1) and state.has("Shotgun", player, 1) and state.has("Chaingun", player, 1) and (state.has("Fortress of Mystery (E2M9) - Yellow skull key", player, 1)))

    # Hell Keep (E3M1) - E3M1
    set_rule(world.get_entrance("Mars -> Hell Keep (E3M1) Main", player), lambda state: state.has("Hell Keep (E3M1)", player, 1))
    set_rule(world.get_entrance("Mars -> Hell Keep (E3M1) Narrow", player), lambda state: state.has("Hell Keep (E3M1)", player, 1) and (state.has("Shotgun", player, 1) or state.has("Chaingun", player, 1)))

    # Slough of Despair (E3M2) - E3M2
    set_rule(world.get_entrance("Mars -> Slough of Despair (E3M2) Blue", player), lambda state: state.has("Slough of Despair (E3M2)", player, 1) and state.has("Shotgun", player, 1) and (state.has("Slough of Despair (E3M2) - Blue skull key", player, 1)))
    set_rule(world.get_entrance("Mars -> Slough of Despair (E3M2) Main", player), lambda state: state.has("Slough of Despair (E3M2)", player, 1) and state.has("Shotgun", player, 1))

    # Pandemonium (E3M3) - E3M3
    set_rule(world.get_entrance("Mars -> Pandemonium (E3M3) Blue", player), lambda state: state.has("Pandemonium (E3M3)", player, 1) and state.has("Shotgun", player, 1) and (state.has("Pandemonium (E3M3) - Blue skull key", player, 1)))
    set_rule(world.get_entrance("Mars -> Pandemonium (E3M3) Main", player), lambda state: state.has("Pandemonium (E3M3)", player, 1) and state.has("Shotgun", player, 1))

    # House of Pain (E3M4) - E3M4
    set_rule(world.get_entrance("Mars -> House of Pain (E3M4) Blue", player), lambda state: state.has("House of Pain (E3M4)", player, 1) and state.has("Shotgun", player, 1) and state.has("Chaingun", player, 1) and (state.has("House of Pain (E3M4) - Blue skull key", player, 1)))
    set_rule(world.get_entrance("Mars -> House of Pain (E3M4) Blue Red", player), lambda state: state.has("House of Pain (E3M4)", player, 1) and state.has("Shotgun", player, 1) and state.has("Chaingun", player, 1)and state.has("House of Pain (E3M4) - Red skull key", player, 1)and state.has("House of Pain (E3M4) - Blue skull key", player, 1))
    set_rule(world.get_entrance("Mars -> House of Pain (E3M4) Blue Yellow", player), lambda state: state.has("House of Pain (E3M4)", player, 1) and state.has("Shotgun", player, 1) and state.has("Chaingun", player, 1)and state.has("House of Pain (E3M4) - Yellow skull key", player, 1)and state.has("House of Pain (E3M4) - Blue skull key", player, 1))
    set_rule(world.get_entrance("Mars -> House of Pain (E3M4) Main", player), lambda state: state.has("House of Pain (E3M4)", player, 1) and state.has("Shotgun", player, 1) and state.has("Chaingun", player, 1))

    # Unholy Cathedral (E3M5) - E3M5
    set_rule(world.get_entrance("Mars -> Unholy Cathedral (E3M5) Blue", player), lambda state: state.has("Unholy Cathedral (E3M5)", player, 1) and state.has("Shotgun", player, 1) and state.has("Chaingun", player, 1) and (state.has("Unholy Cathedral (E3M5) - Blue skull key", player, 1)))
    set_rule(world.get_entrance("Mars -> Unholy Cathedral (E3M5) Main", player), lambda state: state.has("Unholy Cathedral (E3M5)", player, 1) and state.has("Shotgun", player, 1) and state.has("Chaingun", player, 1))
    set_rule(world.get_entrance("Mars -> Unholy Cathedral (E3M5) Yellow", player), lambda state: state.has("Unholy Cathedral (E3M5)", player, 1) and state.has("Shotgun", player, 1) and state.has("Chaingun", player, 1) and (state.has("Unholy Cathedral (E3M5) - Yellow skull key", player, 1)))

    # Mt. Erebus (E3M6) - E3M6
    set_rule(world.get_entrance("Mars -> Mt. Erebus (E3M6) Blue", player), lambda state: state.has("Mt. Erebus (E3M6)", player, 1) and state.has("Shotgun", player, 1) and state.has("Chaingun", player, 1) and (state.has("Mt. Erebus (E3M6) - Blue skull key", player, 1)))
    set_rule(world.get_entrance("Mars -> Mt. Erebus (E3M6) Main", player), lambda state: state.has("Mt. Erebus (E3M6)", player, 1) and state.has("Shotgun", player, 1) and state.has("Chaingun", player, 1))

    # Limbo (E3M7) - E3M7
    set_rule(world.get_entrance("Mars -> Limbo (E3M7) Blue", player), lambda state: state.has("Limbo (E3M7)", player, 1) and state.has("Shotgun", player, 1) and state.has("Chaingun", player, 1) and (state.has("Limbo (E3M7) - Blue skull key", player, 1)))
    set_rule(world.get_entrance("Mars -> Limbo (E3M7) Main", player), lambda state: state.has("Limbo (E3M7)", player, 1) and state.has("Shotgun", player, 1) and state.has("Chaingun", player, 1))
    set_rule(world.get_entrance("Mars -> Limbo (E3M7) Red", player), lambda state: state.has("Limbo (E3M7)", player, 1) and state.has("Shotgun", player, 1) and state.has("Chaingun", player, 1) and (state.has("Limbo (E3M7) - Red skull key", player, 1)))
    set_rule(world.get_entrance("Mars -> Limbo (E3M7) Yellow Red", player), lambda state: state.has("Limbo (E3M7)", player, 1) and state.has("Shotgun", player, 1) and state.has("Chaingun", player, 1) and (state.has("Limbo (E3M7) - Yellow skull key", player, 1) or state.has("Limbo (E3M7) - Red skull key", player, 1)))

    # Dis (E3M8) - E3M8
    set_rule(world.get_entrance("Mars -> Dis (E3M8) Main", player), lambda state: state.has("Dis (E3M8)", player, 1) and state.has("Shotgun", player, 1) and state.has("Chaingun", player, 1) and (state.has("Rocket launcher", player, 1) or state.has("Plasma gun", player, 1) or state.has("BFG9000", player, 1)))

    # Warrens (E3M9) - E3M9
    set_rule(world.get_entrance("Mars -> Warrens (E3M9) Main", player), lambda state: state.has("Warrens (E3M9)", player, 1) and state.has("Shotgun", player, 1) and state.has("Chaingun", player, 1) and (state.has("Rocket launcher", player, 1) or state.has("Plasma gun", player, 1) or state.has("BFG9000", player, 1)))
    set_rule(world.get_entrance("Mars -> Warrens (E3M9) Red", player), lambda state: state.has("Warrens (E3M9)", player, 1) and state.has("Shotgun", player, 1) and state.has("Chaingun", player, 1) and (state.has("Warrens (E3M9) - Red skull key", player, 1)))

