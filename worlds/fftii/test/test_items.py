from Fill import distribute_items_restrictive
from .bases import FFTIITestBase

from ..data.locations import (story_zodiac_stone_locations, sidequest_zodiac_stone_locations,
                              altima_only_story_zodiac_stone_locations)
from ..data.items import zodiac_stone_names, earned_job_names, shop_item_names, rare_item_names, gil_item_names, \
    jp_item_names


class TestZodiacStonesCorrectCount(FFTIITestBase):
    options = {
        "zodiac_stone_locations": 1,
        "zodiac_stones_in_pool": 13,
        "sidequest_battles": "true"
    }

    run_default_tests = False

    def test_correct_stone_count(self):
        stones_in_pool = self.get_items_by_name(zodiac_stone_names)
        self.assertEqual(len(stones_in_pool), 13, stones_in_pool)

class TestZodiacStonesCorrectAdjustment(FFTIITestBase):
    options = {
        "zodiac_stone_locations": 1,
        "zodiac_stones_in_pool": 6,
        "zodiac_stones_required": 12,
        "sidequest_battles": "true"
    }

    def test_correct_stone_count(self):
        stones_in_pool = self.get_items_by_name(zodiac_stone_names)
        self.assertEqual(len(stones_in_pool), 12, stones_in_pool)

class TestZodiacStonesCorrectAdjustmentForVanillaStones(FFTIITestBase):
    options = {
        "zodiac_stone_locations": 0,
        "zodiac_stones_in_pool": 11,
        "zodiac_stones_required": 13,
        "sidequest_battles": "false",
        "final_battles": 0
    }

    def test_correct_stone_count(self):
        self.world_setup()
        distribute_items_restrictive(self.multiworld)
        all_locations = self.multiworld.get_locations(self.player)
        zodiac_stone_locations = [location for location in all_locations if location.item.name in zodiac_stone_names]
        self.assertEqual(len(zodiac_stone_locations), len(story_zodiac_stone_locations), zodiac_stone_locations)

class TestZodiacStonesCorrectAdjustmentForVanillaStonesForSidequestsOn(FFTIITestBase):
    options = {
        "zodiac_stone_locations": 0,
        "zodiac_stones_in_pool": 11,
        "zodiac_stones_required": 13,
        "sidequest_battles": "true",
        "final_battles": 0
    }

    def test_correct_stone_count(self):
        self.world_setup()
        distribute_items_restrictive(self.multiworld)
        all_locations = self.multiworld.get_locations(self.player)
        zodiac_stone_locations = [location for location in all_locations if location.item.name in zodiac_stone_names]
        self.assertEqual(
            len(zodiac_stone_locations),
            len(story_zodiac_stone_locations) + len(sidequest_zodiac_stone_locations),
            zodiac_stone_locations)


class TestZodiacStonesCorrectAdjustmentForVanillaStonesForSidequestsAndAltimaOnlyOn(FFTIITestBase):
    options = {
        "zodiac_stone_locations": 0,
        "zodiac_stones_in_pool": 11,
        "zodiac_stones_required": 13,
        "sidequest_battles": "true",
        "final_battles": 1
    }

    def test_correct_stone_count(self):
        self.world_setup()
        distribute_items_restrictive(self.multiworld)
        all_locations = self.multiworld.get_locations(self.player)
        zodiac_stone_locations = [location for location in all_locations if location.item.name in zodiac_stone_names]
        self.assertEqual(
            len(zodiac_stone_locations),
            len(story_zodiac_stone_locations) + len(sidequest_zodiac_stone_locations) + len(altima_only_story_zodiac_stone_locations),
            zodiac_stone_locations)


class TestZodiacStonesCorrectAdjustmentForVanillaStonesForAltimaOnly(FFTIITestBase):
    options = {
        "zodiac_stone_locations": 0,
        "zodiac_stones_in_pool": 11,
        "zodiac_stones_required": 13,
        "sidequest_battles": "false",
        "final_battles": 1
    }

    def test_correct_stone_count(self):
        self.world_setup()
        distribute_items_restrictive(self.multiworld)
        all_locations = self.multiworld.get_locations(self.player)
        zodiac_stone_locations = [location for location in all_locations if location.item.name in zodiac_stone_names]
        self.assertEqual(
            len(zodiac_stone_locations),
            len(story_zodiac_stone_locations) + len(altima_only_story_zodiac_stone_locations),
            zodiac_stone_locations)

