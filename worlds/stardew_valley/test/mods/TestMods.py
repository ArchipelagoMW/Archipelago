import random

from BaseClasses import get_seed, ItemClassification
from .. import SVTestBase, SVTestCase
from ..assertion import ModAssertMixin, WorldAssertMixin
from ..options.presets import allsanity_mods_6_x_x
from ..options.utils import fill_dataclass_with_default
from ... import options, items, Group, create_content
from ...mods.mod_data import ModNames
from ...options import SkillProgression, Walnutsanity
from ...options.options import all_mods
from ...regions import RandomizationFlag, randomize_connections, create_final_connections_and_regions


class TestGenerateModsOptions(WorldAssertMixin, ModAssertMixin, SVTestCase):

    def test_given_single_mods_when_generate_then_basic_checks(self):
        for mod in options.Mods.valid_keys:
            world_options = {options.Mods: mod, options.ExcludeGingerIsland: options.ExcludeGingerIsland.option_false}
            with self.solo_world_sub_test(f"Mod: {mod}", world_options) as (multi_world, _):
                self.assert_basic_checks(multi_world)
                self.assert_stray_mod_items(mod, multi_world)

    # The following tests validate that ER still generates winnable and logically-sane games with given mods.
    # Mods that do not interact with entrances are skipped
    # Not all ER settings are tested, because 'buildings' is, essentially, a superset of all others
    def test_deepwoods_entrance_randomization_buildings(self):
        self.perform_basic_checks_on_mod_with_er(ModNames.deepwoods, options.EntranceRandomization.option_buildings)

    def test_juna_entrance_randomization_buildings(self):
        self.perform_basic_checks_on_mod_with_er(ModNames.juna, options.EntranceRandomization.option_buildings)

    def test_jasper_entrance_randomization_buildings(self):
        self.perform_basic_checks_on_mod_with_er(ModNames.jasper, options.EntranceRandomization.option_buildings)

    def test_alec_entrance_randomization_buildings(self):
        self.perform_basic_checks_on_mod_with_er(ModNames.alec, options.EntranceRandomization.option_buildings)

    def test_yoba_entrance_randomization_buildings(self):
        self.perform_basic_checks_on_mod_with_er(ModNames.yoba, options.EntranceRandomization.option_buildings)

    def test_eugene_entrance_randomization_buildings(self):
        self.perform_basic_checks_on_mod_with_er(ModNames.eugene, options.EntranceRandomization.option_buildings)

    def test_ayeisha_entrance_randomization_buildings(self):
        self.perform_basic_checks_on_mod_with_er(ModNames.ayeisha, options.EntranceRandomization.option_buildings)

    def test_riley_entrance_randomization_buildings(self):
        self.perform_basic_checks_on_mod_with_er(ModNames.riley, options.EntranceRandomization.option_buildings)

    def test_sve_entrance_randomization_buildings(self):
        self.perform_basic_checks_on_mod_with_er(ModNames.sve, options.EntranceRandomization.option_buildings)

    def test_alecto_entrance_randomization_buildings(self):
        self.perform_basic_checks_on_mod_with_er(ModNames.alecto, options.EntranceRandomization.option_buildings)

    def test_lacey_entrance_randomization_buildings(self):
        self.perform_basic_checks_on_mod_with_er(ModNames.lacey, options.EntranceRandomization.option_buildings)

    def test_boarding_house_entrance_randomization_buildings(self):
        self.perform_basic_checks_on_mod_with_er(ModNames.boarding_house, options.EntranceRandomization.option_buildings)

    def test_all_mods_entrance_randomization_buildings(self):
        self.perform_basic_checks_on_mod_with_er(all_mods, options.EntranceRandomization.option_buildings)

    def perform_basic_checks_on_mod_with_er(self, mods: str | set[str], er_option: int) -> None:
        if isinstance(mods, str):
            mods = {mods}
        world_options = {
            options.EntranceRandomization: er_option,
            options.Mods: frozenset(mods),
            options.ExcludeGingerIsland: options.ExcludeGingerIsland.option_false
        }
        with self.solo_world_sub_test(f"entrance_randomization: {er_option}, Mods: {mods}", world_options) as (multi_world, _):
            self.assert_basic_checks(multi_world)

    def test_allsanity_all_mods_when_generate_then_basic_checks(self):
        with self.solo_world_sub_test(world_options=allsanity_mods_6_x_x()) as (multi_world, _):
            self.assert_basic_checks(multi_world)

    def test_allsanity_all_mods_exclude_island_when_generate_then_basic_checks(self):
        world_options = allsanity_mods_6_x_x()
        world_options.update({options.ExcludeGingerIsland.internal_name: options.ExcludeGingerIsland.option_true})
        with self.solo_world_sub_test(world_options=world_options) as (multi_world, _):
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
        Walnutsanity.internal_name: Walnutsanity.preset_all,
        options.Mods.internal_name: frozenset(options.Mods.valid_keys)
    }

    def test_all_progression_items_are_added_to_the_pool(self):
        all_created_items = [item.name for item in self.multiworld.itempool]
        # Ignore all the stuff that the algorithm chooses one of, instead of all, to fulfill logical progression
        items_to_ignore = [event.name for event in items.events]
        items_to_ignore.extend(deprecated.name for deprecated in items.items_by_group[Group.DEPRECATED])
        items_to_ignore.extend(season.name for season in items.items_by_group[Group.SEASON])
        items_to_ignore.extend(weapon.name for weapon in items.items_by_group[Group.WEAPON])
        items_to_ignore.extend(baby.name for baby in items.items_by_group[Group.BABY])
        items_to_ignore.extend(resource_pack.name for resource_pack in items.items_by_group[Group.RESOURCE_PACK])
        items_to_ignore.append("The Gateway Gazette")
        progression_items = [item for item in items.all_items if item.classification & ItemClassification.progression
                             and item.name not in items_to_ignore]
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
        all_created_items = [item.name for item in self.multiworld.itempool]
        # Ignore all the stuff that the algorithm chooses one of, instead of all, to fulfill logical progression
        items_to_ignore = [event.name for event in items.events]
        items_to_ignore.extend(deprecated.name for deprecated in items.items_by_group[Group.DEPRECATED])
        items_to_ignore.extend(season.name for season in items.items_by_group[Group.SEASON])
        items_to_ignore.extend(weapon.name for weapon in items.items_by_group[Group.WEAPON])
        items_to_ignore.extend(baby.name for baby in items.items_by_group[Group.BABY])
        items_to_ignore.extend(resource_pack.name for resource_pack in items.items_by_group[Group.RESOURCE_PACK])
        items_to_ignore.append("The Gateway Gazette")
        progression_items = [item for item in items.all_items if item.classification & ItemClassification.progression
                             and item.name not in items_to_ignore]
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
                SkillProgression.internal_name: SkillProgression.option_progressive_with_masteries,
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
