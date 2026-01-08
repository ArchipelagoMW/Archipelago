from worlds.AutoWorld import World, WebWorld
from BaseClasses import Region, CollectionState, Tutorial
from .items import PseudoregaliaItem, item_table, item_groups
from .locations import PseudoregaliaLocation, location_table, zones
from .regions import region_table, origin_region_names
from .options import PseudoregaliaOptions
from .rules_normal import PseudoregaliaNormalRules
from .rules_hard import PseudoregaliaHardRules
from .rules_expert import PseudoregaliaExpertRules
from .rules_lunatic import PseudoregaliaLunaticRules
from typing import Dict, Any
from .constants.difficulties import NORMAL, HARD, EXPERT, LUNATIC
from .constants.versions import FULL_GOLD


class PseudoregaliaWebWorld(WebWorld):
    setup_en = Tutorial("name", "description", "English", "setup_en.md", "setup/en", ["TODO"])
    tutorials = [setup_en]
    

class PseudoregaliaWorld(World):
    game = "Pseudoregalia"
    required_client_version = (0, 7, 0)
    apworld_version = (0, 10, 0)

    item_name_to_id = {name: data.code for name, data in item_table.items() if data.code is not None}
    location_name_to_id = {name: data.code for name, data in location_table.items() if data.code is not None}
    item_name_groups = item_groups

    options_dataclass = PseudoregaliaOptions
    options: PseudoregaliaOptions
    
    web = PseudoregaliaWebWorld()

    filler = ("Healing", "Magic Power")
    filler_index = 0

    def get_filler_item_name(self) -> str:
        filler_item_name = self.filler[self.filler_index]
        self.filler_index = (self.filler_index + 1) % len(self.filler)
        return filler_item_name

    def create_item(self, name: str) -> PseudoregaliaItem:
        data = item_table[name]
        return PseudoregaliaItem(name, data.classification, data.code, self.player)

    def collect(self, state: CollectionState, item: PseudoregaliaItem) -> bool:
        ret = super().collect(state, item)
        name = item.name
        # only adding the first Sun Greaves or Cling Gem actually matters
        # to match how the game interprets these items
        if name == "Sun Greaves" and state.count(name, self.player) == 1:
            state.add_item("Kick Count", self.player, 3)
        elif name in ("Heliacal Power", "Air Kick"):
            state.add_item("Kick Count", self.player, 1)
        elif name == "Cling Gem" and state.count(name, self.player) == 1:
            state.add_item("Cling Count", self.player, 6)
        elif name == "Cling Shard":
            state.add_item("Cling Count", self.player, 2)
        return ret

    def remove(self, state: CollectionState, item: PseudoregaliaItem) -> bool:
        ret = super().remove(state, item)
        name = item.name
        # only removing the last Sun Greaves or Cling Gem actually matters
        # to match how the game interprets these items
        if name == "Sun Greaves" and state.count(name, self.player) == 0:
            state.remove_item("Kick Count", self.player, 3)
        elif name in ("Heliacal Power", "Air Kick"):
            state.remove_item("Kick Count", self.player, 1)
        elif name == "Cling Gem" and state.count(name, self.player) == 0:
            state.remove_item("Cling Count", self.player, 6)
        elif name == "Cling Shard":
            state.remove_item("Cling Count", self.player, 2)
        return ret

    def create_items(self):
        itempool = []
        for item_name, item_data in item_table.items():
            if not item_data.can_create(self.options) or not item_data.code:
                continue
            precollect = item_data.precollect(self.options)
            for _ in range(precollect):
                self.multiworld.push_precollected(self.create_item(item_name))
            itempool += [self.create_item(item_name) for _ in range(precollect, item_data.frequency)]
        total_locations = len(self.multiworld.get_unfilled_locations(self.player))
        itempool += [self.create_filler() for _ in range(total_locations - len(itempool))]
        self.multiworld.itempool += itempool

    def generate_early(self):
        if self.options.logic_level in (EXPERT, LUNATIC):
            # obscure is forced on for expert/lunatic difficulties
            self.options.obscure_logic.value = 1
        if self.options.game_version == FULL_GOLD:
            # zero out options that don't do anything on full gold
            self.options.start_with_map.value = 0
            self.options.randomize_time_trials.value = 0
        spawn_point = self.options.spawn_point
        if spawn_point == spawn_point.option_dungeon_mirror:
            # start_with_breaker is forced on for dungeon start to help with sphere 1 size
            self.options.start_with_breaker.value = 1
        elif spawn_point == spawn_point.option_library:
            if not self.options.start_with_breaker and not self.options.randomize_books:
                # start_with_breaker is forced on if otherwise player wouldn't have enough checks
                self.options.start_with_breaker.value = 1

    def create_regions(self):
        self.origin_region_name = origin_region_names[self.options.spawn_point.value]

        for region_name in region_table.keys():
            self.multiworld.regions.append(Region(region_name, self.player, self.multiworld))

        locations = sorted(location_table.items(), key=lambda loc_pair: zones.index(loc_pair[0].split(" - ")[0]))
        for loc_name, loc_data in locations:
            if not loc_data.can_create(self.options):
                continue
            region = self.multiworld.get_region(loc_data.region, self.player)
            new_loc = PseudoregaliaLocation(self.player, loc_name, loc_data.code, region)
            region.locations.append(new_loc)
            if loc_data.locked_item:
                new_loc.place_locked_item(self.create_item(loc_data.locked_item))

        for region_name, exit_list in region_table.items():
            region = self.multiworld.get_region(region_name, self.player)
            region.add_exits(exit_list)

    def create_key_hints(self) -> Any:
        key_hints = [[] for _ in range(5)]
        key_locations = self.multiworld.find_items_in_locations(set(item_groups["major keys"]), self.player, True)
        for location in key_locations:
            if not location.item or not location.item.code or not location.address:
                # guard against optional fields being None
                continue
            # this implementation assumes major key item codes are all in a row starting at 2365810021 and will
            # break if that ever changes
            index = location.item.code - 2365810021
            if index not in range(5):
                # guard against index being out of bounds
                continue
            key_hints[index].append({
                "player": location.player,
                "location": location.address,
            })
        return key_hints

    def fill_slot_data(self) -> Dict[str, Any]:
        slot_data = {
            "apworld_version": self.apworld_version,
            "game_version": self.options.game_version.value,
            "logic_level": self.options.logic_level.value,
            "spawn_point": self.options.spawn_point.value,
            "obscure_logic": bool(self.options.obscure_logic),
            "progressive_breaker": bool(self.options.progressive_breaker),
            "progressive_slide": bool(self.options.progressive_slide),
            "split_sun_greaves": bool(self.options.split_sun_greaves),
            "split_cling_gem": bool(self.options.split_cling_gem),
            "randomize_time_trials": bool(self.options.randomize_time_trials),
            "randomize_goats": bool(self.options.randomize_goats),
            "randomize_chairs": bool(self.options.randomize_chairs),
            "randomize_books": bool(self.options.randomize_books),
            "randomize_notes": bool(self.options.randomize_notes),
        }
        if self.options.major_key_hints:
            slot_data["key_hints"] = self.create_key_hints()
        return slot_data

    def set_rules(self):
        difficulty = self.options.logic_level
        if difficulty == NORMAL:
            PseudoregaliaNormalRules(self).set_pseudoregalia_rules()
        elif difficulty == HARD:
            PseudoregaliaHardRules(self).set_pseudoregalia_rules()
        elif difficulty == EXPERT:
            PseudoregaliaExpertRules(self).set_pseudoregalia_rules()
        elif difficulty == LUNATIC:
            PseudoregaliaLunaticRules(self).set_pseudoregalia_rules()
