import logging
from typing import Any, ClassVar, TextIO

from BaseClasses import CollectionState, Entrance, Item, ItemClassification, MultiWorld, Tutorial
from Options import Accessibility
from Utils import output_path
from settings import FilePath, Group
from worlds.AutoWorld import WebWorld, World
from worlds.LauncherComponents import Component, Type, components
from .client_setup import launch_game
from .connections import CONNECTIONS, RANDOMIZED_CONNECTIONS, TRANSITIONS
from .constants import ALL_ITEMS, ALWAYS_LOCATIONS, BOSS_LOCATIONS, FILLER, NOTES, PHOBEKINS, PROG_ITEMS, TRAPS, \
    USEFUL_ITEMS
from .options import AvailablePortals, Goal, Logic, MessengerOptions, NotesNeeded, ShuffleTransitions
from .portals import PORTALS, add_closed_portal_reqs, disconnect_portals, shuffle_portals, validate_portals
from .regions import LEVELS, MEGA_SHARDS, LOCATIONS, REGION_CONNECTIONS
from .rules import MessengerHardRules, MessengerOOBRules, MessengerRules
from .shop import FIGURINES, PROG_SHOP_ITEMS, SHOP_ITEMS, USEFUL_SHOP_ITEMS, shuffle_shop_prices
from .subclasses import MessengerEntrance, MessengerItem, MessengerRegion, MessengerShopLocation

components.append(
    Component("The Messenger", component_type=Type.CLIENT, func=launch_game, game_name="The Messenger", supports_uri=True)
)


class MessengerSettings(Group):
    class GamePath(FilePath):
        description = "The Messenger game executable"
        is_exe = True
        md5s = ["1b53534569060bc06179356cd968ed1d"]

    game_path: GamePath = GamePath("TheMessenger.exe")


