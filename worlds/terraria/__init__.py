from worlds.AutoWorld import World
from worlds.generic.Rules import add_rule
from BaseClasses import Region, RegionType, ItemClassification
from .Checks import item_name_to_id, location_name_to_id, TerrariaItem, TerrariaLocation, precollected, get_items_locations
from .Options import options

class TerrariaWorld(World):
    """Terraria is a 2D sandbox video game."""
    game: str = "Terraria"
    option_definitions = options

    # data_version is used to signal that items, locations or their names
    # changed. Set this to 0 during development so other games' clients do not
    # cache any texts, then increase by 1 for each release that makes changes.
    data_version = 0

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
        if name == "Nothing":
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
            items_to_create.append("Nothing")
        
        for item in map(self.create_item, items_to_create):
            self.multiworld.itempool.append(item)

    def set_rules(self) -> None:
        fishing = self.multiworld.achievements[self.player].value == 3

        for location in self.ter_locations:
            rule = None
            match location:
                case "Old One's Army Tier 1": rule = lambda state: state.has("Post-Eater of Worlds or Brain of Cthulhu", self.player)
                case "Pirate Invasion": rule = lambda state: state.has("Hardmode", self.player)
                case "Queen Slime": rule = lambda state: state.has("Hardmode", self.player)
                case "The Twins": rule = lambda state: state.has("Hardmode", self.player)
                case "The Destroyer": rule = lambda state: state.has("Hardmode", self.player)
                case "Skeletron Prime": rule = lambda state: state.has_all({"Post-Skeletron", "Hardmode"}, self.player)
                case "Old One's Army Tier 2": rule = lambda state: state.has_any({"Post-The Twins", "Post-The Destroyer", "Post-Skeletron Prime", "Post-Golem"}, self.player) and state.has_all({"Post-Eater of Worlds or Brain of Cthulhu", "Hardmode"}, self.player)
                case "Plantera": rule = lambda state: state.has_all({"Hardmode", "Post-The Twins", "Post-The Destroyer", "Post-Skeletron Prime"}, self.player)
                case "Duke Fishron": rule = lambda state: state.has("Hardmode", self.player)
                case "Frost Legion": rule = lambda state: state.has_all({"Post-Skeletron", "Hardmode", "Post-Plantera"}, self.player)
                case "Golem": rule = lambda state: (state.has_all({"Post-The Twins", "Post-The Destroyer", "Post-Skeletron Prime"}, self.player) or state.has("Post-Golem", self.player)) and state.has_all({"Hardmode", "Post-Plantera"}, self.player)
                case "Old One's Army Tier 3": rule = lambda state: state.has_all({"Post-Eater of Worlds or Brain of Cthulhu", "Hardmode", "Post-Golem"}, self.player)
                case "Martian Madness": rule = lambda state: state.has_all({"Hardmode", "Post-Golem"}, self.player)
                case "Mourning Wood": rule = lambda state: state.has_all({"Post-Skeletron", "Hardmode", "Post-Plantera"}, self.player)
                case "Pumpking": rule = lambda state: state.has_all({"Post-Skeletron", "Hardmode", "Post-Plantera"}, self.player)
                case "Everscream": rule = lambda state: state.has_all({"Post-Skeletron", "Hardmode", "Post-Plantera"}, self.player)
                case "Santa-NK1": rule = lambda state: state.has_all({"Post-Skeletron", "Hardmode", "Post-Plantera"}, self.player)
                case "Ice Queen": rule = lambda state: state.has_all({"Post-Skeletron", "Hardmode", "Post-Plantera"}, self.player)
                case "Empress of Light": rule = lambda state: state.has_all({"Hardmode", "Post-Plantera"}, self.player)
                case "Lunatic Cultist": rule = lambda state: state.has_all({"Post-Skeletron", "Hardmode", "Post-Golem"}, self.player)
                case "Lunar Events": rule = lambda state: state.has_all({"Post-Skeletron", "Hardmode", "Post-Golem"}, self.player)
                case "Moon Lord": rule = lambda state: state.has_all({"Post-Skeletron", "Hardmode", "Post-Golem"}, self.player)
                case "Zenith": rule = lambda state: state.has_all({"Post-Skeletron", "Hardmode", "Post-The Twins", "Post-The Destroyer", "Post-Skeletron Prime", "Post-Plantera", "Post-Golem"}, self.player)
                case "Dungeon Heist": rule = lambda state: state.has("Post-Skeletron", self.player)
                case "Boots of the Hero": rule = lambda state: state.has("Post-Goblin Army", self.player)
                case "Head in the Clouds": rule = lambda state: fishing or state.has("Hardmode", self.player)
                case "Begone, Evil!": rule = lambda state: state.has("Hardmode", self.player)
                case "Extra Shiny!": rule = lambda state: state.has("Hardmode", self.player)
                case "Drax Attax": rule = lambda state: state.has_all({"Post-Skeletron", "Hardmode"}, self.player)
                case "Photosynthesis": rule = lambda state: state.has_all({"Post-Skeletron", "Hardmode"}, self.player)
                case "Get a Life": rule = lambda state: state.has("Hardmode", self.player)
                case "Kill the Sun": rule = lambda state: state.has("Hardmode", self.player)
                case "Mecha Mayhem": rule = lambda state: state.has_all({"Post-Skeletron", "Hardmode"}, self.player)
                case "Prismancer": rule = lambda state: state.has("Hardmode", self.player)
                case "It Can Talk?!": rule = lambda state: state.has("Hardmode", self.player)
                case "Gelatin World Tour": rule = lambda state: state.has_all({"Post-Skeletron", "Hardmode"}, self.player)
                case "Topped Off": rule = lambda state: state.has("Hardmode", self.player)
                case "Don't Dread on Me": rule = lambda state: state.has("Hardmode", self.player)
                case "Temple Raider": rule = lambda state: state.has_all({"Hardmode", "Post-The Twins", "Post-The Destroyer", "Post-Skeletron Prime"}, self.player)
                case "Robbing the Grave": rule = lambda state: state.has_all({"Post-Skeletron", "Hardmode", "Post-Plantera"}, self.player)
                case "Baleful Harvest": rule = lambda state: state.has_all({"Post-Skeletron", "Hardmode", "Post-Plantera"}, self.player)
                case "Ice Scream": rule = lambda state: state.has_all({"Post-Skeletron", "Hardmode", "Post-Plantera"}, self.player)
                case "Sword of the Hero": rule = lambda state: state.has_all({"Post-Skeletron", "Hardmode", "Post-Plantera"}, self.player)
                case "Big Booty": rule = lambda state: state.has_all({"Post-Skeletron", "Hardmode", "Post-Plantera"}, self.player)
                case "Real Estate Agent": rule = lambda state: state.has_all({"Post-Goblin Army", "Post-Eater of Worlds or Brain of Cthulhu", "Post-Queen Bee", "Post-Skeletron", "Hardmode", "Post-Pirate Invasion", "Post-Plantera"}, self.player) and state.has_any({"Post-The Twins", "Post-The Destroyer", "Post-Skeletron Prime"}, self.player)
                case "Rainbows and Unicorns": rule = lambda state: state.has_all({"Post-Skeletron", "Hardmode", "Post-Plantera"}, self.player)
                case "Sick Throw": rule = lambda state: state.has_all({"Post-Skeletron", "Hardmode", "Post-Golem"}, self.player)
                case "You and What Army?": rule = lambda state: state.has_any({"Post-Queen Bee", "Post-Plantera"}, self.player) and state.has_all({"Post-Skeletron", "Hardmode", "Post-Golem"}, self.player)

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
