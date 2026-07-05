from ..TestGeneration import get_all_permanent_progression_items
from ..assertion import ModAssertMixin, WorldAssertMixin
from ..bases import SVTestCase, SVTestBase, solo_multiworld
from ..options.presets import allsanity_mods_7_x_x
from ... import options
from ...items import Group
from ...mods.mod_data import invalid_mod_combinations
from ...options.options import all_mods


class TestCanGenerateAllsanityWithMods(WorldAssertMixin, ModAssertMixin, SVTestCase):

    def test_allsanity_all_mods_when_generate_then_basic_checks(self):
        with solo_multiworld(allsanity_mods_7_x_x()) as (multi_world, _):
            self.assert_basic_checks(multi_world)

    def test_allsanity_all_mods_exclude_island_when_generate_then_basic_checks(self):
        world_options = allsanity_mods_7_x_x()
        world_options.update({options.ExcludeGingerIsland.internal_name: options.ExcludeGingerIsland.option_true})
        with solo_multiworld(world_options) as (multi_world, _):
            self.assert_basic_checks(multi_world)


class TestCanGenerateWithEachMod(WorldAssertMixin, ModAssertMixin, SVTestCase):
    mods = all_mods

    def test_given_single_mods_when_generate_then_basic_checks(self):
        for invalid_combination in invalid_mod_combinations:
            for mod in invalid_combination:
                mods = set(self.mods).difference(invalid_combination)
                mods.add(mod)
                with self.subTest(f"Can generate with mods: {mods}"):
                    world_options = {
                        options.Mods: frozenset(mods),
                        options.ExcludeGingerIsland: options.ExcludeGingerIsland.option_false
                    }
                    with solo_multiworld(world_options) as (multi_world, _):
                        self.assert_basic_checks(multi_world)
                        self.assert_stray_mod_items(mods, multi_world)


class TestBaseLocationDependencies(SVTestBase):
    options = {
        options.Mods.internal_name: frozenset(options.all_mods_except_invalid_combinations),
        options.ToolProgression.internal_name: options.ToolProgression.option_progressive,
        options.SeasonRandomization.internal_name: options.SeasonRandomization.option_randomized
    }


class TestBaseItemGeneration(SVTestBase):
    options = {
        options.SeasonRandomization.internal_name: options.SeasonRandomization.option_progressive,
        options.SkillProgression.internal_name: options.SkillProgression.option_progressive_with_masteries,
        options.ExcludeGingerIsland.internal_name: options.ExcludeGingerIsland.option_false,
        options.SpecialOrderLocations.internal_name: options.SpecialOrderLocations.option_board_qi,
        options.Friendsanity.internal_name: options.Friendsanity.option_all_with_marriage,
        options.Shipsanity.internal_name: options.Shipsanity.option_everything,
        options.Chefsanity.internal_name: options.Chefsanity.preset_all,
        options.Craftsanity.internal_name: options.Craftsanity.option_all,
        options.Booksanity.internal_name: options.Booksanity.option_all,
        options.Walnutsanity.internal_name: options.Walnutsanity.preset_all,
        options.Moviesanity.internal_name: options.Moviesanity.option_all_movies_and_all_loved_snacks,
        options.Eatsanity.internal_name: options.Eatsanity.preset_all,
        options.Secretsanity.internal_name: options.Secretsanity.preset_all,
        options.IncludeEndgameLocations.internal_name: options.IncludeEndgameLocations.option_true,
        options.Mods.internal_name: frozenset(options.all_mods_except_invalid_combinations),
    }

    def test_all_progression_items_are_added_to_the_pool(self):
        all_created_items = self.get_all_created_items()
        progression_items = get_all_permanent_progression_items()
        for progression_item in progression_items:
            with self.subTest(f"{progression_item.name}"):
                self.assertIn(progression_item.name, all_created_items)


class TestNoGingerIslandModItemGeneration(SVTestBase):
    options = {
        options.SeasonRandomization.internal_name: options.SeasonRandomization.option_progressive,
        options.SkillProgression.internal_name: options.SkillProgression.option_progressive_with_masteries,
        options.Friendsanity.internal_name: options.Friendsanity.option_all_with_marriage,
        options.Shipsanity.internal_name: options.Shipsanity.option_everything,
        options.Chefsanity.internal_name: options.Chefsanity.preset_all,
        options.Craftsanity.internal_name: options.Craftsanity.option_all,
        options.Booksanity.internal_name: options.Booksanity.option_all,
        options.Secretsanity.internal_name: options.Secretsanity.preset_all,
        options.Moviesanity.internal_name: options.Moviesanity.option_all_movies_and_all_loved_snacks,
        options.Eatsanity.internal_name: options.Eatsanity.preset_all,
        options.ExcludeGingerIsland.internal_name: options.ExcludeGingerIsland.option_true,
        options.IncludeEndgameLocations.internal_name: options.IncludeEndgameLocations.option_true,
        options.Mods.internal_name: frozenset(options.all_mods_except_invalid_combinations),
    }

    def test_all_progression_items_except_island_are_added_to_the_pool(self):
        all_created_items = self.get_all_created_items()
        progression_items = get_all_permanent_progression_items()
        for progression_item in progression_items:
            with self.subTest(f"{progression_item.name}"):
                if Group.GINGER_ISLAND in progression_item.groups:
                    self.assertNotIn(progression_item.name, all_created_items)
                else:
                    self.assertIn(progression_item.name, all_created_items)


class TestVanillaLogicAlternativeWhenQuestsAreNotRandomized(WorldAssertMixin, SVTestBase):
    """We often forget to add an alternative rule that works when quests are not randomized. When this happens, some
    Location are not reachable because they depend on items that are only added to the pool when quests are randomized.
    """
    options = allsanity_mods_7_x_x() | {
        options.QuestLocations.internal_name: options.QuestLocations.special_range_names["none"],
        options.Goal.internal_name: options.Goal.option_perfection,
    }

    def test_given_no_quest_all_mods_when_generate_then_can_reach_everything(self):
        self.collect_everything()
        self.assert_can_reach_everything(self.multiworld)
