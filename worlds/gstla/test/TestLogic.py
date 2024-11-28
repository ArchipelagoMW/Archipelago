import json
import os
import typing
from typing import List, Dict, Any, TYPE_CHECKING, Set

from mypy.checkexpr import defaultdict

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
    "Lash_Pebble": ItemName.Lash_Pebble,
    "Boss_Briggs": ItemName.Briggs_defeated,
    "BriggsEscaped": ItemName.Briggs_escaped,
    # "FlagPiers": ItemName.Piers,
    "Boss_Serpent": ItemName.Serpent_defeated,
    "GabombaCleared": ItemName.Gabomba_Statue_Completed,
    "ShipWings": ItemName.Wings_of_Anemos,
    "Boss_Poseidon": ItemName.Poseidon_defeated,
    "Boss_Moapa": ItemName.Moapa_defeated,
    "Boss_AquaHydra": ItemName.Aqua_Hydra_defeated,
    "Boss_FlameDragons": ItemName.Flame_Dragons_defeated,
    "Mars Star": ItemName.Mythril_Bag_Mars,
    "Boss_Avimander": ItemName.Briggs_escaped,
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
    # "Boss_Avimander",
    "Boss_Valukar",
    "ShipRevisit",
    "Reunion",
    "VanillaCharacters",
    "Boss_Sentinel",
    # "Boss_KingScorpion",
    "Boss_StarMagician",
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

special_reqs = {
    "YampiBackside": [
        [
            "SkipOobEasy",
        ],
        [
            "Scoop Gem"
        ],
        [
            "Ship"
        ],
        [
            "Sand"
        ]
    ],
    "GondowanAccess": [
        [
            "Ship"
        ],
        [
            "Boss_Briggs",
            "Frost Jewel",
        ],
        [
            "Boss_Briggs",
            "Scoop Gem",
        ],
        [
            "SkipOobHard",
            "Whirlwind",
        ]
    ],
    "MagmaInterior": [
        [
            "Burst Brooch",
            "Growth",
            "Lash Pebble"
        ]
    ],
    "FlagPiers": [
        [
            "Lash Pebble",
        ],
        # [
        #     "Skips_SanctumWarp"
        # ]
    ],
    "Boss_KingScorpion": [
        [
            "Pound Cube",
        ]
    ],
    "Boss_Poseidon": [
        [
            "Trident",
            "Ship",
        ]
    ],
    "Boss_FlameDragons": [
        [
            "Pound Cube",
            "Grindstone",
            "Burst Brooch",
            "Blaze",
            "Reveal",
            "Teleport Lapis",
        ]
    ],
    "Boss_Serpent": [

        [
            # "AnyDjinn_16",
            "Growth",
            "Dancing Idol",
            "Cyclone Chip",
            "Whirlwind"
        ],
        [
            # "AnyDjinn_16",
            "Skips_Maze",
            "Dancing Idol",
            "Cyclone Chip",
            "Whirlwind"
        ],
        [
            # "AnyDjinn_24",
            "Growth",
            "Dancing Idol",
            "Cyclone Chip"
        ],
        [
            # "AnyDjinn_24",
            "Skips_Maze",
            "Dancing Idol",
            "Cyclone Chip"
        ]
    ],
    "GabombaCleared": [
        [
            "Lash Pebble",
            "Pound Cube"
        ],
        [
            "Skips_SaveQuitRG",
            "FlagPiers",
            "Scoop Gem",
            "Pound Cube"
        ]
    ],
    "Reunion": [
        [
            # ItemName.Jupiter_Beacon_Lit,
            # ItemName.Wings_of_Anemos,
            "Cyclone Chip",
            "Hover Jade",
            "Reveal",
            "Red Key",
            "Blue Key",
            "Pound Cube"
        ]
    ],
    "BriggsEscaped": [
        [
            ItemName.Briggs_defeated,
            "Lash Pebble",
            "Pound Cube",
            "Burst Brooch"
        ],
        [
            ItemName.Briggs_defeated,
            "Skips_SaveQuitRG",
            "Burst Brooch"
        ],
        [
            "Skips_SandGlitch",
            "Sand"
        ]
    ]
}



