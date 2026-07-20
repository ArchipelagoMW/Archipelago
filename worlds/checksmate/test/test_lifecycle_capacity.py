from .bases import CMTestBase


class VictoryLifecycleMixin:
    victory_location: str

    def test_create_items_places_victory_and_generate_basic_is_inert(self) -> None:
        locations = self.multiworld.get_locations(self.player)
        victory_location = self.multiworld.get_location(
            self.victory_location,
            self.player,
        )

        self.assertEqual("Victory", victory_location.item.name)
        self.assertNotIn("Victory", {item.name for item in self.multiworld.itempool})
        locked_before = [
            location
            for location in locations
            if location.locked and location.item is not None
        ]
        self.assertEqual(
            len(locations),
            len(self.multiworld.itempool) + len(locked_before),
        )

        victory_location.item = None
        victory_location.locked = False
        locked_without_victory = [
            location
            for location in locations
            if location.locked and location.item is not None
        ]
        self.assertEqual(
            len(locations) - 1,
            len(self.multiworld.itempool) + len(locked_without_victory),
        )

        self.world.generate_basic()

        self.assertFalse(victory_location.locked)
        self.assertIsNone(victory_location.item)


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
