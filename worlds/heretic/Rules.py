# This file is auto generated. More info: https://github.com/Daivuk/apdoom

from typing import TYPE_CHECKING
from worlds.generic.Rules import set_rule

if TYPE_CHECKING:
    from . import HereticWorld


def set_episode1_rules(player, multiworld, pro):
    # The Docks (E1M1)
    set_rule(multiworld.get_entrance("Hub -> The Docks (E1M1) Main", player), lambda state:
        state.has("The Docks (E1M1)", player, 1))
    set_rule(multiworld.get_entrance("The Docks (E1M1) Main -> The Docks (E1M1) Yellow", player), lambda state:
        state.has("The Docks (E1M1) - Yellow key", player, 1))

    # The Dungeons (E1M2)
    set_rule(multiworld.get_entrance("Hub -> The Dungeons (E1M2) Main", player), lambda state:
       (state.has("The Dungeons (E1M2)", player, 1)) and
       (state.has("Dragon Claw", player, 1) or
        state.has("Ethereal Crossbow", player, 1)))
    set_rule(multiworld.get_entrance("The Dungeons (E1M2) Main -> The Dungeons (E1M2) Yellow", player), lambda state:
        state.has("The Dungeons (E1M2) - Yellow key", player, 1))
    set_rule(multiworld.get_entrance("The Dungeons (E1M2) Main -> The Dungeons (E1M2) Green", player), lambda state:
        state.has("The Dungeons (E1M2) - Green key", player, 1))
    set_rule(multiworld.get_entrance("The Dungeons (E1M2) Blue -> The Dungeons (E1M2) Yellow", player), lambda state:
        state.has("The Dungeons (E1M2) - Blue key", player, 1))
    set_rule(multiworld.get_entrance("The Dungeons (E1M2) Yellow -> The Dungeons (E1M2) Blue", player), lambda state:
        state.has("The Dungeons (E1M2) - Blue key", player, 1))

    # The Gatehouse (E1M3)
    set_rule(multiworld.get_entrance("Hub -> The Gatehouse (E1M3) Main", player), lambda state:
       (state.has("The Gatehouse (E1M3)", player, 1)) and
       (state.has("Ethereal Crossbow", player, 1) or
        state.has("Dragon Claw", player, 1)))
    set_rule(multiworld.get_entrance("The Gatehouse (E1M3) Main -> The Gatehouse (E1M3) Yellow", player), lambda state:
        state.has("The Gatehouse (E1M3) - Yellow key", player, 1))
    set_rule(multiworld.get_entrance("The Gatehouse (E1M3) Main -> The Gatehouse (E1M3) Sea", player), lambda state:
        state.has("The Gatehouse (E1M3) - Yellow key", player, 1))
    set_rule(multiworld.get_entrance("The Gatehouse (E1M3) Main -> The Gatehouse (E1M3) Green", player), lambda state:
        state.has("The Gatehouse (E1M3) - Green key", player, 1))
    set_rule(multiworld.get_entrance("The Gatehouse (E1M3) Green -> The Gatehouse (E1M3) Main", player), lambda state:
        state.has("The Gatehouse (E1M3) - Green key", player, 1))

    # The Guard Tower (E1M4)
    set_rule(multiworld.get_entrance("Hub -> The Guard Tower (E1M4) Main", player), lambda state:
       (state.has("The Guard Tower (E1M4)", player, 1)) and
       (state.has("Ethereal Crossbow", player, 1) or
        state.has("Dragon Claw", player, 1)))
    set_rule(multiworld.get_entrance("The Guard Tower (E1M4) Main -> The Guard Tower (E1M4) Yellow", player), lambda state:
        state.has("The Guard Tower (E1M4) - Yellow key", player, 1))
    set_rule(multiworld.get_entrance("The Guard Tower (E1M4) Yellow -> The Guard Tower (E1M4) Green", player), lambda state:
        state.has("The Guard Tower (E1M4) - Green key", player, 1))
    set_rule(multiworld.get_entrance("The Guard Tower (E1M4) Green -> The Guard Tower (E1M4) Yellow", player), lambda state:
        state.has("The Guard Tower (E1M4) - Green key", player, 1))

    # The Citadel (E1M5)
    set_rule(multiworld.get_entrance("Hub -> The Citadel (E1M5) Main", player), lambda state:
       (state.has("The Citadel (E1M5)", player, 1) and
        state.has("Ethereal Crossbow", player, 1)) and
       (state.has("Dragon Claw", player, 1) or
        state.has("Gauntlets of the Necromancer", player, 1)))
    set_rule(multiworld.get_entrance("The Citadel (E1M5) Main -> The Citadel (E1M5) Yellow", player), lambda state:
        state.has("The Citadel (E1M5) - Yellow key", player, 1))
    set_rule(multiworld.get_entrance("The Citadel (E1M5) Blue -> The Citadel (E1M5) Green", player), lambda state:
        state.has("The Citadel (E1M5) - Blue key", player, 1))
    set_rule(multiworld.get_entrance("The Citadel (E1M5) Yellow -> The Citadel (E1M5) Green", player), lambda state:
        state.has("The Citadel (E1M5) - Green key", player, 1))
    set_rule(multiworld.get_entrance("The Citadel (E1M5) Green -> The Citadel (E1M5) Blue", player), lambda state:
        state.has("The Citadel (E1M5) - Blue key", player, 1))

    # The Cathedral (E1M6)
    set_rule(multiworld.get_entrance("Hub -> The Cathedral (E1M6) Main", player), lambda state:
       (state.has("The Cathedral (E1M6)", player, 1) and
        state.has("Ethereal Crossbow", player, 1)) and
       (state.has("Gauntlets of the Necromancer", player, 1) or
        state.has("Dragon Claw", player, 1)))
    set_rule(multiworld.get_entrance("The Cathedral (E1M6) Main -> The Cathedral (E1M6) Yellow", player), lambda state:
        state.has("The Cathedral (E1M6) - Yellow key", player, 1))
    set_rule(multiworld.get_entrance("The Cathedral (E1M6) Yellow -> The Cathedral (E1M6) Green", player), lambda state:
        state.has("The Cathedral (E1M6) - Green key", player, 1))

    # The Crypts (E1M7)
    set_rule(multiworld.get_entrance("Hub -> The Crypts (E1M7) Main", player), lambda state:
       (state.has("The Crypts (E1M7)", player, 1) and
        state.has("Ethereal Crossbow", player, 1)) and
       (state.has("Gauntlets of the Necromancer", player, 1) or
        state.has("Dragon Claw", player, 1)))
    set_rule(multiworld.get_entrance("The Crypts (E1M7) Main -> The Crypts (E1M7) Yellow", player), lambda state:
        state.has("The Crypts (E1M7) - Yellow key", player, 1))
    set_rule(multiworld.get_entrance("The Crypts (E1M7) Main -> The Crypts (E1M7) Green", player), lambda state:
        state.has("The Crypts (E1M7) - Green key", player, 1))
    set_rule(multiworld.get_entrance("The Crypts (E1M7) Yellow -> The Crypts (E1M7) Green", player), lambda state:
        state.has("The Crypts (E1M7) - Green key", player, 1))
    set_rule(multiworld.get_entrance("The Crypts (E1M7) Yellow -> The Crypts (E1M7) Blue", player), lambda state:
        state.has("The Crypts (E1M7) - Blue key", player, 1))
    set_rule(multiworld.get_entrance("The Crypts (E1M7) Green -> The Crypts (E1M7) Main", player), lambda state:
        state.has("The Crypts (E1M7) - Green key", player, 1))

    # Hell's Maw (E1M8)
    set_rule(multiworld.get_entrance("Hub -> Hell's Maw (E1M8) Main", player), lambda state:
        state.has("Hell's Maw (E1M8)", player, 1) and
        state.has("Gauntlets of the Necromancer", player, 1) and
        state.has("Ethereal Crossbow", player, 1) and
        state.has("Dragon Claw", player, 1))

    # The Graveyard (E1M9)
    set_rule(multiworld.get_entrance("Hub -> The Graveyard (E1M9) Main", player), lambda state:
        state.has("The Graveyard (E1M9)", player, 1) and
        state.has("Gauntlets of the Necromancer", player, 1) and
        state.has("Ethereal Crossbow", player, 1) and
        state.has("Dragon Claw", player, 1))
    set_rule(multiworld.get_entrance("The Graveyard (E1M9) Main -> The Graveyard (E1M9) Yellow", player), lambda state:
        state.has("The Graveyard (E1M9) - Yellow key", player, 1))
    set_rule(multiworld.get_entrance("The Graveyard (E1M9) Main -> The Graveyard (E1M9) Green", player), lambda state:
        state.has("The Graveyard (E1M9) - Green key", player, 1))
    set_rule(multiworld.get_entrance("The Graveyard (E1M9) Main -> The Graveyard (E1M9) Blue", player), lambda state:
        state.has("The Graveyard (E1M9) - Blue key", player, 1))
    set_rule(multiworld.get_entrance("The Graveyard (E1M9) Yellow -> The Graveyard (E1M9) Main", player), lambda state:
        state.has("The Graveyard (E1M9) - Yellow key", player, 1))
    set_rule(multiworld.get_entrance("The Graveyard (E1M9) Green -> The Graveyard (E1M9) Main", player), lambda state:
        state.has("The Graveyard (E1M9) - Green key", player, 1))


