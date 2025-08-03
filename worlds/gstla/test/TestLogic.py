from __future__ import annotations

import json
import os
import typing
from collections import defaultdict
from typing import List, Dict, Any, TYPE_CHECKING, Set

from BaseClasses import CollectionState, Item
from . import GSTestBase
from .. import ItemName, all_locations, loc_names_by_id, LocationType
from ..gen.ItemData import events, ItemData, djinn_items

SCRIPT_DIR = os.path.join(os.path.dirname(__file__))

if TYPE_CHECKING:
    from .. import GSTLALocation, GSTLAWorld

requirement_map = {
    # "Ship": ItemName.Ship,
    # "Whirlwind": ItemName.Whirlwind,
    # "Sand": ItemName.Sand,
    # "Lash_Pebble": ItemName.Lash_Pebble,
    # "Boss_Briggs": ItemName.Briggs_defeated,
    # "BriggsEscaped": ItemName.Briggs_escaped,
    # "FlagPiers": ItemName.Piers,
    # "Boss_Serpent": ItemName.Serpent_defeated,
    # "GabombaCleared": ItemName.Gabomba_Statue_Completed,
    "ShipWings": ItemName.Wings_of_Anemos,
    # "Boss_Poseidon": ItemName.Poseidon_defeated,
    # "Boss_Moapa": ItemName.Moapa_defeated,
    # "Boss_AquaHydra": ItemName.Aqua_Hydra_defeated,
    # "Boss_FlameDragons": ItemName.Flame_Dragons_defeated,
    # "Mars Star": ItemName.Mythril_Bag_Mars,
    # "Boss_Avimander": ItemName.Briggs_escaped,
}

omitted_items = {
    "Boss_Dullahan",
    "Skips_BasicRG",
    "Skips_Missable",
    "Skips_OOBRG",
    "Skips_Maze",
    "SkipOobEasy",
    "SkipOobHard",
    "Skips_DeathStorage",
    "Skips_SanctumWarp",
    "Skips_WiggleClip",
    "Skips_SandGlitch",
    "Skips_SaveQuitRG",
    # "GabombaCleared",
    # "Piers",
    # "Boss_Avimander",
    # "Boss_Valukar",
    # "ShipRevisit",
    # "Reunion",
    # "VanillaCharacters",
    # "Boss_Sentinel",
    # "Boss_KingScorpion",
    # "Boss_StarMagician",
}

skips = {
    "Skips_BasicRG",
    "Skips_Missable",
    "Skips_SandGlitch",
    "Skips_Maze",
    "Skips_OOBRG",
    "SkipOobHard",
    "SkipOobEasy",
    "Skips_DeathStorage",
    "Skips_SanctumWarp",
    "Skips_WiggleClip",
    "Skips_SaveQuitRG",
}


class AccessRequirements:

    def __init__(self, requirements: typing.Iterable[str]):
        self.requirements = set(requirements)
        self.has_skips = len([x for x in self.requirements if x in skips]) > 0

    def __repr__(self):
        return f"reqs: {self.requirements} has_skip: {self.has_skips}"


def filter_set_dupes(a: typing.Union[typing.Sized, typing.Iterable[AccessRequirements]]):
    result = []
    remove_list: List[bool] = [False for _ in range(len(a))]
    for i, first in enumerate(a):
        for j, second in enumerate(a):
            if i == j:
                continue
            if first == second and i > j:
                continue
            remove_list[i] |= first.requirements.issuperset(second.requirements)
    result += [x for i, x in enumerate(a) if not remove_list[i]]
    return result


class LocationRequirements:

    def __init__(self, flag: int, access_reqs: typing.Optional[AccessRequirements], requirements: typing.Iterable[str]):
        self.flag = flag
        self.requirements: Set[str] = set(requirements)
        if access_reqs is not None:
            self.requirements |= access_reqs.requirements
        self.has_skips = len([x for x in self.requirements if x in skips]) > 0

    def __repr__(self):
        return f"flag: {hex(self.flag)} reqs: {self.requirements} skips: {self.has_skips}"


