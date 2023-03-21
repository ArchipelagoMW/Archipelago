from BaseClasses import Entrance, Item, ItemClassification, Location, MultiWorld, Region, Tutorial
from worlds.AutoWorld import WebWorld, World
from worlds.generic.Rules import set_rule
from .Options import clique_options

item_table = {
    "The feeling of satisfaction.": 69696969,
    "Button Key": 69696968,
}

location_table = {
    "The Button": 69696969,
    "The Desk": 69696968,
}


class CliqueWebWorld(WebWorld):
    theme = "partyTime"
    tutorials = [
        Tutorial(
            tutorial_name="Start Guide",
            description="A guide to playing Clique.",
            language="English",
            file_name="guide_en.md",
            link="guide/en",
            authors=["Phar"]
        )
    ]


class CliqueWorld(World):
    """The greatest game ever designed. Full of exciting gameplay!"""

    game = "Clique"
    topology_present = False
    data_version = 1
    web = CliqueWebWorld()
    option_definitions = clique_options

    location_name_to_id = location_table
    item_name_to_id = item_table

    def create_item(self, name: str) -> "Item":
        return Item(name, ItemClassification.progression, self.item_name_to_id[name], self.player)

    def get_setting(self, name: str):
        return getattr(self.multiworld, name)[self.player]

    def fill_slot_data(self) -> dict:
        return {option_name: self.get_setting(option_name).value for option_name in self.option_definitions}

    def generate_basic(self) -> None:
        self.multiworld.itempool.append(self.create_item("The feeling of satisfaction."))

        if self.multiworld.hard_mode[self.player]:
            self.multiworld.itempool.append(self.create_item("Button Key"))

    def create_regions(self) -> None:
        if self.multiworld.hard_mode[self.player]:
            self.multiworld.regions += [
                create_region(self.multiworld, self.player, "Menu", None, ["Entrance to THE BUTTON"]),
                create_region(self.multiworld, self.player, "THE BUTTON", self.location_name_to_id)
            ]
        else:
            self.multiworld.regions += [
                create_region(self.multiworld, self.player, "Menu", None, ["Entrance to THE BUTTON"]),
                create_region(self.multiworld, self.player, "THE BUTTON", {"The Button": 69696969})
            ]

        self.multiworld.get_entrance("Entrance to THE BUTTON", self.player)\
            .connect(self.multiworld.get_region("THE BUTTON", self.player))

    def get_filler_item_name(self) -> str:
        return self.multiworld.random.choice(item_table)

    def set_rules(self) -> None:
        if self.multiworld.hard_mode[self.player]:
            set_rule(
                self.multiworld.get_location("The Button", self.player),
                lambda state: state.has("Button Key", self.player)
            )

            self.multiworld.completion_condition[self.player] = lambda state: \
                state.has("Button Key", self.player)
        else:
            self.multiworld.completion_condition[self.player] = lambda state: \
                state.has("The feeling of satisfaction.", self.player)


def create_region(world: MultiWorld, player: int, name: str, locations=None, exits=None):
    region = Region(name, player, world)
    if locations:
        for location_name in locations.keys():
            location = CliqueLocation(player, location_name, locations[location_name], region)
            region.locations.append(location)

    if exits:
        for _exit in exits:
            region.exits.append(Entrance(player, _exit, region))

    return region


class CliqueItem(Item):
    game = "Clique"


class CliqueLocation(Location):
    game: str = "Clique"
