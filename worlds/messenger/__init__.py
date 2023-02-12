from typing import Dict, Any, List

from BaseClasses import Tutorial, ItemClassification
from Options import Accessibility
from worlds.AutoWorld import World, WebWorld
from .Constants import NOTES, PROG_ITEMS, PHOBEKINS, USEFUL_ITEMS, JUNK, ALWAYS_LOCATIONS, SEALS, ALL_ITEMS
from .Options import messenger_options, NotesNeeded, Goal, PowerSeals
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
    """
    As a demon army besieges his village, a young ninja ventures through a cursed world, to deliver a scroll paramount
    to his clan’s survival. What begins as a classic action platformer soon unravels into an expansive time-traveling
    adventure full of thrills, surprises, and humor.
    """
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
    total_seals: int
    required_seals: int

    def generate_early(self) -> None:
        self.rules = MessengerRules(self.player)
        if self.multiworld.goal[self.player] == Goal.option_shop_chest:
            self.multiworld.shuffle_seals[self.player].value = PowerSeals.option_true
            self.total_seals = self.multiworld.total_seals[self.player].value
            self.required_seals = int(self.multiworld.percent_seals_required[self.player].value / 100 * self.total_seals)
        else:
            self.total_seals = 0
            self.required_seals = 0

    def create_regions(self) -> None:
        for region in REGIONS:
            MessengerRegion(region, self)

        for reg_name, exits in REGION_CONNECTIONS.items():
            region = self.multiworld.get_region(reg_name, self.player)
            if type(region) is not MessengerRegion:
                raise KeyError(f"Tried to get {region} for player {self.player} but isn't of type {MessengerRegion}")
            region.add_exits(exits)

    def create_items(self) -> None:
        itempool = []
        if self.multiworld.goal[self.player] == Goal.option_shop_chest:
            seals = [self.create_item("Power Seal") for _ in range(self.total_seals)]
            for i in range(self.required_seals):
                seals[i].classification = ItemClassification.progression_skip_balancing
            itempool += seals
        else:
            precollected_notes_amount = NotesNeeded.range_end - self.multiworld.notes_needed[self.player].value
            if precollected_notes_amount:
                notes = NOTES.copy()
                self.multiworld.random.shuffle(notes)
                notes = notes[:precollected_notes_amount]
                for note in notes:
                    self.multiworld.push_precollected(self.create_item(note))
                itempool += [self.create_item(note) for note in NOTES if note not in notes]
            else:
                itempool += [self.create_item(note) for note in NOTES]

        itempool += [self.create_item(item)
                     for item in self.item_name_to_id
                     if item not in
                     {
                         "Power Seal", "Time Shard", *NOTES,
                         *{collected_item.name for collected_item in self.multiworld.precollected_items[self.player]}
                         # this is a set and currently won't create items for anything that appears in here at all
                         # if we get in a position where this can have duplicates of items that aren't Power Seals
                         # or Time shards, this will need to be redone.
                      }]
        itempool += [self.create_filler()
                     for _ in range(len(self.multiworld.get_unfilled_locations(self.player)) - len(itempool))]

        self.multiworld.itempool += itempool

    def set_rules(self) -> None:
        if self.multiworld.goal[self.player] == Goal.option_shop_chest:
            self.multiworld.get_location("Shop Chest", self.player).access_rule = lambda state: state.has("Power Seal", self.player, self.required_seals)

        if self.multiworld.enable_logic[self.player]:
            if self.multiworld.goal[self.player] == Goal.option_shop_chest:
                self.multiworld.completion_condition[self.player] = lambda state: state.has("Shop Chest", self.player)
            else:
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
            "goal": self.multiworld.goal[self.player].current_key,
            "required_seals": self.required_seals,
            "locations": locations,
            "settings": {"Difficulty": "Basic" if not self.multiworld.shuffle_seals[self.player] else "Advanced"}
        }

    def get_filler_item_name(self) -> str:
        return "Time Shard"

    def create_item(self, name: str) -> MessengerItem:
        item_id = self.item_name_to_id[name] if name in self.item_name_to_id else None
        return MessengerItem(name, self.player, item_id)

