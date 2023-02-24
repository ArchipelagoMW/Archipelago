# Adventure

## Where is the settings page?
The [player settings page for Adventure](../player-settings) contains all the options you need to configure and export a config file.

## What does randomization do to this game?
Adventure items may be distributed into additional locations not possible in the vanilla Adventure randomizer.  All
Adventure items are added to the multiworld item pool.  Depending on the settings, dragon locations may be randomized,
slaying dragons may award items, difficulty switches may require items to unlock, and limited use 'freeincarnates'
can allow reincarnation without resurrecting dragons.  Dragon speeds may also be randomized, and items may exist
to reduce their speeds.

## What is the goal of Adventure when randomized?
Same as vanilla; Find the Enchanted Chalice and return it to the Yellow Castle

## Which items can be in another player's world?
All three keys, the chalice, the sword, the magnet, and the bridge can be found in another player's world.  Depending on
settings, dragon slowdowns, difficulty switch unlocks, and freeincarnates may also be found.

## What is considered a location check in Adventure?
Most areas in Adventure have one or more locations which can contain an Adventure item or an Archipelago item.
A few rooms have two potential locaions.  If the location contains a 'nothing' Adventure item, it will send a check when
that is seen.  If it contains an item from another Adventure or other game, it will show a rough approximation of the
Archipelago logo that can be touched for a check.  Touching a local Adventure item also 'checks' it, allowing it to be
retrieved after a select-reset or hard reset.

## Why isn't my item where the spoiler says it should be?
If something isn't where the spoiler says, most likely the bat carried it somewhere else.  The bat's ability to shuffle
items around makes it somewhat unique in Archipelago.  Touching the item, wherever it is, will award the location check
for wherever the item was originally placed.

## Which notable items are not randomized?
The bat, dot, and map are not yet randomized

## What does another world's item look like in Adventure?
It looks vaguely like a flashing Archipelago logo. 

## When the player receives an item, what happens?
A message is shown in the client log.  While empty handed, the player can press the fire button to retrieve items in the
order they were received.  Once an item is retrieved this way, it cannot be retrieved again until pressing select to 
return to the 'GO' screen or doing a hard reset, either one of which will reset all items to their original positions.

## My yellow key is stuck in a wall!  Am I softlocked?
Maybe!  That's all part of Adventure.  If you have access to the magnet, bridge, or bat, you might be able to retrieve
it.  In general, since the bat always starts outside of castles, you should always be able to find it unless you lock
it in a castle yourself.  This mod's inventory system allows you to quickly recover all the items
you've collected after a hard reset or select-reset (except for the dot), so usually it's not as bad as in vanilla.
