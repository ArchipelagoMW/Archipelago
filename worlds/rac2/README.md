# Ratchet & Clank 2 Archipelago
An Archipelago implementation for Ratchet & Clank 2


## Setup Guide
To get started or for troubleshooting, see [the Setup Guide](https://github.com/evilwb/APRac2/blob/main/docs/setup_en.md).
### Installation video tutorial by Scyker
https://www.youtube.com/watch?v=hRCuEQVgzPE


## What does randomization do to this game?
In Ratchet & Clank 2, all Gadgets, Platinum Bolts and Planet Coordinates are shuffled into the multiworld, giving the game a greater variety in routing to complete the end goal.


## What is the goal of Ratchet & Clank 2 when randomized?
The end goal of the randomizer game is to defeat the giant mutated Protopet on planet Yeedil.


## Which items can be in another player's world?
All Gadgets/Items, Platinum Bolts and Planet Coordinates can be shuffled in other players' worlds.


## What does another world's item look like in Ratchet & Clank 2?
There is no model replacement support yet so all items will their vanilla appearance.


## What versions of the Ratchet & Clank 2 are supported?
Only the PS2 versions of the game are supported. 
  * US `version 1.01 (SCUS-97268)` is it for now.
    Other PS2 regions/versions may get added eventually.
The PS3 Collection is *not* supported.  


## When the player receives an item, what happens?
The player will immediately have their inventory updated and receive a notification in the Client and a HUD message in-game.


## FAQs
### What happens if I pickup an item without having the client running?
In order for Ratchet & Clank 2 to function correctly, the Client should always be running whenever you are playing through your game.  
The client should be able to detect and resync missing items in most cases, but I wouldn't rely on it.


### Aside from item locations being shuffled, how does this differ from the vanilla game?
Some of the changes include:
  - You start at Slim's Ship Shack which will act as a hub.
  - You start with 3 random planets unlocked.
  - Holding `L1 + R1 + L2 + R2 + SELECT` will reset you to the Ship Shack.
  - When the Megacorp Weapon Vendor is randomized, the vendor is split between two modes, one for buying new items and one for buying ammo. 
You can switch between these modes by pressing up/down while in the vendor.
