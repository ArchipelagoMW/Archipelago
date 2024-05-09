from typing import List
from worlds.AutoWorld import World
import random
from .Items import item_data_table, DSTItem
from .Options import DSTOptions
from .Constants import ITEM_ID_OFFSET

class DSTItemPool:
    nonfiller_items:set = set() # All items enabled by the options except junk
    filler_items:set = set()
    trap_items:set = set()
    seasontrap_items:set = set()
    locked_items_local_id:set = set()

    def decide_itempools(self, world:World) -> None:
        options:DSTOptions = world.options
        "Before generating, decide what items go in itempool categories"
        for name, item in item_data_table.items():
            if not item.code:
                continue

            if "deprecated" in item.tags:
                continue

            # Put junk items in the filler pool
            if "junk" in item.tags:
                self.filler_items.add(name)
                continue

            # Put trap items in the trap pools
            if "trap" in item.tags:
                (self.seasontrap_items if "seasontrap" in item.tags else self.trap_items).add(name)
                continue

            # Do not include items disabled by options
            if not options.shuffle_starting_recipes.value and "basic" in item.tags:
                continue

            if not options.shuffle_no_unlock_recipes.value and "nounlock" in item.tags:
                continue

            # All recipe items that must be locked in DST, converted to local id so that it uses less digits
            if not "physical" in item.tags:
                self.locked_items_local_id.add(item.code-ITEM_ID_OFFSET)

            # Add as nonfiller
            self.nonfiller_items.add(name)

    def create_items(self, world: World) -> None:
        item_pool: List[DSTItem] = []

        for name, item in item_data_table.items():
            if item.code and not "deprecated" in item.tags:
                if "junk" in item.tags:
                    self.filler_items.add(name)
                elif "trap" in item.tags:
                    (self.seasontrap_items if "seasontrap" in item.tags else self.trap_items).add(name)
                else:
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
        target_pool = self.filler_items if max(regulartrap_roll, seasontrap_roll) < 0.0 else self.trap_items if regulartrap_roll > seasontrap_roll else self.seasontrap_items
        if len(target_pool) > 0:
            return random.choice(list(target_pool))
        return "20 Health"