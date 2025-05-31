# Jak And Daxter (ArchipelaGOAL)

## FAQ
- [Where is the Options page?](#where-is-the-options-page)
- [What does randomization do to this game?](#what-does-randomization-do-to-this-game)
- [What are the Special Checks and how do I check them?](#what-are-the-special-checks-and-how-do-i-check-them)
- [What are the Special Items and what do they unlock?](#what-are-the-special-items-and-what-do-they-unlock)
- [How do I know which Special Items I have?](#how-do-i-know-which-special-items-i-have)
- [What is the goal of the game once randomized?](#what-is-the-goal-of-the-game-once-randomized)
- [What happens when I pick up or receive a Power Cell?](#what-happens-when-i-pick-up-or-receive-a-power-cell)
- [What happens when I pick up or receive a Scout Fly?](#what-happens-when-i-pick-up-or-receive-a-scout-fly)
- [How do I check the 'Free 7 Scout Flies' Power Cell?](#how-do-i-check-the-free-7-scout-flies-power-cell)
- [What does Death Link do?](#what-does-death-link-do)
- [What does Move Randomizer do?](#what-does-move-randomizer-do)
- [What are the movement options in Move Randomizer?](#what-are-the-movement-options-in-move-randomizer)
- [How do I know which moves I have?](#how-do-i-know-which-moves-i-have)
- [What does Orbsanity do?](#what-does-orbsanity-do)
- [What do Traps do?](#what-do-traps-do)
- [What kind of Traps are there?](#what-kind-of-traps-are-there)
- [I got soft-locked and cannot leave, how do I get out of here?](#i-got-soft-locked-and-cannot-leave-how-do-i-get-out-of-here)
- [How do I generate seeds with 1 Orb Orbsanity and other extreme options?](#how-do-i-generate-seeds-with-1-orb-orbsanity-and-other-extreme-options)
- [How do I check my player options in-game?](#how-do-i-check-my-player-options-in-game)
- [How does the HUD work?](#how-does-the-hud-work)
- [I think I found a bug, where should I report it?](#i-think-i-found-a-bug-where-should-i-report-it)

## Where is the options page

The [Player Options Page](../player-options) for this game contains all the options you need to configure and export 
a config file.

At this time, there are several caveats and restrictions:
- Power Cells and Scout Flies are **always** randomized.
- **All** the traders in the game become in-logic checks **if and only if** you have enough Orbs to pay all of them at once. 
    - This is to prevent hard locks, where an item required for progression is locked behind a trade you can't afford because you spent the orbs elsewhere.
    - By default, that total is 1530.

## What does randomization do to this game
The game now contains the following Location checks:
- All 101 Power Cells 
- All 112 Scout Flies
- All 14 Orb Caches (collect every orb in the cache and let it close)

These may contain Items for different games, as well as different Items from within Jak and Daxter. 
Additionally, several special checks and corresponding items have been added that are required to complete the game.

## What are the special checks and how do I check them
| Check Name             | How To Check                                                                 |
|------------------------|------------------------------------------------------------------------------|
| Fisherman's Boat       | Complete the fishing minigame in Forbidden Jungle                            |
| Jungle Elevator        | Collect the power cell at the top of the temple in Forbidden Jungle          |
| Blue Eco Switch        | Collect the power cell on the blue vent switch in Forbidden Jungle           |
| Flut Flut              | Push the egg off the cliff in Sentinel Beach and talk to the bird lady       |
| Warrior's Pontoons     | Talk to the Warrior in Rock Village once (you do NOT have to trade with him) |
| Snowy Mountain Gondola | Approach the gondola in Volcanic Crater                                      |
| Yellow Eco Switch      | Collect the power cell on the yellow vent switch in Snowy Mountain           |
| Snowy Fort Gate        | Ride the Flut Flut in Snowy Mountain and press the fort gate switch          |
| Freed The Blue Sage    | Free the Blue Sage in Gol and Maia's Citadel                                 | 
| Freed The Red Sage     | Free the Red Sage in Gol and Maia's Citadel                                  | 
| Freed The Yellow Sage  | Free the Yellow Sage in Gol and Maia's Citadel                               | 
| Freed The Green Sage   | Free the Green Sage in Gol and Maia's Citadel                                | 

## What are the special items and what do they unlock
| Item Name                                                                | What it Unlocks                                                                               |
|--------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------|
| Fisherman's Boat                                                         | Misty Island                                                                                  |
| Jungle Elevator                                                          | The blue vent switch inside the temple in Forbidden Jungle                                    |
| Blue Eco Switch                                                          | The plant boss inside the temple in Forbidden Jungle <br/> The cannon tower in Sentinel Beach |
| Flut Flut                                                                | The upper platforms in Boggy Swamp <br/> The fort gate switch in Snowy Mountain               |
| Warrior's Pontoons                                                       | Boggy Swamp and Mountain Pass                                                                 |
| Snowy Mountain Gondola                                                   | Snowy Mountain                                                                                |
| Yellow Eco Switch                                                        | The frozen box in Snowy Mountain <br/> The shortcut in Mountain Pass                          |
| Snowy Fort Gate                                                          | The fort in Snowy Mountain                                                                    |
| Freed The Blue Sage <br/> Freed The Red Sage <br/> Freed The Yellow Sage | The final staircase in Gol and Maia's Citadel                                                 |
| Freed The Green Sage                                                     | The final elevator in Gol and Maia's Citadel                                                  | 

## How do I know which special items I have
Open the game's menu, navigate to `Options`, then `Archipelago Options`, then `Item Tracker`.
This will show you a list of all the special items in the game, ones not normally tracked as power cells or scout flies.
Gray items indicate you do not possess that item, light blue items indicate you possess that item.

## What is the goal of the game once randomized
By default, to complete the game you must defeat the Gol and Maia and stop them from opening the Dark Eco silo. In order 
to reach them, you will need at least 72 Power Cells to cross the Lava Tube, as well as the four special items for 
freeing the Red, Blue, Yellow, and Green Sages.

Alternatively, you can choose from a handful of other completion conditions like defeating a particular boss, crossing
a particular connector level, or opening the 100 Power Cell door after defeating the final boss. You can also customize
the thresholds for connector levels and orb trades. These options allow you to tailor the expected length and difficulty
of your run as you see fit.

## What happens when I pick up or receive a power cell
When you pick up a power cell, Jak and Daxter will perform their victory animation. Your power cell count will 
NOT change. The pause menu will say "Task Completed" below the picked-up Power Cell. If your power cell was related 
to one of the special checks listed above, you will automatically check that location as well - a 2 for 1 deal!
Finally, your text client will inform you what you found and who it belongs to.

When you receive a power cell, your power cell count will tick up by 1. Gameplay will otherwise continue as normal. 
Finally, your text client will inform you where you received the power cell from.

## What happens when I pick up or receive a scout fly
When you pick up a scout fly, your scout fly count will NOT change. The pause menu will show you the number of
scout flies you picked up per-region, and this number will have ticked up by 1 for the region that scout fly belongs to. 
Finally, your text client will inform you what you found and who it belongs to.

When you receive a scout fly, your total scout fly count will tick up by 1. The pause menu will show you the number of
scout flies you received per-region, and this number will have ticked up by 1 for the region that scout fly belongs to. 
Finally, your text client will inform you where you received the scout fly from, and which one it is.

## How do I check the Free 7 Scout Flies power cell
You will automatically check this power cell when you _receive_ your 7th scout fly, NOT when you _pick up_ your 7th
scout fly. So in short:

- When you _pick up_ your 7th fly, the normal rules apply. 
- When you _receive_ your 7th fly, 2 things will happen in quick succession.
    - First, you will receive that scout fly, as normal.
    - Second, you will immediately complete the "Free 7 Scout Flies" check, which will send out another item.

## What does Death Link do
If you enable Death Link, all the other players in your Multiworld who also have it enabled will be linked by death. 
That means when Jak dies in your game, the players in with Death Link also die. Likewise, if any of the other 
players with Death Link die, Jak will also die in a random, possibly spectacular fashion.

You can turn off Death Link at any time in the game by opening the game's menu and navigating to `Options`, 
then `Archipelago Options`, then `Deathlink`.

## What does Move Randomizer do
If you enable Move Randomizer, most of Jak's movement set will be added to the randomized item pool, and you will need 
to receive the move in order to use it (i.e. you must find it, or another player must send it to you). Some moves have
prerequisite moves that you must also have in order to use them (e.g. Crouch Jump is dependent on Crouch). Jak will only
be able to run, swim (including underwater), perform single jumps, and shoot yellow eco from his goggles ("firing from
the hip" requires Punch). Note that Flut Flut and the Zoomer will have access to their full movement sets at all times.

You can turn off Move Rando at any time in the game by opening the game's menu, navigate to `Options`, 
then `Archipelago Options`, then `Move Randomizer`. This will give you access to the full movement set again.

## What are the movement options in Move Randomizer
| Move Name       | Prerequisite Moves |
|-----------------|--------------------|
| Crouch          |                    |
| Crouch Jump     | Crouch             |
| Crouch Uppercut | Crouch             |
| Roll            |                    |
| Roll Jump       | Roll               |
| Double Jump     |                    |
| Jump Dive       |                    |
| Jump Kick       |                    |
| Punch           |                    |
| Punch Uppercut  | Punch              |
| Kick            |                    |

## How do I know which moves I have
Open the game's menu, navigate to `Options`, then `Archipelago Options`, then `Move Tracker`.
This will show you a list of all the moves in the game. 
- Gray items indicate you do not possess that move.
- Yellow items indicate you possess that move, but you are missing its prerequisites.
- Light blue items indicate you possess that move, as well as its prerequisites.

## What does Orbsanity do
If you enable Orbsanity, bundles of Precursor Orbs will be turned into checks. Every time you collect the chosen number 
of orbs, i.e. a "bundle," you will trigger another check. Likewise, the orbs will be added to the random item pool. 
There are several options to change the difficulty of this challenge. 

- "Per Level" Orbsanity means the bundles are for each level in the game. (Geyser Rock, Sandover Village, etc.)
- "Global" Orbsanity means orbs collected from any level count toward the next bundle.
- The options with "Bundle Size" in the name indicate how many orbs are in a bundle. This adds a number of Items 
  and Locations to the pool inversely proportional to the size of the bundle.
    - For example, if your bundle size is 20 orbs, you will add 100 items to the pool. If your bundle size is 250 orbs,
      you will add 8 items to the pool.

## What do Traps do
When creating your player YAML, you can choose to replace some of the game's extraneous Power Cells and Precursor Orbs 
with traps. You can choose which traps you want to generate in your seed and how long they last. A random assortment 
will then be chosen to populate the item pool.

When you receive one, you will hear a buzzer and some kind of negative effect will occur in game. These effects may be 
challenging, maddening, or entertaining. When the trap duration ends, the game should return to its previous state.
Multiple traps can be active at the same time, and they may interact with each other in strange ways. If they become 
too frustrating, you can lower their duration by navigating to `Options`, then `Archipelago Options`, then 
`Seed Options`, then `Trap Duration`. Lowering this number to zero will disable traps entirely.

## What kind of Traps are there
| Trap Name       | Effect                                                                         |
|-----------------|--------------------------------------------------------------------------------|
| Trip Trap       | Jak trips and falls                                                            |
| Slippery Trap   | The world gains the physical properties of Snowy Mountain's ice lake           |
| Gravity Trap    | Jak falls to the ground faster and takes fall damage more easily               |
| Camera Trap     | The camera remains fixed in place no matter how far away Jak moves             |
| Darkness Trap   | The world gains the lighting properties of Dark Cave                           |
| Earthquake Trap | The world and camera shake                                                     |
| Teleport Trap   | Jak immediately teleports to Samos's Hut                                       |
| Despair Trap    | The Warrior sobs profusely                                                     |
| Pacifism Trap   | Jak's attacks have no effect on enemies, crates, or buttons                    |
| Ecoless Trap    | Jak's eco is drained and he cannot collect new eco                             |
| Health Trap     | Jak's health is set to 0 - not dead yet, but he will die to any attack or bonk |
| Ledge Trap      | Jak cannot grab onto ledges                                                    |
| Zoomer Trap     | Jak mounts an invisible zoomer (model loads properly depending on level)       |
| Mirror Trap     | The world is mirrored                                                          |

## I got soft-locked and cannot leave how do I get out of here
Open the game's menu, navigate to `Options`, then `Archipelago Options`, then `Warp To Home`. 
Selecting this option will ask if you want to be teleported to Geyser Rock. From there, you can teleport back 
to the nearest sage's hut to continue your journey.

## How do I generate seeds with 1 orb orbsanity and other extreme options?
Depending on your player YAML, Jak and Daxter can have a lot of items, which can sometimes be overwhelming or 
disruptive to multiworld games. There are also options that are mutually incompatible with each other, even in a solo
game. To prevent the game from disrupting multiworlds, or generating an impossible solo seed, some options have
"friendly limits" that prevent you from choosing more extreme values.

You can override **some**, not all, of those limits by editing the `host.yaml`. In the Archipelago Launcher, click 
`Open host.yaml`, then search for `jakanddaxter_options`, then search for `enforce_friendly_options`, then change this 
value from `true` to `false`. You can then generate a seed locally, and upload that to the Archipelago website to host
for you (or host it yourself). 

**Remember:** disabling this setting allows for more disruptive and challenging options, but it may cause seed 
generation to fail. **Use at your own risk!**

## How do I check my player options in-game
When you connect your text client to the Archipelago Server, the server will tell the game what options were chosen
for this seed, and the game will apply those settings automatically. 

You can verify these options by navigating to `Options`, then `Archipelago Options`, then `Seed Options`. **You can open 
each option to verify them, but you should NOT alter them during a run.** This may cause you to miss important 
progression items and prevent you (and others) from completing the run.

## How does the HUD work
The game's normal HUD shows you how many power cells, precursor orbs, and scout flies you currently have. But if you 
hold `L2 or R2` and press a direction on the D-Pad, the HUD will show you alternate modes. Here is how the HUD works:

| HUD Mode      | Button Combo                 | What the HUD Shows                | Text Messages                         |
|---------------|------------------------------|-----------------------------------|---------------------------------------|
| Per-Level     | `L2 or R2` + `Down`          | Locations Checked (in this level) | `SENT {Other Item} TO {Other Player}` |
| Global        | `L2 or R2` + `Up`            | Locations Checked (in the game)   | `GOT {Your Item} FROM {Other Player}` |
| Normal        | `L2 or R2` + `Left or Right` | Items Received                    | Both Sent and Got Messages            |
|               |                              |                                   |                                       |
| (In Any Mode) |                              | (If you sent an Item to Yourself) | `FOUND {Your Item}`                   |

In all modes, the last 3 sent/received items and the player who sent/received it will be displayed in the 
bottom left corner. This will help you quickly reference information about newly received or sent items. Items in blue 
are Progression (or non-Jak items), in green are Filler, and in red are Traps. You can turn this off by navigating 
to `Options`, then `Archipelago Options`, then set `Item Messages` to `Off`.

## I think I found a bug where should I report it
Depending on the nature of the bug, there are a couple of different options.

* If you found a logical error in the randomizer, please create a new Issue 
[here](https://github.com/ArchipelaGOAL/Archipelago/issues). Use this page if:
    * An item required for progression is unreachable. 
    * The randomizer did not respect one of the Options you chose.
    * You see a mistake, typo, etc. on this webpage.
    * You see an error or stack trace appear on the text client.

* If you encountered an error in OpenGOAL, please create a new Issue 
[here](https://github.com/ArchipelaGOAL/ArchipelaGOAL/issues). Use this page if:
    * You encounter a crash, freeze, reset, etc. in the game.
    * You fail to send Items you find in the game to the Archipelago server.
    * You fail to receive Items the server sends to you.
    * Your game disconnects from the server and cannot reconnect.
    * You go looking for a game item that has already disappeared before you could reach it.

* Please upload your config file, spoiler log file, and any other generated logs in the Issue, so we can troubleshoot the problem.