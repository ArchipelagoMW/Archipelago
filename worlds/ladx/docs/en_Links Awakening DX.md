# Links Awakening DX

## Where is the options page?

The [player options page for this game](../player-options) contains all the options you need to configure and export a
config file.

## What does randomization do to this game?

Items which the player would normally acquire throughout the game have been moved around. Logic remains, so the game is
always able to be completed, but because of the item shuffle the player may need to access certain areas before they
would in the vanilla game.

## What items and locations get shuffled?

All main inventory items, collectables, and ammunition can be shuffled, and all locations in the game which could
contain any of those items may have their contents changed.

## Which items can be in another player's world?

Any of the items which can be shuffled may also be placed into another player's world. It is possible to choose to limit
certain items to your own world.

## What does another world's item look like in Link's Awakening?

The game will try to pick an appropriate sprite for the item (a LttP sword will be a sword!) - it may, however, be a little odd (a Missile Pack may be a single arrow).

If there's no appropriate sprite, a Letter will be shown.

## When the player receives an item, what happens?

When the player receives an item, Link will hold the item above his head and display it to the world. It's good for
business!

## I don't know what to do!

That's not a question - but I'd suggest clicking the crow icon on your client, which will load an AP compatible autotracker for LADXR.

## What is this randomizer based on?

This randomizer is based on (forked from) the wonderful work daid did on LADXR - https://github.com/daid/LADXR

The autotracker code for communication with magpie tracker is directly copied from kbranch's repo - https://github.com/kbranch/Magpie/tree/master/autotracking

### Graphics

The following sprite sheets have been included with permission of their respective authors:

* by Madam Materia (https://www.twitch.tv/isabelle_zephyr)
  * Matty_LA
* by Linker (https://twitter.com/BenjaminMaksym)
  * Bowwow
  * Bunny
  * Luigi
  * Mario
  * Richard
  * Tarin

Title screen graphics by toomanyteeth✨ (https://instagram.com/toomanyyyteeth)

## Some tips from LADXR...

<h3>Locations</h3>
<p>All chests and dungeon keys are always randomized. Also, the 3 songs (Marin, Mambo, and Manu) give a you an item if you present them the Ocarina. The seashell mansion 20 shells reward is also shuffled, but the 5 and 10 shell reward is not, as those can be missed.</p>
<p>The moblin cave with Bowwow contains a chest instead. The color dungeon gives 2 items at the end instead of a choice of tunic. Other item locations are: The toadstool, the reward for delivering the toadstool, hidden seashells, heart pieces, heart containers, golden leaves, the Mad Batters (capacity upgrades), the shovel/bow in the shop, the rooster's grave, and all of the keys' (tail,slime,angler,face,bird) locations.</p>
<p>Finally, new players often forget the following locations: the heart piece hidden in the water at the castle, the heart piece hidden in the bomb cave (screen before the honey), bonk seashells (run with pegasus boots against the tree in at the Tail Cave, and the tree right of Mabe Village, next to the phone booth), and the hookshop drop from Master Stalfos in D5.</p>

<h3>Color Dungeon</h3>
<p>The Color Dungeon is part of the item shuffle, and the red/blue tunics are shuffled in the item pool. Which means the fairy at the end of the color dungeon gives out two random items.</p>
<p>To access the color dungeon, you need the power bracelet, and you need to push the gravestones in the right order: "down, left, up, right, up", going from the lower right gravestone, to the one left of it, above it, and then to the right.</p>

<h3>Bowwow</h3>
<p>Bowwow is in a chest, somewhere. After you find him, he will always be in the swamp with you, but not anywhere else.</p>

<h3>Added things</h3>
<p>In your save and quit menu, there is a 3rd option to return to your home. This has two main uses: it speeds up the game, and prevents softlocks (common in entrance rando).</p>
<p>If you have weapons that require ammunition (bombs, powder, arrows), a ghost will show up inside Marin's house. He will refill you up to 10 ammunition, so you do not run out.</p>
<p>The flying rooster is (optionally) available as an item.</p>
<p>You can access the Bird Key cave item with the L2 Power Bracelet.</p>
<p>Boomerang cave is now a random item gift by default (available post-bombs), and boomerang is in the item pool.</p>
<p>Your inventory has been increased by four, to accommodate these items now coexisting with eachother.</p>

<h3>Removed things</h3>
<p>The ghost mini-quest after D4 never shows up, his seashell reward is always available.</p>
<p>The walrus is moved a bit, so that you can access the desert without taking Marin on a date.</p>

<h3>Logic</h3>
<p>Depending on your options, you can only steal after you find the sword, always, or never.</p>
<p>Do not forget that there are two items in the rafting ride. You can access this with just Hookshot or Flippers.</p>
<p>Killing enemies with bombs is in normal logic. You can switch to casual logic if you do not want this.</p>
<p>D7 confuses some people, but by dropping down pits on the 2nd floor you can access almost all of this dungeon, even without feather and power bracelet.</p>

<h3>Tech</h3>
<p>The toadstool and magic powder used to be the same type of item. LADXR turns this into two items that you can have a the same time. 4 extra item slots in your inventory were added to support this extra item, and have the ability to own the boomerang.</p>
<p>The glitch where the slime key is effectively a 6th golden leaf is fixed, and golden leaves can be collected fine next to the slime key.</p>
