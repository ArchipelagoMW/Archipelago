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

### Gannon (Default)

Standard game completion requiring you to collect the 7 crystals and defeat Gannon.

### Pedestal 

Places a second Triforce at the Master Sword Pedestal, the playthrough may still deem Ganon to be the easier goal. 

### All Dungeons 

Not enforced ingame but considered in the rules. 

```
--difficulty [{normal}]
```

Select game difficulty. Affects available itempool. (default: normal)

```
--algorithm [{regular,flood}]
```

Select item filling algorithm. 

### Regular (Default)
The ordinary VT algorithm. 

### Flood 
Pushes out items starting from Link's House and is slightly biased to placing progression items with less restrictions. 

```
--shuffle [{default,simple,restricted,full,madness,dungeonsfull,dungeonssimple}]
```

Select Entrance Shuffling Algorithm. 

### Default

Is the Vanilla layout. Simple shuffles Dungeon Entrances/Exits between each other and keeps all 4-entrance dungeons confined to one location. All caves outside of death mountain are shuffled in pairs. 

### Full (Default)

Mixes cave and dungeon entrances freely. 

### Restricted

Uses Dungeons shuffling from Simple But freely connects remaining entrances. 

### Madness

Decouples entrances and exits from each other and shuffles them freely, only ensuring that no fake Light/Dark World happens and all locations are reachable. The dungeon variants only mix up dungeons and keep the rest of the overworld vanilla.

```
--openrom OPENROM     
```

Path to a VT21 open normal difficulty rom to use as a base. (default: Open_Base_Rom.sfc)

```
--standardrom STANDARDROM
```

Path to a VT21 standard normal difficulty rom to use as a base. (default: Standard_Base_Rom.sfc)

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

Use to batch generate multiple seeds with same settings. 
If --seed is provided, it will be used for the first seed, then used to derive the next seed (i.e. generating 10 seeds with --seed given will produce the same 10 (different) roms each time). (default: None)
