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
        if name in [
            "Dryad",
            "Progressive Old One's Army",
            "Progressive Dungeon",
            "Hardmode",
            "Underground Evil",
            "Hallow",
            "Truffle Worm",
            "Plantera's Bulb",
            "Lihzahrd Altar",
            "Prismatic Lacewing",
            "Martian Probe",
            "Cultists",
            # "Post-Plantera Eclipse" # Temp
            # "Zenith", # Temp
            "Victory",
        ]:
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
        for _ in range(2):
            items_to_create.append("Progressive Old One's Army")
        items_to_create.append("Progressive Dungeon")
        for item in precollected:
            items_to_create.remove(item)
        items_to_create.remove("Victory")
        # items_to_create.remove("Nothing")
        for _ in range(len(precollected)):
            items_to_create.append("Nothing")
        for item in map(self.create_item, items_to_create):
            self.multiworld.itempool.append(item)

    def set_rules(self) -> None:
        add_rule(self.multiworld.get_location("Old One's Army Tier 1", self.player), lambda state: state.has("Progressive Old One's Army", self.player))
        add_rule(self.multiworld.get_location("Pirate Invasion", self.player), lambda state: state.has("Hardmode", self.player))
        add_rule(self.multiworld.get_location("Frost Legion", self.player), lambda state: state.has("Progressive Dungeon", self.player, 2) and state.has_all({"Hardmode", "Hallow", "Underground Evil"}, self.player))
        add_rule(self.multiworld.get_location("Queen Slime", self.player), lambda state: state.has("Hallow", self.player))
        add_rule(self.multiworld.get_location("The Twins", self.player), lambda state: state.has_all({"Hardmode", "Hallow"}, self.player))
        add_rule(self.multiworld.get_location("The Destroyer", self.player), lambda state: state.has_all({"Hardmode", "Underground Evil"}, self.player))
        add_rule(self.multiworld.get_location("Skeletron Prime", self.player), lambda state: state.has_all({"Progressive Dungeon", "Hardmode", "Underground Evil", "Hallow"}, self.player))
        add_rule(self.multiworld.get_location("Old One's Army Tier 2", self.player), lambda state: state.has("Progressive Old One's Army", self.player, 2))
        add_rule(self.multiworld.get_location("Plantera", self.player), lambda state: state.has("Plantera's Bulb", self.player))
        # Golem can be accessed with HOIKing, which could be relevant for some goals / settings
        add_rule(self.multiworld.get_location("Golem", self.player), lambda state: state.has_any({"Plantera's Bulb", "Cultists"}, self.player) and state.has("Lihzahrd Altar", self.player))
        add_rule(self.multiworld.get_location("Old One's Army Tier 3", self.player), lambda state: state.has("Progressive Old One's Army", self.player, 3))
        add_rule(self.multiworld.get_location("Martian Madness", self.player), lambda state: state.has("Martian Probe", self.player))
        add_rule(self.multiworld.get_location("Duke Fishron", self.player), lambda state: state.has("Truffle Worm", self.player))
        add_rule(self.multiworld.get_location("Pumpkin Moon", self.player), lambda state: state.has("Progressive Dungeon", self.player, 2) and state.has_all({"Dryad", "Hardmode"}, self.player) and (state.has_any({"Hallow", "Underground Evil"}, self.player)))
        add_rule(self.multiworld.get_location("Frost Moon", self.player), lambda state: state.has("Progressive Dungeon", self.player, 2) and state.has_all({"Hardmode", "Hallow", "Underground Evil"}, self.player))
        add_rule(self.multiworld.get_location("Empress of Light", self.player), lambda state: state.has_all({"Hallow", "Prismatic Lacewing"}, self.player))
        add_rule(self.multiworld.get_location("Lunatic Cultist", self.player), lambda state: state.has("Cultists", self.player))
        add_rule(self.multiworld.get_location("Lunar Events", self.player), lambda state: state.has("Cultists", self.player))
        add_rule(self.multiworld.get_location("Moon Lord", self.player), lambda state: state.has("Cultists", self.player))
        # add_rule(self.multiworld.get_location("Zenith", self.player), lambda state: state.has_all({"Dryad", "Hardmode", "Underground Evil", "Hallow", "Plantera's Bulb", "Post-Plantera Eclipse", "Martian Probe", "Cultists"}, self.player) and state.has("Progressive Dungeon", self.player, 2))

    def generate_basic(self) -> None:
        for item in precollected:
            self.multiworld.push_precollected(self.create_item(item))
        self.multiworld.get_location("Moon Lord", self.player).place_locked_item(self.create_item("Victory"))
        # self.multiworld.get_location("Zenith", self.player).place_locked_item(self.create_item("Victory"))
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)
