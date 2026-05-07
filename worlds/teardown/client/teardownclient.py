import asyncio
import subprocess
import os
import json
import xml.etree.ElementTree as ET
from Utils import gui_enabled, open_filename, user_path
from CommonClient import CommonContext, get_base_parser, server_loop


SETTINGS_PATH = user_path("teardownsettings.json")


Missionindex = {
        "mall_intro",
        "lee_computers",
        "lee_login",
        "marina_demolish",
        "marina_cars",
        "mansion_pool",
        "lee_safe",
        "marina_gps",
        "lee_tower",
        "mansion_art",
        "marina_tools",
        "marina_art_back",
        "mall_foodcourt",
        "mansion_fraud",
        "caveisland_computers",
        "mansion_race",
        "mansion_safe",
        "lee_powerplant",
        "caveisland_propane",
        "caveisland_dishes",
        "lee_flooding",
        "frustrum_chase",
        "factory_espionage",
        "caveisland_ingredients",
        "frustrum_tornado",
        "mall_shipping",
        "carib_alarm",
        "carib_barrels",
        "carib_destroy",
        "carib_yacht",
        "frustrum_vehicle",
        "mall_decorations",
        "factory_tools",
        "mall_radiolink",
        "frustrum_pawnshop",
        "factory_robot",
        "lee_woonderland",
        "factory_explosive",
        "caveisland_roboclear",
        "cullington_bomb",
}





