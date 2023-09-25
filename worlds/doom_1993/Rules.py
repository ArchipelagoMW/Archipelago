# This file is auto generated. More info: https://github.com/Daivuk/apdoom

from typing import TYPE_CHECKING
from worlds.generic.Rules import set_rule

if TYPE_CHECKING:
    from . import DOOM1993World


def set_episode1_rules(player, world):
    # Hangar (E1M1)
    set_rule(world.get_entrance("Hub -> Hangar (E1M1) Main", player), lambda state:
        state.has("Hangar (E1M1)", player, 1))

    # Nuclear Plant (E1M2)
    set_rule(world.get_entrance("Hub -> Nuclear Plant (E1M2) Main", player), lambda state:
       (state.has("Nuclear Plant (E1M2)", player, 1)) and
       (state.has("Shotgun", player, 1) or
        state.has("Chaingun", player, 1)))
    set_rule(world.get_entrance("Nuclear Plant (E1M2) Main -> Nuclear Plant (E1M2) Red", player), lambda state:
        state.has("Nuclear Plant (E1M2) - Red keycard", player, 1))
    set_rule(world.get_entrance("Nuclear Plant (E1M2) Red -> Nuclear Plant (E1M2) Main", player), lambda state:
        state.has("Nuclear Plant (E1M2) - Red keycard", player, 1))

    # Toxin Refinery (E1M3)
    set_rule(world.get_entrance("Hub -> Toxin Refinery (E1M3) Main", player), lambda state:
       (state.has("Toxin Refinery (E1M3)", player, 1)) and
       (state.has("Shotgun", player, 1) or
        state.has("Chaingun", player, 1)))
    set_rule(world.get_entrance("Toxin Refinery (E1M3) Main -> Toxin Refinery (E1M3) Blue", player), lambda state:
        state.has("Toxin Refinery (E1M3) - Blue keycard", player, 1))
    set_rule(world.get_entrance("Toxin Refinery (E1M3) Blue -> Toxin Refinery (E1M3) Yellow", player), lambda state:
        state.has("Toxin Refinery (E1M3) - Yellow keycard", player, 1))
    set_rule(world.get_entrance("Toxin Refinery (E1M3) Blue -> Toxin Refinery (E1M3) Main", player), lambda state:
        state.has("Toxin Refinery (E1M3) - Blue keycard", player, 1))
    set_rule(world.get_entrance("Toxin Refinery (E1M3) Yellow -> Toxin Refinery (E1M3) Blue", player), lambda state:
        state.has("Toxin Refinery (E1M3) - Yellow keycard", player, 1))

    # Command Control (E1M4)
    set_rule(world.get_entrance("Hub -> Command Control (E1M4) Main", player), lambda state:
        state.has("Command Control (E1M4)", player, 1) and
        state.has("Shotgun", player, 1) and
        state.has("Chaingun", player, 1))
    set_rule(world.get_entrance("Command Control (E1M4) Main -> Command Control (E1M4) Blue", player), lambda state:
        state.has("Command Control (E1M4) - Blue keycard", player, 1) or
        state.has("Command Control (E1M4) - Yellow keycard", player, 1))
    set_rule(world.get_entrance("Command Control (E1M4) Main -> Command Control (E1M4) Yellow", player), lambda state:
        state.has("Command Control (E1M4) - Blue keycard", player, 1) or
        state.has("Command Control (E1M4) - Yellow keycard", player, 1))
    set_rule(world.get_entrance("Command Control (E1M4) Blue -> Command Control (E1M4) Main", player), lambda state:
        state.has("Command Control (E1M4) - Yellow keycard", player, 1) or
        state.has("Command Control (E1M4) - Blue keycard", player, 1))

    # Phobos Lab (E1M5)
    set_rule(world.get_entrance("Hub -> Phobos Lab (E1M5) Main", player), lambda state:
        state.has("Phobos Lab (E1M5)", player, 1) and
        state.has("Shotgun", player, 1) and
        state.has("Chaingun", player, 1))
    set_rule(world.get_entrance("Phobos Lab (E1M5) Main -> Phobos Lab (E1M5) Yellow", player), lambda state:
        state.has("Phobos Lab (E1M5) - Yellow keycard", player, 1))
    set_rule(world.get_entrance("Phobos Lab (E1M5) Yellow -> Phobos Lab (E1M5) Blue", player), lambda state:
        state.has("Phobos Lab (E1M5) - Blue keycard", player, 1))
    set_rule(world.get_entrance("Phobos Lab (E1M5) Blue -> Phobos Lab (E1M5) Green", player), lambda state:
        state.has("Phobos Lab (E1M5) - Blue keycard", player, 1))
    set_rule(world.get_entrance("Phobos Lab (E1M5) Green -> Phobos Lab (E1M5) Blue", player), lambda state:
        state.has("Phobos Lab (E1M5) - Blue keycard", player, 1))

    # Central Processing (E1M6)
    set_rule(world.get_entrance("Hub -> Central Processing (E1M6) Main", player), lambda state:
        state.has("Central Processing (E1M6)", player, 1) and
        state.has("Shotgun", player, 1) and
        state.has("Chaingun", player, 1) and
        state.has("Rocket launcher", player, 1))
    set_rule(world.get_entrance("Central Processing (E1M6) Main -> Central Processing (E1M6) Yellow", player), lambda state:
        state.has("Central Processing (E1M6) - Yellow keycard", player, 1))
    set_rule(world.get_entrance("Central Processing (E1M6) Main -> Central Processing (E1M6) Red", player), lambda state:
        state.has("Central Processing (E1M6) - Red keycard", player, 1))
    set_rule(world.get_entrance("Central Processing (E1M6) Main -> Central Processing (E1M6) Blue", player), lambda state:
        state.has("Central Processing (E1M6) - Blue keycard", player, 1))
    set_rule(world.get_entrance("Central Processing (E1M6) Main -> Central Processing (E1M6) Nukage", player), lambda state:
        state.has("Central Processing (E1M6) - Blue keycard", player, 1))
    set_rule(world.get_entrance("Central Processing (E1M6) Yellow -> Central Processing (E1M6) Main", player), lambda state:
        state.has("Central Processing (E1M6) - Yellow keycard", player, 1))

    # Computer Station (E1M7)
    set_rule(world.get_entrance("Hub -> Computer Station (E1M7) Main", player), lambda state:
        state.has("Computer Station (E1M7)", player, 1) and
        state.has("Shotgun", player, 1) and
        state.has("Chaingun", player, 1) and
        state.has("Rocket launcher", player, 1))
    set_rule(world.get_entrance("Computer Station (E1M7) Main -> Computer Station (E1M7) Red", player), lambda state:
        state.has("Computer Station (E1M7) - Red keycard", player, 1))
    set_rule(world.get_entrance("Computer Station (E1M7) Main -> Computer Station (E1M7) Yellow", player), lambda state:
        state.has("Computer Station (E1M7) - Yellow keycard", player, 1))
    set_rule(world.get_entrance("Computer Station (E1M7) Blue -> Computer Station (E1M7) Yellow", player), lambda state:
        state.has("Computer Station (E1M7) - Blue keycard", player, 1))
    set_rule(world.get_entrance("Computer Station (E1M7) Red -> Computer Station (E1M7) Main", player), lambda state:
        state.has("Computer Station (E1M7) - Red keycard", player, 1))
    set_rule(world.get_entrance("Computer Station (E1M7) Yellow -> Computer Station (E1M7) Blue", player), lambda state:
        state.has("Computer Station (E1M7) - Blue keycard", player, 1))
    set_rule(world.get_entrance("Computer Station (E1M7) Yellow -> Computer Station (E1M7) Courtyard", player), lambda state:
        state.has("Computer Station (E1M7) - Yellow keycard", player, 1) and
        state.has("Computer Station (E1M7) - Red keycard", player, 1))
    set_rule(world.get_entrance("Computer Station (E1M7) Courtyard -> Computer Station (E1M7) Yellow", player), lambda state:
        state.has("Computer Station (E1M7) - Yellow keycard", player, 1))

    # Phobos Anomaly (E1M8)
    set_rule(world.get_entrance("Hub -> Phobos Anomaly (E1M8) Start", player), lambda state:
       (state.has("Phobos Anomaly (E1M8)", player, 1) and
        state.has("Shotgun", player, 1) and
        state.has("Chaingun", player, 1)) and
       (state.has("Rocket launcher", player, 1) or
        state.has("Plasma gun", player, 1) or
        state.has("BFG9000", player, 1)))

    # Military Base (E1M9)
    set_rule(world.get_entrance("Hub -> Military Base (E1M9) Main", player), lambda state:
        state.has("Military Base (E1M9)", player, 1) and
        state.has("Chaingun", player, 1) and
        state.has("Shotgun", player, 1))
    set_rule(world.get_entrance("Military Base (E1M9) Main -> Military Base (E1M9) Blue", player), lambda state:
        state.has("Military Base (E1M9) - Blue keycard", player, 1))
    set_rule(world.get_entrance("Military Base (E1M9) Main -> Military Base (E1M9) Yellow", player), lambda state:
        state.has("Military Base (E1M9) - Yellow keycard", player, 1))
    set_rule(world.get_entrance("Military Base (E1M9) Main -> Military Base (E1M9) Red", player), lambda state:
        state.has("Military Base (E1M9) - Red keycard", player, 1))
    set_rule(world.get_entrance("Military Base (E1M9) Blue -> Military Base (E1M9) Main", player), lambda state:
        state.has("Military Base (E1M9) - Blue keycard", player, 1))
    set_rule(world.get_entrance("Military Base (E1M9) Yellow -> Military Base (E1M9) Main", player), lambda state:
        state.has("Military Base (E1M9) - Yellow keycard", player, 1))


