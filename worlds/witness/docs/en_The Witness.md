# The Witness

## Where is the options page?

The [player options page for this game](../player-options) contains all the options you need to configure and export a
config file.

## What does randomization do to this game?

Puzzles are randomly generated using the popular [Sigma Rando](https://github.com/sigma144/witness-randomizer).
They are made to be similar to the original game, but with different solutions.

On top of that, each puzzle symbol (Squares, Stars, Dots, etc.) is now an item.
Panels with puzzle symbols on them are now locked initially.

## What is a "check" in The Witness?

Solving the last panel in a row of panels or an important standalone panel will count as a check, and send out an item.
It is also possible to add Environmental Puzzles into the location pool via the "Shuffle Environmental Puzzles" option.

## What "items" can you unlock in The Witness?

Every puzzle symbol and many other puzzle mechanics are items.
This includes symbols such as "Dots", "Black/White Squares", "Colored Squares", "Stars", "Symmetry", "Shapers" (coll. "Tetris Pieces"), "Erasers" and many more.

Alternatively (or additionally), you can play "Door shuffle", where some doors won't open until you receive their "key".

You can also set lasers to be items you can receive.

## What else can I find in the world?

By default, the audio logs scattered around the world will have 10 hints for your locations or items on them. 

Example: "Shipwreck Vault contains Triangles".

## The Jungle, Orchard, Forest and Color Bunker aren't randomized. What gives?

There are limitations to what can currently be randomized in The Witness.
There is an option to turn these non-randomized panels off, called "disable_non_randomized" in your yaml file. This will also slightly change the activation requirement of certain panels, detailed [here](https://github.com/sigma144/witness-randomizer/wiki/Activation-Triggers).

## A note on starting inventory and excluded locations

In this randomizer, items added to start_inventory will be removed from the item pool (as many copies as specified).

It is also possible to add items to the starting inventory that are not part of the mode you are playing.
In this case, the generator will make its best attempt to adjust logic accordingly.
One of the use cases of this could be to pre-open a specific door or pre-activate a single laser.

In "shuffle_EPs: obelisk_sides", any Environmental Puzzles in exclude_locations will be pre-completed and not considered for their Obelisk Side.
If every Environmental Puzzle on an Obelisk Side is pre-completed, that side disappears from the location pool entirely.
