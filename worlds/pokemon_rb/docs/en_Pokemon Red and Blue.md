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

* Bag item space increased to 128 slots (up from 20)
* PC item storage increased to 64 slots (up from 50)
* You can hold B to run (or bike extra fast!).
* You can hold select while talking to a trainer to re-battle them.
* You can return to route 2 from Diglett's Cave without the use of Cut.
* Mew can be encountered at the S.S. Anne dock truck. This can be randomized depending on your settings.
* The S.S. Anne will never depart.
* Seafoam Islands entrances are swapped. This means you need Strength to travel through from Cinnabar Island to Fuchsia
City
* After obtaining one of the fossil item checks in Mt Moon, the remaining item can be received from the Cinnabar Lab
fossil scientist. This may require reviving a number of fossils, depending on your settings.
* Obedience depends on the total number of badges you have obtained instead of depending on specific badges.
* Pokémon that evolve by trading can also evolve by reaching level 35.
* Evolution stones are reusable.
* Much of the dialogue throughout the game has been removed or shortened.
* If the Old Man is blocking your way through Viridian City, you do not have Oak's Parcel in your inventory, and you've
exhausted your money and Poké Balls, you can get a free Poké Ball from your mom.
* HM moves can be overwritten if you have the HM for it in your bag.
* The NPC on the left behind the Celadon Game Corner counter will sell 1500 coins at once instead of giving information
about the Prize Corner

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

A "received item" sound effect will play. Currently, there is no in-game message informing you of what the item is.
If you are in battle, have menus or text boxes opened, or scripted events are occurring, the items will not be given to
you until these have ended.
