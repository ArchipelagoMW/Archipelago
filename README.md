# ALttPEntranceRandomizer

This is a entrance randomizer for _The Legend of Zelda: A Link to the Past_ for the SNES.
See http://vt.alttp.run for more details on the normal randomizer.

## Installation

Clone this repository and then run ```Main.py``` (requires Python 3).

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
--mode [{standard,open}]
```

Select game mode. (default: standard)

### Standard 
Fixes Hyrule Castle Secret Entrance and Front Door, but may lead to weird rain state issues if you exit through the Hyrule Castle side exits before rescuing Zelda in a full shuffle.

### Open

This mode starts with the option to start in your house or the sanctuary, you are free to explore. 

Special notes:

- Uncle already in sewers and most likely does not have a sword.
- Sewers do not get a free light cone.
- It may be a while before you find a sword, think of other ways to do damage to enemies. (bombs are a great tool, as well as picking up bushes in over world).

```
--goal [{ganon,pedestal,dungeons,starhunt,triforcehunt}]
```

Select completion goal.

### Ganon (Default)

Standard game completion requiring you to collect the 7 crystals and defeat Ganon.

### Pedestal 

Places the Triforce at the Master Sword Pedestal. Ganon cannot be damaged.

### All Dungeons 

Ganon cannot be damaged until all dungeons (including Hyrule Castle Tower) are cleared.

### Star Hunt

15 Power Stars are placed in the world. Find 10 of them to finish the game. Ganon cannot be damaged.

### Triforce Hunt

The triforce is broken into 3 pieces. Can you find all of them? Ganon cannot be damaged.

```
--difficulty [{normal}]
```

Select game difficulty. Affects available itempool. (default: normal)

```
--algorithm [{freshness,flood,vt21,vt22,restrictive}]
```

Select item filling algorithm. 

### Restrictive (Default)
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

If set, will only ensure the goal can be achieved, but not necessarily that all locations are reachable. Currently only affects restrictive algorithm.

```
--suppress_rom
```

If set, will not produce a patched rom as output. Useful to batch generate spoilers for statistical analysis.
