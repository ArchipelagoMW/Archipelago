from collections import Counter

from BaseClasses import CollectionState
from Fill import distribute_items_restrictive
from Options import OptionError
from test.general import setup_multiworld

from .bases import CMTestBase
from .. import CMWorld
from ..geometry_progression import BoardStage
from ..locations import location_names_for_stage
from ..rules import has_board_stage


class TestDefaultBoardSeries(CMTestBase):
    options = {
        "min_board_size": "8x8",
        "max_board_size": "12x10",
        "difficulty": "grandmaster",
    }

    def test_regions_victory_and_fixed_unlocks_follow_selected_series(self):
        self.assertEqual(
            set(
                location_names_for_stage(
                    BoardStage.Board12x10,
                    "turns",
                    progression_start=BoardStage.Board8x8,
                )
            ),
            {
                location.name
                for location in self.multiworld.get_locations(self.player)
            },
        )
        self.assertEqual(
            {
                "Checkmate Minima": "Board Files",
                "Checkmate Maxima": "Board Ranks",
                "Checkmate 10x10": "Board Files",
                "Checkmate 12x10": "Victory",
            },
            {
                name: self.multiworld.get_location(name, self.player).item.name
                for name in (
                    "Checkmate Minima",
                    "Checkmate Maxima",
                    "Checkmate 10x10",
                    "Checkmate 12x10",
                )
            },
        )
        pool = Counter(item.name for item in self.multiworld.itempool)
        self.assertEqual(0, pool["Board Files"])
        self.assertEqual(0, pool["Board Ranks"])
        self.assertEqual([], self.multiworld.precollected_items[self.player])

    def test_rules_apply_relative_unlocks_to_the_starting_baseline(self):
        state = CollectionState(self.multiworld)
        self.assertTrue(
            has_board_stage(
                state,
                self.player,
                BoardStage.Board8x8,
                self.world.geometry_progression.precollected_unlocks,
            )
        )
        self.assertFalse(
            has_board_stage(
                state,
                self.player,
                BoardStage.Board10x8,
                self.world.geometry_progression.precollected_unlocks,
            )
        )
        self.world.collect(state, self.world.create_item("Board Files"))
        self.assertTrue(
            has_board_stage(
                state,
                self.player,
                BoardStage.Board10x8,
                self.world.geometry_progression.precollected_unlocks,
            )
        )

    def test_slot_data_publishes_normalized_v3_geometry(self):
        slot_data = self.world.fill_slot_data()
        self.assertEqual(0, slot_data["min_board_size"])
        self.assertEqual(3, slot_data["max_board_size"])
        self.assertEqual("8x8", slot_data["geometry_start"])
        self.assertEqual("12x10", slot_data["geometry_end"])
        self.assertEqual(
            {"files": 8, "ranks": 8},
            slot_data["geometry_baseline"],
        )
        self.assertEqual(
            {"board-file-unlock": 1, "board-rank-unlock": 0},
            slot_data["geometry_start_unlocks"],
        )
        self.assertEqual(
            {"board-file-unlock": 2, "board-rank-unlock": 1},
            slot_data["geometry_generated_unlocks"],
        )
        self.assertEqual(
            {"board-file-unlock": 3, "board-rank-unlock": 1},
            slot_data["geometry_end_unlocks"],
        )
        self.assertEqual(
            {"major": 3, "minor": 0},
            slot_data["apmw_contract_version"],
        )
        self.assertEqual(3, slot_data["apmw_contract"]["version"]["major"])

    def test_default_series_fills_and_is_reachable(self):
        distribute_items_restrictive(self.multiworld)
        self.assertTrue(all(self.multiworld.get_spheres()))