class AccessRequirements:

    def __init__(self, requirements: typing.Iterable[str]):
        self.requirements = set(requirements)
        self.has_skips = len([x for x in self.requirements if x in skips]) > 0

    def __repr__(self):
        return f"reqs: {self.requirements} has_skip: {self.has_skips}"


def filter_set_dupes(a: typing.Union[typing.Sized,typing.Iterable[AccessRequirements]]):
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
        3908, # Naribwe - Thorn Crown
        3909, # Naribwe - Reveal Circle
        # Next three are Kobombo Mountains
        3913, # North Screen
        3914, # North Screen Two
        3916, # North Screen Cave
        # Alhafran Cave
        3877,  # Cave Left Side
        3878,  # Cave Left Side Two
        3879,  # Cave Left Side Three
        3982, # Power Bread
        3983, # Right Side
        3984, # Right Side Two
        3985, # Right Side Three
        # Gabomba Catacombs
        3923, # B2F - North Room Weeds
        3987, # Tomegathericon
        # Kibombo
        3919, # North-West House - Jar
        3920, # Inn - Upstairs Barrel flag
        # Character Starting Inventories:
        257, # Carry
        258, # Lift
        259, # Force
        260, # Catch

    }

    other_exclusions = {
        "VanillaCharacters",
        "ShipOpen",
        "FlagPiers"
    }

    def __init__(self):
        self.location_reqs: List[LocationRequirements] = []
        self.flag_data: Dict[str, FlagData] = {}

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

        flags_expanded = True
        while flags_expanded:
            flags_expanded = False
            for datum in self.flag_data.values():
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
                    print(len(self.location_reqs))
                    print("expanded")

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
            result += [x for i,x in enumerate(loc_reqs) if not remove_list[i]]

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
        self.location_reqs = {x for x in self.location_reqs if not x.requirements.intersection(LocationLogic.other_exclusions)}
        for data in self.flag_data.values():
            data.reqs = [x for x in data.reqs if not x.requirements.intersection(LocationLogic.other_exclusions)]
            # for access_req in data.reqs:
            #     access_req.requirements = {x for x in access_req.requirements if not x.startswith("AnyDjinn")}


    def translate_remaining(self):
        for loc in self.location_reqs:
            loc.requirements = {requirement_map.get(x,x) for x in loc.requirements}


    def expand_flag(self, reqs: LocationRequirements, data: FlagData) -> typing.Optional[List[LocationRequirements]]:
        result: List[LocationRequirements] = []
        if data.name in reqs.requirements:
            new_reqs = set(reqs.requirements)
            # for req in reqs.requirements:
            #     new_reqs.add(req)
            # new_reqs |= reqs.requirements
            new_reqs.remove(data.name)
            if data.name in requirement_map:
                new_reqs.add(requirement_map[data.name])
            for flag_reqs in data.reqs:
                result.append(LocationRequirements(reqs.flag, flag_reqs, new_reqs))

        return None if len(result) == 0 else result

    def __repr__(self):
        return f"locations: {self.location_reqs} flags: {self.flag_data}"


