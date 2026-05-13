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
    "mall_intro": [
        "Old Building Problem",
    ],
    "lee_computers": [
        "Lee Computers Required 1",
        "Lee Computers Required 2",
        "Lee Computers Required 3"
    ],
    "lee_login": [
        "Login Devices Required 1",
        "Login Devices Required 2",
        "Login Devices Required 3"
    ],
    "marina_demolish": [
        "Making Space Required 1",
        "Making Space Required 2",
        "Making Space Optional 3",
    ],
    "marina_cars": [
        "Classic Cars Required 1",
        "Classic Cars Required 2",
        "Classic Cars Optional 1",
        "Classic Cars Optional 2",
    ],
    "mansion_pool": [
        "The GPS Devices Required 1",
        "The GPS Devices Required 2",
        "The GPS Devices Required 3",
        "The GPS Devices Optional 1",
        "The GPS Devices Optional 2",
    ],
    "lee_safe": [
        "The Car Wash Required 1",
        "The Car Wash Required 2",
        "The Car Wash Required 3",
        "The Car Wash Optional 1",
        "The Car Wash Optional 2",
        "The Car Wash Optional 3",
    ],
    "marina_gps": [
        "Heavy Lifting Required 1",
        "Heavy Lifting Optional 1",
        "Heavy Lifting Optional 2",
        "Heavy Lifting Optional 3",
        "Heavy Lifting Optional 4",
    ],
    "lee_tower": [
        "The Tower",
    ],
    "mansion_art": [
        "Fine Arts Required 1",
        "Fine Arts Required 2",
        "Fine Arts Required 3",
        "Fine Arts Required 4",
        "Fine Arts Optional 1",
        "Fine Arts Optional 2",
    ],
    "marina_tools": [
        "Tool Up Required 1",
        "Tool Up Required 2",
        "Tool Up Required 3",
        "Tool Up Required 4",
        "Tool Up Optional 1",
        "Tool Up Optional 2",
    ],
    "marina_art_back": [
        "Art Return Required 1",
        "Art Return Required 2",
        "Art Return Required 3",
        "Art Return Required 4",
    ],
    "mall_foodcourt": [
        "Covert Chaos Required 1",
        "Covert Chaos Optional 1",
        "Covert Chaos Optional 2",
    ],
    "mansion_fraud": [
        "Insurance Fraud Required 1",
        "Insurance Fraud Required 2",
        "Insurance Fraud Required 3",
        "Insurance Fraud Optional 1",
        "Insurance Fraud Optional 2",
        "Insurance Fraud Optional 3",
    ],
    "caveisland_computers": [
        "The BlueTide Computers Required 1",
        "The BlueTide Computers Required 2",
        "The BlueTide Computers Required 3",
        "The BlueTide Computers Required 4",
        "The BlueTide Computers Optional 1",
        "The BlueTide Computers Optional 2",
        "The BlueTide Computers Optional 3",
    ],
    "mansion_race": [
        "The Speed Deal Required 1",
        "The Speed Deal Optional 1",
        "The Speed Deal Optional 2",
    ],
    "mansion_safe": [
        "A Wet Affair Required 1",
        "A Wet Affair Required 2",
        "A Wet Affair Required 3",
        "A Wet Affair Optional 1",
        "A Wet Affair Optional 2",
        "A Wet Affair Optional 3",
    ],
    "lee_powerplant": [
        "Power Outage Required 1",
        "Power Outage Required 2",
        "Power Outage Required 3",
        "Power Outage Required 4",
        "Power Outage Optional 1",
        "Power Outage Optional 2",
        "Power Outage Optional 3",
        "Power Outage Optional 4",
    ],
    "caveisland_propane": [
        "Motivational Reminder Required 1",
        "Motivational Reminder Required 2",
        "Motivational Reminder Required 3",
        "Motivational Reminder Required 4",
        "Motivational Reminder Required 5",
        "Motivational Reminder Optional 1",
        "Motivational Reminder Optional 2",
        "Motivational Reminder Optional 3",
    ],
    "caveisland_dishes": [
        "An Assortment Of Dishes Required 1",
        "An Assortment Of Dishes Required 2",
        "An Assortment Of Dishes Required 3",
        "An Assortment Of Dishes Required 4",
        "An Assortment Of Dishes Required 5",
        "An Assortment Of Dishes Optional 1",
        "An Assortment Of Dishes Optional 2",
        "An Assortment Of Dishes Optional 3",
        "An Assortment Of Dishes Optional 4",

    ],
    "lee_flooding": [
        "Flooding Required 1",
        "Flooding Required 2",
        "Flooding Required 3",
        "Flooding Required 4",
        "Flooding Required 5",
        "Flooding Optional 1",
        "Flooding Optional 2",
        "Flooding Optional 3",
    ],
    "frustrum_chase": [
        "The Chase",
    ],
    "factory_espionage": [
        "Roborazzi Required 1",
        "Roborazzi Required 2",
        "Roborazzi Required 3",
        "Roborazzi Required 4",
        "Roborazzi Required 5",
    ],
    "caveisland_ingredients": [
        "The Secret Ingredients Required 1",
        "The Secret Ingredients Required 2",
        "The Secret Ingredients Required 3",
        "The Secret Ingredients Required 4",
        "The Secret Ingredients Optional 1",
        "The Secret Ingredients Optional 2",
    ],
    "frustrum_tornado": [
        "The BlueTide Shortage Required 1",
        "The BlueTide Shortage Required 2",
        "The BlueTide Shortage Required 3",
        "The BlueTide Shortage Optional 1",
        "The BlueTide Shortage Optional 2",
        "The BlueTide Shortage Optional 3",
    ],
    "mall_shipping": [
        "The Shipping Logs Required 1",
        "The Shipping Logs Required 2",
        "The Shipping Logs Required 3",
        "The Shipping Logs Required 4",
        "The Shipping Logs Required 5",
        "The Shipping Logs Optional 1",
        "The Shipping Logs Optional 2",
        "The Shipping Logs Optional 3",
    ],
    "carib_alarm": [
        "The Alarm System Required 1",
        "The Alarm System Required 2",
        "The Alarm System Required 3",
        "The Alarm System Required 4",
        "The Alarm System Optional 1",
        "The Alarm System Optional 2",
    ],
    "carib_barrels": [
        "Moving The Goods Required 1",
        "Moving The Goods Required 2",
        "Moving The Goods Required 3",
        "Moving The Goods Optional 1",
        "Moving The Goods Optional 2",
    ],
    "carib_destroy": [
        "Havoc In Paradise Required 1",
        "Havoc In Paradise Required 2",
        "Havoc In Paradise Required 3",
        "Havoc In Paradise Required 4",
        "Havoc In Paradise Optional 1",
        "Havoc In Paradise Optional 2",
        "Havoc In Paradise Optional 3",
    ],
    "carib_yacht": [
        "Elena's Revenge",
    ],
    "frustrum_vehicle": [
        "Truckload Of Trouble Required 1",
        "Truckload Of Trouble Required 2",
        "Truckload Of Trouble Optional 1",
    ],
    "mall_decorations": [
        "Ornament Ordeal Required 1",
        "Ornament Ordeal Required 2",
        "Ornament Ordeal Required 3",
        "Ornament Ordeal Required 4",
        "Ornament Ordeal Optional 1",
        "Ornament Ordeal Optional 2",
    ],
    "factory_tools": [
        "The Quilez Tools Required 1",
        "The Quilez Tools Required 2",
        "The Quilez Tools Required 3",
        "The Quilez Tools Required 4",
        "The Quilez Tools Optional 1",
        "The Quilez Tools Optional 2",
    ],
    "mall_radiolink": [
        "Connecting The Dots Required 1",
        "Connecting The Dots Required 2",
        "Connecting The Dots Required 3",
        "Connecting The Dots Optional 1",
        "Connecting The Dots Optional 2",
    ],
    "frustrum_pawnshop": [
        "The Pawn Shop Required 1",
        "The Pawn Shop Required 2",
        "The Pawn Shop Required 3",
        "The Pawn Shop Required 4",
        "The Pawn Shop Required 5",
        "The Pawn Shop Optional 1",
        "The Pawn Shop Optional 2",
    ],
    "factory_robot": [
        "The Droid Abduction Required 1",
        "The Droid Abduction Optional 1",
        "The Droid Abduction Optional 2",
        "The Droid Abduction Optional 3",
    ],
    "lee_woonderland": [
        "Malice In Woonderland Required 1",
        "Malice In Woonderland Required 2",
        "Malice In Woonderland Required 3",
        "Malice In Woonderland Required 4",
        "Malice In Woonderland Required 5",
        "Malice In Woonderland Optional 1",
        "Malice In Woonderland Optional 2",
        "Malice In Woonderland Optional 3",
    ],
    "factory_explosive": [
        "Handle With Care Required 1",
        "Handle With Care Required 2",
        "Handle With Care Required 3",
        "Handle With Care Optional 1",
        "Handle With Care Optional 2",
        "Handle With Care Optional 3",
        "Handle With Care Optional 4",
    ],
    "caveisland_roboclear": [
        "Droid Dismount Required 1",
        "Droid Dismount Required 2",
        "Droid Dismount Required 3",
        "Droid Dismount Required 4",
        "Droid Dismount Required 5",
        "Droid Dismount Optional 1",
        "Droid Dismount Optional 2",
    ],
    "cullington_bomb": [
        "The Final Diversion",
    ],
}

