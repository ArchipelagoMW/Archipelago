# This file is auto generated. More info: https://github.com/Daivuk/apdoom

from typing import TYPE_CHECKING
from worlds.generic.Rules import set_rule

if TYPE_CHECKING:
    from . import DOOM2World


def set_episode1_rules(player, world, pro):
    # Entryway (MAP01)
    set_rule(world.get_entrance("Hub -> Entryway (MAP01) Main", player), lambda state:
        state.has("Entryway (MAP01)", player, 1))
    set_rule(world.get_entrance("Hub -> Entryway (MAP01) Main", player), lambda state:
        state.has("Entryway (MAP01)", player, 1))

    # Underhalls (MAP02)
    set_rule(world.get_entrance("Hub -> Underhalls (MAP02) Main", player), lambda state:
        state.has("Underhalls (MAP02)", player, 1))
    set_rule(world.get_entrance("Hub -> Underhalls (MAP02) Main", player), lambda state:
        state.has("Underhalls (MAP02)", player, 1))
    set_rule(world.get_entrance("Hub -> Underhalls (MAP02) Main", player), lambda state:
        state.has("Underhalls (MAP02)", player, 1))
    set_rule(world.get_entrance("Underhalls (MAP02) Main -> Underhalls (MAP02) Red", player), lambda state:
        state.has("Underhalls (MAP02) - Red keycard", player, 1))
    set_rule(world.get_entrance("Underhalls (MAP02) Blue -> Underhalls (MAP02) Red", player), lambda state:
        state.has("Underhalls (MAP02) - Blue keycard", player, 1))
    set_rule(world.get_entrance("Underhalls (MAP02) Red -> Underhalls (MAP02) Blue", player), lambda state:
        state.has("Underhalls (MAP02) - Blue keycard", player, 1))

    # The Gantlet (MAP03)
    set_rule(world.get_entrance("Hub -> The Gantlet (MAP03) Main", player), lambda state:
       (state.has("The Gantlet (MAP03)", player, 1)) and
       (state.has("Shotgun", player, 1) or
        state.has("Chaingun", player, 1) or
        state.has("Super Shotgun", player, 1)))
    set_rule(world.get_entrance("The Gantlet (MAP03) Main -> The Gantlet (MAP03) Blue", player), lambda state:
        state.has("The Gantlet (MAP03) - Blue keycard", player, 1))
    set_rule(world.get_entrance("The Gantlet (MAP03) Blue -> The Gantlet (MAP03) Red", player), lambda state:
        state.has("The Gantlet (MAP03) - Red keycard", player, 1))

    # The Focus (MAP04)
    set_rule(world.get_entrance("Hub -> The Focus (MAP04) Main", player), lambda state:
       (state.has("The Focus (MAP04)", player, 1)) and
       (state.has("Shotgun", player, 1) or
        state.has("Chaingun", player, 1) or
        state.has("Super Shotgun", player, 1)))
    set_rule(world.get_entrance("The Focus (MAP04) Main -> The Focus (MAP04) Red", player), lambda state:
        state.has("The Focus (MAP04) - Red keycard", player, 1))
    set_rule(world.get_entrance("The Focus (MAP04) Main -> The Focus (MAP04) Blue", player), lambda state:
        state.has("The Focus (MAP04) - Blue keycard", player, 1))
    set_rule(world.get_entrance("The Focus (MAP04) Yellow -> The Focus (MAP04) Red", player), lambda state:
        state.has("The Focus (MAP04) - Yellow keycard", player, 1))
    set_rule(world.get_entrance("The Focus (MAP04) Red -> The Focus (MAP04) Yellow", player), lambda state:
        state.has("The Focus (MAP04) - Yellow keycard", player, 1))
    set_rule(world.get_entrance("The Focus (MAP04) Red -> The Focus (MAP04) Main", player), lambda state:
        state.has("The Focus (MAP04) - Red keycard", player, 1))

    # The Waste Tunnels (MAP05)
    set_rule(world.get_entrance("Hub -> The Waste Tunnels (MAP05) Main", player), lambda state:
       (state.has("The Waste Tunnels (MAP05)", player, 1) and
        state.has("Shotgun", player, 1) and
        state.has("Chaingun", player, 1) and
        state.has("Super Shotgun", player, 1)) and
       (state.has("Rocket launcher", player, 1) or
        state.has("Plasma gun", player, 1) or
        state.has("BFG9000", player, 1)))
    set_rule(world.get_entrance("The Waste Tunnels (MAP05) Main -> The Waste Tunnels (MAP05) Red", player), lambda state:
        state.has("The Waste Tunnels (MAP05) - Red keycard", player, 1))
    set_rule(world.get_entrance("The Waste Tunnels (MAP05) Main -> The Waste Tunnels (MAP05) Blue", player), lambda state:
        state.has("The Waste Tunnels (MAP05) - Blue keycard", player, 1))
    set_rule(world.get_entrance("The Waste Tunnels (MAP05) Blue -> The Waste Tunnels (MAP05) Yellow", player), lambda state:
        state.has("The Waste Tunnels (MAP05) - Yellow keycard", player, 1))
    set_rule(world.get_entrance("The Waste Tunnels (MAP05) Blue -> The Waste Tunnels (MAP05) Main", player), lambda state:
        state.has("The Waste Tunnels (MAP05) - Blue keycard", player, 1))
    set_rule(world.get_entrance("The Waste Tunnels (MAP05) Yellow -> The Waste Tunnels (MAP05) Blue", player), lambda state:
        state.has("The Waste Tunnels (MAP05) - Yellow keycard", player, 1))

    # The Crusher (MAP06)
    set_rule(world.get_entrance("Hub -> The Crusher (MAP06) Main", player), lambda state:
       (state.has("The Crusher (MAP06)", player, 1) and
        state.has("Shotgun", player, 1) and
        state.has("Chaingun", player, 1) and
        state.has("Super Shotgun", player, 1)) and
       (state.has("Rocket launcher", player, 1) or
        state.has("Plasma gun", player, 1) or
        state.has("BFG9000", player, 1)))
    set_rule(world.get_entrance("The Crusher (MAP06) Main -> The Crusher (MAP06) Blue", player), lambda state:
        state.has("The Crusher (MAP06) - Blue keycard", player, 1))
    set_rule(world.get_entrance("The Crusher (MAP06) Blue -> The Crusher (MAP06) Red", player), lambda state:
        state.has("The Crusher (MAP06) - Red keycard", player, 1))
    set_rule(world.get_entrance("The Crusher (MAP06) Blue -> The Crusher (MAP06) Main", player), lambda state:
        state.has("The Crusher (MAP06) - Blue keycard", player, 1))
    set_rule(world.get_entrance("The Crusher (MAP06) Yellow -> The Crusher (MAP06) Red", player), lambda state:
        state.has("The Crusher (MAP06) - Yellow keycard", player, 1))
    set_rule(world.get_entrance("The Crusher (MAP06) Red -> The Crusher (MAP06) Yellow", player), lambda state:
        state.has("The Crusher (MAP06) - Yellow keycard", player, 1))
    set_rule(world.get_entrance("The Crusher (MAP06) Red -> The Crusher (MAP06) Blue", player), lambda state:
        state.has("The Crusher (MAP06) - Red keycard", player, 1))

    # Dead Simple (MAP07)
    set_rule(world.get_entrance("Hub -> Dead Simple (MAP07) Main", player), lambda state:
       (state.has("Dead Simple (MAP07)", player, 1) and
        state.has("Shotgun", player, 1) and
        state.has("Chaingun", player, 1) and
        state.has("Super Shotgun", player, 1)) and
       (state.has("Rocket launcher", player, 1) or
        state.has("Plasma gun", player, 1) or
        state.has("BFG9000", player, 1)))

    # Tricks and Traps (MAP08)
    set_rule(world.get_entrance("Hub -> Tricks and Traps (MAP08) Main", player), lambda state:
       (state.has("Tricks and Traps (MAP08)", player, 1) and
        state.has("Shotgun", player, 1) and
        state.has("Chaingun", player, 1) and
        state.has("Super Shotgun", player, 1)) and
       (state.has("Rocket launcher", player, 1) or
        state.has("Plasma gun", player, 1) or
        state.has("BFG9000", player, 1)))
    set_rule(world.get_entrance("Tricks and Traps (MAP08) Main -> Tricks and Traps (MAP08) Red", player), lambda state:
        state.has("Tricks and Traps (MAP08) - Red skull key", player, 1))
    set_rule(world.get_entrance("Tricks and Traps (MAP08) Main -> Tricks and Traps (MAP08) Yellow", player), lambda state:
        state.has("Tricks and Traps (MAP08) - Yellow skull key", player, 1))

    # The Pit (MAP09)
    set_rule(world.get_entrance("Hub -> The Pit (MAP09) Main", player), lambda state:
       (state.has("The Pit (MAP09)", player, 1) and
        state.has("Shotgun", player, 1) and
        state.has("Chaingun", player, 1) and
        state.has("Super Shotgun", player, 1)) and
       (state.has("Rocket launcher", player, 1) or
        state.has("Plasma gun", player, 1) or
        state.has("BFG9000", player, 1)))
    set_rule(world.get_entrance("The Pit (MAP09) Main -> The Pit (MAP09) Yellow", player), lambda state:
        state.has("The Pit (MAP09) - Yellow keycard", player, 1))
    set_rule(world.get_entrance("The Pit (MAP09) Main -> The Pit (MAP09) Blue", player), lambda state:
        state.has("The Pit (MAP09) - Blue keycard", player, 1))
    set_rule(world.get_entrance("The Pit (MAP09) Yellow -> The Pit (MAP09) Main", player), lambda state:
        state.has("The Pit (MAP09) - Yellow keycard", player, 1))

    # Refueling Base (MAP10)
    set_rule(world.get_entrance("Hub -> Refueling Base (MAP10) Main", player), lambda state:
       (state.has("Refueling Base (MAP10)", player, 1) and
        state.has("Shotgun", player, 1) and
        state.has("Chaingun", player, 1) and
        state.has("Super Shotgun", player, 1)) and
       (state.has("Rocket launcher", player, 1) or
        state.has("Plasma gun", player, 1) or
        state.has("BFG9000", player, 1)))
    set_rule(world.get_entrance("Refueling Base (MAP10) Main -> Refueling Base (MAP10) Yellow", player), lambda state:
        state.has("Refueling Base (MAP10) - Yellow keycard", player, 1))
    set_rule(world.get_entrance("Refueling Base (MAP10) Yellow -> Refueling Base (MAP10) Yellow Blue", player), lambda state:
        state.has("Refueling Base (MAP10) - Blue keycard", player, 1))

    # Circle of Death (MAP11)
    set_rule(world.get_entrance("Hub -> Circle of Death (MAP11) Main", player), lambda state:
       (state.has("Circle of Death (MAP11)", player, 1) and
        state.has("Shotgun", player, 1) and
        state.has("Chaingun", player, 1) and
        state.has("Super Shotgun", player, 1)) and
       (state.has("Rocket launcher", player, 1) or
        state.has("Plasma gun", player, 1) or
        state.has("BFG9000", player, 1)))
    set_rule(world.get_entrance("Circle of Death (MAP11) Main -> Circle of Death (MAP11) Blue", player), lambda state:
        state.has("Circle of Death (MAP11) - Blue keycard", player, 1))
    set_rule(world.get_entrance("Circle of Death (MAP11) Main -> Circle of Death (MAP11) Red", player), lambda state:
        state.has("Circle of Death (MAP11) - Red keycard", player, 1))


