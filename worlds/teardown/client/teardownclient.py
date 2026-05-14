import asyncio
import subprocess
import os
import json
import time
import xml.etree.ElementTree as ET
from Utils import gui_enabled, open_filename, user_path
from CommonClient import CommonContext, get_base_parser, server_loop
from NetUtils import ClientStatus
from typing import Any
import typing
import re
import traceback


SETTINGS_PATH = user_path("teardownsettings.json")
Missionindex = {
        "mall_intro": 0,
        "lee_computers": 1,
        "lee_login": 2,
        "marina_demolish": 3,
        "marina_cars": 4,
        "mansion_pool": 5,
        "lee_safe": 6,
        "marina_gps": 7,
        "lee_tower": 8,
        "mansion_art": 9,
        "marina_tools": 10,
        "marina_art_back": 11,
        "mall_foodcourt": 12,
        "mansion_fraud": 13,
        "caveisland_computers": 14,
        "mansion_race": 15,
        "mansion_safe": 16,
        "lee_powerplant": 17,
        "caveisland_propane": 18,
        "caveisland_dishes": 19,
        "lee_flooding": 20,
        "frustrum_chase": 21,
        "factory_espionage": 22,
        "caveisland_ingredients": 23,
        "frustrum_tornado": 24,
        "mall_shipping": 25,
        "carib_alarm": 26,
        "carib_barrels": 27,
        "carib_destroy": 28,
        "carib_yacht": 29,
        "frustrum_vehicle": 30,
        "mall_decorations": 31,
        "factory_tools": 32,
        "mall_radiolink": 33,
        "frustrum_pawnshop": 34,
        "factory_robot": 35,
        "lee_woonderland": 36,
        "factory_explosive": 37,
        "caveisland_roboclear": 38,
        "cullington_bomb": 39,
}

Missionmap = {
    1: "message/mall_intro",
    2: "message/lee_computers",
    3: "message/lee_login",
    4: "message/marina_demolish",
    5: "message/marina_cars",
    6: "message/marina_gps",
    7: "message/mansion_pool",
    8: "message/lee_safe",
    9: "message/lee_tower",
    10: "message/mansion_art",
    11: "message/marina_tools",
    12: "message/marina_art_back",
    13: "message/mall_foodcourt",
    14: "message/mansion_fraud",
    15: "message/caveisland_computers",
    16: "message/mansion_race",
    17: "message/mansion_safe",
    18: "message/lee_powerplant",
    19: "message/caveisland_propane",
    20: "message/caveisland_dishes",
    21: "message/lee_flooding",
    22: "message/frustrum_chase",
    23: "message/factory_espionage",
    24: "message/caveisland_ingredients",
    25: "message/frustrum_tornado",
    26: "message/mall_shipping",
    27: "message/carib_alarm",
    28: "message/carib_barrels",
    29: "message/carib_destroy",
    30: "message/carib_yacht",
    31: "message/frustrum_vehicle",
    32: "message/mall_decorations",
    33: "message/factory_tools",
    34: "message/mall_radiolink",
    35: "message/frustrum_pawnshop",
    36: "message/factory_robot",
    37: "message/lee_woonderland",
    38: "message/factory_explosive",
    39: "message/caveisland_roboclear",
    40: "message/cullington_bomb",
}

Toolmap = {
    41: "tool/sledge/enabled",
    42: "tool/spraycan/enabled",
    43: "tool/extinguisher/enabled",
    51: "tool/blowtorch/enabled",
    52: "tool/shotgun/enabled",
    53: "tool/plank/enabled",
    54: "tool/pipebomb/enabled",
    55: "tool/gun/enabled",
    56: "tool/bomb/enabled",
    57: "tool/rocket/enabled",
    58: "tool/booster/enabled",
    59: "tool/leafblower/enabled",
    60: "tool/wire/enabled",
    61: "tool/turbo/enabled",
    62: "tool/explosive/enabled",
    63: "tool/rifle/enabled",
    64: "tool/steroid/enabled",
}

