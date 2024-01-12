import logging
from typing import Any, ClassVar, Dict, List, Optional

from BaseClasses import CollectionState, Item, ItemClassification, Tutorial
from Options import Accessibility
from settings import FilePath, Group
from worlds.AutoWorld import WebWorld, World
from worlds.LauncherComponents import Component, Type, components
from .client_setup import launch_game
from .constants import ALL_ITEMS, ALWAYS_LOCATIONS, BOSS_LOCATIONS, FILLER, NOTES, PHOBEKINS
from .options import AvailablePortals, Goal, Logic, MessengerOptions, NotesNeeded
from .portals import SHUFFLEABLE_PORTAL_ENTRANCES, add_closed_portal_reqs, disconnect_portals, shuffle_portals
from .regions import MEGA_SHARDS, REGIONS, REGION_CONNECTIONS, SEALS
from .rules import MessengerHardRules, MessengerOOBRules, MessengerRules
from .shop import FIGURINES, SHOP_ITEMS, shuffle_shop_prices
from .subclasses import MessengerItem, MessengerRegion

components.append(
    Component("The Messenger", component_type=Type.CLIENT, func=launch_game)
)


class MessengerSettings(Group):
    class GamePath(FilePath):
        description = "The Messenger game executable"
        is_exe = True

    game_path: GamePath = GamePath("TheMessenger.exe")


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
    options_dataclass = MessengerOptions
    options: MessengerOptions
    settings_key = "messenger_settings"
    settings: ClassVar[MessengerSettings]

    base_offset = 0xADD_000
    item_name_to_id = {item: item_id
                       for item_id, item in enumerate(ALL_ITEMS, base_offset)}
    location_name_to_id = {location: location_id
                           for location_id, location in
                           enumerate([
                               *ALWAYS_LOCATIONS,
                               *[seal for seals in SEALS.values() for seal in seals],
                               *[shard for shards in MEGA_SHARDS.values() for shard in shards],
                               *BOSS_LOCATIONS,
                               *[f"The Shop - {shop_loc}" for shop_loc in SHOP_ITEMS],
                               *FIGURINES,
                               "Money Wrench",
                           ], base_offset)}
    item_name_groups = {
        "Notes": set(NOTES),
        "Keys": set(NOTES),
        "Crest": {"Sun Crest", "Moon Crest"},
        "Phobe": set(PHOBEKINS),
        "Phobekin": set(PHOBEKINS),
    }

    required_client_version = (0, 4, 2)

    web = MessengerWeb()

    total_seals: int = 0
    required_seals: int = 0
    total_shards: int = 0
    shop_prices: Dict[str, int]
    figurine_prices: Dict[str, int]
    _filler_items: List[str]
    starting_portals: List[str]
    portal_mapping: List[int]

    def generate_early(self) -> None:
        if self.options.goal == Goal.option_power_seal_hunt:
            self.total_seals = self.options.total_seals.value

        if self.options.limited_movement:
            self.options.accessibility.value = Accessibility.option_minimal
            if self.options.logic_level < Logic.option_hard:
                self.options.logic_level.value = Logic.option_hard

        self.multiworld.early_items[self.player]["Meditation"] = self.options.early_meditation.value

        self.shop_prices, self.figurine_prices = shuffle_shop_prices(self)

        if self.options.available_portals > AvailablePortals.range_start:
            # there's 3 specific portals that the game forces open
            self.starting_portals = self.random.choices(SHUFFLEABLE_PORTAL_ENTRANCES,
                                                        k=self.options.available_portals - 3)

    def create_regions(self) -> None:
        # MessengerRegion adds itself to the multiworld
        for region in [MessengerRegion(reg_name, self) for reg_name in REGIONS]:
            if region.name in REGION_CONNECTIONS:
                region.add_exits(REGION_CONNECTIONS[region.name])

    def create_items(self) -> None:
        # create items that are always in the item pool
        main_movement_items = ["Rope Dart", "Wingsuit"]
        itempool: List[MessengerItem] = [
            self.create_item(item)
            for item in self.item_name_to_id
            if item not in
            {
                "Power Seal", *NOTES, *FIGURINES, *main_movement_items,
                *{collected_item.name for collected_item in self.multiworld.precollected_items[self.player]},
            } and "Time Shard" not in item
        ]

        if self.options.limited_movement:
            itempool.append(self.create_item(self.random.choice(main_movement_items)))
        else:
            itempool += [self.create_item(move_item) for move_item in main_movement_items]

        if self.options.goal == Goal.option_open_music_box:
            # make a list of all notes except those in the player's defined starting inventory, and adjust the
            # amount we need to put in the itempool and precollect based on that
            notes = [note for note in NOTES if note not in self.multiworld.precollected_items[self.player]]
            self.random.shuffle(notes)
            precollected_notes_amount = NotesNeeded.range_end - \
                self.options.notes_needed - \
                (len(NOTES) - len(notes))
            if precollected_notes_amount:
                for note in notes[:precollected_notes_amount]:
                    self.multiworld.push_precollected(self.create_item(note))
                notes = notes[precollected_notes_amount:]
            itempool += [self.create_item(note) for note in notes]

        elif self.options.goal == Goal.option_power_seal_hunt:
            total_seals = min(len(self.multiworld.get_unfilled_locations(self.player)) - len(itempool),
                              self.options.total_seals.value)
            if total_seals < self.total_seals:
                logging.warning(f"Not enough locations for total seals setting "
                                f"({self.options.total_seals}). Adjusting to {total_seals}")
                self.total_seals = total_seals
            self.required_seals = int(self.options.percent_seals_required.value / 100 * self.total_seals)

            seals = [self.create_item("Power Seal") for _ in range(self.total_seals)]
            for i in range(self.required_seals):
                seals[i].classification = ItemClassification.progression_skip_balancing
            itempool += seals

        self.multiworld.itempool += itempool
        remaining_fill = len(self.multiworld.get_unfilled_locations(self.player)) - len(itempool)
        if remaining_fill < 10:
            self._filler_items = self.random.choices(
                                      list(FILLER)[2:],
                                      weights=list(FILLER.values())[2:],
                                      k=remaining_fill
            )
        filler = [self.create_filler() for _ in range(remaining_fill)]

        self.multiworld.itempool += filler

    def set_rules(self) -> None:
        logic = self.options.logic_level
        if logic == Logic.option_normal:
            MessengerRules(self).set_messenger_rules()
        elif logic == Logic.option_hard:
            MessengerHardRules(self).set_messenger_rules()
        else:
            MessengerOOBRules(self).set_messenger_rules()
        add_closed_portal_reqs(self)
        # i need ER to happen after rules exist so i can validate it
        if self.options.shuffle_portals:
            disconnect_portals(self)
            shuffle_portals(self)

    def fill_slot_data(self) -> Dict[str, Any]:
        return {
            "shop": {SHOP_ITEMS[item].internal_name: price for item, price in self.shop_prices.items()},
            "figures": {FIGURINES[item].internal_name: price for item, price in self.figurine_prices.items()},
            "max_price": self.total_shards,
            "required_seals": self.required_seals,
            "starting_portals": self.starting_portals,
            **self.options.as_dict("music_box", "death_link", "logic_level"),
        }

    def get_filler_item_name(self) -> str:
        if not getattr(self, "_filler_items", None):
            self._filler_items = [name for name in self.random.choices(
                list(FILLER),
                weights=list(FILLER.values()),
                k=20
            )]
        return self._filler_items.pop(0)

    def create_item(self, name: str) -> MessengerItem:
        item_id: Optional[int] = self.item_name_to_id.get(name, None)
        override_prog = getattr(self, "multiworld") is not None and \
            name in {"Windmill Shuriken"} and \
            self.options.logic_level > Logic.option_normal
        count = 0
        if "Time Shard " in name:
            count = int(name.strip("Time Shard ()"))
            count = count if count >= 100 else 0
            self.total_shards += count
        return MessengerItem(name, self.player, item_id, override_prog, count)

    def collect(self, state: "CollectionState", item: "Item") -> bool:
        change = super().collect(state, item)
        if change and "Time Shard" in item.name:
            state.prog_items[self.player]["Shards"] += int(item.name.strip("Time Shard ()"))
        return change

    def remove(self, state: "CollectionState", item: "Item") -> bool:
        change = super().remove(state, item)
        if change and "Time Shard" in item.name:
            state.prog_items[self.player]["Shards"] -= int(item.name.strip("Time Shard ()"))
        return change