def set_episode2_rules(player, world, pro):
    # The Factory (MAP12)
    set_rule(world.get_entrance("Hub -> The Factory (MAP12) Main", player), lambda state:
       (state.has("The Factory (MAP12)", player, 1) and
        state.has("Shotgun", player, 1) and
        state.has("Chaingun", player, 1) and
        state.has("Super Shotgun", player, 1)) and
       (state.has("Rocket launcher", player, 1) or
        state.has("Plasma gun", player, 1) or
        state.has("BFG9000", player, 1)))
    set_rule(world.get_entrance("The Factory (MAP12) Main -> The Factory (MAP12) Yellow", player), lambda state:
        state.has("The Factory (MAP12) - Yellow keycard", player, 1))
    set_rule(world.get_entrance("The Factory (MAP12) Main -> The Factory (MAP12) Blue", player), lambda state:
        state.has("The Factory (MAP12) - Blue keycard", player, 1))

    # Downtown (MAP13)
    set_rule(world.get_entrance("Hub -> Downtown (MAP13) Main", player), lambda state:
       (state.has("Downtown (MAP13)", player, 1) and
        state.has("Shotgun", player, 1) and
        state.has("Chaingun", player, 1) and
        state.has("Super Shotgun", player, 1)) and
       (state.has("Rocket launcher", player, 1) or
        state.has("Plasma gun", player, 1) or
        state.has("BFG9000", player, 1)))
    set_rule(world.get_entrance("Downtown (MAP13) Main -> Downtown (MAP13) Yellow", player), lambda state:
        state.has("Downtown (MAP13) - Yellow keycard", player, 1))
    set_rule(world.get_entrance("Downtown (MAP13) Main -> Downtown (MAP13) Red", player), lambda state:
        state.has("Downtown (MAP13) - Red keycard", player, 1))
    set_rule(world.get_entrance("Downtown (MAP13) Main -> Downtown (MAP13) Blue", player), lambda state:
        state.has("Downtown (MAP13) - Blue keycard", player, 1))

    # The Inmost Dens (MAP14)
    set_rule(world.get_entrance("Hub -> The Inmost Dens (MAP14) Main", player), lambda state:
       (state.has("The Inmost Dens (MAP14)", player, 1) and
        state.has("Shotgun", player, 1) and
        state.has("Chaingun", player, 1) and
        state.has("Super Shotgun", player, 1)) and
       (state.has("Rocket launcher", player, 1) or
        state.has("Plasma gun", player, 1) or
        state.has("BFG9000", player, 1)))
    set_rule(world.get_entrance("The Inmost Dens (MAP14) Main -> The Inmost Dens (MAP14) Red", player), lambda state:
        state.has("The Inmost Dens (MAP14) - Red skull key", player, 1))
    set_rule(world.get_entrance("The Inmost Dens (MAP14) Blue -> The Inmost Dens (MAP14) Red East", player), lambda state:
        state.has("The Inmost Dens (MAP14) - Blue skull key", player, 1))
    set_rule(world.get_entrance("The Inmost Dens (MAP14) Red -> The Inmost Dens (MAP14) Main", player), lambda state:
        state.has("The Inmost Dens (MAP14) - Red skull key", player, 1))
    set_rule(world.get_entrance("The Inmost Dens (MAP14) Red East -> The Inmost Dens (MAP14) Blue", player), lambda state:
        state.has("The Inmost Dens (MAP14) - Blue skull key", player, 1))

    # Industrial Zone (MAP15)
    set_rule(world.get_entrance("Hub -> Industrial Zone (MAP15) Main", player), lambda state:
       (state.has("Industrial Zone (MAP15)", player, 1) and
        state.has("Shotgun", player, 1) and
        state.has("Chaingun", player, 1) and
        state.has("Super Shotgun", player, 1)) and
       (state.has("Rocket launcher", player, 1) or
        state.has("Plasma gun", player, 1) or
        state.has("BFG9000", player, 1)))
    set_rule(world.get_entrance("Industrial Zone (MAP15) Main -> Industrial Zone (MAP15) Yellow East", player), lambda state:
        state.has("Industrial Zone (MAP15) - Yellow keycard", player, 1))
    set_rule(world.get_entrance("Industrial Zone (MAP15) Main -> Industrial Zone (MAP15) Yellow West", player), lambda state:
        state.has("Industrial Zone (MAP15) - Yellow keycard", player, 1))
    set_rule(world.get_entrance("Industrial Zone (MAP15) Blue -> Industrial Zone (MAP15) Yellow East", player), lambda state:
        state.has("Industrial Zone (MAP15) - Blue keycard", player, 1))
    set_rule(world.get_entrance("Industrial Zone (MAP15) Yellow East -> Industrial Zone (MAP15) Blue", player), lambda state:
        state.has("Industrial Zone (MAP15) - Blue keycard", player, 1))

    # Suburbs (MAP16)
    set_rule(world.get_entrance("Hub -> Suburbs (MAP16) Main", player), lambda state:
       (state.has("Suburbs (MAP16)", player, 1) and
        state.has("Shotgun", player, 1) and
        state.has("Chaingun", player, 1) and
        state.has("Super Shotgun", player, 1)) and
       (state.has("Rocket launcher", player, 1) or
        state.has("Plasma gun", player, 1) or
        state.has("BFG9000", player, 1)))
    set_rule(world.get_entrance("Suburbs (MAP16) Main -> Suburbs (MAP16) Red", player), lambda state:
        state.has("Suburbs (MAP16) - Red skull key", player, 1))
    set_rule(world.get_entrance("Suburbs (MAP16) Main -> Suburbs (MAP16) Blue", player), lambda state:
        state.has("Suburbs (MAP16) - Blue skull key", player, 1))

    # Tenements (MAP17)
    set_rule(world.get_entrance("Hub -> Tenements (MAP17) Main", player), lambda state:
       (state.has("Tenements (MAP17)", player, 1) and
        state.has("Shotgun", player, 1) and
        state.has("Chaingun", player, 1) and
        state.has("Super Shotgun", player, 1)) and
       (state.has("Rocket launcher", player, 1) or
        state.has("Plasma gun", player, 1) or
        state.has("BFG9000", player, 1)))
    set_rule(world.get_entrance("Tenements (MAP17) Main -> Tenements (MAP17) Red", player), lambda state:
        state.has("Tenements (MAP17) - Red keycard", player, 1))
    set_rule(world.get_entrance("Tenements (MAP17) Red -> Tenements (MAP17) Yellow", player), lambda state:
        state.has("Tenements (MAP17) - Yellow skull key", player, 1))
    set_rule(world.get_entrance("Tenements (MAP17) Red -> Tenements (MAP17) Blue", player), lambda state:
        state.has("Tenements (MAP17) - Blue keycard", player, 1))

    # The Courtyard (MAP18)
    set_rule(world.get_entrance("Hub -> The Courtyard (MAP18) Main", player), lambda state:
       (state.has("The Courtyard (MAP18)", player, 1) and
        state.has("Shotgun", player, 1) and
        state.has("Chaingun", player, 1) and
        state.has("Super Shotgun", player, 1)) and
       (state.has("Rocket launcher", player, 1) or
        state.has("Plasma gun", player, 1) or
        state.has("BFG9000", player, 1)))
    set_rule(world.get_entrance("The Courtyard (MAP18) Main -> The Courtyard (MAP18) Yellow", player), lambda state:
        state.has("The Courtyard (MAP18) - Yellow skull key", player, 1))
    set_rule(world.get_entrance("The Courtyard (MAP18) Main -> The Courtyard (MAP18) Blue", player), lambda state:
        state.has("The Courtyard (MAP18) - Blue skull key", player, 1))
    set_rule(world.get_entrance("The Courtyard (MAP18) Blue -> The Courtyard (MAP18) Main", player), lambda state:
        state.has("The Courtyard (MAP18) - Blue skull key", player, 1))
    set_rule(world.get_entrance("The Courtyard (MAP18) Yellow -> The Courtyard (MAP18) Main", player), lambda state:
        state.has("The Courtyard (MAP18) - Yellow skull key", player, 1))

    # The Citadel (MAP19)
    set_rule(world.get_entrance("Hub -> The Citadel (MAP19) Main", player), lambda state:
       (state.has("The Citadel (MAP19)", player, 1) and
        state.has("Shotgun", player, 1) and
        state.has("Chaingun", player, 1) and
        state.has("Super Shotgun", player, 1)) and
       (state.has("Rocket launcher", player, 1) or
        state.has("Plasma gun", player, 1) or
        state.has("BFG9000", player, 1)))
    set_rule(world.get_entrance("The Citadel (MAP19) Main -> The Citadel (MAP19) Red", player), lambda state:
       (state.has("The Citadel (MAP19) - Red skull key", player, 1)) and       (state.has("The Citadel (MAP19) - Blue skull key", player, 1) or
        state.has("The Citadel (MAP19) - Yellow skull key", player, 1)))
    set_rule(world.get_entrance("The Citadel (MAP19) Red -> The Citadel (MAP19) Main", player), lambda state:
       (state.has("The Citadel (MAP19) - Red skull key", player, 1)) and       (state.has("The Citadel (MAP19) - Yellow skull key", player, 1) or
        state.has("The Citadel (MAP19) - Blue skull key", player, 1)))

    # Gotcha! (MAP20)
    set_rule(world.get_entrance("Hub -> Gotcha! (MAP20) Main", player), lambda state:
       (state.has("Gotcha! (MAP20)", player, 1) and
        state.has("Shotgun", player, 1) and
        state.has("Chaingun", player, 1) and
        state.has("Super Shotgun", player, 1)) and
       (state.has("Rocket launcher", player, 1) or
        state.has("Plasma gun", player, 1) or
        state.has("BFG9000", player, 1)))


