# Risk of Rain 2 Setup Guide

## Install using r2modman

### Install r2modman

Head on over to the r2modman page on Thunderstore and follow the installation instructions.

[r2modman Page](https://thunderstore.io/package/ebkr/r2modman/)

### Install Archipelago Mod using r2modman

You can install the Archipelago mod using r2modman in one of two ways.

[Archipelago Mod Download Page](https://thunderstore.io/package/ArchipelagoMW/Archipelago/)

One, you can use the Thunderstore website and click on the "Install with Mod Manager" link.

You can also search for the "Archipelago" mod in the r2modman interface. The mod manager should automatically install
all necessary dependencies as well.

### Running the Modded Game

Click on the "Start modded" button in the top left in r2modman to start the game with the Archipelago mod installed.

## Joining an Archipelago Session

There will be a menu button on the right side of the screen in the character select menu. Click it in order to bring up
the in lobby mod config. From here you can expand the Archipelago sections and fill in the relevant info. Keep password
blank if there is no password on the server. If you are using the website, put `archipelago.gg` in the server URL field (no `https://` or anything else).

In a multiplayer game, only the host needs to configure these settings.

Simply check `Enable Archipelago?` and when you start the run it will automatically connect.

## Gameplay

The Risk of Rain 2 players send checks by causing items to spawn in-game. That means opening chests or killing bosses,
generally. An item check is only sent out after a certain number of items are picked up. This count is configurable in
the player's YAML.

## YAML Settings

An example YAML would look like this:

```yaml
description: Ijwu-ror2
name: Ijwu

game:
  Risk of Rain 2: 1

Risk of Rain 2:
  total_locations: 15
  total_revivals: 4
  start_with_revive: true
  item_pickup_step: 1
  enable_lunar: true
  item_weights:
    default: 50
    new: 0
    uncommon: 0
    legendary: 0
    lunartic: 0
    chaos: 0
    no_scraps: 0
    even: 0
    scraps_only: 0
  item_pool_presets: true
  # custom item weights
  green_scrap: 16
  red_scrap: 4
  yellow_scrap: 1
  white_scrap: 32
  common_item: 64
  uncommon_item: 32
  legendary_item: 8
  boss_item: 4
  lunar_item: 16
  equipment: 32
```

| Name | Description | Allowed values |
| ---- | ----------- | -------------- |
| total_locations | The total number of location checks that will be attributed to the Risk of Rain player. This option is ALSO the total number of items in the item pool for the Risk of Rain player. | 10 - 100 |
| total_revivals | The total number of items in the Risk of Rain player's item pool (items other players pick up for them) replaced with `Dio's Best Friend`. | 0 - 5 |
| start_with_revive | Starts the player off with a `Dio's Best Friend`. Functionally equivalent to putting a `Dio's Best Friend` in your `starting_inventory`. | true/false |
| item_pickup_step | The number of item pickups which you are allowed to claim before they become an Archipelago location check. | 0 - 5 |
| enable_lunar | Allows for lunar items to be shuffled into the item pool on behalf of the Risk of Rain player. | true/false |
| item_weights | Each option here is a preset item weight that can be used to customize your generate item pool with certain settings. | default, new, uncommon, legendary, lunartic, chaos, no_scraps, even, scraps_only |
| item_pool_presets | A simple toggle to determine whether the item_weight presets are used or the custom item pool as defined below | true/false |
| custom item weights | Each defined item here is a single item in the pool that will have a weight against the other items when the item pool gets generated. These values can be modified to adjust how frequently certain items appear | 0-100|

Using the example YAML above: the Risk of Rain 2 player will have 15 total items which they can pick up for other
players. (total_locations = 15)

They will have 15 items waiting for them in the item pool which will be distributed out to the multiworld. (
total_locations = 15)

They will complete a location check every second item. (item_pickup_step = 1)

They will have 4 of the items which other players can grant them replaced with `Dio's Best Friend`. (total_revivals = 4)

The player will also start with a `Dio's Best Friend`. (start_with_revive = true)

The player will have lunar items shuffled into the item pool on their behalf. (enable_lunar = true)

The player will have the default preset generated item pool with the custom item weights being ignored. (item_weights:
default and item_pool_presets: true)