class TestLoad(GSTestBase):
    options = {
        'omit_locations': 0,
        'item_shuffle': 3,
        'reveal_hidden_item': 0,
        'djinn_logic': 0,
        'character_shuffle': 2,
    }


    def setUp(self) -> None:
        super().setUp()
        world = self.get_world()
        self.locations_by_flag: Dict[int, 'GSTLALocation'] = {
            x.rando_flag: world.get_location(loc_names_by_id[x.ap_id])
            for x in all_locations if x.loc_type != LocationType.Event and x.loc_type != LocationType.Djinn
        }
        self.test_state = world.multiworld.state.copy()
        self.event_items: Dict[str, ItemData] = {}
        for event in events:
            self.event_items[event.name] = event
        for _ in range(72):
            self.test_state.collect(world.create_item(ItemName.Fizz), True)
        for _ in range(7):
            self.test_state.collect(world.create_item(ItemName.Isaac), True)
        # self.test_state.collect(world.create_item(ItemName.Black_Crystal), True)

    def test_load(self):
        logic = LocationLogic()
        dir_name = os.path.join(SCRIPT_DIR, '..', 'data', 'location_logic')
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
                logic.load(json_data)

        logic.filter_skips()
        logic.filter_djinn_reqs()
        logic.filter_other()

        logic.filter_excluded_flags()
        logic.expand_flags()

        logic.translate_remaining()
        logic.filter_dupes()
        print(len(logic.location_reqs))
        for reqs in logic.location_reqs:
            print(reqs)

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
            with self.subTest(f"Can access {location.name} with flag {flag} with no items", flag=loc.flag, reqs=loc.requirements):
                state = self.test_state.copy()
                self.assertTrue(location.can_reach(state))
        else:
            for req in reqs:
                without_req = set(reqs)
                without_req.remove(req)

                with self.subTest(f"Cannot access {location.name} flag {flag} without {req}", req=req, reqs=reqs):
                    state = self.test_state.copy()
                    items = self.get_items_and_events(without_req)
                    self.verify_item_length(items, without_req)

                    for item in items:
                        self.assertTrue(state.collect(item, prevent_sweep=True))
                    self.assertFalse(location.can_reach(state),
                                     f"Could reach {location.name} with flag {hex(flag)} without {req} but with {without_req} with state {state.prog_items}")

            with self.subTest(f"Can access {location.name} flag {flag} with all reqs", reqs=reqs):
                # state = world.multiworld.state.copy()
                state = self.test_state.copy()
                items = self.get_items_and_events(reqs)
                self.verify_item_length(items, reqs)
                for item in items:
                    self.assertTrue(state.collect(item, False))
                self.assertTrue(location.can_reach(state), f"Location {location} with flag {hex(flag)} cannot be reached with items {items} state {state.prog_items}")


class LogicData:
    def __init__(self, json_data: Dict[str, Any], name: str):
        self.access_requirements = LogicData._transform_item_requirements(json_data['Access'])
        # TODO: fix when rando fixes
        # if name == "YampiDesertCave":
        #     self.access_requirements[0].remove("YampiBackside")
        self.treasure_requirements: Dict[int, List[List[str]]] = {}
        for treasure in json_data['Treasure']:
            self.treasure_requirements[int(treasure['Addr'], 16)] = LogicData._transform_item_requirements(treasure['Reqs'])
        self.name = name

    @staticmethod
    def _transform_item_requirements(req: List[List[str]]) -> List[List[str]]:
        # ret = []
        # for option in req:
        #     result = []
        #     for item in option:
        #         result.append(requirement_map.get(item, item))
        #     ret.append(result)
        # return ret
        return LogicData.cleanup_access_reqs(req)

    @staticmethod
    def cleanup_access_reqs(reqs_of_reqs: List[List[str]]) -> List[List[str]]:
        ret = []
        for reqs in reqs_of_reqs:
            funny_val = None
            for req in reqs:
                if req in special_reqs:
                    # assumes only one funny val in each list
                    funny_val = req
                    break

            if funny_val is not None:
                reqs.remove(funny_val)
                result = set()
                # if not reqs:
                #     for special in special_reqs[funny_val]:
                #         # result = []
                #         for item in special:
                #             result.add(requirement_map.get(item, item))
                # else:
                #     for special in special_reqs[funny_val]:
                #         for item in special:
                #             result.add(requirement_map.get(item, item))
                #         result |= set(reqs)
                for special in special_reqs[funny_val]:
                    for item in special:
                        result.add(requirement_map.get(item, item))
                    # result |= set(reqs)
                extra = requirement_map.get(funny_val, None)
                if extra is not None:
                    result.add(extra)
                for item in reqs:
                    result.add(requirement_map.get(item, item))
                ret.append(result)
            else:
                result = set()
                for item in reqs:
                    result.add(requirement_map.get(item, item))
                ret.append(result)
            print(ret)
        return ret

