# Archipelago Setup Guide

This guide is intended to provide an overview of how to:
- Install, set up, and run the Archipelago multiworld software
- Generate and host multiworlds
- Connect to the multiworld after hosting has begun

This is a general overview. For more specific steps, reference the relevant game's [setup guide](/tutorial).

Some steps also assume use of Windows, so may vary with your OS.

## Installing the Archipelago software

The most recent public release of Archipelago can be found on the GitHub Releases page:
[Archipelago Releases Page](https://github.com/ArchipelagoMW/Archipelago/releases).

Run the exe file, and after accepting the license agreement you will be asked which components you would like to
install.

The generator allows you to generate multiworld games on your computer. The ROM setups are required if anyone in the
game that you generate wants to play any of those games as they are needed to generate the relevant patch files. If you
do not own the game, uncheck the relevant box. If you gain the game later, the installer can be run again to install and
set up new components.

The server will allow you to host the multiworld on your machine. Hosting on your machine requires forwarding the port
you are hosting on. The default port for Archipelago is `38281`. If you are unsure how to do this there are plenty of
other guides on the internet that will be more suited to your hardware.

The `Clients` are what are used to connect your game to the multiworld. If the game you plan to play is available
here, go ahead and install its client as well. If the game you choose to play is supported by Archipelago but not listed
in the installation, check the setup guide for that game. Installing a client for a ROM based game requires you to have
a legally obtained ROM for that game as well.

## Generating a game

### What is a YAML?

YAML is the file format which Archipelago uses in order to configure a player's world. It allows you to dictate which
game you will be playing as well as the settings you would like for that game.

YAML is a format very similar to JSON however it is made to be more human-readable. If you are ever unsure of the
validity of your YAML file you may check the file by uploading it to the check page on the Archipelago website:
[YAML Validation Page](/check)

### Creating a YAML

YAML files may be generated on the Archipelago website by visiting the [games page](/games) and clicking the
"Settings Page" link under the relevant game. Clicking "Export Settings" in a game's settings page will download the
YAML to your system.

Alternatively, you can run `ArchipelagoLauncher.exe` and click on `Generate Template Settings` to create a set of template 
YAMLs for each game in your Archipelago install (including for APWorlds). These will be placed in your `Players/Templates` folder.

In a multiworld there must be one YAML per world. Any number of players can play on each world using either the game's
native coop system or using Archipelago's coop support. Each world will hold one slot in the multiworld and will have a
slot name and, if the relevant game requires it, files to associate it with that multiworld.

If multiple people plan to play in one world cooperatively then they will only need one YAML for their coop world. If
each player is planning on playing their own game then they will each need a YAML.

### Generating a single player game

#### On the website

The easiest way to get started playing an Archipelago generated game, after following the base setup from the game's
setup guide, is to find the game on the [Archipelago Games List](/games), click on `Settings Page`, set the settings for
how you want to play, and click `Generate Game` at the bottom of the page. This will create a page for the seed, from
which you can create a room, and then [connect](#connecting-to-an-archipelago-server).

If you have downloaded the settings, or have created a settings file manually, this file can be uploaded on the
[Generation Page](/generate) where you can also set any specific hosting settings.

#### On your local installation

To generate a game on your local machine, make sure to install the Archipelago software, and ensure to select the
`Generator` component, as well as the `ROM setup` for any games you will want to play. Navigate to your Archipelago
installation (usually C:\ProgramData\Archipelago), and place the settings file you have either created or downloaded
from the website in the `Players` folder.

Run `ArchipelagoGenerate.exe`, and it will inform you whether the generation was successful or not. If successful, there
will be an output zip in the `output` folder (usually named something like `AP_XXXXX.zip`). This will contain all
relevant information to the session, including the spoiler log, if one was generated.

### Generating a multiplayer game

Archipelago is a multi-game multiworld architecture, so any number of players and any number of games may be used to
generate. Of note, the website currently has a maximum generated player count of 30. If you would like to generate a game
larger than that, it must be done on a local installation. Generally, it is better to generate locally to free server
resources, and host the resulting multiworld on the website.

#### Gather All Player YAMLs

All players that wish to play in the generated multiworld must have a YAML file which contains the settings that they
wish to play with. One person should gather all files from all participants in the generated multiworld. It is possible
for a single player to have multiple games, or even multiple slots of a single game, but each YAML must have a unique
player name.

#### On the website

Gather all player YAML files into a single place, and compress them into a zip file. This can be done by pressing
ctrl/cmd + clicking on each file until all are selected, right-clicking one of the files, and clicking
`compress to ZIP file` or `send to > compressed folder`.

Navigate to the [Generate Page](/generate), select the host settings you would like, click on `Upload File`, and
select the newly created zip from the opened window.

After some time, you will be redirected to a seed info page that will display the generated seed, the time it was
created, the number of players, the spoiler (if one was created) and all rooms created from this seed.


#### On your local installation

It is possible to generate the multiworld locally, using a local Archipelago installation. This is done by entering the
Archipelago installation folder (usually C:\ProgramData\Archipelago) and placing each YAML file in the `Players` folder.
If the folder does not exist then it must be created manually. The files here should not be compressed.

After filling the `Players` folder, the `ArchipelagoGenerate.exe` program should be run in order to generate a
multiworld. The output of this process is placed in the `output` folder (usually named something like `AP_XXXXX.zip`).

##### Changing local host settings for generation

Sometimes there are various settings that you may want to change before rolling a seed such as enabling race mode,
auto-release, plando support, or setting a password.

All of these settings, plus other options, may be changed by modifying the `host.yaml` file in the Archipelago
installation folder. The settings chosen here are baked into the `.archipelago` file that gets output with the other
files after generation, so if you are rolling locally, ensure this file is edited to your liking **before** rolling the
seed. This file is overwritten when running the Archipelago Installation software. If you have changed settings in this
file, and would like to retain them, you may rename the file to `options.yaml`.

## Hosting an Archipelago Server

When a multiworld seed is generated, the multidata will be output as a `.archipelago`. If the game was generated locally,
a compressed folder will be in `/output` and will contain the `.archipelago`, the spoiler log, and any relevant files
for the generated games.

### Hosting on the website

After a seed page has been created on the website, clicking on `Create Room` will create a new server instance, and a
page that can be linked to the other players, so they can all see the connection info, obtain their data files, and
connect to the multiworld. Simply click on the url in the title bar, copy the link, and send it to your friends. Room
servers will shut down after 2 hours of inactivity, saving the multiworld progress. By returning to the room page, the
room server can be started back up, and the multiworld can continue to be played. If the link to the room is lost, the
creator of the room can find it on their [User Content Page](/user-content). The person who created the room becomes the
"owner" of the room, and as such has access to the server console. Clearing cookies will remove access to this console,
and there is no way to regain it. If a server password was set when generating the multiworld game, server admin
privileges may be gained by entering `!admin <password>` from the `ArchipelagoTextClient.exe`.

#### The room page

![Screenshot of Room Page](/static/generated/docs/Archipelago/example_room.png)
1. Server/Host Name
2. Port
3. Slot Name
4. Download link for data files
5. Link to tracker page for this player

#### From a website generated game

After generating a game on the website, you will be redirected to the seed page. To begin playing click on `Create Room`
to create a new room page and server for your game.

#### From a locally generated game

After generating a game, a compressed folder will be output to the `/output` folder. Go to the
[Archipelago Host Game Page](/uploads), click on `Upload File`, navigate to your Archipelago installation, and select
the generated folder. This will create a new seed page using the information from this folder.

### Hosting on a local machine

The `.archipelago` file may be extracted from the compressed file. Double-clicking the file will then open
`ArchipelagoServer.exe` in order to host the multiworld on the local machine. Alternatively, running
`ArchipelagoServer.exe` and pointing the resulting file selection prompt to the `.archipelago` file or the generated
compressed folder will begin hosting.

## Connecting to an Archipelago Server

The actual method of connection will vary depending on the game, so follow that game's setup guide, but all games will
use the same general connection info noted here.

### Connection Info

For connecting from the game to the server, the connection info is needed for any of the game clients. Games that use
data files will usually contain the connection info within these files, when hosted on the Archipelago website. If the
information needs to be entered manually, it is usually comprised of four different sections.

* `Server`, `Server Name` or `Host Name` are all used interchangeably as the domain or IP address of the server. If the
game is being hosted on the main Archipelago website this will be `archipelago.gg`. If the game is being hosted on your
own local machine `localhost` will work. If the game is being hosted on another person's computer then you enter that
person's public IP address.
* `Port` is which port on the domain or IP address the game is being hosted on. On the website room pages, this is
displayed as `archipelago.gg:<port>`. Most clients will accept that information being entered directly as is. If the
information needs to be entered separately, then the port is the sequence of numbers after the `:`, and the `:` does
not need to be entered. If a game is being hosted from the `ArchipelagoServer.exe`, this will default to `38281` but may
be changed in the `host.yaml`.
* `Slot Name` is the name of your player slot that you are connecting to. This is the same as the name that was set
when creating your [YAML file](#creating-a-yaml). If the game is hosted on the website, this is also displayed on the
room page. The name is case-sensitive.
* `Password` is the password set by the host in order to join the multiworld. By default, this will be empty and is almost
never required, but one can be set when generating the game. Generally, leave this field blank when it exists,
unless you know that a password was set, and what that password is.