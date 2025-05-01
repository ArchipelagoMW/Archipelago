import asyncio
import traceback

import dolphin_memory_engine as dme

from CommonClient import logger
from worlds.pokepark.adresses import \
    stage_id_address, intro_stage_id, ZONESYSTEM, \
    valid_stage_ids
from worlds.pokepark.dme_helper import write_memory, write_bit

delay_seconds = 1


async def state_watcher(ctx):
    def initialize_game_state():

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

        # Skip tutorial elements
        dme.write_byte(0x80375021, 0x20)  # Skip driffzepeli quest
        dme.write_word(0x8037502E, 0x5840)  # Skip munchlax tutorial
        dme.write_byte(0x80375020, 0x02)  # init bulbasaur quest state

        # Initialize prismas
        dme.write_word(0x80377E1C, 0x2)  # Init prisma for minigame bulbasaur
        dme.write_word(0x80376DA8, 0x2)  # Init prisma for minigame Venusaur
        dme.write_word(0x803772B8, 0x2)  # Init prisma for minigame Pelipper
        dme.write_word(0x80377174, 0x2)  # Init prisma for minigame Gyarados
        dme.write_word(0x80377540, 0x2)  # Init prisma for minigame Empoleon
        dme.write_word(0x80377684, 0x2)  # Init prisma for minigame Bastiodon
        dme.write_word(0x803777C8, 0x2)  # Init prisma for minigame Rhyperior
        dme.write_word(0x8037790C, 0x2)  # Init prisma for minigame Blaziken
        dme.write_word(0x80376EEC, 0x2)  # Init prisma for minigame Tangrowth
        dme.write_word(0x80377030, 0x2)  # Init prisma for minigame Dusknoir
        dme.write_word(0x80377A50, 0x2)  # Init prisma for minigame Rotom
        dme.write_word(0x80376B20, 0x02)  # Init prisma for minigame Absol
        dme.write_word(0x80377CD8, 0x02)  # Init prisma for minigame Salamence
        dme.write_word(0x80376C64, 0x02)  # Init prisma for minigame Rayquaza

        # remove hide and seek popup
        dme.write_byte(0x8037502b, 0x01)
        # drifblim fast travel skippable
        dme.write_byte(0x80375022, 0x80)
        # allow lapras travel skip
        dme.write_byte(0x80375014, 0x02)
        # skip power up explanation
        dme.write_byte(0x8037501b, 0x08)

    def update_zone_state(zone_system, received_items):

        available_states = [
            state for state in zone_system.states
            if state.item_id in received_items
        ]
        if available_states:
            current_state = max(available_states,
                                key=lambda x: x.world_state_value)  # highest world state from Region Unlocks

            if int.from_bytes(dme.read_bytes(zone_system.world_state_address, 2)) < 0x272e:
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

        if not dme.is_hooked():
            return

        stage_id = dme.read_word(stage_id_address)

        if not stage_id in valid_stage_ids:
            return

        if stage_id == intro_stage_id:
            initialize_game_state()

        received_items = [item.item for item in ctx.items_received]

        update_zone_systems(received_items)

    while not ctx.exit_event.is_set():
        try:
            if not dme.is_hooked():
                dme.hook()
            else:
                _sub()
        except Exception as e:
            logger.error(f"Error in world_state_watcher: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            dme.un_hook()

        await asyncio.sleep(delay_seconds)
