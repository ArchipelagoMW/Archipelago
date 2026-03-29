\# Kirby \& The Amazing Mirror



## Where is the options page?



You can read through all the options and generate a YAML here.



## What does randomization do to this game?



This randomizer currently treats boss defeats, major chests, vitality chests, and sound player chests as primary AP checks. In vanilla shard mode, each area's boss defeat check awards that area's shard as the AP item. In completely random shard mode, shards can appear at any physical check.

An optional Room Sanity mode is also available (`room_sanity`). When enabled, room visits become AP checks using labels like `Room 1-01` and `Room 9-27`. Room Sanity is disabled by default because it adds 257 checks.



## What items and locations get randomized?



The locations of Shards, Maps, Vitality Counters, and the Sound Player are all randomized. For example, the big chest in Moonlight Mansion might contain the mirror shard that normally drops from defeating Wiz.
Boss defeats are separate checks from shard progression. Shards are delivered through Archipelago item placement instead of being granted directly by boss defeats.

If Room Sanity is enabled, each eligible NORMAL/BIG room visit is also a randomized check. Special STAR/UNKNOWN rooms are excluded from Room Sanity in the current implementation.



## Item Groups

The KirbyAM world defines the following item groups for use in YAML-based item/location filters (e.g., `local_items`, plando, multiworld hints):

| Group Name | Also Known As | Items Included | Use Case |
|---|---|---|---|
| `Shards` | `Shard` | One shard per area (8 total) | Boss-defeat progression items; use in `local_items` if you want local shard discovery |
| `Unique` | — | Mirror shards + maps + Sound Player + vitality counters | One-of-a-kind progression items; often treated as important progression |
| `Maps` | `Map` | Area map items (9 total) | Area maps; non-critical but helpful for navigation |
| `Vitality` | Vitality Counters | Vitality counter upgrades (I, II, III, IV) | Life upgrades; use in plando to guarantee health increases |
| `Useful` | — | Maps + vitality counters + Sound Player | Non-critical progression enhancers; useful for strategic item placement |
| `Filler` | — | 1-Up, 2-Up, 3-Up | Generic filler items; often used as low-priority junk |

**Example Usage:**

- To require all shards to be found locally (not in other worlds): Add `Shards: all` to `local_items` in your YAML.
- To exclude maps from consideration as progression in a difficult plando: Use `!include_group items: [Filler, Vitality]` to seed only filler + vitality items.
- To ensure you get at least one helpful item early: Plando the first chest to require an item from the `Useful` group.



## What other changes are made to the game?



Additional changes planned, none currently implemented.



## What does another world's item look like in Kirby \& The Amazing Mirror?



When you find an item that is not your own, you will be able to see what it was and who it was sent to in the client window. The sprite for the item will still appear, but you will need to receive it via Archipelago before it's usable.



## When the player receives an item, what happens?



You will not see an indicator in the game, instead you'll see you received an item from the client window.



\# Can I play offline?



Yes, the client and connector are only necessary for sending and receiving items. If you're playing a solo game, you
don't need to play online unless you want the rest of Archipelago's functionality (like hints). If
you're playing a multiworld game, the client will sync your game with the server the next time you connect.



## Acknowledgements



\[jiangzhengwenjz](https://github.com/jiangzhengwenjz) and other contributors — creators of the \[Kirby \& The Amazing Mirror disassembly](https://github.com/jiangzhengwenjz/katam), which was instrumental in understanding ROM internals for this integration.

