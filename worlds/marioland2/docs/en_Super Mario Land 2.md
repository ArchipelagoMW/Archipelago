# Super Mario Land 2: 6 Golden Coins

## Where is the options page?

The [player options page for this game](../player-options) contains all the options you need to configure and export a
config file.

## What items and locations get shuffled?

Completing a level's exits results in a location check instead of automatically bringing you to the next level.
Where there are secret exits, the secret exit will be a separate location check. There is one exception, Hippo Zone,
that does not have a separate check for its secret exit. The Hippo Zone secret exit will still bring you to the Space
Zone.

Ringing the Midway Bells in each level that has one will register a location check. If the "Shuffle Midway Bells" option
is turned on, then ringing the bell will not grant the checkpoint, and instead you must obtain the Midway Bell item from
the item pool to gain the checkpoint for that level. Holding SELECT while loading into a level where you have unlocked
the Midway Bell checkpoint will start you at the beginning of the level.

Unlocking paths to new levels requires finding or receiving Zone Progression items. For example, receiving the first
"Turtle Zone Progression" will unlock the path from Turtle Zone 1 to Turtle Zone 2. Paths to secret levels are separate
items, so Turtle Zone Secret will open the path from Turtle Zone 2 to the Turtle Zone Secret Course.

Depending on settings, there may be some "Zone Progression x2" items that open two paths at once.

The path from Tree Zone 2 to the branch to Tree Zone 3 and 4 is one unlock, so both levels will open at this point.

Besides the zone progression unlocks, the following items are always shuffled:
- Mushroom: required to become Big Mario. If you are Fire or Bunny Mario and take damage, and have not obtained the
Mushroom, you will drop straight down to Small Mario.
- Fire Flower: required to become Fire Mario.
- Carrot: required to become Bunny Mario.
- Hippo Bubble: required to use the bubbles in Hippo Zone to fly.
- Water Physics: Mario will fall through water as though it is air until this is obtained.
- Space Physics: the Space Zone levels will have normal gravity until this is obtained.
- Super Star Duration Increase: you begin with a drastically lowered invincibility star duration, and these items will
increase it.

Additionally, the following items can be shuffled depending on your YAML options:
- The 6 Golden Coins: note that the game will still show you the coin being sent to the castle when defeating a boss
regardless of whether the coin is actually obtained in that location.
- Mario Coin Fragments: As an alternative to shuffling the 6 Golden Coins, you can shuffle Mario Coin Fragments,
a chosen percentage of which are needed to assemble the Mario Coin. You will start with the other 5 coins.
- Normal Mode/Easy Mode: you can start the game in Normal Mode with an Easy Mode "upgrade" in the item pool, or start in
Easy Mode with a Normal Mode "trap" item, swapping the difficulty.
- Auto Scroll: auto-scrolling levels can be set to not auto scroll until this trap item is received.
- Pipe Traversal: required to enter pipes. Can also be split into 4 items, each enabling pipe entry from a different
direction.
- Coins: if Coinsanity is enabled, coins will be shuffled into the item pool. A number of checks will be added to each
level for obtaining a specific number of coins within a single playthrough of the level.


## When the player receives an item, what happens?

There is no in-game indication that an item has been received. You will need to watch the client or web tracker to be
sure you're aware of the items you've received.

## Special Thanks to:

- [froggestspirit](https://github.com/froggestspirit) for his Super Mario Land 2 disassembly. While very incomplete, it
had enough memory values mapped out to make my work significantly easier.
- [slashinfty](https://github.com/slashinfty), the author of the
[Super Mario Land 2 Randomizer](https://sml2r.download/) for permitting me to port features such as Randomize Enemies
and Randomize Platforms directly from it.