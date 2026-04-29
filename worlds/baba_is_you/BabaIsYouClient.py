from __future__ import annotations
import os, sys, re
import asyncio

import ModuleUpdate
ModuleUpdate.update()

import Utils

# Items that have multiple copies; makes duplicate files for each copy of the item
MULTI_ITEMS = ("Blossom Petal", "Blossom", "Bonus Orb")

# Pack version
VERSION = "0.2.0"

import typing, zipfile

# Function for extracting a ZIP file while removing the root
# https://stackoverflow.com/questions/8689938/extract-files-from-zip-without-keep-the-top-level-folder-with-python-zipfile
def _members_without_root(archive: zipfile.ZipFile, root_filename: str) -> typing.Generator:
    for info in archive.infolist():
        parts = info.filename.split(root_filename)
        if len(parts) > 1 and parts[1]:
            # We join using the root filename, because there might be a subdirectory with the same name.
            info.filename = root_filename.join(parts[1:])
            yield info

# Removes characters that Baba Is You won't like in the storage files
# ($ is used for color codes, = is used to tell when the data starts)
def clean(text: str) -> str:
    text.replace("=", "")
    text.replace("$", "S")
    text.replace("#", "")
    return text

def auto_install_pack(path: str, world: str, forceInstall: bool = False):
    defaultWorldPath = os.path.join(path, "Data", "Worlds", "baba")
    if os.path.exists(defaultWorldPath):
        worldPath = os.path.join(path, "Data", "Worlds", world)
        valid = (forceInstall or (not (os.path.exists(worldPath) and os.path.exists(os.path.join(worldPath, "0level.l")))))
        updateOnly = False
        if not valid: # check for only updating the data file
            updateOnly = True
            dataPath = os.path.join(worldPath, "world_data.txt")
            if os.path.isfile(dataPath):
                lines = []
                try:
                    with open(dataPath, 'r') as f:
                        lines = f.readlines()
                        f.close()
                except OSError:
                    pass

                for line in lines:
                    if line[0:8] == "version=":
                        testVersion = line[8:]
                        if testVersion != VERSION:
                            valid = True
                            print("Out of date version: ",testVersion)
                        break

        if valid:
            print("Attempting to create babapelago world")

            import shutil
            from .. import user_folder, local_folder

            try:
                if not updateOnly:
                    shutil.copytree(defaultWorldPath, worldPath, dirs_exist_ok=True)
                
                isAPWorld = ".apworld" in sys.modules[__name__].__file__
                if isAPWorld:
                    apWorldPath = os.path.join(user_folder, "baba_is_you.apworld")
                    
                    with zipfile.ZipFile(apWorldPath, mode="r") as archive:
                        # We will use the first directory with no more than one path segment as the root.
                        archive.extractall(path=worldPath, members=_members_without_root(archive, "baba_is_you/babapelago"))
                else:
                    apWorldPath = os.path.join(local_folder, "baba_is_you")
                    shutil.copytree(os.path.join(apWorldPath, "babapelago"), worldPath, dirs_exist_ok=True)
            except Exception as e:
                print(e)
                return False
            
            return True
        else:
            return True
    else:
        print("Unable to locate default Baba world")
        return False

if __name__ == "__main__":
    Utils.init_logging("BabaIsYouClient", exception_logger="Client")

from .locations import LOCATION_NAME_TO_ID as baba_loc_name_to_id
from NetUtils import NetworkItem, ClientStatus
from CommonClient import gui_enabled, logger, get_base_parser, ClientCommandProcessor, \
    CommonContext, server_loop

