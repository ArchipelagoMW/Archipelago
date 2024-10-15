from typing import Dict, List, Set, FrozenSet
from worlds.AutoWorld import World
from BaseClasses import ItemClassification as IC, LocationProgressType
from .Items import item_data_table, item_name_to_id, DSTItem
from .Options import DSTOptions
from .Constants import ITEM_ID_OFFSET

class DSTItemPool:
    nonfiller_itempool:List[str] # All items enabled by the options except junk
    filler_items:List[str]
    trap_items:List[str]
    seasontrap_items:List[str]
    locked_items_local_id:Set
    locked_items:Set[str]
    # These are to be set by rules, using set_progression_items
    progression_items:FrozenSet[str] = frozenset() 
    prioritized_useful_items:FrozenSet[str] = frozenset() # For items that would be progression under different logic settings

    def decide_itempools(self, world:World) -> None:
        "Before generating, decide what items go in itempool categories"
        options:DSTOptions = world.options
        self.nonfiller_itempool = list()
        self.filler_items = list()
        self.trap_items = list()
        self.seasontrap_items = list()
        self.locked_items_local_id = set()
        self.locked_items = set()
        start_inventory:FrozenSet = frozenset(options.start_inventory.value.keys())
        nonshuffled:FrozenSet = frozenset() # TODO: Support for nonshuffled options
        region_valid = {
            # Caves
            "cave":         options.cave_regions.value >= options.cave_regions.option_light,
            "ruins":        options.cave_regions.value >= options.cave_regions.option_full,
            "archive":      options.cave_regions.value >= options.cave_regions.option_full,

            # Ocean
            "ocean":        options.ocean_regions.value >= options.ocean_regions.option_light,
            "moonquay":     options.ocean_regions.value >= options.ocean_regions.option_light,
            "moonstorm":    options.ocean_regions.value >= options.ocean_regions.option_full,
        }

        for name, item in item_data_table.items():
            # Don't shuffle nonshuffled items
            if (
                name in nonshuffled
                or "nonshuffled" in item.tags
                or "progressive" in item.tags # Add these somewhere else
            ):
                continue

            if not name in start_inventory:
                # Do not include things that are deprecated or disabled by options
                if (
                    not item.code
                    or "deprecated" in item.tags
                    or (not options.shuffle_no_unlock_recipes.value and "nounlock" in item.tags)
                    or (not options.season_change_helper_items.value and "seasonhelper" in item.tags)
                    or (not options.seed_items.value and "seeds" in item.tags)
                    or (not options.chesspiece_sketch_items.value and "chesspiecesketch" in item.tags)
                ):
                    continue

                # Add items that are in our regions
                _enabled = True
                for regiontag, istrue in region_valid.items():
                    if regiontag in item.tags:
                        _enabled = False
                        if istrue:
                            _enabled = True
                            break

                if not _enabled: 
                    continue

                # Add basic items as dummy event items so we can do logic with them
                if not options.shuffle_starting_recipes.value and "basic" in item.tags:
                    if item.type == IC.progression:
                        world.multiworld.push_precollected(DSTItem(name, IC.progression, None, world.player))
                    continue

            # Put junk items in the filler pool
            if "junk" in item.tags:
                self.filler_items.append(name)
                continue

            # Put trap items in the trap pools
            if "trap" in item.tags:
                (self.seasontrap_items if "seasontrap" in item.tags else self.trap_items).append(name)
                continue

            # All recipe items that must be locked in DST, converted to local id so that it uses less digits
            if not "physical" in item.tags:
                self.locked_items_local_id.add(item.code-ITEM_ID_OFFSET)
                self.locked_items.add(name)

            # Add into the nonfiller pool
            if not name in start_inventory:
                self.nonfiller_itempool.append(name)
        
        # Handle progressive items here
        for _ in range(options.extra_damage_against_bosses.value):
            self.nonfiller_itempool.append("Extra Damage Against Bosses")
    
    def create_item(self, world:World, name: str) -> DSTItem:
        itemtype = (
            IC.progression if name in self.progression_items
            else item_data_table[name].type if name in item_name_to_id 
            else IC.progression
        )
        return DSTItem(
            name, 
            itemtype, 
            item_data_table[name].code if name in item_name_to_id else None, 
            world.player
        )

    def create_items(self, world: World) -> None:
        item_pool: List[DSTItem] = []

        options:DSTOptions = world.options
        NUM_JUNK_ITEMS:int = options.junk_item_amount.value
        items_by_classification:Dict[int, List[DSTItem]] = {
            "filler": [],
            "useful": [],
            "prioritized_useful": [],
            "progression": [],
        }

        for name in self.nonfiller_itempool:
            item = world.create_item(name)
            if not name in self.locked_items:
                # Add physical items always
                item_pool.append(item)
            else:
                # Group items by classification
                if IC.progression in item.classification:
                    items_by_classification["progression"].append(item)
                elif item.name in self.prioritized_useful_items:
                    items_by_classification["prioritized_useful"].append(item)
                elif IC.useful in item.classification:
                    items_by_classification["useful"].append(item)
                else:
                    items_by_classification["filler"].append(item)
        
        for _list in items_by_classification.values():
            world.multiworld.random.shuffle(_list) # In case of overflow, shuffle so our overflows are random

        unfilled_locations = world.multiworld.get_unfilled_locations(world.player)
        num_total_locations = len(unfilled_locations)
        num_nonexcluded_locations = \
            len([location for location in unfilled_locations if location.progress_type != LocationProgressType.EXCLUDED])
        num_excluded_locations = \
            len([location for location in unfilled_locations if location.progress_type == LocationProgressType.EXCLUDED])
        num_preplaced_priority = len([item for item in item_pool if (item.advancement or item.useful)])
        num_preplaced_filler = len([item for item in item_pool if not (item.advancement or item.useful)])

        # Fill with progression and useful items until there's no more valid locations
        for _ in range(num_nonexcluded_locations - num_preplaced_priority - max(NUM_JUNK_ITEMS + num_preplaced_filler - num_excluded_locations , 0) ):
            _list = (
                items_by_classification["progression"] if len(items_by_classification["progression"])
                else items_by_classification["prioritized_useful"] if len(items_by_classification["prioritized_useful"])
                else items_by_classification["useful"] if len(items_by_classification["useful"])
                else None
            )
            if _list:
                item_pool.append(_list.pop())
            else:
                break

        # Fill until we reach the junk threshold
        for _ in range(max(num_total_locations - len(item_pool) - NUM_JUNK_ITEMS, 0)):
            _list = items_by_classification["filler"]
            if len(_list):
                item_pool.append(_list.pop())
            else:
                break
        
        # If we ran out of locations to put things, then remaining items will be added into starting inventory
        for _list in items_by_classification.values():
            while len(_list):
                world.multiworld.push_precollected(_list.pop())
        
        # Fill up with junk items
        while len(item_pool) < len(world.multiworld.get_unfilled_locations(world.player)):
            item_pool.append(world.create_item(world.get_filler_item_name()))

        if len(item_pool) > len(world.multiworld.get_unfilled_locations(world.player)):
            print(f"{world.multiworld.get_player_name(world.player)} (Don't Starve Together): Warning! More items than locations!")

        world.multiworld.itempool += item_pool

    def get_filler_item_name(self, world: World) -> str:
        options:DSTOptions = world.options
        regulartrap_chance = float(options.trap_items.value) / 100
        seasontrap_chance = float(options.season_trap_items.value) / 100
        trap_percent = max(regulartrap_chance, seasontrap_chance)
        roll = world.multiworld.random.random()
        # Decide if we get a trap, and split chance between the two kinds
        target_pool = (
            self.filler_items if roll >= trap_percent
            else self.trap_items if roll < (regulartrap_chance / (regulartrap_chance + seasontrap_chance)) * trap_percent
            else self.seasontrap_items
        )
        if len(target_pool) > 0:
            return world.multiworld.random.choice(list(target_pool))
        return "20 Health"

    def set_progression_items(self, progression_dict:Dict[str, bool]):
        self.progression_items = frozenset([name for name, is_true in progression_dict.items() if is_true])
        self.prioritized_useful_items = frozenset([name for name, is_true in progression_dict.items() if not is_true])