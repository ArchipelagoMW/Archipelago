# ALttPEntranceRandomizer

This is a entrance randomizer for _The Legend of Zelda: A Link to the Past_ for the SNES. 

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

May require Fake Flippers, Bunny Revival and Dark Room Navigation. (default: noglitches)

```
--mode [{standard,open}]
```

Select game mode. 

### Standard 
Fixes Hyrule Castle Secret Entrance and Front Door, but may lead to weird rain state issues if you exit through the Hyrule Castle side exits before rescuing Zelda in a full shuffle. (default: open)

### Open

This mode starts with the option to start in your house or the sanctuary, you are free to explore. 

Special notes:

- Uncle already in sewers and most likely does not have a sword.
- Dark rooms do not get a free light cone.
- It may be a while before you find a sword, think of other ways to do damage to enemies. (bombs are a great tool, as well as picking up bushes in over world).

```
--goal [{ganon,pedestal,dungeons}]
```

Select completion goal.

### Ganon (Default)

Standard game completion requiring you to collect the 7 crystals and defeat Ganon.

### Pedestal 

Places a second Triforce at the Master Sword Pedestal. It may still be faster to actually beat Ganon.

### All Dungeons 

Not enforced ingame but considered in the playthrough output.

```
--difficulty [{normal}]
```

Select game difficulty. Affects available itempool. (default: normal)

```
--algorithm [{regular,flood}]
```

Select item filling algorithm. 

### Regular (Default)
The ordinary VT v8.21 algorithm. As unbiased as possible, but may lead to distributions that seem a bit wonky (high likelyhood of ice rod in Turtle Rock, for instance)

### Flood 
Pushes out items starting from Link's House and is slightly biased to placing progression items with less restrictions. 

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

Path to a VT21 normal difficulty rom to use as a base. (default: Base_Rom.sfc)
See http://vt.alttp.run for more details on the normal randomizer.

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

If set, removes Compasses and Maps are removed from the dungeon item pools and replaced by empty chests that may end up anywhere in the world. This may lead to different amount of itempool items being placed in a dungeon than you are used to. (default: False)

```
--heartbeep [{normal,half,quarter,off}]
```

Select frequency of beeps when on low health. (default: normal)

```
--sprite SPRITE
```

Use to select a different sprite sheet to use for Link. Path to a binary file of length 0x7000 containing the sprite data stored at address 0x80000 in the rom. (default: None)
