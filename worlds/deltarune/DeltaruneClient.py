from __future__ import annotations
import os
import asyncio
import typing
import webbrowser
import bsdiff4
import shutil
import json
import hashlib
import websockets
import functools
import shutil

import Utils

from NetUtils import NetworkItem, ClientStatus
from worlds import deltarune
from MultiServer import mark_raw, Context, Client, Endpoint
from Utils import async_start, logging
from worlds.deltarune.LinuxProxy import encode, proxy, proxy_loop

ap_world_version = "v2.2.1"
deltarune_mod_github = "https://github.com/Tenebrosful/DeltaruneAP-mod/releases"

DEBUG = True

# Try importing gui_enabled in Utils first before trying to import them from CommonClient
# Core AP will be officially moving it to Utils in the future, so this is in accommodation for that
gui_loaded_from_utils: bool = False
try:
    from Utils import gui_enabled

    gui_loaded_from_utils = True
except ImportError:
    pass

tracker_loaded = False
try:
    from worlds.tracker.TrackerClient import (
        TrackerCommandProcessor as ClientCommandProcessor,
        TrackerGameContext as SuperContext,
        get_base_parser,
        server_loop,
    )

    tracker_loaded = True

    if not gui_loaded_from_utils:
        from worlds.tracker.TrackerClient import gui_enabled
except ImportError:
    from CommonClient import ClientCommandProcessor, CommonContext as SuperContext, get_base_parser, server_loop

    if not gui_loaded_from_utils:
        from CommonClient import gui_enabled


def guess_deltarune_path(path: str | None):
    tempInstall = ""
    if path == "steaminstall" or path == None:
        tempInstall = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\DELTARUNE"
        if os.path.exists(tempInstall):
            return tempInstall
        else:
            tempInstall = "C:\\Program Files\\Steam\\steamapps\\common\\DELTARUNE"
            if os.path.exists(tempInstall):
                return tempInstall

    if path == "steamdepot":
        tempInstall = "C:\\Program Files (x86)\\Steam\\steamapps\\content\\app_1671210\\depot_1671212"
        if os.path.exists(tempInstall):
            return tempInstall
        else:
            tempInstall = "C:\\Program Files\\Steam\\steamapps\\content\\app_1671210\\depot_1671212"
            if os.path.exists(tempInstall):
                return tempInstall

    if path == "linux":
        tempInstall = os.path.expanduser("~/.local/share/Steam/steamapps/common/DELTARUNE")
        if os.path.exists(tempInstall):
            return tempInstall

    if path == "linuxdepot":
        tempInstall = os.path.expanduser("~/.local/share/Steam/steamapps/content/app_1671210/depot_1671212")
        if os.path.exists(tempInstall):
            return tempInstall

    return path


class DeltaruneCommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx):
        super().__init__(ctx)

    def _cmd_resync(self):
        """Manually trigger a resync."""
        if isinstance(self.ctx, DeltaruneContext):
            self.output(f"Syncing items.")
            self.ctx.syncing = True

    def _cmd_patch(self):
        """Patch the game. Only use this command if /auto_patch fails."""
        if isinstance(self.ctx, DeltaruneContext):
            os.makedirs(name=Utils.user_path("DELTARUNE"), exist_ok=True)
            self.ctx.patch_game()
            self.output("Patched.")

    async def _cmd_linux_proxy(self):
        """Use this to create a proxy between Archipelago Server and your game"""
        self.ctx.proxy = websockets.serve(
            functools.partial(proxy, ctx=self.ctx),
            host="localhost",
            port=1225,
            ping_timeout=999999,
            ping_interval=999999,
        )
        self.ctx.proxy_task = asyncio.create_task(proxy_loop(self.ctx), name="ProxyLoop")

        await self.ctx.proxy
        self.output("You should now be able to connect to localhost:1225 in game")
        await self.ctx.proxy_task

    def _cmd_delete_saves(self):
        """Delete all archipelago saves and caches."""

        if isinstance(self.ctx, DeltaruneContext):
            path = self.ctx.save_game_folder
            for root, dirs, files in os.walk(path):
                for dir in dirs:
                    shutil.rmtree(os.path.join(root, dir), ignore_errors=False)
                    self.output(f"Deleted {os.path.join(root, dir)}")

    def _cmd_inspect_datastore(self, key: typing.Optional[str] = None):
        """Inspect the contents of your datastore."""
        if isinstance(self.ctx, DeltaruneContext):
            if key is not None:
                self.output(
                    f"{self.ctx.get_datastore_prefix() + key}: {self.ctx.stored_data.get(self.ctx.get_datastore_prefix() + key)}"
                )
            else:
                for data in self.ctx.stored_data:
                    self.output(f"{data}: {self.ctx.stored_data[data]}")

    def _cmd_chosen_route(self):
        """Use this to figure out your chosen route, if you don't know or have forgotten."""
        if isinstance(self.ctx, DeltaruneContext):
            if self.ctx.chosen_route == "all_recruits":
                self.output("""You're doing "All Recruits" - Progress through the story normally. Recruit Everyone!!!
Gaining recruits has been turned into checks.""")
            elif self.ctx.chosen_route == "weird_route":
                self.output(
                    """You're doing "Weird Route" - Proceed through the "Weird Route" storyline while losing all possible recruits.
Losing recruits has been turned into checks."""
                )
            elif self.ctx.chosen_route == "all_routes":
                self.output(
                    """You're doing "All Routes" - All checks from doing both the normal and weird route storylines exist.
Both gaining and losing recruits have been turned into checks."""
                )
            else:
                self.output("You'll need to connect to a Multiworld, first.")

    @mark_raw
    async def _cmd_auto_patch(self, path: typing.Optional[str] = None):
        """Patch the game automatically."""
        if isinstance(self.ctx, DeltaruneContext):
            os.path.exists("DELTARUNE")
            for root, dirs, files in os.walk("DELTARUNE"):
                for file in files:
                    os.remove(os.path.join(root, file))
            os.makedirs(name=Utils.user_path("DELTARUNE"), exist_ok=True)

            pathInstall = guess_deltarune_path(path)

            if not os.path.exists(pathInstall) or not os.path.isfile(os.path.join(pathInstall, "data.win")):
                self.output(
                    "ERROR: Cannot find DELTARUNE. Please rerun the command with the correct folder."
                    ' command. "/auto_patch (Steam directory)".'
                )
            else:
                error = False
                opened_browsers = False
                matching_hash = [
                    "83A5A14F9B92A20F21FB9EC6C8528469",
                    "0CCBFD7C4F9FB1B86DE1E2AAEC0BACC9",
                    "1592C9BFFA2D9E53DDEEDC0C4F9A07D6",
                    "B43158DB2E958E767EBB1AAE72FB05A1",
                    "27E36F883F4ADE21707DC8261072D416",
                    "9C80E6300E0548D933CC006F3C22760D",
                ]
                matching_hash_04 = [
                    "9D1FEA9DE81219EA7304F32F1AE7A878",
                    "276441245F2F9C11061E36370E6E9C9D",
                    "F0ECF91309E55E93C1A9D6E10AF1064F",
                    "A3CC0CE00949C538DEC395BC07097069",
                    "300559ED63E1009FD694DEB2784BF1C6",
                ]
                matching_hash_1_05 = [
                    "5D3E158DBE6888FBF24471019FBDE3C9",
                    "F2CA0969E982C9DEDC77EA5EC0DB0972",
                    "D96E6AFD0B40F8B4A39CAE86D0F89A0B",
                    "A3D804E9B101C0D1A6C71117DA214F71",
                    "591BF5321C70F17818559B8A50A99A7F",
                ]
                matching_hash_1_05_30TBPS = [
                    "7A0DDC20059BDFB56E7E5523B0B65ABF",
                    "DEE4F1831C7438AEDD375DBE1B587C3F",
                    "51ABC72791C0AFA533F2DB1D7BE3D44E",
                    "085C34120F7E25B0766E105A56B14B0B",
                    "E5DA918F0C064AAE5068F871E5885605",
                ]
                for chapter in range(0, 5):
                    additional_path = ""
                    file_name = "data.win"

                    if chapter > 0:
                        additional_path = f"chapter{chapter}_windows/"

                    hash = ""

                    with open(f"{pathInstall}/{additional_path}{file_name}", "rb") as f:
                        hash = hashlib.file_digest(f, "md5").hexdigest().upper()

                    if hash != matching_hash[chapter]:
                        self.output(
                            f"{pathInstall}/{additional_path}{file_name} is not DELTARUNE Vanilla. (Manifest 2054633419585385858)"
                        )
                        if hash == matching_hash_1_05[chapter]:
                            self.output("Detected as 1.05")
                        elif hash == matching_hash_04[chapter]:
                            self.output("Dectected as 1.04")
                        elif hash == matching_hash_1_05_30TBPS[chapter]:
                            self.output("Are you a speedrunner ? Because 1.05 30TBPS is detected")
                        else:
                            self.output(f"Expected: {matching_hash[chapter]}, got {hash}")

                        error = True

                if not os.path.exists(Utils.user_path("DELTARUNE_PATCH")):
                    error = True
                    self.output(
                        "ERROR: DELTARUNE_PATCH folder is missing. Please download the patch files and deposit them in the DELTARUNE_PATCH folder at the root of your Archipelago installation."
                    )
                    os.makedirs(name=Utils.user_path("DELTARUNE_PATCH"), exist_ok=True)
                    os.startfile(Utils.user_path("DELTARUNE_PATCH"))
                    opened_browsers = True
                    webbrowser.open(deltarune_mod_github, new=2, autoraise=True)
                for i in range(0, 6):
                    if not os.path.exists(Utils.user_path("DELTARUNE_PATCH", f"chapter_{i}.bsdiff")):
                        error = True
                        self.output(
                            f"ERROR: DELTARUNE_PATCH/chapter_{i}.bsdiff is missing. Please download the patch files and deposit them in the DELTARUNE_PATCH folder at the root of your Archipelago installation."
                        )
                        if not opened_browsers:
                            os.startfile(Utils.user_path("DELTARUNE_PATCH"))
                            opened_browsers = True
                            webbrowser.open(deltarune_mod_github, new=2, autoraise=True)

                if not error:
                    self.output(
                        f"Your game will now be patched. Please wait... it might take a while and make your client not respond but that's normal."
                    )
                    await asyncio.sleep(0.1)
                    shutil.copytree(pathInstall, Utils.user_path("DELTARUNE"), dirs_exist_ok=True)
                    self.ctx.patch_game()
                    self.output(f"Patching successful! You can now start {Utils.user_path("DELTARUNE")}\\DELTARUNE.exe")


