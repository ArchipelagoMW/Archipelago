# Setup Guide for Metroid Prime Archipelago

This guide is meant to help you get up and running with Metroid Prime APWorld with Archipelago.
This has only been tested on Windows, but feel free to let us know if you get the chance to try it on other OS platforms!

## Requirements

The following are required in order to play _Metroid Prime_ in Archipelago:

- [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases)
   For Archipelago 5.0/5.1, see the Note about Python versions in [APWorld Installation](#apworld-installation)
- [Dolphin Emulator](https://dolphin-emu.org/download/). We recommend the latest Release version.
- A _Metroid Prime_ (GameCube version) ISO file
  - Any official release copy of the GameCube version will work. (All region versions are compatible, including all three versions of NTSC-USA)
  - The Wii and Switch version of the game are _not_ supported.

## APWorld Installation

1. Download the latest version of the [Metroid Prime AP](https://github.com/Electro1512/MetroidAPrime/releases/latest)
2. Unzip the downloaded Metroid Prime APWorld zip file and extract its files.
3. In the Archipelago Launcher, select `Install APWorld`, and then select `metroidprime.apworld` file from the previous step.

>[!NOTE]
> Because Archipelago 5.1 on Windows transitioned to using Python 3.12, current releases of Metroid Prime AP offers two options to download:
> | Archipelago Version                             |                                              |
> |-------------------------------------------------|----------------------------------------------|
> | Archipelago 5.1 or later for Windows            | Download APWorld file ending with `3.12.zip`.|
> | Archipelago 5.1 AppImage or Tarball for Linux   | Download APWorld file ending with `3.11.zip`.|
> | Archipelago 5.0 or earlier for Windows          | Download APWorld file ending with `3.11.zip`.|
>
>  Future versions after Metroid Prime AP 0.4.9 will likely target only Python 3.12 and will only work on Archipelago 5.1.

>[!IMPORTANT]
> If you have used a previous version of Metroid Prime AP that required copying folders into the `/lib` folder, go to your `Archipelago/lib` folder and delete the following directories:
> - `dolphin_memory_engine` (This may be kept if another APWorld depends on this folder, but may cause issues if versions are mismatched.)
> - `ppc_asm`
> - `py_randomprime`
>
> These are now included in the APWorld file.

## Setting Up Player Options YAML File

All players playing _Metroid Prime_ must provide the room host with a YAML file containing the player options for their world.
A sample YAML file for _Metroid Prime_ is supplied in the Metroid Prime APWorld download. Refer to the comments in that file for details about what each setting does.

Once complete, provide the person generating with your YAML file.

## Generating a Multiworld
As usual, randomized Archipelago games with custom worlds must be generated locally - see [Archipelago Setup Guide: Generating a game - On your local installation](https://archipelago.gg/tutorial/Archipelago/setup/en#on-your-local-installation)

## Hosting a Room

If you're generating the multiworld, follow the instructions in the previous section.
Once you have the zip file corresponding to your multiworld, follow [Archipelago Setup Guide: Hosting an Archipelago Server](https://archipelago.gg/tutorial/Archipelago/setup/en#hosting-an-archipelago-server) to host a room.

> [!NOTE]
> When hosting with the Archipelago website, the website will *not* host patch files from imported custom worlds, such as Metroid Prime AP.
> The person generating must manually distribute the `.apmp1` patch files to the corresponding players.

## Starting the Game and Connecting to a Room

You should have the `.apmp1` patch file provided to you by the multiworld generator. You should also have the room's server
name and port number from the room's host.

Once you do, follow these steps to connect to the room:

1. In the Archipelago Launcher, click `Open Patch File`. Then select the `.apmp1` patch file.
   If you have not done so before, it will ask you what program you want to open it with.
2. If this is your first time, it will prompt you for an input iso. Select your _Metroid Prime_ GameCube ISO file.
3. The patch will take some time to complete in the background. (Be patient! The game is 1.46 GB!)
4. Once the output iso file appears in the same directory as your `.apmp1` file (it should be named `AP_XXXX.iso`), open it with Dolphin.
5. After the game is running, connect the Metroid Prime Client to the room by entering the server name and port number at the top and pressing `Connect`.
   For rooms hosted on the website, this will be `archipelago.gg:<port>`, where `<port>` is the port number.
   If a game is hosted from the `ArchipelagoServer.exe` (without `.exe` on Linux), this will default to `38281` but may be changed in the `host.yaml`.

>[!TIP]
>  **Optional**
>  If you want double-clicking `.apmp1` patch file to automatically open your game for you,
>    - Navigate to your `Archipelago` installation and edit the `host.yaml` file.
>    - Scroll down to `metroidprime_options` and either set `rom_start` to `true` if ISO files are already associated with Dolphin or set it to the path to your `Dolphin.exe`.
>    - If `metroidprime_options` isn't in the `host.yaml` yet, click your `.apmp1` patch file and then reopen the `host.yaml` and it should now be there.
>
>    Now when double-clicking the `.apmp1` patch file, it should open the client, patch, and launch Dolphin all at once!

## Troubleshooting

### General Troubleshooting Tips
- Use the latest Metroid Prime Archipelago release
  - Metroid Prime Archipelago: [Releases · Electro1512_MetroidAPrime](https://github.com/Electro1512/MetroidAPrime/releases)

- Use the latest Dolphin Emulator
  - Dolphin Emulator Release (**Recommended**): [Dolphin Emulator - Download](https://dolphin-emu.org/download/)
  - PrimeHack: [Releases · shiiion/dolphin](https://github.com/shiiion/dolphin/releases)
    - While the dependencies that Metroid Prime AP uses does not target PrimeHack, many users report that PrimeHack can work.
      However, any issues found while using PrimeHack should be reproduced with the official Dolphin Emulator before reporting.

### Generating and Patching Troubleshooting

- If you do not see the client in the Archipelago Launcher
  - Ensure you have your `metroidprime.apworld` in the correct folder (The `custom_worlds` folder).
  - Check if you have residual files from previous versions in the lib/worlds folder - see the [APWorld Installation section](#apworld-installation)
  - Go to `%TEMP%` (C:\Users\<Username>\AppData\Local\Temp) and delete the folder `ap_metroidprime_temp_lib_vX.Y.Z`. Then restart the Archipelago Launcher.

- If you receive this error in a dialog box after opening the AP_XXXXX_PX.apmp1 file:
  > Count Mount File
  > The disc image is corrupted.

  This is not an error related to the patcher - this is Windows File Explorer attempting to mount the GameCube ISO as a removable drive. It's likely that the patcher did sucessfully patch the game.
  See if the patched ISO exists (often named AP_XXXXX_PX.iso). If it does, you can load it manually in Dolphin.

### Connection Troubleshooting
- I have the randomized game open in Dolphin, but the Metroid Prime client says it can't connect to it!
  - Make Sure the ISO is Randomized
    - On the Main Menu, "Archipelago Metroid Prime" text should appear. ([image example](https://i.imgur.com/W6172zf.png))
  - Ensure Only One Instance of Dolphin is Running
    - Check Task Manager to see if there's multiple emulator instances running.
    - You can also just restart your computer to be sure.

  - Disable Emulated Memory Size Override
    - In Dolphin,
      Config -> Advanced tab,
      **Uncheck** Enable Emulated Memory Size Override
  - Start the Metroid Prime Client and Dolphin in a Specific Order

    - For some users, connecting to the AP server before letting the Metroid Prime client causes connection issues.
      Try starting the game in this order:
      1.) Start the Metroid Prime client
      2.) Start Dolphin and start the game (if it launches automatically, that's fine)
      3.) Select or create a save file and enter the game
      4.) Enter the AP server address into the Metroid Prime Client

  - For Linux, use Dolphin FlatPak
    - Install Dolphin Emulator from [Flathub](https://flathub.org/apps/org.DolphinEmu.dolphin-emu)
    - Dolphin Memory Engine, as part of the Prime AP Client, can not access regular Dolphin's process but can access Flatpak's containerized Dolphin's process

### In-Game Troubleshooting
- In Dolphin, when fighting Ridley my screen keeps changing width
  - This is an issue with Dolphin's widescreen detection heuristic.
  - In Dolphin, go to Graphics > General tab, and then set Aspect Ratio to `Force 4:3`

## Feedback

In the offical [Archipelago Discord](https://discord.com/invite/8Z65BR2) under the `future-game-design` channel, there is a [_Metroid Prime_ thread](https://discord.com/channels/731205301247803413/1172631093837570068).
Feel free to ping `@Electro15` or `@hesto2` with any bugs/thoughts/complaints/wishes/jokes you may have!
