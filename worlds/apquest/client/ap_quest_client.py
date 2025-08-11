# isort: off
from kivy.core.window import Keyboard, Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.layout import Layout
from kivymd.uix.recycleview import MDRecycleView
from kvui import GameManager
# isort: on

import asyncio
import sys
from pathlib import Path
from typing import Any

import colorama
from CommonClient import CommonContext, get_base_parser, gui_enabled, handle_url_arg, logger, server_loop
from NetUtils import ClientStatus

from ..apquest.events import LocationClearedEvent
from ..apquest.game import Game, Input
from .graphics import IMAGE_GRAPHICS


class APQuestContext(CommonContext):
    game = "APQuest"
    items_handling = 0b111  # full remote

    slot_data: dict[str, Any]

    ap_quest_game: Game | None = None
    client_loop: asyncio.Task[None]

    highest_processed_item_index: int = 0
    queued_locations: list[int]
    victory: bool = False

    top_image_grid: list[list[Image]]

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.top_image_grid = []
        self.queued_locations = []
        self.slot_data = {}

    async def server_auth(self, password_requested: bool = False) -> None:
        await super().server_auth(password_requested)
        await self.get_username()
        await self.send_connect(game=self.game)

    async def client_loop(self):
        while not self.exit_event.is_set():
            if not self.ap_quest_game or not self.ap_quest_game.gameboard or not self.ap_quest_game.gameboard.ready:
                await asyncio.sleep(0.1)
                continue

            try:
                while self.queued_locations:
                    location = self.queued_locations.pop(0)
                    await self.send_msgs([{"cmd": "LocationChecks", "locations": [location]}])

                new_items = self.items_received[self.highest_processed_item_index :]
                if new_items:
                    for item in new_items:
                        self.highest_processed_item_index += 1
                        self.ap_quest_game.receive_item(item.item, item.location, item.player)
                    self.render()

                if self.ap_quest_game.player.has_won and not self.finished_game:
                    await self.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                    self.finished_game = True
            except Exception as e:
                logger.exception(e)

            await asyncio.sleep(0.1)

    def on_package(self, cmd: str, args: dict) -> None:
        if cmd == "Connected":
            self.slot_data = args["slot_data"]
            hard_mode = self.slot_data["hard_mode"]

            self.ap_quest_game = Game(hard_mode)
            self.highest_processed_item_index = 0
            self.ap_quest_game.gameboard.fill_remote_location_content()
            self.initial_render()

            self.ui.game_view.bind_keyboard()

            self.render()

    def initial_render(self):
        if self.ui.upper_game_grid.children:
            return

        self.top_image_grid = []

        for row in self.ap_quest_game.gameboard.gameboard:
            self.top_image_grid.append([])
            for _ in row:
                empty_path = Path(__file__).parent.parent / "apquest" / "graphics" / "empty.png"
                image = Image(fit_mode="fill", source=str(empty_path.absolute()))
                image.texture.mag_filter = "nearest"
                self.ui.lower_game_grid.add_widget(image)

                image2 = Image(fit_mode="fill")

                self.ui.upper_game_grid.add_widget(image2)

                self.top_image_grid[-1].append(image2)

        self.render()

    def render(self):
        for gameboard_row, image_row in zip(self.ap_quest_game.render(), self.top_image_grid, strict=False):
            for graphic, image in zip(gameboard_row, image_row, strict=False):
                image_name = IMAGE_GRAPHICS[graphic]
                if image_name is None:
                    image.opacity = 0
                    image.source = ""
                    continue

                image_path = Path(__file__).parent.parent / "apquest" / "graphics" / image_name
                image.source = str(image_path.absolute())
                image.texture.mag_filter = "nearest"
                image.opacity = 1

    def handle_game_events(self):
        while self.ap_quest_game.queued_events:
            event = self.ap_quest_game.queued_events.pop(0)

            if isinstance(event, LocationClearedEvent):
                self.queued_locations.append(event.location_id)

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

                    def check_resize(self, instance, x, y):
                        side = min(self.parent.size)
                        self.size = (side, side)

                self.game_view = APQuestGameView()

                self.add_client_tab("APQuest", self.game_view)

                game_container = self.game_view.ids["game_container"]
                self.lower_game_grid = APQuestGrid()
                self.upper_game_grid = APQuestGrid()
                game_container.add_widget(self.lower_game_grid)
                game_container.add_widget(self.upper_game_grid)

                Window.bind(on_resize=self.lower_game_grid.check_resize)
                Window.bind(on_resize=self.upper_game_grid.check_resize)

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
