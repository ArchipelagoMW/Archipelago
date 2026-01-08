# Donkey Kong Country

## Where is the options page?

The [player options page for this game](../player-options) contains all the options you need to configure and export a 
config file.

## What does randomization do to this game?

Access to each world, Kong abilities, animal buddies, barrels and even Donkey or Diddy are randomized in the multiworld. The requirements for getting inside Gangplank Galleon is collecting enough Big Banana items which are found at Boss Levels.

The game will be marked as completed once you enter the Banana Hoard and it's full of bananas.

## What Donkey Kong Country items can appear in other players' worlds?
- World unlocks
- Diddy/Donkey
- Abilities
- Animal buddies
- Barrels
- Minecarts
- Platforms
- Tires
- Backup DK Barrels

## What is considered a location check in Donkey Kong Country?
- Clearing a level
- Finishing a bonus
- Optionally:
    - Collecting KONG letters
    - Grabbing banana bunches
    - Grabbing animal tokens
    - Obtaining a balloon

## When the player receives an item, what happens?
A sound effect will play based on the type of item received, and the effects of the item will be immediately applied, 
such as unlocking the use of a new ability mid-stage. If the effects of the item cannot be fully applied (such as receiving an Backup DK Barrel with both Kongs alive), the remaining are withheld until they can be applied.

## Quality of Life
The implementation features some enhancements to the original game's systems which attempt to make Donkey Kong Country a much smoother experience.
- **Exit levels at any time:** Allows players to exit from unfinished levels with `START` + `SELECT`
- **Open world:** Can access any level in each world after unlocking said world
- **Forget the level Checkpoint status:** By holding `L` or `R` at the map, the game will forget the player has reached its Checkpoint Barrel

## What is EnergyLink?
EnergyLink is an energy storage supported by certain games that is shared across all worlds in a multiworld. In Donkey Kong Country, when enabled, deposits a certain amount of energy labeled "Banana" to the EnergyLink pool. Only 10% of a banana is successfully sent to the EnergyLink pool, this can be enhanced up to 15% after receiving `Banana Extractinator` items.

Energy from the EnergyLink pool can be transmuted into Backup DK Barrels for 20 EnergyLink bananas. This can be only achieved via SNIClient with the `/barrel` command.

## Unique Local Commands
- `/barrel` Invokes a DK Barrel at the player's position. Can be queued multiple times.