class FlagData:

    def __init__(self, name: str, flag_type: str, reqs: List[AccessRequirements]):
        self.name = name
        self.flag_type = flag_type
        self.reqs = reqs

    def __repr__(self):
        return f"name: {self.name} type: {self.flag_type} reqs: {self.reqs}"


class LocationLogic:
    # Locations that don't behave properly with these tests, so we omit them from the tests
    exclude_flags = {
        # 2490, # Gaia Rock Sand Tablet
        # 3908, # Naribwe - Thorn Crown
        # 3909, # Naribwe - Reveal Circle
        # Next three are Kobombo Mountains
        # 3913, # North Screen
        # 3914, # North Screen Two
        # 3916, # North Screen Cave
        # Alhafran Cave
        # 3877,  # Cave Left Side
        # 3878,  # Cave Left Side Two
        # 3879,  # Cave Left Side Three
        # 3982, # Power Bread
        # 3983, # Right Side
        # 3984, # Right Side Two
        # 3985, # Right Side Three
        # Gabomba Catacombs
        # 3923, # B2F - North Room Weeds
        # 3987, # Tomegathericon
        # Kibombo
        # 3919,  # North-West House - Jar
        # 3920,  # Inn - Upstairs Barrel flag
        # Character Starting Inventories:
        261, # Douse Drop
        262, # Frost Jewel
        257,  # Carry
        258,  # Lift
        259,  # Force
        260,  # Catch
    }

    other_exclusions = {
        "VanillaCharacters",
        "ShipOpen",
        # "FlagPiers"
    }

    def __init__(self):
        self.location_reqs: List[LocationRequirements] = []
        self.flag_data: Dict[str, FlagData] = {}
        # piers = [
        #     [
        #         "Lash Pebble",
        #         "Ship"
        #     ],
        #     [
        #         "Boss_Briggs",
        #         "Frost Jewel",
        #         "Lash Pebble",
        #     ],
        #     [
        #         "Boss_Briggs",
        #         "Scoop Gem",
        #         "Lash Pebble",
        #         "Whirlwind",
        #     ],
        # ]
        # self.flag_data["FlagPiers"] = FlagData("FlagPiers","Flag", [AccessRequirements(x) for x in piers])

    def load(self, data: Dict[str, Any]):

        access_data = [AccessRequirements(x) for x in data['Access']]

        for datum in data['Treasure']:
            flag = int(datum['Addr'], 16)
            reqs = datum['Reqs']
            for req in reqs:
                if access_data:
                    for access_datum in access_data:
                        self.location_reqs.append(LocationRequirements(flag, access_datum, req))
                else:
                    self.location_reqs.append(LocationRequirements(flag, None, req))

        for datum in data['Special']:
            name = datum['Name']
            reqs = [AccessRequirements(x) for x in datum['Reqs']]
            result = []
            for req in reqs:
                if access_data:
                    for access_datum in access_data:
                        if name in access_datum.requirements:
                            continue
                        result.append(AccessRequirements(req.requirements | access_datum.requirements))
                else:
                    result.append(AccessRequirements(req.requirements))
            self.flag_data[name] = FlagData(name, datum["Type"], filter_set_dupes(result))

    def expand_flags(self) -> None:

        outer_flags_expanded = True
        # count = 0
        while outer_flags_expanded:
            outer_flags_expanded = False
            flags_expanded = False
            # count += 1
            for datum in self.flag_data.values():
                flags_expanded = False
                new_reqs: defaultdict[int, List[LocationRequirements]] = defaultdict(lambda: [])
                for loc_reqs in self.location_reqs:
                    result = self.expand_flag(loc_reqs, datum)
                    if result is not None:
                        flags_expanded = True
                        new_reqs[loc_reqs.flag] += result
                    else:
                        new_reqs[loc_reqs.flag].append(loc_reqs)
                if flags_expanded:
                    result = []
                    for results in new_reqs.values():
                        result += filter_set_dupes(results)
                    # self.location_reqs = filter_set_dupes(new_reqs)
                    self.location_reqs = result
                    # print("foobar")
                    # print(len(self.location_reqs))
                    # print("expanded")
                outer_flags_expanded |= flags_expanded
            # print(count)

        for name in self.flag_data.keys():
            for loc in self.location_reqs:
                assert name not in loc.requirements, f"Flag {name} is in req list of {loc}"

    def filter_skips(self):
        self.location_reqs = [x for x in self.location_reqs if not x.has_skips]
        for data in self.flag_data.values():
            data.reqs = [x for x in data.reqs if not x.has_skips]

    def filter_dupes(self):
        flag_map: defaultdict[int, List[LocationRequirements]] = defaultdict(lambda: [])
        for loc in self.location_reqs:
            flag_map[loc.flag].append(loc)

        result: List[LocationRequirements] = []

        for loc_reqs in flag_map.values():
            remove_list: List[bool] = [False for _ in range(len(loc_reqs))]
            for i, first in enumerate(loc_reqs):
                for j, second in enumerate(loc_reqs):
                    if i == j:
                        continue
                    if first == second and i > j:
                        continue
                    remove_list[i] |= first.requirements.issuperset(second.requirements)
            result += [x for i, x in enumerate(loc_reqs) if not remove_list[i]]

    def filter_djinn_reqs(self):
        for loc in self.location_reqs:
            loc.requirements = {x for x in loc.requirements if not x.startswith("AnyDjinn")}
        for data in self.flag_data.values():
            for access_req in data.reqs:
                access_req.requirements = {x for x in access_req.requirements if not x.startswith("AnyDjinn")}

    def filter_excluded_flags(self):
        self.location_reqs = [loc for loc in self.location_reqs if loc.flag not in LocationLogic.exclude_flags]
        # self.location_reqs = [loc for loc in self.location_reqs if loc.flag == 0xf54]

    def filter_other(self):
        self.location_reqs = {x for x in self.location_reqs if
                              not x.requirements.intersection(LocationLogic.other_exclusions)}
        for data in self.flag_data.values():
            data.reqs = [x for x in data.reqs if not x.requirements.intersection(LocationLogic.other_exclusions)]
            # for access_req in data.reqs:
            #     access_req.requirements = {x for x in access_req.requirements if not x.startswith("AnyDjinn")}

    def translate_remaining(self):
        for loc in self.location_reqs:
            loc.requirements = {requirement_map.get(x, x) for x in loc.requirements}

    def expand_flag(self, reqs: LocationRequirements, data: FlagData) -> typing.Optional[List[LocationRequirements]]:
        result: List[LocationRequirements] = []
        if data.name in reqs.requirements:
            new_reqs = set(reqs.requirements)
            # for req in reqs.requirements:
            #     new_reqs.add(req)
            # new_reqs |= reqs.requirements
            new_reqs.remove(data.name)
            assert data.name not in new_reqs
            if data.name in requirement_map:
                new_reqs.add(requirement_map[data.name])
            for flag_reqs in data.reqs:
                result.append(LocationRequirements(reqs.flag, flag_reqs, new_reqs))

        return None if len(result) == 0 else result

    def __repr__(self):
        return f"locations: {self.location_reqs} flags: {self.flag_data}"


