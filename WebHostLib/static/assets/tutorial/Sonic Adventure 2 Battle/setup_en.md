# Sonic Adventure 2: Battle Randomizer Setup Guide

## Required Software

- Sonic Adventure 2: Battle from: [Sonic Adventure 2: Battle Steam Store Page](https://store.steampowered.com/app/213610/Sonic_Adventure_2/)
- Sonic Adventure 2 Mod Loader from: [Sonic Retro Mod Loader Page](http://info.sonicretro.org/SA2_Mod_Loader)
- Archipelago Mod for Sonic Adventure 2: Battle
  from: [Sonic Adventure 2: Battle Archipelago Randomizer Mod Releases Page](https://github.com/PoryGone/SA2B_Archipelago)

## Installation Procedures

1. Install Sonic Adventure 2 Mod Loader as per its instructions.

2. The folder you installed the Sonic Adventure 2 Mod Loader into will now have a /mods directory.

3. Unpack the Archipelago Mod into this folder, so that "/mods/SonicAdventure2Randomizer" is a valid path.

4. From the SonicAdventure2Randomizer folder, copy the APCpp.dll, move up two folders to where the sonic2app.exe is, and paste the APCpp.dll

5. Launch the SA2ModManager.exe and make sure the SonicAdventure2Randomizer mod is listed and enabled.

## Joining a MultiWorld Game

1. At the location where you unpacked the mod (EX: "Sonic Adventure 2/mods/SonicAdventure2Randomizer") edit the config.ini file in the SonicAdventure2Randomizer folder in a program such as Notepad.

2. For the IP field, enter the address of the server, such as archipelago.gg:38281, your server host should be able to tell you this.

3. For the PlayerName field, enter your "name" field from the yaml, or website config.

4. For the Password field, enter the server password if one exists, otherwise leave blank.

5. Save the file and lauch the game. Once you create a new save file, the game will attempt to connect and the message "Connected to Archipelago" will appear if you sucessfully connect.

## Save File Safeguard (Advanced Option)

The mod contains a save file safeguard which associates a savefile to a specific Archipelago seed. By default, save files can only connect to archipelago servers that match their seed. The safeguard can be disabled in the mod config.ini by setting `IgnoreFileSafety` to true. This is NOT recommended for the standard user as it will allow any save file to connect and send items to the archipelago server.