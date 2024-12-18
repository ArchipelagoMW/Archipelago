# Pokémon Red and Blue

## Where is the options page?

The [player options page for this game](../player-options) contains all the options you need to configure and export a
config file.

## What does randomization do to this game?

Items which the player would normally acquire throughout the game have been moved around. Logic remains, so the game is
always able to be completed, but because of the item shuffle the player may need to access certain areas before they
would in the vanilla game.

A great many things besides item placement can be randomized, such as the location of Pokémon, their stats, types, etc.,
depending on your yaml options.

Many baseline changes are made to the game, including:

* Bag item space increased to 128 slots (up from 20).
* PC item storage increased to 64 slots (up from 50).
* You can hold B to run (or bike extra fast!).
* You can hold select while talking to a trainer to re-battle them.
* You can select "Pallet Warp" below the "Continue" option to warp to Pallet Town as you load your save.
* Mew can be encountered at the S.S. Anne dock truck. This can be randomized depending on your options.
* The S.S. Anne will never depart.
* Seafoam Islands entrances are swapped. This means you need Strength to travel through from Cinnabar Island to Fuchsia
City. You also cannot Surf onto the water from the end of Seafoam Islands going backwards if you have not yet dropped
the boulders.
* After obtaining one of the fossil item checks in Mt Moon, the remaining item can be received from the Cinnabar Lab
fossil scientist. This may require reviving a number of fossils, depending on your options.
* Obedience depends on the total number of badges you have obtained instead of depending on specific badges.
* Pokémon that evolve by trading can also evolve by reaching level 35.
* Evolution stones are reusable key items.
* Much of the dialogue throughout the game has been removed or shortened.
* The Pokédex shows which HMs can be learned by any Pokémon registered as seen.
* HM moves can be overwritten if you have the HM for it in your bag.
* The NPC on the left behind the Celadon Game Corner counter will sell 1500 coins at once instead of giving information
about the Prize Corner.
* A woman in Oak's Lab can send you back in time to replay the first rival battle, in case you have no other reachable
and repeatable source of money.
* You can disable and re-enable experience gains by talking to an aide in Oak's Lab.
* You can reset static encounters (Poké Flute encounter, legendaries, and the trap Poké Ball battles in Power Plant)
for any Pokémon you have defeated but not caught, by talking to an aide in Oak's Lab.
* Dungeons normally hidden on the Town Map are now present, and the "Sea Cottage" has been removed. This is to allow
Simple Door Shuffle to update the locations of all of the dungeons on the Town Map.

## What items and locations get shuffled?

All items that go into your bags given by NPCs or found on the ground, as well as gym badges.
Various options add more items / location checks to the pool, including:
* Randomize Hidden Items.
* Stonesanity: Replace 4 of the 5 Moon Stones in the item pool with the other 4 stones, and remove them from the
Celadon Department Store shop. Will shuffle the hidden item locations that contain Moon Stones in the original game
regardless of the Randomize Hidden Items option.
* Prizesanity: Shuffle the three item prizes from the Celadon Prize Corner.
* Tea: Adds a Tea item to the item pool which is required to pass the Saffron Gate guards instead of vending machine
drinks. Adds a location check to the woman in Celadon Mansion 1F, where the Tea item is found in FireRed and LeafGreen.
* Extra Key Items: Adds key items that will be required to access the Power Plant, Pokémon Mansion, Rocket Hideout,
and Safari Zone. Adds 4 extra item locations to Rock Tunnel B1F
* Split Card Key: Splits the Card Key into 10 different Card Keys, one for each floor of Silph Co that has locked doors.
Adds 9 location checks to friendly NPCs in Silph Co. You can also choose Progressive Card Keys to always obtain the
keys in order from Card Key 2F to Card Key 11F.
* Trainersanity: Adds location checks to trainers. You may choose between 0 and 317 trainersanity checks. Trainers
will be randomly selected to be given checks. Does not include scripted trainers, most of which disappear
after battling them, but also includes Gym Leaders. You must talk to the trainer after defeating them to receive
your prize. Adds random filler items to the item pool.
* Dexsanity: Location checks occur when registering Pokémon as owned in the Pokédex. You can choose between 0 and 151
Pokémon to have checks added to, chosen randomly. You can identify which Pokémon have location checks by an empty
Poké Ball icon shown in battle or in the Pokédex menu.

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

## Unique Local Commands

You can use `/bank` commands to deposit and withdraw money from the server's EnergyLink storage. This can be accessed by
any players playing games that use the EnergyLink feature.

- `/bank` - check the amount of money available on the server.
- `/bank withdraw #` - withdraw money from the server.
- `/bank deposit #` - deposit money into the server. 25% of the amount will be lost to taxation.