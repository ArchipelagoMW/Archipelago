# Noita Setup Guide

## Installation

### Game

Go through the standard installation process for [Noita](https://noitagame.com/) on any of its supported platforms.

### Install Archipelago Mod

Download the Archipelago mod zip from the GitHub page:

[Archipelago Mod Download](https://github.com/DaftBrit/NoitaArchipelago/releases/latest)

Firstly, go to your Noita installation directory.

* **On Steam:** Find **Noita** in your Steam library. Right click, select *Manage* → *Browse local files*.
* **On GOG Galaxy:** Find **Noita** in your Installed Games library. Right click, select *Manage installation* →
*Show folder*.

Here you should see your game files and a folder called `mods`. Create a folder called `archipelago` and place all files
from within the zip folder directly into the `archipelago` folder. After starting Noita, select the *Mods* menu. Here
you should see the *Archipelago* mod listed.

In order to enable the mod you will first need to toggle **Unsafe mods** from *Disabled* to *Allowed*. This is required,
as some external libraries are used by the mod in order to communicate with the Archipelago server. Once that is done,
you can now enable the *Archipelago* mod (it should have an `[x]` next to it).

### Configure Archipelago Mod

In the Options menu, select Mod Settings. Under the Archipelago drop down, you will see the options for *Server*,
*Port*, *Slot*, and *Password* where you can fill in the relevant information.

Once you start a new run in Noita, you should see an Archipelago logo in the bottom right corner of the screen with a 
checkmark on it. If you do not see this icon, ensure that the mod is enabled and installed per the instructions above, 
or try restarting your game.

## Configuring your YAML File

### What is a YAML and why do I need one?
You can see the [basic multiworld setup guide](/tutorial/Archipelago/setup/en) here on the Archipelago website to learn
about why Archipelago uses YAML files and what they're for.
Please note that Noita only allows you to type certain characters for your slot name.
These characters are: `` !#$%&'()+,-.0123456789;=@ABCDEFGHIJKLMNOPQRSTUVWXYZ[]^_`abcdefghijklmnopqrstuvwxyz{}~<>|\/``

### Where do I get a YAML?
You can use the [game options page for Noita](/games/Noita/player-options) here on the Archipelago website to
generate a YAML using a graphical interface.

## Poptracker Pack

You may optionally use the [Noita Poptracker pack](https://github.com/ScipioWright/Noita-poptracker/releases/latest).

To use it, download the pack as well as [PopTracker](https://github.com/black-sliver/PopTracker/releases) itself.
Place the unzipped pack in the `packs` folder. Then, open Poptracker and open the pack.
Click on the "AP" symbol at the top, then enter the desired address, slot name, and password.

That's all you need for it. It will provide you with a quick reference to see which checks you've done and
which checks you still have left.
