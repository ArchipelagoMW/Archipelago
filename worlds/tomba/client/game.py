import asyncio

from CommonClient import logger

from worlds.tomba import constants
from worlds.tomba.client import retroarch
from worlds.tomba.items import ITEMS, GAME_ID_TO_ITEM

CORE_TYPE = "playstation"


class TombaException(Exception):
    pass


class TombaGame:
    """Interface with the game itself"""

    playstation: retroarch.RetroArch

    def __init__(self, retroarch_address="127.0.0.1", retroarch_port=55355):
        self.retroarch_address = retroarch_address
        self.retroarch_port = retroarch_port
        self.should_reset_auth = False
        self.auth = None

    async def wait_for_retroarch_connection(self):
        logger.info("Waiting on connection to Retroarch...")
        self.playstation = retroarch.RetroArch(self.retroarch_address, self.retroarch_port)

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

    async def wait_for_game_ready(self):
        logger.info("Waiting on game to be in valid state...")
        while not await self.check_safe_gameplay():
            if self.should_reset_auth:
                self.should_reset_auth = False
                raise TombaException("Resetting due to wrong archipelago server")

            await asyncio.sleep(1.0)
        logger.info("Game connection ready!")

    async def check_safe_gameplay(self):
        game_state = (await self.playstation.async_read_memory(constants.GAME_STATE_ADDRESS))[0]
        return game_state == constants.GAME_PLAYING

    async def main_tick(self):
        # inventory = await self.get_inventory()
        # logger.debug(inventory)
        pass

    async def get_inventory_counter(self) -> int:
        return (await self.playstation.async_read_memory(constants.INVENTORY_COUNTER_ADDRESS))[0]

    async def get_inventory_stack(self) -> bytearray:
        return await self.playstation.read_memory_block(
            constants.INVENTORY_STACK_ADDRESS, constants.INVENTORY_STACK_SIZE
        )

    async def get_item_amount(self, game_id: int) -> int:
        return (await self.playstation.async_read_memory(constants.INVENTORY_ITEM_AMOUNT_ADDRESS + game_id))[0]

    async def get_inventory(self) -> list[dict]:
        inventory = []
        inventory_stack = await self.get_inventory_stack()
        inventory_counter = await self.get_inventory_counter()

        item_processed = 0

        for i in range(0, constants.INVENTORY_STACK_SIZE, 4):
            game_id = inventory_stack[i]

            item_object = GAME_ID_TO_ITEM.get(game_id)
            if item_object:
                inventory.append(item_object)

            item_processed += 1
            if item_processed >= inventory_counter:
                return inventory

        return inventory

    async def receive_item(self, id, player) -> bool:
        if not await self.check_safe_gameplay():
            return False

        inventory_stack = await self.get_inventory_stack()
        inventory_counter = await self.get_inventory_counter()

        # Item stack is limited
        if inventory_counter >= 0xFF:
            logger.warning("Player has too much items: Cannot receive more items")
            return False

        if id >= len(ITEMS):
            logger.warning(f"Received an unknown item from {player}: ID is {id}")
            return True

        # Fetch the correct item
        item = ITEMS[id]

        game_id = item.get("game_id", None)
        if game_id is None:
            logger.warning(f"Received an item with no known game_id from {player}: ID is {id}")
            return True

        has_item_already = game_id.to_bytes() in inventory_stack[:inventory_counter]
        should_display_acquired = False

        if item.get("has_quantity", False):
            current_amount = await self.get_item_amount(game_id)
            has_item_already = has_item_already or current_amount > 0

            new_amount = current_amount + 1
            self.playstation.write_memory(constants.INVENTORY_ITEM_AMOUNT_ADDRESS + game_id, new_amount.to_bytes())

            should_display_acquired = True

        if not has_item_already:
            # Adding an item means shifting the whole stack to the right
            # and putting the item at the first position
            inventory_stack = game_id.to_bytes() + inventory_stack[:-1]
            inventory_counter += 1

            self.playstation.write_memory(constants.INVENTORY_STACK_ADDRESS, inventory_stack)
            self.playstation.write_memory(constants.INVENTORY_COUNTER_ADDRESS, inventory_counter.to_bytes())

            should_display_acquired = True

        if should_display_acquired:
            logger.info(f"Received {item["name"]} from {player}")

        return True
