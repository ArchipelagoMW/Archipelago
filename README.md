# ALttPEntranceRandomizer

This is a entrance randomizer for _The Legend of Zelda: A Link to the Past_ for the SNES.
See https://alttpr.com/ for more details on the normal randomizer.

# Installation

Clone this repository and then run ```EntranceRandomizer.py``` (requires Python 3).

Alternatively, run ```Gui.py``` for a simple graphical user interface.

For releases, a Windows standalone executable is available for users without Python 3.

# Settings

## Game Mode

### Standard

Fixes Hyrule Castle Secret Entrance and Front Door, but may lead to weird rain state issues if you exit through the Hyrule Castle side exits before rescuing Zelda in a full shuffle.

Gives lightcone in Hyrule Castle Sewers even without the Lamp.

### Open

This mode starts with the option to start in your house or the sanctuary, you are free to explore.

Special notes:

- Uncle already in sewers and most likely does not have a sword.
- Sewers do not get a free light cone.
- It may be a while before you find a sword, think of other ways to do damage to enemies. (bombs are a great tool, as well as picking up bushes in over world).

### Swordless

This mode removes all swords from the itempool. Otherwise just like open.

Special notes:

- The Medallions to open Misery Mire and Turtle Rock can be used without a sword if you stand on the symbol.
- The curtains in Skull Woods and Hyrule Castle Tower that normally require a sword to cut have been removed.
- Ganon takes damage from the Hammer.
- The magic barrier to Hyrule Castle Tower can be broken with a Hammer.
- The Hammer can be used to activate the Ether and Bombos tablets.

## Game Logic
This determines the Item Requirements for each location.

### No Glitches

The game can be completed without knowing how to perform glitches of any kind.

### Minor Glitches

May require Fake Flippers, Bunny Revival.

### No Logic

Items are placed without regard for progression or the seed being possible. Major glitches are likely required.

## Game Goal

### Ganon

Standard game completion requiring you to collect the 7 crystals, defeat Agahnim 2 and then beat Ganon.

### Pedestal

Places the Triforce at the Master Sword Pedestal. Ganon cannot be damaged.

### All Dungeons

Ganon cannot be damaged until all dungeons (including Hyrule Castle Tower and Ganons Tower) are cleared.

### Triforce Hunt

Triforce Pieces are added to the item pool, and some number of them being found will trigger game completion. Ganon cannot be damaged.
By default 30 Triforce Pieces are placed while 20 are needed to beat the game. Both values can be adjusted with the custom item pool feature.

### Crystals

Standard game completion requiring you to collect the 7 crystals and then beat Ganon.

This is only noticeably different if the the Ganon shuffle option is enabled.

## Game Difficulty

### Easy

This setting doubles the number of swords, shields, armors, bottles, and silver arrows in the item pool.
This setting will also triple the number of Lamps available, and all will be obtainable before dark rooms.
Within dungeons, the number of items found will be displayed on screen if there is no timer.

### Normal

This is the default setting that has an item pool most similar to the original
The Legend of Zelda: A Link to the Past.

### Hard

This setting reduces the availability of a variety of minor helpful items, most notably
limiting the player to two bottles, a Tempered Sword, and Blue Mail. Several minor game
mechanics are adjusted to increase difficulty, most notably weakening potions and preventing
the player from having fairies in bottles.

### Expert

This setting is a more extreme version of the Hard setting. Potions are further nerfed, the item
pool is less helpful, and the player can find no armor, only a Master Sword, and only a single bottle.

### Insane

This setting is a modest step up from Expert. The main difference is that the player will never find any
additional health.

## Timer Setting

### None

Does not invoke a timer.

### Display

Displays a timer on-screen but does not alter the item pool.
This will prevent the dungeon item count feature in Easy and Keysanity from working.

### Timed

Displays a count-up timer on screen that can be reduced with Green Clocks and Blue Clocks or
increased with Red Clocks found in chests that will be added to the itempool.

### Timed-OHKO

Displays a countdown timer on screen that, when it hits zero, will put the player into a one hit
knockout state until more time is added to the clock via some of the Green Clocks that will be added
to the itempool.

### OHKO

The player will be in a one hit knockout state the entire game. This is the same as Timed-OHKO except
without the Clock items and the timer permanently at zero.

### Timed-countdown

Displays a countdown timer on screen that can be increased with Green Clocks and Blue Clocks or
decreased with Red Clocks found in chests that will be added to the itempool. The goal of this mode
is to finish the game without the timer reaching zero, but the game will continue uninterrupted if
the player runs out of time.

## Progressive equipment

Determines if Sword, Shield, and gloves are progressive (upgrading in sequence) or not.

### On (Default)

This setting makes swords, shields, armor, and gloves progressive. The first of any type of equipment found
by the player will be the lowest level item, and each subsequent find of a category will upgrade that type of
equipment.

### Off

This setting makes swords, shields, armor, and gloves non-progressive. All of the items of these types will be
randomly placed in chests, and the player could find them in any order and thus instantly receive high level equipment.
Downgrades are not possible; finding a lower level piece of equipment than what is already in the player's possession
will simply do nothing.