def set_episode2_rules(player, multiworld, pro):
    # The Crater (E2M1)
    set_rule(multiworld.get_entrance("Hub -> The Crater (E2M1) Main", player), lambda state:
        state.has("The Crater (E2M1)", player, 1))
    set_rule(multiworld.get_entrance("The Crater (E2M1) Main -> The Crater (E2M1) Yellow", player), lambda state:
        state.has("The Crater (E2M1) - Yellow key", player, 1))
    set_rule(multiworld.get_entrance("The Crater (E2M1) Yellow -> The Crater (E2M1) Green", player), lambda state:
        state.has("The Crater (E2M1) - Green key", player, 1))
    set_rule(multiworld.get_entrance("The Crater (E2M1) Green -> The Crater (E2M1) Yellow", player), lambda state:
        state.has("The Crater (E2M1) - Green key", player, 1))

    # The Lava Pits (E2M2)
    set_rule(multiworld.get_entrance("Hub -> The Lava Pits (E2M2) Main", player), lambda state:
       (state.has("The Lava Pits (E2M2)", player, 1)) and
       (state.has("Ethereal Crossbow", player, 1) or
        state.has("Dragon Claw", player, 1)))
    set_rule(multiworld.get_entrance("The Lava Pits (E2M2) Main -> The Lava Pits (E2M2) Yellow", player), lambda state:
        state.has("The Lava Pits (E2M2) - Yellow key", player, 1))
    set_rule(multiworld.get_entrance("The Lava Pits (E2M2) Yellow -> The Lava Pits (E2M2) Green", player), lambda state:
        state.has("The Lava Pits (E2M2) - Green key", player, 1))
    set_rule(multiworld.get_entrance("The Lava Pits (E2M2) Yellow -> The Lava Pits (E2M2) Main", player), lambda state:
        state.has("The Lava Pits (E2M2) - Yellow key", player, 1))
    set_rule(multiworld.get_entrance("The Lava Pits (E2M2) Green -> The Lava Pits (E2M2) Yellow", player), lambda state:
        state.has("The Lava Pits (E2M2) - Green key", player, 1))

    # The River of Fire (E2M3)
    set_rule(multiworld.get_entrance("Hub -> The River of Fire (E2M3) Main", player), lambda state:
        state.has("The River of Fire (E2M3)", player, 1) and
        state.has("Dragon Claw", player, 1) and
        state.has("Ethereal Crossbow", player, 1))
    set_rule(multiworld.get_entrance("The River of Fire (E2M3) Main -> The River of Fire (E2M3) Yellow", player), lambda state:
        state.has("The River of Fire (E2M3) - Yellow key", player, 1))
    set_rule(multiworld.get_entrance("The River of Fire (E2M3) Main -> The River of Fire (E2M3) Blue", player), lambda state:
        state.has("The River of Fire (E2M3) - Blue key", player, 1))
    set_rule(multiworld.get_entrance("The River of Fire (E2M3) Main -> The River of Fire (E2M3) Green", player), lambda state:
        state.has("The River of Fire (E2M3) - Green key", player, 1))
    set_rule(multiworld.get_entrance("The River of Fire (E2M3) Blue -> The River of Fire (E2M3) Main", player), lambda state:
        state.has("The River of Fire (E2M3) - Blue key", player, 1))
    set_rule(multiworld.get_entrance("The River of Fire (E2M3) Yellow -> The River of Fire (E2M3) Main", player), lambda state:
        state.has("The River of Fire (E2M3) - Yellow key", player, 1))
    set_rule(multiworld.get_entrance("The River of Fire (E2M3) Green -> The River of Fire (E2M3) Main", player), lambda state:
        state.has("The River of Fire (E2M3) - Green key", player, 1))

    # The Ice Grotto (E2M4)
    set_rule(multiworld.get_entrance("Hub -> The Ice Grotto (E2M4) Main", player), lambda state:
       (state.has("The Ice Grotto (E2M4)", player, 1) and
        state.has("Ethereal Crossbow", player, 1) and
        state.has("Dragon Claw", player, 1)) and
       (state.has("Hellstaff", player, 1) or
        state.has("Firemace", player, 1)))
    set_rule(multiworld.get_entrance("The Ice Grotto (E2M4) Main -> The Ice Grotto (E2M4) Green", player), lambda state:
        state.has("The Ice Grotto (E2M4) - Green key", player, 1))
    set_rule(multiworld.get_entrance("The Ice Grotto (E2M4) Main -> The Ice Grotto (E2M4) Yellow", player), lambda state:
        state.has("The Ice Grotto (E2M4) - Yellow key", player, 1))
    set_rule(multiworld.get_entrance("The Ice Grotto (E2M4) Blue -> The Ice Grotto (E2M4) Green", player), lambda state:
        state.has("The Ice Grotto (E2M4) - Blue key", player, 1))
    set_rule(multiworld.get_entrance("The Ice Grotto (E2M4) Yellow -> The Ice Grotto (E2M4) Magenta", player), lambda state:
        state.has("The Ice Grotto (E2M4) - Green key", player, 1) and
        state.has("The Ice Grotto (E2M4) - Blue key", player, 1))
    set_rule(multiworld.get_entrance("The Ice Grotto (E2M4) Green -> The Ice Grotto (E2M4) Blue", player), lambda state:
        state.has("The Ice Grotto (E2M4) - Blue key", player, 1))

    # The Catacombs (E2M5)
    set_rule(multiworld.get_entrance("Hub -> The Catacombs (E2M5) Main", player), lambda state:
       (state.has("The Catacombs (E2M5)", player, 1) and
        state.has("Gauntlets of the Necromancer", player, 1) and
        state.has("Ethereal Crossbow", player, 1) and
        state.has("Dragon Claw", player, 1)) and
       (state.has("Phoenix Rod", player, 1) or
        state.has("Firemace", player, 1) or
        state.has("Hellstaff", player, 1)))
    set_rule(multiworld.get_entrance("The Catacombs (E2M5) Main -> The Catacombs (E2M5) Yellow", player), lambda state:
        state.has("The Catacombs (E2M5) - Yellow key", player, 1))
    set_rule(multiworld.get_entrance("The Catacombs (E2M5) Blue -> The Catacombs (E2M5) Green", player), lambda state:
        state.has("The Catacombs (E2M5) - Blue key", player, 1))
    set_rule(multiworld.get_entrance("The Catacombs (E2M5) Yellow -> The Catacombs (E2M5) Green", player), lambda state:
        state.has("The Catacombs (E2M5) - Green key", player, 1))
    set_rule(multiworld.get_entrance("The Catacombs (E2M5) Green -> The Catacombs (E2M5) Blue", player), lambda state:
        state.has("The Catacombs (E2M5) - Blue key", player, 1))

    # The Labyrinth (E2M6)
    set_rule(multiworld.get_entrance("Hub -> The Labyrinth (E2M6) Main", player), lambda state:
       (state.has("The Labyrinth (E2M6)", player, 1) and
        state.has("Gauntlets of the Necromancer", player, 1) and
        state.has("Ethereal Crossbow", player, 1) and
        state.has("Dragon Claw", player, 1)) and
       (state.has("Phoenix Rod", player, 1) or
        state.has("Firemace", player, 1) or
        state.has("Hellstaff", player, 1)))
    set_rule(multiworld.get_entrance("The Labyrinth (E2M6) Main -> The Labyrinth (E2M6) Blue", player), lambda state:
        state.has("The Labyrinth (E2M6) - Blue key", player, 1))
    set_rule(multiworld.get_entrance("The Labyrinth (E2M6) Main -> The Labyrinth (E2M6) Yellow", player), lambda state:
        state.has("The Labyrinth (E2M6) - Yellow key", player, 1))
    set_rule(multiworld.get_entrance("The Labyrinth (E2M6) Main -> The Labyrinth (E2M6) Green", player), lambda state:
        state.has("The Labyrinth (E2M6) - Green key", player, 1))
    set_rule(multiworld.get_entrance("The Labyrinth (E2M6) Blue -> The Labyrinth (E2M6) Main", player), lambda state:
        state.has("The Labyrinth (E2M6) - Blue key", player, 1))

    # The Great Hall (E2M7)
    set_rule(multiworld.get_entrance("Hub -> The Great Hall (E2M7) Main", player), lambda state:
       (state.has("The Great Hall (E2M7)", player, 1) and
        state.has("Gauntlets of the Necromancer", player, 1) and
        state.has("Ethereal Crossbow", player, 1) and
        state.has("Dragon Claw", player, 1) and
        state.has("Firemace", player, 1)) and
       (state.has("Phoenix Rod", player, 1) or
        state.has("Hellstaff", player, 1)))
    set_rule(multiworld.get_entrance("The Great Hall (E2M7) Main -> The Great Hall (E2M7) Yellow", player), lambda state:
        state.has("The Great Hall (E2M7) - Yellow key", player, 1))
    set_rule(multiworld.get_entrance("The Great Hall (E2M7) Main -> The Great Hall (E2M7) Green", player), lambda state:
        state.has("The Great Hall (E2M7) - Green key", player, 1))
    set_rule(multiworld.get_entrance("The Great Hall (E2M7) Blue -> The Great Hall (E2M7) Yellow", player), lambda state:
        state.has("The Great Hall (E2M7) - Blue key", player, 1))
    set_rule(multiworld.get_entrance("The Great Hall (E2M7) Yellow -> The Great Hall (E2M7) Blue", player), lambda state:
        state.has("The Great Hall (E2M7) - Blue key", player, 1))
    set_rule(multiworld.get_entrance("The Great Hall (E2M7) Yellow -> The Great Hall (E2M7) Main", player), lambda state:
        state.has("The Great Hall (E2M7) - Yellow key", player, 1))

    # The Portals of Chaos (E2M8)
    set_rule(multiworld.get_entrance("Hub -> The Portals of Chaos (E2M8) Main", player), lambda state:
        state.has("The Portals of Chaos (E2M8)", player, 1) and
        state.has("Gauntlets of the Necromancer", player, 1) and
        state.has("Ethereal Crossbow", player, 1) and
        state.has("Dragon Claw", player, 1) and
        state.has("Phoenix Rod", player, 1) and
        state.has("Firemace", player, 1) and
        state.has("Hellstaff", player, 1))

    # The Glacier (E2M9)
    set_rule(multiworld.get_entrance("Hub -> The Glacier (E2M9) Main", player), lambda state:
       (state.has("The Glacier (E2M9)", player, 1) and
        state.has("Gauntlets of the Necromancer", player, 1) and
        state.has("Ethereal Crossbow", player, 1) and
        state.has("Dragon Claw", player, 1) and
        state.has("Firemace", player, 1)) and
       (state.has("Phoenix Rod", player, 1) or
        state.has("Hellstaff", player, 1)))
    set_rule(multiworld.get_entrance("The Glacier (E2M9) Main -> The Glacier (E2M9) Yellow", player), lambda state:
        state.has("The Glacier (E2M9) - Yellow key", player, 1))
    set_rule(multiworld.get_entrance("The Glacier (E2M9) Main -> The Glacier (E2M9) Blue", player), lambda state:
        state.has("The Glacier (E2M9) - Blue key", player, 1))
    set_rule(multiworld.get_entrance("The Glacier (E2M9) Main -> The Glacier (E2M9) Green", player), lambda state:
        state.has("The Glacier (E2M9) - Green key", player, 1))
    set_rule(multiworld.get_entrance("The Glacier (E2M9) Blue -> The Glacier (E2M9) Main", player), lambda state:
        state.has("The Glacier (E2M9) - Blue key", player, 1))
    set_rule(multiworld.get_entrance("The Glacier (E2M9) Yellow -> The Glacier (E2M9) Main", player), lambda state:
        state.has("The Glacier (E2M9) - Yellow key", player, 1))


