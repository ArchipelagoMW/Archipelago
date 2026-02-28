# Based (read: copied almost wholesale and edited) off the KHDays and Manual clients.

import asyncio
from typing import Callable

import Utils
from CommonClient import CommonContext, server_loop, gui_enabled, get_base_parser
from NetUtils import ClientStatus

from .data.locations import all_locations


class Shapez2Context(CommonContext):
    items_handling = 0b000  # None
    game = "shapez 2"

    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.slot_data = None

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super().server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    def on_package(self, cmd: str, args: dict):
        if cmd == 'Connected':
            self.slot_data = args["slot_data"]

    def run_gui(self):
        from kvui import GameManager
        from kivy.uix.button import Button
        from kivy.uix.gridlayout import GridLayout
        from kivy.uix.layout import Layout
        from kivy.uix.scrollview import ScrollView
        from kivy.uix.widget import Widget

        class Shapez2Manager(GameManager):
            base_title = "Archipelago shapez 2 Client"
            ctx: Shapez2Context

            def build(self) -> Layout:
                container = super().build()
                self.add_client_tab("Milestones", self.build_milestones_panel())
                self.add_client_tab("Tasks", self.build_tasks_panel())
                self.add_client_tab("Operator levels", self.build_operator_panel())
                self.add_client_tab("Goal", self.build_goal_panel())
                return container

            def build_milestones_panel(self) -> Widget:
                try:
                    def action(num: int) -> Callable:
                        return lambda instance: self.send_milestone(num)

                    milestones: int = 20
                    scroll = ScrollView(do_scroll=(False, True))
                    commander_group = GridLayout(cols=5, size_hint_y=None)
                    for i in range(milestones):
                        commander_button = Button(text=f"Milestone {i+1}")
                        commander_button.bind(on_press=action(i+1))
                        commander_group.add_widget(commander_button)
                    scroll.add_widget(commander_group)
                    return scroll
                except Exception as e:
                    print(e)

            def build_tasks_panel(self) -> Widget:
                try:
                    def action(line: int, num: int) -> Callable:
                        return lambda instance: self.send_task(line, num)

                    task_lines: int = 200
                    scroll = ScrollView(do_scroll=(False, True))
                    commander_group = GridLayout(cols=5, height=6000, size_hint_y=None)
                    for i in range(task_lines):
                        for j in range(1, 6):
                            commander_button = Button(text=f"Task #{i+1}-{j}", height=30, size_hint_y=None)
                            commander_button.bind(on_press=action(i+1, j))
                            commander_group.add_widget(commander_button)
                    scroll.add_widget(commander_group)
                    return scroll
                except Exception as e:
                    print(e)

            def build_operator_panel(self) -> Widget:
                try:
                    def action(level: int) -> Callable:
                        return lambda instance: self.send_operator_level(level)

                    operator_levels: int = 200
                    scroll = ScrollView(do_scroll=(False, True))
                    commander_group = GridLayout(cols=5, height=600, size_hint_y=None)
                    for i in range(operator_levels):
                        commander_button = Button(text=f"Operator level {i+1}", height=30, size_hint_y=None)
                        commander_button.bind(on_press=action(i+1))
                        commander_group.add_widget(commander_button)
                    scroll.add_widget(commander_group)
                    return scroll
                except Exception as e:
                    print(e)

            def build_goal_panel(self) -> Widget:
                try:
                    scroll = ScrollView(do_scroll=(False, True))
                    commander_group = GridLayout(cols=1, height=30, size_hint_y=None)
                    commander_button = Button(text="Goal", height=30, size_hint_y=None)
                    commander_button.bind(on_press=lambda instance: asyncio.create_task(
                        self.ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                    ))
                    commander_group.add_widget(commander_button)
                    scroll.add_widget(commander_group)
                    return scroll
                except Exception as e:
                    print(e)

            def send_milestone(self, num: int):
                asyncio.create_task(self.ctx.check_locations(tuple(
                    all_locations[f"Milestone {num} reward #{i}"].location_id for i in range(1, 13)
                )))

            def send_task(self, line: int, num: int):
                asyncio.create_task(self.ctx.check_locations((all_locations[f"Task #{line}-{num}"].location_id, )))

            def send_operator_level(self, level: int):
                asyncio.create_task(self.ctx.check_locations((all_locations[f"Operator level {level}"].location_id, )))

        self.ui = Shapez2Manager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")


def main():
    # Text Mode to use !hint and such with games that have no text entry
    Utils.init_logging("shapez2Client", exception_logger="Client")

    async def _main():
        ctx = Shapez2Context(None, None)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()

        await ctx.exit_event.wait()
        ctx.server_address = None

        await ctx.shutdown()

    import colorama

    colorama.init()

    asyncio.run(_main())
    colorama.deinit()


if __name__ == "__main__":
    parser = get_base_parser(description="shapez 2 manual-like client, intended for playing without the mod.")
    args = parser.parse_args()
    main()
