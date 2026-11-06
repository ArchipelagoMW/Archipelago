from typing import cast, override

from test.bases import WorldTestBase
from worlds.autopelago import GAME_NAME, AutopelagoWorld


class MoonShoesAtVictoryLocationRegressionTest(WorldTestBase):
    victory_location = "snakes_on_a_planet"
    game = GAME_NAME
    run_default_tests = False # pyright: ignore[reportIncompatibleMethodOverride, reportAssignmentType]

    @override
    def setUp(self):
        self.options = {
            "victory_location": self.victory_location,
        }
        super().setUp()

    def test_moon_shoes_at_victory_location(self) -> None:
        world = cast(AutopelagoWorld, self.world)
        victory_location_item = world.get_location(world.victory_location).item
        if victory_location_item:
            self.assertEqual("Moon Shoes", victory_location_item.name)
        else:
            self.fail(f"Victory location item is None at {world.victory_location}")


class MoonShoesAtSecretCacheRegressionTest(MoonShoesAtVictoryLocationRegressionTest):
    victory_location = "secret_cache"


class MoonShoesAtCapturedGoldfishRegressionTest(MoonShoesAtVictoryLocationRegressionTest):
    victory_location = "captured_goldfish"