def set_episode3_rules(player, multiworld, pro):
    # The Storehouse (E3M1)
    set_rule(multiworld.get_entrance("Hub -> The Storehouse (E3M1) Main", player), lambda state:
        state.has("The Storehouse (E3M1)", player, 1))
    set_rule(multiworld.get_entrance("The Storehouse (E3M1) Main -> The Storehouse (E3M1) Yellow", player), lambda state:
        state.has("The Storehouse (E3M1) - Yellow key", player, 1))
    set_rule(multiworld.get_entrance("The Storehouse (E3M1) Main -> The Storehouse (E3M1) Green", player), lambda state:
        state.has("The Storehouse (E3M1) - Green key", player, 1))
    set_rule(multiworld.get_entrance("The Storehouse (E3M1) Yellow -> The Storehouse (E3M1) Main", player), lambda state:
        state.has("The Storehouse (E3M1) - Yellow key", player, 1))
    set_rule(multiworld.get_entrance("The Storehouse (E3M1) Green -> The Storehouse (E3M1) Main", player), lambda state:
        state.has("The Storehouse (E3M1) - Green key", player, 1))

    # The Cesspool (E3M2)
    set_rule(multiworld.get_entrance("Hub -> The Cesspool (E3M2) Main", player), lambda state:
        state.has("The Cesspool (E3M2)", player, 1) and
        state.has("Ethereal Crossbow", player, 1) and
        state.has("Dragon Claw", player, 1) and
        state.has("Firemace", player, 1) and
        state.has("Hellstaff", player, 1))
    set_rule(multiworld.get_entrance("The Cesspool (E3M2) Main -> The Cesspool (E3M2) Yellow", player), lambda state:
        state.has("The Cesspool (E3M2) - Yellow key", player, 1))
    set_rule(multiworld.get_entrance("The Cesspool (E3M2) Blue -> The Cesspool (E3M2) Green", player), lambda state:
        state.has("The Cesspool (E3M2) - Blue key", player, 1))
    set_rule(multiworld.get_entrance("The Cesspool (E3M2) Yellow -> The Cesspool (E3M2) Green", player), lambda state:
        state.has("The Cesspool (E3M2) - Green key", player, 1))
    set_rule(multiworld.get_entrance("The Cesspool (E3M2) Green -> The Cesspool (E3M2) Blue", player), lambda state:
        state.has("The Cesspool (E3M2) - Blue key", player, 1))
    set_rule(multiworld.get_entrance("The Cesspool (E3M2) Green -> The Cesspool (E3M2) Yellow", player), lambda state:
        state.has("The Cesspool (E3M2) - Green key", player, 1))

    # The Confluence (E3M3)
    set_rule(multiworld.get_entrance("Hub -> The Confluence (E3M3) Main", player), lambda state:
       (state.has("The Confluence (E3M3)", player, 1) and
        state.has("Ethereal Crossbow", player, 1) and
        state.has("Dragon Claw", player, 1)) and
       (state.has("Gauntlets of the Necromancer", player, 1) or
        state.has("Phoenix Rod", player, 1) or
        state.has("Firemace", player, 1) or
        state.has("Hellstaff", player, 1)))
    set_rule(multiworld.get_entrance("The Confluence (E3M3) Main -> The Confluence (E3M3) Green", player), lambda state:
        state.has("The Confluence (E3M3) - Green key", player, 1))
    set_rule(multiworld.get_entrance("The Confluence (E3M3) Main -> The Confluence (E3M3) Yellow", player), lambda state:
        state.has("The Confluence (E3M3) - Yellow key", player, 1))
    set_rule(multiworld.get_entrance("The Confluence (E3M3) Blue -> The Confluence (E3M3) Green", player), lambda state:
        state.has("The Confluence (E3M3) - Blue key", player, 1))
    set_rule(multiworld.get_entrance("The Confluence (E3M3) Green -> The Confluence (E3M3) Main", player), lambda state:
        state.has("The Confluence (E3M3) - Green key", player, 1))
    set_rule(multiworld.get_entrance("The Confluence (E3M3) Green -> The Confluence (E3M3) Blue", player), lambda state:
        state.has("The Confluence (E3M3) - Blue key", player, 1))

    # The Azure Fortress (E3M4)
    set_rule(multiworld.get_entrance("Hub -> The Azure Fortress (E3M4) Main", player), lambda state:
       (state.has("The Azure Fortress (E3M4)", player, 1) and
        state.has("Ethereal Crossbow", player, 1) and
        state.has("Dragon Claw", player, 1) and
        state.has("Hellstaff", player, 1)) and
       (state.has("Firemace", player, 1) or
        state.has("Phoenix Rod", player, 1) or
        state.has("Gauntlets of the Necromancer", player, 1)))
    set_rule(multiworld.get_entrance("The Azure Fortress (E3M4) Main -> The Azure Fortress (E3M4) Green", player), lambda state:
        state.has("The Azure Fortress (E3M4) - Green key", player, 1))
    set_rule(multiworld.get_entrance("The Azure Fortress (E3M4) Main -> The Azure Fortress (E3M4) Yellow", player), lambda state:
        state.has("The Azure Fortress (E3M4) - Yellow key", player, 1))

    # The Ophidian Lair (E3M5)
    set_rule(multiworld.get_entrance("Hub -> The Ophidian Lair (E3M5) Main", player), lambda state:
       (state.has("The Ophidian Lair (E3M5)", player, 1) and
        state.has("Ethereal Crossbow", player, 1) and
        state.has("Dragon Claw", player, 1) and
        state.has("Hellstaff", player, 1)) and
       (state.has("Gauntlets of the Necromancer", player, 1) or
        state.has("Phoenix Rod", player, 1) or
        state.has("Firemace", player, 1)))
    set_rule(multiworld.get_entrance("The Ophidian Lair (E3M5) Main -> The Ophidian Lair (E3M5) Yellow", player), lambda state:
        state.has("The Ophidian Lair (E3M5) - Yellow key", player, 1))
    set_rule(multiworld.get_entrance("The Ophidian Lair (E3M5) Main -> The Ophidian Lair (E3M5) Green", player), lambda state:
        state.has("The Ophidian Lair (E3M5) - Green key", player, 1))

    # The Halls of Fear (E3M6)
    set_rule(multiworld.get_entrance("Hub -> The Halls of Fear (E3M6) Main", player), lambda state:
       (state.has("The Halls of Fear (E3M6)", player, 1) and
        state.has("Firemace", player, 1) and
        state.has("Hellstaff", player, 1) and
        state.has("Dragon Claw", player, 1) and
        state.has("Ethereal Crossbow", player, 1)) and
       (state.has("Gauntlets of the Necromancer", player, 1) or
        state.has("Phoenix Rod", player, 1)))
    set_rule(multiworld.get_entrance("The Halls of Fear (E3M6) Main -> The Halls of Fear (E3M6) Yellow", player), lambda state:
        state.has("The Halls of Fear (E3M6) - Yellow key", player, 1))
    set_rule(multiworld.get_entrance("The Halls of Fear (E3M6) Blue -> The Halls of Fear (E3M6) Yellow", player), lambda state:
        state.has("The Halls of Fear (E3M6) - Blue key", player, 1))
    set_rule(multiworld.get_entrance("The Halls of Fear (E3M6) Yellow -> The Halls of Fear (E3M6) Blue", player), lambda state:
        state.has("The Halls of Fear (E3M6) - Blue key", player, 1))
    set_rule(multiworld.get_entrance("The Halls of Fear (E3M6) Yellow -> The Halls of Fear (E3M6) Green", player), lambda state:
        state.has("The Halls of Fear (E3M6) - Green key", player, 1))

    # The Chasm (E3M7)
    set_rule(multiworld.get_entrance("Hub -> The Chasm (E3M7) Main", player), lambda state:
       (state.has("The Chasm (E3M7)", player, 1) and
        state.has("Ethereal Crossbow", player, 1) and
        state.has("Dragon Claw", player, 1) and
        state.has("Firemace", player, 1) and
        state.has("Hellstaff", player, 1)) and
       (state.has("Gauntlets of the Necromancer", player, 1) or
        state.has("Phoenix Rod", player, 1)))
    set_rule(multiworld.get_entrance("The Chasm (E3M7) Main -> The Chasm (E3M7) Yellow", player), lambda state:
        state.has("The Chasm (E3M7) - Yellow key", player, 1))
    set_rule(multiworld.get_entrance("The Chasm (E3M7) Yellow -> The Chasm (E3M7) Main", player), lambda state:
        state.has("The Chasm (E3M7) - Yellow key", player, 1))
    set_rule(multiworld.get_entrance("The Chasm (E3M7) Yellow -> The Chasm (E3M7) Green", player), lambda state:
        state.has("The Chasm (E3M7) - Green key", player, 1))
    set_rule(multiworld.get_entrance("The Chasm (E3M7) Yellow -> The Chasm (E3M7) Blue", player), lambda state:
        state.has("The Chasm (E3M7) - Blue key", player, 1))
    set_rule(multiworld.get_entrance("The Chasm (E3M7) Green -> The Chasm (E3M7) Yellow", player), lambda state:
        state.has("The Chasm (E3M7) - Green key", player, 1))

    # D'Sparil'S Keep (E3M8)
    set_rule(multiworld.get_entrance("Hub -> D'Sparil'S Keep (E3M8) Main", player), lambda state:
        state.has("D'Sparil'S Keep (E3M8)", player, 1) and
        state.has("Gauntlets of the Necromancer", player, 1) and
        state.has("Ethereal Crossbow", player, 1) and
        state.has("Dragon Claw", player, 1) and
        state.has("Phoenix Rod", player, 1) and
        state.has("Firemace", player, 1) and
        state.has("Hellstaff", player, 1))

    # The Aquifier (E3M9)
    set_rule(multiworld.get_entrance("Hub -> The Aquifier (E3M9) Main", player), lambda state:
        state.has("The Aquifier (E3M9)", player, 1) and
        state.has("Gauntlets of the Necromancer", player, 1) and
        state.has("Ethereal Crossbow", player, 1) and
        state.has("Dragon Claw", player, 1) and
        state.has("Phoenix Rod", player, 1) and
        state.has("Firemace", player, 1) and
        state.has("Hellstaff", player, 1))
    set_rule(multiworld.get_entrance("The Aquifier (E3M9) Main -> The Aquifier (E3M9) Yellow", player), lambda state:
        state.has("The Aquifier (E3M9) - Yellow key", player, 1))
    set_rule(multiworld.get_entrance("The Aquifier (E3M9) Yellow -> The Aquifier (E3M9) Green", player), lambda state:
        state.has("The Aquifier (E3M9) - Green key", player, 1))
    set_rule(multiworld.get_entrance("The Aquifier (E3M9) Yellow -> The Aquifier (E3M9) Main", player), lambda state:
        state.has("The Aquifier (E3M9) - Yellow key", player, 1))
    set_rule(multiworld.get_entrance("The Aquifier (E3M9) Green -> The Aquifier (E3M9) Yellow", player), lambda state:
        state.has("The Aquifier (E3M9) - Green key", player, 1))


