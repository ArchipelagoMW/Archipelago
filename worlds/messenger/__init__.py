from typing import Dict, Any, List

from BaseClasses import Tutorial
from Options import Accessibility
from worlds.AutoWorld import World, WebWorld
from .Constants import NOTES, PROG_ITEMS, PHOBEKINS, USEFUL_ITEMS, JUNK, ALWAYS_LOCATIONS, SEALS, ALL_ITEMS
from .Options import messenger_options, NotesNeeded
from .Regions import REGIONS, REGION_CONNECTIONS
from .Rules import MessengerRules, set_self_locking_items
from .SubClasses import MessengerRegion, MessengerItem


class MessengerWeb(WebWorld):
    theme = "ocean"

    bug_report_page = "https://github.com/minous27/TheMessengerRandomizerMod/issues"

    tut_en = Tutorial(
        "Multiworld Setup Tutorial",
        "A guide to setting up The Messenger randomizer on your computer.",
        "English",
        "setup_en.md",
        "setup/en",
        ["alwaysintreble"]
    )

    tutorials = [tut_en]


class MessengerWorld(World):
    game = "The Messenger"

    item_name_groups = {
        "Notes": NOTES,
        "Keys": NOTES,
        "Crest": {"Sun Crest", "Moon Crest"},
        "Phobe": PHOBEKINS,
        "Phobekin": PHOBEKINS,
        "Shuriken": {"Windmill Shuriken"},
    }

    option_definitions = messenger_options

    base_offset = 0xADD_000
    item_name_to_id = {item: item_id
                       for item_id, item in enumerate(ALL_ITEMS, base_offset)}
    location_name_to_id = {location: location_id
                           for location_id, location in enumerate([*ALWAYS_LOCATIONS, *SEALS], base_offset)}

    data_version = 0

    web = MessengerWeb()

    rules: MessengerRules

    def generate_early(self) -> None:
        self.rules = MessengerRules(self.player)

    def create_regions(self) -> None:
        for region in REGIONS:
            MessengerRegion(region, self)

        for reg_name, exits in REGION_CONNECTIONS.items():
            region = self.multiworld.get_region(reg_name, self.player)
            if type(region) is not MessengerRegion:
                raise KeyError(f"Tried to get {region} for player {self.player} but isn't of type {MessengerRegion}")
            region.add_exits(exits)

    def create_items(self) -> None:
        precollected_amount = NotesNeeded.range_end - self.multiworld.notes_needed[self.player].value
        notes = []
        if precollected_amount:
            notes = NOTES.copy()
            self.multiworld.random.shuffle(notes)
            notes = notes[:precollected_amount]
            for note in notes:
                self.multiworld.push_precollected(self.create_item(note))
        itempool = []
        for item in self.item_name_to_id:
            if item not in {"Power Seal", "Time Shard", *self.multiworld.precollected_items}:  # if we create this with power seal shuffling off we'll have too many items
                itempool.append(self.create_item(item))
        while len(itempool) < len(self.multiworld.get_unfilled_locations(self.player)):
            itempool.append(self.create_filler())

        self.multiworld.itempool += itempool

    def set_rules(self) -> None:
        if self.multiworld.enable_logic[self.player]:
            self.multiworld.completion_condition[self.player] = lambda state: state.has("Rescue Phantom", self.player)
        else:
            self.multiworld.accessibility[self.player].value = Accessibility.option_minimal
        if self.multiworld.accessibility[self.player] == Accessibility.option_items:
            set_self_locking_items(self.multiworld, self.player)

    def fill_slot_data(self) -> Dict[str, Any]:
        locations: Dict[int, List[str]] = {}
        for loc in self.multiworld.get_filled_locations(self.player):
            if loc.item.code:
                locations[loc.address] = [loc.item.name, self.multiworld.player_name[loc.item.player]]

        return {
            "deathlink": bool(self.multiworld.death_link[self.player].value),
            "locations": locations,
            "settings": {"Difficulty": "Basic" if not self.multiworld.shuffle_seals[self.player] else "Advanced"}
        }

    def get_filler_item_name(self) -> str:
        return "Time Shard"

    def create_item(self, name: str) -> MessengerItem:
        item_id = self.item_name_to_id[name] if name in self.item_name_to_id else None
        return MessengerItem(name, self.player, item_id)

