import random

from BaseClasses import get_seed
from .mod_testing_decorators import must_test_all_mods, mod_testing
from .. import SVTestBase, SVTestCase, allsanity_mods_6_x_x, fill_dataclass_with_default, solo_multiworld
from ..assertion import ModAssertMixin, WorldAssertMixin
from ... import items, Group, ItemClassification, create_content
from ... import options
from ...mods.mod_data import ModNames
from ...options import SkillProgression, Walnutsanity
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


@must_test_all_mods
class TestCanGenerateWithEachMod(WorldAssertMixin, ModAssertMixin, SVTestCase):

    @mod_testing(ModNames.deepwoods)
    def test_given_deepwoods_when_generate_with_all_vanilla_content_then_basic_checks(self):
        self.perform_basic_checks_on_mod_with_all_vanilla_content(ModNames.deepwoods)

    @mod_testing(ModNames.tractor)
    def test_given_tractor_when_generate_with_all_vanilla_content_then_basic_checks(self):
        self.perform_basic_checks_on_mod_with_all_vanilla_content(ModNames.tractor)

    @mod_testing(ModNames.big_backpack)
    def test_given_big_backpack_when_generate_with_all_vanilla_content_then_basic_checks(self):
        self.perform_basic_checks_on_mod_with_all_vanilla_content(ModNames.big_backpack)

    @mod_testing(ModNames.luck_skill)
    def test_given_luck_skill_when_generate_with_all_vanilla_content_then_basic_checks(self):
        self.perform_basic_checks_on_mod_with_all_vanilla_content(ModNames.luck_skill)

    @mod_testing(ModNames.magic)
    def test_given_magic_when_generate_with_all_vanilla_content_then_basic_checks(self):
        self.perform_basic_checks_on_mod_with_all_vanilla_content(ModNames.magic)

    @mod_testing(ModNames.socializing_skill)
    def test_given_socializing_skill_when_generate_with_all_vanilla_content_then_basic_checks(self):
        self.perform_basic_checks_on_mod_with_all_vanilla_content(ModNames.socializing_skill)

    @mod_testing(ModNames.archaeology)
    def test_given_archaeology_when_generate_with_all_vanilla_content_then_basic_checks(self):
        self.perform_basic_checks_on_mod_with_all_vanilla_content(ModNames.archaeology)

    @mod_testing(ModNames.cooking_skill)
    def test_given_cooking_skill_when_generate_with_all_vanilla_content_then_basic_checks(self):
        self.perform_basic_checks_on_mod_with_all_vanilla_content(ModNames.cooking_skill)

    @mod_testing(ModNames.binning_skill)
    def test_given_binning_skill_when_generate_with_all_vanilla_content_then_basic_checks(self):
        self.perform_basic_checks_on_mod_with_all_vanilla_content(ModNames.binning_skill)

    @mod_testing(ModNames.juna)
    def test_given_juna_when_generate_with_all_vanilla_content_then_basic_checks(self):
        self.perform_basic_checks_on_mod_with_all_vanilla_content(ModNames.juna)

    @mod_testing(ModNames.jasper)
    def test_given_jasper_when_generate_with_all_vanilla_content_then_basic_checks(self):
        self.perform_basic_checks_on_mod_with_all_vanilla_content(ModNames.jasper)

    @mod_testing(ModNames.alec)
    def test_given_alec_when_generate_with_all_vanilla_content_then_basic_checks(self):
        self.perform_basic_checks_on_mod_with_all_vanilla_content(ModNames.alec)

    @mod_testing(ModNames.yoba)
    def test_given_yoba_when_generate_with_all_vanilla_content_then_basic_checks(self):
        self.perform_basic_checks_on_mod_with_all_vanilla_content(ModNames.yoba)

    @mod_testing(ModNames.eugene)
    def test_given_eugene_when_generate_with_all_vanilla_content_then_basic_checks(self):
        self.perform_basic_checks_on_mod_with_all_vanilla_content(ModNames.eugene)

    @mod_testing(ModNames.wellwick)
    def test_given_wellwick_when_generate_with_all_vanilla_content_then_basic_checks(self):
        self.perform_basic_checks_on_mod_with_all_vanilla_content(ModNames.wellwick)

    @mod_testing(ModNames.ginger)
    def test_given_ginger_when_generate_with_all_vanilla_content_then_basic_checks(self):
        self.perform_basic_checks_on_mod_with_all_vanilla_content(ModNames.ginger)

    @mod_testing(ModNames.shiko)
    def test_given_shiko_when_generate_with_all_vanilla_content_then_basic_checks(self):
        self.perform_basic_checks_on_mod_with_all_vanilla_content(ModNames.shiko)

    @mod_testing(ModNames.delores)
    def test_given_delores_when_generate_with_all_vanilla_content_then_basic_checks(self):
        self.perform_basic_checks_on_mod_with_all_vanilla_content(ModNames.delores)

    @mod_testing(ModNames.ayeisha)
    def test_given_ayeisha_when_generate_with_all_vanilla_content_then_basic_checks(self):
        self.perform_basic_checks_on_mod_with_all_vanilla_content(ModNames.ayeisha)

    @mod_testing(ModNames.riley)
    def test_given_riley_when_generate_with_all_vanilla_content_then_basic_checks(self):
        self.perform_basic_checks_on_mod_with_all_vanilla_content(ModNames.riley)

    @mod_testing(ModNames.skull_cavern_elevator)
    def test_given_skull_cavern_elevator_when_generate_with_all_vanilla_content_then_basic_checks(self):
        self.perform_basic_checks_on_mod_with_all_vanilla_content(ModNames.skull_cavern_elevator)

    @mod_testing(ModNames.sve)
    def test_given_sve_when_generate_with_all_vanilla_content_then_basic_checks(self):
        self.perform_basic_checks_on_mod_with_all_vanilla_content(ModNames.sve)

    @mod_testing(ModNames.alecto)
    def test_given_alecto_when_generate_with_all_vanilla_content_then_basic_checks(self):
        self.perform_basic_checks_on_mod_with_all_vanilla_content(ModNames.alecto)

    @mod_testing(ModNames.distant_lands)
    def test_given_distant_lands_when_generate_with_all_vanilla_content_then_basic_checks(self):
        self.perform_basic_checks_on_mod_with_all_vanilla_content(ModNames.distant_lands)

    @mod_testing(ModNames.lacey)
    def test_given_lacey_when_generate_with_all_vanilla_content_then_basic_checks(self):
        self.perform_basic_checks_on_mod_with_all_vanilla_content(ModNames.lacey)

    @mod_testing(ModNames.boarding_house)
    def test_given_boarding_house_when_generate_with_all_vanilla_content_then_basic_checks(self):
        self.perform_basic_checks_on_mod_with_all_vanilla_content(ModNames.boarding_house)

    def perform_basic_checks_on_mod_with_all_vanilla_content(self, mod):
        world_options = {options.Mods: mod, options.ExcludeGingerIsland: options.ExcludeGingerIsland.option_false}
        with solo_multiworld(world_options) as (multi_world, _):
            self.assert_basic_checks(multi_world)
            self.assert_stray_mod_items(mod, multi_world)