locations_by_flag = {
    x.rando_flag: x
    for x in all_locations if x
}

class TestTreasureLogic(GSTestBase):
    options = {
        'omit_locations': 0,
        'item_shuffle': 3,
        'reveal_hidden_item': 0,
        'djinn_logic': 0,

        # 'character_shuffle': 0
    }


    def setUp(self) -> None:
        super().setUp()
        world = self.get_world()
        self.locations_by_flag: Dict[int, 'GSTLALocation'] = {
                x.rando_flag: world.get_location(loc_names_by_id[x.ap_id])
                for x in all_locations if x.loc_type != LocationType.Event and x.loc_type != LocationType.Djinn
            }
        self.test_state = world.multiworld.state.copy()
        self.event_items: Dict[str, ItemData] = {}
        for event in events:
            self.event_items[event.name] = event
        for _ in range(72):
            self.test_state.collect(world.create_item(ItemName.Fizz), True)
        for _ in range(7):
            self.test_state.collect(world.create_item(ItemName.Isaac), True)

    def test_treasure_logic(self):
        # TODO:
        # YampiBackside, GondowanAccess need special handling
        dir_name = os.path.join(SCRIPT_DIR, '..', 'data', 'location_logic')
        for file_name in os.listdir(dir_name):
            if not file_name.endswith(".json"):
                continue
            if file_name != "Kibombo.json":
                # Kibombo is a hot mess right now due to new character shuffle
                continue
            if file_name == "Contigo.json" or file_name == "Idejima.json":
                # Character shuffle is making these files difficult
                continue
            # if not file_name == "MarsLighthouse.json":
            #     continue
            with open(os.path.join(dir_name, file_name)) as logic_file:
                logic_data = LogicData(json.load(logic_file), file_name[:-5])
            with self.subTest("Test Area", name=logic_data.name):
                self.run_region_logic_test(logic_data)
        # with open(
        #                        # 'AnkohlRuins.json')) as logic_file:
        #                         'Daila.json')) as logic_file:
        #     logic_data = LogicData(json.load(logic_file), logic_file.name)
        # # access_requirements = transform_access_requirements(logic_data["Access"])
        # with self.subTest("Test Area", name=logic_data.name):
        #     self.run_region_logic_test(logic_data)

    def cleanup_access_reqs(self, reqs_of_reqs: List[List[str]], name: typing.Optional[str] = '') -> List[List[str]]:
        ret = []
        for reqs in reqs_of_reqs:
            funny_val = None
            for req in reqs:
                if req in special_reqs:
                    # assumes only one funny val in each list
                    funny_val = req
                    break

            if funny_val is not None:
                reqs.remove(funny_val)
                result = set()
                if not reqs:
                    for special in special_reqs[funny_val]:
                        # result = []
                        for item in special:
                            result.add(requirement_map.get(item, item))
                        # ret.append(result)
                        # print(name)
                        # print(ret)
                else:
                    for special in special_reqs[funny_val]:
                        # result = set()
                        for item in special:
                            result.add(requirement_map.get(item, item))
                        # print(result)
                        result |= set(reqs)
                        # print(result)
                        # ret.append(result)
                        # print(name)
                        # print(ret)
                extra = requirement_map.get(funny_val, None)
                if extra is not None:
                    result.append(extra)
                ret.append(result)
            else:
                ret.append(reqs)
                # print(name)
                # print(ret)
        return ret

    def run_region_logic_test(self, logic_data: LogicData):
        access_requirements = logic_data.access_requirements if logic_data.access_requirements else [[]]
        # world = self.get_world()
        # access_requirements = self.cleanup_access_reqs(access_requirements, logic_data.name)
        access_options_for_locations: defaultdict[int, List[Set[str]]] = defaultdict(lambda: [])
        for access_index, access_reqs in enumerate(access_requirements):
            loc_reqs = set(access_reqs)
            for flag, treasure_requirements in logic_data.treasure_requirements.items():
                treasure_reqs = treasure_requirements if treasure_requirements else [[]]

                # treasure_reqs = self.cleanup_access_reqs(treasure_reqs)
                for treasure_index, reqs in enumerate(treasure_reqs):
                    total_reqs = loc_reqs | set(reqs)
                    # print(total_reqs)
                    access_options_for_locations[flag].append(total_reqs)

        for flag, access_options_for_location in access_options_for_locations.items():
            remove_list = [False for _ in access_options_for_location]
            for i, access_reqs in enumerate(access_options_for_location):
                for j, other_reqs in enumerate(access_options_for_location):
                    if i == j:
                        continue
                    if access_reqs == other_reqs and i > j:
                        continue
                    # remove_list[i] = access_reqs.issubset(other_reqs)
                    remove_list[i] |= access_reqs.issuperset(other_reqs)
            final_list = [access_options_for_location[i] for i in range(len(access_options_for_location))
                          if not remove_list[i]]
            # print(flag)
            # print(remove_list)
            # print(final_list)
            for final_reqs in final_list:
                self.run_sub_test(logic_data, flag, final_reqs)

    def get_items_and_events(self, item_names: typing.Union[str, typing.Iterable[str]]) -> typing.List[Item]:
        items = self.get_items_by_name(item_names)
        for item_name in item_names:
            if item_name in self.event_items:
                items.append(self.world.create_item(item_name))
        return items

    def verify_item_length(self, ap_items, rando_items) -> None:
        if len(ap_items) == len(rando_items):
            return

        if len(ap_items) > len(rando_items):
            raise AssertionError("Impossible code flow found")
        count = 0
        for item in rando_items:
            if item in omitted_items:
                count += 1

        if len(ap_items) + count != len(rando_items):
            raise AssertionError(f"Item lengths do not match {ap_items} vs {rando_items}")

    def run_sub_test(self, logic_data: LogicData, flag: int, reqs: Set[str]):
        world = self.get_world()
        location = self.locations_by_flag[flag]
        for req in reqs:
            if req in skips:
                return
        if not reqs:
            with self.subTest(f"Can Access {location.name} with flag {hex(flag)} with no items", reqs=reqs):
                # state = world.multiworld.state.copy()
                state = self.test_state.copy()
                self.assertTrue(location.can_reach(state))
        else:
            for req in reqs:
                if req in omitted_items:
                    continue
                without_req = set(reqs)
                without_req.remove(req)

                with self.subTest(f"Cannot access {location.name} with missing Req", req=req, reqs=reqs):
                    # state = world.multiworld.state.copy()
                    state = self.test_state.copy()
                    items = self.get_items_and_events(without_req)
                    self.verify_item_length(items, without_req)
                    for item in items:
                        self.assertTrue(state.collect(item, True))
                    self.assertFalse(location.can_reach(state),
                                     f"Could reach {location.name} with flag {hex(flag)} without {req} but with {without_req} with state {state.prog_items}")

            with self.subTest(f"Can access with all reqs", reqs=reqs):
                # state = world.multiworld.state.copy()
                state = self.test_state.copy()
                items = self.get_items_and_events(reqs)
                self.verify_item_length(items, reqs)
                for item in items:
                    self.assertTrue(state.collect(item, False))
                self.assertTrue(location.can_reach(state), f"Location {location} with flag {hex(flag)} cannot be reached with items {items} state {state.prog_items}")
