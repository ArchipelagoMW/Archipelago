# Archipelago Setup Guide

This guide provides an overview of how to install, set up, and run the Archipelago multiworld software.
This guide should take about 5 minutes to read.

## Installing the Archipelago software

The most recent public release of Archipelago can be found on the
[GitHub releases page](https://github.com/ArchipelagoMW/Archipelago/releases).

Run the .exe file. After accepting the license agreement, you will be asked which components you would like to install.

The first component is the `Generator`. It is not needed to play games with Archipelago -- our website also has a
generator that does not need to be installed. If you install the generator, it allows you to create a multiworld using
only your own computer. (Note: if you want to create a multiworld using certain games, you will need to enable their
"ROM Setup" options now, and you will need a legally-obtained ROM for each of those games.)

The second component is the `Server`. It is also not needed to play games with Archipelago -- our website can host
multiworlds using its own server. If you install the server, it allows you to host multiworlds on your own computer.
(Note: hosting on your own computer requires forwarding the port you are hosting on. We do not provide a guide for how
to do this. The default port for Archipelago is `38281`.)

The last components are the `Clients`. They __are__ needed to play games with Archipelago. If you see a game that you
don't intend to play with Archipelago, you may uncheck it now. You will need a legally-obtained ROM for each game that
uses ROMS.

If you change your mind and would like to install more components later, simply run the .exe again and check the boxes
for each new component.

Once the installer finishes, you're done installing the basics for Archipelago! However, each individual game needs
additional setup to work properly. Check out the [Supported Games](https://archipelago.gg/games) page to see what each
randomizer is like and how to set them up.

## Generating a game

### What is a YAML?

YAML is the file format which Archipelago uses in order to configure a player's world. It allows you to dictate which
game you will be playing as well as the settings you would like for that game.

YAML is a format very similar to JSON however it is made to be more human-readable. If you are ever unsure of the
validity of your YAML file you may check the file by uploading it to the check page on the Archipelago website. Check
page: [YAML Validation Page](/mysterycheck)

### Creating a YAML

YAML files may be generated on the Archipelago website by visiting the games page and clicking the "Settings Page" link
under any game. Clicking "Export Settings" in a game's settings page will download the YAML to your system. Games
page: [Archipelago Games List](/games)

In a multiworld there must be one YAML per world. Any number of players can play on each world using either the game's
native coop system or using Archipelago's coop support. Each world will hold one slot in the multiworld and will have a
slot name and, if the relevant game requires it, files to associate it with that multiworld.

If multiple people plan to play in one world cooperatively then they will only need one YAML for their coop world. If
each player is planning on playing their own game then they will each need a YAML.

### Gather All Player YAMLs

All players that wish to play in the generated multiworld must have a YAML file which contains the settings that they
wish to play with.

Typically, a single participant of the multiworld will gather the YAML files from all other players. After getting the
YAML files of each participant for your multiworld game they can be compressed into a ZIP folder to then be uploaded to
the multiworld generator page. Multiworld generator
page: [Archipelago Seed Generator Page](/generate)

#### Rolling a YAML Locally

It is possible to roll the multiworld locally, using a local Archipelago installation. This is done by entering the
installation directory of the Archipelago installation and placing each YAML file in the `Players` folder. If the folder
does not exist then it can be created manually.

After filling the `Players` folder the `ArchipelagoGenerate.exe` program should be run in order to generate a
multiworld. The output of this process is placed in the `output` folder.

#### Changing local host settings for generation

Sometimes there are various settings that you may want to change before rolling a seed such as enabling race mode,
auto-forfeit, plando support, or setting a password.

All of these settings plus other options are able to be changed by modifying the `host.yaml` file in the Archipelago
installation folder. The settings chosen here are baked into the `.archipelago` file that gets output with the other
files after generation so if rolling locally ensure this file is edited to your liking *before* rolling the seed.

## Hosting an Archipelago Server

The output of rolling a YAML will be a `.archipelago` file which can be subsequently uploaded to the Archipelago host
game page. Archipelago host game page: [Archipelago Seed Upload Page](/uploads)

The `.archipelago` file may be run locally in order to host the multiworld on the local machine. This is done by
running `ArchipelagoServer.exe` and pointing the resulting file selection prompt to the `.archipelago` file that was
generated.