# Mindustry Setup Guide

To generate a World(APworld), you will need to install the Mindustry World to your Archipelago folder. You can find the Mindustry World release here -> (https://github.com/JohnMahglass/Archipelago-Mindustry/releases)

# Table of Contents
1. [Introduction](#introduction)
2. [Changelog](#changelog)
3. [Installation](#setup)
4. [How to compile](#compile)

### What has been changed from the vanilla game? <a name="introduction" />

- Save data are separated from vanilla game so that playing Archipelago doesn't erase your vanilla saves. (You should still backup your saves as this is in developement)
- Most node from the research tree has been replaced with location checks.
- A "Victory" node has been added, researching this node will info~~~~rm Archipelago that the player has finished their World. If both planet are selected as a campaign, each victory nodes need to be researched to complete the goal.
- A new menu has been added in Settings to configure Archipelago's settings.
- You can use the chat to send messages to other client (If they support it).
- Use '/help' in the client to list all client commands.
- It is not possible to construct a fabricator if the associated unit has not been researched as well on Erekir planet.
- The research tree now shows every nodes. This change makes it easier to plan a route if you need to get a specific location.

## Version 0.4.1 changelog <a name="changelog" />
### Changes
- Reverted game version to the last official Mindustry release.
- Added new Conquest goal. This goal will require you to capture every **named** sector from the selected campaign.
- Reverted previous derelict change that was made in version 0.3.0.
- Added new "Progressive Drills" option.
- Added new "Progressive Generators" option.
- Added new "Faster Conveyor" option. @Antydon
- It is now possible to play multiple Mindustry multiworld on the same computer. To do so, simply copy/paste the client into **another directory**.
- Added 4 new abilities to the list of possible ability on Erekir for the "Randomize core units weapon" option.
- The `/options` command from the client chat will now only display relevant information for your selected yaml option. (ex: Death link mode will not be shown if death link is not enabled)
- Added `/options f` command to the client chat to display every option chosen in the yaml file.

### Fix
- Fixed multiple randomization logic bugs.
- Fixed AI on Erekir being 'frozen' on some sectors.
- Fixed a bug that would cause the death link signal to not be received until the player restarted their client.
- Fixed a bug where the event "Produce Slag on Serpulo" was being incorrectly triggered.


## Setup guide <a name="setup" />

### Windows
1. Download the latest release.
2. Extract the downloaded files in a directory.
3. Run `Mindustry-Archipelago.exe`
4. Go to Settings -> Archipelago and enter your game information to connect. (Or use the chat's client commands)
5. Have fun.


### Linux
1. Download the .jar file from the latest release.
2. Make sure you have Java JRE installed. You can install the Java 17 JRE using the terminal:\
   Ubuntu => `sudo apt install openjdk-17-jre`\
   Arch based => `sudo pacman -S jdk17-openjdk`
3. Open the terminal
4. Make sure you are in the directory containing `Mindustry-Archipelago.jar` (The file you downloaded from the release page.)
5. Run the game by typing `java -jar Mindustry-Archipelago.jar` in the terminal.
6. Go to Settings -> Archipelago and enter your game information to connect. (Or use the chat's client commands)
7. Have fun.


## Known bugs

- Sometimes when unlocking a research from a new category, the selectable block UI will not update until you exit the sector and enter again or receive another item.

### Report a bug.
You can report bugs that you find in the game's thread in the Archipelago Discord server, you
can find the Discord invite on the Archipelago website. You can find the game's thread by searching `Mindustry` in the "future-game-design" section.

## How to compile <a name="compile" />
If you would like to compile this code on your machine you can follow these instructions:
1. Create a directory for the project.
2. Open a terminal and clone this repo `git clone https://github.com/JohnMahglass/Mindustry-Archipelago-Randomizer.git`
3. Wait until the repo is done being downloaded.
4. In the same terminal, type `git clone https://github.com/JohnMahglass/mindustry-v146-arc`,
   this library is required for the project to compile.
5. Open the directory named `mindustry-v146-arc` there should be a single directory named `Arc`.
6. Move the `Arc` directory to be on the same level as your `Mindustry-Archipelago-Randomizer`
   directory. (The first one you cloned)
7. Delete the `mindustry-v146-arc` directory.
8. You should now have a directory with `Mindustry-Archipelago-Randomizer` and `Arc`
9. Open the `Mindustry-Archipelago-Randomizer` directory and open the terminal.
10. Type `gradlew desktop:run`
11. The project should compile and run!
