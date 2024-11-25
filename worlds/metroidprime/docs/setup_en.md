# Setup Guide for Metroid Prime Archipelago

This guide is meant to help you get up and running with Metroid Prime in your Archipelago run.

Windows is the only OS this has been tested on, but feel free to let us know if you get the chance to try it on Linux or MacOS

## Requirements

The following are required in order to play Metroid Prime in Archipelago

- Installed [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases) v0.4.5 or higher.\
   **Make sure to install the Generator if you intend to generate multiworlds.**
- The latest version of the [Metroid Prime apworld](https://github.com/Electro1512/MetroidAPrime/releases/latest).
- [Dolphin Emulator](https://dolphin-emu.org/download/). We recommend the latest beta version.
- A Metroid Prime US ISO (`DOL-GM8E-0-00 USA`)

## AP World Installation

1. Unzip the downloaded Metroid Prime apworld zip file
2. Double click the `metroidprime.apworld` to install it to your local Archipelago instance.

   - If you have used a version that required copying folders into the `/lib` folder, go to your `Archipelago/lib` folder and delete the following directories. These are now included in the `.apworld`

     - `ppc_asm`
     - `dolphin_memory_engine`
     - `py_randomprime`

   - If you are currently on Archipelago version < `0.5.0` Place the `metroidprime.apworld` file in your Archipelago installation's `lib/worlds` folder (Default location for Windows: `%programdata%/Archipelago`). Overwrite any existing `metroidprime.apworld` file

## Setting Up a YAML

All players playing Metroid Prime must provide the room host with a YAML file containing the settings for their world.
A sample YAML file for Metroid Prime is supplied in the Metroid Prime apworld download. Refer to the comments in that file for details about what each setting does.

Once complete, provide the room host with your YAML file.

## Generating a Multiworld

If you're generating a multiworld game that includes Metroid Prime, you'll need to run it locally since the online
generator does not yet support it. Follow these steps to generate a multiworld:

1. Gather all player's YAMLs. Place these YAMLs into the `Players` folder of your Archipelago installation. If the
   folder does not exist, then it must be created manually. The files here should not be compressed.

2. Modify any local host settings for generation, as desired.

3. Run `ArchipelagoGenerate.exe` (without `.exe` on Linux) or click `Generate` in the launcher. The generation output
   is placed in the `output` folder (usually named something like `AP_XXXXX.zip`). \* Please note that if any player in the game you want to generate plays a game that needs a ROM file to generate,
   you will need the corresponding ROM files.

4. Unzip the `AP_XXXXX.zip` file. It should include a zip file for each player in the room playing Metroid Prime. Distribute each file to the appropriate player.

5. **Delete the distributed zip files and re-zip the remaining files**. In the next section, use this archive file to
   host a room or provide it to the room host. \* If you plan to host the room on a local machine, skip this step and use the original zip file (`AP_XXXX.zip`) instead.

## Hosting a Room

If you're generating the multiworld, follow the instructions in the previous section.
Once you have the zip file corresponding to your multiworld, follow [these steps](https://archipelago.gg/tutorial/Archipelago/setup/en#hosting-an-archipelago-server) to host a room.
Follow the instructions for hosting on the website from a locally generated game or on a local machine.

## Starting the Game and Connecting to a Room

You should have the `apmp1` file provided to you by the multiworld generator. You should also have the room's server
name and port number from the room's host.

Once you do, follow these steps to connect to the room:

0. (Optional): If you want the `apmp1` file to automatically open your game for you, navigate to your `Archipelago` installation and edit the `host.yaml` file.
   - Scroll down to `metroidprime_options` and either set `rom_start` to `true` if ISO files are already associated with Dolphin, or set it to the path to your `Dolphin.exe`.
   - If `metroidprime_options` isn't in the `host.yaml` yet, click your `apmp1` file and then reopen the `host.yaml` and it should now be there.
1. Double click the `apmp1` file. If you have not done so before, it will ask you what program you want to open it with.
   Click "Choose another program" and browser to your Archipelago directory. Select `ArchipelagoLauncher.exe`.
2. Be patient, after clicking the `apmp1` file, it can take a minute to have the client and patched iso showup
3. If this is your first time, it will prompt you for an input iso. Select your Metroid Prime DOL-GM8E-0-00 USA iso
4. Once the output iso file appears in the same directory as your `apmp1` file (it should have a name `AP_XXXX.iso`), open it with Dolphin (or if you associated the file type with Dolphin, sit back and enjoy watching the computer do this menial task for you)
5. After the game is running, connect the Metroid Prime Client to the room by entering the server name and port number at the top and pressing `Connect`.
   For rooms hosted on the website, this will be `archipelago.gg:<port>`, where `<port>` is the port number.
   If a game is hosted from the `ArchipelagoServer.exe` (without `.exe` on Linux), this will default to `38281` but may be changed in the `host.yaml`.

## Troubleshooting

- If you launch the client and the game but are still getting an error saying it is waiting for the game to start, verify you are running version `0-00`. To check this:

  - Add your original ISO to the list of games in Dolphin
  - Right click on it, select properties
  - Browse to the info tab (you will need to click the arrow to view more tabs to the right)
  - Verify under name it says `Metroid Prime  (Revision 0)`

- If the client is running, connected to the Archipelago server but it appears to not be able to connect to dolphin, verify you only have one instance of Dolphin opened up. If there are other windows (even if they aren't running anything) it will cause problems with the client.

- If you do not see the client in the launcher, ensure you have your `metroidprime.apworld` in the correct folder (either the `custom_worlds` folder or the
  `lib/worlds` folder of your Archipelago installation).

- If you receive this error in a dialog box after opening the AP_XXXXX_PX.apmp1 file:
  > Count Mount File
  > The disc image is corrupted.
  > This is not an error related to the patcher - this Windows File Explorer attempting to mount the GameCube ISO as a removable drive. It's likely that the patcher did sucessfully patch the game.
  > See if the patched ISO exists (often named AP_XXXXX_PX.iso),
  > If it does, you can load it manually in Dolphin.

## Connection Troubleshooting

- Use the latest Metroid Prime Archipelago release

  - Metroid Prime Archipelago: [Releases · Electro1512_MetroidAPrime](https://github.com/Electro1512/MetroidAPrime/releases)

- Use the latest Dolphin

  - Dolphin Beta (**Recommended**): [Dolphin Emulator - Download](https://dolphin-emu.org/download/#download-beta)
  - PrimeHack (Not thorougly tested with Metroid Prime AP): [Releases · shiiion_dolphin.htm](https://github.com/shiiion/dolphin/releases)

- Use the Correct Version of the Game

  - Ensure your ISO of Metroid Prime is the supported version:
    - Platform: `GameCube` (None of the Wii versions are supported.)
    - Game ID: `GM8E01`
    - Version Number: `DOL-GM8E-0-00 USA` ("0-00")
    - SHA-1: `ac20c744db18fdf0339f37945e880708fd317231`
    - For information on determining the disc's version number, see [metroid2002.com metroid prime version differences version number](https://www.metroid2002.com/version_differences_version_number.php).

- Ensure Only One Instance of Dolphin is Running

  - Check Task Manager to see if there's multiple emulator instances running.
  - You can also just restart your computer to be sure.

- Disable Emulated Memory Size Override
  - In Dolphin,
    Config -> Advanced tab,
    **Uncheck** Enable Emulated Memory Size Override
- Start the Metroid Prime Client and Dolphin in a Specific Order

  - For some users, connecting to the AP server before letting the Metroid Prime client causes connection issues
    Try starting the game in this order:
    1 . Start the Metroid Prime client
    2 . Start Dolphin and start the game (if it launches automatically, that's fine)
    3 . Select or create a save file and enter the game
    4 . Enter the AP server address into the Metroid Prime Client

- Avoid using Dolphin FlatPak

  - FlatPak may block the Metroid Prime client's ability to connect to Dolphin
    You may need to build and run the Dolphin binaries directly - see [Building for Linux · dolphin-emu_dolphin Wiki.htm](https://github.com/dolphin-emu/dolphin/wiki/Building-for-Linux)

- Make Sure the ISO is Randomized
  - On the Main Menu, "Archipelago Metroid Prime" text should appear. ([image example](https://i.imgur.com/W6172zf.png))

## Feedback

In the offical [Archipelago Discord](https://discord.com/invite/8Z65BR2) under the `future-game-design` channel, there is a [_Metroid Prime_ thread](https://discord.com/channels/731205301247803413/1172631093837570068).
Feel free to ping `@Electro15` or `@hesto2` with any bugs/thoughts/complaints/wishes/jokes you may have!
