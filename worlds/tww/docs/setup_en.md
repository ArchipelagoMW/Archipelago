# Setup Guide for The Wind Waker Archipelago

Welcome to The Wind Waker Archipelago! This guide will help you set up the randomizer and play your first multiworld.
Whether playing, generating, or hosting an Archipelago room with The Wind Waker, you must follow a few simple steps to
get started.

Unfortunately, Mac OS is not officially supported at this time.

## Requirements

You'll need the following components to be able to play/generate with The Wind Waker:
* Install [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases) v0.5.1 or higher.  
    **Make sure to install the Generator if you intend to generate multiworlds.**
* The latest version of the [TWW APWorld](https://github.com/tanjo3/tww_apworld/releases/latest).

If you're playing The Wind Waker, you'll also need:
* Install [Dolphin Emulator](https://dolphin-emu.org/download/).  
    **We recommend using the latest release.**
* The latest version of the [TWW AP Randomizer Build](https://github.com/tanjo3/wwrando/releases/latest).
* A The Wind Waker ISO (North American version), probably named "Legend of Zelda, The - The Wind Waker (USA).iso".

If you intend to play under Linux, you will need to consider the following information.
* Grab the `tar.gz` version of Archipelago, not the `AppImage`. The file name should be similar to the following on the
release page: `Archipelago_X.X.X_linux-x86_64.tar.gz`.
* For Dolphin, you can use the flatpak package
[available on Flathub](https://flathub.org/apps/org.DolphinEmu.dolphin-emu).

## Installation

All users should follow these steps:
1. Unzip the downloaded TWW APWorld zip file.
2. Double-click the `tww.apworld` file. It should automatically install the APWorld after a little while. You will get a
little dialog window telling you it has been installed successfully.
    * Alternatively, copy the `tww.apworld` to your Archipelago installation's `custom_worlds` folder (Windows default
    to: `%programdata%/Archipelago`).
3. Copy the contents of the `lib` folder in the downloaded TWW APWorld zip file to your Archipelago installation's `lib`
folder.

If you're playing The Wind Waker, you must also unzip the TWW AP Randomizer Build downloaded from the release page.

## Setting Up a YAML

All players playing The Wind Waker must provide the room host with a YAML file containing the settings for their world.
The TWW APWorld download includes a sample YAML file for The Wind Waker. The comments in that file explain each
setting's function.

Once you're happy with your settings, provide the room host with your YAML file and proceed to the next step.

## Generating a Multiworld

If you're generating a multiworld game that includes The Wind Waker, you'll need to do so locally as the online
generator does not yet support The Wind Waker. Follow these steps to generate a multiworld:
1. Gather all player's YAMLs. Place these YAMLs into the `Players` folder of your Archipelago installation. If the
folder does not exist, then it must be created manually. The files here should not be compressed.
2. Modify any local host settings for generation, as desired.
3. Run `ArchipelagoGenerate.exe` (without `.exe` on Linux) or click `Generate` in the launcher. The generation output
is placed in the `output` folder (usually named something like `AP_XXXXX.zip`).
    * Please note that if any player in the game you want to generate plays a game that needs a ROM file to generate,
    you will need the corresponding ROM files. A ROM file is not required for The Wind Waker at this stage.
4. Unzip the `AP_XXXXX.zip` file. It should include a `aptww` file for each player in the room playing The Wind Waker.
Each file will be named `AP_XXXXX_P#_<name>.aptww`, where `#` corresponds to that player's slot number and `<name>` is
their slot (player) name. Distribute each file to the appropriate player.
5. In the next section, use the archive file `AP_XXXXX.zip` to host a room or provide it to the room host.

## Hosting a Room

If you're generating the multiworld, follow the instructions in the previous section. Once you have the zip file
corresponding to your multiworld, follow
[these steps](https://archipelago.gg/tutorial/Archipelago/setup/en#hosting-an-archipelago-server) to host a room. Follow
the instructions for hosting on the website from a locally generated game or on a local machine.

## Connecting to a Room

You should have the `.aptww` file provided to you by the multiworld generator. You should also have the room's server
name and port number from the room's host.

Once you do, follow these steps to connect to the room:
1. Run the TWW AP Randomizer Build. If this is the first time you've opened the randomizer, you'll need to specify the
path to your The Wind Waker ISO and the output folder for the randomized ISO. These will be saved for the next time you
open the program.
2. Modify any cosmetic convenience tweaks and player customization options as desired.
[This repository](https://github.com/Sage-of-Mirrors/Custom-Wind-Waker-Player-Models) contains a collection of custom
player models for The Wind Waker. To set up custom player models, follow the installation instructions there.
3. For the APTWW file, browse and locate the path to the `.aptww` you received from the multiworld generator.
4. Click `Randomize` at the bottom. This randomizes the ISO and puts it in the output folder you specified. The file
will be named `TWW AP_XXXXX_P# (<name>).iso`, where `#` is the slot number and `<name>` is the slot (player) name.
Verify that the values are correct for the multiworld.
    * If nothing happens when you click `Randomize`, ensure you are using the correct build version for the `aptww` file
    you provided.
    * v2.5.x APWorlds should use the 2.3.0 build, v2.4.0 APWorlds should use the 2.2.0 build, v2.3.x APWorlds should use
    the 2.1.0 build, and older APWorlds should use 2.0.0.
5. Open Dolphin and use it to open the randomized ISO.
6. Start `ArchipelagoLauncher.exe` (without `.exe` on Linux) and choose `The Wind Waker Client`, which will open the
text client. If Dolphin is not already open, or you have yet to start a new file, you will be prompted to do so.
    * Launch `The Wind Waker Client`, not `WW Client`. The latter is the name of the client's previous (pre-v2.0.0)
    version and is no longer supported. You should delete the `ww.apworld` from your `lib/worlds` folder.
7. Connect to the room by entering the server name and port number at the top and pressing `Connect`. For rooms hosted
on the website, this will be `archipelago.gg:<port>`, where `<port>` is the port number. If a game is hosted from the
`ArchipelagoServer.exe` (without `.exe` on Linux), this will default to `38281` but may be changed in the `host.yaml`.
8. If you've opened a ROM corresponding to the multiworld to which you are connected, it should authenticate your slot
name automatically when you start a new save file.
    * If you encounter issues with authenticating, ensure that the randomized ROM is open in Dolphin and corresponds to
    the multiworld to which you are connecting.

## Troubleshooting

* Ensure that you are running version v0.5.1 or higher of Archipelago.
* If you do not see the client in the launcher, ensure the `tww.apworld` file is in the correct folder (the
`custom_worlds` folder of your Archipelago installation). Additionally, ensure you have copied the contents of the `lib`
folder in the downloaded TWW APWorld zip file to your Archipelago installation's `lib` folder.
* If the client is not working, double-check that you have the most recent release of the `tww.apworld` file.
Additionally, ensure no `ww.apworld`/`tww.apworld` files or `ww`/`tww` folders are in your `lib/worlds` folder. If those
exist, delete them. Finally, ensure that the content of the `lib` folder from the release download has been placed in
your Archipelago installation's `lib` folder.
* If you press Randomize in the build and nothing happens, ensure that you are using the correct version of the build
for the `aptww` file you are using.
    * v2.5.x APWorlds should use the 2.3.0 build, v2.4.0 APWorlds should use the 2.2.0 build, v2.3.x APWorlds should use
    the 2.1.0 build, and older APWorlds should use 2.0.0.
    * Remember that you should use the same APWorld version with which the `aptww` file was generated; ask the
    multiworld generator if you're unsure which version was used.
* Ensure that you do not have any Dolphin cheats or codes enabled. Some cheats or codes can unexpectedly interfere with
emulation and make troubleshooting errors difficult.
* If you get an error message, ensure that `Enable Emulated Memory Size Override` in Dolphin (under `Options` >
`Configuration` > `Advanced`) is **disabled**.
* If you run with a custom GC boot menu, you'll need to skip it by going to `Options` > `Configuration` > `GameCube`
and checking `Skip Main Menu`.
