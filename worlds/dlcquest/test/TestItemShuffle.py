from . import DLCQuestTestBase
from .. import Options

sword = "Sword"
gun = "Gun"
wooden_sword = "Wooden Sword"
pickaxe = "Pickaxe"
humble_bindle = "Humble Indie Bindle"
box_supplies = "Box of Various Supplies"
locations = [sword, gun, wooden_sword, pickaxe, humble_bindle, box_supplies]
prog_weapon_basic = "DLC Quest: Progressive Weapon"
prog_weapon_lfod = "Live Freemium or Die: Progressive Weapon"
items = [prog_weapon_basic, prog_weapon_lfod, humble_bindle, box_supplies]

important_pack = "Incredibly Important Pack"


class TestItemShuffle(DLCQuestTestBase):
    options = {Options.ItemShuffle.internal_name: Options.ItemShuffle.option_shuffled,
               Options.Campaign.internal_name: Options.Campaign.option_both}

    def test_items_in_pool(self):
        item_names = {item.name for item in self.multiworld.get_items()}
        for item in items:
            with self.subTest(f"{item}"):
                self.assertIn(item, item_names)

    def test_progressive_weapon_in_pool(self):
        item_names = [item.name for item in self.multiworld.get_items()]
        self.assertEqual(item_names.count(prog_weapon_basic), 2)
        self.assertEqual(item_names.count(prog_weapon_lfod), 2)

    def test_item_locations_in_pool(self):
        location_names = {location.name for location in self.multiworld.get_locations()}
        for item_location in locations:
            with self.subTest(f"{item_location}"):
                self.assertIn(item_location, location_names)

    def test_sword_location_has_correct_rules(self):
        self.assertFalse(self.can_reach_location(sword))
        movement_pack = self.multiworld.create_item("Movement Pack", self.player)
        self.collect(movement_pack)
        self.assertFalse(self.can_reach_location(sword))
        time_pack = self.multiworld.create_item("Time is Money Pack", self.player)
        self.collect(time_pack)
        self.assertTrue(self.can_reach_location(sword))

    def test_gun_location_has_correct_rules(self):
        self.assertFalse(self.can_reach_location(gun))
        movement_pack = self.multiworld.create_item("Movement Pack", self.player)
        self.collect(movement_pack)
        self.assertFalse(self.can_reach_location(gun))
        sword_item = self.multiworld.create_item(prog_weapon_basic, self.player)
        self.collect(sword_item)
        self.assertFalse(self.can_reach_location(gun))
        gun_pack = self.multiworld.create_item("Gun Pack", self.player)
        self.collect(gun_pack)
        self.assertTrue(self.can_reach_location(gun))

    def test_wooden_sword_location_has_correct_rules(self):
        self.assertFalse(self.can_reach_location(wooden_sword))
        important_pack_item = self.multiworld.create_item(important_pack, self.player)
        self.collect(important_pack_item)
        self.assertTrue(self.can_reach_location(wooden_sword))

    def test_bindle_location_has_correct_rules(self):
        self.assertFalse(self.can_reach_location(humble_bindle))
        wooden_sword_item = self.multiworld.create_item(prog_weapon_lfod, self.player)
        self.collect(wooden_sword_item)
        self.assertFalse(self.can_reach_location(humble_bindle))
        plants_pack = self.multiworld.create_item("Harmless Plants Pack", self.player)
        self.collect(plants_pack)
        self.assertFalse(self.can_reach_location(humble_bindle))
        wall_jump_pack = self.multiworld.create_item("Wall Jump Pack", self.player)
        self.collect(wall_jump_pack)
        self.assertFalse(self.can_reach_location(humble_bindle))
        name_change_pack = self.multiworld.create_item("Name Change Pack", self.player)
        self.collect(name_change_pack)
        self.assertFalse(self.can_reach_location(humble_bindle))
        cut_content_pack = self.multiworld.create_item("Cut Content Pack", self.player)
        self.collect(cut_content_pack)
        self.assertFalse(self.can_reach_location(humble_bindle))
        box_supplies_item = self.multiworld.create_item(box_supplies, self.player)
        self.collect(box_supplies_item)
        self.assertTrue(self.can_reach_location(humble_bindle))

    def test_box_supplies_location_has_correct_rules(self):
        self.assertFalse(self.can_reach_location(box_supplies))
        wooden_sword_item = self.multiworld.create_item(prog_weapon_lfod, self.player)
        self.collect(wooden_sword_item)
        self.assertFalse(self.can_reach_location(box_supplies))
        plants_pack = self.multiworld.create_item("Harmless Plants Pack", self.player)
        self.collect(plants_pack)
        self.assertFalse(self.can_reach_location(box_supplies))
        wall_jump_pack = self.multiworld.create_item("Wall Jump Pack", self.player)
        self.collect(wall_jump_pack)
        self.assertFalse(self.can_reach_location(box_supplies))
        name_change_pack = self.multiworld.create_item("Name Change Pack", self.player)
        self.collect(name_change_pack)
        self.assertFalse(self.can_reach_location(box_supplies))
        cut_content_pack = self.multiworld.create_item("Cut Content Pack", self.player)
        self.collect(cut_content_pack)
        self.assertTrue(self.can_reach_location(box_supplies))

    def test_pickaxe_location_has_correct_rules(self):
        self.assertFalse(self.can_reach_location(pickaxe))
        wooden_sword_item = self.multiworld.create_item(prog_weapon_lfod, self.player)
        self.collect(wooden_sword_item)
        self.assertFalse(self.can_reach_location(pickaxe))
        plants_pack = self.multiworld.create_item("Harmless Plants Pack", self.player)
        self.collect(plants_pack)
        self.assertFalse(self.can_reach_location(pickaxe))
        wall_jump_pack = self.multiworld.create_item("Wall Jump Pack", self.player)
        self.collect(wall_jump_pack)
        self.assertFalse(self.can_reach_location(pickaxe))
        name_change_pack = self.multiworld.create_item("Name Change Pack", self.player)
        self.collect(name_change_pack)
        self.assertFalse(self.can_reach_location(pickaxe))
        bindle_item = self.multiworld.create_item("Humble Indie Bindle", self.player)
        self.collect(bindle_item)
        self.assertTrue(self.can_reach_location(pickaxe))


class TestNoItemShuffle(DLCQuestTestBase):
    options = {Options.ItemShuffle.internal_name: Options.ItemShuffle.option_disabled,
               Options.Campaign.internal_name: Options.Campaign.option_both}

    def test_items_not_in_pool(self):
        item_names = {item.name for item in self.multiworld.get_items()}
        for item in items:
            with self.subTest(f"{item}"):
                self.assertNotIn(item, item_names)

    def test_item_locations_not_in_pool(self):
        location_names = {location.name for location in self.multiworld.get_locations()}
        for item_location in locations:
            with self.subTest(f"{item_location}"):
                self.assertNotIn(item_location, location_names)