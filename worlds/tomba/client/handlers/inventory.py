from asyncio import Lock

from CommonClient import logger

from . import AbstractHandler
from ...constants import SFX, Addresses, Items, GameState
from ...items import ItemHandler, ItemData
from .player import TombaState

INVENTORY_STACK_SIZE = 0xFF
ITEM_MAX_AMOUNT = 99


class Weapons(int):
    BLACKJACK = 0x00
    NOTHING = 0x01
    WOOD_BOOMERANG = 0x05
    STONE_BOOMERANG = 0x06
    IRON_BOOMERANG = 0x07
    GRAPPLE = 0x08
    GRAPPLEJACK = 0x09


class InventoryHandler(AbstractHandler):
    """Manages in game inventory"""

    inventory_stack_size: int = 0

    # Used to list all items Tomba! has received from external means
    given_items: list[ItemData] = []

    lock: Lock = Lock()

    async def give_item(self, item: ItemData):
        self.given_items.append(item)

        await self.update_given_items()

    async def is_accessible(self):
        return (await self.tomba.playstation.async_read_memory(Addresses.INVENTORY_ACCESSIBLE))[0] != 0x00

    async def update_inventory(self):
        """Monitor inventory changes"""
        new_stack_size = await self.get_inventory_counter()

        if await self.tomba.get_status() is GameState.TITLE:
            self.inventory_stack_size = -1
            return

        if self.inventory_stack_size != new_stack_size:
            logger.debug(f"Inventory size changed from {self.inventory_stack_size} to {new_stack_size}")

            self.inventory_stack_size = new_stack_size
            await self.on_inventory_updated()

        await self.update_given_items()

    async def update_given_items(self):
        """Handle given items"""
        async with self.lock:
            if len(self.given_items) > 0:
                item = self.given_items[0]
                if await self.receive_item(item):
                    self.given_items.pop(0)

    async def on_inventory_updated(self):
        # Assume its the start of a new game if not checked locations
        if len(self.ctx.sent_checks) > 0:
            return

        # Check if this is enabled
        if not self.ctx.slot_data["keep_blackjack"]:
            logger.debug("Removing starting Blackjack")

            blackjack = ItemHandler.by_name[Items.BLACKJACK]
            await self.tomba.inventory_handler.remove_item(blackjack)
            await self.tomba.inventory_handler.equip_weapon(Weapons.NOTHING)

    async def get_inventory_counter(self) -> int:
        return (await self.tomba.playstation.async_read_memory(Addresses.INVENTORY_COUNTER))[0]

    async def get_inventory_stack(self) -> bytearray:
        return await self.tomba.playstation.read_memory_block(Addresses.INVENTORY_STACK, INVENTORY_STACK_SIZE)

    async def get_item_amount(self, game_id: int) -> int:
        return (await self.tomba.playstation.async_read_memory(Addresses.INVENTORY_ITEM_AMOUNT + game_id))[0]

    async def set_item_amount(self, game_id: int, amount: int):
        amount = max(0, min(amount, 99))

        await self.tomba.playstation.write_memory(Addresses.INVENTORY_ITEM_AMOUNT + game_id, amount.to_bytes())

    async def get_inventory(self) -> list[dict]:
        inventory = []
        inventory_stack = await self.get_inventory_stack()
        inventory_counter = await self.get_inventory_counter()

        item_processed = 0

        for i in range(0, INVENTORY_STACK_SIZE, 4):
            game_id = inventory_stack[i]
            item = ItemHandler.by_game_id.get(game_id, None)
            if item is not None:
                inventory.append(item)

            item_processed += 1
            if item_processed >= inventory_counter:
                return inventory

        return inventory

    async def receive_item(self, item: ItemData, player: int | None = None) -> bool:
        """Give iem to the player

        Returns:
            True: The player now owns the item or the item is impossible to give to the player
            False: The item has not been given and should be retried (game is not ready to receive items)
        """
        if not await self.tomba.is_playing():
            return False

        # Special items handling
        if item.game_id >= 0xA0:
            return await self.receive_special(item, player)

        inventory_counter = await self.get_inventory_counter()

        # Item stack is limited
        if inventory_counter >= 0xFF:
            logger.warning("Player has too much items: Cannot receive more items")
            return False

        inventory_stack = await self.get_inventory_stack()

        has_item_already = item.game_id.to_bytes() in inventory_stack[:inventory_counter]
        should_display_acquired = False

        new_amount = 1
        if item.countable:
            current_amount = await self.get_item_amount(item.game_id)
            has_item_already = has_item_already or current_amount > 0

            if current_amount < ITEM_MAX_AMOUNT:
                new_amount = current_amount + 1

            should_display_acquired = True

        if item.record_amount:
            await self.set_item_amount(item.game_id, new_amount)

        if not has_item_already:
            # Adding an item means shifting the whole stack to the right
            # and putting the item at the first position
            inventory_stack = item.game_id.to_bytes() + inventory_stack[:-1]

            if inventory_counter != await self.get_inventory_counter():
                logger.warning("Player inventory changed while adding the item, aborting...")
                return False

            inventory_counter += 1

            await self.tomba.playstation.write_memory(Addresses.INVENTORY_STACK, inventory_stack)
            await self.tomba.playstation.write_memory(Addresses.INVENTORY_COUNTER, inventory_counter.to_bytes())

            should_display_acquired = True

        if should_display_acquired:
            await self.notify_acquired(item, player)

        await self.tomba.pickup_handler.handle(item.name)

        return True

    async def notify_acquired(self, item: ItemData, player: int | None):
        message = f"Found {item.name}"
        if player is not None and self.ctx.slot != player:
            player_name = self.ctx.player_names[player]
            message = f"{player_name} sent {item.name}"

        logger.debug(message)
        await self.tomba.message_handler.print(message)
        await self.tomba.play_sfx(SFX.ACQUIRED)

    async def remove_item(self, item: ItemData, amount: int = 1):
        inventory_counter = await self.get_inventory_counter()
        inventory_stack = await self.get_inventory_stack()
        current_amount = await self.get_item_amount(item.game_id)

        new_amount = max(current_amount - amount, 0)
        await self.tomba.playstation.write_memory(Addresses.INVENTORY_ITEM_AMOUNT + item.game_id, new_amount.to_bytes())

        if new_amount == 0:
            for index in range(inventory_counter):
                if inventory_stack[index] == item.game_id:
                    del inventory_stack[index]
                    inventory_counter -= 1
                    break

            await self.tomba.playstation.write_memory(Addresses.INVENTORY_STACK, inventory_stack)
            await self.tomba.playstation.write_memory(Addresses.INVENTORY_COUNTER, inventory_counter.to_bytes())

    async def equip_weapon(self, weapon: int):
        await self.tomba.playstation.write_memory(Addresses.TOMBA_WEAPON, weapon.to_bytes())

    async def receive_special(self, item: ItemData, player: int | None = None) -> bool:
        if item.name == Items.ONE_UP:
            await self.tomba.player_handler.add_life()

        elif item.name == Items.MAX_VITALITY_1:
            await self.tomba.player_handler.add_vitality()

        elif item.name == Items.HEAL:
            await self.tomba.player_handler.heal()

        elif item.name == Items.LAUGH:
            await self.tomba.player_handler.set_status(TombaState.LAUGHING)

        elif item.name == Items.CRY:
            await self.tomba.player_handler.set_status(TombaState.CRYING)

        await self.notify_acquired(item, player)

        return True
