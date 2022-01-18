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

## Troubleshooting

If you don't see the connect window check that you see a qmodmanager_log-Subnautica.txt in Subnautica, if not
QModManager4 is not correctly installed, otherwise open it and look
for `[Info   :   BepInEx] Loading [Archipelago 1.0.0.0]`, version number doesn't matter. If it doesn't show this, then
QModManager4 didn't find the Archipelago mod, so check your paths.

## Joining a MultiWorld Game

1. In Host, enter the address of the server, such as archipelago.gg:38281, your server host should be able to tell you
   this.

2. In Password enter the server password if one exists, otherwise leave blank.

3. In PlayerName enter your "name" field from the yaml, or website config.

4. Hit Connect. If it says successfully authenticated you can now create a new savegame or resume the correct savegame.