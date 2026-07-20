from .bases import CMTestBase


class VictoryLifecycleMixin:
    victory_location: str

    def test_generate_basic_fills_the_reserved_victory_capacity(self) -> None:
        locations = self.multiworld.get_locations(self.player)
        victory_location = self.multiworld.get_location(
            self.victory_location,
            self.player,
        )

        self.assertEqual("Victory", victory_location.item.name)
        self.assertNotIn("Victory", {item.name for item in self.multiworld.itempool})

        victory_location.item = None
        victory_location.locked = False
        locked_before = [
            location
            for location in locations
            if location.locked and location.item is not None
        ]
        self.assertEqual(
            len(locations) - 1,
            len(self.multiworld.itempool) + len(locked_before),
        )

        self.world.generate_basic()

        locked_after = [
            location
            for location in locations
            if location.locked and location.item is not None
        ]
        self.assertTrue(victory_location.locked)
        self.assertEqual("Victory", victory_location.item.name)
        self.assertEqual(
            len(locations),
            len(self.multiworld.itempool) + len(locked_after),
        )


class TestSingleVictoryLifecycle(VictoryLifecycleMixin, CMTestBase):
    options = {"goal": "single"}
    victory_location = "Checkmate Minima"

    def world_setup(self, *args, **kwargs) -> None:
        super().world_setup(seed=0)


class TestProgressiveVictoryLifecycle(VictoryLifecycleMixin, CMTestBase):
    options = {"goal": "progressive"}
    victory_location = "Checkmate 12x12"

    def world_setup(self, *args, **kwargs) -> None:
        super().world_setup(seed=0)


class TestOrderedVictoryLifecycle(VictoryLifecycleMixin, CMTestBase):
    options = {"goal": "ordered_progressive"}
    victory_location = "Checkmate 12x12"

    def world_setup(self, *args, **kwargs) -> None:
        super().world_setup(seed=0)
