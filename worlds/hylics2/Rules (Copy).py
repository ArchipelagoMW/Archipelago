from typing import TYPE_CHECKING

from ..generic.Rules import set_rule

if TYPE_CHECKING:
    from . import Hylics2World

def _hylics2_has_pneumatophore(self, player: int):
    return self.has('PNEUMATOPHORE', player)

def _hylics2_has_airship(self, player: int):
    return self.has('DOCK KEY', player)

def _hylics2_has_jail_key(self, player: int):
    return self.has('JAIL KEY', player)

def _hylics2_has_paddle(self, player: int):
    return self.has('PADDLE', player)

def _hylics2_has_worm_room_key(self, player: int):
    return self.has('WORM ROOM KEY', player)

def _hylics2_has_bridge_key(self, player: int):
    return self.has('BRIDGE KEY', player)

def _hylics2_has_upper_chamber_key(self, player: int):
    return self.has('UPPER CHAMBER KEY', player)

def _hylics2_has_vessel_room_key(self, player: int):
    return self.has('VESSEL ROOM KEY', player)

# not required but unlocks more locations
def _hylics2_has_house_key(self, player: int):
    return self.has('HOUSE KEY', player)

def _hylics2_has_cave_key(self, player: int):
    return self.has('CAVE KEY', player)

def _hylics2_has_skull_bomb(self, player: int):
    return self.has('SKULL BOMB', player)

def _hylics2_has_tower_key(self, player: int):
    return self.has('TOWER KEY', player)

def _hylics2_has_deep_key(self, player: int):
    return self.has('DEEP KEY', player)

def _hylics2_has_upper_house_key(self, player: int):
    return self.has('UPPER HOUSE KEY', player)

def _hylics2_has_clicker(self, player: int):
    return self.has('CLICKER', player)

def _hylics2_has_tokens(self, player: int):
    return self.has('SAGE TOKEN', player, 3)

