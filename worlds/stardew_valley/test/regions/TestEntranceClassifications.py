from ..bases import SVTestBase
from ... import options
from ...regions.model import RandomizationFlag
from ...regions.regions import create_all_connections


class EntranceRandomizationAssertMixin:

    def assert_non_progression_are_all_accessible_with_empty_inventory(self: SVTestBase):
        # You need a tiny bit of money, for Jojamart specifically, because of a safeguard in case you get an early theater
        self.collect("Shipping Bin")
        self.collect_months(1)
        all_connections = create_all_connections(self.world.content.registered_packs)
        non_progression_connections = [connection for connection in all_connections.values() if RandomizationFlag.BIT_NON_PROGRESSION in connection.flag]

        for non_progression_connections in non_progression_connections:
            with self.subTest(connection=non_progression_connections.name):
                self.assert_can_reach_entrance(non_progression_connections.name)


# This test does not actually need to generate with entrance randomization. Entrances rules are the same regardless of the randomization.
class TestVanillaEntranceClassifications(EntranceRandomizationAssertMixin, SVTestBase):
    options = {
        options.ExcludeGingerIsland: options.ExcludeGingerIsland.option_false,
        options.Mods: frozenset()
    }

    def test_non_progression_are_all_accessible_with_empty_inventory(self):
        self.assert_non_progression_are_all_accessible_with_empty_inventory()


class TestModdedEntranceClassifications(EntranceRandomizationAssertMixin, SVTestBase):
    options = {
        options.ExcludeGingerIsland: options.ExcludeGingerIsland.option_false,
        options.Mods: frozenset(options.all_mods_except_invalid_combinations),
    }

    def test_non_progression_are_all_accessible_with_empty_inventory(self):
        self.assert_non_progression_are_all_accessible_with_empty_inventory()
