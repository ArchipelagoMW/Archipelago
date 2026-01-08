# Setup Guide for Mario Kart: Double Dash!! Archipelago

## Requirements

You'll need the following components to be able to play MKDD AP:
* [Archipelago](https://archipelago.gg/tutorial/Archipelago/setup/en) 0.6.1 or newer
    * If you are new to Archipelago it is recommended to read the guide above.
* [Mario Kart Double Dash APWorld](https://github.com/aXu-AP/archipelago-double-dash/releases)
    * The apworld should install simply by double clicking it if you have Archipelago installed.
    * Alternatively, drop the apworld inside `custom_worlds` folder in your Archipelago installation (presumably `C:/ProgramData/Archipelago/custom_worlds`)
* [Dolphin Emulator](https://dolphin-emu.org/download/). **We recommend using the latest release.**
    * For Linux users, you can use the flatpak package
    [available on Flathub](https://flathub.org/apps/org.DolphinEmu.dolphin-emu).
* A rom of Mario Kart: Double Dash!! (NTSC-U / USA version)
    * Format (`.iso`, `.rvz`) doesn't matter.

Optionally, there's 2 options for tracking your progress:
* [PopTracker pack](https://github.com/Razerock/double-dash-ap-tracker/releases) by Raze
    * Requires [PopTracker](https://github.com/black-sliver/PopTracker/releases).
    * Shows available locations and obtained items with a nice interface.
    * Logic doesn't follow the difficulty modeling exactly, but is close enough.
* [Universal Tracker](https://github.com/FarisTheAncient/Archipelago/releases)
    * Text-based, shows a list of accessible locations.
    * If you have Universal Tracker installed, the client will have a tracker page automatically.
    * Might be better on single screen / small screen setups.
    * NOTE: Make sure you have up to date version of UT. Having old version installed prevents the client from launching!

## Setting Up a YAML

All players must provide the room host with a YAML file containing the settings for their world. Modify the template yaml from the [releases](https://github.com/aXu-AP/archipelago-double-dash/releases) page to your liking.
Once you're happy with your settings, provide the room host with your YAML file and proceed to the step "Connecting to a Room". If you want to play by yourself, you need to host the game yourself, see the next section.

## Self-hosting

* Place your YAML file in `Players` folder in your Archipelago installation (presumably `C:/ProgramData/Archipelago/Players`).
* Open Archipelago Launcher and click Generate. A console window should pop up, do its stuff and close shortly.
* Click Host and locate your generated seed named `AP_#######.zip` at `output` folder in your Archipelago installation (presumably `C:/ProgramData/Archipelago/output`).

## Connecting to a Room

Unlike most randomizers, MKDD AP doesn't need you to patch your rom beforehand. Everything is done at runtime.
Do note, that using the randomizer unlocks everything in your save of MKDD and you will probably make unrealistically good time trials times. So if you care for your vanilla save, you should do a backup of your save first!
* Open Mario Kart Double Dash Client from Archipelago Launcher.
* Open Dolphin and launch the game.
  * At this point, the client should say "Patch Applied".
  * **Important!** Do not go further than the title screen before you are connected to the host!
* Write your host connection info in the box at the top of the client (if you are hosting yourself it's `localhost`) and press enter.
* Write your slot/player name (if you didn't modify the YAML then it's `Player1`) into the box at the bottom and press enter.

## Playing the Game

You should now get checks whenever you finish races. To see what is currently unlocked, type `/unlocked` in the client. To see what checks you can do, use Tracker page located at the top of the client (if you installed Universal Tracker).

## Troubleshooting

* Client screen is black.
  * You probably have an out of date version of Universal Tracker. Update or remove `tracker.apworld`.
* The game crashes when I try to select a character.
  * You probably aren't connected to a server. Restart the game and ensure you have connection.
* I can't select character X.
  * The characters need to be unlocked by completing checks. The game currently doesn't give any visual indication what is unlocked, but you can use `/unlocked` command in the client to see your current status.
* The client doesn't register any checks.
  * Restart both the game and the client. Open the client before launching the game to apply the patch as early as possible.
* Where's my patch?
  * There's no patch, use vanilla rom.
* Can I use ar/gecko cheat codes?
  * Most of them should work.
  * If you find a cheat that doesn't work and you would like it to work, you can open an issue and we'll try to look into it.
* The client can't connect to Dolphin.
  * Make sure you are using USA version of MKDD.
  * Use Archipelago 0.6.1 or newer.
  * Try running the client with admin privileges.
  * As a last resort try resetting your settings (MAKE BACKUP FIRST - deleting `%appdata%/Dolphin Emulator` deletes your saves as well).
* On-screen notifications doesn't appear.
  * They don't appear in the title screen due to limitations posed by the patching system used.
  * If they don't appear in other screens, it might be a cache issue. Try making a savestate (shift + F1) and loading it (F1) to invalidate cache.