class TeardownContext(CommonContext):
    game = "Teardown"
    tags = CommonContext.tags | {"AP"}
    items_handling = 0b111
    want_slot_data = True



    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(TeardownContext, self).server_auth(password_requested)
        await self.get_username()
        await self.send_connect(game="")

    def on_package(self, cmd: str, args: dict):
        if cmd == "Connected":
                self.game = self.slot_info[self.slot].game

    async def disconnect(self, allow_autoreconnect: bool = False):
        self.game = ""
        await super().disconnect(allow_autoreconnect)




    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game_exe_path = ""
        self.savegame_path = ""
        self.loadsettings()


    def loadsettings(self):
        # Load our settings from our json file
        if os.path.exists(SETTINGS_PATH):
            with open(SETTINGS_PATH, "r") as f:
                data = json.load(f)
                self.game_exe_path = data.get("game_exe_path", "")
                self.savegame_path = data.get("savegame_path", "")

    def savesettings(self):
        # Save our settings to our json file
        data = {
            "game_exe_path": self.game_exe_path,
            "savegame_path": self.savegame_path
        }
        with open(SETTINGS_PATH, "w") as f:
            json.dump(data, f, indent=4)


    def checkgamepath(self):
        # Ask for exe if not found
        if not self.game_exe_path or not os.path.exists(self.game_exe_path):
            if gui_enabled:
                new_path = open_filename(
                    "Select Teardown Executable",
                    (("Teardown Executable", ".exe"), ("All Files", "*"))
                )
                if new_path:
                    self.game_exe_path = new_path
                    self.savesettings()

        if not self.savegame_path or not os.path.exists(self.savegame_path):
            if gui_enabled:
                new_save = open_filename(
                    "Select Teardown savegame.xml",
                    (("Teardown Save File", ".xml"), ("All Files", "*"))
                )
                if new_save:
                    self.savegame_path = new_save
                    self.savesettings()

    def sync_savegame(self):
        if not self.savegame_path or not os.path.exists(self.savegame_path):
            return

        try:
            tree = ET.parse(self.savegame_path)
            root = tree.getroot()
            player_data = root.find("mod/steam-3708322400")

            if player_data is not None:
                # Check file to ensure no new completed missions
                self.check_missions_and_tools(player_data)

                # Write newly received items if any
                self.apply_received_items(player_data)

                # Save xml if anything was changed
                tree.write(self.savegame_path, encoding="UTF-8", xml_declaration=True)

        except Exception as e:
            print(f"Error syncing savegame: {e}")


    def check_missions_and_tools(self, player_data):
        # 1. See what mission the game just finished
        lastcompletedmission = player_data.find("lastcompleted")
        if lastcompletedmission is None:
            return
        missionid = lastcompletedmission.get("value")

        if missionid and missionid != "":
            self.complete_mission(missionid)
            mission = player_data.find(f"mission/{missionid}")

            if mission is not None:
                score = mission.find("score")
                if score is not None:
                    # Convert the "score" string (e.g., "3") to an integer
                    current_score = int(score.get("value", "0"))

                    # Logic: Send 'n' locations based on the score
                    # Example: If score is 3, send Location_Mission_1, _2, and _3
                    for i in range(1, current_score + 1):
                        # You'll define this helper to map "lee_login_1", "lee_login_2", etc.
                        loc_name = f"{missionid}_{i}"
                        location_id = self.get_location_id_from_name(loc_name)

                        if location_id and location_id not in self.checked_locations:
                            self.locations_checked.append(location_id)

            # 2. Wipe it immediately so we don't process it again
            lastcompletedmission.set("value", "")


    def complete_mission(self, mission_id: str):
        # 1. Get the index for the mission (e.g., lee_login is index 2)
        index = Missionindex.get(mission_id)

        if index is not None:
            # 2. Get the current string from DataStorage (Default to 40 zeros if empty)
            # We use a temporary key check or a cached value from the server
            current_str = self.slot_data.get("mission_progress", "0" * 40)

            # 3. Convert string to a list so we can change one character
            # Strings are immutable in Python, so we make it a list: ['0','0','0'...]
            list_str = list(current_str)

            # 4. Set the character at our index to '1'
            list_str[index] = "1"

            # 5. Join it back into a string: "0010..."
            new_bin_str = "".join(list_str)

            # 6. Send the whole 40-character string back to the server
            self.set_value("Teardown_Missions", new_bin_str)

            print(f"Mission {mission_id} marked as 1. New Progress: {new_bin_str}")


    def apply_received_items(self, player_data):
        # Clear "lastcompleted" as per your comment to increase data storage number
        last_comp = player_data.find("lastcompleted")
        if last_comp is not None:
            last_comp.set("value", "")

        # Get the tool section
        tool_section = player_data.find("tool")
        if tool_section is None:
            return

        # Iterate through all items received from the Archipelago server
        for network_item in self.items_received:
            tool_name = self.get_tool_name_from_id(network_item.item)
            tool_node = tool_section.find(tool_name)

            if tool_node is not None:
                enabled_node = tool_node.find("enabled")
                if enabled_node is not None:
                    # Flip the value to "1" to unlock it in Teardown
                    enabled_node.set("value", "1")

                # Handle upgrades if the item is an upgrade
                # upgrade_node = tool_node.find("upgrades") ...

    # lvl unlock sets messages from 0 to 1, 2 means completed, doesn't matter
    # check data storage to set mission value, and sent locations to set score value IF mission is completed
    # tool unlock sets enabled value to 1 from 0
    # tool upgrade sets it's specific tool to x*number of upgrades
    # delete the lastcompleted value upon connection and use it to incease data storage number
    # save cash value in data storage

    def launch_game(self):
        if self.game_exe_path and os.path.exists(self.game_exe_path):
            # shell=False is safer; it starts the game as a child process
            subprocess.Popen([self.game_exe_path])
        else:
            print("Cannot launch: Valid executable path not found.")


async def main(args):
    ctx = TeardownContext(args.connect, args.password)
    ctx.auth = args.name
    ctx.checkgamepath()
    ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")

    if gui_enabled:
        ctx.run_gui()
    ctx.run_cli()

    await ctx.exit_event.wait()
    await ctx.shutdown()

import colorama

def launch():
    parser = get_base_parser()

    parser.add_argument('--name', default=None, help="Slot Name to connect as.")

    args = parser.parse_args()
    colorama.init()
    asyncio.run(main(args))
    colorama.deinit()


if __name__ == "__main__":
    launch()