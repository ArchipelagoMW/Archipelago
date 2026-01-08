# The Binding of Isaac: Repentance
## Where is the settings page?
The [player settings](/games/The%20Binding%20of%20Isaac%20Repentance/player-options) page for this game contains all the options you need to configure and export a config file.  
... if the game ever gets core-verified that is. For now you'll have to generate a yaml template via the Archipelago Launcher or download it from the release page.

## What does randomization do to this game?
The Binding of Isaac: Repentance is already random. The Archipelago mod mostly implements how you can progress throughout your run.  
By default, all stage types except for Basement, Caves and Depths are locked. Therefore you could only progress until Mom's Foot at the beginning of a session.  
The unlocks for other stages or areas of the game need to be found by you or other players in the MultiWorld first before you can access them.

## What is the goal of The Binding of Isaac: Repentance in Archipelago?
In The Binding of Isaac: Repentance the goal in Archipelago is to defeat a configurable set of main bosses.  
By default, these are the four endgame bosses: Mega Satan, Delirium, Beast and Mother.  
This usually requires multiple runs. It is not expected to complete all goals in a single run but rather to explore and unlock all areas of the game through multiple runs first until you're able to reach all the required bosses.

## What does another world's item look like in The Binding of Isaac: Repentance?
There are three ways to find items from another world
### AP Items
Occasionally pedestal items are replaced with a special Archipelago Item. Picking it up sends an item to another world. It's not possible to know what item it is going to be prior to picking it up.  
If one of these items is inaccessible or you're otherwise unable to pick it up, it is not detrimental to skip it. The next AP Item you pick up will send the expected item instead.  
The frequency on how many of these AP Items show up can be configured via the player settings. On average your runs are initially weaker as you're getting less passive items for yourself but eventually become stronger as you receive items from other worlds instead. (see section below)
### Finding/Clearing special rooms
Apart from directly picking up an AP Item. You're also sending an item to someone the first time you enter/clear a special room on each stage type.  
For example, finding your secret room on basement will send an item to someone, finding it in the Caves another, etc. If you find your basement secret room again in a subsequent run, it will not send one. It's only once per stage type. However we also differntiate between stage variants, so the same room type in Basement and Burning Basement are two different checks.  
The game will also avoid sending you to a stage variant if you already collected all items on that variant but have another one unlocked where you're still missing some.

The room types containing items are:
- Common rooms (always spawn)
  - Treasure Room
  - Shop
  - Secret Room
  - Super Secret Room
  - Boss Room
  - Closet (In Home)
  - Knife Piece 2 (Escape sequence in Mines/Ashpit)
- Uncommon rooms (spawn every couple floors)
  - Arcade
  - Challenge Room
  - Curse Room
  - Sacrifice Room
  - Miniboss Room
  - Deal Room
- Rare rooms (spawn once or twice a run)
  - Vault
  - Dice Room
  - Bedroom
  - Library

Rare rooms also cannot contain essential progression items. They can still hold useful items though.  
Extremly rare rooms that you only see once every couple of runs (Planetarium, Crawl Space, Ultra secret room, etc.) are excluded and do not contain MultiWorld items as this would be very grindy to get them for every stage type. But there may be an option to configure this in the future.

### [Optional] Main boss rewards
There is also a setting to send additional items the first time you beat each of the main bosses of the game.

#### What if an essential progression item is locked in an uncommon room but I have terrible RNG and it just doesn't spawn?
To avoid these bad RNG situations, there is a setting you can enable which automatically collects all missed locations for the stages you have visited when you sucessfully finish a run.  
That means, even if a mini boss room in the Flooded Caves didn't spawn, sucessfully winning your run will collect the item for it anyways as long as you have been to the Flooded Caves on that run.

## What The Binding of Isaac: Repentance items can appear in other players' worlds?
There are 5 categories of items you can receive:
1. Progression Items
   These items unlock all the areas in your game and are called "*Unlock [Stage name]*".  
   In your game, most doors and trapdoors that lead to other areas do not spawn unless you have received one of the respective Unlock items.  
   So there will be no door to Downpour/Dross after your Basement boss unless Dross or Downpour has been unlocked for you.  
   Negative and Polaroid are replaced by Boss items unless Chest/Dark Room is unlocked respectively.  
   Key pieces are replaced by Angel items unless Mega Satan is unlocked.  
   Etc.
2. Usefull Items
   These are your traditional Isaac items and are grouped by their item pool.  
   An item from the following pools can be sent to you:
   - Treasure Room Item
   - Shop Item
   - Boss Item
   - Devil Deal Item
   - Angle Deal Item
   - Secret Room Item
   - Library Item
   - Curse Room Item
   - Planetarium Item
   - Golden Chest Item
   - Red Chest Item
3. "Junk" Items
   These include all sorts of pickups like random hearts, bombs, coins, etc. and are what you'll receive most frequently.
4. [Optional] Traps
5. [Optional] 1-Ups

### What happens to the Items I received when I start a new run?
Unlocks and 1-Ups are always retained and re-given on each run once you have received them.  
For items and consumables you are given a percentage of them on each new run. Either at the very begining or spread across the first 6 floors.  
This can be configured in the settings. By default, 30% of all items and 10% of all consumables you received from the MultiWorld are spread across the first 6 floors on every new run.  
Setting this to 100% and given immeaditely on run start would make subsequent runs very overpowered very quickly.  
Traps do never carry over into new runs and are only applied the moment they're received.

## Does the mod affect my saves?
It does not. If you want to clear later bosses and don't want to bother with unlocking, you can use the isaac-save-insaller by Zamiell to install a fully-unlocked save file and backup you old saves.

## Can you play multiplayer?
Currently no support for multiplayer has been implemented. It will not crash the game or anything but probably won't be the experience you imagine.

## How many items are there?
With the default settings, the game includes 448 location checks. But these can be lowered by excluding segments of the game, like the alt paths or the ascend for example.  
They can also be increased by including more AP Items. By default there are 80 of them and once you collected them all they will not show up anymore.

## Is Archipelago compatible with other The Binding of Isaac: Repentance mods?
From initial testing it is compatible with most visual, small or QoL mods. However, big mods that heavily change the game, like adding extra stages may not work as well as mods that change the lua modding API like Repentogon.
