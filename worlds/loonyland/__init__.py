import logging
from typing import Tuple

from BaseClasses import CollectionState, Item, ItemClassification, Tutorial, EntranceType

from Options import OptionError
from Utils import visualize_regions
from entrance_rando import randomize_entrances, disconnect_entrance_for_randomization
from worlds.AutoWorld import WebWorld, World

from .Data.game_data import (
    VAR_WBOMBS,
    VAR_WHOTPANTS,
    loony_item_table,
    loonyland_location_table,
    loonyland_region_table,
    set_rules, setup_entrances,
)
from .Data.game_data import (
    ll_base_id as loonyland_base_id,
)
from .entrances import LLEntrance
from .flags import LLFlags
from .items import LLItemCat, LoonylandItem
from .locations import LLLocCat, LoonylandLocation
from .options import LoonylandOptions, WinCondition
from .regions import LoonylandRegion
from .rules import have_x_badges


class LoonylandWebWorld(WebWorld):
    rich_text_options_doc = True
    theme = "dirt"

    setup_en = Tutorial(
        tutorial_name="Start Guide",
        description="A guide to playing Loonyland.",
        language="English",
        file_name="setup_en.md",
        link="setup/en",
        authors=["AutomaticFrenzy"],
    )

    tutorials = [setup_en]


