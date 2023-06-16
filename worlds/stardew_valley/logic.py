from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Dict, Union, Optional, Iterable, Sized, List, Set

from . import options
from .data import all_fish, FishItem, all_purchasable_seeds, SeedItem, all_crops, CropItem
from .data.bundle_data import BundleItem
from .data.fish_data import island_fish
from .data.museum_data import all_museum_items, MuseumItem, all_artifact_items
from .data.recipe_data import all_cooking_recipes, CookingRecipe, RecipeSource, FriendshipSource, QueenOfSauceSource
from .data.villagers_data import all_villagers_by_name, Villager
from .items import all_items, Group
from .mods.mod_data import ModNames
from .mods.mod_logic import can_earn_mod_skill_level, append_mod_skill_level
from .options import StardewOptions
from .regions import vanilla_regions
from .stardew_rule import False_, Reach, Or, True_, Received, Count, And, Has, TotalReceived, StardewRule
from .strings.animal_product_names import AnimalProduct
from .strings.building_names import Building
from .strings.crop_names import Crop
from .strings.forageable_names import Forageable
from .strings.generic_names import Generic
from .strings.geode_names import Geode
from .strings.ingredient_names import Ingredient
from .strings.item_names import Item
from .strings.machine_names import Machine
from .strings.meal_names import Meal
from .strings.metal_names import Ore, MetalBar
from .strings.quest_names import Quest
from .strings.region_names import Region
from .strings.season_names import Season
from .strings.skill_names import Skill
from .strings.tool_names import Tool, Material
from .strings.tv_channel_names import Channel
from .strings.villager_names import NPC

MAX_MONTHS = 12
MONEY_PER_MONTH = 15000
MISSING_ITEM = "THIS ITEM IS MISSING"

tool_materials = {
    Material.copper: 1,
    Material.iron: 2,
    Material.gold: 3,
    Material.iridium: 4
}

tool_prices = {
    Material.copper: 2000,
    Material.iron: 5000,
    Material.gold: 10000,
    Material.iridium: 25000
}

week_days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]


