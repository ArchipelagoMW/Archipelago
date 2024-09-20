import unittest
from worlds.AutoWorld import AutoWorldRegister
from test.general import setup_solo_multiworld
from .. import HKWorld


class TestBase(unittest.TestCase):
    def testCollect(self):
        game_name, world_type = "Hollow Knight", HKWorld
        multiworld = setup_solo_multiworld(world_type)
        proxy_world = multiworld.worlds[1]
        empty_state = multiworld.state.copy()

        for item_name in world_type.item_name_to_id:
            with self.subTest("Create Item", item_name=item_name, game_name=game_name):
                item = proxy_world.create_item(item_name)

            with self.subTest("Item Name", item_name=item_name, game_name=game_name):
                self.assertEqual(item.name, item_name)

            if item.advancement:
                with self.subTest("Item State Collect", item_name=item_name, game_name=game_name):
                    multiworld.state.collect(item, True)

                with self.subTest("Item State Remove", item_name=item_name, game_name=game_name):
                    multiworld.state.remove(item)

                    self.assertEqual(multiworld.state.prog_items, empty_state.prog_items,
                                     "Item Collect -> Remove should restore empty state.")
            else:
                with self.subTest("Item State Collect No Change", item_name=item_name, game_name=game_name):
                    # Non-Advancement should not modify state.
                    base_state = multiworld.state.prog_items.copy()
                    multiworld.state.collect(item)
                    self.assertEqual(base_state, multiworld.state.prog_items)

            multiworld.state.prog_items = empty_state.prog_items

    # def testCollect_split_cloak(self):
    #     game_name, world_type = "Hollow Knight", HKWorld
    #     multiworld = setup_solo_multiworld(world_type)
    #     proxy_world = multiworld.worlds[1]
    #     empty_state = multiworld.state.copy()

    #     l_cloaks = ["Left_Mothwing_Cloak", "Right_Mothwing_Cloak", "Left_Mothwing_Cloak"]
    #     r_cloaks = ["Left_Mothwing_Cloak", "Right_Mothwing_Cloak", "Right_Mothwing_Cloak"]
    #     for cloaks in [l_cloaks, r_cloaks]:
    #         items = []
    #         for item_name in cloaks:
    #             with self.subTest("Create Item", item_name=item_name, game_name=game_name):
    #                 item = proxy_world.create_item(item_name)
    #                 items.append(item)

    #             with self.subTest("Item Name", item_name=item_name, game_name=game_name):
    #                 self.assertEqual(item.name, item_name)

    #             if item.advancement:
    #                 with self.subTest("Item State Collect", item_name=item_name, game_name=game_name):
    #                     multiworld.state.collect(item, True)
    #         proxy_world.random.shuffle(items)
    #         for item in items:
    #             with self.subTest("Item State Remove", item_name=item_name, game_name=game_name):
    #                 multiworld.state.remove(item)

    #         self.assertEqual(multiworld.state.prog_items, empty_state.prog_items,
    #                          f"Item Collect -> Remove should restore empty state.\n{multiworld.state.prog_items}\n\n{empty_state.prog_items}")

    #         multiworld.state.prog_items = empty_state.prog_items

    def cloak_test(self, collect_cloaks, remove_cloaks, final_state):
        game_name, world_type = "Hollow Knight", HKWorld
        multiworld = setup_solo_multiworld(world_type)
        proxy_world = multiworld.worlds[1]
        empty_state = multiworld.state.copy()

        items = []
        for item_name in collect_cloaks:
            with self.subTest("Create Item", item_name=item_name, game_name=game_name):
                item = proxy_world.create_item(item_name)
                items.append(item)

            with self.subTest("Item State Collect", item_name=item_name, game_name=game_name):
                multiworld.state.collect(item, True)

        for item_name in remove_cloaks:
            index, item = next((index, item) for index, item in enumerate(items) if item.name == item_name)
            items.pop(index)
            with self.subTest("Item State Remove", item_name=item_name, game_name=game_name):
                multiworld.state.remove(item)

        for item_name in ("Left_Mothwing_Cloak", "LEFTDASH", "Right_Mothwing_Cloak", "RIGHTDASH",):
            if item_name in final_state:
                self.assertEqual(
                    multiworld.state.prog_items[1][item_name], final_state[item_name],
                    f"expected {final_state[item_name]} {item_name}, found {multiworld.state.prog_items[1][item_name]}"
                    f"\nTest collected\n{collect_cloaks}\nand removed\n{remove_cloaks}\n"
                    )
            else:
                self.assertEqual(
                    multiworld.state.prog_items[1][item_name], 0,
                    f"expected 0 {item_name}, found {multiworld.state.prog_items[1][item_name]}"
                    f"\nTest collected\n{collect_cloaks}\nand removed\n{remove_cloaks}\n"
                    )

        multiworld.state.prog_items = empty_state.prog_items

    def testCollect_cloak_iterations(self):
        # with self.subTest("Split Left Only"):
        #     self.cloak_test(
        #         ["Left_Mothwing_Cloak"],
        #         ["Left_Mothwing_Cloak"],
        #         {},
        #     )

        # with self.subTest("LRR - L"):
        #     self.cloak_test(
        #         ["Left_Mothwing_Cloak", "Right_Mothwing_Cloak", "Right_Mothwing_Cloak"],
        #         ["Left_Mothwing_Cloak"],
        #         {"Right_Mothwing_Cloak": 2, "RIGHTDASH": 2},
        #     )

        # with self.subTest("RLL - R"):
        #     self.cloak_test(
        #         ["Right_Mothwing_Cloak", "Left_Mothwing_Cloak", "Left_Mothwing_Cloak"],
        #         ["Right_Mothwing_Cloak"],
        #         {"Left_Mothwing_Cloak": 2, "LEFTDASH": 2},
        #     )

        # LLR
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
                ["Mothwing_Cloak"],
                {"Shade_Cloak": 1, "LEFTDASH": 1, "RIGHTDASH": 1},
            )
            self.cloak_test(
                ["Mothwing_Cloak", "Shade_Cloak"],
                ["Shade_Cloak"],
                {"Mothwing_Cloak": 1, "LEFTDASH": 1, "RIGHTDASH": 1},
            )