Upgrademap = {
    71: ["tool/blowtorch/ammo", 10, 20],
    81: ["tool/shotgun/ammo", 12, 12],
    82: ["tool/shotgun/range", 20, 20],
    83: ["tool/shotgun/damage", 1, 3],
    91: ["tool/plank/ammo", 8, 8],
    92: ["tool/plank/width", 1, 3],
    93: ["tool/plank/length", 8, 36],
    101: ["tool/pipebomb/ammo", 6, 6],
    102: ["tool/pipebomb/damage", 1, 2],
    111: ["tool/gun/ammo", 6, 6],
    112: ["tool/gun/range", 20, 40],
    113: ["tool/gun/damage", 1, 1],
    121: ["tool/bomb/ammo", 6, 6],
    122: ["tool/bomb/damage", 1, 4],
    131: ["tool/rocket/ammo", 6, 6],
    132: ["tool/rocket/damage", 1, 3],
    141: ["tool/booster/ammo", 6, 6],
    142: ["tool/booster/power", 100, 200],
    143: ["tool/booster/time", 2, 4],
    151: ["tool/leafblower/power", 10, 20],
    161: ["tool/wire/ammo", 6, 6],
    162: ["tool/wire/stretch", 1, 3],
    171: ["tool/turbo/ammo", 6, 6],
    172: ["tool/turbo/power", 100, 200],
    181: ["tool/explosive/ammo", 4, 4],
    182: ["tool/explosive/damage", 1, 5],
    191: ["tool/rifle/ammo", 6, 6],
    201: ["tool/steroid/ammo", 1, 2],
    202: ["tool/steroid/time", 1, 4],

}



Mission_upgrade_send_map = {
    "mall_intro": 1,
    "lee_computers": 11,
    "lee_login": 21,
    "marina_demolish": 31,
    "marina_cars": 41,
    "mansion_pool": 61,
    "lee_safe": 71,
    "marina_gps": 51,
    "lee_tower": 81,
    "mansion_art": 91,
    "marina_tools": 101,
    "marina_art_back": 111,
    "mall_foodcourt": 121,
    "mansion_fraud": 131,
    "caveisland_computers": 141,
    "mansion_race": 151,
    "mansion_safe": 161,
    "lee_powerplant": 171,
    "caveisland_propane": 181,
    "caveisland_dishes": 191,
    "lee_flooding": 201,
    "frustrum_chase": 211,
    "factory_espionage": 221,
    "caveisland_ingredients": 231,
    "frustrum_tornado": 241,
    "mall_shipping": 251,
    "carib_alarm": 261,
    "carib_barrels": 271,
    "carib_destroy": 281,
    "carib_yacht": 291,
    "frustrum_vehicle": 301,
    "mall_decorations": 311,
    "factory_tools": 321,
    "mall_radiolink": 331,
    "frustrum_pawnshop": 341,
    "factory_robot": 351,
    "lee_woonderland": 361,
    "factory_explosive": 371,
    "caveisland_roboclear": 381,
    "cullington_bomb": 393,
}

