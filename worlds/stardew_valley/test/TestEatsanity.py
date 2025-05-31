import unittest

from .bases import SVTestBase
from ..options import ExcludeGingerIsland, Eatsanity
from ..strings.ap_names.ap_option_names import EatsanityOptionName


class SVEatsanityTestBase(SVTestBase):
    expected_eating_locations: set[str] = set()
    unexpected_eating_locations: set[str] = set()
    expected_eating_items: set[str] = set()
    unexpected_eating_items: set[str] = set()

    @classmethod
    def setUpClass(cls) -> None:
        if cls is SVEatsanityTestBase:
            raise unittest.SkipTest("Base tests disabled")

        super().setUpClass()

    def test_eatsanity_locations(self):
        location_names = {location.name for location in self.multiworld.get_locations()}
        for location in self.expected_eating_locations:
            self.assertIn(location, location_names, f"{location} should be in the location names")
        for location in self.unexpected_eating_locations:
            self.assertNotIn(location, location_names, f"{location} should not be in the location names")

    def test_eatsanity_items(self):
        item_names = {item.name for item in self.multiworld.get_items()}
        for item in self.expected_eating_items:
            self.assertIn(item, item_names, f"{item} should be in the item names")
        for item in self.unexpected_eating_items:
            self.assertNotIn(item, item_names, f"{item} should not be in the item names")


class TestEatsanityNone(SVEatsanityTestBase):
    options = {
        ExcludeGingerIsland: ExcludeGingerIsland.option_false,
        Eatsanity: Eatsanity.preset_none,
    }
    unexpected_eating_locations = {
        "Eat Parsnip",
        "Drink Parsnip",
        "Eat Vinegar",
        "Drink Vinegar",
        "Eat Carp",
        "Drink Pina Colada",
        "Eat Pufferfish",
        "Eat Tortilla",
    }
    unexpected_eating_items = {
        "Energy Enzyme",
        "Health Enzyme",
        "Mining Enzyme",
        "Luck Enzyme",
    }


class TestEatsanityCrops(SVEatsanityTestBase):
    options = {
        ExcludeGingerIsland: ExcludeGingerIsland.option_false,
        Eatsanity: frozenset({EatsanityOptionName.crops}),
    }
    expected_eating_locations = {
        "Eat Parsnip",
        "Eat Yam",
        "Eat Summer Spangle",
        "Eat Apple",
        "Eat Sweet Pea",
    }
    unexpected_eating_locations = {
        "Drink Parsnip",
        "Eat Vinegar",
        "Drink Vinegar",
        "Eat Carp",
        "Drink Pina Colada",
        "Eat Pufferfish",
        "Eat Tortilla",
    }
    unexpected_eating_items = {
        "Energy Enzyme",
        "Health Enzyme",
        "Mining Enzyme",
        "Luck Enzyme",
    }

    def test_need_crop_to_eat_it(self):
        crops = {"Apple": "Apple Sapling", "Yam": "Yam Seeds", "Parsnip": "Parsnip Seeds"}
        self.collect("Fall")
        self.collect("Spring")
        for crop in crops:
            location = self.world.get_location(f"Eat {crop}")
            self.assert_cannot_reach_location(location)
            self.collect(crops[crop])
            self.assert_can_reach_location(location)


class TestEatsanityCooking(SVEatsanityTestBase):
    options = {
        ExcludeGingerIsland: ExcludeGingerIsland.option_false,
        Eatsanity: frozenset({EatsanityOptionName.cooking}),
    }
    expected_eating_locations = {
        "Eat Tortilla",
        "Eat Pepper Poppers",
    }
    unexpected_eating_locations = {
        "Eat Parsnip",
        "Eat Yam",
        "Eat Summer Spangle",
        "Eat Apple",
        "Eat Sweet Pea",
        "Drink Parsnip",
        "Eat Vinegar",
        "Drink Vinegar",
        "Eat Carp",
        "Drink Pina Colada",
        "Eat Pufferfish",
    }
    unexpected_eating_items = {
        "Energy Enzyme",
        "Health Enzyme",
        "Mining Enzyme",
        "Luck Enzyme",
    }


