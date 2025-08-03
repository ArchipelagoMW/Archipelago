# Choo-Choo Charles MultiWorld Setup Guide
This page is a simplified guide of [the Choo-Choo Charles Multiworld Randomizer Mod Documentation](https://github.com/lgbarrere/CCCharles-Random?tab=readme-ov-file#cccharles-random).

## Requirements and Required Softwares
* A computer running Windows (the Mod is not handled by Linux or Mac)
* [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases)
* A legal copy of the Choo-Choo Charles original game (can be found on [Steam](https://store.steampowered.com/app/1766740/ChooChoo_Charles/))

## Mod Installation for playing
To install the Mod, open [the Choo-Choo Charles Multiworld Randomizer Mod page](https://github.com/lgbarrere/CCCharles-Random) and follow the steps below.

### Game Setup
The releases of this game are currently unofficial. However, the Mod can be installed and played by following these instructions :
1. Click the green "<> Code" button
2. Click "Download ZIP" and unzip the downloaded archive or clone this project
3. From this folder, in **Release/**, copy the **Obscure/** folder to **\<GameFolder\>** (where the **Obscure/** folder and **Obscure.exe** are placed)
4. Launch the game, if "OFFLINE" is written in the upper-right corner of the screen, the Mod is working
> [!NOTE]
> The content from the **Release/** folder can be manually placed while the paths to files are respected.

### Create a Config (.yaml) File
> [!NOTE]
> The purpose of a YAML file is described at [the Basic Multiworld Setup Guide](https://archipelago.gg/tutorial/Archipelago/setup/en#generating-a-game).

No option is currently taken into account by the Mod, this is a work in progress.

A default YAML should be used while the options are not implemented, it can be found :
* In the Release/ folder, downloaded in the **[Game Setup](https://github.com/lgbarrere/CCCharles-Random?tab=readme-ov-file#game-setup)** section
* In [the Choo-Choo Charles Multiworld Randomizer YAML page](https://github.com/lgbarrere/CCCharles-Random/blob/main/Release/CCCharles.yaml), by clicking the "Download raw file" icon

The player name configured by this default YAML is "CCCharles", it can be changed by renaming both the YAML and the "name" section inside of this YAML, **both must be identical**.

## Joining a MultiWorld Game
> [!NOTE]
> Before playing, it is highly recommended to check out the **[Known Issues](https://github.com/lgbarrere/CCCharles-Random?tab=readme-ov-file#known-issues)** section
* The game console must be opened to type Archipelago commands, press "F10" key or "`" (or "~") key in querty ("²" key in azerty)
* Type ``/connect <IP> <PlayerName>`` with \<IP\> and \<PlayerName\> found on the hosting Archipelago web page in the form ``archipelago.gg:XXXXX`` and ``CCCharles``
* Disconnection is automatic at game closure but can be manually done with ``/disconnect``

## Hosting a MultiWorld or Single-Player Game
See **[Game Setup](https://github.com/lgbarrere/CCCharles-Random#setup-the-game)** section to have the **Release/** folder downloaded.

In this section, **Archipelago/** refers to the path where [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases) is installed locally.

Follow these steps to host a remote multiplayer or a local single-player session :
1. Double-click the **cccharles.apworld** in **Release/** to automatically install the world randomization logic
2. Put the **CCCharles.yaml** from **Release/** to **Archipelago/Players/** with the YAML of each player to host
3. Launch the Archipelago launcher and click "Generate" to configure a game with the YAML in **Archipelago/output/**
4. For a multiplayer session, go to [the Archipelago HOST GAME page](https://archipelago.gg/uploads)
5. Click "Upload File" and select the generated **AP_\<seed\>.zip** in **Archipelago/output/**
6. Send the generated room page to each player
> [!TIP]
> For a local single-player session, click "Host" in the Archipelago launcher by using the generated **AP_\<seed\>.zip** in **Archipelago/output/**

## Known Issues
### Major issues
* If the player receives the **Box of Rockets**, the bunker at the **Training Explosive** region will be opened once loaded. It may be possible to break the mission state if the player interacts with elements in unexpected order.

### Minor issues
* The current version of the command parser does not accept console commands with a player names containing whitespaces. It is recommended to use underscores "_" instead, for instance : CCCharles_Player_1.
* Sometimes, an item reception or sending a location can fail (rare cases). Reloading the game is supposed to respawn all items on the ground and restarting a new game retrieves all unlocked items from Archipelago, that can be used as workarounds.
* When an egg is received, if the player goes to one of the three mine exits before talking to the NPC who gives its entry key, the player will no longer be able to interact with this NPC. Make sure to talk to them before approaching their respective mines. Restart a new game otherwise.
