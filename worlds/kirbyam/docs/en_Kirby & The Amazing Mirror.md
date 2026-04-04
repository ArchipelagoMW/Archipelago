\# Kirby \& The Amazing Mirror



## Where is the options page?



- As this is a custom AP world you will need to first install Kirby & The Amazing Mirror's apworld, then run the Archipelago launcher and open Options Creator. Select Kirby & The Amazing Mirror and your options and then choose your save destination. 
- If you prefer to setup your options via a standard yaml file, you will need to first install Kirby & The Amazing Mirror's apworld, run the Archipelago launcher, and select the Generate Template Options. A file explorer will open which you can then locate the Kirby & The Amazing Mirror yaml file to edit.



## What does randomization do to this game?



- Progression & useful items which the player would normally acquire throughout the game have been moved around. (Mirror Shards, Maps, Vitality, Sound Player)
- Normal copy ability enemies can be randomized to give a different copy ability.
- Enemies which typically do not give abilities can be randomized to give abilities.
- The chance for an enemy to not have a copy ability can be controlled via the `ability_randomization_no_ability_weight`



## What items and locations get randomized?



Locations in which items can be found:
- All Big Chests
- All Mirror Shards
- All Rooms (Optional, not enabled by default)
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



- There is an optional setting to enable one-life mode (no_extra_lives). If you die you are instantly sent back to the Hub, and any 1Ups you receive will be immediately removed.
- There is an optional setting to enable one-hit mode. Kirby's HP cap is clamped to 1 plus collected Vitality Counters. In `exclude_vitality_counters` mode, Vitality Counter items are removed from the item pool and health-restoring filler (Small Food and Max Tomato) is also removed from filler selection so randomized filler cannot counteract the 1 HP challenge.



## What does another world's item look like in Kirby \& The Amazing Mirror?



When you find an item that is not your own, you will be able to see what it was and who it was sent to in both Bizhawk and the Archipelago Bizhawk client. The sprite for the item will still appear, but you will need to receive it via Archipelago before it's usable. When collecting a mirror shard check, the cutscene will still play as if you've received the mirror shard, however it will not be given until you receive it properly via Archipelago.



## When the player receives an item, what happens?



You will not see an indicator in the game, instead you'll see you received an item from the client window.



## Trackers



Currently a tracker is not available, however with the current version the only logic is that you need all 8 mirror shards to goal the game. Everything else is considered to always be in logic.



\# Can I play offline?



Yes, the client and connector are only necessary for sending and receiving items. If you're playing a solo game, you
don't need to play online unless you want the rest of Archipelago's functionality (like hints). If
you're playing a multiworld game, the client will sync your game with the server the next time you connect.



## Acknowledgements



\[jiangzhengwenjz](https://github.com/jiangzhengwenjz) and other contributors — creators of the \[Kirby \& The Amazing Mirror disassembly](https://github.com/jiangzhengwenjz/katam), which was instrumental in understanding ROM internals for this integration.

