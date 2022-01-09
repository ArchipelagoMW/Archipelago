# Risk of Rain 2

## Where is the settings page?

The [player settings page for this game](../player-settings) contains all the options you need to configure and export a
config file.

## What does randomization do to this game?

Risk of Rain is already a random game, by virtue of being a roguelite. The Archipelago mod implements pure multiworld
functionality in which certain chests (made clear via a location check progress bar) will send an item out to the
multiworld. The items that _would have been_ in those chests will be returned to the Risk of Rain player via grants by
other players in other worlds.

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

## What does another world's item look like in Risk of Rain?

When the Risk of Rain player fills up their location check bar then the next spawned item will become an item grant for
another player's world. The item in Risk of Rain will disappear in a poof of smoke and the grant will automatically go
out to the multiworld.

## What is the item pickup step?

The item pickup step is a YAML setting which allows you to set how many items you need to spawn before the _next_ item
that is spawned disappears (in a poof of smoke) and goes out to the multiworld.
