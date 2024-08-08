# Jak And Daxter (ArchipelaGOAL)

## Where is the options page?

The [Player Options Page](../player-options) for this game contains 
all the options you need to configure and export a config file.

At this time, there are several caveats and restrictions:
- Power Cells and Scout Flies are **always** randomized.
- Precursor Orbs are **never** randomized.
- **All** of the traders in the game become in-logic checks **if and only if** you have enough Orbs (1530) to pay them all at once. 
  - This is to prevent hard locks, where an item required for progression is locked behind a trade you can't afford.

## What does randomization do to this game?
The game now contains the following Location checks:
- All 101 Power Cells 
- All 112 Scout Flies
- All the Orb Caches that are not in Gol and Maia's Citadel (a total of 11)

These may contain Items for different games, as well as different Items from within Jak and Daxter. 
Additionally, several special checks and corresponding items have been added that are required to complete the game.

## What are the special checks and how do I check them?
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

## What are the special items and what do they unlock?
| Item Name                                                                | What It Unlocks                                                                               |
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

## How do I know which special items I have?
Open the game's menu, navigate to `Options`, then `Archipelago Options`, then `Item Tracker`.
This will show you a list of all the special items in the game, ones not normally tracked as power cells or scout flies.
Gray items indicate you do not possess that item, light blue items indicate you possess that item.

## What is the goal of the game once randomized?
To complete the game, you must defeat the Gol and Maia and stop them from opening the Dark Eco silo.

In order to reach them, you will need at least 72 Power Cells to cross the Lava Tube. In addition, 
you will need the four special items that free the Red, Blue, Yellow, and Green Sages.

## What happens when I pick up or receive a power cell?
When you pick up a power cell, Jak and Daxter will perform their victory animation. Your power cell count will 
NOT change. The pause menu will say "Task Completed" below the picked-up Power Cell. If your power cell was related 
to one of the special checks listed above, you will automatically check that location as well - a 2 for 1 deal!
Finally, your text client will inform you what you found and who it belongs to.

When you receive a power cell, your power cell count will tick up by 1. Gameplay will otherwise continue as normal. 
Finally, your text client will inform you where you received the power cell from.

## What happens when I pick up or receive a scout fly?
When you pick up a scout fly, your scout fly count will NOT change. The pause menu will show you the number of
scout flies you picked up per-region, and this number will have ticked up by 1 for the region that scout fly belongs to. 
Finally, your text client will inform you what you found and who it belongs to.

When you receive a scout fly, your total scout fly count will tick up by 1. The pause menu will show you the number of
scout flies you received per-region, and this number will have ticked up by 1 for the region that scout fly belongs to. 
Finally, your text client will inform you where you received the scout fly from, and which one it is.

## How do I check the "Free 7 Scout Flies" power cell?
You will automatically check this power cell when you _receive_ your 7th scout fly, NOT when you _pick up_ your 7th
scout fly. So in short:

- When you _pick up_ your 7th fly, the normal rules apply. 
- When you _receive_ your 7th fly, 2 things will happen in quick succession.
  - First, you will receive that scout fly, as normal.
  - Second, you will immediately complete the "Free 7 Scout Flies" check, which will send out another item.

## What does Deathlink do?
If you enable Deathlink, all the other players in your Multiworld who also have it enabled will be linked on death. 
That means when Jak dies in your game, the players in your Deathlink group also die. Likewise, if any of the other 
players die, Jak will also die in a random fashion.

You can turn off Deathlink at any time in the game by opening the game's menu, navigate to `Options`, 
then `Archipelago Options`, then `Deathlink`.

## What does Move Randomizer do?
If you enable Move Randomizer, most of Jak's movement set will be added to the randomized item pool, and you will need 
to receive the move in order to use it (i.e. you must find it, or another player must send it to you). Some moves have
prerequisite moves that you must also have in order to use them (e.g. Crouch Jump is dependent on Crouch). Jak will only
be able to run, swim (including underwater), and perform single jumps. Note that Flut Flut will have access to her full
movement set at all times.

You can turn off Move Rando at any time in the game by opening the game's menu, navigate to `Options`, 
then `Archipelago Options`, then `Move Randomizer`. This will give you access to the full movement set again.

## What are the movement options in Move Randomizer?
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

## How do I know which moves I have?
Open the game's menu, navigate to `Options`, then `Archipelago Options`, then `Move Tracker`.
This will show you a list of all the moves in the game. 
- Gray items indicate you do not possess that move.
- Yellow items indicate you possess that move, but you are missing its prerequisites.
- Light blue items indicate you possess that move, as well as its prerequisites.

## What does Orbsanity do?
If you enable Orbsanity, Precursor Orbs will be turned into ordered lists of progressive checks. Every time you collect 
a "bundle" of the correct number of orbs, you will trigger the next release in the list. Likewise, these bundles of orbs 
will be added to the item pool to be randomized. There are several options to change the difficulty of this challenge. 

- "Per Level" Orbsanity means the lists of orb checks are generated and populated for each level in the game.
  - (Geyser Rock, Sandover Village, etc.)
- "Global" Orbsanity means there is only one list of checks for the entire game.
  - It does not matter where you pick up the orbs, they all count toward the same list.
- The options with "Bundle Size" in the name indicate how many orbs are in a "bundle." This adds a number of Items 
  and Locations to the pool inversely proportional to the size of the bundle.
    - For example, if your bundle size is 20 orbs, you will add 100 items to the pool. If your bundle size is 250 orbs,
      you will add 8 items to the pool.

### A WARNING ABOUT ORBSANITY OPTIONS

Unlike other settings, you CANNOT alter Orbsanity options after you generate a seed and start a game. **If you turn 
Orbsanity OFF in the middle of an Orbsanity game, you will have NO way of completing the orb checks.** This may cause
you to miss important progression items and prevent you (and others) from completing the run.

When you connect your text client to the Archipelago Server, the server will tell the game what settings were chosen
for this seed, and the game will apply those settings automatically. You can verify (but DO NOT ALTER) these settings 
by navigating to `Options`, then `Archipelago Options`.

## I got soft-locked and can't leave, how do I get out of here?
Open the game's menu, navigate to `Options`, then to `Archipelago Options`, then to `Warp To Home`. 
Selecting this option will ask if you want to be teleported to Geyser Rock. From there, you can teleport back 
to the nearest sage's hut to continue your journey.

## I think I found a bug, where should I report it?
Depending on the nature of the bug, there are a couple of different options.

* If you found a logical error in the randomizer, please create a new Issue 
[here.](https://github.com/ArchipelaGOAL/Archipelago/issues)
  * Use this page if:
    * An item required for progression is unreachable. 
    * The randomizer did not respect one of the Options you chose.
    * You see a mistake, typo, etc. on this webpage.
    * You see an error or stack trace appear on the text client.
  * Please upload your config file and spoiler log file in the Issue, so we can troubleshoot the problem.

* If you encountered an error in OpenGOAL, please create a new Issue 
[here.](https://github.com/ArchipelaGOAL/ArchipelaGOAL/issues)
  * Use this page if:
    * You encounter a crash, freeze, reset, etc in the game.
    * You fail to send Items you find in the game to the Archipelago server.
    * You fail to receive Items the server sends to you.
    * Your game disconnects from the server and cannot reconnect.
    * You go looking for a game item that has already disappeared before you could reach it.
  * Please upload any log files that may have been generated.