class TestJobsOn(FFTIITestBase):
    options = {
        "job_unlocks": "true"
    }

    def test_jobs_in_pool(self):
        jobs_in_pool = self.get_items_by_name(earned_job_names)
        self.assertEqual(len(jobs_in_pool), 19, jobs_in_pool)

    def test_job_requirements(self):
        with self.subTest("Starter jobs"):
            # Because we start with Squire precollected, we can reach Knight/Archer from the start.
            self.assertTrue(self.can_reach_location("Squire Unlock"))
            self.assertTrue(self.can_reach_location("Chemist Unlock"))
            self.assertTrue(self.can_reach_location("Knight Unlock"))
            self.assertTrue(self.can_reach_location("Archer Unlock"))
        with self.subTest("Knight unlocks"):
            self.assertAccessDependency(
                ["Monk Unlock", "Samurai Unlock"],
                [["Knight"]],
                only_check_listed=True)
        with self.subTest("Archer unlocks"):
            self.assertAccessDependency(
                ["Thief Unlock", "Ninja Unlock"],
                [["Archer"]],
                only_check_listed=True)
        with self.subTest("Monk unlocks"):
            self.assertAccessDependency(
                ["Geomancer Unlock", "Samurai Unlock"],
                [["Monk"]],
                only_check_listed=True)
        with self.subTest("Thief unlocks"):
            self.assertAccessDependency(
                ["Lancer Unlock", "Ninja Unlock"],
                [["Thief"]],
                only_check_listed=True)
        with self.subTest("Lancer unlocks"):
            self.assertAccessDependency(
                ["Dancer Unlock", "Samurai Unlock", "Mime Unlock"],
                [["Lancer"]],
                only_check_listed=True)
        with self.subTest("Geomancer unlocks"):
            self.assertAccessDependency(
                ["Dancer Unlock", "Ninja Unlock", "Mime Unlock"],
                [["Geomancer"]],
                only_check_listed=True)
        with self.subTest("Chemist unlocks"):
            self.assertAccessDependency(
                ["Priest Unlock", "Wizard Unlock"],
                [["Chemist"]],
                only_check_listed=True)
        with self.subTest("Priest unlocks"):
            self.assertAccessDependency(
                ["Oracle Unlock", "Calculator Unlock"],
                [["Priest"]],
                only_check_listed=True)
        with self.subTest("Wizard unlocks"):
            self.assertAccessDependency(
                ["Time Mage Unlock", "Calculator Unlock"],
                [["Wizard"]],
                only_check_listed=True)
        with self.subTest("Oracle unlocks"):
            self.assertAccessDependency(
                ["Mediator Unlock", "Calculator Unlock"],
                [["Oracle"]],
                only_check_listed=True)
        with self.subTest("Time Mage unlocks"):
            self.assertAccessDependency(
                ["Summoner Unlock", "Calculator Unlock"],
                [["Time Mage"]],
                only_check_listed=True)
        with self.subTest("Mediator unlocks"):
            self.assertAccessDependency(
                ["Bard Unlock", "Mime Unlock"],
                [["Mediator"]],
                only_check_listed=True)
        with self.subTest("Summoner unlocks"):
            self.assertAccessDependency(
                ["Bard Unlock", "Mime Unlock"],
                [["Summoner"]],
                only_check_listed=True)

class TestJobsOff(FFTIITestBase):
    options = {
        "job_unlocks": "false"
    }

    def test_jobs_in_pool(self):
        jobs_in_pool = self.get_items_by_name(earned_job_names)
        self.assertEqual(len(jobs_in_pool), 0, jobs_in_pool)

class TestNormalItemsOff(FFTIITestBase):
    options = {
        "normal_item_weight": 0,
        "rare_item_weohjt": 1
    }

    def test_normal_items_not_in_pool(self):
        normal_items_in_pool = self.get_items_by_name(shop_item_names)
        self.assertEqual(len(normal_items_in_pool), 0, normal_items_in_pool)

class TestRareItemsOff(FFTIITestBase):
    options = {
        "normal_item_weight": 1,
        "rare_item_weight": 0
    }

    def test_rare_items_not_in_pool(self):
        rare_items_in_pool = self.get_items_by_name(rare_item_names)
        self.assertEqual(len(rare_items_in_pool), 0, rare_items_in_pool)

class TestGilItemsOff(FFTIITestBase):
    options = {
        "normal_item_weight": 1,
        "bonus_gil_item_weight": 0
    }

    def test_normal_items_not_in_pool(self):
        gil_items_in_pool = self.get_items_by_name(gil_item_names)
        self.assertEqual(len(gil_items_in_pool), 0, gil_items_in_pool)

class TestJPItemsOff(FFTIITestBase):
    options = {
        "normal_item_weight": 1,
        "jp_boon_item_weight": 0
    }

    def test_normal_items_not_in_pool(self):
        jp_items_in_pool = self.get_items_by_name(jp_item_names)
        self.assertEqual(len(jp_items_in_pool), 0, jp_items_in_pool)