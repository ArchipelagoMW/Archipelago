from worlds.generic.Rules import set_rule, add_rule
from ..AutoWorld import LogicMixin


class Hylics2Logic(LogicMixin):

    def _hylics2_can_air_dash(self, player):
        return self.has("PNEUMATOPHORE", player)

    def _hylics2_has_airship(self, player):
        return self.has("DOCK KEY", player)

    def _hylics2_has_jail_key(self, player):
        return self.has("JAIL KEY", player)

    def _hylics2_has_paddle(self, player):
        return self.has("PADDLE", player)

    def _hylics2_has_worm_room_key(self, player):
        return self.has("WORM ROOM KEY", player)

    def _hylics2_has_bridge_key(self, player):
        return self.has("BRIDGE KEY", player)

    def _hylics2_has_upper_chamber_key(self, player):
        return self.has("UPPER CHAMBER KEY", player)

    def _hylics2_has_vessel_room_key(self, player):
        return self.has("VESSEL ROOM KEY", player)
    
    def _hylics2_has_house_key(self, player):
        return self.has("HOUSE KEY", player)

    def _hylics2_has_cave_key(self, player):
        return self.has("CAVE KEY", player)

    def _hylics2_has_skull_bomb(self, player):
        return self.has("SKULL BOMB", player)

    def _hylics2_has_tower_key(self, player):
        return self.has("TOWER KEY", player)

    def _hylics2_has_deep_key(self, player):
        return self.has("DEEP KEY", player)

    def _hylics2_has_upper_house_key(self, player):
        return self.has("UPPER HOUSE KEY", player)

    def _hylics2_has_clicker(self, player):
        return self.has("CLICKER", player)

    def _hylics2_has_tokens(self, player):
        return self.has("SAGE TOKEN", player, 3)

    def _hylics2_has_charge_up(self, player):
        return self.has("CHARGE UP", player)

    def _hylics2_has_cup(self, player):
        return self.has("PAPER CUP", player, 1)

    def _hylics2_has_1_member(self, player):
        return self.has("Pongorma", player) or self.has("Dedusmuln", player) or self.has("Somsnosa", player)

    def _hylics2_has_2_members(self, player):
        return (self.has("Pongorma", player) and self.has("Dedusmuln", player)) or\
            (self.has("Pongorma", player) and self.has("Somsnosa", player)) or\
                (self.has("Dedusmuln", player) and self.has("Somsnosa", player))

    def _hylics2_has_3_members(self, player):
        return self.has("Pongorma", player) and self.has("Dedusmuln", player) and self.has("Somsnosa", player)

    def _hylics2_enter_arcade2(self, player):
        return self._hylics2_can_air_dash(player) and self._hylics2_has_airship(player)

    def _hylics2_enter_wormpod(self, player):
        return self._hylics2_has_airship(player) and self._hylics2_has_worm_room_key(player)

    def _hylics2_enter_sageship(self, player):
        return self._hylics2_has_skull_bomb(player) and self._hylics2_has_airship(player)

    def _hylics2_enter_foglast(self, player):
        return self._hylics2_enter_wormpod(player)

    def _hylics2_enter_hylemxylem(self, player):
        return self._hylics2_can_air_dash(player) and self._hylics2_has_paddle(player) and\
            self._hylics2_enter_wormpod(player) and self._hylics2_has_bridge_key(player)


