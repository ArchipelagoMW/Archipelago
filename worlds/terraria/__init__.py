from worlds.AutoWorld import WebWorld, World
from worlds.generic.Rules import add_rule
from BaseClasses import Region, RegionType, ItemClassification, Tutorial
from .Checks import item_name_to_id, location_name_to_id, TerrariaItem, TerrariaLocation, precollected, get_items_locations
from .Options import options
from .Rules import get_rules

class TerrariaWeb(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Terraria randomizer connected to an Archipelago Multiworld",
        "English",
        "setup_en.md",
        "setup/en",
        ["Seldom"]
    )]

class TerrariaWorld(World):
    """
    Terraria is a 2D multiplayer sandbox game featuring mining, building, exploration, and combat.
    Features 18 bosses and 4 classes.
    """
    game: str = "Terraria"
    web = TerrariaWeb()
    option_definitions = options

    # data_version is used to signal that items, locations or their names
    # changed. Set this to 0 during development so other games' clients do not
    # cache any texts, then increase by 1 for each release that makes changes.
    data_version = 2

    item_name_to_id = item_name_to_id
    location_name_to_id = location_name_to_id

    def generate_early(self) -> None:
        self.ter_items, self.ter_locations = get_items_locations(self.multiworld.goal[self.player].value, self.multiworld.achievements[self.player].value, self.multiworld.fill_extra_checks_with[self.player].value)

    def create_item(self, name: str) -> TerrariaItem:
        classification = ItemClassification.useful
        if name in {
            "Post-Goblin Army",
            "Post-Eater of Worlds or Brain of Cthulhu",
            "Post-Queen Bee",
            "Post-Skeletron",
            "Hardmode",
            "Post-Pirate Invasion",
            "Post-The Twins",
            "Post-The Destroyer",
            "Post-Skeletron Prime",
            "Post-Plantera",
            "Post-Golem",
            "Victory",
        }:
            classification = ItemClassification.progression
        if name == "50 Silver":
            classification = ItemClassification.filler
        return TerrariaItem(name, classification, item_name_to_id[name], self.player)

    def create_regions(self) -> None:
        menu = Region("Menu", RegionType.Generic, "Menu", self.player, self.multiworld)

        for location in self.ter_locations:
            menu.locations.append(TerrariaLocation(self.player, location, location_name_to_id[location], menu))
        self.multiworld.regions.append(menu)

    def create_items(self) -> None:
        items_to_create = self.ter_items.copy()
        for item in precollected:
            items_to_create.remove(item)
        for _ in range(len(precollected)):
            items_to_create.append("50 Silver")
        
        for item in map(self.create_item, items_to_create):
            self.multiworld.itempool.append(item)

    def set_rules(self) -> None:
        rules = get_rules(self.player, self.multiworld.achievements[self.player].value == 3)

        for location in self.ter_locations:
            rule = rules.get(location)
            if rule != None:
                add_rule(self.multiworld.get_location(location, self.player), rule)

    def generate_basic(self) -> None:
        for item in precollected:
            self.multiworld.push_precollected(self.create_item(item))
        
        goal = self.multiworld.goal[self.player].value

        if goal == 0:
            goal_location = "Wall of Flesh"
        elif goal == 1:
            goal_location = "Plantera"
        elif goal == 2:
            goal_location = "Moon Lord"
        elif goal == 3:
            goal_location = "Zenith"

        self.multiworld.get_location(goal_location, self.player).place_locked_item(self.create_item("Victory"))
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)
