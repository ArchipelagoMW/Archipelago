# Saving Princess

## Where is the options page?

The [player options page for this game](../player-options) contains all the options you need to configure and export a config file.

## What does randomization do to this game?

The contents of all chests are shuffled into the pool.
These chests become locations where items from this or the other games in the MultiWorld can be found.

Because of this, the player may end up fighting a boss or getting through an area with a different set of upgrades available to them compared to a vanilla playthrough.

In Expanded Pool, the way to open the final area of the game changes, going from having to defeat bosses to having to locate some items, which can also alter the order the game is tackled in.

Finally, there are also new items to work as filler and traps, ranging from a full health and ammo restore to spawning a Ninja on top of you.

## Are there any other changes made?

The game has had several changes made to add new features, fix original issues and prevent new ones. 

The most important changes to know are the following:
- There is an in-game connection settings menu, autotracker and client console.
- New save files are created and used automatically for each seed and slot played.
- The game window can now be dragged and a new integer scaling option has been added.

## What is the goal of Saving Princess when randomized?

You must defeat the final boss and escape the space station in time after securing your mission objective.

In short, the goal is unchanged.

## What items and locations get shuffled?

The chests and special weapons in the game and their contents are the locations and items that get shuffled.

By default, bosses are also made into locations, meaning that defeating a boss will count as a check.
The door to the final area will open once the player has received the 4 Keys which will be shuffled, instead of when the main area bosses are defeated.

## Which items can be in another player's world?

Any shuffled item can be in other players' worlds.

## What does another world's item look like in Saving Princess?

Some locations, such as boss kills, have no visual representation, but those that do will have either a vanilla sprite corresponding to the item or, if it's an item from a different game, the Archipelago icon.

Once the item is picked up a textbox will, without halting gameplay, inform you of the item that was found as well as the player that will be receiving it.

These textboxes will have colored backgrounds and comments about the item category, as well.
For example, Progression items will have a purple background and say "Looks plenty important!".

## When the player receives an item, what happens?

When you receive an item, a textbox will show up.
This textbox shows both which item you got and which player sent it to you.

If you send an item to yourself, however, the sending player will be omitted.
If the items are cheated in, no textbox will be displayed.

## Unique Local Commands

The following commands are only available when using the in-game console in Saving Princess:
- `/help` Returns the help listing.
- `/options` Lists currently applied options.
- `/resync` Manually triggers a resync. This also resends all found locations.
- `/unstuck` Sets save point to the first save point. Portia is then killed.
- `/deathlink [on|off]` Toggles or sets death link mode.
- `/instantsaving [on|off]` Toggles or sets instant saving.
- `/sprint {never|always|jacket}` Sets sprint mode.
- `/cliff {never|always|vanilla}` Sets Cliff's weapon upgrade condition.
- `/ace {never|always|vanilla}` Sets Ace's weapon upgrade condition.
- `/shake n` Sets the shake intensity % multiplier to n, where 0 <= n <= 100.
- `/iframes n` Sets the iframe duration % multiplier to n, where 0 <= n <= 400.
