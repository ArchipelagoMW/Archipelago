# import json
# import os
# import typing
# from typing import List, Dict, Any, TYPE_CHECKING, Set
#
# from mypy.checkexpr import defaultdict
#
# from BaseClasses import CollectionState, Item
# from . import GSTestBase
# from .. import ItemName, all_locations, loc_names_by_id, LocationType
# from ..gen.ItemData import events, ItemData, djinn_items
#
# SCRIPT_DIR = os.path.join(os.path.dirname(__file__))
#
# if TYPE_CHECKING:
#     from .. import GSTLALocation, GSTLAWorld
#
# requirement_map = {
#     # "Ship": ItemName.Ship,
#     # "Whirlwind": ItemName.Whirlwind,
#     # "Sand": ItemName.Sand,
#     "Lash_Pebble": ItemName.Lash_Pebble,
#     "Boss_Briggs": ItemName.Briggs_defeated,
#     "BriggsEscaped": ItemName.Briggs_escaped,
#     # "FlagPiers": ItemName.Piers,
#     "Boss_Serpent": ItemName.Serpent_defeated,
#     "GabombaCleared": ItemName.Gabomba_Statue_Completed,
#     "ShipWings": ItemName.Wings_of_Anemos,
#     "Boss_Poseidon": ItemName.Poseidon_defeated,
#     "Boss_Moapa": ItemName.Moapa_defeated,
#     "Boss_AquaHydra": ItemName.Aqua_Hydra_defeated,
#     "Boss_FlameDragons": ItemName.Flame_Dragons_defeated,
#     "Mars Star": ItemName.Mythril_Bag_Mars,
#     "Boss_Avimander": ItemName.Briggs_escaped,
# }
#
# omitted_items = {
#     "Boss_Dullahan",
#     "Skips_BasicRG",
#     "Skips_Missable",
#     "Skips_OOBRG",
#     "Skips_Maze",
#     "SkipOobEasy",
#     "SkipOobHard",
#     "Skips_DeathStorage",
#     "Skips_SanctumWarp",
#     "Skips_WiggleClip",
#     "Skips_SandGlitch",
#     "Skips_SaveQuitRG",
#     # "Boss_Avimander",
#     "Boss_Valukar",
#     "ShipRevisit",
#     "Reunion",
#     "VanillaCharacters",
#     "Boss_Sentinel",
#     # "Boss_KingScorpion",
#     "Boss_StarMagician",
# }
#
# no_can_handle = {
#     "Skips_BasicRG",
#     "Skips_Missable",
#     "Skips_SandGlitch",
#     "Skips_Maze",
#     "Skips_OOBRG",
#     "SkipOobHard",
#     "SkipOobEasy",
#     "Skips_DeathStorage",
#     "Skips_SanctumWarp",
#     "Skips_WiggleClip",
#     "Skips_SaveQuitRG",
# }
#
# special_reqs = {
#     "YampiBackside": [
#         [
#             "SkipOobEasy",
#         ],
#         [
#             "Scoop Gem"
#         ],
#         [
#             "Ship"
#         ],
#         [
#             "Sand"
#         ]
#     ],
#     "GondowanAccess": [
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
#         ],
#         [
#             "SkipOobHard",
#             "Whirlwind",
#         ]
#     ],
#     "MagmaInterior": [
#         [
#             "Burst Brooch",
#             "Growth",
#             "Lash Pebble"
#         ]
#     ],
#     "FlagPiers": [
#         [
#             "Lash Pebble",
#         ],
#         # [
#         #     "Skips_SanctumWarp"
#         # ]
#     ],
#     "Boss_KingScorpion": [
#         [
#             "Pound Cube",
#         ]
#     ],
#     "Boss_Poseidon": [
#         [
#             "Trident",
#             "Ship",
#         ]
#     ],
#     "Boss_FlameDragons": [
#         [
#             "Pound Cube",
#             "Grindstone",
#             "Burst Brooch",
#             "Blaze",
#             "Reveal",
#             "Teleport Lapis",
#         ]
#     ],
#     "Boss_Serpent": [
#
#         [
#             # "AnyDjinn_16",
#             "Growth",
#             "Dancing Idol",
#             "Cyclone Chip",
#             "Whirlwind"
#         ],
#         [
#             # "AnyDjinn_16",
#             "Skips_Maze",
#             "Dancing Idol",
#             "Cyclone Chip",
#             "Whirlwind"
#         ],
#         [
#             # "AnyDjinn_24",
#             "Growth",
#             "Dancing Idol",
#             "Cyclone Chip"
#         ],
#         [
#             # "AnyDjinn_24",
#             "Skips_Maze",
#             "Dancing Idol",
#             "Cyclone Chip"
#         ]
#     ],
#     "GabombaCleared": [
#         [
#             "Lash Pebble",
#             "Pound Cube"
#         ],
#         [
#             "Skips_SaveQuitRG",
#             "FlagPiers",
#             "Scoop Gem",
#             "Pound Cube"
#         ]
#     ],
#     "Reunion": [
#         [
#             # ItemName.Jupiter_Beacon_Lit,
#             # ItemName.Wings_of_Anemos,
#             "Cyclone Chip",
#             "Hover Jade",
#             "Reveal",
#             "Red Key",
#             "Blue Key",
#             "Pound Cube"
#         ]
#     ],
#     "BriggsEscaped": [
#         [
#             ItemName.Briggs_defeated,
#             "Lash Pebble",
#             "Pound Cube",
#             "Burst Brooch"
#         ],
#         [
#             ItemName.Briggs_defeated,
#             "Skips_SaveQuitRG",
#             "Burst Brooch"
#         ],
#         [
#             "Skips_SandGlitch",
#             "Sand"
#         ]
#     ]
#
# }
#
# class LogicData:
#     def __init__(self, json_data: Dict[str, Any], name: str):
#         self.access_requirements = LogicData._transform_item_requirements(json_data['Access'])
#         # TODO: fix when rando fixes
#         # if name == "YampiDesertCave":
#         #     self.access_requirements[0].remove("YampiBackside")
#         self.treasure_requirements: Dict[int, List[List[str]]] = {}
#         for treasure in json_data['Treasure']:
#             self.treasure_requirements[int(treasure['Addr'], 16)] = LogicData._transform_item_requirements(treasure['Reqs'])
#         self.name = name
#
#     @staticmethod
#     def _transform_item_requirements(req: List[List[str]]) -> List[List[str]]:
#         # ret = []
#         # for option in req:
#         #     result = []
#         #     for item in option:
#         #         result.append(requirement_map.get(item, item))
#         #     ret.append(result)
#         # return ret
#         return LogicData.cleanup_access_reqs(req)
#
#     @staticmethod
#     def cleanup_access_reqs(reqs_of_reqs: List[List[str]]) -> List[List[str]]:
#         ret = []
#         for reqs in reqs_of_reqs:
#             funny_val = None
#             for req in reqs:
#                 if req in special_reqs:
#                     # assumes only one funny val in each list
#                     funny_val = req
#                     break
#
#             if funny_val is not None:
#                 reqs.remove(funny_val)
#                 result = set()
#                 # if not reqs:
#                 #     for special in special_reqs[funny_val]:
#                 #         # result = []
#                 #         for item in special:
#                 #             result.add(requirement_map.get(item, item))
#                 # else:
#                 #     for special in special_reqs[funny_val]:
#                 #         for item in special:
#                 #             result.add(requirement_map.get(item, item))
#                 #         result |= set(reqs)
#                 for special in special_reqs[funny_val]:
#                     for item in special:
#                         result.add(requirement_map.get(item, item))
#                     # result |= set(reqs)
#                 extra = requirement_map.get(funny_val, None)
#                 if extra is not None:
#                     result.add(extra)
#                 for item in reqs:
#                     result.add(requirement_map.get(item, item))
#                 ret.append(result)
#             else:
#                 result = set()
#                 for item in reqs:
#                     result.add(requirement_map.get(item, item))
#                 ret.append(result)
#             print(ret)
#         return ret
#
# locations_by_flag = {
#     x.rando_flag: x
#     for x in all_locations if x
# }
#
# class TestTreasureLogic(GSTestBase):
#     options = {
#         'omit_locations': 0,
#         'item_shuffle': 3,
#         'reveal_hidden_item': 0,
#         'djinn_logic': 0,
#
#         # 'character_shuffle': 0
#     }
#
#
#     def setUp(self) -> None:
#         super().setUp()
#         world = self.get_world()
#         self.locations_by_flag: Dict[int, 'GSTLALocation'] = {
#                 x.rando_flag: world.get_location(loc_names_by_id[x.ap_id])
#                 for x in all_locations if x.loc_type != LocationType.Event and x.loc_type != LocationType.Djinn
#             }
#         self.test_state = world.multiworld.state.copy()
#         self.event_items: Dict[str, ItemData] = {}
#         for event in events:
#             self.event_items[event.name] = event
#         for _ in range(72):
#             self.test_state.collect(world.create_item(ItemName.Fizz), True)
#         for _ in range(7):
#             self.test_state.collect(world.create_item(ItemName.Isaac), True)
#
#     def test_treasure_logic(self):
#         # TODO:
#         # YampiBackside, GondowanAccess need special handling
#         dir_name = os.path.join(SCRIPT_DIR, '..', 'data', 'location_logic')
#         for file_name in os.listdir(dir_name):
#             if not file_name.endswith(".json"):
#                 continue
#             if file_name != "Kibombo.json":
#                 # Kibombo is a hot mess right now due to new character shuffle
#                 continue
#             if file_name == "Contigo.json" or file_name == "Idejima.json":
#                 # Character shuffle is making these files difficult
#                 continue
#             # if not file_name == "MarsLighthouse.json":
#             #     continue
#             with open(os.path.join(dir_name, file_name)) as logic_file:
#                 logic_data = LogicData(json.load(logic_file), file_name[:-5])
#             with self.subTest("Test Area", name=logic_data.name):
#                 self.run_region_logic_test(logic_data)
#         # with open(
#         #                        # 'AnkohlRuins.json')) as logic_file:
#         #                         'Daila.json')) as logic_file:
#         #     logic_data = LogicData(json.load(logic_file), logic_file.name)
#         # # access_requirements = transform_access_requirements(logic_data["Access"])
#         # with self.subTest("Test Area", name=logic_data.name):
#         #     self.run_region_logic_test(logic_data)
#
#     def cleanup_access_reqs(self, reqs_of_reqs: List[List[str]], name: typing.Optional[str] = '') -> List[List[str]]:
#         ret = []
#         for reqs in reqs_of_reqs:
#             funny_val = None
#             for req in reqs:
#                 if req in special_reqs:
#                     # assumes only one funny val in each list
#                     funny_val = req
#                     break
#
#             if funny_val is not None:
#                 reqs.remove(funny_val)
#                 result = set()
#                 if not reqs:
#                     for special in special_reqs[funny_val]:
#                         # result = []
#                         for item in special:
#                             result.add(requirement_map.get(item, item))
#                         # ret.append(result)
#                         # print(name)
#                         # print(ret)
#                 else:
#                     for special in special_reqs[funny_val]:
#                         # result = set()
#                         for item in special:
#                             result.add(requirement_map.get(item, item))
#                         # print(result)
#                         result |= set(reqs)
#                         # print(result)
#                         # ret.append(result)
#                         # print(name)
#                         # print(ret)
#                 extra = requirement_map.get(funny_val, None)
#                 if extra is not None:
#                     result.append(extra)
#                 ret.append(result)
#             else:
#                 ret.append(reqs)
#                 # print(name)
#                 # print(ret)
#         return ret
#
#     def run_region_logic_test(self, logic_data: LogicData):
#         access_requirements = logic_data.access_requirements if logic_data.access_requirements else [[]]
#         # world = self.get_world()
#         # access_requirements = self.cleanup_access_reqs(access_requirements, logic_data.name)
#         access_options_for_locations: defaultdict[int, List[Set[str]]] = defaultdict(lambda: [])
#         for access_index, access_reqs in enumerate(access_requirements):
#             loc_reqs = set(access_reqs)
#             for flag, treasure_requirements in logic_data.treasure_requirements.items():
#                 treasure_reqs = treasure_requirements if treasure_requirements else [[]]
#
#                 # treasure_reqs = self.cleanup_access_reqs(treasure_reqs)
#                 for treasure_index, reqs in enumerate(treasure_reqs):
#                     total_reqs = loc_reqs | set(reqs)
#                     # print(total_reqs)
#                     access_options_for_locations[flag].append(total_reqs)
#
#         for flag, access_options_for_location in access_options_for_locations.items():
#             remove_list = [False for _ in access_options_for_location]
#             for i, access_reqs in enumerate(access_options_for_location):
#                 for j, other_reqs in enumerate(access_options_for_location):
#                     if i == j:
#                         continue
#                     if access_reqs == other_reqs and i > j:
#                         continue
#                     # remove_list[i] = access_reqs.issubset(other_reqs)
#                     remove_list[i] |= access_reqs.issuperset(other_reqs)
#             final_list = [access_options_for_location[i] for i in range(len(access_options_for_location))
#                           if not remove_list[i]]
#             # print(flag)
#             # print(remove_list)
#             # print(final_list)
#             for final_reqs in final_list:
#                 self.run_sub_test(logic_data, flag, final_reqs)
#
#     def get_items_and_events(self, item_names: typing.Union[str, typing.Iterable[str]]) -> typing.List[Item]:
#         items = self.get_items_by_name(item_names)
#         for item_name in item_names:
#             if item_name in self.event_items:
#                 items.append(self.world.create_item(item_name))
#         return items
#
#     def verify_item_length(self, ap_items, rando_items) -> None:
#         if len(ap_items) == len(rando_items):
#             return
#
#         if len(ap_items) > len(rando_items):
#             raise AssertionError("Impossible code flow found")
#         count = 0
#         for item in rando_items:
#             if item in omitted_items:
#                 count += 1
#
#         if len(ap_items) + count != len(rando_items):
#             raise AssertionError(f"Item lengths do not match {ap_items} vs {rando_items}")
#
#     def run_sub_test(self, logic_data: LogicData, flag: int, reqs: Set[str]):
#         world = self.get_world()
#         location = self.locations_by_flag[flag]
#         for req in reqs:
#             if req in no_can_handle:
#                 return
#         if not reqs:
#             with self.subTest(f"Can Access {location.name} with flag {hex(flag)} with no items", reqs=reqs):
#                 # state = world.multiworld.state.copy()
#                 state = self.test_state.copy()
#                 self.assertTrue(location.can_reach(state))
#         else:
#             for req in reqs:
#                 if req in omitted_items:
#                     continue
#                 without_req = set(reqs)
#                 without_req.remove(req)
#
#                 with self.subTest(f"Cannot access {location.name} with missing Req", req=req, reqs=reqs):
#                     # state = world.multiworld.state.copy()
#                     state = self.test_state.copy()
#                     items = self.get_items_and_events(without_req)
#                     self.verify_item_length(items, without_req)
#                     for item in items:
#                         self.assertTrue(state.collect(item, True))
#                     self.assertFalse(location.can_reach(state),
#                                      f"Could reach {location.name} with flag {hex(flag)} without {req} but with {without_req} with state {state.prog_items}")
#
#             with self.subTest(f"Can access with all reqs", reqs=reqs):
#                 # state = world.multiworld.state.copy()
#                 state = self.test_state.copy()
#                 items = self.get_items_and_events(reqs)
#                 self.verify_item_length(items, reqs)
#                 for item in items:
#                     self.assertTrue(state.collect(item, True))
#                 self.assertTrue(location.can_reach(state), f"Location {location} with flag {hex(flag)} cannot be reached with items {items} state {state.prog_items}")