class TestEatsanityFish(SVEatsanityTestBase):
    options = {
        ExcludeGingerIsland: ExcludeGingerIsland.option_false,
        Eatsanity: frozenset({EatsanityOptionName.fish}),
    }
    expected_eating_locations = {
        "Eat Carp",
        "Eat Bullhead",
    }
    unexpected_eating_locations = {
        "Eat Parsnip",
        "Eat Yam",
        "Eat Summer Spangle",
        "Eat Apple",
        "Eat Sweet Pea",
        "Drink Parsnip",
        "Eat Vinegar",
        "Drink Vinegar",
        "Drink Pina Colada",
        "Eat Pufferfish",
        "Eat Tortilla",
        "Eat Pepper Poppers",
    }
    unexpected_eating_items = {
        "Energy Enzyme",
        "Health Enzyme",
        "Mining Enzyme",
        "Luck Enzyme",
    }


class TestEatsanityArtisan(SVEatsanityTestBase):
    options = {
        ExcludeGingerIsland: ExcludeGingerIsland.option_false,
        Eatsanity: frozenset({EatsanityOptionName.artisan}),
    }
    expected_eating_locations = {
        "Drink Vinegar",
        "Drink Wine",
    }
    unexpected_eating_locations = {
        "Eat Parsnip",
        "Eat Yam",
        "Eat Summer Spangle",
        "Eat Apple",
        "Eat Sweet Pea",
        "Drink Parsnip",
        "Eat Vinegar",
        "Drink Pina Colada",
        "Eat Pufferfish",
        "Eat Tortilla",
        "Eat Pepper Poppers",
        "Eat Carp",
        "Eat Bullhead",
    }
    unexpected_eating_items = {
        "Energy Enzyme",
        "Health Enzyme",
        "Mining Enzyme",
        "Luck Enzyme",
    }


class TestEatsanityShop(SVEatsanityTestBase):
    options = {
        ExcludeGingerIsland: ExcludeGingerIsland.option_false,
        Eatsanity: frozenset({EatsanityOptionName.shop}),
    }
    expected_eating_locations = {
        "Drink Pina Colada",
        "Eat Stardrop",
    }
    unexpected_eating_locations = {
        "Eat Parsnip",
        "Eat Yam",
        "Eat Summer Spangle",
        "Eat Apple",
        "Eat Sweet Pea",
        "Drink Parsnip",
        "Drink Vinegar",
        "Drink Wine",
        "Eat Vinegar",
        "Eat Pufferfish",
        "Eat Tortilla",
        "Eat Pepper Poppers",
        "Eat Carp",
        "Eat Bullhead",
    }
    unexpected_eating_items = {
        "Energy Enzyme",
        "Health Enzyme",
        "Mining Enzyme",
        "Luck Enzyme",
    }


class TestEatsanityPoisonousFish(SVEatsanityTestBase):
    options = {
        ExcludeGingerIsland: ExcludeGingerIsland.option_false,
        Eatsanity: frozenset({EatsanityOptionName.poisonous, EatsanityOptionName.fish}),
    }
    expected_eating_locations = {
        "Eat Pufferfish",
        "Eat Carp",
        "Eat Bullhead",
    }
    unexpected_eating_locations = {
        "Eat Parsnip",
        "Eat Yam",
        "Eat Summer Spangle",
        "Eat Apple",
        "Eat Sweet Pea",
        "Drink Parsnip",
        "Drink Vinegar",
        "Drink Wine",
        "Eat Vinegar",
        "Eat Tortilla",
        "Eat Pepper Poppers",
        "Drink Pina Colada",
        "Eat Stardrop",
        "Eat Red Mushroom"
    }
    unexpected_eating_items = {
        "Energy Enzyme",
        "Health Enzyme",
        "Mining Enzyme",
        "Luck Enzyme",
    }


class TestEatsanityEnzymeEffects(SVEatsanityTestBase):
    options = {
        ExcludeGingerIsland: ExcludeGingerIsland.option_false,
        Eatsanity: frozenset({EatsanityOptionName.crops, EatsanityOptionName.fish, EatsanityOptionName.lock_effects}),
    }
    expected_eating_locations = {
        "Eat Parsnip",
        "Eat Yam",
        "Eat Summer Spangle",
        "Eat Apple",
        "Eat Sweet Pea",
        "Eat Carp",
        "Eat Bullhead",
    }
    unexpected_eating_locations = {
        "Drink Parsnip",
        "Drink Vinegar",
        "Drink Wine",
        "Eat Vinegar",
        "Eat Tortilla",
        "Eat Pepper Poppers",
        "Drink Pina Colada",
        "Eat Stardrop",
        "Eat Red Mushroom"
        "Eat Pufferfish",
    }
    expected_eating_items = {
        "Energy Enzyme",
        "Health Enzyme",
        "Mining Enzyme",
        "Luck Enzyme",
    }