# Super Mario 64 EX MultiWorld Setup Guide

## Required Software

- Super Mario 64 US Rom (Japanese may work also. Europe and Shindou not supported)
- Either of [sm64pclauncher](https://github.com/N00byKing/sm64pclauncher/releases) or
- Cloning and building [sm64ex](https://github.com/N00byKing/sm64ex) manually.

NOTE: The above linked sm64pclauncher is a special version designed to work with the Archipelago build of sm64ex.
You can use other sm64-port based builds with it, but you can't use a different launcher with the Archipelago build of sm64ex.

## Installation and Game Start Procedures

# Installation via sm64pclauncher (For Windows)

First, install [MSYS](https://www.msys2.org/) as described on the page. DO NOT INSTALL INTO A FOLDER PATH WITH SPACES.
Do all steps up to including step 6.
Best use default install directory.
Then follow the steps below

1. Go to the page linked for sm64pclauncher, and press on the topmost entry
3. Scroll down, and download the zip file
4. Unpack the zip file in an empty folder
5. Run the Launcher and press build.
6. Set the location where you installed MSYS when prompted. Check the "Install Dependencies" Checkbox
7. Set the Repo link to `https://github.com/N00byKing/sm64ex` and the Branch to `archipelago` (Top two boxes). You can choose the folder (Secound Box) at will, as long as it does not exist yet
8. Point the Launcher to your Super Mario 64 US/JP Rom, and set the Region correspondingly
9. Set Build Options. Recommended: `-jn` where `n` is the Number of CPU Cores, to build faster.
10. SM64EX will now be compiled. The Launcher will appear to have crashed, but this is not likely the case. Best wait a bit, but there may be a problem if it takes longer than 10 Minutes

After it's done, the Build list should have another entry titled with what you named the folder in step 7.

NOTE: For some reason first start of the game always crashes the launcher. Just restart it.
If it still crashes, recheck if you typed the launch options correctly (Described in "Joining a MultiWorld Game")

# Manual Compilation (Linux/Windows)

Dependencies for Linux: `sdl2 glew cmake python make`.
Dependencies for Windows: `mingw-w64-x86_64-gcc mingw-w64-x86_64-glew mingw-w64-x86_64-SDL2 git make python3 mingw-w64-x86_64-cmake`
SM64EX will link `jsoncpp` dynamic if installed. If not, it will compile and link statically.

1. Clone `https://github.com/N00byKing/sm64ex` recursively
2. Enter `sm64ex` and copy your Rom to `baserom.REGION.z64` where `REGION` is either `us` or `jp` respectively.
3. Compile with `make`. For faster compilation set the parameter `-jn` where `n` is the Number of CPU Cores.

The Compiled binary will be in `build/REGION_pc/`.

# Joining a MultiWorld Game

To join, set the following launch options: `--sm64ap_name YourName --sm64ap_ip ServerIP:Port`.
Optionally, add `--sm64ap_passwd "YourPassword"` if the room you are using requires a password.
The Name in this case is the one specified in your generated .yaml file.
In case you are using the Archipelago Website, the IP should be `archipelago.gg`.

If everything worked out, you will see a textbox informing you the connection has been established after the story intro.

# Playing offline

To play offline, first generate a seed on the game's settings page.
Create a room and download the `.apsm64ex` file, and start the game with the `--sm64ap_file "path/to/FileName"` launch argument.

## Installation Troubleshooting

Start the game from the command line to view helpful messages regarding SM64EX.

### Game doesn't start after compiling

Most likely you forgot to set the launch options. `--sm64ap_name YourName` and `--sm64ap_ip ServerIP:Port` are required for startup for Multiworlds, and
`--sm64ap_file FileName` is required for (offline) singleplayer.
If your Name or Password have spaces in them, surround them in quotes.

### Game crashes upon entering Peach's Castle

This happens when the game is missing the relevant randomizer data. If you are trying to connect to a server, verify the
information entered is correct, and for a local file ensure you are using the full file path to the file in conjunction
with its name.

## Game Troubleshooting

### Known Issues

When using a US Rom, the In-Game messages are missing some letters: `J Q V X Z` and `?`.
The Japanese Version should have no problem displaying these.

### What happens if I lose connection?

SM64EX tries to reconnect a few times, so be patient.
Should the problem still be there after about a minute or two, just save and restart the game.

### How do I update the Game to a new Build?

When manually compiling just pull in changes and run `make` again. Sometimes it helps to run `make clean` before.

When using the Launcher follow the normal build steps, but when choosing a folder name use the same as before. Then continue as normal.