### Random

This setting makes swords, shields, armor, and gloves randomly either progressive or not. Each category is independently
randomized.

## Item Distribution Algorithm

Determines how the items are shuffled.

### Balanced
This is a variation of VT26 that aims to strike a balance between the overworld heavy VT25 and the dungeon heavy VT26 algorithm.
It does this by reshuffling the remaining locations after placing dungeon items.

### VT26
Items and locations are shuffled like in VT25, and dungeon items are now placed using the same algorithm. When Ganon is not
shuffled it includes a slight deliberate bias against having too many desireable items in Ganon's Tower to help counterbalance
the sheer number of chests in that single location.

### VT25
Items and locations are shuffled and placed from the top of the lists. The only thing preventing an item from being placed into a spot
is if is absolutely impossible to be there given the previous made placement choices. Leads to very uniform but guaranteed solvable distributions.

### VT22
The ordinary VT v8.22 algorithm. Fixes issues in placement in VT21 by discarding all previously skipped and unfilled locations
after 2/3 of the progression items were placed to prevent stale late game locations from soaking up the same items all the time.

### VT21
The ordinary VT v8.21 algorithm. Unbiased placement of items into unlocked locations, placing items that unlock new locations first.
May lead to distributions that seem a bit wonky (high likelyhood of ice rod in Turtle Rock, for instance)

### Flood
Pushes out items starting from Link's House and is slightly biased to placing progression items with less restrictions. Use for relatively simple distributions.

### Freshness
Alternative approach to VT22 to improve on VT21 flaws. Locations that are skipped because they are currently unreachable increase in
staleness, decreasing the likelihood of receiving a progress item.

## Entrance Shuffle Algorithm

Determines how locations are shuffled. In all modes other than Insanity and the similar legacy versions, holes shuffle as a pair with the connecting cave and the front
two sections of Skull Woods remain confined to the general Skull Woods area. Link's house is never shuffled as a design decision.

### Vanilla

Places entrances in the same locations they were in the original The Legend of Zelda: A Link to the Past.

### Simple

Shuffles dungeon entrances between each other and keeps all 4-entrance dungeons confined to one location such that dungeons will one to one swap with each other.
Other than on Light World Death Mountain, interiors are shuffled but still connect the same points on the overworld. On Death Mountain, entrances are connected more freely.

### Restricted

Uses dungeon shuffling from Simple but freely connects remaining entrances. Caves and dungeons with multiple entrances will be confined to one world.

### Full

Mixes cave and dungeon entrances freely. Caves and dungeons with multiple entrances will be confined to one world.

### Crossed

Mixes cave and dungeon entrances freely, but now connector caves and dungeons can link Light World and Dark World.

### Insanity

Decouples entrances and exits from each other and shuffles them freely. Caves that were single entrance in vanilla still can only exit to the same location from which they were entered.

### Legacy Variants

Similar to the base shuffles, but the distinction between single entrance and multi-entrance caves from older versions of the randomizer is maintained.
Madness_Legacy is the more similar to the modern Insanity. Insanity_Legacy has fake worlds and guaranteed Moon Pearl and Magic Mirror for a very different experience.

### Dungeon Variants

The dungeon variants only mix up dungeons and keep the rest of the overworld vanilla.

## Heartbeep Sound Rate

Select frequency of beeps when on low health. Can completely disable them.

## Heart Color

Select the color of Link's hearts.

## Menu Speed

A setting that lets the player set the rate at which the menu opens and closes.

## Create Spoiler Log

Output a Spoiler File.

## Do not Create Patched Rom

If set, will not produce a patched rom as output. Useful in conjunction with the spoiler log option to batch
generate spoilers for statistical analysis.

## Enable L/R button quickswapping

Use to enable quick item swap with L/R buttons. Press L and R together to switch the state of items like the Mushroom/Powder pair.

## Keysanity

This setting allows dungeon specific items (Small Key, Big Key, Map, Compass) to be distributed anywhere in the world and not just
in their native dungeon. Small Keys dropped by enemies or found in pots are not affected. The chest in southeast Skull Woods that
is traditionally a guaranteed Small Key still is. These items will be distributed according to the v26/balanced algorithm, but
the rest of the itempool will respect the algorithm setting. Music for dungeons is randomized so it cannot be used as a tell
for which dungeons contain pendants and crystals; finding a Map for a dungeon will allow the overworld map to display its prize.

## Retro

This setting turns all Small Keys into universal Small Keys that can be used in any dungeon and are distributed across the world.
The Bow now consumed rupees to shoot; the cost is 10 rupees per Wood Arrow and 50 per Silver Arrow. Shooting Wood Arrows requires
the purchase of an arrow item from shops, and to account for this and the dynamic use of keys, both Wood Arrows and Small Keys will
be added to several shops around the world. Four "take any" caves are added that allow the player to choose between an extra Heart
Container and a Bottle being filled with Blue Potion, and one of the four swords from the item pool is placed into a special cave as
well. The five caves that are removed for these will be randomly selected single entrance caves that did not contain any items or any shops.
In further concert with the Bow changes, all arrows under pots, in chests, and elsewhere in the seed will be replaced with rupees.

