from worlds.AutoWorld import World
from worlds.generic.Rules import add_rule
from BaseClasses import Region, Location, Entrance, Item, RegionType, ItemClassification
from Utils import get_options, output_path

next_id = 0x7E0000

items = [
    "Bound Goblin",
    "Dryad",
    "Progressive Old One's Army",
    "Witch Doctor",
    "Dungeon",
    "Hardmode",
    "Underground Evil",
    "Hallow",
    "Wizard",
    "Truffle",
    "Hardmode Fishing",
    "Truffle Worm",
    "Steampunker",
    "Life Fruit",
    "Solar Eclipse",
    "Plantera's Bulb",
    "Cyborg",
    "Autohammer",
    "Post-Plantera Dungeon",
    "Biome Chests",
    "Post-Plantera Eclipse",
    "Lihzahrd Altar",
    "Prismatic Lacewing",
    "Martian Probe",
    "Cultists",
    "Win",
]

locations = [
    "King Slime",
    "Eye of Cthulhu",
    "Eater of Worlds or Brain of Cthulhu",
    "Queen Bee",
    "Skeletron",
    "Deerclops",
    "Wall of Flesh",
    "Queen Slime",
    "The Twins",
    "The Destroyer",
    "Skeletron Prime",
    "Plantera",
    "Golem",
    "Empress of Light",
    "Duke Fishron",
    "Lunatic Cultist",
    "Moon Lord",
    "Goblin Army",
    "Old One's Army Tier 1",
    "Old One's Army Tier 2",
    "Old One's Army Tier 3",
    "Torch God",
    "Frost Legion",
    "Frost Moon",
    "Lunar Events",
    "Martian Madness",
    "Pirate Invasion",
    "Pumpkin Moon",
]

item_name_to_id: dict[str, int] = {}
location_name_to_id: dict[str, int] = {}

for item in items:
    item_name_to_id[item] = next_id
    next_id += 1

for location in locations:
    location_name_to_id[location] = next_id
    next_id += 1

class TerrariaItem(Item):  # or from Items import MyGameItem
    game = "Terraria"  # name of the game/world this item is from

class TerrariaLocation(Location):  # or from Locations import MyGameLocation
    game = "Terraria"  # name of the game/world this location is in

class TerrariaWorld(World):
    """Terraria is a 2D sandbox video game."""
    game: str = "Terraria"  # name of the game/world
    topology_present: bool = True  # show path to required location checks in spoiler
    option_definitions = {}

    # data_version is used to signal that items, locations or their names
    # changed. Set this to 0 during development so other games' clients do not
    # cache any texts, then increase by 1 for each release that makes changes.
    data_version = 0

    # The following two dicts are required for the generation to know which
    # items exist. They could be generated from json or something else. They can
    # include events, but don't have to since events will be placed manually.
    item_name_to_id = item_name_to_id
    location_name_to_id = location_name_to_id

    def create_item(self, name: str) -> TerrariaItem:
        classification = ItemClassification.useful
        if name == "Cultists" or name == "Win":
            classification = ItemClassification.progression
        return TerrariaItem(name, classification, item_name_to_id[name], self.player)

    def create_regions(self) -> None:
        menu = Region("Menu", RegionType.Generic, "Menu", self.player, self.multiworld)
        for location in locations:
            menu.locations.append(TerrariaLocation(self.player, location, location_name_to_id[location], menu))
        self.multiworld.regions.append(menu)

    def create_items(self) -> None:
        items_to_create = items.copy()
        for _ in range(2):
            items_to_create.append("Progressive Old One's Army")
        items_to_create.remove("Win")
        for item in map(self.create_item, items_to_create):
            self.multiworld.itempool.append(item)

    def set_rules(self) -> None:
        add_rule(self.multiworld.get_location("Queen Slime", self.player), lambda state: state.has("Hallow", self.player))
        add_rule(self.multiworld.get_location("The Twins", self.player), lambda state: state.has_all({"Hardmode", "Hallow"}, self.player))
        add_rule(self.multiworld.get_location("The Destroyer", self.player), lambda state: state.has_all({"Hardmode", "Underground Evil"}, self.player))
        add_rule(self.multiworld.get_location("Skeletron Prime", self.player), lambda state: state.has_all({"Dungeon", "Hardmode", "Hallow", "Underground Evil"}, self.player))
        add_rule(self.multiworld.get_location("Plantera", self.player), lambda state: state.has("Plantera's Bulb", self.player))
        add_rule(self.multiworld.get_location("Golem", self.player), lambda state: state.has("Lihzahrd Altar", self.player))
        add_rule(self.multiworld.get_location("Empress of Light", self.player), lambda state: state.has_all({"Hallow", "Prismatic Lacewing"}, self.player))
        add_rule(self.multiworld.get_location("Duke Fishron", self.player), lambda state: state.has("Truffle Worm", self.player))
        add_rule(self.multiworld.get_location("Lunatic Cultist", self.player), lambda state: state.has("Cultists", self.player))
        add_rule(self.multiworld.get_location("Moon Lord", self.player), lambda state: state.has("Cultists", self.player))
        add_rule(self.multiworld.get_location("Old One's Army Tier 1", self.player), lambda state: state.has("Progressive Old One's Army", self.player))
        add_rule(self.multiworld.get_location("Old One's Army Tier 2", self.player), lambda state: state.has("Progressive Old One's Army", self.player, 2))
        add_rule(self.multiworld.get_location("Old One's Army Tier 3", self.player), lambda state: state.has("Progressive Old One's Army", self.player, 3))
        add_rule(self.multiworld.get_location("Frost Legion", self.player), lambda state: state.has_all({"Dungeon", "Hardmode", "Hallow", "Underground Evil", "Post-Plantera Dungeon"}, self.player))
        add_rule(self.multiworld.get_location("Frost Moon", self.player), lambda state: state.has_all({"Dungeon", "Hardmode", "Hallow", "Underground Evil", "Post-Plantera Dungeon"}, self.player))
        add_rule(self.multiworld.get_location("Lunar Events", self.player), lambda state: state.has("Cultists", self.player))
        add_rule(self.multiworld.get_location("Martian Madness", self.player), lambda state: state.has("Martian Probe", self.player))
        add_rule(self.multiworld.get_location("Pirate Invasion", self.player), lambda state: state.has("Hardmode", self.player))
        add_rule(self.multiworld.get_location("Pumpkin Moon", self.player), lambda state: state.has_all({"Hardmode", "Dryad", "Post-Plantera Dungeon"}, self.player) and (state.has_any({"Hallow", "Underground Evil"}, self.player)))

    def generate_basic(self) -> None:
        self.multiworld.get_location("Moon Lord", self.player).place_locked_item(self.create_item("Win"))
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Win", self.player)
