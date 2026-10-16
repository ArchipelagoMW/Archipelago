from collections import Counter
import json
from pathlib import Path

from BaseClasses import CollectionState
from Fill import distribute_items_restrictive
from Options import OptionError

from .cm_mock_test_case import CMMockTestCase
from .bases import CMTestBase
from ..apmw_contract import compute_manifest_sha256
from ..contract_resource import (
    UNLOCK_ITEM_ROLES,
    load_production_contract,
    production_contract_document,
    production_contract_text,
)
from ..item_pool import CMItemPool
from ..items import (
    FUNDAMENTAL_ITEMS,
    LEGACY_CHESSMEN_GROUP,
    LEGACY_MATERIAL_ITEMS,
    item_name_groups,
    item_table,
)
from ..options import MaxBoardSize, MinBoardSize, ProgressionItemization
from ..rules import effective_castlers
from ..locations import (
    BoardStage,
    chessmen_requirement_for_world,
    highest_chessmen_requirement_for_series,
    tactics_mode_for_options,
)


class TestV2ItemizationUnit(CMMockTestCase):
    def fundamental_world(self, start="8x8", end="12x10"):
        world = self.create_mock_world()
        world.options.progression_itemization = ProgressionItemization(
            ProgressionItemization.option_fundamental
        )
        world.options.min_board_size = MinBoardSize.from_any(start)
        world.options.max_board_size = MaxBoardSize.from_any(end)
        return world

    def test_new_item_contract(self):
        expected = {
            "Chessmen": (4_901_008, 107, 100),
            "Material": (4_901_011, 321, 400),
            "Castler": (4_901_012, 2, 0),
            "Board Files": (4_901_013, 3, 0),
            "Board Ranks": (4_901_014, 2, 0),
        }
        self.assertEqual(
            expected,
            {
                name: (
                    item_table[name].code,
                    item_table[name].quantity,
                    item_table[name].material,
                )
                for name in expected
            },
        )
        self.assertNotIn("Chessmen", item_name_groups)
        self.assertIn(LEGACY_CHESSMEN_GROUP, item_name_groups)

    def test_mode_specific_progression_pool_exclusivity(self):
        legacy = CMItemPool(self.create_mock_world())
        legacy.initialize_item_tracking()
        legacy_pool = set(legacy.prepare_progression_item_pool())
        self.assertTrue(LEGACY_MATERIAL_ITEMS & legacy_pool)
        self.assertFalse(FUNDAMENTAL_ITEMS & legacy_pool)

        fundamental = CMItemPool(self.fundamental_world())
        fundamental.initialize_item_tracking()
        fundamental_pool = set(fundamental.prepare_progression_item_pool())
        self.assertTrue(FUNDAMENTAL_ITEMS <= fundamental_pool)
        self.assertFalse(LEGACY_MATERIAL_ITEMS & fundamental_pool)
        self.assertIn("Progressive Pocket", fundamental_pool)

    def test_fundamental_generation_conserves_pool_and_castler_prerequisites(self):
        world = self.fundamental_world()
        pool = CMItemPool(world)
        items = pool.create_items()
        counts = Counter(item.name for item in items)
        self.assertEqual(
            pool.get_max_items() - 1 - len(world.geometry_progression.transitions),
            len(items),
        )
        self.assertFalse(LEGACY_MATERIAL_ITEMS & counts.keys())
        self.assertLessEqual(counts["Castler"], 2)
        self.assertGreaterEqual(counts["Chessmen"], counts["Castler"])
        self.assertGreaterEqual(counts["Material"] * 400, counts["Castler"] * 500)
        self.assertEqual(0, counts["Board Files"])
        self.assertEqual(0, counts["Board Ranks"])

    def test_board_series_first_unlock_behavior(self):
        expected = {
            ("8x8", "10x8"): ("Checkmate Minima",),
            ("8x8", "12x10"): (
                "Checkmate Minima",
                "Checkmate Maxima",
                "Checkmate 10x10",
            ),
            ("6x8", "12x10"): (
                "Checkmate 6x8",
                "Checkmate Minima",
                "Checkmate Maxima",
                "Checkmate 10x10",
            ),
        }
        for bounds, transition_locations in expected.items():
            with self.subTest(bounds=bounds):
                world = self.fundamental_world(*bounds)
                items = CMItemPool(world).create_items()
                self.assertEqual(
                    0,
                    sum(
                        item.name in {"Board Files", "Board Ranks"}
                        for item in items
                    ),
                )
                self.assertEqual(
                    len(transition_locations),
                    sum(
                        world.multiworld.get_location(
                            name, world.player
                        ).item is not None
                        for name in transition_locations
                    ),
                )
                self.assertEqual(
                    0,
                    len(world.multiworld.precollected_items[world.player]),
                )

        world = self.fundamental_world()
        world.options.locked_items.value = {"Board Files": 1}
        with self.assertRaisesRegex(
            OptionError,
            "Board Files.*fixed board-series event",
        ):
            CMItemPool(world).create_items()

    def test_valid_fundamental_locks_are_preserved_without_truncation(self):
        world = self.fundamental_world()
        world.options.locked_items.value = {
            "Chessmen": 20,
            "Material": 20,
            "Castler": 2,
        }
        pool = CMItemPool(world)
        items = pool.create_items()
        counts = Counter(item.name for item in items)
        self.assertLessEqual(
            len(items),
            pool.get_max_items()
            - 1
            - len(world.geometry_progression.transitions),
        )
        self.assertNotIn("Progressive Pawn", counts)
        self.assertGreaterEqual(counts["Chessmen"], 20)
        self.assertGreaterEqual(counts["Material"], 20)
        self.assertEqual(2, counts["Castler"])

    def test_incompatible_items_are_ignored_and_castler_prerequisites_are_finite(self):
        world = self.fundamental_world()
        pool = CMItemPool(world)
        pool.initialize_item_tracking()
        self.assertEqual(
            {},
            pool.normalize_counts({"Progressive Pawn": 20, "Chessmen": 0}),
        )
        self.assertFalse(pool.has_prereqs("Castler", {}))
        pool.items_used[world.player]["Chessmen"] = 1
        pool.items_used[world.player]["Material"] = 1
        self.assertFalse(pool.has_prereqs("Castler", {}))
        pool.items_used[world.player]["Material"] = 2
        self.assertTrue(pool.has_prereqs("Castler", {}))

    def test_precollected_castler_prerequisites_are_not_locked_twice(self):
        world = self.fundamental_world()
        world.options.locked_items.value = {"Castler": 1}
        pool = CMItemPool(world)
        locked = pool.handle_locked_items(
            Counter({
                "Play as White": 1,
                "Chessmen": 1,
                "Material": 2,
            })
        )
        self.assertEqual({"Castler": 1}, locked)
        self.assertEqual({"Castler": 1}, pool.fit_locked_items(locked, 1))
        with self.assertRaisesRegex(
            OptionError,
            "need 4 additional items.*only 2 slots",
        ):
            pool.fit_locked_items(
                {"Castler": 1, "Chessmen": 1, "Material": 2},
                2,
            )

    def test_full_access_valid_locks_preserve_required_chessmen(self):
        world = self.fundamental_world()
        world.options.accessibility.value = 1
        world.options.locked_items.value = {
            "Material": 10,
            "Chessmen": 10,
        }
        items = CMItemPool(world).create_items()
        counts = Counter(item.name for item in items)

        progression = world.geometry_progression
        required_chessmen = highest_chessmen_requirement_for_series(
            progression.stages[0].stage,
            progression.endpoint.stage,
            tactics_mode_for_options(world.options),
        )
        self.assertGreaterEqual(
            counts["Chessmen"],
            required_chessmen,
        )
        self.assertGreater(counts["Material"], 0)

    def test_item_removal_preserves_room_for_the_series_chessmen_requirement(self):
        world = self.fundamental_world()
        world.options.accessibility.value = 1
        pool = CMItemPool(world)
        pool.initialize_item_tracking()
        required = chessmen_requirement_for_world(world)

        self.assertTrue(
            pool.should_remove_item(
                "Material",
                0,
                item_table["Material"].material
                + (required - 1) * item_table["Chessmen"].material,
                [],
                ["Material"],
                {},
            )
        )

        chessmen = [
            world.create_item("Chessmen")
            for _ in range(required - 1)
        ]
        self.assertFalse(
            pool.should_remove_item(
                "Chessmen",
                (required - 1) * item_table["Chessmen"].material,
                required * item_table["Chessmen"].material,
                chessmen,
                ["Chessmen"],
                {},
            )
        )

    def test_fundamental_early_material_is_local_chessmen(self):
        world = self.fundamental_world()
        world.options.early_material.value = 3
        CMItemPool(world).create_items()
        early = world.multiworld.get_location("King to E2/E7 Early", world.player).item
        self.assertIsNotNone(early)
        self.assertEqual("Chessmen", early.name)


