# Saving Princess

## Quick Links
- [Setup Guide](/tutorial/Saving%20Princess/setup/en)
- [Options Page](/games/Saving%20Princess/player-options)
- [Saving Princess Archipelago GitHub](https://github.com/LeonarthCG/saving-princess-archipelago)

## What changes have been made?

The game has had several changes made to add new features and prevent issues. The most important changes are the following:
- There is an in-game connection settings menu, autotracker and client console.
- New save files are created and used automatically for each seed and slot played.
- The game window can now be dragged and a new integer scaling option has been added.

## What items and locations get shuffled?

The chest contents and special weapons are the items and locations that get shuffled.

Additionally, there are new items to work as filler and traps, ranging from a full health and ammo restore to spawning a Ninja on top of you.

The Expanded Pool option, which is enabled by default, adds a few more items and locations:
- Completing the intro sequence, powering the generator with the Volt Laser and defeating each boss become locations.
- 4 Keys will be shuffled, which serve to open the door to the final area in place of defeating the main area bosses.
- A System Power item will be shuffled, which restores power to the final area instead of this happening when the generator is powered.

## What does another world's item look like in Saving Princess?

Some locations, such as boss kills, have no visual representation, but those that do will have the Archipelago icon.

Once the item is picked up, a textbox will inform you of the item that was found as well as the player that will be receiving it.

These textboxes will have colored backgrounds and comments about the item category.
For example, progression items will have a purple background and say "Looks plenty important!".

## When the player receives an item, what happens?

When you receive an item, a textbox will show up.
This textbox shows both which item you got and which player sent it to you.

If you send an item to yourself, however, the sending player will be omitted.

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
- `/iframes n` Sets the iframe duration % multiplier to n, where 0 <= n <= 400.
- `/shake n` Sets the shake intensity % multiplier to n, where 0 <= n <= 100.
