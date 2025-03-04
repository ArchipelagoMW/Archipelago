import asyncio
import traceback

import dolphin_memory_engine as dme

from CommonClient import logger
from worlds.pokepark_1.adresses import  UNLOCKS, \
    stage_id_address, main_menu_stage_id, main_menu2_stage_id, main_menu3_stage_id, PRISMAS, \
    POKEMON_STATES, MINIGAME_LOCATIONS, QUEST_LOCATIONS
from worlds.pokepark_1.dme_helper import read_memory, write_memory

delay_seconds = 0.9


async def location_watcher(ctx):
    # Meadow Zone
    # Beach Zone
    minigame_remaining = [
        (loc.location, loc.locationId)
        for loc in MINIGAME_LOCATIONS
    ]
    prisma_remaining = set(
        (prisma.location.final_address, prisma.location.value, prisma.locationId)
        for prisma in PRISMAS.values()
        if prisma.location and prisma.locationId
    )
    quest_remaining = [(quest.location,quest.locationId,quest.check_mask) for quest in QUEST_LOCATIONS]
    unlock_remaining = [
        (unlock.location, unlock.locationId)
        for unlock in UNLOCKS.values()
        if unlock.location and unlock.locationId
    ]

    def check_unlock_locations():
        for check in unlock_remaining.copy():
            locations, location_id = check

            for loc in locations:
                current_value = read_memory(dme,loc)
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
        zone_locations = []
        for state in POKEMON_STATES.values():
            if state.locations is not None:
                for location in state.locations:
                    if location.zone_id == stage_id and location.location:
                        zone_locations.append(location)

        for location in zone_locations:
            expected_value = location.location.value
            current_value = read_memory(dme, location.location)
            if current_value == expected_value:
                ctx.locations_checked.add(location.locationId)
                write_memory(dme, location.location, 0x0)


    def check_minigame_locations():
        for check in minigame_remaining.copy():
            location, location_id = check
            current_value = read_memory(dme,location)
            if current_value == location.value:
                ctx.locations_checked.add(location_id)
                minigame_remaining.remove(check)

    def check_quest_locations():
        for check in quest_remaining.copy():
            location, location_id, check_mask = check
            current_value = read_memory(dme,location)
            if(current_value & check_mask) == location.value:
                ctx.locations_checked.add(location_id)
                quest_remaining.remove(check)

    def _sub():
        if not dme.is_hooked():
            return
        stage_id = dme.read_word(stage_id_address)

        if stage_id == main_menu_stage_id or stage_id == main_menu2_stage_id or stage_id == main_menu3_stage_id:
            return

        check_friendship_locations(stage_id)

        check_minigame_locations()

        check_prisma_locations()

        check_quest_locations()

        check_unlock_locations()

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
