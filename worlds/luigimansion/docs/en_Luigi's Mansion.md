# Luigi's Mansion

## Where is the settings page?

The [player settings page for this game](../player-settings) contains all the options you need to configure and export a
config file.

## What does randomization do to this game?

When it comes to Luigi's Mansion, randomization changes the locations of Mario's Items, door keys and element medallions,
as well as all the treasure bundles that are found in chests. This primarily changes the route the player must take 
through the game.

The Randomizer allows you to set different goals and modify the game in several other ways
([see below](#changes-from-the-vanilla-game)). 

## What items and locations get shuffled?

Door Keys, Mario's items, and the element medallions are shuffled. These are found in the chests in various rooms in the 
mansion, as well as a few specific objects. There are options for Boos, Portrait Ghosts, Toads, Plants, Gold Mice, Blue 
Ghosts (Speedy Spirits), and even every interactable object in the game.

## Which items can be in another player's world?

Keys, Mario's Items, and Element Medals can be found in other worlds, along with money , hearts, and poison mushrooms.

## What does another world's item look like in Luigi's Mansion?

Items belonging to other worlds are represented by an AP icon and are called AP items.

## When the player receives an item, what happens?

_______. 

## Changes from the vanilla game

###### Customization options:

- Choose a goal for your world. Possible goals are: 1) Reach the final floor; 2) Defeat the boss on the final floor; 3)
  Retrieve a (customizable) number of Iris treasures from the cave; 4) Retrieve the Iris treasures *and* defeat the boss
- You can also randomize the goal; The blue-haired NPC in front of the cafe can tell you about the selected objective
- Customize the chances of encountering blue chests, healing tiles, Iris treasures, etc.
- Customize the default party lineup and capsule monster
- Customize the party starting level as well as capsule monster level and form
- Customize the initial and final floor numbers
- Customize the boss that resides on the final floor
- Customize the multiworld item pool. (By default, your pool is filled with random blue chest items, but you can place
  any cave item you want instead)
- Customize start inventory, i.e., begin every run with certain items or spells of your choice
- Adjust how much EXP is gained from enemies
- Randomize enemy movement patterns, enemy sprites, and which enemy types can appear at which floor numbers
- Option to shuffle your party members and/or capsule monsters into the multiworld, meaning that someone will have to
  find them in order to unlock them for you to use. While cave diving, you can add newly unlocked members to your party
  by using the character items from your inventory

###### Quality of life:

- Various streamlining tweaks (removed cutscenes, dialogue, transitions)
- You can elect to lock the cave layout for the next run, giving you exactly the same floors and red chest contents as
  on your previous attempt. This functionality is accessed via the bald NPC behind the counter at the Ancient Cave
  Entrance
- Multiple people can connect to the same slot and collaboratively search for Iris treasures and blue chests
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
