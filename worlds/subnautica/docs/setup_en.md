# Subnautica Randomizer Setup Guide

## Required Software

- Subnautica from: [Subnautica Steam Store Page](https://store.steampowered.com/app/264710/Subnautica/) | [Subnautica Epic Game Store Page](https://store.epicgames.com/p/subnautica)
- Archipelago Mod for Subnautica
  from: [Subnautica Archipelago Mod Releases Page](https://github.com/Berserker66/ArchipelagoSubnauticaModSrc/releases)

## Installation Procedure

1. Unpack the Archipelago Mod into your Subnautica folder, so that `Subnautica/BepInEx` is a valid path.

2. Start Subnautica. You should see a connect form with three text boxes in the top left of your main menu.

**If using Linux,** add ``WINEDLLOVERRIDES="winhttp=n,b" %command%`` to your Subnautica launch arguments on Steam. If you bought Subnautica elsewhere, you can either add it as a non-steam game and use those launch arguments or use winecfg to set the dll override.

## Connecting

Use the connect form in Subnautica's main menu to enter your connection information to connect to an Archipelago multiworld.
Connection information consists of:
 - Host: the full url that you're trying to connect to, such as `archipelago.gg:38281`.
 - PlayerName: your name in the multiworld. Can also be called "slot name" and is the name you entered when creating your settings.
 - Password: optional password, leave blank if no password was set.

After the connection is made, start a new game. You should start to see Archipelago chat messages to appear, such as a message announcing that you joined the multiworld.

## Resuming

Savegames store their connection information and automatically attempt to reestablish the connection upon loading.
If the connection information is no longer valid, such as if the server's IP and/or port have changed,
you need to use the connect form on the main menu beforehand.

Warning: Currently it is not checked whether a loaded savegame belongs to the multiworld you are connecting to. Please ensure that yourself beforehand.

## Console Commands

The mod adds the following console commands:
 - `say` sends the text following it to Archipelago as a chat message.
   - For example, to use the [`!hint` command](/tutorial/Archipelago/commands/en#remote-commands), type `say !hint`.
 - `silent` toggles Archipelago messages appearing.
 - `tracker` rotates through the possible settings for the in-game tracker that displays the closest uncollected location.
 - `deathlink` toggles death link.

To enable the console in Subnautica, press `Shift+Enter`.

## Known Issues

- Do not attempt playing vanilla saves while the mod is installed, as the mod will override the scan information of the savegame.
- When exiting to the main menu the mod's state is not properly reset. Loading a savegame from here will break various things.
  If you want to reload a save it is recommended you relaunch the game entirely.
- Attempting to load a savegame containing no longer valid connection information without entering valid information on the main menu will hang on the loading screen.

## Troubleshooting

If you don't see the connect form on the main menu screen, check whether you see a file named `LogOutput.txt` in the Subnautica/BepInEx directory. 
If not, BepInEx is not correctly installed, otherwise open it and look for `Plugin Archipelago is loaded!`. 
If the file doesn't contain this text, then BepInEx didn't find the Archipelago mod, so check your paths.
