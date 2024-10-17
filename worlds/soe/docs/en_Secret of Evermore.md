# Secret of Evermore

## Where is the options page?

The [player options page for this game](../player-options) contains all the options you need to configure and export a
config file.

## What does randomization do to this game?

Items which would normally be acquired throughout the game have been moved around! Progression logic remains, so the
game is always able to be completed. However, because of the item shuffle, the player may need to access certain areas
before they would in the vanilla game. For example, the Windwalker (flying machine) is accessible as soon as any weapon
is obtained.

Additional help can be found in the [Evermizer guide](https://github.com/black-sliver/evermizer/blob/master/guide.md).

## What items and locations get shuffled?

All gourds/chests/pots, boss drops and alchemists are shuffled. Alchemy ingredients, sniff spot items, call bead spells
and the dog can be randomized using yaml options.

## Which items can be in another player's world?

Any of the items which can be shuffled may also be placed in another player's world. Specific items can be limited to
your own world using plando.

## What does another world's item look like in Secret of Evermore?

Secret of Evermore will display "Sent an Item". Check the client output if you want to know which.

## What happens when the player receives an item?

When the player receives an item, a popup will appear to show which item was received. Items won't be received while a
script is active such as when visiting Nobilia Market or during most Boss Fights. Once all scripts have ended, items
will be received.
