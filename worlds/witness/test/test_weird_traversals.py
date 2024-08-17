from ..test import WitnessTestBase


class TestWeirdTraversalRequirements(WitnessTestBase):
    options = {
        "shuffle_vault_boxes": True,
        "shuffle_symbols": False,
        "shuffle_EPs": "individual",
        "EP_difficulty": "tedious",
        "shuffle_doors": "doors",
        "door_groupings": "off",
        "puzzle_randomization": "sigma_expert",
    }

    def test_weird_traversal_requirements(self) -> None:
        """
        Test that Door Shuffle grants early access to Swamp Laser from the back shortcut.
        """

        with self.subTest("Tunnels Theater Flowers EP"):
            self.assertAccessDependency(
                ["Tunnels Theater Flowers EP"],
                [
                    ["Theater Exit Left (Door)", "Windmill Entry (Door)", "Tunnels Theater Shortcut (Door)"],
                    ["Theater Exit Right (Door)", "Windmill Entry (Door)", "Tunnels Theater Shortcut (Door)"],
                    ["Theater Exit Left (Door)", "Tunnels Town Shortcut (Door)"],
                    ["Theater Exit Right (Door)", "Tunnels Town Shortcut (Door)"],
                    ["Theater Entry (Door)", "Tunnels Theater Shortcut (Door)"],
                    ["Theater Entry (Door)", "Windmill Entry (Door)", "Tunnels Town Shortcut (Door)"],
                ],
                only_check_listed=True,
            )

        with self.subTest("Expert Keep Pressure Plates 2"):
            exit_paths = [
                ["Keep Shadows Shortcut (Door)"],
                ["Keep Pressure Plates 4 Exit (Door)", "Keep Tower Shortcut (Door)"],
                ["Keep Pressure Plates 4 Exit (Door)", "Keep Hedge Maze 4 Exit (Door)",
                 "Keep Hedge Maze 4 Shortcut (Door)"],
                ["Keep Pressure Plates 4 Exit (Door)", "Keep Hedge Maze 4 Exit (Door)",
                 "Keep Hedge Maze 3 Exit (Door)", "Keep Hedge Maze 3 Shortcut (Door)"],
                ["Keep Pressure Plates 4 Exit (Door)", "Keep Hedge Maze 4 Exit (Door)",
                 "Keep Hedge Maze 3 Exit (Door)", "Keep Hedge Maze 2 Exit (Door)", "Keep Hedge Maze 2 Shortcut (Door)"],
                ["Keep Pressure Plates 4 Exit (Door)", "Keep Hedge Maze 4 Exit (Door)",
                 "Keep Hedge Maze 3 Exit (Door)", "Keep Hedge Maze 2 Exit (Door)", "Keep Hedge Maze 1 Exit (Door)"],
            ]

            possible_items = [
                ["Keep Pressure Plates 1 Exit (Door)", "Keep Pressure Plates 3 Exit (Door)", *exit_path]
                for exit_path in exit_paths
            ]

            self.assertAccessDependency(["Keep Pressure Plates 2"], possible_items, only_check_listed=True)
