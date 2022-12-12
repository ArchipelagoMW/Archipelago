# Castlevania 64

## Where is the settings page?

The player settings page for this game(../player-settings) contains all the options you need to configure and export a
config file.

## What does randomization do to this game?

Items which the player would normally acquire throughout the game have been moved around. Because of the item shuffle,
instead of simply playing through each of the stages as they come, the player will most likely be required to hop around
them via a new menu. Logic remains so that the game is beatable under these new conditions.

## How do I return to a previous stage?

Instant travel to an earlier or later stage is made possible through a menu that can be pulled up while not in a boss
fight by pressing START while holding Z and R. By finding Special1 jewels, more destinations can be selected on
this menu. The destinations on this list are randomized per seed and the first one will always be the player's
starting location.

Regardless of which option you have selected, you can hold Z or R while making your selection to return to Villa's crypt
or Castle Center's top elevator room respectively, provided you've already been in there at least once.

## Do I need to do separate playthroughs with each character to check everything?

Nope! Which character stage slot the Villa coffin sends you to depends on the time of day and both bridges at the top of Castle
Center's elevator are intact regardless of who you are. Because of these changes in game behavior, every stage can be
accessed by any character in a single playthrough.

## What is the goal of Castlevania 64 when randomized?

Make it to Castle Keep, enter Dracula's chamber, and defeat him to complete your goal. Which ending you get does **not**
matter.

The chamber's entrance door is initially locked until whichever of the following objectives that was specified on the
player's YAML under `Dracula's Condition` is completed:
- `Activate Crystal`: Activate the big crystal in Castle Center basement's bull room.
- `Kill Bosses`: Kill the specified number of bosses with health meters on the player's YAML.
- `Special2 Hunt`: Collect the amount of Special2 jewels specified on the player's YAML.

If `None` was specified, then there is no objective; the chamber door is unlocked from the start.

## What items and locations get shuffled?

Inventory items, jewels, moneybags, and PowerUps are all placed in the item pool. Location checks include freestanding
items, items from one-hit breakables, and items given through text. Items from three-hit breakables and the salesman
Renon are unchanged. Sub-weapons can optionally be shuffled in their own separate pool.

The infamous Nitro transport sequence has been reworked. Two Magical Nitro jars and two Mandragora jars are placed into
the item pool for blowing up the cracked walls in Castle Center and a randomized item is placed on both of their
shelves. The randomized Magical Nitro will **NOT** kill you upon landing or taking damage, so don't panic when you
receive one! Hazardous Waste Dispoal bins are disabled and the bull room crack will not let you set anything until its
seal is removed so none of the limited ingredients can be wasted.

## Which items can be in another player's world?

Any of the items which can be shuffled may also be placed into another player's world. It is possible to choose to limit
sub weapons to your own world.

## What does another world's item look like in Castlevania 64?

An item belonging to another world is represented as a Wooden Stake if it is important or a Rose if it is not. These are
unused sub-weapons in the vanilla game that, in the randomizer, were modified to not change your current sub-weapon.


## When the player receives an item, what happens?

When the player receives an item, a textbox containing that item's name will pop up on-screen as when an item would
normally be picked up.

## What tricks and glitches should I know for Hard Logic?

The following tricks always have a chance to be required:
- Left Tower skip in Castle Wall
- Maze (Copper Key) skip in Villa
- Waterfall skip in reverse Underground Waterway
- Slope Jump to Room of Clocks from Castle Keep
- Jump to the gated ledge in Tower of Execution

Enabling Carrie Logic will also expect these tricks:

- Sniping dogs through the front gates in Villa
- Library jump in Castle Center

Note that the downstairs hallway crack will always logically expect two Nitros and two Mandragoras even with these
settings on due to the possibility of wasting a pair on the upper wall.

## How do I set Nitro/Mandragora?

C-right.
