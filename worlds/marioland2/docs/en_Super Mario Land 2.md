# Super Mario Land 2: 6 Golden Coins

## Where is the settings page?

The [player settings page for this game](../player-settings) contains all the options you need to configure and export a
config file.

## What items and locations get shuffled?

Completing a level's normal exit OR secret exit results in a location check for that level. Completing a normal exit
does not automatically unlock the next level, but completing a secret exit does always bring you to the secret course.
This means that if you can complete the secret exit, you do not need to return to complete the normal exit, as the check
for the level will have been registered already.

Unlocking "normal exit" paths requires shuffled zone progression items. So, for example, finding or receiving a "Tree
Zone Progression" will unlock the path from Tree Zone 1 to Tree Zone 2.

Besides the zone progression unlocks, the following items are always shuffled:
- Mushroom: required to become Big Mario. If you are Fire or Bunny Mario and take damage, and have not obtained the
Mushroom, you will drop straight down to Small Mario.
- Fire Flower: required to become Fire Mario.
- Carrot: required to become Bunny Mario.
- Swim: Mario will fall through water as though it is air until this is obtained.
- Hippo Bubble: required to use the bubbles in Hippo Zone to fly.
- Space Physics: the Space Zone levels will have normal gravity until this is obtained.
- Super Star Duration Increase: you begin with a drastically lowered invincibility star duration, and these items will
increase it.

Additionally, the following items can be shuffled depending on your YAML settings:
- The 6 Golden Coins: note that the game will still show you the coin being sent to the castle when defeating a boss
regardless of whether the coin is actually obtained in that location.
- Midway Bells: ringing bells results in a location check, and the midway check points are shuffled as items.
Note that you may have to backtrack from the midway point to reach some secret exits!
- Normal Mode/Easy Mode: you can start the game in Normal Mode with an Easy Mode "upgrade" in the item pool, or start in
Easy Mode with a Normal Mode "trap" item, swapping the difficulty.
- Auto Scroll: auto-scrolling levels can be set to not auto scroll until this trap item is received.

## When the player receives an item, what happens?

There is no in-game indication that an item has been received. You will need to watch the client to be sure you're aware
of the items you've received.