from __future__ import annotations
import os
import sys
import asyncio
import random
from typing import Tuple, List
from worlds.wargroove.Items import faction_table, CommanderData

import ModuleUpdate
ModuleUpdate.update()

import Utils
import json

if __name__ == "__main__":
    Utils.init_logging("WargrooveClient", exception_logger="Client")

from NetUtils import NetworkItem, ClientStatus
from CommonClient import gui_enabled, logger, get_base_parser, ClientCommandProcessor, \
    CommonContext, server_loop


class WargrooveClientCommandProcessor(ClientCommandProcessor):
    def _cmd_resync(self):
        """Manually trigger a resync."""
        self.output(f"Syncing items.")
        self.ctx.syncing = True

    def _cmd_commander(self, commander_name: str = ''):
        """Set the current commander to the given commander."""
        if commander_name:
            self.ctx.set_commander(commander_name)
        else:
            commanders = self.ctx.get_commanders()
            logger.info('Unlocked commanders: ' +
                        ', '.join((commander.name for commander, unlocked in commanders if unlocked))
                        )
            logger.info('Locked commanders: ' +
                        ', '.join((commander.name for commander, unlocked in commanders if not unlocked))
                        )

class WargrooveContext(CommonContext):
    command_processor: int = WargrooveClientCommandProcessor
    game = "Wargroove"
    items_handling = 0b111  # full remote
    current_commander: CommanderData = faction_table["Starter"][0]
    can_choose_commander: bool
    starting_groove_multiplier: float

    def __init__(self, server_address, password):
        super(WargrooveContext, self).__init__(server_address, password)
        self.send_index: int = 0
        self.syncing = False
        self.awaiting_bridge = False
        # self.game_communication_path: files go in this path to pass data between us and the actual game
        if "appdata" in os.environ:
            options = Utils.get_options()
            root_directory = options["wargroove_options"]["root_directory"].replace("/", "\\")
            if not os.path.isfile(root_directory + "\\win64_bin\\wargroove64.exe"):
                msg = "WargrooveClient couldn't find wargroove64.exe. Unable to infer required game_communication_path"
                logger.error("Error: " + msg)
                Utils.messagebox("Error", msg, error=True)
                sys.exit(1)
            self.game_communication_path = root_directory + "\\AP"
            if not os.path.exists(self.game_communication_path):
                os.makedirs(self.game_communication_path)
        else:
            msg = "WargrooveClient couldn't detect system type. Unable to infer required game_communication_path"
            logger.error("Error: " + msg)
            Utils.messagebox("Error", msg, error=True)
            sys.exit(1)

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(WargrooveContext, self).server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    async def connection_closed(self):
        await super(WargrooveContext, self).connection_closed()
        for root, dirs, files in os.walk(self.game_communication_path):
            for file in files:
                if file.find("obtain") <= -1:
                    os.remove(root + "/" + file)

    @property
    def endpoints(self):
        if self.server:
            return [self.server]
        else:
            return []

    async def shutdown(self):
        await super(WargrooveContext, self).shutdown()
        for root, dirs, files in os.walk(self.game_communication_path):
            for file in files:
                if file.find("obtain") <= -1:
                    os.remove(root+"/"+file)

    def on_package(self, cmd: str, args: dict):
        if cmd in {"Connected"}:
            filename = f"AP_settings.json"
            with open(os.path.join(self.game_communication_path, filename), 'w') as f:
                slot_data = args["slot_data"]
                json.dump(args["slot_data"], f)
                self.can_choose_commander = slot_data["can_choose_commander"]
                self.starting_groove_multiplier = slot_data["starting_groove_multiplier"]
                f.close()
            for ss in self.checked_locations:
                filename = f"send{ss}"
                with open(os.path.join(self.game_communication_path, filename), 'w') as f:
                    f.close()
            self.update_commander_data()

            random.seed(self.seed_name + str(self.slot))
            # Our indexes start at 1 and we have 23 levels
            for i in range(1, 24):
                filename = f"seed{i}"
                with open(os.path.join(self.game_communication_path, filename), 'w') as f:
                    f.write(str(random.randint(0, 4294967295)))
                    f.close()

        if cmd in {"RoomInfo"}:
            self.seed_name = args["seed_name"]

        if cmd in {"ReceivedItems"}:
            start_index = args["index"]
            if start_index != len(self.items_received):
                for item in args['items']:
                    network_item = NetworkItem(*item)
                    filename = f"AP_{str(network_item.item)}.item"
                    path = os.path.join(self.game_communication_path, filename)

                    # Newly-obtained items
                    if not os.path.isfile(path):
                        open(path, 'w').close()
                        # Announcing commander unlocks
                        item_name = self.item_names[network_item.item]
                        if item_name in faction_table.keys():
                            for commander in faction_table[item_name]:
                                logger.info(f"{commander.name} has been unlocked!")

                    with open(path, 'r+') as f:
                        line = f.readline()
                        if line is None or line == "" or not line.isnumeric():
                            f.truncate(0)
                            f.seek(0)
                            f.write("1")
                        else:
                            itemCount = int(line) + 1
                            f.truncate(0)
                            f.seek(0)
                            f.write(f"{itemCount}")
                        f.close()

                    print_filename = f"AP_{str(network_item.item)}.item.print"
                    print_path = os.path.join(self.game_communication_path, print_filename)
                    if not os.path.isfile(print_path):
                        open(print_path, 'w').close()
                    with open(print_path, 'w') as f:
                        f.write("Received " +
                                self.item_names[network_item.item] +
                                " from " +
                                self.player_names[network_item.player])
                        f.close()
                self.update_commander_data()

        if cmd in {"RoomUpdate"}:
            if "checked_locations" in args:
                for ss in self.checked_locations:
                    filename = f"send{ss}"
                    with open(os.path.join(self.game_communication_path, filename), 'w') as f:
                        f.close()

    def run_gui(self):
        """Import kivy UI system and start running it as self.ui_task."""
        from kvui import GameManager

        class WargrooveManager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago")
            ]
            base_title = "Archipelago Wargroove Client"

        self.ui = WargrooveManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")

    def update_commander_data(self):
        faction_items = 0
        faction_item_names = [faction + ' Commanders' for faction in faction_table.keys()]
        for network_item in self.items_received:
            if self.item_names[network_item.item] in faction_item_names:
                faction_items += 1
        starting_groove = (faction_items - 1) * self.starting_groove_multiplier
        # Must be an integer larger than 0
        starting_groove = int(max(starting_groove, 0))
        data = {
            "commander": self.current_commander.internal_name,
            "starting_groove": starting_groove
        }
        filename = 'commander.json'
        with open(os.path.join(self.game_communication_path, filename), 'w') as f:
            json.dump(data, f)

    def set_commander(self, commander_name: str) -> bool:
        """Sets the current commander to the given one, if possible"""
        if not self.can_choose_commander:
            logger.error("Cannot set commanders in this game mode.")
            return
        match_name = commander_name.lower()
        for commander, unlocked in self.get_commanders():
            if commander.name.lower() == match_name or commander.alt_name and commander.alt_name.lower() == match_name:
                if unlocked:
                    self.current_commander = commander
                    self.syncing = True
                    logger.info(f"Commander set to {commander.name}.")
                    self.update_commander_data()
                    return True
                else:
                    logger.error(f"Commander {commander.name} has not been unlocked.")
                    return False
        else:
            logger.error(f"{commander_name} is not a recognized Wargroove commander.")

    def get_commanders(self) -> List[Tuple[CommanderData, bool]]:
        """Gets a list of commanders with their unlocked status"""
        received_item_names = (self.item_names[network_item.item] for network_item in self.items_received)
        received_factions = {item_name[:-11] for item_name in received_item_names if item_name.endswith(' Commanders')}
        for faction in received_factions:
            print('received', faction)
        commanders = []
        for faction in faction_table.keys():
            unlocked = faction == 'Starter' or str(faction) in received_factions
            print(faction, unlocked)
            commanders += [(commander, unlocked) for commander in faction_table[faction]]
        return commanders