class MessengerWeb(WebWorld):
    theme = "ocean"

    bug_report_page = "https://github.com/alwaysintreble/TheMessengerRandomizerModAP/issues"

    tut_en = Tutorial(
        "Multiworld Setup Guide",
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
    location_name_groups = {
        "Notes": {
            "Autumn Hills - Key of Hope",
            "Searing Crags - Key of Strength",
            "Underworld - Key of Chaos",
            "Sunken Shrine - Key of Love",
            "Elemental Skylands - Key of Symbiosis",
            "Corrupted Future - Key of Courage",
        },
        "Keys": {
            "Autumn Hills - Key of Hope",
            "Searing Crags - Key of Strength",
            "Underworld - Key of Chaos",
            "Sunken Shrine - Key of Love",
            "Elemental Skylands - Key of Symbiosis",
            "Corrupted Future - Key of Courage",
        },
        "Phobe": {
            "Catacombs - Necro",
            "Bamboo Creek - Claustro",
            "Searing Crags - Pyro",
            "Cloud Ruins - Acro",
        },
        "Phobekin": {
            "Catacombs - Necro",
            "Bamboo Creek - Claustro",
            "Searing Crags - Pyro",
            "Cloud Ruins - Acro",
        },
    }

    required_client_version = (0, 4, 4)

    web = MessengerWeb()

    total_seals: int = 0
    required_seals: int = 0
    created_seals: int = 0
    total_shards: int = 0
    shop_prices: dict[str, int]
    figurine_prices: dict[str, int]
    _filler_items: list[str]
    starting_portals: list[str]
    plando_portals: list[str]
    spoiler_portal_mapping: dict[str, str]
    portal_mapping: list[int]
    transitions: list[Entrance]
    reachable_locs: int = 0
    filler: dict[str, int]

    def generate_early(self) -> None:
        if self.options.goal == Goal.option_power_seal_hunt:
            self.total_seals = self.options.total_seals.value

        if self.options.limited_movement:
            self.options.accessibility.value = Accessibility.option_minimal
            if self.options.logic_level < Logic.option_hard:
                self.options.logic_level.value = Logic.option_hard

        if self.options.early_meditation:
            self.multiworld.early_items[self.player]["Meditation"] = 1

        self.shop_prices, self.figurine_prices = shuffle_shop_prices(self)

        starting_portals = ["Autumn Hills", "Howling Grotto", "Glacial Peak", "Riviere Turquoise", "Sunken Shrine", "Searing Crags"]
        self.starting_portals = [f"{portal} Portal"
                                 for portal in starting_portals[:3] +
                                 self.random.sample(starting_portals[3:], k=self.options.available_portals - 3)]

        # super complicated method for adding searing crags to starting portals if it wasn't chosen
        # TODO add a check for transition shuffle when that gets added back in
        if not self.options.shuffle_portals and "Searing Crags Portal" not in self.starting_portals:
            self.starting_portals.append("Searing Crags Portal")
            portals_to_strip = [portal for portal in ["Riviere Turquoise Portal", "Sunken Shrine Portal"]
                                if portal in self.starting_portals]
            if portals_to_strip:
                self.starting_portals.remove(self.random.choice(portals_to_strip))

        self.filler = FILLER.copy()
        if self.options.traps:
            self.filler.update(TRAPS)

        self.plando_portals = []
        self.portal_mapping = []
        self.spoiler_portal_mapping = {}
        self.transitions = []

    def create_regions(self) -> None:
        # MessengerRegion adds itself to the multiworld
        # create simple regions
        simple_regions = [MessengerRegion(level, self) for level in LEVELS]
        # create complex regions that have sub-regions
        complex_regions = [MessengerRegion(f"{parent} - {reg_name}", self, parent)
                           for parent, sub_region in CONNECTIONS.items()
                           for reg_name in sub_region]

        for region in complex_regions:
            region_name = region.name.removeprefix(f"{region.parent} - ")
            connection_data = CONNECTIONS[region.parent][region_name]
            for exit_region in connection_data:
                region.connect(self.multiworld.get_region(exit_region, self.player))

        # all regions need to be created before i can do these connections so we create and connect the complex first
        for region in [level for level in simple_regions if level.name in REGION_CONNECTIONS]:
            region.add_exits(REGION_CONNECTIONS[region.name])

    def create_items(self) -> None:
        # create items that are always in the item pool
        main_movement_items = ["Rope Dart", "Wingsuit"]
        precollected_names = [item.name for item in self.multiworld.precollected_items[self.player]]
        itempool: list[MessengerItem] = [
            self.create_item(item)
            for item in self.item_name_to_id
            if item not in {
                "Power Seal", *NOTES, *FIGURINES, *main_movement_items,
                *precollected_names, *FILLER, *TRAPS,
            }
        ]

        if self.options.limited_movement:
            itempool.append(self.create_item(self.random.choice(main_movement_items)))
        else:
            itempool += [self.create_item(move_item) for move_item in main_movement_items]

        if self.options.goal == Goal.option_open_music_box:
            # make a list of all notes except those in the player's defined starting inventory, and adjust the
            # amount we need to put in the itempool and precollect based on that
            notes = [note for note in NOTES if note not in precollected_names]
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
                logging.warning(
                    f"Not enough locations for total seals setting "
                    f"({self.options.total_seals}). Adjusting to {total_seals}"
                )
                self.total_seals = total_seals
            self.required_seals = int(self.options.percent_seals_required.value / 100 * self.total_seals)

            seals = [self.create_item("Power Seal") for _ in range(self.total_seals)]
            itempool += seals

        self.multiworld.itempool += itempool
        remaining_fill = len(self.multiworld.get_unfilled_locations(self.player)) - len(itempool)
        if remaining_fill < 10:
            self._filler_items = self.random.choices(
                list(self.filler)[2:],
                weights=list(self.filler.values())[2:],
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
            raise ValueError(f"Somehow you have a logic option that's currently invalid."
                             f" {logic} for {self.multiworld.get_player_name(self.player)}")
        #     MessengerOOBRules(self).set_messenger_rules()

        add_closed_portal_reqs(self)
        # i need portal shuffle to happen after rules exist so i can validate it
        attempts = 5
        if self.options.shuffle_portals:
            self.portal_mapping = []
            self.spoiler_portal_mapping = {}
            for _ in range(attempts):
                disconnect_portals(self)
                shuffle_portals(self)
                if validate_portals(self):
                    break
            # failsafe mostly for invalid plandoed portals with no transition shuffle
            else:
                raise RuntimeError("Unable to generate valid portal output.")

    def write_spoiler_header(self, spoiler_handle: TextIO) -> None:
        if self.options.available_portals < 6:
            spoiler_handle.write(f"\nStarting Portals:\n\n")
            for portal in self.starting_portals:
                spoiler_handle.write(f"{portal}\n")

        spoiler = self.multiworld.spoiler

        if self.options.shuffle_portals:
            # sort the portals as they appear left to right in-game
            portal_info = sorted(
                self.spoiler_portal_mapping.items(),
                key=lambda portal:
                ["Autumn Hills", "Riviere Turquoise",
                 "Howling Grotto", "Sunken Shrine",
                 "Searing Crags", "Glacial Peak"].index(portal[0]))
            for portal, output in portal_info:
                spoiler.set_entrance(f"{portal} Portal", output, "I can write anything I want here lmao", self.player)

    def fill_slot_data(self) -> dict[str, Any]:
        slot_data = {
            "shop": {SHOP_ITEMS[item].internal_name: price for item, price in self.shop_prices.items()},
            "figures": {FIGURINES[item].internal_name: price for item, price in self.figurine_prices.items()},
            "max_price": self.total_shards,
            "required_seals": self.required_seals,
            "starting_portals": self.starting_portals,
            "portal_exits": self.portal_mapping,
            "transitions": [[TRANSITIONS.index("Corrupted Future") if transition.name == "Artificer's Portal"
                             else TRANSITIONS.index(RANDOMIZED_CONNECTIONS[transition.parent_region.name]),
                             TRANSITIONS.index(transition.connected_region.name)]
                            for transition in self.transitions],
            **self.options.as_dict("music_box", "death_link", "logic_level"),
        }
        return slot_data

    def get_filler_item_name(self) -> str:
        if not getattr(self, "_filler_items", None):
            self._filler_items = [name for name in self.random.choices(
                list(self.filler),
                weights=list(self.filler.values()),
                k=20
            )]
        return self._filler_items.pop(0)

    def create_item(self, name: str) -> MessengerItem:
        item_id: int | None = self.item_name_to_id.get(name, None)
        return MessengerItem(
            name,
            ItemClassification.progression if item_id is None else self.get_item_classification(name),
            item_id,
            self.player
        )

    def get_item_classification(self, name: str) -> ItemClassification:
        if "Time Shard " in name:
            count = int(name.strip("Time Shard ()"))
            count = count if count >= 100 else 0
            self.total_shards += count
            return ItemClassification.progression_skip_balancing if count else ItemClassification.filler

        if name == "Windmill Shuriken" and getattr(self, "multiworld", None) is not None:
            return ItemClassification.progression if self.options.logic_level else ItemClassification.filler

        if name == "Power Seal":
            self.created_seals += 1
            return ItemClassification.progression_skip_balancing \
                if self.required_seals >= self.created_seals else ItemClassification.filler

        if name in {*NOTES, *PROG_ITEMS, *PHOBEKINS, *PROG_SHOP_ITEMS}:
            return ItemClassification.progression

        if name in {*USEFUL_ITEMS, *USEFUL_SHOP_ITEMS}:
            return ItemClassification.useful
        
        if name in TRAPS:
            return ItemClassification.trap

        return ItemClassification.filler

    @classmethod
    def create_group(cls, multiworld: "MultiWorld", new_player_id: int, players: set[int]) -> World:
        group = super().create_group(multiworld, new_player_id, players)
        assert isinstance(group, MessengerWorld)
        
        group.filler = FILLER.copy()
        group.options.traps.value = all(multiworld.worlds[player].options.traps for player in players)
        if group.options.traps:
            group.filler.update(TRAPS)
        return group

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

    @classmethod
    def stage_generate_output(cls, multiworld: MultiWorld, output_directory: str) -> None:
        # using stage_generate_output because it doesn't increase the logged player count for players without output
        # only generate output if there's a single player
        if multiworld.players > 1:
            return
        # the messenger client calls into AP with specific args, so check the out path matches what the client sends
        out_path = output_path(multiworld.get_out_file_name_base(1) + ".aptm")
        if "The Messenger\\Archipelago\\output" not in out_path:
            return
        import orjson
        data = {
            "name": multiworld.get_player_name(1),
            "slot_data": multiworld.worlds[1].fill_slot_data(),
            "loc_data": {loc.address: {loc.item.name: [loc.item.code, loc.item.flags]}
                         for loc in multiworld.get_filled_locations() if loc.address},
        }
    
        output = orjson.dumps(data, option=orjson.OPT_NON_STR_KEYS)
        with open(out_path, "wb") as f:
            f.write(output)
