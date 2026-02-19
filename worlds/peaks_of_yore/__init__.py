import logging
from typing import Any

from Options import Toggle, OptionError
from worlds.AutoWorld import World, WebWorld
from BaseClasses import Tutorial, Item
from .options import PeaksOfYoreOptions, Goal, StartingBook, RopeUnlockMode, StartingHands, poy_option_groups, \
    poy_option_presets, GameMode
from .data import *

from .regions import create_poy_regions, RegionLocationInfo


class PeaksOfYoreItem(Item):
    game = "Peaks of Yore"


class PeaksOfWeb(WebWorld):
    rich_text_options_doc = True
    theme = "stone"
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Peaks of Yore Mod.",
        "English",
        "setup_en.md",
        "setup/en",
        ["c0der23"]
    )]
    option_groups = poy_option_groups
    options_presets = poy_option_presets


def get_error_item_count(item_pool: list[Item], location_info: RegionLocationInfo) -> str:
    prog_list: list[Item] = [i for i in item_pool if i.classification == ItemClassification.progression]
    msg = "Error: not enough locations to place progression items:\n"
    msg += f"Found {len(prog_list)} progression items:\n"

    msg += f"{(" \n").join([i.name for i in prog_list if i.code >= 1000])}\n"
    peak_count = len([i for i in prog_list if i.code < 1000])
    if peak_count > 0:
        msg += f"+ {peak_count} peaks\n"
    msg += "\n"

    loc_count = location_info.get_total_location_count()
    msg += f"found {loc_count} locations: \n"
    msg += f"({len(location_info.peaks_in_pool)}/{loc_count}) peaks \n"
    msg += f"({len(location_info.time_attack_in_pool)}/{loc_count}) time attack locations \n"
    msg += f"({len(location_info.artefacts_in_pool)}/{loc_count}) artefacts \n"
    msg += f"({len(location_info.other_in_pool)}/{loc_count}) other collectables/free solo's \n"

    if len(location_info.time_attack_in_pool) == 0:
        msg += "Consider enabling time attack to add more locations"
    return msg


