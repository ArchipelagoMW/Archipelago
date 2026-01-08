# ANIMAL WELL

## Where is the options page?
Generate a template yaml by placing the apworld in your `custom_worlds` folder, then opening the Archipelago Launcher and clicking on Generate Template Options.
When the game is on the website,
the [player options page for this game](../player-options) contains all the options you need to configure and export a config file.

## I haven't played ANIMAL WELL before.
It is recommended to play the vanilla game first. The randomizer will spoil mechanics, items, and the locations of secrets.
We recommend you find all of the eggs, all of the equipment items, and as many bunnies as you can before playing this randomizer.

## What does randomization do to this game?
All items you normally find in chests (eggs, toys, keys, matches) are shuffled into the item pool.
Locations that contain random items from the item pool include opening chests, as well as optionally finding bunnies, lighting candles, and eating fruits.

## What is the goal of ANIMAL WELL when randomized?
The standard goal is the same as the vanilla game. Find the 4 flames and set off the fireworks at the end.
There will be alternate goals later in development.

## How many checks are in ANIMAL WELL?
In the game's base settings, there are around 100 checks in ANIMAL WELL. This number can currently get as high as 240 with all check-adding options enabled.
When we have finalized these options, this doc will be updated to reflect the actual numbers.

## What do items from other worlds look like in ANIMAL WELL?
They just look like the standard chests.

## Is there a tracker?
A map tracker is built into the client, and is visible on your in-game map.
Universal Tracker is also an option, and will not run into any of its common issues.

## What should I know regarding logic?
Locations that may softlock you (such as the B. Wand chest) are included in logic. To escape these softlocks, you can either quit to menu and continue (the chest will appear closed, but you will have already sent the check, so it's fine), or you can use the Warp to Hub button in the pause menu.

## Does this game have item and location groups?
Yes! To find what they are, type `/item_groups` or `/location_groups` into the ANIMAL WELL Client, or the Archipelago Text Client while connected to an ANIMAL WELL session.

## What are the current known issues?
The client rarely fails for no discernable reason when opening a chest. We do not know why yet. If it fails, please let us know in the discord and send us your log file (in your `Archipelago/logs` folder). We may ask you to troubleshoot a few things as well.
Some yaml options are missing. This is intentional. They don't work yet.
When reloading a game already in progress, if you've been sent the Mock Disc, there is a chance that the mock disc will appear in your inventory instead of in a disc shrine and the Ghost will begin to persue you. A fix for this is still in brainstorming.
If you use the Remote by the bunny mural before you have any other mobility options, the blast will prevent you from crossing over to the other side. You will need to reset your save in order to get over there again. Consult the Discord channel to ask how to do this.

## Who contributed to this?
The ANIMAL WELL randomizer is brought to you by many contributors over the course of many months.
ScipioWright and RoobyRoo wrote a majority of the logic and apworld.
Franklesby wrote the client. Dicene and Dregu contributed major features to the client.
The fruitsanity option was developed and implemented almost entirely by Froggle.
Various others helped with some bug fixes and minor additions.
Special thanks to SporyTike for making the poptracker, GameWyrm for their help early on, and Kevin for convincing Scipio to get the game.
