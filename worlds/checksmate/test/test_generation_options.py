from collections import Counter

from BaseClasses import ItemClassification, PlandoOptions
from Fill import distribute_items_restrictive
from Options import OptionError, StartInventory, StartInventoryPool
from test.general import setup_multiworld

from .bases import CMTestBase
from .. import CMWorld
from ..item_pool import CMItemPool
from ..options import (
    CMOptions,
    FairyChessPawns,
    LockedItems,
    early_material_candidates,
)


def make_partial_world(options=None, seed=0):
    option_values = {"goal": "single"}
    option_values.update(options or {})
    multiworld = setup_multiworld(
        CMWorld,
        steps=("generate_early", "create_regions"),
        seed=seed,
        options=option_values,
    )
    return multiworld.worlds[1]


class TestGenerationInventoryAndEarlyMaterial(CMTestBase):
    auto_construct = False

    def test_early_material_prefers_local_when_locality_sets_overlap(self):
        options = [
            {
                "early_material": "pawn",
                "local_items": {"Progressive Pawn"},
                "non_local_items": {"Progressive Pawn"},
            },
            {"early_material": "off"},
        ]
        multiworld = setup_multiworld(
            [CMWorld, CMWorld],
            steps=("generate_early",),
            seed=0,
            options=options,
        )
        self.assertEqual(
            "Progressive Pawn",
            multiworld.worlds[1]._early_material_item_name,
        )

    def test_early_material_rejects_an_effectively_non_local_choice(self):
        options = [
            {
                "early_material": "pawn",
                "non_local_items": {"Progressive Pawn"},
            },
            {"early_material": "off"},
        ]
        with self.assertRaisesRegex(
            OptionError,
            "Early Material 'pawn' has no local candidate",
        ):
            setup_multiworld(
                [CMWorld, CMWorld],
                steps=("generate_early",),
                seed=0,
                options=options,
            )

    def test_inventory_sources_follow_upstream_pool_semantics(self):
        start_inventory = StartInventory.from_any(
            {"Progressive King Promotion": 2}
        )
        start_inventory_pool = StartInventoryPool.from_any(
            {"Progressive King Promotion": 2}
        )
        start_inventory.verify(CMWorld, "Tester", PlandoOptions.none)
        start_inventory_pool.verify(CMWorld, "Tester", PlandoOptions.none)

        base_options = {"fairy_kings": 2}
        clean = make_partial_world(base_options, seed=7)
        clean_pool = Counter(
            item.name for item in clean._item_pool.create_items()
        )

        ordinary = make_partial_world(
            {
                **base_options,
                "start_inventory": dict(start_inventory.value),
            },
            seed=7,
        )
        for _ in range(2):
            ordinary.multiworld.push_precollected(
                ordinary.create_item("Progressive King Promotion")
            )
        ordinary_pool = Counter(
            item.name for item in ordinary._item_pool.create_items()
        )

        self.assertIsInstance(ordinary.options.start_inventory, StartInventory)
        self.assertEqual(clean_pool, ordinary_pool)
        self.assertIs(
            StartInventoryPool,
            CMOptions.type_hints["start_inventory_from_pool"],
        )

        from_pool = make_partial_world(
            {
                **base_options,
                "start_inventory_from_pool": dict(
                    start_inventory_pool.value
                ),
            },
            seed=7,
        )
        for _ in range(2):
            from_pool.multiworld.push_precollected(
                from_pool.create_item("Progressive King Promotion")
            )
        generated = from_pool._item_pool.create_items()
        self.assertEqual(
            2,
            sum(
                item.name == "Progressive King Promotion"
                for item in generated
            ),
        )
        self.assertEqual(
            2,
            sum(
                item.name == "Progressive King Promotion"
                for item in from_pool.multiworld.precollected_items[1]
            ),
        )

        depleted = []
        remaining = 2
        for item in generated:
            if (
                item.name == "Progressive King Promotion"
                and remaining > 0
            ):
                remaining -= 1
            else:
                depleted.append(item)
        depleted.extend(from_pool.create_filler() for _ in range(2))
        self.assertEqual(0, remaining)
        self.assertEqual(len(generated), len(depleted))
        self.assertEqual(
            0,
            sum(
                item.name == "Progressive King Promotion"
                for item in depleted
            ),
        )
        self.assertTrue(
            all(
                item.name == "Progressive Pocket Gems"
                for item in depleted[-2:]
            )
        )

    def test_pool_inventory_rejects_the_replacement_item(self):
        with self.assertRaisesRegex(
            OptionError,
            "Progressive Pocket Gems.*replacement item.*cannot be removed",
        ):
            make_partial_world(
                {
                    "start_inventory_from_pool": {
                        "Progressive Pocket Gems": 1
                    }
                }
            )

    def test_legacy_pool_reserves_castlers_after_queen_upgrades(self):
        world = make_partial_world(
            {
                "progression_itemization": "legacy",
                "accessibility": "full",
            },
            seed=0,
        )
        generated = Counter(
            item.name for item in world._item_pool.create_items()
        )
        self.assertGreaterEqual(
            generated["Progressive Major Piece"]
            + generated["Progressive Jack"]
            - generated["Progressive Major To Queen"],
            2,
        )

    def test_jacks_can_satisfy_legacy_castler_reserve(self):
        world = make_partial_world(
            {
                "progression_itemization": "legacy",
                "accessibility": "full",
                "asymmetric_trades": "jacks",
                "major_piece_limit_by_type": 1,
                "queen_piece_limit": 1,
                "queen_piece_limit_by_type": 1,
                "locked_items": {
                    "Progressive Major To Queen": 1,
                },
            },
            seed=2,
        )
        generated = Counter(
            item.name for item in world._item_pool.create_items()
        )
        self.assertGreaterEqual(
            generated["Progressive Major Piece"],
            generated["Progressive Major To Queen"],
        )
        self.assertGreaterEqual(
            generated["Progressive Major Piece"]
            + generated["Progressive Jack"]
            - generated["Progressive Major To Queen"],
            2,
        )

    def test_fundamental_pockets_reduce_minimum_chessmen_plan(self):
        world = make_partial_world(
            {
                "goal": "single",
                "enable_tactics": "none",
                "progression_itemization": "fundamental",
                "accessibility": "full",
                "pocket_limit_by_pocket": 1,
                "locked_items": {
                    "Progressive Pocket": 3,
                },
            },
            seed=3,
        )
        items = world._item_pool.create_items()
        self.assertEqual(60, len(items))

    def test_start_inventory_queen_upgrades_also_reserve_castlers(self):
        starting_queens = 9
        world = make_partial_world(
            {
                "progression_itemization": "legacy",
                "accessibility": "full",
                "queen_piece_limit": 1,
                "queen_piece_limit_by_type": 1,
                "start_inventory": {
                    "Progressive Major To Queen": starting_queens
                },
            },
            seed=1,
        )
        generated = Counter(
            item.name for item in world._item_pool.create_items()
        )
        total_queens = world.fill_slot_data()["total_queens"]
        self.assertEqual(
            min(
                generated["Progressive Major To Queen"] + starting_queens,
                9,
            ),
            total_queens,
        )
        self.assertGreaterEqual(
            generated["Progressive Major Piece"]
            + generated["Progressive Jack"]
            - total_queens,
            2,
        )

    def test_legacy_early_material_candidate_mapping(self):
        expected_without_jacks = {
            "off": (),
            "pawn": ("Progressive Pawn",),
            "minor": ("Progressive Minor Piece",),
            "major": ("Progressive Major Piece",),
            "piece": (
                "Progressive Minor Piece",
                "Progressive Major Piece",
            ),
            "any": (
                "Progressive Pawn",
                "Progressive Minor Piece",
                "Progressive Major Piece",
            ),
            "jack": ("Progressive Major Piece",),
        }
        expected_with_jacks = {
            **expected_without_jacks,
            "any": (
                "Progressive Pawn",
                "Progressive Minor Piece",
                "Progressive Major Piece",
                "Progressive Jack",
            ),
            "jack": ("Progressive Jack",),
        }

        for asymmetric_trades, expected in (
            ("disabled", expected_without_jacks),
            ("jacks", expected_with_jacks),
        ):
            for early_material, expected_names in expected.items():
                with self.subTest(
                    asymmetric_trades=asymmetric_trades,
                    early_material=early_material,
                ):
                    world = make_partial_world(
                        {
                            "asymmetric_trades": asymmetric_trades,
                            "early_material": early_material,
                            "progression_itemization": "legacy",
                        }
                    )
                    self.assertEqual(
                        expected_names,
                        early_material_candidates(world.options),
                    )

        jack_world = make_partial_world(
            {
                "asymmetric_trades": "jacks",
                "early_material": "jack",
            }
        )
        starter = jack_world._item_pool.assign_starter_items({}, [])
        self.assertEqual(["Progressive Jack"], [item.name for item in starter])
        self.assertEqual(
            ItemClassification.progression,
            starter[0].classification,
        )

    def test_fundamental_early_material_candidate_mapping(self):
        for early_material in (
            "off",
            "pawn",
            "minor",
            "major",
            "piece",
            "any",
            "jack",
        ):
            with self.subTest(early_material=early_material):
                world = make_partial_world(
                    {
                        "early_material": early_material,
                        "progression_itemization": "fundamental",
                    }
                )
                expected = () if early_material == "off" else ("Chessmen",)
                self.assertEqual(
                    expected,
                    early_material_candidates(world.options),
                )


