import traceback

import dolphin_memory_engine as dme
import asyncio
from CommonClient  import logger
from worlds.pokepark_1 import PRISM_ITEM

from worlds.pokepark_1.adresses import stage_id_address, is_in_menu_address, pokemon_id_address, \
    tmp_addresses_disabled_friendship_overwrite, UNCHECKED_MEADOW_ZONE_LOCATION_POKEMON_IDS, \
    MEADOW_ZONE_SPECIAL_EXCEPTION_POKEMON, UNCHECKED_BEACH_ZONE_LOCATION_POKEMON_IDS, meadow_zone_stage_id, \
    beach_zone_stage_id, blocked_unlocks, prisma_overwrites, prisma_item_checks, venusaur_minigame_stage_id, \
    bulbasaur_minigame_stage_id, meadow_zone_unlock_pokemon_addresses_for_location, unlock_item_checks, \
    pelliper_minigame_stage_id, gyarados_minigame_stage_id, beach_zone_unlock_pokemon_addresses_for_location

empty_pokemon_id = 0x00



friendship_deactivated_value = 0x0

friendship_activated_value = 0x80

delay_seconds = 0.5

original_values = {}  # {address: value}


def store_and_overwrite_address(address, value):
    if address not in original_values:
        original_values[address] = dme.read_byte(address)
    dme.write_byte(address, value)
    tmp_addresses_disabled_friendship_overwrite.append(address)


def restore_addresses():
    for address in tmp_addresses_disabled_friendship_overwrite:
        if address in original_values:
            dme.write_byte(address, original_values[address])
            del original_values[address]
    tmp_addresses_disabled_friendship_overwrite.clear()

class ZoneStateManager:
    def __init__(self, zone_id, unchecked_pokemon_ids, special_exceptions=None,unlock_pokemon_blocks=None):
        self.zone_id = zone_id
        self.unchecked_pokemon_ids = unchecked_pokemon_ids
        self.checked_pokemon_ids = []
        self.special_exceptions = special_exceptions or []
        self.unlock_pokemon_blocks = unlock_pokemon_blocks or {}  # {pokemon_id: [unlock_items]}
        self.temp_blocked_unlocks = []
    def update_states(self, location_id):
        entries_to_move = [
            entry for entry in self.unchecked_pokemon_ids
            if entry[2] == location_id
        ]

        for entry in entries_to_move:
            self.unchecked_pokemon_ids.remove(entry)
            self.checked_pokemon_ids.append(entry)

        for entry in self.special_exceptions[:]:
            if entry[0] == location_id:
                self.special_exceptions.remove(entry)

    def handle_pokemon_state(self, pokemon_id, is_in_menu):
        for pid, checks, location_id in self.unchecked_pokemon_ids:
            if pokemon_id == pid:
                address, check_value = checks[0]
                store_and_overwrite_address(address, friendship_deactivated_value)
                if pid in self.unlock_pokemon_blocks:
                    for unlock in self.unlock_pokemon_blocks[pid]:
                        if unlock not in blocked_unlocks:
                            blocked_unlocks.append(unlock)
                            self.temp_blocked_unlocks.append(unlock)
                            unlock_address, _ = unlock_item_checks[unlock]
                            store_and_overwrite_address(unlock_address, 0)
                break

        for pid, checks, location_id in self.checked_pokemon_ids:
            if pokemon_id == pid:
                address, check_value = checks[0]
                store_and_overwrite_address(address, friendship_activated_value)
                break

        if pokemon_id == empty_pokemon_id:
            restore_addresses()
            for unlock in self.temp_blocked_unlocks:
                if unlock in blocked_unlocks:
                    blocked_unlocks.remove(unlock)
            self.temp_blocked_unlocks.clear()

            if is_in_menu != 0x01:
                for location_id, checks in self.special_exceptions:
                    address, check_value = checks[0]
                    store_and_overwrite_address(address, friendship_deactivated_value)


# Zone Manager Instances

zone_managers = {
    meadow_zone_stage_id: ZoneStateManager(
        meadow_zone_stage_id,  # Meadow Zone
        UNCHECKED_MEADOW_ZONE_LOCATION_POKEMON_IDS,
        MEADOW_ZONE_SPECIAL_EXCEPTION_POKEMON,
        meadow_zone_unlock_pokemon_addresses_for_location
    ),
    beach_zone_stage_id: ZoneStateManager(
        beach_zone_stage_id,  # Beach Zone
        UNCHECKED_BEACH_ZONE_LOCATION_POKEMON_IDS,
        unlock_pokemon_blocks=beach_zone_unlock_pokemon_addresses_for_location
    ),
}


def handle_prisma_overwrites(stage_id, ctx):
    # Mapping of stage IDs to their specific Prisma
    stage_prisma_map = {
        bulbasaur_minigame_stage_id: PRISM_ITEM.get("Bulbasaur Prisma"),
        venusaur_minigame_stage_id: PRISM_ITEM.get("Venusaur Prisma"),
        pelliper_minigame_stage_id: PRISM_ITEM.get("Pelliper Prisma"),
        gyarados_minigame_stage_id: PRISM_ITEM.get("Gyarados Prisma")
    }

    current_stage_prisma = stage_prisma_map.get(stage_id)

    if current_stage_prisma is None:
        for prisma in prisma_item_checks:
            for address, value in prisma_item_checks[prisma]:
                if prisma in prisma_overwrites:
                    if address in original_values:
                        dme.write_word(address, original_values[address])
                        del original_values[address]
        prisma_overwrites.clear()
        return

    if current_stage_prisma not in ctx.checked_locations:

        prisma_overwrites.append(current_stage_prisma)

        for address, value in prisma_item_checks[current_stage_prisma]:
            if address not in original_values:
                original_values[address] = dme.read_word(address)
            dme.write_word(address, 0x2)

    if current_stage_prisma in ctx.checked_locations:

        prisma_overwrites.append(current_stage_prisma)

        for address, value in prisma_item_checks[current_stage_prisma]:
            if address not in original_values:
                original_values[address] = dme.read_word(address)
            dme.write_word(address, 0x3)

async def location_state_watcher(ctx):
    async def _sub():
        if not dme.is_hooked():
            return

        for location_id in ctx.checked_locations:
            for manager in zone_managers.values():
                manager.update_states(location_id)

        stage_id = dme.read_word(stage_id_address)
        is_in_menu = dme.read_byte(is_in_menu_address)
        pokemon_id = dme.read_word(pokemon_id_address)

        handle_prisma_overwrites(
            stage_id,
            ctx,
        )

        if stage_id in zone_managers:
            zone_managers[stage_id].handle_pokemon_state(pokemon_id, is_in_menu)

        for location_id in ctx.checked_locations:
            if location_id in blocked_unlocks:
                blocked_unlocks.remove(location_id)


    while not ctx.exit_event.is_set():
        try:
            if not dme.is_hooked():
                dme.hook()
            else:
                await _sub()
        except Exception as e:
            logger.error(f"Error in location_state_watcher: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")

            raise
        await asyncio.sleep(delay_seconds)
