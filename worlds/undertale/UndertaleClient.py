from __future__ import annotations
import os
import asyncio
import typing
import bsdiff4
import shutil
import platformdirs
import platform
import uuid

import Utils

from typing import List, Tuple
from NetUtils import NetworkItem, ClientStatus
from . import data_path
from .Locations import advancement_table
from MultiServer import mark_raw
from CommonClient import CommonContext, server_loop, \
    gui_enabled, ClientCommandProcessor, logger, get_base_parser
from Utils import async_start

undertale_gifting_options = {
    "AcceptsAnyGift": False,
    "DesiredTraits": [
        "Trap", "Heal", "Speed", "Consumable", "Food", "Heal", "Health"
    ],
    "MinimumGiftVersion": 2,
}

undertale_gifts = {
    "1": {
        "ItemName": "Monster Candy",
        "Amount": 1,
        "ItemValue": 0,
        "Traits": [
            {
                "Trait": "Consumable",
                "Quality": 0.45,
                "Duration": 1,
            },
            {
                "Trait": "Heal",
                "Quality": 0.45,
                "Duration": 1,
            }
        ]
    },
    "7": {
        "ItemName": "Spider Donut",
        "Amount": 1,
        "ItemValue": 0,
        "Traits": [
            {
                "Trait": "Consumable",
                "Quality": 0.54,
                "Duration": 1,
            },
            {
                "Trait": "Heal",
                "Quality": 0.54,
                "Duration": 1,
            }
        ]
    },
    "10": {
        "ItemName": "Spider Cider",
        "Amount": 1,
        "ItemValue": 0,
        "Traits": [
            {
                "Trait": "Consumable",
                "Quality": 1.09,
                "Duration": 1,
            },
            {
                "Trait": "Heal",
                "Quality": 1.09,
                "Duration": 1,
            }
        ]
    },
    "11": {
        "ItemName": "Butterscotch Pie",
        "Amount": 1,
        "ItemValue": 0,
        "Traits": [
            {
                "Trait": "Consumable",
                "Quality": 4.5,
                "Duration": 1,
            },
            {
                "Trait": "Heal",
                "Quality": 4.5,
                "Duration": 1,
            }
        ]
    },
    "63": {
        "ItemName": "Snail Pie",
        "Amount": 1,
        "ItemValue": 0,
        "Traits": [
            {
                "Trait": "Consumable",
                "Quality": 4.45,
                "Duration": 1,
            },
            {
                "Trait": "Heal",
                "Quality": 4.45,
                "Duration": 1,
            }
        ]
    },
    "16": {
        "ItemName": "Snowman Piece",
        "Amount": 1,
        "ItemValue": 0,
        "Traits": [
            {
                "Trait": "Consumable",
                "Quality": 2.04,
                "Duration": 1,
            },
            {
                "Trait": "Heal",
                "Quality": 2.04,
                "Duration": 1,
            }
        ]
    },
    "17": {
        "ItemName": "Nice Cream",
        "Amount": 1,
        "ItemValue": 0,
        "Traits": [
            {
                "Trait": "Consumable",
                "Quality": 0.68,
                "Duration": 1,
            },
            {
                "Trait": "Heal",
                "Quality": 0.68,
                "Duration": 1,
            }
        ]
    },
    "19": {
        "ItemName": "Bisicle",
        "Amount": 1,
        "ItemValue": 0,
        "Traits": [
            {
                "Trait": "Consumable",
                "Quality": 1,
                "Duration": 1,
            },
            {
                "Trait": "Heal",
                "Quality": 1,
                "Duration": 1,
            }
        ]
    },
    "20": {
        "ItemName": "Unisicle",
        "Amount": 1,
        "ItemValue": 0,
        "Traits": [
            {
                "Trait": "Consumable",
                "Quality": 0.5,
                "Duration": 1,
            },
            {
                "Trait": "Heal",
                "Quality": 0.5,
                "Duration": 1,
            }
        ]
    },
    "21": {
        "ItemName": "Cinnamon Bunny",
        "Amount": 1,
        "ItemValue": 0,
        "Traits": [
            {
                "Trait": "Consumable",
                "Quality": 1,
                "Duration": 1,
            },
            {
                "Trait": "Heal",
                "Quality": 1,
                "Duration": 1,
            }
        ]
    },
    "35": {
        "ItemName": "Astronaut Food",
        "Amount": 1,
        "ItemValue": 0,
        "Traits": [
            {
                "Trait": "Consumable",
                "Quality": 0.95,
                "Duration": 1,
            },
            {
                "Trait": "Heal",
                "Quality": 0.95,
                "Duration": 1,
            }
        ]
    },
    "37": {
        "ItemName": "Crab Apple",
        "Amount": 1,
        "ItemValue": 0,
        "Traits": [
            {
                "Trait": "Consumable",
                "Quality": 0.81,
                "Duration": 1,
            },
            {
                "Trait": "Heal",
                "Quality": 0.81,
                "Duration": 1,
            }
        ]
    },
    "41": {
        "ItemName": "Sea Tea",
        "Amount": 1,
        "ItemValue": 0,
        "Traits": [
            {
                "Trait": "Consumable",
                "Quality": 0.6,
                "Duration": 1,
            },
            {
                "Trait": "Heal",
                "Quality": 0.45,
                "Duration": 1,
            },
            {
                "Trait": "Speed",
                "Quality": 1,
                "Duration": 1,
            }
        ]
    },
    "23": {
        "ItemName": "Abandoned Quiche",
        "Amount": 1,
        "ItemValue": 0,
        "Traits": [
            {
                "Trait": "Consumable",
                "Quality": 1.54,
                "Duration": 1,
            },
            {
                "Trait": "Heal",
                "Quality": 1.54,
                "Duration": 1,
            }
        ]
    },
    "22": {
        "ItemName": "Temmie Flakes",
        "Amount": 1,
        "ItemValue": 0,
        "Traits": [
            {
                "Trait": "Consumable",
                "Quality": 0.09,
                "Duration": 1,
            },
            {
                "Trait": "Heal",
                "Quality": 0.09,
                "Duration": 1,
            }
        ]
    },
    "28": {
        "ItemName": "Dog Salad",
        "Amount": 1,
        "ItemValue": 0,
        "Traits": [
            {
                "Trait": "Consumable",
                "Quality": 0.45,
                "Duration": 1,
            },
            {
                "Trait": "Heal",
                "Quality": 0.45,
                "Duration": 1,
            }
        ]
    },
    "36": {
        "ItemName": "Instant Noodles",
        "Amount": 1,
        "ItemValue": 0,
        "Traits": [
            {
                "Trait": "Consumable",
                "Quality": 2.72,
                "Duration": 1,
            },
            {
                "Trait": "Heal",
                "Quality": 2.72,
                "Duration": 1,
            }
        ]
    },
    "38": {
        "ItemName": "Hot Dog...?",
        "Amount": 1,
        "ItemValue": 0,
        "Traits": [
            {
                "Trait": "Consumable",
                "Quality": 0.9,
                "Duration": 1,
            },
            {
                "Trait": "Heal",
                "Quality": 0.9,
                "Duration": 1,
            }
        ]
    },
    "39": {
        "ItemName": "Hot Cat",
        "Amount": 1,
        "ItemValue": 0,
        "Traits": [
            {
                "Trait": "Consumable",
                "Quality": 0.95,
                "Duration": 1,
            },
            {
                "Trait": "Heal",
                "Quality": 0.95,
                "Duration": 1,
            }
        ]
    },
    "59": {
        "ItemName": "Junk Food",
        "Amount": 1,
        "ItemValue": 0,
        "Traits": [
            {
                "Trait": "Consumable",
                "Quality": 0.77,
                "Duration": 1,
            },
            {
                "Trait": "Heal",
                "Quality": 0.77,
                "Duration": 1,
            }
        ]
    },
    "62": {
        "ItemName": "Hush Puppy",
        "Amount": 1,
        "ItemValue": 0,
        "Traits": [
            {
                "Trait": "Consumable",
                "Quality": 2.96,
                "Duration": 1,
            },
            {
                "Trait": "Heal",
                "Quality": 2.96,
                "Duration": 1,
            }
        ]
    },
    "42": {
        "ItemName": "Starfait",
        "Amount": 1,
        "ItemValue": 0,
        "Traits": [
            {
                "Trait": "Consumable",
                "Quality": 0.63,
                "Duration": 1,
            },
            {
                "Trait": "Heal",
                "Quality": 0.63,
                "Duration": 1,
            }
        ]
    },
    "40": {
        "ItemName": "Glamburger",
        "Amount": 1,
        "ItemValue": 0,
        "Traits": [
            {
                "Trait": "Consumable",
                "Quality": 1.22,
                "Duration": 1,
            },
            {
                "Trait": "Heal",
                "Quality": 1.22,
                "Duration": 1,
            }
        ]
    },
    "43": {
        "ItemName": "Legendary Hero",
        "Amount": 1,
        "ItemValue": 0,
        "Traits": [
            {
                "Trait": "Consumable",
                "Quality": 1.81,
                "Duration": 1,
            },
            {
                "Trait": "Heal",
                "Quality": 1.81,
                "Duration": 1,
            }
        ]
    },
    "61": {
        "ItemName": "Face Steak",
        "Amount": 1,
        "ItemValue": 0,
        "Traits": [
            {
                "Trait": "Consumable",
                "Quality": 2.72,
                "Duration": 1,
            },
            {
                "Trait": "Heal",
                "Quality": 2.72,
                "Duration": 1,
            }
        ]
    },
    "58": {
        "ItemName": "Popato Chisps",
        "Amount": 1,
        "ItemValue": 0,
        "Traits": [
            {
                "Trait": "Consumable",
                "Quality": 0.59,
                "Duration": 1,
            },
            {
                "Trait": "Heal",
                "Quality": 0.59,
                "Duration": 1,
            }
        ]
    },
    "18": {
        "ItemName": "Puppydough Icecream",
        "Amount": 1,
        "ItemValue": 0,
        "Traits": [
            {
                "Trait": "Consumable",
                "Quality": 1.27,
                "Duration": 1,
            },
            {
                "Trait": "Heal",
                "Quality": 1.27,
                "Duration": 1,
            }
        ]
    },
    "6": {
        "ItemName": "Pumpkin Rings",
        "Amount": 1,
        "ItemValue": 0,
        "Traits": [
            {
                "Trait": "Consumable",
                "Quality": 0.36,
                "Duration": 1,
            },
            {
                "Trait": "Heal",
                "Quality": 0.36,
                "Duration": 1,
            }
        ]
    },
    "2": {
        "ItemName": "Croquet Roll",
        "Amount": 1,
        "ItemValue": 0,
        "Traits": [
            {
                "Trait": "Consumable",
                "Quality": 0.68,
                "Duration": 1,
            },
            {
                "Trait": "Heal",
                "Quality": 0.68,
                "Duration": 1,
            }
        ]
    },
    "9": {
        "ItemName": "Ghost Fruit",
        "Amount": 1,
        "ItemValue": 0,
        "Traits": [
            {
                "Trait": "Consumable",
                "Quality": 0.72,
                "Duration": 1,
            },
            {
                "Trait": "Heal",
                "Quality": 0.72,
                "Duration": 1,
            }
        ]
    },
    "8": {
        "ItemName": "Stoic Onion",
        "Amount": 1,
        "ItemValue": 0,
        "Traits": [
            {
                "Trait": "Consumable",
                "Quality": 0.22,
                "Duration": 1,
            },
            {
                "Trait": "Heal",
                "Quality": 0.22,
                "Duration": 1,
            }
        ]
    },
    "5": {
        "ItemName": "Rock Candy",
        "Amount": 1,
        "ItemValue": 0,
        "Traits": [
            {
                "Trait": "Consumable",
                "Quality": 0.04,
                "Duration": 1,
            },
            {
                "Trait": "Heal",
                "Quality": 0.04,
                "Duration": 1,
            }
        ]
    },
}


