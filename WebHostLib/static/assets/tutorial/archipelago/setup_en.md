# Archipelago Setup Guide

## Installing the Archipelago software
The most recent public release of Archipelago can be found [here](https://github.com/ArchipelagoMW/Archipelago/releases).
Run the exe file, and after accepting the license agreement you will be prompted on which components you would like to install. 
The generator allows you to generate multiworld games on your computer. The ROM setups are optional but are required if 
anyone in the game that you generate wants to play any of those games as they are needed to generate the relevant patch 
files. The server will allow you to host the multiworld on your machine but this also requires you to port forward. The 
default port for Archipelago is `38281`. If you are unsure how to do this there are plenty of other guides on the internet 
that will be more suited to your hardware. The `Clients` are what you use to connect your game to the multiworld. If the 
game/games you plan to play are available here go ahead and install these as well. If the game you choose to play is 
supported by Archipelago but not listed in the installation check the relevant tutorial.

## Generating a game
### Gather all player YAMLS
All players that wish to play in the generated multiworld must have a YAML file which contains the settings that they wish to play with.
A YAML is a file which contains human readable markup. In other words, this is a settings file kind of like an INI file or a TOML file. 
Each player can go to the game's player settings page in order to determine the settings how they want them and then download a YAML file containing these settings.
After getting the YAML files of each participant for your multiworld game, these can all either be placed together in the 
`Archipelago\Players` folder or compressed into a ZIP folder to then be uploaded to the [website generator](/generate).
If rolling locally ensure that the folder is clear of any files you do not wish to include in the game such as the 
included default player settings files.

#### Changing local host settings for generation
Sometimes there are various settings that you may want to change before rolling a seed such as enabling race mode, 
auto-forfeit, plando support, or setting a password. All of these settings plus other options are able to be changed by 
modifying the `host.yaml` file in the base `Archipelago` folder. The settings chosen here are baked into
the serverdata file that gets output with the other files after generation so if rolling locally ensure this file is edited
to your liking *before* rolling the seed.

### Rolling the seed

#### On the Website
After gathering the YAML files together in one location, select all of the files and compress them into a .zip folder. 
Next go to the [Start Playing](/start-playing) page and click on `generate a randomized game` to reach the website generator. 
Here, you can adjust some server settings such as forfeit rules and the cost for a player to use a hint before generation. 
After adjusting the host settings to your liking click on the Upload File button and using the explorer window that opens, 
navigate to the location where you zipped the player files and upload this zip. The page will generate your game and refresh
multiple times to check on completion status. After the generation completes you will be on a Seed Info page that provides
the seed, the date/time of creation, a link to the spoiler log, if available, and links to any rooms created from this seed.
To begin playing, click on `Create New Room`, which will take you to the room page. From here you can navigate back to thse
Seed Info page or to the Tracker page. Sharing the link to this page with your friends will provide them with the
necessary info and files for them to connect to the multiworld.

#### Rolling using the generation program
After gathering the YAML files together in the `Archipelago\Players` folder, run the program `ArchipelagoGenerate.exe` 
in the base `Archipelago` folder. This will then open a console window and either silently close itself or spit out an 
error. If you receive an error, it is likely due to an error in the YAML file. If the error is unhelpful in figuring 
out the issue asking in the ***#tech-support*** channel of our Discord for help with finding it is highly recommended. 
The generator will put a zip folder into your `Archipelago\output` folder with the format `AP_XXXXXXXXX`.zip. 
This contains the patch files and relevant mods for the players as well as the serverdata for the host.

## Hosting a multiworld
### Uploading the seed to the website
The easiest and most recommended method is to generate the game on the website which will allow you to create a private
room with all the necessary files you can share, as well as hosting the game and supporting item trackers for various games. 
If for some reason the seed was rolled on a machine then either the resulting zip file or the resulting `AP_XXXXX.archipelago`
inside the zip file can be uploaded to the [upload page](/uploads). This will give a page with the seed info and have a 
link to the spoiler if it exists. Click on Create New room and then share the link for the room with the other players 
so that they can download their patches or mods. The room will also have a link to a Multiworld Tracker and tell you 
what the players need to connect to from their clients. 

### Hosting a seed locally
For this we'll assume you have already port forwarding `38281` and have generated a seed that is still in the `outputs` 
folder. Next, you'll want to run `ArchipelagoServer.exe`. A window will open in order to open the multiworld data for the 
game. You can either use the generated zip folder or extract the .archipelago file and use it. If everything worked correctly the console window should tell you it's now hosting a game with the IP, port, and password that clients will need in order to connect.
Extract the patch and mod files then send those to your friends, and you're done!
