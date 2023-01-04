# Lufia II - Rise of the Sinistrals (Ancient Cave)

## Where is the settings page?

The [player settings page for this game](../player-settings) contains all the options you need to configure and export a
config file.

## What does randomization do to this game?

As you may or may not know, randomization was already a core feature of the Ancient Cave in Lufia II, basically being a
whole game within a game. The Ancient Cave has 99 floors with increasingly hard enemies, red chests and blue chests. At
the end of the Ancient Cave you get to fight the Royal Jelly... if you make it that far. You cannot lose the Royal
Jelly fight as it kills itself after giving you three rounds to try and kill it (or manage to vanquish your own party, 
whichever one you can manage).

The Randomizer allows you to set different goals and modify the game in several other ways
([see below](#changes-from-the-vanilla-game)). 

## What items and locations get shuffled?

In general, all Items can appear in the red and blue chests, the blue chest items are items you get to keep after you
die in or escape the Ancient Cave using Providence. Archipelago Items can also appear in said chests. Iris Treasures are
always in your local game.

## Which items can be in another player's world?

Any of the blue chest items from the vanilla game may be placed into another player's world.

## What does another world's item look like in Lufia II?

Items belonging to other worlds are represented by an AP icon and are called AP items.

## When the player receives an item, what happens?

Your Party Leader will hold up the item they received when not in a fight or in a menu. 

## Changes from the vanilla game

###### Customization options:

- Choose a goal for your world. Possible goals are: 1) Reach the final floor; 2) Defeat the boss on the final floor; 3)
  Retrieve a (customizable) number of iris treasures from the cave; 4) Retrieve the iris treasures *and* defeat the boss
- You can also randomize the goal; The blue-haired NPC in front of the cafe can tell you about the selected objective
- Customize (or randomize) the chances of encountering blue chests, healing tiles, iris treasures, etc.
- Customize (or randomize) the default party lineup and capsule monster
- Customize (or randomize) the party starting level as well as capsule monster level and form
- Customize (or randomize) the initial and final floor numbers
- Customize (or randomize) the boss that resides on the final floor
- Customize start inventory, i.e., begin every run with certain items or spells of your choice
- Option to shuffle your party members and/or capsule monsters into the multiworld, meaning that someone will have to
  find them in order to unlock them for you to use

###### Quality of life:

- Various streamlining tweaks (removed cutscenes, dialogue, transitions)
- Always start with Providence already in your inventory. (It is no longer obtained from red chests)
- (optional) Run button that allows you to move at faster than normal speed

###### Quality of death:

- Blue chest items that you received from the multiworld are kept, even if your party dies. (I.e., you do not need to
  use Providence to make them permanent)
- Similarly, but in the opposite direction: All location checks you make are immediately sent out to the multiworld and
  don't require Providence for persistence.
- (optional) Death link support. (I.e., if your party is defeated, everyone else participating in death link also dies)

###### Bug fixes:

- Vanilla game bugs that could result in softlocks or save file corruption have been fixed
- (optional) Bugfix for the algorithm that determines the item pool for red chest gear. Enabling this allows the cave to
  generate shields, headgear, rings, and jewels in red chests even after floor B9
- (optional) Bugfix for the outlandish cravings of capsule monsters in the US version. Enabling this makes feeding work
  like in the JP and EU versions of the game, resulting in more reasonable cravings
