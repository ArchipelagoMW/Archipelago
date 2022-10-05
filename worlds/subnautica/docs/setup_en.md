# Subnautica Randomizer Setup Guide

## Required Software

- Subnautica from: [Subnautica Steam Store Page](https://store.steampowered.com/app/264710/Subnautica/)
- QModManager4 from: [QModManager4 Nexus Mods Page](https://www.nexusmods.com/subnautica/mods/201)
- Archipelago Mod for Subnautica
  from: [Subnautica Archipelago Mod Releases Page](https://github.com/Berserker66/ArchipelagoSubnauticaModSrc/releases)

## Installation Procedure

1. Install QModManager4 as per its instructions.

2. The Subnautica game directory should now contain a `QMods` folder. Unpack the Archipelago Mod into this folder, so that `Subnautica/QMods/Archipelago/` is a valid path.

3. Start Subnautica. You should see a connect form with three text boxes in the top left of your main menu.

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
 - `silent` toggles Archipelago chat messages appearing.
 - `deathlink` toggles death link.

To enable the console in Subnautica, press `F3` and `F8`, then uncheck "Disable Console" in the top left. Press `F3` and `F8` again to close the menus.
To enter a console command, press `Enter`.

## Known Issues

- Do not attempt playing vanilla saves while the mod is installed, as the mod will override the scan information of the savegame.
- When exiting to the main menu the mod's state is not properly reset. Loading a savegame from here will break various things.
  If you want to reload a save it is recommended you restart the game entirely.
- Attempting to load a savegame containing no longer valid connection information without entering valid information on the main menu will hang on the loading screen.

## Troubleshooting

If you don't see the connect form on the main menu screen, check whether you see a file named `qmodmanager_log-Subnautica.txt` in the Subnautica game directory. If not,
QModManager4 is not correctly installed, otherwise open it and look for `Loading [Archipelago`. If the file doesn't contain this text, then
QModManager4 didn't find the Archipelago mod, so check your paths.
