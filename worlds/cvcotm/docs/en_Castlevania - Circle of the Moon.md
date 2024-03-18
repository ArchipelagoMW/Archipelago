# Castlevania: Circle of the Moon

## Where is the settings page?

The [player settings page for this game](../player-settings) contains all the options you need to configure and export a
config file.

## What does randomization do to this game?

All items that you would normally find on pedestals throughout the game have had their locations changed. In addition to
magic items and stat max ups, the DSS Cards have been added to the item pool as well; you will now receive these as randomized
items rather than by farming them via enemy drops.

## What is the goal of Castlevania: Circle of the Moon when randomized?

Make it to the Ceremonial Room and kill Dracula to beat the game. The door to the Ceremonial Room can be set to require anywhere
between 0-9 Last Keys to open it. If `require_all_bosses` is enabled, 8 keys will be required, and they will be guaranteed to be
placed behind all 8 bosses (that are not Dracula).

## What items and locations get shuffled?

Stat max ups, magic items, and DSS Cards are all randomized into the item pool, and the check locations are the pedestals
that you would normally find the first two types of items on.

The sole exception currently is the Shining Armor at the end of the Battle Arena and its associated pedestal. This spot will
always be vanilla regardless of the settings.

## Which items can be in another player's world?

Any of the items which can be shuffled may also be placed into another player's world.

## What does another world's item look like in Castlevania: Circle of the Moon?

All items from other worlds will show up as the unused map magic item. In-game, it does nothing when picked up besides set
the flag for the location so that the client can detect the location check.

## When the player receives an item, what happens?

The textbox(s) for the item will appear as if the player picked up the item in-game normally, and they will get it.

## What are the item name groups?
The groups you can use for Castlevania: Circle of the Moon are `Action Card` and `Attribute Card`, both of which will
hint for a random card of their type.

## What are the location name groups?
In Castlevania: Circle of the Moon, every location is part of a location group under that location's area name.
So if you want to exclude all of, say, Underground Waterway, you can do so by just excluding "Underground Waterway" as a whole.
