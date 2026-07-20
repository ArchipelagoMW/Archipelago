from collections import Counter

from BaseClasses import ItemClassification, PlandoOptions
from Fill import distribute_items_restrictive
from Options import StartInventory, StartInventoryPool
from test.general import setup_multiworld

from .bases import CMTestBase
from .. import CMWorld
from ..item_pool import CMItemPool
from ..options import CMOptions, LockedItems


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

    def test_legacy_inventory_sources_use_upstream_types_but_merge_as_precollected(self):
        """Legacy behavior: ChecksMate has no from-pool option or precollected source provenance."""
        start_inventory = StartInventory.from_any({"Progressive Pawn": 2})
        start_inventory_pool = StartInventoryPool.from_any({"Progressive Pawn": 3})
        start_inventory.verify(CMWorld, "Tester", PlandoOptions.none)
        start_inventory_pool.verify(CMWorld, "Tester", PlandoOptions.none)

        world = make_partial_world({"start_inventory": dict(start_inventory.value)})
        self.assertIsInstance(world.options.start_inventory, StartInventory)
        self.assertEqual({"Progressive Pawn": 2}, world.options.start_inventory.value)
        self.assertNotIn("start_inventory_from_pool", CMOptions.type_hints)

        for source in (start_inventory, start_inventory_pool):
            for item_name, count in source.value.items():
                for _ in range(count):
                    world.multiworld.push_precollected(world.create_item(item_name))

        pool = CMItemPool(world)
        self.assertEqual({"Progressive Pawn": 5}, pool.get_excluded_items())

    def test_legacy_early_material_candidate_names(self):
        expected_without_jacks = {
            "off": set(),
            "pawn": {"Progressive Pawn"},
            "minor": {"Progressive Minor Piece"},
            "major": {"Progressive Major Piece"},
            "piece": {"Progressive Minor Piece", "Progressive Major Piece"},
            "any": {
                "Progressive Pawn",
                "Progressive Minor Piece",
                "Progressive Major Piece",
            },
            # Legacy behavior: "jack" currently broadens to every basic class.
            "jack": {
                "Progressive Pawn",
                "Progressive Minor Piece",
                "Progressive Major Piece",
            },
        }
        expected_with_jacks = {
            name: candidates | ({"Progressive Jack"} if name in {"major", "piece", "any", "jack"} else set())
            for name, candidates in expected_without_jacks.items()
        }

        for asymmetric_trades, expected in (
            ("disabled", expected_without_jacks),
            ("jacks", expected_with_jacks),
        ):
            for early_material, expected_names in expected.items():
                with self.subTest(
                    itemization="legacy",
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
                        self.observe_early_material_candidates(world),
                    )

    def test_fundamental_early_material_candidate_names(self):
        for early_material in ("off", "pawn", "minor", "major", "piece", "any", "jack"):
            with self.subTest(itemization="fundamental", early_material=early_material):
                world = make_partial_world(
                    {
                        "early_material": early_material,
                        "progression_itemization": "fundamental",
                    }
                )
                expected = set() if early_material == "off" else {"Chessmen"}
                self.assertEqual(expected, self.observe_early_material_candidates(world))

    def observe_early_material_candidates(self, world):
        location = world.multiworld.get_location("King to E2/E7 Early", world.player)
        observed = set()
        for seed in range(64):
            location.item = None
            location.locked = False
            world.random.seed(seed)
            starter_items = CMItemPool(world).assign_starter_items({}, [])
            self.assertEqual(bool(starter_items), location.item is not None)
            if starter_items:
                self.assertIs(starter_items[0], location.item)
                self.assertEqual(ItemClassification.progression, location.item.classification)
                observed.add(location.item.name)
        return observed


