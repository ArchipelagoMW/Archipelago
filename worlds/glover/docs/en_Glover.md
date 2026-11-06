# Glover

## Where is the options page?

The [player options page (todo)](../player-options) for Glover contains all the options you need to create a config file.

## What does randomization do to Glover?

- Randomizes your moves, potion access, and ball transformations. Starts you with Crystal by default, but allows you to change your starting ball.
- Skips the opening castle cinematic.
- Option to randomize levels to be in any hub and door.
- Option to randomize the checkpoint you spawn out of.
- Option to disable bonus levels.
- Option to put your jump in the item pool.
- Option to include Power Ball in the item pool.
- Option to include score as checks.
- Ability to choose a win condition.
- The Cheat Chicken can give hints. The hint types can be modified.
- Mr. Tip can both give checks and hints. The hint types can be modified.
- Puts a star above levels you've gotten all Garibs for without requiring you complete the level.
- Lots of Garib logic customization.
---
### What locations can get shuffled?
- Garibs
- All Garibs in Level
- Lives
- Potions
- Level Goals
- Checkpoints
- Switches
- Enemies
- Insects
- Mr. Tips
- Score
---
### What items can get shuffled?
- Garibs
- Lives
- Potion Use
- Instant Potion Effects
- Level Doors
- Level Star Marks
- Checkpoints
- Level Events (Atlantis 3's Waterwheel)
- Ball Transformations
- Glover's Moves
- Traps
---
## Garib Options

|Garib Order|Description|Example|
|-|-|-|
|<center>`Level Garibs`|<center>Disables Garibs as items and locations, as vanilla Glover.|<center>N/A|
|<center>`Garib Groups`|<center>Adds 300 groups of Garibs as items, sized anywhere from 1 to 16. Garib locations are sent when you collect all Garibs grouped nearby eachother.|<center>`Smg065 sent jjjj12212 10 Garibs`<br>`Cross-Stitch found their FoF2 4 Garibs`|
|<center>`Garibsanity`|<center>Adds all 1497 individual Garibs as items and locations.|<center>`Smg065 sent jjjj12212 Garib`<br>`Cross-Stitch found their FoF2 Garib`|


|Garib Sorting|Description|Example|
|-|-|-|
|<center>`By Level`|<center>Garibs are linked to the levels they originate from.|<center>`Smg065 sent jjjj12212 Crn2 Garib`<br>`Cross-Stitch found their Atl1 4 Garibs`|
|<center>`In Order`|<center>Garibs are put into a total pool, and assigned to levels based on your game's level order, starting with the level at Atlantis Hub's 1 Portal.|<center>Total Garibs: 52/1496<br>Atl1: 50/50<br>Atl2: 2/60|
|<center>`Random Order`|<center>Garibs are put into a total pool, and assigned to levels randomly.|<center>Total Garibs: 52/1496<br>Crn?: 20/20<br>OtW3: 32/80|

## Local Commands

The following commands are available when using the Glover Client to play Archipelago.
- `/n64` Check N64 Connection State
- `/deathlink` Enable/Disable Deathlink
- `/taglink` Enable/Disable Taglink
- `/traplink` Enable/Disable Traplink
-  `/debug` Turns Debug Mode on, giving Glover all moves, ball transformations, potions and the ability to give himself the Helicopter Spell by pressing right on the D-Pad.
- `/autostart` Allows configuring a program to automatically start with the client. This allows you to, for example, automatically start Bizhawk with the patched ROM and lua. If already configured, disables the configuration.
-   `/rom_path (path)` Sets (or unsets) the file path of the vanilla ROM used for patching.
-   `/patch_path (path)` Sets (or unsets) the folder path of where to save the patched ROM.
-   `/program_args (path)` Sets (or unsets) the arguments to pass to the automatically run program. Defaults to passing the lua to Bizhawk.
