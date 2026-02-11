from typing import TYPE_CHECKING
from BaseClasses import Entrance, Region
from enum import IntEnum

from .DSZeldaClient.subclasses import DSTransition, split_bits, AddrFromPointer
from .DSZeldaClient.ItemClass import DSItem, remove_vanilla_normal
from .data.SwitchLogic import *
from .data.Constants import EQUIPPED_SHIP_PARTS_ADDR, BOSS_DOOR_DATA, ITEM_GROUPS
from .data.Addresses import PHAddr

if TYPE_CHECKING:
    from entrance_rando import ERPlacementState
    from .Client import PhantomHourglassClient
    from worlds._bizhawk.context import BizHawkClientContext

async def receive_ship(client: "PhantomHourglassClient", ctx: "BizHawkClientContext", item: "PHItem", _):
    res = []
    if not (await PHAddr.custom_storage.read(ctx) & 2):
        for addr in EQUIPPED_SHIP_PARTS_ADDR:
            res += addr.get_write_list(item.ship)
    return res

async def receive_boss_key(client: "PhantomHourglassClient", ctx: "BizHawkClientContext", item: "PHItem", _):
    res = []
    if (ctx.slot_data.get("boss_key_behaviour", True)
            and client.current_stage in BOSS_DOOR_DATA
            and BOSS_DOOR_DATA[client.current_stage]["name"] in item.name):  # TODO: Add boss door data to boss key items?
        data = BOSS_DOOR_DATA[client.current_stage]
        last_value = await data["address"].read(ctx)
        new_value = last_value | data["value"]
        res += data["address"].get_write_list(new_value)
    return res

async def receive_potion(client: "PhantomHourglassClient", ctx: "BizHawkClientContext", item: "PHItem", _):
    res = []
    await client.update_potion_tracker(ctx)
    print(f"Potion data: {client.last_potions} {item.value}")
    for slot, pot, addr in zip([0, 1], client.last_potions, [PHAddr.potion_left, PHAddr.potion_right]):
        if not pot:
            res += addr.get_write_list(item.value)
            prev = await PHAddr.inventory_2.read(ctx, silent=True)
            res += PHAddr.inventory_2.get_write_list(prev | 0x6)
            client.last_potions[slot] = item.value
            break
    return res

async def receive_dummy(*args): return []

async def receive_full_heal(client, ctx, item, rii):
    await client.full_heal(ctx)
    return []

async def remove_vanilla_treasure(client: "PhantomHourglassClient", ctx: "BizHawkClientContext", item: "PHItem", _):
    treasure_write_list = split_bits(client.last_treasures, 8)
    return [(0x1BA5AC, treasure_write_list, item.domain)]

async def remove_vanilla_ship_part(client: "PhantomHourglassClient", ctx: "BizHawkClientContext", item: "PHItem", _):
    await client.remove_ship_parts(ctx)
    if client.last_scene == 0xB0D:
        await client.edit_ship(ctx)
    return []

async def remove_vanilla_potion(client: "PhantomHourglassClient", ctx: "BizHawkClientContext", item: "PHItem", _):
    print(f"Pots {client.last_potions}")
    for _i, slot in enumerate(client.last_potions):
        if not slot:
            addr = [PHAddr.potion_left, PHAddr.potion_right][_i]
            return addr.get_write_list(0)
    # else:
    rupee_item = client.item_data[item.overflow_item]
    print(f"Removing potion rupees")
    prev_rupees = await PHAddr.rupee_count.read(ctx)
    rupee_count = max(prev_rupees - rupee_item.value, 0)
    return PHAddr.rupee_count.get_write_list(ctx, rupee_count)

async def remove_vanilla_oshus_sword(client: "PhantomHourglassClient", ctx: "BizHawkClientContext", item: "PHItem", _):
    res = item.ammo_address.get_write_list(0)
    res += await remove_vanilla_normal(client, ctx, item, _)
    return res

async def remove_vanilla_sea_charts(client: "PhantomHourglassClient", ctx: "BizHawkClientContext", item: "PHItem", _):
    if ctx.slot_data.get("map_warp_options", 0):
        return []
    return await remove_vanilla_normal(client, ctx, item, _)

