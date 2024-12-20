from unittest import TestCase

from test.bases import WorldTestBase
from .. import options_presets, ShapezWorld
from ..options import max_levels_and_upgrades, max_shapesanity


class ShapezTestBase(WorldTestBase):
    game = "shapez"
    world: ShapezWorld

    def test_location_count(self):
        self.assertTrue(self.world.location_count > 0,
                        f"location_count is {self.world.location_count} for some reason.")

    def test_logic_lists(self):
        logic_buildings = ["Cutter", "Rotator", "Painter", "Color Mixer", "Stacker"]
        for building in logic_buildings:
            count = self.world.level_logic.count(building)
            self.assertTrue(count == 1, f"{building} was found {count} times in level_logic.")
            count = self.world.upgrade_logic.count(building)
            self.assertTrue(count == 1, f"{building} was found {count} times in upgrade_logic.")
        self.assertTrue(len(self.world.level_logic) == 5,
                        f"level_logic contains {len(self.world.level_logic)} entries instead of the expected 5.")
        self.assertTrue(len(self.world.upgrade_logic) == 5,
                        f"upgrade_logic contains {len(self.world.upgrade_logic)} entries instead of the expected 5.")

    def test_random_logic_phase_length(self):
        self.assertTrue(len(self.world.random_logic_phase_length) == 5,
                        f"random_logic_phase_length contains {len(self.world.random_logic_phase_length)} entries " +
                        f"instead of the expected 5.")
        self.assertTrue(sum(self.world.random_logic_phase_length) < self.world.maxlevel,
                        f"The sum of all random phase lengths is greater than allowed: " +
                        str(sum(self.world.random_logic_phase_length)))
        for length in self.world.random_logic_phase_length:
            self.assertTrue(length in range(self.world.maxlevel),
                            f"Found an illegal value in random_logic_phase_length: {length}")

    def test_category_random_logic_amounts(self):
        self.assertTrue(len(self.world.category_random_logic_amounts) == 4,
                        f"Found {len(self.world.category_random_logic_amounts)} instead of 4 keys in "
                        f"category_random_logic_amounts.")
        self.assertTrue(min(self.world.category_random_logic_amounts.values()) == 0,
                        "Found a value less than or no 0 in category_random_logic_amounts.")
        self.assertTrue(max(self.world.category_random_logic_amounts.values()) <= 5,
                        "Found a value greater than 5 in category_random_logic_amounts.")

    def test_maxlevel_and_finaltier(self):
        self.assertTrue(self.world.maxlevel in range(25, max_levels_and_upgrades),
                        f"Found an illegal value for maxlevel: {self.world.maxlevel}")
        self.assertTrue(self.world.finaltier in range(8, max_levels_and_upgrades+1),
                        f"Found an illegal value for finaltier: {self.world.finaltier}")

    def test_included_locations(self):
        self.assertTrue(len(self.world.included_locations) > 0, "Found no locations cached in included_locations.")
        self.assertTrue("Level 1" in self.world.included_locations.keys(),
                        "Could not find Level 1 (guraranteed location) cached in included_locations.")
        self.assertTrue("Belt Upgrade Tier II" in self.world.included_locations.keys(),
                        "Could not find Belt Upgrade Tier II (guraranteed location) cached in included_locations.")
        self.assertTrue("Shapesanity 1" in self.world.included_locations.keys(),
                        "Could not find Shapesanity 1 (guraranteed location) cached in included_locations.")

    def test_shapesanity_names(self):
        names_length = len(self.world.shapesanity_names)
        locations_length = len([0 for loc in self.multiworld.get_locations(self.player) if "Shapesanity" in loc.name])
        self.assertEqual(names_length,
                         locations_length,
                         f"The amount of shapesanity names ({names_length}) does not match the amount of included " +
                         f"shapesanity locations ({locations_length}).")
        self.assertTrue("Uncolored Circle" in self.world.shapesanity_names,
                        "Uncolored Circle is guaranteed but was not found in shapesanity_names.")


class TestGlobalOptionsImport(TestCase):

    def test_global_options_import(self):
        self.assertTrue(isinstance(max_levels_and_upgrades, int), f"The global option max_levels_and_upgrades is not " +
                                                                  f"an integer, but instead a " +
                                                                  f"{type(max_levels_and_upgrades)}.")
        self.assertTrue(max_levels_and_upgrades >= 27, f"max_levels_and_upgrades must be at least 27, but is " +
                                                       f"{max_levels_and_upgrades} instead.")
        self.assertTrue(isinstance(max_shapesanity, int), f"The global option max_shapesanity is not an integer, but " +
                                                          f"instead a {type(max_levels_and_upgrades)}.")
        self.assertTrue(max_shapesanity >= 4, f"max_shapesanity must be at least 4, but is " +
                                              f"{max_levels_and_upgrades} instead.")