class TestSixByEightPrologue(CMTestBase):
    options = {
        "min_board_size": "6x8",
        "max_board_size": "10x8",
        "difficulty": "grandmaster",
    }

    def test_prologue_transitions_twice_by_fixed_file_events(self):
        self.assertEqual(
            "Board Files",
            self.multiworld.get_location("Checkmate 6x8", self.player).item.name,
        )
        self.assertEqual(
            "Board Files",
            self.multiworld.get_location(
                "Checkmate Minima", self.player
            ).item.name,
        )
        self.assertEqual(
            "Victory",
            self.multiworld.get_location(
                "Checkmate Maxima", self.player
            ).item.name,
        )
        self.assertNotIn(
            "Checkmate 10x10",
            {
                location.name
                for location in self.multiworld.get_locations(self.player)
            },
        )


class TestSixByEightOnly(CMTestBase):
    options = {
        "min_board_size": "6x8",
        "max_board_size": "6x8",
        "difficulty": "grandmaster",
        "early_material": "pawn",
    }

    def test_preserves_start_capacity_without_geometry_transition(self):
        self.assertEqual((), self.world.geometry_progression.transitions)
        self.assertEqual(
            "Victory",
            self.multiworld.get_location(
                "Checkmate 6x8", self.player
            ).item.name,
        )
        self.assertEqual(
            "Progressive Pawn",
            self.multiworld.get_location(
                "King to E2/E7 Early", self.player
            ).item.name,
        )
        pool = Counter(item.name for item in self.multiworld.itempool)
        self.assertEqual(1, pool["Play as White"])
        self.assertEqual(0, pool["Board Files"])
        self.assertEqual(0, pool["Board Ranks"])
        self.assertEqual(
            len(self.multiworld.get_locations(self.player)) - 2,
            len(self.multiworld.itempool),
        )

    def test_fills_and_is_reachable(self):
        distribute_items_restrictive(self.multiworld)
        self.assertTrue(all(self.multiworld.get_spheres()))


class TestSixByEightFundamental(CMTestBase):
    options = {
        "min_board_size": "6x8",
        "max_board_size": "6x8",
        "progression_itemization": "fundamental",
        "enable_tactics": "all",
        "difficulty": "grandmaster",
        "early_material": "any",
    }

    def test_compact_chessmen_thresholds_remain_reachable(self):
        distribute_items_restrictive(self.multiworld)
        spheres = list(self.multiworld.get_spheres())

        self.assertTrue(all(spheres))
        self.assertIn(
            "Current Objective: Survive 20 Turns",
            {
                location.name
                for sphere in spheres
                for location in sphere
            },
        )


class TestTenByEightStart(CMTestBase):
    options = {
        "min_board_size": "10x8",
        "max_board_size": "12x10",
        "difficulty": "grandmaster",
    }

    def test_uses_physical_baseline_and_only_relative_transition_events(self):
        locations = {
            location.name
            for location in self.multiworld.get_locations(self.player)
        }
        self.assertNotIn("Checkmate 6x8", locations)
        self.assertNotIn("Checkmate Minima", locations)
        self.assertEqual(
            "Board Ranks",
            self.multiworld.get_location(
                "Checkmate Maxima", self.player
            ).item.name,
        )
        self.assertEqual(
            "Board Files",
            self.multiworld.get_location(
                "Checkmate 10x10", self.player
            ).item.name,
        )
        self.assertEqual(
            "Victory",
            self.multiworld.get_location(
                "Checkmate 12x10", self.player
            ).item.name,
        )
        self.assertEqual([], self.multiworld.precollected_items[self.player])
        pool = Counter(item.name for item in self.multiworld.itempool)
        self.assertEqual(0, pool["Board Files"])
        self.assertEqual(0, pool["Board Ranks"])

        slot_data = self.world.fill_slot_data()
        self.assertEqual({"files": 10, "ranks": 8}, slot_data["geometry_baseline"])
        self.assertEqual(
            {"board-file-unlock": 2, "board-rank-unlock": 0},
            slot_data["geometry_start_unlocks"],
        )
        self.assertEqual(
            {"board-file-unlock": 1, "board-rank-unlock": 1},
            slot_data["geometry_generated_unlocks"],
        )
        self.assertEqual(
            {"board-file-unlock": 3, "board-rank-unlock": 1},
            slot_data["geometry_end_unlocks"],
        )