class DeltaruneContext(SuperContext):
    tags = {"TextOnly"}
    game = "DELTARUNE"
    command_processor = DeltaruneCommandProcessor
    items_handling = 0b111
    save_game_folder = os.path.expandvars(r"%localappdata%/DELTARUNEAP")
    proxy = None
    connected = False
    authenticated = False
    proxy_endpoint: Endpoint = None
    proxy_task = None
    proxy_autoreconnect_task = None
    proxy_server_msgs = []
    proxy_message_queue = []
    room_info = {}
    connected_msg = {}
    is_processing_outgoing_messages = False

    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.game = "DELTARUNE"

    def is_connected(self) -> bool:
        return self.server and self.server.socket.open

    def is_proxy_connected(self) -> bool:
        return self.proxy_endpoint and self.proxy_endpoint.socket.open

    async def disconnect_proxy(self):
        if self.proxy_endpoint and not self.proxy_endpoint.socket.closed:
            await self.proxy_endpoint.socket.close()
        if self.proxy_task is not None:
            await self.proxy_task

    def get_datastore_prefix(self):
        return f"{self.slot}_{self.team}_"

    def patch_game(self):
        with open(Utils.user_path("DELTARUNE", "chapter1_windows", "data.win"), "rb") as f:
            with open(Utils.user_path("DELTARUNE_PATCH", "chapter_1.bsdiff"), "rb") as patch_file:
                logging.info(f"Patching Chapter 1...")
                patchedFile = bsdiff4.patch(f.read(), patch_file.read())
        with open(Utils.user_path("DELTARUNE", "chapter1_windows", "data.win"), "wb") as f:
            f.write(patchedFile)
        with open(Utils.user_path("DELTARUNE", "chapter2_windows", "data.win"), "rb") as f:
            with open(Utils.user_path("DELTARUNE_PATCH", "chapter_2.bsdiff"), "rb") as patch_file:
                logging.info(f"Patching Chapter 2...")
                patchedFile = bsdiff4.patch(f.read(), patch_file.read())
        with open(Utils.user_path("DELTARUNE", "chapter2_windows", "data.win"), "wb") as f:
            f.write(patchedFile)
        with open(Utils.user_path("DELTARUNE", "chapter3_windows", "data.win"), "rb") as f:
            with open(Utils.user_path("DELTARUNE_PATCH", "chapter_3.bsdiff"), "rb") as patch_file:
                logging.info(f"Patching Chapter 3...")
                patchedFile = bsdiff4.patch(f.read(), patch_file.read())
        with open(Utils.user_path("DELTARUNE", "chapter3_windows", "data.win"), "wb") as f:
            f.write(patchedFile)
        with open(Utils.user_path("DELTARUNE", "chapter4_windows", "data.win"), "rb") as f:
            with open(Utils.user_path("DELTARUNE_PATCH", "chapter_4.bsdiff"), "rb") as patch_file:
                logging.info(f"Patching Chapter 4...")
                patchedFile = bsdiff4.patch(f.read(), patch_file.read())
        with open(Utils.user_path("DELTARUNE", "chapter4_windows", "data.win"), "wb") as f:
            f.write(patchedFile)
        with open(Utils.user_path("DELTARUNE", "chapter5_windows", "data.win"), "rb") as f:
            with open(Utils.user_path("DELTARUNE_PATCH", "chapter_5.bsdiff"), "rb") as patch_file:
                logging.info(f"Patching Chapter 5...")
                patchedFile = bsdiff4.patch(f.read(), patch_file.read())
        with open(Utils.user_path("DELTARUNE", "chapter5_windows", "data.win"), "wb") as f:
            f.write(patchedFile)
        with open(Utils.user_path("DELTARUNE", "data.win"), "rb") as f:
            with open(Utils.user_path("DELTARUNE_PATCH", "chapter_0.bsdiff"), "rb") as patch_file:
                logging.info(f"Patching Chapter Select...")
                patchedFile = bsdiff4.patch(f.read(), patch_file.read())
        with open(Utils.user_path("DELTARUNE", "data.win"), "wb") as f:
            f.write(patchedFile)

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super().server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    def on_package(self, cmd: str, args: dict):
        super().on_package(cmd, args)
        if self.proxy != None:
            logging.info(f"Server -> Proxy | {args}")
        if cmd == "Connected":
            self.game = self.slot_info[self.slot].game
            self.set_notify(
                self.get_datastore_prefix() + "completed_chapters", self.get_datastore_prefix() + "current_location"
            )
            self.connected_msg = args
            self.connected = True
            self.authenticated = True
        elif cmd == "RoomInfo":
            self.room_info = args
            logging.info(f"Room info received: {args}")
        elif self.proxy != None:
            if cmd != "PrintJSON":
                self.proxy_server_msgs.append(args)
        async_start(process_deltarune_cmd(self, cmd, args))

    def make_gui(self):
        ui = super().make_gui()
        ui.base_title = "Archipelago DELTARUNE Client " + ap_world_version + " - AP version"
        ui.logging_pairs = [("Client", "Archipelago")]
        return ui

    async def version_mismatch(self):
        DeltaruneCommandProcessor.output(
            self, """*****\nWARNING: Incompatible DELTARUNEAP version. Unable to connect.\n*****"""
        )
        await super().disconnect(False)


async def process_deltarune_cmd(ctx: DeltaruneContext, cmd: str, args: dict):
    if cmd == "Connected":
        try:
            options = args["slot_data"]["options"]   
            DeltaruneCommandProcessor.output(
                ctx, """*****\nRemember that you are only connected to a text client.
To connect in-game, make sure to patch DELTARUNE using the setup guide and put the connection details there.\n*****"""
            )
        except:
            await ctx.version_mismatch()
            return


def main():
    Utils.init_logging("DeltaruneClient" + ap_world_version, exception_logger="Client")

    async def _main():
        ctx = DeltaruneContext(None, None)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")

        if tracker_loaded:
            ctx.run_generator()
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()

        await ctx.exit_event.wait()
        await ctx.shutdown()

    import colorama

    colorama.init()

    asyncio.run(_main())
    colorama.deinit()


if __name__ == "__main__":
    parser = get_base_parser(description="DELTARUNE Client, for text interfacing.")
    args = parser.parse_args()
    main()