async def pop_object(ctx, key: str, value: str):
    await ctx.send_msgs([
        {
            "cmd": "Set",
            "key": key,
            "default": {},
            "want_reply": False,
            "operations": [
                {"operation": "pop", "value": value}
            ]
        }
    ])


async def pick_gift_recipient(ctx, gift):
    gift_base = undertale_gifts[gift.split("]:::[", maxsplit=1)[0]]
    most_applicable_slot: str = gift.split("]:::[", maxsplit=1)[1]
    chosen_slot = ctx.slot
    for slot in ctx.player_names:
        if ctx.player_names[slot] == most_applicable_slot:
            chosen_slot = slot
            break
    found_giftee = False
    for slot, info in ctx.stored_data[ctx.motherbox_key].items():
        if int(slot) == chosen_slot:
            found_giftee = True
            desire = len(set(info["DesiredTraits"]).intersection([trait["Trait"] for trait in gift_base["Traits"]]))
            if not info["IsOpen"] or (desire <= 0 and not info["AcceptsAnyGift"]):
                chosen_slot = ctx.slot
    if not found_giftee:
        chosen_slot = ctx.slot
    item_uuid = uuid.uuid4().hex
    item = {
        **gift_base,
        "ID": item_uuid,
        "Sender": ctx.player_names[ctx.slot],
        "Receiver": ctx.player_names[chosen_slot],
        "SenderTeam": ctx.team,
        "ReceiverTeam": ctx.team,  # for the moment
        "IsRefund": False
    }
    # print(item)
    # print(str(gift.split("]:::[", maxsplit=1)[0]))
    if chosen_slot == ctx.slot:
        filename = f"fail.gift"
        with open(os.path.join(ctx.save_game_folder, filename), "a") as f:
            f.write(gift.split("]:::[", maxsplit=1)[0]+"\n")
            f.close()
    else:
        await update_object(ctx, f"Giftbox;{ctx.team};{chosen_slot}", {
            item_uuid: item,
        })