def set_episode2_rules(player, world):
    # Deimos Anomaly (E2M1)
    set_rule(world.get_entrance("Hub -> Deimos Anomaly (E2M1) Main", player), lambda state:
        state.has("Deimos Anomaly (E2M1)", player, 1))
    set_rule(world.get_entrance("Deimos Anomaly (E2M1) Main -> Deimos Anomaly (E2M1) Red", player), lambda state:
        state.has("Deimos Anomaly (E2M1) - Red keycard", player, 1))
    set_rule(world.get_entrance("Deimos Anomaly (E2M1) Main -> Deimos Anomaly (E2M1) Blue", player), lambda state:
        state.has("Deimos Anomaly (E2M1) - Blue keycard", player, 1))
    set_rule(world.get_entrance("Deimos Anomaly (E2M1) Blue -> Deimos Anomaly (E2M1) Main", player), lambda state:
        state.has("Deimos Anomaly (E2M1) - Blue keycard", player, 1))
    set_rule(world.get_entrance("Deimos Anomaly (E2M1) Red -> Deimos Anomaly (E2M1) Main", player), lambda state:
        state.has("Deimos Anomaly (E2M1) - Red keycard", player, 1))

    # Containment Area (E2M2)
    set_rule(world.get_entrance("Hub -> Containment Area (E2M2) Main", player), lambda state:
       (state.has("Containment Area (E2M2)", player, 1) and
        state.has("Shotgun", player, 1)) and
       (state.has("Chaingun", player, 1) or
        state.has("Plasma gun", player, 1)))
    set_rule(world.get_entrance("Containment Area (E2M2) Main -> Containment Area (E2M2) Yellow", player), lambda state:
        state.has("Containment Area (E2M2) - Yellow keycard", player, 1))
    set_rule(world.get_entrance("Containment Area (E2M2) Main -> Containment Area (E2M2) Blue", player), lambda state:
        state.has("Containment Area (E2M2) - Blue keycard", player, 1))
    set_rule(world.get_entrance("Containment Area (E2M2) Main -> Containment Area (E2M2) Red", player), lambda state:
        state.has("Containment Area (E2M2) - Red keycard", player, 1))
    set_rule(world.get_entrance("Containment Area (E2M2) Blue -> Containment Area (E2M2) Main", player), lambda state:
        state.has("Containment Area (E2M2) - Blue keycard", player, 1))
    set_rule(world.get_entrance("Containment Area (E2M2) Red -> Containment Area (E2M2) Main", player), lambda state:
        state.has("Containment Area (E2M2) - Red keycard", player, 1))

    # Refinery (E2M3)
    set_rule(world.get_entrance("Hub -> Refinery (E2M3) Main", player), lambda state:
       (state.has("Refinery (E2M3)", player, 1) and
        state.has("Shotgun", player, 1)) and
       (state.has("Chaingun", player, 1) or
        state.has("Plasma gun", player, 1)))
    set_rule(world.get_entrance("Refinery (E2M3) Main -> Refinery (E2M3) Blue", player), lambda state:
        state.has("Refinery (E2M3) - Blue keycard", player, 1))
    set_rule(world.get_entrance("Refinery (E2M3) Blue -> Refinery (E2M3) Main", player), lambda state:
        state.has("Refinery (E2M3) - Blue keycard", player, 1))

    # Deimos Lab (E2M4)
    set_rule(world.get_entrance("Hub -> Deimos Lab (E2M4) Main", player), lambda state:
        state.has("Deimos Lab (E2M4)", player, 1) and
        state.has("Shotgun", player, 1) and
        state.has("Chaingun", player, 1) and
        state.has("Plasma gun", player, 1))
    set_rule(world.get_entrance("Deimos Lab (E2M4) Main -> Deimos Lab (E2M4) Blue", player), lambda state:
        state.has("Deimos Lab (E2M4) - Blue keycard", player, 1))
    set_rule(world.get_entrance("Deimos Lab (E2M4) Blue -> Deimos Lab (E2M4) Yellow", player), lambda state:
        state.has("Deimos Lab (E2M4) - Yellow keycard", player, 1))

    # Command Center (E2M5)
    set_rule(world.get_entrance("Hub -> Command Center (E2M5) Main", player), lambda state:
        state.has("Command Center (E2M5)", player, 1) and
        state.has("Shotgun", player, 1) and
        state.has("Chaingun", player, 1) and
        state.has("Plasma gun", player, 1))

    # Halls of the Damned (E2M6)
    set_rule(world.get_entrance("Hub -> Halls of the Damned (E2M6) Main", player), lambda state:
        state.has("Halls of the Damned (E2M6)", player, 1) and
        state.has("Chaingun", player, 1) and
        state.has("Shotgun", player, 1) and
        state.has("Plasma gun", player, 1))
    set_rule(world.get_entrance("Halls of the Damned (E2M6) Main -> Halls of the Damned (E2M6) Blue Yellow Red", player), lambda state:
        state.has("Halls of the Damned (E2M6) - Blue skull key", player, 1) and
        state.has("Halls of the Damned (E2M6) - Yellow skull key", player, 1) and
        state.has("Halls of the Damned (E2M6) - Red skull key", player, 1))
    set_rule(world.get_entrance("Halls of the Damned (E2M6) Main -> Halls of the Damned (E2M6) Yellow", player), lambda state:
        state.has("Halls of the Damned (E2M6) - Yellow skull key", player, 1))
    set_rule(world.get_entrance("Halls of the Damned (E2M6) Main -> Halls of the Damned (E2M6) One way Yellow", player), lambda state:
        state.has("Halls of the Damned (E2M6) - Yellow skull key", player, 1))
    set_rule(world.get_entrance("Halls of the Damned (E2M6) Blue Yellow Red -> Halls of the Damned (E2M6) Main", player), lambda state:
        state.has("Halls of the Damned (E2M6) - Blue skull key", player, 1) and
        state.has("Halls of the Damned (E2M6) - Yellow skull key", player, 1) and
        state.has("Halls of the Damned (E2M6) - Red skull key", player, 1))
    set_rule(world.get_entrance("Halls of the Damned (E2M6) One way Yellow -> Halls of the Damned (E2M6) Main", player), lambda state:
        state.has("Halls of the Damned (E2M6) - Yellow skull key", player, 1))

    # Spawning Vats (E2M7)
    set_rule(world.get_entrance("Hub -> Spawning Vats (E2M7) Main", player), lambda state:
        state.has("Spawning Vats (E2M7)", player, 1) and
        state.has("Shotgun", player, 1) and
        state.has("Chaingun", player, 1) and
        state.has("Plasma gun", player, 1) and
        state.has("Rocket launcher", player, 1))
    set_rule(world.get_entrance("Spawning Vats (E2M7) Main -> Spawning Vats (E2M7) Blue", player), lambda state:
        state.has("Spawning Vats (E2M7) - Blue keycard", player, 1))
    set_rule(world.get_entrance("Spawning Vats (E2M7) Main -> Spawning Vats (E2M7) Entrance Secret", player), lambda state:
        state.has("Spawning Vats (E2M7) - Blue keycard", player, 1) and
        state.has("Spawning Vats (E2M7) - Red keycard", player, 1))
    set_rule(world.get_entrance("Spawning Vats (E2M7) Main -> Spawning Vats (E2M7) Red", player), lambda state:
        state.has("Spawning Vats (E2M7) - Red keycard", player, 1))
    set_rule(world.get_entrance("Spawning Vats (E2M7) Main -> Spawning Vats (E2M7) Yellow", player), lambda state:
        state.has("Spawning Vats (E2M7) - Yellow keycard", player, 1))
    set_rule(world.get_entrance("Spawning Vats (E2M7) Yellow -> Spawning Vats (E2M7) Main", player), lambda state:
        state.has("Spawning Vats (E2M7) - Yellow keycard", player, 1))
    set_rule(world.get_entrance("Spawning Vats (E2M7) Red -> Spawning Vats (E2M7) Main", player), lambda state:
        state.has("Spawning Vats (E2M7) - Red keycard", player, 1))
    set_rule(world.get_entrance("Spawning Vats (E2M7) Entrance Secret -> Spawning Vats (E2M7) Main", player), lambda state:
        state.has("Spawning Vats (E2M7) - Blue keycard", player, 1) and
        state.has("Spawning Vats (E2M7) - Red keycard", player, 1))

    # Tower of Babel (E2M8)
    set_rule(world.get_entrance("Hub -> Tower of Babel (E2M8) Main", player), lambda state:
        state.has("Tower of Babel (E2M8)", player, 1))

    # Fortress of Mystery (E2M9)
    set_rule(world.get_entrance("Hub -> Fortress of Mystery (E2M9) Main", player), lambda state:
       (state.has("Fortress of Mystery (E2M9)", player, 1) and
        state.has("Shotgun", player, 1) and
        state.has("Chaingun", player, 1)) and
       (state.has("Rocket launcher", player, 1) or
        state.has("Plasma gun", player, 1) or
        state.has("BFG9000", player, 1)))
    set_rule(world.get_entrance("Fortress of Mystery (E2M9) Main -> Fortress of Mystery (E2M9) Blue", player), lambda state:
        state.has("Fortress of Mystery (E2M9) - Blue skull key", player, 1))
    set_rule(world.get_entrance("Fortress of Mystery (E2M9) Main -> Fortress of Mystery (E2M9) Red", player), lambda state:
        state.has("Fortress of Mystery (E2M9) - Red skull key", player, 1))
    set_rule(world.get_entrance("Fortress of Mystery (E2M9) Main -> Fortress of Mystery (E2M9) Yellow", player), lambda state:
        state.has("Fortress of Mystery (E2M9) - Yellow skull key", player, 1))
    set_rule(world.get_entrance("Fortress of Mystery (E2M9) Blue -> Fortress of Mystery (E2M9) Main", player), lambda state:
        state.has("Fortress of Mystery (E2M9) - Blue skull key", player, 1))
    set_rule(world.get_entrance("Fortress of Mystery (E2M9) Red -> Fortress of Mystery (E2M9) Main", player), lambda state:
        state.has("Fortress of Mystery (E2M9) - Red skull key", player, 1))
    set_rule(world.get_entrance("Fortress of Mystery (E2M9) Yellow -> Fortress of Mystery (E2M9) Main", player), lambda state:
        state.has("Fortress of Mystery (E2M9) - Yellow skull key", player, 1))


