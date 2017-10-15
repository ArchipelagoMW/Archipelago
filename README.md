# ALttPEntranceRandomizer

This is a entrance randomizer for _The Legend of Zelda: A Link to the Past_ for the SNES.
See http://vt.alttp.run for more details on the normal randomizer.

## Installation

Clone this repository and then run ```EntranceRandomizer.py``` (requires Python 3).

Alternatively, run ```Gui.py``` for a simple graphical user interface.

For releases, a Windows standalone executable is available for users without Python 3.

## Options


```
-h, --help            
```

Show the help message and exit.

```
--create_spoiler      
```

Output a Spoiler File (default: False)

```
--logic [{noglitches,minorglitches}]
```

Select Enforcement of Item Requirements. 

### No Glitches

The game can be completed without knowing how to perform glitches of any kind.

### Minor Glitches 

May require Fake Flippers, Bunny Revival. (default: noglitches)

```
--mode [{standard,open,swordless}]
```

Select game mode. (default: standard)

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

```
--goal [{ganon,pedestal,dungeons,triforcehunt,crystals}]
```

Select completion goal.

### Ganon (Default)

Standard game completion requiring you to collect the 7 crystals, defeat Agahnim 2 and then beat Ganon.

### Pedestal 

Places the Triforce at the Master Sword Pedestal. Ganon cannot be damaged.

### All Dungeons 

Ganon cannot be damaged until all dungeons (including Hyrule Castle Tower and Ganons Tower) are cleared.

### Triforce Hunt

30 Power Stars are placed in the world. Find 20 of them to finish the game. Ganon cannot be damaged.

### Crystals

Standard game completion requiring you to collect the 7 crystals and then beat Ganon.

This is only noticeably different if the --shuffleganon option is enabled.

```
--difficulty [{normal}]
```

Select game difficulty. Affects available itempool. (default: normal)

```
--algorithm [{freshness,flood,vt21,vt22,vt25}]
```

Select item filling algorithm. 

### VT26 (Default)
Items and locations are shuffled like in VT25, and dungeon items are now placed using the same algorithm. It includes 
a slight deliberate bias against having too many desireable items in Ganon's Tower to help counterbalance the sheer number
of chests in that single location.

### VT25 
Items and locations are shuffled and placed from the top of the lists. The only thing preventing an item from being placed into a spot
is if is absolutely impossible to be there given the previous made placement choices. Leads to very uniform but guaranteed solvable distributions.

### VT21
The ordinary VT v8.21 algorithm. Unbiased placement of items into unlocked locations, placing items that unlock new locations first.
May lead to distributions that seem a bit wonky (high likelyhood of ice rod in Turtle Rock, for instance)

### VT22
The ordinary VT v8.21 algorithm. Fixes issues in placement in VT21 by discarding all previously skipped and unfilled locations
after 2/3 of the progression items were placed to prevent stale late game locations from soaking up the same items all the time.

### Flood
Pushes out items starting from Link's House and is slightly biased to placing progression items with less restrictions. Use for relatively simple distributions.

### Freshness
Alternative approach to VT22 to improve on VT21 flaws. Locations that are skipped because they are currently unreachable increase in
staleness, decreasing the likelihood of receiving a progress item.

```
--shuffle [{default,simple,restricted,full,madness,insanity,dungeonsfull,dungeonssimple}]
```

Select Entrance Shuffling Algorithm. 

### Default

Is the Vanilla layout.

### Simple

Shuffles Dungeon Entrances/Exits between each other and keeps all 4-entrance dungeons confined to one location. Outside Light World Death Mountain, interiors are shuffled but still connect the same points
on the overworld. On Death Mountain, entrances are connected more freely.

### Full (Default)

Mixes cave and dungeon entrances freely. 

### Restricted

Uses Dungeons shuffling from Simple but freely connects remaining entrances.

### Madness

Decouples entrances and exits from each other and shuffles them freely, only ensuring that no fake Light/Dark World happens and all locations are reachable.

### Insanity

Madness, but without the light/dark world restrictions. Gives access to Mirror and Moon Pearl from the start.

### Dungeon Variants

The dungeon variants only mix up dungeons and keep the rest of the overworld vanilla.

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

Define seed number to generate. (default: None) Using the same seed with same settings on the same version of the entrance randomizer will always yield an identical output.

```
--count COUNT         
```

Use to batch generate multiple seeds with same settings. 
If --seed is provided, it will be used for the first seed, then used to derive the next seed (i.e. generating 10 seeds with --seed given will produce the same 10 (different) roms each time). (default: None)

```
--quickswap
```

Use to enable quick item swap with L/R buttons. (default: False)

```
--nodungeonitems
```

If set, Compasses and Maps are removed from the dungeon item pools and replaced by empty chests that may end up anywhere in the world. This may lead to different amount of itempool items being placed in a dungeon than you are used to. (default: False)

```
--heartbeep [{normal,half,quarter,off}]
```

Select frequency of beeps when on low health. (default: normal)

```
--sprite SPRITE
```

Use to select a different sprite sheet to use for Link. Path to a binary file of length 0x7000 containing the sprite data stored at address 0x80000 in the rom. (default: None)

```
--beatableonly
```

If set, will only ensure the goal can be achieved, but not necessarily that all locations are reachable. Currently only affects VT25 algorithm.

```
--shuffleganon
```

If set, Ganon's Tower is included in the dungeon shuffle pool and the Pyramid Hole/Exit pair is included in the Holes shuffle pool. Ganon can not be defeated until the primary goal is fulfilled.

Note: This option is under development and may sometimes lead to dungeon and crystal distributions that cannot be solved. If this is the case, the generation will fail. Simply retry with a different seed number if you run into this issue.

```
--suppress_rom
```

If set, will not produce a patched rom as output. Useful to batch generate spoilers for statistical analysis.

```
--gui
```

Open the graphical user interface. Preloads selections with set command line parameters.