class LoonylandWorld(World):
    """
    Loonyland: Halloween Hill is an action-adventure game,
    where you must explore to improve Loony's abilities and gain
    access to ever more dangerous areas, all in an effort to find out
    what lies behind the madness going on in Halloween Hill.
    """

    game = "Loonyland"
    web = LoonylandWebWorld()
    options: LoonylandOptions
    options_dataclass = LoonylandOptions
    location_name_to_id = {name: data.id + loonyland_base_id for name, data in loonyland_location_table.items()}
    item_name_to_id = {name: data.id for name, data in loony_item_table.items()}
    item_name_to_id["Max Life and Gems"] = loonyland_base_id + 3000
    loonyland_entrance_list: list[LLEntrance] = []
    entrance_name_dict: dict[str, LLEntrance] = { }
    er_pairing_list: list[Tuple[int, int]] = []
    badges_in_world = 0

    item_name_groups = {
        "physical_items": {name for name, data in loony_item_table.items() if data.category == LLItemCat.ITEM},
        "monster_dolls": {name for name, data in loony_item_table.items() if data.category == LLItemCat.DOLL},
        "cheats": {name for name, data in loony_item_table.items() if data.category == LLItemCat.CHEAT},
        "special_weapons": {
            name
            for name, data in loony_item_table.items()
            if VAR_WBOMBS <= data.id - loonyland_base_id <= VAR_WHOTPANTS
        },
        "power": {name for name, data in loony_item_table.items() if LLFlags.PWR in data.flags},
        "power_big": {name for name, data in loony_item_table.items() if LLFlags.PWR_BIG in data.flags},
        "power_max": {name for name, data in loony_item_table.items() if LLFlags.PWR_MAX in data.flags},
    }

    location_name_groups = {
        "quests": {name for name, data in loonyland_location_table.items() if data.category == LLLocCat.QUEST},
        "badges": {name for name, data in loonyland_location_table.items() if data.category == LLLocCat.BADGE},
    }

    def generate_early(self) -> None:
        if (
            self.options.win_condition.value == self.options.win_condition.option_badges
            and self.options.badges.value == self.options.badges.option_none
        ):
            raise OptionError("Cannot have badges set to none with wincon as Badges")

    def get_filler_item_name(self) -> str:
        """Called when the item pool needs to be filled with additional items to match location count."""
        return "Max Life and Gems"

    def create_item(self, name: str) -> LoonylandItem:
        if name == "Max Life and Gems":
            return LoonylandItem("Max Life and Gems", ItemClassification.filler, loonyland_base_id + 3000, self.player)
        return LoonylandItem(
            name, loony_item_table[name].modified_classification(self.options), loony_item_table[name].id, self.player
        )

    def create_items(self) -> None:
        item_pool: list[LoonylandItem] = []
        for name, item in loony_item_table.items():
            if item.id and item.can_create(self.options) and item.should_generate(self.options):
                for i in range(item.frequency):
                    new_item = self.create_item(name)
                    item_pool.append(new_item)

        junk_len = len(self.multiworld.get_unfilled_locations(self.player)) - len(item_pool)
        item_pool += [self.create_filler() for _ in range(junk_len)]

        self.multiworld.itempool += item_pool

    def create_event(self, event: str) -> LoonylandItem:
        return LoonylandItem(event, ItemClassification.progression, None, self.player)

    def create_regions(self) -> None:
        # print(self.player_name)
        # for key in LoonylandOptions.__annotations__:
        #    print(key, getattr(self.options, key))

        for region_name, region_data in loonyland_region_table.items():
            if region_data.can_create(self.options):
                region = LoonylandRegion(region_name, self.player, self.multiworld, region_data)
                self.multiworld.regions.append(region)

        for loc_name, loc_data in loonyland_location_table.items():
            if not loc_data.can_create(self.options):
                continue
            region = self.get_region(loc_data.region)
            new_loc = LoonylandLocation(self.player, loc_name, loc_data.id + loonyland_base_id, region)
            if not loc_data.should_generate(self.options):
                new_loc.place_locked_item(self.create_event(loc_data.base_item))
                new_loc.address = None
            region.locations.append(new_loc)
            if loc_data.category == LLLocCat.BADGE:
                new_loc_as_event = LoonylandLocation(self.player, loc_name + " Earned", None, region)
                new_loc_as_event.place_locked_item(self.create_event("BadgeEarned"))
                region.locations.append(new_loc_as_event)
                self.badges_in_world += 1
        if (
            self.options.win_condition == WinCondition.option_badges
            and self.badges_in_world < self.options.badges_required
        ):
            raise OptionError(
                f'Not enough badge locations in world ("{self.badges_in_world}") '
                f'for amount required ("{self.options.badges_required}")'
            )

        # Completion condition.
        final_loc = None
        if self.options.win_condition == WinCondition.option_evilizer:
            final_loc = self.get_location("Q: Save Halloween Hill")
            final_loc.address = None
        elif self.options.win_condition == WinCondition.option_badges:
            final_loc = LoonylandLocation(
                self.player, str(self.options.badges_required.value) + " Badges Earned", None, self.get_region("Menu")
            )
            final_loc.access_rule = lambda state: have_x_badges(state, self.player, self.options.badges_required.value)
            self.get_region("Menu").locations.append(final_loc)
        else:  # no win con
            final_loc = self.get_location("Swamp: Outside Luniton")

        final_loc.place_locked_item(self.create_event("Victory"))
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)

        # force torch at curse the darkness
        torch_loc = self.get_location("Q: Curse The Darkness")
        torch_loc.place_locked_item(self.create_item("Torch"))




    def set_rules(self):
        # location rules
        set_rules(self)
        # entrance rules
        self.loonyland_entrance_list = setup_entrances(self)
        self.entrance_name_dict = {entry.entrance_name: entry for entry in self.loonyland_entrance_list}
        for region in self.multiworld.get_regions(self.player):
            for entry in self.loonyland_entrance_list:
                if entry.source_region==region.name and entry.can_create(self.options):
                    target_region = entry.target_exit  # for 0 id
                    name = entry.source_region + " -> " + entry.target_exit
                    if entry.id!=0:
                        name = entry.entrance_name
                        target_region = self.entrance_name_dict.get(entry.target_exit).source_region
                    logger = logging.getLogger("Client")
                    logger.info(entry.entrance_name + " " + entry.source_region + " " + entry.target_exit + " " + target_region)
                    e = region.connect(connecting_region=self.get_region(target_region), name=name, rule=entry.rule)
                    if self.options.entrance_rando:
                        if entry.id!=0:
                            e.randomization_type = EntranceType.TWO_WAY
                            disconnect_entrance_for_randomization(e)

    def connect_entrances(self):
        logger = logging.getLogger("Client")
        #randomize entrances
        if self.options.entrance_rando:
            placement_state = randomize_entrances(self, True, target_group_lookup={0: [0]})
            logger.info(msg=placement_state.pairings)
            for er_entrance, er_exit in placement_state.pairings:
                ent_id = self.entrance_name_dict[er_entrance].id
                exit_id = self.entrance_name_dict[er_exit].id
                logger.info(er_entrance + " " + str(ent_id) + " " + er_exit + " " + str(exit_id))
                self.er_pairing_list.append((ent_id, exit_id))
            visualize_regions(self.get_region("Menu"), f"Player{self.player}.puml", show_entrance_names=True)
            for entrance in self.get_entrances():
                if entrance.randomization_group == 1:
                    logger.info(entrance.name + " "
                                + entrance.parent_region.name + " "
                                + str(entrance.parent_region.llregion.map_id) + " "
                                + entrance.connected_region.name + " "
                                + str(entrance.connected_region.llregion.map_id)
                                )
        # setup data package

    def fill_slot_data(self):
        options_data = self.options.as_dict(
            "win_condition",
            "badges_required",
            "difficulty",
            "long_checks",
            "multisave",
            "remix",
            "overpowered_cheats",
            "badges",
            "dolls",
            "death_link")
        options_data["entrance_rando_data"] = self.er_pairing_list
        return options_data

    def collect(self, state: "CollectionState", item: "Item") -> bool:
        value = super().collect(state, item)
        if item.name in self.item_name_groups["power"]:
            state.prog_items[self.player]["total_power"] += 1
        if item.name in self.item_name_groups["power_big"]:
            state.prog_items[self.player]["total_power"] += 5
        if item.name in self.item_name_groups["power_max"]:
            state.prog_items[self.player]["total_power"] += 50
        return value
    def remove(self, state: "CollectionState", item: "Item") -> bool:
        value = super().remove(state, item)

        if item.name in self.item_name_groups["power"]:
            state.prog_items[self.player]["total_power"] -= 1
        if item.name in self.item_name_groups["power_big"]:
            state.prog_items[self.player]["total_power"] -= 5
        if item.name in self.item_name_groups["power_max"]:
            state.prog_items[self.player]["total_power"] -= 50
        return value