async def pop_gift(ctx):
    if ctx.giftbox_key in ctx.stored_data.keys():
        if ctx.stored_data[ctx.giftbox_key]:
            key, gift = ctx.stored_data[ctx.giftbox_key].popitem()
            await pop_object(ctx, ctx.giftbox_key, key)
            # first, special cases
            item_to_write = "22"
            traits = [trait["Trait"] for trait in gift["Traits"]]
            qualities = [quality["Quality"] for quality in gift["Traits"]]
            if "Trap" in traits:
                item_to_write = "trap"
            elif "Speed" in traits:
                item_to_write = "41"
            elif any(x in traits for x in ["Consumable", "Food", "Heal", "Health"]):
                closeness = 999999
                for item in undertale_gifts:
                    if abs(undertale_gifts[item]["Traits"][0]["Quality"]-qualities[traits.index("Consumable")]) < closeness:
                        closeness = abs(undertale_gifts[item]["Traits"][0]["Quality"]-qualities[traits.index("Consumable")])
                        item_to_write = item
            filename = f"add.gift"
            # print(str(item_to_write))
            with open(os.path.join(ctx.save_game_folder, filename), "a") as f:
                f.write(str(item_to_write)+"\n")
                f.close()


async def update_object(ctx, key: str, value: typing.Dict):
    await ctx.send_msgs([
        {
            "cmd": "Set",
            "key": key,
            "default": {},
            "want_reply": False,
            "operations": [
                {"operation": "update", "value": value}
            ]
        }
    ])


async def initialize_giftboxes(ctx, giftbox_key: str, motherbox_key: str, is_open: bool):
    ctx.set_notify(motherbox_key, giftbox_key)
    await update_object(ctx, f"Giftboxes;{ctx.team}", {f"{ctx.slot}":
        {
            "IsOpen": is_open,
            **undertale_gifting_options
        }})
    ctx.gifting = is_open


class UndertaleCommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx):
        super().__init__(ctx)

    # def _cmd_gift(self):
    #         """Toggles gifting for the current game."""
    #         if not getattr(self.ctx, "gifting", None):
    #             self.ctx.gifting = True
    #         else:
    #             self.ctx.gifting = not self.ctx.gifting
    #         self.output(f"Gifting set to {self.ctx.gifting}")
    #         async_start(update_object(self.ctx, f"Giftboxes;{self.ctx.team}",
    #                                  {f"{self.ctx.slot}": {"IsOpen": self.ctx.gifting, **undertale_gifting_options}}))

    def _cmd_patch(self):
        """Patch the game. Only use this command if /auto_patch fails."""
        if isinstance(self.ctx, UndertaleContext):
            os.makedirs(name=os.path.join(os.getcwd(), "Undertale"), exist_ok=True)
            self.ctx.patch_game()
            self.output("Patched.")

    def _cmd_savepath(self, directory: str):
        """Redirect to proper save data folder. This is necessary for Linux users to use before connecting."""
        if isinstance(self.ctx, UndertaleContext):
            self.ctx.save_game_folder = directory
            self.output("Changed to the following directory: " + self.ctx.save_game_folder)

    @mark_raw
    def _cmd_auto_patch(self, steaminstall: typing.Optional[str] = ""):
        """Patch the game automatically."""
        if isinstance(self.ctx, UndertaleContext):
            if platform.system() == "Linux":
                os.makedirs(name=os.path.expanduser("~/Archipelago/Undertale/assets"), exist_ok=True)
            else:
                os.makedirs(name=os.path.join(os.getcwd(), "Undertale"), exist_ok=True)
            tempInstall = steaminstall
            if tempInstall is not None:
                if platform.system() == "Linux":
                    if not os.path.isfile(os.path.join(tempInstall, "assets", "game.unx")):
                        tempInstall = None
                else:
                    if not os.path.isfile(os.path.join(tempInstall, "data.win")):
                        tempInstall = None
            if tempInstall is None:
                if platform.system() == "Linux":
                    tempInstall = os.path.expanduser("~/.steam/steam/steamapps/common/Undertale/")
                else:
                    tempInstall = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Undertale"
                    if not os.path.exists(tempInstall):
                        tempInstall = "C:\\Program Files\\Steam\\steamapps\\common\\Undertale"
            elif not os.path.exists(tempInstall) and platform.system() != "Linux":
                tempInstall = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Undertale"
                if not os.path.exists(tempInstall):
                    tempInstall = "C:\\Program Files\\Steam\\steamapps\\common\\Undertale"
            if platform.system() == "Linux":
                if not os.path.exists(tempInstall) or \
                        not os.path.isfile(os.path.join(tempInstall, "assets", "game.unx")):
                    self.output("ERROR: Cannot find Undertale. Please rerun the command with the correct folder."
                                " command. \"/auto_patch (Undertale directory)\".")
                else:
                    shutil.copytree(os.path.join(tempInstall), os.path.expanduser("~/Archipelago/Undertale"),
                                    dirs_exist_ok=True)
                    self.ctx.patch_game()
                    self.output("Patching successful!")
            else:
                if not os.path.exists(tempInstall) or not os.path.isfile(os.path.join(tempInstall, "data.win")):
                    self.output("ERROR: Cannot find Undertale. Please rerun the command with the correct folder."
                                " command. \"/auto_patch (Undertale directory)\".")
                else:
                    shutil.copytree(os.path.join(tempInstall), os.path.join(os.getcwd(), "Undertale"),
                                    dirs_exist_ok=True)
                    for file_name in os.listdir(os.path.join(os.getcwd(), "Undertale")):
                        if file_name == "steam_api.dll":
                            os.remove(os.path.join(os.getcwd(), "Undertale", file_name))
                        if file_name == "UNDERTALE.exe":
                            os.rename(os.path.join(os.getcwd(), "Undertale", file_name), os.path.join(os.getcwd(), "Undertale", "UNDERTALEAP.exe"))
                    self.ctx.patch_game()
                    self.output("Patching successful!")

    def _cmd_online(self):
        """Toggles seeing other Undertale players."""
        if isinstance(self.ctx, UndertaleContext):
            self.ctx.update_online_mode(not ("Online" in self.ctx.tags))
            if "Online" in self.ctx.tags:
                self.output(f"Now online.")
            else:
                self.output(f"Now offline.")

    def _cmd_deathlink(self):
        """Toggles deathlink"""
        if isinstance(self.ctx, UndertaleContext):
            self.ctx.deathlink_status = not self.ctx.deathlink_status
            if self.ctx.deathlink_status:
                self.output(f"Deathlink enabled.")
            else:
                self.output(f"Deathlink disabled.")


