# Archipelago Setup Guide

## Installing the Archipelago software
The most recent public release of Archipelago can be found [here](https://github.com/ArchipelagoMW/Archipelago/releases).
Run the exe file, and after accepting the license agreement you will be prompted on which components you would like to install. The generator allows you to generate multiworld games on your computer. The ROM setups are optional but are required if anyone in the game that you generate wants to play any of those games as they are needed to generate the relevant patch files. The server will allow you to host the multiworld on your machine but this also requires you to port forward. The default port for Archipelago is `38281` If you are unsure how to do this there are plenty of other guides on the internet that will be more suited to your hardware. The Clients are what you use to connect your game to the multiworld. If the game/games you plan to play are available here go ahead and install these as well. If the game you choose to play is supported by Archipelago but not listed check the relevant tutorial.

## Generating a game
### Gather all player YAMLS
All players that wish to play in the generated multiworld must have a YAML file which contains all of the settings that they wish to play with.
A YAML is a file which contains human readable markup. In other words, this is a settings file kind of like an INI file or a TOML file. 
Each player can go to the game's player settings page in order to determine the settings how they want them and then download a YAML file containing these settings.
After getting all of the YAML files these can all either be placed together in the `Archipelago\Players` folder or compressed into a ZIP folder to then be uploaded to the [website generator](/generate).
If rolling locally ensure that the folder is clear of any files you do not wish to include in the game such as the included default player settings files.

### Rolling the seed
After gathering all of the YAML files together in the `Archipelago\Players` folder, run the program `ArchipelagoGenerate.exe` in the base `Archipelago` folder. This will then open a console window and either silently close itself or spit out an error. If you receive an error, it is likely due to an error in the YAML file. If the error is unhelpful in you figuring out the issue asking in the ***#tech-support*** channel of our Discord. The generator will put a zip folder into your `Archipelago\output` folder with the format `AP_XXXXXXXXX`.zip. This contains all of the patch files and relevant mods for the players as well as the serverdata for the host.

### Changing host settings
Sometimes there are various settings that you may want to change before rolling a seed such as enabling race mode, auto-forfeit, or set a password. All of these settings plus other options are able to be changed by modifying the `host.yaml` file in the base `Archipelago` folder. 

## Hosting a multiworld
### Uploading the seed to the website
The easiest and most recommended method is to upload the zip file that you generated to the website [here](/uploads). This will give a page with the seed info and have a link to the spoiler if it exists. Click on Create New room and then share the link fo rhe room with the other players so that they can download their patches or mods. The room will also have a link to a Multiworld Tracker and tell you what the players need to connect to from their clients. 

### Hosting a seed locally
For this we'll assume you have already port forwarding `38281` and have generated a seed that is still in the `outputs` folder. Next, you'll want to run `ArchipelagoServer.exe`. A window will open in order to open the multiworld data for the game. You can either use the generated zip folder or extract the .archipelago file and use it. If everything worked correctly the console window should tell you it's now hosting a game with the IP, port, and password that clients will need in order to connect.
Extract the patch and mod files then send those to your friends and you're done!
