# The Legend of Zelda: Phantom Hourglass AP Setup Guide

## Required Software

* [Archipelago 0.6.1+](https://archipelago.gg/tutorial/Archipelago/setup/en)
* [Bizhawk 2.10+](https://github.com/TASEmulators/BizHawk)
* Legally acquired Phantom Hourglass EU rom (US support coming soon). Apparently it only works in English
* [Latest tloz_ph.apworld](https://github.com/carrotinator/Archipelago/releases)

## Recommended Software

* [Universal Tracker](https://github.com/FarisTheAncient/Archipelago/releases)

## Setup

1. Find your Archipelago directory, and put tloz_ph.apworld in the 'custom_worlds' folder
2. Create a yaml settings file, and put it in the Archipelago directories 'players' folder. You can generate a template yaml with the archipelago launcher.
3. Generate your game
4. Host the game, either locally or via the archipelago web hosting service
5. Open the 'generic bizhawk client' in Archipelago, and connect to the server
6. Launch the vanilla game in bizhawk, and open the lua console. Add the 'connector_bizhawk_generic.lua' script that can be found in 'Archipelago\data\lua'. 
7. You are now ready to play! Start a new savefile and go! You can check that everything worked by checking if the bridge has been repaired.
8. The sword and items menu don't work until you've save and quit. Likewise, the sword chest will give you a fake usable sword until you save and quit to remove it.