def set_episode4_rules(player, multiworld, pro):
    # Catafalque (E4M1)
    set_rule(multiworld.get_entrance("Hub -> Catafalque (E4M1) Main", player), lambda state:
        state.has("Catafalque (E4M1)", player, 1))
    set_rule(multiworld.get_entrance("Catafalque (E4M1) Main -> Catafalque (E4M1) Yellow", player), lambda state:
        state.has("Catafalque (E4M1) - Yellow key", player, 1))
    set_rule(multiworld.get_entrance("Catafalque (E4M1) Yellow -> Catafalque (E4M1) Green", player), lambda state:
       (state.has("Catafalque (E4M1) - Green key", player, 1)) and       (state.has("Ethereal Crossbow", player, 1) or
        state.has("Dragon Claw", player, 1) or
        state.has("Phoenix Rod", player, 1) or
        state.has("Firemace", player, 1) or
        state.has("Hellstaff", player, 1)))

    # Blockhouse (E4M2)
    set_rule(multiworld.get_entrance("Hub -> Blockhouse (E4M2) Main", player), lambda state:
        state.has("Blockhouse (E4M2)", player, 1) and
        state.has("Ethereal Crossbow", player, 1) and
        state.has("Dragon Claw", player, 1))
    set_rule(multiworld.get_entrance("Blockhouse (E4M2) Main -> Blockhouse (E4M2) Yellow", player), lambda state:
        state.has("Blockhouse (E4M2) - Yellow key", player, 1))
    set_rule(multiworld.get_entrance("Blockhouse (E4M2) Main -> Blockhouse (E4M2) Green", player), lambda state:
        state.has("Blockhouse (E4M2) - Green key", player, 1))
    set_rule(multiworld.get_entrance("Blockhouse (E4M2) Main -> Blockhouse (E4M2) Blue", player), lambda state:
        state.has("Blockhouse (E4M2) - Blue key", player, 1))
    set_rule(multiworld.get_entrance("Blockhouse (E4M2) Green -> Blockhouse (E4M2) Main", player), lambda state:
        state.has("Blockhouse (E4M2) - Green key", player, 1))
    set_rule(multiworld.get_entrance("Blockhouse (E4M2) Blue -> Blockhouse (E4M2) Main", player), lambda state:
        state.has("Blockhouse (E4M2) - Blue key", player, 1))

    # Ambulatory (E4M3)
    set_rule(multiworld.get_entrance("Hub -> Ambulatory (E4M3) Main", player), lambda state:
       (state.has("Ambulatory (E4M3)", player, 1) and
        state.has("Ethereal Crossbow", player, 1) and
        state.has("Dragon Claw", player, 1) and
        state.has("Gauntlets of the Necromancer", player, 1)) and
       (state.has("Phoenix Rod", player, 1) or
        state.has("Firemace", player, 1) or
        state.has("Hellstaff", player, 1)))
    set_rule(multiworld.get_entrance("Ambulatory (E4M3) Main -> Ambulatory (E4M3) Blue", player), lambda state:
        state.has("Ambulatory (E4M3) - Blue key", player, 1))
    set_rule(multiworld.get_entrance("Ambulatory (E4M3) Main -> Ambulatory (E4M3) Yellow", player), lambda state:
        state.has("Ambulatory (E4M3) - Yellow key", player, 1))
    set_rule(multiworld.get_entrance("Ambulatory (E4M3) Main -> Ambulatory (E4M3) Green", player), lambda state:
        state.has("Ambulatory (E4M3) - Green key", player, 1))
    set_rule(multiworld.get_entrance("Ambulatory (E4M3) Main -> Ambulatory (E4M3) Green Lock", player), lambda state:
        state.has("Ambulatory (E4M3) - Green key", player, 1))

    # Sepulcher (E4M4)
    set_rule(multiworld.get_entrance("Hub -> Sepulcher (E4M4) Main", player), lambda state:
       (state.has("Sepulcher (E4M4)", player, 1) and
        state.has("Ethereal Crossbow", player, 1) and
        state.has("Dragon Claw", player, 1) and
        state.has("Gauntlets of the Necromancer", player, 1) and
        state.has("Firemace", player, 1)) and
       (state.has("Phoenix Rod", player, 1) or
        state.has("Hellstaff", player, 1)))

    # Great Stair (E4M5)
    set_rule(multiworld.get_entrance("Hub -> Great Stair (E4M5) Main", player), lambda state:
       (state.has("Great Stair (E4M5)", player, 1) and
        state.has("Gauntlets of the Necromancer", player, 1) and
        state.has("Ethereal Crossbow", player, 1) and
        state.has("Dragon Claw", player, 1) and
        state.has("Firemace", player, 1)) and
       (state.has("Hellstaff", player, 1) or
        state.has("Phoenix Rod", player, 1)))
    set_rule(multiworld.get_entrance("Great Stair (E4M5) Main -> Great Stair (E4M5) Yellow", player), lambda state:
        state.has("Great Stair (E4M5) - Yellow key", player, 1))
    set_rule(multiworld.get_entrance("Great Stair (E4M5) Blue -> Great Stair (E4M5) Green", player), lambda state:
        state.has("Great Stair (E4M5) - Blue key", player, 1))
    set_rule(multiworld.get_entrance("Great Stair (E4M5) Yellow -> Great Stair (E4M5) Green", player), lambda state:
        state.has("Great Stair (E4M5) - Green key", player, 1))
    set_rule(multiworld.get_entrance("Great Stair (E4M5) Green -> Great Stair (E4M5) Blue", player), lambda state:
        state.has("Great Stair (E4M5) - Blue key", player, 1))
    set_rule(multiworld.get_entrance("Great Stair (E4M5) Green -> Great Stair (E4M5) Yellow", player), lambda state:
        state.has("Great Stair (E4M5) - Green key", player, 1))

    # Halls of the Apostate (E4M6)
    set_rule(multiworld.get_entrance("Hub -> Halls of the Apostate (E4M6) Main", player), lambda state:
       (state.has("Halls of the Apostate (E4M6)", player, 1) and
        state.has("Gauntlets of the Necromancer", player, 1) and
        state.has("Ethereal Crossbow", player, 1) and
        state.has("Dragon Claw", player, 1) and
        state.has("Firemace", player, 1)) and
       (state.has("Phoenix Rod", player, 1) or
        state.has("Hellstaff", player, 1)))
    set_rule(multiworld.get_entrance("Halls of the Apostate (E4M6) Main -> Halls of the Apostate (E4M6) Yellow", player), lambda state:
        state.has("Halls of the Apostate (E4M6) - Yellow key", player, 1))
    set_rule(multiworld.get_entrance("Halls of the Apostate (E4M6) Blue -> Halls of the Apostate (E4M6) Green", player), lambda state:
        state.has("Halls of the Apostate (E4M6) - Blue key", player, 1))
    set_rule(multiworld.get_entrance("Halls of the Apostate (E4M6) Yellow -> Halls of the Apostate (E4M6) Green", player), lambda state:
        state.has("Halls of the Apostate (E4M6) - Green key", player, 1))
    set_rule(multiworld.get_entrance("Halls of the Apostate (E4M6) Green -> Halls of the Apostate (E4M6) Yellow", player), lambda state:
        state.has("Halls of the Apostate (E4M6) - Green key", player, 1))
    set_rule(multiworld.get_entrance("Halls of the Apostate (E4M6) Green -> Halls of the Apostate (E4M6) Blue", player), lambda state:
        state.has("Halls of the Apostate (E4M6) - Blue key", player, 1))

    # Ramparts of Perdition (E4M7)
    set_rule(multiworld.get_entrance("Hub -> Ramparts of Perdition (E4M7) Main", player), lambda state:
       (state.has("Ramparts of Perdition (E4M7)", player, 1) and
        state.has("Gauntlets of the Necromancer", player, 1) and
        state.has("Ethereal Crossbow", player, 1) and
        state.has("Dragon Claw", player, 1) and
        state.has("Firemace", player, 1)) and
       (state.has("Phoenix Rod", player, 1) or
        state.has("Hellstaff", player, 1)))
    set_rule(multiworld.get_entrance("Ramparts of Perdition (E4M7) Main -> Ramparts of Perdition (E4M7) Yellow", player), lambda state:
        state.has("Ramparts of Perdition (E4M7) - Yellow key", player, 1))
    set_rule(multiworld.get_entrance("Ramparts of Perdition (E4M7) Blue -> Ramparts of Perdition (E4M7) Yellow", player), lambda state:
        state.has("Ramparts of Perdition (E4M7) - Blue key", player, 1))
    set_rule(multiworld.get_entrance("Ramparts of Perdition (E4M7) Yellow -> Ramparts of Perdition (E4M7) Main", player), lambda state:
        state.has("Ramparts of Perdition (E4M7) - Yellow key", player, 1))
    set_rule(multiworld.get_entrance("Ramparts of Perdition (E4M7) Yellow -> Ramparts of Perdition (E4M7) Green", player), lambda state:
        state.has("Ramparts of Perdition (E4M7) - Green key", player, 1))
    set_rule(multiworld.get_entrance("Ramparts of Perdition (E4M7) Yellow -> Ramparts of Perdition (E4M7) Blue", player), lambda state:
        state.has("Ramparts of Perdition (E4M7) - Blue key", player, 1))
    set_rule(multiworld.get_entrance("Ramparts of Perdition (E4M7) Green -> Ramparts of Perdition (E4M7) Yellow", player), lambda state:
        state.has("Ramparts of Perdition (E4M7) - Green key", player, 1))

    # Shattered Bridge (E4M8)
    set_rule(multiworld.get_entrance("Hub -> Shattered Bridge (E4M8) Main", player), lambda state:
        state.has("Shattered Bridge (E4M8)", player, 1) and
        state.has("Gauntlets of the Necromancer", player, 1) and
        state.has("Ethereal Crossbow", player, 1) and
        state.has("Dragon Claw", player, 1) and
        state.has("Phoenix Rod", player, 1) and
        state.has("Firemace", player, 1) and
        state.has("Hellstaff", player, 1))
    set_rule(multiworld.get_entrance("Shattered Bridge (E4M8) Main -> Shattered Bridge (E4M8) Yellow", player), lambda state:
        state.has("Shattered Bridge (E4M8) - Yellow key", player, 1))
    set_rule(multiworld.get_entrance("Shattered Bridge (E4M8) Yellow -> Shattered Bridge (E4M8) Main", player), lambda state:
        state.has("Shattered Bridge (E4M8) - Yellow key", player, 1))

    # Mausoleum (E4M9)
    set_rule(multiworld.get_entrance("Hub -> Mausoleum (E4M9) Main", player), lambda state:
       (state.has("Mausoleum (E4M9)", player, 1) and
        state.has("Gauntlets of the Necromancer", player, 1) and
        state.has("Ethereal Crossbow", player, 1) and
        state.has("Dragon Claw", player, 1) and
        state.has("Firemace", player, 1)) and
       (state.has("Phoenix Rod", player, 1) or
        state.has("Hellstaff", player, 1)))
    set_rule(multiworld.get_entrance("Mausoleum (E4M9) Main -> Mausoleum (E4M9) Yellow", player), lambda state:
        state.has("Mausoleum (E4M9) - Yellow key", player, 1))
    set_rule(multiworld.get_entrance("Mausoleum (E4M9) Yellow -> Mausoleum (E4M9) Main", player), lambda state:
        state.has("Mausoleum (E4M9) - Yellow key", player, 1))


