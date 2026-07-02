from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Location, Region, LocationProgressType
from .items import MKSMItem
from .options import Character
from .consts import CHARACTER_PURCHASE_AMOUNTS

if TYPE_CHECKING:
    from .world import MKSMWorld

REGION_NAME_LOCATIONS = {
    "Goro's Lair 1": {
        "GL: koin inside the skeleton": 1,
        "GL: koin above the doorway": 2,
        "GL: koin from shooting the moon": 3,
        "GL: koin on the ledge after the pit": 4,
        "GL: koin from the chandelier": 5,
        "GL: koin above the breakable door": 6,
    },
    "Goro's Lair - Boss arena": {
        "GL: Oni Warlord defeated": 7,
        "GL: long jump obtained": 8,
    },
    "Goro's Lair 2": {
        "GL: koin on the ledge after the broken bridge": 9
    },
    "Wu-Shi": {
        "WSA: koin from the catapult": 10,
        "WSA: koin after the tree branch swing": 11,
        "WSA: koin after the bamboo swing": 12,
        "WSA: koin on a high wall near the lava pots": 13,
        "WSA: wu-shi academy health upgrade": 14
    },
    "Wu-Shi - Ermac arena": {
        "WSA: koin from defeating Ermac": 15,
        "WSA: Ermac defeated": 16
    },
    "Wu-Shi - Fire": {
        "WSA: koin in the small room": 17
    },
    "Wu-Shi - Wall Run area": {
        "WSA: wall run obtained": 18
    },
    "Portal 2": {
        "P: koin from performing a fatality on the dragon symbol": 19
    },
    "Netherrealm": {
        "N: koin above the arch": 20,
        "N: Scorpion defeated": 21,
        "N: Medallion from defeating Scorpion": 200,
    },
    "Forest": {
        "LF: koin behind the breakable wall": 22,
        "LF: koin behind the living tree": 23,
        "LF: koin hidden behind the waterfall": 24,
        "LF: koin near the giant snake head": 25,
        "LF: koin from shooting the closed eye": 26,
        "LF: Forest health upgrade": 27,
        "LF: koin from breaking the fast statues": 28,
    },
    "Forest - Bridges": {
        "LF: koin from shooting at dragon koin": 29,
        "LF: koin from defeating Mileena": 30,
        "LF: Mileena defeated": 31
    },
    "Forest - Reptile arena": {
        "LF: Reptile defeated": 32,
        "LF: climb obtained": 33,
    },
    "Wasteland 1": {
        "W: koin from impaling an enemy on the big spike": 34,
        "W: koin on the ledge above": 35,
        "W: koin found after freeing kabal": 36,
        "W: koin from defeating the Oni Warlord in the blood bath room": 37,
        "W: koin found on the lion statue": 38,
        "W: Kabal freed": 39,
        "W: Wasteland health upgrade": 40,
        "W: Sub-Zero defeated": 41,
    },
    "Wasteland 2": {
        "W: koin found above the spike wheel": 42
    },
    "Wasteland 3": {
        "W: koin from shooting the dragon koin": 43,
        "W: koin from goro's arena": 44,
        "W: Goro defeated": 45,
        "W: Double jump obtained": 46
    },
    "Dead Pool": {
        "DP: koin from drowning enemies in both pools": 47,
        "DP: swing obtained": 48
    },
    "Tombs": {
        "ST: koin from shooting the dragon koin near the portal": 49,
        "ST: koin above Baraka's entrance": 50,
        "ST: koin from using all three death traps": 51,
        "ST: koin from the broken statue": 52,
        "ST: koin above the broken statue": 53,
        "ST: koin from high button in the rolling spikes room": 54,
        "ST: koin above the ceiling in the room with the hooks": 55,
        "ST: koin from shooting the dragon koin in the test your might room": 56,
        "ST: koin from killing the strolling skeleton": 57,
        "ST: koin from the button after defeating orochi hellbeast": 58,
        "ST: koin from impaling an enemy on the rising spikes": 59,
        "ST: koin from launching a tarkata on the flying bird": 60,
        "ST: koin behind statue in the falling spike trap room": 61,
        "ST: koin above broken statue in the falling spike trap room": 62,
        "ST: koin near the fan": 63,
        "ST: koin from the destroyed soul tomb": 64,
    },
    "Tombs - Baraka arena": {
        "ST: Baraka defeated": 65,
        "ST: wall jump obtained": 66
    },
    "Monastery": {
        "EM: koin from shooting the dragon koin behind the window": 67,
        "EM: koin from impaling enemies on the statue's hands": 68,
        "EM: koin above the ceiling in the multality room": 69,
    },
    "Monastery - Kitana arena": {
        "EM: koin from the Kitana Mileena and Jade arena": 70,
        "EM: Kitana Mileena and Jade defeated": 71,
        "EM: Fist of Ruin obtained": 72,
    },
    "Foundry": {
        "F: koin from wall jumping above the main room": 73,
        "F: koin above the wood ceiling": 74,
        "F: koin from breaking the big pot": 75,
        "F: koin behind the fire": 76,
        "F: koin from shooting the dragon koin behind the breakable wall": 77,
        "F: koin above the lava pit": 78,
        "F: koin from smash an enemy with the big hammers": 79,
        "F: koin from breaking the pipe with the axe": 80,
        "F: Kano defeated": 81,
        "F: Shao Kahn defeated": 82,
    },
    "Menu": {
        "Purchase upgrade - Square 2": 83,
        "Purchase upgrade - Square 3": 84,
        "Purchase upgrade - Square 4": 85,
        "Purchase upgrade - Triangle 2": 86,
        "Purchase upgrade - Triangle 3": 87,
        "Purchase upgrade - Triangle 4": 88,
        "Purchase upgrade - Circle 2": 89,
        "Purchase upgrade - Circle 3": 90,
        "Purchase upgrade - Circle 4": 91,
        "Purchase upgrade - Circle 5": 92,
        "Purchase upgrade - R2 2": 93,
        "Purchase upgrade - R2 3": 94,
        "Purchase upgrade - R2 4": 95,
        "Purchase upgrade - R2 5": 96,
        "Purchase 1st combo": 97,
        "Purchase 2nd combo": 98,
        "Purchase 3rd combo": 99,
        "Purchase 4th combo": 100,
        "Purchase 5th combo": 101,
    },
}

