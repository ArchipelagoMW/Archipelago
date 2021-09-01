# Risk of Rain 2 Setup Guide

## Install using r2modman
### Install r2modman
Head on over to the r2modman page on Thunderstore and follow the installation instructions.

https://thunderstore.io/package/ebkr/r2modman/

### Install Archipelago Mod using r2modman
You can install the Archipelago mod using r2modman in one of two ways. 
One, you can use the Thunderstore website and click on the "Install with Mod Manager" link.

https://thunderstore.io/package/ArchipelagoMW/Archipelago/

You can also search for the "Archipelago" mod in the r2modman interface.
The mod manager should automatically install all necessary dependencies as well.

### Running the Modded Game
Click on the "Start modded" button in the top left in r2modman to start the game with the
Archipelago mod installed.

## Joining an Archipelago Session
There will be a menu button on the right side of the screen in the character select menu. 
Click it in order to bring up the in lobby mod config. 
From here you can expand the Archipelago sections and fill in the relevant info.
Keep password blank if there is no password on the server.

Simply check `Enable Archipelago?` and when you start the run it will automatically connect.

## Gameplay
The Risk of Rain 2 players send checks by causing items to spawn in-game. That means opening chests or killing bosses, generally. 
An item check is only sent out after a certain number of items are picked up. This count is configurable in the player's YAML.

## YAML Settings
An example YAML would look like this:
```yaml
description: Ijwu-ror2
name: Ijwu

game:
  Risk of Rain 2: 1

Risk of Rain 2:
  total_locations: 15
  total_items: 30
  total_revivals: 4
  start_with_revive: true
  item_pickup_step: 1
  enable_lunar: true
```

| Name | Description | Allowed values |
| ---- | ----------- | -------------- |
| total_locations | The total number of location checks that will be attributed to the Risk of Rain player. | 10 - 50 |
| total_items | The total number of items which are added to the multiworld on behalf of the Risk of Rain player. | 10-50 |
| total_revivals | The total number of items in the Risk of Rain player's item pool (items other players pick up for them) replaced with `Dio's Best Friend`. | 0 - 5 |
| start_with_revive | Starts the player off with a `Dio's Best Friend`. Functionally equivalent to putting a `Dio's Best Friend` in your `starting_inventory`. | true/false |
| item_pickup_step | The number of item pickups which you are allowed to claim before they become an Archipelago location check. | 0 - 5 |
| enable_lunar | Allows for lunar items to be shuffled into the item pool on behalf of the Risk of Rain player. | true/false |

Using the example YAML above: the Risk of Rain 2 player will have 15 total items which they can pick up for other players. (total_locations = 15)
They will have 30 items which can be granted to them through the multiworld. (total_items = 30)
They will complete a location check every second item. (item_pickup_step = 1)
They will have 4 of the items which other players can grant them replaced with `Dio's Best Friend`. (total_revivals = 4)
The player will also start with a `Dio's Best Friend`. (start_with_revive = true)
The player will have lunar items shuffled into the item pool on their behalf. (enable_lunar = true)