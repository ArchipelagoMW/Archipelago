import asyncio
import sys
from pathlib import Path
from typing import Any

import colorama
from CommonClient import CommonContext, get_base_parser, gui_enabled, handle_url_arg

from kvui import GameManager

from kivy.core.window import Keyboard, Window
from kivy.uix.layout import Layout
from kivymd.uix.recycleview import MDRecycleView

sys.path.append(str(Path(__file__).parent / "apquest"))

from game import Game, Input
from play_in_console import render_to_text


class APQuestContext(CommonContext):
    game = "APQuest"
    items_handling = 0b111  # full remote

    slot_data: dict[str, Any]

    ap_quest_game: Game | None = None

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.slot_data = {}

    async def server_auth(self, password_requested: bool = False) -> None:
        await super().server_auth(password_requested)
        await self.get_username()
        await self.send_connect(game=self.game)

    def on_package(self, cmd: str, args: dict) -> None:
        if cmd == "Connected":
            self.slot_data = args["slot_data"]
            hard_mode = self.slot_data["hard_mode"]

            self.ap_quest_game = Game(hard_mode)
            self.ap_quest_game.gameboard.fill_default_location_content()

            self.ui.game_view.bind_keyboard()

            self.render()

    def render(self):
        self.ui.game_view.ids.game.text = render_to_text(self.ap_quest_game)

    def input_and_rerender(self, input_key: Input) -> None:
        if self.ap_quest_game is None:
            return
        if not self.ap_quest_game.gameboard.ready:
            return
        self.ap_quest_game.input(input_key)
        self.render()

    def make_gui(self) -> type[GameManager]:
        ui = super().make_gui()

        class APQuestManager(ui):
            base_title = "APQuest for AP version"
            ctx: APQuestContext

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

                self.game_view = APQuestGameView()

                self.add_client_tab("APQuest", self.game_view)

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
    # ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")

    if not gui_enabled:
        raise RuntimeError("APQuest cannot be played without gui.")

    ctx.run_gui()
    ctx.run_cli()

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