Tool_upgrade_send_map = {
    "toolupgrade/blowtorch/ammo": {
        30: 501,
        40: 502,
        50: 503,
        60: 504,
    },
    "toolupgrade/shotgun/ammo": {
        24: 511,
        36: 512,
        48: 513,
        60: 514,
        72: 515,
        84: 516,
        96: 517,
    },
    "toolupgrade/shotgun/range": {
        40: 521,
        60: 521,
    },
    "toolupgrade/shotgun/damage": {
        4: 531,
        5: 532,
    },
    "toolupgrade/plank/ammo": {
        16: 541,
        24: 542,
        32: 543,
        40: 544,
        48: 545,
        56: 546,
        64: 547,
    },
    "toolupgrade/plank/width": {
        4: 551,
        5: 552,
    },
    "toolupgrade/plank/length": {
        48: 561,
        56: 562,
        64: 563,
    },
    "toolupgrade/pipebomb/ammo": {
        12: 571,
        18: 572,
        25: 573,
        30: 574,
        36: 575,
    },
    "toolupgrade/pipebomb/damage": {
        3: 581,
        4: 582,
    },
    "toolupgrade/gun/ammo": {
        12: 591,
        18: 592,
        24: 593,
        30: 594,
        36: 595,
    },
    "toolupgrade/gun/range": {
        60: 601,
        80: 602,
        100: 603,
    },
    "toolupgrade/gun/damage": {
        2: 611,
        3: 612,
    },
    "toolupgrade/bomb/ammo": {
        12: 621,
        18: 622,
        24: 623,
        30: 624,
        36: 625,
    },
    "toolupgrade/bomb/damage": {
        5: 631,
        6: 632,
    },
    "toolupgrade/rocket/ammo": {
        12: 641,
        18: 642,
        24: 643,
    },
    "toolupgrade/rocket/damage": {
        4: 651,
        5: 652,
    },
    "toolupgrade/booster/ammo": {
        12: 661,
        18: 662,
        24: 663,
    },
    "toolupgrade/booster/power": {
        300: 671,
        400: 672,
    },
    "toolupgrade/booster/time": {
        6: 681,
        8: 682,
    },
    "toolupgrade/leafblower/power": {
        30: 691,
        40: 692,
        50: 693,
    },
    "toolupgrade/wire/ammo": {
        12: 701,
        18: 702,
        24: 703,
    },
    "toolupgrade/wire/stretch": {
        4: 711,
        5: 712,
    },
    "toolupgrade/turbo/ammo": {
        12: 721,
        18: 722,
        36: 723,
    },
    "toolupgrade/turbo/power": {
        300: 731,
        400: 732,
    },
    "toolupgrade/explosive/ammo": {
        8: 741,
        12: 742,
        16: 743,
    },
    "toolupgrade/explosive/damage": {
        6: 751,
        7: 752,
        8: 753,
    },
    "toolupgrade/rifle/ammo": {
        12: 761,
        18: 762,
    },
    "toolupgrade/steroid/ammo": {
        3: 771,
        4: 772,
    },
    "toolupgrade/steroid/time": {
        5: 781,
        6: 782,
    },

}

