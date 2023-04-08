from BaseClasses import Entrance, Item, ItemClassification, Location, MultiWorld, Region, Tutorial
from worlds.AutoWorld import WebWorld, World
from worlds.generic.Rules import set_rule
from .Options import clique_options


class CliqueItem(Item):
    game = "Clique"


class CliqueLocation(Location):
    game = "Clique"


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
    data_version = 2
    web = CliqueWebWorld()
    option_definitions = clique_options

    # Yes, I'm like 12 for this.
    location_name_to_id = {
        "The Big Red Button":   69696969,
        "The Item on the Desk": 69696968,
    }

    item_name_to_id = {
        "Feeling of Satisfaction": 69696969,
        "Button Activation":       69696968,
    }

    def create_item(self, name: str) -> CliqueItem:
        return CliqueItem(name, ItemClassification.progression, self.item_name_to_id[name], self.player)

    def create_items(self) -> None:
        self.multiworld.itempool.append(self.create_item("Feeling of Satisfaction"))
        self.multiworld.priority_locations[self.player].value.add("The Big Red Button")

        if self.multiworld.hard_mode[self.player]:
            self.multiworld.itempool.append(self.create_item("Button Activation"))

    def create_regions(self) -> None:
        if self.multiworld.hard_mode[self.player]:
            self.multiworld.regions += [
                create_region(self.multiworld, self.player, "Menu", None, ["The entrance to the button."]),
                create_region(self.multiworld, self.player, "The realm of the button.", self.location_name_to_id)
            ]
        else:
            self.multiworld.regions += [
                create_region(self.multiworld, self.player, "Menu", None, ["The entrance to the button."]),
                create_region(self.multiworld, self.player, "The realm of the button.", {
                    "The Big Red Button": 69696969
                })]

        self.multiworld.get_entrance("The entrance to the button.", self.player) \
            .connect(self.multiworld.get_region("The realm of the button.", self.player))

    def get_filler_item_name(self) -> str:
        return self.multiworld.random.choice(self.item_name_to_id)

    def set_rules(self) -> None:
        if self.multiworld.hard_mode[self.player]:
            set_rule(
                self.multiworld.get_location("The Big Red Button", self.player),
                lambda state: state.has("Button Activation", self.player))

        self.multiworld.completion_condition[self.player] = lambda state: \
            state.has("Feeling of Satisfaction", self.player)


def create_region(world: MultiWorld, player: int, name: str, locations=None, exits=None):
    region = Region(name, player, world)
    if locations:
        for location_name in locations.keys():
            region.locations.append(CliqueLocation(player, location_name, locations[location_name], region))

    if exits:
        for _exit in exits:
            region.exits.append(Entrance(player, _exit, region))

    return region
