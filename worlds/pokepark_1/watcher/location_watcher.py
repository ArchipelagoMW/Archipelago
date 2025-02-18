import asyncio
import traceback

import dolphin_memory_engine as dme

from CommonClient import logger
from worlds.pokepark_1.adresses import minigame_location_checks, meadow_zone_friendship_location_checks, \
    beach_zone_friendship_checks, prisma_location_checks, \
    quests_location_checks, unlocks_location_checks, stage_id_address, meadow_zone_stage_id, beach_zone_stage_id, \
    main_menu_stage_id, main_menu2_stage_id, power_item_location_checks, main_menu3_stage_id

delay_seconds = 0.9

async def location_watcher(ctx):
    # Meadow Zone
    meadow_friendship_remaining = set(meadow_zone_friendship_location_checks)
    # Beach Zone
    beach_friendship_remaining = set(beach_zone_friendship_checks)
    minigame_remaining = set(minigame_location_checks)
    prisma_remaining = set(prisma_location_checks)
    quest_remaining = set(quests_location_checks)
    unlock_remaining = set(unlocks_location_checks)
    power_remaining = set(power_item_location_checks)

    def _sub():
        if not dme.is_hooked():
            return
        stage_id = dme.read_word(stage_id_address)

        if stage_id == main_menu_stage_id or stage_id == main_menu2_stage_id or stage_id == main_menu3_stage_id:
            return
        if stage_id == meadow_zone_stage_id:  # Meadow Zone
            for check in meadow_friendship_remaining.copy():
                address, expected_value, location_id = check
                if dme.read_byte(address) == expected_value:
                    ctx.locations_checked.add(location_id)
                    dme.write_byte(address, 0x0)
                    meadow_friendship_remaining.remove(check)
        elif stage_id == beach_zone_stage_id:  # Beach Zone
            for check in beach_friendship_remaining.copy():
                address, expected_value, location_id = check
                if dme.read_byte(address) == expected_value:
                    ctx.locations_checked.add(location_id)
                    dme.write_byte(address, 0x0)
                    beach_friendship_remaining.remove(check)

        for check in minigame_remaining.copy():
            address, expected_value, location_id = check
            if int.from_bytes(dme.read_bytes(address, 2), byteorder='big') == expected_value:
                ctx.locations_checked.add(location_id)
                minigame_remaining.remove(check)

        for check in prisma_remaining.copy():
            address, expected_value, location_id = check
            if dme.read_byte(address) == expected_value:
                ctx.locations_checked.add(location_id)
                prisma_remaining.remove(check)

        for check in quest_remaining.copy():
            address, expected_value, location_id = check
            if dme.read_byte(address) == expected_value:
                ctx.locations_checked.add(location_id)
                quest_remaining.remove(check)

        for check in unlock_remaining.copy():
            address, expected_value, location_id = check
            if dme.read_byte(address) == expected_value:
                ctx.locations_checked.add(location_id)
                unlock_remaining.remove(check)

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

            raise
        await asyncio.sleep(delay_seconds)