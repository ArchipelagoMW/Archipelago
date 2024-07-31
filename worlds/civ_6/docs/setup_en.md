# Setup Guide for Civilization VI Archipelago

This guide is meant to help you get up and running with Civlization VI in your Archipelago run. Note that this requires you to have both Rise & Fall as well as Gathering Storm installed. This will not work unless both of those DLCs are enabled.

## Requirements

The following are required in order to play Civ VI in Archipelago

- Windows OS (Firaxis does not support the necessary tooling for Mac, Linux is yet to bet verified)

- Installed [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases) v0.4.5 or higher.\
   **Make sure to install the Generator if you intend to generate multiworlds.**
- The latest version of the [Civ VI apworld](https://github.com/hesto2/civilization_vi_apworld/releases/latest).

- The latest version of the [Civ VI AP Mod](https://github.com/hesto2/civilization_archipelago_mod).

- Tuner setting enabled so the archipelago client can communicate with the game

## Enabling the tuner
Depending on how you installed Civ 6 you will have to navigate to one of the following:
- `YOUR_USER/Documents/My Games/Sid Meier's Civilization VI/AppOptions.txt`
- `YOUR_USER/AppData/Local/Firaxis Games/Sid Meier's Civilization VI/AppOptions.txt`

Once you have located your `AppOptions.txt`, do a search for `Enable FireTuner`. Set `EnableTuner` to `1` instead of `0`. __NOTE__: While this is active, achievments will be disabled.

## Mod Installation

1. Download and unzip the latest release of the mod from [github](https://github.com/hesto2/civilization_archipelago_mod/releases).

2. Copy the folder containing the mod files to your Civ VI mods folder. On Windows, this is usually located at `C:\Users\YOUR_USER\Documents\My Games\Sid Meier's Civilization VI\Mods`

3. After the Archipelago host generates a game, you should be given another zip file titled `AP-{playername}....zip`. Unzip this and copy all of its contents into your mod folder.

4. Your finished mod folder should look something like this:
- Civ VI Mods Directory
  - civilization_archipelago_mod
    - NewItems.xml
    - InitOptions.lua
    - Archipelago.modinfo
    - All the other mod files, etc.

## AP World Installation

1. Unzip the downloaded Civ VI apworld zip file
2. Place the `civ6.apworld` file in your Archipelago installation's `lib/worlds` folder (Windows default to:
   `%programdata%/Archipelago`).

- If you have a `civ6.apworld` file from a previous version of the apworld, you **must** delete it, as it is no longer
  supported. Additionally, if there is a `civ6` folder in that folder, you **must** also delete it. Keeping
  these around will cause issues, even if multiworlds are successfully generated.

## Setting Up a YAML

All players playing Civ VI must provide the room host with a YAML file containing the settings for their world.
A sample YAML file for Civ VI is supplied in the Civ VI apworld download. Refer to the comments in that file for
details about what each setting does.

Once complete, provide the room host with your YAML file.

## Generating a Multiworld

If you're generating a multiworld game that includes Civ VI, you'll need to run it locally since the online
generator does not yet support it. Follow these steps to generate a multiworld:

1. Gather all player's YAMLs. Place these YAMLs into the `Players` folder of your Archipelago installation. If the
   folder does not exist, then it must be created manually. The files here should not be compressed.
2. Modify any local host settings for generation, as desired.
3. Run `ArchipelagoGenerate.exe` (without `.exe` on Linux) or click `Generate` in the launcher. The generation output
   is placed in the `output` folder (usually named something like `AP_XXXXX.zip`). \* Please note that if any player in the game you want to generate plays a game that needs a ROM file to generate,
   you will need the corresponding ROM files.
4. Unzip the `AP_XXXXX.zip` file. It should include a zip file for each player in the room playing Civ VI. Distribute each file to the appropriate player.
5. **Delete the distributed zip files and re-zip the remaining files**. In the next section, use this archive file to
   host a room or provide it to the room host. \* If you plan to host the room on a local machine, skip this step and use the original zip file (`AP_XXXX.zip`) instead.

## Hosting a Room

If you're generating the multiworld, follow the instructions in the previous section. Once you have the zip file
corresponding to your multiworld, follow
[these steps](https://archipelago.gg/tutorial/Archipelago/setup/en#hosting-an-archipelago-server) to host a room. Follow
the instructions for hosting on the website from a locally generated game or on a local machine.

## Connecting to a Room

You should have the zip file provided to you by the multiworld generator. You should also have the room's server
name and port number from the room's host.

Once you do, follow these steps to connect to the room:

1. Unzip the folder given to you and copy its contents (should include `NewItems.xml` an `archipelago.json`, and more) into the installed mod folder.
2. Start `ArchipelagoLauncher.exe` and choose `Civ6 Client`, which will open the text client.
3. Connect to the room by entering the server name and port number at the top and pressing `Connect`. For rooms hosted
   on the website, this will be `archipelago.gg:<port>`, where `<port>` is the port number. If a game is hosted from the
   `ArchipelagoServer.exe` (without `.exe` on Linux), this will default to `38281` but may be changed in the `host.yaml`.
4. Once you successfully configure and launch a game, the client should let you know it is connected and you will be ready to play!

## Configuring your game

When configuring your game, make sure to start the game in the Ancient Era and leave all settings related to starting technologies and civics as the defaults. Other than that, configure difficulty, AI, etc. as you normally would.

## Troubleshooting

- If you do not see the client in the launcher, ensure you have placed the `civ6.apworld` in the correct folder (the
  `lib/worlds` folder of your Archipelago installation).

- If you are getting an error: `The remote computer refused the network connection`, or something else related to the client (or tuner) not being able to connect, it likely indicates the tuner is not actually enabled. One simple way to verify that it is enabled is, after completing the setup steps, to go Main Menu -> Options -> Look for an option named "Tuner" and verify it is set to "Enabled"

- If your game gets in a state where someone has sent you items or you have sent locations but these are not correctly replicated to the multiworld, you can run `/resync` from the Civ 6 client. This may take up to a minute depending on how many items there are.


## Feedback
In the offical [Archipelago Discord](https://discord.com/invite/8Z65BR2) under the `future-game-design` channel there is a `civilization-vi` [thread](https://discord.com/channels/731205301247803413/1235473969487024189/1235473969487024189). Feel free to ping `@hesto2` with any bugs/thoughts/complaints/wishes/jokes you may have!