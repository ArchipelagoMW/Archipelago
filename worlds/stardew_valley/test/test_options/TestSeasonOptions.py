from ...options import SeasonRandomization
from ...strings.season_names import Season
from ...test.bases import SVTestCase, solo_multiworld


SEASONS = {Season.spring, Season.summer, Season.fall, Season.winter}


class TestSeasonOptions(SVTestCase):
    def test_given_disabled_when_generate_then_all_seasons_are_precollected(self):
        world_options = {SeasonRandomization.internal_name: SeasonRandomization.option_disabled}
        with solo_multiworld(world_options) as (multi_world, _):
            precollected_items = {item.name for item in multi_world.precollected_items[1]}
            self.assertTrue(all([season in precollected_items for season in SEASONS]))

    def test_given_randomized_when_generate_then_all_seasons_are_in_the_pool_or_precollected(self):
        world_options = {SeasonRandomization.internal_name: SeasonRandomization.option_randomized}
        with solo_multiworld(world_options) as (multi_world, _):
            precollected_items = {item.name for item in multi_world.precollected_items[1]}
            items = {item.name for item in multi_world.get_items()} | precollected_items
            self.assertTrue(all([season in items for season in SEASONS]))
            self.assertEqual(len(SEASONS.intersection(precollected_items)), 1)

    def test_given_progressive_when_generate_then_3_progressive_seasons_are_in_the_pool(self):
        world_options = {SeasonRandomization.internal_name: SeasonRandomization.option_progressive}
        with solo_multiworld(world_options) as (multi_world, _):
            items = [item.name for item in multi_world.get_items()]
            self.assertEqual(items.count(Season.progressive), 3)