def set_location_rules(hylics2_world: "Hylics2World"):
    player = hylics2_world.player
    world = hylics2_world.world

    # Exits
    for i in world.get_region("Afterlife", player).exits:
        if i.name is "To Viewax":
            set_rule(i, lambda state: _hylics2_has_pneumatophore(state, player))
        elif i.name is "To TV Island" or "To Shield Facility":
            set_rule(i, lambda state: _hylics2_has_airship(state, player))
        elif i.name is "To Worm Pod":
            set_rule(i, lambda state: _hylics2_has_worm_room_key(state, player))
        elif i.name is "To Foglast":
            set_rule(i, lambda state: _hylics2_has_airship(state, player) and _hylics2_has_worm_room_key(state, player))
        elif i.name is "To Sage Labyrinth":
            set_rule(i, lambda state: _hylics2_has_airship(state, player) and _hylics2_has_skull_bomb(state, player) and _hylics2_has_bridge_key(state, player))
        elif i.name is "To Hylemxylem":
            set_rule(i, lambda state: _hylics2_has_airship(state, player) and _hylics2_has_worm_room_key(player) and _hylics2_has_bridge_key(state, player))

    for i in world.get_region("World", player).exits:
        if i.name is "To Viewax":
            set_rule(i, lambda state: _hylics2_has_pneumatophore(state, player))
        elif i.name is "To TV Island" or "To Shield Facility" or "To Airship" or "To Arcade Island" or "To Juice Ranch":
            set_rule(i, lambda state: _hylics2_has_airship(state, player))
        elif i.name is "To Worm Pod":
            set_rule(i, lambda state: _hylics2_has_worm_room_key(state, player))
        elif i.name is "To Foglast":
            set_rule(i, lambda state: _hylics2_has_airship(state, player) and _hylics2_has_worm_room_key(state, player))
        elif i.name is "To Sage Labyrinth":
            set_rule(i, lambda state: _hylics2_has_airship(state, player) and _hylics2_has_skull_bomb(state, player) and _hylics2_has_bridge_key(state, player))
        elif i.name is "To Sage Airship":
            set_rule(i, lambda state: _hylics2_has_airship(state, player) and _hylics2_has_skull_bomb(state, player) and _hylics2_has_deep_key(state, player))
        elif i.name is "To Hylemxylem":
            set_rule(i, lambda state: _hylics2_has_airship(state, player) and _hylics2_has_worm_room_key(player) and _hylics2_has_bridge_key(state, player))

    for i in world.get_region("Shield Facility", player).exits:
        if i.name is "To Worm Pod":
            set_rule(i, lambda state: _hylics2_has_worm_room_key(state, player))

    for i in world.get_region("Drill Castle", player).exits:
        if i.name is "To Sage Labyrinth":
            set_rule(i, lambda state: _hylics2_has_airship(state, player) and _hylics2_has_skull_bomb(state, player) and _hylics2_has_bridge_key(state, player))


    # New Muldul
    set_rule(world.get_location("New Muldul: Underground Chest", player), lambda state: _hylics2_has_pneumatophore(state, player))
    set_rule(world.get_location("New Muldul: Upper House Chest 1", player), lambda state: _hylics2_has_upper_house_key(state, player))
    set_rule(world.get_location("New Muldul: Upper House Chest 2", player), lambda state: _hylics2_has_upper_house_key(state, player))
    set_rule(world.get_location("New Muldul: TV", player), lambda state: _hylics2_has_house_key(state, player))
    set_rule(world.get_location("New Muldul: Rescued Blerol", player), lambda state: _hylics2_has_jail_key(state, player))
    set_rule(world.get_location("New Muldul: Rescued Blerol 2", player), lambda state: _hylics2_has_jail_key(state, player))
    set_rule(world.get_location("New Muldul: Vault Left Chest", player), lambda state: _hylics2_has_worm_room_key(state, player))
    set_rule(world.get_location("New Muldul: Vault Right Chest", player), lambda state: _hylics2_has_worm_room_key(state, player))
    set_rule(world.get_location("New Muldul: Vault Bomb", player), lambda state: _hylics2_has_worm_room_key(state, player))

    # Viewax's Edifice
    set_rule(world.get_location("Viewax's Edifice: Canopic Jar", player), lambda state: _hylics2_has_paddle(state, player))
    set_rule(world.get_location("Viewax's Edifice: Cave Sarcophagus", player), lambda state: _hylics2_has_paddle(state, player))
    set_rule(world.get_location("Viewax's Edifice: Shielded Key", player), lambda state: _hylics2_has_paddle(state, player))
    set_rule(world.get_location("Viewax's Edifice: Tower Pot", player), lambda state: _hylics2_has_paddle(state, player))
    set_rule(world.get_location("Viewax's Edifice: Tower Jar", player), lambda state: _hylics2_has_paddle(state, player))
    set_rule(world.get_location("Viewax's Edifice: Tower Chest", player), lambda state: _hylics2_has_tower_key(state, player) and _hylics2_has_paddle(state, player))
    set_rule(world.get_location("Viewax's Edifice: Viewax Pot", player), lambda state: _hylics2_has_paddle(state, player))
    set_rule(world.get_location("Viewax's Edifice: Defeat Viewax", player), lambda state: _hylics2_has_paddle(state, player))
    set_rule(world.get_location("Viewax's Edifice: TV", player), lambda state: _hylics2_has_paddle(state, player) and _hylics2_has_jail_key(state, player))

    # Arcade 1
    set_rule(world.get_location("Arcade 1: Key", player), lambda state: _hylics2_has_paddle(state, player))
    set_rule(world.get_location("Arcade 1: Coin Dash", player), lambda state: _hylics2_has_paddle(state, player))
    set_rule(world.get_location("Arcade 1: Burrito Alcove 1", player), lambda state: _hylics2_has_paddle(state, player))
    set_rule(world.get_location("Arcade 1: Burrito Alcove 2", player), lambda state: _hylics2_has_paddle(state, player))
    set_rule(world.get_location("Arcade 1: Behind Spikes Banana", player), lambda state: _hylics2_has_paddle(state, player))
    set_rule(world.get_location("Arcade 1: Pyramid Banana", player), lambda state: _hylics2_has_paddle(state, player))
    set_rule(world.get_location("Arcade 1: Moving Platforms Muscle Applique", player), lambda state: _hylics2_has_paddle(state, player))
    set_rule(world.get_location("Arcade 1: Bed Banana", player), lambda state: _hylics2_has_paddle(state, player))

    # Airship
    set_rule(world.get_location("Airship: Talk to Somsnosa", player), lambda state: _hylics2_has_worm_room_key(state, player))

    # Foglast
    set_rule(world.get_location("Foglast: TV", player), lambda state: _hylics2_has_clicker(state, player))
    set_rule(world.get_location("Foglast: Roof Sarcophagus", player), lambda state: _hylics2_has_bridge_key(state, player))
    set_rule(world.get_location("Foglast: Under Lair Sarcophagus 1", player), lambda state: _hylics2_has_bridge_key(state, player))
    set_rule(world.get_location("Foglast: Under Lair Sarcophagus 2", player), lambda state: _hylics2_has_bridge_key(state, player))
    set_rule(world.get_location("Foglast: Under Lair Sarcophagus 3", player), lambda state: _hylics2_has_bridge_key(state, player))
    set_rule(world.get_location("Foglast: Sage Sarcophagus", player), lambda state: _hylics2_has_bridge_key(state, player))
    set_rule(world.get_location("Foglast: Sage Item 1", player), lambda state: _hylics2_has_bridge_key(state, player))
    set_rule(world.get_location("Foglast: Sage Item 2", player), lambda state: _hylics2_has_bridge_key(state, player))

    # Drill Castle
    set_rule(world.get_location("Drill Castle: Island Banana", player), lambda state: _hylics2_has_pneumatophore(state, player))
    set_rule(world.get_location("Drill Castle: Island Pot", player), lambda state: _hylics2_has_pneumatophore(state, player))
    set_rule(world.get_location("Drill Castle: Cave Sarcophagus", player), lambda state: _hylics2_has_pneumatophore(state, player))
    set_rule(world.get_location("Drill Castle: Roof Banana", player), lambda state: _hylics2_has_pneumatophore(state, player))
    set_rule(world.get_location("Drill Castle: TV", player), lambda state: _hylics2_has_pneumatophore(state, player))

    # Sage Labyrinth
    set_rule(world.get_location("Sage Labyrinth: Sage Item 1", player), lambda state: _hylics2_has_worm_room_key(state, player))
    set_rule(world.get_location("Sage Labyrinth: Sage Item 2", player), lambda state: _hylics2_has_worm_room_key(state, player))
    set_rule(world.get_location("Sage Labyrinth: Sage Left Arm", player), lambda state: _hylics2_has_worm_room_key(state, player))
    set_rule(world.get_location("Sage Labyrinth: Sage Right Arm", player), lambda state: _hylics2_has_worm_room_key(state, player))
    set_rule(world.get_location("Sage Labyrinth: Sage Left Leg", player), lambda state: _hylics2_has_worm_room_key(state, player))
    set_rule(world.get_location("Sage Labyrinth: Sage Right Leg", player), lambda state: _hylics2_has_worm_room_key(state, player))

    # Sage Airship
    set_rule(world.get_location("Sage Airship: TV", player), lambda state: _hylics2_has_tokens(state, player))

    # Hylemxylem
    set_rule(world.get_location("Hylemxylem: Upper Chamber Banana", player), lambda state: _hylics2_has_upper_chamber_key(state, player))