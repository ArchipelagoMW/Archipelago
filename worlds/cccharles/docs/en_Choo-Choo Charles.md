# Choo-Choo Charles

## Game page in other languages
* [Français](fr)

## Where is the options page?
The [Player Options page](../player-options) contains all the options to configure and export a yaml config file.

## What does randomization do to this game?
All scraps or any collectable item on the ground (except from Loot Crates) and items received from NPCs missions are considered as locations to check.

## What is the goal of Choo-Choo Charles when randomized?
Beating the evil train from Hell named "Charles".

## How is the game managed in Nightmare mode?
At death, the player has to restart a brand-new game, giving him the choice to stay under the Nightmare mode or continuing with the Normal mode if considered too hard.
In this case, all collected items will be redistributed in the inventory and the missions states will be kept.
The Deathlink is not implemented yet. When this option will be available, a choice will be provided to:
* Disable the Deathlink
* Enable the soft Deathlink with respawn at Player Train when a Deathlink event is received
* Enable the hard Deathlink with removal of the game save when a Deathlink event is received

## What does another world's item look like in Choo-Choo Charles?
Items appearance are kept unchanged.
Any hint that cannot be normally represented in the game is replaced by the miniaturized "DeathDuck" Easter Egg that can be seen out from the physical wall limits of the original game.

## How is the player informed by an item transmission and hints?
A message appears in game to inform what item is sent or received, including which world and what player the item comes from.
The same method is used for hints.

## Is it possible to use hints in the game?
No, this is a work in progress.
The following options will be possible once the implementations are available:

At any moment, the player can press one of the following keys to display a console in the game:
* "~" or "`" (qwerty)
* "²" (azerty)
* "F10"
Then, a hint can be revealed by typing "/hint [player] <item>".
