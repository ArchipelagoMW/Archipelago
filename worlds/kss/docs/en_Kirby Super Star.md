# Kirby Super Star

## Where is the options page?

The [player options page for this game](../player-options) contains all the options you need to configure and export a
config file.

## What does randomization do to this game?
### All Subgames
- Access to a subgame will be blocked until the subgame is received from the multiworld.
- Kirby will be unable to absorb copy abilities from enemies until the respective ability has been received from the multiworld.

### Dyna Blade
- Stage progression is locked by receiving `Progressive Stage` from the multiworld.
- Access to each of the EX stages is locked by the multiworld.

### The Great Cave Offensive
- Access to each subsection of The Great Cave is blocked behind collecting a certain amount of treasure, based on the value of each treasure.

### Milky Way Wishes
- Access to each planet within the galaxy is locked by receiving them from the multiworld. 
- Each player is given a single planet to begin with. This can be the `???` planet.

## What is considered a location check in Kirby Super Star?
- Defeating most major bosses/completing stages in each subgame
- Winning the race in each round of Gourmet Race
- Collecting treasures in The Great Cave Offensive
- Collecting Copy Essence Deluxes in Milky Way Wishes
- Interacting with Copy Essences (optional)
- Collecting 1-Ups/Maxim Tomatoes/Invincibility Candy (optional, excludes Gourmet Race)

## When the player receives an item, what happens?
A sound effect will play, and Kirby will immediately receive the effects of that item, such as being able to receive Copy Abilities from enemies that 
give said Copy Ability. Receiving a subgame will require you to refresh the corkboard screen (ie. enter a subgame's title screen then back out) before applying.

## What is the goal of Kirby Super Star?
Two major options control the goal of Kirby Super Star:
- `required_subgame_completions` requires a specific number of subgames to have been completed, from 1 to all 7. 
- `required_subgames` allows for a specific subgame(s) to be required as one of the required completions.

### Goals for each subgame
- Spring Breeze: defeat King Dedede in Castle Dedede
- Dyna Blade: defeat Dyna Blade in her nest
- Gourmet Race: achieve Victory against Dedede
- The Great Cave Offensive: escape the cave after defeating Wham Bam Rock
- Revenge of Meta Knight: complete Chapter 7 and escape the sinking Halberd
- Milky Way Wishes: defeat Marx
- The Arena: defeat Marx in round 20
