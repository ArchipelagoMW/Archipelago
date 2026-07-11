# Kingdom Hearts Archipelago Randomizer Setup Guide

For the full, up-to-date setup guide with screenshots, see the
[Setup Guide](https://www.kh1fmrando.com/setup_guide) on kh1fmrando.com. The steps below cover the
Archipelago-specific parts of setup; kh1fmrando.com covers installing and configuring the required
software and applying your seed's mod.

## Required software

- KINGDOM HEARTS -HD 1.5+2.5 ReMIX- from the [Epic Games Store](https://store.epicgames.com/en-US/discover/kingdom-hearts) or [Steam](https://store.steampowered.com/app/2552430/KINGDOM_HEARTS_HD_1525_ReMIX/)

- The latest release of [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases/latest)

- The tools covered in the [Software Setup](https://www.kh1fmrando.com/software_setup) guide (OpenKH, Panacea, and the Lua Backend)

## Obtaining and using the patch

- [Generate an Archipelago game](https://archipelago.gg/generate) using the KH1 yaml generated from the KH1 [options page](https://archipelago.gg/games/Kingdom%20Hearts/player-options). 
- When you generate a game you will see a download link for a KH1 patch (.kh1rpatch) on the room page.
- Follow the [Installing the Mod](https://www.kh1fmrando.com/installing_the_mod) guide to apply this patch and launch your modded game.

## Connecting to your multiworld

For the latest information on connecting to a multiworld, check the
[Multiworld Guide](https://www.kh1fmrando.com/multiworld_guide) on kh1fmrando.com.

## FAQ

For questions about what unlocks a specific world, cup, or event (e.g. why the evidence boxes aren't
spawning in Wonderland, or why Phil won't let you start the Prelims), see the world-by-world
breakdown in the [Locations Guide](https://www.kh1fmrando.com/locations_guide) on kh1fmrando.com.

### How do I enter Destiny Islands?

After obtaining the item `Destiny Islands`, you can land there as an additional option in Traverse Town.

### Why can't I use the summon I obtained?

You need at least one magic spell before you can use summons.

## Troubleshooting

### Why am I not sending or receiving any items, despite being connected to the server?

Try reinstalling both Panacea and Lua Backend via the Setup Wizard under Settings.
Uncommonly, the folder `KH1FM` failed to generate within `%LocalAppData%`, and needs to be manually created. Alternately, the contents within `%LocalAppData%/KH1FM/` may need to be deleted.

### Why am I sending and/or receiving the wrong items?

Make sure you are using the correct seed zip and mod for your Archipelago game.<br>
It's also possible you are playing on a non-English language. Unfortunately, only English is supported.

### Why don't I have any worlds on the world map? Am I supposed to play through the Dive to the Heart?

If you have any of these symptoms: you find that the title screen does not have the Archipelago logo, that you had to do the entirety of Dive to the Heart, that you do not warp to the world map after choosing your Dream Weapons, or that when you get to the world map there are no worlds there;<br><br>

This is likely due to the mod not being applied properly. First, reinstall both Panacea and Lua Backend via the Setup Wizard under Settings. Second, make sure the seed mod is enabled [x]. Finally, ensure the game builds with no errors after selecting Build and Run under Mod Loader.

### Why did the game send checks that I had not collected?

The game caches your inventory and does not clear the cache when switching slots, even if backed out to the title screen. Therefore, it's highly encouraged, whenever switching slots or connecting to a different server, to always fully close the game first.

### Why is my seed missing important world progression items?

This is likely related to the Stacking World Items setting. When it is off, each world will have unique items that allow progression at some point in the world. When it is on, that item is replaced with a second world item.
Even when Stacking World Items is off, if Halloween Town Key Item Bundle is on then only the Forget-me-not is to be collected.
