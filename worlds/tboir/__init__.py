import json
import pkgutil
import random
from typing import Any
from BaseClasses import CollectionState, Item, ItemClassification, Location, Region
from Options import Option
from Utils import visualize_regions
import settings
from worlds.LauncherComponents import Component, Type, launch_subprocess, icon_paths, components
from worlds.generic.Rules import add_item_rule, add_rule, forbid_item
from .locations import location_list
from .items import item_list
from .options import TboiOptions
from worlds.AutoWorld import World

def launch_client():
    from . import client
    launch_subprocess(client.launch, name="Isaac Client")

components.append(Component("Isaac Client",
                            func=launch_client,
                            component_type=Type.CLIENT,
                            icon="isaac"))

icon_paths["isaac"] = f"ap:{__name__}/icons/isaac.png"

class TboiLocation(Location):
    game = "The Binding of Isaac Repentance"
    
class TboiItem(Item):
    game = "The Binding of Isaac Repentance"

class TboiSettings(settings.Group):
    class GameFolder(settings.UserFolderPath):
        """Location of The Binding of Isaac installation directory"""
        description = "Isaac installation directory"

    game_folder: GameFolder = GameFolder("The Binding of Isaac Rebirth")

class TboiWorld(World):
    """
    Experience the modern classic, The Binding of Isaac, like you've never seen it before. 
    It's a game too big to be called a sequel: Repentance takes Isaac to new heights of 
    roguelike dungeon adventure, as the brave boy descends into the basement for his 
    greatest challenge yet! Isaac's new quest takes him to unknown places he's never been, 
    filled with horrible new enemies and bosses, weapon combos you've never synergized 
    before and items he's never seen... unholy terrors from his wildest dreams and worst 
    nightmares!
    """
    game = "The Binding of Isaac Repentance"
    options_dataclass = TboiOptions
    options: TboiOptions
    topology_present = True
    settings: TboiSettings

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
                ItemClassification.progression if item.endswith('Unlock') else \
                ItemClassification.useful if item.startswith('1-UP') or item.startswith('Angel Deal') or item.startswith('Devil Deal') or item.startswith('Planetarium') else \
                ItemClassification.trap if item.endswith('Trap') else \
                ItemClassification.filler
        return TboiItem(item, classification, self.item_name_to_id[item], self.player)
    
    def create_event(self, event: str) -> TboiItem:
        return TboiItem(event, ItemClassification.progression, None, self.player)
    
    def rule_from_data(self, state: CollectionState, rule):
        if "has" in rule:
            return state.has(f'{rule["has"]} Unlock', self.player)
        if "or" in rule:
            return any(self.rule_from_data(state, x) for x in rule["or"])
        if "and" in rule:
            return all(self.rule_from_data(state, x) for x in rule["and"])
        
    def create_regions(self):
        existing_regions = set()

        for name, floor in self.data["regions"].items():
            if "type" in floor and floor["type"] == "alt" and "Alt Path" in self.options.excluded_areas.value: continue
            if "type" in floor and floor["type"] == "void" and "The Void" in self.options.excluded_areas.value: continue
            if "type" in floor and floor["type"] == "ascend" and "Ascend" in self.options.excluded_areas.value: continue
            if "type" in floor and floor["type"] == "timed" and "Timed Areas" in self.options.excluded_areas.value: continue
            region = Region(name, self.player, self.multiworld)
            if "rooms" in floor:
                for room in floor["rooms"]:
                    location_name = f'{name} - {room}'
                    region.add_locations(self.create_location(location_name), TboiLocation)
                    if self.data["rooms"][room]["rng"]:
                        add_item_rule(self.get_location(location_name),
                                lambda item: (item.classification & ItemClassification.progression) == 0)
                    if "requires" in self.data["rooms"][room]:
                        add_rule(self.get_location(location_name),
                                lambda state, rule=self.data["rooms"][room]["requires"]: self.rule_from_data(state, rule))
                        #add_item_rule(self.get_location(location_name),
                        #        lambda item: item.classification == ItemClassification.progression or item.classification == ItemClassification.useful)
            if name in self.options.additional_item_locations_per_stage.keys():
                for i in range(self.options.additional_item_locations_per_stage[name]):
                    region.add_locations(self.create_location(f'{name} - Item #{i+1}'))
            self.multiworld.regions.append(region)
            existing_regions.add(region.name)
        
        for region in self.multiworld.get_regions(self.player):
            if region.name in self.data["regions"].keys() and "connects_to" in self.data["regions"][region.name]:
                for connection in self.data["regions"][region.name]["connects_to"]:
                    if connection not in existing_regions: continue
                    exit_region = self.multiworld.get_region(connection, self.player)
                    if exit_region.name in self.data["regions"].keys() and "requires" in self.data["regions"][exit_region.name]:
                        region.connect(exit_region, None, 
                                       lambda state, rule=self.data["regions"][exit_region.name]["requires"]: self.rule_from_data(state, rule))
                    else:
                        region.connect(exit_region)

        for boss, reward in self.data["boss_rewards"].items():
            available = False
            boss_region = Region(f'Boss: {boss}', self.player, self.multiworld)
            for region in self.multiworld.get_regions(self.player):
                if region.name in self.data["regions"].keys():
                    if "boss" in self.data["regions"][region.name] and boss == self.data["regions"][region.name]["boss"]:
                        available = True
                        region.connect(boss_region)
            if available:
                if self.options.additional_boss_rewards:
                    for i in range(reward["amount"]):
                        boss_region.add_locations(self.create_location(f'{boss} Reward #{i+1}'), TboiLocation)
                    self.multiworld.regions.append(boss_region)
                if boss in self.goals:
                    boss_region.add_locations(self.create_location(f'Defeat {boss}'), TboiLocation)

    
    def addWeightedItems(self, items: dict[str, float], amount: float) -> int:
        items_added = 0
        total_weights = 0
        for weight in items.values():
            total_weights += weight
        item_factor = 1.0 / total_weights * amount

        for item, weight in items.items():
            for _ in range(round(weight*item_factor)):
                self.multiworld.itempool.append(self.create_item(item))
                items_added += 1

        return items_added

    def create_items(self):
        own_items = len(self.goals)
        for name, unlock in self.data['unlocks'].items():
            if "type" in unlock and unlock["type"] == "alt" and "Alt Path" in self.options.excluded_areas.value: continue
            if "type" in unlock and unlock["type"] == "void" and "The Void" in self.options.excluded_areas.value: continue
            if "type" in unlock and unlock["type"] == "ascend" and "Ascend" in self.options.excluded_areas.value: continue
            if "type" in unlock and unlock["type"] == "timed" and "Timed Areas" in self.options.excluded_areas.value: continue
            self.multiworld.itempool.append(self.create_item(f'{name} Unlock'))
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
            for _ in range(own_items - total_locations):
                self.multiworld.itempool.pop()
        if own_items < total_locations:
            for _ in range(total_locations - own_items):
                self.multiworld.itempool.append(self.create_item("Random Coin"))

    def set_rules(self) -> None:
        goal_amount = 0
        for goal in self.goals:
            if goal == "Mother" and "Alt Path" in self.options.excluded_areas.value: continue
            if goal == "Delirium" and "The Void" in self.options.excluded_areas.value: continue
            if goal == "Beast" and "Ascend" in self.options.excluded_areas.value: continue
            if (goal == "Boss Rush" or goal == "Hush") and "Timed Areas" in self.options.excluded_areas.value: continue
            self.multiworld.get_location(f'Defeat {goal}', self.player).place_locked_item(self.create_event("Victory Condition"))
            goal_amount += 1

        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory Condition", self.player, goal_amount)
        #self.multiworld.completion_condition[self.player] = self.has_location_lambda("Mega Satan - Boss Room")
        
        #visualize_regions(self.multiworld.get_region("Menu", self.player), "my_world.puml")

    def fill_slot_data(self) -> dict[str, Any]:
        return {
            "options": self.options.as_dict(
                "bad_rng_protection",
                "fortune_machine_hint_percentage",
                "crystal_ball_hint_percentage",
                "fortune_cookie_hint_percentage",
                "hint_types_from_fortunes",
                "excluded_areas",
                "additional_item_locations_per_stage",
                "item_location_percentage",
                "additional_boss_rewards",
                "scatter_previous_items",
                "junk_percentage",
                "trap_percentage",
                "item_weights",
                "retain_items_percentage",
                "junk_weights",
                "retain_junk_percentage",
                "trap_weights",
                "one_ups",
                "retain_one_ups_percentage",
                "exclude_items_as_rewards",
                "death_link",
                toggles_as_bools=True) 
                |
                { "goals": self.goals }
           }
    
    def generate_early(self) -> None:
        self.goals = []
        available_bosses = list(self.data["boss_rewards"].keys())

        if "All" in self.options.goals.value:
            self.goals = available_bosses
        else:
            for goal in self.options.goals.value:
                if goal in available_bosses:
                    self.goals.append(goal)
                    available_bosses.remove(goal)

            random.shuffle(available_bosses)
            for goal in self.options.goals.value:
                if goal.startswith("Random"):
                    amount = int(goal.split('-')[1])
                    for _ in range(amount):
                        self.goals.append(available_bosses.pop())

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
    