class TestBoardSeriesValidation(CMTestBase):
    auto_construct = False

    @staticmethod
    def _legacy_slot_data(goal: int) -> dict:
        return {
            "goal": goal,
            "required_chess_client_version": "0.4.0",
            "apmw_contract": {
                "version": {"major": 2, "minor": 0},
                "minimum_client_version": "0.4.0",
            },
        }

    @staticmethod
    def _tracker_world(slot_data: dict):
        multiworld = setup_multiworld(CMWorld, steps=(), seed=0)
        multiworld.generation_is_fake = True
        multiworld.re_gen_passthrough = {
            "ChecksMate": CMWorld.interpret_slot_data(slot_data)
        }
        return multiworld, multiworld.worlds[1]

    def test_all_ordered_board_series_generate_with_expected_events(self):
        stages = {
            -1: BoardStage.Board6x8,
            0: BoardStage.Board8x8,
            1: BoardStage.Board10x8,
            2: BoardStage.Board10x10,
            3: BoardStage.Board12x10,
        }
        victory_locations = {
            -1: "Checkmate 6x8",
            0: "Checkmate Minima",
            1: "Checkmate Maxima",
            2: "Checkmate 10x10",
            3: "Checkmate 12x10",
        }
        transition_items = {
            -1: "Board Files",
            0: "Board Files",
            1: "Board Ranks",
            2: "Board Files",
        }
        unlocks = {
            -1: (0, 0),
            0: (1, 0),
            1: (2, 0),
            2: (2, 1),
            3: (3, 1),
        }

        for start in (-1, 0, 1):
            for end in range(start, 4):
                with self.subTest(start=start, end=end):
                    multiworld = setup_multiworld(
                        CMWorld,
                        steps=(
                            "generate_early",
                            "create_regions",
                            "create_items",
                            "set_rules",
                        ),
                        seed=0,
                        options={
                            "min_board_size": start,
                            "max_board_size": end,
                            "difficulty": "grandmaster",
                            "enable_tactics": "all",
                        },
                    )
                    world = multiworld.worlds[1]
                    self.assertEqual(
                        set(
                            location_names_for_stage(
                                stages[end],
                                progression_start=stages[start],
                            )
                        ),
                        {
                            location.name
                            for location in multiworld.get_locations(1)
                        },
                    )
                    self.assertEqual(
                        "Victory",
                        multiworld.get_location(
                            victory_locations[end],
                            1,
                        ).item.name,
                    )
                    self.assertEqual(
                        end - start,
                        len(world.geometry_progression.transitions),
                    )
                    for transition_stage in range(start, end):
                        self.assertEqual(
                            transition_items[transition_stage],
                            multiworld.get_location(
                                victory_locations[transition_stage],
                                1,
                            ).item.name,
                        )

                    pool = Counter(item.name for item in multiworld.itempool)
                    self.assertEqual(0, pool["Board Files"])
                    self.assertEqual(0, pool["Board Ranks"])
                    if start == end:
                        self.assertEqual(
                            ["Victory"],
                            [
                                location.item.name
                                for location in multiworld.get_locations(1)
                                if location.locked
                            ],
                        )

                    slot_data = world.fill_slot_data()
                    self.assertEqual(start, slot_data["min_board_size"])
                    self.assertEqual(end, slot_data["max_board_size"])
                    self.assertEqual(
                        world.geometry_progression.stages[0].stage_id,
                        slot_data["geometry_start"],
                    )
                    self.assertEqual(
                        world.geometry_progression.endpoint.stage_id,
                        slot_data["geometry_end"],
                    )
                    self.assertEqual(
                        {
                            "files": world.geometry_progression.stages[0].files,
                            "ranks": world.geometry_progression.stages[0].ranks,
                        },
                        slot_data["geometry_baseline"],
                    )
                    start_files, start_ranks = unlocks[start]
                    end_files, end_ranks = unlocks[end]
                    self.assertEqual(
                        {
                            "board-file-unlock": start_files,
                            "board-rank-unlock": start_ranks,
                        },
                        slot_data["geometry_start_unlocks"],
                    )
                    self.assertEqual(
                        {
                            "board-file-unlock": end_files - start_files,
                            "board-rank-unlock": end_ranks - start_ranks,
                        },
                        slot_data["geometry_generated_unlocks"],
                    )
                    self.assertEqual(
                        {
                            "board-file-unlock": end_files,
                            "board-rank-unlock": end_ranks,
                        },
                        slot_data["geometry_end_unlocks"],
                    )

    def test_transition_events_stay_local_in_multiworld_generation(self):
        multiworld = setup_multiworld(
            [CMWorld, CMWorld],
            steps=(
                "generate_early",
                "create_regions",
                "create_items",
                "set_rules",
            ),
            seed=0,
            options=[
                {
                    "min_board_size": "6x8",
                    "max_board_size": "12x10",
                },
                {
                    "min_board_size": "10x8",
                    "max_board_size": "12x10",
                },
            ],
        )
        expected = {
            1: {
                "Checkmate 6x8": "Board Files",
                "Checkmate Minima": "Board Files",
                "Checkmate Maxima": "Board Ranks",
                "Checkmate 10x10": "Board Files",
            },
            2: {
                "Checkmate Maxima": "Board Ranks",
                "Checkmate 10x10": "Board Files",
            },
        }

        for player, transitions in expected.items():
            for location_name, item_name in transitions.items():
                with self.subTest(player=player, location=location_name):
                    location = multiworld.get_location(location_name, player)
                    self.assertTrue(location.locked)
                    self.assertEqual(item_name, location.item.name)
                    self.assertEqual(player, location.item.player)

        self.assertFalse(
            any(
                item.name in {"Board Files", "Board Ranks"}
                for item in multiworld.itempool
            )
        )

    def test_reversed_board_series_raise_option_error(self):
        for start, end in ((0, -1), (1, -1), (1, 0)):
            with self.subTest(start=start, end=end):
                with self.assertRaisesRegex(
                    OptionError,
                    "board series is invalid.*must not follow",
                ):
                    setup_multiworld(
                        CMWorld,
                        steps=("generate_early",),
                        options={
                            "min_board_size": start,
                            "max_board_size": end,
                        },
                    )

    def test_new_world_generation_rejects_legacy_only_twelve_by_twelve(self):
        multiworld = setup_multiworld(CMWorld, steps=(), seed=0)
        world = multiworld.worlds[1]
        world.options.max_board_size.value = BoardStage.Board12x12.value

        with self.assertRaisesRegex(
            OptionError,
            "legacy-only.*not selectable",
        ):
            world.generate_early()

    def test_legacy_single_goal_normalizes_without_losing_v2_metadata(self):
        original = self._legacy_slot_data(0)
        interpreted = CMWorld.interpret_slot_data(original)

        self.assertEqual(0, interpreted["goal"])
        self.assertEqual("0.4.0", interpreted["required_chess_client_version"])
        self.assertEqual(original["apmw_contract"], interpreted["apmw_contract"])
        self.assertEqual((0, 0), (
            interpreted["min_board_size"],
            interpreted["max_board_size"],
        ))
        self.assertEqual("8x8", interpreted["geometry_start"])
        self.assertEqual("8x8", interpreted["geometry_end"])
        self.assertEqual("fixed", interpreted["geometry_unlock_distribution"])

        multiworld, world = self._tracker_world(original)
        world.generate_early()
        world.create_regions()
        world.create_items()
        world.set_rules()
        self.assertEqual(
            "Victory",
            multiworld.get_location("Checkmate Minima", 1).item.name,
        )
        self.assertNotIn(
            "Checkmate 12x12",
            {location.name for location in multiworld.get_locations(1)},
        )

    def test_legacy_ordered_goal_reconstructs_fixed_twelve_by_twelve_series(self):
        interpreted = CMWorld.interpret_slot_data(self._legacy_slot_data(1))
        self.assertEqual((0, 4), (
            interpreted["min_board_size"],
            interpreted["max_board_size"],
        ))
        self.assertEqual("fixed", interpreted["geometry_unlock_distribution"])
        self.assertEqual("12x12", interpreted["geometry_end"])

        multiworld, world = self._tracker_world(self._legacy_slot_data(1))
        world.generate_early()
        world.create_regions()
        world.create_items()
        world.set_rules()
        self.assertEqual(
            BoardStage.Board12x12,
            world.geometry_progression.endpoint.stage,
        )
        self.assertEqual(
            {
                "Checkmate Minima": "Board Files",
                "Checkmate Maxima": "Board Ranks",
                "Checkmate 10x10": "Board Files",
                "Checkmate 12x10": "Board Ranks",
                "Checkmate 12x12": "Victory",
            },
            {
                name: multiworld.get_location(name, 1).item.name
                for name in (
                    "Checkmate Minima",
                    "Checkmate Maxima",
                    "Checkmate 10x10",
                    "Checkmate 12x10",
                    "Checkmate 12x12",
                )
            },
        )

    def test_legacy_distributed_goals_are_preserved_then_rejected_explicitly(self):
        expected_bounds = {
            2: (0, 4),
            3: (1, 4),
        }
        for goal, bounds in expected_bounds.items():
            with self.subTest(goal=goal):
                original = self._legacy_slot_data(goal)
                interpreted = CMWorld.interpret_slot_data(original)
                self.assertEqual(goal, interpreted["goal"])
                self.assertEqual(bounds, (
                    interpreted["min_board_size"],
                    interpreted["max_board_size"],
                ))
                self.assertEqual(
                    "distributed",
                    interpreted["geometry_unlock_distribution"],
                )
                self.assertEqual(
                    original["apmw_contract"],
                    interpreted["apmw_contract"],
                )

                _, world = self._tracker_world(original)
                with self.assertRaisesRegex(
                    OptionError,
                    "legacy Goal.*distributed.*cannot be faithfully reconstructed",
                ):
                    world.generate_early()

    def test_invalid_legacy_goal_is_rejected_instead_of_using_new_defaults(self):
        for goal in (-1, 4, True):
            with self.subTest(goal=goal):
                with self.assertRaisesRegex(
                    OptionError,
                    "legacy goal must be an integer from 0 through 3",
                ):
                    CMWorld.interpret_slot_data({"goal": goal})

    def test_tracker_geometry_mismatch_is_an_option_error(self):
        multiworld = setup_multiworld(CMWorld, steps=(), seed=0)
        multiworld.re_gen_passthrough = {
            "ChecksMate": {
                "min_board_size": 0,
                "max_board_size": 3,
                "geometry_start": "6x8",
            }
        }
        with self.assertRaisesRegex(
            OptionError,
            "geometry_start.*does not match",
        ):
            multiworld.worlds[1].generate_early()

    def test_geometry_items_cannot_be_requested_from_the_pool(self):
        with self.assertRaisesRegex(
            OptionError,
            "Board Files.*fixed board-series event",
        ):
            setup_multiworld(
                CMWorld,
                steps=("generate_early",),
                options={"locked_items": {"Board Files": 1}},
            )

    def test_legacy_geometry_marker_cannot_override_new_start_state(self):
        with self.assertRaisesRegex(
            OptionError,
            "Super-Size Me.*cannot be precollected",
        ):
            setup_multiworld(
                CMWorld,
                steps=("generate_early",),
                options={"start_inventory": {"Super-Size Me": 1}},
            )
