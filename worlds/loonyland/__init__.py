from BaseClasses import ItemClassification, Region, Tutorial

from worlds.AutoWorld import WebWorld, World

from .Data.game_data import (
    VAR_WBOMBS,
    VAR_WHOTPANTS,
    loony_item_table,
    loonyland_location_table,
    loonyland_region_table,
    set_entrance_rules,
    set_rules,
)
from .Data.game_data import (
    ll_base_id as loonyland_base_id,
)
from .items import LLItemCat, LoonylandItem
from .locations import LLLocCat, LoonylandLocation
from .options import Badges, LoonylandOptions


class LoonylandWebWorld(WebWorld):
    theme = "dirt"

    setup_en = Tutorial(
        tutorial_name="Start Guide",
        description="A guide to playing Loonyland.",
        language="English",
        file_name="guide_en.md",
        link="guide/en",
        authors=["AutomaticFrenzy"],
    )

    tutorials = [setup_en]


class LoonylandWorld(World):
    """The greatest game of all time."""

    game = "Loonyland"
    web = LoonylandWebWorld()
    options: LoonylandOptions
    options_dataclass = LoonylandOptions
    location_name_to_id = {name: data.id + loonyland_base_id for name, data in loonyland_location_table.items()}
    item_name_to_id = {name: data.id for name, data in loony_item_table.items()}

    item_name_groups = {
        "physical_items": {name for name, data in loony_item_table.items() if data.category == LLItemCat.ITEM},
        "monster_dolls": {name for name, data in loony_item_table.items() if data.category == LLItemCat.DOLL},
        "cheats": {name for name, data in loony_item_table.items() if data.category == LLItemCat.CHEAT},
        "special_weapons": {
            name
            for name, data in loony_item_table.items()
            if VAR_WBOMBS <= data.id - loonyland_base_id <= VAR_WHOTPANTS
        },
    }

    location_name_groups = {
        "quests": {name for name, data in loonyland_location_table.items() if data.category == LLLocCat.QUEST},
        "badges": {name for name, data in loonyland_location_table.items() if data.category == LLLocCat.BADGE},
    }

    def create_item(self, name: str) -> LoonylandItem:
        return LoonylandItem(name, loony_item_table[name].classification, loony_item_table[name].id, self.player)

    def create_junk(self) -> LoonylandItem:
        return LoonylandItem("A Cool Filler Item", ItemClassification.filler, loonyland_base_id + 3000, self.player)

    def create_items(self) -> None:
        item_pool: list[LoonylandItem] = []
        for name, item in loony_item_table.items():
            if item.id and item.can_create(self.options):
                for i in range(item.frequency):
                    new_item = self.create_item(name)
                    item_pool.append(new_item)

        junk_len = (
            len(self.multiworld.get_unfilled_locations(self.player)) - len(item_pool) - 1
        )  # - 1 for win con location
        item_pool += [self.create_junk() for _ in range(junk_len)]

        self.multiworld.itempool += item_pool

    def create_event(self, event: str) -> LoonylandItem:
        return LoonylandItem(event, ItemClassification.progression, None, self.player)

    def create_regions(self) -> None:
        for region_name in loonyland_region_table:
            region = Region(region_name, self.player, self.multiworld)
            self.multiworld.regions.append(region)

        for loc_name, loc_data in loonyland_location_table.items():
            if not loc_data.can_create(self.options):
                continue
            region = self.multiworld.get_region(loc_data.region, self.player)
            new_loc = LoonylandLocation(self.player, loc_name, loc_data.id + loonyland_base_id, region)
            if not loc_data.in_logic(self.options):
                new_loc.place_locked_item(self.create_event(loc_data.base_item))
                new_loc.address = None
            region.locations.append(new_loc)

    def set_rules(self):
        # Completion condition.
        # self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)
        final_loc = self.get_location("Q: Save Halloween Hill")
        final_loc.address = None
        final_loc.place_locked_item(self.create_event("Victory"))
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)

        # location rules
        set_rules(self.multiworld, self, self.player)
        # entrance rules
        set_entrance_rules(self.multiworld, self, self.player)

    def fill_slot_data(self):
        return {"DeathLink": self.options.death_link.value, "Difficulty": self.options.difficulty.value}
