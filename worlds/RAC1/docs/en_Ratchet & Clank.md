# Ratchet & Clank Archipelago
An Archipelago implementation for Ratchet & Clank


## Setup Guide
To get started or for troubleshooting, see [the Setup Guide](https://github.com/Panda291/Archipelago/blob/main/worlds/RAC1/docs/setup_en.md).


## What does randomization do to this game?
In Ratchet & Clank 1, all Gadgets, Gold Bolts and Planet Infobots are shuffled into the multiworld, giving the game a greater variety in routing to complete the end goal.


## What is the goal of Ratchet & Clank when randomized?
The end goal of the randomizer game is to defeat Ultimate Supreme Executive Chairman Drek in planet Veldin.


## Which items can be in another player's world?
All Gadgets/Items, Gold Bolts and Planet Infobots can be shuffled in other players' worlds.


## What does another world's item look like in Ratchet & Clank?
There is no model replacement support yet so all items will their vanilla appearance.


## What versions of the Ratchet & Clank are supported?
Only the PS3 version of the game is supported: NPEA00385


## When the player receives an item, what happens?
The player will immediately have their inventory updated and receive a notification in the Client and a HUD message in-game.

### Aside from item locations being shuffled, how does this differ from the vanilla game?
Some of the changes include:
  - The Metal Detector has a 50x multiplier for found bolts.
  - If you turn on cheat mode in the lobby, you can enable ghost ratchet for 1 second by pressing R1 while paused. (ghost ratchet means you can walk through walls, among other things speedrunners use)
  - You can also play in coop in the same world as your friend. One person sets up a lobby and fills in the archipelago details, the others can join for jolly cooperation.

## Are there any other things I should know?
- It has come to my attention some people have been using save/load to get back to their ship if they get stuck. This is not a scenario I had anticipated and as such is untested. For now avoid using it, instead use the quit game option and create a new lobby (or reconnect if another player is still in)
- Any location that costs more than 7500 bolts has the metal detector listed as a requirement

# Credit
The following wonderful people helped on this project:

[Bordplate](https://github.com/bordplate) - Client
[evilwb](https://github.com/evilwb/APRac2) - APWorld
[Myth197](https://github.com/Myth197) - APWorld
[SharloBun](https://www.twitch.tv/sharlobun) - Playtesting
Amondo - Playtesting