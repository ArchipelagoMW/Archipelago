from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Union, Optional, Iterable, Sized, Tuple, List

from . import options
from .data import all_fish, FishItem, all_purchasable_seeds, SeedItem, all_crops, CropItem
from .data.bundle_data import BundleItem
from .data.museum_data import all_museum_items, MuseumItem
from .data.region_data import SVRegion
from .data.villagers_data import all_villagers_by_name
from .items import all_items, Group
from .options import StardewOptions
from .stardew_rule import False_, Reach, Or, True_, Received, Count, And, Has, TotalReceived, StardewRule

MONEY_PER_MONTH = 15000
MISSING_ITEM = "THIS ITEM IS MISSING"

tool_materials = {
    "Copper": 1,
    "Iron": 2,
    "Gold": 3,
    "Iridium": 4
}

tool_prices = {
    "Copper": 2000,
    "Iron": 5000,
    "Gold": 10000,
    "Iridium": 25000
}

skill_level_per_month_end = {
    0: {
        "Farming": 2,
        "Fishing": 2,
        "Foraging": 2,
        "Mining": 2,
        "Combat": 2,
    },
    1: {
        "Farming": 4,
        "Fishing": 4,
        "Foraging": 4,
        "Mining": 4,
        "Combat": 3,
    },
    2: {
        "Farming": 7,
        "Fishing": 5,
        "Foraging": 5,
        "Mining": 5,
        "Combat": 4,
    },
    3: {
        "Farming": 7,
        "Fishing": 7,
        "Foraging": 6,
        "Mining": 7,
        "Combat": 5,
    },
    4: {
        "Farming": 10,
        "Fishing": 10,
        "Foraging": 10,
        "Mining": 10,
        "Combat": 10,
    },
}
month_end_per_skill_level: Dict[Tuple[str, int], int] = {}
month_end_per_total_level: Dict[int, int] = {}


def initialize_season_per_skill_level():
    current_level = {
        "Farming": 0,
        "Fishing": 0,
        "Foraging": 0,
        "Mining": 0,
        "Combat": 0,
    }
    for month_end, skills in skill_level_per_month_end.items():
        for skill, expected_level in skills.items():
            for level_up in range(current_level[skill] + 1, expected_level + 1):
                skill_level = (skill, level_up)
                if skill_level not in month_end_per_skill_level:
                    month_end_per_skill_level[skill_level] = month_end
        level_up = 0
        for level_up in range(level_up + 1, sum(skills.values()) + 1):
            if level_up not in month_end_per_total_level:
                month_end_per_total_level[level_up] = month_end


initialize_season_per_skill_level()
week_days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]


