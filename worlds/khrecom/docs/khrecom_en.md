# Kingdom Hearts RECOM Randomizer Setup Guide

##Setting up the required mods
1. Install OpenKH and the LUA Backend.

    Download the latest release of OpenKH here: https://github.com/OpenKH/OpenKh/releases/tag/latest
    
    Extract the files to a directory of your choosing.
    
    Open OpenKh.Tools.ModsManager.exe and run first time set up.
    
    When prompted for game edition, choose PC Release via Epic Games Store and navigate to your KH_1.5_2.5 in the path box and click "Next"
    
    When prompted, install Panacea, then click "Next"
    
    When prompted, check ReCoM plus any other AP game you play (KH2) and click "Install and configure LUA backend", then click "Next".
    
    Ensure that "Launch via Epic Games" is checked and click "Next"
    
    Extract game data for ReCoM and any other AP game you play (KH2), then click "Next".
    
    Click "Finish"
    
2. Open "OpenKh.Tools.ModsManager.exe"

3. Click the drop down menu at the top-right and choose "Re:Chain of Memories"

4. Click `Mods>Install a New Mod`

5. In "Add a new mod from GitHub" paste `gaithern/KH-RECOM-AP-LUA`

6. Click Install

7. Navigate to Mod Loader and click "Build Only"


## Configuring your YAML file

### What is a YAML file and why do I need one?

Your YAML file contains a set of configuration options which provide the generator with information about how it should
generate your game. Each player of a multiworld will provide their own YAML file. This setup allows each player to enjoy
an experience customized for their taste, and different players in the same multiworld can all have different options.

### Where do I get a YAML file?

you can customize your settings by visiting the [Kingdom Hearts RE Chain of Memories Settings Page](/games/Kingdom%20Hearts%20RE%20Chain%20of%20Memories/player-settings).

## Connect to the MultiServer

On the title screen, open your KHRECOM Client and connect to your MultiServer.
