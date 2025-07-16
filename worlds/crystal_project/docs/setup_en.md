# Crystal Project AP World Setup Guide

## What You Need

- Crystal Project Installer from the
  [Crystal Project AP World Releases Page](https://github.com/Emerassi/CrystalProjectAPWorld/releases)

- .Net 8.0 Desktop Runtime x64 (not the SDK, ASP.NET Core or generic Runtime!) is required to run the Crystal Project Archipelago Mod Installer: 
https://dotnet.microsoft.com/en-us/download/dotnet/8.0

## Recommended Installation Instructions

In your Steam library, right-click Crystal Project in the list and select "Properties...". Go to the Betas section, open the Beta Participation dropdown, and select the archipelago branch (version 1.6.5). 

Install .Net 8.0 x64 if you don't already have it.

Go to [Crystal Project AP World Releases Page](https://github.com/Emerassi/CrystalProjectAPWorld/releases).
Download the installer file, extract it, and run the executable. When prompted, choose your Crystal Project installation location.

## Switching Between Different Versions of Archipelago

Your save files for the unmodified game will not be visible inside the Archipelago version of the game and vice versa.
 The unmodified game and the AP version of the game store saves in different folders to prevent you from loading incompatible saves and getting errors.

If you want to switch back to unmodded Crystal Project:
 1. In your Steam library, right-click Crystal Project in the list and select "Properties...".
 1. In the Betas menu, select the branch that matches the save file you want to switch to (likely the release branch, a.k.a. None in the Beta Participation dropdown).

When you want to switch back to the Archipelago version of Crystal Project:
 1. Change back to the archipelago branch in Steam's Beta Participation menu.
 1. Run the installer for the version you want.

If you want to switch to a different version of Archipelago Crystal Project:
 1. In your Steam library, right-click Crystal Project in the list and select "Properties...".
 1. Go to the Installed Files section and select "Verify integrity of game files".
 1. Run the installer for the version of Crystal Project Archipelago you want to switch to.

## Configuring your YAML file

### What is a YAML file and why do I need one?

A YAML file lets you configure options for your randomizer game.
See [Archipelago Multiworld Setup Guide](https://archipelago.gg/tutorial/Archipelago/setup/en#generating-a-game) for a more in-depth explanation!

### Where do I get a YAML file?

Two YAML files are included on the [Crystal Project AP World Releases Page](https://github.com/Emerassi/CrystalProjectAPWorld/releases): a default YAML, and an Explorer preset that maximizes platforming and minimizes combat.

## Is there a tracker for this game?

### Yes!

But not a separate one. We have modified the base game to provide in-game tracking, including a full locations list, goal items tracker, world map icons, and minimap icons (with custom art to indicate accessibility and importance!) You can even bind the world map and locations list to hotkeys.

## Connect to the MultiServer

1. Start a new game in Crystal Project. An Archipelago connection screen will appear.
1. Fill out the hostname and port (archipelago.gg: #####), slot name, and password (if applicable). You can use your keyboard to type, or you can hit the Paste button on controller.
1. Hit the Connect button. You should now be connected!

Continue through the new game setup as normal - though it is not recommended to enable any of the base game's randomizer settings. (Some of them may still work, but some of them will break things lol).

### Can I use other Crystal Project mods?
Using other Crystal Project mods along with Archipelago is not yet fully supported. Apply them with caution! Mods newer than the Archipelago version (Editor version 30) will be incompatible.

The Use Mods YAML option adds items and locations from other Crystal Project mods to the item and location pools at generation.
WARNING: This option is very in beta right now! Enabling it is not recommended for: multiworlds that do not allow releasing items or with Regionsanity enabled (some mods add items to regions but don't place them anywhere near that region).

Multiworld host instructions for the Use Mods option:
1. In order to select the mods you'd like to include in randomization, make a folder named "crystal_project_mods" inside your root Archipelago directory.
1. Go to your Steam installation folder for Crystal Project (<YourSteamInstallFolder>/steamapps/workshop/content/1637730) and find the individual folders for the mods you'd like to include.
1. Inside each mod's folder is a mod json. Copy that json to the crystal_project_mods folder you made inside the Archipelago directory.
1. If you have a specific order you want to apply the mods, rename the jsons such that they are in alphabetical order in the order you want them to be applied. E.g. name the first mod a_modname, the second b_modname, etc.

NOTE: When the Use Mods option is on, all Crystal Project players in the multiworld with this option enabled MUST use the same mods.

The in-game tracking will use special icons for modded locations that will not display their accessibility (as we can only guess at how accessible they are based on coordinates, and would prefer the tracking to be as accurate as possible).

When disabled, only base game locations and items will be randomized. You can still use other mods - at your own risk, adventurer - they just won't add checks.

The game will warn you if you open a game with mods that don't match the mods used to generate the multiworld.

## Play the game

After you've successfully connected once, your save file will automatically reconnect to the multiworld the next time you open the game.
(Remember to refresh the multiworld room page if no one has connected in a while.) If the room number has changed, open the menu and select Archipelago from the sidebar to update your connection information and reconnect.

Set forth on adventure! Remember to touch any save points you come across so you can teleport to them from the world map.
