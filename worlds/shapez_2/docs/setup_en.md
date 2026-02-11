# Setup guide for shapez 2 in Archipelago

## Required Software

- The shapez 2 game ([Steam](https://store.steampowered.com/app/2162800/shapez_2/))

## Optional Software

- Optional depending on multiworld details:
  - Archipelago from the [Archipelago Releases Page](https://github.com/ArchipelagoMW/Archipelago/releases)
    (Used for the manual-like client)
  - The 2hapezipelago mod from the Steam workshop (not available at the moment)
- Completely optional:
  - Universal Tracker (check UT's channel in the discord server for more information and instructions)

## Obtaining your scenario file

Once you have generated the multiworld, a `.zip` file will be generated for your world. If you generated locally, 
then it will be inside the multiworld's output `.zip` file. If hosted on the website (no matter if generated locally 
or on the website), there will be download link next to the name of your slot on the room page. Your world's `.zip` 
file will contain a `scenario_[...].json` file and a `preset_[...].json` file. Put those files into the
`custom-scenarios` and `custom-scenario-parameter-presets` subfolders (respectively) in the game's data folder. 
If you don't know where that is, then open the game, click `Play` (and **not** `Continue`!), click `Show folder` 
(which will open your file browser), and go one folder up.

## Playing your slot

If you generated a single shapez 2 world, then you can just start playing the custom scenario without further setup.
If there are multiple worlds in the generated multiworld, you will need to connect to the multiworld using the 
2hapezipelago mod. However, as of writing this setup page, the mod is unavailable due to the 1.0 update of shapez 2 
(and with it official modding support) not being released yet. So in order to still be able to play it, you'll need to 
use the manual-like client and ingame cheats.

### Sending locations using the manual-like client

Open the Archipelago Launcher and select `shapez 2 Client`. A client window that looks like the text client should then 
appear. Connect to the multiworld like you would do with the standard text client and switch to the various tabs. 
There you can click the milestone, task, or operator level you just completed in order to send the location check(s).
Do note that the client will show you more locations than you actually have in your world. Clicking them won't have any 
effect.

### Receiving items from other players without the mod

If you've found one of your own items in your game, then no further action is needed as the game already added it to 
your inventory automatically. If instead another player finds your item, then open the debug console by pressing `F1` 
on your keyboard, type in `cheats.enable`, and then type in `research.set [remote name] true`, where `[remote name]` is 
the internal name used for the item. [Here](remote_items.md) is a list of all items and their corresponding remote name.
However, do note that research points, blueprint points, and platform points **cannot be received (currently)** due to 
the limitations of custom scenarios.
