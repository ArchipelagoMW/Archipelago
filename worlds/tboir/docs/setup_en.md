# Setup Guide for The Binding of Isaac: Repentance

## Required Software
- The Binding of Isaac: Rebirth including all DLC's up to Repentance or Repentance+
  - [Steam](https://store.steampowered.com/bundle/2405/The_Binding_of_Isaac_Rebirth_Complete_Bundle/)
- A save file where the paths to all the endgame bosses are unlocked
- The Archipelago of Isaac mod
  - [Steam Workshop](https://steamcommunity.com/sharedfiles/filedetails/?id=3640861678)
- The Isaac .apworld
  - [Github](https://github.com/NaveTK/Archipelago/releases/latest)

## Optional Software
- isaac-save-installer by Zamiell for a 100% completed save file
  - [Github](https://github.com/Zamiell/isaac-save-installer/)

## Installation Procedures
(You'll need to have the Archipelago Launcher installed)

1. Open the Steam Workshop page for the mod linked above
2. Click **Subscribe**
3. Download the tboir.apworld linked above
4. Double click to install it

## Create a Config (.yaml) File

### Manual Creation

As the game is not officially supported yet. Please use the new Options Creator in your Archipelago Launcher to create a YAML file.

### ~~What is a config file and why do I need one?~~

~~See the guide on setting up a basic YAML at the Archipelago setup guide: [Basic Multiworld Setup Guide](/tutorial/Archipelago/setup/en)~~

### ~~Where do I get a config file?~~

~~The Player Options page on the website allows you to configure your personal options and export a config file from them. Player options page: [The Binding of Isaac Repentance Player Options Page](/games/The%20Binding%20of%20Isaac%20Repentance/player-options)~~

### ~~Verifying your config file~~

~~If you would like to validate your config file to make sure it works, you may do so on the YAML Validator page.~~  
~~[YAML Validation page](/check)~~

## Joining a MultiWorld Game
1. Open the game
2. Select a save file with a sufficient progression state
3. Ensure **The Archipelago of Isaac** is enabled in the mod menu
4. Start a run with any character
5. Open the **Isaac Client** in your Archipelago Launcher
6. Input the address and port for the MultiWorld Server
7. Click **Connect**
8. Enter your slot name and which save file you're playing on when prompted
9. Once the connection status in the top left corner of your game turns green you can start playing

## Hosting a MultiWorld game
The recommended way to host a game is to use our hosting service. The process is relatively simple:

1. Collect config files from your players.
2. Create a zip file containing your players' config files.
3. Upload that zip file to the Generate page above.
   - Generate page: [WebHost Seed Generation Page](/generate)
4. Wait a moment while the seed is generated.
5. When the seed is generated, you will be redirected to a "Seed Info" page.
6. Click "Create New Room". This will take you to the server page. Provide the link to this page to your players, so they may download their patch files from there.
7. Note that a link to a MultiWorld Tracker is at the top of the room page. The tracker shows the progress of all players in the game. Any observers may also be given the link to this page.
8. Once all players have joined, you may begin playing.