class UndertaleContext(CommonContext):
    tags = {"AP", "Online"}
    game = "Undertale"
    command_processor = UndertaleCommandProcessor
    items_handling = 0b111
    route = None
    pieces_needed = None
    completed_routes = None
    completed_count = 0
    kill_pack_size = None
    spare_pack_size = None
    spare_max = None
    giftbox_key = ""
    motherbox_key = ""
    enable_gifting = False
    gifting = False
    initialize_gifting = False
    entrances: List[Tuple[str, str]] = None
    locked_doors: List[str] = None
    save_game_folder = platformdirs.user_config_dir(appname="UNDERTALEAP", ensure_exists=True, appauthor=False)

    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.pieces_needed = 0
        self.kill_pack_size = 1
        self.spare_pack_size = 1
        self.spare_max = 0
        self.finished_game = False
        self.game = "Undertale"
        self.got_deathlink = False
        self.giftbox_key = ""
        self.motherbox_key = ""
        self.enable_gifting = False
        self.gifting = False
        self.initialize_gifting = False
        self.deathlink_status = False
        self.tem_armor = False
        self.entrances = []
        self.locked_doors = []
        self.completed_count = 0
        self.completed_routes = {"pacifist": 0, "genocide": 0, "neutral": 0}
        # self.save_game_folder: files go in this path to pass data between us and the actual game
        self.save_game_folder = platformdirs.user_config_dir(appname="UNDERTALEAP", ensure_exists=True, appauthor=False)
        # print(self.save_game_folder)

    def patch_game(self):
        if os.path.isfile(os.path.join(os.getcwd(), "Undertale", "data.win")):
            with open(os.path.join(os.getcwd(), "Undertale", "data.win"), "rb") as f:
                patchedFile = bsdiff4.patch(f.read(), data_path("patch.bsdiff"))
            with open(os.path.join(os.getcwd(), "Undertale", "data.win"), "wb") as f:
                f.write(patchedFile)
        os.makedirs(name=os.path.join(os.getcwd(), "Undertale", "Custom Sprites"), exist_ok=True)
        with open(os.path.expandvars(os.path.join(os.getcwd(), "Undertale", "Custom Sprites",
                                                  "which_character.txt")), "w") as f:
            f.writelines(["// Put the folder name of the sprites you want to play as, make sure it is the only "
                          "line other than this one.\n", "frisk"])
            f.close()

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super().server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    def clear_undertale_files(self):
        path = self.save_game_folder
        self.finished_game = False
        for root, dirs, files in os.walk(path):
            for file in files:
                try:
                    if "total_pieces" == file or "add.gift" == file or "remove.gift" == file or "doorlock.locked" == file or "team_players" == file or "doorcheck.doorspot" == file or "check.spot" == file or "scout" == file or "entrance_rando.dest" == file or \
                            "roomrando.enabled" == file:
                        os.remove(os.path.join(root, file))
                    elif file.endswith(("only_tem", "disconnected", "connected", ".item", "items.itsem", ".victory", ".route", ".playerspot", ".mad",
                                        ".youdied", ".lv", ".flag", ".hint", ".pack", "roomrando", "no_chest", "hub_shop_cost", "hub_shop_count", "allow_gifting")):
                        os.remove(os.path.join(root, file))
                except Exception as error:
                    print(str(error))

    async def connect(self, address: typing.Optional[str] = None):
        self.clear_undertale_files()
        await super().connect(address)

    async def disconnect(self, allow_autoreconnect: bool = False):
        self.clear_undertale_files()
        await super().disconnect(allow_autoreconnect)

    async def connection_closed(self):
        self.clear_undertale_files()
        filename = f"disconnected"
        with open(os.path.join(self.save_game_folder, filename), "w") as f:
            f.close()
        await super().connection_closed()

    async def shutdown(self):
        self.clear_undertale_files()
        await super().shutdown()

    def update_online_mode(self, online):
        old_tags = self.tags.copy()
        if online:
            self.tags.add("Online")
        else:
            self.tags -= {"Online"}
        if old_tags != self.tags and self.server and not self.server.socket.closed:
            async_start(self.send_msgs([{"cmd": "ConnectUpdate", "tags": self.tags}]))

    def on_package(self, cmd: str, args: dict):
        if cmd == "Connected":
            self.game = self.slot_info[self.slot].game
        async_start(process_undertale_cmd(self, cmd, args))

    def run_gui(self):
        from kvui import GameManager

        class UTManager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago")
            ]
            base_title = "Archipelago Undertale Client"

        self.ui = UTManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")

    def on_deathlink(self, data: typing.Dict[str, typing.Any]):
        self.got_deathlink = True
        super().on_deathlink(data)