@dataclass(frozen=True, repr=False)
class StardewLogic:
    player: int
    options: StardewOptions

    item_rules: Dict[str, StardewRule] = field(default_factory=dict)
    tree_fruit_rules: Dict[str, StardewRule] = field(default_factory=dict)
    seed_rules: Dict[str, StardewRule] = field(default_factory=dict)
    crop_rules: Dict[str, StardewRule] = field(default_factory=dict)
    fish_rules: Dict[str, StardewRule] = field(default_factory=dict)
    museum_rules: Dict[str, StardewRule] = field(default_factory=dict)
    building_rules: Dict[str, StardewRule] = field(default_factory=dict)
    quest_rules: Dict[str, StardewRule] = field(default_factory=dict)

    def __post_init__(self):
        self.fish_rules.update({fish.name: self.can_catch_fish(fish) for fish in all_fish})
        self.museum_rules.update({donation.name: self.can_find_museum_item(donation) for donation in all_museum_items})

        self.tree_fruit_rules.update({
            "Apple": self.has_lived_months(1) & (self.has_season("Fall") | self.can_reach_region(SVRegion.greenhouse)),
            "Apricot": self.has_lived_months(1) & (self.has_season("Spring") | self.can_reach_region(SVRegion.greenhouse)),
            "Cherry": self.has_lived_months(1) & (self.has_season("Spring") | self.can_reach_region(SVRegion.greenhouse)),
            "Orange": self.has_lived_months(1) & (self.has_season("Summer") | self.can_reach_region(SVRegion.greenhouse)),
            "Peach": self.has_lived_months(1) & (self.has_season("Summer") | self.can_reach_region(SVRegion.greenhouse)),
            "Pomegranate": self.has_lived_months(1) & (self.has_season("Fall") | self.can_reach_region(SVRegion.greenhouse)),
            "Banana Sapling": self.can_reach_region(SVRegion.ginger_island),
            "Mango Sapling": self.can_reach_region(SVRegion.ginger_island),
            "Banana": self.has("Banana Sapling") & (self.has_season("Summer") | self.can_reach_region(SVRegion.greenhouse)),
            "Mango": self.has("Mango Sapling") & (self.has_season("Summer") | self.can_reach_region(SVRegion.greenhouse)),
        })

        self.seed_rules.update({seed.name: self.can_buy_seed(seed) for seed in all_purchasable_seeds})
        self.crop_rules.update({crop.name: self.can_grow_crop(crop) for crop in all_crops})
        self.crop_rules.update({
            "Coffee Bean": (self.has_season("Spring") | self.has_season("Summer")) & self.has_traveling_merchant(),
        })

        self.item_rules.update({
            "Aged Roe": self.has("Preserves Jar") & self.has("Roe"),
            "Algae Soup": self.can_cook() & self.has("Green Algae") & self.has_relationship("Clint", 3),
            "Any Egg": self.has("Chicken Egg") | self.has("Duck Egg"),
            "Artichoke Dip": self.can_cook() & self.has_season("Fall") & self.has("Artichoke") & self.has("Cow Milk"),
            "Artifact Trove": self.has("Omni Geode") & self.can_reach_region(SVRegion.desert),
            "Bait": self.has_skill_level("Fishing", 2),
            "Bat Wing": self.can_mine_in_the_mines_floor_41_80() | self.can_mine_in_the_skull_cavern(),
            "Battery Pack": self.has("Lightning Rod"),
            "Bean Hotpot": self.can_cook() & self.has_relationship("Clint", 7) & self.has("Green Bean"),
            "Bee House": self.has_skill_level("Farming", 3) & self.has("Iron Bar") & self.has("Maple Syrup"),
            "Beer": (self.has("Keg") & self.has("Wheat")) | self.can_spend_money(400),
            "Blackberry": self.has_season("Fall"),
            "Blackberry Cobbler": self.can_cook() & self.has_season("Fall") & self.has_year_two() &
                                  self.has("Blackberry") & self.has("Sugar") & self.has("Wheat Flour"),
            "Blueberry Tart": self.has("Blueberry") & self.has("Any Egg") & self.has_relationship("Pierre", 3),
            "Bouquet": self.has_relationship("Bachelor", 8),
            "Bread": self.can_spend_money(120) | (self.can_spend_money(100) & self.can_cook()),
            "Broken CD": self.can_crab_pot(),
            "Broken Glasses": self.can_crab_pot(),
            "Bug Meat": self.can_mine_in_the_mines_floor_1_40(),
            "Cactus Fruit": self.can_reach_region(SVRegion.desert),
            "Cave Carrot": self.can_mine_to_floor(10),
            "Caviar": self.has("Preserves Jar") & self.has("Sturgeon Roe"),
            "Chanterelle": self.has_season("Fall") & self.can_reach_region(SVRegion.secret_woods),
            "Cheese Press": self.has_skill_level("Farming", 6) & self.has("Hardwood") & self.has("Copper Bar"),
            "Cheese": (self.has("Cow Milk") & self.has("Cheese Press")) |
                      (self.can_reach_region(SVRegion.desert) & self.has("Emerald")),
            "Cheese Cauliflower": self.has(["Cheese", "Cauliflower"]) & self.has_relationship("Pam", 3) &
                                  self.can_cook(),
            "Chicken": self.has_building("Coop"),
            "Chicken Egg": self.has(["Egg", "Egg (Brown)", "Large Egg", "Large Egg (Brown)"], 1),
            "Chocolate Cake": self.can_cook() & self.has_season("Winter") & self.has("Wheat Flour") & self.has(
                "Sugar") & self.has("Any Egg"),
            "Chowder": self.can_cook() & self.has_relationship("Willy", 3) & self.has(["Clam", "Cow Milk"]),
            "Clam": True_(),
            "Clay": True_(),
            "Glazed Yams": self.can_cook() & self.has_season("Fall") & self.has("Yam") & self.has("Sugar"),
            "Cloth": (self.has("Wool") & self.has("Loom")) |
                     (self.can_reach_region(SVRegion.desert) & self.has("Aquamarine")),
            "Coal": True_(),
            "Cockle": True_(),
            "Coconut": self.can_reach_region(SVRegion.desert),
            "Coffee": (self.has("Keg") & self.has("Coffee Bean")) | self.has("Coffee Maker") |
                      self.can_spend_money(300) | self.has("Hot Java Ring"),
            "Coffee Maker": False_(),
            "Common Mushroom": self.has_season("Fall") |
                               (self.has_season("Spring") & self.can_reach_region(SVRegion.secret_woods)),
            "Complete Breakfast": self.can_cook() & self.has_season("Spring") & self.has_lived_months(4) &
                                  self.has("Fried Egg") & self.has("Cow Milk") & self.has("Hashbrowns") | self.has(
                "Pancakes"),
            "Copper Bar": self.can_smelt("Copper Ore"),
            "Copper Ore": self.can_mine_in_the_mines_floor_1_40() | self.can_mine_in_the_skull_cavern(),
            "Coral": self.can_reach_region(SVRegion.tide_pools) | self.has_season("Summer"),
            "Cow": self.has_building("Barn"),
            "Cow Milk": self.has("Milk") | self.has("Large Milk"),
            "Crab": self.can_crab_pot(),
            "Crab Cakes": self.can_mine_in_the_skull_cavern() |
                          (self.can_cook() & self.has_season("Fall") & self.has_year_two() & self.has("Crab") &
                           self.has("Wheat Flour") & self.has("Chicken Egg") & self.has("Oil")),
            "Crab Pot": self.has_skill_level("Fishing", 3),
            "Cranberry Candy": self.can_cook() & self.has_season("Winter") & self.has("Cranberries") &
                               self.has("Apple") & self.has("Sugar"),
            "Crayfish": self.can_crab_pot(),
            "Crispy Bass": self.can_cook() & self.has_relationship("Kent", 3) & self.has("Largemouth Bass") &
                           self.has("Wheat Flour") & self.has("Oil"),
            "Crocus": self.has_season("Winter"),
            "Crystal Fruit": self.has_season("Winter"),
            "Daffodil": self.has_season("Spring"),
            "Dandelion": self.has_season("Spring"),
            "Dish O' The Sea": self.can_cook() & self.has_skill_level("Fishing", 3) &
                               self.has(["Sardine", "Hashbrowns"]),
            "Dorado": self.can_fish(78) & self.has_season("Summer"),
            "Dried Starfish": self.can_fish() & self.can_reach_region(SVRegion.beach),
            "Driftwood": self.can_crab_pot(),
            "Duck Egg": self.has("Duck"),
            "Duck Feather": self.has("Duck"),
            "Duck": self.has_building("Big Coop"),
            "Egg": self.has("Chicken"),
            "Egg (Brown)": self.has("Chicken"),
            "Eggplant Parmesan": self.can_cook() & self.has_relationship("Lewis", 7) & self.has("Eggplant") & self.has(
                "Tomato"),
            "Escargot": self.can_cook() & self.has_relationship("Willy", 5) & self.has("Snail") & self.has("Garlic"),
            "Farmer's Lunch": self.can_cook() & self.has_skill_level("Farming", 3) & self.has("Omelet") & self.has(
                "Parsnip"),
            "Fiber": True_(),
            "Fiddlehead Fern": self.can_reach_region(SVRegion.secret_woods) & self.has_season("Summer"),
            "Fiddlehead Risotto": self.can_cook() & self.has_season("Fall") & self.has("Oil") &
                                  self.has("Fiddlehead Fern") & self.has("Garlic"),
            "Fishing Chest": self.can_fish_chests(),
            "Fish Taco": self.can_cook() & self.has_relationship("Linus", 7) & self.has("Tuna") & self.has("Tortilla") &
                         self.has("Red Cabbage") & self.has("Mayonnaise"),
            "Fried Calamari": self.can_cook() & self.has_relationship("Jodi", 3) & self.has("Squid") &
                              self.has("Wheat Flour") & self.has("Oil"),
            "Fried Eel": self.can_cook() & self.has_relationship("George", 3) & self.has("Eel") & self.has("Oil"),
            "Fried Egg": self.can_cook() & self.has("Any Egg"),
            "Fried Mushroom": self.can_cook() & self.has_relationship("Demetrius", 3) & self.has(
                "Morel") & self.has("Common Mushroom"),
            "Frozen Geode": self.can_mine_in_the_mines_floor_41_80(),
            "Fruit Salad": self.can_cook() & self.has_season("Fall") & self.has_year_two() & self.has("Blueberry") &
                           self.has("Melon") & self.has("Apricot"),
            "Furnace": self.has("Stone") & self.has("Copper Ore"),
            "Geode": self.can_mine_in_the_mines_floor_1_40(),
            "Ginger": self.can_reach_region(SVRegion.ginger_island),
            "Ginger Ale": self.can_cook() & self.can_reach_region(SVRegion.ginger_island) & self.has("Ginger") & self.has(
                "Sugar"),
            "Goat Cheese": self.has("Goat Milk") & self.has("Cheese Press"),
            "Goat Milk": self.has("Goat"),
            "Goat": self.has_building("Big Barn"),
            "Gold Bar": self.can_smelt("Gold Ore"),
            "Gold Ore": self.can_mine_in_the_mines_floor_81_120() | self.can_mine_in_the_skull_cavern(),
            "Golden Pumpkin": self.has_season("Fall") | self.has("Artifact Trove"),
            "Green Algae": self.can_fish(),
            "Green Tea": self.has("Keg") & self.has("Tea Leaves"),
            "Hardwood": self.has_tool("Axe", "Copper"),
            "Hashbrowns": self.can_cook() & self.can_spend_money(50) & self.has("Potato"),
            "Hazelnut": self.has_season("Fall"),
            "Holly": self.has_season("Winter"),
            "Honey": self.can_reach_region(SVRegion.desert) |
                     (self.has("Bee House") &
                      (self.has_season("Spring") | self.has_season("Summer") | self.has_season("Fall"))),
            "Hot Java Ring": self.can_reach_region(SVRegion.ginger_island),
            "Ice Cream": (self.has_season("Summer") & self.can_reach_region(SVRegion.town)) | self.can_reach_region(
                "The Desert"),
            # | (self.can_cook() & self.has_relationship("Jodi", 7) & self.has("Cow Milk") & self.has("Sugar")),
            "Iridium Bar": self.can_smelt("Iridium Ore"),
            "Iridium Ore": self.can_mine_in_the_skull_cavern(),
            "Iron Bar": self.can_smelt("Iron Ore"),
            "Iron Ore": self.can_mine_in_the_mines_floor_41_80() | self.can_mine_in_the_skull_cavern(),
            "Jelly": self.has("Preserves Jar"),
            "JotPK Small Buff": self.has_jotpk_power_level(2),
            "JotPK Medium Buff": self.has_jotpk_power_level(4),
            "JotPK Big Buff": self.has_jotpk_power_level(7),
            "JotPK Max Buff": self.has_jotpk_power_level(9),
            "Juice": self.has("Keg"),
            "Junimo Kart Small Buff": self.has_junimo_kart_power_level(2),
            "Junimo Kart Medium Buff": self.has_junimo_kart_power_level(4),
            "Junimo Kart Big Buff": self.has_junimo_kart_power_level(6),
            "Junimo Kart Max Buff": self.has_junimo_kart_power_level(8),
            "Keg": self.has_skill_level("Farming", 8) & self.has("Iron Bar") & self.has("Copper Bar") & self.has(
                "Oak Resin"),
            "Large Egg": self.has("Chicken"),
            "Large Egg (Brown)": self.has("Chicken"),
            "Large Goat Milk": self.has("Goat"),
            "Large Milk": self.has("Cow"),
            "Leek": self.has_season("Spring"),
            "Lightning Rod": self.has_skill_level("Foraging", 6),
            "Lobster": self.can_crab_pot(),
            "Loom": self.has_skill_level("Farming", 7) & self.has("Pine Tar"),
            "Magic Rock Candy": self.can_reach_region(SVRegion.desert) & self.has("Prismatic Shard"),
            "Magma Geode": self.can_mine_in_the_mines_floor_81_120() |
                           (self.has("Lava Eel") & self.has_building("Fish Pond")),
            "Maki Roll": self.can_cook() & self.can_fish(),
            "Maple Bar": self.can_cook() & self.has_season("Summer") & self.has_year_two() & self.has("Maple Syrup") &
                         self.has("Sugar") & self.has("Wheat Flour"),
            "Maple Syrup": self.has("Tapper"),
            "Mayonnaise": self.has("Mayonnaise Machine") & self.has("Chicken Egg"),
            "Mayonnaise Machine": self.has_skill_level("Farming", 2) & self.has("Wood") & self.has("Stone") &
                                  self.has("Earth Crystal") & self.has("Copper Bar"),
            "Mead": self.has("Keg") & self.has("Honey"),
            "Milk": self.has("Cow"),
            "Miner's Treat": self.can_cook() & self.has_skill_level("Mining", 3) & self.has("Cow Milk") & self.has(
                "Cave Carrot"),
            "Morel": self.can_reach_region(SVRegion.secret_woods),
            "Mussel": True_(),
            "Nautilus Shell": self.has_season("Winter"),
            "Oak Resin": self.has("Tapper"),
            "Oil": True_(),
            "Oil Maker": self.has_skill_level("Farming", 8) & self.has("Hardwood") & self.has("Gold Bar"),
            "Omelet": self.can_cook() & self.can_spend_money(100) & self.has("Any Egg") & self.has("Cow Milk"),
            "Omni Geode": self.can_mine_in_the_mines_floor_41_80() |
                          self.can_reach_region(SVRegion.desert) |
                          self.can_do_panning() |
                          self.received("Rusty Key") |
                          (self.has("Octopus") & self.has_building("Fish Pond")) |
                          self.can_reach_region(SVRegion.ginger_island),
            "Ostrich": self.has_building("Barn") & self.has("Ostrich Egg"),
            "Ostrich Egg": self.can_reach_region(SVRegion.ginger_island),
            "Oyster": True_(),
            "Pale Ale": self.has("Keg") & self.has("Hops"),
            "Pale Broth": self.can_cook() & self.has_relationship("Marnie", 3) & self.has("White Algae"),
            "Pancakes": self.can_cook() & self.can_spend_money(100) & self.has("Any Egg"),
            "Parsnip Soup": self.can_cook() & self.has_relationship("Caroline", 3) & self.has(
                "Parsnip") & self.has("Cow Milk"),
            "Pearl": (self.has("Blobfish") & self.has_building("Fish Pond")) |
                     (self.has_lived_months(4) & self.has("Artifact Trove")),
            "Pepper Poppers": self.can_cook() & self.has("Cheese") & self.has(
                "Hot Pepper") & self.has_relationship("Shane", 3),
            "Periwinkle": self.can_crab_pot(),
            "Pickles": self.has("Preserves Jar"),
            "Pig": self.has_building("Deluxe Barn"),
            "Piña Colada": False_(),  # self.can_reach_region(SVRegion.ginger_island),
            "Pine Tar": self.has("Tapper"),
            "Pink Cake": self.can_cook() & self.has_season("Summer") & self.has("Melon") & self.has(
                "Wheat Flour") & self.has("Sugar") & self.has("Any Egg"),
            "Pizza": self.can_spend_money(600),
            "Plum Pudding": self.can_cook() & self.has_season("Winter") & self.has("Wild Plum") &
                            self.has("Wheat Flour") & self.has("Sugar"),
            "Poppyseed Muffin": self.can_cook() & self.has_season("Winter") & self.has_year_two() &
                                self.has("Poppy") & self.has("Wheat Flour") & self.has("Sugar"),
            "Preserves Jar": self.has_skill_level("Farming", 4),
            "Pumpkin Pie": self.can_cook() & self.has_season("Winter") & self.has("Wheat Flour") &
                           self.has("Cow Milk") & self.has("Sugar"),
            "Purple Mushroom": self.can_mine_in_the_mines_floor_81_120() | self.can_mine_in_the_skull_cavern(),
            "Rabbit": self.has_building("Deluxe Coop"),
            "Rabbit's Foot": self.has("Rabbit"),
            "Radioactive Bar": self.can_smelt("Radioactive Ore"),
            "Radioactive Ore": self.can_mine_perfectly_in_the_skull_cavern() & self.can_reach_region(SVRegion.ginger_island),
            "Rainbow Shell": self.has_season("Summer"),
            "Rain Totem": self.has_skill_level("Foraging", 9),
            "Recycling Machine": self.has_skill_level("Fishing", 4) & self.has("Wood") &
                                 self.has("Stone") & self.has("Iron Bar"),
            "Red Mushroom": self.can_reach_region(SVRegion.secret_woods) & (
                    self.has_season("Summer") | self.has_season("Fall")),
            "Refined Quartz": self.can_smelt("Quartz") | self.can_smelt("Fire Quartz") |
                              (self.has("Recycling Machine") & (self.has("Broken CD") | self.has("Broken Glasses"))),
            "Rhubarb Pie": self.can_cook() & self.has_relationship("Marnie", 7) & self.has("Rhubarb") &
                           self.has("Wheat Flour") & self.has("Sugar"),
            "Rice": True_(),
            "Rice Pudding": self.can_cook() & self.has_relationship("Evelyn", 7) & self.has("Cow Milk") &
                            self.has("Sugar") & self.has("Rice"),
            "Roe": self.can_fish() & self.has_building("Fish Pond"),
            "Roots Platter": self.can_cook() & self.has_skill_level("Combat", 3) &
                             self.has("Cave Carrot") & self.has("Winter Root"),
            "Roasted Hazelnuts": self.can_cook() & self.has_season("Summer") & self.has("Hazelnut"),
            "Salad": self.can_spend_money(220),
            # | (self.can_cook() & self.has_relationship("Emily", 3) & self.has("Leek") & self.has("Dandelion") & self.has("Vinegar")),
            "Salmonberry": self.has_season("Spring"),
            "Salmon Dinner": self.can_cook() & self.has_relationship("Gus", 3) & self.has("Salmon") & self.has(
                "Amaranth") & self.has("Kale"),
            "Sashimi": self.can_fish() & self.can_cook() & self.has_relationship("Linus", 3),
            "Sea Urchin": self.can_reach_region(SVRegion.tide_pools) | self.has_season("Summer"),
            "Seaweed": self.can_fish() | self.can_reach_region(SVRegion.tide_pools),
            "Secret Note": self.received("Magnifying Glass"),
            "Sheep": self.has_building("Deluxe Barn"),
            "Shrimp": self.can_crab_pot(),
            "Slime": self.can_mine_in_the_mines_floor_1_40(),
            "Snail": self.can_crab_pot(),
            "Snow Yam": self.has_season("Winter"),
            "Soggy Newspaper": self.can_crab_pot(),
            "Solar Essence": self.can_mine_in_the_mines_floor_41_80() | self.can_mine_in_the_skull_cavern(),
            "Spaghetti": self.can_spend_money(240),
            "Spice Berry": self.has_season("Summer"),
            "Spring Onion": self.has_season("Spring"),
            "Squid Ink": self.can_mine_in_the_mines_floor_81_120() | (
                    self.has_building("Fish Pond") & self.has("Squid")),
            "Staircase": self.has_skill_level("Mining", 2),
            "Stir Fry": self.can_cook() & self.has_season("Spring") & self.has("Cave Carrot") &
                        self.has("Common Mushroom") & self.has("Kale") & self.has("Oil"),
            "Stone": self.has_tool("Pickaxe"),
            "Stuffing": self.has_season("Winter") |
                        (self.can_cook() & self.has_relationship("Pam", 7) & self.has("Bread") &
                         self.has("Cranberries") & self.has("Hazelnut")),
            "Sturgeon Roe": self.has("Sturgeon") & self.has_building("Fish Pond"),
            "Sugar": True_(),
            "Survival Burger": self.can_cook() & self.has_skill_level("Foraging", 2) &
                               self.has(["Bread", "Cave Carrot", "Eggplant"]),
            "Sweet Pea": self.has_season("Summer"),
            "Tapper": self.has_skill_level("Foraging", 3),
            "Tea Bush": self.has_relationship("Caroline", 2),
            "Tea Leaves": self.has_lived_months(1) & self.has("Tea Bush"),
            "Tortilla": self.can_cook() & self.can_spend_money(100) & self.has("Corn"),
            "Trash": self.can_crab_pot(),
            "Triple Shot Espresso": (self.has("Hot Java Ring") |
                                     (self.can_cook() & self.can_spend_money(5000) & self.has("Coffee"))),
            "Tropical Curry": False_(),
            # self.can_cook() & self.can_reach_region(SVRegion.ginger_island) & self.has("Coconut") & self.has("Pineapple") & self.has("Hot Pepper"),
            "Truffle Oil": self.has("Truffle") & self.has("Oil Maker"),
            "Truffle": self.has("Pig") & self.has_spring_summer_or_fall(),
            "Vegetable Medley": self.can_cook() & self.has_relationship("Caroline", 7) & self.has("Tomato") & self.has(
                "Beet"),
            "Vinegar": True_(),
            "Void Egg": self.can_meet("Krobus") | (self.has_building("Fish Pond") & self.has("Void Salmon")),
            "Void Essence": self.can_mine_in_the_mines_floor_81_120() | self.can_mine_in_the_skull_cavern(),
            "Void Mayonnaise": self.has("Mayonnaise Machine") & self.has("Void Egg"),
            "Wheat Flour": True_(),
            "White Algae": self.can_fish() & self.can_mine_in_the_mines_floor_1_40(),
            "Wild Horseradish": self.has_season("Spring"),
            "Wild Plum": self.has_season("Fall"),
            "Wilted Bouquet": self.has("Furnace") & self.has("Bouquet") & self.has("Coal"),
            "Wine": self.has("Keg"),
            "Winter Root": self.has_season("Winter"),
            "Wood": self.has_tool("Axe"),
            "Wool": self.has("Rabbit") | self.has("Sheep"),
            "Hay": self.has_building("Silo"),
        })
        self.item_rules.update(self.fish_rules)
        self.item_rules.update(self.museum_rules)
        self.item_rules.update(self.tree_fruit_rules)
        self.item_rules.update(self.seed_rules)
        self.item_rules.update(self.crop_rules)

        self.building_rules.update({
            "Barn": self.can_spend_money(6000) & self.has(["Wood", "Stone"]),
            "Big Barn": self.can_spend_money(12000) & self.has(["Wood", "Stone"]) & self.has_building("Barn"),
            "Deluxe Barn": self.can_spend_money(25000) & self.has(["Wood", "Stone"]) & self.has_building("Big Barn"),
            "Coop": self.can_spend_money(4000) & self.has(["Wood", "Stone"]),
            "Big Coop": self.can_spend_money(10000) & self.has(["Wood", "Stone"]) & self.has_building("Coop"),
            "Deluxe Coop": self.can_spend_money(20000) & self.has(["Wood", "Stone"]) & self.has_building("Big Coop"),
            "Fish Pond": self.can_spend_money(5000) & self.has(["Stone", "Seaweed", "Green Algae"]),
            "Mill": self.can_spend_money(2500) & self.has(["Stone", "Wood", "Cloth"]),
            "Shed": self.can_spend_money(15000) & self.has("Wood"),
            "Big Shed": self.can_spend_money(20000) & self.has(["Wood", "Stone"]) & self.has_building("Shed"),
            "Silo": self.can_spend_money(100) & self.has(["Stone", "Clay", "Copper Bar"]),
            "Slime Hutch": self.can_spend_money(10000) & self.has(["Stone", "Refined Quartz", "Iridium Bar"]),
            "Stable": self.can_spend_money(10000) & self.has(["Hardwood", "Iron Bar"]),
            "Well": self.can_spend_money(1000) & self.has("Stone"),
            "Shipping Bin": self.can_spend_money(250) & self.has("Wood"),
            "Kitchen": self.can_spend_money(10000) & self.has("Wood") & self.has_house(0),
            "Kids Room": self.can_spend_money(50000) & self.has("Hardwood") & self.has_house(1),
            "Cellar": self.can_spend_money(100000) & self.has_house(2),
        })

        self.quest_rules.update({
            "Introductions": True_(),
            "How To Win Friends": self.can_complete_quest("Introductions"),
            "Getting Started": self.has("Parsnip") & self.has_tool("Hoe") & self.has_tool("Watering Can"),
            "To The Beach": True_(),
            "Raising Animals": self.can_complete_quest("Getting Started") & self.has_building("Coop"),
            "Advancement": self.can_complete_quest("Getting Started") & self.has_skill_level("Farming", 1),
            "Archaeology": self.has_tool("Hoe") | self.can_mine_in_the_mines_floor_1_40() | self.can_fish(),
            "Meet The Wizard": True_() & self.can_reach_region(SVRegion.community_center),
            "Forging Ahead": self.has("Copper Ore") & self.has("Furnace"),
            "Smelting": self.has("Copper Bar"),
            "Initiation": self.can_mine_in_the_mines_floor_1_40(),
            "Robin's Lost Axe": self.has_season("Spring"),
            "Jodi's Request": self.has_season("Spring") & self.has("Cauliflower"),
            "Mayor's \"Shorts\"": self.has_season("Summer") & self.has_relationship("Marnie", 4),
            "Blackberry Basket": self.has_season("Fall"),
            "Marnie's Request": self.has_relationship("Marnie", 3) & self.has("Cave Carrot"),
            "Pam Is Thirsty": self.has_season("Summer") & self.has("Pale Ale"),
            "A Dark Reagent": self.has_season("Winter") & self.has("Void Essence"),
            "Cow's Delight": self.has_season("Fall") & self.has("Amaranth"),
            "The Skull Key": self.received("Skull Key") & self.can_reach_region(SVRegion.desert),
            "Crop Research": self.has_season("Summer") & self.has("Melon"),
            "Knee Therapy": self.has_season("Summer") & self.has("Hot Pepper"),
            "Robin's Request": self.has_season("Winter") & self.has("Hardwood"),
            "Qi's Challenge": self.can_mine_in_the_skull_cavern(),
            "The Mysterious Qi": self.has("Battery Pack") & self.can_reach_region(SVRegion.desert) & self.has(
                "Rainbow Shell") & self.has("Beet") & self.has("Solar Essence"),
            "Carving Pumpkins": self.has_season("Fall") & self.has("Pumpkin"),
            "A Winter Mystery": self.has_season("Winter"),
            "Strange Note": self.received("Magnifying Glass") & self.can_reach_region(SVRegion.secret_woods) & self.has(
                "Maple Syrup"),
            "Cryptic Note": self.received("Magnifying Glass") & self.can_reach_region(SVRegion.perfect_skull_cavern),
            "Fresh Fruit": self.has("Apricot"),
            "Aquatic Research": self.has("Pufferfish"),
            "A Soldier's Star": self.has_relationship("Kent") & self.has("Starfruit"),
            "Mayor's Need": self.has("Truffle Oil"),
            "Wanted: Lobster": self.has("Lobster"),
            "Pam Needs Juice": self.has("Battery Pack"),
            "Fish Casserole": self.has_relationship("Jodi", 4) & self.has("Largemouth Bass"),
            "Catch A Squid": self.has("Squid"),
            "Fish Stew": self.has("Albacore"),
            "Pierre's Notice": self.has("Sashimi"),
            "Clint's Attempt": self.has("Amethyst"),
            "A Favor For Clint": self.has("Iron Bar"),
            "Staff Of Power": self.has("Iridium Bar"),
            "Granny's Gift": self.has("Leek"),
            "Exotic Spirits": self.has("Coconut"),
            "Catch a Lingcod": self.has("Lingcod"),
        })

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

    def can_reach_location(self, spot: str) -> StardewRule:
        return Reach(spot, "Location", self.player)

    def can_reach_entrance(self, spot: str) -> StardewRule:
        return Reach(spot, "Entrance", self.player)

    def can_have_earned_total_money(self, amount: int) -> StardewRule:
        return self.has_lived_months(min(8, amount // MONEY_PER_MONTH))

    def can_spend_money(self, amount: int) -> StardewRule:
        return self.has_lived_months(min(8, amount // (MONEY_PER_MONTH // 5)))

    def has_tool(self, tool: str, material: str = "Basic") -> StardewRule:
        if material == "Basic":
            return True_()

        if self.options[options.ToolProgression] == options.ToolProgression.option_progressive:
            return self.received(f"Progressive {tool}", count=tool_materials[material])

        return self.has(f"{material} Bar") & self.can_spend_money(tool_prices[material])

    def has_skill_level(self, skill: str, level: int) -> StardewRule:
        if level == 0:
            return True_()

        if self.options[options.SkillProgression] == options.SkillProgression.option_progressive:
            return self.received(f"{skill} Level", count=level)

        if skill == "Fishing" and self.options[options.ToolProgression] == options.ToolProgression.option_progressive:
            return self.can_get_fishing_xp()

        return self.has_lived_months(month_end_per_skill_level[(skill, level)])

    def has_total_skill_level(self, level: int) -> StardewRule:
        if level == 0:
            return True_()

        if self.options[options.SkillProgression] == options.SkillProgression.option_progressive:
            skills_items = ["Farming Level", "Mining Level", "Foraging Level",
                            "Fishing Level", "Combat Level"]
            return self.received(skills_items, count=level)

        if level > 40 and self.options[options.ToolProgression] == options.ToolProgression.option_progressive:
            return self.has_lived_months(month_end_per_total_level[level]) & self.can_get_fishing_xp()

        return self.has_lived_months(month_end_per_total_level[level])

    def has_building(self, building: str) -> StardewRule:
        if not self.options[options.BuildingProgression] == options.BuildingProgression.option_vanilla:
            count = 1
            if building in ["Coop", "Barn", "Shed"]:
                building = f"Progressive {building}"
            elif building.startswith("Big"):
                count = 2
                building = " ".join(["Progressive", *building.split(" ")[1:]])
            elif building.startswith("Deluxe"):
                count = 3
                building = " ".join(["Progressive", *building.split(" ")[1:]])
            return self.received(f"{building}", count)

        return Has(building, self.building_rules)

    def has_house(self, upgrade_level: int) -> StardewRule:
        if upgrade_level < 1:
            return True_()

        if upgrade_level > 3:
            return False_()

        if not self.options[options.BuildingProgression] == options.BuildingProgression.option_vanilla:
            return self.received(f"Progressive House", upgrade_level)

        if upgrade_level == 1:
            return Has("Kitchen", self.building_rules)

        if upgrade_level == 2:
            return Has("Kids Room", self.building_rules)

        # if upgrade_level == 3:
        return Has("Cellar", self.building_rules)

    def can_complete_quest(self, quest: str) -> StardewRule:
        return Has(quest, self.quest_rules)

    def can_get_fishing_xp(self) -> StardewRule:
        if self.options[options.SkillProgression] == options.SkillProgression.option_progressive:
            return self.can_fish() | self.can_crab_pot()

        return self.can_fish()

    def has_max_fishing_rod(self) -> StardewRule:
        if self.options[options.ToolProgression] == options.ToolProgression.option_progressive:
            return self.received("Progressive Fishing Rod", 4)
        return self.can_get_fishing_xp()

    def can_fish(self, difficulty: int = 0) -> StardewRule:
        skill_required = max(0, int((difficulty / 10) - 1))
        if difficulty <= 40:
            skill_required = 0
        skill_rule = self.has_skill_level("Fishing", skill_required)
        number_fishing_rod_required = 1 if difficulty < 50 else 2
        if self.options[options.ToolProgression] == options.ToolProgression.option_progressive:
            return self.received("Progressive Fishing Rod", number_fishing_rod_required) & skill_rule

        return skill_rule

    def has_max_fishing(self) -> StardewRule:
        skill_rule = self.has_skill_level("Fishing", 10)
        return self.has_max_fishing_rod() & skill_rule

    def can_fish_chests(self) -> StardewRule:
        skill_rule = self.has_skill_level("Fishing", 4)
        return self.has_max_fishing_rod() & skill_rule

    def can_buy_seed(self, seed: SeedItem):
        if self.options[options.SeedShuffle] == options.SeedShuffle.option_disabled or seed.name == "Rare Seed":
            item_rule = True_()
        else:
            item_rule = self.received(seed.name)
        season_rule = self.has_any_season(seed.seasons)
        region_rule = self.can_reach_any_region(seed.regions)
        return season_rule & region_rule & item_rule

    def can_grow_crop(self, crop: CropItem):
        season_rule = self.has_any_season(crop.farm_growth_seasons)
        seed_rule = self.has(crop.seed.name)
        farm_rule = self.can_reach_region(SVRegion.farm) & season_rule
        region_rule = farm_rule | self.can_reach_region(SVRegion.greenhouse)
        return seed_rule & region_rule

    def can_catch_fish(self, fish: FishItem) -> StardewRule:
        region_rule = self.can_reach_any_region(fish.locations)
        season_rule = self.has_any_season(fish.seasons)
        difficulty_rule = self.can_fish(fish.difficulty)
        if fish.difficulty == -1:
            difficulty_rule = self.can_crab_pot()
        return region_rule & season_rule & difficulty_rule

    def can_catch_every_fish(self) -> StardewRule:
        rules = [self.has_skill_level("Fishing", 10), self.has_max_fishing_rod()]
        for fish in all_fish:
            rules.append(self.can_catch_fish(fish))
        return And(rules)

    def has_max_fishing_rod(self) -> StardewRule:
        if self.options[options.ToolProgression] == options.ToolProgression.option_progressive:
            return self.received("Progressive Fishing Rod", 4)
        return self.can_get_fishing_xp()

    def can_cook(self) -> StardewRule:
        return self.has_house(1) or self.has_skill_level("Foraging", 9)

    def can_smelt(self, item: str) -> StardewRule:
        return self.has("Furnace") & self.has(item)

    def can_crab_pot(self) -> StardewRule:
        if self.options[options.SkillProgression] == options.SkillProgression.option_progressive:
            return self.has("Crab Pot")

        return True_()

    def can_do_panning(self) -> StardewRule:
        return self.received("Glittering Boulder Removed")

    # Regions
    def can_mine_in_the_mines_floor_1_40(self) -> StardewRule:
        return self.can_reach_region(SVRegion.mines_floor_5)

    def can_mine_in_the_mines_floor_41_80(self) -> StardewRule:
        return self.can_reach_region(SVRegion.mines_floor_45)

    def can_mine_in_the_mines_floor_81_120(self) -> StardewRule:
        return self.can_reach_region(SVRegion.mines_floor_85)

    def can_mine_in_the_skull_cavern(self) -> StardewRule:
        return (self.can_progress_in_the_mines_from_floor(120) &
                self.can_reach_region(SVRegion.skull_cavern))

    def can_mine_perfectly_in_the_skull_cavern(self) -> StardewRule:
        return (self.can_progress_in_the_mines_from_floor(160) &
                self.can_reach_region(SVRegion.skull_cavern))

    def get_weapon_rule_for_floor_tier(self, tier: int):
        if tier >= 4:
            return self.has_galaxy_weapon()
        if tier >= 3:
            return self.has_great_weapon()
        if tier >= 2:
            return self.has_good_weapon()
        if tier >= 1:
            return self.has_decent_weapon()
        return self.has_any_weapon()

    def can_progress_in_the_mines_from_floor(self, floor: int) -> StardewRule:
        tier = int(floor / 40)
        rules = []
        weapon_rule = self.get_weapon_rule_for_floor_tier(tier)
        rules.append(weapon_rule)
        if self.options[options.ToolProgression] == options.ToolProgression.option_progressive:
            rules.append(self.received("Progressive Pickaxe", tier))
        if self.options[options.SkillProgression] == options.SkillProgression.option_progressive:
            combat_tier = min(10, max(0, tier * 2))
            rules.append(self.has_skill_level("Combat", combat_tier))
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
            rules.append(self.has_skill_level("Combat", combat_tier))
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

    def has_traveling_merchant(self, tier: int = 1):
        traveling_merchant_days = [f"Traveling Merchant: {day}" for day in week_days]
        return self.received(traveling_merchant_days, tier)

    def can_get_married(self) -> StardewRule:
        return self.can_reach_region(SVRegion.tide_pools) & self.has_relationship("Bachelor", 10) & self.has_house(1)

    def can_have_two_children(self) -> StardewRule:
        return self.can_get_married() & self.has_house(2) & self.has_relationship("Bachelor", 12)

    def has_relationship(self, npc: str, hearts: int = 1) -> StardewRule:
        if hearts <= 0:
            return True_()
        if self.options[options.Friendsanity] == options.Friendsanity.option_none:
            return self.can_earn_relationship(npc, hearts)
        if npc not in all_villagers_by_name:
            if npc == "Pet":
                if self.options[options.Friendsanity] == options.Friendsanity.option_bachelors:
                    return self.can_befriend_pet(hearts)
                return self.received(f"Pet: 1 <3", hearts)
            if npc == "Any" or npc == "Bachelor":
                possible_friends = []
                for name in all_villagers_by_name:
                    if npc == "Any" or all_villagers_by_name[name].bachelor:
                        possible_friends.append(self.has_relationship(name, hearts))
                return Or(possible_friends)
            if npc == "All":
                mandatory_friends = []
                for name in all_villagers_by_name:
                    mandatory_friends.append(self.has_relationship(name, hearts))
                return And(mandatory_friends)
            if npc.isnumeric():
                possible_friends = []
                for name in all_villagers_by_name:
                    possible_friends.append(self.has_relationship(name, hearts))
                return Count(int(npc), possible_friends)
            return self.can_earn_relationship(npc, hearts)

        villager = all_villagers_by_name[npc]
        if self.options[options.Friendsanity] == options.Friendsanity.option_bachelors and not villager.bachelor:
            return self.can_earn_relationship(npc, hearts)
        if self.options[options.Friendsanity] == options.Friendsanity.option_starting_npcs and not villager.available:
            return self.can_earn_relationship(npc, hearts)
        if self.options[
            options.Friendsanity] != options.Friendsanity.option_all_with_marriage and villager.bachelor and hearts > 8:
            return self.received(f"{villager.name}: 1 <3", 8) & self.can_earn_relationship(npc, hearts)
        return self.received(f"{villager.name}: 1 <3", hearts)

    def can_meet(self, npc: str) -> StardewRule:
        if npc not in all_villagers_by_name:
            return True_()
        villager = all_villagers_by_name[npc]
        rules = [self.can_reach_any_region(villager.locations)]
        if npc == "Kent":
            rules.append(self.has_lived_months(4))
        if npc == "Dwarf":
            rules.append(self.received("Dwarvish Translation Guide"))
            rules.append(self.has_tool("Pickaxe", "Iron"))

        return And(rules)

    def can_earn_relationship(self, npc: str, hearts: int = 0) -> StardewRule:
        if npc == "Pet":
            return self.can_befriend_pet(hearts)
        if npc in all_villagers_by_name:
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
        return self.can_reach_region(SVRegion.farm) & \
            ((self.has_tool("Watering Can") & self.has_lived_months(points // points_per_water_month)) |
             self.has_lived_months(points // points_per_month))

    def can_complete_bundle(self, bundle_requirements: List[BundleItem], number_required: int) -> StardewRule:
        item_rules = []
        for bundle_item in bundle_requirements:
            if bundle_item.item.item_id == -1:
                return self.can_spend_money(bundle_item.amount)
            else:
                item_rules.append(bundle_item.item.name)
        return self.has(item_rules, number_required)

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
                               self.has_relationship("Pet", 5),  # Max Pet
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

    def has_spring_summer_or_fall(self) -> StardewRule:
        return self.has_season("Spring") | self.has_season("Summer") | self.has_season("Fall")

    def can_find_museum_item(self, item: MuseumItem) -> StardewRule:
        region_rule = self.can_reach_all_regions(item.locations)
        geodes_rule = self.has(item.geodes)
        # monster_rule = self.can_farm_monster(item.monsters)
        # extra_rule = True_()
        return region_rule & geodes_rule  # & monster_rule & extra_rule

    def can_complete_museum(self) -> StardewRule:
        rules = [self.can_mine_perfectly_in_the_skull_cavern()]

        if self.options[options.Museumsanity] != options.Museumsanity.option_none:
            rules.append(self.received("Traveling Merchant Metal Detector", 4))

        for donation in all_museum_items:
            rules.append(self.can_find_museum_item(donation))
        return And(rules)

    def has_season(self, season: str) -> StardewRule:
        seasons_order = ["Spring", "Summer", "Fall", "Winter"]
        if self.options[options.SeasonRandomization] == options.SeasonRandomization.option_progressive:
            return self.received("Progressive Season", seasons_order.index(season))
        if self.options[options.SeasonRandomization] == options.SeasonRandomization.option_disabled:
            if season == "Spring":
                return True_()
            return self.has_lived_months(1)
        return self.received(season)

    def has_any_season(self, seasons: Iterable[str]):
        if not seasons:
            return True_()
        return Or([self.has_season(season) for season in seasons])

    def has_all_seasons(self, seasons: Iterable[str]):
        if not seasons:
            return True_()
        return And([self.has_season(season) for season in seasons])

    def has_lived_months(self, number: int) -> StardewRule:
        number = max(0, min(number, 8))
        return self.received("Month End", number)

    def has_rusty_key(self) -> StardewRule:
        if self.options[options.Museumsanity] == options.Museumsanity.option_none:
            return True_()
        return self.received("Rusty Key")