## Place Dungeon Items

If not set, Compasses and Maps are removed from the dungeon item pools and replaced by empty chests that may end up anywhere in the world.
This may lead to different amount of itempool items being placed in a dungeon than you are used to.

## Only Ensure Seed Beatable

If set, will only ensure the goal can be achieved, but not necessarily that all locations are reachable. Currently only affects VT25, VT26 and balanced algorithms.

## Include Ganon's Tower and Pyramid Hole in Shuffle pool

If set, Ganon's Tower is included in the dungeon shuffle pool and the Pyramid Hole/Exit pair is included in the Holes shuffle pool. Ganon can not be defeated until the primary goal is fulfilled.
This setting removes any bias against Ganon's Tower that some algorithms may have.

## Include Helpful Hints

If set, the 15 telepathic tiles and 5 storytellers scattered about Hyrule will give helpful hints about various items and entrances. An exact breakdown of the hint
distribution is provided as an included text file.

## Use Custom Item Pool

If set, the item pool normally associated with your difficulty setting is replaced by the item pool specified in the custom tab. This feature is only supported when the randomizer is run
via the GUI; attempting to set this via the command line does nothing.

## Seed

Can be used to set a seed number to generate. Using the same seed with same settings on the same version of the entrance randomizer will always yield an identical output.

## Count

Use to batch generate multiple seeds with same settings. If a seed number is provided, it will be used for the first seed, then used to derive the next seed (i.e. generating 10 seeds with the same seed number given will produce the same 10 (different) roms each time).

# Command Line Options

```
-h, --help            
```

Show the help message and exit.

```
--create_spoiler      
```

Output a Spoiler File (default: False)

```
--logic [{noglitches,minorglitches,nologic}]
```

Select the game logic (default: noglitches)

```
--mode [{standard,open,swordless}]
```

Select the game mode. (default: open)

```
--goal [{ganon,pedestal,dungeons,triforcehunt,crystals}]
```

Select the game completion goal. (default: ganon)

```
--difficulty [{easy,normal,hard,expert,insane}]
```

Select the game difficulty. Affects available itempool. (default: normal)

```
--timer [{none,display,timed,timed-ohko,ohko,timed-countdown}]
```

Select the timer setting. (default: none)

```
--progressive [{on,off,random}]
```

Select the setting for progressive equipment. (default: on)

```
--algorithm [{freshness,flood,vt21,vt22,vt25,vt26,balanced}]
```

Select item distribution algorithm. (default: balanced)

```
--shuffle [{default,simple,restricted,full,crossed,insanity,restricted_legacy,full_legacy,madness_legacy,insanity_legacy,dungeonsfull,dungeonssimple}]
```

Select entrance shuffle algorithm. (default: full)

```
--rom ROM
```

Path to a Japanese 1.0 A Link to the Past Rom. (default: Zelda no Densetsu - Kamigami no Triforce (Japan).sfc)

```
--loglevel [{error,info,warning,debug}]
```

Select level of logging for output. (default: info)

```
--seed SEED           
```

Define seed number to generate. (default: None)

```
--count COUNT         
```

Set the count option (default: None)

```
--quickswap
```

Use to enable quick item swap with L/R buttons. (default: False)

```
--fastmenu [{normal,instant,double,triple,quadruple,half}]
```

Alters the rate at which the menu opens and closes. (default: normal)


```
--disablemusic
```

Disables game music, resulting in the game sound being just the SFX. (default: False)

```
--keysanity
```

Enable Keysanity (default: False)

```
--retro
```

Enable Retro mode (default: False)

```
--nodungeonitems
```

If set, Compasses and Maps are removed from the dungeon item pools and replaced by empty chests that may end up anywhere in the world.
This may lead to different amount of itempool items being placed in a dungeon than you are used to. (default: False)

```
--heartbeep [{normal,half,quarter,off}]
```

Select frequency of beeps when on low health. (default: normal)

```
--heartcolor [{red,blue,green,yellow,random}]
```

Select the color of Link\'s heart meter. (default: red)

```
--sprite SPRITE
```

Use to select a different sprite sheet to use for Link. Path to a binary file of length 0x7000 containing the sprite data stored at address 0x80000 in the rom. (default: None)

```
--beatableonly
```

Enables the "Only Ensure Seed Beatable" option (default: False)

```
--hints
```

Enables helpful hints from storytellers and telepathic tiles (default: False)

```
--no-shuffleganon
```

Disables the "Include Ganon's Tower and Pyramid Hole in Shuffle pool" option. (default: Enabled)

```
--suppress_rom
```

Enables the "Do not Create Patched Rom" option. (default: False)

```
--gui
```

Open the graphical user interface. Preloads selections with set command line parameters.
