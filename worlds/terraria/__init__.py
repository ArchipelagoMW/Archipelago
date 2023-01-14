from worlds.AutoWorld import World
from worlds.generic.Rules import add_rule
from BaseClasses import Region, RegionType, ItemClassification
from .Checks import item_name_to_id, location_name_to_id, TerrariaItem, locations, TerrariaLocation, items, precollected
from .Options import options

class TerrariaWorld(World):
    """Terraria is a 2D sandbox video game."""
    game: str = "Terraria"
    topology_present: bool = True
    option_definitions = options

    # data_version is used to signal that items, locations or their names
    # changed. Set this to 0 during development so other games' clients do not
    # cache any texts, then increase by 1 for each release that makes changes.
    data_version = 0

    item_name_to_id = item_name_to_id
    location_name_to_id = location_name_to_id

    def create_item(self, name: str) -> TerrariaItem:
        classification = ItemClassification.useful
        if name in {
            "Post-Eye of Cthulhu",
            "Post-Eater of Worlds or Brain of Cthulhu",
            "Post-Skeletron",
            "Hardmode",
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
        for location in locations:
            menu.locations.append(TerrariaLocation(self.player, location, location_name_to_id[location], menu))
        self.multiworld.regions.append(menu)

    def create_items(self) -> None:
        items_to_create = items.copy()
        for item in precollected:
            items_to_create.remove(item)
        items_to_create.remove("Victory")
        for _ in range(len(precollected)):
            items_to_create.append("Nothing")
        for item in map(self.create_item, items_to_create):
            self.multiworld.itempool.append(item)

    def set_rules(self) -> None:
        # TODO some of these might be wrong ex. Old One's Army might not check for previous bosses
        add_rule(self.multiworld.get_location("Old One's Army Tier 1", self.player), lambda state: state.has("Post-Eater of Worlds or Brain of Cthulhu", self.player))
        add_rule(self.multiworld.get_location("Pirate Invasion", self.player), lambda state: state.has("Hardmode", self.player))
        add_rule(self.multiworld.get_location("Frost Legion", self.player), lambda state: state.has_all({"Post-Skeletron", "Hardmode", "Post-Plantera"}, self.player))
        add_rule(self.multiworld.get_location("Queen Slime", self.player), lambda state: state.has("Hardmode", self.player))
        add_rule(self.multiworld.get_location("The Twins", self.player), lambda state: state.has("Hardmode", self.player))
        add_rule(self.multiworld.get_location("The Destroyer", self.player), lambda state: state.has("Hardmode", self.player))
        add_rule(self.multiworld.get_location("Skeletron Prime", self.player), lambda state: state.has_all({"Post-Skeletron", "Hardmode"}, self.player))
        add_rule(self.multiworld.get_location("Old One's Army Tier 2", self.player), lambda state: state.has_any({"Post-The Twins", "Post-The Destroyer", "Post-Skeletron Prime", "Post-Golem"}, self.player) and state.has_all({"Post-Eater of Worlds or Brain of Cthulhu", "Hardmode"}, self.player))
        add_rule(self.multiworld.get_location("Plantera", self.player), lambda state: state.has_all({"Hardmode", "Post-The Twins", "Post-The Destroyer", "Post-Skeletron Prime"}, self.player))
        # Golem can be accessed with HOIKing, which could be relevant to settings
        add_rule(self.multiworld.get_location("Golem", self.player), lambda state: (state.has_all({"Post-The Twins", "Post-The Destroyer", "Post-Skeletron Prime"}, self.player) or state.has("Post-Golem", self.player)) and state.has_all({"Hardmode", "Post-Plantera"}, self.player))
        add_rule(self.multiworld.get_location("Old One's Army Tier 3", self.player), lambda state: state.has_all({"Post-Eater of Worlds or Brain of Cthulhu", "Hardmode", "Post-Golem"}, self.player))
        add_rule(self.multiworld.get_location("Martian Madness", self.player), lambda state: state.has_all({"Hardmode", "Post-Golem"}, self.player))
        add_rule(self.multiworld.get_location("Duke Fishron", self.player), lambda state: state.has("Hardmode", self.player))

        for boss in ["Mourning Wood", "Pumpking"]:
            add_rule(self.multiworld.get_location(boss, self.player), lambda state: state.has_all({"Post-Skeletron", "Hardmode", "Post-Plantera"}, self.player) and state.has_any({"Post-Eye of Cthulhu", "Post-Eater of Worlds or Brain of Cthulhu", "Post-Skeletron"}, self.player))

        for boss in ["Everscream", "Santa-NK1", "Ice Queen"]:
            add_rule(self.multiworld.get_location(boss, self.player), lambda state: state.has_all({"Post-Skeletron", "Hardmode", "Post-Plantera"}, self.player))

        add_rule(self.multiworld.get_location("Empress of Light", self.player), lambda state: state.has_all({"Hardmode", "Post-Plantera"}, self.player))
        add_rule(self.multiworld.get_location("Lunatic Cultist", self.player), lambda state: state.has_all({"Hardmode", "Post-Skeletron", "Post-Golem"}, self.player))
        add_rule(self.multiworld.get_location("Lunar Events", self.player), lambda state: state.has_all({"Hardmode", "Post-Skeletron", "Post-Golem"}, self.player))
        add_rule(self.multiworld.get_location("Moon Lord", self.player), lambda state: state.has_all({"Hardmode", "Post-Skeletron", "Post-Golem"}, self.player))

    def generate_basic(self) -> None:
        for item in precollected:
            self.multiworld.push_precollected(self.create_item(item))
        self.multiworld.get_location("Moon Lord", self.player).place_locked_item(self.create_item("Victory"))
        # self.multiworld.get_location("Zenith", self.player).place_locked_item(self.create_item("Victory"))
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)