async def process_undertale_cmd(ctx: UndertaleContext, cmd: str, args: dict):
    if cmd == "Connected":
        if not os.path.exists(ctx.save_game_folder):
            os.mkdir(ctx.save_game_folder)
        ctx.route = args["slot_data"]["route_required"]
        ctx.pieces_needed = args["slot_data"]["key_pieces"]
        with open(os.path.join(ctx.save_game_folder, "total_pieces"), "w") as f:
            f.write(str(ctx.pieces_needed))
            f.close()
        ctx.kill_pack_size = args["slot_data"]["kill_sanity_pack_size"]
        ctx.spare_pack_size = args["slot_data"]["spare_sanity_pack_size"]
        ctx.spare_max = args["slot_data"]["spare_sanity_max"]
        ctx.tem_armor = args["slot_data"]["temy_include"]
        ctx.locked_doors = args["slot_data"]["Locked Doors"]
        if len(ctx.locked_doors) > 0:
            with open(os.path.join(ctx.save_game_folder, "doorlock.locked"), "w") as f:
                for item in ctx.locked_doors:
                    f.write(item + "\n")
                f.close()

        await ctx.send_msgs([{"cmd": "Get", "keys": [str(ctx.slot) + " RoutesDone neutral",
                                                     str(ctx.slot) + " RoutesDone pacifist",
                                                     str(ctx.slot) + " RoutesDone genocide"]}])
        await ctx.send_msgs([{"cmd": "SetNotify", "keys": [str(ctx.slot) + " RoutesDone neutral",
                                                           str(ctx.slot) + " RoutesDone pacifist",
                                                           str(ctx.slot) + " RoutesDone genocide"]}])
        if args["slot_data"]["only_flakes"]:
            with open(os.path.join(ctx.save_game_folder, "genonochest.flag"), "w") as f:
                f.close()
        if args["slot_data"]["spare_sanity"]:
            with open(os.path.join(ctx.save_game_folder, "spare_sanity.flag"), "w") as f:
                f.close()
        if args["slot_data"]["key_hunt"]:
            with open(os.path.join(ctx.save_game_folder, "key_hunt.flag"), "w") as f:
                f.close()
        if args["slot_data"]["kill_sanity"] != "off":
            with open(os.path.join(ctx.save_game_folder, "kill_sanity.flag"), "w") as f:
                f.close()
        if args["slot_data"]["entrance_rando"]:
            ctx.entrances = args["slot_data"]["Entrance Rando"]
            with open(os.path.join(ctx.save_game_folder, "roomrando.enabled"), "w") as f:
                f.close()
            filename = f"entrance_rando.dest"
            with open(os.path.join(ctx.save_game_folder, filename), "w") as f:
                for item in ctx.entrances:
                    f.write(item[0] + "\n" + item[1] + "\n")
                f.close()
        ctx.enable_gifting = bool(args["slot_data"]["gifting"])

        if not args["slot_data"]["key_hunt"]:
            ctx.pieces_needed = 0
        if args["slot_data"]["rando_love"]:
            filename = f"loverando.lv"
            with open(os.path.join(ctx.save_game_folder, filename), "w") as f:
                f.close()
        if args["slot_data"]["only_flakes"]:
            filename = f"only_tem"
            with open(os.path.join(ctx.save_game_folder, filename), "w") as f:
                f.close()
        with open(os.path.join(ctx.save_game_folder, f"allow_gifting"), "w") as f:
            f.write(str(ctx.enable_gifting))
            f.close()
        with open(os.path.join(ctx.save_game_folder, f"hub_shop_cost"), "w") as f:
            f.write(str(args["slot_data"]["hub_shop_cost"]))
            f.close()
        all_locs = ctx.server_locations
        counter = 1
        while counter in all_locs:
            counter += 1
        counter -= 1
        with open(os.path.join(ctx.save_game_folder, f"hub_shop_count"), "w") as f:
            f.write(str(counter))
            f.close()
        if args["slot_data"]["rando_stats"]:
            filename = f"statrando.lv"
            with open(os.path.join(ctx.save_game_folder, filename), "w") as f:
                f.close()
        if not args["slot_data"]["bonus_locations"]:
            filename = f"no_chest"
            with open(os.path.join(ctx.save_game_folder, filename), "w") as f:
                f.close()
        filename = f"{ctx.route}.route"
        with open(os.path.join(ctx.save_game_folder, filename), "w") as f:
            f.close()
        filename = f"kill_size.pack"
        with open(os.path.join(ctx.save_game_folder, filename), "w") as f:
            f.write(str(ctx.kill_pack_size) + "\n")
            f.close()
        filename = f"spare_size.pack"
        with open(os.path.join(ctx.save_game_folder, filename), "w") as f:
            f.write(str(ctx.spare_pack_size) + "\n")
            f.close()
        filename = f"spare_max.pack"
        with open(os.path.join(ctx.save_game_folder, filename), "w") as f:
            f.write(str(ctx.spare_max) + "\n")
            f.close()
        filename = f"check.spot"
        with open(os.path.join(ctx.save_game_folder, filename), "a") as f:
            for ss in set(args["checked_locations"]):
                f.write(str(ss - 12000) + "\n")
            f.close()
        filename = f"team_players"
        with open(os.path.join(ctx.save_game_folder, filename), "w") as f:
            f.write(str(len(ctx.player_names))+"\n")
            for ss in ctx.player_names:
                if ctx.player_names[ss] != "Archipelago":
                    f.write(ctx.player_names[ss]+"\n")
            f.close()
        ctx.giftbox_key = f"Giftbox;{ctx.team};{ctx.slot}"
        ctx.motherbox_key = f"Giftboxes;{ctx.team}"
        await initialize_giftboxes(ctx, ctx.giftbox_key, ctx.motherbox_key, ctx.enable_gifting)
        ctx.initialize_gifting = True
        filename = f"connected"
        with open(os.path.join(ctx.save_game_folder, filename), "w") as f:
            f.close()
    elif cmd == "LocationInfo":
        for loc in args["locations"]:
            locationid = NetworkItem(*loc).location
            filename = f"{str(locationid - 12000)}.hint"
            with open(os.path.join(ctx.save_game_folder, filename), "w") as f:
                toDraw = ""
                for i in range(20):
                    if i < len(str(ctx.item_names.lookup_in_slot(NetworkItem(*loc).item, NetworkItem(*loc).player))):
                        toDraw += str(ctx.item_names.lookup_in_slot(NetworkItem(*loc).item, NetworkItem(*loc).player))[i]
                    else:
                        break
                f.write(toDraw)
                f.close()
    elif cmd == "Retrieved":
        if str(ctx.slot) + " RoutesDone neutral" in args["keys"]:
            if args["keys"][str(ctx.slot) + " RoutesDone neutral"] is not None:
                ctx.completed_routes["neutral"] = args["keys"][str(ctx.slot) + " RoutesDone neutral"]
        if str(ctx.slot) + " RoutesDone genocide" in args["keys"]:
            if args["keys"][str(ctx.slot) + " RoutesDone genocide"] is not None:
                ctx.completed_routes["genocide"] = args["keys"][str(ctx.slot) + " RoutesDone genocide"]
        if str(ctx.slot) + " RoutesDone pacifist" in args["keys"]:
            if args["keys"][str(ctx.slot) + " RoutesDone pacifist"] is not None:
                ctx.completed_routes["pacifist"] = args["keys"][str(ctx.slot) + " RoutesDone pacifist"]
    elif cmd == "SetReply":
        if args["value"] is not None:
            if str(ctx.slot) + " RoutesDone pacifist" == args["key"]:
                ctx.completed_routes["pacifist"] = args["value"]
            elif str(ctx.slot) + " RoutesDone genocide" == args["key"]:
                ctx.completed_routes["genocide"] = args["value"]
            elif str(ctx.slot) + " RoutesDone neutral" == args["key"]:
                ctx.completed_routes["neutral"] = args["value"]
    elif cmd == "ReceivedItems":
        start_index = args["index"]

        if start_index == 0:
            ctx.items_received = []
        elif start_index != len(ctx.items_received):
            sync_msg = [{"cmd": "Sync"}]
            if ctx.locations_checked:
                sync_msg.append({"cmd": "LocationChecks",
                                 "locations": list(ctx.locations_checked)})
            await ctx.send_msgs(sync_msg)
        if start_index == len(ctx.items_received):
            counter = -1
            placedWeapon = 0
            placedArmor = 0
            filename = "items.itsem"
            with open(os.path.join(ctx.save_game_folder, filename), "w") as f:
                f.close()
            for item in args["items"]:
                itm_id = NetworkItem(*item).location
                while NetworkItem(*item).location < 0 and \
                        counter <= itm_id:
                    itm_id -= 1
                if NetworkItem(*item).location < 0:
                    counter -= 1
                if 2000 >= NetworkItem(*item).item >= 1000:
                    if ctx.item_names.lookup_in_game(NetworkItem(*item).item).removeprefix("Door Unlock - ") in ctx.locked_doors:
                        ctx.locked_doors.remove(ctx.item_names.lookup_in_game(NetworkItem(*item).item).removeprefix("Door Unlock - "))
                else:
                    filename = "items.itsem"
                    with open(os.path.join(ctx.save_game_folder, filename), "a") as f:
                        f.write(f"{str(itm_id)}plr{str(NetworkItem(*item).player)}.item\n")
                        if NetworkItem(*item).item == 77701:
                            if placedWeapon == 0:
                                f.write(str(77013))
                            elif placedWeapon == 1:
                                f.write(str(77014))
                            elif placedWeapon == 2:
                                f.write(str(77025))
                            elif placedWeapon == 3:
                                f.write(str(77045))
                            elif placedWeapon == 4:
                                f.write(str(77049))
                            elif placedWeapon == 5:
                                f.write(str(77047))
                            elif placedWeapon == 6:
                                if str(ctx.route) == "genocide" or str(ctx.route) == "all_routes":
                                    f.write(str(77052))
                                else:
                                    f.write(str(77051))
                            else:
                                f.write(str(77003))
                            placedWeapon += 1
                        elif NetworkItem(*item).item == 77702:
                            if placedArmor == 0:
                                f.write(str(77012))
                            elif placedArmor == 1:
                                f.write(str(77015))
                            elif placedArmor == 2:
                                f.write(str(77024))
                            elif placedArmor == 3:
                                f.write(str(77044))
                            elif placedArmor == 4:
                                f.write(str(77048))
                            elif placedArmor == 5:
                                if str(ctx.route) == "genocide":
                                    f.write(str(77053))
                                else:
                                    f.write(str(77046))
                            elif placedArmor == 6 and ((not str(ctx.route) == "genocide") or ctx.tem_armor):
                                if str(ctx.route) == "all_routes":
                                    f.write(str(77053))
                                elif str(ctx.route) == "genocide":
                                    f.write(str(77064))
                                else:
                                    f.write(str(77050))
                            elif placedArmor == 7 and ctx.tem_armor and not str(ctx.route) == "genocide":
                                f.write(str(77064))
                            else:
                                f.write(str(77004))
                            placedArmor += 1
                        else:
                            f.write(str(NetworkItem(*item).item))
                        f.write("\n")
                        f.close()
                ctx.items_received.append(NetworkItem(*item))
                if [item.item for item in ctx.items_received].count(77000) >= ctx.pieces_needed > 0:
                    filename = "items.itsem"
                    with open(os.path.join(ctx.save_game_folder, filename), "a") as f:
                        f.write(f"{str(-99999)}plr{str(0)}.item")
                        f.write("\n")
                        f.write(str(77787))
                        f.write("\n")
                        f.close()
                    with open(os.path.join(ctx.save_game_folder, filename), "a") as f:
                        f.write(f"{str(-99998)}plr{str(0)}.item")
                        f.write("\n")
                        f.write(str(77789))
                        f.write("\n")
                        f.close()
            with open(os.path.join(ctx.save_game_folder, "doorlock.locked"), "w") as ff:
                    for item in ctx.locked_doors:
                        ff.write(item + "\n")
                    ff.close()
        ctx.watcher_event.set()

    elif cmd == "RoomUpdate":
        if "checked_locations" in args:
            filename = f"check.spot"
            with open(os.path.join(ctx.save_game_folder, filename), "a") as f:
                for ss in set(args["checked_locations"]):
                    f.write(str(ss - 12000) + "\n")
                f.close()

    elif cmd == "Bounced":
        tags = args.get("tags", [])
        if "Online" in tags:
            data = args.get("data", {})
            if data["player"] != ctx.slot and data["player"] is not None:
                filename = f"frisk" + str(data["player"]) + ".playerspot"
                with open(os.path.join(ctx.save_game_folder, filename), "w") as f:
                    f.write(str(data["x"]) + str(data["y"]) + str(data["room"]) + str(
                        data["spr"]) + str(data["frm"]))
                    f.close()


