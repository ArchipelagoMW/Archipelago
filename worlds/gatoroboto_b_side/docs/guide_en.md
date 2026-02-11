# Gato Roboto Randomizer Setup Guide

## Required Software

- Gato Roboto: [Steam Store](https://store.steampowered.com/app/391540)
- Archipelago: [Archipelago Releases Page](https://github.com/ArchipelagoMW/Archipelago/releases)

## First Time Setup

>Gato Roboto Archipelago **does not** overwrite vanilla saves, but you may wish to create a backup as a precaution.

Open the Archipelago Launcher and start the `Gato Roboto Client` from the clients list, and input 
`/auto_patch <Your Gato Roboto Install Directory>` in the command line at the bottom of the client. 

The default directory is located at `C:\Program Files\Steam\steamapps\common\Gato Roboto` or 
`C:\Program Files (x86)\Steam\steamapps\common\Gato Roboto`, but it can change depending on your installation. 
Navigate to your Steam library, right-click on Gato Roboto, and select `Manage -> Browse local files` to view your 
install directory.

After the `/auto_patch` command fires, your installation of Gato Roboto will be updated to the Archipelago version. You can open it through Steam as normal.

>Any major updates to the APWorld will require you to re-patch the game.

## Connecting to a Multi-World Server

Make sure both Gato Roboto and its client are running.

In the top text box of the client, enter the `IP Address` (or `Hostname`) and `Port` separated with a `:` symbol. (Ex. `archipelago.gg:38281`)

You will then be prompted for the slot name to connect to. Input your slot name chosen during YAML creation in the 
command line at the bottom of the client.

## Playing the Game

When the client console tells you that you have joined the room, you're all set. Congratulations on successfully joining
a multi-world game!

## Reverting Changes

When you would like to revert any AP changes to Gato Roboto, you can input `/unpatch` in the command line of the client.
This will provide a vanilla installation and remove any existing related AP files.

## Where do I get a YAML file?

You can generate a YAML file by visiting the [Gato Roboto Player Options Page](/games/Gato Roboto/player-options).
