import asyncio
import traceback

import dolphin_memory_engine as dme

from CommonClient import logger
from worlds.pokepark_1.adresses import minigame_location_checks, quests_location_checks, UNLOCKS, \
    power_item_location_checks, \
    MemoryRange, stage_id_address, main_menu_stage_id, main_menu2_stage_id, main_menu3_stage_id, PRISMAS, POKEMON_STATES

delay_seconds = 0.9

async def location_watcher(ctx):
    # Meadow Zone
    # Beach Zone
    minigame_remaining = set(minigame_location_checks)
    prisma_remaining = set(
        (prisma.location.final_address, prisma.location.value, prisma.locationId)
        for prisma in PRISMAS.values()
        if prisma.location and prisma.locationId
    )
    quest_remaining = set(quests_location_checks)
    unlock_remaining = [
        (unlock.location, unlock.locationId)
        for unlock in UNLOCKS.values()
        if unlock.location and unlock.locationId
    ]
    power_remaining = set(power_item_location_checks)

    def check_unlock_locations():
        for check in unlock_remaining.copy():
            locations, location_id = check

            for loc in locations:
                current_value:int | None = None
                if loc.memory_range == MemoryRange.WORD:
                    current_value = dme.read_word(loc.final_address)
                elif loc.memory_range == MemoryRange.BYTE:
                    current_value = dme.read_byte(loc.final_address)

                if current_value == loc.value:
                    ctx.locations_checked.add(location_id)
                    unlock_remaining.remove(check)
                    break

    def check_prisma_locations():
        for check in prisma_remaining.copy():
            address, expected_value, location_id = check
            if dme.read_byte(address) == expected_value:
                ctx.locations_checked.add(location_id)
                prisma_remaining.remove(check)

    def check_friendship_locations(stage_id):
        zone_pokemon_states = [
            state for state in POKEMON_STATES.values()
            if state.zone_id == stage_id and state.location
        ]
        for pokemon_state in zone_pokemon_states:
            location_address = pokemon_state.location.final_address
            expected_value = pokemon_state.location.value
            memory_range = pokemon_state.location.memory_range
            current_value = None
            if memory_range == MemoryRange.WORD:
                current_value = dme.read_word(location_address)
            elif memory_range == MemoryRange.BYTE:
                current_value = dme.read_byte(location_address)

            if current_value == expected_value:
                ctx.locations_checked.add(pokemon_state.locationId)
                if memory_range == MemoryRange.WORD:
                    dme.write_word(location_address, 0x0)
                elif memory_range == MemoryRange.BYTE:
                    dme.write_byte(location_address, 0x0)

    def _sub():
        if not dme.is_hooked():
            return
        stage_id = dme.read_word(stage_id_address)

        if stage_id == main_menu_stage_id or stage_id == main_menu2_stage_id or stage_id == main_menu3_stage_id:
            return

        check_friendship_locations(stage_id)

        for check in minigame_remaining.copy():
            address, expected_value, location_id = check
            if int.from_bytes(dme.read_bytes(address, 2), byteorder='big') == expected_value:
                ctx.locations_checked.add(location_id)
                minigame_remaining.remove(check)

        check_prisma_locations()

        for check in quest_remaining.copy():
            address, expected_value, location_id = check
            if dme.read_byte(address) == expected_value:
                ctx.locations_checked.add(location_id)
                quest_remaining.remove(check)

        check_unlock_locations()

        for check in power_remaining.copy():
            address, expected_value, location_id, mask = check
            if (dme.read_byte(address) & mask) == expected_value:
                ctx.locations_checked.add(location_id)
                power_remaining.remove(check)

    while not ctx.exit_event.is_set():
        try:
            if not dme.is_hooked():
                dme.hook()
            else:
                _sub()
        except Exception as e:
            logger.error(f"Error in location_state_watcher: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")

        await asyncio.sleep(delay_seconds)