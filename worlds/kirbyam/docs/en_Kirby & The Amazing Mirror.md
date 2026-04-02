\# Kirby \& The Amazing Mirror



## Where is the options page?



As this is a custom AP world you will need to first install Kirby & The Amazing Mirror's apworld, then run the Archipelago launcher and open Options Creator. Select Kirby & The Amazing Mirror and your options and then choose your save destination.



## What does randomization do to this game?


Items which the player would normally acquire throughout the game have been moved around. (Maps, Vitality, Sound Player)
Abilities enemies provide can be randomized to give another copy ability.

An optional Room Sanity mode is also available (`room_sanity`). When enabled, room visits become AP checks using labels like `Room 1-01` and `Room 9-27`. Room Sanity is disabled by default because it adds 257 checks.



## What items and locations get randomized?



Locations in which items can be found:
- All Big Chests
- All Mirror Shards
- All Rooms
Items that can be shuffled:
- All Mirror Shards
- All Maps
- All Vitality
- Sound Player
- All consumable items (Small Food, Battery, Maximum Tomato, Invincibility Candy)


## Common Item/Location Options

KirbyAM supports the standard Archipelago common options for item and location control:

- `local_items`: force selected item names/groups to stay in your world.
- `non_local_items`: force selected item names/groups out of your world.
- `start_inventory`: begin with selected items precollected.
- `start_hints`: begin with hints for selected item names/groups.
- `start_location_hints`: begin with hints for selected location names.
- `exclude_locations`: remove selected locations from placement.
- `priority_locations`: bias selected locations toward important item placement.
- `item_links`: configure linked/shared item pools across players.
- `plando_items`: explicitly plan item placement.

Use exact item/location names from this world (or the item groups listed above) when configuring these fields.



## What other changes are made to the game?



Additional changes planned, none currently implemented.



## What does another world's item look like in Kirby \& The Amazing Mirror?



When you find an item that is not your own, you will be able to see what it was and who it was sent to in both Bizhawk and the Archipelago Bizhawk client. The sprite for the item will still appear, but you will need to receive it via Archipelago before it's usable.



## When the player receives an item, what happens?



You will not see an indicator in the game, instead you'll see you received an item from the client window.



\# Can I play offline?



Yes, the client and connector are only necessary for sending and receiving items. If you're playing a solo game, you
don't need to play online unless you want the rest of Archipelago's functionality (like hints). If
you're playing a multiworld game, the client will sync your game with the server the next time you connect.



## Acknowledgements



\[jiangzhengwenjz](https://github.com/jiangzhengwenjz) and other contributors — creators of the \[Kirby \& The Amazing Mirror disassembly](https://github.com/jiangzhengwenjz/katam), which was instrumental in understanding ROM internals for this integration.

