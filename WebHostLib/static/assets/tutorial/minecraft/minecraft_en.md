# Minecraft Randomizer Setup Guide

## Required Software

- [Minecraft Java Edition](https://www.minecraft.net/en-us/store/minecraft-java-edition) (update 1.17.1)
- [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases) (select `Minecraft Client` durring installation.)

## Configuring your YAML file

### What is a YAML file and why do I need one?
Your YAML file contains a set of configuration options which provide the generator with information about how
it should generate your game. Each player of a multiworld will provide their own YAML file. This setup allows
each player to enjoy an experience customized for their taste, and different players in the same multiworld
can all have different options.

### Where do I get a YAML file?
you can customize your settings by visiting the [minecraft player settings](/games/Minecraft/player-settings)

## Joining a MultiWorld Game

### Obtain your Minecraft data file
**Only one yaml file needs to be submitted per minecraft world regardless of how many players play on it.**

When you join a multiworld game, you will be asked to provide your YAML file to whoever is hosting. Once that
is done, the host will provide you with either a link to download your data file, or with a zip file containing
everyone's data files. Your data file should have a `.apmc` extension.

double-click on your `.apmc` file to have the minecraft client auto-launch the installed forge server.
make sure to leave this window open as this is your server console.

### Connect to the MultiServer
Using minecraft 1.17.1 connect to the server `localhost`.

Once in game type `/connect <AP-Address> (Port) (Password)` where `<AP-Address>` is the address of the
Archipelago server. `(Port)` is only required if the Archipelago server is not using the default port of 38281. `(Password)`
is only required if the Archipleago server you are using has a password set.

### Play the game
When the console tells you that you have joined the room, you're all set. Congratulations
on successfully joining a multiworld game! At this point any additional minecraft players may connect to your
forge server. to star the game once everyone is ready type `/start`. 

### Useful commands
- `!help` displays a list all server commands
- `!hint` will display how many hint points you have, along with any hints that have been given that are related to your game.
- `!hint (item)` will ask the server to tell you where (item) is
- `!hint_location (location)` will ask the server to tell you what item is on (location)

## Manual Installation
it is highly recommended to ues the Archipelago installer to handle the installation of the forge server for you.
support will not be given for those wishing to manually install forge. but for those of you who know how, and wish to
do so the following links are the versions of the software we use.
### Manual install Software links
- [Minecraft Forge](https://files.minecraftforge.net/net/minecraftforge/forge/index_1.17.1.html)
- [Minecraft Archipelago Randomizer Mod](https://github.com/KonoTyran/Minecraft_AP_Randomizer/releases)
**DO NOT INSTALL THIS ON YOUR CLIENT**
- [Java 16](https://docs.aws.amazon.com/corretto/latest/corretto-16-ug/downloads-list.html)

