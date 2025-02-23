# Setup Guide for The Wind Waker Archipelago

Welcome to The Wind Waker Archipelago! This guide will help you set up the randomizer and play your first multiworld.
If you're playing The Wind Waker, you must follow a few simple steps to get started.

## Requirements

You'll need the following components to be able to play with The Wind Waker:
* Install [Dolphin Emulator](https://dolphin-emu.org/download/). **We recommend using the latest release.**
    * For Linux users, you can use the flatpak package
    [available on Flathub](https://flathub.org/apps/org.DolphinEmu.dolphin-emu).
* The 2.5.0 version of the [TWW AP Randomizer Build](https://github.com/tanjo3/wwrando/releases/tag/ap_2.5.0).
* A The Wind Waker ISO (North American version), probably named "Legend of Zelda, The - The Wind Waker (USA).iso".

Optionally, you can also download:
* [Wind Waker Tracker](https://github.com/Mysteryem/ww-poptracker/releases/latest)
  * Requires [PopTracker](https://github.com/black-sliver/PopTracker/releases)
* [Custom Wind Waker Player Models](https://github.com/Sage-of-Mirrors/Custom-Wind-Waker-Player-Models)

## Setting Up a YAML

All players playing The Wind Waker must provide the room host with a YAML file containing the settings for their world.
Visit the [The Wind Waker options page](/games/The%20Wind%20Waker/player-options) to generate a YAML with your desired
options. Only locations categorized under the options enabled under "Progression Locations" will be randomized in your
world. Once you're happy with your settings, provide the room host with your YAML file and proceed to the next step.

## Connecting to a Room

The multiworld host will provide you a link to download your `aptww` file or a zip file containing everyone's files. The
`aptww` file should be named `P#_<name>_XXXXX.aptww`, where `#` is your player ID, `<name>` is your player name, and
`XXXXX` is the room ID. The host should also provide you with the room's server name and port number.

Once you do, follow these steps to connect to the room:
1. Run the TWW AP Randomizer Build. If this is the first time you've opened the randomizer, you'll need to specify the
path to your The Wind Waker ISO and the output folder for the randomized ISO. These will be saved for the next time you
open the program.
2. Modify any cosmetic convenience tweaks and player customization options as desired.
3. For the APTWW file, browse and locate the path to your `aptww` file.
4. Click `Randomize` at the bottom-right. This randomizes the ISO and puts it in the output folder you specified. The
file will be named `TWW AP_YYYYY_P# (<name>).iso`, where `YYYYY` is the seed name, `#` is your player ID, and `<name>`
is your player (slot) name. Verify that the values are correct for the multiworld.
5. Open Dolphin and use it to open the randomized ISO.
6. Start `ArchipelagoLauncher.exe` (without `.exe` on Linux) and choose `The Wind Waker Client`, which will open the
text client. If Dolphin is not already open, or you have yet to start a new file, you will be prompted to do so.
    * Once you've opened the ISO in Dolphin, the client should say "Dolphin connected successfully.".
7. Connect to the room by entering the server name and port number at the top and pressing `Connect`. For rooms hosted
on the website, this will be `archipelago.gg:<port>`, where `<port>` is the port number. If a game is hosted from the
`ArchipelagoServer.exe` (without `.exe` on Linux), the port number will default to `38281` but may be changed in the
`host.yaml`.
8. If you've opened a ROM corresponding to the multiworld to which you are connected, it should authenticate your slot
name automatically when you start a new save file.

## Troubleshooting

* Ensure you are running the same version of Archipelago on which the multiworld was generated.
* Ensure `tww.apworld` is not in your Archipelago installation's `custom_worlds` folder.
* Ensure you are using the correct randomizer build for the version of Archipelago you are using. The build should
provide an error message directing you to the correct version. You can also look at the release notes of TWW AP builds
[here](https://github.com/tanjo3/wwrando/releases) to see which versions of Archipelago each build is compatible with.
* If you encounter issues with authenticating, ensure that the randomized ROM is open in Dolphin and corresponds to the
multiworld to which you are connecting.
* Ensure that you do not have any Dolphin cheats or codes enabled. Some cheats or codes can unexpectedly interfere with
emulation and make troubleshooting errors difficult.
* If you get an error message, ensure that `Enable Emulated Memory Size Override` in Dolphin (under `Options` >
`Configuration` > `Advanced`) is **disabled**.
* If you run with a custom GC boot menu, you'll need to skip it by going to `Options` > `Configuration` > `GameCube`
and checking `Skip Main Menu`.
