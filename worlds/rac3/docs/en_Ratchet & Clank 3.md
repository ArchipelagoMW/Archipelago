# Ratchet and Clank 3 Up your Arsenal (PS2)

An Archipelago implementation for Ratchet and Clank 3

## Setup Guide

To get started,
see [the Setup Guide](https://github.com/Taoshix/Archipelago-RaC3/blob/main/worlds/rac3/docs/setup_en.md).

## Where is the options page?

The [player options page for this game](../player-options) contains all the options you need to configure and export a
config file.

## What does randomization do to this game?

Weapons, Planets, Gadgets, Titanium bolts, Trophies, Weapon upgrades, Sewer Crystals are all randomized

## What items and locations get shuffled?

20 different weapons, 4 progressive upgrades per weapon are available, 10 different gadgets, 17 post-planet completions
that unlock other planets, 4 progressive armors, 35 titanium bolts, 15 trophies, and Bolts/Weapon EXP along with Inferno
Mode and Jackpot get shuffled in as filler.
Addtional locations may be included through yaml options: Annihilation Nation missions, The Ranger missions, Phoenix VR
missions, Sewer Crystals and Nanotech Levels.

## Which items can be in another player's world?

Any of the items which can be shuffled may also be placed into another player's world. It is possible to choose to limit
certain items to your own world.

## When the player receives an item, what happens?

You will be able to visit the planets with whatever post-planet you receive, receiving Post Marcadia will unlock Aquatos
for travel within Ratchet's Ship. Upon receiving a weapon it unlocks in ratchet's inventory, which will let you equip it
and use to fire on enemy troops. Progressive upgrades will upgrade your weapons from V1 up to V5 increasing their
firepower. Receiving Jackpot Mode filler item acts like you just broke the corresponding crate.
When you receive a trap, you will get its effect for 10 seconds and then it expires.
For 1-Hit KO Trap and No Ammo Trap, the effects are instant and will not revert after 10 seconds.
Receiving the Inferno Mode trap will not change your armor, but you will still receive the full effect for a random amount of time rather than 10 seconds.
