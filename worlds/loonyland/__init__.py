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
from .flags import LLFlags
from .items import LLItemCat, LoonylandItem
from .locations import LLLocCat, LoonylandLocation
from .options import LoonylandOptions, WinCondition
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

    def create_junk(self) -> LoonylandItem:
        return LoonylandItem("Max Life and Gems", ItemClassification.filler, loonyland_base_id + 3000, self.player)

    def create_item(self, name: str) -> LoonylandItem:
        if name == "Max Life and Gems":
            return self.create_junk()
        return LoonylandItem(
            name, loony_item_table[name].modified_classification(self.options), loony_item_table[name].id, self.player
        )

    def create_items(self) -> None:
        item_pool: list[LoonylandItem] = []
        for name, item in loony_item_table.items():
            if item.id and item.can_create(self.options) and item.in_logic(self.options):
                for i in range(item.frequency):
                    new_item = self.create_item(name)
                    item_pool.append(new_item)

        junk_len = len(self.multiworld.get_unfilled_locations(self.player)) - len(item_pool) - 1
        if self.options.win_condition == WinCondition.option_evilizer:
            junk_len = junk_len - 1
        item_pool += [self.create_junk() for _ in range(junk_len)]

        self.multiworld.itempool += item_pool

    def create_event(self, event: str) -> LoonylandItem:
        return LoonylandItem(event, ItemClassification.progression, None, self.player)

    def create_regions(self) -> None:
        # print(self.player_name)
        # for key in LoonylandOptions.__annotations__:
        #    print(key, getattr(self.options, key))

        for region_name, region_data in loonyland_region_table.items():
            if region_data.can_create(self.options):
                region = Region(region_name, self.player, self.multiworld)
                self.multiworld.regions.append(region)

        for loc_name, loc_data in loonyland_location_table.items():
            if not loc_data.can_create(self.options):
                continue
            region = self.get_region(loc_data.region)
            new_loc = LoonylandLocation(self.player, loc_name, loc_data.id + loonyland_base_id, region)
            if not loc_data.in_logic(self.options):
                new_loc.place_locked_item(self.create_event(loc_data.base_item))
                new_loc.address = None
            region.locations.append(new_loc)
            if loc_data.category == LLLocCat.BADGE:
                new_loc_as_event = LoonylandLocation(self.player, loc_name + " Earned", None, region)
                new_loc_as_event.place_locked_item(self.create_event("BadgeEarned"))
                region.locations.append(new_loc_as_event)

    def set_rules(self):
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

        # location rules
        set_rules(self.multiworld, self)
        # entrance rules
        set_entrance_rules(self.multiworld, self)

    def fill_slot_data(self):
        return {
            "WinCondition": self.options.win_condition.value,
            "BadgesRequired": self.options.badges_required.value,
            "Difficulty": self.options.difficulty.value,
            "LongChecks": self.options.long_checks.value,
            "MultipleSaves": self.options.multisave.value,
            "Remix": self.options.remix.value,
            "OverpoweredCheats": self.options.overpowered_cheats.value,
            "Badges": self.options.badges.value,
            "Dolls": self.options.dolls.value,
            "DeathLink": self.options.death_link.value,
        }
