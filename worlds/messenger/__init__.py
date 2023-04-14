import logging
from typing import Dict, Any, Optional, List

from BaseClasses import Tutorial, ItemClassification
from worlds.AutoWorld import World, WebWorld
from .Constants import NOTES, PHOBEKINS, ALL_ITEMS, ALWAYS_LOCATIONS, SEALS, BOSS_LOCATIONS
from .Options import messenger_options, NotesNeeded, Goal, PowerSeals, Logic
from .Regions import REGIONS, REGION_CONNECTIONS, MEGA_SHARDS
from .SubClasses import MessengerRegion, MessengerItem
from . import Rules


class MessengerWeb(WebWorld):
    theme = "ocean"

    bug_report_page = "https://github.com/alwaysintreble/TheMessengerRandomizerModAP/issues"

    tut_en = Tutorial(
        "Multiworld Setup Tutorial",
        "A guide to setting up The Messenger randomizer on your computer.",
        "English",
        "setup_en.md",
        "setup/en",
        ["alwaysintreble"],
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
        "Notes": set(NOTES),
        "Keys": set(NOTES),
        "Crest": {"Sun Crest", "Moon Crest"},
        "Phobe": set(PHOBEKINS),
        "Phobekin": set(PHOBEKINS),
        "Shuriken": {"Windmill Shuriken"},
    }

    option_definitions = messenger_options

    base_offset = 0xADD_000
    item_name_to_id = {item: item_id
                       for item_id, item in enumerate(ALL_ITEMS, base_offset)}
    mega_shard_locs = [shard for region in MEGA_SHARDS for shard in MEGA_SHARDS[region]]
    location_name_to_id = {location: location_id
                           for location_id, location in
                           enumerate([
                               *ALWAYS_LOCATIONS,
                               *SEALS,
                               *mega_shard_locs,
                               *BOSS_LOCATIONS,
                           ], base_offset)}

    data_version = 2
    required_client_version = (0, 3, 9)

    web = MessengerWeb()

    total_seals: int = 0
    required_seals: int = 0

    def generate_early(self) -> None:
        if self.multiworld.goal[self.player] == Goal.option_power_seal_hunt:
            self.multiworld.shuffle_seals[self.player].value = PowerSeals.option_true
            self.total_seals = self.multiworld.total_seals[self.player].value

    def create_regions(self) -> None:
        for region in [MessengerRegion(reg_name, self) for reg_name in REGIONS]:
            if region.name in REGION_CONNECTIONS:
                region.add_exits(REGION_CONNECTIONS[region.name])

    def create_items(self) -> None:
        itempool: List[MessengerItem] = []
        if self.multiworld.goal[self.player] == Goal.option_open_music_box:
            notes = self.multiworld.random.sample(NOTES, k=len(NOTES))
            precollected_notes_amount = NotesNeeded.range_end - self.multiworld.notes_needed[self.player]
            if precollected_notes_amount:
                for note in notes[:precollected_notes_amount]:
                    self.multiworld.push_precollected(self.create_item(note))
            itempool += [self.create_item(note) for note in notes[precollected_notes_amount:]]

        itempool += [self.create_item(item)
                     for item in self.item_name_to_id
                     if item not in
                     {
                         "Power Seal", "Time Shard", *NOTES,
                         *{collected_item.name for collected_item in self.multiworld.precollected_items[self.player]},
                         # this is a set and currently won't create items for anything that appears in here at all
                         # if we get in a position where this can have duplicates of items that aren't Power Seals
                         # or Time shards, this will need to be redone.
                     }]

        if self.multiworld.goal[self.player] == Goal.option_power_seal_hunt:
            total_seals = min(len(self.multiworld.get_unfilled_locations(self.player)) - len(itempool),
                              self.multiworld.total_seals[self.player].value)
            if total_seals < self.total_seals:
                logging.warning(f"Not enough locations for total seals setting. Adjusting to {total_seals}")
                self.total_seals = total_seals
            self.required_seals = int(self.multiworld.percent_seals_required[self.player].value / 100 * self.total_seals)

            seals = [self.create_item("Power Seal") for _ in range(self.total_seals)]
            for i in range(self.required_seals):
                seals[i].classification = ItemClassification.progression_skip_balancing
            itempool += seals

        itempool += [self.create_filler()
                     for _ in range(len(self.multiworld.get_unfilled_locations(self.player)) - len(itempool))]

        self.multiworld.itempool += itempool

    def set_rules(self) -> None:
        logic = self.multiworld.logic_level[self.player]
        if logic == Logic.option_normal:
            Rules.MessengerRules(self).set_messenger_rules()
        elif logic == Logic.option_hard:
            Rules.MessengerHardRules(self).set_messenger_rules()
        elif logic == Logic.option_challenging:
            Rules.MessengerChallengeRules(self).set_messenger_rules()
        else:
            Rules.MessengerOOBRules(self).set_messenger_rules()

    def fill_slot_data(self) -> Dict[str, Any]:
        locations: Dict[int, List[str]] = {}
        for loc in self.multiworld.get_filled_locations(self.player):
            if loc.item.code:
                locations[loc.address] = [loc.item.name, self.multiworld.player_name[loc.item.player]]

        return {
            "deathlink": self.multiworld.death_link[self.player].value,
            "goal": self.multiworld.goal[self.player].current_key,
            "music_box": self.multiworld.music_box[self.player].value,
            "required_seals": self.required_seals,
            "locations": locations,
            "settings": {
                "Difficulty": "Basic" if not self.multiworld.shuffle_seals[self.player] else "Advanced",
                "Mega Shards": self.multiworld.shuffle_shards[self.player].value
            },
            "logic": self.multiworld.logic_level[self.player].current_key,
        }

    def get_filler_item_name(self) -> str:
        return "Time Shard"

    def create_item(self, name: str) -> MessengerItem:
        item_id: Optional[int] = self.item_name_to_id.get(name, None)
        override_prog = name in {"Windmill Shuriken"} and getattr(self, "multiworld") is not None \
            and self.multiworld.logic_level[self.player] > Logic.option_normal
        return MessengerItem(name, self.player, item_id, override_prog)
