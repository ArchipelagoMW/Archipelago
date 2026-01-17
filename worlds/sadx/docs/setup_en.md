# Sonic Adventure DX Setup Guide

## Required Software

- Sonic Adventure DX (2004 version)
- SA Mod Manager from: [SA Mod Manager GameBanana Page](https://gamebanana.com/tools/15436)
- Archipelago Mod for Sonic Adventure DX
  from: [Sonic Adventure DX Classic Randomizer Mod Releases Page](https://github.com/ClassicSpeed/sadx-classic-randomizer/releases)

## Installation Procedures (Windows)

1. Install Sonic Adventure DX
   from: [Sonic Adventure DX Steam Store Page](https://store.steampowered.com/app/71250/Sonic_Adventure_DX/).
2. Install SA Mod Manager as per [its instructions in GameBanana](https://gamebanana.com/tools/15436).
3. Unpack the Archipelago Mod into the `/mods` directory in the folder into which you installed Sonic Adventure DX so
   that `/mods/SADX_Archipelago` is a valid path.
4. Launch the `SAModManager.exe` and make sure the SADX_Archipelago mod is listed and enabled. Make sure the mod is at
   the bottom of the list.
5. Disable the "Steam Achievements Mod" if enabled.
6. Disable the "Fixes, Adds, and Beta Restores" if enabled.

## Generating the player configuration

1. Download the sadx.apworld from the release page and double click it to install it and restart the Archipelago
   launcher.
2. On the AP Launcher click on `Generate Template Options`.
3. Copy the `Sonic Adventure DX.yaml` file from the `Players/Templates` folder and edit it to your liking.
4. Don't forget to remove the {number} from the `name` field, it should just be your nick and nothing else.

## Joining a MultiWorld Game

1. Before launching the game, run the `SAModManager.exe`, select the SADX_Archipelago mod, and hit the `Configure Mod`
   button.
2. For the `Server IP` field under `AP Settings`, enter the address of the server, such as archipelago.gg:54321. Your
   server host should be able to tell you this.
3. For the `PlayerName` field under `AP Settings`, enter your "name" field from the yaml or website config.
4. For the `Password` field under `AP Settings`, enter the server password if one exists, otherwise leave blank.
5. Click the `Save` button then hit `Save & Play` to launch the game.
6. Create a new save file to start playing! Use the same save file to continue playing.

## Using Universal Tracker

1. Download and install the
   latest [Universal Tracker](https://discord.com/channels/731205301247803413/1170094879142051912) version.
2. Make sure you have installed the sadx.apworld for the current version by double-clicking it.
3. Restart the Archipelago Launcher and open the Universal Tracker then connect with your server IP/port and slot name.
    - You don't need the yaml in your players folder for the tracker to work.

## Music Randomization

You can use music from SA2B, Sonic Heroes, or any extra custom songs you want.
Both the Steam version and the original 2004 disc version work with music randomization.

### SA2B Music

If SA2B and SADX are installed in the same Steam folder, you don't have to do anything.  
If not, or you want to copy the music manually, follow these steps:

1. In the mod manager, open the SADX_Archipelago mod settings. Under Music Shuffle Settings, change the SA2B songs path
   to `songs/ADX/`.
2. Download SA2B from Steam and find the folder where it is installed.
3. Go to `\Sonic Adventure 2\resource\gd_PC\` and copy the ADX folder.
4. Paste the ADX folder inside the `\Sonic Adventure DX\songs\` folder (create the `songs` folder if it doesn't exist).

### Sonic Heroes Music

If you want to use Sonic Heroes music, follow these steps:

1. Open your Sonic Heroes game folder.
2. Go to the `\bgm\` folder and copy every file.
3. Paste the ADX files into the `\Sonic Adventure DX\songs\custom\` folder (create the `songs\custom` folder if it
   doesn't exist).

### Extra Custom Music

This mod supports any custom music you want to add, as long as it is in the ADX format.
It's highly recommended that if you're going to add extra custom music, you change the path of the `songs.json` in the
mod settings (under Music Shuffle Settings) to `songs/`, for example, so you don't override your mappings when updating
the mod.

To add custom music, follow these steps:

1. Get the ADX files you want to add. You can get them from other games or convert them from other formats.
2. Move the ADX files to the `\Sonic Adventure DX\songs\custom\` folder (create the `songs\custom` folder if it doesn't
   exist).
3. Inside the mod folder, open the `songs.json` file to add the song at the end. You can copy entries from other Heroes
   songs.

The entry must have this format:

```json
{
  "myCustomSong": {
    "name": "My Custom Song",
    "type": "level"
  }
}
```

- The key name (`myCustomSong`) must match the name of your ADX file.
- The `name` field is the name of the song that will be displayed in the game.
- The `type` field determines how the song is shuffled when you shuffle by type:
    - The type can be `level`, `fight`, `theme`, `jingle`, `menu`, `adventurefield`, `event`, or `any`.
    - If the type is `jingle`, the song won't loop. Even in full randomization, jingles are randomized separately.
    - If the type is `any`, the song will be randomized with any other song type, except jingles.
- If you want to add these songs to the curated list of a level, you can do so by adding the song key to the
  `curatedCustom` property of that level.

- Additionally, if you don't want to modify the `songs.json` file, you can add custom music to the
  `\Sonic Adventure DX\songs\custom\` folder, and it will be automatically included in the randomizer. The file name
  will be
  used as the song name, and the type will default to `any`.

## Supported and recommended mods/tools

- The DC conversion mod is fully supported.
    - This includes every mod from the SA Mod Manager installer except for the "Steam Achievements Mod".
- Kell's Super Sonic mod. If playing with Chaos Emeralds, you can only transform after collecting all 7.
- Cream the Rabbit mod, every Tails check will work for her.
- If you want to import or export Chao, you can
  use [this tool](https://chao-island.com/downloads/pc-tools/chao-exporter-importer/).
    - Remember that by default, the chao save will be redirected to the `/mods/SADX_Archipelago/SAVEDATA` folder.

## Troubleshooting

- You get the SADX_Archipelago: DLL error - The specified module could not be found.
    - Make sure that the antivirus didn't delete the `/mods/SADX_Archipelago/sadx-classic-randomizer.dll` file.
- You get error: The code execution cannot proceeD because MSVCP140.dll was not found.
    - Install the .NET 8
      from [Microsoft's website](https://dotnet.microsoft.com/en-us/download/dotnet/thank-you/runtime-desktop-8.0.10-windows-x64-installer).
- The game closes when you press start.
    - This is a Steam input issue. Either run the game from Steam or adjust the "Desktop controller configuration" to
      just be a controller.
    - You can also simply close Steam.
- Some of the emblems don't give me checks.
    - Disable the "Steam Achievements Mod" if enabled.
- Some checks or elements of the randomizer are missing.
    - Disable the "Fixes, Adds, and Beta Restores" mod if enabled.
- Some enemies are not being tracked correctly with the indicator when playing with enemy-sanity.
    - Disable the "SADX:FE" mod if enabled.
- Failed to generate the world.
    - Try updating your Archipelago mod to the latest version (at least 0.5.0).
    - Try enabling more options in the yaml, being too restrictive will prevent the world from generating.
- While playing with Metal Sonic enabled, some checks aren't being sent correctly.
    - Disable the Metal Sonic code, this mod is not compatible with it.
- Music not being picked up:
    - Make sure the music files are in the correct format (ADX) and placed in the correct folder.
    - If it seems like the game is not using your custom music, you can enable the **Show Missing Song Warning** option
      in the mod settings to check.
      If a song is missing, a warning message will appear showing the filename of the missing track.
