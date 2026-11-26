import unittest

from BaseClasses import CollectionState, MultiWorld
from test.general import setup_solo_multiworld

from .. import HKWorld


class TestBase(unittest.TestCase):
    game_name = "Hollow Knight"
    world_type = HKWorld
    multiworld: MultiWorld
    world: HKWorld

    def setUp(self):
        self.multiworld = setup_solo_multiworld(self.world_type)
        self.world = self.multiworld.worlds[1]

    def test_collect(self):
        empty_state = CollectionState(self.multiworld)
        state_under_test = CollectionState(self.multiworld)

        for item_name in self.world_type.item_name_to_id:
            with self.subTest("Create Item", item_name=item_name):
                item = self.world.create_item(item_name)

            with self.subTest("Item Name", item_name=item_name):
                self.assertEqual(item.name, item_name)

            if item.advancement:
                with self.subTest("Item State Collect", item_name=item_name):
                    state_under_test.collect(item, True)

                with self.subTest("Item State Remove", item_name=item_name):
                    state_under_test.remove(item)

                    self.assertEqual(state_under_test.prog_items, empty_state.prog_items,
                                     "Item Collect -> Remove should restore empty state.")
            else:
                with self.subTest("Item State Collect No Change", item_name=item_name):
                    # Non-Advancement should not modify state.
                    base_state = state_under_test.prog_items.copy()
                    state_under_test.collect(item)
                    self.assertEqual(base_state, state_under_test.prog_items)

            state_under_test.prog_items = empty_state.prog_items

    # def test_collect_split_cloak(self):
    #     game_name, world_type = "Hollow Knight", HKWorld
    #     multiworld = setup_solo_multiworld(world_type)
    #     proxy_world = multiworld.worlds[1]
    #     empty_state = multiworld.state.copy()

    #     l_cloaks = ["Left_Mothwing_Cloak", "Right_Mothwing_Cloak", "Left_Mothwing_Cloak"]
    #     r_cloaks = ["Left_Mothwing_Cloak", "Right_Mothwing_Cloak", "Right_Mothwing_Cloak"]
    #     for cloaks in [l_cloaks, r_cloaks]:
    #         items = []
    #         for item_name in cloaks:
    #             with self.subTest("Create Item", item_name=item_name):
    #                 item = proxy_world.create_item(item_name)
    #                 items.append(item)

    #             with self.subTest("Item Name", item_name=item_name):
    #                 self.assertEqual(item.name, item_name)

    #             if item.advancement:
    #                 with self.subTest("Item State Collect", item_name=item_name):
    #                     multiworld.state.collect(item, True)
    #         proxy_world.random.shuffle(items)
    #         for item in items:
    #             with self.subTest("Item State Remove", item_name=item_name):
    #                 multiworld.state.remove(item)

    #         self.assertEqual(
    #             multiworld.state.prog_items, empty_state.prog_items,
    #             "Item Collect -> Remove should restore empty state.\n"
    #             f"{multiworld.state.prog_items}\n\n{empty_state.prog_items}"
    #         )

    #         multiworld.state.prog_items = empty_state.prog_items

    def cloak_test(self, collect_cloaks, remove_cloaks, final_state):
        empty_state = CollectionState(self.multiworld)
        state_under_test = CollectionState(self.multiworld)

        items = []
        for item_name in collect_cloaks:
            with self.subTest("Create Item", item_name=item_name):
                item = self.world.create_item(item_name)
                items.append(item)

            with self.subTest("Item State Collect", item_name=item_name):
                state_under_test.collect(item, True)

        for item_name in remove_cloaks:
            index, item = next((index, item) for index, item in enumerate(items) if item.name == item_name)
            items.pop(index)
            with self.subTest("Item State Remove", item_name=item_name):
                state_under_test.remove(item)

        for item_name in ("Left_Mothwing_Cloak", "Right_Mothwing_Cloak",):
            if item_name in final_state:
                self.assertEqual(
                    state_under_test._hk_processed_item_cache[1][item_name], final_state[item_name],
                    f"expected {final_state[item_name]} {item_name}, "
                    f"found {state_under_test._hk_processed_item_cache[1][item_name]}"
                    f"\nTest collected\n{collect_cloaks}\nand removed\n{remove_cloaks}\n"
                    )
            else:
                self.assertEqual(
                    state_under_test._hk_processed_item_cache[1][item_name], 0,
                    f"expected 0 {item_name}, found {state_under_test._hk_processed_item_cache[1][item_name]}"
                    f"\nTest collected\n{collect_cloaks}\nand removed\n{remove_cloaks}\n"
                    )

        for item_name in ("LEFTDASH", "RIGHTDASH",):
            if item_name in final_state:
                self.assertEqual(
                    state_under_test.prog_items[1][item_name], final_state[item_name],
                    f"expected {final_state[item_name]} {item_name}, found {state_under_test.prog_items[1][item_name]}"
                    f"\nTest collected\n{collect_cloaks}\nand removed\n{remove_cloaks}\n"
                    )
            else:
                self.assertEqual(
                    state_under_test.prog_items[1][item_name], 0,
                    f"expected 0 {item_name}, found {state_under_test.prog_items[1][item_name]}"
                    f"\nTest collected\n{collect_cloaks}\nand removed\n{remove_cloaks}\n"
                    )

        state_under_test.prog_items = empty_state.prog_items

    def test_collect_cloak_iterations(self):


        # LLR
        with self.subTest("LLR"):
            self.cloak_test(
                ["Left_Mothwing_Cloak", "Left_Mothwing_Cloak", "Right_Mothwing_Cloak"],
                [],
                {"Left_Mothwing_Cloak": 2, "LEFTDASH": 2, "Right_Mothwing_Cloak": 1, "RIGHTDASH": 2},
            )
        with self.subTest("L - L"):
            self.cloak_test(
                ["Left_Mothwing_Cloak"],
                ["Left_Mothwing_Cloak"],
                {},
            )
        with self.subTest("LL - L"):
            self.cloak_test(
                ["Left_Mothwing_Cloak", "Left_Mothwing_Cloak"],
                ["Left_Mothwing_Cloak"],
                {"Left_Mothwing_Cloak": 1, "LEFTDASH": 1},
            )
        with self.subTest("LLR - L"):
            self.cloak_test(
                ["Left_Mothwing_Cloak", "Left_Mothwing_Cloak", "Right_Mothwing_Cloak"],
                ["Left_Mothwing_Cloak"],
                {"Left_Mothwing_Cloak": 1, "LEFTDASH": 1, "Right_Mothwing_Cloak": 1, "RIGHTDASH": 1},
            )
        # with self.subTest("L - R"):
        #     self.cloak_test(
        #         ["Left_Mothwing_Cloak"],
        #         ["Right_Mothwing_Cloak"],
        #         {},
        #     )
        # with self.subTest("LL - R"):
        #     self.cloak_test(
        #         ["Left_Mothwing_Cloak", "Left_Mothwing_Cloak"],
        #         ["Right_Mothwing_Cloak"],
        #         {},
        #     )
        with self.subTest("LLR - R"):
            self.cloak_test(
                ["Left_Mothwing_Cloak", "Left_Mothwing_Cloak", "Right_Mothwing_Cloak"],
                ["Right_Mothwing_Cloak"],
                {"Left_Mothwing_Cloak": 2, "LEFTDASH": 2},
            )

        # LRL
        with self.subTest("LRL"):
            self.cloak_test(
                ["Left_Mothwing_Cloak", "Right_Mothwing_Cloak", "Left_Mothwing_Cloak"],
                [],
                {"Left_Mothwing_Cloak": 2, "LEFTDASH": 2, "Right_Mothwing_Cloak": 1, "RIGHTDASH": 2},
            )
        with self.subTest("L - L"):
            self.cloak_test(
                ["Left_Mothwing_Cloak"],
                ["Left_Mothwing_Cloak"],
                {},
            )
        with self.subTest("LR - L"):
            self.cloak_test(
                ["Left_Mothwing_Cloak", "Right_Mothwing_Cloak"],
                ["Left_Mothwing_Cloak"],
                {"Right_Mothwing_Cloak": 1, "RIGHTDASH": 1},
            )
        with self.subTest("LRL - L"):
            self.cloak_test(
                ["Left_Mothwing_Cloak", "Right_Mothwing_Cloak", "Left_Mothwing_Cloak"],
                ["Left_Mothwing_Cloak"],
                {"Left_Mothwing_Cloak": 1, "LEFTDASH": 1, "Right_Mothwing_Cloak": 1, "RIGHTDASH": 1},
            )
        # with self.subTest("L - R"):
        #     self.cloak_test(
        #         ["Left_Mothwing_Cloak"],
        #         ["Right_Mothwing_Cloak"],
        #         {},
        #     )
        with self.subTest("LR - R"):
            self.cloak_test(
                ["Left_Mothwing_Cloak", "Right_Mothwing_Cloak"],
                ["Right_Mothwing_Cloak"],
                {"Left_Mothwing_Cloak": 1, "LEFTDASH": 1},
            )
        with self.subTest("LRL - R"):
            self.cloak_test(
                ["Left_Mothwing_Cloak", "Right_Mothwing_Cloak", "Left_Mothwing_Cloak"],
                ["Right_Mothwing_Cloak"],
                {"Left_Mothwing_Cloak": 2, "LEFTDASH": 2},
            )

        # RLL
        with self.subTest("RLL"):
            self.cloak_test(
                ["Right_Mothwing_Cloak", "Left_Mothwing_Cloak", "Left_Mothwing_Cloak"],
                [],
                {"Left_Mothwing_Cloak": 2, "LEFTDASH": 2, "Right_Mothwing_Cloak": 1, "RIGHTDASH": 2},
            )
        # with self.subTest("R - L"):
        #     self.cloak_test(
        #         ["Right_Mothwing_Cloak"],
        #         ["Left_Mothwing_Cloak"],
        #         {},
        #     )
        with self.subTest("RL - L"):
            self.cloak_test(
                ["Right_Mothwing_Cloak", "Left_Mothwing_Cloak"],
                ["Left_Mothwing_Cloak"],
                {"Right_Mothwing_Cloak": 1, "RIGHTDASH": 1},
            )
        with self.subTest("RLL - L"):
            self.cloak_test(
                ["Right_Mothwing_Cloak", "Left_Mothwing_Cloak", "Left_Mothwing_Cloak"],
                ["Left_Mothwing_Cloak"],
                {"Left_Mothwing_Cloak": 1, "LEFTDASH": 1, "Right_Mothwing_Cloak": 1, "RIGHTDASH": 1},
            )
        with self.subTest("R - R"):
            self.cloak_test(
                ["Right_Mothwing_Cloak"],
                ["Right_Mothwing_Cloak"],
                {},
            )
        with self.subTest("RL - R"):
            self.cloak_test(
                ["Right_Mothwing_Cloak", "Left_Mothwing_Cloak"],
                ["Right_Mothwing_Cloak"],
                {"Left_Mothwing_Cloak": 1, "LEFTDASH": 1},
            )
        with self.subTest("RLL - R"):
            self.cloak_test(
                ["Right_Mothwing_Cloak", "Left_Mothwing_Cloak", "Left_Mothwing_Cloak"],
                ["Right_Mothwing_Cloak"],
                {"Left_Mothwing_Cloak": 2, "LEFTDASH": 2},
            )

        # RRL
        with self.subTest("RRL"):
            self.cloak_test(
                ["Right_Mothwing_Cloak", "Right_Mothwing_Cloak", "Left_Mothwing_Cloak"],
                [],
                {"Left_Mothwing_Cloak": 1, "LEFTDASH": 2, "Right_Mothwing_Cloak": 2, "RIGHTDASH": 2},
            )
        # with self.subTest("R - L"):
        #     self.cloak_test(
        #         ["Right_Mothwing_Cloak"],
        #         ["Left_Mothwing_Cloak"],
        #         {},
        #     )
        # with self.subTest("RR - L"):
        #     self.cloak_test(
        #         ["Right_Mothwing_Cloak", "Right_Mothwing_Cloak"],
        #         ["Left_Mothwing_Cloak"],
        #         {"Right_Mothwing_Cloak": 1, "RIGHTDASH": 1},
        #     )
        with self.subTest("RRL - L"):
            self.cloak_test(
                ["Right_Mothwing_Cloak", "Right_Mothwing_Cloak", "Left_Mothwing_Cloak"],
                ["Left_Mothwing_Cloak"],
                {"Right_Mothwing_Cloak": 2, "RIGHTDASH": 2},
            )
        with self.subTest("R - R"):
            self.cloak_test(
                ["Right_Mothwing_Cloak"],
                ["Right_Mothwing_Cloak"],
                {},
            )
        with self.subTest("RR - R"):
            self.cloak_test(
                ["Right_Mothwing_Cloak", "Right_Mothwing_Cloak"],
                ["Right_Mothwing_Cloak"],
                {"Right_Mothwing_Cloak": 1, "RIGHTDASH": 1},
            )
        with self.subTest("RRL - R"):
            self.cloak_test(
                ["Right_Mothwing_Cloak", "Right_Mothwing_Cloak", "Left_Mothwing_Cloak"],
                ["Right_Mothwing_Cloak"],
                {"Left_Mothwing_Cloak": 1, "LEFTDASH": 1, "Right_Mothwing_Cloak": 1, "RIGHTDASH": 1},
            )

        # RLR
        with self.subTest("RLR"):
            self.cloak_test(
                ["Right_Mothwing_Cloak", "Left_Mothwing_Cloak", "Right_Mothwing_Cloak"],
                [],
                {"Left_Mothwing_Cloak": 1, "LEFTDASH": 2, "Right_Mothwing_Cloak": 2, "RIGHTDASH": 2},
            )
        # with self.subTest("R - L"):
        #     self.cloak_test(
        #         ["Right_Mothwing_Cloak"],
        #         ["Left_Mothwing_Cloak"],
        #         {},
        #     )
        with self.subTest("RL - L"):
            self.cloak_test(
                ["Right_Mothwing_Cloak", "Left_Mothwing_Cloak"],
                ["Left_Mothwing_Cloak"],
                {"Right_Mothwing_Cloak": 1, "RIGHTDASH": 1},
            )
        with self.subTest("RLR - L"):
            self.cloak_test(
                ["Right_Mothwing_Cloak", "Left_Mothwing_Cloak", "Right_Mothwing_Cloak"],
                ["Left_Mothwing_Cloak"],
                {"Right_Mothwing_Cloak": 2, "RIGHTDASH": 2},
            )
        with self.subTest("R - R"):
            self.cloak_test(
                ["Right_Mothwing_Cloak"],
                ["Right_Mothwing_Cloak"],
                {},
            )
        with self.subTest("RL - R"):
            self.cloak_test(
                ["Right_Mothwing_Cloak", "Left_Mothwing_Cloak"],
                ["Right_Mothwing_Cloak"],
                {"Left_Mothwing_Cloak": 1, "LEFTDASH": 1},
            )
        with self.subTest("RLR - R"):
            self.cloak_test(
                ["Right_Mothwing_Cloak", "Left_Mothwing_Cloak", "Right_Mothwing_Cloak"],
                ["Right_Mothwing_Cloak"],
                {"Left_Mothwing_Cloak": 1, "LEFTDASH": 1, "Right_Mothwing_Cloak": 1, "RIGHTDASH": 1},
            )

        # LRR
        with self.subTest("LRR"):
            self.cloak_test(
                ["Left_Mothwing_Cloak", "Right_Mothwing_Cloak", "Right_Mothwing_Cloak"],
                [],
                {"Left_Mothwing_Cloak": 1, "LEFTDASH": 2, "Right_Mothwing_Cloak": 2, "RIGHTDASH": 2},
            )
        with self.subTest("L - L"):
            self.cloak_test(
                ["Left_Mothwing_Cloak"],
                ["Left_Mothwing_Cloak"],
                {},
            )
        with self.subTest("LR - L"):
            self.cloak_test(
                ["Left_Mothwing_Cloak", "Right_Mothwing_Cloak"],
                ["Left_Mothwing_Cloak"],
                {"Right_Mothwing_Cloak": 1, "RIGHTDASH": 1},
            )
        with self.subTest("LRR - L"):
            self.cloak_test(
                ["Left_Mothwing_Cloak", "Right_Mothwing_Cloak", "Right_Mothwing_Cloak"],
                ["Left_Mothwing_Cloak"],
                {"Right_Mothwing_Cloak": 2, "RIGHTDASH": 2},
            )
        # with self.subTest("L - R"):
        #     self.cloak_test(
        #         ["Left_Mothwing_Cloak"],
        #         ["Right_Mothwing_Cloak"],
        #         {},
        #     )
        with self.subTest("LR - R"):
            self.cloak_test(
                ["Left_Mothwing_Cloak", "Right_Mothwing_Cloak"],
                ["Right_Mothwing_Cloak"],
                {"Left_Mothwing_Cloak": 1, "LEFTDASH": 1},
            )
        with self.subTest("LRR - R"):
            self.cloak_test(
                ["Left_Mothwing_Cloak", "Right_Mothwing_Cloak", "Right_Mothwing_Cloak"],
                ["Right_Mothwing_Cloak"],
                {"Left_Mothwing_Cloak": 1, "LEFTDASH": 1, "Right_Mothwing_Cloak": 1, "RIGHTDASH": 1},
            )

        # extra in pool
        with self.subTest("Bonus: LLRL - L"):
            self.cloak_test(
                ["Left_Mothwing_Cloak", "Left_Mothwing_Cloak", "Right_Mothwing_Cloak", "Left_Mothwing_Cloak"],
                ["Left_Mothwing_Cloak"],
                {"Left_Mothwing_Cloak": 2, "LEFTDASH": 2, "Right_Mothwing_Cloak": 1, "RIGHTDASH": 2},
            )
        with self.subTest("Bonus: LLRL - R"):
            self.cloak_test(
                ["Left_Mothwing_Cloak", "Left_Mothwing_Cloak", "Right_Mothwing_Cloak", "Left_Mothwing_Cloak"],
                ["Right_Mothwing_Cloak"],
                {"Left_Mothwing_Cloak": 3, "LEFTDASH": 3},
            )

        # non-split
        with self.subTest("Bonus: non-split"):
            self.cloak_test(
                ["Mothwing_Cloak", "Shade_Cloak"],
                [],
                {"Mothwing_Cloak": 1, "Shade_Cloak": 1, "LEFTDASH": 2, "RIGHTDASH": 2},
            )
            self.cloak_test(
                ["Mothwing_Cloak", "Shade_Cloak"],
                ["Mothwing_Cloak"],
                {"Shade_Cloak": 1, "LEFTDASH": 1, "RIGHTDASH": 1},
            )
            self.cloak_test(
                ["Mothwing_Cloak", "Shade_Cloak"],
                ["Shade_Cloak"],
                {"Mothwing_Cloak": 1, "LEFTDASH": 1, "RIGHTDASH": 1},
            )

    def test_collect_charm(self):
        empty_state = CollectionState(self.multiworld)

        king_fragment = next(item for item in self.multiworld.itempool if item.name == "King_Fragment")
        queen_fragment = next(item for item in self.multiworld.itempool if item.name == "Queen_Fragment")
        deep_focus = next(item for item in self.multiworld.itempool if item.name == "Deep_Focus")
        fragile_strength = next(item for item in self.multiworld.itempool if item.name == "Fragile_Strength")
        unbreakable_strength = next(item for item in self.multiworld.itempool if item.name == "Unbreakable_Strength")

        assert empty_state.prog_items[1]["CHARMS"] == 0
        empty_state.collect(king_fragment)
        assert empty_state.prog_items[1]["CHARMS"] == 0
        empty_state.collect(queen_fragment)
        assert empty_state.prog_items[1]["CHARMS"] == 1

        empty_state.collect(deep_focus)
        assert empty_state.prog_items[1]["CHARMS"] == 2

        empty_state.collect(fragile_strength)
        assert empty_state.prog_items[1]["CHARMS"] == 3
        empty_state.collect(unbreakable_strength)
        assert empty_state.prog_items[1]["CHARMS"] == 3

        all_state = self.multiworld.get_all_state()

        assert all_state.prog_items[1]["CHARMS"] == 40
        all_state.remove(king_fragment)
        assert all_state.prog_items[1]["CHARMS"] == 40
        all_state.remove(queen_fragment)
        assert all_state.prog_items[1]["CHARMS"] == 39

        all_state.remove(deep_focus)
        assert all_state.prog_items[1]["CHARMS"] == 38

        all_state.remove(fragile_strength)
        assert all_state.prog_items[1]["CHARMS"] == 38
        all_state.remove(unbreakable_strength)
        assert all_state.prog_items[1]["CHARMS"] == 37

    # def test_collect_charm_just_whitefragment(self):
    #     game_name, world_type = "Hollow Knight", HKWorld
    #     multiworld = setup_solo_multiworld(world_type)
    #     empty_state = multiworld.state

    #     king_fragment = next(item for item in multiworld.itempool if item.name == "King_Fragment")
    #     queen_fragment = next(item for item in multiworld.itempool if item.name == "Queen_Fragment")

    #     assert empty_state.prog_items[1]["CHARMS"] == 0
    #     empty_state.collect(king_fragment)
    #     assert empty_state.prog_items[1]["CHARMS"] == 0
    #     empty_state.collect(queen_fragment)
    #     assert empty_state.prog_items[1]["CHARMS"] == 1