class TestGenerationLockedItems(CMTestBase):
    auto_construct = False

    def test_locked_items_reject_fractional_negative_and_unknown_counts(self):
        with self.assertRaises(TypeError):
            LockedItems.from_any({"Progressive Pawn": 1.5})

        negative = LockedItems.from_any({"Progressive Pawn": -2})
        with self.assertRaisesRegex(
            OptionError,
            "counts must be zero or greater.*Progressive Pawn: -2",
        ):
            negative.verify(CMWorld, "Tester", PlandoOptions.none)

        unknown = LockedItems.from_any({"Not A ChecksMate Item": 1})
        with self.assertRaisesRegex(Exception, "is not a valid item name"):
            unknown.verify(CMWorld, "Tester", PlandoOptions.none)

    def test_locked_internal_items_are_actionable_errors(self):
        for item_name in ("Victory", "Play as White", "Super-Size Me"):
            with self.subTest(item=item_name):
                with self.assertRaisesRegex(
                    OptionError,
                    rf"Locked Items: '{item_name}'.*internal/event item",
                ):
                    make_partial_world(
                        {"locked_items": {item_name: 1}}
                    )

    def test_locked_mode_and_goal_incompatibilities_are_errors(self):
        cases = (
            (
                {
                    "locked_items": {"Chessmen": 1},
                    "progression_itemization": "legacy",
                },
                "Chessmen.*progression_itemization 'legacy'",
            ),
            (
                {
                    "locked_items": {"Progressive Pawn": 1},
                    "progression_itemization": "fundamental",
                },
                "Progressive Pawn.*progression_itemization 'fundamental'",
            ),
            (
                {
                    "goal": "single",
                    "locked_items": {"Board Files": 1},
                },
                "Board Files.*unavailable for goal 'single'",
            ),
            (
                {
                    "asymmetric_trades": "disabled",
                    "locked_items": {"Progressive Jack": 1},
                },
                "Progressive Jack.*at most 0 remain available",
            ),
        )
        for options, message in cases:
            with self.subTest(options=options):
                with self.assertRaisesRegex(OptionError, message):
                    make_partial_world(options)

    def test_locked_counts_above_remaining_maximum_are_errors(self):
        with self.assertRaisesRegex(
            OptionError,
            "requested 61 'Progressive Pawn'.*at most 60 remain",
        ):
            make_partial_world(
                {"locked_items": {"Progressive Pawn": 61}}
            )

        with self.assertRaisesRegex(
            OptionError,
            "requested 60 'Progressive Pawn'.*at most 59 remain",
        ):
            make_partial_world(
                {
                    "early_material": "pawn",
                    "locked_items": {"Progressive Pawn": 60},
                }
            )

        with self.assertRaisesRegex(
            OptionError,
            "requested 57 'Progressive Pawn'.*at most 56 remain",
        ):
            make_partial_world(
                {
                    "early_material": "pawn",
                    "locked_items": {"Progressive Pawn": 57},
                    "start_inventory_from_pool": {
                        "Progressive Pawn": 3
                    },
                }
            )

    def test_locked_aggregate_capacity_is_validated(self):
        with self.assertRaisesRegex(
            OptionError,
            "require at least 61 generated pool slots.*only 60",
        ):
            make_partial_world(
                {
                    "accessibility": "minimal",
                    "enable_tactics": "none",
                    "locked_items": {
                        "Progressive Pocket Gems": 60
                    },
                }
            )

    def test_valid_inventory_and_locked_capacity_interaction_generates(self):
        world = make_partial_world(
            {
                "accessibility": "minimal",
                "early_material": "pawn",
                "locked_items": {"Progressive Pawn": 56},
                "start_inventory": {"Progressive Pawn": 5},
                "start_inventory_from_pool": {"Progressive Pawn": 3},
            },
            seed=3,
        )
        for _ in range(5):
            world.multiworld.push_precollected(
                world.create_item("Progressive Pawn")
            )
        items = world._item_pool.create_items()
        self.assertEqual(
            59,
            sum(item.name == "Progressive Pawn" for item in items),
        )
        self.assertEqual(
            "Progressive Pawn",
            world.multiworld.get_location(
                "King to E2/E7 Early", world.player
            ).item.name,
        )


