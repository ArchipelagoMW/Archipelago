from ..bases import SVTestBase
from ...data.hats_data import Hats
from ...options import Hatsanity, SeasonRandomization, FestivalLocations, Shipsanity, Eatsanity, Cooksanity, Fishsanity, Craftsanity


class TestHatsLogic(SVTestBase):
    options = {
        SeasonRandomization.internal_name: SeasonRandomization.option_randomized,
        FestivalLocations.internal_name: FestivalLocations.option_hard,
        Shipsanity.internal_name: Shipsanity.option_everything,
        Hatsanity.internal_name: Hatsanity.option_post_perfection,
        "start_inventory": {"Fall": 1}
    }

    def test_need_spring_to_grab_leprechaun_hat(self):
        hat_location = Hats.leprechaun_hat.to_location_name()
        self.assert_cannot_reach_location(hat_location)
        self.collect("Spring")
        self.assert_can_reach_location(hat_location)

    def test_need_pans_to_wear_pan_hats(self):
        pan_hats = [Hats.copper_pan_hat, Hats.steel_pan_hat, Hats.gold_pan_hat, Hats.iridium_pan_hat]
        locations = [hat.to_location_name() for hat in pan_hats]
        for location in locations:
            self.assert_cannot_reach_location(location)
            self.collect("Progressive Pan")
            self.assert_can_reach_location(location)

    def test_reach_frog_hat(self):
        required_item_names = ["Progressive Fishing Rod", "Wizard Invitation", "Island Obelisk", "Island West Turtle", "Island Farmhouse"]
        required_items = [self.create_item(item_name) for item_name in required_item_names]
        location = Hats.frog_hat.to_location_name()
        for required_item in required_items:
            self.collect(required_item)
        self.assert_can_reach_location(location)
        for required_item in required_items:
            with self.subTest(f"Requires {required_item.name} to {location}"):
                self.remove(required_item)
                self.assert_cannot_reach_location(location)
                self.collect(required_item)

    def test_no_hats_in_item_pool(self):
        item_pool = self.multiworld.itempool
        for item in item_pool:
            self.assertTrue("Hat" not in item.name)
            self.assertTrue("Mask" not in item.name)


class TestNoHatsLogic(SVTestBase):
    options = {
        SeasonRandomization.internal_name: SeasonRandomization.option_randomized,
        FestivalLocations.internal_name: FestivalLocations.option_hard,
        Fishsanity.internal_name: Fishsanity.option_all,
        Shipsanity.internal_name: Shipsanity.option_everything,
        Cooksanity.internal_name: Cooksanity.option_all,
        Craftsanity.internal_name: Craftsanity.option_all,
        Eatsanity.internal_name: Eatsanity.preset_all,
        Hatsanity.internal_name: Hatsanity.option_none,
        "start_inventory": {"Fall": 1}
    }

    def test_there_are_hats_in_item_pool(self):
        item_pool = [item.name for item in self.multiworld.itempool]
        self.assertTrue("Leprechaun Hat" in item_pool)
        self.assertTrue("Straw Hat" in item_pool)
        self.assertTrue("Cone Hat" in item_pool)
        self.assertTrue("Mummy Mask" in item_pool)


