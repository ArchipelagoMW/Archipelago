# Subnautica Randomizer Setup Guide

## Required Software

- Subnautica from: [Subnautica Steam Store Page](https://store.steampowered.com/app/264710/Subnautica/)
- QModManager4 from: [QModManager4 Nexus Mods Page](https://www.nexusmods.com/subnautica/mods/201)
- Archipelago Mod for Subnautica
  from: [Subnautica Archipelago Mod Releases Page](https://github.com/Berserker66/ArchipelagoSubnauticaModSrc/releases)

## Installation Procedures

1. Install QModManager4 as per its instructions.

2. The folder you installed QModManager4 into will now have a /QMods directory. It might appear after a start of
   Subnautica. You can also create this folder yourself.

3. Unpack the Archipelago Mod into this folder, so that Subnautica/QMods/Archipelago/ is a valid path.

4. Start Subnautica. You should see a Connect Menu in the topleft of your main Menu.

## Connecting

Using the Connect Menu in Subnautica's Main Menu you enter your connection info to connect to an Archipelago Multiworld.
Menu points:
 - Host: the full url that you're trying to connect to, such as `archipelago.gg:38281`.
 - PlayerName: your name in the multiworld. Can also be called Slot Name and is the name you entered when creating your settings.
 - Password: optional password, leave blank if no password was set.

After the connection is made, start a new game. You should start to see Archipelago chat messages to appear, such as a message announcing that you joined the multiworld.

## Resuming

When loading a savegame it will automatically attempt to resume the connection that was active when the savegame was made. 
If that connection information is no longer valid, such as if the server's IP and/or port has changed, the Connect Menu will reappear after loading. Use the Connect Menu before or after loading the savegame to connect to the new instance.

Warning: Currently it is not checked if this is the correct multiworld belonging to that savegame, please ensure that yourself beforehand.

## Troubleshooting

If you don't see the Connect Menu within the Main Menu, check that you see a file named `qmodmanager_log-Subnautica.txt` in the Subnautica game directory. If not,
QModManager4 is not correctly installed, otherwise open it and look
for `[Info   :   BepInEx] Loading [Archipelago`. If it doesn't show this, then
QModManager4 didn't find the Archipelago mod, so check your paths.
