from math import ceil
from typing import List

from BaseClasses import MultiWorld, Item
from worlds.AutoWorld import World

from . import Constants

def get_junk_item_names(rand, k: int) -> str:
	junk_weights = Constants.item_info["junk_weights"]
	junk = rand.choices(
		list(junk_weights.keys()),
		weights=list(junk_weights.values()),
		k=k)
	return junk

def build_item_pool(self: World) -> List[Item]:
	multiworld = self.multiworld
	player = self.player

	itempool = []
	total_location_count = len(multiworld.get_unfilled_locations(player))

	required_pool = Constants.item_info["required_pool"]
	junk_weights = Constants.item_info["junk_weights"]

	# Add required progression items
	for item_name, num in required_pool.items():
		itempool += [self.create_item(item_name) for _ in range(num)]

	# Add structure compasses
	if self.options.structure_compasses.value:
		compasses = [name for name in self.item_name_to_id if "Structure Compass" in name]
		for item_name in compasses:
			itempool.append(self.create_item(item_name))

	# Dragon egg shards
	if self.options.egg_shards_required.value > 0:
		num = self.options.egg_shards_available.value
		itempool += [self.create_item("Dragon Egg Shard") for _ in range(num)]

	# Bee traps
	bee_trap_percentage = self.options.bee_traps.value * 0.01
	if bee_trap_percentage > 0:
		bee_trap_qty = ceil(bee_trap_percentage * (total_location_count - len(itempool)))
		itempool += [self.create_item("Bee Trap") for _ in range(bee_trap_qty)]

	# Fill remaining itempool with randomly generated junk
	junk = get_junk_item_names(self.random, total_location_count - len(itempool))
	itempool += [self.create_item(name) for name in junk]

	return itempool