class BabaIsYouClientCommandProcessor(ClientCommandProcessor):
    def _cmd_resync(self):
        """Manually trigger a resync."""
        self.output(f"Syncing items.")
        self.ctx.syncing = True
        if self.ctx.is_connected:
            self.ctx.create_options_files()
    
    def _cmd_filepath(self) -> bool:
        """Change filepath to Baba Is You installation."""
        import platform
        osName = platform.system()

        path = Utils.open_directory("Select Baba Is You directory...")
        if path is None:
            msg = "No directory was entered!"
            self.output("Error: " + msg)
            return False

        if osName == "Darwin": # Mac
            path = path.replace("\\ ", " ")
            path = path.strip()
        path = path.strip("\"")
        
        if osName == "Darwin": # Navigate inside application package
            path = os.path.join(path, "Baba Is You.app", "Contents", "Resources")

        if os.path.isdir(path):
            self.output(f"Set communication path to: {os.path.abspath(path)}")
        else:
            msg = f"Couldn't find directory at \"{os.path.abspath(path)}\"! Does it exist?"
            self.output("Error: " + msg)
            return False
    
        self.ctx.game_data_path = path
        self.ctx.game_communication_path = os.path.join(path, "AP", f"save{self.ctx.save_slot}")

        if not os.path.exists(self.ctx.game_communication_path):
            os.makedirs(self.ctx.game_communication_path)

        return True
    
    def _cmd_save_slot(self, slot: str = "1") -> bool:
        """Changes the save slot being used. Defaults to 1. Note that using a slot higher than 3 requires an additional mod."""

        slotNum = int(slot)
        if slotNum < 1 or slotNum > 100:
            self.output(f"Slot out of range (1-100)")
            return False

        self.ctx.save_slot = slotNum
        self.ctx.game_communication_path = os.path.join(self.ctx.game_data_path, "AP", f"save{self.ctx.save_slot}")

        if not os.path.exists(self.ctx.game_communication_path):
            os.makedirs(self.ctx.game_communication_path)
        
        self.output(f"Set save slot to {slotNum}")
        if self.ctx.is_connected:
            self._cmd_resync(self) # Also run resync
        return True
    
    def _cmd_install_pack(self) -> bool:
        """Install the Babapelago level pack, replacing all files."""
        result = auto_install_pack(self.ctx.game_data_path, "babapelago", True)
        if result:
            self.output("Successfully installed the pack!")
        else:
            self.output("An error occured when trying to install the pack.")
        return result

