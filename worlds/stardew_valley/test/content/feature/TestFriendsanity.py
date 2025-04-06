import unittest

from ....content.feature import friendsanity


class TestHeartSteps(unittest.TestCase):

    def test_given_size_of_one_when_calculate_steps_then_advance_one_heart_at_the_time(self):
        steps = friendsanity.get_heart_steps(4, 1)

        self.assertEqual(steps, (1, 2, 3, 4))

    def test_given_size_of_two_when_calculate_steps_then_advance_two_heart_at_the_time(self):
        steps = friendsanity.get_heart_steps(6, 2)

        self.assertEqual(steps, (2, 4, 6))

    def test_given_size_of_three_and_max_heart_not_multiple_of_three_when_calculate_steps_then_add_max_as_last_step(self):
        steps = friendsanity.get_heart_steps(7, 3)

        self.assertEqual(steps, (3, 6, 7))


class TestExtractNpcFromLocation(unittest.TestCase):

    def test_given_npc_with_space_in_name_when_extract_then_find_name_and_heart(self):
        npc = "Mr. Ginger"
        location_name = friendsanity.to_location_name(npc, 34)

        found_name, found_heart = friendsanity.extract_npc_from_location_name(location_name)

        self.assertEqual(found_name, npc)
        self.assertEqual(found_heart, 34)