class TestMinimum(ShapezTestBase):
    options = options_presets["Minimum checks"]


class TestMaximum(ShapezTestBase):
    options = options_presets["Maximum checks"]


class TestRestrictive(ShapezTestBase):
    options = options_presets["Restrictive start"]


class TestAllRelevantOptions1(ShapezTestBase):
    options = {
        "goal": "vanilla",
        "randomize_level_requirements": False,
        "randomize_upgrade_requirements": False,
        "complexity_growth_gradient": "0.1234",
        "early_balancer_tunnel_and_trash": "none",
        "lock_belt_and_extractor": True,
        "include_achievements": True,
        "exclude_softlock_achievements": False,
        "exclude_long_playtime_achievements": False,
        "exclude_progression_unreasonable": True,
        "shapesanity_amount": max_shapesanity,
        "traps_percentage": "random"
    }


class TestAllRelevantOptions2(ShapezTestBase):
    options = {
        "goal": "mam",
        "goal_amount": max_levels_and_upgrades,
        "randomize_level_requirements": True,
        "randomize_upgrade_requirements": True,
        "randomize_level_logic": "random_steps",
        "randomize_upgrade_logic": "vanilla_like",
        "complexity_growth_gradient": "2",
        "early_balancer_tunnel_and_trash": "5_buildings",
        "lock_belt_and_extractor": False,
        "include_achievements": True,
        "exclude_softlock_achievements": False,
        "exclude_long_playtime_achievements": False,
        "exclude_progression_unreasonable": False,
        "shapesanity_amount": 4,
        "traps_percentage": 0
    }


class TestAllRelevantOptions3(ShapezTestBase):
    options = {
        "goal": "even_fasterer",
        "goal_amount": max_levels_and_upgrades,
        "randomize_level_requirements": True,
        "randomize_upgrade_requirements": True,
        "randomize_level_logic": "vanilla_shuffled",
        "randomize_upgrade_logic": "linear",
        "complexity_growth_gradient": "1e-003",
        "early_balancer_tunnel_and_trash": "3_buildings",
        "lock_belt_and_extractor": False,
        "include_achievements": True,
        "exclude_softlock_achievements": True,
        "exclude_long_playtime_achievements": True,
        "shapesanity_amount": "random",
        "traps_percentage": 100,
        "split_inventory_draining_trap": True
    }


class TestAllRelevantOptions4(ShapezTestBase):
    options = {
        "goal": "efficiency_iii",
        "randomize_level_requirements": True,
        "randomize_upgrade_requirements": True,
        "randomize_level_logic": "stretched_shuffled",
        "randomize_upgrade_logic": "category",
        "early_balancer_tunnel_and_trash": "sphere_1",
        "lock_belt_and_extractor": False,
        "include_achievements": True,
        "exclude_softlock_achievements": True,
        "exclude_long_playtime_achievements": True,
        "shapesanity_amount": "random",
        "traps_percentage": "random"
    }


class TestAllRelevantOptions5(ShapezTestBase):
    options = {
        "goal": "mam",
        "goal_amount": "random-range-27-500",
        "randomize_level_requirements": True,
        "randomize_upgrade_requirements": True,
        "randomize_level_logic": "quick_shuffled",
        "randomize_upgrade_logic": "category_random",
        "lock_belt_and_extractor": False,
        "include_achievements": True,
        "exclude_softlock_achievements": True,
        "exclude_long_playtime_achievements": True,
        "shapesanity_amount": "random",
        "traps_percentage": 100,
        "split_inventory_draining_trap": False
    }


class TestAllRelevantOptions6(ShapezTestBase):
    options = {
        "goal": "mam",
        "goal_amount": "random-range-27-500",
        "randomize_level_requirements": True,
        "randomize_upgrade_requirements": True,
        "randomize_level_logic": "hardcore",
        "randomize_upgrade_logic": "hardcore",
        "lock_belt_and_extractor": False,
        "include_achievements": False,
        "shapesanity_amount": "random",
        "traps_percentage": "random"
    }
