# Pokémon Crystal Setup Guide

## Required Software

- [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases)
- An English (UE) Pokémon Crystal v1.0 or v1.1 ROM. The Archipelago community cannot provide this.
    - A valid v1.1 ROM can be extracted from the 3DS eShop release of the game.
- One of the following:
    - [BizHawk](https://tasvideos.org/BizHawk/ReleaseHistory) 2.7 or later. 2.10 is recommended.
    - [mGBA](https://mgba.io) 0.10.3 or later.
        - You will also need
          the [mGBA to Bizhawk Client connector script](https://gist.github.com/gerbiljames/7b92dc62843794bd5902aad191b65efc).
          You should add it to `data/lua/` in your Archipelago install.

### Configuring BizHawk

Once you have installed BizHawk, open `EmuHawk.exe` and change the following settings:

- On BizHawk 2.8 or earlier, navigate to `Config -> Customize` and click on the Advanced tab. Change the Lua core
  from `NLua+KopiLua` to `Lua+LuaInterface`, then restart EmuHawk. This step is not required on BizHawk 2.9 or later.
- Under `Config -> Customize -> Advanced`, make sure the box for AutoSaveRAM is checked, and click the 5s button.
  This reduces the possibility of losing save data in emulator crashes.
- In `Config -> Customize`, enable `Run in background`. This will prevent the game from losing connection to the client
  when tabbed out.
- To adjust controller settings, open a Game Boy or Game Boy Color game (`.gb` or `.gbc`) and then navigate to
  `Config -> Controllers...`. This menu may not be available if a game is not already open.
- Ensure that `Config -> Preferred Cores -> GB in SGB` is disabled.

### Configuring mGBA

Once you have installed mGBA, open `mGBA`, navigate to Settings/Preferences, and change the following setting:

- In `Game Boy`, under Models, select `Game Boy Color (CGB)` for all models.

## Optional Software

[Pokémon Crystal AP Tracker](https://github.com/palex00/crystal-ap-tracker/releases/latest) for use
with [PopTracker](https://github.com/black-sliver/PopTracker/releases)

## Generating and Patching a Game

1. Add `pokemon_crystal.apworld` to your `custom_worlds` folder in your Archipelago install. It should not be in
   `lib\worlds`.
2. Create your options file (YAML). You can make one by choosing Generate Templates
   from the Archipelago Launcher. From there, you can edit the `.yaml` in any text editor.
3. Follow the general Archipelago instructions
   for [generating a game on your local installation](https://archipelago.gg/tutorial/Archipelago/setup/en#on-your-local-installation).
   This will generate an output file for you. Your patch file will have the `.apcrystal` file extension and will be
   inside the output file.
4. Open `ArchipelagoLauncher.exe`.
5. Select "Open Patch" on the left side and select your patch file.
6. If this is your first time patching, you will be prompted to locate your vanilla ROM.
7. A patched `.gbc` file will be created in the same place as the patch file.
8. On your first time opening a patch with BizHawk Client, you will also be asked to locate `EmuHawk.exe` in your
   BizHawk install. For mGBA users, you can select `Cancel` and manually open mGBA.

### Option Overrides

Pokemon Crystal has several options which do not affect Archipelago's logic, and as such can be changed after
generation without significantly changing the randomizer experience.

To do that, open the `host.yaml` file in your Archipelago folder and locate the `pokemon_crystal_settings` section.
In it, add an `option_overrides` setting like so:

```yaml
pokemon_crystal_settings:
  rom_file: "Pokemon - Crystal Version (UE) [C][!].gbc"
  option_overrides:
    # Enter your overrides here
```

You can then type in the options you would like to override as you would in a player YAML. Option weights and triggers
are supported.

The following options can always be overridden: `trainer_name`, `trainer_palette`, `game_options`,
`field_move_menu_order`, `default_pokedex_mode`, `shopsanity_restrict_rare_candies`, `reusable_tms`,
`minimum_catch_rate`, `skip_elite_four`, `better_marts`, `build_a_mart`, `experience_modifier`, `starting_money`.

You can change these settings at any time after patching the ROM and re-apply them by patching the ROM again. Your
save data will be preserved.

If you're playing a single-player seed, and you don't care about autotracking or hints, you can stop here, close the
client, and load the patched ROM in any emulator. However, for multiworlds and other Archipelago features, continue
below using BizHawk or mGBA as your emulator.

## Connecting to a Server

By default, opening a patch file will do steps 1-5 below for you automatically. Even so, keep them in your memory just
in case you have to close and reopen a window mid-game for some reason.

1. Pokémon Crystal uses Archipelago's BizHawk Client. If the client isn't still open from when you patched your game,
   you can re-open it from the launcher.
2. Ensure EmuHawk or mGBA is running the patched ROM.
3. In EmuHawk:
    - Go to `Tools > Lua Console`. This window must stay open while playing.
    - In the Lua Console window, go to `Script > Open Script...`.
    - Navigate to your Archipelago install folder and open `data/lua/connector_bizhawk_generic.lua`.
4. In mGBA:
    - Go to `Tools > Scripting...`. This window must stay open while playing.
    - Go to `File > Load Script...`.
    - Navigate to your Archipelago install folder and open `data/lua/connector_bizhawkclient_mgba.lua`.
5. The emulator and client will eventually connect to each other. The BizHawk Client window should indicate that it
   connected and recognized Pokémon Crystal.

You should now be able to receive and send items. You'll need to do these steps every time you want to reconnect. It is
perfectly safe to make progress offline; everything will re-sync when you reconnect.

## Auto-Tracking

Pokémon Crystal has a fully functional map tracker that supports auto-tracking.

1. Download [Pokémon Crystal AP Tracker](https://github.com/palex00/crystal-ap-tracker/releases/latest) and
   [PopTracker](https://github.com/black-sliver/PopTracker/releases).
2. Put the tracker pack into `packs/` in your PopTracker install.
3. Open PopTracker, and load the Pokémon Crystal pack.
4. For autotracking, click on the "AP" symbol at the top.
5. Enter the Archipelago server address (the one you connected your client to), slot name, and password. If you did not
   set a password for your room, leave that field empty. 
