# Risk of Rain 2 Setup Guide

## Install using r2modman

### Install r2modman

Head on over to the `r2modman` page on Thunderstore and follow the installation instructions.

[r2modman Page](https://thunderstore.io/package/ebkr/r2modman/)

### Install Archipelago Mod using r2modman

You can install the Archipelago mod using `r2modman` in one of two ways.

[Archipelago Mod Download Page](https://thunderstore.io/package/Sneaki/Archipelago/)

One, you can use the Thunderstore website and click on the "Install with Mod Manager" link.

You can also search for the "Archipelago" mod in the `r2modman` interface. The mod manager should automatically install
all necessary dependencies as well.

## Running the Modded Game

Click on the `Start modded` button in the top left in `r2modman` to start the game with the Archipelago mod installed.

## Configuring your YAML File
### What is a YAML and why do I need one?
You can see the [basic multiworld setup guide](/tutorial/Archipelago/setup/en) here on the Archipelago website to learn 
about why Archipelago uses YAML files and what they're for.

### Where do I get a YAML?
You can use the [game settings page](/games/Risk%20of%20Rain%202/player-settings) here on the Archipelago 
website to generate a YAML using a graphical interface.


## Joining an Archipelago Session
### Connecting to server
Once in game, join whatever lobby you wish, and you should see the AP connection fields which consist of:
 - Slot Name: your name in the multiworld. This is the name you entered in the YAML.
 - Password: optional password, leave blank if no password was set.
 - Server URL: (default: archipelago.gg).
 - Server Port: (default: 38281).

Once everything is entered click the Connect to AP button to connect to the server, and you should be connected!

Start the game whenever you are ready.

### Gameplay

The Risk of Rain 2 players send checks by causing items to spawn in-game. That means opening chests or killing bosses,
generally. An item check is only sent out after a certain number of items are picked up. This count is configurable in
the player's YAML.

### Chat/Commands
You can talk to other in the multiworld chat using the RoR2 chat. All other multiworld
remote commands list in the [commands guide](/tutorial/Archipelago/commands/en) work as well in the RoR2 chat. You can 
also optionally connect to the multiworld using the text client, which can be found in the 
[main Archipelago installation](https://github.com/ArchipelagoMW/Archipelago/releases).

### In-Game Commands
These commands are to be used in-game by using ``Ctrl + Alt + ` `` and then typing the following:
 - `archipelago_connect <url> <port> <slot> [password]` example: "archipelago_connect archipelago.gg 38281 SlotName".
 - `archipelago_deathlink true/false` Toggle deathlink.
 - `archipelago_disconnect` Disconnect from AP.
 - `archipelago_final_stage_death true/false` Toggle final stage death.

Explore Mode only
 - `archipelago_show_unlocked_stages` Show which stages have been received.
 - `archipelago_highlight_satellite true/false` This will highlight the satellite to make it easier to see (Default false).