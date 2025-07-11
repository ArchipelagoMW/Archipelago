# Scooby Doo: Night of 100 Frights Setup Guide

## Required Software

- [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases) v0.5.1 or higher. Make sure to install the Generator.
- [This AP world](https://github.com/vgm5/Night_Of_100_Frights_ap_world/releases)
- Microsoft .NET Framework 4.8 or higher
- [Dolphin](https://dolphin-emu.org/download/)
- Your US Version of Night of 100 Frights Revision 0 (The original 1.0 release), probably named ``Scooby-Doo! Night of 100 Frights.iso``.

## Installation Procedures

- Place ``no100f.apworld`` in ``custom_worlds/`` of your AP installation.
- Place the included ``.pyd`` files and the ``dolphin_memory_engine`` folder into ``lib/`` of your AP installation. (Depending on your version of AP this might be different depending on which version of python is being used, the default file in the dolphin_memory_engine folder should be the correct one for the current release of AP, the other files are for backwards compatibility for any user using a non python 3.12 setup)
- Place the Uncompressed ISO in the root folder of your AP installation and make sure it's named ``Scooby-Doo! Night of 100 Frights.iso``.  (Using an invalid version of the game [Rev1 or Compressed .ciso] will likely result in the necessary game patches breaking)

Note: If you have previously setup the Wind Waker AP and you get exceptions relation to the Dolphine Memory Engine/DME .pyd files you may need to just clear the entire folder and just use the .pyds included with this release.

For more information about .apworlds
see [here](https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/apworld%20specification.md)

## Create a Config (.yaml) File

### What is a config file and why do I need one?

See the guide on setting up a basic YAML at the Archipelago setup
guide: [Basic Multiworld Setup Guide](https://archipelago.gg/tutorial/Archipelago/setup/en)

### Where do I get a config file?

A default yaml is included in the download. Alternative you can use the Web Host when running from source.

### Verifying your config file

If you would like to validate your config file to make sure it works, you may do so on the YAML Validator page. YAML
validator page: [YAML Validation page](https://archipelago.gg/mysterycheck)

## Joining a MultiWorld Game

Start ``ArchipelagoLauncher.exe`` and choose ``NO100F Client``. You will be asked to provide a ``.apno100f`` patch file so
choose your patch file. The client will then open, patch and attempt to open the resulting ``.gcm`` ISO file. Patching
can take a while and the client will become unresponsive while patching. You can also select a ``.gcm`` directly to just
open it without patching or just click cancel, if you don't want to patch or open any ISO.

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
