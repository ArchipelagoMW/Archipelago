# Pokémon Red and Blue

## Where is the settings page?

The [player settings page for this game](../player-settings) contains all the options you need to configure and export a
config file.

## What does randomization do to this game?

Items which the player would normally acquire throughout the game have been moved around. Logic remains, so the game is
always able to be completed, but because of the item shuffle the player may need to access certain areas before they
would in the vanilla game.

A great many things besides item placement can be randomized, such as the location of Pokémon, their stats, types, etc., depending on your yaml settings.

Many baseline changes are made to the game, including:

* You can hold B to run (or bike extra fast!).
* You can hold select while talking to a trainer to re-battle them.
* Seafoam Islands entrances are swapped.
* The S.S. Anne will never depart.
* After obtaining one of the fossil item checks in Mt Moon, the remaining item can be received from the Cinnabar Lab
fossil scientist after reviving a Pokémon from a fossil.
* A hidden item location that was outside the bounds of the Safari Zone Gate map has been moved to a reachable tile on
this screen. Another hidden item location that was on an unused map has been moved to the Vermilion Dock truck
* Obedience depends on the total number of badges you have obtained instead of depending on specific badges.

## What items and locations get shuffled?

All items that go into your bags given by NPCs or found on the ground, as well as gym badges.
Optionally, hidden items (those located with the Item Finder) can be shuffled as well.

## Which items can be in another player's world?

Any of the items which can be shuffled may also be placed into another player's world.
By default, gym badges are shuffled across only the 8 gyms, but you can turn on Badgesanity in your yaml to shuffle them
into the general item pool.

## What does another world's item look like in Pokémon Red and Blue?

All items for other games will display simply as "AP ITEM," including those for other Pokémon Red and Blue games.

## When the player receives an item, what happens?

A "received item" sound effect will play. Currently there is no in-game message informing you of what the item is.
If you are in battle, have menus or text boxes opened, or scripted events are occurring, the items will not be given to
you until these have ended.