class TestV2SlotDataAndMaterial(CMTestBase):
    options = {"progression_itemization": "fundamental"}

    def test_slot_data_publishes_accepted_contract_and_options(self):
        slot_data = self.world.fill_slot_data()
        contract = load_production_contract()
        self.assertEqual("fundamental", slot_data["progression_itemization"])
        self.assertEqual(400, slot_data["material_item_value"])
        self.assertEqual(2, slot_data["castling_location_count"])
        self.assertEqual(UNLOCK_ITEM_ROLES, slot_data["geometry_unlock_items"])
        self.assertEqual(production_contract_document(), slot_data["apmw_contract"])
        self.assertEqual(contract.manifest_sha256, compute_manifest_sha256(production_contract_text()))
        self.assertEqual("91cf4323ae53663d1e3a7ea8facb449c74fdcd5093fa1620337f51cc5cdbe00c",
                         contract.manifest_sha256)
        self.assertEqual("0.4.0", contract.minimum_client_version)
        self.assertEqual("0.4.0", slot_data["required_chess_client_version"])
        fixture = (
            Path(__file__).parent
            / "fixtures"
            / "projection-v3"
            / "baseline.json"
        )
        self.assertEqual(
            json.loads(fixture.read_text(encoding="utf-8")),
            production_contract_document(),
        )

    def test_logic_projection_is_the_authoritative_material_view(self):
        state = CollectionState(self.multiworld)
        self.assertTrue(
            self.world.collect(state, self.world.create_item("Material"))
        )
        self.assertEqual(1, state.prog_items[self.player]["Material"])
        self.assertEqual(
            0,
            self.world.logic_projection.metrics(
                state,
                self.player,
                BoardStage.Board8x8,
            ).material,
        )
        self.assertTrue(
            self.world.collect(state, self.world.create_item("Chessmen"))
        )
        metrics = self.world.logic_projection.metrics(
            state,
            self.player,
            BoardStage.Board8x8,
        )
        self.assertEqual(485, metrics.material)
        self.assertEqual(1, metrics.chessmen)

    def test_item_link_style_overcounts_cap_logic_and_castler_effect(self):
        state = CollectionState(self.multiworld)
        material = self.world.create_item("Material")
        chessman = self.world.create_item("Chessmen")
        castler = self.world.create_item("Castler")
        for _ in range(400):
            self.world.collect(state, material)
        for _ in range(150):
            self.world.collect(state, chessman)
        for _ in range(5):
            self.world.collect(state, castler)
        self.assertEqual(321, state.count("Material", self.player))
        self.assertEqual(107, state.count("Chessmen", self.player))
        self.assertEqual(2, state.count("Castler", self.player))
        metrics = self.world.logic_projection.metrics(
            state,
            self.player,
            BoardStage.Board8x8,
        )
        self.assertEqual(1500, metrics.material)
        self.assertEqual(15, metrics.chessmen)
        self.assertEqual(2, metrics.castlers)
        self.assertEqual(2, effective_castlers(state, self.player))

        parentless = CollectionState(self.multiworld)
        self.world.collect(parentless, castler)
        self.assertEqual(0, effective_castlers(parentless, self.player))

    def test_fundamental_world_pool_excludes_legacy_material_items(self):
        names = Counter(item.name for item in self.multiworld.itempool)
        self.assertFalse(LEGACY_MATERIAL_ITEMS & names.keys())
        self.assertTrue({"Chessmen", "Material", "Castler"} <= names.keys())
        self.assertIn("Play as White", names)


class TestFundamentalLockedOverflowWorld(CMTestBase):
    options = {
        "accessibility": "full",
        "enable_tactics": "turns",
        "max_board_size": "10x8",
        "locked_items": {"Material": 10, "Chessmen": 10},
        "progression_itemization": "fundamental",
    }

    def test_full_access_valid_locks_fill_successfully(self):
        names = Counter(item.name for item in self.multiworld.itempool)
        progression = self.world.geometry_progression
        required_chessmen = highest_chessmen_requirement_for_series(
            progression.stages[0].stage,
            progression.endpoint.stage,
            tactics_mode_for_options(self.world.options),
        )
        self.assertGreaterEqual(
            names["Chessmen"],
            required_chessmen,
        )
        distribute_items_restrictive(self.multiworld)
        self.assertTrue(all(self.multiworld.get_spheres()))