async def multi_watcher(ctx: UndertaleContext):
    while not ctx.exit_event.is_set():
        path = ctx.save_game_folder
        for root, dirs, files in os.walk(path):
            for file in files:
                if "spots.mine" in file and "Online" in ctx.tags:
                    with open(os.path.join(root, file), "r") as mine:
                        this_x = mine.readline()
                        this_y = mine.readline()
                        this_room = mine.readline()
                        this_sprite = mine.readline()
                        this_frame = mine.readline()
                        mine.close()
                    message = [{"cmd": "Bounce", "tags": ["Online"],
                                "data": {"player": ctx.slot, "x": this_x, "y": this_y, "room": this_room,
                                         "spr": this_sprite, "frm": this_frame}}]
                    await ctx.send_msgs(message)

        await asyncio.sleep(0.1)


async def game_watcher(ctx: UndertaleContext):
    while not ctx.exit_event.is_set():
        await ctx.update_death_link(ctx.deathlink_status)
        path = ctx.save_game_folder
        if ctx.got_deathlink:
            ctx.got_deathlink = False
            with open(os.path.join(ctx.save_game_folder, "welcometothedead.youdied"), "w") as f:
                f.close()
        sending = []
        victory = False
        found_routes = 0
        if hasattr(ctx, "gifting") and ctx.gifting and ctx.initialize_gifting:
            await pop_gift(ctx)
        for root, dirs, files in os.walk(path):
            for file in files:
                if "dontbemad.mad" in file:
                    os.remove(os.path.join(root, file))
                    if "DeathLink" in ctx.tags:
                        await ctx.send_death()
                if "remove.gift" in file:
                    if hasattr(ctx, "gifting") and ctx.gifting and ctx.initialize_gifting:
                        with open(os.path.join(root, file), "r") as f:
                            lines = f.readlines()
                        for lin in lines:
                            await pick_gift_recipient(ctx, lin.rstrip('\n').rstrip(' '))
                        os.remove(os.path.join(root, file))
                if "scout" == file:
                    sending = []
                    try:
                        with open(os.path.join(root, file), "r") as f:
                            lines = f.readlines()
                        for lin in lines:
                            if ctx.server_locations.__contains__(int(lin) + 12000):
                                sending = sending + [int(lin.rstrip('\n')) + 12000]
                    except Exception as error:
                        print(str(error))
                    finally:
                        await ctx.send_msgs([{"cmd": "LocationScouts", "locations": sending,
                                              "create_as_hint": int(2)}])
                        os.remove(root + "/" + file)
                if "check.spot" in file:
                    sending = []
                    try:
                        with open(os.path.join(root, file), "r") as f:
                            lines = f.readlines()
                        for lin in lines:
                            sending = sending + [(int(lin.rstrip('\n'))) + 12000]
                        message = [{"cmd": "LocationChecks", "locations": sending}]
                        await ctx.send_msgs(message)
                    except Exception as error:
                        print(str(error))
                if "doorcheck.doorspot" in file:
                    sending = []
                    try:
                        with open(os.path.join(root, file), "r") as f:
                            lines = f.readlines()
                        for lin in lines:
                            if "Approach Door "+(lin.rstrip('\n')) in advancement_table:
                                sending = sending + [advancement_table["Approach Door "+(lin.rstrip('\n'))].id]
                        message = [{"cmd": "LocationChecks", "locations": sending}]
                        await ctx.send_msgs(message)
                    except Exception as error:
                        print(str(error))
                if "victory" in file and str(ctx.route) in file:
                    victory = True
                if ".playerspot" in file and "Online" not in ctx.tags:
                    os.remove(os.path.join(root, file))
                if "victory" in file:
                    if str(ctx.route) == "all_routes":
                        if "neutral" in file and ctx.completed_routes["neutral"] != 1:
                            text = ""
                            if not ctx.completed_routes["pacifist"]:
                                text += "Pacifist"
                            if not ctx.completed_routes["genocide"]:
                                if len(text) > 0:
                                    text += " and "
                                text += "Genocide"
                            if len(text) == 0:
                                logger.info("Goal: Completed Neutral route! Nothing is left.")
                            elif text.__contains__(", "):
                                logger.info("Goal: Completed Neutral route! " + text + " are left.")
                            else:
                                logger.info("Goal: Completed Neutral route! Only " + text + " is left.")
                            ctx.completed_routes["neutral"] = 1
                            await ctx.send_msgs([{"cmd": "Set", "key": str(ctx.slot) + " RoutesDone neutral",
                                                  "default": 0, "want_reply": True, "operations": [{"operation": "max",
                                                                                                    "value": 1}]}])
                        elif "pacifist" in file and ctx.completed_routes["pacifist"] != 1:
                            text = ""
                            if not ctx.completed_routes["neutral"]:
                                text += "Neutral"
                            if not ctx.completed_routes["genocide"]:
                                if len(text) > 0:
                                    text += " and "
                                text += "Genocide"
                            if len(text) == 0:
                                logger.info("Goal: Completed Pacifist route! Nothing is left.")
                            elif text.__contains__(", "):
                                logger.info("Goal: Completed Pacifist route! " + text + " are left.")
                            else:
                                logger.info("Goal: Completed Pacifist route! Only " + text + " is left.")
                            ctx.completed_routes["pacifist"] = 1
                            await ctx.send_msgs([{"cmd": "Set", "key": str(ctx.slot) + " RoutesDone pacifist",
                                                  "default": 0, "want_reply": True, "operations": [{"operation": "max",
                                                                                                    "value": 1}]}])
                        elif "genocide" in file and ctx.completed_routes["genocide"] != 1:
                            text = ""
                            if not ctx.completed_routes["pacifist"]:
                                text += "Pacifist"
                            if not ctx.completed_routes["neutral"]:
                                if len(text) > 0:
                                    text += " and "
                                text += "Neutral"
                            if len(text) == 0:
                                logger.info("Goal: Completed Genocide route! Nothing is left.")
                            elif text.__contains__(", "):
                                logger.info("Goal: Completed Genocide route! " + text + " are left.")
                            else:
                                logger.info("Goal: Completed Genocide route! Only " + text + " is left.")
                            ctx.completed_routes["genocide"] = 1
                            await ctx.send_msgs([{"cmd": "Set", "key": str(ctx.slot) + " RoutesDone genocide",
                                                  "default": 0, "want_reply": True, "operations": [{"operation": "max",
                                                                                                    "value": 1}]}])
        if str(ctx.route) == "all_routes":
            found_routes += ctx.completed_routes["neutral"]
            found_routes += ctx.completed_routes["pacifist"]
            found_routes += ctx.completed_routes["genocide"]
        if str(ctx.route) == "all_routes" and found_routes >= 3:
            victory = True
        ctx.locations_checked = sending
        if (not ctx.finished_game) and victory:
            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
            ctx.finished_game = True
        await asyncio.sleep(0.1)


def main():
    Utils.init_logging("UndertaleClient", exception_logger="Client")

    async def _main():
        ctx = UndertaleContext(None, None)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")
        asyncio.create_task(
            game_watcher(ctx), name="UndertaleProgressionWatcher")

        asyncio.create_task(
            multi_watcher(ctx), name="UndertaleMultiplayerWatcher")

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
    parser = get_base_parser(description="Undertale Client, for text interfacing.")
    args = parser.parse_args()
    main()
