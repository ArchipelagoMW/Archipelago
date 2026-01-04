# A Link to the Past Randomizer Plando Guide

## Configuration

1. All plando options are enabled by default, except for "items plando" which has to be enabled before it can be used (opt-in).
2. To enable it, go to your installation directory (Windows default: `C:\ProgramData\Archipelago`), then open the host.yaml
   file with a text editor.
3. In it, you're looking for the option key `plando_options`. To enable all plando modules you can set the value
   to `bosses, items, texts, connections`

## Modules

### Bosses

- This module is enabled by default and available to be used on [https://archipelago.gg/generate](/generate)
- Plando versions of boss shuffles can be added like any other boss shuffle option in a yaml and weighted.
- Boss Plando works as a list of instructions from left to right, if any arenas are empty at the end, it defaults to
  vanilla.
- Instructions are separated by a semicolon.
- Available Instructions:
    - Direct Placement:
        - Example: `Eastern Palace-Trinexx`
        - Takes a particular Arena and particular boss, then places that boss into that arena
        - Ganons Tower has 3 placements, `Ganons Tower Top`, `Ganons Tower Middle` and `Ganons Tower Bottom`
    - Boss Placement:
        - Example: `Trinexx`
        - Takes a particular boss and places that boss in any remaining slots in which this boss can function.
        - In this example, it would fill Desert Palace, but not Tower of Hera.
        - If no other options are provided this will follow normal singularity rules with that boss.
    - Boss Shuffle:
        - Example: `basic`
            - Runs a particular boss shuffle mode to finish construction instead of vanilla placement, typically used as
              a last instruction.
            - Supports `random` which will choose a random option from the normal choices.
            - If one is not supplied any remaining locations will be unshuffled unless a single specific boss is
              supplied in which case it will use singularity as noted above.
- [Available Bosses](https://github.com/ArchipelagoMW/Archipelago/blob/main/worlds/alttp/Bosses.py#L135)
- [Available Arenas](https://github.com/ArchipelagoMW/Archipelago/blob/main/worlds/alttp/Bosses.py#L150)

#### Examples

```yaml
boss_shuffle:
  Turtle Rock-Trinexx;basic: 1
  full: 2
  Mothula: 3
  Ganons Tower Bottom-Kholdstare;Trinexx;Kholdstare: 4
```

1. Would be basic boss shuffle but prevent Trinexx from appearing outside of Turtle Rock, as there's only one Trinexx in
   the pool
2. Regular full boss shuffle. With a 2 in 10 chance to occur.
3. A Mothula Singularity, as Mothula works in any arena.
4. A Trinexx -> Kholdstare Singularity that prevents ice Trinexx in GT

### Items

- This module is disabled by default.
- Has the options from_pool, world, percentage, force and either item and location or items and locations
- All of these options support subweights
- percentage is the percentage chance for this block to trigger
    - is a number in the range [0, 100], can be omitted entirely for 100%
- from_pool denotes if the item should be taken from the item pool, or be an additional item entirely.
    - can be true or false, defaults to true when omitted
- world is the target world to place the item
    - ignored if only one world is generated
    - can be a number, to target that slot in the multiworld
    - can be a name, to target that player's world
    - can be a list of names, to target those players' worlds
    - can be true, to target any other player's world
    - can be false, to target own world and is the default
    - can be null, to target a random world
- force is either `silent`, `true` or `false`.
    - `true` means the item has to be placed, or the generator aborts with an exception.
    - `false` means the generator logs a warning if the placement can't be done.
    - `silent` means that this entry is entirely ignored if the placement fails and is the default.
- Single Placement
    - place a single item at a single location
    - item denotes the Item to place
    - location denotes the Location to place it into
- Multi Placement
    - place multiple items into multiple locations, until either list is exhausted.
    - items denotes the items to use, can be given a number to have multiple of that item
    - locations lists the possible locations those items can be placed in
    - placements are picked randomly, not sorted in any way
- Warning: Placing non-Dungeon Prizes on Prize locations and Prizes on non-Prize locations will break the game in
  various ways.
- [Available Items](https://github.com/ArchipelagoMW/Archipelago/blob/main/worlds/alttp/Items.py#L52)
- [Available Locations](https://github.com/ArchipelagoMW/Archipelago/blob/main/worlds/alttp/Regions.py#L434)

#### Examples

```yaml
plando_items:
  - item: # 1
      Lamp: 1
      Fire Rod: 1
    location: Link's House
    from_pool: true
    world: true
    percentage: 50
  - items: # 2
      Progressive Sword: 4
      Progressive Bow: 1
      Progressive Bow (Alt): 1
    locations:
      - Desert Palace - Big Chest
      - Eastern Palace - Big Chest
      - Tower of Hera - Big Chest
      - Swamp Palace - Big Chest
      - Thieves' Town - Big Chest
      - Skull Woods - Big Chest
      - Ice Palace - Big Chest
      - Misery Mire - Big Chest
      - Turtle Rock - Big Chest
      - Palace of Darkness - Big Chest
    world: false
  - items: # 3
      Red Pendant: 1
      Green Pendant: 1
      Blue Pendant: 1
    locations:
      - Desert Palace - Prize
      - Eastern Palace - Prize
      - Tower of Hera - Prize
    from_pool: true
```

1. has a 50% chance to occur, which if it does places either the Lamp or Fire Rod in one's own Link's House and removes
   the picked item from the item pool.
2. Always triggers and places the Swords and Bows into one's own Big Chests
3. Locks Pendants to The Light World and therefore Crystals to dark world

### Texts

- Has the options `text`, `at`, and `percentage`
- All of these options support subweights
- percentage is the percentage chance for this text to be placed, can be omitted entirely for 100%
- text is the text to be placed.
    - `\n` is a newline.
    - `@` is the entered player's name.
    - Warning: Text Mapper does not support full unicode.
    - [Alphabet](https://github.com/ArchipelagoMW/Archipelago/blob/main/worlds/alttp/Text.py#L758)
- at is the location within the game to attach the text to.
    - [List of targets](https://github.com/ArchipelagoMW/Archipelago/blob/main/worlds/alttp/Text.py#L1499)

#### Example

```yaml
plando_texts:
  - text: "This is a plando.\nYou've been warned."
    at:
      uncle_leaving_text: 1
      uncle_dying_sewer: 1
    percentage: 50
```

![Example plando text at Uncle](https://cdn.discordapp.com/attachments/731214280439103580/794953870903083058/unknown.png)
This has a 50% chance to trigger at all. If it does, it throws a coin between `uncle_leaving_text`
and `uncle_dying_sewer`, then places the text "This is a plando. You've been warned." at that location.

### Connections

- Has the options `percentage`, `entrance`, `exit` and `direction`.
- All options support subweights
- percentage is the percentage chance for this to be connected, can be omitted entirely for 100%
- Any Door has 4 total directions, as a door can be unlinked like in insanity ER
- entrance is the overworld door
- exit is the underworld exit
- direction can be `both`, `entrance` or `exit`
- doors can be found
  in [this file](https://github.com/ArchipelagoMW/Archipelago/blob/main/worlds/alttp/EntranceShuffle.py#L3852)

#### Example

```yaml
plando_connections:
  - entrance: Links House
    exit: Hyrule Castle Exit (West)
    direction: both
  - entrance: Hyrule Castle Entrance (West)
    exit: Links House Exit
    direction: both
```

The first block connects the overworld entrance that normally leads to Link's House to put you into the HC West Wing
instead, exiting from within there will put you at the Overworld exiting Link's House.

Without the second block, you'd still exit from within Link's House to outside Link's House and the left side Balcony
Entrance would still lead into HC West Wing