class BabaIsYouContext(CommonContext):
    command_processor: int = BabaIsYouClientCommandProcessor
    game = "Baba Is You"
    items_handling = 0b111  # full remote

    def __init__(self, server_address, password):
        super(BabaIsYouContext, self).__init__(server_address, password)
        self.send_index: int = 0
        self.syncing = False
        self.awaiting_bridge = False
        self.is_connected = False
        self.duplicate_files = {}

        import platform
        osName = platform.system()

        # Find Baba Is You steam installation (dennisw100, modified)
        if osName == "Windows":
            import winreg
            steam_path = os.path.join(winreg.QueryValueEx(winreg.OpenKey(winreg.HKEY_CURRENT_USER, "SOFTWARE\\VALVE\\Steam"), "SteamPath")[0], 'steamapps', 'libraryfolders.vdf')
        elif osName == "Darwin":
            steam_path = os.path.expanduser("~/Library/Application Support/Steam/steamapps/libraryfolders.vdf")
        else:
            steam_path = os.path.expanduser("~/.steam/steam/steamapps/libraryfolders.vdf")
        try:
            with open(steam_path, 'r', encoding='utf-8') as file:
                content = file.read()
                library_paths = {index: path for index, path in re.findall(r"\"(\d+)\"\s+?\{[^}]*\"path\"\s+?\"([^\"]+)\"", content)}
                for index, testpath in library_paths.items():
                    testpath = os.path.join(testpath, "steamapps", "common", "Baba Is You")
                    if os.path.isfile(os.path.join(testpath, "Baba Is You.exe")) or os.path.isdir(os.path.join(testpath, "Baba Is You.app") or os.path.isfile(os.path.join(testpath, "run.sh"))):
                        path = testpath
        except OSError:
            path = None # couldn't open
        
        if (path is not None) and os.path.isdir(path):
            logger.info(f"Found steam installation at: {os.path.abspath(path)}")
        else:
            path = Utils.open_directory("Select Baba Is You directory...")
            if not path:
                msg = "No directory was entered!"
                logger.error("Error: " + msg)
                Utils.messagebox("Error", msg, error=True)
                sys.exit(1)
                return

            if osName == "Darwin": # Mac
                path = path.replace("\\ ", " ")
                path = path.strip()
        path = path.strip("\"")
        
        if osName == "Darwin": # Navigate inside application package
            path = os.path.join(path, "Baba Is You.app", "Contents", "Resources")

        if os.path.isdir(path):
            logger.info(f"Set communication path to: {os.path.abspath(path)}")
        else:
            msg = f"Couldn't find directory at \"{os.path.abspath(path)}\"! Does it exist?"
            logger.error("Error: " + msg)
            Utils.messagebox("Error", msg, error=True)
            sys.exit(1)
            return
        
        self.save_slot = 1
        self.game_data_path = path
        self.game_communication_path = os.path.join(path, "AP", f"save{self.save_slot}")

        # auto install pack
        auto_install_pack(path, "babapelago")

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(BabaIsYouContext, self).server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    async def connection_closed(self):
        self.is_connected = False
        self.duplicate_files = {}
        await super(BabaIsYouContext, self).connection_closed()
        for root, dirs, files in os.walk(self.game_communication_path):
            for file in files:
                if file.endswith(".item") or file.endswith(".data") or file.endswith(".tmp") or file.endswith(".sent"):
                    os.remove(root + "/" + file)

    @property
    def endpoints(self):
        if self.server:
            return [self.server]
        else:
            return []

    async def shutdown(self):
        self.is_connected = False
        self.duplicate_files = {}
        await super(BabaIsYouContext, self).shutdown()
        for root, dirs, files in os.walk(self.game_communication_path):
            for file in files:
                if file.endswith(".item") or file.endswith(".data") or file.endswith(".tmp") or file.endswith(".sent"):
                    os.remove(root+"/"+file)

    def on_package(self, cmd: str, args: dict):
        if cmd in {"Connected"}:
            self.is_connected = True
            if not os.path.exists(self.game_communication_path):
                os.makedirs(self.game_communication_path)

            self.slot_data = args["slot_data"]
            self.create_options_files()
        
        if cmd in {"RoomInfo"}:
            self.seed_name = args['seed_name']

        if cmd in {"ReceivedItems"}:
            start_index = args["index"]
            if start_index != len(self.items_received):
                for item in args['items']:
                    networkItem = NetworkItem(*item)

                    itemname = self.item_names.lookup_in_game(networkItem.item)
                    if itemname == "Speck": # Don't bother sending specks
                        continue
                    
                    # Create files for each item.
                    # A strange quirk with Baba Is You is that while we can dynamically tell when a file exists,
                    # its contents are stored into memory as soon as it is read (or something like that),
                    # meaning that once we create a file, its contents are "locked" from the perspective of the game.
                    # This is why it is necessary to create a new file for every individual item, even for multiple counts, such as Blossoms.
                    filename = f"AP_{str(networkItem.location)}_PLR{str(networkItem.player)}_ITM{str(networkItem.item)}"
                    if itemname in MULTI_ITEMS:
                        count = 0
                        if self.duplicate_files.get(filename):
                            count = self.duplicate_files[filename]
                        count += 1

                        # Make duplicates of this file (only really relative for the cheat console)
                        if count > 1:
                            filename = f"{filename}_{count}"
                        self.duplicate_files[filename] = count
                    filename = filename + ".item"
                    filepath = os.path.join(self.game_communication_path, filename)
                    with open(filepath, 'w') as f:
                        f.write("[data]\n")
                        f.write(f"item={itemname}\n")
                        f.write(f"player={clean(self.player_names[networkItem.player])}\n")
                        f.write(f"location={clean(self.location_names.lookup_in_slot(networkItem.location, networkItem.player))}\n")
                        f.close()

    def run_gui(self):
        """Import kivy UI system and start running it as self.ui_task."""
        from kvui import GameManager

        class BabaIsYouManager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago")
            ]
            base_title = "Archipelago BabaIsYou Client"

        self.ui = BabaIsYouManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")
    
    def create_options_files(self):  
        currPath = os.path.join(self.game_communication_path,"AP_OPTIONS.data")
        with open(currPath, 'w') as f:
            f.write("[options]\n")
            for option in self.slot_data:
                if option != "level_shuffle_dict":
                    f.write(f"{option}={self.slot_data[option]}\n")
            f.write(f"seed={str(self.seed_name)}")
            f.close()

        # Remove existing seed file
        for root, dirs, files in os.walk(self.game_communication_path):
            for file in files:
                if file.startswith("AP_SEED_") and file.endswith(".data"):
                    os.remove(root + "/" + file)

        # Set up seed file (done to prevent getting checks from previous games)
        currPath = os.path.join(self.game_communication_path,f"AP_SEED_{self.seed_name}.data")
        with open(currPath, 'w') as f:
            f.close()

        # Set up level shuffle dict file
        if self.slot_data["level_shuffle"] != 0:
            currPath = os.path.join(self.game_communication_path,"AP_SHUFFLE.data")
            with open(currPath, 'w') as f:
                f.write("[general]\n")
                i = 0
                for region1 in self.slot_data["level_shuffle_dict"]:
                    region2 = self.slot_data["level_shuffle_dict"][region1]
                    f.write(f"{i}={region1}@{region2}\n")
                    i += 1
                f.write(f"total={i}")
                f.close()

        # Set up already checked locations
        currPath = os.path.join(self.game_communication_path,"AP_CHECKS.data")
        with open(currPath, 'w') as f:
            f.write("[checks]\n")
            for ss in self.checked_locations:
                locationName = self.location_names.lookup_in_game(ss)
                f.write(f"{locationName}=1\n")
            f.close()


