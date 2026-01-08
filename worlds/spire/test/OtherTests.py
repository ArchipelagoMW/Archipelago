from worlds.spire import location_table, loc_ids_to_data
from worlds.spire.test import SpireTestBase


class TestEnsureLocationActs(SpireTestBase):

    def test_check_act_one(self):
        data = loc_ids_to_data[location_table["Ironclad Reached Floor 17"]]
        self.assertEqual(1, data.act)
        data = loc_ids_to_data[location_table["Ironclad Card Reward 4"]]
        self.assertEqual(1, data.act)
        data = loc_ids_to_data[location_table["Ironclad Combat Gold 6"]]
        self.assertEqual(1, data.act)
        data = loc_ids_to_data[location_table["Ironclad Relic 3"]]
        self.assertEqual(1, data.act)
        data = loc_ids_to_data[location_table["Ironclad Elite Gold 2"]]
        self.assertEqual(1, data.act)
        data = loc_ids_to_data[location_table["Ironclad Shop Slot 5"]]
        self.assertEqual(1, data.act)
        data = loc_ids_to_data[location_table["Ironclad Potion Drop 3"]]
        self.assertEqual(1, data.act)

    def test_check_act_two(self):
        data = loc_ids_to_data[location_table["Ironclad Reached Floor 18"]]
        self.assertEqual(2, data.act)
        data = loc_ids_to_data[location_table["Ironclad Reached Floor 34"]]
        self.assertEqual(2, data.act)
        data = loc_ids_to_data[location_table["Ironclad Card Reward 5"]]
        self.assertEqual(2, data.act)
        data = loc_ids_to_data[location_table["Ironclad Card Reward 8"]]
        self.assertEqual(2, data.act)
        data = loc_ids_to_data[location_table["Ironclad Combat Gold 7"]]
        self.assertEqual(2, data.act)
        data = loc_ids_to_data[location_table["Ironclad Combat Gold 12"]]
        self.assertEqual(2, data.act)
        data = loc_ids_to_data[location_table["Ironclad Relic 4"]]
        self.assertEqual(2, data.act)
        data = loc_ids_to_data[location_table["Ironclad Relic 6"]]
        self.assertEqual(2, data.act)
        data = loc_ids_to_data[location_table["Ironclad Elite Gold 3"]]
        self.assertEqual(2, data.act)
        data = loc_ids_to_data[location_table["Ironclad Elite Gold 4"]]
        self.assertEqual(2, data.act)
        data = loc_ids_to_data[location_table["Ironclad Shop Slot 6"]]
        self.assertEqual(2, data.act)
        data = loc_ids_to_data[location_table["Ironclad Shop Slot 10"]]
        self.assertEqual(2, data.act)
        data = loc_ids_to_data[location_table["Ironclad Potion Drop 4"]]
        self.assertEqual(2, data.act)
        data = loc_ids_to_data[location_table["Ironclad Potion Drop 6"]]
        self.assertEqual(2, data.act)

    def test_check_act_three(self):
        data = loc_ids_to_data[location_table["Ironclad Reached Floor 35"]]
        self.assertEqual(3, data.act)
        data = loc_ids_to_data[location_table["Ironclad Reached Floor 56"]]
        self.assertEqual(3, data.act)
        data = loc_ids_to_data[location_table["Ironclad Card Reward 9"]]
        self.assertEqual(3, data.act)
        data = loc_ids_to_data[location_table["Ironclad Card Reward 13"]]
        self.assertEqual(3, data.act)
        data = loc_ids_to_data[location_table["Ironclad Combat Gold 13"]]
        self.assertEqual(3, data.act)
        data = loc_ids_to_data[location_table["Ironclad Combat Gold 18"]]
        self.assertEqual(3, data.act)
        data = loc_ids_to_data[location_table["Ironclad Relic 7"]]
        self.assertEqual(3, data.act)
        data = loc_ids_to_data[location_table["Ironclad Relic 10"]]
        self.assertEqual(3, data.act)
        data = loc_ids_to_data[location_table["Ironclad Elite Gold 5"]]
        self.assertEqual(3, data.act)
        data = loc_ids_to_data[location_table["Ironclad Elite Gold 7"]]
        self.assertEqual(3, data.act)
        data = loc_ids_to_data[location_table["Ironclad Shop Slot 11"]]
        self.assertEqual(3, data.act)
        data = loc_ids_to_data[location_table["Ironclad Shop Slot 16"]]
        self.assertEqual(3, data.act)
        data = loc_ids_to_data[location_table["Ironclad Potion Drop 7"]]
        self.assertEqual(3, data.act)
        data = loc_ids_to_data[location_table["Ironclad Potion Drop 9"]]
        self.assertEqual(3, data.act)