def set_rules(hylics2world):
    world = hylics2world.world
    player = hylics2world.player

    # entrances
    for i in world.get_region("Viewax", player).entrances:
        set_rule(i, lambda state: state._hylics2_can_air_dash(player) or state._hylics2_has_airship(player))
    for i in world.get_region("TV Island", player).entrances:
        set_rule(i, lambda state: state._hylics2_has_airship(player))
    for i in world.get_region("Shield Facility", player).entrances:
        set_rule(i, lambda state: state._hylics2_has_airship(player))
    for i in world.get_region("Airship", player).entrances:
        set_rule(i, lambda state: state._hylics2_has_airship(player))
    for i in world.get_region("Juice Ranch", player).entrances:
        set_rule(i, lambda state: state._hylics2_has_airship(player))
    for i in world.get_region("Arcade Island", player).entrances:
        set_rule(i, lambda state: state._hylics2_has_airship(player) and state._hylics2_can_air_dash(player))
    for i in world.get_region("Worm Pod", player).entrances:
        set_rule(i, lambda state: state._hylics2_enter_wormpod(player))
    for i in world.get_region("Foglast", player).entrances:
        set_rule(i, lambda state: state._hylics2_enter_foglast(player))
    for i in world.get_region("Sage Labyrinth", player).entrances:
        set_rule(i, lambda state: state._hylics2_has_skull_bomb(player))
    for i in world.get_region("Sage Airship", player).entrances:
        set_rule(i, lambda state: state._hylics2_enter_sageship(player))
    for i in world.get_region("Hylemxylem", player).entrances:
        set_rule(i, lambda state: state._hylics2_enter_hylemxylem(player))

    # Afterlife
    set_rule(world.get_location("Afterlife: TV", player), 
        lambda state: state._hylics2_has_cave_key(player))

    # New Muldul
    set_rule(world.get_location("New Muldul: Underground Chest", player), 
        lambda state: state._hylics2_can_air_dash(player))
    set_rule(world.get_location("New Muldul: Upper House Chest 1", player), 
        lambda state: state._hylics2_has_upper_house_key(player))
    set_rule(world.get_location("New Muldul: Upper House Chest 2", player), 
        lambda state: state._hylics2_has_upper_house_key(player))

    # New Muldul Vault
    set_rule(world.get_location("New Muldul: Rescued Blerol 1", player), 
        lambda state: state._hylics2_has_jail_key(player))
    set_rule(world.get_location("New Muldul: Rescued Blerol 2", player), 
        lambda state: state._hylics2_has_jail_key(player))
    set_rule(world.get_location("New Muldul: Vault Left Chest", player), 
        lambda state: state._hylics2_enter_foglast(player) and state._hylics2_has_bridge_key(player))
    set_rule(world.get_location("New Muldul: Vault Right Chest", player), 
        lambda state: state._hylics2_enter_foglast(player) and state._hylics2_has_bridge_key(player))
    set_rule(world.get_location("New Muldul: Vault Bomb", player), 
        lambda state: state._hylics2_enter_foglast(player) and state._hylics2_has_bridge_key(player))

    # Viewax's Edifice
    set_rule(world.get_location("Viewax's Edifice: Canopic Jar", player), 
        lambda state: state._hylics2_has_paddle(player))
    set_rule(world.get_location("Viewax's Edifice: Cave Sarcophagus", player), 
        lambda state: state._hylics2_has_paddle(player))
    set_rule(world.get_location("Viewax's Edifice: Shielded Key", player), 
        lambda state: state._hylics2_has_paddle(player))
    set_rule(world.get_location("Viewax's Edifice: Shielded Key", player), 
        lambda state: state._hylics2_has_paddle(player))
    set_rule(world.get_location("Viewax's Edifice: Tower Pot", player), 
        lambda state: state._hylics2_has_paddle(player))
    set_rule(world.get_location("Viewax's Edifice: Tower Jar", player), 
        lambda state: state._hylics2_has_paddle(player))
    set_rule(world.get_location("Viewax's Edifice: Tower Chest", player), 
        lambda state: state._hylics2_has_paddle(player) and state._hylics2_has_tower_key(player))
    set_rule(world.get_location("Viewax's Edifice: Viewax Pot", player), 
        lambda state: state._hylics2_has_paddle(player))
    set_rule(world.get_location("Viewax's Edifice: Defeat Viewax", player), 
        lambda state: state._hylics2_has_paddle(player))
    set_rule(world.get_location("Viewax's Edifice: TV", player), 
        lambda state: state._hylics2_has_paddle(player) and state._hylics2_has_jail_key(player))
    set_rule(world.get_location("Viewax's Edifice: Sage Fridge", player), 
        lambda state: state._hylics2_can_air_dash(player))
    set_rule(world.get_location("Viewax's Edifice: Sage Item 1", player), 
        lambda state: state._hylics2_can_air_dash(player))
    set_rule(world.get_location("Viewax's Edifice: Sage Item 2", player), 
        lambda state: state._hylics2_can_air_dash(player))

    # Arcade 1
    set_rule(world.get_location("Arcade 1: Key", player), 
        lambda state: state._hylics2_has_paddle(player))
    set_rule(world.get_location("Arcade 1: Coin Dash", player), 
        lambda state: state._hylics2_has_paddle(player))
    set_rule(world.get_location("Arcade 1: Burrito Alcove 1", player), 
        lambda state: state._hylics2_has_paddle(player))
    set_rule(world.get_location("Arcade 1: Burrito Alcove 2", player), 
        lambda state: state._hylics2_has_paddle(player))
    set_rule(world.get_location("Arcade 1: Behind Spikes Banana", player), 
        lambda state: state._hylics2_has_paddle(player))
    set_rule(world.get_location("Arcade 1: Pyramid Banana", player), 
        lambda state: state._hylics2_has_paddle(player))
    set_rule(world.get_location("Arcade 1: Moving Platforms Muscle Applique", player), 
        lambda state: state._hylics2_has_paddle(player))
    set_rule(world.get_location("Arcade 1: Bed Banana", player), 
        lambda state: state._hylics2_has_paddle(player))

    # Airship
    set_rule(world.get_location("Airship: Talk to Somsnosa", player), 
        lambda state: state._hylics2_has_worm_room_key(player))

    # Foglast
    set_rule(world.get_location("Foglast: Underground Sarcophagus", player), 
        lambda state: state._hylics2_can_air_dash(player))
    set_rule(world.get_location("Foglast: Shielded Key", player), 
        lambda state: state._hylics2_can_air_dash(player))
    set_rule(world.get_location("Foglast: TV", player), 
        lambda state: state._hylics2_can_air_dash(player) and state._hylics2_has_clicker(player))
    set_rule(world.get_location("Foglast: Buy Clicker", player), 
        lambda state: state._hylics2_can_air_dash(player))
    set_rule(world.get_location("Foglast: Shielded Chest", player), 
        lambda state: state._hylics2_can_air_dash(player))
    set_rule(world.get_location("Foglast: Cave Fridge", player), 
        lambda state: state._hylics2_can_air_dash(player))
    set_rule(world.get_location("Foglast: Roof Sarcophagus", player), 
        lambda state: state._hylics2_can_air_dash(player) and state._hylics2_has_bridge_key(player))
    set_rule(world.get_location("Foglast: Under Lair Sarcophagus 1", player), 
        lambda state: state._hylics2_can_air_dash(player) and state._hylics2_has_bridge_key(player))
    set_rule(world.get_location("Foglast: Under Lair Sarcophagus 2", player), 
        lambda state: state._hylics2_can_air_dash(player) and state._hylics2_has_bridge_key(player))
    set_rule(world.get_location("Foglast: Under Lair Sarcophagus 3", player), 
        lambda state: state._hylics2_can_air_dash(player) and state._hylics2_has_bridge_key(player))
    set_rule(world.get_location("Foglast: Sage Sarcophagus", player), 
        lambda state: state._hylics2_can_air_dash(player) and state._hylics2_has_bridge_key(player))
    set_rule(world.get_location("Foglast: Sage Item 1", player), 
        lambda state: state._hylics2_can_air_dash(player) and state._hylics2_has_bridge_key(player))
    set_rule(world.get_location("Foglast: Sage Item 2", player), 
        lambda state: state._hylics2_can_air_dash(player) and state._hylics2_has_bridge_key(player))

    # Drill Castle
    set_rule(world.get_location("Drill Castle: Island Banana", player), 
        lambda state: state._hylics2_can_air_dash(player))
    set_rule(world.get_location("Drill Castle: Island Pot", player), 
        lambda state: state._hylics2_can_air_dash(player))
    set_rule(world.get_location("Drill Castle: Cave Sarcophagus", player), 
        lambda state: state._hylics2_can_air_dash(player))
    set_rule(world.get_location("Drill Castle: TV", player), 
        lambda state: state._hylics2_can_air_dash(player))

    # Sage Labyrinth
    set_rule(world.get_location("Sage Labyrinth: Sage Item 1", player), 
        lambda state: state._hylics2_has_deep_key(player))
    set_rule(world.get_location("Sage Labyrinth: Sage Item 2", player), 
        lambda state: state._hylics2_has_deep_key(player))
    set_rule(world.get_location("Sage Labyrinth: Sage Left Arm", player), 
        lambda state: state._hylics2_has_deep_key(player))
    set_rule(world.get_location("Sage Labyrinth: Sage Right Arm", player), 
        lambda state: state._hylics2_has_deep_key(player))
    set_rule(world.get_location("Sage Labyrinth: Sage Left Leg", player), 
        lambda state: state._hylics2_has_deep_key(player))
    set_rule(world.get_location("Sage Labyrinth: Sage Right Leg", player), 
        lambda state: state._hylics2_has_deep_key(player))

    # Sage Airship
    set_rule(world.get_location("Sage Airship: TV", player), 
        lambda state: state._hylics2_has_tokens(player))

    # Hylemxylem
    set_rule(world.get_location("Hylemxylem: Upper Chamber Banana", player), 
        lambda state: state._hylics2_has_upper_chamber_key(player))
    set_rule(world.get_location("Hylemxylem: Across Upper Reservoir Chest", player), 
        lambda state: state._hylics2_has_upper_chamber_key(player))
    set_rule(world.get_location("Hylemxylem: Drained Lower Reservoir Chest", player), 
        lambda state: state._hylics2_has_upper_chamber_key(player))
    set_rule(world.get_location("Hylemxylem: Drained Lower Reservoir Burrito 1", player), 
        lambda state: state._hylics2_has_upper_chamber_key(player))
    set_rule(world.get_location("Hylemxylem: Drained Lower Reservoir Burrito 2", player), 
        lambda state: state._hylics2_has_upper_chamber_key(player))
    set_rule(world.get_location("Hylemxylem: Lower Reservoir Hole Pot 1", player), 
        lambda state: state._hylics2_has_upper_chamber_key(player))
    set_rule(world.get_location("Hylemxylem: Lower Reservoir Hole Pot 2", player), 
        lambda state: state._hylics2_has_upper_chamber_key(player))
    set_rule(world.get_location("Hylemxylem: Lower Reservoir Hole Pot 3", player), 
        lambda state: state._hylics2_has_upper_chamber_key(player))
    set_rule(world.get_location("Hylemxylem: Lower Reservoir Hole Sarcophagus", player), 
        lambda state: state._hylics2_has_upper_chamber_key(player))
    set_rule(world.get_location("Hylemxylem: Drained Upper Reservoir Burrito 1", player), 
        lambda state: state._hylics2_has_upper_chamber_key(player))
    set_rule(world.get_location("Hylemxylem: Drained Upper Reservoir Burrito 2", player), 
        lambda state: state._hylics2_has_upper_chamber_key(player))
    set_rule(world.get_location("Hylemxylem: Drained Upper Reservoir Burrito 3", player), 
        lambda state: state._hylics2_has_upper_chamber_key(player))
    set_rule(world.get_location("Hylemxylem: Upper Reservoir Hole Key", player), 
        lambda state: state._hylics2_has_upper_chamber_key(player))

    # extra rules if Extra Items in Logic is enabled
    if world.extra_items_in_logic[player]:
        for i in world.get_region("Foglast", player).entrances:
            add_rule(i, lambda state: state._hylics2_has_charge_up(player))
        for i in world.get_region("Sage Airship", player).entrances:
            add_rule(i, lambda state: state._hylics2_has_charge_up(player))
        for i in world.get_region("Hylemxylem", player).entrances:
            add_rule(i, lambda state: state._hylics2_has_charge_up(player) and state._hylics2_has_cup(player))

        add_rule(world.get_location("Sage Labyrinth: Motor Hunter Sarcophagus", player), 
            lambda state: state._hylics2_has_charge_up(player))

    # extra rules if Shuffle Party Members is enabled
    if world.party_shuffle[player]:
        for i in world.get_region("Viewax", player).entrances:
            add_rule(i, lambda state: state._hylics2_has_1_member(player))
        for i in world.get_region("Arcade Island", player).entrances:
            add_rule(i, lambda state: state._hylics2_has_1_member(player))
        for i in world.get_region("Foglast", player).entrances:
            add_rule(i, lambda state: state._hylics2_has_3_members(player))
        for i in world.get_region("New Muldul Vault", player).entrances:
            add_rule(i, lambda state: state._hylics2_has_3_members(player))
        for i in world.get_region("Sage Airship", player).entrances:
            add_rule(i, lambda state: state._hylics2_has_3_members(player))
        for i in world.get_region("Hylemxylem", player).entrances:
            add_rule(i, lambda state: state._hylics2_has_3_members(player))

        add_rule(world.get_location("Viewax's Edifice: Defeat Viewax", player), 
            lambda state: state._hylics2_has_2_members(player))
        add_rule(world.get_location("Juice Ranch: Battle with Somsnosa", player), 
            lambda state: state._hylics2_has_2_members(player))
        add_rule(world.get_location("Juice Ranch: Fridge", player), 
            lambda state: state._hylics2_has_2_members(player))