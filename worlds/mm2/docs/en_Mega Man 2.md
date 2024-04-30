# Mega Man 2

## Where is the options page?

The [player options page for this game](../player-options) contains all the options you need to configure and export a
config file.

## What does randomization do to this game?

Weapons received from Robot Masters, access to each individual stage, and Items from Dr. Light are randomized
into the multiworld. Access to the Wily Stages is locked behind receiving Item 1, 2, and 3. The game is complete upon 
viewing the ending sequence after defeating the Alien.

## What is considered a location check in Mega Man 2?
- The defeat of a Robot Master or Wily Boss
- Receiving a weapon or item from Dr. Light
- Optionally, 1-Ups and E-Tanks present within stages
- Optionally, Weapon and Health Energy pickups present within stages

## When the player receives an item, what happens?
A sound effect will play based on the type of item received, and the effects of the item will be immediately applied, 
such as unlocking the use of a weapon mid-stage. If the effects of the item cannot be fully applied (such as receiving 
Health Energy while at full health), the remaining are withheld until they can be applied.

## What is EnergyLink?
EnergyLink is an energy storage supported by certain games that is shared across all worlds in a multiworld. In Mega Man
 2, when enabled, drops from enemies are not applied directly to Mega Man and are instead deposited into the EnergyLink.
Half of the energy that would be gained is lost upon transfer to the EnergyLink. 

Energy from the EnergyLink storage can be converted into health, weapon energy, and lives at different conversion rates.
You can find out how much of each type you can pull using `/pool` in the client. Additionally, you can have it 
automatically pull from the EnergyLink storage to keep Mega Man healed using the `/autoheal` command in the client. 
Finally, you can use the `/request` command to request a certain type of energy from the storage.

## Unique Local Commands
- `/pool` Only present with EnergyLink, prints the max amount of each type of request that could be fulfilled.
- `/autoheal` Only present with EnergyLink, will automatically drain energy from the EnergyLink in order to 
restore Mega Man's health.
- `/request <amount> <type>` Only present with EnergyLink, sends a request of a certain type of energy to be pulled from
the EnergyLink. Types are as follows:
  - `HP` Health
  - `AF` Atomic Fire
  - `AS` Air Shooter
  - `LS` Leaf Shield
  - `BL` Bubble Lead
  - `QB` Quick Boomerang
  - `TS` Time Stopper
  - `MB` Metal Blade
  - `CB` Crash Bomber
  - `I1` Item 1
  - `I2` Item 2
  - `I3` Item 3
  - `1U` Lives