SAVE_TEMPLATE = {
    "toolupgrade": {

        "blowtorch/enabled": "0",
        "blowtorch/ammo": "20",

        "shotgun/enabled": "0",
        "shotgun/ammo": "12",
        "shotgun/range": "20",
        "shotgun/damage": "3",

        "plank/enabled": "0",
        "plank/ammo": "8",
        "plank/width": "3",
        "plank/length": "36",

        "pipebomb/enabled": "0",
        "pipebomb/ammo": "6",
        "pipebomb/damage": "2",

        "gun/enabled": "0",
        "gun/ammo": "6",
        "gun/range": "40",
        "gun/damage": "1",

        "bomb/enabled": "0",
        "bomb/ammo": "6",
        "bomb/damage": "4",

        "rocket/enabled": "0",
        "rocket/ammo": "6",
        "rocket/damage": "3",

        "booster/enabled": "0",
        "booster/ammo": "6",
        "booster/power": "200",
        "booster/time": "4",

        "leafblower/enabled": "0",
        "leafblower/power": "20",

        "wire/enabled": "0",
        "wire/ammo": "6",
        "wire/stretch": "3",

        "turbo/enabled": "0",
        "turbo/ammo": "6",
        "turbo/power": "200",

        "explosive/enabled": "0",
        "explosive/ammo": "4",
        "explosive/damage": "5",

        "rifle/enabled": "0",
        "rifle/ammo": "6",

        "steroid/enabled": "0",
        "steroid/ammo": "2",
        "steroid/time": "4",

    },

    "tool": {
        "sledge/enabled": "0",

        "spraycan/enabled": "0",

        "extinguisher/enabled": "0",

        "blowtorch/enabled": "0",
        "blowtorch/ammo": "20",

        "shotgun/enabled": "0",
        "shotgun/ammo": "12",
        "shotgun/range": "20",
        "shotgun/damage": "3",

        "plank/enabled": "0",
        "plank/ammo": "8",
        "plank/width": "3",
        "plank/length": "36",

        "pipebomb/enabled": "0",
        "pipebomb/ammo": "6",
        "pipebomb/damage": "2",

        "gun/enabled": "0",
        "gun/ammo": "6",
        "gun/range": "40",
        "gun/damage": "1",

        "bomb/enabled": "0",
        "bomb/ammo": "6",
        "bomb/damage": "4",

        "rocket/enabled": "0",
        "rocket/ammo": "6",
        "rocket/damage": "3",

        "booster/enabled": "0",
        "booster/ammo": "6",
        "booster/power": "200",
        "booster/time": "4",

        "leafblower/enabled": "0",
        "leafblower/power": "20",

        "wire/enabled": "0",
        "wire/ammo": "6",
        "wire/stretch": "3",

        "turbo/enabled": "0",
        "turbo/ammo": "6",
        "turbo/power": "200",

        "explosive/enabled": "0",
        "explosive/ammo": "4",
        "explosive/damage": "5",

        "rifle/enabled": "0",
        "rifle/ammo": "6",

        "steroid/enabled": "0",
        "steroid/ammo": "2",
        "steroid/time": "4",

    },

    "message": {
        "boss_intro": "0",
        "mall_intro": "0",
        "boss_busted": "0",
        "lee_computers": "0",
        "lee_login": "0",
        "boss_coffee": "0",
        "marina_demolish": "0",
        "marina_cars": "0",
        "lockelle_parade_ad": "0",
        "marina_gps": "0",
        "mansion_pool": "0",
        "lee_safe": "0",
        "lee_safe_done": "0",
        "lee_tower": "0",
        "boss_encourage_1": "0",
        "mansion_art": "0",
        "marina_tools": "0",
        "marina_art_back": "0",
        "mall_foodcourt": "0",
        "marina_art_back_done": "0",
        "mansion_fraud": "0",
        "caveisland_computers": "0",
        "mansion_race": "0",
        "mansion_safe": "0",
        "lee_powerplant": "0",
        "lee_powerplant_done": "0",
        "boss_encourage_2": "0",
        "caveisland_propane": "0",
        "caveisland_dishes": "0",
        "lee_flooding": "0",
        "frustrum_chase": "0",
        "boss_part2": "0",
        "factory_espionage": "0",
        "factory_espionage_done": "0",
        "caveisland_ingredients": "0",
        "frustrum_tornado": "0",
        "mall_shipping": "0",
        "mall_shipping_done": "0",
        "carib_travel": "0",
        "carib_alarm": "0",
        "boss_vacation": "0",
        "carib_barrels": "0",
        "carib_destroy": "0",
        "carib_yacht": "0",
        "carib_last": "0",
        "frustrum_vehicle": "0",
        "mall_decorations": "0",
        "factory_tools": "0",
        "mall_radiolink": "0",
        "frustrum_pawnshop": "0",
        "factory_robot": "0",
        "lee_woonderland": "0",
        "factory_explosive": "0",
        "tracy_dinner": "0",
        "factory_explosive_done": "0",
        "caveisland_roboclear": "0",
        "caveisland_roboclear_done1": "0",
        "caveisland_roboclear_done2": "0",
        "cullington_bomb": "0",

    },
    "mission": {
        "mall_intro": "0",
        "mall_intro/score": "0",
        "lee_computers": "0",
        "lee_computers/score": "0",
        "lee_login": "0",
        "lee_login/score": "0",
        "marina_demolish": "0",
        "marina_demolish/score": "0",
        "marina_cars": "0",
        "marina_cars/score": "0",
        "mansion_pool": "0",
        "mansion_pool/score": "0",
        "lee_safe": "0",
        "lee_safe/score": "0",
        "marina_gps": "0",
        "marina_gps/score": "0",
        "lee_tower": "0",
        "lee_tower/score": "0",
        "mansion_art": "0",
        "mansion_art/score": "0",
        "marina_tools": "0",
        "marina_tools/score": "0",
        "marina_art_back": "0",
        "marina_art_back/score": "0",
        "mall_foodcourt": "0",
        "mall_foodcourt/score": "0",
        "mansion_fraud": "0",
        "mansion_fraud/score": "0",
        "caveisland_computers": "0",
        "caveisland_computers/score": "0",
        "mansion_race": "0",
        "mansion_race/score": "0",
        "mansion_safe": "0",
        "mansion_safe/score": "0",
        "lee_powerplant": "0",
        "lee_powerplant/score": "0",
        "caveisland_propane": "0",
        "caveisland_propane/score": "0",
        "caveisland_dishes": "0",
        "caveisland_dishes/score": "0",
        "lee_flooding": "0",
        "lee_flooding/score": "0",
        "frustrum_chase": "0",
        "frustrum_chase/score": "0",
        "factory_espionage": "0",
        "factory_espionage/score": "0",
        "caveisland_ingredients": "0",
        "caveisland_ingredients/score": "0",
        "frustrum_tornado": "0",
        "frustrum_tornado/score": "0",
        "mall_shipping": "0",
        "mall_shipping/score": "0",
        "carib_alarm": "0",
        "carib_alarm/score": "0",
        "carib_barrels": "0",
        "carib_barrels/score": "0",
        "carib_destroy": "0",
        "carib_destroy/score": "0",
        "carib_yacht": "0",
        "carib_yacht/score": "0",
        "frustrum_vehicle": "0",
        "frustrum_vehicle/score": "0",
        "mall_decorations": "0",
        "mall_decorations/score": "0",
        "factory_tools": "0",
        "factory_tools/score": "0",
        "mall_radiolink": "0",
        "mall_radiolink/score": "0",
        "frustrum_pawnshop": "0",
        "frustrum_pawnshop/score": "0",
        "factory_robot": "0",
        "factory_robot/score": "0",
        "lee_woonderland": "0",
        "lee_woonderland/score": "0",
        "factory_explosive": "0",
        "factory_explosive/score": "0",
        "caveisland_roboclear": "0",
        "caveisland_roboclear/score": "0",
        "cullington_bomb": "0",
        "cullington_bomb/score": "0",

    }
}







