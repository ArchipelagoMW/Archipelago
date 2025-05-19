# Pokémon FireRed and LeafGreen Setup Guide

## Required Software

* [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases)
* [Pokémon FireRed and LeafGreen apworld](https://github.com/vyneras/Archipelago/releases/latest)
* [Bizhawk](https://tasvideos.org/BizHawk/ReleaseHistory)
* An English FireRed or LeafGreen ROM
  * FireRed 1.0 `sha1: 41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc`
  * FireRed 1.1 `sha1: dd5945db9b930750cb39d00c84da8571feebf417`
  * LeafGreen 1.0 `sha1: 574fa542ffebb14be69902d1d36f1ec0a4afd71e`
  * LeafGreen 1.1 `sha1: 7862c67bdecbe21d1d69ce082ce34327e1c6ed5e`

 Place the `pokemon_frlg.apworld` file in your Archipelago installation's `custom_worlds` folder (Default location for Windows: `%programdata%/Archipelago`).

It is recommended you follow the setup guide for Bizhawk in the [Pokémon Emerald Setup Guide](https://archipelago.gg/tutorial/Pokemon%20Emerald/setup/en#configuring-bizhawk).

## Optional Software

- [Pokémon FireRed/LeafGreen Tracker](https://github.com/vyneras/pokemon-frlg-tracker/releases/latest)

## Generating and Patching

1. Open `ArchipelagoLauncher.exe` and select "Generate Template Options" to create a default YAML.
2. Modify the default YAML and place it into the `Players` folder
3. Launch `ArchipelagoGenerate.exe`. This will generate an output file for you. Your patch file will have one of the following file extensions:
   * `.apfirered`
   * `.apleafgreen`
4. Open `ArchipelagoLauncher.exe`
5. Select "Open Patch" on the left side and select your patch file.
6. If this is your first time patching, you will be prompted to locate your vanilla ROM.
7. A patched `.gba` file will be created in the same place as the patch file.
8. On your first time opening a patch with BizHawk Client, you will also be asked to locate `EmuHawk.exe` in your
BizHawk install.

If you're playing a single-player seed and you don't care about autotracking or hints, you can stop here, close the
client, and load the patched ROM in any emulator. However, for multiworlds and other Archipelago features, continue
below using BizHawk as your emulator.

## Connecting to a Server

By default, opening a patch file will do steps 1-5 below for you automatically. Even so, keep them in your memory just
in case you have to close and reopen a window mid-game for some reason.

1. Pokémon FireRed and LeafGreen uses Archipelago's BizHawk Client. If the client isn't still open from when you patched your game,
you can re-open it from the launcher.
2. Ensure EmuHawk is running the patched ROM.
3. In EmuHawk, go to `Tools > Lua Console`. This window must stay open while playing.
4. In the Lua Console window, go to `Script > Open Script…`.
5. Navigate to your Archipelago install folder and open `data/lua/connector_bizhawk_generic.lua`.
6. The emulator and client will eventually connect to each other. The BizHawk Client window should indicate that it
connected and recognized Pokémon FireRed and LeafGreen.
7. To connect the client to the server, enter your room's address and port (e.g. `archipelago.gg:38281`) into the
top text field of the client and click Connect.

You should now be able to receive and send items. You'll need to do these steps every time you want to reconnect. It is
perfectly safe to make progress offline; everything will re-sync when you reconnect.

## Auto-Tracking

Pokémon FireRed and LeafGreen has a fully functional map tracker that supports auto-tracking.

1. Download [Pokémon FireRed/LeafGreen Tracker](https://github.com/vyneras/pokemon-frlg-tracker/releases/latest) and
[PopTracker](https://github.com/black-sliver/PopTracker/releases).
2. Put the tracker pack into packs/ in your PopTracker install.
3. Open PopTracker, and load the Pokémon FireRed/LeafGreen pack.
4. For autotracking, click on the "AP" symbol at the top.
5. Enter the Archipelago server address (the one you connected your client to), slot name, and password.