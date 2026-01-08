# Setup Guide for Ratchet & Clank 2 Archipelago

This guide is meant to help you get up and running with Ratchet & Clank 2 in your Archipelago run.

## Requirements

The following are required in order to play Ratchet & Clank 2 in Archipelago

- Installed [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases) v0.5.0 or higher.\
   **Make sure to install the Generator if you intend to generate multiworlds.**
- The latest version of the [Ratchet & Clank 2 apworld](https://github.com/evilwb/APRac2/releases).
- [PCSX2 Emulator](https://pcsx2.net/downloads/). Must be v1.7 or higher for the required PINE support.
- A Ratchet & Clank 2 US ISO (`SCUS-97268`)

## AP World Installation

1. Unzip the downloaded Ratchet & Clank 2 apworld zip file
2. Double-click the `rac2.apworld` to install it to your local Archipelago instance

## PCSX2 Settings
- Enable PINE in PCSX2
  - In PCSX2, Under Tools, **Check** Show Advanced Settings
  - In PCSX2, System -> Settings -> Advanced tab -> PINE Settings,
    **Check** Enable and ensure Slot is set to 28011

## Setting Up a YAML

All players playing Ratchet & Clank 2 must provide the room host with a YAML file containing the settings for their world.
A sample YAML file for Ratchet & Clank 2 is supplied in the Ratchet & Clank 2 apworld download. Refer to the comments in that file for details about what each setting does.

Once complete, provide the room host with your YAML file.

## Generating a Multiworld

If you're generating a multiworld game that includes Ratchet & Clank 2, you'll need to run it locally since the online
generator does not yet support it. Follow these steps to generate a multiworld:

1. Gather all player's YAMLs. Place these YAMLs into the `Players` folder of your Archipelago installation. If the
   folder does not exist, then it must be created manually. The files here should not be compressed.

2. Modify any local host settings for generation, as desired.

3. Run `ArchipelagoGenerate.exe` (without `.exe` on Linux) or click `Generate` in the launcher. The generation output
   is placed in the `output` folder (usually named something like `AP_XXXXX.zip`). \* Please note that if any player in the game you want to generate plays a game that needs a ROM file to generate,
   you will need the corresponding ROM files.

4. Unzip the `AP_XXXXX.zip` file. It should include a zip file for each player in the room playing Ratchet & Clank 2. Distribute each file to the appropriate player.

5. **Delete the distributed zip files and re-zip the remaining files**. In the next section, use this archive file to
   host a room or provide it to the room host. \* If you plan to host the room on a local machine, skip this step and use the original zip file (`AP_XXXX.zip`) instead.

## Hosting a Room

If you're generating the multiworld, follow the instructions in the previous section.
Once you have the zip file corresponding to your multiworld, follow [these steps](https://archipelago.gg/tutorial/Archipelago/setup/en#hosting-an-archipelago-server) to host a room.
Follow the instructions for hosting on the website from a locally generated game or on a local machine.

## Starting the Game and Connecting to a Room

You should have the `aprac2` file provided to you by the multiworld generator. You should also have the room's server
name and port number from the room's host.

Once you do, follow these steps to connect to the room:

0. (Optional): If you want the `aprac2` file to automatically open your game for you, navigate to your `Archipelago` installation and edit the `host.yaml` file.
   - Scroll down to `rac2_options` and either set `rom_start` to `true` if ISO files are already associated with PCSX2, or set it to the path to your `PCSX2` binary.
   - If `rac2_options` isn't in the `host.yaml` yet, click your `aprac2` file and then reopen the `host.yaml` and it should now be there.
1. Double click the `aprac2` file. If you have not done so before, it will ask you what program you want to open it with.
   Click "Choose another program" and browser to your Archipelago directory. Select `ArchipelagoLauncher.exe`.
2. Be patient, after clicking the `aprac2` file, it can take a minute to have the client and patched iso showup
3. If this is your first time, it will prompt you for an input iso. Select your Ratchet & Clank 2 SCUS-97268 iso
4. Once the output iso file appears in the same directory as your `aprac2` file (it should have a name `AP_XXXX.iso`), open it with PCSX2 (or if you associated the file type with PCSX2, sit back and enjoy watching the computer do this menial task for you)
5. After the game is running, connect the Ratchet & Clank 2 Client to the room by entering the server name and port number at the top and pressing `Connect`.
   For rooms hosted on the website, this will be `archipelago.gg:<port>`, where `<port>` is the port number.
   If a game is hosted from the `ArchipelagoServer.exe` (without `.exe` on Linux), this will default to `38281` but may be changed in the `host.yaml`.

## Troubleshooting

- If you launch the client and the game but are still getting an error saying it is waiting for the game to start, verify you are running version `SCUS-97268`. To check this:

  - Add your original ISO to the list of games in PCSX2
  - Right click on it, select properties
  - Browse the Summary tab
  - Verify under Serial it says `SCUS-97268`

- If you do not see the client in the launcher, ensure you have your `rac2.apworld` in the correct folder (either the `custom_worlds` folder or the
  `lib/worlds` folder of your Archipelago installation).

## Connection Troubleshooting

- Use the latest Ratchet & Clank 2 Archipelago release

  - Ratchet & Clank 2 Archipelago: [Releases](https://github.com/evilwb/APRac2/releases)

- Use the latest PCSX2

  - [PCSX2 Emulator](https://pcsx2.net/downloads/)

- Use the Correct Version of the Game

  - Ensure your ISO of Ratchet & Clank 2 is the supported version:
    - Platform: `PlayStation 2` (None of the PlayStation 3 versions are supported.)
    - Version: `1.01`
    - Serial: `SCUS-97268`
    - CRC: `38996035`
    - MD5: `3cbbb5127ee8a0be93ef0876f7781ee8`

- Ensure Only One Instance of PCSX2 is Running
  - Check Task Manager to see if there's multiple emulator instances running.
  - You can also just restart your computer to be sure.

- Enable PINE in PCSX2
  - In PCSX2, Under Tools, **Check** Show Advanced Settings
  - In PCSX2, System -> Settings -> Advanced tab -> PINE Settings,
    **Check** Enable and ensure Slot is set to 28011

- Avoid using PCSX2 FlatPak
  - FlatPak may block the Ratchet & Clank 2 client's ability to connect to PCSX2

- Make Sure the ISO is Randomized
  - When you start a new game it should send you to Slim's Ship Shack instead of the Aranos Tutorial.

## Feedback

In the official [Archipelago Discord](https://discord.com/invite/8Z65BR2) under the `future-game-design` channel, there is a [_Ratchet & Clank 2_ thread](https://discord.com/channels/731205301247803413/1325015730218860554).
