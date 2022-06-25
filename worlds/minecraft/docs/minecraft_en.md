# Minecraft Randomizer Setup Guide

## Required Software

- Minecraft Java Edition from
  the [Minecraft Java Edition Store Page](https://www.minecraft.net/en-us/store/minecraft-java-edition)
- Archipelago from the [Archipelago Releases Page](https://github.com/ArchipelagoMW/Archipelago/releases)
    - (select `Minecraft Client` during installation.)

## Configuring your YAML file

### What is a YAML file and why do I need one?

See the guide on setting up a basic YAML at the Archipelago setup
guide: [Basic Multiworld Setup Guide](/tutorial/Archipelago/setup/en)

### Where do I get a YAML file?

You can customize your settings by visiting the [Minecraft Player Settings Page](/games/Minecraft/player-settings)

## Joining a MultiWorld Game

### Obtain Your Minecraft Data File

**Only one yaml file needs to be submitted per minecraft world regardless of how many players play on it.**

When you join a multiworld game, you will be asked to provide your YAML file to whoever is hosting. Once that is done,
the host will provide you with either a link to download your data file, or with a zip file containing everyone's data
files. Your data file should have a `.apmc` extension.

Double-click on your `.apmc` file to have the Minecraft client auto-launch the installed forge server. Make sure to
leave this window open as this is your server console.

### Connect to the MultiServer

Using Minecraft 1.18.2 connect to the server `localhost`.

If you are using the website to host the game then it should auto-connect to the AP server without the need to `/connect`

otherwise once you are in game type `/connect <AP-Address> (Port) (Password)` where `<AP-Address>` is the address of the
Archipelago server. `(Port)` is only required if the Archipelago server is not using the default port of 38281.
`(Password)` is only required if the Archipelago server you are using has a password set.

### Play the game

When the console tells you that you have joined the room, you're all set. Congratulations on successfully joining a
multiworld game! At this point any additional minecraft players may connect to your forge server. To start the game once
everyone is ready use the command `/start`.

## Manual Installation

It is highly recommended to ues the Archipelago installer to handle the installation of the forge server for you.
support will not be given for those wishing to manually install forge. For those of you who know how, and wish to do so,
the following links are the versions of the software we use.

### Manual install Software links

- [Minecraft Forge Download Page](https://files.minecraftforge.net/net/minecraftforge/forge/index_1.18.2.html)
- [Minecraft Archipelago Randomizer Mod Releases Page](https://github.com/KonoTyran/Minecraft_AP_Randomizer/releases)
    - **DO NOT INSTALL THIS ON YOUR CLIENT**
- [Amazon Corretto Java 17 Download Page](https://docs.aws.amazon.com/corretto/latest/corretto-17-ug/downloads-list.html)

