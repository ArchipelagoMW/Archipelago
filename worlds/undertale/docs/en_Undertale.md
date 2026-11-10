# Undertale

## Where is the options page?

The [player options page for this game](../player-options) contains all the options you need to configure and export a
config file.

## What is considered a location check in Undertale?

Location checks in Undertale are all the spots in the game where you can get an item. Exceptions are the Dog Residue, 
the Nicecream bought in Hotland, and anything you cannot get on your chosen route.

## When the player receives an item, what happens?

When the player receives an item in Undertale, it will go into their Infinite Box found within the Cell, which they now start with.

## What is the victory condition?

Victory is achieved when the player completes their chosen route. If they chose `all_routes` then they need to complete 
every major route in the game, those being `Pacifist`, `Neutral`, and `Genocide`.

## What is different from the vanilla game?

There are some major differences between vanilla and the randomizer. 

There are now doors to every major area in the underground located in the flower room (the first room of the game.)
These doors lead to Ruins, Snowdin, Waterfall, Hotland, and New Home from left to right. 
Each door needs their respective key from the pool to enter, with the exception of New Home, which is always unlocked. 

You start with the key of your choice, and the rest of the keys will be in the item pool to be found by players.

**Genocide** works a little differently in terms of the requirements. 

In order to win with the genocide route, you only need to beat Sans to win. 
If you choose to fight other major bosses, you will still need to grind out the area before fighting them like normal.

**Pacifist** remains mostly the same.

In the Pacifist run, you are not required to go to the Ruins to spare Toriel. The only necessary spares are Papyrus, 
Undyne, and Mettaton EX. Just as it is in the vanilla game, you cannot kill anyone. You are also required to complete 
the date/hangout with Papyrus, Undyne, and Alphys, in that order, before entering the True Lab. A Neutral run is no 
longer a requirement.

Additionally, custom items are required to hang out with Papyrus, Undyne, and to enter the True Lab. 
The respective items for each interaction are `Complete Skeleton`, `Fish`, and `DT Extractor`.
Alongside the `Undyne Letter EX` to date Alphys like vanilla.

There are also a few **universal** changes, which are always true.

The Riverperson will only take you to locations you have seen them at. For example, they will only take you to
Waterfall if you have seen them at Waterfall at least once.

If you press `W` while in the savepoint menu, you will be able to access a warp menu which can take you to any 
savepoint you have been to before on this save.

## Unique Local Commands

The following commands are only available when using the UndertaleClient to play with Archipelago.

- `/savepath` Redirect to proper save data folder. This is only necessary for Linux users which have to use before connecting.
- `/auto_patch` Patch the game automatically.
- `/patch` Patch the game. Only use this command if `/auto_patch` fails.
- `/online` Toggles seeing other Undertale players.
- `/deathlink` Toggles deathlink.
