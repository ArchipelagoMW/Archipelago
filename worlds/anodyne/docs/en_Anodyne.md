# Anodyne

## Where is the options page?

The [player options page for this game](../player-options) contains all the
options you need to configure and export a config file.

## What does randomization do to this game?

Most items you can receive in the game become Archipelago items, including the
broom, broom upgrades, cards, big keys, small keys, the trade quest, and health
cicadas. Similarly, most places where you receive items also become Archipelago
locations, including treasure chests, big keys, the trade quest, and health
cicadas.

## How does Swap work?

The behavior of the Swap upgrade has been changed in the Archipelago mod. See
[extended_swap.md](https://github.com/SephDB/AnodyneArchipelagoClient/blob/main/docs/extended_swap.md)
for more information.

## What about the wiggle glitch?

There is a technique in the base game where you can cross back and forth over a
screen transition while holding a directional key perpendicular to this
movement, and it will cause you to slowly move into solid geometry. This is
called the **wiggle glitch** (although it is not actually a glitch and is in
fact an intended mechanic).

The wiggle glitch can be used to bypass most progression barriers in the game,
including allowing you to reach the credits as soon as you have access to the
Fields area. Because of this, it is impossible to design randomizer logic that
includes the wiggle glitch, because allowing it would make almost everything in
logic immediately. Thus, the wiggle glitch is (almost) never is logic for
Archipelago.

There is one exception to this rule. In the secret top part of the Nexus, there
is a chest on an isolated platform. Swap is disabled in this area (both in the
base game and in the mod). The intended way of reaching this chest is by using
the wiggle glitch. Thus, you are expected to use the wiggle glitch in this room
to reach that chest. Any other use of the wiggle glitch is out-of-logic.
