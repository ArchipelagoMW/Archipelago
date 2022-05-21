# Risk of Rain 2

## Where is the settings page?

The [player settings page for this game](../player-settings) contains all the options you need to configure and export a
config file.

## What does randomization do to this game?

Risk of Rain is already a random game, by virtue of being a roguelite. The Archipelago mod implements pure multiworld
functionality in which certain chests (made clear via a location check progress bar) will send an item out to the
multiworld. The items that _would have been_ in those chests will be returned to the Risk of Rain player via grants by
other players in other worlds.

## What is the goal of Risk of Rain 2 in Archipelago?

There are several ways you can finish a Risk of Rain 2 run:

- Reach the final stage (Commencement) and die
- Defeat the final boss, Mythrix
- Reach the Obelisk and obliterate yourself
    - Note, if you die while fighting the secret boss at **A Moment, Whole** this does not count as a win.

If you die before you accomplish your goal, you can start a new run. You will start the run with any items that you received from other players. Any items that you picked up the "normal" way will be lost.

Note, you can play Simulacrum mode as part of an Archipelago, but you can't achieve any of the victory conditions in Simulacrum. So you can, for example, collect most of your items through a Simulacrum run, then finish a normal mode run while holding anything you received via the multiworld.

## Can you play multiplayer?

Yes! You can have a single multiplayer instance as one world in the multiworld. All the players involved need to have the Archipelago mod, but only the host needs to configure the Archipelago settings. When someone finds an item for your world, all the connected players will receive a copy of the item, and the location check bar will increase whenever any player finds an item in Risk of Rain.

## What Risk of Rain items can appear in other players' worlds?

The Risk of Rain items are:

* `Common Item`    (White items)
* `Uncommon Item`  (Green items)
* `Boss Item`      (Yellow items)
* `Legendary Item` (Red items)
* `Lunar Item`     (Blue items)
* `Equipment`      (Orange items)
* `Dio's Best Friend` (Used if you set the YAML setting `total_revives_available` above `0`)

Each item grants you a random in-game item from the category it belongs to.

When an item is granted by another world to the Risk of Rain player (one of the items listed above) then a random
in-game item of that tier will appear in the Risk of Rain player's inventory. If the item grant is an `Equipment` and
the player already has an equipment item equipped then the _item that was equipped_ will be dropped on the ground and _
the new equipment_ will take it's place. (If you want the old one back, pick it up.)

### How many items are there?

Since a Risk of Rain 2 run can go on indefinitely, you have to configure how many collectible items (also known as "checks") the game has for purposes of Archipelago when you set up a multiworld. You can configure anywhere from **10 to 500** items. The number of items will be randomized between all players, so you may want to adjust the number and item pickup step based on how many items the other players in the multiworld have.

## What does another world's item look like in Risk of Rain?

When the Risk of Rain player fills up their location check bar then the next spawned item will become an item grant for
another player's world. The item in Risk of Rain will disappear in a poof of smoke and the grant will automatically go
out to the multiworld.

## What is the item pickup step?

The item pickup step is a YAML setting which allows you to set how many items you need to spawn before the _next_ item
that is spawned disappears (in a poof of smoke) and goes out to the multiworld.

## Is Archipelago compatible with other Risk of Rain 2 mods?

Mostly, yes. Not every mod will work; in particular, anything that causes items to go directly into your inventory rather than spawning onto the map will interfere with the way the Archipelago mod works. However, many common mods work just fine with Archipelago.

For competitive play, of course, you should only use mods that are agreed-upon by the competitors so that you don't have an unfair advantage.