class TeardownContext(CommonContext):
    game = "Teardown"
    tags = CommonContext.tags | {"AP"}
    items_handling = 0b111
    want_slot_data = True
    slot_data: dict[str, Any]
    last_connected_slot: int | None = None
    stored_data: dict[str, typing.Any]
    stored_data_notification_keys: set[str]
    items_received: int = 0




    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.last_known_item_count = None
        self.last_mtime = None
        self.game_exe_path = ""
        self.savegame_path = ""
        self.player_data = None
        self.first_sync_done = False
        self.loadsettings()
        self.MissionAmount = 0
        self.mission_count = 0
        self.finished_game = False
        self.location_name_to_id = ""
        self.items_received_event = asyncio.Event()
        self.auth_event = asyncio.Event()
        self.locations_checked = []


    def loadsettings(self):
        # Load our settings from our json file
        if os.path.exists(SETTINGS_PATH):
            with open(SETTINGS_PATH, "r") as f:
                data = json.load(f)
                self.game_exe_path = data.get("game_exe_path", "")
                self.savegame_path = data.get("savegame_path", "")


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


    def savesettings(self):
        # Save our settings to our json file
        data = {
            "game_exe_path": self.game_exe_path,
            "savegame_path": self.savegame_path
        }
        with open(SETTINGS_PATH, "w") as f:
            json.dump(data, f, indent=4)


    async def reset_and_initialize_save(self):

        print("Initializing: Waiting for items to be received from server")
        while not self.items_received:
            await asyncio.sleep(0.5)
        await asyncio.sleep(0.5)

        if not self.savegame_path or not os.path.exists(self.savegame_path):
            return

        with open(self.savegame_path, 'r', encoding='utf-8') as f:
            text_data = f.read()
        clean_text = re.sub(r'^\s*<\d+[^>]*/>.*\n?', '', text_data, flags=re.MULTILINE)

        try:
            with open(self.savegame_path, "w", encoding='utf-8') as f:
                f.write(clean_text)

            tree = ET.parse(self.savegame_path)
            root = tree.getroot()

            self.player_data = root.find("savegame/mod/steam-3708322400")
            print(f"Initializing: player_data found: {self.player_data is not None}")

            if self.player_data is None:
                mod_node = root.find("mod")
                if mod_node is None:
                    mod_node = ET.SubElement(root, "mod")
                self.player_data = ET.SubElement(mod_node, "steam-3708322400")


            for category, nodes in SAVE_TEMPLATE.items():

                print(f"Initializing: Processing Category: {category}")
                cat_node = self.player_data.find(category)
                if cat_node is None:
                    print(f"Initializing: Category '{category}' not found, creating new SubElement.")

                cat_node = self.player_data.find(category)
                if cat_node is None:
                    cat_node = ET.SubElement(self.player_data, category)

                for path, val in nodes.items():
                    parts = path.split('/')
                    current = cat_node
                    for i, part in enumerate(parts):
                        child = current.find(part)
                        if child is None:
                            child = ET.SubElement(current, part)
                        if i == len(parts) - 1:
                            full_path = f"{category} -> {' -> '.join(parts)}"

                            print(f"Initializing:  [{full_path}] to value: {val}")
                            child.set("value", str(val))

                        current = child
            last_node = self.player_data.find("lastcompleted")
            if last_node is None:
                last_node = ET.SubElement(self.player_data, "lastcompleted")
            last_node.set("value", "")

            for message_node in self.player_data.findall("message"):
                self.player_data.remove(message_node)
                print(f"Initializing: Pruned message node: {message_node.tag}")

            self.apply_server_state_to_xml(self.player_data)

            for i in range(5):  # Try 5 times
                try:
                    print(f"Initializing: Attempting initialization write {i + 1}/5")
                    ET.indent(tree, space="          ", level=0)
                    tree.write(self.savegame_path, encoding="UTF-8", xml_declaration=False)

                    print("Teardown Save: Player Data initialized and globally set.")
                    return True

                except PermissionError:
                    print("Initializing: File locked during init, retrying")
                    await asyncio.sleep(0.2)
                except Exception as e:
                    print(f"Failed to initialize player_data: {e}")
                    traceback.print_exc()
                    break

            return False

        except Exception as e:
            print(f"Failed to initialize player_data: {e}")
            traceback.print_exc()

    def apply_server_state_to_xml(self, player_data):
        received_counts = {}
        print(f"First Apply: Total items in self.items_received: {len(self.items_received)}")

        for item in self.items_received:
            item_id = item.item  # This is the raw integer ID (e.g., 41, 42)
            received_counts[item_id] = received_counts.get(item_id, 0) + 1
            print(f"First Apply: Counted Item ID {item_id}")

        def update_node(path, value):
            node = player_data.find(path)
            if node is None:
                # Creation logic
                curr = player_data
                for part in path.split('/'):
                    child = curr.find(part)
                    if child is None: child = ET.SubElement(curr, part)
                    curr = child
                node = curr
            node.set("value", str(value))
            print(f"First Apply: Initial XML Setting - {path} set to {value}")

        # 1. Sync Tools & Missions
        for mapping in [Toolmap, Missionmap]:
            for ap_id, xml_path in mapping.items():
                count = received_counts.get(ap_id, 0)
                if count > 0:
                    update_node(xml_path, "1")

        for ap_id, config in Upgrademap.items():
            count = received_counts.get(ap_id, 0)
            path, mult, base = config
            final_val = (count * mult) + base
            update_node(path, final_val)

            print(f"First Apply: Initial Setting {ap_id} -> {path} is now {final_val} (Base {base} + {count} items)")
            update_node(path, final_val)


    async def sync_savegame(self):
        if not self.savegame_path or not os.path.exists(self.savegame_path):
            return False

        print(f"Sync: Starting Sync")

        try:
            tree = ET.parse(self.savegame_path)
            root = tree.getroot()
            self.player_data = root.find("savegame/mod/steam-3708322400")
            original_xml_string = ET.tostring(root, encoding="unicode")
            print("Sync: Parse successful.")

        except Exception as e:
            print(f"Sync: Parse FAILED with error: {e}")
            return


        self.check_missions()
        self.check_tools()
        self.apply_received_items(self.player_data)
        print("Sync: Functions ran.")

        new_xml_string = ET.tostring(root, encoding="unicode")

        if original_xml_string == new_xml_string:
            print("Sync: No changes in XML, skipping save.")
            return True

        print("Sync: XML Differences, Now Saving.")
        for i in range(5):
            try:
                print(f"Sync: Save started, attempt {i + 1}")
                ET.indent(tree, space="          ", level=0)
                tree.write(self.savegame_path, encoding="UTF-8", xml_declaration=False)
                return True  # Exit function and return to loop
            except PermissionError:
                print("Sync: File locked, waiting...")
                await asyncio.sleep(0.2)
            except Exception as e:
                print(f"Sync: Critical Write Error: {e}")
                return False

        return False


    def check_missions(self):
        print("Sync Mission: Entering check_missions")
        if self.player_data is None:
            print("Sync Mission: Player Data is None")
            return

        last_node = self.player_data.find("lastcompleted")
        if last_node is None:
            print("Sync Mission: Ending check_missions, node 'lastcompleted' not found in XML")
            return

        mission_id = last_node.get("value")

        if mission_id is None:
            print("Sync Mission: Ending check_missions, no lastcompleted")
            return
        print(f"Sync Missions: Starting check_missions, lastcompleted: {mission_id}")

        if mission_id and mission_id in Mission_upgrade_send_map:
            start_id = Mission_upgrade_send_map[mission_id]

            asyncio.create_task(self.send_msgs([{
                "cmd": "Set",
                "key": f"Teardown-{self.auth}-Missions",
                "default": 0,
                "want_reply": True,
                "operations": [{"operation": "add", "value": 1}]
            }]))

            print("Sync Mission: Sends msgs and continues")
            mission_container = self.player_data.find("mission")
            if mission_container is not None:
                score_node = mission_container.find(f"{mission_id}/score")
                print(f"Sync Mission: Sends msgs and continues: {"mission"}")

                if score_node is not None:
                    current_score = int(score_node.get("value", "0"))
                    print(f"Sync Mission: current score is: {current_score}")

                    # Loop through the score
                    for i in range(current_score):
                        # Calculate the specific ID for this check
                        location_id = start_id + i

                        # Send the ID directly to your check function
                        self.send_upgrade_check(location_id)

            # 4. Clear the trigger in the XML data so it doesn't fire again
            last_node.set("value", "")


    def check_tools(self):
        print("Sync Tools: Entering check_tools")
        if self.player_data is None:
            return
        for xml_path, thresholds in Tool_upgrade_send_map.items():
            node = self.player_data.find(xml_path)
            print(f"Sync Tools: {xml_path}")

            if node is not None:
                current_val = int(node.get("value", "0"))
                print(f"Sync Tools:  {current_val}")

                for threshold, location_id in thresholds.items():
                    if current_val >= threshold:
                        self.send_upgrade_check(location_id)


    def send_upgrade_check(self, location_id):
        print("Sync Check: Entering send_upgrade_check")

        if location_id not in self.locations_checked:
            print("Sync Check: before append to list")
            self.locations_checked.append(location_id)
            print("Sync Check: appending list")

            # Send the ID directly to the server
            print(f"Sync Missions: Sending Location ID {location_id}")
            asyncio.create_task(self.send_msgs([{
                "cmd": "LocationChecks",
                "locations": [location_id]
            }]))

            print(f"Success: Sent check for {location_id} (ID: {location_id})")
        else:
            print(f"Error: Could not find an ID for location name: {location_id}")


    def apply_received_items(self, player_data):
        print("Entering Apply Received Items")

        current_count = len(self.items_received)
        if not hasattr(self, 'last_received_count'):
            self.last_received_count = 0

        if current_count == self.last_received_count:
            print("No New Items")
            return

        received_item_counts = {}
        for item in self.items_received:
            item_id = item.item
            received_item_counts[item_id] = received_item_counts.get(item_id, 0) + 1
            print(f"DEBUG: Counted Item ID {item_id}")



        print(f"Sync Apply Items: Starting apply_received_items, total items in queue: {len(self.items_received)}")


        def update_node(path2, value):
            node = player_data.find(path2)
            if node is None:
                curr = player_data
                for part in path2.split('/'):
                    child = curr.find(part)
                    if child is None: child = ET.SubElement(curr, part)
                    curr = child
                node = curr
            node.set("value", str(value))
            print(f"DEBUG: XML Update - {path2} set to {value}")

        for mapping in [Toolmap, Missionmap]:
            for ap_id, xml_path in mapping.items():
                count = received_item_counts.get(ap_id, 0)
                if count > 0:
                    update_node(xml_path, "1")

        for ap_id, config in Upgrademap.items():
            count = received_item_counts.get(ap_id, 0)
            path, mult, base = config
            final_val = (count * mult) + base
            update_node(path, final_val)

            self.last_received_count = current_count
            print(f"DEBUG: {ap_id} -> {path} is now {final_val} (Base {base} + {count} items)")
            update_node(path, final_val)



    def update_xml_value(self, player_data, xml_path, attribute, new_value, is_bool=False):
        node = player_data.find(xml_path)
        if node is not None:
            current_val = node.get(attribute)

            # Handle Boolean (true/false) logic
            if is_bool:
                if current_val == "false" and str(new_value).lower() == "true":
                    node.set(attribute, "true")
                    return True
            # Handle Numeric logic (don't downgrade if the player somehow has more)
            else:
                if int(current_val or 0) < int(new_value):
                    node.set(attribute, str(new_value))
                    return True
        return False



    def complete_mission(self, mission_id: str):
        # 1. Get the index (e.g., lee_login is 2)
        index = Missionindex.get(mission_id)

        if index is not None:
            # 1 << 2 becomes 00000100 in binary
            new_value = 1 << index

            # Send the bitwise OR update to the server
            self.send_encoded_packet([{
                "cmd": "Set",
                "key": f"Teardown_Missions_{self.team}_{self.slot}",
                "default": 0,
                "want_reply": True,
                "operations": [{"operation": "or", "value": new_value}]
            }])
            print(f"Archipelago: Mission {mission_id} (ID {index}) marked as complete.")


    def handle_victory_unlock(self, current_count):
        if self.player_data is None:
            return
        goal_required = getattr(self, 'MissionAmount', 20)

        if current_count >= goal_required:
            # 1. Unlock the Finale Message in the XML
            if self.update_xml_value(self.player_data, "message/cullington_bomb", "value", "1"):
                print(f"Goal Met: {current_count}/{goal_required}. Cullington Bomb Unlocked!")

        # 2. Check if Cullington Bomb is already done (The actual WIN)
        final_mission = self.player_data.find("mission/cullington_bomb")
        if final_mission is not None and final_mission.get("value") == "1":
            if not self.finished_game:
                asyncio.create_task(self.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}]))
                self.finished_game = True



    def launch_game(self):
        if self.game_exe_path and os.path.exists(self.game_exe_path):
            subprocess.Popen([self.game_exe_path])
        else:
            print("Cannot launch: Valid executable path not found.")



    def on_package(self, cmd: str, args: dict):
        if cmd == "Connected":
            self.MissionAmount = args.get("slot_data", {}).get("MissionAmount", 20)
            self.location_name_to_id = args.get("slot_info", {}).get("location_name_to_id", {})
            self.last_connected_slot = self.slot

            async def init_sequence():
                await self.send_msgs([{"cmd": "Get", "keys": [f"Teardown-{self.auth}-Missions"]}])
                await self.reset_and_initialize_save()
                self.auth_event.set()

            asyncio.create_task(init_sequence())


        elif cmd == "Retrieved":
            count = args.get("keys", {}).get(f"Teardown-{self.auth}-Missions") or 0
            self.mission_count = count
            self.handle_victory_unlock(count)


        elif cmd == "SetReply":
            if args.get("key") == f"Teardown-{self.auth}-Missions":
                new_count = args.get("value")
                self.mission_count = new_count
                self.handle_victory_unlock(new_count)


    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(TeardownContext, self).server_auth(password_requested)
        await self.get_username()
        await self.send_connect(game="Teardown")

    async def disconnect(self, allow_autoreconnect: bool = False):
        self.game = ""
        await super().disconnect(allow_autoreconnect)



async def main(args):
    ctx = TeardownContext(args.connect, args.password)
    ctx.auth = args.name
    ctx.checkgamepath()
    ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")

    async def sync_loop():
        await ctx.auth_event.wait()
        print("DEBUG: Sync loop started!")
        while not ctx.exit_event.is_set():
            print("DEBUG: Loop tick...")
            if ctx.savegame_path and os.path.exists(ctx.savegame_path):
                await ctx.sync_savegame()
            await asyncio.sleep(3)

    ctx.sync_task = asyncio.create_task(sync_loop(), name="save sync loop")

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