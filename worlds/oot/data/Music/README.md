To load custom sequences, you need to have a raw N64 sequence file with a `.seq` file extension and a corresponding file with the same name but with a `.meta` file extension. The `.meta` file should be a plaintext file with two lines. The first line is the name of the sequence to be displayed in the cosmetic log, and the second line is the instrument set number, in base 16.

For example, if there is a sequence file `Foo.seq` then you need a meta file `Foo.meta` that could contain
```
Awesome Name
C
```

Additionally, if the sequence is to be shuffled with the non-looping fanfares, a third line must exist containing the word 'fanfare'.

Any sub-directories in this folder will also be read from, but the .meta file and matching .seq file must be in the same folder.

Sequences are in the seq64 format. Other known games that use this format and may be compatible are (list from https://github.com/sauraen/seq64)
```
Super Mario 64
Mario Kart 64
Yoshi's Story
Legend of Zelda: Majora's Mask
1080 Snowboarding
F-ZERO X
Lylat Wars
Pokemon Stadium
Pokemon Stadium 2
Wave Race 64
```

There are also tools available to help convert midi files to valid seq64 files.

The instrument list is as follows (from https://sites.google.com/site/deathbasketslair/zelda/ocarina-of-time/instrument-sets-and-sequences and https://github.com/sauraen/seq64):
```
0x00 - Ocarina Songs?
0x01 - Actor Sounds
0x02 - Nature Sounds
0x03 - Hyrule Field (often the best choice, main orchestra with percussion)
0x04 - Deku Tree
0x05 - Castle Market
0x06 - Title Screen
0x07 - Jabu Jabu's Belly
0x08 - Kakariko Village (Guitar)
0x09 - Fairy Fountain (Harp, Strings)
0x0A - Fire Temple
0x0B - Dodongo's Cavern
0x0C - Forest Temple
0x0D - Lon Lon Ranch
0x0E - Goron City
0x0F - Kokiri Forest
0x10 - Spirit Temple
0x11 - Horse Race
0x12 - Warp Songs
0x13 - Goddess Cutscene
0x14 - Shooting Gallery
0x15 - Zora's Domain
0x16 - Shop
0x17 - Ice Cavern
0x18 - Shadow Temple
0x19 - Water Temple
0x1A - Unused Piano
0x1B - Gerudo Valley
0x1C - Lakeside Laboratory
0x1D - Kotake and Koume's Theme
0x1E - Ganon's Castle (Organ)
0x1F - Inside Ganon's Castle
0x20 - Ganondorf Battle
0x21 - Ending 1
0x22 - Ending 2
0x23 - Game Over / Fanfares
0x24 - Owl
0x25 - Unknown (probably should not use)
```
