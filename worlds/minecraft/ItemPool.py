from math import ceil
from typing import List

from BaseClasses import Item

from . import Constants
from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from . import MinecraftWorld


def get_junk_item_names(rand, k: int) -> str:
	junk_weights = Constants.item_info["junk_weights"]
	junk = rand.choices(
		list(junk_weights.keys()),
		weights=list(junk_weights.values()),
		k=k)
	return junk

def build_item_pool(world: "MinecraftWorld") -> List[Item]:
	multiworld = world.multiworld
	player = world.player

	itempool = []
	total_location_count = len(multiworld.get_unfilled_locations(player))

	required_pool = Constants.item_info["required_pool"]

	# Add required progression items
	for item_name, num in required_pool.items():
		itempool += [world.create_item(item_name) for _ in range(num)]

	# Add structure compasses
	if world.options.structure_compasses:
		compasses = [name for name in world.item_name_to_id if "Structure Compass" in name]
		for item_name in compasses:
			itempool.append(world.create_item(item_name))

	# Dragon egg shards
	if world.options.egg_shards_required > 0:
		num = world.options.egg_shards_available
		itempool += [world.create_item("Dragon Egg Shard") for _ in range(num)]

	# Bee traps
	bee_trap_percentage = world.options.bee_traps * 0.01
	if bee_trap_percentage > 0:
		bee_trap_qty = ceil(bee_trap_percentage * (total_location_count - len(itempool)))
		itempool += [world.create_item("Bee Trap") for _ in range(bee_trap_qty)]

	# Fill remaining itempool with randomly generated junk
	junk = get_junk_item_names(world.random, total_location_count - len(itempool))
	itempool += [world.create_item(name) for name in junk]

	return itempool