def set_episode3_rules(player, world):
    # Hell Keep (E3M1)
    set_rule(world.get_entrance("Hub -> Hell Keep (E3M1) Main", player), lambda state:
        state.has("Hell Keep (E3M1)", player, 1))
    set_rule(world.get_entrance("Hell Keep (E3M1) Main -> Hell Keep (E3M1) Narrow", player), lambda state:
        state.has("Chaingun", player, 1) or
        state.has("Shotgun", player, 1))

    # Slough of Despair (E3M2)
    set_rule(world.get_entrance("Hub -> Slough of Despair (E3M2) Main", player), lambda state:
       (state.has("Slough of Despair (E3M2)", player, 1)) and
       (state.has("Shotgun", player, 1) or
        state.has("Chaingun", player, 1)))
    set_rule(world.get_entrance("Slough of Despair (E3M2) Main -> Slough of Despair (E3M2) Blue", player), lambda state:
        state.has("Slough of Despair (E3M2) - Blue skull key", player, 1))
    set_rule(world.get_entrance("Slough of Despair (E3M2) Blue -> Slough of Despair (E3M2) Main", player), lambda state:
        state.has("Slough of Despair (E3M2) - Blue skull key", player, 1))

    # Pandemonium (E3M3)
    set_rule(world.get_entrance("Hub -> Pandemonium (E3M3) Main", player), lambda state:
       (state.has("Pandemonium (E3M3)", player, 1) and
        state.has("Shotgun", player, 1) and
        state.has("Chaingun", player, 1)) and
       (state.has("Rocket launcher", player, 1) or
        state.has("Plasma gun", player, 1) or
        state.has("BFG9000", player, 1)))
    set_rule(world.get_entrance("Pandemonium (E3M3) Main -> Pandemonium (E3M3) Blue", player), lambda state:
        state.has("Pandemonium (E3M3) - Blue skull key", player, 1))
    set_rule(world.get_entrance("Pandemonium (E3M3) Blue -> Pandemonium (E3M3) Main", player), lambda state:
        state.has("Pandemonium (E3M3) - Blue skull key", player, 1))

    # House of Pain (E3M4)
    set_rule(world.get_entrance("Hub -> House of Pain (E3M4) Main", player), lambda state:
       (state.has("House of Pain (E3M4)", player, 1) and
        state.has("Shotgun", player, 1) and
        state.has("Chaingun", player, 1)) and
       (state.has("Rocket launcher", player, 1) or
        state.has("Plasma gun", player, 1) or
        state.has("BFG9000", player, 1)))
    set_rule(world.get_entrance("House of Pain (E3M4) Main -> House of Pain (E3M4) Blue", player), lambda state:
        state.has("House of Pain (E3M4) - Blue skull key", player, 1))
    set_rule(world.get_entrance("House of Pain (E3M4) Blue -> House of Pain (E3M4) Main", player), lambda state:
        state.has("House of Pain (E3M4) - Blue skull key", player, 1))
    set_rule(world.get_entrance("House of Pain (E3M4) Blue -> House of Pain (E3M4) Yellow", player), lambda state:
        state.has("House of Pain (E3M4) - Yellow skull key", player, 1))
    set_rule(world.get_entrance("House of Pain (E3M4) Blue -> House of Pain (E3M4) Red", player), lambda state:
        state.has("House of Pain (E3M4) - Red skull key", player, 1))
    set_rule(world.get_entrance("House of Pain (E3M4) Red -> House of Pain (E3M4) Blue", player), lambda state:
        state.has("House of Pain (E3M4) - Red skull key", player, 1))
    set_rule(world.get_entrance("House of Pain (E3M4) Yellow -> House of Pain (E3M4) Blue", player), lambda state:
        state.has("House of Pain (E3M4) - Yellow skull key", player, 1))

    # Unholy Cathedral (E3M5)
    set_rule(world.get_entrance("Hub -> Unholy Cathedral (E3M5) Main", player), lambda state:
       (state.has("Unholy Cathedral (E3M5)", player, 1) and
        state.has("Chaingun", player, 1) and
        state.has("Shotgun", player, 1)) and
       (state.has("Rocket launcher", player, 1) or
        state.has("Plasma gun", player, 1) or
        state.has("BFG9000", player, 1)))
    set_rule(world.get_entrance("Unholy Cathedral (E3M5) Main -> Unholy Cathedral (E3M5) Yellow", player), lambda state:
        state.has("Unholy Cathedral (E3M5) - Yellow skull key", player, 1))
    set_rule(world.get_entrance("Unholy Cathedral (E3M5) Main -> Unholy Cathedral (E3M5) Blue", player), lambda state:
        state.has("Unholy Cathedral (E3M5) - Blue skull key", player, 1))
    set_rule(world.get_entrance("Unholy Cathedral (E3M5) Blue -> Unholy Cathedral (E3M5) Main", player), lambda state:
        state.has("Unholy Cathedral (E3M5) - Blue skull key", player, 1))
    set_rule(world.get_entrance("Unholy Cathedral (E3M5) Yellow -> Unholy Cathedral (E3M5) Main", player), lambda state:
        state.has("Unholy Cathedral (E3M5) - Yellow skull key", player, 1))

    # Mt. Erebus (E3M6)
    set_rule(world.get_entrance("Hub -> Mt. Erebus (E3M6) Main", player), lambda state:
        state.has("Mt. Erebus (E3M6)", player, 1) and
        state.has("Shotgun", player, 1) and
        state.has("Chaingun", player, 1))
    set_rule(world.get_entrance("Mt. Erebus (E3M6) Main -> Mt. Erebus (E3M6) Blue", player), lambda state:
        state.has("Mt. Erebus (E3M6) - Blue skull key", player, 1))
    set_rule(world.get_entrance("Mt. Erebus (E3M6) Blue -> Mt. Erebus (E3M6) Main", player), lambda state:
        state.has("Mt. Erebus (E3M6) - Blue skull key", player, 1))

    # Limbo (E3M7)
    set_rule(world.get_entrance("Hub -> Limbo (E3M7) Main", player), lambda state:
       (state.has("Limbo (E3M7)", player, 1) and
        state.has("Shotgun", player, 1) and
        state.has("Chaingun", player, 1)) and
       (state.has("Rocket launcher", player, 1) or
        state.has("Plasma gun", player, 1) or
        state.has("BFG9000", player, 1)))
    set_rule(world.get_entrance("Limbo (E3M7) Main -> Limbo (E3M7) Red", player), lambda state:
        state.has("Limbo (E3M7) - Red skull key", player, 1))
    set_rule(world.get_entrance("Limbo (E3M7) Main -> Limbo (E3M7) Blue", player), lambda state:
        state.has("Limbo (E3M7) - Blue skull key", player, 1))
    set_rule(world.get_entrance("Limbo (E3M7) Main -> Limbo (E3M7) Pink", player), lambda state:
        state.has("Limbo (E3M7) - Blue skull key", player, 1))
    set_rule(world.get_entrance("Limbo (E3M7) Red -> Limbo (E3M7) Yellow", player), lambda state:
        state.has("Limbo (E3M7) - Yellow skull key", player, 1))
    set_rule(world.get_entrance("Limbo (E3M7) Pink -> Limbo (E3M7) Green", player), lambda state:
        state.has("Limbo (E3M7) - Red skull key", player, 1))

    # Dis (E3M8)
    set_rule(world.get_entrance("Hub -> Dis (E3M8) Main", player), lambda state:
       (state.has("Dis (E3M8)", player, 1) and
        state.has("Chaingun", player, 1) and
        state.has("Shotgun", player, 1)) and
       (state.has("Plasma gun", player, 1) or
        state.has("BFG9000", player, 1) or
        state.has("Rocket launcher", player, 1)))

    # Warrens (E3M9)
    set_rule(world.get_entrance("Hub -> Warrens (E3M9) Main", player), lambda state:
       (state.has("Warrens (E3M9)", player, 1) and
        state.has("Shotgun", player, 1) and
        state.has("Chaingun", player, 1) and
        state.has("Plasma gun", player, 1)) and
       (state.has("Rocket launcher", player, 1) or
        state.has("BFG9000", player, 1)))
    set_rule(world.get_entrance("Warrens (E3M9) Main -> Warrens (E3M9) Blue", player), lambda state:
        state.has("Warrens (E3M9) - Blue skull key", player, 1))
    set_rule(world.get_entrance("Warrens (E3M9) Main -> Warrens (E3M9) Blue trigger", player), lambda state:
        state.has("Warrens (E3M9) - Blue skull key", player, 1))
    set_rule(world.get_entrance("Warrens (E3M9) Blue -> Warrens (E3M9) Main", player), lambda state:
        state.has("Warrens (E3M9) - Blue skull key", player, 1))
    set_rule(world.get_entrance("Warrens (E3M9) Blue -> Warrens (E3M9) Red", player), lambda state:
        state.has("Warrens (E3M9) - Red skull key", player, 1))


