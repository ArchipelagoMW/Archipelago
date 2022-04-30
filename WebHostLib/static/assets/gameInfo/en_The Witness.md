# The Witness

## Where is the settings page?

The [player settings page for this game](../player-settings) contains all the options you need to configure and export a
config file.

## What does randomization do to this game?

Puzzles are randomly generated using the popular [Sigma Rando](https://github.com/sigma144/witness-randomizer).
They are made to be similar to the original game, but with different solutions.

Ontop of that each puzzle symbol (Squares, Stars, Dots, etc.) is now an item.
Panels with puzzle symbols on them are now locked initially.

## What is a "check" in The Witness?

Solving the last panel in a row of panels or an important standalone panel will count as a check, and send out an item.

## What "items" can you unlock in The Witness?

Every puzzle symbol and many other puzzle mechanics are items.
This includes symbols such as "Dots", "Black/White Squares", "Colored Squares", "Stars", "Symmetry", "Shapers" (coll. "Tetris Pieces"), "Erasers" and many more.

## The Jungle, Orchard, Forest and Color House aren't randomized. What gives?

There are limitations to what can currently be randomized in The Witness.
There is an option to turn these non-randomized panels off, called "disable_non_randomized" in your yaml file. This will also slightly change the activation requirement of certain panels, detailed [here](https://github.com/sigma144/witness-randomizer/wiki/Activation-Triggers).