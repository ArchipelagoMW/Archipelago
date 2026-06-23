# Shellipelago

## Where is the options page?

The [player options page for this game](../player-options) contains all the options you need to configure and export a config file.

## What does randomization do to this game?

Shellipelago shuffles the items needed to explore the map, fight enemies, and complete the final run.

The main progression items are Graphics, Progressive Room, Bombs, Gun, Sword, Fire, Pickaxe, Water Walkers, Tank Treads, Tank Chassis, and Tank Cannon. Max HP, Max Rounds, Energy, SFX, and BGM can also be shuffled depending on options.

## What is the goal of Shellipelago?

Defeat the final boss in the final run.

## What are location checks in Shellipelago?

Chests and shops are location checks by default.

Optional checks can also be added for destructible objects, defeated enemies, and item-pool drops.

The location list is generated from Shellipelago's map data so that Archipelago logic matches the browser game.

## Which items can be in another player's world?

Progression items, resource upgrades, traps, and filler items can be placed in another player's world. The item placement options can limit whether essential items, resource upgrades, or traps stay local.

## When the player receives an item, what happens?

The browser client shows a message and applies the item immediately. Some received items unlock abilities, increase resources, change presentation, or trigger traps.

## What do the options do?

- `shuffle_essential_items`: Shuffles essential progression items. When off, those items are given at the start.
- `essential_items_in_my_world`: Controls which essential items may be placed in your world.
- `essential_items_in_other_worlds`: Controls which essential items may be placed in other players' worlds.
- `shuffle_max_resource_upgrades`: Shuffles Max HP and Max Rounds upgrades. When off, those upgrades are given at the start.
- `max_resource_upgrades_in_my_world`: Controls which max resource upgrades may be placed in your world.
- `max_resource_upgrades_in_other_worlds`: Controls which max resource upgrades may be placed in other players' worlds.
- `add_easy_destructible_checks`: Adds normal destructible objects as checks.
- `enemies_are_checks`: Adds defeated enemies as checks.
- `enemies_are_hints`: Allows selected enemy defeats to create Archipelago hints for useful or progression Shellipelago locations.
- `shuffle_shops`: Shuffles shop item locations.
- `show_essential_pickup_hints`: Shows special graphics for essential pickups in the client.
- `add_traps_to_pool`: Allows trap items to be placed as rewards. When off, vanilla trap locations are replaced with filler.
- `trap_pool_spawn`: Controls which traps can activate from trap items.
- `trap_pool_in_my_world`: Controls which trap items may be placed in your world.
- `trap_pool_in_other_worlds`: Controls which trap items may be placed in other players' worlds.
- `other_players_can_find_item_pool_drops`: Adds item-pool-only drops as checks.
- `ring_link`: Shares ring pickups with other linked Shellipelago players.
- `energy_link`: Shares energy pickups with other linked Shellipelago players.
- `death_link`: Sends and receives DeathLink events.
- `trap_link`: Sends and receives trap events with other linked Shellipelago players.
- `item_link`: Shares supported item pickups with other linked Shellipelago players.
