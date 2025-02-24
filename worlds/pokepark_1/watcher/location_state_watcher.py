import asyncio
import traceback

import dolphin_memory_engine as dme

from CommonClient import logger
from worlds.pokepark_1.adresses import stage_id_address, is_in_menu_address, pokemon_id_address, \
    blocked_unlock_itemIds, prisma_blocked_itemIds, \
    UNLOCKS, PRISMAS, PrismaItem, POKEMON_STATES, blocked_friendship_itemIds, blocked_friendship_unlock_itemIds, \
    PokemonStateInfo
from worlds.pokepark_1.dme_helper import write_memory, read_memory

empty_pokemon_id = 0x00

delay_seconds = 0.5

original_values = {}  # {address: value}


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

    def handle_prisma_overwrites(stage_id):
        current_prisma = next((prisma for prisma in PRISMAS.values() if prisma.stage_id == stage_id), None)

        if current_prisma is None:
            restore_original_prisma_values()
            return

        if current_prisma.locationId not in ctx.checked_locations:
            set_state_for_unchecked_prisma_location(current_prisma)

        if current_prisma.locationId in ctx.checked_locations:
            set_state_for_checked_prisma_location(current_prisma)

    def activate_state_friendships(state: PokemonStateInfo):
        if state.friendship_items_to_block:
            for item_id in state.friendship_items_to_block:
                blocked_friendship_itemIds.append(item_id)
                item = POKEMON_STATES[item_id].item
                if item.final_address not in original_values:
                    original_values[item.final_address] = read_memory(dme,item)
                write_memory(dme,item, item.value)

    def block_pokemon_state_items(state: PokemonStateInfo):
        if state.friendship_items_to_block:
            for item_id in state.friendship_items_to_block:
                if item_id not in blocked_friendship_itemIds:
                    blocked_friendship_itemIds.append(item_id)
                    item = POKEMON_STATES[item_id].item
                    if item.final_address not in original_values:
                        original_values[item.final_address] = read_memory(dme,item)
                    write_memory(dme,item, 0x0)

        if state.unlock_items_to_block:
            for item_id in state.unlock_items_to_block:
                if item_id not in blocked_friendship_unlock_itemIds:
                    blocked_friendship_unlock_itemIds.append(item_id)
                    item = UNLOCKS[item_id].item
                    if item.final_address not in original_values:
                        original_values[item.final_address] = read_memory(dme,item)
                    write_memory(dme,item, 0x0)

    def restore_blocked_items():
        for item_id in blocked_friendship_itemIds[:]:
            item = POKEMON_STATES[item_id].item
            if item.final_address in original_values:
                write_memory(dme,item, original_values[item.final_address])
                del original_values[item.final_address]
        blocked_friendship_itemIds.clear()

        for item_id in blocked_friendship_unlock_itemIds[:]:
            item = UNLOCKS[item_id].item
            if item.final_address in original_values:
                write_memory(dme,item, original_values[item.final_address])
                del original_values[item.final_address]
        blocked_friendship_unlock_itemIds.clear()

    def handle_pokemon_location_states(stage_id: int, is_in_menu: bool, pokemon_id: int):

        if pokemon_id == empty_pokemon_id:
            restore_blocked_items()

            if not is_in_menu == 0x01:
                for pokemon_state in POKEMON_STATES.values():
                    if (pokemon_state.zone_id == stage_id and
                            pokemon_state.is_special_exception and
                            pokemon_state.locationId not in ctx.checked_locations):
                        block_pokemon_state_items(pokemon_state)
        else:
            current_state = next(
                (state for state in POKEMON_STATES.values()
                 if state.zone_id == stage_id and state.pokemon_ids
                 and pokemon_id in state.pokemon_ids),
                None
            )

            if current_state:
                if current_state.locationId not in ctx.checked_locations:
                    block_pokemon_state_items(current_state)
                else:
                    activate_state_friendships(current_state)

    async def _sub():
        if not dme.is_hooked():
            return

        for location_id in ctx.checked_locations:
            if location_id in blocked_unlock_itemIds:
                blocked_unlock_itemIds.remove(location_id)

        stage_id = dme.read_word(stage_id_address)
        is_in_menu = dme.read_byte(is_in_menu_address)
        pokemon_id = dme.read_word(pokemon_id_address)

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

            raise
        await asyncio.sleep(delay_seconds)
