from worlds.AutoWorld import WebWorld, World
from worlds.generic.Rules import add_rule
from BaseClasses import Region, ItemClassification, Tutorial
from .Checks import item_name_to_id, location_name_to_id, TerrariaItem, TerrariaLocation, get_items_locations
from .Options import options

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
    data_version = 0

    item_name_to_id = item_name_to_id
    location_name_to_id = location_name_to_id

    def generate_early(self) -> None:
        self.ter_items, self.ter_locations = get_items_locations(
            self.multiworld.goal[self.player].value,
            self.multiworld.achievements[self.player].value,
            self.multiworld.fill_extra_checks_with[self.player].value
        )

        goal = self.multiworld.goal[self.player].value

        if goal == 0:
            self.goal_location_id = "Wall of Flesh"
            self.goal_item_id = "Hardmode"
        elif goal == 1:
            self.goal_location_id = "Plantera"
            self.goal_item_id = "Post-Plantera"
        elif goal == 2:
            self.goal_location_id = "Moon Lord"
            self.goal_item_id = "Post-Moon Lord"
        elif goal == 3:
            self.goal_location_id = "Zenith"
            self.goal_item_id = "Has Zenith"


    def create_item(self, name: str, event: bool) -> TerrariaItem:
        classification = ItemClassification.useful
        if name in {
            "Post-Goblin Army",
            "Post-Evil Boss",
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
        
        if event:
            id = None
        else:
            id = item_name_to_id[name]

        return TerrariaItem(name, classification, id, self.player)

    def create_regions(self) -> None:
        menu = Region("Menu", self.player, self.multiworld)

        for location in self.ter_locations:
            menu.locations.append(TerrariaLocation(self.player, location, location_name_to_id[location], menu))
        for event in event_rules:
            menu.locations.append(TerrariaLocation(self.player, event, None, menu))
        if self.calamity:
            for event in calamity_event_rules:
                menu.locations.append(TerrariaLocation(self.player, event, None, menu))
            
        self.multiworld.regions.append(menu)

    def create_items(self) -> None:
        items_to_create = self.ter_items.copy()
        items_to_create.remove(self.goal_item_id)
        
        for item in items_to_create:
            self.multiworld.itempool.append(self.create_item(item, False))

    def set_rules(self) -> None:
        player = self.player
        config = RuleConfig(self.calamity)

        for location in self.ter_locations:
            rule = location_rules[location]
            if rule != None:
                add_rule(self.multiworld.get_location(location, self.player), lambda state: rule(Ctx(state, player, config)))
        for event, rule in event_rules.items():
            if rule != None:
                add_rule(self.multiworld.get_location(event, self.player), lambda state: rule(Ctx(state, player, config)))
        if config.clam:
            for event, rule in event_rules.items():
                if rule != None:
                    add_rule(self.multiworld.get_location(event, self.player), lambda state: rule(Ctx(state, player, config)))

    def generate_basic(self) -> None:
        for event in event_rules:
            self.multiworld.get_location(event, self.player).place_locked_item(self.create_item(event, True))
        if self.calamity:
            for event in event_rules:
                self.multiworld.get_location(event, self.player).place_locked_item(self.create_item(event, True))

        self.multiworld.get_location(self.goal_location_id, self.player).place_locked_item(self.create_item(self.goal_item_id, False))
        self.multiworld.completion_condition[self.player] = lambda state: state.has(self.goal_item_id, self.player)
