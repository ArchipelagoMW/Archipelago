# Sonic Rush

## What is this game?

Sonic Rush is a 2.5D platformer for the Nintendo DS from 2005. It's the game that introduced Blaze the Cat and the
boost ability.

The game features two playable characters, Sonic the Hedgehog and Blaze the Cat, defeating Eggman and his "doppelganger"
while telling the same story from their own perspective. You have to make your way through a number of acts that involve 
running at high speed using the boost ability and doing tricks to raise your score. The game uses the dual screen of the
Nintendo DS in both acts and bosses to visualize the altitude of the player.

## Where is the options page?

The [player options page for this game](../player-options) contains all the options you need to configure
and export a config file.

## What does randomization do to this game?

Each zone is unlocked individually by an item and the chaos and sol emeralds have been shuffled into the item pool. 
Both characters and the overworld are completely accessible from the start, but you cannot enter any zone before having 
it unlocked.

Additionally to being unlocked individually, zones can progressively become accessible through the level select screen, 
which can be entered by unlocking another zone and having enough progressive level selects to include both zones. 

To give an example: Sonic's Zone 5 will be...
- accessible if you have `Huge Crisis`.
- accessible if you have 5 `Progressive Level Select (Sonic)` and at least one of `Leaf Storm`, `Water Palace`, 
  `Mirage Road`, or `Night Carnival` (zones 1-4).
- not accessible if you neither have `Huge Crisis` nor 5x `Progressive Level Select (Sonic)`.
- not accessible if you do not have `Leaf Storm`, `Water Palace`, `Mirage Road`, or `Night Carnival`, even if you 
  have 5 `Progressive Level Select (Sonic)`.

On a side note: If you have more than 5 `Progressive Level Select (Sonic)`, later zones (in this case `Altitude Limit` 
and `Dead Line`) can also be used to access the level select screen (and thereby zone 5).

## What is the goal of Sonic Rush in Archipelago?

You can choose between
- defeating all main game bosses at least once with either Sonic or Blaze,
- defeating all main game bosses with both Sonic and Blaze,
- clearing extra zone, which requires having all chaos and sol emeralds, and
- defeating all main game bosses with both characters AND clearing extra zone.

There is also the option to exclude F-Zone from any goal conditions.

## Which items can be in another player's world?

- Zone unlocks for each zone (8 total)
- Progressive level selects for both characters (14 total)
- Each chaos and sol emerald (14 total)
- Granting an extra life for and halving the extra lives of both characters (filler items)
- Tails and Cream unlocks and kidnapping (optional, 4 total)

## What is considered a location check?

- All acts and bosses of each zone of both characters, including Extra Zone (45 total)
- Optional: S rank for all acts and bosses of each zone (except F-Zone and Extra Zone) of both characters (42 total)
- Sonic's special stages (7 total)