@dataclass(frozen=True, repr=False)
class StardewLogic:
    player: int
    options: StardewOptions

    item_rules: Dict[str, StardewRule] = field(default_factory=dict)
    sapling_rules: Dict[str, StardewRule] = field(default_factory=dict)
    tree_fruit_rules: Dict[str, StardewRule] = field(default_factory=dict)
    seed_rules: Dict[str, StardewRule] = field(default_factory=dict)
    cooking_rules: Dict[str, StardewRule] = field(default_factory=dict)
    crop_rules: Dict[str, StardewRule] = field(default_factory=dict)
    fish_rules: Dict[str, StardewRule] = field(default_factory=dict)
    museum_rules: Dict[str, StardewRule] = field(default_factory=dict)
    building_rules: Dict[str, StardewRule] = field(default_factory=dict)
    quest_rules: Dict[str, StardewRule] = field(default_factory=dict)
    festival_rules: Dict[str, StardewRule] = field(default_factory=dict)
    special_order_rules: Dict[str, StardewRule] = field(default_factory=dict)

    def __post_init__(self):
        self.fish_rules.update({fish.name: self.can_catch_fish(fish) for fish in all_fish})
        self.museum_rules.update({donation.name: self.can_find_museum_item(donation) for donation in all_museum_items})
        self.cooking_rules.update({recipe.meal: self.can_cook(recipe) for recipe in all_cooking_recipes})

        self.sapling_rules.update({
            "Apple Sapling": self.can_buy_sapling("Apple"),
            "Apricot Sapling": self.can_buy_sapling("Apricot"),
            "Cherry Sapling": self.can_buy_sapling("Cherry"),
            "Orange Sapling": self.can_buy_sapling("Orange"),
            "Peach Sapling": self.can_buy_sapling("Peach"),
            "Pomegranate Sapling": self.can_buy_sapling("Pomegranate"),
            "Banana Sapling": self.can_buy_sapling("Banana"),
            "Mango Sapling": self.can_buy_sapling("Mango"),
        })

        for sapling in self.sapling_rules:
            existing_rules = self.sapling_rules[sapling]
            self.sapling_rules[sapling] = self.received(sapling) | existing_rules

        self.tree_fruit_rules.update({
            "Apple": self.can_plant_and_grow_item(Season.fall),
            "Apricot": self.can_plant_and_grow_item(Season.spring),
            "Cherry": self.can_plant_and_grow_item(Season.spring),
            "Orange": self.can_plant_and_grow_item(Season.summer),
            "Peach": self.can_plant_and_grow_item(Season.summer),
            "Pomegranate": self.can_plant_and_grow_item(Season.fall),
            "Banana": self.can_plant_and_grow_item(Season.summer),
            "Mango": self.can_plant_and_grow_item(Season.summer),
        })

        for tree_fruit in self.tree_fruit_rules:
            existing_rules = self.tree_fruit_rules[tree_fruit]
            sapling = f"{tree_fruit} Sapling"
            self.tree_fruit_rules[tree_fruit] = self.has(sapling) & self.has_lived_months(1) & existing_rules

        self.seed_rules.update({seed.name: self.can_buy_seed(seed) for seed in all_purchasable_seeds})
        self.crop_rules.update({crop.name: self.can_grow_crop(crop) for crop in all_crops})
        self.crop_rules.update({
            "Coffee Bean": (self.has_season(Season.spring) | self.has_season(Season.summer)) & self.has_traveling_merchant(),
            "Ancient Fruit": (self.received("Ancient Seeds") | self.received("Ancient Seeds Recipe")) &
                             self.can_reach_region(Region.greenhouse) & self.has("Seed Maker"),
        })

        self.item_rules.update({
            "Aged Roe": self.has(Machine.preserves_jar) & self.has("Roe"),
            "Algae Soup": self.can_cook() & self.has("Green Algae") & self.has_relationship(NPC.clint, 3),
            AnimalProduct.any_egg: self.has("Chicken Egg") | self.has("Duck Egg"),
            "Artichoke Dip": self.can_cook() & self.has_season(Season.fall) & self.has("Artichoke") & self.has("Cow Milk"),
            Geode.artifact_trove: self.has(Geode.omni) & self.can_reach_region(Region.desert),
            "Bait": self.has_skill_level(Skill.fishing, 2),
            "Baked Fish": self.has("Sunfish") & self.has("Bream") & self.has(Ingredient.wheat_flour),
            "Basic Fertilizer": (self.has(Item.sap) & self.has_farming_level(1)) | self.has_lived_months(1),
            "Bat Wing": self.can_mine_in_the_mines_floor_41_80() | self.can_mine_in_the_skull_cavern(),
            "Battery Pack": (self.has(Machine.lightning_rod) & self.has_any_season_not_winter()) | self.has(Machine.solar_panel),
            "Bean Hotpot": self.can_cook() & self.has_relationship(NPC.clint, 7) & self.has("Green Bean"),
            "Bee House": self.has_farming_level(3) & self.has(MetalBar.iron) & self.has("Maple Syrup") &
                         self.has(Item.coal) & self.has(Item.wood),
            "Beer": self.can_keg(Crop.wheat) | self.can_spend_money_at(Region.saloon, 400),
            "Blackberry": self.has_season(Season.fall),
            "Blackberry Cobbler": self.can_cook() & self.has_season(Season.fall) & self.has_year_two() &
                                  self.has("Blackberry") & self.has(Ingredient.sugar) & self.has(Ingredient.wheat_flour),
            "Bomb": self.has_skill_level(Skill.mining, 6) & self.has(Item.coal) & self.has(Ore.iron),
            "Bone Fragment": self.can_reach_region("Dig Site"),
            "Bouquet": self.has_relationship(Generic.bachelor, 8),
            Meal.bread: self.can_spend_money_at(Region.saloon, 120),
            "Broken CD": self.can_crab_pot(),
            "Broken Glasses": self.can_crab_pot(),
            "Bug Meat": self.can_mine_in_the_mines_floor_1_40(),
            "Cactus Fruit": self.can_reach_region(Region.desert),
            Machine.cask: self.has_house(3) & self.can_reach_region(Region.cellar) & self.has(Item.wood) & self.has(Item.hardwood),
            "Cave Carrot": self.can_mine_to_floor(10),
            "Caviar": self.has(Machine.preserves_jar) & self.has("Sturgeon Roe"),
            "Chanterelle": self.has_season(Season.fall) & self.can_reach_region(Region.secret_woods),
            Machine.cheese_press: self.has_farming_level(6) & self.has(Item.wood) & self.has(Item.stone) &
                                  self.has(Item.hardwood) & self.has(MetalBar.copper),
            "Cheese": (self.has("Cow Milk") & self.has(Machine.cheese_press)) |
                      (self.can_reach_region(Region.desert) & self.has("Emerald")),
            "Cheese Cauliflower": self.has(["Cheese", "Cauliflower"]) & self.has_relationship(NPC.pam, 3) &
                                  self.can_cook(),
            "Cherry Bomb": self.has_skill_level(Skill.mining, 1) & self.has(Item.coal) & self.has(Ore.copper),
            "Chicken": self.has_building(Building.coop),
            "Chicken Egg": self.has(["Egg", "Egg (Brown)", "Large Egg", "Large Egg (Brown)"], 1),
            "Chocolate Cake": self.can_cook() & self.has_season(Season.winter) & self.has(Ingredient.wheat_flour) & self.has(
                Ingredient.sugar) & self.has(AnimalProduct.any_egg),
            "Chowder": self.can_cook() & self.has_relationship(NPC.willy, 3) & self.has(["Clam", "Cow Milk"]),
            "Clam": True_(),
            "Clay": True_(),
            "Cloth": (self.has("Wool") & self.has("Loom")) |
                     (self.can_reach_region(Region.desert) & self.has("Aquamarine")),
            Item.coal: self.can_mine_in_the_mines_floor_41_80() | self.can_do_panning(),
            "Cockle": True_(),
            "Coconut": self.can_reach_region(Region.desert),
            "Coffee": (self.has(Machine.keg) & self.has("Coffee Bean")) | self.has("Coffee Maker") |
                      (self.can_spend_money(300) & self.can_reach_region(Region.saloon)) | self.has("Hot Java Ring"),
            "Coffee Maker": self.received("Coffee Maker"),
            "Common Mushroom": self.has_season(Season.fall) |
                               (self.has_season(Season.spring) & self.can_reach_region(Region.secret_woods)),
            "Complete Breakfast": self.can_cook() & self.has_season(Season.spring) & self.has_lived_months(4) &
                                  self.has("Fried Egg") & self.has("Cow Milk") & self.has("Hashbrowns") | self.has(
                "Pancakes"),
            MetalBar.copper: self.can_smelt(Ore.copper),
            Ore.copper: self.can_mine_in_the_mines_floor_1_40() | self.can_mine_in_the_skull_cavern() | self.can_do_panning(),
            "Coral": self.can_reach_region(Region.tide_pools) | self.has_season(Season.summer),
            "Cow": self.has_building(Building.barn),
            "Cow Milk": self.has("Milk") | self.has("Large Milk"),
            "Crab": self.can_crab_pot(),
            "Crab Cakes": self.can_mine_in_the_skull_cavern() |
                          (self.can_cook() & self.has_season(Season.fall) & self.has_year_two() & self.has("Crab") &
                           self.has(Ingredient.wheat_flour) & self.has("Chicken Egg") & self.has(Ingredient.oil)),
            "Crab Pot": self.has_skill_level(Skill.fishing, 3),
            "Cranberry Candy": self.can_cook() & self.has_season(Season.winter) & self.has("Cranberries") &
                               self.has("Apple") & self.has(Ingredient.sugar),
            "Crayfish": self.can_crab_pot(),
            "Crispy Bass": self.can_cook() & self.has_relationship(NPC.kent, 3) & self.has("Largemouth Bass") &
                           self.has(Ingredient.wheat_flour) & self.has(Ingredient.oil),
            "Crocus": self.has_season(Season.winter),
            "Crystal Fruit": self.has_season(Season.winter),
            "Daffodil": self.has_season(Season.spring),
            "Dandelion": self.has_season(Season.spring),
            "Deluxe Fertilizer": False_(), # self.received("Deluxe Fertilizer Recipe") & self.has("Iridium Bar") & self.has(SVItem.sap),
            "Dinosaur": self.has_building(Building.big_coop) & self.has("Dinosaur Egg"),
            "Dish O' The Sea": self.can_cook() & self.has_skill_level(Skill.fishing, 3) &
                               self.has(["Sardine", "Hashbrowns"]),
            "Dorado": self.can_fish(78) & self.has_season(Season.summer),
            "Dragon Tooth": self.can_reach_region(Region.volcano_floor_10),
            "Dried Starfish": self.can_fish() & self.can_reach_region(Region.beach),
            "Driftwood": self.can_crab_pot(),
            "Duck Egg": self.has_animal("Duck"),
            "Duck Feather": self.has_animal("Duck"),
            "Duck": self.has_building(Building.big_coop),
            "Egg": self.has_animal("Chicken"),
            "Egg (Brown)": self.has_animal("Chicken"),
            "Eggplant Parmesan": self.can_cook() & self.has_relationship(NPC.lewis, 7) & self.has("Eggplant") & self.has(
                "Tomato"),
            "Energy Tonic": self.can_reach_region(Region.hospital) & self.can_spend_money(1000),
            "Escargot": self.can_cook() & self.has_relationship(NPC.willy, 5) & self.has("Snail") & self.has(Crop.garlic),
            "Farmer's Lunch": self.can_cook() & self.has_farming_level(3) & self.has("Omelet") & self.has(
                Crop.parsnip),
            Item.fiber: True_(),
            Forageable.fiddlehead_fern: self.can_reach_region(Region.secret_woods) & self.has_season(Season.summer),
            "Fishing Chest": self.can_fish_chests(),
            "Fish Taco": self.can_cook() & self.has_relationship(NPC.linus, 7) & self.has("Tuna") & self.has("Tortilla") &
                         self.has("Red Cabbage") & self.has("Mayonnaise"),
            "Flute Block": self.has_relationship(NPC.robin, 6),
            "Fried Calamari": self.can_cook() & self.has_relationship(NPC.jodi, 3) & self.has("Squid") &
                              self.has(Ingredient.wheat_flour) & self.has(Ingredient.oil),
            "Fried Eel": self.can_cook() & self.has_relationship(NPC.george, 3) & self.has("Eel") & self.has(Ingredient.oil),
            "Fried Egg": self.can_cook() & self.has(AnimalProduct.any_egg),
            "Fried Mushroom": self.can_cook() & self.has_relationship(NPC.demetrius, 3) & self.has(
                "Morel") & self.has("Common Mushroom"),
            Geode.frozen: self.can_mine_in_the_mines_floor_41_80(),
            "Fruit Salad": self.can_cook() & self.has_season(Season.fall) & self.has_year_two() & self.has("Blueberry") &
                           self.has("Melon") & self.has("Apricot"),
            "Furnace": self.has(Item.stone) & self.has(Ore.copper),
            Geode.geode: self.can_mine_in_the_mines_floor_1_40(),
            "Ginger": self.can_reach_region(Region.island_west),
            "Ginger Ale": self.can_cook() & self.has("Ginger") & self.has(Ingredient.sugar),
            "Glazed Yams": self.can_cook() & self.has_season(Season.fall) & self.has("Yam") & self.has(Ingredient.sugar),
            "Goat Cheese": self.has("Goat Milk") & self.has(Machine.cheese_press),
            "Goat Milk": self.has("Goat"),
            "Goat": self.has_building(Building.big_barn),
            MetalBar.gold: self.can_smelt(Ore.gold),
            Ore.gold: self.can_mine_in_the_mines_floor_81_120() | self.can_mine_in_the_skull_cavern() | self.can_do_panning(),
            "Golden Pumpkin": self.has_season(Season.fall) | self.has(Geode.artifact_trove),
            "Green Algae": self.can_fish(),
            "Green Tea": self.has(Machine.keg) & self.has("Tea Leaves"),
            Item.hardwood: self.has_tool(Tool.axe, Material.copper) & self.can_reach_region(Region.secret_woods),
            "Hashbrowns": self.can_cook() & self.can_spend_money(50) & self.has("Potato"),
            "Hazelnut": self.has_season(Season.fall),
            "Holly": self.has_season(Season.winter),
            "Honey": self.can_reach_region(Region.desert) |
                     (self.has("Bee House") &
                      (self.has_season(Season.spring) | self.has_season(Season.summer) | self.has_season(Season.fall))),
            "Hot Java Ring": self.can_reach_region(Region.volcano_floor_10),
            "Ice Cream": (self.has_season(Season.summer) & self.can_reach_region(Region.town)) | self.can_reach_region(
                Region.desert),
            # | (self.can_cook() & self.has_relationship(NPC.jodi, 7) & self.has("Cow Milk") & self.has(Ingredient.sugar)),
            "Iridium Bar": self.can_smelt(Ore.iridium),
            Ore.iridium: self.can_mine_in_the_skull_cavern(),
            MetalBar.iron: self.can_smelt(Ore.iron),
            Ore.iron: self.can_mine_in_the_mines_floor_41_80() | self.can_mine_in_the_skull_cavern() | self.can_do_panning(),
            "Jelly": self.has(Machine.preserves_jar),
            "Joja Cola": self.can_reach_region(Region.saloon) & self.can_spend_money(75),
            "JotPK Small Buff": self.has_jotpk_power_level(2),
            "JotPK Medium Buff": self.has_jotpk_power_level(4),
            "JotPK Big Buff": self.has_jotpk_power_level(7),
            "JotPK Max Buff": self.has_jotpk_power_level(9),
            "Juice": self.has(Machine.keg),
            "Junimo Kart Small Buff": self.has_junimo_kart_power_level(2),
            "Junimo Kart Medium Buff": self.has_junimo_kart_power_level(4),
            "Junimo Kart Big Buff": self.has_junimo_kart_power_level(6),
            "Junimo Kart Max Buff": self.has_junimo_kart_power_level(8),
            Machine.keg: self.has_farming_level(8) & self.has(MetalBar.iron) & self.has(MetalBar.copper) & self.has(
                "Oak Resin"),
            "Large Egg": self.has_animal("Chicken"),
            "Large Egg (Brown)": self.has_animal("Chicken"),
            "Large Goat Milk": self.has("Goat"),
            "Large Milk": self.has_animal("Cow"),
            "Leek": self.has_season(Season.spring),
            "Life Elixir": self.has_skill_level(Skill.combat, 2) & self.has("Red Mushroom") & self.has("Purple Mushroom")
                           & self.has("Morel") & self.has("Chanterelle"),
            Machine.lightning_rod: self.has_skill_level(Skill.foraging, 6),
            "Lobster": self.can_crab_pot(),
            "Loom": self.has_farming_level(7) & self.has("Pine Tar") & self.has(Item.wood) & self.has(Item.fiber),
            "Magic Rock Candy": self.can_reach_region(Region.desert) & self.has("Prismatic Shard"),
            "Magma Cap": self.can_reach_region(Region.volcano_floor_5),
            Geode.magma: self.can_mine_in_the_mines_floor_81_120() |
                           (self.has("Lava Eel") & self.has_building(Building.fish_pond)),
            "Maki Roll": self.can_cook() & self.can_fish(),
            "Maple Bar": self.can_cook() & self.has_season(Season.summer) & self.has_year_two() & self.has("Maple Syrup") &
                         self.has(Ingredient.sugar) & self.has(Ingredient.wheat_flour),
            "Maple Syrup": self.has("Tapper"),
            "Mayonnaise": self.has("Mayonnaise Machine") & self.has("Chicken Egg"),
            "Mayonnaise Machine": self.has_farming_level(2) & self.has(Item.wood) & self.has(Item.stone) &
                                  self.has("Earth Crystal") & self.has(MetalBar.copper),
            "Mead": self.has(Machine.keg) & self.has("Honey"),
            "Mega Bomb": self.has_skill_level(Skill.mining, 8) & self.has(Item.coal) & self.has(Ore.gold),
            "Milk": self.has_animal("Cow"),
            "Miner's Treat": self.can_cook() & self.has_skill_level(Skill.mining, 3) & self.has("Cow Milk") & self.has(
                "Cave Carrot"),
            "Morel": self.can_reach_region(Region.secret_woods),
            "Muscle Remedy": self.can_reach_region(Region.hospital) & self.can_spend_money(1000),
            "Mussel": self.can_reach_region(Region.beach) or self.has("Mussel Node"),
            "Mussel Node": self.can_reach_region(Region.island_west),
            "Nautilus Shell": self.has_season(Season.winter),
            "Oak Resin": self.has("Tapper"),
            Ingredient.oil: True_(),
            "Oil Maker": self.has_farming_level(8) & self.has(Item.hardwood) & self.has(MetalBar.gold),
            "Omelet": self.can_cook() & self.can_spend_money(100) & self.has(AnimalProduct.any_egg) & self.has("Cow Milk"),
            Geode.omni: self.can_mine_in_the_mines_floor_41_80() |
                          self.can_reach_region(Region.desert) |
                          self.can_do_panning() |
                          self.received("Rusty Key") |
                          (self.has("Octopus") & self.has_building(Building.fish_pond)) |
                          self.can_reach_region(Region.volcano_floor_10),
            "Ostrich": self.has_building(Building.barn) & self.has("Ostrich Egg"),
            "Ostrich Egg": self.can_reach_region(Region.island_north),
            "Oyster": True_(),
            "Pale Ale": self.has(Machine.keg) & self.has("Hops"),
            "Pale Broth": self.can_cook() & self.has_relationship(NPC.marnie, 3) & self.has("White Algae"),
            "Pancakes": self.can_cook() & self.can_spend_money(100) & self.has(AnimalProduct.any_egg),
            "Parsnip Soup": self.can_cook() & self.has_relationship(NPC.caroline, 3) & self.has(
                Crop.parsnip) & self.has("Cow Milk"),
            "Pearl": (self.has("Blobfish") & self.has_building(Building.fish_pond)) |
                     (self.has_lived_months(4) & self.has(Geode.artifact_trove)),
            "Pepper Poppers": self.can_cook() & self.has("Cheese") & self.has(
                "Hot Pepper") & self.has_relationship(NPC.shane, 3),
            "Periwinkle": self.can_crab_pot(),
            "Pickles": self.has(Machine.preserves_jar),
            "Pig": self.has_building(Building.deluxe_barn),
            "Piña Colada": self.received("Island Resort") & self.can_reach_region("Island South"),
            "Pine Tar": self.has("Tapper"),
            "Pink Cake": self.can_cook() & self.has_season(Season.summer) & self.has("Melon") & self.has(
                Ingredient.wheat_flour) & self.has(Ingredient.sugar) & self.has(AnimalProduct.any_egg),
            "Pizza": self.can_spend_money(600),
            "Plum Pudding": self.can_cook() & self.has_season(Season.winter) & self.has("Wild Plum") &
                            self.has(Ingredient.wheat_flour) & self.has(Ingredient.sugar),
            "Poppyseed Muffin": self.can_cook() & self.has_season(Season.winter) & self.has_year_two() &
                                self.has("Poppy") & self.has(Ingredient.wheat_flour) & self.has(Ingredient.sugar),
            Machine.preserves_jar: self.has_farming_level(4),
            "Pumpkin Pie": self.can_cook() & self.has_season(Season.winter) & self.has(Ingredient.wheat_flour) &
                           self.has("Cow Milk") & self.has(Ingredient.sugar),
            "Purple Mushroom": self.can_mine_in_the_mines_floor_81_120() | self.can_mine_in_the_skull_cavern(),
            "Quality Fertilizer": (self.has(Item.sap) & self.can_crab_pot() & self.has_farming_level(9)) | self.has_lived_months(4),
            "Rabbit": self.has_building(Building.deluxe_coop),
            "Rabbit's Foot": self.has_animal("Rabbit"),
            "Radioactive Bar": self.can_smelt("Radioactive Ore"),
            "Radioactive Ore": self.can_mine_perfectly() & self.can_reach_region(Region.qi_walnut_room),
            "Rainbow Shell": self.has_season(Season.summer),
            "Rain Totem": self.has_skill_level(Skill.foraging, 9),
            "Recycling Machine": self.has_skill_level(Skill.fishing, 4) & self.has(Item.wood) &
                                 self.has(Item.stone) & self.has(MetalBar.iron),
            "Red Mushroom": self.can_reach_region(Region.secret_woods) & (
                    self.has_season(Season.summer) | self.has_season(Season.fall)),
            "Red Plate": self.can_cook() & self.has(["Radish", "Red Cabbage"]) & self.has_relationship(NPC.emily, 7),
            "Refined Quartz": self.can_smelt("Quartz") | self.can_smelt("Fire Quartz") |
                              (self.has("Recycling Machine") & (self.has("Broken CD") | self.has("Broken Glasses"))),
            "Rhubarb Pie": self.can_cook() & self.has_relationship(NPC.marnie, 7) & self.has("Rhubarb") &
                           self.has(Ingredient.wheat_flour) & self.has(Ingredient.sugar),
            "Rice": True_(),
            "Rice Pudding": self.can_cook() & self.has_relationship(NPC.evelyn, 7) & self.has("Cow Milk") &
                            self.has(Ingredient.sugar) & self.has("Rice"),
            "Roe": self.can_fish() & self.has_building(Building.fish_pond),
            "Roots Platter": self.can_cook() & self.has_skill_level(Skill.combat, 3) &
                             self.has("Cave Carrot") & self.has("Winter Root"),
            "Roasted Hazelnuts": self.can_cook() & self.has_season(Season.summer) & self.has("Hazelnut"),
            "Salad": self.can_spend_money(220),
            # | (self.can_cook() & self.has_relationship(NPC.emily, 3) & self.has("Leek") & self.has("Dandelion") &
            # self.has("Vinegar")),
            "Salmonberry": self.has_season(Season.spring),
            "Salmon Dinner": self.can_cook() & self.has_relationship(NPC.gus, 3) & self.has("Salmon") & self.has(
                "Amaranth") & self.has("Kale"),
            Item.sap: self.can_chop_trees(),
            "Sashimi": self.can_fish() & self.can_cook() & self.has_relationship(NPC.linus, 3),
            "Sea Urchin": self.can_reach_region(Region.tide_pools) | self.has_season(Season.summer),
            "Seaweed": self.can_fish() | self.can_reach_region(Region.tide_pools),
            "Secret Note": self.received("Magnifying Glass"),
            "Seed Maker": self.has_farming_level(9) & self.has(Item.wood) & self.has(MetalBar.gold) & self.has(Item.coal),
            "Sheep": self.has_building(Building.deluxe_barn),
            "Shrimp": self.can_crab_pot(),
            "Slime": self.can_mine_in_the_mines_floor_1_40(),
            "Slingshot": self.received("Slingshot") | self.received("Master Slingshot"),
            "Snail": self.can_crab_pot(),
            "Snow Yam": self.has_season(Season.winter),
            "Soggy Newspaper": self.can_crab_pot(),
            "Solar Essence": self.can_mine_in_the_mines_floor_41_80() | self.can_mine_in_the_skull_cavern(),
            Machine.solar_panel: self.received("Solar Panel Recipe") & self.has(MetalBar.quartz) & self.has(MetalBar.iron) & self.has(MetalBar.gold),
            "Spaghetti": self.can_spend_money(240),
            "Spice Berry": self.has_season(Season.summer),
            "Spring Onion": self.has_season(Season.spring),
            "Squid Ink": self.can_mine_in_the_mines_floor_81_120() | (
                    self.has_building(Building.fish_pond) & self.has("Squid")),
            "Staircase": self.has_skill_level(Skill.mining, 2),
            "Stir Fry": self.can_cook() & self.has_season(Season.spring) & self.has("Cave Carrot") &
                        self.has("Common Mushroom") & self.has("Kale") & self.has(Ingredient.oil),
            Item.stone: self.has_tool(Tool.pickaxe),
            "Stuffing": self.has_season(Season.winter) |
                        (self.can_cook() & self.has_relationship(NPC.pam, 7) & self.has(Meal.bread) &
                         self.has("Cranberries") & self.has("Hazelnut")),
            "Sturgeon Roe": self.has("Sturgeon") & self.has_building(Building.fish_pond),
            Ingredient.sugar: True_(),
            "Survival Burger": self.can_cook() & self.has_skill_level(Skill.foraging, 2) &
                               self.has([Meal.bread, "Cave Carrot", "Eggplant"]),
            "Sweet Pea": self.has_season(Season.summer),
            "Tapper": self.has_skill_level(Skill.foraging, 3) & self.has(Item.wood) & self.has(MetalBar.copper),
            "Tea Bush": self.has_relationship(NPC.caroline, 2),
            "Tea Leaves": self.has_lived_months(1) & self.has("Tea Bush"),
            "Tortilla": self.can_cook() & self.can_spend_money(100) & self.has("Corn"),
            "Trash": self.can_crab_pot(),
            "Triple Shot Espresso": (self.has("Hot Java Ring") |
                                     (self.can_cook() & self.can_spend_money(5000) & self.has("Coffee"))),
            "Tropical Curry": self.received("Island Resort") & self.can_reach_region(Region.island_south) &
                              self.can_cook() & self.has("Coconut") &
                              self.has("Pineapple") & self.has("Hot Pepper"),
            "Truffle Oil": self.has("Truffle") & self.has("Oil Maker"),
            "Truffle": self.has_animal("Pig") & self.has_spring_summer_or_fall(),
            "Vegetable Medley": self.can_cook() & self.has_relationship(NPC.caroline, 7) & self.has("Tomato") & self.has(
                "Beet"),
            "Vinegar": True_(),
            "Void Egg": self.can_meet(NPC.krobus) | (self.has_building(Building.fish_pond) & self.has("Void Salmon")),
            "Void Essence": self.can_mine_in_the_mines_floor_81_120() | self.can_mine_in_the_skull_cavern(),
            "Void Mayonnaise": self.has("Mayonnaise Machine") & self.has("Void Egg"),
            Ingredient.wheat_flour: self.can_spend_money_at(Region.pierre_store, 100) |
                                    (self.has_building(Building.mill) & self.has(Crop.wheat)),
            "White Algae": self.can_fish() & self.can_mine_in_the_mines_floor_1_40(),
            "Wild Horseradish": self.has_season(Season.spring),
            "Wild Plum": self.has_season(Season.fall),
            "Wilted Bouquet": self.has("Furnace") & self.has("Bouquet") & self.has(Item.coal),
            "Wine": self.has(Machine.keg),
            "Winter Root": self.has_season(Season.winter),
            Item.wood: self.has_tool(Tool.axe),
            "Wool": self.has_animal("Rabbit") | self.has_animal("Sheep"),
            "Hay": self.has_building(Building.silo),
        })
        self.item_rules.update(self.fish_rules)
        self.item_rules.update(self.museum_rules)
        self.item_rules.update(self.sapling_rules)
        self.item_rules.update(self.tree_fruit_rules)
        self.item_rules.update(self.seed_rules)
        self.item_rules.update(self.crop_rules)

        # For some recipes, the cooked item can be obtained directly, so we either cook it or get it
        for recipe in self.cooking_rules:
            cooking_rule = self.cooking_rules[recipe]
            obtention_rule = self.item_rules[recipe] if recipe in self.item_rules else False_()
            self.item_rules[recipe] = obtention_rule | cooking_rule

        self.building_rules.update({
            Building.barn: self.can_spend_money(6000) & self.has([Item.wood, Item.stone]),
            Building.big_barn: self.can_spend_money(12000) & self.has([Item.wood, Item.stone]) & self.has_building(Building.barn),
            Building.deluxe_barn: self.can_spend_money(25000) & self.has([Item.wood, Item.stone]) & self.has_building(Building.big_barn),
            Building.coop: self.can_spend_money(4000) & self.has([Item.wood, Item.stone]),
            Building.big_coop: self.can_spend_money(10000) & self.has([Item.wood, Item.stone]) & self.has_building(Building.coop),
            Building.deluxe_coop: self.can_spend_money(20000) & self.has([Item.wood, Item.stone]) & self.has_building(Building.big_coop),
            Building.fish_pond: self.can_spend_money(5000) & self.has([Item.stone, "Seaweed", "Green Algae"]),
            Building.mill: self.can_spend_money(2500) & self.has([Item.stone, Item.wood, "Cloth"]),
            Building.shed: self.can_spend_money(15000) & self.has(Item.wood),
            Building.big_shed: self.can_spend_money(20000) & self.has([Item.wood, Item.stone]) & self.has_building(Building.shed),
            Building.silo: self.can_spend_money(100) & self.has([Item.stone, "Clay", MetalBar.copper]),
            Building.slime_hutch: self.can_spend_money(10000) & self.has([Item.stone, "Refined Quartz", MetalBar.iridium]),
            Building.stable: self.can_spend_money(10000) & self.has([Item.hardwood, MetalBar.iron]),
            Building.well: self.can_spend_money(1000) & self.has(Item.stone),
            Building.shipping_bin: self.can_spend_money(250) & self.has(Item.wood),
            Building.kitchen: self.can_spend_money(10000) & self.has(Item.wood) & self.has_house(0),
            Building.kids_room: self.can_spend_money(50000) & self.has(Item.hardwood) & self.has_house(1),
            Building.cellar: self.can_spend_money(100000) & self.has_house(2),
        })

        self.quest_rules.update({
            Quest.introductions: True_(),
            Quest.how_to_win_friends: self.can_complete_quest(Quest.introductions),
            Quest.getting_started: self.has(Crop.parsnip) & self.has_tool(Tool.hoe) & self.can_water(0),
            Quest.to_the_beach: True_(),
            Quest.raising_animals: self.can_complete_quest(Quest.getting_started) & self.has_building(Building.coop),
            Quest.advancement: self.can_complete_quest(Quest.getting_started) & self.has_farming_level(1),
            Quest.archaeology: self.has_tool(Tool.hoe) | self.can_mine_in_the_mines_floor_1_40() | self.can_fish(),
            Quest.meet_the_wizard: True_() & self.can_reach_region(Region.community_center),
            Quest.forging_ahead: self.has(Ore.copper) & self.has("Furnace"),
            Quest.smelting: self.has(MetalBar.copper),
            Quest.initiation: self.can_mine_in_the_mines_floor_1_40(),
            Quest.robins_lost_axe: self.has_season(Season.spring),
            Quest.jodis_request: self.has_season(Season.spring) & self.has("Cauliflower"),
            Quest.mayors_shorts: self.has_season(Season.summer) & (self.has_relationship(NPC.marnie, 2) |
                                                                    (self.can_blink() & self.can_earn_spells())),
            Quest.blackberry_basket: self.has_season(Season.fall),
            Quest.marnies_request: self.has_relationship(NPC.marnie, 3) & self.has("Cave Carrot"),
            Quest.pam_is_thirsty: self.has_season(Season.summer) & self.has("Pale Ale"),
            Quest.a_dark_reagent: self.has_season(Season.winter) & self.has("Void Essence"),
            Quest.cows_delight: self.has_season(Season.fall) & self.has("Amaranth"),
            Quest.the_skull_key: self.received("Skull Key") & self.can_reach_region(Region.desert),
            Quest.crop_research: self.has_season(Season.summer) & self.has("Melon"),
            Quest.knee_therapy: self.has_season(Season.summer) & self.has("Hot Pepper"),
            Quest.robins_request: self.has_season(Season.winter) & self.has(Item.hardwood),
            Quest.qis_challenge: self.can_mine_in_the_skull_cavern(),
            Quest.the_mysterious_qi: self.has("Battery Pack") & self.can_reach_region(Region.desert) & self.has(
                "Rainbow Shell") & self.has("Beet") & self.has("Solar Essence"),
            Quest.carving_pumpkins: self.has_season(Season.fall) & self.has("Pumpkin"),
            Quest.a_winter_mystery: self.has_season(Season.winter),
            Quest.strange_note: self.received("Magnifying Glass") & self.can_reach_region(Region.secret_woods) & self.has(
                "Maple Syrup"),
            Quest.cryptic_note: self.received("Magnifying Glass") & self.can_reach_region(Region.skull_cavern_100),
            Quest.fresh_fruit: self.has("Apricot"),
            Quest.aquatic_research: self.has("Pufferfish"),
            Quest.a_soldiers_star: self.has_relationship(NPC.kent) & self.has("Starfruit"),
            Quest.mayors_need: self.has("Truffle Oil"),
            Quest.wanted_lobster: self.has_season(Season.fall) & self.has("Lobster"),
            Quest.pam_needs_juice: self.has("Battery Pack"),
            Quest.fish_casserole: self.has_relationship(NPC.jodi, 4) & self.has("Largemouth Bass"),
            Quest.catch_a_squid: self.has("Squid"),
            Quest.fish_stew: self.has("Albacore"),
            Quest.pierres_notice: self.has("Sashimi"),
            Quest.clints_attempt: self.has("Amethyst"),
            Quest.a_favor_for_clint: self.has(MetalBar.iron),
            Quest.staff_of_power: self.has(MetalBar.iridium),
            Quest.grannys_gift: self.has("Leek"),
            Quest.exotic_spirits: self.has("Coconut"),
            Quest.catch_a_lingcod: self.has("Lingcod"),
            Quest.the_pirates_wife: self.can_reach_region(Region.island_west) & self.can_meet(NPC.kent) &
                                 self.can_meet(NPC.gus) & self.can_meet(NPC.sandy) & self.can_meet(NPC.george) &
                                 self.can_meet(NPC.wizard) & self.can_meet(NPC.willy),
        })

        self.festival_rules.update({
            "Egg Hunt Victory": self.has_season(Season.spring) & self.can_reach_region(
                Region.town) & self.can_win_egg_hunt(),
            "Egg Festival: Strawberry Seeds": self.has_season(Season.spring) & self.can_reach_region(
                Region.town) & self.can_spend_money(1000),
            "Dance with someone": self.has_season(Season.spring) & self.can_reach_region(
                Region.forest) & self.has_relationship(Generic.bachelor, 4),
            "Rarecrow #5 (Woman)": self.has_season(Season.spring) & self.can_reach_region(
                Region.forest) & self.can_spend_money(2500),
            "Luau Soup": self.has_season(Season.summer) & self.can_reach_region(
                Region.beach) & self.can_succeed_luau_soup(),
            "Dance of the Moonlight Jellies": self.has_season(Season.summer) & self.can_reach_region(Region.beach),
            "Smashing Stone": self.has_season(Season.fall) & self.can_reach_region(Region.town),
            "Grange Display": self.has_season(Season.fall) & self.can_reach_region(
                Region.town) & self.can_succeed_grange_display(),
            "Rarecrow #1 (Turnip Head)": self.has_season(Season.fall) & self.can_reach_region(Region.town),
            # only cost star tokens
            "Fair Stardrop": self.has_season(Season.fall) & self.can_reach_region(Region.town),  # only cost star tokens
            "Spirit's Eve Maze": self.has_season(Season.fall) & self.can_reach_region(Region.town),
            "Rarecrow #2 (Witch)": self.has_season(Season.fall) & self.can_reach_region(
                Region.town) & self.can_spend_money(5000),
            "Win Fishing Competition": self.has_season(Season.winter) & self.can_reach_region(
                Region.forest) & self.can_win_fishing_competition(),
            "Rarecrow #4 (Snowman)": self.has_season(Season.winter) & self.can_reach_region(
                Region.forest) & self.can_spend_money(5000),
            "Mermaid Pearl": self.has_season(Season.winter) & self.can_reach_region(Region.beach),
            "Cone Hat": self.has_season(Season.winter) & self.can_reach_region(Region.beach) & self.can_spend_money(2500),
            "Iridium Fireplace": self.has_season(Season.winter) & self.can_reach_region(
                Region.beach) & self.can_spend_money(15000),
            "Rarecrow #7 (Tanuki)": self.has_season(Season.winter) & self.can_reach_region(
                Region.beach) & self.can_spend_money(5000) & self.can_find_museum_artifacts(20),
            "Rarecrow #8 (Tribal Mask)": self.has_season(Season.winter) & self.can_reach_region(
                Region.beach) & self.can_spend_money(5000) & self.can_find_museum_items(40),
            "Lupini: Red Eagle": self.has_season(Season.winter) & self.can_reach_region(
                Region.beach) & self.can_spend_money(1200),
            "Lupini: Portrait Of A Mermaid": self.has_season(Season.winter) & self.can_reach_region(
                Region.beach) & self.can_spend_money(1200),
            "Lupini: Solar Kingdom": self.has_season(Season.winter) & self.can_reach_region(
                Region.beach) & self.can_spend_money(1200),
            "Lupini: Clouds": self.has_season(Season.winter) & self.can_reach_region(
                Region.beach) & self.has_year_two() & self.can_spend_money(1200),
            "Lupini: 1000 Years From Now": self.has_season(Season.winter) & self.can_reach_region(
                Region.beach) & self.has_year_two() & self.can_spend_money(1200),
            "Lupini: Three Trees": self.has_season(Season.winter) & self.can_reach_region(
                Region.beach) & self.has_year_two() & self.can_spend_money(1200),
            "Lupini: The Serpent": self.has_season(Season.winter) & self.can_reach_region(
                Region.beach) & self.has_year_three() & self.can_spend_money(1200),
            "Lupini: 'Tropical Fish #173'": self.has_season(Season.winter) & self.can_reach_region(
                Region.beach) & self.has_year_three() & self.can_spend_money(1200),
            "Lupini: Land Of Clay": self.has_season(Season.winter) & self.can_reach_region(
                Region.beach) & self.has_year_three() & self.can_spend_money(1200),
            "Secret Santa": self.has_season(Season.winter) & self.can_reach_region(
                Region.town) & self.has_any_universal_love(),
        })

        self.special_order_rules.update({
            "Island Ingredients": self.can_reach_region(Region.island_west) & self.can_farm_perfectly() &
                                  self.has("Taro Root") & self.has("Pineapple") & self.has("Ginger"),
            "Cave Patrol": self.can_mine_perfectly() & self.can_mine_to_floor(120),
            "Aquatic Overpopulation": self.can_fish_perfectly(),
            "Biome Balance": self.can_fish_perfectly(),
            "Rock Rejuvenation": self.has("Ruby") & self.has("Topaz") & self.has("Emerald") &
                                 self.has("Jade") & self.has("Amethyst") & self.has_relationship(NPC.emily, 4) &
                                 self.has("Cloth") & self.can_reach_region(Region.haley_house),
            "Gifts for George": self.has_season(Season.spring) & self.has("Leek"),
            "Fragments of the past": self.can_reach_region("Dig Site"),
            "Gus' Famous Omelet": self.has(AnimalProduct.any_egg),
            "Crop Order": self.can_farm_perfectly(),
            "Community Cleanup": self.can_crab_pot(),
            "The Strong Stuff": self.can_keg("Potato"),
            "Pierre's Prime Produce": self.can_farm_perfectly(),
            "Robin's Project": self.can_chop_perfectly() & self.has(Item.hardwood),
            "Robin's Resource Rush": self.can_chop_perfectly() & self.can_mine_perfectly(),
            "Juicy Bugs Wanted!": self.has("Bug Meat"),
            "Tropical Fish": self.has("Stingray") & self.has("Blue Discus") & self.has("Lionfish"),
            "A Curious Substance": self.can_mine_perfectly() & self.can_mine_to_floor(80),
            "Prismatic Jelly": self.can_mine_perfectly() & self.can_mine_to_floor(40),
            "Qi's Crop": self.can_farm_perfectly() & self.can_reach_region(Region.greenhouse) &
                         self.can_reach_region(Region.island_west) & self.has_total_skill_level(50) &
                         self.has("Seed Maker"),
            "Let's Play A Game": self.has_junimo_kart_max_level(),
            "Four Precious Stones": self.has_lived_months(MAX_MONTHS) & self.has("Prismatic Shard") &
                                    self.can_mine_perfectly_in_the_skull_cavern(),
            "Qi's Hungry Challenge": self.can_mine_perfectly_in_the_skull_cavern() & self.has_max_buffs(),
            "Qi's Cuisine": self.can_cook() & self.can_spend_money(250000),
            "Qi's Kindness": self.can_give_loved_gifts_to_everyone(),
            "Extended Family": self.can_fish_perfectly() & self.has("Angler") & self.has("Glacierfish") &
                               self.has("Crimsonfish") & self.has("Mutant Carp") & self.has("Legend"),
            "Danger In The Deep": self.can_mine_perfectly() & self.has_mine_elevator_to_floor(120),
            "Skull Cavern Invasion": self.can_mine_perfectly_in_the_skull_cavern() & self.has_max_buffs(),
            "Qi's Prismatic Grange": self.has("Bug Meat") & self.can_spend_money(80000), # All colors can be bought except purple
        })

        # Mod Building List (For now smh)
        if ModNames.tractor in self.options[options.Mods]:
            self.building_rules.update({
                "Tractor Garage": self.can_spend_money(150000) & self.has(MetalBar.iron) &
                                  self.has(MetalBar.iridium) & self.has("Battery Pack")})

    def has(self, items: Union[str, (Iterable[str], Sized)], count: Optional[int] = None) -> StardewRule:
        if isinstance(items, str):
            return Has(items, self.item_rules)

        if len(items) == 0:
            return True_()

        if count is None or count == len(items):
            return And(self.has(item) for item in items)

        if count == 1:
            return Or(self.has(item) for item in items)

        return Count(count, (self.has(item) for item in items))

    def received(self, items: Union[str, Iterable[str]], count: Optional[int] = 1) -> StardewRule:
        if count <= 0 or not items:
            return True_()

        if isinstance(items, str):
            return Received(items, self.player, count)

        if count is None:
            return And(self.received(item) for item in items)

        if count == 1:
            return Or(self.received(item) for item in items)

        return TotalReceived(count, items, self.player)

    def can_reach_region(self, spot: str) -> StardewRule:
        return Reach(spot, "Region", self.player)

    def can_reach_any_region(self, spots: Iterable[str]) -> StardewRule:
        return Or(self.can_reach_region(spot) for spot in spots)

    def can_reach_all_regions(self, spots: Iterable[str]) -> StardewRule:
        return And(self.can_reach_region(spot) for spot in spots)

    def can_reach_all_regions_except_one(self, spots: Iterable[str]) -> StardewRule:
        num_required = len(list(spots)) - 1
        if num_required <= 0:
            num_required = len(list(spots))
        return Count(num_required, [self.can_reach_region(spot) for spot in spots])

    def can_reach_location(self, spot: str) -> StardewRule:
        return Reach(spot, "Location", self.player)

    def can_reach_entrance(self, spot: str) -> StardewRule:
        return Reach(spot, "Entrance", self.player)

    def can_have_earned_total_money(self, amount: int) -> StardewRule:
        return self.has_lived_months(min(8, amount // MONEY_PER_MONTH))

    def can_spend_money(self, amount: int) -> StardewRule:
        if self.options[options.StartingMoney] == -1:
            return True_()
        return self.has_lived_months(min(8, amount // (MONEY_PER_MONTH // 5)))

    def can_spend_money_at(self, region: str, amount: int) -> StardewRule:
        return self.can_reach_region(region) & self.can_spend_money(amount)

    def has_tool(self, tool: str, material: str = Material.basic) -> StardewRule:
        if material == Material.basic:
            return True_()

        if self.options[options.ToolProgression] == options.ToolProgression.option_progressive:
            return self.received(f"Progressive {tool}", count=tool_materials[material])

        return self.has(f"{material} Bar") & self.can_spend_money(tool_prices[material])

    def can_earn_skill_level(self, skill: str, level: int) -> StardewRule:
        if level == 0:
            return True_()

        tool_rule = True_()
        if skill == Skill.fishing:
            tool_rule = self.can_get_fishing_xp()
        if skill == Skill.farming and level >= 6:
            tool_rule = self.has_tool(Tool.hoe, Material.iron) & self.can_water(2)
        if skill == Skill.foraging and level >= 6:
            tool_rule = self.has_tool(Tool.axe, Material.iron) | self.can_use_clear_debris_instead_of_tool_level(3)
        if skill == Skill.mining and level >= 6:
            tool_rule = self.has_tool(Tool.pickaxe, Material.iron) | self.can_use_clear_debris_instead_of_tool_level(3)
        if skill == Skill.combat:
            if level >= 6:
                tool_rule = self.can_do_combat_at_level("Good")
            else:
                tool_rule = self.can_do_combat_at_level("Basic")
        tool_rule = can_earn_mod_skill_level(self, skill, level, tool_rule)

        months = max(1, level - 1)
        return self.has_lived_months(months) & tool_rule

    def has_skill_level(self, skill: str, level: int) -> StardewRule:
        if level == 0:
            return True_()

        if self.options[options.SkillProgression] == options.SkillProgression.option_progressive:
            return self.received(f"{skill} Level", count=level)

        return self.can_earn_skill_level(skill, level)

    def has_farming_level(self, level: int) -> StardewRule:
        return self.has_skill_level(Skill.farming, level)

    def has_total_skill_level(self, level: int, allow_modded_skills: bool = False) -> StardewRule:
        if level == 0:
            return True_()

        if self.options[options.SkillProgression] == options.SkillProgression.option_progressive:
            skills_items = ["Farming Level", "Mining Level", "Foraging Level",
                            "Fishing Level", "Combat Level"]
            if allow_modded_skills:
                append_mod_skill_level(skills_items, self.options)
            return self.received(skills_items, count=level)

        months_5_skills = max(1, (level // 5) - 1)
        months_4_skills = max(1, (level // 5) - 1)
        rule_with_fishing = self.has_lived_months(months_5_skills) & self.can_get_fishing_xp()
        if level > 40:
            return rule_with_fishing
        return self.has_lived_months(months_4_skills) | rule_with_fishing

    def has_building(self, building: str) -> StardewRule:
        carpenter_rule = self.can_reach_region(Region.carpenter)
        if not self.options[options.BuildingProgression] == options.BuildingProgression.option_vanilla:
            count = 1
            if building in [Building.coop, Building.barn, Building.shed]:
                building = f"Progressive {building}"
            elif building.startswith("Big"):
                count = 2
                building = " ".join(["Progressive", *building.split(" ")[1:]])
            elif building.startswith("Deluxe"):
                count = 3
                building = " ".join(["Progressive", *building.split(" ")[1:]])
            return self.received(f"{building}", count) & carpenter_rule

        return Has(building, self.building_rules) & carpenter_rule

    def has_house(self, upgrade_level: int) -> StardewRule:
        if upgrade_level < 1:
            return True_()

        if upgrade_level > 3:
            return False_()

        if not self.options[options.BuildingProgression] == options.BuildingProgression.option_vanilla:
            return self.received(f"Progressive House", upgrade_level)

        if upgrade_level == 1:
            return Has(Building.kitchen, self.building_rules)

        if upgrade_level == 2:
            return Has(Building.kids_room, self.building_rules)

        # if upgrade_level == 3:
        return Has(Building.cellar, self.building_rules)

    def can_complete_quest(self, quest: str) -> StardewRule:
        return Has(quest, self.quest_rules)

    def can_get_fishing_xp(self) -> StardewRule:
        if self.options[options.SkillProgression] == options.SkillProgression.option_progressive:
            return self.can_fish() | self.can_crab_pot()

        return self.can_fish()

    def can_fish(self, difficulty: int = 0) -> StardewRule:
        skill_required = max(0, int((difficulty / 10) - 1))
        if difficulty <= 40:
            skill_required = 0
        skill_rule = self.has_skill_level(Skill.fishing, skill_required)
        number_fishing_rod_required = 1 if difficulty < 50 else 2
        if self.options[options.ToolProgression] == options.ToolProgression.option_progressive:
            return self.received("Progressive Fishing Rod", number_fishing_rod_required) & skill_rule

        return skill_rule

    def has_max_fishing(self) -> StardewRule:
        skill_rule = self.has_skill_level(Skill.fishing, 10)
        return self.has_max_fishing_rod() & skill_rule

    def can_fish_chests(self) -> StardewRule:
        skill_rule = self.has_skill_level(Skill.fishing, 4)
        return self.has_max_fishing_rod() & skill_rule

    def can_buy_seed(self, seed: SeedItem) -> StardewRule:
        if self.options[options.SeedShuffle] == options.SeedShuffle.option_disabled:
            item_rule = True_()
        else:
            item_rule = self.received(seed.name)
        season_rule = self.has_any_season(seed.seasons)
        region_rule = self.can_reach_all_regions(seed.regions)
        currency_rule = True_()
        if seed.name == "Pineapple Seeds":
            currency_rule = self.has("Magma Cap")
        if seed.name == "Taro Tuber":
            currency_rule = self.has("Bone Fragment")
        return season_rule & region_rule & item_rule & currency_rule

    def can_buy_sapling(self, fruit: str) -> StardewRule:
        sapling_prices = {"Apple": 4000, "Apricot": 2000, "Cherry": 3400, "Orange": 4000, "Peach": 6000,
                          "Pomegranate": 6000, "Banana": 0, "Mango": 0}
        item_rule = self.received(f"{fruit} Sapling")
        if self.options[options.SeedShuffle] == options.SeedShuffle.option_disabled:
            item_rule = item_rule | self.can_spend_money(sapling_prices[fruit])
        if fruit == "Banana":
            access_rule = self.has_island_trader() & self.has("Dragon Tooth")
        elif fruit == "Mango":
            access_rule = self.has_island_trader() & self.has("Mussel Node")
        else:
            access_rule = self.can_reach_region(Region.pierre_store)
        return item_rule & access_rule

    def can_grow_crop(self, crop: CropItem) -> StardewRule:
        season_rule = self.has_any_season(crop.farm_growth_seasons)
        seed_rule = self.has(crop.seed.name)
        farm_rule = self.can_reach_region(Region.farm) & season_rule
        region_rule = farm_rule | self.can_reach_region(Region.greenhouse) | self.can_reach_region(Region.island_west)
        return seed_rule & region_rule

    def can_plant_and_grow_item(self, seasons: Union[str, Iterable[str]]) -> StardewRule:
        if isinstance(seasons, str):
            seasons = [seasons]
        season_rule = self.has_any_season(seasons) | self.can_reach_region(Region.greenhouse) | self.has_island_farm()
        farm_rule = self.can_reach_region(Region.farm) | self.can_reach_region(
            Region.greenhouse) | self.has_island_farm()
        return season_rule & farm_rule

    def has_island_farm(self) -> StardewRule:
        return self.can_reach_region(Region.island_south)

    def can_catch_fish(self, fish: FishItem) -> StardewRule:
        region_rule = self.can_reach_any_region(fish.locations)
        season_rule = self.has_any_season(fish.seasons)
        difficulty_rule = self.can_fish(fish.difficulty)
        if fish.difficulty == -1:
            difficulty_rule = self.can_crab_pot()
        return region_rule & season_rule & difficulty_rule

    def can_catch_every_fish(self) -> StardewRule:
        rules = [self.has_skill_level(Skill.fishing, 10), self.has_max_fishing_rod()]
        for fish in all_fish:
            if self.options[options.ExcludeGingerIsland] == options.ExcludeGingerIsland.option_true and\
                    fish in island_fish:
                continue
            rules.append(self.can_catch_fish(fish))
        return And(rules)

    def has_max_fishing_rod(self) -> StardewRule:
        if self.options[options.ToolProgression] == options.ToolProgression.option_progressive:
            return self.received("Progressive Fishing Rod", 4)
        return self.can_get_fishing_xp()

    def can_cook(self, recipe: CookingRecipe = None) -> StardewRule:
        cook_rule = self.has_house(1) | self.has_skill_level(Skill.foraging, 9)
        if recipe is None:
            return cook_rule

        learn_rule = self.can_learn_recipe(recipe.source)
        ingredients_rule = And([self.has(ingredient) for ingredient in recipe.ingredients])
        return cook_rule & learn_rule & ingredients_rule

    def can_learn_recipe(self, source: RecipeSource) -> StardewRule:
        if isinstance(source, FriendshipSource):
            return self.has_relationship(source.friend, source.hearts)
        if isinstance(source, QueenOfSauceSource):
            year_rule = self.has_year_two() if source.year == 2 else self.has_year_three()
            return self.can_watch(Channel.queen_of_sauce) & self.has_season(source.season) & year_rule

        return False_()

    def can_watch(self, channel: str = None):
        tv_rule = True_()
        if channel is None:
            return tv_rule
        return self.received(channel) & tv_rule

    def can_smelt(self, item: str) -> StardewRule:
        return self.has("Furnace") & self.has(item)

    def can_do_panning(self, item: str = Generic.any) -> StardewRule:
        return self.received("Glittering Boulder Removed")

    def can_crab_pot(self) -> StardewRule:
        if self.options[options.SkillProgression] == options.SkillProgression.option_progressive:
            return self.has("Crab Pot")

        return True_()

    # Regions
    def can_mine_in_the_mines_floor_1_40(self) -> StardewRule:
        return self.can_reach_region(Region.mines_floor_5)

    def can_mine_in_the_mines_floor_41_80(self) -> StardewRule:
        return self.can_reach_region(Region.mines_floor_45)

    def can_mine_in_the_mines_floor_81_120(self) -> StardewRule:
        return self.can_reach_region(Region.mines_floor_85)

    def can_mine_in_the_skull_cavern(self) -> StardewRule:
        return (self.can_progress_in_the_mines_from_floor(120) &
                self.can_reach_region(Region.skull_cavern))

    def can_mine_perfectly(self) -> StardewRule:
        return self.can_progress_in_the_mines_from_floor(160)

    def can_mine_perfectly_in_the_skull_cavern(self) -> StardewRule:
        return (self.can_mine_perfectly() &
                self.can_reach_region(Region.skull_cavern))

    def can_farm_perfectly(self) -> StardewRule:
        tool_rule = self.has_tool(Tool.hoe, Material.iridium) & self.can_water(4)
        return tool_rule & self.has_farming_level(10)

    def can_fish_perfectly(self) -> StardewRule:
        skill_rule = self.has_skill_level(Skill.fishing, 10)
        return skill_rule & self.has_max_fishing_rod()

    def can_chop_trees(self) -> StardewRule:
        return self.has_tool(Tool.axe) & self.can_reach_region(Region.forest)

    def can_chop_perfectly(self) -> StardewRule:
        magic_rule = (self.can_use_clear_debris_instead_of_tool_level(3)) & self.has_skill_level("Magic", 10)
        tool_rule = self.has_tool(Tool.axe, Material.iridium)
        foraging_rule = self.has_skill_level(Skill.foraging, 10)
        region_rule = self.can_reach_region(Region.forest)
        return region_rule & ((tool_rule & foraging_rule) | magic_rule)

    def has_max_buffs(self) -> StardewRule:
        num_buffs: int = self.options[options.NumberOfPlayerBuffs]
        return self.received("Movement Speed Bonus", num_buffs) & self.received("Luck Bonus", num_buffs)

    def get_weapon_rule_for_floor_tier(self, tier: int):
        if tier >= 4:
            return self.can_do_combat_at_level("Galaxy")
        if tier >= 3:
            return self.can_do_combat_at_level("Great")
        if tier >= 2:
            return self.can_do_combat_at_level("Good")
        if tier >= 1:
            return self.can_do_combat_at_level("Decent")
        return self.can_do_combat_at_level("Basic")

    def can_progress_in_the_mines_from_floor(self, floor: int) -> StardewRule:
        tier = int(floor / 40)
        rules = []
        weapon_rule = self.get_weapon_rule_for_floor_tier(tier)
        rules.append(weapon_rule)
        if self.options[options.ToolProgression] == options.ToolProgression.option_progressive:
            rules.append(self.received("Progressive Pickaxe", tier))
        if self.options[options.SkillProgression] == options.SkillProgression.option_progressive:
            combat_tier = min(10, max(0, tier * 2))
            rules.append(self.has_skill_level(Skill.combat, combat_tier))
        return And(rules)

    def can_progress_easily_in_the_mines_from_floor(self, floor: int) -> StardewRule:
        tier = int(floor / 40) + 1
        rules = []
        weapon_rule = self.get_weapon_rule_for_floor_tier(tier)
        rules.append(weapon_rule)
        if self.options[options.ToolProgression] == options.ToolProgression.option_progressive:
            rules.append(self.received("Progressive Pickaxe", count=tier))
        if self.options[options.SkillProgression] == options.SkillProgression.option_progressive:
            combat_tier = min(10, max(0, tier * 2))
            rules.append(self.has_skill_level(Skill.combat, combat_tier))
        return And(rules)

    def has_mine_elevator_to_floor(self, floor: int) -> StardewRule:
        if (self.options[options.TheMinesElevatorsProgression] ==
                options.TheMinesElevatorsProgression.option_progressive or
                self.options[options.TheMinesElevatorsProgression] ==
                options.TheMinesElevatorsProgression.option_progressive_from_previous_floor):
            return self.received("Progressive Mine Elevator", count=int(floor / 5))
        return True_()

    def can_mine_to_floor(self, floor: int) -> StardewRule:
        previous_elevator = max(floor - 5, 0)
        previous_previous_elevator = max(floor - 10, 0)
        return ((self.has_mine_elevator_to_floor(previous_elevator) &
                 self.can_progress_in_the_mines_from_floor(previous_elevator)) |
                (self.has_mine_elevator_to_floor(previous_previous_elevator) &
                 self.can_progress_easily_in_the_mines_from_floor(previous_previous_elevator)))

    def has_jotpk_power_level(self, power_level: int) -> StardewRule:
        if self.options[options.ArcadeMachineLocations] != options.ArcadeMachineLocations.option_full_shuffling:
            return True_()
        jotpk_buffs = ["JotPK: Progressive Boots", "JotPK: Progressive Gun",
                       "JotPK: Progressive Ammo", "JotPK: Extra Life", "JotPK: Increased Drop Rate"]
        return self.received(jotpk_buffs, power_level)

    def has_junimo_kart_power_level(self, power_level: int) -> StardewRule:
        if self.options[options.ArcadeMachineLocations] != options.ArcadeMachineLocations.option_full_shuffling:
            return True_()
        return self.received("Junimo Kart: Extra Life", power_level)

    def has_junimo_kart_max_level(self) -> StardewRule:
        play_rule = self.can_reach_region(Region.junimo_kart_3)
        if self.options[options.ArcadeMachineLocations] != options.ArcadeMachineLocations.option_full_shuffling:
            return play_rule
        return self.has_junimo_kart_power_level(8)

    def has_traveling_merchant(self, tier: int = 1):
        traveling_merchant_days = [f"Traveling Merchant: {day}" for day in week_days]
        return self.received(traveling_merchant_days, tier)

    def can_get_married(self) -> StardewRule:
        return self.can_reach_region(Region.tide_pools) & self.has_relationship(Generic.bachelor, 10) & self.has_house(1)

    def can_have_two_children(self) -> StardewRule:
        return self.can_get_married() & self.has_house(2) & self.has_relationship(Generic.bachelor, 12)

    def has_relationship(self, npc: str, hearts: int = 1) -> StardewRule:
        if hearts <= 0:
            return True_()
        if self.options[options.Friendsanity] == options.Friendsanity.option_none:
            return self.can_earn_relationship(npc, hearts)
        if npc not in all_villagers_by_name:
            if npc == "Pet":
                if self.options[options.Friendsanity] == options.Friendsanity.option_bachelors:
                    return self.can_befriend_pet(hearts)
                return self.received_hearts("Pet", hearts)
            if npc == Generic.any or npc == Generic.bachelor:
                possible_friends = []
                for name in all_villagers_by_name:
                    if not self.npc_is_in_current_slot(name):
                        continue
                    if npc == Generic.any or all_villagers_by_name[name].bachelor:
                        possible_friends.append(self.has_relationship(name, hearts))
                return Or(possible_friends)
            if npc == Generic.all:
                mandatory_friends = []
                for name in all_villagers_by_name:
                    if not self.npc_is_in_current_slot(name):
                        continue
                    mandatory_friends.append(self.has_relationship(name, hearts))
                return And(mandatory_friends)
            if npc.isnumeric():
                possible_friends = []
                for name in all_villagers_by_name:
                    if not self.npc_is_in_current_slot(name):
                        continue
                    possible_friends.append(self.has_relationship(name, hearts))
                return Count(int(npc), possible_friends)
            return self.can_earn_relationship(npc, hearts)

        if not self.npc_is_in_current_slot(npc):
            return True_()
        villager = all_villagers_by_name[npc]
        if self.options[options.Friendsanity] == options.Friendsanity.option_bachelors and not villager.bachelor:
            return self.can_earn_relationship(npc, hearts)
        if self.options[options.Friendsanity] == options.Friendsanity.option_starting_npcs and not villager.available:
            return self.can_earn_relationship(npc, hearts)
        if self.options[options.Friendsanity] != options.Friendsanity.option_all_with_marriage and villager.bachelor and hearts > 8:
            return self.received_hearts(villager, 8) & self.can_earn_relationship(npc, hearts)
        return self.received_hearts(villager, hearts)

    def received_hearts(self, npc: Union[str, Villager], hearts: int) -> StardewRule:
        if isinstance(npc, Villager):
            return self.received_hearts(npc.name, hearts)
        heart_size: int = self.options[options.FriendsanityHeartSize]
        return self.received(self.heart(npc), math.ceil(hearts / heart_size))

    def can_meet(self, npc: str) -> StardewRule:
        if npc not in all_villagers_by_name or not self.npc_is_in_current_slot(npc):
            return True_()
        villager = all_villagers_by_name[npc]
        rules = [self.can_reach_any_region(villager.locations)]
        if npc == NPC.kent:
            rules.append(self.has_lived_months(4))
        if npc == "Dwarf":
            rules.append(self.received("Dwarvish Translation Guide"))
            rules.append(self.has_tool(Tool.pickaxe, Material.iron))

        return And(rules)

    def can_give_loved_gifts_to_everyone(self) -> StardewRule:
        rules = []
        for npc in all_villagers_by_name:
            if not self.npc_is_in_current_slot(npc):
                continue
            villager = all_villagers_by_name[npc]
            rules.append(self.can_meet(npc) & self.has(villager.gifts))
        return And(rules)

    def can_earn_relationship(self, npc: str, hearts: int = 0) -> StardewRule:
        if npc == "Pet":
            return self.can_befriend_pet(hearts)
        if npc == NPC.wizard and ModNames.magic in self.options[options.Mods]:
            return self.can_meet(npc) & self.has_lived_months(hearts)
        if npc in all_villagers_by_name:
            if not self.npc_is_in_current_slot(npc):
                return True_()
            villager = all_villagers_by_name[npc]
            option1 = self.has_season(villager.birthday) & self.has(villager.gifts) & self.has_lived_months(1)
            option2 = self.has_season(villager.birthday) & self.has(villager.gifts, 1) & self.has_lived_months(
                hearts // 3)
            option3 = (self.has_season(villager.birthday) | self.has(villager.gifts, 1)) & self.has_lived_months(
                hearts // 2)
            option4 = self.has_lived_months(hearts)
            return self.can_meet(npc) & (option1 | option2 | option3 | option4)
        else:
            return self.has_lived_months(min(hearts // 2, 8))

    def can_befriend_pet(self, hearts: int):
        if hearts == 0:
            return True_()
        points = hearts * 200
        points_per_month = 12 * 14
        points_per_water_month = 18 * 14
        return self.can_reach_region(Region.farm) & \
               ((self.can_water(0) & self.has_lived_months(points // points_per_water_month)) |
                self.has_lived_months(points // points_per_month))

    def can_complete_bundle(self, bundle_requirements: List[BundleItem], number_required: int) -> StardewRule:
        item_rules = []
        highest_quality_yet = 0
        for bundle_item in bundle_requirements:
            if bundle_item.item.item_id == -1:
                return self.can_spend_money(bundle_item.amount)
            else:
                item_rules.append(bundle_item.item.name)
                if bundle_item.quality > highest_quality_yet:
                    highest_quality_yet = bundle_item.quality
        return self.has(item_rules, number_required) & self.can_grow_gold_quality(highest_quality_yet)

    def can_grow_gold_quality(self, quality: int) -> StardewRule:
        if quality <= 0:
            return True_()
        if quality == 1:
            return self.has_farming_level(5) | (self.has_fertilizer(1) & self.has_farming_level(2)) | (self.has_fertilizer(2) & self.has_farming_level(1)) | self.has_fertilizer(3)
        if quality == 2:
            return self.has_farming_level(10) | (self.has_fertilizer(1) & self.has_farming_level(5)) | (self.has_fertilizer(2) & self.has_farming_level(3)) | (self.has_fertilizer(3) & self.has_farming_level(2))
        if quality >= 3:
            return self.has_fertilizer(3) & self.has_farming_level(4)

    def has_fertilizer(self, tier: int) -> StardewRule:
        if tier <= 0:
            return True_()
        if tier == 1:
            return self.has("Basic Fertilizer")
        if tier == 2:
            return self.has("Quality Fertilizer")
        if tier >= 3:
            return self.has("Deluxe Fertilizer")

    def can_complete_community_center(self) -> StardewRule:
        return (self.can_reach_location("Complete Crafts Room") &
                self.can_reach_location("Complete Pantry") &
                self.can_reach_location("Complete Fish Tank") &
                self.can_reach_location("Complete Bulletin Board") &
                self.can_reach_location("Complete Vault") &
                self.can_reach_location("Complete Boiler Room"))

    def can_finish_grandpa_evaluation(self) -> StardewRule:
        # https://stardewvalleywiki.com/Grandpa
        rules_worth_a_point = [self.can_have_earned_total_money(50000),  # 50 000g
                               self.can_have_earned_total_money(100000),  # 100 000g
                               self.can_have_earned_total_money(200000),  # 200 000g
                               self.can_have_earned_total_money(300000),  # 300 000g
                               self.can_have_earned_total_money(500000),  # 500 000g
                               self.can_have_earned_total_money(1000000),  # 1 000 000g first point
                               self.can_have_earned_total_money(1000000),  # 1 000 000g second point
                               self.has_total_skill_level(30),  # Total Skills: 30
                               self.has_total_skill_level(50),  # Total Skills: 50
                               # Completing the museum not expected
                               # Catching every fish not expected
                               # Shipping every item not expected
                               self.can_get_married() & self.has_house(2),
                               self.has_relationship("5", 8),  # 5 Friends
                               self.has_relationship("10", 8),  # 10 friends
                               self.has_relationship(NPC.pet, 5),  # Max Pet
                               self.can_complete_community_center(),  # Community Center Completion
                               self.can_complete_community_center(),  # CC Ceremony first point
                               self.can_complete_community_center(),  # CC Ceremony second point
                               self.received("Skull Key"),  # Skull Key obtained
                               self.has_rusty_key(),  # Rusty key not expected
                               ]
        return Count(12, rules_worth_a_point)

    def has_any_weapon(self) -> StardewRule:
        return self.has_decent_weapon() | self.received(item.name for item in all_items if Group.WEAPON in item.groups)

    def has_decent_weapon(self) -> StardewRule:
        return (self.has_good_weapon() |
                self.received(item.name for item in all_items
                              if Group.WEAPON in item.groups and
                              (Group.MINES_FLOOR_50 in item.groups or Group.MINES_FLOOR_60 in item.groups)))

    def has_good_weapon(self) -> StardewRule:
        return ((self.has_great_weapon() |
                 self.received(item.name for item in all_items
                               if Group.WEAPON in item.groups and
                               (Group.MINES_FLOOR_80 in item.groups or Group.MINES_FLOOR_90 in item.groups))) &
                self.received("Adventurer's Guild"))

    def has_great_weapon(self) -> StardewRule:
        return ((self.has_galaxy_weapon() |
                 self.received(item.name for item in all_items
                               if Group.WEAPON in item.groups and Group.MINES_FLOOR_110 in item.groups)) &
                self.received("Adventurer's Guild"))

    def has_galaxy_weapon(self) -> StardewRule:
        return (self.received(item.name for item in all_items
                              if Group.WEAPON in item.groups and Group.GALAXY_WEAPONS in item.groups) &
                self.received("Adventurer's Guild"))

    def has_year_two(self) -> StardewRule:
        return self.has_lived_months(4)

    def has_year_three(self) -> StardewRule:
        return self.has_lived_months(8)

    def has_spring_summer_or_fall(self) -> StardewRule:
        return self.has_season(Season.spring) | self.has_season(Season.summer) | self.has_season(Season.fall)

    def can_find_museum_item(self, item: MuseumItem) -> StardewRule:
        region_rule = self.can_reach_all_regions_except_one(item.locations)
        geodes_rule = And([self.can_open_geode(geode) for geode in item.geodes])
        # monster_rule = self.can_farm_monster(item.monsters)
        # extra_rule = True_()
        pan_rule = False_()
        if item.name == "Earth Crystal" or item.name == "Fire Quartz" or item.name == "Frozen Tear":
            pan_rule = self.can_do_panning()
        return pan_rule | (region_rule & geodes_rule)  # & monster_rule & extra_rule

    def can_find_museum_artifacts(self, number: int) -> StardewRule:
        rules = []
        for donation in all_museum_items:
            if donation in all_artifact_items:
                rules.append(self.can_find_museum_item(donation))

        return Count(number, rules)

    def can_find_museum_items(self, number: int) -> StardewRule:
        rules = []
        for donation in all_museum_items:
            rules.append(self.can_find_museum_item(donation))

        return Count(number, rules)

    def can_complete_museum(self) -> StardewRule:
        rules = [self.can_mine_perfectly()]

        if self.options[options.Museumsanity] != options.Museumsanity.option_none:
            rules.append(self.received("Traveling Merchant Metal Detector", 4))

        for donation in all_museum_items:
            rules.append(self.can_find_museum_item(donation))
        return And(rules)

    def has_season(self, season: str) -> StardewRule:
        seasons_order = [Season.spring, Season.summer, Season.fall, Season.winter]
        if self.options[options.SeasonRandomization] == options.SeasonRandomization.option_progressive:
            return self.received(Season.progressive, seasons_order.index(season))
        if self.options[options.SeasonRandomization] == options.SeasonRandomization.option_disabled:
            if season == Season.spring:
                return True_()
            return self.has_lived_months(1)
        return self.received(season)

    def has_any_season(self, seasons: Iterable[str]):
        if not seasons:
            return True_()
        return Or([self.has_season(season) for season in seasons])

    def has_any_season_not_winter(self):
        return self.has_any_season([Season.spring, Season.summer, Season.fall])

    def has_all_seasons(self, seasons: Iterable[str]):
        if not seasons:
            return True_()
        return And([self.has_season(season) for season in seasons])

    def has_lived_months(self, number: int) -> StardewRule:
        number = max(0, min(number, MAX_MONTHS))
        return self.received("Month End", number)

    def has_rusty_key(self) -> StardewRule:
        if self.options[options.Museumsanity] == options.Museumsanity.option_none:
            return True_()
        return self.received("Rusty Key")

    def can_win_egg_hunt(self) -> StardewRule:
        number_of_buffs: int = self.options[options.NumberOfPlayerBuffs]
        if self.options[options.FestivalLocations] == options.FestivalLocations.option_hard or number_of_buffs < 2:
            return True_()
        return self.received("Movement Speed Bonus", number_of_buffs // 2)

    def can_succeed_luau_soup(self) -> StardewRule:
        if self.options[options.FestivalLocations] != options.FestivalLocations.option_hard:
            return True_()
        eligible_fish = ["Blobfish", "Crimsonfish", "Ice Pip", "Lava Eel", "Legend", "Angler", "Catfish", "Glacierfish",
                         "Mutant Carp", "Spook Fish", "Stingray", "Sturgeon", "Super Cucumber"]
        fish_rule = [self.has(fish) for fish in eligible_fish]
        eligible_kegables = ["Ancient Fruit", "Apple", "Banana", "Coconut", "Crystal Fruit", "Mango", "Melon", "Orange",
                             "Peach", "Pineapple", "Pomegranate", "Rhubarb", "Starfruit", "Strawberry", "Cactus Fruit",
                             "Cherry", "Cranberries", "Grape", "Spice Berry", "Wild Plum", "Hops", Crop.wheat]
        keg_rules = [self.can_keg(kegable) for kegable in eligible_kegables]
        aged_rule = [self.can_age(rule, "Iridium") for rule in keg_rules]
        # There are a few other valid items but I don't feel like coding them all
        return Or(fish_rule) | Or(aged_rule)

    def can_succeed_grange_display(self) -> StardewRule:
        if self.options[options.FestivalLocations] != options.FestivalLocations.option_hard:
            return True_()
        animal_rule = self.has_animal(Generic.any)
        artisan_rule = self.can_keg(Generic.any) | self.can_jelly(Generic.any)
        cooking_rule = True_()  # Salads at the bar are good enough
        fish_rule = self.can_fish(50)
        forage_rule = True_()  # Hazelnut always available since the grange display is in fall
        mineral_rule = self.can_open_geode(Generic.any)  # More than half the minerals are good enough
        good_fruits = ["Apple", "Banana", "Coconut", "Crystal Fruit", "Mango", "Orange", "Peach", "Pomegranate",
                       "Strawberry", "Melon", "Rhubarb", "Pineapple", "Ancient Fruit", "Starfruit", ]
        fruit_rule = Or([self.has(fruit) for fruit in good_fruits])
        good_vegetables = ["Amaranth", "Artichoke", "Beet", "Cauliflower", Forageable.fiddlehead_fern, "Kale",
                           "Radish", "Taro Root", "Yam", "Red Cabbage", "Pumpkin"]
        vegetable_rule = Or([self.has(vegetable) for vegetable in good_vegetables])

        return animal_rule & artisan_rule & cooking_rule & fish_rule & \
               forage_rule & fruit_rule & mineral_rule & vegetable_rule

    def can_win_fishing_competition(self) -> StardewRule:
        return self.can_fish(60)

    def has_any_universal_love(self) -> StardewRule:
        return self.has("Golden Pumpkin") | self.has("Magic Rock Candy") | self.has("Pearl") | self.has(
            "Prismatic Shard") | self.has("Rabbit's Foot")

    def can_keg(self, item: str) -> StardewRule:
        keg_rule = self.has(Machine.keg)
        if item == Generic.any:
            return keg_rule
        return keg_rule & self.has(item)

    def can_jelly(self, item: str) -> StardewRule:
        jelly_rule = self.has(Machine.preserves_jar)
        if item == Generic.any:
            return jelly_rule
        return jelly_rule & self.has(item)

    def can_age(self, item: Union[str, StardewRule], quality: str) -> StardewRule:
        months = 1
        if quality == "Gold":
            months = 2
        elif quality == "Iridium":
            months = 3
        if isinstance(item, str):
            rule = self.has(item)
        else:
            rule: StardewRule = item
        return self.has(Machine.cask) & self.has_lived_months(months) & rule

    def has_animal(self, animal: str) -> StardewRule:
        if animal == Generic.any:
            return self.has_any_animal()
        elif animal == Building.coop:
            return self.has_any_coop_animal()
        elif animal == Building.barn:
            return self.has_any_barn_animal()
        return self.has(animal)

    def has_any_animal(self) -> StardewRule:
        return self.has_any_coop_animal() | self.has_any_barn_animal()

    def has_any_coop_animal(self) -> StardewRule:
        coop_animals = ["Chicken", "Rabbit", "Duck", "Dinosaur"]
        coop_rule = Or([self.has_animal(coop_animal) for coop_animal in coop_animals])
        return coop_rule

    def has_any_barn_animal(self) -> StardewRule:
        barn_animals = ["Cow", "Sheep", "Pig", "Ostrich"]
        barn_rule = Or([self.has_animal(barn_animal) for barn_animal in barn_animals])
        return barn_rule

    def can_open_geode(self, geode: str) -> StardewRule:
        blacksmith_access = self.can_reach_region("Clint's Blacksmith")
        geodes = [Geode.geode, Geode.frozen, Geode.magma, Geode.omni]
        if geode == Generic.any:
            return blacksmith_access & Or([self.has(geode_type) for geode_type in geodes])
        return blacksmith_access & self.has(geode)

    def has_island_trader(self) -> StardewRule:
        if self.options[options.ExcludeGingerIsland] == options.ExcludeGingerIsland.option_true:
            return False_()
        return self.can_reach_region(Region.island_trader)

    def has_walnut(self, number: int) -> StardewRule:
        if self.options[options.ExcludeGingerIsland] == options.ExcludeGingerIsland.option_true:
            return False_()
        if number <= 0:
            return True_()
        # https://stardewcommunitywiki.com/Golden_Walnut#Walnut_Locations
        reach_south = self.can_reach_region(Region.island_south)
        reach_north = self.can_reach_region(Region.island_north)
        reach_west = self.can_reach_region(Region.island_west)
        reach_hut = self.can_reach_region(Region.leo_hut)
        reach_southeast = self.can_reach_region(Region.island_south_east)
        reach_pirate_cove = self.can_reach_region(Region.pirate_cove)
        reach_outside_areas = And(reach_south, reach_north, reach_west, reach_hut)
        reach_volcano_regions = [self.can_reach_region(Region.volcano), self.can_reach_region(Region.volcano_secret_beach),
                                 self.can_reach_region(Region.volcano_floor_5), self.can_reach_region(Region.volcano_floor_10)]
        reach_volcano = Or(reach_volcano_regions)
        reach_all_volcano = And(reach_volcano_regions)
        reach_walnut_regions = [reach_south, reach_north, reach_west, reach_volcano]
        reach_caves = And(self.can_reach_region(Region.qi_walnut_room), self.can_reach_region(Region.dig_site),
                          self.can_reach_region(Region.gourmand_frog_cave), self.can_reach_region(Region.colored_crystals_cave),
                          self.can_reach_region(Region.shipwreck), self.has("Slingshot"))
        reach_entire_island = And(reach_outside_areas, reach_all_volcano,
                                  reach_caves, reach_southeast, reach_pirate_cove)
        if number <= 5:
            return Or(reach_south, reach_north, reach_west, reach_volcano)
        if number <= 10:
            return Count(2, reach_walnut_regions)
        if number <= 15:
            return Count(3, reach_walnut_regions)
        if number <= 20:
            return And(reach_walnut_regions)
        if number <= 50:
            return reach_entire_island
        gems = ["Amethyst", "Aquamarine", "Emerald", "Ruby", "Topaz"]
        return reach_entire_island & self.has("Banana") & self.has(gems) & self.can_mine_perfectly() & \
               self.can_fish_perfectly() & self.has("Flute Block")

    def has_everything(self, all_progression_items: Set[str]) -> StardewRule:
        all_regions = [region.name for region in vanilla_regions]
        rules = self.received(all_progression_items, len(all_progression_items)) &\
                self.can_reach_all_regions(all_regions)
        return rules

    def heart(self, npc: Union[str, Villager]) -> str:
        if isinstance(npc, str):
            return f"{npc} <3"
        return self.heart(npc.name)

        # Mod Logic definitions until I figure out how to weave this together...

    def can_earn_spell_count(self, spell_count: int):
        # Player always has an Axe, Pickaxe, and Watering Can, and starts with Magic Missile and Analyze
        spell_rules = [self.can_reach_region(Region.volcano_floor_10) | self.has_mine_elevator_to_floor(100),
                       self.can_reach_region(Region.farm),
                       self.can_reach_region(Region.witch_swamp),
                       self.has("Staircase"),
                       self.has("Coffee"),
                       self.has("Life Elixir"),
                       self.has("Earth Crystal"),
                       self.has("Fire Quartz"),
                       self.can_fish(85) & self.has_mine_elevator_to_floor(60) & self.can_reach_region(Region.mines)
                       ]
        # If the player can't even learn magic, you have no spells.
        if not (self.has_relationship(NPC.wizard, 3) & self.can_reach_region(Region.pierre_store) &
                self.can_reach_region(Region.wizard_tower)):
            return False_()
        return Count(spell_count, spell_rules)

    def can_reach_woods_depth(self, depth: int) -> StardewRule:
        rules = []
        if depth > 10:
            rules.append(self.has("Cherry Bomb") | self.has_tool(Tool.axe, Material.iridium))
        if depth > 30:
            rules.append(self.received("Woods Obelisk"))
        if depth > 50:
            rules.append(self.can_do_combat_at_level("Great") & self.can_cook())
        return And(rules)

    def npc_is_in_current_slot(self, name: str) -> bool:
        npc = all_villagers_by_name[name]
        mod = npc.mod_name
        return mod is None or mod in self.options[options.Mods]

# Spell Logic in terms of combat usability (similar to weapons)  Strategy is that if the mod doesn't exist, its
# always false and thus doesn't get considered relative to other logic tests.

    def can_earn_spells(self) -> StardewRule:
        return self.has_relationship(NPC.wizard, 3) & self.can_reach_region(Region.pierre_store) & \
               self.can_reach_region(Region.wizard_tower)

    def has_any_spell(self) -> StardewRule:
        if ModNames.magic not in self.options[options.Mods]:
            return False_()
        return self.can_earn_spells()

    def has_attack_spell_count(self, count: int) -> StardewRule:
        attack_spell_rule = [self.received("Spell: Fireball"), self.received(
            "Spell: Frostbite"), self.received("Spell: Shockwave"), self.received("Spell: Spirit"),
                             self.received("Spell: Meteor")
        ]
        return Count(count, attack_spell_rule)

    def has_support_spell_count(self, count: int) -> StardewRule:
        support_spell_rule = [self.can_earn_spells(), self.received("Magic Level", 2)
        ]
        return Count(count, support_spell_rule)

    def has_decent_spells(self) -> StardewRule:
        if ModNames.magic not in self.options[options.Mods]:
            return False_()
        magic_resource_rule = self.can_earn_spells() & self.received("Magic Level", 2)
        magic_attack_options_rule = self.has_attack_spell_count(1)
        return magic_resource_rule & magic_attack_options_rule

    def has_good_spells(self) -> StardewRule:
        if ModNames.magic not in self.options[options.Mods]:
            return False_()
        magic_resource_rule = self.can_earn_spells() & self.received("Magic Level", 4)
        magic_attack_options_rule = self.has_attack_spell_count(2)
        magic_support_options_rule = self.has_support_spell_count(1)
        return magic_resource_rule & magic_attack_options_rule & magic_support_options_rule

    def has_great_spells(self) -> StardewRule:
        if ModNames.magic not in self.options[options.Mods]:
            return False_()
        magic_resource_rule = self.can_earn_spells() & self.received("Magic Level", 6)
        magic_attack_options_rule = self.has_attack_spell_count(3)
        magic_support_options_rule = self.has_support_spell_count(1)
        return magic_resource_rule & magic_attack_options_rule & magic_support_options_rule

    def has_amazing_spells(self) -> StardewRule:
        if ModNames.magic not in self.options[options.Mods]:
            return False_()
        magic_resource_rule = self.can_earn_spells() & self.received("Magic Level", 8)
        magic_attack_options_rule = self.has_attack_spell_count(4)
        magic_support_options_rule = self.has_support_spell_count(2)
        return magic_resource_rule & magic_attack_options_rule & magic_support_options_rule

    def can_blink(self) -> StardewRule:
        if ModNames.magic not in self.options[options.Mods]:
            return False_()
        return self.received("Spell: Blink") & self.can_earn_spells()

    def can_do_combat_at_level(self, level: str) -> StardewRule:
        if level == "Basic":
            return self.has_any_weapon() | self.has_any_spell()
        if level == "Decent":
            return self.has_decent_weapon() | self.has_decent_spells()
        if level == "Good":
            return self.has_good_weapon() | self.has_good_spells()
        if level == "Great":
            return self.has_great_weapon() | self.has_great_spells()
        if level == "Galaxy":
            return self.has_galaxy_weapon() | self.has_amazing_spells()

    def can_water(self, level: int) -> StardewRule:
        watering_can_dict = {
            0: Material.basic,
            1: Material.copper,
            2: Material.iron,
            3: Material.gold,
            4: Material.iridium
        }
        return self.has_tool(Tool.watering_can, watering_can_dict[level]) | \
            (self.received("Spell: Water") & self.can_earn_spells() & self.has_skill_level("Magic", level))

    def can_use_clear_debris_instead_of_tool_level(self, level: int) -> StardewRule:
        if ModNames.magic not in self.options[options.Mods]:
            return False_()
        return self.received("Spell: Clear Debris") & self.can_earn_spells() & self.received("Magic Level", level)

