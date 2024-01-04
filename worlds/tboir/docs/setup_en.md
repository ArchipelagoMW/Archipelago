# The Binding of Isaac: Repentance Setup Guide

## Required Software

- The Binding of Isaac: Rebirth including all DLCs up to Repentance
  - [The Binding of Isaac: Rebirth Complete Bundle](https://store.steampowered.com/bundle/2405/The_Binding_of_Isaac_Rebirth_Complete_Bundle/)
- Mod Config Menu Pure
  - [GitHub](https://github.com/Zamiell/isaac-mod-config-menu)
  - [Steam Workshop](https://steamcommunity.com/sharedfiles/filedetails/?id=2681875787)
- [The Binding of Isaac AP Mod](https://github.com/Cyb3RGER/TBoI-AP-Mod/releases)
- [isaac-save-insaller by Zamiell](https://github.com/Zamiell/isaac-save-installer) (optional for 100% save file)

## Installation Procedures

After installing *The Binding of Isaac: Rebirth* via Steam locate its installation folder by right-clicking it your
Steam Library and choosing *Manage* -> *Browse local files*. If it does not exist already create a folder named *mods*
inside the installation folder. Inside this folder unpack the *The Binding of Isaac AP Mod* zip file. If you download 
Mod Config Menu via GitHub/gitlab you will have to place the folder in zip file inside the *mods* folder. 
If you used SteamWorkshop for Mod Config Menu you don't need to place anything into the *mods* folder.

Now navigate back to your Steam Library and right-click *The Binding of Isaac: Rebirth* again, this time choosing 
*Properties...*. Then put ``--luadebug`` into launch options. 

**Please Note:** Setting this launch option has security implications but is required for network capability. Please 
inform yourself about the security risk that comes with setting this option, only use mods you trust while having it 
enabled and remove it again, when you do not need it anymore. It is also recommended to manually install mods rather 
than using Steam Workshop with this option set, as attackers could gain control of a mod authors Steam profile and use 
the autoupdate feature to inject dangerous code.


## Create a Config (.yaml) File

### What is a config file and why do I need one?

See the guide on setting up a basic YAML at the Archipelago setup
guide: [Basic Multiworld Setup Guide](/tutorial/Archipelago/setup/en)

### Where do I get a config file?

The Player Settings page on the website allows you to configure your personal settings and export a config file from
them. Player settings page: [The Binding of Isaac: Repentance Player Settings Page](/games/The%20Binding%20of%20Isaac%20Repentance/player-settings)

**NOTE:** For The Binding of Isaac: Repentance it is recommended to not use any special characters in your name since
you may not be able to input the name ingame. This can be worked around by modifying the games savefile and 
entering the name there. 

### Verifying your config file

If you would like to validate your config file to make sure it works, you may do so on the YAML Validator page. YAML
validator page: [YAML Validation page](/mysterycheck)

## Joining a MultiWorld Game

Open the game, select a save file and start a new run. Open the Mod Config Menu (the default key binding is ``L``) and 
navigate to *AP Integration* and set the appropriate ip, port, slot name and optionally password for your Archipelago 
server and slot and hit reconnect.

## Hosting a MultiWorld game

The recommended way to host a game is to use our hosting service. The process is relatively simple:

1. Collect config files from your players.
2. Create a zip file containing your players' config files.
3. Upload that zip file to the Generate page above.
    - Generate page: [WebHost Seed Generation Page](/generate)
4. Wait a moment while the seed is generated.
5. When the seed is generated, you will be redirected to a "Seed Info" page.
6. Click "Create New Room". This will take you to the server page. Provide the link to this page to your players, so
   they may download their patch files from there.
7. Note that a link to a MultiWorld Tracker is at the top of the room page. The tracker shows the progress of all
   players in the game. Any observers may also be given the link to this page.
8. Once all players have joined, you may begin playing.
