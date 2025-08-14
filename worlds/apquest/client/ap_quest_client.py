# isort: off
from argparse import Namespace

from kvui import GameManager
# isort: on

import asyncio
import sys
from collections.abc import Sequence
from enum import Enum
from typing import Any

import colorama
from CommonClient import CommonContext, get_base_parser, gui_enabled, handle_url_arg, logger, server_loop
from NetUtils import ClientStatus, NetworkItem

from worlds.apquest.apquest.items import Item
from worlds.apquest.client.game_manager import APQuestManager

from ..apquest.events import ConfettiFired, LocationClearedEvent, VictoryEvent
from ..apquest.game import Game, Input
from ..apquest.locations import LOCATION_NAME_TO_ID, Location
from .graphics import PlayerSprite
from .item_quality import get_quality_for_network_item
from .sounds import CONFETTI_CANNON, ITEM_JINGLES, VICTORY_JINGLE


class ConnectionStatus(Enum):
    NOT_CONNECTED = 0
    SCOUTS_NOT_SENT = 1
    SCOUTS_SENT = 2
    GAME_RUNNING = 3


class APQuestContext(CommonContext):
    game = "APQuest"
    items_handling = 0b111  # full remote

    client_loop: asyncio.Task[None]

    last_connected_slot: int | None = None

    slot_data: dict[str, Any]
    location_to_item: dict[int, NetworkItem]

    ap_quest_game: Game | None = None
    hard_mode: bool = False
    player_sprite: PlayerSprite = PlayerSprite.HUMAN

    connection_status: ConnectionStatus = ConnectionStatus.NOT_CONNECTED

    highest_processed_item_index: int = 0
    queued_locations: list[int]

    ui: APQuestManager

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.queued_locations = []
        self.slot_data = {}
        self.location_to_item = {}

    async def server_auth(self, password_requested: bool = False) -> None:
        await super().server_auth(password_requested)
        await self.get_username()
        await self.send_connect(game=self.game)

    async def apquest_loop(self) -> None:
        while not self.exit_event.is_set():
            if self.connection_status != ConnectionStatus.GAME_RUNNING:
                if self.connection_status == ConnectionStatus.SCOUTS_NOT_SENT:
                    await self.send_msgs([{"cmd": "LocationScouts", "locations": list(LOCATION_NAME_TO_ID.values())}])
                    self.connection_status = ConnectionStatus.SCOUTS_SENT

                await asyncio.sleep(0.1)
                continue

            if not self.ap_quest_game or not self.ap_quest_game.gameboard or not self.ap_quest_game.gameboard.ready:
                await asyncio.sleep(0.1)
                continue

            try:
                while self.queued_locations:
                    location = self.queued_locations.pop(0)
                    self.location_checked_side_effects(location)
                    self.locations_checked.add(location)
                    await self.check_locations({location})

                rerender = False

                new_items = self.items_received[self.highest_processed_item_index :]
                for item in new_items:
                    self.highest_processed_item_index += 1
                    self.ap_quest_game.receive_item(item.item, item.location, item.player)
                    rerender = True

                for new_remotely_cleared_location in self.checked_locations - self.locations_checked:
                    self.ap_quest_game.force_clear_location(new_remotely_cleared_location)
                    rerender = True

                if rerender:
                    self.render()

                if self.ap_quest_game.player.has_won and not self.finished_game:
                    await self.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                    self.finished_game = True
            except Exception as e:
                logger.exception(e)

            await asyncio.sleep(0.1)

    def on_package(self, cmd: str, args: dict) -> None:
        if cmd == "Connected":
            if self.connection_status == ConnectionStatus.GAME_RUNNING:
                # In a connection loss -> auto reconnect scenario, we can seamlessly keep going
                return

            self.last_connected_slot = self.slot

            self.connection_status = ConnectionStatus.NOT_CONNECTED  # for safety, it will get set again later

            self.location_to_item = {}
            self.slot_data = args["slot_data"]
            self.hard_mode = self.slot_data["hard_mode"]
            try:
                self.player_sprite = PlayerSprite(self.slot_data["player_sprite"])
            except Exception as e:
                logger.exception(e)
                self.player_sprite = PlayerSprite.UNKNOWN

            self.ap_quest_game = Game(self.hard_mode)
            self.highest_processed_item_index = 0
            self.render()

            self.connection_status = ConnectionStatus.SCOUTS_NOT_SENT
        if cmd == "LocationInfo":
            self.location_to_item.update({network_item.location: network_item for network_item in args["locations"]})

            remote_item_graphic_overrides = {
                Location(location): Item(network_item.item)
                for location, network_item in self.location_to_item.items()
                if self.slot_info[network_item.player].game == self.game
            }

            assert self.ap_quest_game is not None
            self.ap_quest_game.gameboard.fill_remote_location_content(remote_item_graphic_overrides)
            self.render()
            self.ui.game_view.bind_keyboard()

            self.connection_status = ConnectionStatus.GAME_RUNNING
            self.ui.start_background_music()
            self.ui.switch_to_game_tab()

    async def disconnect(self, *args, **kwargs) -> None:
        self.finished_game = False
        self.locations_checked = set()
        self.connection_status = ConnectionStatus.NOT_CONNECTED
        await super().disconnect(*args, **kwargs)

    def render(self) -> None:
        self.ui.render(self.ap_quest_game, self.player_sprite)

    def location_checked_side_effects(self, location: int) -> None:
        network_item = self.location_to_item[location]

        item_quality = get_quality_for_network_item(network_item)
        self.play_jingle(ITEM_JINGLES[item_quality])

    def play_jingle(self, audio_filename: str) -> None:
        self.ui.play_jingle(audio_filename)

    def handle_game_events(self) -> None:
        if self.ap_quest_game is None:
            return

        while self.ap_quest_game.queued_events:
            event = self.ap_quest_game.queued_events.pop(0)

            if isinstance(event, LocationClearedEvent):
                self.queued_locations.append(event.location_id)

            if isinstance(event, VictoryEvent):
                self.play_jingle(VICTORY_JINGLE)

            if isinstance(event, ConfettiFired):
                gameboard_x, gameboard_y = self.ap_quest_game.gameboard.size
                gameboard_x += 1  # vertical item column
                x = (event.x + 0.5) / gameboard_x
                y = 1 - (event.y + 0.5) / gameboard_y  # Kivy's y is bottom to top (ew)

                self.ui.play_jingle(CONFETTI_CANNON)
                self.ui.add_confetti((x, y), (self.slot_data["confetti_explosiveness"] + 1) * 5)

    def input_and_rerender(self, input_key: Input) -> None:
        if self.ap_quest_game is None:
            return
        if not self.ap_quest_game.gameboard.ready:
            return
        self.ap_quest_game.input(input_key)
        self.handle_game_events()
        self.render()

    def make_gui(self) -> type[GameManager]:
        self.load_kv()
        return APQuestManager

    def load_kv(self) -> None:
        import pkgutil

        from kivy.lang import Builder

        data = pkgutil.get_data(__name__, "ap_quest_client.kv").decode()
        Builder.load_string(data)


async def main(args: Namespace) -> None:
    ctx = APQuestContext(args.connect, args.password)
    ctx.auth = args.name
    ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")

    if not gui_enabled:
        raise RuntimeError("APQuest cannot be played without gui.")

    ctx.run_gui()
    ctx.run_cli()

    ctx.client_loop = asyncio.create_task(ctx.apquest_loop(), name="Client Loop")

    await ctx.exit_event.wait()
    await ctx.shutdown()


def launch_client(*args: Sequence[str]) -> None:
    parser = get_base_parser()
    parser.add_argument("--name", default=None, help="Slot Name to connect as.")
    parser.add_argument("url", nargs="?", help="Archipelago connection url")

    launch_args = handle_url_arg(parser.parse_args(args))

    if launch_args.nogui:
        raise RuntimeError("APQuest cannot be played without gui.")

    colorama.just_fix_windows_console()

    asyncio.run(main(launch_args))
    colorama.deinit()


if __name__ == "__main__":
    launch_client(*sys.argv[1:])
