# Noita Setup Guide

## Installation

### Steam

Go through the standard installation process for Noita on Steam.

### Install Archipelago Mod

Download the Archipelago mod zip from the GitHub page:

[Archipelago Mod Download](https://github.com/DaftBrit/NoitaArchipelago/archive/refs/heads/master.zip)

Find Noita in your Steam library, right click, select Manage > Browse Local Files

Here you should see your game files and a folder called "mods". Create a folder called "archipelago" and place all files
from within the zip folder directly into the archipelago folder. After starting Noita, select the Mods menu. Here you 
should see the Archipelago mod listed.

In order to enable the mod you will first need to toggle "Allow unsafe mods". This is required, as some external 
libraries are used in the mod in order to communicate with the Archipelago server. Enable "Allow unsafe mods" and enable
the Archipelago mod.

### Configure Archipelago Mod

In the Options menu, select Mod Settings. Under the Archipelago drop down, you will see the options for Hostname, Port,
and Slot name, where you can fill in the relevant information. There are also options to toggle redelivery of items when
starting a new run and the number of kills required to spawn a chest.

Once you start a new run in Noita, you should see "Connected to Archipelago server" in the bottom left of the screen. If
you do not see this message, ensure that the mod is enabled and installed per the instructions above.

## Configuring your YAML File
### What is a YAML and why do I need one?
You can see the [basic multiworld setup guide](/tutorial/Archipelago/setup/en) here on the Archipelago website to learn 
about why Archipelago uses YAML files and what they're for.

### Where do I get a YAML?
You can use the [game settings page for Noita](/games/Noita/player-settings) here on the  Archipelago website to 
generate a YAML using a graphical interface.