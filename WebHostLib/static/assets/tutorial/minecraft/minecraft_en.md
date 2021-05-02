# Minecraft Randomizer Setup Guide

## Required Software

### Server Host
- [Minecraft Forge Dedicated Server](https://files.minecraftforge.net/net/minecraftforge/forge/index_1.16.5.html)
- [Minecraft Archipelago Randomizer Mod](https://github.com/KonoTyran/Minecraft_AP_Randomizer/releases)

### Players
- [Minecraft](https://www.minecraft.net/en-us/)

## Installation Procedures

### Dedicated Server Setup
Only one person has to do this setup and host a dedicated server for everyone else playing to connect to.
1. Download the 1.16.5 **Minecraft Forge** installer from the link above, making sure to download the most recent recommended version.

2. Run the `forge-1.16.5-xx.x.x-installer.jar` file and choose **install server**.
    - On this page you will also choose where to install the server to remember this directory its important in the next step.

3. Navigate to where you installed the server and open `forge-1.16.5-xx.x.x-installer.jar`
    - Upon first launch of the server it will close and ask you to accept Minecraft's EULA there should be a new file in that directory called `eula.txt` that contains a link to Minecraft's EULA and change a line that you need to change to `eula=true` in there to accept Minecraft's EULA
    - This will create the appropriate directories for you to place the file in the following step.

3. Place the `aprandomizer-x.x.x.jar` from the link above file into the `mods` folder of the above installation of your forge server.
    - Once again run the server, it will load up and generate the required directory `APData` for when you are ready to play a game!

### Basic Player Setup
- Purchace and Install Minecraft from the above link.
  **Your Done**.
  Players only need to have a Vanilla unmodified version of Minecraft to play!

### Advanced Player Setup
***This is not required to play a randomized minecraft game.***
however this recommended as it helps make the experience more enjoyable in the view of the developers.

#### Recomended Mods
- [JourneyMap](https://www.curseforge.com/minecraft/mc-mods/journeymap) (Minimap)


1. Install and run Minecraft from the link above at least once.
2. Run the `forge-1.16.5-xx.x.x-installer.jar` file and choose **install client**.
    - Start Minecraft forge at least once to create the directories needed for the next steps.
3. Navigate to your minecraft install directory and place desired mods `.jar` files the mods in the `mods` directory
    - The default install directories are as follows
        - Windows `%APPDATA%\.minecraft\mods`
        - macOS `~/Library/Application Support/minecraft\mods`
        - Linux `~/.minecraft\mods`

## Configuring your YAML file

### What is a YAML file and why do I need one?
Your YAML file contains a set of configuration options which provide the generator with information about how
it should generate your game. Each player of a multiworld will provide their own YAML file. This setup allows
each player to enjoy an experience customized for their taste, and different players in the same multiworld
can all have different options.

### Where do I get a YAML file?
A basic minecraft yaml will look like this.
```yaml
description: Template Name # Used to describe your yaml. Useful if you have multiple files
name: YourName # Your name in-game. Spaces will be replaced with underscores and there is a 16 character limit
#{player} will be replaced with the player's slot number.
#{PLAYER} will be replaced with the player's slot number if that slot number is greater than 1.
#{number} will be replaced with the counter value of the name.
#{NUMBER} will be replaced with the counter value of the name if the counter value is greater than 1.
game: Minecraft
# Shared Options supported by all games:
accessibility: locations
progression_balancing: off # we recommend turning this off for minecraft, as it has a much smaller pool of items, as well as many more logic skips that can be done than other games.
# Minecraft Specific Options
advancement_goal: # Number of advancements required (out of 92 total) to spawn the Ender Dragon and complete the game. 
  few: 0 # 30 advancements
  normal: 1 # 50
  many: 0 # 70
combat_difficulty: # Modifies the level of items logically required for exploring dangerous areas and fighting bosses. 
  easy: 0
  normal: 1
  hard: 0
include_hard_advancements: # Junk-fills certain RNG-reliant or tedious advancements with XP rewards. 
  on: 0
  off: 1
include_insane_advancements: # Junk-fills extremely difficult advancements; this is only How Did We Get Here? and Adventuring Time. 
  on: 0
  off: 1
include_postgame_advancements: # Some advancements require defeating the Ender Dragon; this will junk-fill them so you won't have to finish to send some items. 
  on: 0
  off: 1
shuffle_structures: # CURRENTLY DISABLED; enables shuffling of villages, outposts, fortresses, bastions, and end cities. 
  on: 0
  off: 1
```

## Joining a MultiWorld Game

### Obtain your Minecraft data file
**Only one yaml file needs to be submitted per minecraft world regardless of how many players play on it.**

When you join a multiworld game, you will be asked to provide your YAML file to whoever is hosting. Once that
is done, the host will provide you with either a link to download your data file, or with a zip file containing
everyone's data files. Your data file should have a `.apmc` extension.

Put your data file in your forge server `APData` folder. Make sure to remove any previous data file that was in
there all ready

### Connect to the MultiServer
After having placed your data file in the `APData` folder, start the Forge server and make sure you have OP
status by typing `/op YourMinecraftUsername` in the forge server console then connecting in your Minecraft client.

Once in game type `/connect <AP-Address> <Name> (<Password>)` where `<AP-Address>` is the address of the
Archipelago server and `<Name>` is the case-sensitive name that was in your YAML file. `(<Password>)`
is only required if the Archipleago server you are using has a password set.

### Play the game
When the console tells you that you have joined the room, you're ready to begin playing. Congratulations
on successfully joining a multiworld game! At this point any additional minecraft players may connect to your
forge server.

