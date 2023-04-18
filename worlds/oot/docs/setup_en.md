# Setup Guide for Ocarina of Time Archipelago

## Important

As we are using Bizhawk, this guide is only applicable to Windows and Linux systems.

## Required Software

- Bizhawk: [Bizhawk Releases from TASVideos](https://tasvideos.org/BizHawk/ReleaseHistory)
  - Version 2.3.1 and later are supported. Version 2.7 is recommended for stability.
  - Detailed installation instructions for Bizhawk can be found at the above link.
  - Windows users must run the prereq installer first, which can also be found at the above link.
- The built-in Archipelago client, which can be installed [here](https://github.com/ArchipelagoMW/Archipelago/releases)
  (select `Ocarina of Time Client` during installation).
- An Ocarina of Time v1.0 ROM.

## Configuring Bizhawk

Once Bizhawk has been installed, open Bizhawk and change the following settings:

- Go to Config > Customize. Switch to the Advanced tab, then switch the Lua Core from "NLua+KopiLua" to
  "Lua+LuaInterface". Then restart Bizhawk. This is required for the Lua script to function correctly.
  **NOTE: Even if "Lua+LuaInterface" is already selected, toggle between the two options and reselect it. Fresh installs** 
  **of newer versions of Bizhawk have a tendency to show "Lua+LuaInterface" as the default selected option but still load** 
  **"NLua+KopiLua" until this step is done.**
- Under Config > Customize > Advanced, make sure the box for AutoSaveRAM is checked, and click the 5s button.
  This reduces the possibility of losing save data in emulator crashes.
- Under Config > Customize, check the "Run in background" and "Accept background input" boxes. This will allow you to
  continue playing in the background, even if another window is selected.
- Under Config > Hotkeys, many hotkeys are listed, with many bound to common keys on the keyboard. You will likely want
  to disable most of these, which you can do quickly using `Esc`.
- If playing with a controller, when you bind controls, disable "P1 A Up", "P1 A Down", "P1 A Left", and "P1 A Right"
  as these interfere with aiming if bound. Set directional input using the Analog tab instead.
- Under N64 enable "Use Expansion Slot". This is required for savestates to work.
  (The N64 menu only appears after loading a ROM.)

It is strongly recommended to associate N64 rom extensions (\*.n64, \*.z64) to the Bizhawk we've just installed.
To do so, we simply have to search any N64 rom we happened to own, right click and select "Open with...", unfold
the list that appears and select the bottom option "Look for another application", then browse to the Bizhawk folder
and select EmuHawk.exe.

An alternative Bizhawk setup guide as well as various pieces of troubleshooting advice can be found
[here](https://wiki.ootrandomizer.com/index.php?title=Bizhawk).

## Configuring your YAML file

### What is a YAML file and why do I need one?

Your YAML file contains a set of configuration options which provide the generator with information about how it should
generate your game. Each player of a multiworld will provide their own YAML file. This setup allows each player to enjoy
an experience customized for their taste, and different players in the same multiworld can all have different options.

### Where do I get a YAML file?

A basic OoT yaml will look like this. There are lots of cosmetic options that have been removed for the sake of this
tutorial, if you want to see a complete list, download Archipelago from
the [Archipelago Releases Page](https://github.com/ArchipelagoMW/Archipelago/releases) and look for the sample file in
the "Players" folder.

```yaml
description: Default Ocarina of Time Template # Used to describe your yaml. Useful if you have multiple files
# Your name in-game. Spaces will be replaced with underscores and there is a 16 character limit
name: YourName
game:
  Ocarina of Time: 1
requires:
  version: 0.1.7 # Version of Archipelago required for this yaml to work as expected.
# Shared Options supported by all games:
accessibility:
  items: 0 # Guarantees you will be able to acquire all items, but you may not be able to access all locations
  locations: 50 # Guarantees you will be able to access all locations, and therefore all items
  none: 0 # Guarantees only that the game is beatable. You may not be able to access all locations or acquire all items
progression_balancing: # A system to reduce BK, as in times during which you can't do anything, by moving your items into an earlier access sphere
  0: 0 # Choose a lower number if you don't mind a longer multiworld, or can glitch/sequence break around missing items.
  25: 0
  50: 50 # Make it likely you have stuff to do.
  99: 0 # Get important items early, and stay at the front of the progression.
Ocarina of Time:
  logic_rules: # Set the logic used for the generator.
    glitchless: 50
    glitched: 0
    no_logic: 0
  logic_no_night_tokens_without_suns_song: # Nighttime skulltulas will logically require Sun's Song.
    false: 50
    true: 0
  open_forest: # Set the state of Kokiri Forest and the path to Deku Tree.
    open: 50
    closed_deku: 0
    closed: 0
  open_kakariko: # Set the state of the Kakariko Village gate.
    open: 50
    zelda: 0
    closed: 0
  open_door_of_time: # Open the Door of Time by default, without the Song of Time.
    false: 0
    true: 50
  zora_fountain: # Set the state of King Zora, blocking the way to Zora's Fountain.
    open: 0
    adult: 0
    closed: 50
  gerudo_fortress: # Set the requirements for access to Gerudo Fortress.
    normal: 0
    fast: 50
    open: 0
  bridge: # Set the requirements for the Rainbow Bridge.
    open: 0
    vanilla: 0
    stones: 0
    medallions: 50
    dungeons: 0
    tokens: 0
  trials: # Set the number of required trials in Ganon's Castle.
    # you can add additional values between minimum and maximum
    0: 50 # minimum value
    6: 0 # maximum value
    random: 0
    random-low: 0
    random-high: 0
  starting_age: # Choose which age Link will start as.
    child: 50
    adult: 0
  triforce_hunt: # Gather pieces of the Triforce scattered around the world to complete the game.
    false: 50
    true: 0
  triforce_goal: # Number of Triforce pieces required to complete the game. Total number placed determined by the Item Pool setting.
    # you can add additional values between minimum and maximum
    1: 0 # minimum value
    50: 0 # maximum value
    random: 0
    random-low: 0
    random-high: 0
    20: 50
  bombchus_in_logic: # Bombchus are properly considered in logic. The first found pack will have 20 chus; Kokiri Shop and Bazaar sell refills; bombchus open Bombchu Bowling.
    false: 50
    true: 0
  bridge_stones: # Set the number of Spiritual Stones required for the rainbow bridge.
    # you can add additional values between minimum and maximum
    0: 0 # minimum value
    3: 50 # maximum value
    random: 0
    random-low: 0
    random-high: 0
  bridge_medallions: # Set the number of medallions required for the rainbow bridge.
    # you can add additional values between minimum and maximum
    0: 0 # minimum value
    6: 50 # maximum value
    random: 0
    random-low: 0
    random-high: 0
  bridge_rewards: # Set the number of dungeon rewards required for the rainbow bridge.
    # you can add additional values between minimum and maximum
    0: 0 # minimum value
    9: 50 # maximum value
    random: 0
    random-low: 0
    random-high: 0
  bridge_tokens: # Set the number of Gold Skulltula Tokens required for the rainbow bridge.
    # you can add additional values between minimum and maximum
    0: 0 # minimum value
    100: 50 # maximum value
    random: 0
    random-low: 0
    random-high: 0
  shuffle_mapcompass: # Control where to shuffle dungeon maps and compasses.
    remove: 0
    startwith: 50
    vanilla: 0
    dungeon: 0
    overworld: 0
    any_dungeon: 0
    keysanity: 0
  shuffle_smallkeys: # Control where to shuffle dungeon small keys.
    remove: 0
    vanilla: 0
    dungeon: 50
    overworld: 0
    any_dungeon: 0
    keysanity: 0
  shuffle_hideoutkeys: # Control where to shuffle the Gerudo Fortress small keys.
    vanilla: 50
    overworld: 0
    any_dungeon: 0
    keysanity: 0
  shuffle_bosskeys: # Control where to shuffle boss keys, except the Ganon's Castle Boss Key.
    remove: 0
    vanilla: 0
    dungeon: 50
    overworld: 0
    any_dungeon: 0
    keysanity: 0
  shuffle_ganon_bosskey: # Control where to shuffle the Ganon's Castle Boss Key.
    remove: 50
    vanilla: 0
    dungeon: 0
    overworld: 0
    any_dungeon: 0
    keysanity: 0
    on_lacs: 0
  enhance_map_compass: # Map tells if a dungeon is vanilla or MQ. Compass tells what the dungeon reward is.
    false: 50
    true: 0
  lacs_condition: # Set the requirements for the Light Arrow Cutscene in the Temple of Time.
    vanilla: 50
    stones: 0
    medallions: 0
    dungeons: 0
    tokens: 0
  lacs_stones: # Set the number of Spiritual Stones required for LACS.
    # you can add additional values between minimum and maximum
    0: 0 # minimum value
    3: 50 # maximum value
    random: 0
    random-low: 0
    random-high: 0
  lacs_medallions: # Set the number of medallions required for LACS.
    # you can add additional values between minimum and maximum
    0: 0 # minimum value
    6: 50 # maximum value
    random: 0
    random-low: 0
    random-high: 0
  lacs_rewards: # Set the number of dungeon rewards required for LACS.
    # you can add additional values between minimum and maximum
    0: 0 # minimum value
    9: 50 # maximum value
    random: 0
    random-low: 0
    random-high: 0
  lacs_tokens: # Set the number of Gold Skulltula Tokens required for LACS.
    # you can add additional values between minimum and maximum
    0: 0 # minimum value
    100: 50 # maximum value
    random: 0
    random-low: 0
    random-high: 0
  shuffle_song_items: # Set where songs can appear.
    song: 50
    dungeon: 0
    any: 0
  shopsanity: # Randomizes shop contents. Set to "off" to not shuffle shops; "0" shuffles shops but does not allow multiworld items in shops.
    0: 0
    1: 0
    2: 0
    3: 0
    4: 0
    random_value: 0
    off: 50
  tokensanity: # Token rewards from Gold Skulltulas are shuffled into the pool.
    off: 50
    dungeons: 0
    overworld: 0
    all: 0
  shuffle_scrubs: # Shuffle the items sold by Business Scrubs, and set the prices.
    off: 50
    low: 0
    regular: 0
    random_prices: 0
  shuffle_cows: # Cows give items when Epona's Song is played.
    false: 50
    true: 0
  shuffle_kokiri_sword: # Shuffle Kokiri Sword into the item pool.
    false: 50
    true: 0
  shuffle_ocarinas: # Shuffle the Fairy Ocarina and Ocarina of Time into the item pool.
    false: 50
    true: 0
  shuffle_weird_egg: # Shuffle the Weird Egg from Malon at Hyrule Castle.
    false: 50
    true: 0
  shuffle_gerudo_card: # Shuffle the Gerudo Membership Card into the item pool.
    false: 50
    true: 0
  shuffle_beans: # Adds a pack of 10 beans to the item pool and changes the bean salesman to sell one item for 60 rupees.
    false: 50
    true: 0
  shuffle_medigoron_carpet_salesman: # Shuffle the items sold by Medigoron and the Haunted Wasteland Carpet Salesman.
    false: 50
    true: 0
  skip_child_zelda: # Game starts with Zelda's Letter, the item at Zelda's Lullaby, and the relevant events already completed.
    false: 50
    true: 0
  no_escape_sequence: # Skips the tower collapse sequence between the Ganondorf and Ganon fights.
    false: 0
    true: 50
  no_guard_stealth: # The crawlspace into Hyrule Castle skips straight to Zelda.
    false: 0
    true: 50
  no_epona_race: # Epona can always be summoned with Epona's Song.
    false: 0
    true: 50
  skip_some_minigame_phases: # Dampe Race and Horseback Archery give both rewards if the second condition is met on the first attempt.
    false: 0
    true: 50
  complete_mask_quest: # All masks are immediately available to borrow from the Happy Mask Shop.
    false: 50
    true: 0
  useful_cutscenes: # Reenables the Poe cutscene in Forest Temple, Darunia in Fire Temple, and Twinrova introduction. Mostly useful for glitched.
    false: 50
    true: 0
  fast_chests: # All chest animations are fast. If disabled, major items have a slow animation.
    false: 0
    true: 50
  free_scarecrow: # Pulling out the ocarina near a scarecrow spot spawns Pierre without needing the song.
    false: 50
    true: 0
  fast_bunny_hood: # Bunny Hood lets you move 1.5x faster like in Majora's Mask.
    false: 50
    true: 0
  chicken_count: # Controls the number of Cuccos for Anju to give an item as child.
    \# you can add additional values between minimum and maximum
    0: 0 # minimum value
    7: 50 # maximum value
    random: 0
    random-low: 0
    random-high: 0
  hints: # Gossip Stones can give hints about item locations.
    none: 0
    mask: 0
    agony: 0
    always: 50
  hint_dist: # Choose the hint distribution to use. Affects the frequency of strong hints, which items are always hinted, etc.
    balanced: 50
    ddr: 0
    league: 0
    mw2: 0
    scrubs: 0
    strong: 0
    tournament: 0
    useless: 0
    very_strong: 0
  text_shuffle: # Randomizes text in the game for comedic effect.
    none: 50
    except_hints: 0
    complete: 0
  damage_multiplier: # Controls the amount of damage Link takes.
    half: 0
    normal: 50
    double: 0
    quadruple: 0
    ohko: 0
  no_collectible_hearts: # Hearts will not drop from enemies or objects.
    false: 50
    true: 0
  starting_tod: # Change the starting time of day.
    default: 50
    sunrise: 0
    morning: 0
    noon: 0
    afternoon: 0
    sunset: 0
    evening: 0
    midnight: 0
    witching_hour: 0
  start_with_consumables: # Start the game with full Deku Sticks and Deku Nuts.
    false: 50
    true: 0
  start_with_rupees: # Start with a full wallet. Wallet upgrades will also fill your wallet.
    false: 50
    true: 0
  item_pool_value: # Changes the number of items available in the game.
    plentiful: 0
    balanced: 50
    scarce: 0
    minimal: 0
  junk_ice_traps: # Adds ice traps to the item pool.
    off: 0
    normal: 50
    on: 0
    mayhem: 0
    onslaught: 0
  ice_trap_appearance: # Changes the appearance of ice traps as freestanding items.
    major_only: 50
    junk_only: 0
    anything: 0
  logic_earliest_adult_trade: # Earliest item that can appear in the adult trade sequence.
    pocket_egg: 0
    pocket_cucco: 0
    cojiro: 0
    odd_mushroom: 0
    poachers_saw: 0
    broken_sword: 0
    prescription: 50
    eyeball_frog: 0
    eyedrops: 0
    claim_check: 0
  logic_latest_adult_trade: # Latest item that can appear in the adult trade sequence.
    pocket_egg: 0
    pocket_cucco: 0
    cojiro: 0
    odd_mushroom: 0
    poachers_saw: 0
    broken_sword: 0
    prescription: 0
    eyeball_frog: 0
    eyedrops: 0
    claim_check: 50

```

## Joining a MultiWorld Game

### Obtain your OOT patch file

When you join a multiworld game, you will be asked to provide your YAML file to whoever is hosting. Once that is done,
the host will provide you with either a link to download your data file, or with a zip file containing everyone's data
files. Your data file should have a `.apz5` extension.

Double-click on your `.apz5` file to start your client and start the ROM patch process. Once the process is finished
(this can take a while), the client and the emulator will be started automatically (if you associated the extension
to the emulator as recommended).

### Connect to the Multiserver

Once both the client and the emulator are started, you must connect them. Within the emulator click on the "Tools"
menu and select "Lua Console". Click the folder button or press Ctrl+O to open a Lua script.

Navigate to your Archipelago install folder and open `data/lua/connector_oot.lua`.

To connect the client to the multiserver simply put `<address>:<port>` on the textfield on top and press enter (if the
server uses password, type in the bottom textfield `/connect <address>:<port> [password]`)

Now you are ready to start your adventure in Hyrule.
