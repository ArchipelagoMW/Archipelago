# ChecksFinder

## Where is the settings page?

The [player settings page for this game](../player-settings) contains all the options you need to configure and export a
config file.

## What is considered a location check in ChecksFinder?

Location checks in are completed when the player finds a spot on a board that has the archipelago logo. The bottom of
the screen has a number next to the archipelago logo, that number is how many you can find so far. You can only get as 
many checks as you have gained items, plus five to start with being available.

## When the player receives an item, what happens?

When the player receives an item in ChecksFinder, it either can make the future boards they play be bigger in width or
height, or add a new bomb to the future boards, with a limit to having up to one fifth of the _current_ board being
bombs. The items you have gained _before_ the current board was made will be said at the bottom of the screen as a
number
next to an icon, the number is how many you have gotten and the icon represents which item it is.

## What is the victory condition?

Victory is achieved when the player wins a board they were given after they have received all of their Map Width, Map
Height, and Map Bomb items. The game will say at the bottom of the screen how many of each you have received.

## Unique Local Commands

The following command is only available when using the ChecksFinderClient to play with Archipelago.

- `/resync` Manually trigger a resync.
