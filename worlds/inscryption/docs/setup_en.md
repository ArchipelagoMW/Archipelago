# Inscryption Randomizer Setup Guide

## Required Software

- [Inscryption](https://store.steampowered.com/app/1092790/Inscryption/)
- For easy setup (recommended):
  - [r2modman](https://inscryption.thunderstore.io/package/ebkr/r2modman/) OR [Thunderstore Mod Manager](https://www.overwolf.com/app/Thunderstore-Thunderstore_Mod_Manager)
- For manual setup:
  - [BepInEx pack for Inscryption](https://inscryption.thunderstore.io/package/BepInEx/BepInExPack_Inscryption/)
  - [MonoMod Loader for Inscryption](https://inscryption.thunderstore.io/package/BepInEx/MonoMod_Loader_Inscryption/)
  - [Inscryption API](https://inscryption.thunderstore.io/package/API_dev/API/)
  - [ArchipelagoMod](https://inscryption.thunderstore.io/package/Ballin_Inc/ArchipelagoMod/)

## Installation
**Only install the mods mentionned in this guide if you want a guaranteed smooth experience! Other mods were NOT tested with ArchipelagoMod and could cause unwanted issues.** It is strongly recommended to use a mod manager if you want a quicker and easier installation process. If you don't like installing extra software and are comfortable with moving files around, refer to the manual setup instead.

### Easy setup (mod manager)
1. Back up your save file! Go to your Inscryption installation directory and move the "SaveFile.gwsave" file somewhere safe.
2. If you see them in your game directory, delete "SaveFile.gwsave", "SaveFile-Backup.gwsave" and "ModdedSaveFile.gwsave".
3. Download [r2modman](https://inscryption.thunderstore.io/package/ebkr/r2modman/) using the "Manual Download" button, then install it using the executable in the downloaded zip package (You can also use [Thunderstore Mod Manager](https://www.overwolf.com/app/Thunderstore-Thunderstore_Mod_Manager) which is exactly the same but it requires [Overwolf](https://www.overwolf.com/))
4. Open the mod manager and select Inscryption in the game selection screen.
5. Select the default profile or create a new one.
6. Open the "Online" tab on the left, then search for "ArchipelagoMod".
7. Expand InscryptionMod and click the "Download" button to install the latest version and all its dependencies.
8. Click "Start Modded" to open the game with the mods (a console should appear if everything was done correctly).

### Manual setup
1. Backup your save file! Go to your Inscryption installation directory and move the "SaveFile.gwsave" file somewhere safe.
2. If you see them in your game folder, delete "SaveFile.gwsave", "SaveFile-Backup.gwsave" and "ModdedSaveFile.gwsave".
3. Download the following mods using the "Manual Download" button:
   - [BepInEx pack for Inscryption](https://inscryption.thunderstore.io/package/BepInEx/BepInExPack_Inscryption/)
   - [MonoMod Loader for Inscryption](https://inscryption.thunderstore.io/package/BepInEx/MonoMod_Loader_Inscryption/)
   - [Inscryption API](https://inscryption.thunderstore.io/package/API_dev/API/)
   - [ArchipelagoMod](https://inscryption.thunderstore.io/package/Ballin_Inc/ArchipelagoMod/)
4. Open your Inscryption installation directory. On Steam, you can find it easily by right clicking the game and clicking "Manage" > "Browse local files".
5. Open the BepInEx pack zip file, then open the "BepInExPack_Inscryption" folder.
6. Drag the two folders and three files located inside the "BepInExPack_Inscryption" folder and drop them in your Inscryption directory.
7. Open the "BepInEx" folder in your Inscryption directory.
8. Open the MonoMod Loader zip file.
9. Drag and drop the "patchers" folder in the "BepInEx" folder.
10. Open the API zip file.
11. Drag and drop the "monomod" and "plugins" folder in the "BepInEx" folder.
12. Open the ArchipelagoMod zip file.
13. Drag and drop the "plugins" folder in the "BepInEx" folder to fuse with the existing "plugins" folder.
14. Open the game to play with mods (if BepInEx was installed correctly, a console should appear).

## Joining a MultiWorld Game
1. Make sure you have a fresh save everytime you start a new multiworld! Refer to the first two steps of the installation guide.
2. In the game's main menu, open the settings menu.
3. If everything was installed correctly, you should see a fourth tab with the Archipelago logo.
4. Open the fourth tab and fill the text boxes with the multiworld server information (if the server is hosted on the website, leave the host name as "archipelago.gg").
5. Click the "connect" button. If successful, the status on the top-right should change to "connected". If not, a red error message should appear.
6. Return to the main menu and start the game.
7. Everything you've written in the text boxes are saved. There is no need to rewrite anything when you re-open the game. Just select "continue" the next time and it will automatically connect you with the saved information.

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

### I connected to a new multiworld and it sent a bunch of items to other players.
Assuming this is not your first multiworld with Inscryption, this means that you didn't properly reset your save. Refer to the first two steps of the installation guide to back up and delete your save file. Since a bunch of items were sent, you will obviously need to reset the multiworld.

### I'm getting a different issue.
You can ask for help in the [Archipelago Discord Server](https://discord.gg/8Z65BR2) or, if you think you've found a problem with the mod, create an issue in our [GitHub](https://github.com/DrBibop/Archipelago_Inscryption/issues).