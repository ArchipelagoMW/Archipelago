# Minecraft Randomizer Setup Guide

#Automatic Hosting Install
- Download and install Archipelago at: [https://github.com/ArchipelagoMW/Archipelago/releases](https://github.com/ArchipelagoMW/Archipelago/releases) 
  - Choose the `Minecraft Client` module during the installation.

## Required Software

- Minecraft Java Edition from: [https://www.minecraft.net/en-us/store/minecraft-java-edition](https://www.minecraft.net/en-us/store/minecraft-java-edition)

## Configuring your YAML file

### What is a YAML file and why do I need one?
See the guide on setting up a basic YAML at the Archipelago setup guide: [click here](/tutorial/archipelago/setup/en)

### What Does a YAML Look Like for Minecraft?
A basic minecraft yaml will look like this.
```yaml
description: Basic Minecraft Yaml
# Your name in-game. Spaces will be replaced with underscores and
# there is a 16 character limit
name: YourName
game: Minecraft

# Shared Options supported by all games:
accessibility: locations
progression_balancing: on
# Minecraft Specific Options

Minecraft:
  # Number of advancements required (87 max) to spawn the Ender Dragon and complete the game.
  advancement_goal: 50   
  
  # Number of dragon egg shards to collect (30 max) before the Ender Dragon will spawn. 
  egg_shards_required: 10 
  
  # Number of egg shards available in the pool (30 max).
  egg_shards_available: 15 
  
  # Modifies the level of items logically required for
  # exploring dangerous areas and fighting bosses.
  combat_difficulty: 
    easy: 0
    normal: 1
    hard: 0
    
  # Junk-fills certain RNG-reliant or tedious advancements.
  include_hard_advancements: 
    on: 0
    off: 1
    
  # Junk-fills extremely difficult advancements;
  # this is only How Did We Get Here? and Adventuring Time.
  include_insane_advancements: 
    on: 0
    off: 1
  
  # Some advancements require defeating the Ender Dragon;
  # this will junk-fill them, so you won't have to finish them to send some items.  
  include_postgame_advancements: 
    on: 0
    off: 1
    
  # Enables shuffling of villages, outposts, fortresses, bastions, and end cities. 
  shuffle_structures: 
    on: 0
    off: 1
  
  # Adds structure compasses to the item pool,
  # which point to the nearest indicated structure.  
  structure_compasses: 
    on: 0
    off: 1
  
  # Replaces a percentage of junk items with bee traps
  # which spawn multiple angered bees around every player when received.   
  bee_traps: 
    0: 1
    25: 0
    50: 0
    75: 0
    100: 0
```

## Joining a MultiWorld Game

### Obtain Your Minecraft Data File
**Only one yaml file needs to be submitted per minecraft world regardless of how many players play on it.**

When you join a multiworld game, you will be asked to provide your YAML file to whoever is hosting. Once that is done, the host will provide you with either a link to download your data file, or with a zip file containing everyone's data files. Your data file should have a `.apmc` extension.

Double-click on your `.apmc` file to have the minecraft client auto-launch the installed forge server.

### Connect to the MultiServer
If you are running Forge manually, you must place the `.apmc` file in your `APData` folder in the Forge installation directory. If the `APData` folder does not exist then you may create it. After having placed your data file in the `APData` folder, start the Forge server and make sure you have OP status by typing `/op YourMinecraftUsername` in the forge server console then connecting in your Minecraft client.

In all cases, no matter how the Forge server is hosted: once you are in game type `/connect <AP-Address> (Port) (Password)` where `<AP-Address>` is the address of the Archipelago server. `(Port)` is only required if the Archipelago server is not using the default port of 38281. `(Password)` is only required if the Archipelago server you are using has a password set.

### Play the game
When the console tells you that you have joined the room, you're ready to begin playing. Congratulations on successfully joining a multiworld game! At this point any additional minecraft players may connect to your forge server. When you are ready to start the game use the `/start` command within the Minecraft game.


## Manual Installation Procedures
This is only required if you wish to set up a forge install yourself, it's recommended to just use the Archipelago Installer.

###Required Software
- Minecraft Forge from: [https://files.minecraftforge.net/net/minecraftforge/forge/index_1.16.5.html](https://files.minecraftforge.net/net/minecraftforge/forge/index_1.16.5.html)
- Minecraft Archipelago Randomizer Mod from: [https://github.com/KonoTyran/Minecraft_AP_Randomizer/releases](https://github.com/KonoTyran/Minecraft_AP_Randomizer/releases)
  - **DO NOT INSTALL THIS ON YOUR CLIENT**
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
