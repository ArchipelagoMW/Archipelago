# TUNIC

## Where is the options page?

The [player options page for this game](../player-options) contains all the options you need to configure and export a config file.

## I haven't played TUNIC before.

<u>**Play vanilla first.**</u> It is **_heavily discouraged_** to play this randomizer before playing the vanilla game.
It is recommended that you achieve both endings in the vanilla game before playing the randomizer.

## What does randomization do to this game?

In the TUNIC Randomizer, every item in the game is randomized. All chests, key item pickups, instruction manual pages, hero relics,
and other unique items are shuffled.<br>

Ability shuffling is an option available from the options page to shuffle certain abilities (prayer, holy cross, and the icebolt combo),
preventing them from being used until they are unlocked.<br>

Entrances can also be randomized, shuffling the connections between every door, teleporter, etc. in the game.

Enemy randomization and other options are also available and can be turned on in the client mod.

## What is the goal of TUNIC when randomized?
The standard goal is the same as the vanilla game. Find the three hexagon keys, then Take Your
Rightful Place or seek another path and Share Your Wisdom.

Alternatively, Hexagon Quest is a mode that shuffles a certain number of Gold Questagons into the item pool, with the goal 
being to find the required amount of them and then Share Your Wisdom.

## What items from TUNIC can appear in another player's world?
Every item has a chance to appear in another player's world.

## How many checks are in TUNIC?
There are 302 checks located across the world of TUNIC. The Fairy Seeking Spell can help you locate them.

## What do items from other worlds look like in TUNIC?
Items belonging to other TUNIC players will either appear as that item directly (if in a freestanding location) or in a
chest with the original chest texture for that item.

Items belonging to non-TUNIC players will either appear as a question-mark block (if in a freestanding location) or in a chest with
a question mark symbol on it. Additionally, non-TUNIC items are color-coded by classification, with green for filler, blue for useful, and gold for progression.

## Is there a tracker pack?
There is a [tracker pack](https://github.com/SapphireSapphic/TunicTracker/releases/latest). It is compatible with both Poptracker and Emotracker. Using Poptracker, it will automatically track checked locations and important items received. It can also automatically tab between maps as you traverse the world. This tracker was originally created by SapphireSapphic and ScoutJD, and has been extensively updated by Br00ty.

There is also a [standalone item tracker](https://github.com/radicoon/tunic-rando-tracker/releases/latest), which tracks what items you have received. It is great for adding an item overlay to streaming setups. This item tracker was created by Radicoon.

There is an [entrance tracker](https://scipiowright.gitlab.io/tunic-tracker/) for the entrance randomizer. This is a manual tracker that runs in your browser. This tracker was created by ScipioWright, and is a fork of the Pokémon Tracker by [Sergi "Sekii" Santana](https://gitlab.com/Sekii/pokemon-tracker).

You can also use the Universal Tracker (by Faris and qwint) to find a complete list of what checks are in logic with your current items. You can find it on the Archipelago Discord, in its post in the future-game-design channel. This tracker is an extension of the regular Archipelago Text Client.

## What should I know regarding logic?
In general:
- Nighttime is not considered in logic. Every check in the game is obtainable during the day.
- Bushes are not considered in logic. It is assumed that the player will find a way past them, whether it is with a sword, a bomb, fire, luring an enemy, etc. There is also an option in the in-game randomizer settings menu to clear some of the early bushes.
- The Cathedral is accessible during the day by using the Hero's Laurels to reach the Overworld fuse near the Swamp entrance.
- The Secret Legend chest at the Cathedral can be obtained during the day by opening the Holy Cross door from the outside.
- For the Ice Grappling, Ladder Storage, and Laurels Zips options, there is [this document](https://docs.google.com/document/d/1SFZBfsqZWH1_EAV9zyZobvrBcvCd3_54JP3iVnJ8rUg/edit?usp=sharing) that shows the individual applications of these tricks in logic.

For the Entrance Randomizer:
- Activating a fuse to turn on a yellow teleporter pad also activates its counterpart in the Far Shore.
- The West Garden fuse can be activated from below.
- You can pray at the tree at the exterior of the Library.
- The elevators in the Rooted Ziggurat only go down.
- The portal in the trophy room of the Old House is active from the start.
- The elevator in Cathedral is immediately usable without activating the fuse. Activating the fuse does nothing.

## Does this game have item and location groups?
Yes! To find what they are, open up the Archipelago Text Client while connected to a TUNIC session and type in `/item_groups` or `/location_groups`.

## Is Connection Plando supported?
Yes. The host needs to enable it in their `host.yaml`, and the player's yaml needs to contain a plando_connections block.
Example:
```
plando_connections:
  - entrance: Stick House Entrance
    exit: Stick House Exit
  - entrance: Special Shop Exit
    exit: Stairs to Top of the Mountain
```
Notes:
- The Entrance Randomizer option must be enabled for it to work.
- The `direction` field is not supported. Connections are always coupled.
- For a list of entrance names, check `er_data.py` in the TUNIC world folder or generate a game with the Entrance Randomizer option enabled and check the spoiler log.
- There is no limit to the number of Shops you can plando.

See the [Archipelago Plando Guide](../../../tutorial/Archipelago/plando/en) for more information on Plando and Connection Plando.

## Is there anything else I should know?
You can go to [The TUNIC Randomizer Website](https://rando.tunic.run/) for a list of randomizer features as well as some helpful tips.
You can use the Fairy Seeking Spell (ULU RDR) to locate the nearest unchecked location.
You can use the Entrance Seeking Spell (RDR ULU) to locate the nearest unused entrance.
