from .. import SVTestBase, SVTestCase,  allsanity_mods_6_x_x
from ..assertion import ModAssertMixin, WorldAssertMixin
from ... import items, Group, ItemClassification, StardewValleyWorld
from ... import options
from ...mods.mod_data import ModNames
from ...options.options import all_mods
from ...regions.entrance_rando import create_player_randomization_flag
from ...regions.regions import create_all_connections


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
        options.Walnutsanity.internal_name: options.Walnutsanity.preset_all,
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

    def test_entrance_randomization(self):
        for option in (options.EntranceRandomization.option_pelican_town, options.EntranceRandomization.option_non_progression,
                       options.EntranceRandomization.option_buildings_without_house, options.EntranceRandomization.option_buildings):
            test_options = {
                options.EntranceRandomization: option,
                options.ExcludeGingerIsland: options.ExcludeGingerIsland.option_false,
                options.SkillProgression: options.SkillProgression.option_progressive_with_masteries,
                options.Mods: frozenset(options.Mods.valid_keys)
            }
            with self.solo_world_sub_test(world_options=test_options, world_caching=False) as (multiworld, world):
                world: StardewValleyWorld
                entrances_placement = world.randomized_entrances
                flag = create_player_randomization_flag(world.options.entrance_randomization, world.content)

                expected_randomized_connections = [connection
                                                   for connection in create_all_connections(world.content.registered_packs).values()
                                                   if connection.is_eligible_for_randomization(flag)]
                for connection in expected_randomized_connections:
                    self.assertIn(connection.name, entrances_placement,
                                  f"Connection {connection.name} should be randomized but it is not in the output.")
                    self.assertIn(connection.reverse, entrances_placement,
                                  f"Connection {connection.reverse} should be randomized but it is not in the output.")

                self.assertEqual(len(set(entrances_placement.values())), len(entrances_placement.values()),
                                 f"Connections are duplicated in randomization.")