def set_episode4_rules(player, world):
    # Hell Beneath (E4M1)
    set_rule(world.get_entrance("Hub -> Hell Beneath (E4M1) Main", player), lambda state:
        state.has("Hell Beneath (E4M1)", player, 1))
    set_rule(world.get_entrance("Hell Beneath (E4M1) Main -> Hell Beneath (E4M1) Red", player), lambda state:
       (state.has("Hell Beneath (E4M1) - Red skull key", player, 1) and
        state.has("Shotgun", player, 1) and
        state.has("Chaingun", player, 1)) and       (state.has("Plasma gun", player, 1) or
        state.has("BFG9000", player, 1)))
    set_rule(world.get_entrance("Hell Beneath (E4M1) Main -> Hell Beneath (E4M1) Blue", player), lambda state:
        state.has("Shotgun", player, 1) or
        state.has("Chaingun", player, 1) or
        state.has("Hell Beneath (E4M1) - Blue skull key", player, 1))

    # Perfect Hatred (E4M2)
    set_rule(world.get_entrance("Hub -> Perfect Hatred (E4M2) Main", player), lambda state:
       (state.has("Perfect Hatred (E4M2)", player, 1) and
        state.has("Shotgun", player, 1) and
        state.has("Chaingun", player, 1)) and
       (state.has("Rocket launcher", player, 1) or
        state.has("Plasma gun", player, 1) or
        state.has("BFG9000", player, 1)))
    set_rule(world.get_entrance("Perfect Hatred (E4M2) Main -> Perfect Hatred (E4M2) Blue", player), lambda state:
        state.has("Perfect Hatred (E4M2) - Blue skull key", player, 1))
    set_rule(world.get_entrance("Perfect Hatred (E4M2) Main -> Perfect Hatred (E4M2) Yellow", player), lambda state:
        state.has("Perfect Hatred (E4M2) - Yellow skull key", player, 1))

    # Sever the Wicked (E4M3)
    set_rule(world.get_entrance("Hub -> Sever the Wicked (E4M3) Main", player), lambda state:
       (state.has("Sever the Wicked (E4M3)", player, 1) and
        state.has("Shotgun", player, 1) and
        state.has("Chaingun", player, 1)) and
       (state.has("Rocket launcher", player, 1) or
        state.has("Plasma gun", player, 1) or
        state.has("BFG9000", player, 1)))
    set_rule(world.get_entrance("Sever the Wicked (E4M3) Main -> Sever the Wicked (E4M3) Red", player), lambda state:
        state.has("Sever the Wicked (E4M3) - Red skull key", player, 1))
    set_rule(world.get_entrance("Sever the Wicked (E4M3) Red -> Sever the Wicked (E4M3) Blue", player), lambda state:
        state.has("Sever the Wicked (E4M3) - Blue skull key", player, 1))
    set_rule(world.get_entrance("Sever the Wicked (E4M3) Red -> Sever the Wicked (E4M3) Main", player), lambda state:
        state.has("Sever the Wicked (E4M3) - Red skull key", player, 1))
    set_rule(world.get_entrance("Sever the Wicked (E4M3) Blue -> Sever the Wicked (E4M3) Red", player), lambda state:
        state.has("Sever the Wicked (E4M3) - Blue skull key", player, 1))

    # Unruly Evil (E4M4)
    set_rule(world.get_entrance("Hub -> Unruly Evil (E4M4) Main", player), lambda state:
       (state.has("Unruly Evil (E4M4)", player, 1) and
        state.has("Shotgun", player, 1) and
        state.has("Chaingun", player, 1)) and
       (state.has("Rocket launcher", player, 1) or
        state.has("Plasma gun", player, 1) or
        state.has("BFG9000", player, 1)))
    set_rule(world.get_entrance("Unruly Evil (E4M4) Main -> Unruly Evil (E4M4) Red", player), lambda state:
        state.has("Unruly Evil (E4M4) - Red skull key", player, 1))

    # They Will Repent (E4M5)
    set_rule(world.get_entrance("Hub -> They Will Repent (E4M5) Main", player), lambda state:
       (state.has("They Will Repent (E4M5)", player, 1) and
        state.has("Shotgun", player, 1) and
        state.has("Chaingun", player, 1)) and
       (state.has("Rocket launcher", player, 1) or
        state.has("Plasma gun", player, 1) or
        state.has("BFG9000", player, 1)))
    set_rule(world.get_entrance("They Will Repent (E4M5) Main -> They Will Repent (E4M5) Red", player), lambda state:
        state.has("They Will Repent (E4M5) - Red skull key", player, 1))
    set_rule(world.get_entrance("They Will Repent (E4M5) Red -> They Will Repent (E4M5) Main", player), lambda state:
        state.has("They Will Repent (E4M5) - Red skull key", player, 1))
    set_rule(world.get_entrance("They Will Repent (E4M5) Red -> They Will Repent (E4M5) Yellow", player), lambda state:
        state.has("They Will Repent (E4M5) - Yellow skull key", player, 1))
    set_rule(world.get_entrance("They Will Repent (E4M5) Red -> They Will Repent (E4M5) Blue", player), lambda state:
        state.has("They Will Repent (E4M5) - Blue skull key", player, 1))

    # Against Thee Wickedly (E4M6)
    set_rule(world.get_entrance("Hub -> Against Thee Wickedly (E4M6) Main", player), lambda state:
       (state.has("Against Thee Wickedly (E4M6)", player, 1) and
        state.has("Shotgun", player, 1) and
        state.has("Chaingun", player, 1)) and
       (state.has("Rocket launcher", player, 1) or
        state.has("Plasma gun", player, 1) or
        state.has("BFG9000", player, 1)))
    set_rule(world.get_entrance("Against Thee Wickedly (E4M6) Main -> Against Thee Wickedly (E4M6) Blue", player), lambda state:
        state.has("Against Thee Wickedly (E4M6) - Blue skull key", player, 1))
    set_rule(world.get_entrance("Against Thee Wickedly (E4M6) Blue -> Against Thee Wickedly (E4M6) Yellow", player), lambda state:
        state.has("Against Thee Wickedly (E4M6) - Yellow skull key", player, 1))
    set_rule(world.get_entrance("Against Thee Wickedly (E4M6) Blue -> Against Thee Wickedly (E4M6) Red", player), lambda state:
        state.has("Against Thee Wickedly (E4M6) - Red skull key", player, 1))

    # And Hell Followed (E4M7)
    set_rule(world.get_entrance("Hub -> And Hell Followed (E4M7) Main", player), lambda state:
       (state.has("And Hell Followed (E4M7)", player, 1) and
        state.has("Shotgun", player, 1) and
        state.has("Chaingun", player, 1)) and
       (state.has("Rocket launcher", player, 1) or
        state.has("Plasma gun", player, 1) or
        state.has("BFG9000", player, 1)))
    set_rule(world.get_entrance("And Hell Followed (E4M7) Main -> And Hell Followed (E4M7) Blue", player), lambda state:
        state.has("And Hell Followed (E4M7) - Blue skull key", player, 1))
    set_rule(world.get_entrance("And Hell Followed (E4M7) Main -> And Hell Followed (E4M7) Red", player), lambda state:
        state.has("And Hell Followed (E4M7) - Red skull key", player, 1))
    set_rule(world.get_entrance("And Hell Followed (E4M7) Main -> And Hell Followed (E4M7) Yellow", player), lambda state:
        state.has("And Hell Followed (E4M7) - Yellow skull key", player, 1))
    set_rule(world.get_entrance("And Hell Followed (E4M7) Red -> And Hell Followed (E4M7) Main", player), lambda state:
        state.has("And Hell Followed (E4M7) - Red skull key", player, 1))

    # Unto the Cruel (E4M8)
    set_rule(world.get_entrance("Hub -> Unto the Cruel (E4M8) Main", player), lambda state:
       (state.has("Unto the Cruel (E4M8)", player, 1) and
        state.has("Chainsaw", player, 1) and
        state.has("Shotgun", player, 1) and
        state.has("Chaingun", player, 1) and
        state.has("Rocket launcher", player, 1)) and
       (state.has("BFG9000", player, 1) or
        state.has("Plasma gun", player, 1)))
    set_rule(world.get_entrance("Unto the Cruel (E4M8) Main -> Unto the Cruel (E4M8) Red", player), lambda state:
        state.has("Unto the Cruel (E4M8) - Red skull key", player, 1))
    set_rule(world.get_entrance("Unto the Cruel (E4M8) Main -> Unto the Cruel (E4M8) Yellow", player), lambda state:
        state.has("Unto the Cruel (E4M8) - Yellow skull key", player, 1))
    set_rule(world.get_entrance("Unto the Cruel (E4M8) Main -> Unto the Cruel (E4M8) Orange", player), lambda state:
        state.has("Unto the Cruel (E4M8) - Yellow skull key", player, 1) and
        state.has("Unto the Cruel (E4M8) - Red skull key", player, 1))

    # Fear (E4M9)
    set_rule(world.get_entrance("Hub -> Fear (E4M9) Main", player), lambda state:
        state.has("Fear (E4M9)", player, 1) and
        state.has("Shotgun", player, 1) and
        state.has("Chaingun", player, 1) and
        state.has("Rocket launcher", player, 1) and
        state.has("Plasma gun", player, 1) and
        state.has("BFG9000", player, 1))
    set_rule(world.get_entrance("Fear (E4M9) Main -> Fear (E4M9) Yellow", player), lambda state:
        state.has("Fear (E4M9) - Yellow skull key", player, 1))
    set_rule(world.get_entrance("Fear (E4M9) Yellow -> Fear (E4M9) Main", player), lambda state:
        state.has("Fear (E4M9) - Yellow skull key", player, 1))


def set_rules(doom_1993_world: "DOOM1993World", included_episodes):
    player = doom_1993_world.player
    world = doom_1993_world.multiworld

    if included_episodes[0]:
        set_episode1_rules(player, world)
    if included_episodes[1]:
        set_episode2_rules(player, world)
    if included_episodes[2]:
        set_episode3_rules(player, world)
    if included_episodes[3]:
        set_episode4_rules(player, world)