async def remove_vanilla_throwable_keys(client: "PhantomHourglassClient", ctx: "BizHawkClientContext", item: "PHItem", _):
    # Don't do anything if vanilla bk behaviour
    if "Boss Key" in item.name and not ctx.slot_data["boss_key_behaviour"]:
        return []
    # Don't do anything if vanilla pedestal item behaviour
    if ("Crystal" in item.name or "Force Gem" in item.name) and not ctx.slot_data.get("randomize_pedestal_items", 0):
        return []

    # Read actor id in link's held item address. For some reason it's somewhere else in GT
    if client.current_stage == 0x20:
        bk_id = await PHAddr.link_held_item_goron.read(ctx, silent=True)
    elif client.current_stage == 0x25:
        bk_id = await PHAddr.link_held_item_2.read(ctx, silent=True)
    else:
        bk_id = await PHAddr.link_held_item.read(ctx, silent=True)

    # Get the actor table
    actor_table_addr =  AddrFromPointer(await PHAddr.actor_table_pointer.read(ctx, silent=True) - 0x2000000, size=250)
    actor_table = hex(await actor_table_addr.read(ctx, silent=True))
    actor_table = "0" + actor_table[2:]
    print(f"Removing throwable key {item.name} with bk_id {bk_id}")

    # Loop through the actor table checking if each actor has the bk_id.
    for _i in range(len(actor_table) // 8):
        actor_data = actor_table[_i * 8:(_i + 1) * 8]
        if actor_data[1] == "0":  # filter out empty slots
            continue
        actor_id_addr = AddrFromPointer(int(actor_data, 16) + 8 - 0x2000000, size=4)
        actor_id = await actor_id_addr.read(ctx,  silent=True)
        # If you find the boss key, delete its pointer
        if actor_id == bk_id:
            little_endian_lol = AddrFromPointer(actor_table_addr + len(actor_table) // 2 - (_i + 1) * 4, size=4)
            print(f"Found bk pointer: {actor_table_addr} at index {_i}")
            await little_endian_lol.overwrite(ctx, 0, silent=True)
            break
    return []

class PHItem(DSItem):

    def __init__(self, name, data, all_items):
        super().__init__(name, data, all_items)

    def get_receive_function(self):
        receive_func = super().get_receive_function()
        if receive_func is None:
            if hasattr(self, "ship"):
                return receive_ship
            if self.name == "Refill: Health":
                return receive_full_heal
            if "Boss Key" in self.name:
                return receive_boss_key
            if "Potion" in self.name:
                return receive_potion
            return receive_dummy
        return receive_func

    def get_remove_vanilla_function(self):
        if self.name == "Treasure":
            return remove_vanilla_treasure
        if self.name  == "Ship Part":
            return remove_vanilla_ship_part
        if "Potion" in self.name:
            return remove_vanilla_potion
        if "Oshus' Sword" in self.name:
            return remove_vanilla_oshus_sword
        if "Sea Chart" in self.name:
            return remove_vanilla_sea_charts
        if self.name in ITEM_GROUPS["Throwable Keys"]:
            return remove_vanilla_throwable_keys
        return super().get_remove_vanilla_function()


class PHEntrance(Entrance):
    switch_state = {"TotOK": 0b1, "ToF": 0b1, "ToC": 0b1, "GT": 0b1, "ToI": 0b1}
    global_switch_state = 0b1


    def is_valid_source_transition(self, er_state: "ERPlacementState") -> bool:
        return self.can_reach(er_state.collection_state)

    def can_connect_to(self, other: Entrance, dead_end: bool, er_state: "ERPlacementState") -> bool:
        # the implementation of coupled causes issues for self-loops since the reverse entrance will be the
        # same as the forward entrance. In decoupled they are ok.
        # print(f"Checking connection for {self.name} -> {other.name}")
        # Vanilla GER Check first, cause the less resource intensive
        if not (self.randomization_type == other.randomization_type and (not er_state.coupled or self.name != other.name)):
            # print(f"\t{self.name} could not connect to {other.name}")
            return False

        # Don't connect to the same scene if using an entrance type that doesn't like it
        from .data.Entrances import ENTRANCES
        old_scene = ENTRANCES[self.name].scene
        new_scene =  ENTRANCES[other.name].scene
        if (old_scene == new_scene
                and (self.randomization_group & EntranceGroups.AREA_MASK in [EntranceGroups.OVERWORLD, EntranceGroups.ISLAND]
                or other.randomization_group & EntranceGroups.AREA_MASK in [EntranceGroups.OVERWORLD, EntranceGroups.ISLAND])):
            # print(f"Tried connecting to the same scene: {self.name}")
            return False

        # Check if you have a valid switch state for the transition you are trying
        if hasattr(er_state, "switch_state_option") and other.name in switch_sensitive_entrances:
            if er_state.switch_state_option == 2:
                if not self.global_switch_state & switch_sensitive_entrances[other.name]:
                    print(f"\t{self.name} could not connect to {other.name} cause switch state 2")
                    return False
            else:
                dungeon = other.name.split(None, 1)[0]
                if dungeon in self.switch_state and not self.switch_state[dungeon] & switch_sensitive_entrances[other.name]:
                    print(f"\t{self.name} could not connect to {other.name} cause switch state 1/0")
                    print(f"\t{self.switch_state[dungeon]} & {switch_sensitive_entrances[other.name]}")
                    return False


        # Target group lookup is passed in through on_connect cause cursed.
        # That means it's not in here until the first entrance has been connected
        if not hasattr(er_state, "target_group_lookup"):
            return True

        # Check if there are enough valid entrances to go around for the dead ends
        if not hasattr(er_state, "dead_end_counter"):
            self.make_dead_end_counter(er_state)

        # In stage 2 it is allowed to finish off groups with dead ends in them
        if dead_end and not hasattr(er_state, "stage_2"):
            er_state.stage_2 = True

        # When in phase 3, ignore?
        """ This wasn't working, ignore
        if dead_end or not hasattr(er_state, "dead_end_2"):
            # print(f"Trying to connect {self.name} => {other.name}")
            for counter in er_state.dead_end_counter.values():
                # print(f"\t{decode_entrance_groups(counter.group)}: {counter.others}")
                if self.name in counter.others or other.name in counter.others:
                    for counter2 in er_state.dead_end_counter.values():
                        # print(f"\t\tChecking dead ends {counter2.dead_ends} for group {decode_entrance_groups(counter2.group)}")
                        # print(f"\t\tChecking others {counter2.others}")
                        sub, sub_d = 0, 0
                        if self.name in counter2.others:
                            sub += 1
                        if other.name in counter2.others:
                            sub += 1
                        if self.name in counter2.dead_ends:
                            sub_d += 1
                        if other.name in counter2.dead_ends:
                            sub_d += 1
                        # print(f"\tFound {sub} entrances in others and {sub_d} entrances in dead_ends")
                        # print(f"\tde {len(counter2.dead_ends) - sub_d} > {len(counter2.others) - sub}")
                        if len(counter2.dead_ends) - sub_d > len(counter2.others) - sub:
                            print(f"\tFailed {self.name} => {other.name} "
                                  f"for group {decode_entrance_groups(counter2.group)} "
                                  f"from group {decode_entrance_groups(counter.group)}")
                            # return False
        """


        return True

    def make_dead_end_counter(self, er_state: "ERPlacementState"):
        class DECounter:
            def __init__(self, entrance_group):
                self.group = entrance_group
                self.dead_ends = []
                self.others = []

        # Create counter objects, and populate remaining entrances dict and dead ends
        remaining_entrances = {}
        for dead_end in er_state.entrance_lookup.dead_ends:
            remaining_entrances.setdefault(dead_end.randomization_group, DECounter(dead_end.randomization_group))
            remaining_entrances[dead_end.randomization_group].dead_ends.append(dead_end.name)

        # Add potential connected entrances
        target_group_lookup = er_state.target_group_lookup
        for group, counter in remaining_entrances.items():
            # print(f"Added group {decode_entrance_groups(group)}")
            for entrance in er_state.entrance_lookup.others:
                if entrance.randomization_group in target_group_lookup[group]:
                    # print(f"\t{entrance.name}")
                    remaining_entrances[group].others.append(entrance.name)

        er_state.dead_end_counter = remaining_entrances

class PHRegion(Region):
    entrance_type = PHEntrance


island_lookup = {
    0: "sea",
    1: "mercay",
    2: "cannon",
    3: "ember",
    4: "molida",
    5: "spirit",
    6: "gust",
    7: "bannan",
    8: "uncharted",
    9: "zauz",
    10: "ghost",
    11: "goron",
    12: "frost",
    13: "dead",
    14: "ruins"
}
direction_lookup = {
    0: "none",
    1: "left",
    2: "right",
    3: "up",
    4: "down",
    5: "enter",
    6: "exit"}
type_lookup = {
    0: "none",
    1: "house",
    2: "cave",
    3: "port",
    4: "overworld",
    5: "dungeon",
    6: "boss",
    7: "dungeon_room",
    8: "warp",
    9: "stairs",
    10: "holes",
}

# Print EntranceGroups as human readable string
def decode_entrance_groups(group):
    direction = group & EntranceGroups.DIRECTION_MASK
    area = (group & EntranceGroups.AREA_MASK) >> 3
    island = (group & EntranceGroups.ISLAND_MASK) >> 7

    return f"{direction_lookup[direction]}_{type_lookup[area]}_{island_lookup[island]}"

class EntranceGroups(IntEnum):
    NONE = 0
    # Directions
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4
    INSIDE = 5
    OUTSIDE = 6
    # Types
    HOUSE = 1 << 3
    CAVE = 2 << 3
    ISLAND = 3 << 3
    OVERWORLD = 4 << 3
    DUNGEON_ENTRANCE = 5 << 3
    BOSS = 6 << 3
    DUNGEON_ROOM = 7 << 3
    WARP_PORTAL = 8 << 3
    STAIRS = 9 << 3
    HOLES = 10 << 3
    EVENT = 11 << 3
    # Island mask
    SEA = 0 << 7
    MERCAY = 1 << 7
    CANNON = 2 << 7
    EMBER = 3 << 7
    MOLIDA = 4 << 7
    SPIRIT = 5 << 7
    GUST = 6 << 7
    BANNAN = 7 << 7
    UNCHARTED = 8 << 7
    ZAUZ = 9 << 7
    GHOST = 10 << 7
    GORON = 11 << 7
    FROST = 12 << 7
    DEAD = 13 << 7
    RUINS = 14 << 7

    # Bitmasks
    DIRECTION_MASK = HOUSE - 1
    AREA_MASK = MERCAY - HOUSE
    ISLAND_MASK =  ~0 << 7

    def __str__(self):
        return decode_entrance_groups(self.value)

    def island(self):
        return self & self.ISLAND_MASK

    def entrance_type(self):
        return self & self.AREA_MASK

    @staticmethod
    def area_shift(area):
        return area << 3

    @staticmethod
    def area_unshift(area):
        return area >> 3

    @staticmethod
    def island_shift(island):
        return island << 7

    @staticmethod
    def island_unshift(island):
        return island >> 7

OPPOSITE_ENTRANCE_GROUPS = {
    EntranceGroups.RIGHT: EntranceGroups.LEFT,
    EntranceGroups.LEFT: EntranceGroups.RIGHT,
    EntranceGroups.UP: EntranceGroups.DOWN,
    EntranceGroups.DOWN: EntranceGroups.UP,
    0: 0,
    EntranceGroups.NONE: EntranceGroups.NONE,
    EntranceGroups.INSIDE: EntranceGroups.OUTSIDE,
    EntranceGroups.OUTSIDE: EntranceGroups.INSIDE
}

class PHTransition(DSTransition):
    """
    Datastructures for dealing with Transitions on the client side.
    Not to be confused with PHEntrances, that deals with entrance objects during ER placement.
    """
    entrance_groups = EntranceGroups
    opposite_entrance_groups = OPPOSITE_ENTRANCE_GROUPS

switch_logic_lookup = {}
for i in switch_logic:
    switch_logic_lookup.setdefault(i[0], [])
    switch_logic_lookup[i[0]].append(i)
# print(f"SLL: {switch_logic_lookup}")

# Called in on_connect. updates the switch states one can reach an exit with, based on switch_logic
def update_switch_logic(old_ex: "PHEntrance", entr: "PHEntrance", er_state, logic_option, switch_option, new_exits):
    # Get the entrance object for an exit to set its logical switch states
    def find_exit(exit_name):
        for e in er_state.entrance_lookup._usable_exits:
            if e.name == exit_name:
                return e
        return None

    # Don't process if vanilla behaviour and the connection doesn't connect rooms in the same dungeon
    if switch_option == 0:
        dungeon_connections = [EntranceGroups.DUNGEON_ROOM, EntranceGroups.WARP_PORTAL, EntranceGroups.DUNGEON_ENTRANCE]
        if not (entr.randomization_group & EntranceGroups.AREA_MASK in dungeon_connections
                and old_ex.randomization_group & EntranceGroups.AREA_MASK in dungeon_connections
                and old_ex.randomization_group & EntranceGroups.ISLAND_MASK == entr.randomization_group & EntranceGroups.ISLAND_MASK):
            print(f"Switch logic canceled due to entrance pairing being in different dungeons on vanilla setting")
            return

    # Lookup switch logic and propagate it to the newly revealed exits
    # print(f"\tAttempting SLL {entr.name}")
    if entr.name in switch_logic_lookup:
        # print(f"\tsuccess found {switch_logic_lookup[entr.name]}")
        for _, ex, *logic in switch_logic_lookup[entr.name]:
            logic_state = min(logic_option, len(logic)-1)
            ex_object = find_exit(ex)
            print(f"\tpropagating switch logic for {ex} with state {logic[logic_state]} from {entr.name}")
            if ex_object:
                if switch_option == 2:
                    ex_object.global_switch_state = logic[logic_state]
                else:
                    dungeon = entr.name.split(None, 1)[0]
                    ex_object.switch_state = entr.switch_state
                    ex_object.switch_state[dungeon] = logic[logic_state]

    # if not in switch logic, propagate the previous exit's logic
    for ex in new_exits:
        print(f"\tupdating switch logic for {ex.name} to from {old_ex.name} to {old_ex.global_switch_state}")
        ex.global_switch_state = old_ex.global_switch_state
        ex.switch_state = old_ex.switch_state

