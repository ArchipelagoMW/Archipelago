from __future__ import annotations
import asyncio
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .client import TombaContext

from CommonClient import logger

from ..constants import (
    GameState,
    HudState,
    MenuState,
    EventStatus,
    Addresses,
    GameState1,
    GameState3,
    Regions,
    CustomCommand,
)
from .handlers.inventory import InventoryHandler
from .handlers.pickup import PickupHandler
from .handlers.warp import WarpHandler
from .handlers.transition import TransitionHandler
from .handlers.events import EventsHandler
from .handlers.door import DoorHandler
from .handlers.message import MessageHandler
from .handlers.player import PlayerHandler
from .emulators.emulator import Emulator, CORE_TYPE, EmulatorStatus
from .emulators.retroarch import RetroArch
from .emulators.bizhawk import BizHawk
from ..sections import Sections, Section
from ..events import EventData
from .patcher import Patcher


class TombaException(Exception):
    pass


class TombaGame:
    """Interface with the game itself"""

    ctx: TombaContext
    patcher: Patcher
    playstation: Emulator
    section: Section

    inventory_handler: InventoryHandler
    pickup_handler: PickupHandler
    warp_hanlder: WarpHandler
    events_handler: EventsHandler
    doors_handler: DoorHandler
    transition_handler: TransitionHandler

    def __init__(self, ctx: TombaContext, emulator_address="127.0.0.1", emulator_port=55355):
        self.ctx = ctx

        self.emulator_address = emulator_address
        self.emulator_port = emulator_port
        self.should_reset_auth = False

        self.status = GameState.UNKNOWN
        self.section: Section = Section(0xFF, 0xFF)

        self.playstation: Emulator

        self.should_update_entrances = False

        self.inventory_handler = InventoryHandler(self.ctx, self)
        self.pickup_handler = PickupHandler(self.ctx, self)
        self.warp_hanlder = WarpHandler(self.ctx, self)
        self.events_handler = EventsHandler(self.ctx, self)
        self.doors_handler = DoorHandler(self.ctx, self)
        self.message_handler = MessageHandler(self.ctx, self)
        self.player_handler = PlayerHandler(self.ctx, self)
        self.transition_handler = TransitionHandler(self.ctx, self)

    async def wait_for_emulator_connection(self):
        logger.info("Waiting on connection to emulator...")

        emulator: Emulator | None = None
        while True:
            if emulator is None:
                if hasattr(self.ctx, "slot_data"):
                    if self.ctx.slot_data["emulator"] is RetroArch.ID:
                        emulator = RetroArch(self.emulator_address, self.emulator_port)
                    else:
                        emulator = BizHawk(self.emulator_address, self.emulator_port)
            else:
                try:
                    if not await emulator.connect():
                        continue

                    version = await emulator.get_version()
                    status, core_type, rom_name, _ = await emulator.get_status()

                    if (status == EmulatorStatus.PAUSED or status == EmulatorStatus.PLAYING) and core_type == CORE_TYPE:
                        break
                except (BlockingIOError, TimeoutError, ConnectionResetError):
                    await asyncio.sleep(1.0)

            await asyncio.sleep(1.0)

        self.playstation = emulator
        self.patcher = Patcher(emulator)
        logger.info(f"Connected to {emulator.name} version {version} running {rom_name}")

    async def play_sfx(self, sfx_id: int):
        await self.playstation.write_memory(Addresses.PLAY_SFX, sfx_id.to_bytes())

    async def set_music(self, music_id: int):
        await self.playstation.write_memory(Addresses.PARAM_A0, music_id.to_bytes())
        await self.set_command(CustomCommand.SET_MUSIC)

    async def show_event(self, event: EventData, status: EventStatus):
        is_cleared = status == EventStatus.CLEARED
        await self.message_handler.print_event(event.name, is_cleared)

    async def get_command(self, command_mask=0xFF) -> int:
        command = (await self.playstation.async_read_memory(Addresses.CUSTOM_COMMAND))[0]
        return command & command_mask

    async def set_command(self, command_mask):
        command = await self.get_command()
        command |= command_mask

        await self.playstation.write_memory(Addresses.CUSTOM_COMMAND, command.to_bytes())

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

    async def set_saved_archipelago_index(self, index):
        index = index.to_bytes(2, byteorder="big")
        await self.playstation.write_memory(Addresses.ARCHIPELAGO_RECEIVED_INDEX, index)

    async def get_ap_score(self):
        ap_score_raw = await self.playstation.read_memory_block(Addresses.AP_SCORE, 4)
        return int.from_bytes(ap_score_raw, byteorder="little")

    async def set_ap_score(self, value: int):
        await self.playstation.write_memory(Addresses.AP_SCORE, value.to_bytes(4, byteorder="little"))

    async def get_menu_state(self):
        return (await self.playstation.async_read_memory(Addresses.MENU_STATE))[0]

    async def get_game_state_1(self) -> GameState1:
        state_raw = (await self.playstation.async_read_memory(Addresses.GAME_STATE_1))[0]

        try:
            return GameState1(state_raw)
        except Exception:
            return GameState1.TITLE_SCREEN

    async def get_game_state_3(self) -> GameState3:
        state_raw = (await self.playstation.async_read_memory(Addresses.GAME_STATE_3))[0]

        try:
            return GameState3(state_raw)
        except Exception:
            return GameState3.LOADING

    async def is_hud_visible(self):
        hud_visibility = (await self.playstation.async_read_memory(Addresses.HUD_VISIBILITY))[0]
        hud_visibility_timer = (await self.playstation.async_read_memory(Addresses.HUD_VISIBILITY_TIMER))[0]

        return hud_visibility == HudState.VISIBLE and hud_visibility_timer == HudState.VISIBLE

    async def is_playing(self):
        status = await self.get_status()
        return status == GameState.PLAYING or status == GameState.NO_HUD

    async def is_in_menu(self):
        status = await self.get_status()
        return status == GameState.IN_MENU

    async def has_game_in_progress(self):
        status = await self.get_status()
        return status == GameState.IN_MENU or status == GameState.PLAYING or status == GameState.NO_HUD

    async def patch_game(self):
        await self.patcher.patch_game()

        status = await self.get_status()
        if status == GameState.IN_MENU:
            await self.check_inventory_patch()

    async def check_inventory_patch(self):
        # Patch only if the menu is fully loaded
        if not await self.is_in_menu():
            return

        if (await self.playstation.async_read_memory(Addresses.GAME_STATE_4))[0] != 0x03:
            return

        # Fix Yan's Lunch Box
        await self.patcher.patch_inventory_yans_lunch_box()

        # Fix Flower Tears
        if await self.patcher.is_inventory_flower_tears_patched():
            return

        # Patch only if its unpurified
        if self.section != Sections.CHARITY_SQUARE or await self.warp_hanlder.is_purified(
            Regions.FOREST_OF_100_FLOWERS
        ):
            return

        await self.patcher.patch_inventory_flower_tears()

    async def get_status(self) -> GameState:
        """Called when needed in order to always have the most updated status"""
        state_1 = await self.get_game_state_1()
        status = GameState.UNKNOWN

        if state_1 == GameState1.GAME_SCREEN:
            state_3 = await self.get_game_state_3()
            if state_3 == GameState3.LOADING:
                status = GameState.LOADING
            elif await self.get_menu_state() == MenuState.OPEN:
                status = GameState.IN_MENU
            elif await self.is_hud_visible():
                status = GameState.PLAYING
            elif await self.inventory_handler.is_accessible():
                status = GameState.NO_HUD
            else:
                status = GameState.CUTSCENE
        elif state_1 == GameState1.OPTION_SCREEN:
            status = GameState.OPTIONS
        elif state_1 == GameState1.TRAILER_SCREEN or state_1 == GameState1.TITLE_SCREEN:
            status = GameState.TITLE

        return status

    async def update_section(self):
        area_id = (await self.playstation.async_read_memory(Addresses.SELECTED_AREA))[0]
        section_id = (await self.playstation.async_read_memory(Addresses.SELECTED_SECTION))[0]
        new_section = Section(area_id, section_id)

        if new_section != self.section:
            old_section = self.section
            self.section = new_section
            logger.debug(f"Player is now entering: {self.section}")

            self.should_update_entrances = True

            await self.warp_hanlder.handle_leaving(old_section, to=self.section)
            await self.warp_hanlder.handle(self.section, coming_from=old_section)

        if self.should_update_entrances and await self.has_game_in_progress():
            await self.transition_handler.update_transitions(new_section)
            self.should_update_entrances = False

    async def update_events(self):
        await self.events_handler.update_events()

    async def update_inventory(self):
        """Checks modification to the player inventory and
        tries to give items manually added"""
        await self.inventory_handler.update_inventory()

    async def update_messages(self):
        await self.message_handler.update_messages()

    async def update_deathlink(self):
        await self.player_handler.update_deathlink()

    async def keep_alive(self):
        """Raise error if the emulator is no longer working"""
        await self.playstation.keep_alive()