class TestFairyPawnValidation(CMTestBase):
    auto_construct = False

    def test_reserved_value_fails_option_verify_and_generate_early(self):
        reserved = FairyChessPawns.from_any("reserved")
        with self.assertRaisesRegex(
            OptionError,
            "Fairy Chess Pawns 'reserved' is not implemented",
        ):
            reserved.verify(CMWorld, "Tester", PlandoOptions.none)

        with self.assertRaisesRegex(
            OptionError,
            "Fairy Chess Pawns 'reserved' is not implemented",
        ):
            make_partial_world({"fairy_chess_pawns": "reserved"})

    def test_all_named_supported_values_still_parse(self):
        for name in (
            "vanilla",
            "mixed",
            "berolina",
            "checkers",
            "any_pawn",
            "any_fairy",
            "any_classical",
        ):
            with self.subTest(name=name):
                option = FairyChessPawns.from_any(name)
                option.verify(CMWorld, "Tester", PlandoOptions.none)


class _CompleteGenerationMixin:
    def test_representative_configuration_fills_completely(self):
        expected_itemization = self.options["progression_itemization"]
        names = Counter(item.name for item in self.multiworld.itempool)
        if expected_itemization == "legacy":
            self.assertGreater(names["Progressive Pawn"], 0)
            self.assertEqual(0, names["Chessmen"])
        else:
            self.assertGreater(names["Chessmen"], 0)
            self.assertEqual(0, names["Progressive Pawn"])

        distribute_items_restrictive(self.multiworld)
        spheres = list(self.multiworld.get_spheres())
        self.assertTrue(spheres)
        self.assertTrue(all(spheres))
        self.assertTrue(
            all(
                location.item is not None
                for location in self.multiworld.get_locations()
            )
        )


class TestGenerationLegacySingle(_CompleteGenerationMixin, CMTestBase):
    options = {"goal": "single", "progression_itemization": "legacy"}


class TestGenerationLegacyProgressive(_CompleteGenerationMixin, CMTestBase):
    options = {
        "goal": "progressive",
        "progression_itemization": "legacy",
    }


class TestGenerationLegacySuper(_CompleteGenerationMixin, CMTestBase):
    options = {"goal": "super", "progression_itemization": "legacy"}


class TestGenerationFundamentalSingle(_CompleteGenerationMixin, CMTestBase):
    options = {
        "goal": "single",
        "progression_itemization": "fundamental",
    }


class TestGenerationFundamentalProgressive(
    _CompleteGenerationMixin,
    CMTestBase,
):
    options = {
        "goal": "progressive",
        "progression_itemization": "fundamental",
    }


class TestGenerationFundamentalSuper(_CompleteGenerationMixin, CMTestBase):
    options = {
        "goal": "super",
        "progression_itemization": "fundamental",
    }
