# The Binding of Isaac: Repentance

## Where is the settings page?

The [player settings page for this game](../player-settings) contains all the options you need to configure and export a
config file.

## What does randomization do to this game?

The Binding of Isaac: Repentance is already random. The Archipelago mod only implements multiworld functionality in 
which certain pedestal items will be replaced with an *AP Check* item when you try to pick them up that will send an
item out to the multiworld. When an item gets replace is configured via the item pickup step setting. The items that 
*would have been* in those places will be returned to the player via grants by other players in other worlds.

## What is the goal of The Binding of Isaac: Repentance in Archipelago?

In The Binding of Isaac: Repentance the goal is always tied to a configurable amount of required locations. The goal can be 
just collecting that amount or beating a (also configurable) ending boss after collecting that amount. To reach that 
goal you will probably have to do multiple runs. 

## Does the mod affect my saves?

It does not. If you want to clear later bosses and don't want to bother with unlocking, you can use the 
[isaac-save-insaller by Zamiell](https://github.com/Zamiell/isaac-save-installer) to install a fully-unlocked save file 
and backup you old saves.

## Can you play multiplayer?

ToDo: needs testing

## What The Binding of Isaac: Repentance items can appear in other players' worlds?

By default, The Binding of Isaac items are:

* `Treasure Room Item`
* `Shop Item`
* `Boss Item`
* `Devil Deal Item`
* `Angle Deal Item`
* `Secret Room Item` 
* `Library Item`
* `Curse Room Item`
* `Planetarium Item`
* `Golden Chest Item`
* `Red Chest Item`
* "trash" items (pickups like random hearts, coins, etc.)
* (optionally) traps

Each item grants you a random in-game item from that item pool. Normally the items granted by other worlds will directly be added to your inventory, the exception being active items. 
If you cannot hold another active item the incoming item will spawn on a pedestal in the current room. 
"Trash" items will always spawn on the ground.

Items can also be configured to be from any item pool or even to be any specific item via custom item weights.


### How many items are there?

In The Binding of Isaac: Repentance you can configure how many collectible items (also known as
"checks") the game has. You can configure anywhere from **10 to 500** items. The number of items will be randomized 
between all players, so you may want to adjust the number and item pickup step based on how many items the other players
in the multiworld have. (Around 150 seems to be a good ballpark if you want to have a similar number of items to most 
other games.)

After you have completed the specified number of checks, you won't send anything else to the multiworld and items will 
not be replaced anymore, so you can continue playing as normal.

## What does another world's item look like in The Binding of Isaac: Repentance?

When the player reaches the next item pickup step then the next pedestal item you try to pickup will be replaced by an 
``AP Check`` item which sends out an item to another player's world (or possibly get sent back to yourself) on pickup.

## What is the item pickup step?

The item pickup step is a YAML setting which allows you to set how many items you need to spawn before the _next_ item
that you try to collect will be replaced with a ``AP Check`` item which will be sent out to the multiworld.

## Is Archipelago compatible with other The Binding of Isaac: Repentance mods?

ToDo: Needs testing
