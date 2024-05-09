# Jak And Daxter (ArchipelaGOAL)

## Where is the options page?

The [Player Options Page](../player-options) for this game contains 
all the options you need to configure and export a config file.

At this time, these options don't do anything. Scout Flies are always randomized, and Precursor Orbs 
are never randomized.

## What does randomization do to this game?
All 101 Power Cells and 112 Scout Flies are now Location Checks 
and may contain Items for different games as well as different Items from within Jak and Daxter.

## What is the goal of the game once randomized?
To complete the game, you must defeat the Gol and Maia and stop them from opening the Dark Eco silo.

In order to reach them, you will need at least 72 Power Cells to cross the Lava Tube. In addition, 
you will need the four specific Power Cells obtained by freeing the Red, Blue, Yellow, and Green Sages.

## How do I progress through the game?
You can progress by performing tasks and completing the challenges that would normally give you Power Cells and 
Scout Flies in the game. If you are playing with others, those players may find Power Cells and Scout Flies 
in their games, and those Items will be automatically sent to your game. 

If you have completed all possible tasks available to you but still cannot progress, you may have to wait for 
another player to find enough of your game's Items to allow you to progress. If that does not apply, 
double check your spoiler log to make sure you have all the items you should have. If you don't, 
you may have encountered a bug. Please see the options for bug reporting below.

## What happens when I pick up an item?
Jak and Daxter will perform their victory animation, if applicable. You will not receive that item, and 
the Item count for that item will not change. The pause menu will say "Task Completed" below the 
picked-up Power Cell, but the icon will remain "dormant." You will see a message in your text client saying 
what you found and who it belongs to.

## What happens when I receive an item?
Jak and Daxter won't perform their victory animation, and gameplay will continue as normal. Your text client will 
inform you where you received the Item from, and which one it is. Your Item count for that type of Item will also 
tick up. The pause menu will not say "Task Completed" below the selected Power Cell, but the icon will be "activated."

## I can't reach a certain area within an accessible region, how do I get there?
Some areas are locked behind ownership of specific Power Cells. For example, you cannot access Misty Island 
until you have the "Catch 200 Pounds of Fish" Power Cell. Keep in mind, your access to Misty Island is determined 
_through ownership of this specific Power Cell only,_ **not** _by you completing the Fishing minigame._

## I got soft-locked and can't leave, how do I get out of here?
As stated before, some areas are locked behind ownership of specific Power Cells. But you may already be past 
a point-of-no-return preventing you from backtracking. One example is the Forbidden Jungle temple, where 
the elevator is locked at the bottom, and if you haven't unlocked the Blue Eco Switch, you cannot access 
the Plant Boss's room and escape.

In this scenario, you will need to open your menu and find the "Teleport Home" option. Selecting this option 
will instantly teleport you to the nearest Sage's Hut in the last hub area you were in... or always to 
the Green Sage's Hut, depending on the feasibility of the former option. This feature is a work in progress.

## I think I found a bug, where should I report it?
Depending on the nature of the bug, there are a couple of different options.

* If you found a logical error in the randomizer, please create a new Issue 
[here.](https://github.com/ArchipelaGOAL/Archipelago/issues)
  * Use this page if:
    * For example, you are stuck on Geyser Rock because one of the four Geyser Rock Power Cells is not on Geyser Rock.
    * The randomizer did not respect one of the Options you chose.
    * You see a mistake, typo, etc. on this webpage.
  * Please upload your config file and spoiler log file in the Issue, so we can troubleshoot the problem.

* If you encountered an error in OpenGOAL, please create a new Issue 
[here.](https://github.com/ArchipelaGOAL/ArchipelaGOAL/issues)
  * Use this page if:
    * You encounter a crash, freeze, reset, etc.
    * You fail to send Items you find in the game to the Archipelago server.
    * You fail to receive Items the server sends to you.
    * Your game disconnects from the server and cannot reconnect.
  * Please upload any log files that may have been generated.