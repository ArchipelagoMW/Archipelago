from collections import Counter
from unittest.mock import patch

from ..bases import SVTestBase
from ..options import presets
from ... import options, StardewLogic, StardewRule
from ...logic.museum_logic import MuseumLogic
from ...stardew_rule import true_, LiteralStardewRule


class TestMuseumMilestones(SVTestBase):
    options = {
        options.Museumsanity: options.Museumsanity.option_milestones
    }

    def test_50_milestone(self):
        self.multiworld.state.prog_items = {1: Counter()}

        milestone_rule = self.world.logic.museum.can_find_museum_items(50)
        self.assert_rule_false(milestone_rule, self.multiworld.state)


class DisabledMuseumRule(LiteralStardewRule):
    value = False

    def __or__(self, other) -> StardewRule:
        return other

    def __and__(self, other) -> StardewRule:
        return self

    def __repr__(self):
        return "Disabled Museum Rule"


class TestMuseumsanityDisabledExcludesMuseumDonationsFromOtherLocations(SVTestBase):
    options = {
        **presets.allsanity_mods_6_x_x(),
        options.Museumsanity.internal_name: options.Museumsanity.option_none
    }

    def test_museum_donations_are_never_required_in_any_locations(self):
        with patch("worlds.stardew_valley.logic.museum_logic.MuseumLogic") as MockMuseumLogic:
            museum_logic: MuseumLogic = MockMuseumLogic.return_value
            museum_logic.can_donate_museum_items.return_value = DisabledMuseumRule()
            museum_logic.can_donate_museum_artifacts.return_value = DisabledMuseumRule()
            museum_logic.can_find_museum_artifacts.return_value = DisabledMuseumRule()
            museum_logic.can_find_museum_minerals.return_value = DisabledMuseumRule()
            museum_logic.can_find_museum_items.return_value = DisabledMuseumRule()
            museum_logic.can_complete_museum.return_value = DisabledMuseumRule()
            museum_logic.can_donate.return_value = DisabledMuseumRule()
            # Allowing calls to museum rules since a lot of other logic depends on it, for minerals for instance.
            museum_logic.can_find_museum_item.return_value = true_

            regions = {region.name for region in self.multiworld.regions}
            self.world.logic = StardewLogic(self.player, self.world.options, self.world.content, regions)
            self.world.set_rules()

            self.collect_everything()
            for location in self.get_real_locations():
                with self.subTest(location.name):
                    self.assert_can_reach_location(location)
