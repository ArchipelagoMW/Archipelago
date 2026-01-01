import unittest
from collections import Counter
from typing import ClassVar, Set

from .bases import SVTestBase
from ..content.feature import friendsanity
from ..options import Friendsanity, FriendsanityHeartSize

all_vanilla_bachelor = {
    "Harvey", "Elliott", "Sam", "Alex", "Shane", "Sebastian", "Emily", "Haley", "Leah", "Abigail", "Penny", "Maru"
}

all_vanilla_starting_npc = {
    "Alex", "Elliott", "Harvey", "Sam", "Sebastian", "Shane", "Abigail", "Emily", "Haley", "Leah", "Maru", "Penny", "Caroline", "Clint", "Demetrius", "Evelyn",
    "George", "Gus", "Jas", "Jodi", "Lewis", "Linus", "Marnie", "Pam", "Pierre", "Robin", "Vincent", "Willy", "Wizard", "Pet",
}

all_vanilla_npc = {
    "Alex", "Elliott", "Harvey", "Sam", "Sebastian", "Shane", "Abigail", "Emily", "Haley", "Leah", "Maru", "Penny", "Caroline", "Clint", "Demetrius", "Evelyn",
    "George", "Gus", "Jas", "Jodi", "Lewis", "Linus", "Marnie", "Pam", "Pierre", "Robin", "Vincent", "Willy", "Wizard", "Pet", "Sandy", "Dwarf", "Kent", "Leo",
    "Krobus"
}


class SVFriendsanityTestBase(SVTestBase):
    expected_npcs: ClassVar[Set[str]] = set()
    expected_pet_heart_size: ClassVar[Set[str]] = set()
    expected_bachelor_heart_size: ClassVar[Set[str]] = set()
    expected_other_heart_size: ClassVar[Set[str]] = set()

    @classmethod
    def setUpClass(cls) -> None:
        if cls is SVFriendsanityTestBase:
            raise unittest.SkipTest("Base tests disabled")

        super().setUpClass()

    def test_friendsanity(self):
        with self.subTest("Items are valid"):
            self.check_all_items_match_expected_npcs()
        with self.subTest("Correct number of items"):
            self.check_correct_number_of_items()
        with self.subTest("Locations are valid"):
            self.check_all_locations_match_expected_npcs()
        with self.subTest("Locations heart size are valid"):
            self.check_all_locations_match_heart_size()

    def check_all_items_match_expected_npcs(self):
        npc_names = {
            name
            for item in self.multiworld.itempool
            if (name := friendsanity.extract_npc_from_item_name(item.name)) is not None
        }

        self.assertEqual(npc_names, self.expected_npcs)

    def check_correct_number_of_items(self):
        item_by_npc = Counter()
        for item in self.multiworld.itempool:
            name = friendsanity.extract_npc_from_item_name(item.name)
            if name is None:
                continue

            item_by_npc[name] += 1

        for name, count in item_by_npc.items():

            if name == "Pet":
                self.assertEqual(count, len(self.expected_pet_heart_size))
            elif self.world.content.villagers[name].bachelor:
                self.assertEqual(count, len(self.expected_bachelor_heart_size))
            else:
                self.assertEqual(count, len(self.expected_other_heart_size))

    def check_all_locations_match_expected_npcs(self):
        npc_names = {
            name_and_heart[0]
            for location_name in self.get_real_location_names()
            if (name_and_heart := friendsanity.extract_npc_from_location_name(location_name))[0] is not None
        }

        self.assertEqual(npc_names, self.expected_npcs)

    def check_all_locations_match_heart_size(self):
        for location_name in self.get_real_location_names():
            name, heart_size = friendsanity.extract_npc_from_location_name(location_name)
            if name is None:
                continue

            if name == "Pet":
                self.assertIn(heart_size, self.expected_pet_heart_size)
            elif self.world.content.villagers[name].bachelor:
                self.assertIn(heart_size, self.expected_bachelor_heart_size)
            else:
                self.assertIn(heart_size, self.expected_other_heart_size)


class TestFriendsanityNone(SVFriendsanityTestBase):
    options = {
        Friendsanity: Friendsanity.option_none,
    }

    @property
    def run_default_tests(self) -> bool:
        # None is default
        return False


class TestFriendsanityBachelors(SVFriendsanityTestBase):
    options = {
        Friendsanity: Friendsanity.option_bachelors,
        FriendsanityHeartSize: 1,
    }
    expected_npcs = all_vanilla_bachelor
    expected_bachelor_heart_size = {1, 2, 3, 4, 5, 6, 7, 8}


class TestFriendsanityStartingNpcs(SVFriendsanityTestBase):
    options = {
        Friendsanity: Friendsanity.option_starting_npcs,
        FriendsanityHeartSize: 1,
    }
    expected_npcs = all_vanilla_starting_npc
    expected_pet_heart_size = {1, 2, 3, 4, 5}
    expected_bachelor_heart_size = {1, 2, 3, 4, 5, 6, 7, 8}
    expected_other_heart_size = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}


class TestFriendsanityAllNpcs(SVFriendsanityTestBase):
    options = {
        Friendsanity: Friendsanity.option_all,
        FriendsanityHeartSize: 4,
    }
    expected_npcs = all_vanilla_npc
    expected_pet_heart_size = {4, 5}
    expected_bachelor_heart_size = {4, 8}
    expected_other_heart_size = {4, 8, 10}


class TestFriendsanityHeartSize3(SVFriendsanityTestBase):
    options = {
        Friendsanity: Friendsanity.option_all_with_marriage,
        FriendsanityHeartSize: 3,
    }
    expected_npcs = all_vanilla_npc
    expected_pet_heart_size = {3, 5}
    expected_bachelor_heart_size = {3, 6, 9, 12, 14}
    expected_other_heart_size = {3, 6, 9, 10}


class TestFriendsanityHeartSize5(SVFriendsanityTestBase):
    options = {
        Friendsanity: Friendsanity.option_all_with_marriage,
        FriendsanityHeartSize: 5,
    }
    expected_npcs = all_vanilla_npc
    expected_pet_heart_size = {5}
    expected_bachelor_heart_size = {5, 10, 14}
    expected_other_heart_size = {5, 10}
