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

## Configuring your YAML File
### What is a YAML and why do I need one?
You can see the [basic multiworld setup guide](/tutorial/Archipelago/setup/en) here on the Archipelago website to learn 
about why Archipelago uses YAML files and what they're for.

### Where do I get a YAML?
You can use the [game settings page for Hollow Knight](/games/Hollow%20Knight/player-settings) here on the Archipelago 
website to generate a YAML using a graphical interface.


## Joining an Archipelago Session

There will be a menu button on the right side of the screen in the character select menu. Click it in order to bring up
the in lobby mod config. From here you can expand the Archipelago sections and fill in the relevant info. Keep password
blank if there is no password on the server.

Simply check `Enable Archipelago?` and when you start the run it will automatically connect.

## Gameplay

The Risk of Rain 2 players send checks by causing items to spawn in-game. That means opening chests or killing bosses,
generally. An item check is only sent out after a certain number of items are picked up. This count is configurable in
the player's YAML.

## Commands
While playing the multiworld you can type `say` then your message to type in the multiworld chat. All other multiworld
remote commands list in the [commands guide](/tutorial/Archipelago/commands/en) work as well in the RoR2 chat. You can 
also optionally connect to the multiworld using the text client, which can be found in the 
[main Archipelago installation](https://github.com/ArchipelagoMW/Archipelago/releases).