from worlds.generic.Rules import add_rule
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
        return self._hylics2_has_airship(player) and self._hylics2_has_worm_room_key(player) and\
            self._hylics2_has_paddle(player)

    def _hylics2_enter_sageship(self, player):
        return self._hylics2_has_skull_bomb(player) and self._hylics2_has_airship(player) and\
            self._hylics2_has_paddle(player)

    def _hylics2_enter_foglast(self, player):
        return self._hylics2_enter_wormpod(player)

    def _hylics2_enter_hylemxylem(self, player):
        return self._hylics2_can_air_dash(player) and self._hylics2_enter_foglast(player) and\
            self._hylics2_has_bridge_key(player)


def set_rules(hylics2world):
    world = hylics2world.multiworld
    player = hylics2world.player

    # Afterlife
    add_rule(world.get_location("Afterlife: TV", player),
        lambda state: state._hylics2_has_cave_key(player))

    # New Muldul
    add_rule(world.get_location("New Muldul: Underground Chest", player),
        lambda state: state._hylics2_can_air_dash(player))
    add_rule(world.get_location("New Muldul: TV", player),
        lambda state: state._hylics2_has_house_key(player))
    add_rule(world.get_location("New Muldul: Upper House Chest 1", player),
        lambda state: state._hylics2_has_upper_house_key(player))
    add_rule(world.get_location("New Muldul: Upper House Chest 2", player),
        lambda state: state._hylics2_has_upper_house_key(player))
    add_rule(world.get_location("New Muldul: Pot above Vault", player),
        lambda state: state._hylics2_can_air_dash(player))

    # New Muldul Vault
    add_rule(world.get_location("New Muldul: Rescued Blerol 1", player),
        lambda state: ((state._hylics2_has_jail_key(player) and state._hylics2_has_paddle(player)) and\
            (state._hylics2_can_air_dash(player) or state._hylics2_has_airship(player))) or\
                state._hylics2_enter_hylemxylem(player))
    add_rule(world.get_location("New Muldul: Rescued Blerol 2", player),
        lambda state: ((state._hylics2_has_jail_key(player) and state._hylics2_has_paddle(player)) and\
            (state._hylics2_can_air_dash(player) or state._hylics2_has_airship(player))) or\
                state._hylics2_enter_hylemxylem(player))
    add_rule(world.get_location("New Muldul: Vault Left Chest", player),
        lambda state: state._hylics2_enter_hylemxylem(player))
    add_rule(world.get_location("New Muldul: Vault Right Chest", player),
        lambda state: state._hylics2_enter_hylemxylem(player))
    add_rule(world.get_location("New Muldul: Vault Bomb", player),
        lambda state: state._hylics2_enter_hylemxylem(player))

    # Viewax's Edifice
    add_rule(world.get_location("Viewax's Edifice: Canopic Jar", player),
        lambda state: state._hylics2_has_paddle(player))
    add_rule(world.get_location("Viewax's Edifice: Cave Sarcophagus", player),
        lambda state: state._hylics2_has_paddle(player))
    add_rule(world.get_location("Viewax's Edifice: Shielded Key", player),
        lambda state: state._hylics2_has_paddle(player))
    add_rule(world.get_location("Viewax's Edifice: Shielded Key", player),
        lambda state: state._hylics2_has_paddle(player))
    add_rule(world.get_location("Viewax's Edifice: Tower Pot", player),
        lambda state: state._hylics2_has_paddle(player))
    add_rule(world.get_location("Viewax's Edifice: Tower Jar", player),
        lambda state: state._hylics2_has_paddle(player))
    add_rule(world.get_location("Viewax's Edifice: Tower Chest", player),
        lambda state: state._hylics2_has_paddle(player) and state._hylics2_has_tower_key(player))
    add_rule(world.get_location("Viewax's Edifice: Viewax Pot", player),
        lambda state: state._hylics2_has_paddle(player))
    add_rule(world.get_location("Viewax's Edifice: Defeat Viewax", player),
        lambda state: state._hylics2_has_paddle(player))
    add_rule(world.get_location("Viewax's Edifice: TV", player),
        lambda state: state._hylics2_has_paddle(player) and state._hylics2_has_jail_key(player))
    add_rule(world.get_location("Viewax's Edifice: Sage Fridge", player),
        lambda state: state._hylics2_can_air_dash(player))
    add_rule(world.get_location("Viewax's Edifice: Sage Item 1", player),
        lambda state: state._hylics2_can_air_dash(player))
    add_rule(world.get_location("Viewax's Edifice: Sage Item 2", player),
        lambda state: state._hylics2_can_air_dash(player))

    # Arcade 1
    add_rule(world.get_location("Arcade 1: Key", player),
        lambda state: state._hylics2_has_paddle(player))
    add_rule(world.get_location("Arcade 1: Coin Dash", player),
        lambda state: state._hylics2_has_paddle(player))
    add_rule(world.get_location("Arcade 1: Burrito Alcove 1", player),
        lambda state: state._hylics2_has_paddle(player))
    add_rule(world.get_location("Arcade 1: Burrito Alcove 2", player),
        lambda state: state._hylics2_has_paddle(player))
    add_rule(world.get_location("Arcade 1: Behind Spikes Banana", player),
        lambda state: state._hylics2_has_paddle(player))
    add_rule(world.get_location("Arcade 1: Pyramid Banana", player),
        lambda state: state._hylics2_has_paddle(player))
    add_rule(world.get_location("Arcade 1: Moving Platforms Muscle Applique", player),
        lambda state: state._hylics2_has_paddle(player))
    add_rule(world.get_location("Arcade 1: Bed Banana", player),
        lambda state: state._hylics2_has_paddle(player))

    # Airship
    add_rule(world.get_location("Airship: Talk to Somsnosa", player),
        lambda state: state._hylics2_has_worm_room_key(player))

    # Foglast
    add_rule(world.get_location("Foglast: Underground Sarcophagus", player),
        lambda state: state._hylics2_can_air_dash(player))
    add_rule(world.get_location("Foglast: Shielded Key", player),
        lambda state: state._hylics2_can_air_dash(player))
    add_rule(world.get_location("Foglast: TV", player),
        lambda state: state._hylics2_can_air_dash(player) and state._hylics2_has_clicker(player))
    add_rule(world.get_location("Foglast: Buy Clicker", player),
        lambda state: state._hylics2_can_air_dash(player))
    add_rule(world.get_location("Foglast: Shielded Chest", player),
        lambda state: state._hylics2_can_air_dash(player))
    add_rule(world.get_location("Foglast: Cave Fridge", player),
        lambda state: state._hylics2_can_air_dash(player))
    add_rule(world.get_location("Foglast: Roof Sarcophagus", player),
        lambda state: state._hylics2_can_air_dash(player) and state._hylics2_has_bridge_key(player))
    add_rule(world.get_location("Foglast: Under Lair Sarcophagus 1", player),
        lambda state: state._hylics2_can_air_dash(player) and state._hylics2_has_bridge_key(player))
    add_rule(world.get_location("Foglast: Under Lair Sarcophagus 2", player),
        lambda state: state._hylics2_can_air_dash(player) and state._hylics2_has_bridge_key(player))
    add_rule(world.get_location("Foglast: Under Lair Sarcophagus 3", player),
        lambda state: state._hylics2_can_air_dash(player) and state._hylics2_has_bridge_key(player))
    add_rule(world.get_location("Foglast: Sage Sarcophagus", player),
        lambda state: state._hylics2_can_air_dash(player) and state._hylics2_has_bridge_key(player))
    add_rule(world.get_location("Foglast: Sage Item 1", player),
        lambda state: state._hylics2_can_air_dash(player) and state._hylics2_has_bridge_key(player))
    add_rule(world.get_location("Foglast: Sage Item 2", player),
        lambda state: state._hylics2_can_air_dash(player) and state._hylics2_has_bridge_key(player))

    # Drill Castle
    add_rule(world.get_location("Drill Castle: Island Banana", player),
        lambda state: state._hylics2_can_air_dash(player))
    add_rule(world.get_location("Drill Castle: Island Pot", player),
        lambda state: state._hylics2_can_air_dash(player))
    add_rule(world.get_location("Drill Castle: Cave Sarcophagus", player),
        lambda state: state._hylics2_can_air_dash(player))
    add_rule(world.get_location("Drill Castle: TV", player),
        lambda state: state._hylics2_can_air_dash(player))

    # Sage Labyrinth
    add_rule(world.get_location("Sage Labyrinth: Sage Item 1", player),
        lambda state: state._hylics2_has_deep_key(player))
    add_rule(world.get_location("Sage Labyrinth: Sage Item 2", player),
        lambda state: state._hylics2_has_deep_key(player))
    add_rule(world.get_location("Sage Labyrinth: Sage Left Arm", player),
        lambda state: state._hylics2_has_deep_key(player))
    add_rule(world.get_location("Sage Labyrinth: Sage Right Arm", player),
        lambda state: state._hylics2_has_deep_key(player))
    add_rule(world.get_location("Sage Labyrinth: Sage Left Leg", player),
        lambda state: state._hylics2_has_deep_key(player))
    add_rule(world.get_location("Sage Labyrinth: Sage Right Leg", player),
        lambda state: state._hylics2_has_deep_key(player))

    # Sage Airship
    add_rule(world.get_location("Sage Airship: TV", player),
        lambda state: state._hylics2_has_tokens(player))

    # Hylemxylem
    add_rule(world.get_location("Hylemxylem: Upper Chamber Banana", player),
        lambda state: state._hylics2_has_upper_chamber_key(player))
    add_rule(world.get_location("Hylemxylem: Across Upper Reservoir Chest", player),
        lambda state: state._hylics2_has_upper_chamber_key(player))
    add_rule(world.get_location("Hylemxylem: Drained Lower Reservoir Chest", player),
        lambda state: state._hylics2_has_upper_chamber_key(player))
    add_rule(world.get_location("Hylemxylem: Drained Lower Reservoir Burrito 1", player),
        lambda state: state._hylics2_has_upper_chamber_key(player))
    add_rule(world.get_location("Hylemxylem: Drained Lower Reservoir Burrito 2", player),
        lambda state: state._hylics2_has_upper_chamber_key(player))
    add_rule(world.get_location("Hylemxylem: Lower Reservoir Hole Pot 1", player),
        lambda state: state._hylics2_has_upper_chamber_key(player))
    add_rule(world.get_location("Hylemxylem: Lower Reservoir Hole Pot 2", player),
        lambda state: state._hylics2_has_upper_chamber_key(player))
    add_rule(world.get_location("Hylemxylem: Lower Reservoir Hole Pot 3", player),
        lambda state: state._hylics2_has_upper_chamber_key(player))
    add_rule(world.get_location("Hylemxylem: Lower Reservoir Hole Sarcophagus", player),
        lambda state: state._hylics2_has_upper_chamber_key(player))
    add_rule(world.get_location("Hylemxylem: Drained Upper Reservoir Burrito 1", player),
        lambda state: state._hylics2_has_upper_chamber_key(player))
    add_rule(world.get_location("Hylemxylem: Drained Upper Reservoir Burrito 2", player),
        lambda state: state._hylics2_has_upper_chamber_key(player))
    add_rule(world.get_location("Hylemxylem: Drained Upper Reservoir Burrito 3", player),
        lambda state: state._hylics2_has_upper_chamber_key(player))
    add_rule(world.get_location("Hylemxylem: Upper Reservoir Hole Key", player),
        lambda state: state._hylics2_has_upper_chamber_key(player))

    # extra rules if Extra Items in Logic is enabled
    if world.extra_items_in_logic[player]:
        for i in world.get_region("Foglast", player).entrances:
            add_rule(i, lambda state: state._hylics2_has_charge_up(player))
        for i in world.get_region("Sage Airship", player).entrances:
            add_rule(i, lambda state: state._hylics2_has_charge_up(player) and state._hylics2_has_cup(player) and\
                state._hylics2_has_worm_room_key(player))
        for i in world.get_region("Hylemxylem", player).entrances:
            add_rule(i, lambda state: state._hylics2_has_charge_up(player) and state._hylics2_has_cup(player))

        add_rule(world.get_location("Sage Labyrinth: Motor Hunter Sarcophagus", player),
            lambda state: state._hylics2_has_charge_up(player) and state._hylics2_has_cup(player))

    # extra rules if Shuffle Party Members is enabled
    if world.party_shuffle[player]:
        for i in world.get_region("Arcade Island", player).entrances:
            add_rule(i, lambda state: state._hylics2_has_3_members(player))
        for i in world.get_region("Foglast", player).entrances:
            add_rule(i, lambda state: state._hylics2_has_3_members(player) or\
                (state._hylics2_has_2_members(player) and state._hylics2_has_jail_key(player)))
        for i in world.get_region("Sage Airship", player).entrances:
            add_rule(i, lambda state: state._hylics2_has_3_members(player))
        for i in world.get_region("Hylemxylem", player).entrances:
            add_rule(i, lambda state: state._hylics2_has_3_members(player))

        add_rule(world.get_location("Viewax's Edifice: Defeat Viewax", player),
            lambda state: state._hylics2_has_2_members(player))
        add_rule(world.get_location("New Muldul: Rescued Blerol 1", player),
            lambda state: state._hylics2_has_2_members(player))
        add_rule(world.get_location("New Muldul: Rescued Blerol 2", player),
            lambda state: state._hylics2_has_2_members(player))
        add_rule(world.get_location("New Muldul: Vault Left Chest", player),
            lambda state: state._hylics2_has_3_members(player))
        add_rule(world.get_location("New Muldul: Vault Right Chest", player),
            lambda state: state._hylics2_has_3_members(player))
        add_rule(world.get_location("New Muldul: Vault Bomb", player),
            lambda state: state._hylics2_has_3_members(player))
        add_rule(world.get_location("Juice Ranch: Battle with Somsnosa", player),
            lambda state: state._hylics2_has_2_members(player))
        add_rule(world.get_location("Juice Ranch: Somsnosa Joins", player),
            lambda state: state._hylics2_has_2_members(player))
        add_rule(world.get_location("Airship: Talk to Somsnosa", player),
            lambda state: state._hylics2_has_3_members(player))
        add_rule(world.get_location("Sage Labyrinth: Motor Hunter Sarcophagus", player),
            lambda state: state._hylics2_has_3_members(player))

    # extra rules if Shuffle Red Medallions is enabled
    if world.medallion_shuffle[player]:
        add_rule(world.get_location("New Muldul: Upper House Medallion", player),
            lambda state: state._hylics2_has_upper_house_key(player))
        add_rule(world.get_location("New Muldul: Vault Rear Left Medallion", player),
            lambda state: state._hylics2_enter_foglast(player) and state._hylics2_has_bridge_key(player))
        add_rule(world.get_location("New Muldul: Vault Rear Right Medallion", player),
            lambda state: state._hylics2_enter_foglast(player) and state._hylics2_has_bridge_key(player))
        add_rule(world.get_location("New Muldul: Vault Center Medallion", player),
            lambda state: state._hylics2_enter_foglast(player) and state._hylics2_has_bridge_key(player))
        add_rule(world.get_location("New Muldul: Vault Front Left Medallion", player),
            lambda state: state._hylics2_enter_foglast(player) and state._hylics2_has_bridge_key(player))
        add_rule(world.get_location("New Muldul: Vault Front Right Medallion", player),
            lambda state: state._hylics2_enter_foglast(player) and state._hylics2_has_bridge_key(player))
        add_rule(world.get_location("Viewax's Edifice: Fort Wall Medallion", player),
            lambda state: state._hylics2_has_paddle(player))
        add_rule(world.get_location("Viewax's Edifice: Jar Medallion", player),
            lambda state: state._hylics2_has_paddle(player))
        add_rule(world.get_location("Viewax's Edifice: Sage Chair Medallion", player),
            lambda state: state._hylics2_can_air_dash(player))
        add_rule(world.get_location("Arcade 1: Lonely Medallion", player),
            lambda state: state._hylics2_has_paddle(player))
        add_rule(world.get_location("Arcade 1: Alcove Medallion", player),
            lambda state: state._hylics2_has_paddle(player))
        add_rule(world.get_location("Foglast: Under Lair Medallion", player),
            lambda state: state._hylics2_has_bridge_key(player))
        add_rule(world.get_location("Foglast: Mid-Air Medallion", player),
            lambda state: state._hylics2_can_air_dash(player))
        add_rule(world.get_location("Foglast: Top of Tower Medallion", player),
            lambda state: state._hylics2_has_paddle(player))
        add_rule(world.get_location("Hylemxylem: Lower Reservoir Hole Medallion", player),
            lambda state: state._hylics2_has_upper_chamber_key(player))

    # extra rules is Shuffle Red Medallions and Party Shuffle are enabled
    if world.party_shuffle[player] and world.medallion_shuffle[player]:
        add_rule(world.get_location("New Muldul: Vault Rear Left Medallion", player),
            lambda state: state._hylics2_has_3_members(player))
        add_rule(world.get_location("New Muldul: Vault Rear Right Medallion", player),
            lambda state: state._hylics2_has_3_members(player))
        add_rule(world.get_location("New Muldul: Vault Center Medallion", player),
            lambda state: state._hylics2_has_3_members(player))
        add_rule(world.get_location("New Muldul: Vault Front Left Medallion", player),
            lambda state: state._hylics2_has_3_members(player))
        add_rule(world.get_location("New Muldul: Vault Front Right Medallion", player),
            lambda state: state._hylics2_has_3_members(player))

    # entrances
    for i in world.get_region("Airship", player).entrances:
        add_rule(i, lambda state: state._hylics2_has_airship(player))
    for i in world.get_region("Arcade Island", player).entrances:
        add_rule(i, lambda state: state._hylics2_has_airship(player) and state._hylics2_can_air_dash(player))
    for i in world.get_region("Worm Pod", player).entrances:
        add_rule(i, lambda state: state._hylics2_enter_wormpod(player))
    for i in world.get_region("Foglast", player).entrances:
        add_rule(i, lambda state: state._hylics2_enter_foglast(player))
    for i in world.get_region("Sage Labyrinth", player).entrances:
        add_rule(i, lambda state: state._hylics2_has_skull_bomb(player))
    for i in world.get_region("Sage Airship", player).entrances:
        add_rule(i, lambda state: state._hylics2_enter_sageship(player))
    for i in world.get_region("Hylemxylem", player).entrances:
        add_rule(i, lambda state: state._hylics2_enter_hylemxylem(player))

    # random start logic (default)
    if ((not world.random_start[player]) or \
        (world.random_start[player] and hylics2world.start_location == "Waynehouse")):
        # entrances
        for i in world.get_region("Viewax", player).entrances:
            add_rule(i, lambda state: state._hylics2_can_air_dash(player) or state._hylics2_has_airship(player))
        for i in world.get_region("TV Island", player).entrances:
            add_rule(i, lambda state: state._hylics2_has_airship(player))
        for i in world.get_region("Shield Facility", player).entrances:
            add_rule(i, lambda state: state._hylics2_has_airship(player))
        for i in world.get_region("Juice Ranch", player).entrances:
            add_rule(i, lambda state: state._hylics2_has_airship(player))

    # random start logic (Viewax's Edifice)
    elif (world.random_start[player] and hylics2world.start_location == "Viewax's Edifice"):
        for i in world.get_region("Waynehouse", player).entrances:
            add_rule(i, lambda state: state._hylics2_can_air_dash(player) or state._hylics2_has_airship(player))
        for i in world.get_region("New Muldul", player).entrances:
            add_rule(i, lambda state: state._hylics2_can_air_dash(player) or state._hylics2_has_airship(player))
        for i in world.get_region("New Muldul Vault", player).entrances:
            add_rule(i, lambda state: state._hylics2_can_air_dash(player) or state._hylics2_has_airship(player))
        for i in world.get_region("Drill Castle", player).entrances:
            add_rule(i, lambda state: state._hylics2_can_air_dash(player) or state._hylics2_has_airship(player))
        for i in world.get_region("TV Island", player).entrances:
            add_rule(i, lambda state: state._hylics2_has_airship(player))
        for i in world.get_region("Shield Facility", player).entrances:
            add_rule(i, lambda state: state._hylics2_has_airship(player))
        for i in world.get_region("Juice Ranch", player).entrances:
            add_rule(i, lambda state: state._hylics2_has_airship(player))
        for i in world.get_region("Sage Labyrinth", player).entrances:
            add_rule(i, lambda state: state._hylics2_has_airship(player))

    # random start logic (TV Island)
    elif (world.random_start[player] and hylics2world.start_location == "TV Island"):
        for i in world.get_region("Waynehouse", player).entrances:
            add_rule(i, lambda state: state._hylics2_has_airship(player))
        for i in world.get_region("New Muldul", player).entrances:
            add_rule(i, lambda state: state._hylics2_has_airship(player))
        for i in world.get_region("New Muldul Vault", player).entrances:
            add_rule(i, lambda state: state._hylics2_has_airship(player))
        for i in world.get_region("Drill Castle", player).entrances:
            add_rule(i, lambda state: state._hylics2_has_airship(player))
        for i in world.get_region("Viewax", player).entrances:
            add_rule(i, lambda state: state._hylics2_has_airship(player))
        for i in world.get_region("Shield Facility", player).entrances:
            add_rule(i, lambda state: state._hylics2_has_airship(player))
        for i in world.get_region("Juice Ranch", player).entrances:
            add_rule(i, lambda state: state._hylics2_has_airship(player))
        for i in world.get_region("Sage Labyrinth", player).entrances:
            add_rule(i, lambda state: state._hylics2_has_airship(player))

    # random start logic (Shield Facility)
    elif (world.random_start[player] and hylics2world.start_location == "Shield Facility"):
        for i in world.get_region("Waynehouse", player).entrances:
            add_rule(i, lambda state: state._hylics2_has_airship(player))
        for i in world.get_region("New Muldul", player).entrances:
            add_rule(i, lambda state: state._hylics2_has_airship(player))
        for i in world.get_region("New Muldul Vault", player).entrances:
            add_rule(i, lambda state: state._hylics2_has_airship(player))
        for i in world.get_region("Drill Castle", player).entrances:
            add_rule(i, lambda state: state._hylics2_has_airship(player))
        for i in world.get_region("Viewax", player).entrances:
            add_rule(i, lambda state: state._hylics2_has_airship(player))
        for i in world.get_region("TV Island", player).entrances:
            add_rule(i, lambda state: state._hylics2_has_airship(player))
        for i in world.get_region("Sage Labyrinth", player).entrances:
            add_rule(i, lambda state: state._hylics2_has_airship(player))
