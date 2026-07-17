import asyncio

from CommonClient import logger

from .. import constants
from ..constants import (
    EventStatus,
    GameState,
    HudState,
    MenuState,
    SFX,
    CustomCommand,
    Addresses,
    Events,
)
from ..client import retroarch
from ..items import ItemHandler
from ..events import EventHandler
from .patcher import Patcher

CORE_TYPE = "playstation"


class TombaException(Exception):
    pass


class TombaGame:
    """Interface with the game itself"""

    playstation: retroarch.RetroArch
    area_id: int
    section_id: int

    def __init__(self, retroarch_address="127.0.0.1", retroarch_port=55355):
        self.retroarch_address = retroarch_address
        self.retroarch_port = retroarch_port
        self.should_reset_auth = False
        self.auth = None
        self.status = GameState.UNKNOWN
        self.area_id: int = 0
        self.section_id: int = 0

    async def wait_for_retroarch_connection(self):
        logger.info("Waiting on connection to Retroarch...")
        self.playstation = retroarch.RetroArch(self.retroarch_address, self.retroarch_port)
        self.patcher = Patcher(self.playstation)

        while True:
            try:
                version = await self.playstation.get_retroarch_version()
                status, core_type, rom_name, _ = await self.playstation.get_retroarch_status()

                if retroarch.is_connected(status) and core_type == CORE_TYPE:
                    break
            except (BlockingIOError, TimeoutError, ConnectionResetError):
                await asyncio.sleep(1.0)
                pass

            await asyncio.sleep(1.0)

        logger.info(f"Connected to Retroarch {version} running {rom_name}")

    async def perform_auth(self):
        """Reads the username patched into the ROM for authentication"""
        auth = "T4g1"  # TODO
        self.auth = auth

    # --------
    # Custom feature patched into the RAM
    # --------

    def play_sfx(self, sfx_id: int):
        logger.debug(f"Playing SFX {sfx_id}")
        self.playstation.write_memory(Addresses.PLAY_SFX, sfx_id.to_bytes())

    async def show_message(self, code: int):
        logger.debug(f"Display message: {code:04x}")
        self.playstation.write_memory(Addresses.MESSAGE, code.to_bytes(2))
        await self.set_command(CustomCommand.SHOW_MESSAGE)

    async def get_command(self, command_mask=0xFF) -> int:
        command = (await self.playstation.async_read_memory(Addresses.CUSTOM_COMMAND))[0]
        return command & command_mask

    async def set_command(self, command_mask):
        command = await self.get_command()
        command |= command_mask

        self.playstation.write_memory(Addresses.CUSTOM_COMMAND, command.to_bytes())

    async def request_clear_obtained_items(self):
        await self.set_command(CustomCommand.CLEAR_STACK)

    async def has_pending_clear_obtained_items(self) -> bool:
        return bool(await self.get_command(CustomCommand.CLEAR_STACK))

    async def get_saved_archipelago_index(self) -> int | None:
        """Give saved last index of item received from Archipelago.

        Returns:
            int: The last successfully processed item index.
            None: If we can't read it yet (not patched or emulator issue)
        """
        if not await self.patcher.is_patched():
            return None

        # Assumes Tomba! set this to zero at game start
        stored_index = await self.playstation.read_memory_block(Addresses.ARCHIPELAGO_RECEIVED_INDEX, 2)
        return int.from_bytes(stored_index, byteorder="big")

    def set_saved_archipelago_index(self, index):
        index = index.to_bytes(2, byteorder="big")
        self.playstation.write_memory(Addresses.ARCHIPELAGO_RECEIVED_INDEX, index)

    # --------
    # Handle in game inventory
    # --------

    async def get_inventory_counter(self) -> int:
        return (await self.playstation.async_read_memory(Addresses.INVENTORY_COUNTER))[0]

    async def get_inventory_stack(self) -> bytearray:
        return await self.playstation.read_memory_block(Addresses.INVENTORY_STACK, constants.INVENTORY_STACK_SIZE)

    async def get_item_amount(self, game_id: int) -> int:
        return (await self.playstation.async_read_memory(Addresses.INVENTORY_ITEM_AMOUNT + game_id))[0]

    async def get_inventory(self) -> list[dict]:
        inventory = []
        inventory_stack = await self.get_inventory_stack()
        inventory_counter = await self.get_inventory_counter()

        item_processed = 0

        for i in range(0, constants.INVENTORY_STACK_SIZE, 4):
            game_id = inventory_stack[i]
            item = ItemHandler.by_game_id.get(game_id, None)
            if item is not None:
                inventory.append(item)

            item_processed += 1
            if item_processed >= inventory_counter:
                return inventory

        return inventory

    # --------
    # Handle in game received items
    # --------

    async def get_found_items_counter(self) -> int:
        return (await self.playstation.async_read_memory(Addresses.FOUND_ITEMS_STACK_SIZE))[0]

    async def get_found_items_stack(self) -> bytearray:
        size = await self.get_found_items_counter()
        return await self.playstation.read_memory_block(Addresses.FOUND_ITEMS_STACK, size)

    async def get_pending_found_items(self) -> list[int] | None:
        """Give list of found items from the game.

        Returns:
            list[int]: The list of item collected by the player.
            None: If we can't read it yet (not patched or emulator issue)
        """
        if not await self.patcher.is_patched():
            return None

        if await self.has_pending_clear_obtained_items():
            # Wait until the emulator has cleared the stack before processing it again
            return []

        item_stack = await self.get_found_items_stack()
        return list(item_stack)

    # --------
    # Handle victory conditions
    # --------

    async def is_victory(self):
        return (await self.get_event_state(Events.INSIDE_THE_KOKKA_EGGS)) == EventStatus.CLEARED

    async def get_event_state(self, event_name: str) -> EventStatus:
        event = EventHandler.by_name[event_name]

        events_states = await self.playstation.read_memory_block(Addresses.EVENT_FLAGS, 0xFF)
        return events_states[event.id]

    async def receive_item(self, item_id: int, player) -> bool:
        """Give iem to the player

        Returns:
            True: The player now owns the item or the item is impossible to give to the player
            False: The item has not been given and should be retried (game is not ready to receive items)
        """
        if not self.check_safe_gameplay():
            return False

        inventory_counter = await self.get_inventory_counter()

        # Item stack is limited
        if inventory_counter >= 0xFF:
            logger.warning("Player has too much items: Cannot receive more items")
            return False

        item = ItemHandler.by_id.get(item_id, None)
        if item is None:
            logger.warning(f"Received an unknown item from {player}: ID is {item_id}")
            return True

        inventory_stack = await self.get_inventory_stack()

        has_item_already = item.game_id.to_bytes() in inventory_stack[:inventory_counter]
        should_display_acquired = False

        if item.countable:
            current_amount = await self.get_item_amount(item.game_id)
            has_item_already = has_item_already or current_amount > 0

            new_amount = current_amount + 1
            self.playstation.write_memory(Addresses.INVENTORY_ITEM_AMOUNT + item.game_id, new_amount.to_bytes())

            should_display_acquired = True

        if not has_item_already:
            # Adding an item means shifting the whole stack to the right
            # and putting the item at the first position
            inventory_stack = item.game_id.to_bytes() + inventory_stack[:-1]
            inventory_counter += 1

            self.playstation.write_memory(Addresses.INVENTORY_STACK, inventory_stack)
            self.playstation.write_memory(Addresses.INVENTORY_COUNTER, inventory_counter.to_bytes())

            should_display_acquired = True

        if should_display_acquired:
            logger.debug(f"Received {item.name} from {player}")

            self.play_sfx(SFX.ACQUIRED)

        return True

    async def get_menu_state(self):
        return (await self.playstation.async_read_memory(Addresses.MENU_STATE))[0]

    async def is_hud_visible(self):
        hud_visibility = (await self.playstation.async_read_memory(Addresses.HUD_VISIBILITY))[0]
        hud_visibility_timer = (await self.playstation.async_read_memory(Addresses.HUD_VISIBILITY_TIMER))[0]

        return hud_visibility == HudState.VISIBLE and hud_visibility_timer == HudState.VISIBLE

    async def update_status(self):
        if await self.get_menu_state() == MenuState.OPEN:
            self.status = GameState.IN_MENU
        # TODO: Check credit shown too ?
        elif await self.is_hud_visible():
            self.status = GameState.PLAYING
        else:
            self.status = GameState.CUTSCENE

    async def update_area_and_section(self):
        self.area_id = (await self.playstation.async_read_memory(Addresses.SELECTED_AREA))[0]
        self.section_id = (await self.playstation.async_read_memory(Addresses.SELECTED_SECTION))[0]

    def check_safe_gameplay(self):
        return self.status == GameState.PLAYING

    async def main_tick(self, win_callback):
        if self.should_reset_auth:
            self.should_reset_auth = False
            raise TombaException("Resetting due to wrong archipelago server")

        await self.update_status()
        await self.update_area_and_section()

        if not await self.patcher.is_save_patched():
            await self.patcher.patch_save()

        if not self.check_safe_gameplay():
            return

        if not await self.patcher.is_patched():
            await self.patcher.patch_game()

        if await self.is_victory():
            await win_callback()
