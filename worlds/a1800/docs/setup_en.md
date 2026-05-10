# Anno 1800 Randomizer Setup Guide

## Required Software

- Anno 1800, any one of
  - [Steam](https://store.steampowered.com/app/916440/Anno_1800/)
  - [Ubisoft Connect](https://store.ubisoft.com/us/anno-1800/5b647010ef3aa548048c5958.html?lang=en_US)
  - [Epic]((https://www.epicgames.com/store/en-US/product/anno-1800/home))
- Archipelago: [Archipelago Releases Page](https://github.com/ArchipelagoMW/Archipelago/releases)

## Optional Software

- None yet, but I'll create a poptracker pack eventually

## Overview

This guide walks you through installing the Anno 1800 Archipelago mod, configuring an Archipelago slot for Anno 1800,
and playing the game with an Anno 1800 client.

### Defining Some Terms

In Archipelago, multiple Anno 1800 worlds may be played simultaneously.
Each of these worlds must be connected to the Archipelago Server via the Archipelago mod.

This guide uses the following terms to refer to the software:

- **Archipelago Server** - The central Archipelago server, which connects all games to each other.
- **Archipelago Client** - The desktop application used by many Archipelago games as middleware. Accessed via the
  menu point `Anno 1800 Client` in the Archipelago Launcher.
- **Archipelago (Anno 1800) mod** - The Anno 1800 mod which implements Archipelago in-game functionality and
  connectivity. All Anno 1800 players must have this mod installed.
- **Anno 1800** - The Anno 1800 instance (game client) with which players play the actual game.

### What a Playable State Looks Like

- An Archipelago Server
- An Archipelago client, connected to both the Archipelago Server and a modded Anno 1800 instance
- One running modded Anno 1800 instance

## Preparing to Play Anno 1800 Archipelago

### Installing Anno 1800

Purchase and install Anno 1800 via one the sources linked [above](#required-software). DLCs are currently not supported.

Install Archipelago via the link [above](#required-software).

### Installing the Archipelago Mod

The host of the Archipelago multiworld should supply you with a zip file name `AP-%1-P%2-%3-%4.zip`, where `%1` is the
seed number, `%2` is the slot number, `%3` is the slot name and `%4` is the Archipelago version this mod was created by.

You can install the Anno 1800 mod in either of the following two locations:
- `<user folder>\Documents\Anno 1800\mods`
- `<game installation>\Anno 1800\mods`

To install the mod, extract the zip file and move or copy the resulting folder into one of the above locations. The
resulting folder structure should look like `mods\AP-%1-P%2-%3-%4\modinfo.json`.

If this worked, then Anno 1800 should display a gear next to the main menu point `Mod Browser`. If you hover over it,
it should display `[Gameplay] AP-%1-P%2-%3-%4` (might be cut off due to length).

### Installing Additional Mods

You can install additional mods by adding them to the same folder. Note that there may be compatibility issues if other
mods modify the game's unlocks. If other mods add new building unlocks, they will not be modified and work as usual.

## Running and Connecting the Game

Start the Archipelago Client. It will ask for the Anno 1800 mods folder. Point it to the folder you installed the mod to
[above](#installing-the-archipelago-mod). Then start a new Anno 1800 free play game or load into your existing savegame.
Be careful not to load into vanilla savegames or those from other modding setups as this mod will likely trigger some
irreversible unlocks. Once loaded into the savegame, the client should print that it is connected to the game within a
few seconds. The order in which you start the client and Anno 1800 does not matter.

Note: due to the way Anno 1800 simulates game ticks, the client will lose connection to the game when the game is
paused. This is not a problem and the client will reconnecting briefly after unpausing the game.

Now you can enter the server's ip and port and click `Connect` or type `/connect <ip>:<port>` in the client to connect
to the Archipelago server. This can only succeed after the client connected to Anno 1800 once.

It's also possible to play the game asynchronously without server or client. In this case, everything will be synced
once you connect the next time. If Anno 1800 is the only slot in the multiworld, you can even forgo the client and
server entirely and just locally play a randomized game - all unlocks will happen standalone.

## Hosting Your Own Anno 1800 Game

If you're hosting your own Anno 1800 game, you will need to configure and generate an Archipelago world.

### Create a Config (.yaml) File

#### What is a config file and why do I need one?

Your config file contains a set of configuration options which provide the generator with information about how it
should generate your game. Each player of a multiworld will provide their own config file. This setup allows each player
to enjoy an experience customized for their taste, and different players in the same multiworld can all have different
options.

#### Where do I get a config file?

Usually, the [Player Options](/games/Anno%201800/player-options) [dead link] page on the website would allow you to configure your
personal options and export them into a config file. However, this is a custom apworld, so either start your Achipelago
Launcher and select `Generate Template Options` to find a template yaml in your `Players` subfolder or use the one in
the download.

#### Verifying Your Config File

If you would like to validate your config file to make sure it works, you may do so on the
[Yaml Validation Page](https://archipelago.gg/check)<!--(/check)-->.

### Generating and Hosting the Multiworld

Generating a game and hosting an Archipelago server is explained in the
[Archipelago Setup Guide](https://archipelago.gg/tutorial/Archipelago/setup/en)<!--(/tutorial/Archipelago/setup/en)-->.

### Allowing Other People to Join Your Game

Additional players can join your game using the game's built-in multiplayer functionality if you start a multiplayer
session. Co-op play works as normal, but if you join as separate players, all unlocks will be shared - whoever reaches
unlocks an unlock first, triggers the location check and all players will receive all unlocks.

Have anyone you want to join follow the 
[Preparing to Play Anno 1800 Archipelago](#preparing-to-play-anno-1800-archipelago) section above. If you're using any
additional mods, all other players need to use the same mods as you.

However, only one player should to use the Archipelago client.

Note: multiplayer is as of yet untested.

## Frequently Asked Questions

### Does this work with Proton/Linux?

If you managed to get your Anno 1800 running under Linux, the mods folder in the user directory will be inside Anno
1800's wine prefix. Everything else should behave the same as under Windows. The Archipelago client will expect a Linux
path to your mods folder, which might be inside the same wine prefix. The file browser should work for selecting the
path correctly.

## Troubleshooting

No known frequent issues yet.
