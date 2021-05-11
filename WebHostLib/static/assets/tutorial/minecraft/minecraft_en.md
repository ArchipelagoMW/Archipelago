# Minecraft Randomizer Setup Guide

## Required Software

### Server Host
- [Minecraft Forge](https://files.minecraftforge.net/net/minecraftforge/forge/index_1.16.5.html)
- [Minecraft Archipelago Randomizer Mod](https://github.com/KonoTyran/Minecraft_AP_Randomizer/releases)

### Players
- [Minecraft Java Edition](https://www.minecraft.net/en-us/store/minecraft-java-edition)

## Installation Procedures

### Dedicated Server Setup
Only one person has to do this setup and host a dedicated server for everyone else playing to connect to.
1. Download the 1.16.5 **Minecraft Forge** installer from the link above, making sure to download the most recent recommended version.

2. Run the `forge-1.16.5-xx.x.x-installer.jar` file and choose **install server**.
    - On this page you will also choose where to install the server to remember this directory it's important in the next step.

3. Navigate to where you installed the server and open `forge-1.16.5-xx.x.x.jar`
    - Upon first launch of the server it will close and ask you to accept Minecraft's EULA. There will be a new file called `eula.txt` that contains a link to Minecraft's EULA, and a line that you need to change to `eula=true` to accept Minecraft's EULA.
    - This will create the appropriate directories for you to place the files in the following step.

4. Place the `aprandomizer-x.x.x.jar` from the link above file into the `mods` folder of the above installation of your forge server.
    - Once again run the server, it will load up and generate the required directory `APData` for when you are ready to play a game!

### Basic Player Setup
- Purchase and install Minecraft from the above link.

  **You're Done**.
  
  Players only need to have a Vanilla unmodified version of Minecraft to play!

### Advanced Player Setup
***This is not required to play a randomized minecraft game.***
however this recommended as it helps make the experience more enjoyable.

#### Recomended Mods
- [JourneyMap](https://www.curseforge.com/minecraft/mc-mods/journeymap) (Minimap)


1. Install and run Minecraft from the link above at least once.
2. Run the `forge-1.16.5-xx.x.x-installer.jar` file and choose **install client**.
    - Start Minecraft forge at least once to create the directories needed for the next steps.
3. Navigate to your minecraft install directory and place desired mods `.jar` file the in the `mods` directory.
    - The default install directories are as follows.
        - Windows `%APPDATA%\.minecraft\mods`
        - macOS `~/Library/Application Support/minecraft/mods`
        - Linux `~/.minecraft/mods`

## Configuring your YAML file

### What is a YAML file and why do I need one?
Your YAML file contains a set of configuration options which provide the generator with information about how
it should generate your game. Each player of a multiworld will provide their own YAML file. This setup allows
each player to enjoy an experience customized for their taste, and different players in the same multiworld
can all have different options.

### Where do I get a YAML file?
A basic minecraft yaml will look like this.
```yaml
description: Template Name
# Your name in-game. Spaces will be replaced with underscores and
# there is a 16 character limit
name: YourName 
game: Minecraft

# Shared Options supported by all games:
accessibility: locations
progression_balancing: off
# Minecraft Specific Options

# Number of advancements required (out of 92 total) to spawn the
# Ender Dragon and complete the game. 
advancement_goal:
  few: 0 #30
  normal: 1 #50
  many: 0 #70
  
# Modifies the level of items logically required for exploring
# dangerous areas and fighting bosses. 
combat_difficulty:
  easy: 0
  normal: 1
  hard: 0
  
# Junk-fills certain RNG-reliant or tedious advancements with XP rewards. 
include_hard_advancements:
  on: 0
  off: 1
  
# Junk-fills extremely difficult advancements;
# this is only How Did We Get Here? and Adventuring Time.
include_insane_advancements:
  on: 0
  off: 1
  
# Some advancements require defeating the Ender Dragon;
# this will junk-fill them so you won't have to finish to send some items. 
include_postgame_advancements:
  on: 0
  off: 1
  
#enables shuffling of villages, outposts, fortresses, bastions, and end cities. 
shuffle_structures:
  on: 1
  off: 0
```

For more detail on what each setting does check the default `PlayerSettings.yaml` that comes with the Archipelago install.

## Joining a MultiWorld Game

### Obtain your Minecraft data file
**Only one yaml file needs to be submitted per minecraft world regardless of how many players play on it.**

When you join a multiworld game, you will be asked to provide your YAML file to whoever is hosting. Once that
is done, the host will provide you with either a link to download your data file, or with a zip file containing
everyone's data files. Your data file should have a `.apmc` extension.

Put your data file in your forge servers `APData` folder. Make sure to remove any previous data file that was in there
previously.

### Connect to the MultiServer
After having placed your data file in the `APData` folder, start the Forge server and make sure you have OP
status by typing `/op YourMinecraftUsername` in the forge server console then connecting in your Minecraft client.

Once in game type `/connect <AP-Address> (Port) (Password)` where `<AP-Address>` is the address of the
Archipelago server. `(Port)` is only required if the Archipelago server is not using the default port of 38281. `(Password)`
is only required if the Archipleago server you are using has a password set.

### Play the game
When the console tells you that you have joined the room, you're ready to begin playing. Congratulations
on successfully joining a multiworld game! At this point any additional minecraft players may connect to your
forge server.

