# A Link to the Past Randomizer Plando Guide

## Configuration
1. Plando features have to be enabled first, before they can be used (opt-in).
2. To do so, go to your installation directory (Windows default: C:\ProgramData\BerserkerMultiWorld), 
   then open the host.yaml file therein with a text editor.
3. In it, you're looking for the option key "plando_options", 
   to enable all plando modules you can set the value to "bosses, items, texts, connections"

## Modules

### Bosses

- This module is enabled by default and available to be used on 
  [https://archipelago.gg/generate](https://archipelago.gg/generate)
- Plando versions of boss shuffles can be added like any other boss shuffle option in a yaml and weighted.
- Boss Plando works as a list of instructions from left to right, if any arenas are empty at the end, 
  it defaults to vanilla
- Instructions are separated by a semicolon
- Available Instructions:
  -  Direct Placement: 
     - Example: "Eastern Palace-Trinexx"
     - Takes a particular Arena and particular boss, then places that boss into that arena
     - Ganons Tower has 3 placements, "Ganons Tower Top", "Ganons Tower Middle" and "Ganons Tower Bottom"
  - Boss Placement:
     - Example: "Trinexx"
     - Takes a particular boss and places that boss in any remaining slots in which this boss can function.
     - In this example, it would fill Desert Palace, but not Tower of Hera.
  - Boss Shuffle:
     - Example: "simple"
     - Runs a particular boss shuffle mode to finish construction instead of vanilla placement, typically used as a last instruction.
- [Available Bosses](https://github.com/Berserker66/MultiWorld-Utilities/blob/65fa39df95c90c9b66141aee8b16b7e560d00819/Bosses.py#L135)
- [Available Arenas](https://github.com/Berserker66/MultiWorld-Utilities/blob/65fa39df95c90c9b66141aee8b16b7e560d00819/Bosses.py#L186)

#### Examples:
```yaml
boss_shuffle:
  Turtle Rock-Trinexx;basic: 1
  full: 2
  Mothula: 3
  Ganons Tower Bottom-Kholdstare;Trinexx;Kholdstare: 4
```
1. Would be basic boss shuffle but prevent Trinexx from appearing outside of Turtle Rock, 
   as there's only one Trinexx in the pool
2. Regular full boss shuffle. With a 2 in 10 chance to occur.
3. A Mothula Singularity, as Mothula works in any arena.
4. A Trinexx -> Kholdstare Singularity that prevents ice Trinexx in GT



### Text
- This module is disabled by default.
- Has the options "text", "at" and "percentage"
- percentage is the percentage chance for this text to be placed, can be omitted entirely for 100%
- text is the text to be placed. 
  - can be weighted.
  - \n is a newline. 
  - @ is the entered player's name.
  - Warning: Text Mapper does not support full unicode.
  - [Alphabet](https://github.com/Berserker66/MultiWorld-Utilities/blob/65fa39df95c90c9b66141aee8b16b7e560d00819/Text.py#L756)
- at is the location within the game to attach the text to.
  - can be weighted.
  - [List of targets](https://github.com/Berserker66/MultiWorld-Utilities/blob/65fa39df95c90c9b66141aee8b16b7e560d00819/Text.py#L1498)
   
#### Example
```yaml
plando_texts:
  - text: "This is a plando.\nYou've been warned."
    at:
      uncle_leaving_text: 1
      uncle_dying_sewer: 1
    percentage: 50
```
![Uncle Example](https://cdn.discordapp.com/attachments/731214280439103580/794953870903083058/unknown.png)
This has a 50% chance to trigger at all, if it does, 
it throws a coin between "uncle_leaving_text" and "uncle_dying_sewer", then places the text 
"This is a plando.\nYou've been warned." at that location.
