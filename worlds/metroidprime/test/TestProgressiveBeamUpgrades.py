from ..Items import PROGRESSIVE_ITEM_MAPPING, ProgressiveUpgrade, SuitUpgrade
from . import MetroidPrimeTestBase


class TestProgressiveBeamUpgradesNormalStart(MetroidPrimeTestBase):
    options = {"starting_room": "normal", "progressive_beam_upgrades": True}

    def test_progressive_items_are_added_to_pool(self):
        counts = {upgrade.value: 0 for upgrade in ProgressiveUpgrade}
        for item in self.multiworld.itempool:
            if item.name in counts:
                counts[item.name] += 1
        for upgrade in ProgressiveUpgrade:
            if upgrade == ProgressiveUpgrade.Progressive_Power_Beam:
                self.assertTrue(
                    counts[upgrade.value] == 2,
                    f"{upgrade.value} had: {counts[upgrade.value]}",
                )
            else:
                self.assertTrue(
                    counts[upgrade.value] == 3,
                    f"{upgrade.value} had: {counts[upgrade.value]}",
                )

    def test_power_beam_is_precollected(self):
        has_power_beam = False
        for item in self.multiworld.precollected_items[self.player]:
            if item.name == ProgressiveUpgrade.Progressive_Power_Beam.value:
                has_power_beam = True
                break
        self.assertTrue(has_power_beam)

    def test_non_progressive_items_are_removed_from_pool(self):
        excluded_items = [SuitUpgrade.Charge_Beam.value]
        for items in PROGRESSIVE_ITEM_MAPPING.values():
            excluded_items += items

        self.assertTrue(len(excluded_items) > 10)

        for item in self.multiworld.itempool:
            self.assertTrue(item.name not in excluded_items)
