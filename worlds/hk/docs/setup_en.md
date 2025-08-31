# Hollow Knight for Archipelago Setup Guide

## Required Software
* Download and unzip the Lumafly Mod Manager from the [Lumafly website](https://themulhima.github.io/Lumafly/).
* A legal copy of Hollow Knight.
    * Steam, Gog, and Xbox Game Pass versions of the game are supported.
    * Windows, Mac, and Linux (including Steam Deck) are supported.

## Installing the Archipelago Mod using Lumafly
1. Launch Lumafly and ensure it locates your Hollow Knight installation directory.
2. Install the Archipelago mods by doing either of the following:
    * Click one of the links below to allow Lumafly to install the mods. Lumafly will prompt for confirmation.
        * [Archipelago and dependencies only](https://themulhima.github.io/Lumafly/commands/download/?mods=Archipelago)
        * [Archipelago with rando essentials](https://themulhima.github.io/Lumafly/commands/download/?mods=Archipelago/Archipelago%20Map%20Mod/RecentItemsDisplay/DebugMod/RandoStats/Additional%20Timelines/CompassAlwaysOn/AdditionalMaps/)
          (includes Archipelago Map Mod, RecentItemsDisplay, DebugMod, RandoStats, AdditionalTimelines, CompassAlwaysOn,
          and AdditionalMaps).
    * Click the "Install" button near the "Archipelago" mod entry. If desired, also install "Archipelago Map Mod"
      to use as an in-game tracker.
3. Launch the game, you're all set!

### What to do if Lumafly fails to find your installation directory
1. Find the directory manually.
    * Xbox Game Pass:
        1. Enter the Xbox app and move your mouse over "Hollow Knight" on the left sidebar. 
        2. Click the three points then click "Manage".
        3. Go to the "Files" tab and select "Browse...". 
        4. Click "Hollow Knight", then "Content", then click the path bar and copy it.
    * Steam:
        1. You likely put your Steam library in a non-standard place. If this is the case, you probably know where 
           it is. Find your steam library and then find the Hollow Knight folder and copy the path.
            * Windows - `C:\Program Files (x86)\Steam\steamapps\common\Hollow Knight`
            * Linux/Steam Deck - ~/.local/share/Steam/steamapps/common/Hollow Knight
            * Mac - ~/Library/Application Support/Steam/steamapps/common/Hollow Knight/hollow_knight.app
2. Run Lumafly as an administrator and, when it asks you for the path, paste the path you copied.

## Configuring your YAML File
### What is a YAML and why do I need one?
An YAML file is the way that you provide your player options to Archipelago.
See the [basic multiworld setup guide](/tutorial/Archipelago/setup/en) here on the Archipelago website to learn more.

### Where do I get a YAML?
You can use the [game options page for Hollow Knight](/games/Hollow%20Knight/player-options) here on the Archipelago 
website to generate a YAML using a graphical interface.

### Joining an Archipelago Game in Hollow Knight
1. Start the game after installing all necessary mods.
2. Create a **new save game.**
3. Select the **Archipelago** game mode from the mode selection screen.
4. Enter the correct settings for your Archipelago server.
5. Hit **Start** to begin the game. The game will stall for a few seconds while it does all item placements.
6. The game will immediately drop you into the randomized game. 
    * If you are waiting for a countdown then wait for it to lapse before hitting Start.
    * Or hit Start then pause the game once you're in it.

## Hints and other commands
While playing in a multiworld, you can interact with the server using various commands listed in the 
[commands guide](/tutorial/Archipelago/commands/en). You can use the Archipelago Text Client to do this,
which is included in the latest release of the [Archipelago software](https://github.com/ArchipelagoMW/Archipelago/releases/latest).
