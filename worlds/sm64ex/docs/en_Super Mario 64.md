# Super Mario 64 EX

## Where is the options page?

The player options page for this game contains all the options you need to configure and export a config file. Player
options page link: [SM64EX Player Options Page](../player-options).

## What does randomization do to this game?
All 120 Stars, the 3 Cap Switches, the Basement and Second Floor Key are now location checks and may contain items for different games as well
as different items from within SM64.


## What is the goal of SM64EX when randomized?
As in most Mario games, save the Princess!

## Which items can be in another player's world?
Any of the 120 Stars, and the two Castle Keys. Additionally, Cap Switches are also considered "Items" and the "!"-Boxes will only be active
when someone collects the corresponding Cap Switch item.

## What does another world's item look like in SM64EX?
The items are visually unchanged, though after collecting a message will pop up to inform you what you collected,
and who will receive it.

## When the player receives an item, what happens?
When you receive an item, a message will pop up to inform you where you received the item from,
and which one it is.

NOTE: The Secret Star count in the menu is broken.

## Is Connection Plando supported?
Yes. The host needs to enable it in their `host.yaml`, and the player's yaml needs to contain a `plando_connections` block.

Entances and exits:
```
"Bob-omb Battlefield"
"Whomp's Fortress"
"Jolly Roger Bay"
"Cool, Cool Mountain"
"Big Boo's Haunt"
"Hazy Maze Cave"
"Lethal Lava Land"
"Shifting Sand Land"
"Dire, Dire Docks"
"Snowman's Land"
"Wet-Dry World"
"Tall, Tall Mountain"
"Tiny-Huge Island (Tiny)"
"Tiny-Huge Island (Huge)"
"Tick Tock Clock"
"Rainbow Ride"
"The Princess's Secret Slide"
"The Secret Aquarium"
"Bowser in the Dark World"
"Tower of the Wing Cap"
"Cavern of the Metal Cap"
"Vanish Cap under the Moat"
"Bowser in the Fire Sea"
"Wing Mario over the Rainbow"
```

Example:
```
plando_connections:
  - entrance: "Bob-omb Battlefield"
    exit: "Jolly Roger Bay"
  - entrance: "Cavern of the Metal Cap"
    exit: "Cavern of the Metal Cap"
  - entrance: "Jolly Roger Bay"
    exit: "Tower of the Wing Cap"
```
Notes:
- The `direction` field is not supported.

See the Archipelago Plando Guide for more information on Plando and Connection Plando.
