import asyncio
import os

import urllib.parse

from CommonClient import get_base_parser, server_loop
from kvui import GameManager
from worlds import AutoWorldRegister, network_data_package
from ..ManualClient import read_apmanual_file, ManualContext, tracker_loaded, gui_enabled, game_watcher_manual
from .. import Locations, Items


client_name = "Final Fantasy XIV Manual Client"
client_description = "Manual Final Fantasy XIV Client, for operating the Final Fantasy XIV Manual implementation in Archipelago."

def get_context(args, config_file):
    return XivContext(args.connect, args.password, config_file.get("game"), config_file.get("player_name"))

class XivContext(ManualContext):
    game = ""

    def make_gui(self) -> type[GameManager]:
        from kivy.uix.layout import Layout
        ManualUi = super().make_gui()
        class XivUi(ManualUi):
            def build(self) -> Layout:
                layout = super().build()
                self.game_bar_text.text = "Manual_FFXIV_Silasary"
                self.manual_game_layout.parent.remove_widget(self.manual_game_layout)
                return layout
            pass
        return XivUi

    def after_run_gui(self):
        # add a custom tab to the client named "Deck Builder"
        # self.ui.manual_game_layout.remove_widget(self.game_bar_label)
        self.ui.base_title = client_name # set a custom title for the custom client window

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(ManualContext, self).server_auth(password_requested)

        world = AutoWorldRegister.world_types.get(self.game)
        if not self.location_table and not self.item_table and world is None:
            self.location_table = Locations.location_name_to_location
            self.item_table = Items.item_name_to_item

        data_package = network_data_package["games"].get(self.game, {}) or network_data_package["games"].get("Final Fantasy XIV", {})

        if data_package:
            self.update_ids(data_package)

        if world is not None and hasattr(world, "victory_names"):
            self.victory_names = world.victory_names
            self.goal_location = self.get_location_by_name(world.victory_names[0])
        else:
            self.victory_names = Locations.victory_names
            self.goal_location = self.get_location_by_name(Locations.victory_names[0])

        if not self.game:
            self.tags = {"AP", "Tracker"}
        else:
            self.tags = {"AP"}

        await self.get_username()
        await self.send_connect()

    def on_package(self, cmd: str, args: dict):
        super().on_package(cmd, args)
        if cmd == "RoomInfo":
            pass
        if cmd in {"Connected"}:
            if not self.game:
                slot_info = args['slot_info'][str(args['slot'])]
                game = slot_info.get('game', self.game)
                if game not in {"Manual_FFXIV_Silasary", "Final Fantasy XIV"}:
                    super().event_invalid_game()
                self.game = game


            for key in ['prog_classes']:
                if key in args.get('slot_data', {}):
                    setattr(self, key, args['slot_data'][key])

            self.update_custom_ui()
        elif cmd in {"DataPackage", "ReceivedItems", "RoomUpdate"}:
            self.update_custom_ui()


    def update_custom_ui(self):
        from kivy.uix.modalview import ModalView
        from kivy.uix.scrollview import ScrollView
        from kivy.uix.gridlayout import GridLayout
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.label import Label
        from kivy.uix.spinner import Spinner, SpinnerOption
        from kivy.uix.button import Button
        from kivy.uix.image import AsyncImage
        from kivy.metrics import dp



#######################################################
########### End of *ManualContext class ###############
#######################################################

async def game_watcher_xiv(ctx: ManualContext):
    while not ctx.exit_event.is_set():
        if "Tracker" in ctx.tags and ctx.game:
            ctx.tags.remove("Tracker")
            await ctx.send_msgs([{"cmd": "ConnectUpdate", "tags": ctx.tags}])
        await asyncio.sleep(1)


#################################################################
# The below is copied from the Manual client with minimal changes.
# Leave it alone unless you know what you're doing.
#################################################################

async def main(args):
    config_file = {}
    if args.apmanual_file and args.apmanual_file.startswith("archipelago://"):
        url = urllib.parse.urlparse(args.apmanual_file)
        args.connect = url.netloc
        if url.username:
            args.name = urllib.parse.unquote(url.username)
        if url.password:
            args.password = urllib.parse.unquote(url.password)
        queries = urllib.parse.parse_qs(url.query)
        if "game" in queries:
            config_file['game'] = queries["game"][0]

    elif args.apmanual_file and os.path.exists(args.apmanual_file):
        config_file = read_apmanual_file(args.apmanual_file)
    ctx = get_context(args, config_file)
    ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")

    ctx.item_table = config_file.get("items", {})
    ctx.location_table = config_file.get("locations", {})
    ctx.region_table = config_file.get("regions", {})
    ctx.category_table = config_file.get("categories", {})

    if tracker_loaded:
        ctx.run_generator()

    if gui_enabled:
        ctx.run_gui()
        ctx.after_run_gui()

    ctx.run_cli()

    progression_watcher = asyncio.create_task(
        game_watcher_manual(ctx), name="ManualProgressionWatcher")
    extra_watcher = asyncio.create_task(
        game_watcher_xiv(ctx), name="XivProgressionWatcher")



    await ctx.exit_event.wait()
    ctx.server_address = None

    await progression_watcher
    await extra_watcher

    await ctx.shutdown()

def launch() -> None:
    import colorama

    parser = get_base_parser(description=client_description)
    parser.add_argument('apmanual_file', default="", type=str, nargs="?",
                        help='Path to an APMANUAL file')
    args, rest = parser.parse_known_args()

    colorama.init()
    asyncio.run(main(args))
    colorama.deinit()

if __name__ == '__main__':
    launch()
