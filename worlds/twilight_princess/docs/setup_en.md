# Setup Guide for Twilight Princess Archipelago

Welcome to Twilight Princess Archipelago! This guide will help you set up the randomizer and play your first multiworld.
Whether playing, generating, or hosting an Archipelago room with Twilight Princess, you must follow a few simple steps to
get started.

Unfortunately, Mac OS is not officially supported at this time.

## Requirements

You'll need the following components to be able to play/generate with Twilight Princess:

- Install [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases) v0.6.1 or higher.\
   **Make sure to install the Generator if you intend to generate multiworlds.**
- The latest version of the [Twilight Princess APWorld](https://github.com/WritingHusky/Twilight_Princess_apworld/releases/latest).

If you're playing Twilight Princess, you'll also need:

- Install [Dolphin Emulator](https://dolphin-emu.org/download/).\
   **We recommend using the latest release.**
- A Twilight Princess ISO (North American version), probably named "Legend of Zelda, The - Twilight Princess (USA).iso".

If you intend to play under Linux, you will need to consider the following information.

- Grab the `tar.gz` version of Archipelago, not the `AppImage`. The file name should be similar to the following on the
  release page: `Archipelago_X.X.X_linux-x86_64.tar.gz`.
- For Dolphin, you can use the flatpak package
  [available on Flathub](https://flathub.org/apps/org.DolphinEmu.dolphin-emu).

## Installation

All users should follow these steps:

1. Unzip the downloaded Twilight Princess APWorld zip file.
2. Double-click the `Twilight Princess.apworld` file. It should automatically install the APWorld after a little while. You will get a
   little dialog window telling you it has been installed successfully. \* Alternatively, copy the `Twilight Princess.apworld` to your Archipelago installation's `custom_worlds` folder (Windows default
   to: `%programdata%/Archipelago`).

If you're playing Twilight Princess, you must also download the REL loader from https://tprandomizer.com/ and the [custom seed file](https://generator.tprandomizer.com/s/aptest) and place both in the save data of dolphin, alongside the RandomizerAP.US.gci file from the zip folder

## Setting Up a YAML

All players playing Twilight Princess must provide the room host with a YAML file containing the settings for their world.
The TP APWorld download includes a sample YAML file for Twilight Princess. The comments in that file explain each
setting's function.

Once you're happy with your settings, provide the room host with your YAML file and proceed to the next step.

Note: Please note the settings labled NON-DEFAULT CHOICE NOT REPRESENTED IN GAME, as these settings will alter logic however they will not be changed from default when playing the game.

## Generating a Multiworld

If you're generating a multiworld game that includes Twilight Princess, you'll need to do so locally as the online
generator does not yet support Twilight Princess. Follow these steps to generate a multiworld:

1. Gather all player's YAMLs. Place these YAMLs into the `Players` folder of your Archipelago installation. If the
   folder does not exist, then it must be created manually. The files here should not be compressed.
2. Modify any local host settings for generation, as desired.
3. Run `ArchipelagoGenerate.exe` (without `.exe` on Linux) or click `Generate` in the launcher. The generation output
   is placed in the `output` folder (usually named something like `AP_XXXXX.zip`). \* Please note that if any player in the game you want to generate plays a game that needs a ROM file to generate,
   you will need the corresponding ROM files. A ROM file is not required for Twilight Princess at this stage.
4. Unzip the `AP_XXXXX.zip` file. It should include a `.aptp` file for each player in the room playing Twilight Princess.
   Each file will be named `AP_XXXXX_P#_<name>.aptp`, where `#` corresponds to that player's slot number and `<name>` is
   their slot (player) name. The `.aptp` file currently contains a spoiler log and other debug information it can be safely ignored.
5. In the next section, use the archive file `AP_XXXXX.zip` to host a room or provide it to the room host.

## Hosting a Room

If you're generating the multiworld, follow the instructions in the previous section. Once you have the zip file
corresponding to your multiworld, follow
[these steps](https://archipelago.gg/tutorial/Archipelago/setup/en#hosting-an-archipelago-server) to host a room. Follow
the instructions for hosting on the website from a locally generated game or on a local machine.

## Connecting to a Room

You may have the `.aptp` file provided to you by the multiworld generator (you can ignore it.) You should also have the room's server
name and port number from the room's host.

Once you do, follow these steps to connect to the room:

1. Visit https://generator.tprandomizer.com/s/aptest to download the seed file needed to run the randomizer, Feel free to randomize cosmetics and audio as you would like
2. If you haven't gotten the REL loader, now is a good time to do that from the randomizer website.
3. From the zip folder downloaded add the RandomizerAP.US.gci to the dolphin save data. (If you are using a non-US version you will have to use the Randomizer file from tprandomizer website and killing gannon will not auto-complete your world)

**Your save data folder should have aptest.gci, RELoader, and RandomizerAP.US.gci** (Non AP for Non US versions)

4. Open Dolphin and use it to open Twilight Princess. (Ensure `Enable Emulated Memory Size Override` is disabled. See troubleshooting for more details)
5. Start the REL loader save file and select APTest as the seed you want to use.
   (If US Randomizer) The console should say "Archipelego Randomizer" at the top
6. Start a new save file and leave links name as default for now, we will change it later.
7. Start `ArchipelagoLauncher.exe` (without `.exe` on Linux) and choose `Twilight Princess Client`, which will open the
   text client. It should automatically connect to Dolphin.
8. Now with dolphin connected run the `/name` command with the player name you put in the YAML file (max 16 characters.) eg: /name Player1
9. Connect to the room by entering the server name and port number at the top and pressing `Connect`. For rooms hosted
   on the website, this will be `archipelago.gg:<port>`, where `<port>` is the port number. If a game is hosted from the
   `ArchipelagoServer.exe` (without `.exe` on Linux), this will default to `38281` but may be changed in the `host.yaml`.

## Troubleshooting

- Ensure that you are running version v0.6.1 or higher of Archipelago, and the latest version of the world.
- If you do not see the client in the launcher, ensure the `Twilight Princess.apworld` file is in the correct folder (the
  `custom_worlds` folder of your Archipelago installation).
- If the client says that seed version and client version do not match, it is recomended regenerate the seed with the current version.
  Differences in version can cause bugs which may make it unplayable.
- If the client throws an error along the lines of "could not read memory at < some-number >", dolphin has been disconnected.
  It should automaticly reconnect, so ensure that dolphin is open and running
- Ensure that you do not have any Dolphin cheats or codes enabled. Some cheats or codes can unexpectedly interfere with
  emulation and make troubleshooting errors difficult.
- If Dolphin is not connecting, ensure that `Enable Emulated Memory Size Override` in Dolphin (under `Options` >
  `Configuration` > `Advanced`) is **disabled**.
- If you run with a custom GC boot menu, you'll need to skip it by going to `Options` > `Configuration` > `GameCube`
  and checking `Skip Main Menu`.
- If Dolphin does load the RELoader save file and has a popup saying something like "Save file cannot be loaded",
  There may be a normal save file in your dolphin save folder, this will need to be removed in order for the randomizer to load.
- If you have killed Ganon but the world has not been realesed. Ensure that the host settings allows player releases.
  If you are not playing the US verison it will not work.
  Check that the Archipelego Randomizer is loaded by bringing up the console window.
