# Setup Guide for Okami HD for Archipelago

*Install guide still WIP*

## Warning
The mod and Apworld for this game are still in development. We don't recommend using them for syncs at the moment.

## Mod Installation

1. Download the WOLF Okami Loader Framework from https://github.com/Axertin/wolf/releases. Select the wolf-runtime.zip
2. Unzip in your game folder.
3. Create a "mods" folder in your game folder.
4. Download the APclient mod from https://github.com/Axertin/okami-apclient/releases
5. Unzip in your "mods" folder (you should have an apclient folder inside your mods folder)
6. Start the game with wolf-loader.exe.

## Setting up the apworld
1. Download and install Archipelago
2. Download the Okami HD .apworld file from https://github.com/Ragmoa/Archipelago/releases
3. Double Click to install the apworld or place it in your custom_worlds Archipelago folder.
4. Restart Archipelago if it was open during this process.

## Setting up an Archipelago game
1. For each game you want randomized, you'll need to provide Archipelago with a .yaml file containing the randomization settings for said game.
2. 
   1. You can get a template by opening archipelago and using the option builder.
   2. Alternatively, you can generate all templates with the Generate templates option in archipelago, then manually edit the file.(They'll appear in your archipelago folder/Players/templates) 
3. Place your .yaml files in the Players folder of your archipelago install
4. Select the Generate option in archipelago to randomize games.
5. If everything goes well, the command prompt should disappear after generation, it'll stay and display an error if it doesn't.
6. You should get a .zip in your archipelago/output folder. You'll need to start an Archipelago server with it:
   1. You can start one yourself by using the Host option in archipelago. This will run a local server on your computer.
   2. (Recommended if you want to play with other players) You can host your game on the official archipelago website: head to https://archipelago.gg/start-playing, then use the "host a pre-generated game" link.


## Connecting to the game
1. When opening the game, you should see a window to connect to the archipelago server.
2. Make sure you connect BEFORE starting or loading a save, or you game might not get properly randomized.

