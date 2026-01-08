import json
from math import floor
import pkgutil
from typing import Any
from BaseClasses import Item, ItemClassification, Location, Region
from Options import Option
from Utils import visualize_regions
from worlds.generic.Rules import add_item_rule, add_rule, forbid_item, set_rule
from .locations import location_list
from .items import item_list
from .options import TboiOptions
from worlds.AutoWorld import World


class TboiLocation(Location):
    game = "The Binding of Isaac Repentance"
    
class TboiItem(Item):
    game = "The Binding of Isaac Repentance"

class TboiWorld(World):
    """TODO: Description"""
    game = "The Binding of Isaac Repentance"
    options_dataclass = TboiOptions
    options: TboiOptions
    topology_present = True

    data = json.loads(pkgutil.get_data(__name__, "data.json").decode())

    item_name_to_id = {name: id for
                       id, name in enumerate(item_list(data), 1)}
    location_name_to_id = {name: id for
                           id, name in enumerate(location_list(data), 1)}
        
    ut_can_gen_without_yaml = True
    tracker_world = {
        "map_page_folder": "tracker",
        "map_page_maps": "maps/maps.json",
        "map_page_locations": "locations/locations.json"
    }

    def create_location(self, location: str) -> dict[str, int : None]:
        id = self.location_name_to_id[location] if location in self.location_name_to_id.keys() else None
        return {location: id}

    def create_item(self, item: str) -> TboiItem:
        classification = \
                ItemClassification.progression if item.startswith('Unlock') else \
                ItemClassification.filler if item.startswith('Random') else \
                ItemClassification.trap if item.endswith('Trap') else \
                ItemClassification.useful
        return TboiItem(item, classification, self.item_name_to_id[item], self.player)
    
    def create_tracked_event(self, event: str) -> TboiItem:
        return TboiItem(event, ItemClassification.progression, self.item_name_to_id[event], self.player)
    
    def create_event(self, event: str) -> TboiItem:
        return TboiItem(event, ItemClassification.progression, None, self.player)

    def create_regions(self):
        menu_region = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu_region)

        existing_regions = set()

        for i in range(self.options.additional_item_locations):
            menu_region.add_locations(self.create_location(f'Item Pickup #{i+1}'), TboiLocation)

        for name, floor in self.data["floors"].items():
            if floor["type"] == "alt" and "Alt Path" in self.options.excluded_areas.value: continue
            if floor["type"] == "void" and "The Void" in self.options.excluded_areas.value: continue
            if floor["type"] == "ascend" and "Ascend" in self.options.excluded_areas.value: continue
            if floor["type"] == "timed" and "Timed Areas" in self.options.excluded_areas.value: continue
            region = Region(name, self.player, self.multiworld)
            for room in floor["rooms"]:
                location_name = f'{name} - {room}'
                region.add_locations(self.create_location(location_name), TboiLocation)
                if self.data["rooms"][room]["rare"]:
                    add_item_rule(self.multiworld.get_location(location_name, self.player),
                                lambda item: item.classification != ItemClassification.progression)
            self.multiworld.regions.append(region)
            existing_regions.add(region.name)
        
        for region in self.multiworld.get_regions(self.player):
            if region.name in self.data["floors"].keys():
                for connection in self.data["floors"][region.name]["connected"]:
                    if connection not in existing_regions: continue
                    exit_region = self.multiworld.get_region(connection, self.player)
                    if exit_region.name in self.data["floors"].keys() and not self.data["floors"][exit_region.name]["unlocked"]:
                        region.connect(exit_region, None, 
                                       lambda state, r=exit_region.name: state.has(f"Unlock {r}", self.player))
                    else:
                        region.connect(exit_region)
        
        menu_region.connect(self.multiworld.get_region("Basement", self.player))
        menu_region.connect(self.multiworld.get_region("Cellar", self.player), None, 
            lambda state: state.has(f"Unlock Cellar", self.player))
        menu_region.connect(self.multiworld.get_region("Burning Basement", self.player), None, 
            lambda state: state.has(f"Unlock Burning Basement", self.player))

        for boss, reward in self.data["boss_rewards"].items():
            available = False
            boss_region = Region(f'Boss: {boss}', self.player, self.multiworld)
            for region in self.multiworld.get_regions(self.player):
                if region.name in self.data["floors"].keys():
                    if boss == self.data["floors"][region.name]["boss"]:
                        available = True
                        region.connect(boss_region)
            if available:
                if self.options.additional_boss_rewards:
                    for i in range(reward):
                        boss_region.add_locations(self.create_location(f'{boss} Reward #{i+1}'), TboiLocation)
                    self.multiworld.regions.append(boss_region)
                if boss in self.options.goals:
                    boss_region.add_locations(self.create_location(f'Defeat {boss}'), TboiLocation)

    
    def addWeightedItems(self, items: dict[str, float], amount: float) -> int:
        items_added = 0
        total_weights = 0
        for weight in items.values():
            total_weights += weight
        item_factor = 1.0 / total_weights * amount

        for item, weight in items.items():
            for i in range(round(weight*item_factor)):
                self.multiworld.itempool.append(self.create_item(item))
                items_added += 1

        return items_added

    def create_items(self):
        own_items = len(self.options.goals.value)
        for name, floor in self.data['floors'].items():
            if floor["unlocked"]: continue
            if floor["type"] == "alt" and "Alt Path" in self.options.excluded_areas.value: continue
            if floor["type"] == "void" and "The Void" in self.options.excluded_areas.value: continue
            if floor["type"] == "ascend" and "Ascend" in self.options.excluded_areas.value: continue
            if floor["type"] == "timed" and "Timed Areas" in self.options.excluded_areas.value: continue
            self.multiworld.itempool.append(self.create_item(f'Unlock {name}'))
            own_items += 1
        
        for _ in range(self.options.one_ups.value):
            self.multiworld.itempool.append(self.create_item('1-UP'))
            own_items += 1

        total_locations = len(self.multiworld.get_locations(self.player))
        filler_amount = total_locations - own_items

        item_factor = 100 - self.options.junk_percentage
        trap_factor = self.options.junk_percentage * self.options.trap_percentage / 100.0
        junk_factor = self.options.junk_percentage - trap_factor

        own_items += self.addWeightedItems(self.options.item_weights.value, filler_amount * item_factor / 100.0)
        own_items += self.addWeightedItems(self.options.trap_weights.value, filler_amount * trap_factor / 100.0)
        own_items += self.addWeightedItems(self.options.junk_weights.value, filler_amount * junk_factor / 100.0)

        if own_items > total_locations:
            for i in range(own_items - total_locations):
                self.multiworld.itempool.pop()
        if own_items < total_locations:
            for i in range(total_locations - own_items):
                self.multiworld.itempool.append(self.create_item("Random Coin"))

    def set_rules(self) -> None:
        for i in range(5, self.options.additional_item_locations):
            add_item_rule(self.multiworld.get_location(f'Item Pickup #{i+1}', self.player),
                lambda item: item.classification != ItemClassification.progression)

        if "Alt Path" not in self.options.excluded_areas.value:
            for escape_entrance in self.multiworld.get_region("The Escape", self.player).entrances:
                add_rule(escape_entrance,
                        lambda state: state.can_reach_region("Mirrorworld", self.player))
            for corpse_entrance in self.multiworld.get_region("Corpse", self.player).entrances:
                add_rule(corpse_entrance,
                        lambda state: state.can_reach_region("Mirrorworld", self.player) and
                                    state.can_reach_region("The Escape", self.player))
        
        if "Ascend" not in self.options.excluded_areas.value:
            for home_entrance in self.multiworld.get_region("Home", self.player).entrances:
                add_rule(home_entrance,
                        lambda state: state.has("Unlock Chest", self.player) or
                                    state.has("Unlock Dark Room", self.player))
                if "Alt Path" not in self.options.excluded_areas.value:
                    add_rule(home_entrance,
                            lambda state: state.has("Unlock Mausoleum", self.player))

        early_floors = list(self.data["floors"].keys())[:9]
        early_locations = []
        for early_floor in early_floors:
            early_locations.extend(self.multiworld.get_region(early_floor, self.player).get_locations())
        late_floors = [ name for name, area in self.data["floors"].items() if area["late"] ]

        for location in early_locations:
            for late_floor in late_floors:
                forbid_item(location, f'Unlock {late_floor}', self.player)

        goal_amount = 0
        for goal in self.options.goals.value:
            if goal == "Mother" and "Alt Path" in self.options.excluded_areas.value: continue
            if goal == "Delirium" and "The Void" in self.options.excluded_areas.value: continue
            if goal == "Beast" and "Ascend" in self.options.excluded_areas.value: continue
            if (goal == "Boss Rush" or goal == "Hush") and "Timed Areas" in self.options.excluded_areas.value: continue
            self.multiworld.get_location(f'Defeat {goal}', self.player).place_locked_item(self.create_tracked_event("Victory Condition"))
            goal_amount += 1

        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory Condition", self.player, goal_amount)
        #self.multiworld.completion_condition[self.player] = self.has_location_lambda("Mega Satan - Boss Room")
        
        #visualize_regions(self.multiworld.get_region("Menu", self.player), "my_world.puml")

    def fill_slot_data(self) -> dict[str, Any]:
        return {
            "options": self.options.as_dict("deathlink", "scatter_previous_items", "fortunes_are_hints", "win_collects_missed_locations", "item_location_step", "additional_item_locations", "excluded_areas", "additional_boss_rewards", "goals", "one_ups", "junk_percentage", "trap_percentage", "item_weights", "retain_one_ups_percentage", "retain_items_percentage", "retain_junk_percentage"),
        }
    
    def generate_early(self) -> None:
        re_gen_passthrough = getattr(self.multiworld, "re_gen_passthrough", {})
        if re_gen_passthrough and self.game in re_gen_passthrough:
            # Get the passed through slot data from the real generation
            slot_data: dict[str, Any] = re_gen_passthrough[self.game]

            slot_options: dict[str, Any] = slot_data.get("options", {})
            # Set all your options here instead of getting them from the yaml
            for key, value in slot_options.items():
                opt: Option | None = getattr(self.options, key, None)
                if opt is not None:
                    # You can also set .value directly but that won't work if you have OptionSets
                    setattr(self.options, key, opt.from_any(value))

    @staticmethod
    def interpret_slot_data(slot_data: dict[str, Any]) -> dict[str, Any]:
        return slot_data
    