Tool_upgrade_send_map = {
    "toolupgrade/blowtorch/ammo": {
        30: "Blowtorch Fuel Upgrade 1",
        40: "Blowtorch Fuel Upgrade 2",
        50: "Blowtorch Fuel Upgrade 3",
        60: "Blowtorch Fuel Upgrade 4",
    },
    "toolupgrade/shotgun/ammo": {
        24: "Shotgun Rounds Upgrade 1",
        36: "Shotgun Rounds Upgrade 2",
        48: "Shotgun Rounds Upgrade 3",
        60: "Shotgun Rounds Upgrade 4",
        72: "Shotgun Rounds Upgrade 5",
        84: "Shotgun Rounds Upgrade 6",
        96: "Shotgun Rounds Upgrade 7",
    },
    "toolupgrade/shotgun/range": {
        40: "Shotgun Damage Upgrade 1",
        60: "Shotgun Damage Upgrade 1",
    },
    "toolupgrade/shotgun/damage": {
        4: "Shotgun Rounds Upgrade 1",
        5: "Shotgun Rounds Upgrade 2",
    },
    "toolupgrade/plank/ammo": {
        16: "Plank Amount Upgrade 1",
        24: "Plank Amount Upgrade 2",
        32: "Plank Amount Upgrade 3",
        40: "Plank Amount Upgrade 4",
        48: "Plank Amount Upgrade 5",
        56: "Plank Amount Upgrade 6",
        64: "Plank Amount Upgrade 7",
    },
    "toolupgrade/plank/width": {
        4: "Plank Width Upgrade 1",
        5: "Plank Width Upgrade 2",
    },
    "toolupgrade/plank/length": {
        48: "Plank Max Length Upgrade 1",
        56: "Plank Max Length Upgrade 2",
        64: "Plank Max Length Upgrade 3",
    },
    "toolupgrade/pipebomb/ammo": {
        12: "Pipe Bomb Rounds Upgrade 1",
        18: "Pipe Bomb Rounds Upgrade 2",
        25: "Pipe Bomb Rounds Upgrade 3",
        30: "Pipe Bomb Rounds Upgrade 4",
        36: "Pipe Bomb Rounds Upgrade 5",
    },
    "toolupgrade/pipebomb/damage": {
        3: "Pipe Bomb Blast Upgrade 1",
        4: "Pipe Bomb Blast Upgrade 2",
    },
    "toolupgrade/gun/ammo": {
        12: "Gun Rounds Upgrade 1",
        18: "Gun Rounds Upgrade 2",
        24: "Gun Rounds Upgrade 3",
        30: "Gun Rounds Upgrade 4",
        36: "Gun Rounds Upgrade 5",
    },
    "toolupgrade/gun/range": {
        60: "Gun Range Upgrade 1",
        80: "Gun Range Upgrade 2",
        100: "Gun Range Upgrade 3",
    },
    "toolupgrade/gun/damage": {
        2: "Gun Damage Upgrade 1",
        3: "Gun Damage Upgrade 2",
    },
    "toolupgrade/bomb/ammo": {
        12: "Bomb Rounds Upgrade 1",
        18: "Bomb Rounds Upgrade 2",
        24: "Bomb Rounds Upgrade 3",
        30: "Bomb Rounds Upgrade 4",
        36: "Bomb Rounds Upgrade 5",
    },
    "toolupgrade/bomb/damage": {
        5: "Bomb Blast Upgrade 1",
        6: "Bomb Blast Upgrade 2",
    },
    "toolupgrade/rocket/ammo": {
        12: "Rocket Launcher Rounds Upgrade 1",
        18: "Rocket Launcher Rounds Upgrade 2",
        24: "Rocket Launcher Rounds Upgrade 3",
    },
    "toolupgrade/rocket/damage": {
        4: "Rocket Launcher Blast Upgrade 1",
        5: "Rocket Launcher Blast Upgrade 2",
    },
    "toolupgrade/booster/ammo": {
        12: "Rocket Booster Rounds Upgrade 1",
        18: "Rocket Booster Rounds Upgrade 2",
        24: "Rocket Booster Rounds Upgrade 3",
    },
    "toolupgrade/booster/power": {
        300: "Rocket Booster Power Upgrade 1",
        400: "Rocket Booster Power Upgrade 2",
    },
    "toolupgrade/booster/time": {
        6: "Rocket Booster Time Upgrade 1",
        8: "Rocket Booster Time Upgrade 2",
    },
    "toolupgrade/leafblower/power": {
        30: "Leaf Blower Power Upgrade 1",
        40: "Leaf Blower Power Upgrade 2",
        50: "Leaf Blower Power Upgrade 3",
    },
    "toolupgrade/wire/ammo": {
        12: "Cable Amount Upgrade 1",
        18: "Cable Amount Upgrade 2",
        24: "Cable Amount Upgrade 3",
    },
    "toolupgrade/wire/stretch": {
        4: "Cable Stretch Upgrade 1",
        5: "Cable Stretch Upgrade 2",
    },
    "toolupgrade/turbo/ammo": {
        12: "Vehicle Thruster Rounds Upgrade 1",
        18: "Vehicle Thruster Rounds Upgrade 2",
        36: "Vehicle Thruster Rounds Upgrade 3",
    },
    "toolupgrade/turbo/power": {
        300: "Vehicle Thruster Power Upgrade 1",
        400: "Vehicle Thruster Power Upgrade 2",
    },
    "toolupgrade/explosive/ammo": {
        8: "Nitroglycerin Rounds Upgrade 1",
        12: "Nitroglycerin Rounds Upgrade 2",
        16: "Nitroglycerin Rounds Upgrade 3",
    },
    "toolupgrade/explosive/damage": {
        6: "Nitroglycerin Blast Upgrade 1",
        7: "Nitroglycerin Blast Upgrade 2",
        8: "Nitroglycerin Blast Upgrade 3",
    },
    "toolupgrade/rifle/ammo": {
        12: "Hunting Rifle Rounds Upgrade 1",
        18: "Hunting Rifle Rounds Upgrade 2",
    },
    "toolupgrade/steroid/ammo": {
        3: "BlueTide Bottles Upgrade 1",
        4: "BlueTide Bottles Upgrade 2",
    },
    "toolupgrade/steroid/time": {
        5: "BlueTide Duration Upgrade 1",
        6: "BlueTide Duration Upgrade 2",
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

        print("DEBUG: Waiting for items to be received from server...")
        while not self.items_received:
            await asyncio.sleep(0.5)
        await asyncio.sleep(1.0)

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

            # Find or Create the player_data node
            self.player_data = root.find("savegame/mod/steam-3708322400")


            print(f"DEBUG: player_data found: {self.player_data is not None}")
            if self.player_data is not None:
                print(f"DEBUG: player_data tag: {self.player_data.tag}")


            if self.player_data is None:
                mod_node = root.find("mod")
                if mod_node is None:
                    mod_node = ET.SubElement(root, "mod")
                self.player_data = ET.SubElement(mod_node, "steam-3708322400")

            # Now use self.player_data to build/reset the structure
            for category, nodes in SAVE_TEMPLATE.items():

                print(f"DEBUG: Processing Category: {category}")
                cat_node = self.player_data.find(category)
                if cat_node is None:
                    print(f"DEBUG: Category '{category}' not found, creating new SubElement.")

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

                            print(f"DEBUG: Setting [{full_path}] to value: {val}")
                            child.set("value", str(val))  # Ensure val is a string

                        current = child
            last_node = self.player_data.find("lastcompleted")
            if last_node is None:
                last_node = ET.SubElement(self.player_data, "lastcompleted")
            last_node.set("value", "")

            for message_node in self.player_data.findall("message"):
                self.player_data.remove(message_node)
                print(f"DEBUG: Pruned message node: {message_node.tag}")

            self.apply_server_state_to_xml(self.player_data)

            for i in range(5):  # Try 5 times
                try:
                    ET.indent(tree, space="          ", level=0)
                    tree.write(self.savegame_path, encoding="UTF-8", xml_declaration=False)
                    return True
                except PermissionError:
                    time.sleep(0.2)
                    print("Teardown Save: Player Data initialized and globally set.")
            return False

        except Exception as e:
            print(f"Failed to initialize player_data: {e}")
            traceback.print_exc()

    def apply_server_state_to_xml(self, player_data):
        received_counts = {}
        print(f"DEBUG: Total items in self.items_received: {len(self.items_received)}")

        for item in self.items_received:
            item_id = item.item  # This is the raw integer ID (e.g., 41, 42)
            received_counts[item_id] = received_counts.get(item_id, 0) + 1
            print(f"DEBUG: Counted Item ID {item_id}")

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
            print(f"DEBUG: XML Update - {path} set to {value}")

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

            print(f"DEBUG: {ap_id} -> {path} is now {final_val} (Base {base} + {count} items)")
            update_node(path, final_val)


    def sync_savegame(self):
        if not self.savegame_path:
            return

        # We still need to parse the tree to save it, but we use our stored node
        tree = ET.parse(self.savegame_path)

        self.check_tools()
        self.apply_received_items()

        for i in range(5):  # Try 5 times
            try:
                ET.indent(self.player_data.getroottree(), space="          ", level=0)
                tree.write(self.savegame_path, encoding="UTF-8", xml_declaration=False)
                return True
            except PermissionError:
                time.sleep(0.2)
        return False

    def check_missions(self):
        if self.player_data is None:
            return

        last_node = self.player_data.find("lastcompleted")
        if last_node is None:
            return

        mission_id = last_node.get("value")

        if mission_id and mission_id in Mission_upgrade_send_map:
            # 1. Get the list of names for this mission
            location_names = Mission_upgrade_send_map[mission_id]

            self.send_msgs([{
                "cmd": "Set",
                "key": f"Teardown-{self.auth}-Missions",
                "default": 0,
                "want_reply": True,  # This triggers the 'SetReply' packet we need
                "operations": [{"operation": "add", "value": 1}]
            }])

            # 2. Find the actual score path (we can assume mission/ID/score for consistency)
            score_node = self.player_data.find(f"mission/{mission_id}/score")

            if score_node is not None:
                current_score = int(score_node.get("value", "0"))

                # 3. Loop from 1 up to the current score
                for i in range(1, current_score + 1):
                    # We subtract 1 because lists start at 0 (Score 1 = index 0)
                    index = i - 1

                    # Safety check: make sure the score isn't higher than our list
                    if index < len(location_names):
                        loc_name = location_names[index]
                        self.send_upgrade_check(loc_name)

            # 4. Clear the trigger
            last_node.set("value", "")


    def check_tools(self):
        if self.player_data is None:
            return
        for xml_path, thresholds in Tool_upgrade_send_map.items():
            node = self.player_data.find(xml_path)

            if node is not None:
                current_val = int(node.get("value", "0"))

                for threshold, location_name in thresholds.items():
                    if current_val >= threshold:
                        self.send_upgrade_check(location_name)

    def send_upgrade_check(self, location_name):
        # 1. Use the built-in Archipelago name-to-ID mapper
        # This replaces your 'get_location_id_from_name' which was missing
        location_id = self.location_name_to_id.get(location_name)

        if location_id is not None:
            # 2. Check if we haven't already sent this location to the server
            if location_id not in self.checked_locations:
                # 3. Add to local list to prevent spamming the same check
                self.locations_checked.append(location_id)

                # 4. SEND THE DATA TO THE SERVER
                # This is the part that actually gives the player the item!
                asyncio.create_task(self.send_msgs([{"cmd": "LocationChecks", "checks": [location_id]}]))

                print(f"Success: Sent check for {location_name} (ID: {location_id})")
        else:
            print(f"Error: Could not find an ID for location name: {location_name}")


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

    def apply_received_items(self):
        changed = False

        # 1. TALLY EVERYTHING
        # This counts how many of each item you have received from Archipelago
        received_item_counts = {}
        for network_item in self.items_received:
            item_name = self.item_names.lookup_in_game(network_item.item)
            received_item_counts[item_name] = received_item_counts.get(item_name, 0) + 1

        # 2. HANDLE MISSIONS & TOOLS (The 0 or 1 unlocks)
        # We loop through your Missionmap and Toolmap
        for item_name, xml_path in {**Missionmap, **Toolmap}.items():
            if item_name in received_item_counts:
                # If we have the item, ensure the XML is set to "1"
                if self.update_xml_value(self.player_data, xml_path, "value", "1"):
                    changed = True

        # 3. HANDLE PROGRESSIVE UPGRADES (The numeric values)
        # We loop through your Tool_upgrade_send_map
        for xml_path, value_dict in Tool_upgrade_send_map.items():
            # Get all threshold numbers (e.g., [24, 36, 48]) and sort them
            thresholds = sorted(value_dict.keys())

            # Count how many total upgrades we have for THIS specific tool path
            # (e.g. adding up "Shotgun Rounds 1", "Shotgun Rounds 2", etc.)
            total_upgrades = 0
            for val_name in value_dict.values():
                total_upgrades += received_item_counts.get(val_name, 0)

            if total_upgrades > 0:
                # Find the correct threshold. If they have 2 items, pick the 2nd number.
                # Use min() so we don't index out of range if they have extra items.
                idx = min(total_upgrades - 1, len(thresholds) - 1)
                target_value = thresholds[idx]

                # Update the XML (update_xml_value handles the "don't downgrade" check)
                if self.update_xml_value(self.player_data, xml_path, "value", str(target_value)):
                    changed = True

        return changed




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
            asyncio.create_task(self.send_msgs([{"cmd": "Get", "keys": [f"Teardown-{self.auth}-Missions"]}]))
            self.location_name_to_id = args.get("slot_info", {}).get("location_name_to_id", {})
            self.last_connected_slot = self.slot
            asyncio.create_task(self.reset_and_initialize_save())


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
        while not ctx.exit_event.is_set():
            if ctx.savegame_path and os.path.exists(ctx.savegame_path):
                ctx.sync_savegame()
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