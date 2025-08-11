# isort: off
from kvui import GameManager
# isort: on

import asyncio
import sys
from enum import Enum
from typing import Any

import colorama
from CommonClient import CommonContext, get_base_parser, gui_enabled, handle_url_arg, logger, server_loop
from kivy.core.audio import Sound, SoundLoader
from kivy.core.window import Keyboard, Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.layout import Layout
from kivymd.uix.recycleview import MDRecycleView
from NetUtils import ClientStatus, NetworkItem

from ..apquest.events import LocationClearedEvent, VictoryEvent
from ..apquest.game import Game, Input
from ..apquest.graphics import Graphic
from ..apquest.locations import LOCATION_NAME_TO_ID
from .graphics import IMAGE_GRAPHICS, PLAYER_GRAPHICS, TEXTURES, PlayerSprite
from .item_quality import get_quality_for_network_item
from .sounds import ALL_SOUNDS, ITEM_JINGLES, SOUND_PATHS, VICTORY_JINGLE


class ConnectionStatus(Enum):
    NOT_CONNECTED = 0
    SCOUTS_NOT_SENT = 1
    SCOUTS_SENT = 2
    CONNECTED = 3


class APQuestContext(CommonContext):
    game = "APQuest"
    items_handling = 0b111  # full remote

    client_loop: asyncio.Task[None]

    slot_data: dict[str, Any]
    location_to_item: dict[int, NetworkItem]

    ap_quest_game: Game | None = None
    hard_mode: bool = False
    player_sprite: PlayerSprite = PlayerSprite.HUMAN

    connection_status: ConnectionStatus = ConnectionStatus.NOT_CONNECTED

    highest_processed_item_index: int = 0
    queued_locations: list[int]
    ingame_cleared_locations: set[int]

    top_image_grid: list[list[Image]]

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.top_image_grid = []
        self.queued_locations = []
        self.slot_data = {}
        self.location_to_item = {}
        self.ingame_cleared_locations = set()

    async def server_auth(self, password_requested: bool = False) -> None:
        await super().server_auth(password_requested)
        await self.get_username()
        await self.send_connect(game=self.game)

    async def client_loop(self):
        while not self.exit_event.is_set():
            if self.connection_status != ConnectionStatus.CONNECTED:
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
                    self.ingame_cleared_locations.add(location)
                    await self.check_locations({location})

                rerender = False

                new_items = self.items_received[self.highest_processed_item_index :]
                for item in new_items:
                    self.highest_processed_item_index += 1
                    self.ap_quest_game.receive_item(item.item, item.location, item.player)
                    rerender = True

                for new_remotely_cleared_location in (self.checked_locations - self.ingame_cleared_locations):
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
            self.initial_render()

            self.connection_status = ConnectionStatus.SCOUTS_NOT_SENT
        if cmd == "LocationInfo":
            self.location_to_item.update({network_item.location: network_item for network_item in args["locations"]})

            self.ap_quest_game.gameboard.fill_remote_location_content()
            self.render()
            self.ui.game_view.bind_keyboard()

            self.connection_status = ConnectionStatus.CONNECTED
        if cmd == "Disconnected":
            self.connection_status = ConnectionStatus.NOT_CONNECTED
            self.checked_locations = set()
            self.ingame_cleared_locations = set()
            self.finished_game = False

    async def disconnect(self, *args, **kwargs) -> None:
        self.checked_locations = set()
        self.finished_game = False
        self.connection_status = ConnectionStatus.NOT_CONNECTED
        self.ingame_cleared_locations = set()
        await super().disconnect(*args, **kwargs)

    def initial_render(self):
        if self.ui.upper_game_grid.children:
            return

        self.top_image_grid = []

        for row in self.ap_quest_game.gameboard.gameboard:
            self.top_image_grid.append([])
            for _ in row:
                image = Image(fit_mode="fill", texture=TEXTURES["empty.png"])
                image.texture.mag_filter = "nearest"
                self.ui.lower_game_grid.add_widget(image)

                image2 = Image(fit_mode="fill")

                self.ui.upper_game_grid.add_widget(image2)

                self.top_image_grid[-1].append(image2)

        self.render()

    def render(self):
        for gameboard_row, image_row in zip(self.ap_quest_game.render(), self.top_image_grid, strict=False):
            for graphic, image in zip(gameboard_row, image_row, strict=False):
                if graphic in PLAYER_GRAPHICS:
                    image_name = PLAYER_GRAPHICS[graphic].get(self.player_sprite, IMAGE_GRAPHICS[Graphic.UNKNOWN])
                    if image_name is None:
                        logger.exception(f"Couldn't find player sprite graphics for player sprite {self.player_sprite}")
                else:
                    image_name = IMAGE_GRAPHICS[graphic]

                if image_name is None:
                    image.opacity = 0
                    image.texture = None
                    continue

                image.texture = TEXTURES.get(image_name, TEXTURES[IMAGE_GRAPHICS[Graphic.UNKNOWN]])
                image.texture.mag_filter = "nearest"
                image.opacity = 1

    def location_checked_side_effects(self, location: int):
        network_item = self.location_to_item[location]

        item_quality = get_quality_for_network_item(network_item)
        self.play_audio(ITEM_JINGLES[item_quality])

    def play_audio(self, audio_filename: str) -> None:
        self.ui.play_audio(audio_filename)

    def handle_game_events(self):
        while self.ap_quest_game.queued_events:
            event = self.ap_quest_game.queued_events.pop(0)

            if isinstance(event, LocationClearedEvent):
                self.queued_locations.append(event.location_id)

            if isinstance(event, VictoryEvent):
                self.play_audio(VICTORY_JINGLE)

    def input_and_rerender(self, input_key: Input) -> None:
        if self.ap_quest_game is None:
            return
        if not self.ap_quest_game.gameboard.ready:
            return
        self.ap_quest_game.input(input_key)
        self.handle_game_events()
        self.render()

    def make_gui(self) -> type[GameManager]:
        ui = super().make_gui()

        class APQuestManager(ui):
            base_title = "APQuest for AP version"
            ctx: APQuestContext

            lower_game_grid: GridLayout
            upper_game_grid: GridLayout

            game_view: MDRecycleView

            sounds: dict[int, list[Sound]]

            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.sounds = {}

            def load_audio(self, sound_filename: str):
                audio_path = SOUND_PATHS[sound_filename]

                sound_object = SoundLoader.load(str(audio_path.absolute()))
                sound_object.seek(0)
                return sound_object

            def populate_sounds(self):
                try:
                    self.sounds = {
                        sound_filename: [self.load_audio(sound_filename) for _ in range(3)]
                        for sound_filename in ALL_SOUNDS
                    }
                except Exception as e:
                    logger.exception(e)

            def play_audio(self, audio_filename):
                preloaded_sound_list = self.sounds.get(audio_filename)
                sound = preloaded_sound_list.pop(0)
                sound.play()
                preloaded_sound_list.append(sound)

            def build(self) -> Layout:
                container = super().build()

                input_and_rerender = self.ctx.input_and_rerender

                class APQuestGameView(MDRecycleView):
                    _keyboard: Keyboard | None

                    def __init__(self, **kwargs):
                        super().__init__(**kwargs)
                        self.bind_keyboard()

                    def bind_keyboard(self):
                        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
                        self._keyboard.bind(on_key_down=self._on_keyboard_down)

                    def _keyboard_closed(self):
                        if self._keyboard is None:
                            return
                        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
                        self._keyboard = None

                    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
                        if keycode[1] == "up":
                            input_and_rerender(Input.UP)
                        elif keycode[1] == "down":
                            input_and_rerender(Input.DOWN)
                        elif keycode[1] == "left":
                            input_and_rerender(Input.LEFT)
                        elif keycode[1] == "right":
                            input_and_rerender(Input.RIGHT)
                        elif keycode[1] == "spacebar":
                            input_and_rerender(Input.ACTION)
                        elif keycode[1] == "c":
                            input_and_rerender(Input.CONFETTI)
                        return True

                class APQuestGrid(GridLayout):
                    def __init__(self, **kwargs):
                        super().__init__(**kwargs)

                    def check_resize(self, x, y):
                        side = min(self.parent.size)
                        self.size = (side, side)

                self.game_view = APQuestGameView()

                self.add_client_tab("APQuest", self.game_view)

                game_container = self.game_view.ids["game_container"]
                self.lower_game_grid = APQuestGrid()
                self.upper_game_grid = APQuestGrid()
                game_container.add_widget(self.lower_game_grid)
                game_container.add_widget(self.upper_game_grid)

                game_container.bind(size=self.lower_game_grid.check_resize)
                game_container.bind(size=self.upper_game_grid.check_resize)

                self.populate_sounds()

                return container

        self.load_kv()

        return APQuestManager

    def load_kv(self):
        import pkgutil

        from kivy.lang import Builder

        data = pkgutil.get_data(__name__, "ap_quest_client.kv").decode()
        Builder.load_string(data)


async def main(args):
    ctx = APQuestContext(args.connect, args.password)
    ctx.auth = args.name
    ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")

    if not gui_enabled:
        raise RuntimeError("APQuest cannot be played without gui.")

    ctx.run_gui()
    ctx.run_cli()

    ctx.client_loop = asyncio.create_task(ctx.client_loop(), name="Client Loop")

    await ctx.exit_event.wait()
    await ctx.shutdown()


def launch_client(*args):
    parser = get_base_parser()
    parser.add_argument("--name", default=None, help="Slot Name to connect as.")
    parser.add_argument("url", nargs="?", help="Archipelago connection url")

    args = handle_url_arg(parser.parse_args(args))

    if args.nogui:
        raise RuntimeError("APQuest cannot be played without gui.")

    colorama.just_fix_windows_console()

    asyncio.run(main(args))
    colorama.deinit()


if __name__ == "__main__":
    launch_client(*sys.argv[1:])
