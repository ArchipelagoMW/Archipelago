# Factorio

## Where is the options page?

The [player options page for this game](../player-options) contains all the options you need to configure and export a
config file.

## What does randomization do to this game?

In Factorio, the research tree is shuffled, causing certain technologies to be obtained in a non-standard order. Recipe
costs, technology requirements, and science pack requirements may also be shuffled at the player's discretion.

## What Factorio items can appear in other players' worlds?

Factorio's technologies are removed from its tech tree and placed into other players' worlds. When those technologies
are found, they are sent back to Factorio along with, optionally, free samples of those technologies.

## What is a free sample?

A free sample is a single or stack of items in Factorio, granted by a technology received from another world. For
example, receiving the technology `Portable Solar Panel` may also grant the player a stack of portable solar panels, and
place them directly into the player's inventory.

## What does another world's item look like in Factorio?

In Factorio, items which need to be sent to other worlds appear in the tech tree as new research items. They are
represented by the Archipelago icon, and must be researched as if they were normal technologies. Upon successful
completion of research, the item will be sent to its home world.

## When the engineer receives an item, what happens?

When the player receives a technology, it is instantly learned and able to be crafted. A message will appear in the chat
log to notify the player, and if free samples are enabled the player may also receive some items directly to their
inventory.

## What is EnergyLink?

EnergyLink is an energy storage supported by certain games that is shared across all worlds in a multiworld.
In Factorio, if enabled in the player options, EnergyLink Bridge buildings can be crafted and placed, which allow
depositing excess energy and supplementing energy deficits, much like Accumulators.

Each placed EnergyLink Bridge provides 10 MW of throughput. The shared storage has unlimited capacity, but 25% of energy
is lost during depositing. The amount of energy currently in the shared storage is displayed in the Archipelago client.
It can also be queried by typing `/energy-link` in-game.

## Unique Local Commands
The following commands are only available when using the FactorioClient to play Factorio with Archipelago.

- `/factorio <command text>` Sends the command argument to the Factorio server as a command.
- `/energy-link` Displays the amount of energy currently in shared storage for EnergyLink
