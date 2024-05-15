from typing import List, Set
from worlds.AutoWorld import World
from BaseClasses import ItemClassification as IC
import random
from .Items import item_data_table, DSTItem
from .Options import DSTOptions
from .Constants import ITEM_ID_OFFSET

class DSTItemPool:
    nonfiller_itempool:List[str] = list() # All items enabled by the options except junk
    filler_items:Set = set()
    trap_items:Set = set()
    seasontrap_items:Set = set()
    locked_items_local_id:Set = set()

    def decide_itempools(self, world:World) -> None:
        "Before generating, decide what items go in itempool categories"
        options:DSTOptions = world.options
        self.nonfiller_itempool = list()
        for name, item in item_data_table.items():
            # Do not include things that are deprecated or disabled by options
            if (
                not item.code
                or "deprecated" in item.tags
                or "progressive" in item.tags # Add these somewhere else
                or (not options.shuffle_no_unlock_recipes.value and "nounlock" in item.tags)
                or (not options.season_change_helper_items.value and "seasonhelper" in item.tags)
            ):
                continue

            # Add basic items as dummy event items so we can do logic with them
            if (item.type == IC.progression and not options.shuffle_starting_recipes.value and "basic" in item.tags):
                world.multiworld.precollected_items[world.player].append(DSTItem(name, IC.progression, None, world.player))

            # Put junk items in the filler pool
            if "junk" in item.tags:
                self.filler_items.add(name)
                continue

            # Put trap items in the trap pools
            if "trap" in item.tags:
                (self.seasontrap_items if "seasontrap" in item.tags else self.trap_items).add(name)
                continue

            # All recipe items that must be locked in DST, converted to local id so that it uses less digits
            if not "physical" in item.tags:
                self.locked_items_local_id.add(item.code-ITEM_ID_OFFSET)

            # Add as nonfiller
            self.nonfiller_itempool.append(name)
        
        # Handle progressive items here
        for _ in range(options.extra_damage_against_bosses.value):
            self.nonfiller_itempool.append("Extra Damage Against Bosses")


    def create_items(self, world: World) -> None:
        item_pool: List[DSTItem] = []

        for name in self.nonfiller_itempool:
            item_pool.append(world.create_item(name))
        
        # Fill up with filler items
        while len(item_pool) < len(world.multiworld.get_unfilled_locations(world.player)):
            item_pool.append(world.create_item(world.get_filler_item_name()))

        world.multiworld.itempool += item_pool

    def get_filler_item_name(self, world: World) -> str:
        options:DSTOptions = world.options
        WEIGHTS = {
            "none": 0.0,
            "low": 0.2,
            "medium": 0.5,
            "high": 0.8,
        }
        # Decide if we get a trap, and choose the one with the highest number
        regulartrap_roll = WEIGHTS[options.trap_items.current_key] - random.random()
        seasontrap_roll = WEIGHTS[options.season_trap_items.current_key] - random.random()
        target_pool = (
            self.filler_items if max(regulartrap_roll, seasontrap_roll) < 0.0 
            else self.trap_items if regulartrap_roll > seasontrap_roll 
            else self.seasontrap_items
        )
        if len(target_pool) > 0:
            return random.choice(list(target_pool))
        return "20 Health"