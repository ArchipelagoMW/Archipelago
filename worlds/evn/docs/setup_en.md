# EVNova Randomizer Setup Guide

## Required Software

- [EV Nova CE edition with AP mod](https://github.com/Dorrulf/EV-Nova-CE-APClient/releases)
- [EV New](https://github.com/Dorrulf/EV-Nova-CE-APClient/releases)

## Optional Software

- [ArchipelagoTextClient](https://github.com/ArchipelagoMW/Archipelago/releases)

## First Time Setup

1. If you have an existing EV Nova folder, make a copy of it and rename it.
2. Extract the downloaded EV Nova CE AP edition into the new EV Nova folder, or into its own folder.
3. Extract EV New into this folder as well. It should be in the same folder as the EV Nova exe.
4. Install the font files (Geneva and Charcoal) by double-clicking them and selecting "Install".
5. Open the ddraw.ini file to change desired system settings. There are setting available here that are not available in game.

## Joining an Archipelago

Before joining, use the options page to choose your settings for the run and make a yaml (or generate a single player room).

1. Get the link for the room and visit it.
2. Next to your player name, there will be a download link for a patch file. Download it.
3. Drag the downloaded zip onto the "DROP_AP_PATCH_HERE" file to automatically sort the files for you.
4. Open ap_config.ini and update the details based on those on the room page.
5. Run the game!

EV Nova will automatically connect for you. Sometimes, this may take a moment, so just keep playing and it'll catch up.
Don't worry, no checks will be lost, it'll go through all of them once it connects.

### Quick note on Pilot options

When creating a pilot, you can choose "Trader" for a standard start (shuttle, 25k)
or you can pick "Head Start" to start with a Mod Starbridge and 500k for a slightly quicker AP.

## Archipelago Text Client

We recommend having Archipelago's Text Client open on the side to keep track of what items you receive and send.
EV Nova has in-game messages (bottom left),
but they disappear quickly and there's no reasonable way to check your message history in-game.

## ap_config.ini

- conn_addr: Put the address and port that's listed after '/connect' on the room. E.g. archipelago.gg:12345
- game_name: Leave this alone, it doesn't need to change.
- username: The player name you put in the options page / yaml.
- password: If the room has a password, you can put it here. Usually, this will be blank.

## Manual setup / DROP_AP_PATCH_HERE didn't work

The batch file only does the following for you to make things simpler. Feel free to open it and verify.
Optionally, you can run the following steps:

1. Move the zip file to the EV Nova AP folder and unzip it.
2. In the folder, unzip the new zip file as well. (It should look like AP-##############-P#).
3. Move the contents of the AP folder (aplocids.txt, archipelago.json, zzzapdata.txt) to the root folder (where EV Nova.exe is).
4. Open a command prompt window here, and run the following command:
.\EVNEW.exe -torez "zzzapdata.txt" "zzzapdata.rez"
5. Move the newly created zzzapdata.rez file to the plugins folder.
6. Run the game!

The next time you manually set up for a new archipelago run, you'll need to remove these files.
The batch file does this automatically.

## Plugins

There is a plugin (apicons) that comes with EV Nova CE AP. Please leave it there. It provides the AP icon for the outfitter checks.

Each AP generation will result in a plugin (zzzapdata) that is specifically for that run. This is largely how the game data is shuffled and is necessary for things to work properly!

### But can I use other plugins?

Generally, no. Because this required reimplementing so much game data in the plugin, things that touch
ships, outfits, missions, crons, chars, etc. will largely be incompatible.

You may be able to use some graphic overhauls, but they have not been tested yet. *Use at your own risk.*

### Will any TCs ever be implemented?

Maybe. Game data for that specific TC would have to be implemented as well. Unfortunately, even
the base game was significantly less straight forward than expected due to many hidden and
incompletable "missions" that are used to facilitate other aspects of gameplay.

If there are enough votes for a favorite, it may happen. Let us know in the discord community (link on game page).