class TestTreasureLogic(GSTestBase):
    options = {
        'omit_locations': 0,
        'item_shuffle': 3,
        'reveal_hidden_item': 0,
        'djinn_logic': 1,
        'character_shuffle': 2,
        'lemurian_ship': 0
    }

    skip_missing_reqs: defaultdict[int, Set[str]] = defaultdict(lambda: set())

    def setUp(self) -> None:
        super().setUp()
        world = self.get_world()
        self.locations_by_flag: Dict[int, 'GSTLALocation'] = {
            x.rando_flag: world.get_location(loc_names_by_id[x.ap_id])
            for x in all_locations if x.loc_type != LocationType.Event and x.loc_type != LocationType.Djinn
        }
        self.test_state = CollectionState(self.multiworld)
        self.event_items: Dict[str, ItemData] = {}
        for event in events:
            self.event_items[event.name] = event
        for _ in range(72):
            self.test_state.collect(world.create_item(ItemName.Fizz), True)
        for _ in range(7):
            self.test_state.collect(world.create_item(ItemName.Isaac), True)

        TestTreasureLogic.skip_missing_reqs[2328] = {ItemName.Douse_Drop, ItemName.Black_Crystal, ItemName.Piers}
        TestTreasureLogic.skip_missing_reqs[3923] = {ItemName.Douse_Drop, ItemName.Black_Crystal, ItemName.Piers}
        TestTreasureLogic.skip_missing_reqs[3987] = {ItemName.Douse_Drop, ItemName.Black_Crystal, ItemName.Piers}
        TestTreasureLogic.skip_missing_reqs[2303] = {ItemName.Douse_Drop, ItemName.Black_Crystal, ItemName.Piers}
        TestTreasureLogic.skip_missing_reqs[3922] = {ItemName.Douse_Drop, ItemName.Black_Crystal, ItemName.Piers, ItemName.Pound_Cube}
        TestTreasureLogic.skip_missing_reqs[3919] = {ItemName.Douse_Drop, ItemName.Black_Crystal, ItemName.Piers}
        TestTreasureLogic.skip_missing_reqs[3920] = {ItemName.Douse_Drop, ItemName.Black_Crystal, ItemName.Piers}
        # self.test_state.collect(world.create_item(ItemName.Black_Crystal), True)

    def tearDown(self) -> None:
        self.locations_by_flag.clear()
        self.test_state = None
        super().tearDown()

    def test_treasure_logic(self):
        if True:
            pass
        logic = LocationLogic()
        dir_name = os.path.join(SCRIPT_DIR, '..', 'data', 'location_logic')

        filled_locs = self.multiworld.get_filled_locations(self.player)
        for loc in filled_locs:
            if loc.item.name == ItemName.Piers:
                loc.item.location = None
                loc.item = None
                loc.locked = False
                break
        # with open(os.path.join(dir_name, 'MagmaRock.json')) as infile:
        # with open(os.path.join(dir_name, 'MarsLighthouse.json')) as infile:
        #         json_data = json.load(infile)
        for file_name in os.listdir(dir_name):
            if not file_name.endswith(".json"):
                continue
            # if file_name == "Kibombo.json" or file_name == "Contigo.json":
            #     # Character shuffle messes with these
            #     continue
            # if file_name != "YampiDesert.json" and file_name != "YampiDesertCave.json":
            #     continue

            # if file_name not in {
            #     # "Alhafra.json",
            #     # "YampiDesert.json",
            #     # "YampiDesertCave.json",
            #     # "Champa.json",
            #     # "GondowanCliffs.json",
            #     # "AlhafranCave.json",
            #     "LemurianShip.json",
            #     # "Lemuria.json",
            #     # "SeaOfTime.json",
            #     "GabombaStatue.json",
            #     # "GabombaCatacombs.json",
            #     "Kibombo.json",
            #     # "KibomboMountains.json",
            # }:
            #     continue
            # if file_name != "LemurianShip.json":
            #     continue
            # if file_name == "Contigo.json" or file_name == "Idejima.json":
            # Character shuffle is making these files difficult
            # continue
            # if not file_name == "MarsLighthouse.json":
            #     continue
            with open(os.path.join(dir_name, file_name)) as logic_file:
                json_data = json.load(logic_file)
                if file_name == "LemurianShip.json":
                    # json_data['Access'] = [x for x in json_data['Access'] if "FlagPiers" not in x]
                    json_data['Access'] = [

                        [
                            "Black Crystal",
                            "Scoop Gem",
                            "Lash Pebble",
                            "Pound Cube",
                            "Piers"
                        ],
                        # [
                        #     "Black Crystal",
                        #     "GabombaCleared",
                        #     "FlagPiers",
                        #     "VanillaCharacters"
                        # ],
                        # [
                        #     "ShipOpen"
                        # ],
                        [
                            "Ship",
                            "Grindstone"
                        ],
                        [
                            "Ship",
                            "ShipWings",
                            "Hover Jade"
                        ],
                        [
                            "Ship",
                            "Boss_Poseidon"
                        ]
                    ]
                # elif file_name == 'GabombaStatue.json':
                #     json_data['Access'] = [[y for y in x if y != 'FlagPiers'] for x in json_data['Access']]
                #     json_data['Access'] = [
                #         [
                #             "Ship",
                #             "Lash Pebble",
                #             "Scoop Gem",
                #         ],
                #         [
                #             "Ship",
                #             "Frost Jewel",
                #             "Lash Pebble",
                #             "Scoop Gem",
                #         ],
                #         [
                #             "Boss_Briggs",
                #             "Frost Jewel",
                #             "Lash Pebble",
                #             "Scoop Gem",
                #         ],
                #         [
                #             "Ship",
                #             "Lash Pebble",
                #             "Whirlwind",
                #             "Scoop Gem",
                #         ],
                #         [
                #             "Boss_Briggs",
                #             "Lash Pebble",
                #             "Whirlwind",
                #             "Scoop Gem",
                #         ],
                #     ]
                # elif file_name == "Kibombo.json":
                #     json_data['Access'] = [
                #         [
                #             "Ship"
                #         ],
                #         [
                #             "Boss_Briggs",
                #             "Frost Jewel",
                #         ],
                #         [
                #             "Boss_Briggs",
                #             "Scoop Gem",
                #             "Lash Pebble",
                #             "Whirlwind",
                #         ],
                #     ]
                logic.load(json_data)

        logic.filter_skips()
        logic.filter_djinn_reqs()
        logic.filter_other()

        logic.filter_excluded_flags()
        logic.expand_flags()

        logic.translate_remaining()
        logic.filter_dupes()
        # print(len(logic.location_reqs))
        # for reqs in logic.location_reqs:
        #     print(reqs)

        for loc in logic.location_reqs:
            self.sub_test_location(loc)

    def get_items_and_events(self, item_names: typing.Union[str, typing.Iterable[str]]) -> typing.List[Item]:
        items = self.get_items_by_name(item_names)
        for item_name in item_names:
            if item_name in self.event_items:
                items.append(self.world.create_item(item_name))
            if item_name == ItemName.Piers:
                items.append(self.world.create_item(item_name))
        return items

    def verify_item_length(self, ap_items, rando_items) -> None:
        if len(ap_items) == len(rando_items):
            return

        if len(ap_items) > len(rando_items):
            raise AssertionError(f"Impossible code flow found {ap_items} vs {rando_items}")
        count = 0
        for item in rando_items:
            if item in omitted_items:
                count += 1

        if len(ap_items) + count != len(rando_items):
            raise AssertionError(f"Item lengths do not match {ap_items} vs {rando_items}")

    def sub_test_location(self, loc: LocationRequirements):
        reqs = loc.requirements
        flag = loc.flag
        location = self.locations_by_flag[flag]
        if not reqs:
            with self.subTest(f"Can access {location.name} with flag {flag} with no items", flag=loc.flag,
                              reqs=loc.requirements):
                state = self.test_state.copy()
                self.assertTrue(location.can_reach(state))
        else:
            for req in reqs:
                without_req = set(reqs)
                without_req.remove(req)
                if req in TestTreasureLogic.skip_missing_reqs[loc.flag]:
                    continue
                with self.subTest(f"Cannot access {location.name} flag {flag} without {req}", req=req, reqs=reqs):
                    state = self.test_state.copy()
                    items = self.get_items_and_events(without_req)
                    self.verify_item_length(items, without_req)

                    for item in items:
                        self.assertTrue(state.collect(item, prevent_sweep=False))
                    # if req in state.prog_items[self.player]:
                    #     # TODO: not a valid test in this case
                    #     continue
                    self.assertFalse(location.can_reach(state),
                                     f"Could reach {location.name} with flag {hex(flag)} without {req} but with {without_req} with state {state.prog_items}")

            with self.subTest(f"Can access {location.name} flag {flag} with all reqs", reqs=reqs):
                # state = world.multiworld.state.copy()
                state = self.test_state.copy()
                items = self.get_items_and_events(reqs)
                self.verify_item_length(items, reqs)
                for item in items:
                    self.assertTrue(state.collect(item, False))
                self.assertTrue(location.can_reach(state),
                                f"Location {location} with flag {hex(flag)} cannot be reached with items {items} state {state.prog_items}")


