# Kingdom Hearts Archipelago Randomizer Setup Guide

## Required software

- KINGDOM HEARTS -HD 1.5+2.5 ReMIX- from the [Epic Games Store](https://store.epicgames.com/en-US/discover/kingdom-hearts) or [Steam](https://store.steampowered.com/app/2552430/KINGDOM_HEARTS_HD_1525_ReMIX/)

- The latest release of [OpenKH](https://github.com/OpenKH/OpenKh/releases/latest)

- The latest release of the [Kingdom Hearts 1FM Randomizer Software](https://github.com/gaithern/KH1FM-RANDOMIZER/releases/latest)

- The latest release of [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases/latest)

## Setting up the required software

- Before beginning, ensure that KH1 has been launched to the title screen at least once before.
- Verify game files via Steam/Epic; clean files are needed for the modding process to work.

### OpenKH

- Extract the OpenKH files to a directory within the same drive you have the game installed.
- Open `OpenKh.Tools.ModsManager.exe` within the OpenKH folder.
- When prompted for game edition, choose PC Release, select which platform you're using (EGS or Steam), navigate to your `Kingdom Hearts I.5 + II.5` installation folder in the path box and click `Next`.
- When prompted, install Panacea, then click `Next`.
- When prompted, check KH1 plus any other AP game you want to play, and click `Install and configure Lua backend`, then click `Next`.
- Extract the data for KH1.
- Click `Finish`

### Kingdom Hearts 1FM Randomizer Software

- Extract the Kingdom Hearts 1FM Randomizer Software files in a directory of your choosing.

## Obtaining and using the patch

- [Generate an Archipelago game](https://archipelago.gg/generate) using the KH1 yaml generated from the KH1 [options page](https://archipelago.gg/games/Kingdom%20Hearts/player-options). 
- When you generate a game you will see a download link for a KH1 .zip patch on the room page.
- After downloading this zip, open `mod_generator.exe` in your Kingdom Hearts 1FM Randomizer Software folder.
- Direct `mod_generator.exe` to both your patch zip and your KH1 data folder extracted during your OpenKH set up.
- Click `start`.
- After some time, you will find a file in your `Output` folder called `mod_YYYYMMDDHHMMSS.zip`
- Open `OpenKh.Tools.ModsManager.exe` and ensure that the dropdown in the top right is set to `Kingdom Hearts 1`
- Click the green plus, choose `Select and install Mod Archive or Lua Script`, and direct the prompt to your new mod zip.
- You should now see a mod on your list called `KH1 Randomizer Seed XYZ` where XYZ is your seed hex value.
- Ensure this mod is checked `[x]`.
- Click `Mod Loader` at the top, then click `Build and Run`.  Your modded game should now open.

## Connecting to your multiworld via the KH1 Client

- Once your game is being hosted, open `ArchipelagoLauncher.exe`.
- Find `KH1 Client` and open it.
- At the top, in the `Server:` bar, type in the host address and port.
- Click the `Connect` button in the top right.
- If connection to the server was successful, you'll be prompted to type in your slot named in the `Command:` bar at the bottom.
- After typing your slot name, press enter.
- If all is well, you are now connected.

## FAQ

### The client did not confirm connection to the game, is that normal?

Yes, the game and client communicate via a game communication path set up in your in your `%AppData%` folder, and therefore don't need to establish a socket connection.

### Why aren't the evidence boxes spawning in Wonderland?

You'll need to find `Footprints`, or a second `Wonderland`, in your multiworld.

### Why won't Phil let me start the Prelims?

You'll need to find `Entry Pass`, or a second `Olympus Colosseum`, in the multiworld.

### Why aren't the slides spawning in Deep Jungle?

You'll need to find `Slides`, or a second `Deep Jungle`, in the multiworld.

### Why can't I make progress in Atlantica?

You'll need to find `Crystal Trident`, or a second `Atlantica`, in the multiworld.

### Why won't the doctor let me progress in Halloween Town?

You'll need to find either `Forget-Me-Not` and/or `Jack-in-the-Box`, or a second `Halloween Town`, in the multiworld.

### Why is there a book missing in the Hollow Bastion library?

You'll need to find `Theon Vol. 6`, or a second `Hallow Bastion`, in the multiworld.

### How do I unlock End of the World?

Depending on your settings, your options are either finding a specified amount of `Lucky Emblems` or finding the item `End of the World`.

### How do I enter Destiny Islands?

After obtaining the item `Destiny Islands`, you can land there as an additional option in Traverse Town.

### How do I progress to Destiny Islands Day 2 and 3?

In order to access Day 2 and 3, you need to collect an amount of `Raft Materials` specified in your settings.  When you start Day 3, you'll be immediately warped to Homecoming (Final Bosses).

### Why can't I use the summon I obtained?

You need at least one magic spell before you can use summons.

## Troubleshooting

### Why am I not sending or receiving any items, despite being connected to the server?

Make sure you are using the KH1 Client and not the Text Client. You will need to open the client via the Archipelago Launcher.
If the correct client is being used, try reinstalling both Panacea and Lua Backend via the Setup Wizard under Settings.
Uncommonly, the folder `KH1FM` failed to generate within `%LocalAppData%`, and needs to be manually created. Alternately, the contents within `%LocalAppData%/KH1FM/` may need to be deleted.

### Why am I sending and/or receiving the wrong items?

Make sure you are using the correct seed zip and mod for your Archipelago game.<br>
It's also possible you are playing on a non-English language. Unfortunately, only English is supported.

### Why don't I have any worlds on the world map? Am I supposed to play through the Dive to the Heart?

If you have any of these symptoms: you find that the title screen does not have the Archipelago logo, that you had to do the entirety of Dive to the Heart, that you do not warp to the world map after choosing your Dream Weapons, or that when you get to the world map there are no worlds there;<br><br>

This is likely due to the mod not being applied properly. First, reinstall both Panacea and Lua Backend via the Setup Wizard under Settings. Second, make sure the seed mod is enabled [x]. Finally, ensure the game builds with no errors after selecting Build and Run under Mod Loader.

### Why did the game send checks that I had not collected?

The client caches your inventory and does not clear the cache when switching slots. The game also does something similar, even if backed out to the title screen. Therefore, it's highly encouraged, whenever switching slots or connecting to a different server, to always fully close both the game and the client first.

### Why is my seed missing important world progression items?

This is likely related to the Stacking World Items setting. When it is off, each world will have unique items that allow progression at some point in the world. When it is on, that item is replaced with a second world item.
Even when Stacking World Items is off, if Halloween Town Key Item Bundle is on then only the Forget-me-not is to be collected.