class PeaksOfWorld(World):
    """
    Peaks of Yore is a first-person physics-based "climb-em-up" adventure set in 1887.
    Steel your nerves and perfect your climbing skills as you ascend the rock wall, traverse difficult routes,
    and encounter many challenges and obstacles.
    """
    game = "Peaks of Yore"
    options_dataclass = PeaksOfYoreOptions
    options: PeaksOfYoreOptions
    web = PeaksOfWeb()
    item_name_to_id = item_name_to_id
    location_name_to_id = all_locations_to_ids
    topology_present = True
    checks_in_pool: RegionLocationInfo
    origin_region_name = "Cabin"

    def create_item(self, name: str) -> Item:
        id = item_name_to_id[name]
        classification = item_id_to_classification[id]
        return PeaksOfYoreItem(name, classification, id, self.player)

    def get_filler_item_name(self) -> str:
        choices = ["Extra Rope", "Extra Coffee", "Extra Chalk", "Extra Seed"]
        if self.options.item_traps:
            choices.append("Trap")
        return self.random.choice(choices)

    def generate_early(self) -> None:
        if self.options.goal == Goal.option_time_attack and not self.options.include_time_attack:
            logging.warning("Goal is set to time attack but time attack is not enabled, enabling time attack")
            self.options.include_time_attack.value = True

        starting_book_options: dict[str, Toggle] = {
            "Fundamentals Book": self.options.enable_fundamental,
            "Intermediate Book": self.options.enable_intermediate,
            "Advanced Book": self.options.enable_advanced,
            "Expert Book": self.options.enable_expert,
        }

        book_names: list[str] = list(starting_book_options)
        enabled_books: list[str] = [b for b, v in starting_book_options.items() if v]
        start_book: str = self.options.starting_book.get_selected_book()

        if self.options.game_mode == GameMode.option_peak_unlock:
            if self.options.early_hands:
                if self.options.start_with_hands != StartingHands.option_both:
                    raise OptionError("peak unlock with early hands is too restrictive of a start")

            if self.options.rope_unlock_mode == RopeUnlockMode.option_early:
                raise OptionError("peak unlock with early ropes is too restrictive of a start")

        if not enabled_books:
            logging.error(f"Player {self.player_name} has not selected any books!")
            raise OptionError(f"Player {self.player_name} has not selected any books!")

        if start_book not in enabled_books:
            logging.warning(f"Start book {start_book} not enabled, selecting random book from following list: ")
            logging.warning(enabled_books)
            start_book = self.random.choice(enabled_books)
            logging.warning(f"selected book: {start_book}")

        self.options.starting_book.value = book_names.index(start_book)

    def create_regions(self) -> None:
        self.checks_in_pool = create_poy_regions(self, self.options)

    def create_items(self) -> None:
        remaining_items: int = len(self.multiworld.get_unfilled_locations(self.player))
        total_location_count = remaining_items

        local_itempool: list[Item] = []
        for item in all_items:
            if item.is_enabled(self.options):
                if item.is_starter_item(self.options):
                    logging.debug(f"item {item.name} is starter for player {self.player_name}")
                    self.multiworld.push_precollected(self.create_item(item.name))
                else:
                    local_itempool.append(self.create_item(item.name))
                    if item.is_early(self.options):
                        logging.debug(f"item {item.name} is early for player {self.player_name}")
                        self.multiworld.early_items[self.player][item.name] = 1
        total_itempool: list[Item] = list(local_itempool)
        if len(local_itempool) > remaining_items:
            self.random.shuffle(local_itempool)  #
            i = 0
            while len(local_itempool) > remaining_items:  # trim down local item pool to match unfilled locations
                if i > remaining_items:
                    raise OptionError(get_error_item_count(total_itempool, self.checks_in_pool))

                if local_itempool[i].classification == ItemClassification.filler:
                    local_itempool.pop(i)  # removing random non-progression items until itempool isn't overflowing
                else:
                    i += 1

        if len(local_itempool) < remaining_items:  # fill up local item pool to match unfilled locations
            local_itempool += [self.create_filler() for _ in range(remaining_items - len(local_itempool))]

        self.multiworld.itempool += local_itempool[:remaining_items]

    def set_rules(self) -> None:
        if self.options.goal.value == Goal.option_all_artefacts:
            self.multiworld.completion_condition[self.player] = lambda state: all(
                state.can_reach_location(artefact, self.player) for artefact in
                self.checks_in_pool.artefacts_in_pool)

        elif self.options.goal.value == Goal.option_all_peaks:
            self.multiworld.completion_condition[self.player] = lambda state: all(
                state.can_reach_location(peak, self.player) for peak in self.checks_in_pool.peaks_in_pool)

        elif self.options.goal.value == Goal.option_all_artefacts_all_peaks:
            self.multiworld.completion_condition[self.player] = lambda state: all(
                state.can_reach_location(loc, self.player) for loc in [*self.checks_in_pool.peaks_in_pool,
                                                                       *self.checks_in_pool.artefacts_in_pool])

        elif self.options.goal.value == Goal.option_time_attack:
            self.multiworld.completion_condition[self.player] = lambda state: all(
                state.can_reach_location(loc, self.player) for loc in self.checks_in_pool.peaks_in_pool)

        elif self.options.goal.value == Goal.option_all:
            self.multiworld.completion_condition[self.player] = lambda state: all(
                state.can_reach_location(loc.name, self.player) for loc in self.multiworld.get_locations(self.player))

    def fill_slot_data(self) -> dict[str, Any]:
        return self.options.as_dict("death_link", "goal", "rope_unlock_mode", "death_link_traps",
                                    "game_mode", "disable_solemn_tempest", casing="camel")
