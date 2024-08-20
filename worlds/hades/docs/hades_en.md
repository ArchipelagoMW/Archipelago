# Hades Setup Guide

## Required Software

Install the game through Steam. Then install the following mods:

- [ModImporter](https://github.com/SGG-Modding/ModImporter/releases/tag/1.5.2)
- [ModUtils v 2.10.1](https://github.com/SGG-Modding/ModUtil/releases/tag/2.10.1)
- [StyxScribe without the REPL](https://github.com/NaixGames/StyxScribeWithoutREPL).
- [Polycosmos](https://github.com/Naix99/Polycosmos/tree/main/Polycosmos)

Put the hades.apworld file in your worlds folder (normally in your archipelago installation, go to lib\worlds.

## Configuring your YAML file

### What is a YAML file and why do I need one?

Your YAML file contains a set of configuration options which provide the generator with information about how it should
generate your game. Each player of a multiworld will provide their own YAML file. This setup allows each player to enjoy
an experience customized to their taste, and different players in the same multiworld can all have different options.

### Where do I get a YAML file?

You can customize your settings by using the .yaml in the Hades World folder. The repo also has 3 different
templates with different difficulties in mind. We recommend starting with the Easy difficulty.

### Connect to the MultiServer

For launching the game to play in the multiworld you need to open the ArchipelagoLauncher.exe. There should be an option
for HadesClient. This opens a window to look for your Hades installation path (the standard steam path being 
`C:\Program Files\Steam\steamapps\common\Hades` ). Once the folder is selected the game should open Hades and the Archipelago client.

Use the Client window to connect to the Archipelago server before choosing your save file. If this is done correctly, you should
be able to start the game and get a location check on the first room, which prints a message on your console. If the connection
is not successfully made, you will get an error message in the first room. Exit, reconnect and try again.