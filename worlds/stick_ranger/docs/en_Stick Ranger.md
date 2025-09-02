# Stick Ranger

Welcome to Stick Ranger in Archipelago! Form your team of rangers, level up, and unlock new stages and classes as you journey through a randomized adventure!

## Where is the options page?

The [player options page for Stick Ranger](../player-options) contains all the configuration options you need to customize your experience and export a config file.

## What does randomization do to this game?

A Stage would normally be unlocked by completing the previous Stage, but Stage unlocks are now moved around. There is some logic available to make sure you do not end up with needing to complete late-game stages as your first in-logic check, so the game should always be completable.

If enabled, acquiring a book for a stage for the first time sends a check, and enemies have a chance to drop an item that sends a check. Ranger classes can also be shuffled into the item pool, making you start with only 1 class. Classes can be changed at the Forget Tree, which is also unlocked when you have class randomiser on.

## Which items can be in another player's world?

Stage unlocks and class unlocks (if enabled) may be placed into another player's world. Filler items can be traps (if enabled) or any weapon or compo.

## What does another world’s item look like in Stick Ranger?

Enemies that drop a check drop a small AP logo. Stage exits and books do not have anything different than normal.

## What is considered a location check in Stick Ranger?

- **Stage Exits:** Beating a stage for the first time sends a check.
- **Books:** Acquiring a book for a stage sends a check.
- **Enemy Defeats:** Enemies have a chance to drop a check item, depending on settings.

## When the player receives an item, what happens?

Stage unlocks and class unlocks are applied immediately.
Traps are only activated if you are in a playable state (so inside any stage, also shop stages).
Weapons and compos are given to you when you have space in your inventory.

## What is the goal of Stick Ranger when randomized?

The main goal is to reach and clear the end-game stage chosen in your YAML options (Hell Castle, Volcano, Mountaintop, or a mix of these).
