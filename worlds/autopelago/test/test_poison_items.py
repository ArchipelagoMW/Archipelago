from math import ceil, floor
from typing import cast

from test.bases import WorldTestBase
from worlds.autopelago import GAME_NAME, AutopelagoWorld, location_name_to_nonprogression_item


def get_trap_item_count(world: AutopelagoWorld) -> int:
    return floor(sum(
        1
        for loc in world.get_locations()
        if location_name_to_nonprogression_item.get(loc.name) == "filler"
    ) / 2)

def get_expected_poison_item_count(world: AutopelagoWorld) -> int:
    trap_item_count = get_trap_item_count(world)
    return ceil(trap_item_count * world.options.death_item_percentage / 100)


class ItemsShouldGivePoisonByDefault(WorldTestBase):
    game = GAME_NAME
    run_default_tests = False

    def test_poison_items_present(self) -> None:
        world = cast(AutopelagoWorld, self.world)
        expected_poison_count = get_expected_poison_item_count(world)
        actual_poison_count = 0
        for item in self.multiworld.get_items():
            item_id = world.item_name_to_id[item.name]
            if item_id in world.enabled_auras_by_item_id and "poison" in world.enabled_auras_by_item_id[item_id]:
                actual_poison_count += 1
        self.assertEqual(expected_poison_count, actual_poison_count)


class MaxPoison(WorldTestBase):
    victory_location = "snakes_on_a_planet"
    game = GAME_NAME
    run_default_tests = True

    def setUp(self):
        self.options = {
            "victory_location": self.victory_location,
            "death_item_percentage": 100,
        }
        super().setUp()

    def test_all_the_poison(self) -> None:
        world = cast(AutopelagoWorld, self.world)
        actual_poison_count = 0
        for item in self.multiworld.get_items():
            item_id = world.item_name_to_id[item.name]
            if item_id in world.enabled_auras_by_item_id and "poison" in world.enabled_auras_by_item_id[item_id]:
                actual_poison_count += 1
        self.assertEqual(get_trap_item_count(world), actual_poison_count)


class MaxPoisonSecretCache(MaxPoison):
    victory_location = "secret_cache"


class MaxPoisonCapturedGoldfish(MaxPoison):
    victory_location = "captured_goldfish"


class ItemsShouldNotGivePoisonWithNoTrapsEnabled(WorldTestBase):
    game = GAME_NAME
    run_default_tests = False
    def setUp(self):
        self.options = {
            "enabled_buffs": frozenset(),
            "enabled_traps": frozenset(),
        }
        super().setUp()

    def test_poison_items_not_present(self) -> None:
        world = cast(AutopelagoWorld, self.world)
        for item in self.multiworld.get_items():
            item_id = world.item_name_to_id[item.name]
            if item_id in world.enabled_auras_by_item_id:
                self.assertNotIn("poison", world.enabled_auras_by_item_id[item_id])
