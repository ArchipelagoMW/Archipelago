from ..bases import SVTestBase
from ..options.presets import allsanity_mods_7_x_x
from ... import locations_by_tag
from ...content.feature.hatsanity import to_location_name
from ...data.hats_data import Hats
from ...locations import LocationTags
from ...options import Hatsanity, SeasonRandomization, FestivalLocations, Shipsanity, Eatsanity, Cooksanity, Fishsanity, Craftsanity
from ...options.options import AllowedFillerItems
from ...strings.ap_names.ap_option_names import HatsanityOptionName, AllowedFillerOptionName


class TestHatsLogic(SVTestBase):
    options = {
        SeasonRandomization.internal_name: SeasonRandomization.option_randomized,
        FestivalLocations.internal_name: FestivalLocations.option_hard,
        Shipsanity.internal_name: Shipsanity.option_everything,
        Hatsanity.internal_name: Hatsanity.preset_all,
        "start_inventory": {"Fall": 1}
    }

    def test_need_spring_to_grab_leprechaun_hat(self):
        hat_location = to_location_name(Hats.leprechaun_hat)
        self.assert_cannot_reach_location(hat_location)
        self.collect("Spring")
        self.assert_can_reach_location(hat_location)

    def test_need_pans_to_wear_pan_hats(self):
        pan_hats = [Hats.copper_pan_hat, Hats.steel_pan_hat, Hats.gold_pan_hat, Hats.iridium_pan_hat]
        locations = [to_location_name(hat) for hat in pan_hats]
        for location in locations:
            self.assert_cannot_reach_location(location)
            self.collect("Progressive Pan")
            self.assert_can_reach_location(location)

    def test_reach_frog_hat(self):
        required_item_names = ["Progressive Fishing Rod", "Island Obelisk", "Island West Turtle", "Island Farmhouse"]
        required_items = [self.create_item(item_name) for item_name in required_item_names]
        location = to_location_name(Hats.frog_hat)
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
        AllowedFillerItems.internal_name: frozenset({AllowedFillerOptionName.hats}),
        SeasonRandomization.internal_name: SeasonRandomization.option_randomized,
        FestivalLocations.internal_name: FestivalLocations.option_hard,
        Fishsanity.internal_name: Fishsanity.option_all,
        Shipsanity.internal_name: Shipsanity.option_everything,
        Cooksanity.internal_name: Cooksanity.option_all,
        Craftsanity.internal_name: Craftsanity.option_all,
        Eatsanity.internal_name: Eatsanity.preset_all,
        Hatsanity.internal_name: Hatsanity.preset_none,
        "start_inventory": {"Fall": 1}
    }

    def test_there_are_hats_in_item_pool(self):
        item_pool = [item.name for item in self.multiworld.itempool]
        self.assertTrue("Leprechaun Hat" in item_pool)
        self.assertTrue("Straw Hat" in item_pool)
        self.assertTrue("Cone Hat" in item_pool)
        self.assertTrue("Mummy Mask" in item_pool)


class TestHatLocations(SVTestBase):
    options = allsanity_mods_7_x_x()

    def test_all_hat_locations_are_added(self):
        location_names = [location.name for location in self.multiworld.get_locations()]
        for hat_location in locations_by_tag[LocationTags.HATSANITY]:
            with self.subTest(hat_location.name):
                if hat_location.name == "Wear Panda Hat":
                    self.assertNotIn(hat_location.name, location_names, "The Panda Hat cannot be obtained on the standard edition of the game")
                else:
                    self.assertIn(hat_location.name, location_names)


class TestHatsOptionSetIndependence(SVTestBase):
    options = {
        Hatsanity.internal_name: frozenset({HatsanityOptionName.difficult}),
    }

    def test_only_difficult_hats_are_added(self):
        difficult_hats = [Hats.magic_cowboy_hat, Hats.plum_chapeau, Hats.watermelon_band]
        not_difficult_hats = [Hats.steel_pan_hat, Hats.party_hat_blue, Hats.frog_hat, Hats.cowboy, Hats.elegant_turban]
        location_names = [location.name for location in self.multiworld.get_locations()]
        for hat in difficult_hats:
            with self.subTest(hat.name):
                self.assertIn(to_location_name(hat), location_names)
        for hat in not_difficult_hats:
            with self.subTest(hat.name):
                self.assertNotIn(to_location_name(hat), location_names)

