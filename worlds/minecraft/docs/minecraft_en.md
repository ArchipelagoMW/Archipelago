# Minecraft Randomizer Setup Guide

## Required Software

- Minecraft Java Edition from
  the [Minecraft Java Edition Store Page](https://www.minecraft.net/en-us/store/minecraft-java-edition)
- Archipelago from the [Archipelago Releases Page](https://github.com/ArchipelagoMW/Archipelago/releases)

## Configuring your YAML file

### What is a YAML file and why do I need one?

See the guide on setting up a basic YAML at the Archipelago setup
guide: [Basic Multiworld Setup Guide](/tutorial/Archipelago/setup/en)

### Where do I get a YAML file?

You can customize your options by visiting the [Minecraft Player Options Page](/games/Minecraft/player-options)

## Joining a MultiWorld Game

### Obtain Your Minecraft Data File

**Only one yaml file needs to be submitted per minecraft world regardless of how many players play on it.**

When you join a multiworld game, you will be asked to provide your YAML file to whoever is hosting. Once that is done,
the host will provide you with either a link to download your data file, or with a zip file containing everyone's data
files. Your data file should have a `.apmc` extension.

Double-click on your `.apmc` file to have the Minecraft client auto-launch the installed forge server. Make sure to
leave this window open as this is your server console.

### Connect to the MultiServer

Open Minecraft, go to `Multiplayer > Direct Connection`, and join the `localhost` server address.

If you are using the website to host the game then it should auto-connect to the AP server without the need to `/connect`

otherwise once you are in game type `/connect <AP-Address> (Port) (Password)` where `<AP-Address>` is the address of the
Archipelago server. `(Port)` is only required if the Archipelago server is not using the default port of 38281. Note that there is no colon between `<AP-Address>` and `(Port)`.
`(Password)` is only required if the Archipelago server you are using has a password set.

### Play the game

When the console tells you that you have joined the room, you're all set. Congratulations on successfully joining a
multiworld game! At this point any additional minecraft players may connect to your forge server. To start the game once
everyone is ready use the command `/start`.

## Non-Windows Installation

The Minecraft Client will install forge and the mod for other operating systems but Java has to be provided by the
user. Head to [minecraft_versions.json on the MC AP GitHub](https://raw.githubusercontent.com/KonoTyran/Minecraft_AP_Randomizer/master/versions/minecraft_versions.json)
to see which java version is required. New installations will default to the topmost "release" version.
- Install the matching Amazon Corretto JDK
    - see [Manual Installation Software Links](#manual-installation-software-links)
    - or package manager provided by your OS / distribution
- Open your `host.yaml` and add the path to your Java below the `minecraft_options` key
    - `  java: "path/to/java-xx-amazon-corretto/bin/java"`
- Run the Minecraft Client and select your .apmc file

## Full Manual Installation

It is highly recommended to ues the Archipelago installer to handle the installation of the forge server for you.
Support will not be given for those wishing to manually install forge. For those of you who know how, and wish to do so,
the following links are the versions of the software we use.

### Manual Installation Software Links

- [Minecraft Forge Download Page](https://files.minecraftforge.net/net/minecraftforge/forge/)
- [Minecraft Archipelago Randomizer Mod Releases Page](https://github.com/KonoTyran/Minecraft_AP_Randomizer/releases)
    - **DO NOT INSTALL THIS ON YOUR CLIENT**
- [Amazon Corretto](https://docs.aws.amazon.com/corretto/)
    - pick the matching version and select "Downloads" on the left

