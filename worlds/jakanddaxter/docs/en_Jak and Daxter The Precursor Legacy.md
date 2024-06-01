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
All 101 Power Cells and 112 Scout Flies are now Location Checks and may contain Items for different games, 
as well as different Items from within Jak and Daxter. Additionally, several special checks and corresponding items
have been added that are required to complete the game.

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

## I got soft-locked and can't leave, how do I get out of here?
Open the game's menu, navigate to `Options`, then to `Archipelago Options`, then to `Warp To Home`. 
Selecting this option will ask if you want to be teleported to Geyser Rock. From there, you can teleport back 
to the nearest sage's hut to continue your journey.

## How do I know which special items I have?
Open the game's menu, navigate to `Options`, then to `Archipelago Options`, then to `Item Tracker`.
This will show you a list of all the special items in the game, ones not normally tracked as power cells or scout flies.
Grayed-out items indicate you do not possess that item, light blue items indicate you possess that item.

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