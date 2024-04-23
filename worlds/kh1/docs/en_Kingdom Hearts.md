# Kingdom Hearts (PC)

##Credits
This is a collaborative effort from several individuals in the Kingdom Hearts community, but most of all, denhonator.

Denho's original KH rando laid the foundation for the work here and makes everything here possible, so thank you Denho for such a blast of a randomizer.

Other credits include:

Sonicshadowsilver2 for their work finding many memory addresses and working to idenitify and resolve bugs.

Shananas and the rest of the OpenKH team for providing such an amazing tool for us to utilize on this project.

Krujo and the team from the KH1 Critical Mix Riku mod for their work on the `Show Prompt` method.

JaredWeakStrike for helping clean up my mess of code.

## Where is the options page?

The [player options page for this game](../player-options) contains most of the options you need to 
configure and export a config file.

## What does randomization do to this game?

The Kingdom Hearts AP Randomizer randomizes most rewards in the game, and adds several items which are used to unlock worlds, Olympus Coliseum cups, and world progression.

Worlds can only be accessed by finding the corresponding item.  For example, you need to find the "Monstro" item to enter Monstro.

The default goal is to enter End of the World and defeat Final Ansem.  You can enter the world by obtaining a number of Ansem's Reports defined in your YAML.

## What items and locations get shuffled?

###Items

Any weapon, accessory, spell, trinity, summon, world, key item, stat up, consumable, or ability can be found in any location.

###Locations

Locations the player can find items include chests, event rewards, Atlantica clams, level up rewards, 101 Dalmation rewards, and postcard rewards.

## Which items can be in another player's world?

Any of the items which can be shuffled may also be placed into another player's world. It is possible to choose to limit
certain items to your own world.
## When the player receives an item, what happens?

When the player receives an item, your client will display a message displaying the item you have obtained.  You will also see a notification in the "LEVEL UP" box.

## What do I do if I encounter a bug with the game?

Please reach out to Gicu#7034 on Discord.

## How do I progress a certain world?

###The evidence boxes aren't spawning in Wonderland.

Find `Footprints` in the multiworld.

###I can't enter any cups in Olympus Coliseum.

Phil Cup, Pegasus Cup, and Hercules Cup are all multiworld items.  Finding all 3 grant you access to Hades Cup and the Platinum Match.  Clearing all cups lets you challenge Ice Titan.

###The slides aren't spawning in Deep Jungle.

Find `Slide 1` in the multiworld.

###I can't progress Halloween Town.

Find `Jack-in-the-Box` in the multiworld.

###The Hollow Bastion Library is missing a book.

Find `Theon Vol. 6` in the multiworld.

##How do I enter the End of the World?

Find the required number of Ansem's Reports defined in your settings in the multiworld.

##I am stuck in Hollow Bastion, how do I leave?

You can open the full menu and warp out using `L1` + `L2` + `R2` + `Select`

##I am still receiving vanilla rewards in several locations.
There are locations that still grant vanilla rewards, as it is currently not known how to remove them.  Such locations include Atlantica Clams, Spinners in the Hollow Bastion Library, Puppy Rewards, and several Postcard Locations.

Where these items are progression, they remain vanilla.  Where they are filler items, they grant a check in addition to the vanilla reward.