def set_episode3_rules(player, world, pro):
    # Nirvana (MAP21)
    set_rule(world.get_entrance("Hub -> Nirvana (MAP21) Main", player), lambda state:
       (state.has("Nirvana (MAP21)", player, 1) and
        state.has("Shotgun", player, 1) and
        state.has("Chaingun", player, 1) and
        state.has("Super Shotgun", player, 1)) and
       (state.has("Rocket launcher", player, 1) or
        state.has("Plasma gun", player, 1) or
        state.has("BFG9000", player, 1)))
    set_rule(world.get_entrance("Nirvana (MAP21) Main -> Nirvana (MAP21) Yellow", player), lambda state:
        state.has("Nirvana (MAP21) - Yellow skull key", player, 1))
    set_rule(world.get_entrance("Nirvana (MAP21) Yellow -> Nirvana (MAP21) Main", player), lambda state:
        state.has("Nirvana (MAP21) - Yellow skull key", player, 1))
    set_rule(world.get_entrance("Nirvana (MAP21) Yellow -> Nirvana (MAP21) Magenta", player), lambda state:
        state.has("Nirvana (MAP21) - Red skull key", player, 1) and
        state.has("Nirvana (MAP21) - Blue skull key", player, 1))
    set_rule(world.get_entrance("Nirvana (MAP21) Magenta -> Nirvana (MAP21) Yellow", player), lambda state:
        state.has("Nirvana (MAP21) - Red skull key", player, 1) and
        state.has("Nirvana (MAP21) - Blue skull key", player, 1))

    # The Catacombs (MAP22)
    set_rule(world.get_entrance("Hub -> The Catacombs (MAP22) Main", player), lambda state:
       (state.has("The Catacombs (MAP22)", player, 1) and
        state.has("Shotgun", player, 1) and
        state.has("Chaingun", player, 1) and
        state.has("Super Shotgun", player, 1)) and
       (state.has("BFG9000", player, 1) or
        state.has("Rocket launcher", player, 1) or
        state.has("Plasma gun", player, 1)))
    set_rule(world.get_entrance("The Catacombs (MAP22) Main -> The Catacombs (MAP22) Blue", player), lambda state:
        state.has("The Catacombs (MAP22) - Blue skull key", player, 1))
    set_rule(world.get_entrance("The Catacombs (MAP22) Main -> The Catacombs (MAP22) Red", player), lambda state:
        state.has("The Catacombs (MAP22) - Red skull key", player, 1))
    set_rule(world.get_entrance("The Catacombs (MAP22) Red -> The Catacombs (MAP22) Main", player), lambda state:
        state.has("The Catacombs (MAP22) - Red skull key", player, 1))

    # Barrels o Fun (MAP23)
    set_rule(world.get_entrance("Hub -> Barrels o Fun (MAP23) Main", player), lambda state:
       (state.has("Barrels o Fun (MAP23)", player, 1) and
        state.has("Shotgun", player, 1) and
        state.has("Chaingun", player, 1) and
        state.has("Super Shotgun", player, 1)) and
       (state.has("Rocket launcher", player, 1) or
        state.has("Plasma gun", player, 1) or
        state.has("BFG9000", player, 1)))
    set_rule(world.get_entrance("Barrels o Fun (MAP23) Main -> Barrels o Fun (MAP23) Yellow", player), lambda state:
        state.has("Barrels o Fun (MAP23) - Yellow skull key", player, 1))
    set_rule(world.get_entrance("Barrels o Fun (MAP23) Yellow -> Barrels o Fun (MAP23) Main", player), lambda state:
        state.has("Barrels o Fun (MAP23) - Yellow skull key", player, 1))

    # The Chasm (MAP24)
    set_rule(world.get_entrance("Hub -> The Chasm (MAP24) Main", player), lambda state:
        state.has("The Chasm (MAP24)", player, 1) and
        state.has("Shotgun", player, 1) and
        state.has("Chaingun", player, 1) and
        state.has("Rocket launcher", player, 1) and
        state.has("Plasma gun", player, 1) and
        state.has("BFG9000", player, 1) and
        state.has("Super Shotgun", player, 1))
    set_rule(world.get_entrance("The Chasm (MAP24) Main -> The Chasm (MAP24) Red", player), lambda state:
        state.has("The Chasm (MAP24) - Red keycard", player, 1))
    set_rule(world.get_entrance("The Chasm (MAP24) Red -> The Chasm (MAP24) Main", player), lambda state:
        state.has("The Chasm (MAP24) - Red keycard", player, 1))

    # Bloodfalls (MAP25)
    set_rule(world.get_entrance("Hub -> Bloodfalls (MAP25) Main", player), lambda state:
        state.has("Bloodfalls (MAP25)", player, 1) and
        state.has("Shotgun", player, 1) and
        state.has("Chaingun", player, 1) and
        state.has("Rocket launcher", player, 1) and
        state.has("Plasma gun", player, 1) and
        state.has("BFG9000", player, 1) and
        state.has("Super Shotgun", player, 1))
    set_rule(world.get_entrance("Bloodfalls (MAP25) Main -> Bloodfalls (MAP25) Blue", player), lambda state:
        state.has("Bloodfalls (MAP25) - Blue skull key", player, 1))
    set_rule(world.get_entrance("Bloodfalls (MAP25) Blue -> Bloodfalls (MAP25) Main", player), lambda state:
        state.has("Bloodfalls (MAP25) - Blue skull key", player, 1))

    # The Abandoned Mines (MAP26)
    set_rule(world.get_entrance("Hub -> The Abandoned Mines (MAP26) Main", player), lambda state:
        state.has("The Abandoned Mines (MAP26)", player, 1) and
        state.has("Shotgun", player, 1) and
        state.has("Chaingun", player, 1) and
        state.has("Rocket launcher", player, 1) and
        state.has("BFG9000", player, 1) and
        state.has("Plasma gun", player, 1) and
        state.has("Super Shotgun", player, 1))
    set_rule(world.get_entrance("The Abandoned Mines (MAP26) Main -> The Abandoned Mines (MAP26) Yellow", player), lambda state:
        state.has("The Abandoned Mines (MAP26) - Yellow keycard", player, 1))
    set_rule(world.get_entrance("The Abandoned Mines (MAP26) Main -> The Abandoned Mines (MAP26) Red", player), lambda state:
        state.has("The Abandoned Mines (MAP26) - Red keycard", player, 1))
    set_rule(world.get_entrance("The Abandoned Mines (MAP26) Main -> The Abandoned Mines (MAP26) Blue", player), lambda state:
        state.has("The Abandoned Mines (MAP26) - Blue keycard", player, 1))
    set_rule(world.get_entrance("The Abandoned Mines (MAP26) Blue -> The Abandoned Mines (MAP26) Main", player), lambda state:
        state.has("The Abandoned Mines (MAP26) - Blue keycard", player, 1))
    set_rule(world.get_entrance("The Abandoned Mines (MAP26) Yellow -> The Abandoned Mines (MAP26) Main", player), lambda state:
        state.has("The Abandoned Mines (MAP26) - Yellow keycard", player, 1))

    # Monster Condo (MAP27)
    set_rule(world.get_entrance("Hub -> Monster Condo (MAP27) Main", player), lambda state:
        state.has("Monster Condo (MAP27)", player, 1) and
        state.has("Shotgun", player, 1) and
        state.has("Chaingun", player, 1) and
        state.has("Rocket launcher", player, 1) and
        state.has("Plasma gun", player, 1) and
        state.has("BFG9000", player, 1) and
        state.has("Super Shotgun", player, 1))
    set_rule(world.get_entrance("Monster Condo (MAP27) Main -> Monster Condo (MAP27) Yellow", player), lambda state:
        state.has("Monster Condo (MAP27) - Yellow skull key", player, 1))
    set_rule(world.get_entrance("Monster Condo (MAP27) Main -> Monster Condo (MAP27) Red", player), lambda state:
        state.has("Monster Condo (MAP27) - Red skull key", player, 1))
    set_rule(world.get_entrance("Monster Condo (MAP27) Main -> Monster Condo (MAP27) Blue", player), lambda state:
        state.has("Monster Condo (MAP27) - Blue skull key", player, 1))
    set_rule(world.get_entrance("Monster Condo (MAP27) Red -> Monster Condo (MAP27) Main", player), lambda state:
        state.has("Monster Condo (MAP27) - Red skull key", player, 1))

    # The Spirit World (MAP28)
    set_rule(world.get_entrance("Hub -> The Spirit World (MAP28) Main", player), lambda state:
        state.has("The Spirit World (MAP28)", player, 1) and
        state.has("Shotgun", player, 1) and
        state.has("Rocket launcher", player, 1) and
        state.has("Chaingun", player, 1) and
        state.has("Plasma gun", player, 1) and
        state.has("BFG9000", player, 1) and
        state.has("Super Shotgun", player, 1))
    set_rule(world.get_entrance("The Spirit World (MAP28) Main -> The Spirit World (MAP28) Yellow", player), lambda state:
        state.has("The Spirit World (MAP28) - Yellow skull key", player, 1))
    set_rule(world.get_entrance("The Spirit World (MAP28) Main -> The Spirit World (MAP28) Red", player), lambda state:
        state.has("The Spirit World (MAP28) - Red skull key", player, 1))
    set_rule(world.get_entrance("The Spirit World (MAP28) Yellow -> The Spirit World (MAP28) Main", player), lambda state:
        state.has("The Spirit World (MAP28) - Yellow skull key", player, 1))
    set_rule(world.get_entrance("The Spirit World (MAP28) Red -> The Spirit World (MAP28) Main", player), lambda state:
        state.has("The Spirit World (MAP28) - Red skull key", player, 1))

    # The Living End (MAP29)
    set_rule(world.get_entrance("Hub -> The Living End (MAP29) Main", player), lambda state:
        state.has("The Living End (MAP29)", player, 1) and
        state.has("Shotgun", player, 1) and
        state.has("Chaingun", player, 1) and
        state.has("Rocket launcher", player, 1) and
        state.has("Plasma gun", player, 1) and
        state.has("BFG9000", player, 1) and
        state.has("Super Shotgun", player, 1))

    # Icon of Sin (MAP30)
    set_rule(world.get_entrance("Hub -> Icon of Sin (MAP30) Main", player), lambda state:
        state.has("Icon of Sin (MAP30)", player, 1) and
        state.has("Rocket launcher", player, 1) and
        state.has("Shotgun", player, 1) and
        state.has("Chaingun", player, 1) and
        state.has("Plasma gun", player, 1) and
        state.has("BFG9000", player, 1) and
        state.has("Super Shotgun", player, 1))


