# Muse Dash Randomizer Setup Guide

## Quick Links
- [Main Page](../../../../games/Muse%20Dash/info/en)
- [Settings Page](../../../../games/Muse%20Dash/player-settings)

## Required Software

- Windows 8 or Newer.
- Muse Dash: [Available on Steam](https://store.steampowered.com/app/774171/Muse_Dash/)
  - \[Optional\] [Muse Plus] DLC: [Also Available on Steam](https://store.steampowered.com/app/2593750/Muse_Dash__Muse_Plus/)
- Melon Loader: [GitHub](https://github.com/LavaGang/MelonLoader/releases/latest)
  - .Net Framework 4.8 may be needed for the installer: [Download](https://dotnet.microsoft.com/en-us/download/dotnet-framework/net48)
- .NET Desktop Runtime 6.0.XX (If not already installed): [Download](https://dotnet.microsoft.com/en-us/download/dotnet/6.0)
- Muse Dash Archipelago Mod: [GitHub](https://github.com/DeamonHunter/ArchipelagoMuseDash/releases/latest)

## Installing the Archipelago mod to Muse Dash

1. Download [MelonLoader.Installer.exe](https://github.com/LavaGang/MelonLoader/releases/latest) and run it.
2. Choose the automated tab, click the select button and browse to `MuseDash.exe`. Then click install.
  - You can find the folder in steam by finding the game in your library, right clicking it and choosing *Manage→Browse Local Files*.
  - If you click the bar at the top telling you your current folder, this will give you a path you can copy. If you paste that into the window popped up by **MelonLoader**, it will automatically go to the same folder.
3. Run the game once, and wait until you get to the Muse Dash start screen before exiting.
4. Download the latest [Muse Dash Archipelago Mod](https://github.com/DeamonHunter/ArchipelagoMuseDash/releases/latest) and then extract that into the newly created `/Mods/` folder in MuseDash's install location.
  - All files must be under the `/Mods/` folder and not within a sub folder inside of `/Mods/`

If you've successfully installed everything, a button will appear in the bottom right which will allow you to log into an Archipelago server.

## Generating a MultiWorld Game
1. Visit the [Player Settings](/games/Muse%20Dash/player-settings) page and configure the game-specific settings to your taste.
2. Export your yaml file and use it to generate a new randomized game
  - (For instructions on how to generate an Archipelago game, refer to the [Archipelago Web Guide](/tutorial/Archipelago/setup/en))

## Joining a MultiWorld Game

1. Launch Muse Dash and get past the intro screen. Click on the button in the bottom right.
2. Enter in the details for the archipelago game, such as the server address with port (e.g. archipelago.gg:38381), username and password.
3. If entered correctly, the pop-up should disappear and the usual main menu will show. When entering the song select, you should see a limited number of songs.

## Troubleshooting

### No Support Module Loaded

This error occurs when Melon Loader cannot find needed files in order to run mods. There are generally two main sources of this error: a failure to generate the files when the game was first run with Melon Loader, or by a virus scanner is removing the files after generation.

To fix this, first you should remove Melon Loader from Muse Dash. You can do this by deleting the Melon Loader folder within Muse Dash's folder. Afterwards you can follow the installation steps again.

If you continue to run into issues, and are using a virus scanner, you may want to either temporarily turn it off when first running Muse Dash, or whitelist the Muse Dash folder.