FINISHING_MOVES_LOCATIONS = {
    Character.option_liu_kang: {
        "Perform Shaolin Soccer (Fatality)": 500,
        "Perform Bonebreak Combo (Fatality)": 501,
        "Perform Head Clap (Fatality)": 502,
        "Perform Giant Stomp (Fatality)": 503,
        "Perform Fire Kick Combo (Fatality)": 504,
        "Perform Flipping Uppercut (Fatality)": 505,
        "Perform Dragon (Fatality)": 506,
        "Perform Arm Rip (Fatality)": 507,
        "Perform Fire Trails (Multality)": 508,
        "Perform Dragon Fury (Multality)": 509,
        "Perform Rage Mode (Brutality)": 510,
    },
    Character.option_kung_lao: {
        "Perform Body Slice (Fatality)": 511,
        "Perform Mid Air Slice (Fatality)": 512,
        "Perform Friendly Rabit (Fatality)": 513,
        "Perform Tornado (Multality)": 514,
        "Perform Hat Control (Multality)": 515,
        "Perform Arm Cutter (Fatality)": 516,
        "Perform Head Toss (Fatality)": 517,
        "Perform Unfriendly Rabbit (Hidden Fatality)": 518,
        "Perform Many Chops (Fatality)": 519,
        "Perform Headache (Fatality)": 520,
        "Perform Buzzsaw (Fatality)": 521,
        "Perform Razor Edge (Brutality)": 522,
    },
    Character.option_sub_zero: {
        "Perform Spine Rip (Fatality)": 523,
        "Perform Snowball (Fatality)": 524,
        "Perform Freeze Uppercut (Fatality)": 525,
        "Perform Ice Stomp (Multality)": 526,
        "Perform Frostbite Rage (Brutality)": 527,
    },
    Character.option_scorpion: {
        "Perform Flame (Fatality)": 528,
        "Perform Spear Slice (Fatality)": 529,
        "Perform Raise Hell (Multality)": 530,
        "Perform Searing Blade (Brutality)": 531,
    }
}

LOCATION_NAME_TO_ID = {loc: loc_id for k, v in REGION_NAME_LOCATIONS.items() for loc, loc_id in v.items()}
LOCATION_NAME_TO_ID |= {loc: loc_id for k, v in FINISHING_MOVES_LOCATIONS.items() for loc, loc_id in v.items()}


class MKSMLocation(Location):
    game = "Mortal Kombat: Shaolin Monks"


def create_all_locations(world: MKSMWorld) -> None:
    create_region_locations(world)
    create_purchase_locations(world)
    create_finishing_moves_locations(world)
    create_event_locations(world)

    world.get_location("GL: koin above the doorway").progress_type = LocationProgressType.EXCLUDED
    world.get_location("GL: koin above the breakable door").progress_type = LocationProgressType.EXCLUDED