def set_episode4_rules(player, world, pro):
    # Wolfenstein2 (MAP31)
    set_rule(world.get_entrance("Hub -> Wolfenstein2 (MAP31) Main", player), lambda state:
       (state.has("Wolfenstein2 (MAP31)", player, 1) and
        state.has("Shotgun", player, 1) and
        state.has("Chaingun", player, 1) and
        state.has("Super Shotgun", player, 1)) and
       (state.has("Rocket launcher", player, 1) or
        state.has("Plasma gun", player, 1) or
        state.has("BFG9000", player, 1)))

    # Grosse2 (MAP32)
    set_rule(world.get_entrance("Hub -> Grosse2 (MAP32) Main", player), lambda state:
       (state.has("Grosse2 (MAP32)", player, 1) and
        state.has("Shotgun", player, 1) and
        state.has("Chaingun", player, 1) and
        state.has("Super Shotgun", player, 1)) and
       (state.has("Rocket launcher", player, 1) or
        state.has("Plasma gun", player, 1) or
        state.has("BFG9000", player, 1)))


def set_rules(doom_ii_world: "DOOM2World", included_episodes, pro):
    player = doom_ii_world.player
    world = doom_ii_world.multiworld

    if included_episodes[0]:
        set_episode1_rules(player, world, pro)
    if included_episodes[1]:
        set_episode2_rules(player, world, pro)
    if included_episodes[2]:
        set_episode3_rules(player, world, pro)
    if included_episodes[3]:
        set_episode4_rules(player, world, pro)
