# Banjo-Tooie

## Where is the options page?

The [player options page for this game](../player-options) contains all the options you need to configure and export a
config file.

## What does randomization do to this game?

- Randomize the majority of collectable items, unlockable moves, train stations & Chuffy
- If Chuffy is randomized, you can call Chuffy to any unlocked station without being required to defeat Old King Coal first
- Skip majority of cutscenes and dialog
- Option to skip the Tower of Tragedy Game Show
- Option to shorten long mini-games
- Option to randomize jamjar silo costs
- Option to customize world costs
- Option to skip Klungo 1 & 2
- Prison Code Door is always open
- Allows for instant transformation once Mumbo Skull or Humba Wigwam have been tagged by Banjo & Kazooie
- Option to customize the dialog character when receiving certain items
- Pause menu contains a new Archipelago Menu
- Options to randomize opening of worlds order and randomize world entrances
- Option to add nest to the list of locations. If it's active, all un-collected nests have the Archipelago logo as their texture
- Signpost can give out item hints if enabled
- Option to open backdoors:
    - MT -> TDL
    - MT -> HFP
    - GGM -> WW
    - WW -> TDL
    - HFP -> Clifftop
    - George is predropped to make HFP -> JRL more accessible
- Option to open GI frontdoor

## What items and locations can get shuffled?

- Jiggies
- Notes
- Empty Honeycombs
- Cheato Pages
- Jinjos
- Glowbos
- Moves from Jamjars, Roysten & Amaze-O-Gaze
- Doubloons
- Treble Clef
- Train Switches
- Chuffy
- Cheato Rewards
- Honey B Rewards
- Moves from Banjo-Kazooie
- T-Rex Roar
- Nests
- Traps
- Isle O' Hag Silos
- Warp Pads
- Big Top Tickets
- Targitzan's Green Relics
- Beans

## When the player receives an item, what happens?

When the player receives a collectable, the received a collectable will appear on screen. If you received a unlockable move, you will receive a dialog stating what move was obtained.

## Unique Local Commands

The following commands are available when using the Banjo-Tooie Client to play with Archipelago.

- `/n64` Check N64 Connection State
- `/deathlink` Enable/Disable Deathlink
- `/taglink` Enable/Disable Taglink
- `/autostart` Allows configuring a program to automatically start with the client. This allows you to, for example, automatically start Bizhawk with the patched ROM and lua Or the Everdrive connector. If already configured, disables the configuration.
- `/path` Reruns the ROM patcher
- `/rom_path (path)` Sets (or unsets) the file path of the vanilla ROM used for patching.
- `/patch_path (path)` Sets (or unsets) the folder path of where to save the patched ROM.
- `/program_args (path)` Sets (or unsets) the arguments to pass to the automatically run program. Defaults to passing the lua to Bizhawk.