async def game_watcher(ctx: WargrooveContext):
    from worlds.wargroove.Locations import location_table
    while not ctx.exit_event.is_set():
        if ctx.syncing == True:
            sync_msg = [{'cmd': 'Sync'}]
            if ctx.locations_checked:
                sync_msg.append({"cmd": "LocationChecks", "locations": list(ctx.locations_checked)})
            await ctx.send_msgs(sync_msg)
            ctx.syncing = False
        sending = []
        victory = False
        for root, dirs, files in os.walk(ctx.game_communication_path):
            for file in files:
                if file.find("send") > -1:
                    st = file.split("send", -1)[1]
                    sending = sending+[(int(st))]
                if file.find("victory") > -1:
                    victory = True
        ctx.locations_checked = sending
        message = [{"cmd": 'LocationChecks', "locations": sending}]
        await ctx.send_msgs(message)
        if not ctx.finished_game and victory:
            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
            ctx.finished_game = True
        await asyncio.sleep(0.1)


if __name__ == '__main__':
    async def main(args):
        ctx = WargrooveContext(args.connect, args.password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()
        progression_watcher = asyncio.create_task(
            game_watcher(ctx), name="WargrooveProgressionWatcher")

        await ctx.exit_event.wait()
        ctx.server_address = None

        await progression_watcher

        await ctx.shutdown()

    import colorama

    parser = get_base_parser(description="Wargroove Client, for text interfacing.")

    args, rest = parser.parse_known_args()
    colorama.init()
    asyncio.run(main(args))
    colorama.deinit()
