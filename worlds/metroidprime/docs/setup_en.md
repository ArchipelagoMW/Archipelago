# Setup Guide for Metroid Prime Archipelago

This guide is meant to help you get up and running with Metroid Prime in your Archipelago run.

Windows is the only OS this has been tested on, but feel free to let us know if you get the chance to try it on Linux or macOS

## Requirements

The following are required in order to play Metroid Prime in Archipelago

- Installed [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases/latest) v0.4.5 or higher.\
- [Dolphin Emulator](https://dolphin-emu.org/download/). We recommend the latest beta version.
- A Metroid Prime US ISO for GameCube

## Connection Troubleshooting

- Use the latest Dolphin

  - Dolphin Beta (**Recommended**): [Dolphin Emulator - Download](https://dolphin-emu.org/download/#download-beta)
  - PrimeHack (Not thoroughly tested with Metroid Prime AP): [Releases · shiiion_dolphin.htm](https://github.com/shiiion/dolphin/releases)

- Ensure Only One Instance of Dolphin is Running

  - Check Task Manager to see if there's multiple emulator instances running.
  - You can also just restart your computer to be sure.

- Disable Emulated Memory Size Override
  - In Dolphin,  
    Config &rarr; Advanced tab,  
    **Uncheck** Enable Emulated Memory Size Override
- Start the Metroid Prime Client and Dolphin in a Specific Order

  - For some users, connecting to the AP server before letting the Metroid Prime client causes connection issues
    Try starting the game in this order:  
    1\. Start the Metroid Prime client  
    2\. Start Dolphin and start the game (if it launches automatically, that's fine)  
    3\. Select or create a save file and enter the game  
    4\. Enter the AP server address into the Metroid Prime Client

- Avoid using Dolphin FlatPak

  - FlatPak may block the Metroid Prime client's ability to connect to Dolphin
    You may need to build and run the Dolphin binaries directly - see [Building for Linux · dolphin-emu_dolphin Wiki.htm](https://github.com/dolphin-emu/dolphin/wiki/Building-for-Linux)

- Make Sure the ISO is Randomized
  - On the Main Menu, "Archipelago Metroid Prime" text should appear. ([image example](https://i.imgur.com/W6172zf.png))
