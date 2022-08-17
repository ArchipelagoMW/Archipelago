# Castlevania

## Where is the settings page?

The player settings page for this game(../player-settings) contains all the options you need to configure and export a
config file.

## What does randomization do to this game?

Items which the player would normally acquire throughout the game have been moved around. Logic remains, so the game is
always able to be completed, but because of the item shuffle the player may need to access certain areas before they
would in the vanilla game.

Which stage the Villa coffin sends you to depends on whether it is day or night and both bridges at the top of Castle
Center's elevator are intact regardless of who you are. Because of these changes in game behavior, every stage can be
accessed with either character.

Instant travel to an earlier or later stage is also possible through a menu that can be pulled up when not off the
ground or in a boss fight by holding Z + R + Start. By finding Special2 jewels, more destinations can be selected on
this menu. The destinations are randomized per seed, and the first one on the list will always be the player's
starting location.

## What is the goal of Castlevania when randomized?

The goal is to find Castle Keep, enter Dracula's chamber, and kill him to win! Which ending you get does not matter;
your world's goal will complete regardless.

The door into the chamber is locked initially until whichever of the following objectives that was specified on the
player's YAML is completed:
- `Activate Crystal`: Activate the big crystal in Castle Center's basement bull room. 

## What items and locations get shuffled?

All main inventory items, jewels, PowerUps, and sub weapons can be shuffled, and all locations in the game which could
contain any of those items may have their contents changed.

The infamous Nitro transport challenge is cut out entirely in this randomizer. Instead, two Magical Nitro jars and two
Mandragora jars are shuffled into the item pool for blowing up the cracked walls in Castle Center. The randomized
Magical Nitro will **NOT** kill you upon jumping or taking damage, so don't be alarmed when you receive one!

## Which items can be in another player's world?

Any of the items which can be shuffled may also be placed into another player's world. It is possible to choose to limit
sub weapons to your own world.

## What does another world's item look like in Castlevania?

Items belonging to other worlds are represented as large orange jewels if the item is something classified as
progression or small purple jewels if it is not.

For color-blind people, pay attention to the size and speed at which the jewel spins
to tell exactly which one it is:
- No spin - Either a Special1 or 2, if it's small or large respectively.
- Slow spin - Ordinary sub weapon jewel or save jewel. Save jewels will always only ever be in their vanilla spots.
- Fast spin - Item from another world. It will be large if it is possibly progress for someone else or small if it is
- not.

## When the player receives an item, what happens?

When the player receives an item, that item's popup will be displayed in-game as when you would normally pick up the
item.

