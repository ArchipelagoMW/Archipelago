# Donkey Kong Country 2

## Where is the options page?

The [player options page for this game](../player-options) contains all the options you need to configure and export a 
config file.

## What does randomization do to this game?

Access to each world, Kong abilities, animal buddies, barrels and even Dixie or Diddy are randomized in the multiworld. The requirements for getting inside The Flying Krock can be set to either require beating bosses or finding a world access item, while accessing Krocodrile Kore requires finding a customizable amount of Rocks.

The game will be marked as completed once you beat K.Rool at The Flying Krock, Krocodile Kore or even beating him twice at both locations.

## What Donkey Kong Country 2 items can appear in other players' worlds?
- World unlocks
- Diddy/Dixie
- Abilities
- Animal buddies
- Barrels
- DK Coins
- Kremkoins
- Banana Coins
- Instant DK Barrels

## What is considered a location check in Donkey Kong Country 2?
- Clearing a level
- Finishing a bonus
- Optionally:
    - Collecting a DK Coin
    - Collecting KONG letters
    - Grabbing banana bunches
    - Grabbing banana coins
    - Obtaining a balloon
    - Finishing a Swanky quiz

## When the player receives an item, what happens?
A sound effect will play based on the type of item received, and the effects of the item will be immediately applied, 
such as unlocking the use of a new ability mid-stage. If the effects of the item cannot be fully applied (such as receiving 
an Instant DK Barrel with both Kongs alive), the remaining are withheld until they can be applied.

## Quality of Life
The implementation features some enhancements to the original game's systems which attempt to make Donkey Kong Country 2 a 
much smoother experience.
- **Exit levels at any time:** Allows players to exit from unfinished levels with `START` + `SELECT`
- **Open world:** Can access any level in each world after unlocking said world
- **Wrinkly Info:** Wrinkly now offers hints about all of your important items in the session, however, their helpfulness can vary as the hints come in book form and she may have outdated info!
- **Cranky Hints:** Cranky has access to all sorts of information about what's inside a location in the current player's world. His hints may be a bit weird at times as he only visited the location and possibly didn't properly scout the item inside.

## Swanky Trivia
Swanky now has trivia from both the original game and the games present in the session*. The answer is also shuffled from the original position when it comes to the original questions. The additional questions were created by the Archipelago Community.

*as long they actually have questions in the database

## What is EnergyLink?
EnergyLink is an energy storage supported by certain games that is shared across all worlds in a multiworld. In Donkey Kong Country 2, when enabled, deposits a certain amount of energy labeled "Banana" to the EnergyLink pool. Only 10% of a banana is successfully sent to the EnergyLink pool, this can be enhanced up to 15% after receiving `Banana Extractinator` items.

Energy from the EnergyLink pool can be transmuted into Instant DK Barrels for 25 EnergyLink bananas. This can be only achieved via SNIClient with the `/barrel` command.

## Unique Local Commands
- `/barrel` Invokes a DK Barrel at the player's position. Can be queued multiple times.
