import asyncio
import traceback

import dolphin_memory_engine as dme

from CommonClient import logger
from worlds.pokepark import FRIENDSHIP_ITEMS
from worlds.pokepark.LocationIds import MinigameLocationIds
from worlds.pokepark.adresses import UNLOCKS, \
    stage_id_address, PRISMAS, \
    POKEMON_STATES, MINIGAME_LOCATIONS, QUEST_LOCATIONS, pokemon_id_address, valid_stage_ids
from worlds.pokepark.dme_helper import read_memory, write_memory

delay_seconds = 0.3
LAST_KNOWN_POKEMON_ID = 0


async def location_watcher(ctx):
    minigame_remaining = [
        (loc.location, loc.locationId)
        for loc in MINIGAME_LOCATIONS
    ]
    prisma_remaining = set(
        (prisma.location.final_address, prisma.location.value, prisma.locationId)
        for prisma in PRISMAS.values()
        if prisma.location and prisma.locationId
    )
    quest_remaining = [(quest.location, quest.locationId, quest.check_mask) for quest in QUEST_LOCATIONS]
    unlock_remaining = [
        location
        for unlock_state in UNLOCKS.values()
        for location in unlock_state.locations
    ]
    legendary_minigame_ranges = {
        "Jirachi": (MinigameLocationIds.PIKACHU_VINE_SWING.value, MinigameLocationIds.PACHIRISU_VINE_SWING.value),
        "Latias": (MinigameLocationIds.PIKACHU_CIRCLE.value, MinigameLocationIds.WINGULL_CIRCLE.value),
        "Manaphy": (MinigameLocationIds.PIKACHU_AQUA.value, MinigameLocationIds.LOTAD_AQUA.value),
        "Suicune": (MinigameLocationIds.PIKACHU_SLIDE.value, MinigameLocationIds.SPHEAL_SLIDE.value),
        "Metagross": (MinigameLocationIds.PIKACHU_PANEL.value, MinigameLocationIds.MAGBY_PANEL.value),
        "Heatran": (MinigameLocationIds.PIKACHU_BUMPER.value, MinigameLocationIds.BONSLY_BUMPER.value),
        "Groudon": (MinigameLocationIds.PIKACHU_BOULDER.value, MinigameLocationIds.MAWILE_BOULDER.value),
        "Celebi": (MinigameLocationIds.PIKACHU_SWING.value, MinigameLocationIds.CROAGUNK_SWING.value),
        "Darkrai": (MinigameLocationIds.PIKACHU_SLAM.value, MinigameLocationIds.KRABBY_SLAM.value),
        "Rotom": (MinigameLocationIds.PIKACHU_SHOOT.value, MinigameLocationIds.BALTOY_SHOOT.value),
        "Shaymin": (MinigameLocationIds.PIKACHU_HURDLE.value, MinigameLocationIds.VULPIX_HURDLE.value),
        "Latios": (MinigameLocationIds.PIKACHU_SKY.value, MinigameLocationIds.ZUBAT_SKY.value),
        "Deoxys": (MinigameLocationIds.PIKACHU_BALLOON.value, MinigameLocationIds.MIMEJR_BALLOON.value),
    }

    def check_unlock_locations(stage_id):
        for location in unlock_remaining.copy():
            current_value = read_memory(dme, location.location)
            if current_value == location.location.value and location.zone_id == stage_id:
                ctx.locations_checked.add(location.locationId)
                unlock_remaining.remove(location)
                break

    def check_prisma_locations():
        for check in prisma_remaining.copy():
            address, expected_value, location_id = check
            if dme.read_byte(address) == expected_value:
                ctx.locations_checked.add(location_id)
                prisma_remaining.remove(check)

    def check_friendship_locations(stage_id):
        global LAST_KNOWN_POKEMON_ID

        current_pokemon_id = dme.read_word(pokemon_id_address)

        if current_pokemon_id != 0:
            LAST_KNOWN_POKEMON_ID = current_pokemon_id

        check_pokemon_id = current_pokemon_id if current_pokemon_id != 0 else LAST_KNOWN_POKEMON_ID

        for state in POKEMON_STATES.values():
            if state.locations is not None:
                for location in state.locations:
                    if (location.zone_id == stage_id and
                            check_pokemon_id in location.pokemon_ids and
                            location.location):

                        expected_value = location.location.value
                        current_value = read_memory(dme, location.location)

                        if current_value == expected_value:
                            ctx.locations_checked.add(location.locationId)
                            write_memory(dme, location.location, 0x0)

    def check_minigame_locations():
        for check in minigame_remaining.copy():
            location, location_id = check
            current_value = read_memory(dme, location)
            if current_value == location.value:
                ctx.locations_checked.add(location_id)
                minigame_remaining.remove(check)

    def check_quest_locations():
        for check in quest_remaining.copy():
            location, location_id, check_mask = check
            current_value = read_memory(dme, location)
            if (current_value & check_mask) == location.value:
                ctx.locations_checked.add(location_id)
                quest_remaining.remove(check)

    def get_minigames_in_range(min_id, max_id):
        return [minigame.locationId for minigame in MINIGAME_LOCATIONS
                if minigame.locationId and min_id <= minigame.locationId <= max_id]

    def check_minigame_pokemon_unlock_locations():
        for pokemon, (min_id, max_id) in legendary_minigame_ranges.items():
            pokemon_minigames = get_minigames_in_range(min_id, max_id)

            if all(location_id in ctx.locations_checked for location_id in pokemon_minigames):
                ctx.locations_checked.add(FRIENDSHIP_ITEMS[pokemon])

    def _sub():
        if not dme.is_hooked():
            return
        stage_id = dme.read_word(stage_id_address)

        if not stage_id in valid_stage_ids:
            return

        check_friendship_locations(stage_id)

        check_minigame_locations()

        check_prisma_locations()

        check_quest_locations()

        check_unlock_locations(stage_id)

        check_minigame_pokemon_unlock_locations()

    while not ctx.exit_event.is_set():
        try:
            if not dme.is_hooked():
                dme.hook()
            else:
                _sub()
        except Exception as e:
            logger.error(f"Error in location_watcher: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            dme.un_hook()

        await asyncio.sleep(delay_seconds)
