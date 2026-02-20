# Scooby Doo: Night of 100 Frights Setup Guide

## Required Software

- [Dolphin](https://dolphin-emu.org/download/)
- Your US Version of Night of 100 Frights Revision 0 (The original 1.0 release), probably named ``Scooby-Doo! Night of 100 Frights.iso``.

## Create a Config (.yaml) File

### What is a config file and why do I need one?

YAML Files will tell the generator what your player name is, what game you're playing, and what different options you want to use.

YAML Files for NO100F can be found and generated on this page: [Scooby-Doo! Night of 100 Frights Options Page](/games/Scooby-Doo!%20Night%20of%20100%20Frights/player-options)

## Joining a MultiWorld Game

First and foremost, your Night of 100 Frights ISO must be placed at the root of your Archipelago installation

The multiworld host will provide you a link to download your apno100f file or a zip file containing everyone's files. The
apno100f file should be named `AP_XXXXX_P#_<name>_.apno100f`, where `#` is your player ID, `<name>` is your player name, and
`XXXXX` is the room ID. The host should also provide you with the room's server name and port number - and potentially a password if the host has set one.

Start ``ArchipelagoLauncher.exe`` and choose ``NO100F Client``. You will be asked to provide a ``.apno100f`` patch file. 
Once you have selected one the client will then open, and attempt to create a .gcm based on the provided patch file, and then open the resulting ``.gcm`` ISO file. Patching
can take a while and the client will become unresponsive while patching. 

If you already generated the ``.gcm`` file on a previous run of the ``NO100F Client`` then you can opt to not select a file,
the client will begin running as normal and you will just need to manually open the ``.gcm`` in Dolphin

### Connect to the Client

#### With Dolphin

The Client will automatically try to connect to Dolphin every 5 seconds and will do so if NO100F is running - a successful connection is **only** possible after starting a new game and exiting the Intro Cutscene. If this
doesn't work try restarting Dolphin and make sure you only have one instance running of Dolphin. If you still get the
invalid game error message when using the 1.0 US Version make sure that ``Emulated Memory Size Override`` (
under ``Settings`` > ``Advanced``) is disabled.

### Connect to the Archipelago Server

If the client window shows "Server Status: Not Connected", simply ask the host for the address of the server, and
copy/paste it into the "Server" input field then press enter.

The client will attempt to reconnect to the new server address, and should momentarily show "Server Status: Connected".

## Hosting a MultiWorld game

The recommended way to host a game is to use the Archipelago hosting service. The process is relatively simple:

1. Collect config files from your players.
2. Place the config files in the ``Players`` folder in your Archipelago install
3. Run ``ArchipelagoGenerate.exe`` and location the resulting zip in the ``output`` folder
4. Upload that zip file to the Host Game page.
    - Generate page: [WebHost Host Game Page](https://archipelago.gg/uploads)
5. Click "Create New Room". This will take you to the server page. Provide the link to this page to your players, so
   they may download their patch files from there.
6. Note that a link to a MultiWorld Tracker is at the top of the room page. The tracker shows the progress of all
   players in the game. Any observers may also be given the link to this page.
7. Once all players have joined, you may begin playing.