def set_episode5_rules(player, multiworld, pro):
    # Ochre Cliffs (E5M1)
    set_rule(multiworld.get_entrance("Hub -> Ochre Cliffs (E5M1) Main", player), lambda state:
        state.has("Ochre Cliffs (E5M1)", player, 1))
    set_rule(multiworld.get_entrance("Ochre Cliffs (E5M1) Main -> Ochre Cliffs (E5M1) Yellow", player), lambda state:
        state.has("Ochre Cliffs (E5M1) - Yellow key", player, 1))
    set_rule(multiworld.get_entrance("Ochre Cliffs (E5M1) Blue -> Ochre Cliffs (E5M1) Yellow", player), lambda state:
        state.has("Ochre Cliffs (E5M1) - Blue key", player, 1))
    set_rule(multiworld.get_entrance("Ochre Cliffs (E5M1) Yellow -> Ochre Cliffs (E5M1) Main", player), lambda state:
        state.has("Ochre Cliffs (E5M1) - Yellow key", player, 1))
    set_rule(multiworld.get_entrance("Ochre Cliffs (E5M1) Yellow -> Ochre Cliffs (E5M1) Green", player), lambda state:
        state.has("Ochre Cliffs (E5M1) - Green key", player, 1))
    set_rule(multiworld.get_entrance("Ochre Cliffs (E5M1) Yellow -> Ochre Cliffs (E5M1) Blue", player), lambda state:
        state.has("Ochre Cliffs (E5M1) - Blue key", player, 1))
    set_rule(multiworld.get_entrance("Ochre Cliffs (E5M1) Green -> Ochre Cliffs (E5M1) Yellow", player), lambda state:
        state.has("Ochre Cliffs (E5M1) - Green key", player, 1))

    # Rapids (E5M2)
    set_rule(multiworld.get_entrance("Hub -> Rapids (E5M2) Main", player), lambda state:
        state.has("Rapids (E5M2)", player, 1) and
        state.has("Ethereal Crossbow", player, 1) and
        state.has("Dragon Claw", player, 1))
    set_rule(multiworld.get_entrance("Rapids (E5M2) Main -> Rapids (E5M2) Yellow", player), lambda state:
        state.has("Rapids (E5M2) - Yellow key", player, 1))
    set_rule(multiworld.get_entrance("Rapids (E5M2) Yellow -> Rapids (E5M2) Main", player), lambda state:
        state.has("Rapids (E5M2) - Yellow key", player, 1))
    set_rule(multiworld.get_entrance("Rapids (E5M2) Yellow -> Rapids (E5M2) Green", player), lambda state:
        state.has("Rapids (E5M2) - Green key", player, 1))

    # Quay (E5M3)
    set_rule(multiworld.get_entrance("Hub -> Quay (E5M3) Main", player), lambda state:
       (state.has("Quay (E5M3)", player, 1) and
        state.has("Ethereal Crossbow", player, 1) and
        state.has("Dragon Claw", player, 1)) and
       (state.has("Phoenix Rod", player, 1) or
        state.has("Hellstaff", player, 1) or
        state.has("Firemace", player, 1)))
    set_rule(multiworld.get_entrance("Quay (E5M3) Main -> Quay (E5M3) Yellow", player), lambda state:
        state.has("Quay (E5M3) - Yellow key", player, 1))
    set_rule(multiworld.get_entrance("Quay (E5M3) Main -> Quay (E5M3) Green", player), lambda state:
        state.has("Quay (E5M3) - Green key", player, 1))
    set_rule(multiworld.get_entrance("Quay (E5M3) Main -> Quay (E5M3) Blue", player), lambda state:
        state.has("Quay (E5M3) - Blue key", player, 1))
    set_rule(multiworld.get_entrance("Quay (E5M3) Yellow -> Quay (E5M3) Main", player), lambda state:
        state.has("Quay (E5M3) - Yellow key", player, 1))
    set_rule(multiworld.get_entrance("Quay (E5M3) Green -> Quay (E5M3) Main", player), lambda state:
        state.has("Quay (E5M3) - Green key", player, 1))
    set_rule(multiworld.get_entrance("Quay (E5M3) Green -> Quay (E5M3) Cyan", player), lambda state:
        state.has("Quay (E5M3) - Blue key", player, 1))

    # Courtyard (E5M4)
    set_rule(multiworld.get_entrance("Hub -> Courtyard (E5M4) Main", player), lambda state:
       (state.has("Courtyard (E5M4)", player, 1) and
        state.has("Ethereal Crossbow", player, 1) and
        state.has("Dragon Claw", player, 1)) and
       (state.has("Phoenix Rod", player, 1) or
        state.has("Firemace", player, 1) or
        state.has("Hellstaff", player, 1)))
    set_rule(multiworld.get_entrance("Courtyard (E5M4) Main -> Courtyard (E5M4) Kakis", player), lambda state:
        state.has("Courtyard (E5M4) - Yellow key", player, 1) or
        state.has("Courtyard (E5M4) - Green key", player, 1))
    set_rule(multiworld.get_entrance("Courtyard (E5M4) Main -> Courtyard (E5M4) Blue", player), lambda state:
        state.has("Courtyard (E5M4) - Blue key", player, 1))
    set_rule(multiworld.get_entrance("Courtyard (E5M4) Blue -> Courtyard (E5M4) Main", player), lambda state:
        state.has("Courtyard (E5M4) - Blue key", player, 1))
    set_rule(multiworld.get_entrance("Courtyard (E5M4) Kakis -> Courtyard (E5M4) Main", player), lambda state:
        state.has("Courtyard (E5M4) - Yellow key", player, 1) or
        state.has("Courtyard (E5M4) - Green key", player, 1))

    # Hydratyr (E5M5)
    set_rule(multiworld.get_entrance("Hub -> Hydratyr (E5M5) Main", player), lambda state:
       (state.has("Hydratyr (E5M5)", player, 1) and
        state.has("Ethereal Crossbow", player, 1) and
        state.has("Dragon Claw", player, 1) and
        state.has("Firemace", player, 1)) and
       (state.has("Phoenix Rod", player, 1) or
        state.has("Hellstaff", player, 1)))
    set_rule(multiworld.get_entrance("Hydratyr (E5M5) Main -> Hydratyr (E5M5) Yellow", player), lambda state:
        state.has("Hydratyr (E5M5) - Yellow key", player, 1))
    set_rule(multiworld.get_entrance("Hydratyr (E5M5) Blue -> Hydratyr (E5M5) Green", player), lambda state:
        state.has("Hydratyr (E5M5) - Blue key", player, 1))
    set_rule(multiworld.get_entrance("Hydratyr (E5M5) Yellow -> Hydratyr (E5M5) Green", player), lambda state:
        state.has("Hydratyr (E5M5) - Green key", player, 1))
    set_rule(multiworld.get_entrance("Hydratyr (E5M5) Green -> Hydratyr (E5M5) Blue", player), lambda state:
        state.has("Hydratyr (E5M5) - Blue key", player, 1))

    # Colonnade (E5M6)
    set_rule(multiworld.get_entrance("Hub -> Colonnade (E5M6) Main", player), lambda state:
       (state.has("Colonnade (E5M6)", player, 1) and
        state.has("Ethereal Crossbow", player, 1) and
        state.has("Dragon Claw", player, 1) and
        state.has("Firemace", player, 1) and
        state.has("Gauntlets of the Necromancer", player, 1)) and
       (state.has("Phoenix Rod", player, 1) or
        state.has("Hellstaff", player, 1)))
    set_rule(multiworld.get_entrance("Colonnade (E5M6) Main -> Colonnade (E5M6) Yellow", player), lambda state:
        state.has("Colonnade (E5M6) - Yellow key", player, 1))
    set_rule(multiworld.get_entrance("Colonnade (E5M6) Main -> Colonnade (E5M6) Blue", player), lambda state:
        state.has("Colonnade (E5M6) - Blue key", player, 1))
    set_rule(multiworld.get_entrance("Colonnade (E5M6) Blue -> Colonnade (E5M6) Main", player), lambda state:
        state.has("Colonnade (E5M6) - Blue key", player, 1))
    set_rule(multiworld.get_entrance("Colonnade (E5M6) Yellow -> Colonnade (E5M6) Green", player), lambda state:
        state.has("Colonnade (E5M6) - Green key", player, 1))
    set_rule(multiworld.get_entrance("Colonnade (E5M6) Green -> Colonnade (E5M6) Yellow", player), lambda state:
        state.has("Colonnade (E5M6) - Green key", player, 1))

    # Foetid Manse (E5M7)
    set_rule(multiworld.get_entrance("Hub -> Foetid Manse (E5M7) Main", player), lambda state:
       (state.has("Foetid Manse (E5M7)", player, 1) and
        state.has("Ethereal Crossbow", player, 1) and
        state.has("Dragon Claw", player, 1) and
        state.has("Firemace", player, 1) and
        state.has("Gauntlets of the Necromancer", player, 1)) and
       (state.has("Phoenix Rod", player, 1) or
        state.has("Hellstaff", player, 1)))
    set_rule(multiworld.get_entrance("Foetid Manse (E5M7) Main -> Foetid Manse (E5M7) Yellow", player), lambda state:
        state.has("Foetid Manse (E5M7) - Yellow key", player, 1))
    set_rule(multiworld.get_entrance("Foetid Manse (E5M7) Yellow -> Foetid Manse (E5M7) Green", player), lambda state:
        state.has("Foetid Manse (E5M7) - Green key", player, 1))
    set_rule(multiworld.get_entrance("Foetid Manse (E5M7) Yellow -> Foetid Manse (E5M7) Blue", player), lambda state:
        state.has("Foetid Manse (E5M7) - Blue key", player, 1))

    # Field of Judgement (E5M8)
    set_rule(multiworld.get_entrance("Hub -> Field of Judgement (E5M8) Main", player), lambda state:
        state.has("Field of Judgement (E5M8)", player, 1) and
        state.has("Ethereal Crossbow", player, 1) and
        state.has("Dragon Claw", player, 1) and
        state.has("Phoenix Rod", player, 1) and
        state.has("Firemace", player, 1) and
        state.has("Hellstaff", player, 1) and
        state.has("Gauntlets of the Necromancer", player, 1) and
        state.has("Bag of Holding", player, 1))

    # Skein of D'Sparil (E5M9)
    set_rule(multiworld.get_entrance("Hub -> Skein of D'Sparil (E5M9) Main", player), lambda state:
        state.has("Skein of D'Sparil (E5M9)", player, 1) and
        state.has("Bag of Holding", player, 1) and
        state.has("Hellstaff", player, 1) and
        state.has("Phoenix Rod", player, 1) and
        state.has("Dragon Claw", player, 1) and
        state.has("Ethereal Crossbow", player, 1) and
        state.has("Gauntlets of the Necromancer", player, 1) and
        state.has("Firemace", player, 1))
    set_rule(multiworld.get_entrance("Skein of D'Sparil (E5M9) Main -> Skein of D'Sparil (E5M9) Blue", player), lambda state:
        state.has("Skein of D'Sparil (E5M9) - Blue key", player, 1))
    set_rule(multiworld.get_entrance("Skein of D'Sparil (E5M9) Main -> Skein of D'Sparil (E5M9) Yellow", player), lambda state:
        state.has("Skein of D'Sparil (E5M9) - Yellow key", player, 1))
    set_rule(multiworld.get_entrance("Skein of D'Sparil (E5M9) Main -> Skein of D'Sparil (E5M9) Green", player), lambda state:
        state.has("Skein of D'Sparil (E5M9) - Green key", player, 1))
    set_rule(multiworld.get_entrance("Skein of D'Sparil (E5M9) Yellow -> Skein of D'Sparil (E5M9) Main", player), lambda state:
        state.has("Skein of D'Sparil (E5M9) - Yellow key", player, 1))
    set_rule(multiworld.get_entrance("Skein of D'Sparil (E5M9) Green -> Skein of D'Sparil (E5M9) Main", player), lambda state:
        state.has("Skein of D'Sparil (E5M9) - Green key", player, 1))


def set_rules(heretic_world: "HereticWorld", included_episodes, pro):
    player = heretic_world.player
    multiworld = heretic_world.multiworld

    if included_episodes[0]:
        set_episode1_rules(player, multiworld, pro)
    if included_episodes[1]:
        set_episode2_rules(player, multiworld, pro)
    if included_episodes[2]:
        set_episode3_rules(player, multiworld, pro)
    if included_episodes[3]:
        set_episode4_rules(player, multiworld, pro)
    if included_episodes[4]:
        set_episode5_rules(player, multiworld, pro)