async def game_watcher(ctx: BabaIsYouContext):
    # from worlds.baba_is_you.locations import lookup_id_to_name
    while not ctx.exit_event.is_set():

        if ctx.syncing == True:
            ctx.duplicate_files = {}
            sync_msg = [{'cmd': 'Sync'}]
            if ctx.locations_checked:
                sync_msg.append({"cmd": "LocationChecks", "locations": list(ctx.locations_checked)})
            await ctx.send_msgs(sync_msg)
            ctx.syncing = False
        
        sending = []
        victory = False
        if ctx.is_connected:
            currPath = os.path.join(ctx.game_communication_path,"AP_CHECKS.data")
            if os.path.isfile(currPath):
                lines = []
                with open(currPath, 'r') as f:
                    lines = f.readlines()
                    f.close()
                for line in lines:
                    location = line[:-3]
                    if location == "Goal":
                        victory = True
                    else:
                        st = baba_loc_name_to_id.get(location)
                        if st is not None:
                            sending = sending+[(int(st))]
                
                        
        
        ctx.locations_checked = sending
        message = [{"cmd": 'LocationChecks', "locations": sending}]
        await ctx.send_msgs(message)

        if not ctx.finished_game and victory:
            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
            ctx.finished_game = True
        await asyncio.sleep(0.1)

def launch_baba_is_you_client():
    async def main(args):
        ctx = BabaIsYouContext(args.connect, args.password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()
        progression_watcher = asyncio.create_task(
            game_watcher(ctx), name="BabaIsYouProgressionWatcher")

        await ctx.exit_event.wait()
        ctx.server_address = None

        await progression_watcher

        await ctx.shutdown()

    import colorama

    parser = get_base_parser(description="Baba Is You Client, for text interfacing.")

    args, rest = parser.parse_known_args()
    colorama.init()
    asyncio.run(main(args))
    colorama.deinit()


if __name__ == '__main__':
    launch_baba_is_you_client()