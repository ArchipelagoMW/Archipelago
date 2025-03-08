import asyncio
import traceback

import dolphin_memory_engine as dme

from CommonClient import logger
from worlds.pokepark.adresses import \
    stage_id_address, intro_stage_id, ZONESYSTEM, main_menu_stage_id, main_menu2_stage_id, main_menu3_stage_id
from worlds.pokepark.dme_helper import write_memory, write_bit

delay_seconds = 1


async def state_watcher(ctx):
    initialization_done = False

    def initialize_game_state():

        current_stage = dme.read_word(stage_id_address)

        if current_stage == intro_stage_id:
            # Set Treehouse spawn
            dme.write_byte(0x8037AEE0, 0x02)
            dme.write_byte(0x8037AEE1, 0x01)
            dme.write_byte(0x8037AEE3, 0x05)
            dme.write_byte(0x8037AF20, 0x02)
            dme.write_byte(0x8037AF21, 0x01)
            dme.write_byte(0x8037AF23, 0x05)

            # init drifblim fast travel
            dme.write_byte(0x8037502F, 0x00)


            # Set starting values
            dme.write_byte(0x8037AEC9, 0x37)  # Init status menu
            dme.write_byte(0x80376AF7, 0x10)  # Activate Celebi

            # Skip tutorial elements
            dme.write_byte(0x80375021, 0x20)  # Skip driffzepeli quest
            dme.write_word(0x8037502E, 0x5840)  # Skip munchlax tutorial

            # Initialize prismas
            dme.write_word(0x80377E1C, 0x2)  # Init prisma for minigame bulbasaur
            dme.write_word(0x80376DA8, 0x2)  # Init prisma for minigame Venusaur
            dme.write_word(0x803772B8, 0x2)  # Init prisma for minigame Pelipper
            dme.write_word(0x80377174, 0x2)  # Init prisma for minigame Gyarados

            return True

        return False

    def update_zone_state(zone_system, received_items):

        available_states = [
            state for state in zone_system.states
            if state.item_id in received_items
        ]

        if available_states:
            current_state = max(available_states,
                                key=lambda x: x.world_state_value)  # highest world state from Region Unlocks

            dme.write_bytes(zone_system.world_state_address,
                            current_state.world_state_value.to_bytes(2, byteorder='big'))

            for state in available_states:
                for addr in state.addresses:
                    write_bit(dme, addr, addr.value, True)

        update_fast_travel(zone_system, available_states)

    def update_fast_travel(zone_system, available_states):

        fast_travel_value = sum(state.fast_travel_flag for state in available_states)
        dme.write_byte(zone_system.fast_travel_address, fast_travel_value)

    def update_treehouse_gates(zone_system, received_items):
        current_stage = dme.read_word(stage_id_address)

        for gate in zone_system.treehouse_gates:
            if current_stage == gate.stage_id:
                has_all_items = all(item_id in received_items for item_id in gate.item_ids)
                if has_all_items:
                    write_memory(dme, gate.gate, gate.gate.value)
                else:
                    write_memory(dme, gate.gate, 0x00)

    def update_connected_zone_gates(zone_system, received_items):

        for gate in zone_system.connected_zone_gates:
            has_all_items = all(item_id in received_items for item_id in gate.item_ids)
            write_bit(dme, gate.gate, gate.gate.value, has_all_items)

    def update_zone_systems(received_items):

        update_zone_state(ZONESYSTEM, received_items)
        update_treehouse_gates(ZONESYSTEM, received_items)
        update_connected_zone_gates(ZONESYSTEM, received_items)

    def _sub():
        nonlocal initialization_done

        if not dme.is_hooked():
            return

        stage_id = dme.read_word(stage_id_address)

        if stage_id == main_menu_stage_id or stage_id == main_menu2_stage_id or stage_id == main_menu3_stage_id:
            return

        if not initialization_done:
            initialization_done = initialize_game_state()

        received_items = [item.item for item in ctx.items_received]

        update_zone_systems(received_items)

    while not ctx.exit_event.is_set():
        try:
            if not dme.is_hooked():
                dme.hook()
            else:
                _sub()
        except Exception as e:
            logger.error(f"Error in location_state_watcher: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")

            raise
        await asyncio.sleep(delay_seconds)
