# Terraria for Archipelago Setup Guide

## Required Software

Download and install [Terraria](https://store.steampowered.com/app/105600/Terraria/)
and [tModLoader](https://store.steampowered.com/app/1281930/tModLoader/) on Steam

## Installing the Archipelago Mod

1. Subscribe to [the mod](https://steamcommunity.com/sharedfiles/filedetails/?id=2922217554) on Steam
2. Open tModLoader
3. Go to **Workshop -> Manage Mods** and enable the Archipelago mod
4. tModLoader will say that it needs to refresh; exit this menu, and it will do this automatically
5. Once tModLoader finishes loading, the Archipelago mod is finished installing; you can now 
[connect to an Archipelago game](#joining-an-archipelago-game-in-terraria).

This mod might not work with mods that significantly alter progression or vanilla features. It is
highly recommended to use utility mods and features to speed up gameplay, such as:

- Journey Mode
- Ore Excavator
- Magic Storage
- Alchemist NPC Lite
    - (Can be used to break progression)
- Reduced Grinding
- Upgraded Research
    - (WARNING: Do not use without Journey mode)
    - (NOTE: If items you pick up aren't showing up in your inventory, check your research menu. This mod automatically researches certain items.)

## Configuring your YAML File

### What is a YAML and why do I need one?

The [basic multiworld setup guide](/tutorial/Archipelago/setup/en) can be found on Archipelago's website. Among other things, it explains what .yaml 
files are, and how they are used.

### Where do I get a YAML?

You can use the [game options page for Terraria](/games/Terraria/player-options) here
on the Archipelago website to generate a YAML using a graphical interface.

## Joining an Archipelago Game in Terraria

1. Launch tModLoader
2. In **Workshop > Manage Mods**, edit Archipelago Randomizer's settings
    - **Name** should be the player name you set when creating your YAML file.
    - **Port** should be the port number associated with the Archipelago server. It will be a 4 or 5-digit number.
    - If you're not hosting your game on the Archipelago website, change **Address** to the server's URL or IP address
3. Create a new character and world as normal (or use an existing one if you prefer). Terraria usually becomes 
significantly more difficult with this mod, so it is recommended to choose a lower difficulty than you normally would
play on.
4. Open the world in single player or multiplayer.
5. When you're ready, open chat, and enter `/apstart` to start the game.
   
## Commands

While playing Archipelago, you can interact with the server using the commands listed in the
[commands guide](/tutorial/Archipelago/commands/en). To send a command, open chat, and enter `/ap`,
followed by the command you want to send. For example, `/ap !help`.