class TestGenerationLockedItems(CMTestBase):
    auto_construct = False

    def test_locked_items_upstream_validation_and_legacy_negative_handling(self):
        with self.assertRaises(TypeError):
            LockedItems.from_any({"Progressive Pawn": 1.5})

        negative = LockedItems.from_any({"Progressive Pawn": -2})
        negative.verify(CMWorld, "Tester", PlandoOptions.none)
        world = make_partial_world()
        self.assertEqual({}, CMItemPool(world).normalize_counts(negative.value))

        unknown = LockedItems.from_any({"Not A ChecksMate Item": 1})
        with self.assertRaisesRegex(Exception, "is not a valid item name"):
            unknown.verify(CMWorld, "Tester", PlandoOptions.none)

    def test_locked_items_normalize_mode_limits_and_internal_requests(self):
        legacy = CMItemPool(make_partial_world({"goal": "progressive"}))
        self.assertEqual(
            {
                "Progressive Pawn": 60,
                "Progressive Minor Piece": 2,
                "Board Files": 2,
                "Victory": 1,
                "Play as White": 1,
                # Legacy behavior: zero-quantity internal items are treated as uncapped.
                "Super-Size Me": 999,
            },
            legacy.normalize_counts(
                {
                    "Progressive Pawn": 999,
                    "Progressive Minor Piece": 2.9,
                    "Chessmen": 5,
                    "Board Files": 999,
                    "Victory": 999,
                    "Play as White": 999,
                    "Super-Size Me": 999,
                    "Not A ChecksMate Item": 1,
                }
            ),
        )

        fundamental = CMItemPool(
            make_partial_world(
                {"goal": "progressive", "progression_itemization": "fundamental"}
            )
        )
        self.assertEqual(
            {
                "Chessmen": 107,
                "Material": 321,
                "Castler": 2,
                "Board Files": 2,
                "Board Ranks": 2,
            },
            fundamental.normalize_counts(
                {
                    "Progressive Pawn": 999,
                    "Chessmen": 999,
                    "Material": 999,
                    "Castler": 999,
                    "Board Files": 999,
                    "Board Ranks": 999,
                }
            ),
        )

    def test_locked_over_cap_is_reduced_by_precollected_and_early_preplacement(self):
        world = make_partial_world(
            {
                "early_material": "pawn",
                "locked_items": {"Progressive Pawn": 999},
                "progression_itemization": "legacy",
            }
        )
        for _ in range(2):
            world.multiworld.push_precollected(world.create_item("Progressive Pawn"))

        pool = CMItemPool(world)
        pool.initialize_item_tracking()
        excluded = pool.get_excluded_items()
        starter_items = pool.assign_starter_items(excluded, [])
        for item in starter_items:
            pool.consume_item(item.name, {})
        pool.handle_excluded_items(excluded)

        self.assertEqual(["Progressive Pawn"], [item.name for item in starter_items])
        self.assertEqual(3, pool.items_used[world.player]["Progressive Pawn"])
        self.assertEqual(57, pool.handle_locked_items()["Progressive Pawn"])

    def test_locked_internal_requests_survive_normalization_as_legacy_behavior(self):
        world = make_partial_world(
            {
                "locked_items": {
                    "Play as White": 5,
                    "Victory": 5,
                    "Super-Size Me": 5,
                }
            }
        )
        pool = CMItemPool(world)
        pool.initialize_item_tracking()
        required = pool.initialize_required_items()
        locked = pool.handle_locked_items()

        self.assertEqual(["Play as White"], [item.name for item in required])
        self.assertNotIn("Play as White", locked)
        self.assertEqual(1, locked["Victory"])
        self.assertEqual(5, locked["Super-Size Me"])


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
        self.assertTrue(all(location.item is not None for location in self.multiworld.get_locations()))


class TestGenerationLegacySingle(_CompleteGenerationMixin, CMTestBase):
    options = {"goal": "single", "progression_itemization": "legacy"}


class TestGenerationLegacyProgressive(_CompleteGenerationMixin, CMTestBase):
    options = {"goal": "progressive", "progression_itemization": "legacy"}


class TestGenerationLegacySuper(_CompleteGenerationMixin, CMTestBase):
    options = {"goal": "super", "progression_itemization": "legacy"}


class TestGenerationFundamentalSingle(_CompleteGenerationMixin, CMTestBase):
    options = {"goal": "single", "progression_itemization": "fundamental"}


class TestGenerationFundamentalProgressive(_CompleteGenerationMixin, CMTestBase):
    options = {"goal": "progressive", "progression_itemization": "fundamental"}


class TestGenerationFundamentalSuper(_CompleteGenerationMixin, CMTestBase):
    options = {"goal": "super", "progression_itemization": "fundamental"}