def create_region_locations(world: MKSMWorld) -> None:
    can_shoot_moon = world.options.character.value in (Character.option_liu_kang, Character.option_kung_lao)

    for region_name in REGION_NAME_LOCATIONS:
        if not region_name == world.origin_region_name:
            region = world.get_region(region_name)
            region_locations = REGION_NAME_LOCATIONS[region_name]

            if not can_shoot_moon:
                region_locations = {
                    name: loc_id for name, loc_id in region_locations.items()
                    if name != "GL: koin from shooting the moon"
                }

            region.add_locations(region_locations, MKSMLocation)


def create_purchase_locations(world: MKSMWorld) -> None:
    menu = world.get_region(world.origin_region_name)
    amounts = CHARACTER_PURCHASE_AMOUNTS[world.options.character.value]

    prefixes = ["1st", "2nd", "3rd", "4th", "5th"]

    combo_locs = {
        f"Purchase {prefixes[i]} combo": LOCATION_NAME_TO_ID[f"Purchase {prefixes[i]} combo"]
        for i in range(amounts.combo)
    }

    move_amounts = {"Square": amounts.square, "Triangle": amounts.triangle,
                    "Circle": amounts.circle, "R2": amounts.r2}
    move_locs = {
        f"Purchase upgrade - {move} {i + 2}": LOCATION_NAME_TO_ID[f"Purchase upgrade - {move} {i + 2}"]
        for move, amount in move_amounts.items()
        for i in range(amount)
    }

    menu.add_locations({**combo_locs, **move_locs}, MKSMLocation)


def create_finishing_moves_locations(world: MKSMWorld) -> None:
    menu = world.get_region(world.origin_region_name)
    current_character = world.options.character.value

    menu.add_locations(FINISHING_MOVES_LOCATIONS[current_character], MKSMLocation)


def create_event_locations(world: MKSMWorld) -> None:
    wu_shi_ermac: Region = world.get_region("Wu-Shi - Ermac arena")
    monastery_kitana: Region = world.get_region("Monastery - Kitana arena")
    forest_reptile: Region = world.get_region("Forest - Reptile arena")
    forest_bridges: Region = world.get_region("Forest - Bridges")
    tombs_baraka: Region = world.get_region("Tombs - Baraka arena")
    wasteland_3: Region = world.get_region("Wasteland 3")
    dead_pool: Region = world.get_region("Dead Pool")
    netherrealm: Region = world.get_region("Netherrealm")
    foundry: Region = world.get_region("Foundry")

    wu_shi_ermac.add_event(
        location_name="Ermac defeated event",
        item_name="Ermac defeated item",
        location_type=MKSMLocation,
        item_type=MKSMItem,
        show_in_spoiler=False
    )

    monastery_kitana.add_event(
        location_name="Kitana defeated event",
        item_name="Kitana defeated item",
        location_type=MKSMLocation,
        item_type=MKSMItem,
        show_in_spoiler=False
    )

    forest_reptile.add_event(
        location_name="Reptile defeated event",
        item_name="Reptile defeated item",
        location_type=MKSMLocation,
        item_type=MKSMItem,
        show_in_spoiler=False
    )

    forest_bridges.add_event(
        location_name="Mileena defeated event",
        item_name="Mileena defeated item",
        location_type=MKSMLocation,
        item_type=MKSMItem,
        show_in_spoiler=False
    )

    tombs_baraka.add_event(
        location_name="Baraka defeated event",
        item_name="Baraka defeated item",
        location_type=MKSMLocation,
        item_type=MKSMItem,
        show_in_spoiler=False

    )

    wasteland_3.add_event(
        location_name="Goro defeated event",
        item_name="Goro defeated item",
        location_type=MKSMLocation,
        item_type=MKSMItem,
        show_in_spoiler=False

    )

    netherrealm.add_event(
        location_name="Scorpion defeated event",
        item_name="Scorpion defeated item",
        location_type=MKSMLocation,
        item_type=MKSMItem,
        show_in_spoiler=False

    )

    foundry.add_event(
        location_name="Shao Kahn defeated event",
        item_name="Shao Kahn defeated item",
        location_type=MKSMLocation,
        item_type=MKSMItem,
        show_in_spoiler=False
    )

    foundry.add_event(
        location_name="Kano defeated event",
        item_name="Kano defeated item",
        location_type=MKSMLocation,
        item_type=MKSMItem,
        show_in_spoiler=False
    )

    dead_pool.add_event(
        location_name="Dead Pool event",
        item_name="Dead Pool item",
        location_type=MKSMLocation,
        item_type=MKSMItem,
        show_in_spoiler=False

    )
