# Inscryption Randomizer Setup Guide

## Required Software

- [Inscryption](https://store.steampowered.com/app/1092790/Inscryption/)
- For easy setup (recommended):
  - [r2modman](https://inscryption.thunderstore.io/package/ebkr/r2modman/) OR [Thunderstore Mod Manager](https://www.overwolf.com/app/Thunderstore-Thunderstore_Mod_Manager)
- For manual setup:
  - [BepInEx pack for Inscryption](https://inscryption.thunderstore.io/package/BepInEx/BepInExPack_Inscryption/)
  - [ArchipelagoMod](https://inscryption.thunderstore.io/package/Ballin_Inc/ArchipelagoMod/)

## Installation
Before starting the installation process, here's what you should know:
- Only install the mods mentioned in this guide if you want a guaranteed smooth experience! Other mods were NOT tested with ArchipelagoMod and could cause unwanted issues.
- The ArchipelagoMod will create a separate save file when playing, but for safety measures, back up your save file by going to your Inscryption installation directory and copy the "SaveFile.gwsave" file to another folder.
- It is strongly recommended to use a mod manager if you want a quicker and easier installation process, but if you don't like installing extra software and are comfortable moving files around, you can refer to the manual setup guide instead.

### Easy setup (mod manager)
1. Download [r2modman](https://inscryption.thunderstore.io/package/ebkr/r2modman/) using the "Manual Download" button, then install it using the executable in the downloaded zip package (You can also use [Thunderstore Mod Manager](https://www.overwolf.com/app/Thunderstore-Thunderstore_Mod_Manager) which is exactly the same, but it requires [Overwolf](https://www.overwolf.com/))
2. Open the mod manager and select Inscryption in the game selection screen.
3. Select the default profile or create a new one.
4. Open the "Online" tab on the left, then search for "ArchipelagoMod".
5. Expand ArchipelagoMod and click the "Download" button to install the latest version and all its dependencies.
6. Click "Start Modded" to open the game with the mods (a console should appear if everything was done correctly).

### Manual setup
1. Download the following mods using the "Manual Download" button:
   - [BepInEx pack for Inscryption](https://inscryption.thunderstore.io/package/BepInEx/BepInExPack_Inscryption/)
   - [ArchipelagoMod](https://inscryption.thunderstore.io/package/Ballin_Inc/ArchipelagoMod/)
2. Open your Inscryption installation directory. On Steam, you can find it easily by right clicking the game and clicking "Manage" > "Browse local files".
3. Open the BepInEx pack zip file, then open the "BepInExPack_Inscryption" folder.
4. Drag all folders and files located inside the "BepInExPack_Inscryption" folder and drop them in your Inscryption directory.
5. Open the "BepInEx" folder in your Inscryption directory.
6. Open the ArchipelagoMod zip file.
7. Drag and drop the "plugins" folder in the "BepInEx" folder to fuse with the existing "plugins" folder.
8. Open the game normally to play with mods (if BepInEx was installed correctly, a console should appear).

## Joining a new MultiWorld Game
1. Make sure you have a fresh save everytime you start a new MultiWorld! If this isn't your first MultiWorld with Inscryption, press the "Reset save data" button four times in the settings. This should boot you back to the starting cutscene.
2. In the game's main menu, open the settings menu.
3. If everything was installed correctly, you should see a fourth tab with the Archipelago logo.
4. Open the fourth tab and fill the text boxes with the MultiWorld server information (if the server is hosted on the website, leave the host name as "archipelago.gg").
5. Click the "connect" button. If successful, the status on the top-right should change to "connected". If not, a red error message should appear.
6. Return to the main menu and start the game.

## Continuing a MultiWorld Game
Unless the host name or port has changed, you don't need to return to the settings when you re-open the game. Selecting the "Continue" option should automatically connect you to the server. Everything you write in the settings is saved for all future sessions.

## Troubleshooting
### There is no fourth tab in the settings.
If there is no fourth tab, it can be one of two issues:
 - If there was no console appearing when opening the game, this means the mods didn't load correctly. Here's what you can try:
   - If you are using the mod manager, make sure to open it and press "Start Modded". Opening the game normally from Steam won't load any mods.
   - Check if the mod manager correctly found the game path. In the mod manager, click "Settings" then go to the "Locations" tab. Make sure the path listed under "Change Inscryption directory" is correct. You can verify the real path if you right click the game on steam and click "Manage" > "Browse local files". If the path is wrong, click that setting and change the path.
   - If you installed the mods manually, this usually means BepInEx was not correctly installed. Make sure to read the installation guide carefully.
   - If there is still no console when opening the game modded, try asking in the [Archipelago Discord Server](https://discord.gg/8Z65BR2) for help.
 - If there is a console, this means the mods loaded but the ArchipelagoMod wasn't found or had errors while loading.
   - Look in the console and make sure you can find a message about ArchipelagoMod being loaded.
   - If you see any red text, there was an error. Report the issue in the [Archipelago Discord Server](https://discord.gg/8Z65BR2) or create an issue in our [GitHub](https://github.com/DrBibop/Archipelago_Inscryption/issues).

### I'm getting a different issue.
You can ask for help in the [Archipelago Discord Server](https://discord.gg/8Z65BR2) or, if you think you've found a problem with the mod, create an issue in our [GitHub](https://github.com/DrBibop/Archipelago_Inscryption/issues).