@must_test_all_mods(
    excluded_mods=[ModNames.ginger, ModNames.distant_lands, ModNames.skull_cavern_elevator, ModNames.wellwick, ModNames.magic, ModNames.binning_skill,
                   ModNames.big_backpack, ModNames.luck_skill, ModNames.tractor, ModNames.shiko, ModNames.archaeology, ModNames.delores,
                   ModNames.socializing_skill, ModNames.cooking_skill])
class TestModsEntranceRandomizationBuildings(WorldAssertMixin, SVTestCase):
    """The following tests validate that ER still generates winnable and logically-sane games with given mods.
    Mods that do not interact with entrances are skipped
    Not all ER settings are tested, because 'buildings' is, essentially, a superset of all others
    """

    @mod_testing(ModNames.deepwoods)
    def test_deepwoods_entrance_randomization_buildings(self):
        self.perform_basic_checks_on_mod_with_er(ModNames.deepwoods)

    @mod_testing(ModNames.juna)
    def test_juna_entrance_randomization_buildings(self):
        self.perform_basic_checks_on_mod_with_er(ModNames.juna)

    @mod_testing(ModNames.jasper)
    def test_jasper_entrance_randomization_buildings(self):
        self.perform_basic_checks_on_mod_with_er(ModNames.jasper)

    @mod_testing(ModNames.alec)
    def test_alec_entrance_randomization_buildings(self):
        self.perform_basic_checks_on_mod_with_er(ModNames.alec)

    @mod_testing(ModNames.yoba)
    def test_yoba_entrance_randomization_buildings(self):
        self.perform_basic_checks_on_mod_with_er(ModNames.yoba)

    @mod_testing(ModNames.eugene)
    def test_eugene_entrance_randomization_buildings(self):
        self.perform_basic_checks_on_mod_with_er(ModNames.eugene)

    @mod_testing(ModNames.ayeisha)
    def test_ayeisha_entrance_randomization_buildings(self):
        self.perform_basic_checks_on_mod_with_er(ModNames.ayeisha)

    @mod_testing(ModNames.riley)
    def test_riley_entrance_randomization_buildings(self):
        self.perform_basic_checks_on_mod_with_er(ModNames.riley)

    @mod_testing(ModNames.sve)
    def test_sve_entrance_randomization_buildings(self):
        self.perform_basic_checks_on_mod_with_er(ModNames.sve)

    @mod_testing(ModNames.alecto)
    def test_alecto_entrance_randomization_buildings(self):
        self.perform_basic_checks_on_mod_with_er(ModNames.alecto)

    @mod_testing(ModNames.lacey)
    def test_lacey_entrance_randomization_buildings(self):
        self.perform_basic_checks_on_mod_with_er(ModNames.lacey)

    @mod_testing(ModNames.boarding_house)
    def test_boarding_house_entrance_randomization_buildings(self):
        self.perform_basic_checks_on_mod_with_er(ModNames.boarding_house)

    def test_all_mods_entrance_randomization_buildings(self):
        self.perform_basic_checks_on_mod_with_er(all_mods)

    def perform_basic_checks_on_mod_with_er(self, mods: str | set[str]) -> None:
        if isinstance(mods, str):
            mods = {mods}
        world_options = {
            options.EntranceRandomization: options.EntranceRandomization.option_buildings,
            options.Mods: frozenset(mods),
            options.ExcludeGingerIsland: options.ExcludeGingerIsland.option_false
        }
        with solo_multiworld(world_options) as (multi_world, _):
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
