# Setup Guide for The Binding of Isaac: Repentance

## Required Software
- The Binding of Isaac: Rebirth including all DLC's up to Repentance
  - [Steam](https://store.steampowered.com/bundle/2405/The_Binding_of_Isaac_Rebirth_Complete_Bundle/)
- A save file where the paths to all the endgame bosses are unlocked
- The Archipelago of Isaac mod
  - ~~[Steam Workshop]()~~ (Comming soon)
  - [Github](https://github.com/NaveTK/the-archipelago-of-isaac/releases/tag/v0.1)

## Optional Software
- isaac-save-installer by Zamiell for a 100% completed save file
  - [Github](https://github.com/Zamiell/isaac-save-installer/)
- Universal Tracker
  - [Github](https://github.com/FarisTheAncient/Archipelago/blob/tracker/worlds/tracker/docs/setup.md)

## Installation Procedures
After installing *The Binding of Isaac: Rebirth* and its DLCs via Steam you have two options on how to install the mod:
- ~~Via Steam Workshop~~
  1. ~~Open the Steam Workshop page for the mod linked above~~
  2. ~~Click **Subscribe**~~  
     (Comming soon)
- Via Github
  1. Open the installation folder of The Binding of Isaac: Rebirth
     - (Can be found by right-clicking the game in your Steam Library and choosing *Manage -> Browse local files*)
  2. See if there is a folder called "**mods**", if not, create one
  3. Inside the mod folder, unpack the "*the archipelago of isaac.zip*" file
     - (The folder structure should be *mods/the archipelago if isaac/a bunch of files*)

Now navigate back to your Steam Library and right-click The Binding of Isaac: Rebirth again, this time choosing Properties. Then put `--luadebug` into launch options.

**Please Note**: Setting this launch option has security implications but is required for network capability. Please inform yourself about the security risk that comes with setting this option, only use mods you trust while having it enabled and remove it again, when you do not need it anymore. It is also recommended to manually install mods rather than using Steam Workshop with this option set, as attackers could gain control of a mod authors Steam profile and use the autoupdate feature to inject dangerous code.

## Create a Config (.yaml) File

### What is a config file and why do I need one?

See the guide on setting up a basic YAML at the Archipelago setup
guide: [Basic Multiworld Setup Guide](/tutorial/Archipelago/setup/en)

### Where do I get a config file?

The Player Options page on the website allows you to configure your personal options and export a config file from
them. Player options page: [The Binding of Isaac Repentance Player Options Page](/games/The%20Binding%20of%20Isaac%20Repentance/player-options)

### Verifying your config file

If you would like to validate your config file to make sure it works, you may do so on the YAML Validator page. YAML
validator page: [YAML Validation page](/check)

## Joining a MultiWorld Game
1. Open the game
2. Select a save file with a sufficient progression state
3. Ensure *The Archipelago of Isaac* is enabled in the mod menu
4. Start a run with any character
5. Press **F2** to open the connection settings
6. Input the address, port, password and slot name for the MultiWorld Server
7. Confirm and connect by pressing *Enter*
   - (If you're playing with a controller, the game might attempt to add a second player when you press *Enter*. In that case, connect with the default confirm button on your controller instead)
8. Once the connection status in the top left corner of your game turns green you can start playing

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
