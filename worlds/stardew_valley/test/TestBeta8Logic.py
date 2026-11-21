from .. import options
from ..mods.mod_data import ModNames
from ..strings.ap_names.ap_option_names import SecretsanityOptionName, StartWithoutOptionName
from ..strings.region_names import Region
from .bases import SVTestBase


class TestRecipeSourcesProperlyAccountForExtraRequirements(SVTestBase):
    options = {  # noqa: RUF012
        options.SkillProgression: options.SkillProgression.option_progressive_with_masteries,
        options.ToolProgression: options.ToolProgression.option_progressive,
        options.StartWithout: frozenset({StartWithoutOptionName.villagers, StartWithoutOptionName.house}),
        options.Craftsanity: options.Craftsanity.option_all,
        options.ElevatorProgression: options.ElevatorProgression.option_vanilla,
    }

    def test_craft_cask_requires_cellar(self):
        craft_location = "Craft Cask"
        items_required = ["Progressive House", "Shipping Bin", "Progressive Axe"] * 3
        for item in items_required:
            self.collect(item)
        items_to_test = [self.create_item(item) for item in ["Progressive House", "Robin Arrival"]]
        self.collect(items_to_test)
        self.assert_can_reach_region(Region.cellar)
        self.assert_can_reach_location(craft_location)
        for item in items_to_test:
            with self.subTest(f"{craft_location} Requires {item.name}"):
                self.remove(item)
                self.assert_cannot_reach_region(Region.cellar)
                self.assert_cannot_reach_location(craft_location)
                self.collect(item)
                self.assert_can_reach_region(Region.cellar)
                self.assert_can_reach_location(craft_location)

    def test_craft_big_stone_chest_requires_stone_chest(self):
        craft_location = "Craft Big Stone Chest"
        recipe_location = "Big Stone Chest Recipe"
        items_required = ["Dwarvish Translation Guide", "Shipping Bin", "Dwarf Arrival", "Pierre Arrival", "Progressive Pickaxe", "Spring"] * 3
        for item in items_required:
            self.collect(item)
        chest_recipe_item = self.create_item("Stone Chest Recipe")
        big_chest_recipe_item = self.create_item("Big Stone Chest Recipe")
        self.assert_cannot_reach_location(recipe_location)
        self.assert_cannot_reach_location(craft_location)
        self.collect(chest_recipe_item)
        self.assert_can_reach_location(recipe_location)
        self.assert_cannot_reach_location(craft_location)
        self.collect(big_chest_recipe_item)
        self.assert_can_reach_location(recipe_location)
        self.assert_can_reach_location(craft_location)
        self.remove(chest_recipe_item)
        self.assert_cannot_reach_location(recipe_location)
        self.assert_can_reach_location(craft_location)

    def test_craft_garden_pot_requires_evelyn_and_greenhouse(self):
        craft_location = "Craft Garden Pot"
        items_required = ["Shipping Bin", "Pierre Arrival", "Progressive Pickaxe", "Fishing Level", "Progressive Weapon", "Furnace Recipe"] * 5
        for item in items_required:
            self.collect(item)
        items_to_test = [self.create_item(item) for item in ["Greenhouse", "Evelyn Arrival"]]
        self.collect(items_to_test)
        self.assert_can_reach_location(craft_location)
        for item in items_to_test:
            with self.subTest(f"{craft_location} Requires {item.name}"):
                self.remove(item)
                self.assert_cannot_reach_location(craft_location)
                self.collect(item)
                self.assert_can_reach_location(craft_location)

    def test_craft_furnace_requires_only_recipe(self):
        craft_location = "Craft Furnace"
        items_required = ["Shipping Bin", "Pierre Arrival", "Progressive Pickaxe", "Progressive Weapon"] * 5
        for item in items_required:
            self.collect(item)
        items_to_test = [self.create_item(item) for item in ["Furnace Recipe"]]
        self.collect(items_to_test)
        self.assert_can_reach_location(craft_location)
        for item in items_to_test:
            with self.subTest(f"{craft_location} Requires {item.name}"):
                self.remove(item)
                self.assert_cannot_reach_location(craft_location)
                self.collect(item)
                self.assert_can_reach_location(craft_location)

