import random
from typing import ClassVar

from BaseClasses import get_seed
from test.param import classvar_matrix
from .. import SVTestBase, SVTestCase, solo_multiworld
from ..TestGeneration import get_all_permanent_progression_items
from ..assertion import ModAssertMixin, WorldAssertMixin
from ..options.presets import allsanity_mods_6_x_x
from ..options.utils import fill_dataclass_with_default
from ... import options, Group, create_content
from ...mods.mod_data import ModNames
from ...options.options import all_mods
from ...regions import RandomizationFlag, randomize_connections, create_final_connections_and_regions


class TestCanGenerateAllsanityWithMods(WorldAssertMixin, ModAssertMixin, SVTestCase):

    def test_allsanity_all_mods_when_generate_then_basic_checks(self):
        with solo_multiworld(allsanity_mods_6_x_x()) as (multi_world, _):
            self.assert_basic_checks(multi_world)

    def test_allsanity_all_mods_exclude_island_when_generate_then_basic_checks(self):
        world_options = allsanity_mods_6_x_x()
        world_options.update({options.ExcludeGingerIsland.internal_name: options.ExcludeGingerIsland.option_true})
        with solo_multiworld(world_options) as (multi_world, _):
            self.assert_basic_checks(multi_world)


@classvar_matrix(mod=all_mods)
class TestCanGenerateWithEachMod(WorldAssertMixin, ModAssertMixin, SVTestCase):
    mod: ClassVar[str]

    def test_given_single_mods_when_generate_then_basic_checks(self):
        world_options = {
            options.Mods: self.mod,
            options.ExcludeGingerIsland: options.ExcludeGingerIsland.option_false
        }
        with solo_multiworld(world_options) as (multi_world, _):
            self.assert_basic_checks(multi_world)
            self.assert_stray_mod_items(self.mod, multi_world)


@classvar_matrix(mod=all_mods.difference([
    ModNames.ginger, ModNames.distant_lands, ModNames.skull_cavern_elevator, ModNames.wellwick, ModNames.magic, ModNames.binning_skill, ModNames.big_backpack,
    ModNames.luck_skill, ModNames.tractor, ModNames.shiko, ModNames.archaeology, ModNames.delores, ModNames.socializing_skill, ModNames.cooking_skill
]))
class TestCanGenerateEachModWithEntranceRandomizationBuildings(WorldAssertMixin, SVTestCase):
    """The following tests validate that ER still generates winnable and logically-sane games with given mods.
    Mods that do not interact with entrances are skipped
    Not all ER settings are tested, because 'buildings' is, essentially, a superset of all others
    """
    mod: ClassVar[str]

    def test_given_mod_when_generate_then_basic_checks(self) -> None:
        world_options = {
            options.EntranceRandomization: options.EntranceRandomization.option_buildings,
            options.Mods: self.mod,
            options.ExcludeGingerIsland: options.ExcludeGingerIsland.option_false
        }
        with solo_multiworld(world_options, world_caching=False) as (multi_world, _):
            self.assert_basic_checks(multi_world)


class TestBaseLocationDependencies(SVTestBase):
    options = {
        options.Mods.internal_name: frozenset(options.Mods.valid_keys),
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
        options.Chefsanity.internal_name: options.Chefsanity.option_all,
        options.Craftsanity.internal_name: options.Craftsanity.option_all,
        options.Booksanity.internal_name: options.Booksanity.option_all,
        options.Walnutsanity.internal_name: options.Walnutsanity.preset_all,
        options.Mods.internal_name: frozenset(options.Mods.valid_keys)
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
        options.Chefsanity.internal_name: options.Chefsanity.option_all,
        options.Craftsanity.internal_name: options.Craftsanity.option_all,
        options.Booksanity.internal_name: options.Booksanity.option_all,
        options.ExcludeGingerIsland.internal_name: options.ExcludeGingerIsland.option_true,
        options.Mods.internal_name: frozenset(options.Mods.valid_keys)
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


class TestModEntranceRando(SVTestCase):

    def test_mod_entrance_randomization(self):
        for option, flag in [(options.EntranceRandomization.option_pelican_town, RandomizationFlag.PELICAN_TOWN),
                             (options.EntranceRandomization.option_non_progression, RandomizationFlag.NON_PROGRESSION),
                             (options.EntranceRandomization.option_buildings_without_house, RandomizationFlag.BUILDINGS),
                             (options.EntranceRandomization.option_buildings, RandomizationFlag.BUILDINGS)]:
            sv_options = fill_dataclass_with_default({
                options.EntranceRandomization.internal_name: option,
                options.ExcludeGingerIsland.internal_name: options.ExcludeGingerIsland.option_false,
                options.SkillProgression.internal_name: options.SkillProgression.option_progressive_with_masteries,
                options.Mods.internal_name: frozenset(options.Mods.valid_keys)
            })
            content = create_content(sv_options)
            seed = get_seed()
            rand = random.Random(seed)
            with self.subTest(option=option, flag=flag, seed=seed):
                final_connections, final_regions = create_final_connections_and_regions(sv_options)

                _, randomized_connections = randomize_connections(rand, sv_options, content, final_regions, final_connections)

                for connection_name in final_connections:
                    connection = final_connections[connection_name]
                    if flag in connection.flag:
                        connection_in_randomized = connection_name in randomized_connections
                        reverse_in_randomized = connection.reverse in randomized_connections
                        self.assertTrue(connection_in_randomized, f"Connection {connection_name} should be randomized but it is not in the output")
                        self.assertTrue(reverse_in_randomized, f"Connection {connection.reverse} should be randomized but it is not in the output.")

                self.assertEqual(len(set(randomized_connections.values())), len(randomized_connections.values()),
                                 f"Connections are duplicated in randomization.")


class TestVanillaLogicAlternativeWhenQuestsAreNotRandomized(WorldAssertMixin, SVTestBase):
    """We often forget to add an alternative rule that works when quests are not randomized. When this happens, some
    Location are not reachable because they depend on items that are only added to the pool when quests are randomized.
    """
    options = allsanity_mods_6_x_x() | {
        options.QuestLocations.internal_name: options.QuestLocations.special_range_names["none"],
        options.Goal.internal_name: options.Goal.option_perfection,
    }

    def test_given_no_quest_all_mods_when_generate_then_can_reach_everything(self):
        self.collect_everything()
        self.assert_can_reach_everything(self.multiworld)
