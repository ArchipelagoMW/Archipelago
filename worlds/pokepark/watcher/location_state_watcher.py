import asyncio
import traceback

import dolphin_memory_engine as dme

from CommonClient import logger
from worlds.pokepark.adresses import stage_id_address, is_in_menu_address, pokemon_id_address, prisma_blocked_itemIds, \
    UNLOCKS, PRISMAS, PrismaItem, POKEMON_STATES, blocked_friendship_itemIds, blocked_friendship_unlock_itemIds, \
    BLOCKED_UNLOCKS, LOADSCREEN_TO_ZONE, PokemonLocation, valid_stage_ids
from worlds.pokepark.dme_helper import write_memory, read_memory

empty_pokemon_id = 0x00

delay_seconds = 0.5

original_values = {}  # {address: value}
LAST_ZONE = None
SPECIAL_UNLOCK_LOCATIONS = {
    item_id: unlock_state for item_id, unlock_state in UNLOCKS.items()
    if any(location.is_blocked_until_location for location in unlock_state.locations)
}


async def location_state_watcher(ctx):
    def restore_original_prisma_values():
        for prisma in PRISMAS.values():
            address = prisma.item.final_address
            if prisma.itemId in prisma_blocked_itemIds:
                if address in original_values:
                    dme.write_word(address, original_values[address])
                    del original_values[address]
        prisma_blocked_itemIds.clear()

    def set_state_for_unchecked_prisma_location(current_prisma: PrismaItem | None):
        prisma_blocked_itemIds.append(current_prisma.itemId)

        address = current_prisma.item.final_address
        if address not in original_values:
            original_values[address] = dme.read_word(address)
            dme.write_word(address, 0x2)

    def set_state_for_checked_prisma_location(current_prisma: PrismaItem | None):
        prisma_blocked_itemIds.append(current_prisma.itemId)

        address = current_prisma.item.final_address
        value = current_prisma.item.value
        if address not in original_values:
            original_values[address] = dme.read_word(address)
            dme.write_word(address, value)

    def handle_prisma_overwrites(stage_id: int):
        current_prisma = next((prisma for prisma in PRISMAS.values() if prisma.stage_id == stage_id), None)

        if current_prisma is None:
            restore_original_prisma_values()
            return

        if current_prisma.locationId not in ctx.locations_checked:
            set_state_for_unchecked_prisma_location(current_prisma)

        if current_prisma.locationId in ctx.locations_checked:
            set_state_for_checked_prisma_location(current_prisma)

    def activate_state_friendships(location: PokemonLocation):
        if location.friendship_items_to_block:
            for item_id in location.friendship_items_to_block:
                blocked_friendship_itemIds.append(item_id)
                item = POKEMON_STATES[item_id].item
                if item.final_address not in original_values:
                    original_values[item.final_address] = read_memory(dme, item)
                write_memory(dme, item, item.value)

    def block_pokemon_state_items(location: PokemonLocation):
        block_pokemon_friendship_items(location)
        block_pokemon_unlock_items(location)

    def block_pokemon_friendship_items(location: PokemonLocation):
        if location.friendship_items_to_block:
            for item_id in location.friendship_items_to_block:
                if item_id not in blocked_friendship_itemIds:
                    blocked_friendship_itemIds.append(item_id)
                    item = POKEMON_STATES[item_id].item
                    if item.final_address not in original_values:
                        original_values[item.final_address] = read_memory(dme, item)
                    write_memory(dme, item, 0x0)

    def block_pokemon_unlock_items(location: PokemonLocation):
        if location.unlock_items_to_block:
            for item_id in location.unlock_items_to_block:
                if item_id not in blocked_friendship_unlock_itemIds:
                    blocked_friendship_unlock_itemIds.append(item_id)
                    item = UNLOCKS[item_id].item
                    if item.final_address not in original_values:
                        original_values[item.final_address] = read_memory(dme, item)

    def restore_blocked_items():
        for item_id in blocked_friendship_itemIds[:]:
            item = POKEMON_STATES[item_id].item
            if item.final_address in original_values:
                write_memory(dme, item, original_values[item.final_address])
                del original_values[item.final_address]
        blocked_friendship_itemIds.clear()

        for item_id in blocked_friendship_unlock_itemIds[:]:
            item = UNLOCKS[item_id].item
            if item.final_address in original_values:
                write_memory(dme, item, original_values[item.final_address])
                del original_values[item.final_address]
        blocked_friendship_unlock_itemIds.clear()

    def handle_pokemon_location_states(stage_id: int, is_in_menu: int, pokemon_id: int):

        if pokemon_id == empty_pokemon_id:
            restore_blocked_items()

            if not is_in_menu == 0x01:
                for pokemon_state in POKEMON_STATES.values():
                    for location in pokemon_state.locations:
                        if (location.zone_id == stage_id and
                                location.is_special_exception and
                                location.locationId not in ctx.locations_checked):
                            block_pokemon_friendship_items(location)
                            break
        else:
            current_location = None
            current_state = None

            for state in POKEMON_STATES.values():
                if state.locations:
                    for location in state.locations:
                        if (location.zone_id == stage_id and location.pokemon_ids and
                                pokemon_id in location.pokemon_ids):
                            current_location = location
                            current_state = state
                            break
                    if current_location:
                        break

            if current_location and current_state:
                if current_location.locationId not in ctx.locations_checked:
                    block_pokemon_state_items(current_location)
                else:
                    activate_state_friendships(current_location)

    def handle_special_unlock_locations(current_zone: int):
        global LAST_ZONE

        if LAST_ZONE != current_zone:
            BLOCKED_UNLOCKS.clear()
            LAST_ZONE = current_zone

        for item_name, item_data in SPECIAL_UNLOCK_LOCATIONS.items():
            for location in item_data.locations:
                if location.locationId not in ctx.locations_checked:
                    if (location.zone_id == current_zone or
                            (current_zone in LOADSCREEN_TO_ZONE and
                             location.zone_id == LOADSCREEN_TO_ZONE[
                                 current_zone])):
                        if item_name not in BLOCKED_UNLOCKS:
                            BLOCKED_UNLOCKS.append(item_name)
                            write_memory(dme, item_data.item, 0x0)
                else:
                    if item_name in BLOCKED_UNLOCKS:
                        BLOCKED_UNLOCKS.remove(item_name)

    async def _sub():
        if not dme.is_hooked():
            return

        stage_id = dme.read_word(stage_id_address)
        if not stage_id in valid_stage_ids:
            return
        is_in_menu = dme.read_byte(is_in_menu_address)
        pokemon_id = dme.read_word(pokemon_id_address)

        handle_special_unlock_locations(stage_id)

        handle_prisma_overwrites(stage_id)

        handle_pokemon_location_states(stage_id, is_in_menu, pokemon_id)

    while not ctx.exit_event.is_set():
        try:
            if not dme.is_hooked():
                dme.hook()
            else:
                await _sub()
        except Exception as e:
            logger.error(f"Error in location_state_watcher: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")

        await asyncio.sleep(delay_seconds)
